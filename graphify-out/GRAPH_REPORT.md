# Graph Report - portfolio-v2  (2026-09-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 498 nodes · 878 edges · 32 communities (26 shown, 6 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.91)
- Token cost: 27,530 input · 1,519 output

## Graph Freshness
- Built from commit: `5d0be07e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Book Cover Rendering
- FCC Challenge Sync
- Book Content Compilation
- Challenge Import & Notes
- Remote Deployment Scripts
- Database Migrations
- API & Page Routes
- Image Processing
- Challenge Export & PDF
- AWS Notes Book Sync
- App Bootstrap & Auth
- Tunnel Deployment
- Challenge Dashboard & Comments
- Admin Panel
- Graph Data Schema
- Book Reader Frontend
- HTML Description Parser
- Public URL Retrieval
- User Registration & OTP
- Network Watchdog
- Daily Quote & Homepage
- Auto Deploy Scripts
- Error Handlers
- Books Listing
- KaTeX Rendering
- Named Tunnel Setup
- Health Check
- Book Serving
- Dev Sync Script
- Scraper Runner
- Setup Script
- Server Setup Script

## God Nodes (most connected - your core abstractions)
1. `Challenge` - 33 edges
2. `render_card()` - 20 edges
3. `Golden` - 13 edges
4. `check()` - 11 edges
5. `load_font()` - 10 edges
6. `_DescriptionParser` - 9 edges
7. `Finding` - 9 edges
8. `_draw_python_code()` - 9 edges
9. `User` - 8 edges
10. `_draw_description_blocks()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `api_challenge()` --uses--> `Challenge`  [INFERRED]
  app.py → models.py
- `api_challenges()` --uses--> `Challenge`  [INFERRED]
  app.py → models.py
- `_bootstrap_content()` --uses--> `Challenge`  [INFERRED]
  app.py → models.py
- `challenge_detail()` --uses--> `Challenge`  [INFERRED]
  app.py → models.py
- `challenges()` --uses--> `Challenge`  [INFERRED]
  app.py → models.py

## Import Cycles
- None detected.

## Communities (32 total, 6 thin omitted)

### Community 0 - "Book Cover Rendering"
Cohesion: 0.06
Nodes (57): build(), _fit_title(), book_cover.py — golden-ratio COVER + per-unit OPENER images for compiled books…, Auto-shrink ladder 233 -> 144 -> 89, re-wrapping at each step., render_cover(), render_opener(), _save(), _wrap() (+49 more)

### Community 1 - "FCC Challenge Sync"
Cohesion: 0.06
Nodes (43): datetime, backfill(), extract_starter_code(), fetch_challenge(), generate_card(), _latest_synced_date(), log(), main() (+35 more)

### Community 2 - "Book Content Compilation"
Cohesion: 0.07
Nodes (43): _derive_toc_group(), load_book(), book_content.py — assemble a BOOK dict from Markdown sources on disk. Each…, Build one TOC group for a section file from its opener + anchors., _assemble_body(), compile_book(), compile_unit_html(), mark_wide_equations() (+35 more)

### Community 3 - "Challenge Import & Notes"
Cohesion: 0.07
Nodes (20): bs4, continuous_notes.py ------------------- This script reads the list of URLs,…, dateparser, _apply(), import_all(), _load_json_files(), main(), import_challenges.py -------------------- Rebuild the ``challenges`` table from… (+12 more)

### Community 4 - "Remote Deployment Scripts"
Cohesion: 0.09
Nodes (16): deploy_bridge.py ---------------- Deploys the Telegram Bridge and logic files…, fix_sudo.py ----------- Forcefully sets up passwordless sudo for 'nishan', paramiko, paramiko_sftp_client, push_templates.py - Push updated HTML templates to the live server, connect(), main(), remote_backfill.py ------------------ Runs fcc_sync.py --backfill directly on… (+8 more)

### Community 5 - "Database Migrations"
Cohesion: 0.11
Nodes (12): alembic, flask, logging, logging_config, get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL… (+4 more)

### Community 6 - "API & Page Routes"
Cohesion: 0.09
Nodes (23): api_challenge(), api_challenges(), book_pdf(), book_reader(), challenges(), gauth_callback(), github(), github_callback() (+15 more)

