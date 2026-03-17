# Overview - Recommended Software & Programs

This page gives you an overview of all Docker containers available with the ei23 script as well as other recommended software for your Smart Home and Home Lab.

## 🏠 Smart Home & IoT

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [Home Assistant](homeassistant.md) | Central smart home platform | 8123 | ✅ |
| [Node-RED](nodered.md) | Visual programming for automations | 1880 | ⚡ Native |
| [ESPHome](esphome.md) | Firmware for ESP devices | 6052 | ✅ |
| [Mosquitto](../start/faq) | MQTT broker | 1883 | ✅ |
| [MQTT Explorer](mqttexplorer.md) | MQTT client GUI | 4004 | ✅ |
| [go2rtc](go2rtc.md) | RTSP/WebRTC stream server | 1984 | ✅ |

## 📹 Monitoring & Cameras

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [Frigate](frigate.md) | NVR with AI detection | 5000 | ✅ |
| [Uptime Kuma](uptimekuma.md) | Service monitoring | 3001 | ✅ |

## 🎬 Media & Entertainment

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [Jellyfin](jellyfin.md) | Media server | 8096 | ✅ |
| [Immich](immich.md) | Photo cloud | 2283 | ✅ |
| [Lyrion Music Server](lms.md) | Multi-room audio | 9000 | ✅ |
| [Music Assistant](music-assistant.md) | Multi-room audio (HA) | 8095 | ✅ |

## 🤖 AI & Machine Learning

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [llama-swap](llama-swap.md) | Local LLMs (llama.cpp) | 9292 | ✅ |
| [Ollama](ollama.md) | Local LLMs | 11434 | ✅ |
| [Open WebUI](open-webui.md) | Chat UI for LLMs | 2280 | ✅ |
| [LiteLLM](litellm.md) | LLM API proxy | 4000 | ✅ |

## 📊 Data & Visualization

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [Grafana](grafana.md) | Dashboard & visualization | 3000 | ✅ |
| [InfluxDB](influx.md) | Time-series database | 8086 | ✅ |

## 📁 Productivity & Office

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [Nextcloud](nextcloud.md) | Cloud storage | 8080 | ✅ |
| [PaperlessNGX](paperlessngx.md) | Document management | 8010 | ✅ |
| [Mealie](mealie.md) | Recipe manager | 9925 | ✅ |
| [FreshRSS](freshrss.md) | RSS reader | 2224 | ✅ |
| [ArchiveBox](archivebox.md) | Web page archiving | 8085 | ✅ |
| [NocoDB](nocodb.md) | Database UI (Airtable) | 2289 | ✅ |
| [Stirling-PDF](stirling-pdf.md) | PDF tools | 2223 | ✅ |
| [Syncthing](syncthing.md) | File synchronization | 8384 | ✅ |
| [PairDrop](pairdrop.md) | File sharing (AirDrop) | 3010 | ✅ |

## 💰 Finance

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [Firefly III](fireflyiii.md) | Finance manager | 2225 | ✅ |
| [Ghostfolio](ghostfolio.md) | Portfolio management | 3333 | ✅ |

## 🔒 Security & Infrastructure

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [Vaultwarden](vaultwarden.md) | Password manager (Bitwarden) | 8812 | ✅ |
| [Traefik](traefik.md) | Reverse proxy with SSL | 80/443 | ✅ |
| [Nginx Proxy Manager](nginxproxy.md) | Reverse proxy | 81 | ✅ |
| [WireGuard](wireguard.md) | VPN server | 51820 | ✅ |
| [AdGuard Home](adguardhome.md) | DNS ad blocker | 53/3001 | ✅ |
| [Duplicati](duplicati.md) | Encrypted backups | 8200 | ✅ |

## 💻 Development

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [VSCode Server](vscode.md) | Browser code editor | 8443 | ✅ |
| [Portainer](portainer.md) | Docker management | 9000 | ✅ |

## 📞 Telephony

| Program | Description | Port | Docker |
|---------|-------------|------|--------|
| [FreePBX / Asterisk](freepbx.md) | VoIP phone system | 2233 | ✅ |

---

## 📋 More Recommended Software

In addition to the Docker programs, there are many other useful programs for Smart Home and Home Lab:

### 🌐 Web Browsers, News Feeds, Calendar & Email

