# AGENT.md - Project Onboarding

Welcome to the ei23 DIY Smart Home project! This document helps both humans and AI assistants understand what this project is about, how it's structured, and how to contribute.

---

## 🎯 Mission / Why This Project Exists

### The Problem

Smart homes today are dominated by big tech. Amazon Echo, Google Home, Apple HomeKit – they all funnel your data through corporate clouds. You don't control your home. They do. Features get removed. Services shut down. Prices increase. You're locked in.

**This is the path to a cyberpunk scenario.** Megacorps controlling the infrastructure of your daily life.

### The Solution

ei23 DIY Smart Home exists to give people **full control over their smart home**:

- ✅ **Own hardware** – Your server, your control
- ✅ **Open source software** – No lock-in, no corporate agenda
- ✅ **Local-first** – Works without internet, without cloud
- ✅ **No monthly fees** – Pay once for hardware, own it forever
- ✅ **Privacy** – Your data stays on your server

**Your home belongs to you. Your data belongs to you. Your automations belong to you.**

### Core Philosophy

> "Energy flows where money goes" – but also: **Don't become a feature-creep.**

- Only automate what saves energy, time, or money
- Keeping things simple is an art
- If something constantly causes problems, you'll lose the fun
- But if you're willing to learn, endlessly much is possible

The project follows the principle: **Make the complex accessible, keep the simple simple.**

---

## 🏗️ Project Structure

```
diy-smart-home/
├── ei23.sh                    # Main installation & maintenance script (Bash)
├── de-file.txt                # German language strings for ei23.sh
├── en-file.txt                # English language strings for ei23.sh
├── README.md                  # GitHub README (English)
├── AGENT.md                   # This file - project onboarding
├── donate_newsletter.md       # Newsletter/donation announcements
├── LICENSE                    # License file
│
├── ei23-docker/               # Docker project root (gets copied to user's home)
│   ├── compose_templates/     # Docker Compose templates (90+ services)
│   │   ├── homeassistant.yml
│   │   ├── nodered.yml
│   │   ├── grafana.yml
│   │   ├── ...                # One .yml per service
│   │   └── env/               # Example .env files for some services
│   │
│   ├── volumes/               # Persistent data directories
│   │   └── ei23/              # ei23 Dashboard / Supervisor
│   │       ├── ei23-supervisor.py   # Python Flask server (the dashboard)
│   │       ├── web/                 # HTML/CSS/JS templates
│   │       ├── .venv/               # Python virtual environment
│   │       └── docs/                # MkDocs documentation source
│   │
│   └── custom_ha_addons-example.sh  # Home Assistant addon automation
│
├── DOCS/                      # Documentation (MkDocs Material)
│   ├── guidelines.md          # Contribution guidelines
│   ├── DE/                    # German documentation
│   │   ├── mkdocs.yml         # MkDocs config (navigation, theme)
│   │   └── docs/
│   │       ├── index.md       # Landing page / Mission Statement
│   │       ├── start/         # Getting started guides
│   │       ├── software/      # Per-software documentation
│   │       └── hardware/      # Hardware recommendations
│   │
│   └── EN/                    # English documentation (mirror of DE)
│       ├── mkdocs.yml
│       └── docs/
│
├── EN/                        # Legacy English files
├── updates/                   # Update mechanism files
└── .gitignore
```

---

## 🔧 Key Components

### 1. `ei23.sh` - The Heart

The main Bash script that users interact with. It handles:

- **Installation** (`part1`, `part2`) – Installs Docker, Node-RED, packages
- **Updates** (`ei23 update`) – Full system update
- **Docker Compose** (`ei23 dc`) – Starts/restarts containers
- **Docker Updates** (`ei23 du`) – Pulls new images
- **Backups** (`ei23 backup`) – Backs up important data
- **Shortcuts** (`ei23 -h`) – Shows all commands

**Language system:** The script uses `de-file.txt` / `en-file.txt` for all user-facing strings. The placeholder `LANGFILE_PLACEHOLDER` gets replaced with the actual language file content.

### 2. `ei23-docker/` - The Docker Environment

This entire directory gets copied to the user's home directory during installation. Key files:

- **`docker-compose.yml`** – Generated from templates, contains all services
- **`compose_templates/`** – One YAML file per service, users copy these into docker-compose.yml
- **`volumes/ei23/`** – The dashboard/supervisor Python application

### 3. `ei23-docker/volumes/ei23/ei23-supervisor.py` - The Dashboard

A Python Flask server (running with Waitress) that provides:

- **Main dashboard** (`/`) – Program tiles, linked to services
- **Server page** (`/server`) – Container management, resource monitoring, server actions
- **Network page** (`/localnet`) – ARP-scan based network discovery
- **Storage page** (`/tree`) – Disk usage visualization
- **API endpoints** – `/api/programs`, `/api/compose-templates`, `/api/resources`, etc.
- **Server-Sent Events (SSE)** – Real-time terminal output for server actions

Runs as systemd service `ei23.service`.

### 4. `DOCS/` - Documentation

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/):

