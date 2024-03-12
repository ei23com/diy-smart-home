## Changelog

### v1.1 - Die Version 1.1 des Skripts ist verfügbar! Hurra!

#### Was gibt es Neues? [Hier ein Video](https://youtu.be/Ar_j29EbX98)

- Das [Dashboard](/start/ei23-dashboard/) wurde überarbeitet und bietet nun:
  - Einen IP-Scanner für das lokale Netzwerk (ähnlich wie in Routern, nur praktischer und schneller)
  - Eine Übersicht der konfigurierten Programme in der docker-compose und der [programs.json](/start/ei23-dashboard/)
- [Home Assistant](/software/homeassistant/) erhält eine [Addon-Funktion](https://github.com/ei23com/diy-smart-home/blob/main/ei23-docker/custom_ha_addons-example.sh). Damit können Community-Integrationen automatisch aktualisiert werden - ähnlich wie bei HACS, nur einfacher und ohne einen Github-Account zu verknüpfen.
- Das Skript ist jetzt auf GitHub verfügbar - Mitarbeit ist willkommen.
- Du liest gerade die neue Dokumentation.

#### Breaking Changes

Wie bereits im [Video](https://youtu.be/Ar_j29EbX98) erklärt:
Das Dashboard läuft nicht mehr als Docker Container, sondern nun als Python Server auf Systemebene.

1. Den ei23 Docker Container aus der [Docker-Compose](/start/docker-compose/) löschen und beenden.
```bash
docker stop ei23
```

2. Das Update durchführen
```bash
ei23 ei23update
ei23 ei23upgrade
```

3. Den neuen [ei23 Supervisor](/start/ei23-dashboard/) neu starten.
```bash
sudo systemctl restart ei23.service
```

Falls die ursprünglichen Programme nicht sichtbar sind
```bash
sudo cp ei23-docker/volumes/ei23/web/programs.json ei23-docker/volumes/ei23/web/static/programs.json
```

Falls ihr die Hostnamen in der Liste vom IP-Scan nicht seht, könnt ihr ein Update von arp-scan ausführen:
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