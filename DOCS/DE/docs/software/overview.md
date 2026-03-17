# Überblick - Empfohlene Software & Programme

Diese Seite gibt dir einen Überblick über alle mit dem ei23-Skript verfügbaren Docker-Container sowie weitere empfohlene Software für dein Smart Home und Home Lab.

## 🏠 Smart Home & IoT

| Programm | Beschreibung | Port | Docker |
|----------|--------------|------|--------|
| [Home Assistant](homeassistant.md) | Zentrale Smart Home Plattform | 8123 | ✅ |
| [NodeRED](nodered.md) | Visual Programming für Automatisierungen | 1880 | ⚡ Nativ |
| [ESPHome](esphome.md) | Firmware für ESP-Geräte | 6052 | ✅ |
| [Mosquitto](../start/faq) | MQTT Broker | 1883 | ✅ |
| [MQTT Explorer](mqttexplorer.md) | MQTT Client GUI | 4004 | ✅ |
| [go2rtc](go2rtc.md) | RTSP/WebRTC Stream Server | 1984 | ✅ |

## 📹 Überwachung & Kameras

| Programm | Beschreibung | Port | Docker |
|----------|--------------|------|--------|
| [Frigate](frigate.md) | NVR mit KI-Erkennung | 5000 | ✅ |
| [Uptime Kuma](uptimekuma.md) | Service-Monitoring | 3001 | ✅ |

## 🎬 Medien & Unterhaltung

| Programm | Beschreibung | Port | Docker |
|----------|--------------|------|--------|
| [Jellyfin](jellyfin.md) | Media Server | 8096 | ✅ |
| [Immich](immich.md) | Foto-Cloud | 2283 | ✅ |
| [Lyrion Music Server](lms.md) | Multi-Room Audio | 9000 | ✅ |
| [Music Assistant](music-assistant.md) | Multi-Room Audio (HA) | 8095 | ✅ |

## 🤖 KI & Machine Learning

| Programm | Beschreibung | Port | Docker |
|----------|--------------|------|--------|
| [llama-swap](llama-swap.md) | Lokale LLMs (llama.cpp) | 9292 | ✅ |
| [Ollama](ollama.md) | Lokale LLMs | 11434 | ✅ |
| [Open WebUI](open-webui.md) | Chat-Oberfläche für LLMs | 2280 | ✅ |
| [LiteLLM](litellm.md) | LLM-API-Proxy | 4000 | ✅ |

## 📊 Daten & Visualisierung

| Programm | Beschreibung | Port | Docker | Empfehlung |
|----------|--------------|------|--------|------------|
| [Grafana](grafana.md) | Dashboard & Visualisierung | 3000 | ✅ | ⭐ Empfohlen |
| [InfluxDB](influx.md) | Time-Series Datenbank | 8086 | ✅ | ⚠️ Nur für Bestandsinstallationen |
| PostgreSQL | Relationale Datenbank | 5432 | ✅ | ⭐ Für neue Projekte empfohlen |

