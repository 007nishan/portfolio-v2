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
# 2. CONTENT SYNC — now handled by the GitHub Action (single-writer model)
# ──────────────────────────────────────────────────────────────────────────────
echo "[2/4] Content sync: GitHub Action is the sole writer (no local cron)..."

# The daily FCC sync + card generation now runs in a GitHub Action
# (.github/workflows/daily-sync.yml), which commits content to the repo. This
# host is a pure CONSUMER: auto_deploy.sh pulls that committed content and
# rebuilds the DB via import_challenges.py. We deliberately do NOT install a
# local fcc_sync cron — a second writer would race the Action and corrupt state.
#
# Belt-and-braces: remove any legacy fcc_sync cron a previous setup left behind
# (auto_deploy.sh also self-heals this on every tick).
if crontab -l 2>/dev/null | grep -q "fcc_sync.py"; then
    crontab -l 2>/dev/null | grep -v "fcc_sync.py" | grep -v "FCC Daily Challenge Sync" | crontab -
    echo "  ✓ Removed legacy fcc_sync cron (GitHub Action is the sole content writer)"
else
    echo "  ✓ No local content cron (correct — content comes from GitHub)"
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
echo "  ✓ Content sync → GitHub Action (this host is a pull-only consumer)"
echo "  ✓ Network watchdog → every 2 minutes via systemd timer"
echo "  ✓ Portfolio service → auto-restart on crash"
echo ""
echo "To verify: sudo systemctl list-timers | grep portfolio"
