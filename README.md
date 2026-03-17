# The ei23 DIY Smart Home (Server)

A dead-easy, clean and slim **installation** and **maintenance** tool for a huge amount of Docker-based home automation and media software, easily accessible on a clean, slim and customizable web dashboard.

**Supports:** Debian, Raspberry Pi OS, Ubuntu, Pop!_OS, Fedora, CentOS, Rocky, Arch/Manjaro | **Architectures:** armv7, arm64, amd64

Maybe it's not as easy to configure as the Home Assistant OS, but you get a lot more customization options and get in touch with the docker-compose.yml notation, which is also a great tool.
And you don't even have to use Home Assistant if you prefer OpenHAB or IObroker for example. All on one system.

**Have fun, get smart and independent!**

![ei23 Dashboard](https://ei23.de/bilder/ei23-terminal.gif)

![ei23 Counter](https://ei23.de/bilder/svg-stats.svg)

---

## ✨ Features

- 🚀 **One-Command Installation** - Script handles everything
- 🐳 **Docker-Based** - 90+ pre-configured templates
- 📊 **Web Dashboard** - Live monitoring, container management, template installer
- 🔄 **Easy Updates** - `ei23 update` for full system update
- 💾 **Backup System** - Integrated backup for all services
- 🌐 **Multi-OS** - Debian, Ubuntu, Fedora, Arch, and more
- 🏠 **Multi-Arch** - ARM (32/64-bit) and x86-64 support

![ei23 Dashboard](https://ei23.de/bilder/ei23-dashboard.jpg)

---

## 📦 What's Included

### Smart Home & IoT
[Home Assistant](https://www.home-assistant.io/) · [Node-RED](https://nodered.org/) · [ESPHome](https://esphome.io/) · [Mosquitto](https://mosquitto.org/) · [Zigbee2MQTT](https://www.zigbee2mqtt.io/)

### Media & Entertainment
[Jellyfin](https://jellyfin.org/) · [Immich](https://immich.app/) · [Lyrion Music Server](https://lyrion.org/) · [Music Assistant](https://music-assistant.io/)

### AI & Machine Learning
[llama-swap](https://github.com/mostlygeek/llama-swap) · [Ollama](https://ollama.ai/) · [Open WebUI](https://openwebui.com/) · [LiteLLM](https://litellm.ai/) · [Frigate](https://frigate.video/)

### Productivity
[Nextcloud](https://nextcloud.com/) · [Paperless-ngx](https://docs.paperless-ngx.com/) · [Mealie](https://mealie.io/) · [FreshRSS](https://freshrss.org/) · [ArchiveBox](https://archivebox.io/) · [NocoDB](https://nocodb.com/) · [Stirling-PDF](https://github.com/Frooodle/Stirling-PDF) · [Syncthing](https://syncthing.net/) · [PairDrop](https://pairdrop.net/)

### Security & Infrastructure
[Vaultwarden](https://github.com/dani-garcia/vaultwarden) · [Traefik](https://traefik.io/) · [WireGuard](https://www.wireguard.com/) · [AdGuard Home](https://adguard.com/en/adguard-home/overview.html) · [Duplicati](https://www.duplicati.com/)

### Telephony
[FreePBX / Asterisk](https://www.freepbx.org/)

### Monitoring & Data
[Grafana](https://grafana.com/) · [InfluxDB](https://www.influxdata.com/) · [Uptime Kuma](https://uptime.kuma.pet/) · [Portainer](https://www.portainer.io/)

**And many more...** Have a look in the [compose_templates](ei23-docker/compose_templates) folder!

---

## 🖥️ Supported Hardware

| Hardware | Price | Power | Performance | Recommendation |
|----------|-------|-------|-------------|----------------|
| **Raspberry Pi 4/5** | 50-80€ | 3-8W | Good | For light use |
| **Intel N100 Mini-PC** | ~150€ | 6-10W | Very Good | ⭐ Recommended |
| **HP/Dell/Lenovo ThinClient** | 50-100€ | 10-25W | Excellent | ⭐ Best value |
| **Intel NUC (i3/i5)** | 200-400€ | 15-35W | Superior | For demanding use |

> 💡 **Mini-PCs recommended:** For best performance per watt, we recommend used ThinClients or Mini-PCs with x86 architecture. They support all Docker images and offer significantly more power than Raspberry Pis.

---

## 📖 Documentation

- 🇩🇪 **[German Docs](https://diy-smart-home.ei23.de)** - Complete documentation in German
- 🇬🇧 **[English Docs](https://diy-smart-home.ei23.com)** - Complete documentation in English

---

## 🚀 Installation

### Easy Installation:

After registering for the newsletter, you'll receive two commands to execute via SSH:

1. **[English Newsletter](https://ei23.com/newsletter)** / **[German Newsletter](https://ei23.de/newsletter)**
2. Execute the received commands on your server
3. Follow the interactive menu

*Why newsletter?*
- Security updates and important announcements
- Community building
- Support the project
- Your email stays private (trash mail is fine!)

The script downloads a USERID for updates and sets the correct language file based on your newsletter choice.

### Manual Installation:
1. Clone the files to a folder.
2. Insert the language file of your choice (de-file.txt / en-file.txt) into [ei23.sh](ei23.sh) and replace "LANGFILE_PLACEHOLDER"
3. Install a fresh Debian / Rasbian system, login via ssh or terminal and create a user like this "useradd -m ei23" (or another name)
4. Copy the entire "ei23-docker" folder into your users home directory (with root privileges)
5. Copy the [ei23.sh](ei23.sh) into your user home directory
6. run "bash [ei23.sh](ei23.sh) part1"
7. follow instructions
8. after you done the reboot, run "ei23", the script then will finish the installation


- ei23 updates won't work with manual installation (USERID from newsletter is needed)
- you won't see a version number and will not get info about new versions (USERID from newsletter is needed)
- everything else works like normal

**Note:** Manual installation doesn't support auto-updates (USERID required).

---

## 🎛️ Dashboard

The ei23 Dashboard is a full **server supervisor** with:

- 📊 **Live Monitoring** - CPU, RAM, Disk usage in real-time
- 🐳 **Container Management** - View status, access web interfaces
- 📋 **Template Manager** - Install new programs with one click
- ✏️ **Program Editor** - Drag & drop dashboard customization
- 🖥️ **Server Actions** - Updates, backups, reboots with live terminal
- 🌐 **Network Scanner** - Discover devices on your network

Access: `http://[your-server-ip]`

---

## 🔧 Common Commands

```bash
ei23                  # Open menu
ei23 update           # Full system update
ei23 dc               # Docker Compose (restart containers)
ei23 du               # Docker Update (pull new images)
ei23 backup           # Create backup
ei23 dstats           # Show Docker container status
ei23 docs             # Build documentation
ei23 -h               # Show all shortcuts
```

---

## 🤝 Contributing

Pull requests are welcome! You can:

- Edit or add [documentation files](DOCS/guidelines.md)
- Add new [compose templates](ei23-docker/compose_templates)
- Add dashboard icons (128x128 PNG with transparent background)

---

## 🌟 Great Open Source Projects

I love open source projects - [here is my best of list](https://ei23.com/opensource/)

Consider supporting them!

---

## 👥 Community

[![YouTube](https://img.shields.io/badge/YouTube-ei23-red?style=for-the-badge&logo=youtube)](https://youtube.com/ei23-de)
[![Discord](https://img.shields.io/badge/Discord-ei23-blue?style=for-the-badge&logo=discord)](https://discord.gg/pS9cZTBUfs)
[![Telegram](https://img.shields.io/badge/Telegram-ei23_DE-blue?style=for-the-badge&logo=telegram)](https://t.me/ei23de)
[![Forum](https://img.shields.io/badge/Forum-ei23-orange?style=for-the-badge)](https://forum.ei23.de/)

---

## 💰 Donations

[![Donate EN](https://img.shields.io/badge/Donate-EN-green?style=for-the-badge)](https://ei23.com/donate/)
[![Donate DE](https://img.shields.io/badge/Donate-DE-green?style=for-the-badge)](https://ei23.de/donate/)

You can expect special perks there. Thanks!

---

## 📄 License

This project is licensed - see [LICENSE](LICENSE) for details.
