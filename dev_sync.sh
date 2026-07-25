#!/bin/bash
# ==============================================================================
# dev_sync.sh  —  Bring this DEV box up to the live site's state
# ==============================================================================
# Two-part "stay live" routine, matching the split the project was designed
# around (see knowledge-graph/05-decisions.md D-001/D-002, 09-operations.md):
#
#   CODE  travels via GitHub  → this script pulls origin/main (fast-forward)
#   DATA  is NOT in git        → this script rebuilds the DB from the FCC API
#                                (data/ is gitignored on purpose; the live DB
#                                 is regenerated per machine, keeping the repo
#                                 light — same as the server's 00:30 cron).
#
# This is the dev-box analogue of the server's auto_deploy.sh + fcc_sync cron.
# Run it whenever you sit down to develop, to match the live site's state.
#
# Usage:
#   bash dev_sync.sh              # pull code + sync TODAY's challenge
#   bash dev_sync.sh --backfill   # pull code + full backfill (from 2025-08-11)
#   bash dev_sync.sh --code-only  # pull code only, skip the data sync
#   bash dev_sync.sh --data-only  # sync data only, skip the git pull
# ==============================================================================

set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRANCH="${DEPLOY_BRANCH:-main}"
PY="${PYTHON:-python}"
cd "$REPO_DIR"

DO_CODE=1
DO_DATA=1
SYNC_ARGS=""

for arg in "$@"; do
    case "$arg" in
        --code-only) DO_DATA=0 ;;
        --data-only) DO_CODE=0 ;;
        --backfill)  SYNC_ARGS="--backfill" ;;
        *) echo "Unknown option: $arg"; echo "Use: --backfill | --code-only | --data-only"; exit 2 ;;
    esac
done

echo "=================================================="
echo "  Portfolio dev sync  (branch: $BRANCH)"
echo "=================================================="

# ── 1. CODE: pull latest from GitHub (safe, fast-forward only) ────────────────
if [ "$DO_CODE" = "1" ]; then
    echo ""
    echo "[1/2] Pulling latest code from origin/$BRANCH ..."
    if ! git fetch --quiet origin "$BRANCH"; then
        echo "  ! git fetch failed (offline / no access) — skipping code update."
    else
        LOCAL=$(git rev-parse HEAD)
        REMOTE=$(git rev-parse "origin/$BRANCH")
        if [ "$LOCAL" = "$REMOTE" ]; then
            echo "  ✓ Already up to date ($(git rev-parse --short HEAD))."
        elif ! git diff --quiet || ! git diff --cached --quiet; then
            echo "  ! Uncommitted local changes present — NOT pulling (would risk your WIP)."
            echo "    Commit or stash first, then re-run. Current changes:"
            git status --short
        elif git merge --ff-only "origin/$BRANCH"; then
            echo "  ✓ Updated: $(git rev-parse --short "$LOCAL") -> $(git rev-parse --short HEAD)"
        else
            echo "  ! Fast-forward failed (history diverged). Resolve manually."
        fi
    fi
else
    echo ""
    echo "[1/2] Skipping code pull (--data-only)."
fi

# ── 2. DATA: rebuild the DB from the FCC API (data/ is gitignored by design) ──
if [ "$DO_DATA" = "1" ]; then
    echo ""
    if [ -n "$SYNC_ARGS" ]; then
        echo "[2/2] Backfilling all challenges from the FCC API (this takes a few minutes)..."
    else
        echo "[2/2] Syncing today's challenge from the FCC API..."
    fi
    "$PY" fcc_sync.py $SYNC_ARGS
    echo "  ✓ Data sync finished."
else
    echo ""
    echo "[2/2] Skipping data sync (--code-only)."
fi

echo ""
echo "Done. Start the dev server with:  FLASK_DEBUG=1 $PY app.py"
echo "Then open: http://127.0.0.1:5001"
