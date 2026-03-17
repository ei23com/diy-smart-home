# VSCode Server

[VSCode Server](https://github.com/coder/code-server) ermöglicht es dir, Visual Studio Code im Browser zu nutzen. Ideal zum Bearbeiten von Konfigurationsdateien, docker-compose.yml oder auch zum Programmieren direkt auf dem Server.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  vscode:
    image: codercom/code-server:latest
    container_name: vscode
    restart: unless-stopped
    ports:
      - 8443:8080
    volumes:
      - ./volumes/vscode:/home/coder/project
      - /home:/home:ro  # Optional: Home-Verzeichnisse einbinden
    environment:
      - PASSWORD=DEIN_PASSWORT
      - SUDO_PASSWORD=DEIN_SUDO_PASSWORT
```

!!!warning "Passwort setzen"
    Ersetze `DEIN_PASSWORT` mit einem sicheren Passwort!

## Erster Start

1. Nach dem Start erreichst du VSCode unter `http://[IP]:8443`
2. Melde dich mit dem konfigurierten Passwort an
3. Du siehst nun VSCode im Browser

## Verwendung

### Konfigurationsdateien bearbeiten

Perfekt für das Bearbeiten von:
- `docker-compose.yml`
- Home Assistant Konfiguration
- Traefik-Einstellungen
- Alle anderen Textdateien

### Home-Verzeichnisse einbinden

Mit dem Volume-Mount `/home:/home:ro` kannst du alle User-Verzeichnisse schreibgeschützt einsehen.

Für vollen Zugriff:

```yaml
volumes:
  - ./volumes/vscode:/home/coder/project
  - /home:/home  # Ohne :ro für vollen Zugriff
```

### Extensions installieren

VSCode Server unterstützt Extensions:

1. Klicke auf das Extensions-Icon (vier Kästchen)
2. Suche und installiere Extensions wie:
    - YAML
    - Docker
    - Git Graph
    - Remote SSH
    - Python

## Tipps für das ei23 Setup

| Aufgabe | Pfad |
|---------|------|
| Docker Compose | `/home/[user]/ei23-docker/docker-compose.yml` |
| Home Assistant | `/home/[user]/ei23-docker/volumes/homeassistant/config/` |
| Traefik | `/home/[user]/ei23-docker/volumes/traefik/` |
| ei23 Dashboard | `/home/[user]/ei23-docker/volumes/ei23/web/` |

!!!tip "YAML-Support"
    Installiere die YAML-Extension von Red Hat für Autovervollständigung und Validierung in docker-compose.yml Dateien.

## Sicherheitshinweise

- VSCode Server gibt vollen Zugriff auf die eingebundenen Dateien
- Nutze ein **starkes Passwort**
- Nutze HTTPS mit [Traefik](traefik.md) oder [Nginx Proxy Manager](nginxproxy.md)
- Der Port 8443 sollte **nicht** ins Internet freigegeben werden

## Hinweise

- Die Daten werden in `./volumes/vscode/` gespeichert
- Der Port ist standardmäßig 8443
- VSCode Server läuft im Container und hat keinen direkten Zugriff auf Host-Befehle

## Weitere Informationen

- [GitHub Repository](https://github.com/coder/code-server)
- [VSCode Dokumentation](https://code.visualstudio.com/docs)
