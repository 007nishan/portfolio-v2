#!/bin/bash
# ==============================================================================
# auto_deploy.sh  —  Pull-based auto-update for the portfolio server
# ==============================================================================
# Runs on the server (via a systemd timer / cron). On each run it:
#   1. Fetches origin/main from GitHub
#   2. If there are new commits, fast-forwards the working tree
#   3. Installs any new Python deps (requirements.txt)
#   4. Restarts the portfolio service so changes go live
#
# Design rationale (see knowledge-graph/05-decisions.md D-001):
#   The server only makes OUTBOUND connections (Cloudflare Tunnel, no open
#   ports). A PULL model fits that: no inbound webhook, no open ports, no
#   passwords in the repo. GitHub is the single source of truth for code;
#   the server converges to it automatically.
#
# Idempotent & safe: does nothing when already up to date. Local uncommitted
# changes abort the update (never clobbers server-only edits) and are logged.
# ==============================================================================

set -euo pipefail

PORTFOLIO_DIR="${PORTFOLIO_DIR:-/home/nishan/portfolio}"
BRANCH="${DEPLOY_BRANCH:-main}"
SERVICE="${PORTFOLIO_SERVICE:-portfolio}"
LOG_FILE="$PORTFOLIO_DIR/data/deploy.log"

log() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$PORTFOLIO_DIR"

# 1. Fetch latest without touching the working tree
git fetch --quiet origin "$BRANCH" || { log "ERROR: git fetch failed (network?)"; exit 1; }

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse "origin/$BRANCH")

if [ "$LOCAL" = "$REMOTE" ]; then
    # Already current — stay quiet to keep the log clean
    exit 0
fi

log "New commits detected: $LOCAL -> $REMOTE. Deploying..."

# 2. Refuse to clobber uncommitted local changes (server-only edits, data, etc.)
if ! git diff --quiet || ! git diff --cached --quiet; then
    log "WARNING: uncommitted local changes present. Aborting auto-deploy to avoid data loss."
    git status --short | tee -a "$LOG_FILE"
    exit 1
fi

# 3. Fast-forward only (never rewrite server history)
if ! git merge --ff-only "origin/$BRANCH" >> "$LOG_FILE" 2>&1; then
    log "ERROR: fast-forward merge failed (diverged history). Manual intervention needed."
    exit 1
fi

# 4. Install any new/updated Python deps into the venv
if [ -f "$PORTFOLIO_DIR/venv/bin/pip" ] && [ -f "$PORTFOLIO_DIR/requirements.txt" ]; then
    "$PORTFOLIO_DIR/venv/bin/pip" install -q -r "$PORTFOLIO_DIR/requirements.txt" >> "$LOG_FILE" 2>&1 || \
        log "WARNING: pip install reported an issue (continuing)."
fi

# 5. Restart the app so template/code changes take effect
#    (Flask/Jinja caches templates; a restart is required.)
if command -v systemctl >/dev/null 2>&1 && systemctl list-unit-files 2>/dev/null | grep -q "^${SERVICE}.service"; then
    sudo systemctl restart "$SERVICE" && log "Restarted systemd service '$SERVICE'."
else
    # Fallback: restart a bare `python app.py` process
    pkill -f "python app.py" 2>/dev/null || true
    ( cd "$PORTFOLIO_DIR" && source venv/bin/activate && nohup python app.py > /tmp/portfolio.log 2>&1 & )
    log "Restarted app.py via nohup fallback."
fi

log "Deploy complete. Now at $(git rev-parse --short HEAD): $(git log -1 --pretty=%s)"
