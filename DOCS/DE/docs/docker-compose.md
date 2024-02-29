## Programme als Container installieren

Mache dich mit dem Bearbeiten der [docker-compose.yml/](https://docs.docker.com/compose/compose-file/compose-file-v3/) vertraut. Diese findest duunter `/home/[user]/ei23-docker/docker-compose.yml`. Für die bearbeitung musst mit dem "root" Benutzer angenmeldet sein oder z.B. sudo nano `/home/[user]/ei23-docker/docker-compose.yml` benutzen um Schreibrechte zu bekommen. 
Es liegen Templates, also "Installationsschablonen" zum nachträglichen Installieren in `/home/pi/ei23-docker/compose_templates` bereit. Du kannst sie benutzen und entsprechend in die docker-compose.yml kopieren. 

Wenn du die docker-compose.yml angepasst hast (Achtung, falsche Zeileneinrückung kann dazu führen, dass die Installation nicht richtig ausgeführt wird) musst du nur noch `ei23` und dann "Docker Compose" bzw. `ei23 dc` ausführen.

Je nach Architektur (armv7/arm64/amd64) kann es vorkommen, dass es ein aktuelles Image des Containers nicht gibt.
Dies kann man unter [hub.docker.com](https://hub.docker.com/) nachschauen. 
Ggf. muss man auf ein älteres Image zurückgreifen - im Beispiel unten wurde `:1.24.0` angehängt

Auch kann es vorkommen, dass ein Port bereits belegt ist.
Das Routing für Docker funktioniert wie die Portfreigabe an einem normalen Router.
Die Notation ist folgdermaßen (auch bei Volumes und Devices)

```
Hostsystem:Container
```
Man so einfach beliebige Ports weiterleiten - Im Beispiel unten steht `8080` für den externen Port, also der Port am Computer ansprechbar ist. Der hintere Port ist nur Docker-intern erreichbar.
Das funktioniert gleichermaßen für Ordner, Geräte, etc. im Hostsystem - Sehr praktisch und sicher!

Beispiel:
```
  image: nginx:1.24.0
  volumes:
   - ./volumes/nginx:/etc/nginx/templates
  ports:
   - 8080:80
  devices:
   - /dev/video0:/dev/video0
```

Folgende Docker-Compose Templates sind an Bord:

- Adguardhome
- Awtrix
- Bitwarden
- Deconz
- Domoticz
- Duplicati
- ei23-Dashboard
- ESPhome
- FHEM
- FireflyIII
- FreePBX-Asterisk
- Gotify
- Grafana
- Grocy
- Homeassistant-Matterserver
- HomeAssistant
- HomeBridge
- Immich
- InfluxDB
- IObroker
- Jellyfin
- LogitechMediaServer
- Mosquitto
- Motioneye
- Nextcloud-Official
- NextcloudPI
- Nginx-ProxyManager
- NginxSSL
- OctoPrint
- OpenHAB
- PaperlessNGX
- PiHole
- Piper
- PLEX
- Portainer
- Rhasspy
- Tasmoadmin
- Teamspeak
- TimescaleDB
- Traefik
- Uptime-Kuma
- VSCode
- Whisper