!!!tip "PostgreSQL statt InfluxDB"
    Für neue Projekte empfehle ich **PostgreSQL** (ggf. mit TimescaleDB-Erweiterung) statt InfluxDB. PostgreSQL ist zukunftssicher, universell einsetzbar und wird von vielen Tools nativ unterstützt. ["Postgres for Everything"](https://www.amazingcto.com/postgres-for-everything/)!

## 📁 Produktivität & Büro

| Programm | Beschreibung | Port | Docker |
|----------|--------------|------|--------|
| [Nextcloud](nextcloud.md) | Cloud-Speicher | 8080 | ✅ |
| [PaperlessNGX](paperlessngx.md) | Dokumentenmanagement | 8010 | ✅ |
| [Mealie](mealie.md) | Rezept-Manager | 9925 | ✅ |
| [FreshRSS](freshrss.md) | RSS-Reader | 2224 | ✅ |
| [ArchiveBox](archivebox.md) | Webseiten-Archivierung | 8085 | ✅ |
| [NocoDB](nocodb.md) | Datenbank-Oberfläche (Airtable) | 2289 | ✅ |
| [Stirling-PDF](stirling-pdf.md) | PDF-Werkzeuge | 2223 | ✅ |
| [Syncthing](syncthing.md) | Datei-Synchronisation | 8384 | ✅ |
| [PairDrop](pairdrop.md) | Dateien teilen (AirDrop) | 3010 | ✅ |

## 💰 Finanzen

| Programm | Beschreibung | Port | Docker |
|----------|--------------|------|--------|
| [Firefly III](fireflyiii.md) | Finanzmanager | 2225 | ✅ |
| [Ghostfolio](ghostfolio.md) | Vermögensverwaltung | 3333 | ✅ |

## 🔒 Sicherheit & Infrastruktur

| Programm | Beschreibung | Port | Docker |
|----------|--------------|------|--------|
| [Vaultwarden](vaultwarden.md) | Passwort-Manager (Bitwarden) | 8812 | ✅ |
| [Traefik](traefik.md) | Reverse Proxy mit SSL | 80/443 | ✅ |
| [Nginx Proxy Manager](nginxproxy.md) | Reverse Proxy | 81 | ✅ |
| [WireGuard](wireguard.md) | VPN Server | 51820 | ✅ |
| [AdGuard Home](adguardhome.md) | DNS-Werbeblocker | 53/3001 | ✅ |
| [Duplicati](duplicati.md) | Verschlüsselte Backups | 8200 | ✅ |

## 💻 Entwicklung

| Programm | Beschreibung | Port | Docker |
|----------|--------------|------|--------|
| [VSCode Server](vscode.md) | Browser-Code-Editor | 8443 | ✅ |
| [Portainer](portainer.md) | Docker Verwaltung | 9000 | ✅ |

## 📞 Telefonie

| Programm | Beschreibung | Port | Docker |
|----------|--------------|------|--------|
| [FreePBX / Asterisk](freepbx.md) | VoIP Telefonanlage | 2233 | ✅ |

---

## 📋 Weitere empfohlene Software

Neben den Docker-Programmen gibt es viele weitere nützliche Programme für das Smart Home und Home Lab:

### 🌐 Webbrowser, Newsfeed, Kalender und E-Mail

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **Firefox** | Webbrowser | [mozilla.org/firefox](https://www.mozilla.org/firefox/) |
| **Chromium** | Webbrowser (Open Source Chrome) | [chromium.org](https://www.chromium.org/) |
| **Thunderbird** | E-Mail-Client mit Kalender | [mozilla.org/thunderbird](https://www.mozilla.org/thunderbird/) |
| **K-9 Mail** | Android E-Mail-Client | [k9mail.app](https://k9mail.app/) |
| **DAVx5** | Android Kalendersynchronisierung | [davx5.com](https://www.davx5.com/) |
| **Flym** | Android RSS Feed Reader | [GitHub](https://github.com/FredJul/Flym) |

### 🎵 Medienwiedergabe und Bearbeitung

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **VLC** | Medienplayer (alle Formate) | [videolan.org](https://www.videolan.org/vlc/) |
| **Kodi** | Medien-Center | [kodi.tv](https://kodi.tv/) |
| **Audacity** | Audio-Bearbeitung | [audacityteam.org](https://www.audacityteam.org/) |
| **OBS Studio** | Streaming und Aufnahme | [obsproject.com](https://obsproject.com/) |
| **Shotcut** | Videobearbeitung | [shotcut.org](https://www.shotcut.org/) |
| **FFmpeg** | Multimedia-Framework (CLI) | [ffmpeg.org](https://www.ffmpeg.org/) |

### 📝 Texteditoren, Notizen und Entwicklung

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **VSCodium** | FOSS VSCode (Code-Editor) | [vscodium.com](https://vscodium.com/) |
| **Obsidian** | Markdown-Notizen | [obsidian.md](https://obsidian.md/) |
| **LibreOffice** | Office Suite | [libreoffice.org](https://libreoffice.org) |
| **Arduino IDE** | Entwicklung für Arduino | [arduino.cc](https://www.arduino.cc/en/software) |
| **ACode** | Android Code Editor | [acode.app](https://acode.app/) |

### 🎨 Grafik und Design

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **GIMP** | Bildbearbeitung | [gimp.org](https://www.gimp.org/) |
| **Inkscape** | Vektorgrafik | [inkscape.org](https://inkscape.org/) |
| **Krita** | Digitales Malen | [krita.org](https://krita.org/) |
| **Blender** | 3D-Modellierung | [blender.org](https://www.blender.org/) |
| **Excalidraw** | Browser-Zeichentool (kollaborativ) | [excalidraw.com](https://excalidraw.com/) |

### 🔐 Sicherheit und Verschlüsselung

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **KeePass** | Passwort-Manager (lokal) | [keepass.info](https://keepass.info/) |
| **VeraCrypt** | Datenverschlüsselung | [veracrypt.fr](https://www.veracrypt.fr/) |
| **Aegis** | Android 2FA-Authenticator | [getaegis.app](https://getaegis.app/) |

### 📁 Dateisynchronisierung und Backup

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **FreeFileSync** | Dateisynchronisation | [freefilesync.org](https://freefilesync.org/) |
| **Kopia** | Backup-Tool | [kopia.io](https://kopia.io/) |
| **Rsync** | Dateisynchronisierung (CLI) | [rsync.samba.org](https://rsync.samba.org/) |
| **Unison** | Bidirektionale Synchronisation | [cis.upenn.edu](https://www.cis.upenn.edu/~bcpierce/unison/) |
| **7-Zip** | Archivierungssoftware | [7-zip.org](https://www.7-zip.org/) |
| **WinSCP** | FTP/SFTP Client | [winscp.net](https://winscp.net/) |

### 🖥️ Remote-Desktop und SSH

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **PuTTY** | SSH-Client (Windows) | [putty.org](https://www.putty.org/) |
| **ConnectBot** | Android SSH Client | [connectbot.org](https://connectbot.org/) |
| **VNC Viewer** | Remote-Desktop | [realvnc.com](https://www.realvnc.com/) |

### 🖨️ 3D-Druck

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **Octoprint** | 3D-Drucker Fernsteuerung | [octoprint.org](https://octoprint.org/) |
| **Prusa Slicer** | 3D-Druck Slicer | [prusa3d.com](https://www.prusa3d.com/) |
| **Ultimaker Cura** | 3D-Druck Slicer | [ultimaker.com](https://ultimaker.com/software/ultimaker-cura) |

### 🔧 Webserver und Server-Software

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **Nginx** | Webserver | [nginx.org](https://nginx.org/) |
| **Apache** | Webserver | [httpd.apache.org](https://httpd.apache.org/) |
| **MySQL/MariaDB** | Datenbank | [mariadb.org](https://mariadb.org/) |
| **PostgreSQL** | Datenbank | [postgresql.org](https://www.postgresql.org/) |
| **Samba** | Dateifreigabe | [samba.org](https://www.samba.org/) |
| **OpenSSH** | SSH-Server | [openssh.com](https://www.openssh.com/) |

### 📚 Doku und Content Management

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **MkDocs** | Statische Dokumentation | [mkdocs.org](https://www.mkdocs.org/) |
| **MkDocs Material** | Modernes MkDocs Theme | [squidfunk.github.io](https://squidfunk.github.io/mkdocs-material/) |
| **WordPress** | Blog / Website | [wordpress.org](https://wordpress.org/) |
| **Kiwix** | Offline Wikipedia | [kiwix.org](https://www.kiwix.org/) |

### 🗣️ Sprachtechnologie

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **Faster-Whisper** | Speech-to-Text (STT) | [GitHub](https://github.com/guillaumekln/faster-whisper/) |
| **Piper TTS** | Text-to-Speech (TTS) | [GitHub](https://github.com/rhasspy/piper) |

### 🐧 System und Virtualisierung

| Programm | Beschreibung | Link |
|----------|--------------|------|
| **Debian Linux** | Linux-Distribution | [debian.org](https://www.debian.org/) |
| **Proxmox** | Server-Virtualisierung | [proxmox.com](https://www.proxmox.com/) |
| **Fail2Ban** | Intrusion Prevention | [fail2ban.org](https://www.fail2ban.org/) |
| **UFW** | Uncomplicated Firewall | [launchpad.net](https://launchpad.net/ufw) |

---

!!!tip "Programm vorschlagen"
    Vermmisst du ein Programm? Erstelle ein [Issue auf GitHub](https://github.com/ei23com/diy-smart-home/issues) oder [pull request](https://github.com/ei23com/diy-smart-home/pulls)!

!!!note "Nicht-Docker Programme"
    [NodeRED](nodered.md) und [RTL-SDR](../start/faq) werden nativ installiert und nicht als Docker Container.
