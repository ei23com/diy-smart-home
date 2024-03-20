# Programme als Container installieren

Mach dich mit dem Bearbeiten der [docker-compose.yml](https://docs.docker.com/compose/compose-file/compose-file-v3/) vertraut. Diese findest du unter `/home/[user]/ei23-docker/docker-compose.yml`.

**Ich habe dazu ein ausführliches Video:**
[![YT](https://ei23.de/bilder/YTthumbs/teV-yfBoTuA.webp)](https://www.youtube.com/watch?v=teV-yfBoTuA)

Für die Bearbeitung musst du mit dem Benutzer "root" angemeldet sein oder z.B. `sudo nano /home/[user]/ei23-docker/docker-compose.yml` verwenden, um Schreibrechte zu bekommen. Alternativ kannst du die Datei auch im Webbrowser mit [vscode](/software/vscode/). Es liegen Templates, also "Installationsschablonen," zum nachträglichen Installieren in `/home/pi/ei23-docker/compose_templates` bereit. Du kannst sie benutzen und entsprechend in die docker-compose.yml kopieren.

Nach der Anpassung der docker-compose.yml (Achtung, falsche Zeileneinrückung kann dazu führen, dass die Installation nicht richtig ausgeführt wird) musst du nur noch `ei23` und dann "Docker Compose" bzw. `ei23 dc` ausführen.

Je nach Architektur (armv7/arm64/amd64) kann es vorkommen, dass es kein aktuelles Image des Containers gibt. Dies kann man beispielsweise unter [hub.docker.com](https://hub.docker.com/) nachschauen. Ggf. muss man auf ein älteres Image zurückgreifen - im Beispiel unten wurde `:1.24.0` angehängt.

Auch kann es vorkommen, dass ein Port bereits belegt ist. Das Routing für Docker funktioniert wie die Portfreigabe an einem normalen Router. Die Notation ist folgendermaßen (auch bei Volumes und Devices):

```yaml
Hostsystem:Container
```

Man kann so einfach beliebige Ports weiterleiten. Im Beispiel unten steht `8080` für den externen Port (host), also der Port am Computer ansprechbar ist. Der hintere Port (container) ist nur Docker-intern erreichbar. Das funktioniert gleichermaßen für Ordner, Geräte, etc. im Hostsystem - Sehr praktisch und sicher!

Beispiel:
```yaml
  image: nginx:1.24.0
  volumes:
   - ./volumes/nginx:/etc/nginx/templates
  ports:
   - 8080:80 #(1)
  devices:
   - /dev/video0:/dev/video0
```

1.   `8080` ist hier der externe Port (host) und `80` der interne Port (container). Im Prinzip genau wie bei einem Router/Modem.