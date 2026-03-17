# Programme als Container installieren

Mach dich mit dem Bearbeiten der [docker-compose.yml](https://docs.docker.com/compose/compose-file/compose-file-v3/) vertraut. Diese findest du unter `/home/[user]/ei23-docker/docker-compose.yml`.

**Ich habe dazu ein ausführliches Video:**
[![YT](https://ei23.de/bilder/YTthumbs/teV-yfBoTuA.webp)](https://www.youtube.com/watch?v=teV-yfBoTuA)

## Bearbeitung

Für die Bearbeitung gibt es mehrere Möglichkeiten:

| Methode | Befehl/Vorgehen |
|---------|-----------------|
| **Terminal** | `sudo nano /home/[user]/ei23-docker/docker-compose.yml` |
| **VSCode Server** | Über das Dashboard → [VSCode](/software/vscode/) |
| **Dashboard** | Server-Seite → "Docker Programme hinzufügen" (einklappbar) |

!!!tip "Dashboard nutzen"
    Das [ei23 Dashboard](/start/ei23-dashboard/) bietet jetzt eine Template-Übersicht direkt im Browser! Einfach klicken und hinzufügen.

## Templates

Es liegen Templates, also "Installationsschablonen," zum nachträglichen Installieren in `/home/[user]/ei23-docker/compose_templates` bereit. Du kannst sie benutzen und entsprechend in die docker-compose.yml kopieren.

### Verfügbare Templates

Die Templates befinden sich im Ordner `ei23-docker/compose_templates/`. Hier einige Beispiele:

| Template | Beschreibung |
|----------|--------------|
| `homeassistant.yml` | Home Assistant |
| `nodered.yml` | Node-RED (Docker-Version) |
| `mosquitto.yml` | MQTT Broker |
| `grafana.yml` | Grafana Dashboard |
| `influxdb.yml` | InfluxDB Zeitseriendatenbank |
| `vaultwarden.yml` | Passwort-Manager |
| `traefik.yml` | Reverse Proxy mit SSL |
| `nextcloudofficial.yml` | Nextcloud |
| `portainer.yml` | Docker-Verwaltung |
| `immich.yml` | Foto-Cloud |
| `jellyfin.yml` | Media Server |
| `ollama.yml` | Lokale LLMs |
| `open-webui.yml` | Chat-Oberfläche für LLMs |
| `frigate.yml` | KI-NVR für Kameras |
| `wireguard.yml` | VPN-Server |
| `nginxproxymanger.yml` | Reverse Proxy (einfach) |
| `pihole.yml` | DNS Ad-Blocker |
| `syncthing.yml` | Datei-Synchronisation |
| `mealie.yml` | Rezept-Manager |
| `freshrss.yml` | RSS-Reader |
| `n8n.yml` | Workflow-Automatisierung |
| `nocodb.yml` | Datenbank-Oberfläche (Airtable-Alternative) |
| `fireflyiii.yml` | Finanzmanager |
| `ghostfolio.yml` | Vermögensverwaltung |
| `archivebox.yml` | Webseiten-Archivierung |
| `uptime-kuma.yml` | Service-Monitoring |

!!!note "Vollständige Liste"
    Schau direkt in den Ordner `/home/[user]/ei23-docker/compose_templates/` um alle verfügbaren Templates zu sehen.

### Template einfügen

1. Öffne die docker-compose.yml
2. Füge den Inhalt des Templates am Ende der Datei ein
3. Achte auf korrekte Einrückung (YAML ist empfindlich!)
4. Speichere die Datei
5. Führe `ei23 dc` aus

!!!warning "Einrückung beachten"
    Falsche Zeileneinrückung kann dazu führen, dass die Installation nicht richtig ausgeführt wird!

## Template anwenden

Nach der Anpassung der docker-compose.yml führe aus:

```bash
ei23 dc
```

Oder über das Dashboard: Server-Seite → "Docker Compose" Button.

## Docker Compose verstehen

### Ports

Das Routing für Docker funktioniert wie die Portfreigabe an einem Router:

```yaml
ports:
  - HOST_PORT:CONTAINER_PORT
```

- **HOST_PORT**: Externer Port am Server erreichbar
- **CONTAINER_PORT**: Interner Port im Container

Beispiel:

```yaml
  image: nginx:1.24.0
  ports:
    - 8080:80
```

Hier ist `8080` der externe Port (am Server) und `80` der interne Port (im Container).

!!!tip "Router-Prinzip"
    Das funktioniert genau wie bei einem Router/Modem - nur dass Docker die Portweiterleitung intern macht.

### Volumes

Volumes binden Ordner des Host-Systems in den Container ein:

```yaml
volumes:
  - HOST_PFAD:CONTAINER_PFAD
```

Beispiel:

```yaml
volumes:
  - ./volumes/nginx:/etc/nginx/templates
```

- **./volumes/nginx** - Ordner auf dem Host (relativ zum docker-compose.yml)
- **/etc/nginx/templates** - Pfad im Container

### Devices

Devices binden Hardware in den Container ein:

```yaml
devices:
  - /dev/video0:/dev/video0
```

Wichtig für:
- Zigbee-Sticks (`/dev/ttyUSB0`)
- Kameras (`/dev/video0`)
- GPIO (Raspberry Pi)

### Environment Variables

Umgebungsvariablen konfigurieren den Container:

```yaml
environment:
  - TZ=Europe/Berlin
  - MYSQL_PASSWORD=password_placeholder
```

!!!tip "Passwort-Platzhalter"
    Das ei23-Skript ersetzt automatisch `password_placeholder` mit zufälligen Passwörtern bei der Erstinstallation.

### Networks

Netzwerke verbinden Container miteinander:

```yaml
networks:
  - default
  - custom_network

# Am Ende der docker-compose.yml definieren:
networks:
  custom_network:
    driver: bridge
    internal: true
```

### Depends_on

Definiert Start-Reihenfolge:

```yaml
depends_on:
  - database
  - redis
```

### Restart Policy

Steuert das Neustart-Verhalten:

```yaml
restart: unless-stopped  # Immer neu starten, außer manuell gestoppt
restart: always          # Immer neu starten
restart: on-failure      # Nur bei Fehler
restart: "no"            # Nie neustarten
```

## Architektur-Hinweise

Je nach Architektur (armv7/arm64/amd64) kann es vorkommen, dass es kein aktuelles Image des Containers gibt. Dies kann man beispielsweise unter [hub.docker.com](https://hub.docker.com/) nachschauen.

### Beispiel: Älteres Image nutzen

```yaml
  image: nginx:1.24.0
```

Hier wurde `:1.24.0` angehängt um eine bestimmte Version zu nutzen.

!!!note "ARM-Unterstützung"
    Nicht alle Docker-Images unterstützen ARM-Architekturen (Raspberry Pi). Prüfe dies vor der Installation.

## Port-Konflikte

Wenn ein Port bereits belegt ist, ändere den Host-Port:

```yaml
# Vorher (Port 8080 belegt)
ports:
  - 8080:80

# Nachher (Port 8081 nutzen)
ports:
  - 8081:80
```

## Beispiel: Komplette docker-compose.yml

```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable
    container_name: homeassistant
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./volumes/homeassistant/config:/config
      - /run/dbus:/run/dbus:ro
    environment:
      - TZ=Europe/Berlin

  mosquitto:
    image: eclipse-mosquitto:2
    container_name: mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883"
    volumes:
      - ./volumes/mosquitto/config:/mosquitto/config
      - ./volumes/mosquitto/data:/mosquitto/data
      - ./volumes/mosquitto/log:/mosquitto/log

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - ./volumes/grafana:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=password_placeholder

# Netzwerke (falls benötigt)
# networks:
#   my_network:
#     driver: bridge
```

## Fehlerbehebung

### Container startet nicht

```bash
# Logs prüfen
docker compose logs [container_name]

# Container manuell starten
docker compose up -d [container_name]
```

### Port belegt

```bash
# Prüfe welcher Port belegt ist
sudo netstat -tulpn | grep [PORT]

# Oder
sudo ss -tulpn | grep [PORT]
```

### YAML-Syntax Fehler

```bash
# YAML validieren
python3 -c "import yaml; yaml.safe_load(open('docker-compose.yml'))"
```

### Container zurücksetzen

!!!warning "Daten gehen verloren!"
    Dies löscht alle Daten des Containers!

```bash
# Einfach über das Skript
ei23 fullreset [container_name]

# Manuell
cd ~/ei23-docker/
docker compose stop [container_name]
docker compose rm -f [container_name]
sudo rm -r volumes/[container_name]/
docker compose up -d
```

## Weitere Informationen

- [Docker Compose Dokumentation](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/) - Images suchen
- [ei23 Dashboard](/start/ei23-dashboard/) - Template-Übersicht