### Community 7 - "Image Processing"
Cohesion: 0.15
Nodes (21): asyncio, cv2, DEFAULT_TYPE, glob, clean_image(), main(), image_processor.py ------------------ Cleans FCC branding (logo at top, mobile…, numpy (+13 more)

### Community 8 - "Challenge Export & PDF"
Cohesion: 0.14
Nodes (17): argparse, challenge_to_dict(), export_one(), _filename(), main(), export_challenges.py -------------------- Serialize every Challenge row from…, Project a Challenge row onto the exportable content fields., Write a single challenge to its per-day JSON file. Returns the path. (+9 more)

### Community 9 - "AWS Notes Book Sync"
Cohesion: 0.16
Nodes (18): build_chapter(), collect_nodes(), _convert_blockquote(), _demote_headings(), _domain_of(), _node_sort_key(), _opener(), r""" aws_sync.py — turn the AWS-ML-Notes engine's content into the "Notes as We… (+10 more)

### Community 10 - "App Bootstrap & Auth"
Cohesion: 0.12
Nodes (14): _bootstrap_content(), gauth(), Make a fresh clone 'just work': ensure tables exist and, if the challenges…, Real Google OAuth Redirection structure., set_sqlite_pragma(), calendar, dotenv, flask_migrate (+6 more)

### Community 11 - "Tunnel Deployment"
Cohesion: 0.24
Nodes (15): connect(), ensure_portfolio_running(), install_cloudflared(), install_ssh_key(), kill_tunnels(), main(), deploy_tunnel.py ---------------- 1. Connects to remote server with password…, Start cloudflared and poll for the trycloudflare.com URL. (+7 more)

### Community 12 - "Challenge Dashboard & Comments"
Cohesion: 0.15
Nodes (12): challenge_detail(), dashboard(), post_comment(), Individual challenge detail, User Dashboard mapping concept scores., Post comment on specific challenge board., Comment, ConceptStrength (+4 more)

### Community 13 - "Admin Panel"
Cohesion: 0.17
Nodes (11): admin(), admin_required(), allowed_file(), get_fcc_quote(), _handle_admin_post(), Formatted quote string for the admin form (uses the hourly cache)., Save an uploaded file from the admin form and return its filename., Process the admin POST form: validate, save files, upsert DB record. (+3 more)

### Community 14 - "Graph Data Schema"
Cohesion: 0.17
Nodes (11): decisions, edges, generatedFrom, clonedOn, commitCount, headCommit, historyRange, repo (+3 more)

### Community 15 - "Book Reader Frontend"
Cohesion: 0.25
Nodes (6): currentUnitIndex(), setActive(), updateProgress(), wireNav(), go(), refreshEnds()

### Community 16 - "HTML Description Parser"
Cohesion: 0.29
Nodes (3): _DescriptionParser, Turn FCC's description HTML into an ordered list of typed blocks so we can…, HTMLParser

### Community 17 - "Public URL Retrieval"
Cohesion: 0.64
Nodes (7): extract_url(), kill_all(), get_public_url.sh script, try_cloudflared(), try_localhost_run(), try_ngrok(), try_serveo()

### Community 18 - "User Registration & OTP"
Cohesion: 0.29
Nodes (6): Handle User Registration with Mock OTP Verification., Verify 6-digit pin to create User in DB., register(), verify_otp(), Stores registered users with GAuth/GitHub support credentials mapping., User

### Community 19 - "Network Watchdog"
Cohesion: 0.52
Nodes (6): check_internet(), get_state(), log(), main(), set_state(), network_watchdog.sh script

### Community 20 - "Daily Quote & Homepage"
Cohesion: 0.33
Nodes (6): _fetch_random_fcc_quote(), get_daily_quote(), home(), Homepage — shows the latest daily challenge and a rotating quote., Fetch a single random (quote, author) from FCC's open-source JSON. Returns the…, Get the daily FCC quote with an hourly file cache. Fetches once per hour,…

### Community 21 - "Auto Deploy Scripts"
Cohesion: 0.40
Nodes (4): log(), auto_deploy.sh script, setup_auto_deploy.sh script, venv_bin_activate

### Community 22 - "Error Handlers"
Cohesion: 0.40
Nodes (5): not_found(), Return JSON for API paths, HTML otherwise., Surface (log) the failure and degrade gracefully rather than crash., server_error(), errorhandler

### Community 23 - "Books Listing"
Cohesion: 0.50
Nodes (4): _book_assets(), books_index(), Return (has_html, has_pdf) for a compiled book slug., Public listing of compiled books (only those actually built).

### Community 24 - "KaTeX Rendering"
Cohesion: 0.50
Nodes (3): katex, path, ref_path

### Community 25 - "Named Tunnel Setup"
Cohesion: 0.83
Nodes (3): die(), log(), setup_named_tunnel.sh script

## Knowledge Gaps
- **17 isolated node(s):** `decisions`, `edges`, `clonedOn`, `commitCount`, `headCommit` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 222 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Challenge` connect `FCC Challenge Sync` to `Book Cover Rendering`, `Challenge Import & Notes`, `API & Page Routes`, `Challenge Export & PDF`, `App Bootstrap & Auth`, `Challenge Dashboard & Comments`, `Admin Panel`, `Daily Quote & Homepage`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `_DescriptionParser` connect `HTML Description Parser` to `Book Cover Rendering`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `Challenge` (e.g. with `api_challenge()` and `api_challenges()`) actually correct?**
  _`Challenge` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `decisions`, `edges`, `clonedOn` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Book Cover Rendering` be split into smaller, more focused modules?**
  _Cohesion score 0.05698778833107191 - nodes in this community are weakly interconnected._
- **Should `FCC Challenge Sync` be split into smaller, more focused modules?**
  _Cohesion score 0.061581920903954805 - nodes in this community are weakly interconnected._
- **Should `Book Content Compilation` be split into smaller, more focused modules?**
  _Cohesion score 0.06636500754147813 - nodes in this community are weakly interconnected._