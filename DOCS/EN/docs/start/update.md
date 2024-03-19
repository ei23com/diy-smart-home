## Changelog

### v1.1 - Version 1.1 of the script is available! Hooray!

#### What's New? [Watch the Video Here](https://youtu.be/Ar_j29EbX98)

- The [dashboard](/start/ei23-dashboard/) has been revamped and now includes:
  - An IP scanner for the local network (similar to routers, but more practical and faster)
  - An overview of configured programs in docker-compose and [programs.json](/start/ei23-dashboard/)
- [Home Assistant](/software/homeassistant/) receives an [addon function](https://github.com/ei23com/diy-smart-home/blob/main/ei23-docker/custom_ha_addons-example.sh). This allows automatic updates of community integrations - similar to HACS, but simpler and without linking to a GitHub account.
- The script is now available on GitHub - contributions are welcome.
- You are currently reading the new documentation.

#### Breaking Changes

As explained in the [video](https://youtu.be/Ar_j29EbX98):
The dashboard no longer runs as a Docker container but now as a Python server at the system level.

1. Remove and stop the ei23 Docker container from the [Docker-Compose](/start/docker-compose/).
```bash
docker stop ei23
```

2. Perform the update.
```bash
ei23 ei23update
ei23 ei23upgrade
```

3. Restart the new [ei23 Supervisor](/start/ei23-dashboard/).
```bash
sudo systemctl restart ei23.service
```

#### Troubleshooting
If the dashboard is not accessible, stop the server with:
```bash
sudo systemctl stop ei23.service
```

Manually start the server with this command:
```bash
cd ei23-docker/volumes/ei23/; sudo .venv/bin/python3 ei23-supervisor.py
```
If there are error messages indicating that "Flask" is not working correctly or missing, the Python Virtual Environment was not installed correctly.
Python has required a Virtual Environment (.venv) for extensions for some time now.
[externally-managed-environments](https://packaging.python.org/en/latest/specifications/externally-managed-environments/)

This is also the reason why the MKDocs installation has not been functioning correctly for some time. I have fixed this issue with the Virtual Environment.

On older or 32-bit systems, installing python3-venv may cause problems and prevent the new dashboard from starting.
It is necessary to ensure that the python3-venv package is correctly installed:
```bash
sudo apt-get install python3-venv -y # (1)
ei23 ei23update 
ei23 ei23upgrade
sudo systemctl restart ei23.service # (2)
```

1.   Only proceed to the following commands if this command is executed without errors.
2.   This command restarts the server. The server should now be accessible.


 If this does not work either, you can still try it manually:

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

This will display all error messages that may occur during installation. If this still does not help, a new installation is probably the easier way.

--- 

If the original programs are not visible:
```bash
sudo cp ei23-docker/volumes/ei23/web/programs.json ei23-docker/volumes/ei23/web/static/programs.json
```
---
If the hostnames in the IP scan list are not visible, an update of arp-scan can be performed:
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