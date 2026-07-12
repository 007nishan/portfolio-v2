#!/bin/bash
# ==============================================================================
# setup_auto_deploy.sh  —  ONE-TIME setup for GitHub -> server auto-deploy
# ==============================================================================
# Run this ONCE on the server (192.168.1.150, user nishan). It:
#   1. Ensures ~/portfolio is a git checkout of the GitHub repo tracking main
#   2. Installs a systemd timer that runs auto_deploy.sh every minute
#   3. Allows the timer to restart the portfolio service without a password
#
# After this, every `git push` to origin/main goes live on the server within
# ~1 minute — no manual SSH, no open ports, no passwords in the repo.
#
# Prerequisite: run this while OFF the corporate VPN if the server is on your
# home LAN. Requires sudo on the server.
# ==============================================================================

set -euo pipefail

PORTFOLIO_DIR="${PORTFOLIO_DIR:-/home/nishan/portfolio}"
REPO_URL="${REPO_URL:-https://github.com/007nishan/portfolio-v2.git}"
BRANCH="${DEPLOY_BRANCH:-main}"
USER_NAME="$(whoami)"

echo "=== Portfolio Auto-Deploy Setup ==="
echo "Dir:    $PORTFOLIO_DIR"
echo "Repo:   $REPO_URL ($BRANCH)"
echo ""

# ──────────────────────────────────────────────────────────────────────────────
# 1. Make ~/portfolio a git checkout of the repo (preserving data/ & venv/)
# ──────────────────────────────────────────────────────────────────────────────
if [ -d "$PORTFOLIO_DIR/.git" ]; then
    echo "[1/3] Git repo already initialized in $PORTFOLIO_DIR."
    cd "$PORTFOLIO_DIR"
    git remote set-url origin "$REPO_URL" 2>/dev/null || git remote add origin "$REPO_URL"
else
    echo "[1/3] Initializing git in existing $PORTFOLIO_DIR (keeping data/, venv/, .env)..."
    cd "$PORTFOLIO_DIR"
    # Safety: back up any file that GitHub also tracks, in case a server-side
    # edit diverged from the repo (e.g. hand-patched app.py/templates).
    BACKUP="$PORTFOLIO_DIR/pre_autodeploy_backup_$(date +%s)"
    git init -q
    git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
    git fetch --quiet origin "$BRANCH"
    mkdir -p "$BACKUP"
    # For every path the repo tracks, if it already exists locally, stash a copy.
    while IFS= read -r f; do
        if [ -f "$f" ]; then
            mkdir -p "$BACKUP/$(dirname "$f")"
            cp -p "$f" "$BACKUP/$f" 2>/dev/null || true
        fi
    done < <(git ls-tree -r --name-only "origin/$BRANCH")
    echo "  ✓ Backed up existing tracked files to: $BACKUP"
    # Adopt the remote branch. `reset --hard` (NOT checkout) is conflict-proof:
    # it overwrites tracked files to the repo version and leaves untracked files
    # (data/, venv/, .env, admin_id.txt, claw_config.json) completely alone.
    # checkout would abort here because the server's existing app.py/templates
    # collide with the incoming tree; reset does not.
    git reset --hard "origin/$BRANCH"
    git branch -M "$BRANCH"
    git branch --set-upstream-to="origin/$BRANCH" "$BRANCH" 2>/dev/null || true
fi
echo "  ✓ Now at $(git rev-parse --short HEAD): $(git log -1 --pretty=%s)"

chmod +x "$PORTFOLIO_DIR/auto_deploy.sh" 2>/dev/null || true

# ──────────────────────────────────────────────────────────────────────────────
# 2. Allow the deploy script to restart the service without a password prompt
#    (scoped to ONLY the restart command — not blanket NOPASSWD)
# ──────────────────────────────────────────────────────────────────────────────
echo "[2/3] Granting scoped sudo for service restart..."
SUDO_RULE="$USER_NAME ALL=(ALL) NOPASSWD: /bin/systemctl restart portfolio, /usr/bin/systemctl restart portfolio"
echo "$SUDO_RULE" | sudo tee /etc/sudoers.d/91-portfolio-deploy > /dev/null
sudo chmod 0440 /etc/sudoers.d/91-portfolio-deploy
echo "  ✓ Scoped sudo rule installed (restart portfolio only)."

# ──────────────────────────────────────────────────────────────────────────────
# 3. systemd service + timer to run auto_deploy.sh every minute
# ──────────────────────────────────────────────────────────────────────────────
echo "[3/3] Installing systemd timer (checks GitHub every 60s)..."

sudo tee /etc/systemd/system/portfolio-deploy.service > /dev/null << EOF
[Unit]
Description=Portfolio GitHub Auto-Deploy (pull + restart)
After=network-online.target

[Service]
Type=oneshot
User=$USER_NAME
WorkingDirectory=$PORTFOLIO_DIR
ExecStart=/bin/bash $PORTFOLIO_DIR/auto_deploy.sh
EOF

sudo tee /etc/systemd/system/portfolio-deploy.timer > /dev/null << EOF
[Unit]
Description=Run Portfolio Auto-Deploy every minute

[Timer]
OnBootSec=60
OnUnitActiveSec=60
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now portfolio-deploy.timer
echo "  ✓ Timer active."

# ──────────────────────────────────────────────────────────────────────────────
# 4. Restart the app NOW so the just-pulled code (calendar fix etc.) goes live
#    immediately — without this, the running Flask process keeps serving the old
#    Jinja-cached templates until the next restart.
# ──────────────────────────────────────────────────────────────────────────────
echo "[4/4] Restarting the app so the new code is live now..."
chmod +x "$PORTFOLIO_DIR/auto_deploy.sh" 2>/dev/null || true
if command -v systemctl >/dev/null 2>&1 && systemctl list-unit-files 2>/dev/null | grep -q "^portfolio.service"; then
    sudo systemctl restart portfolio && echo "  ✓ Restarted systemd service 'portfolio'."
else
    pkill -f "python app.py" 2>/dev/null || true
    ( cd "$PORTFOLIO_DIR" && source venv/bin/activate 2>/dev/null; nohup python app.py > /tmp/portfolio.log 2>&1 & )
    echo "  ✓ Restarted app.py via nohup (no systemd 'portfolio' service found)."
fi

echo ""
echo "=== Auto-Deploy Setup Complete ==="
echo "The calendar fix + standardization are now LIVE on this server."
echo "From now on: 'git push origin main' -> live here within ~60s."
echo "Watch it:  journalctl -u portfolio-deploy.service -f"
echo "Logs:      tail -f $PORTFOLIO_DIR/data/deploy.log"