- **DE/** and **EN/** are mirrors – changes in one should be reflected in the other
- Each software has its own markdown file in `software/`
- Navigation defined in `mkdocs.yml`
- Built via `ei23 docs` command

---

## 📋 Conventions & Guidelines

### Docker Compose Templates

When adding a new template:

1. Create `ei23-docker/compose_templates/[servicename].yml`
2. Use descriptive container names
3. Include `restart: unless-stopped` or `restart: always`
4. Use relative paths for volumes: `./volumes/[service]/...`
5. Use `password_placeholder` for passwords (script replaces these)
6. Add environment variable `TZ=Europe/Berlin` where applicable
7. Add comments for configuration options

Example structure:
```yaml
  servicename:
    image: author/image:latest
    container_name: servicename
    restart: unless-stopped
    ports:
      - "HOST_PORT:CONTAINER_PORT"
    volumes:
      - ./volumes/servicename:/data
    environment:
      - TZ=Europe/Berlin
      - PASSWORD=password_placeholder
```

### Documentation

When adding new software:

1. Create `DOCS/DE/docs/software/[name].md`
2. Create `DOCS/EN/docs/software/[name].md` (English translation)
3. Add entries to both `DOCS/DE/mkdocs.yml` and `DOCS/EN/mkdocs.yml`
4. Follow the template structure:
   - Title + description
   - Personal recommendation (if applicable)
   - Installation (template)
   - Features
   - First start
   - Notes
   - Further information links

### Personal Recommendations

The project maintainer (Felix) has personal preferences that should be documented:

- **llama-swap** over Ollama (better performance, more control)
- **Node-RED** over n8n (more powerful, better HA integration)
- **Portfolio Performance** over Ghostfolio (more detailed, offline)
- **PostgreSQL** over InfluxDB (future-proof, "Postgres for everything")

When documenting these tools, include a tip box with the recommendation.

### Language

- **Code & Comments:** English
- **User-facing strings:** German (primary), English (translation)
- **Documentation:** Both DE and EN (keep in sync)
- **Commit messages:** English preferred

---

## 🤝 How to Contribute

### What's Welcome

1. **Documentation improvements** – Fix typos, add clarity, translate
2. **New compose templates** – Add support for more services
3. **Bug fixes** – In scripts or documentation
4. **Dashboard icons** – 128x128 PNG with transparent background
5. **Feature suggestions** – Via GitHub Issues

### What to Avoid

- Don't break existing installations
- Don't add cloud dependencies or telemetry
- Don't change the simple, user-friendly interface
- Don't add complexity without clear benefit

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test if possible
5. Submit a pull request
6. Be patient – this is a solo project

---

## 🧠 For AI Assistants

If you're an AI assistant working on this project, here's what you should know:

### Key Files to Understand

1. **`ei23.sh`** – The main script, ~1000 lines of Bash
2. **`ei23-docker/volumes/ei23/ei23-supervisor.py`** – The dashboard, ~500 lines of Python
3. **`DOCS/DE/mkdocs.yml`** – Documentation navigation
4. **`DOCS/DE/docs/index.md`** – Landing page with mission statement

### When Making Changes

- **Documentation:** Always update both DE and EN versions
- **Templates:** Follow existing patterns in `compose_templates/`
- **Script:** Be careful with `ei23.sh` – it's the main user interface
- **Dashboard:** The supervisor uses Flask + Jinja2 templates

### Common Tasks

**Adding a new Docker service:**
1. Create template in `ei23-docker/compose_templates/[name].yml`
2. Create docs in `DOCS/DE/docs/software/[name].md`
3. Create docs in `DOCS/EN/docs/software/[name].md`
4. Update both `mkdocs.yml` files
5. Add to overview in `software/overview.md` (both DE and EN)

**Updating documentation:**
1. Edit the DE version first
2. Translate to EN
3. Update navigation in `mkdocs.yml` if needed

**Modifying the dashboard:**
1. Main logic: `ei23-docker/volumes/ei23/ei23-supervisor.py`
2. Templates: `ei23-docker/volumes/ei23/web/*.html`
3. Static files: `ei23-docker/volumes/ei23/web/static/`

---

## 📊 Project Statistics

- **90+ Docker Compose templates**
- **53 documentation pages** (DE + EN)
- **Supported OS:** Debian, Raspberry Pi OS, Ubuntu, Pop!_OS, Fedora, CentOS, Rocky, Arch/Manjaro
- **Supported architectures:** armv7, arm64, amd64
- **License:** See LICENSE file
- **Maintainer:** Felix (ei23)

---

## 🔗 Links

- **Website:** [ei23.de](https://ei23.de) (DE) / [ei23.com](https://ei23.com) (EN)
- **Documentation:** [diy-smart-home.ei23.de](https://diy-smart-home.ei23.de) (DE) / [diy-smart-home.ei23.com](https://diy-smart-home.ei23.com) (EN)
- **GitHub:** [github.com/ei23com/diy-smart-home](https://github.com/ei23com/diy-smart-home)
- **YouTube:** [youtube.com/ei23-de](https://youtube.com/ei23-de)
- **Discord:** [discord.gg/pS9cZTBUfs](https://discord.gg/pS9cZTBUfs)
- **Telegram:** [t.me/ei23de](https://t.me/ei23de)
- **Forum:** [forum.ei23.de](https://forum.ei23.de/)
- **Donations:** [ei23.de/donate](https://ei23.de/donate/)

---

## 💡 Remember

> **The goal is not to build the most complex smart home. The goal is to build YOUR smart home – simple, reliable, and under YOUR control.**

Don't let them take away your control. 🏠🔓
