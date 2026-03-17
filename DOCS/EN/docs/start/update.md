## Changelog


### v1.20
#### What's New? Documentation Update 🎉
- **Completely revised documentation** (DE + EN) - All pages up to date
- **New software documentation:**
  - ArchiveBox, Firefly III, Frigate NVR, FreshRSS, Ghostfolio, go2rtc
  - Jellyfin, llama-swap, Mealie, n8n, NocoDB
  - Ollama & Open WebUI (separated), Portainer, Syncthing
- **Hardware documentation created:**
  - Server recommendations: Mini-PCs/ThinClients vs. Raspberry Pi (performance/watt comparison)
  - Hardware structure with architecture diagrams
  - Edge devices overview (Zigbee, WLAN, ESPHome, 433MHz)
- **Dashboard documentation updated:**
  - Live resources (CPU/RAM/Disk) with real-time bars
  - Server actions with SSE terminal output
  - Template manager for Docker programs
  - Program editor with drag & drop
  - Session badges and reconnect functionality
- **Security & Monitoring completely revised:**
  - Firewall (UFW) configuration
  - Secure SSH (key auth, Fail2Ban)
  - Monitoring with Uptime Kuma
  - Security checklist
- **Translation update:** All new pages also available in English

### v1.12
#### What's New?
- Bugfixes: Improved installation and fixed issues with icons/links on the ei23 Dashboard
- Extended OS support: Ubuntu, Pop!_OS, Fedora, CentOS, Rocky, Arch/Manjaro
- New Docker Templates: fooocus, archivebox, llama-swap, openedai-speech, pairdrop, perplexica, watchyourlan, whisper-webui
- More new templates: ai-toolkit, blocky, duplicati, fireflyiii, freepbx-asterisk, freshrss, frigate, ghostfolio, gitlab, go2rtc, grocy, heimdall, homeassistant-matterserver, homebridge, homegear, jellyfin, litellm, ollama, lyrionmusicserver, matchering, mealie, music-assistant-server, n8n, nextcloudpi, nginxssl, nocodb, open-webui, plex, portainer, rhasspy, stirling-pdf, syncthing, teddycloud, teslamate, theengs-gateway, uptime-kuma, wyoming-openwakeword, wyoming-piper, wyoming-whisper


### v1.11
#### What's New? [Here's a video](https://youtu.be/_eBfsc9YRHE)
- Improved dashboard with automatic showing/hiding of disabled Docker programs
- Improved server overview
- Resource display (RAM / DISK)
- Storage usage by folder
- Port of the ei23-supervisor can be changed [see ei23-supervisor.py](https://github.com/ei23com/diy-smart-home/blob/main/ei23-docker/volumes/ei23/ei23-supervisor.py#L22)

### v1.1 - Version 1.1 of the script is available! Hooray!

#### What's New? [Here's a video](https://youtu.be/Ar_j29EbX98)

- The [Dashboard](/start/ei23-dashboard/) has been redesigned and now offers:
  - An IP scanner for the local network (similar to routers, only more practical and faster)
  - An overview of configured programs in docker-compose and [programs.json](/start/ei23-dashboard/)
- [Home Assistant](/software/homeassistant/) receives an [Addon function](https://github.com/ei23com/diy-smart-home/blob/main/ei23-docker/custom_ha_addons-example.sh). This allows community integrations to be automatically updated — similar to HACS, but simpler and without linking a GitHub account.
- The script is now available on GitHub — contributions are welcome.
- You are reading the new documentation right now.
- The script has now been fully adapted for 64-bit systems and AMD64 architectures with Debian 12 as the operating system.

#### Breaking Changes

As explained in the [video](https://youtu.be/Ar_j29EbX98):
The dashboard no longer runs as a Docker container, but now as a Python server at the system level.

1. Delete and stop the ei23 Docker container from the [Docker-Compose](/start/docker-compose/).
```bash
docker stop ei23
```

2. Perform the update
```bash
ei23 ei23update
ei23 ei23upgrade
```

3. Restart the new [ei23 Supervisor](/start/ei23-dashboard/).
```bash
sudo systemctl restart ei23.service
```

#### Troubleshooting
If the dashboard is not accessible, stop the server with
```bash
sudo systemctl stop ei23.service
```

The server can be started manually with this command
```bash
cd ei23-docker/volumes/ei23/; sudo .venv/bin/python3 ei23-supervisor.py
```
If there are error messages such as "Flask" not working properly or missing, then the Python Virtual Environment was not installed correctly.
Python has required a Virtual Environment (.venv) for extensions for some time now.
[externally-managed-environments](https://packaging.python.org/en/latest/specifications/externally-managed-environments/)

This is also the reason why the MKDocs installation hasn't been working correctly for some time. I was able to fix this.

On older or 32-bit systems, installing python3-venv may cause problems and thus prevent the new dashboard from starting.
It is necessary to install the python3-venv package correctly:
```bash
sudo apt-get install python3-venv -y # (1)
ei23 ei23update 
ei23 ei23upgrade
sudo systemctl restart ei23.service # (2)
```

1.   Only after this command executes without errors can the following commands be run
2.   This command restarts the server. The server should now be accessible.


If that doesn't work either, you can try it manually again:

```bash
sudo apt-get update
sudo python3 -m venv .venv
sudo su
cd ei23-docker/volumes/ei23/
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install flask waitress mkdocs-material ruamel.yaml
exit
sudo systemctl enable ei23.service
sudo systemctl start ei23.service
```

This will show you all error messages that could occur during installation.
If that still doesn't help, a fresh installation is probably the easier way.

--- 


If the original programs are not visible:
```bash
sudo cp ei23-docker/volumes/ei23/web/programs.json ei23-docker/volumes/ei23/web/static/programs.json
```
---
If hostnames are not visible in the IP scan list, an update of arp-scan can be performed:
```bash
sudo apt-get update
sudo apt-get install -y build-essential autoconf automake libtool pkg-config libpcap-dev
git clone https://github.com/royhills/arp-scan.git
cd arp-scan
autoreconf --install
./configure
make
sudo make install
cd ~
rm -r arp-scan/
```
