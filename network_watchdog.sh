#!/bin/bash
# ==============================================================================
# Portfolio Network Watchdog
# ==============================================================================
# Monitors internet connectivity and auto-recovers after outages.
# After connectivity is restored, it:
#   1. Runs fcc_sync.py to catch up on any missed daily challenges
#   2. Restarts the portfolio service if it's not running
#
# Designed to be run as a systemd timer (every 2 minutes).
# ==============================================================================

PORTFOLIO_DIR="/home/nishan/portfolio"
VENV_PYTHON="$PORTFOLIO_DIR/venv/bin/python"
SYNC_SCRIPT="$PORTFOLIO_DIR/fcc_sync.py"
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
            log "RECOVERY: Internet restored after outage. Running catch-up sync..."
            
            # Sync any missed FCC challenges
            cd "$PORTFOLIO_DIR"
            $VENV_PYTHON "$SYNC_SCRIPT" >> "$LOG_FILE" 2>&1
            
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
