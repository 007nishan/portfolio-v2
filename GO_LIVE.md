# Go Live: Custom Domain + Stable Address + Private Repo

This is the runbook for taking the site live on **your own domain** with a
**permanent address** (no more rotating `trycloudflare.com` URLs), and for making
the GitHub repo **private** without breaking the server's auto-updates.

Everything the code needs is already in the repo. This file covers the steps only
**you** can do (they need your accounts / payment / a browser login on the server).

Run all server commands as user `nishan` on the server (`192.168.1.150`), in
`~/portfolio`.

---

## Part 1 — Buy the domain & put it on Cloudflare (browser, ~10 min)

1. **Create a free Cloudflare account:** https://dash.cloudflare.com/sign-up
2. **Get the domain onto Cloudflare** (either way works):
   - *Easiest:* buy the domain **through Cloudflare Registrar** (Dashboard →
     Domain Registration). It's automatically on Cloudflare DNS — nothing else to do.
   - *Or:* buy it anywhere (Namecheap, GoDaddy, etc.), then in Cloudflare add the
     site and **change the domain's nameservers** at your registrar to the two
     Cloudflare gives you. Wait for it to show **Active** (minutes to a few hours).

> Pick the hostname you want the site on, e.g. `nishan.example.com` or the root
> `example.com`. You'll pass it to the setup script below as `TUNNEL_HOSTNAME`.

---

## Part 2 — Stable address via a NAMED Cloudflare Tunnel (server, ~5 min)

On the server:

```bash
cd ~/portfolio

# 1. One-time browser login — opens a link; pick YOUR domain, approve.
cloudflared tunnel login
#   (installs a cert.pem into ~/.cloudflared/)

# 2. Create the permanent tunnel + DNS route + 24/7 systemd service.
#    Replace the hostname with the one you chose in Part 1.
TUNNEL_HOSTNAME=nishan.example.com bash setup_named_tunnel.sh
```

That's it — the script installs `cloudflared` if missing, creates a named tunnel,
points `nishan.example.com` at it, and runs it as a service that **survives
reboots**. Verify:

```bash
sudo systemctl status cloudflared     # should be active (running)
```

Open `https://nishan.example.com` in a browser — the site should load (free HTTPS
included). This address **never changes again**.

> Retire the old rotating tunnel: if a `cloudflared tunnel --url` quick tunnel is
> still running from the old `get_public_url.sh`/`deploy_tunnel.py` flow, stop it
> (`pkill -f 'tunnel --url'`). The named service replaces it.

---

## Part 3 — Make the repo private without breaking auto-updates (~5 min)

The server pulls code+content from GitHub every ~60s (`auto_deploy.sh`). A public
repo pulls anonymously; a **private** repo needs a read-only key. Set that up
BEFORE flipping the repo to private.

### 3a. Generate a read-only deploy key **on the server**
```bash
cd ~/portfolio
ssh-keygen -t ed25519 -N "" -f ~/portfolio/deploy_key -C "portfolio-deploy-key"
#   creates deploy_key (private) + deploy_key.pub (public)
#   both are gitignored — they never get committed.
cat ~/portfolio/deploy_key.pub          # copy this whole line
```

### 3b. Add the PUBLIC key to the repo as a deploy key (browser)
GitHub → your repo → **Settings → Deploy keys → Add deploy key**
- Title: `portfolio-server`
- Key: paste the `deploy_key.pub` line
- **Leave "Allow write access" UNCHECKED** (read-only — the server only pulls).

### 3c. Prove the key works (still public, so this just confirms auth)
```bash
cd ~/portfolio
GIT_SSH_COMMAND="ssh -i ~/portfolio/deploy_key -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new" \
  git ls-remote git@github.com:007nishan/portfolio-v2.git >/dev/null && echo "KEY OK"
```
`auto_deploy.sh` auto-detects `deploy_key` and switches the remote to SSH on its
next run — no further config needed.

### 3d. Flip the repo to private (browser)
GitHub → repo → **Settings → General → Danger Zone → Change visibility → Private**.

Within ~60s the server's next `auto_deploy.sh` tick pulls over SSH using the deploy
key. Confirm:
```bash
tail -n 20 ~/portfolio/data/deploy.log     # look for a successful fetch/deploy
```

> **GitHub Action still works on a private repo** — it uses the built-in
> `GITHUB_TOKEN`, nothing to change. Private repos include 2,000 free Action
> minutes/month; the daily run uses ~1 min, so you're far under the cap.

---

## Quick reference — where each concern is handled

| Concern | Handled by |
|---|---|
| Stable public address | `setup_named_tunnel.sh` (named tunnel + systemd) |
| Custom domain | Cloudflare DNS (Part 1) → tunnel route (Part 2) |
| Site stays running | `portfolio.service` `Restart=always` + watchdog |
| Daily content updates | GitHub Action (cloud) → server pulls |
| Private-repo pulls | `deploy_key` + `auto_deploy.sh` auto-SSH (Part 3) |
| No open inbound ports | Cloudflare Tunnel (outbound-only) |

## If the laptop's power/internet is the worry
This setup keeps the laptop as the server. To remove that single point of failure
later, the same repo can be deployed to a ~$5/mo always-on cloud VPS with no code
changes (domain would then point straight at the VPS). Ask when you want that path.
