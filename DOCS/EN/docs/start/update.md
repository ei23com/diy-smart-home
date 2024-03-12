## Changelog

### v1.1 - Version 1.1 of the script is here! Hooray!

#### What's New? 

- The [dashboard](/start/ei23-dashboard/) has been revamped and now includes:
  - An IP scanner for the local network (similar to routers but more convenient and faster)
  - An overview of configured programs in docker-compose and [programs.json](/start/ei23-dashboard/)
- [Home Assistant](/software/homeassistant/) now has an [addon feature](https://github.com/ei23com/diy-smart-home/blob/main/ei23-docker/custom_ha_addons-example.sh). This allows automatic updates for community integrations - similar to HACS, but simpler and without linking a Github account.
- The script is now on GitHub - contributions are welcome.
- You are currently reading the new documentation.

#### Breaking Changes

The ei23 Dashboard no runs as Docker Container, but as Python Server.

1. Remove and stop the ei23 Docker container from [Docker-Compose](/start/docker-compose/).
```bash
docker stop ei23
```

1. Perform the update.
```bash
ei23 ei23update
ei23 ei23upgrade
```

1. Restart the new [ei23 Supervisor](/start/ei23-dashboard/).
```bash
sudo systemctl restart ei23.service
```

If the original programs are not visible:
```bash
sudo cp ei23-docker/volumes/ei23/web/programs.json ei23-docker/volumes/ei23/web/static/programs.json
```

If you don't see hostnames in the list from the IP scan, you can update arp-scan:
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