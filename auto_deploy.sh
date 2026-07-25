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

# 2. Refuse to clobber uncommitted local changes to server-only edits (hand-
#    patched app.py, templates, etc.) — EXCEPT drift under static/images/, which
#    is expected: the daily cron regenerates challenge cards in place, so those
#    tracked .jpg files legitimately differ. We exclude that path from the guard
#    and then restore the tracked images to HEAD so the merge/reset is clean.
#    Untracked images (a brand-new day's card not yet in git) are left untouched.
if ! git diff --quiet -- ':!static/images' || ! git diff --cached --quiet -- ':!static/images'; then
    log "WARNING: uncommitted local changes present (outside static/images). Aborting to avoid data loss."
    git status --short -- ':!static/images' | tee -a "$LOG_FILE"
    exit 1
fi
# Discard regenerable card drift so ff/reset applies cleanly (safe: cards are
# rebuilt from DB data by challenge_card.py; nothing unique lives here).
git checkout -- static/images 2>/dev/null || true

# 3. Fast-forward if possible. If the remote history was REWRITTEN (e.g. the
#    one-time FCC-image history purge), a fast-forward is impossible. Because
#    step 2 already guaranteed a clean working tree, it is safe to adopt the
#    rewritten history with `reset --hard`: it overwrites TRACKED files to the
#    remote version (deleting files that no longer exist upstream — like the old
#    FCC images) while leaving UNTRACKED files (data/, venv/, .env,
#    admin_id.txt, claw_config.json, and any manual /admin image uploads)
#    completely untouched. This makes the server self-heal on a history rewrite
#    instead of stalling on a failed fast-forward.
if git merge --ff-only "origin/$BRANCH" >> "$LOG_FILE" 2>&1; then
    log "Fast-forwarded to origin/$BRANCH."
else
    log "Fast-forward not possible (remote history was rewritten)."
    log "Working tree is clean (verified above) — adopting rewritten history via reset --hard."
    if git reset --hard "origin/$BRANCH" >> "$LOG_FILE" 2>&1; then
        log "Reset working tree to origin/$BRANCH (untracked files preserved; stale tracked files removed)."
    else
        log "ERROR: reset --hard failed. Manual intervention needed."
        exit 1
    fi
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
