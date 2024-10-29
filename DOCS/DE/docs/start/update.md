## Changelog


### v1.11
#### Was gibt es Neues?
- Bugfixes: Verbesserte Installation und Probleme mit Icons / Links auf dem ei23 Dashboard behoben
- Neue Docker Templates: fooocus, archivebox, ollama, openedai-speech, pairdrop, perplexica, watchyourlan, whisper-webui


### v1.11
#### Was gibt es Neues? [Hier ein Video](https://youtu.be/_eBfsc9YRHE)
- Verbessertes Dashboard mit automatischem Anzeigen / Ausblenden von deaktiverten Docker-Programmen
- Verbesserte Server-Übersicht
- Ressourcen Anzeige (RAM / DISK)
- Speicherbelegung nach Ordnern
- Port des ei23-supervisors kann verändert werden [siehe ei23-supervisor.py](https://github.com/ei23com/diy-smart-home/blob/main/ei23-docker/volumes/ei23/ei23-supervisor.py#L22) 

### v1.1 - Die Version 1.1 des Skripts ist verfügbar! Hurra!

#### Was gibt es Neues? [Hier ein Video](https://youtu.be/Ar_j29EbX98)

- Das [Dashboard](/start/ei23-dashboard/) wurde überarbeitet und bietet nun:
  - Einen IP-Scanner für das lokale Netzwerk (ähnlich wie in Routern, nur praktischer und schneller)
  - Eine Übersicht der konfigurierten Programme in der docker-compose und der [programs.json](/start/ei23-dashboard/)
- [Home Assistant](/software/homeassistant/) erhält eine [Addon-Funktion](https://github.com/ei23com/diy-smart-home/blob/main/ei23-docker/custom_ha_addons-example.sh). Damit können Community-Integrationen automatisch aktualisiert werden - ähnlich wie bei HACS, nur einfacher und ohne einen Github-Account zu verknüpfen.
- Das Skript ist jetzt auf GitHub verfügbar - Mitarbeit ist willkommen.
- Du liest gerade die neue Dokumentation.
- Das Skript ist mittlerweile komplett für 64Bit Systeme und AMD64 Architekturen mit Debian12 als Betriebssystem angepasst.

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

#### Troubleshooting
Ist das Dashboard nicht erreichbar, stoppt den Server mit
```bash
sudo systemctl stop ei23.service
```

Der Server lässt sich diesem Befehl manuell starten
```bash
cd ei23-docker/volumes/ei23/; sudo .venv/bin/python3 ei23-supervisor.py
```
Gibt es die Fehlermeldungen das beispielsweise "Flask" nicht richtig funktioniert oder fehlt, dann wurde das Python Virtual Environment nicht korrekt installiert.
Python verlangt für Erweiterungen seit einiger Zeit ein Virutal Environment (.venv)
[externally-managed-environments](https://packaging.python.org/en/latest/specifications/externally-managed-environments/)

Das ist beispielsweise auch der Grund, warum die MKDocs Intallation seit einiger Zeit nicht korrekt funktionierte. Dies konnte ich damit beheben.

Auf älteren oder 32Bit Systemen kann die Installation von python3-venv Probleme verursachen und damit auch den Start des neuen Dashboards verhindern.
Es ist notwendig, das Paket python3-venv korrekt installiert wird
```bash
sudo apt-get install python3-venv -y # (1)
ei23 ei23update 
ei23 ei23upgrade
sudo systemctl restart ei23.service # (2)
```

1.   Erst wenn dieser Befehl fehlerfrei ausgeführt wird, können die folgenden Befehle ausgeführt werden
2.   Dieser Befehl startet den Server erneut. Der Server sollte nun erreichbar sein.


Wenn das auch nicht klappt, kannst du es nochmal manuell versuchen:

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

Damit werden dir alle Fehlermeldungen angezeigt, die bei der Installation auftreten könnten.
Wenn das immer noch keine Abhilfe schafft, ist eine Neuinstallation vermutlich der einfachere weg.

--- 


Falls die ursprünglichen Programme nicht sichtbar sind
```bash
sudo cp ei23-docker/volumes/ei23/web/programs.json ei23-docker/volumes/ei23/web/static/programs.json
```
---
Falls die Hostnamen in der Liste vom IP-Scan nicht sichtbar sind, kann ein Update von arp-scan ausgeführt werden:
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