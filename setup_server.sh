#!/bin/bash
# ==============================================================================
# Portfolio Server Setup Script
# ==============================================================================
# Run this ONCE on the server to configure:
#   1. Lid close behavior (keep running)
#   2. Cron job for daily FCC sync
#   3. Network watchdog systemd timer
#   4. Portfolio service hardening
# ==============================================================================

set -e

echo "=== Portfolio Server Setup ==="
echo ""

PORTFOLIO_DIR="/home/nishan/portfolio"
SYNC_SCRIPT="$PORTFOLIO_DIR/fcc_sync.py"
WATCHDOG_SCRIPT="$PORTFOLIO_DIR/network_watchdog.sh"
VENV_PYTHON="$PORTFOLIO_DIR/venv/bin/python"

# ──────────────────────────────────────────────────────────────────────────────
# 1. KEEP SERVER RUNNING WHEN LID IS CLOSED
# ──────────────────────────────────────────────────────────────────────────────
echo "[1/4] Configuring lid close behavior..."

# Check if already configured
if grep -q "HandleLidSwitch=ignore" /etc/systemd/logind.conf 2>/dev/null; then
    echo "  ✓ Lid close already set to 'ignore'"
else
    # Backup original
    sudo cp /etc/systemd/logind.conf /etc/systemd/logind.conf.bak
    
    # Set lid close actions to ignore
    sudo sed -i 's/^#HandleLidSwitch=.*/HandleLidSwitch=ignore/' /etc/systemd/logind.conf
    sudo sed -i 's/^HandleLidSwitch=.*/HandleLidSwitch=ignore/' /etc/systemd/logind.conf
    sudo sed -i 's/^#HandleLidSwitchExternalPower=.*/HandleLidSwitchExternalPower=ignore/' /etc/systemd/logind.conf
    sudo sed -i 's/^HandleLidSwitchExternalPower=.*/HandleLidSwitchExternalPower=ignore/' /etc/systemd/logind.conf
    sudo sed -i 's/^#HandleLidSwitchDocked=.*/HandleLidSwitchDocked=ignore/' /etc/systemd/logind.conf
    sudo sed -i 's/^HandleLidSwitchDocked=.*/HandleLidSwitchDocked=ignore/' /etc/systemd/logind.conf
    
    # If the line doesn't exist at all, add it
    if ! grep -q "HandleLidSwitch=" /etc/systemd/logind.conf; then
        echo "HandleLidSwitch=ignore" | sudo tee -a /etc/systemd/logind.conf > /dev/null
    fi
    if ! grep -q "HandleLidSwitchExternalPower=" /etc/systemd/logind.conf; then
        echo "HandleLidSwitchExternalPower=ignore" | sudo tee -a /etc/systemd/logind.conf > /dev/null
    fi
    
    sudo systemctl restart systemd-logind
    echo "  ✓ Lid close behavior set to IGNORE (server keeps running)"
fi

# ──────────────────────────────────────────────────────────────────────────────
# 2. DAILY FCC SYNC CRON JOB
# ──────────────────────────────────────────────────────────────────────────────
echo "[2/4] Setting up daily FCC sync cron job..."

CRON_LINE="30 0 * * * cd $PORTFOLIO_DIR && $VENV_PYTHON $SYNC_SCRIPT >> $PORTFOLIO_DIR/data/cron_sync.log 2>&1"

# Check if cron already exists
if crontab -l 2>/dev/null | grep -q "fcc_sync.py"; then
    echo "  ✓ FCC sync cron job already exists"
else
    (crontab -l 2>/dev/null; echo "# FCC Daily Challenge Sync - runs at 12:30 AM US Central (6:00 AM IST)"; echo "$CRON_LINE") | crontab -
    echo "  ✓ Cron job added: runs daily at 12:30 AM Central"
fi

# ──────────────────────────────────────────────────────────────────────────────
# 3. NETWORK WATCHDOG TIMER
# ──────────────────────────────────────────────────────────────────────────────
echo "[3/4] Setting up network watchdog..."

# Make watchdog executable
chmod +x "$WATCHDOG_SCRIPT"

# Create systemd service
sudo tee /etc/systemd/system/portfolio-watchdog.service > /dev/null << EOF
[Unit]
Description=Portfolio Network Watchdog
After=network.target

[Service]
Type=oneshot
ExecStart=$WATCHDOG_SCRIPT
User=nishan
EOF

# Create systemd timer (every 2 minutes)
sudo tee /etc/systemd/system/portfolio-watchdog.timer > /dev/null << EOF
[Unit]
Description=Run Portfolio Watchdog every 2 minutes

[Timer]
OnBootSec=30
OnUnitActiveSec=120
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable portfolio-watchdog.timer
sudo systemctl start portfolio-watchdog.timer
echo "  ✓ Network watchdog timer active (runs every 2 minutes)"

# ──────────────────────────────────────────────────────────────────────────────
# 4. HARDEN PORTFOLIO SERVICE
# ──────────────────────────────────────────────────────────────────────────────
echo "[4/4] Hardening portfolio systemd service..."

# Check current service file
if systemctl cat portfolio 2>/dev/null | grep -q "Restart=always"; then
    echo "  ✓ Portfolio service already has Restart=always"
else
    # Create/update the drop-in override
    sudo mkdir -p /etc/systemd/system/portfolio.service.d
    sudo tee /etc/systemd/system/portfolio.service.d/resilience.conf > /dev/null << EOF
[Service]
Restart=always
RestartSec=5
StartLimitIntervalSec=0
EOF
    sudo systemctl daemon-reload
    sudo systemctl restart portfolio
    echo "  ✓ Portfolio service hardened with Restart=always + RestartSec=5"
fi

echo ""
echo "=== Setup Complete ==="
echo "Summary:"
echo "  ✓ Lid close → server keeps running"
echo "  ✓ Daily FCC sync → 12:30 AM Central via cron"
echo "  ✓ Network watchdog → every 2 minutes via systemd timer"
echo "  ✓ Portfolio service → auto-restart on crash"
echo ""
echo "To verify: sudo systemctl list-timers | grep portfolio"
