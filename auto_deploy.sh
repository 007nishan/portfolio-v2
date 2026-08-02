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
# Read-only deploy key for PRIVATE-repo pulls. If this file exists, git uses it
# over SSH so `git fetch/pull` works after the repo is made private. Public repos
# don't need it (this stays unset and plain HTTPS/anonymous pull works). See
# GO_LIVE.md for how to generate the key and add it to the repo as a deploy key.
DEPLOY_KEY="${DEPLOY_KEY:-$PORTFOLIO_DIR/deploy_key}"

log() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$PORTFOLIO_DIR"

# 0a. PRIVATE-REPO AUTH: if a deploy key is present, tell git to use it for all
#     remote ops this run (fetch/pull). Harmless when the repo is public.
if [ -f "$DEPLOY_KEY" ]; then
    export GIT_SSH_COMMAND="ssh -i '$DEPLOY_KEY' -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
    # Ensure the remote is the SSH form (deploy keys don't work over HTTPS).
    CUR_REMOTE="$(git remote get-url origin 2>/dev/null || echo '')"
    case "$CUR_REMOTE" in
        https://github.com/*)
            SSH_REMOTE="git@github.com:${CUR_REMOTE#https://github.com/}"
            git remote set-url origin "$SSH_REMOTE" \
                && log "Private-repo: switched origin to SSH ($SSH_REMOTE) for deploy-key auth."
            ;;
    esac
fi

# 0. SINGLE-WRITER SELF-HEAL (runs EVERY tick, before the up-to-date short-circuit).
#    The daily GitHub Action is now the SOLE writer of challenge content. Any
#    fcc_sync cron previously installed on this host (by an older setup_server.sh)
#    would be a SECOND, conflicting writer that hits the FCC API and mutates the DB
#    behind the Action's back. Remove it. This host is a pure CONSUMER: it pulls
#    committed JSON and rebuilds its DB (step 4a2 below). Idempotent + quiet — does
#    nothing once the cron is gone. Placed before the early-exit so the host
#    self-heals even on ticks with no new commits.
if command -v crontab >/dev/null 2>&1 && crontab -l 2>/dev/null | grep -q "fcc_sync.py"; then
    crontab -l 2>/dev/null | grep -v "fcc_sync.py" | grep -v "FCC Daily Challenge Sync" | crontab - \
        && log "Single-writer: removed local fcc_sync cron (GitHub Action is the sole content writer now)."
fi

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
#    Also exclude static/books (generated QA reports + PDFs are rebuilt here).
if ! git diff --quiet -- ':!static/images' ':!static/books' || ! git diff --cached --quiet -- ':!static/images' ':!static/books'; then
    log "WARNING: uncommitted local changes present (outside static/images, static/books). Aborting to avoid data loss."
    git status --short -- ':!static/images' ':!static/books' | tee -a "$LOG_FILE"
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

# 3b. One-time: WeasyPrint native libs (Pango/Cairo/gdk-pixbuf) for PDF export.
#     Sentinel-guarded so it runs only once. Non-fatal if apt is unavailable
#     (PDF export just stays degraded until the libs are present).
WEASY_SENTINEL="$PORTFOLIO_DIR/data/.weasyprint_native_ok"
if [ ! -f "$WEASY_SENTINEL" ] && command -v apt-get >/dev/null 2>&1; then
    log "Installing WeasyPrint native libs (one-time)..."
    if sudo apt-get update -qq && sudo apt-get install -y -qq \
        libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libcairo2 \
        libgdk-pixbuf-2.0-0 libffi-dev libharfbuzz0b libfontconfig1 libglib2.0-0 \
        fonts-liberation shared-mime-info >> "$LOG_FILE" 2>&1; then
        touch "$WEASY_SENTINEL"; log "Native libs installed."
    else
        log "WARNING: apt install of WeasyPrint native libs failed (PDF export may be degraded)."
    fi
fi

# 4. Install any new/updated Python deps into the venv
if [ -f "$PORTFOLIO_DIR/venv/bin/pip" ] && [ -f "$PORTFOLIO_DIR/requirements.txt" ]; then
    "$PORTFOLIO_DIR/venv/bin/pip" install -q -r "$PORTFOLIO_DIR/requirements.txt" >> "$LOG_FILE" 2>&1 || \
        log "WARNING: pip install reported an issue (continuing)."
fi

# 4a2. Sync challenge CONTENT from the committed JSON (GitHub-as-buffer, consumer
#      side). The daily GitHub Action is the sole WRITER of content; every host is
#      a pure CONSUMER that rebuilds its DB from content/challenges/*.json after a
#      pull. import_challenges.py is an idempotent UPSERT — it only ever adds/
#      updates challenge rows and NEVER touches user tables (users/comments/etc.),
#      so live user data is preserved. Non-fatal: a hiccup here must not block the
#      rest of the deploy.
if [ -f "$PORTFOLIO_DIR/venv/bin/python" ] && [ -f "$PORTFOLIO_DIR/import_challenges.py" ]; then
    "$PORTFOLIO_DIR/venv/bin/python" import_challenges.py --quiet >> "$LOG_FILE" 2>&1 \
        && log "Imported challenge content from content/challenges/." \
        || log "WARNING: challenge content import reported an issue (continuing)."
fi

# 4b. Rebuild books (HTML + PDF) if their sources changed, gated by the
#     error-free readability lint. A failing gate aborts the deploy BEFORE the
#     restart so a broken book is never served. Non-fatal if book tooling absent.
if [ -f "$PORTFOLIO_DIR/venv/bin/python" ] && [ -f "$PORTFOLIO_DIR/book_generator.py" ]; then
    for slug in python linear-algebra aws-ml; do
        # Skip a book that has no source yet (nothing to compile).
        if ! "$PORTFOLIO_DIR/venv/bin/python" -c "import book_content,sys; book_content.load_book('$slug')" >/dev/null 2>&1; then
            continue
        fi
        if ! "$PORTFOLIO_DIR/venv/bin/python" book_lint.py --book "$slug" --strict >> "$LOG_FILE" 2>&1; then
            log "ERROR: QA gate FAILED for '$slug' — see static/books/qa/$slug.qa.json. Aborting deploy (service NOT restarted)."
            exit 1
        fi
        "$PORTFOLIO_DIR/venv/bin/python" book_generator.py "$slug" >> "$LOG_FILE" 2>&1 || log "WARNING: HTML build for '$slug' failed."
        "$PORTFOLIO_DIR/venv/bin/python" make_book_pdf.py --book "$slug" >> "$LOG_FILE" 2>&1 || log "WARNING: PDF build for '$slug' failed (native libs?)."
    done
fi

# 5. Restart the app so template/code changes take effect
#    (Flask/Jinja caches templates; a restart is required.)
if command -v systemctl >/dev/null 2>&1 && systemctl cat "${SERVICE}.service" >/dev/null 2>&1; then
    sudo systemctl restart "$SERVICE" && log "Restarted systemd service '$SERVICE'."
else
    # Fallback: restart a bare `python app.py` process
    pkill -f "python app.py" 2>/dev/null || true
    ( cd "$PORTFOLIO_DIR" && source venv/bin/activate && nohup python app.py > /tmp/portfolio.log 2>&1 & )
    log "Restarted app.py via nohup fallback."
fi

log "Deploy complete. Now at $(git rev-parse --short HEAD): $(git log -1 --pretty=%s)"
