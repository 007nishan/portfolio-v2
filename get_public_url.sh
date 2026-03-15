#!/bin/bash
# ============================================================
# get_public_url.sh
# Tries multiple methods in order to expose port 5001 publicly.
# Kills any stale process before retrying. Prints the URL.
# ============================================================
set -e

PORT=5001
LOG=/home/nishan/tunnel.log
TIMEOUT=8   # seconds to wait per attempt

kill_all() {
    pkill -f cloudflared 2>/dev/null || true
    pkill -f ngrok 2>/dev/null || true
    pkill -f lt 2>/dev/null || true
    pkill -f localtunnel 2>/dev/null || true
    sleep 1
}

extract_url() {
    # Try to grep a https URL from a log file
    grep -oP 'https://[a-zA-Z0-9._-]+' "$1" 2>/dev/null | head -1
}

# ── METHOD 1: cloudflared (already installed on this Ubuntu) ──────────────
try_cloudflared() {
    echo "[1] Trying cloudflared..." | tee -a $LOG
    kill_all
    rm -f $LOG
    cloudflared tunnel --url http://localhost:$PORT > $LOG 2>&1 &
    sleep $TIMEOUT
    URL=$(extract_url $LOG)
    if [ -n "$URL" ]; then
        echo "SUCCESS: $URL"
        return 0
    fi
    return 1
}

# ── METHOD 2: ngrok (free, no auth required via v2 binary) ───────────────
try_ngrok() {
    echo "[2] Trying ngrok v2 binary..." | tee -a $LOG
    kill_all
    # Download static binary if not present
    if [ ! -f /tmp/ngrok ]; then
        wget -q -O /tmp/ngrok.zip https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
        cd /tmp && unzip -o ngrok.zip
    fi
    /tmp/ngrok http $PORT > $LOG 2>&1 &
    sleep $TIMEOUT
    URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -oP '"public_url":"https://[^"]+' | head -1 | cut -d'"' -f4)
    if [ -n "$URL" ]; then
        echo "SUCCESS: $URL"
        return 0
    fi
    return 1
}

# ── METHOD 3: localhost.run (pure SSH, zero install) ─────────────────────
try_localhost_run() {
    echo "[3] Trying localhost.run SSH tunnel..." | tee -a $LOG
    kill_all
    ssh -o StrictHostKeyChecking=no \
        -o ServerAliveInterval=5 \
        -o ConnectTimeout=10 \
        -R 80:localhost:$PORT \
        nokey@localhost.run > $LOG 2>&1 &
    sleep $TIMEOUT
    URL=$(extract_url $LOG)
    if [ -n "$URL" ]; then
        echo "SUCCESS: $URL"
        return 0
    fi
    return 1
}

# ── METHOD 4: serveo.net (fallback SSH tunnel) ───────────────────────────
try_serveo() {
    echo "[4] Trying serveo.net SSH tunnel..." | tee -a $LOG
    kill_all
    ssh -o StrictHostKeyChecking=no \
        -o ServerAliveInterval=5 \
        -o ConnectTimeout=10 \
        -R 80:localhost:$PORT \
        serveo.net > $LOG 2>&1 &
    sleep $TIMEOUT
    URL=$(extract_url $LOG)
    if [ -n "$URL" ]; then
        echo "SUCCESS: $URL"
        return 0
    fi
    return 1
}

# ── MAIN LOOP ─────────────────────────────────────────────────────────────
echo "=== Tunnel Setup Start ==="
for ATTEMPT in 1 2 3; do
    echo "--- Attempt $ATTEMPT ---"

    try_cloudflared && exit 0
    echo "[1] cloudflared failed, next..."

    try_ngrok && exit 0
    echo "[2] ngrok failed, next..."

    try_localhost_run && exit 0
    echo "[3] localhost.run failed, next..."

    try_serveo && exit 0
    echo "[4] serveo failed."

    echo "All methods failed on attempt $ATTEMPT. Waiting 5s before retry..."
    sleep 5
done

echo "ERROR: Could not establish any public tunnel after 3 attempts."
echo "Last log output:"
cat $LOG
exit 1