| Program | Description | Link |
|---------|-------------|------|
| **Firefox** | Web browser | [mozilla.org/firefox](https://www.mozilla.org/firefox/) |
| **Chromium** | Web browser (Open Source Chrome) | [chromium.org](https://www.chromium.org/) |
| **Thunderbird** | Email client with calendar | [mozilla.org/thunderbird](https://www.mozilla.org/thunderbird/) |
| **K-9 Mail** | Android email client | [k9mail.app](https://k9mail.app/) |
| **DAVx5** | Android calendar sync | [davx5.com](https://www.davx5.com/) |
| **Flym** | Android RSS feed reader | [GitHub](https://github.com/FredJul/Flym) |

### 🎵 Media Playback & Editing

| Program | Description | Link |
|---------|-------------|------|
| **VLC** | Media player (all formats) | [videolan.org](https://www.videolan.org/vlc/) |
| **Kodi** | Media center | [kodi.tv](https://kodi.tv/) |
| **Audacity** | Audio editing | [audacityteam.org](https://www.audacityteam.org/) |
| **OBS Studio** | Streaming and recording | [obsproject.com](https://obsproject.com/) |
| **Shotcut** | Video editing | [shotcut.org](https://www.shotcut.org/) |
| **FFmpeg** | Multimedia framework (CLI) | [ffmpeg.org](https://www.ffmpeg.org/) |

### 📝 Text Editors, Notes & Development

| Program | Description | Link |
|---------|-------------|------|
| **VSCodium** | FOSS VSCode (Code editor) | [vscodium.com](https://vscodium.com/) |
| **Obsidian** | Markdown notes | [obsidian.md](https://obsidian.md/) |
| **LibreOffice** | Office suite | [libreoffice.org](https://libreoffice.org) |
| **Arduino IDE** | Development for Arduino | [arduino.cc](https://www.arduino.cc/en/software) |
| **ACode** | Android code editor | [acode.app](https://acode.app/) |

### 🎨 Graphics & Design

| Program | Description | Link |
|---------|-------------|------|
| **GIMP** | Image editing | [gimp.org](https://www.gimp.org/) |
| **Inkscape** | Vector graphics | [inkscape.org](https://inkscape.org/) |
| **Krita** | Digital painting | [krita.org](https://krita.org/) |
| **Blender** | 3D modeling | [blender.org](https://www.blender.org/) |
| **Excalidraw** | Browser drawing tool (collaborative) | [excalidraw.com](https://excalidraw.com/) |

### 🔐 Security & Encryption

| Program | Description | Link |
|---------|-------------|------|
| **KeePass** | Password manager (local) | [keepass.info](https://keepass.info/) |
| **VeraCrypt** | Data encryption | [veracrypt.fr](https://www.veracrypt.fr/) |
| **Aegis** | Android 2FA authenticator | [getaegis.app](https://getaegis.app/) |

### 📁 File Synchronization & Backup

| Program | Description | Link |
|---------|-------------|------|
| **FreeFileSync** | File synchronization | [freefilesync.org](https://freefilesync.org/) |
| **Kopia** | Backup tool | [kopia.io](https://kopia.io/) |
| **Rsync** | File synchronization (CLI) | [rsync.samba.org](https://rsync.samba.org/) |
| **Unison** | Bidirectional synchronization | [cis.upenn.edu](https://www.cis.upenn.edu/~bcpierce/unison/) |
| **7-Zip** | Archiving software | [7-zip.org](https://www.7-zip.org/) |
| **WinSCP** | FTP/SFTP client | [winscp.net](https://winscp.net/) |

### 🖥️ Remote Desktop & SSH

| Program | Description | Link |
|---------|-------------|------|
| **PuTTY** | SSH client (Windows) | [putty.org](https://www.putty.org/) |
| **ConnectBot** | Android SSH client | [connectbot.org](https://connectbot.org/) |
| **VNC Viewer** | Remote desktop | [realvnc.com](https://www.realvnc.com/) |

### 🖨️ 3D Printing

| Program | Description | Link |
|---------|-------------|------|
| **Octoprint** | 3D printer remote control | [octoprint.org](https://octoprint.org/) |
| **Prusa Slicer** | 3D printing slicer | [prusa3d.com](https://www.prusa3d.com/) |
| **Ultimaker Cura** | 3D printing slicer | [ultimaker.com](https://ultimaker.com/software/ultimaker-cura) |

### 🔧 Web Servers & Server Software

| Program | Description | Link |
|---------|-------------|------|
| **Nginx** | Web server | [nginx.org](https://nginx.org/) |
| **Apache** | Web server | [httpd.apache.org](https://httpd.apache.org/) |
| **MySQL/MariaDB** | Database | [mariadb.org](https://mariadb.org/) |
| **PostgreSQL** | Database | [postgresql.org](https://www.postgresql.org/) |
| **Samba** | File sharing | [samba.org](https://www.samba.org/) |
| **OpenSSH** | SSH server | [openssh.com](https://www.openssh.com/) |

### 📚 Documentation & Content Management

| Program | Description | Link |
|---------|-------------|------|
| **MkDocs** | Static documentation | [mkdocs.org](https://www.mkdocs.org/) |
| **MkDocs Material** | Modern MkDocs theme | [squidfunk.github.io](https://squidfunk.github.io/mkdocs-material/) |
| **WordPress** | Blog / Website | [wordpress.org](https://wordpress.org/) |
| **Kiwix** | Offline Wikipedia | [kiwix.org](https://www.kiwix.org/) |

### 🗣️ Speech Technology

| Program | Description | Link |
|---------|-------------|------|
| **Faster-Whisper** | Speech-to-Text (STT) | [GitHub](https://github.com/guillaumekln/faster-whisper/) |
| **Piper TTS** | Text-to-Speech (TTS) | [GitHub](https://github.com/rhasspy/piper) |

### 🐧 System & Virtualization

| Program | Description | Link |
|---------|-------------|------|
| **Debian Linux** | Linux distribution | [debian.org](https://www.debian.org/) |
| **Proxmox** | Server virtualization | [proxmox.com](https://www.proxmox.com/) |
| **Fail2Ban** | Intrusion prevention | [fail2ban.org](https://www.fail2ban.org/) |
| **UFW** | Uncomplicated Firewall | [launchpad.net](https://launchpad.net/ufw) |

---

!!!tip "Suggest a Program"
    Missing a program? Create an [issue on GitHub](https://github.com/ei23com/diy-smart-home/issues) or [pull request](https://github.com/ei23com/diy-smart-home/pulls)!

!!!note "Non-Docker Programs"
    [Node-RED](nodered.md) and [RTL-SDR](../start/faq) are installed natively, not as Docker containers.
