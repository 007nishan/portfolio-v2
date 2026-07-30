#!/bin/bash
# ==============================================================================
# Portfolio Network Watchdog
# ==============================================================================
# Monitors internet connectivity and auto-recovers after outages.
# After connectivity is restored, it:
#   1. Pulls the latest committed content from GitHub and rebuilds the DB from
#      it (CONSUMER behaviour — the daily GitHub Action is the sole content
#      WRITER; the watchdog must NOT run fcc_sync or it becomes a second writer).
#   2. Restarts the portfolio service if it's not running
#
# Designed to be run as a systemd timer (every 2 minutes).
# ==============================================================================

PORTFOLIO_DIR="/home/nishan/portfolio"
VENV_PYTHON="$PORTFOLIO_DIR/venv/bin/python"
IMPORT_SCRIPT="$PORTFOLIO_DIR/import_challenges.py"
LOG_FILE="$PORTFOLIO_DIR/data/watchdog.log"
STATE_FILE="$PORTFOLIO_DIR/data/.watchdog_state"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Check internet connectivity (ping Google DNS)
check_internet() {
    ping -c 1 -W 3 8.8.8.8 > /dev/null 2>&1
    return $?
}

# Get last known state
get_state() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo "online"
    fi
}

set_state() {
    echo "$1" > "$STATE_FILE"
}

# Main logic
main() {
    mkdir -p "$(dirname "$LOG_FILE")"
    
    PREV_STATE=$(get_state)
    
    if check_internet; then
        if [ "$PREV_STATE" = "offline" ]; then
            # Internet just came back! Recovery actions:
            log "RECOVERY: Internet restored after outage. Pulling latest content from GitHub..."

            # CONSUMER catch-up: pull committed content and rebuild the DB from it.
            # (auto_deploy.sh also runs on its own timer; doing a lightweight pull
            #  here means content is current the moment connectivity returns.)
            cd "$PORTFOLIO_DIR"
            if git fetch --quiet origin main 2>>"$LOG_FILE" \
               && git merge --ff-only origin/main >> "$LOG_FILE" 2>&1; then
                log "RECOVERY: pulled latest origin/main."
            else
                log "RECOVERY: git pull skipped (auto_deploy.sh will reconcile shortly)."
            fi
            if [ -f "$IMPORT_SCRIPT" ]; then
                $VENV_PYTHON "$IMPORT_SCRIPT" --quiet >> "$LOG_FILE" 2>&1 \
                    && log "RECOVERY: rebuilt DB from committed challenge JSON." \
                    || log "RECOVERY: content import reported an issue (continuing)."
            fi

            # Restart portfolio service if not active
            if ! systemctl is-active --quiet portfolio; then
                log "RECOVERY: Restarting portfolio service..."
                sudo systemctl restart portfolio
                log "RECOVERY: Portfolio service restarted."
            fi
            
            # Restart nginx if not active
            if ! systemctl is-active --quiet nginx; then
                log "RECOVERY: Restarting nginx..."
                sudo systemctl restart nginx
                log "RECOVERY: Nginx restarted."
            fi
            
            log "RECOVERY: All catch-up actions complete."
        fi
        set_state "online"
    else
        if [ "$PREV_STATE" = "online" ]; then
            log "OUTAGE DETECTED: Internet connectivity lost."
        fi
        set_state "offline"
    fi
}

main
