#!/bin/bash
# ==============================================================================
# setup_named_tunnel.sh  —  Permanent Cloudflare tunnel bound to YOUR domain
# ==============================================================================
# Replaces the ephemeral `cloudflared tunnel --url` quick tunnel (whose
# *.trycloudflare.com address changes on every restart) with a NAMED tunnel:
# a permanent, stable address that survives reboots and maps to your own domain.
#
# WHY: with a named tunnel, https://<yourdomain> always points at this server's
# local Flask app (localhost:5001) — no random URLs, no open inbound ports
# (outbound-only, same security model as before), free TLS/HTTPS from Cloudflare.
#
# ── ONE-TIME PREREQUISITES (you do these in a browser / interactively) ────────
#   1. A Cloudflare account (free) and your domain's DNS managed by Cloudflare
#      (buy the domain AT Cloudflare, or move its nameservers to Cloudflare).
#   2. cloudflared installed on this server (this script installs it if missing).
#   3. Run:  cloudflared tunnel login
#      → opens a browser, you pick your domain, it drops a cert.pem locally.
#
# Then run THIS script:
#   TUNNEL_HOSTNAME=nishan.example.com bash setup_named_tunnel.sh
#
# It is idempotent: re-running reuses the existing tunnel and just re-asserts the
# DNS route + systemd service.
# ==============================================================================
set -euo pipefail

# ── Config (override via env) ─────────────────────────────────────────────────
TUNNEL_NAME="${TUNNEL_NAME:-portfolio}"
TUNNEL_HOSTNAME="${TUNNEL_HOSTNAME:-}"          # e.g. nishan.example.com  (REQUIRED)
LOCAL_URL="${LOCAL_URL:-http://localhost:5001}" # the Flask app
CF_DIR="${CF_DIR:-$HOME/.cloudflared}"
SERVICE_USER="${SERVICE_USER:-$USER}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }
die() { echo "ERROR: $1" >&2; exit 1; }

[ -n "$TUNNEL_HOSTNAME" ] || die "Set TUNNEL_HOSTNAME, e.g. TUNNEL_HOSTNAME=nishan.example.com bash setup_named_tunnel.sh"

# ── 1. Ensure cloudflared is installed ────────────────────────────────────────
if ! command -v cloudflared >/dev/null 2>&1; then
    log "Installing cloudflared..."
    ARCH="$(dpkg --print-architecture 2>/dev/null || echo amd64)"
    curl -fsSL -o /tmp/cloudflared.deb \
        "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${ARCH}.deb"
    sudo dpkg -i /tmp/cloudflared.deb || sudo apt-get install -f -y
fi
log "cloudflared: $(cloudflared --version 2>&1 | head -1)"

# ── 2. Verify you've logged in (cert.pem present) ─────────────────────────────
if [ ! -f "$CF_DIR/cert.pem" ]; then
    die "Not logged in. Run:  cloudflared tunnel login   (opens a browser; pick your domain), then re-run this."
fi

# ── 3. Create the named tunnel (reuse if it already exists) ───────────────────
if cloudflared tunnel list 2>/dev/null | grep -qw "$TUNNEL_NAME"; then
    log "Tunnel '$TUNNEL_NAME' already exists — reusing."
else
    log "Creating tunnel '$TUNNEL_NAME'..."
    cloudflared tunnel create "$TUNNEL_NAME"
fi

# Resolve the tunnel UUID (used to find its credentials file).
TUNNEL_ID="$(cloudflared tunnel list 2>/dev/null | awk -v n="$TUNNEL_NAME" '$2==n{print $1}')"
[ -n "$TUNNEL_ID" ] || die "Could not resolve tunnel id for '$TUNNEL_NAME'."
CRED_FILE="$CF_DIR/${TUNNEL_ID}.json"
[ -f "$CRED_FILE" ] || die "Credentials file $CRED_FILE not found (was the tunnel created on this host?)."

# ── 4. Write the tunnel config (ingress → local Flask app) ────────────────────
CONFIG_FILE="$CF_DIR/config.yml"
log "Writing $CONFIG_FILE (route $TUNNEL_HOSTNAME → $LOCAL_URL)..."
cat > "$CONFIG_FILE" <<EOF
tunnel: ${TUNNEL_ID}
credentials-file: ${CRED_FILE}

ingress:
  - hostname: ${TUNNEL_HOSTNAME}
    service: ${LOCAL_URL}
  # Everything else → 404 (required catch-all).
  - service: http_status:404
EOF

# ── 5. Point the DNS record at the tunnel (idempotent) ────────────────────────
log "Routing DNS $TUNNEL_HOSTNAME → tunnel $TUNNEL_NAME..."
cloudflared tunnel route dns "$TUNNEL_NAME" "$TUNNEL_HOSTNAME" \
    || log "DNS route already exists (or needs manual CNAME) — continuing."

# ── 6. Install as a systemd service so it runs 24/7 and survives reboots ──────
log "Installing cloudflared systemd service..."
sudo cloudflared --config "$CONFIG_FILE" service install 2>/dev/null || true
# The stock unit sometimes points at /etc/cloudflared; make sure it uses OUR config.
sudo systemctl daemon-reload
sudo systemctl enable cloudflared 2>/dev/null || true
sudo systemctl restart cloudflared

log "Done. Your site should now be live at: https://${TUNNEL_HOSTNAME}"
log "Verify:  sudo systemctl status cloudflared   and open the URL in a browser."
