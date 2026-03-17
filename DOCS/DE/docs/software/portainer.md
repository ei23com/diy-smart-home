# Portainer

[Portainer](https://www.portainer.io/) ist eine grafische Verwaltungsoberfläche für Docker. Es ermöglicht dir, Container, Images, Volumes und Netzwerke bequem über den Browser zu verwalten.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  portainer:
    container_name: portainer
    image: portainer/portainer-ce
    restart: unless-stopped
    ports:
      - "8000:8000"
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./volumes/portainer/data:/data
```

## Hinweise

- Nach dem Start erreicht du Portainer unter `http://[IP]:9000`
- Beim ersten Start musst du einen Admin-Benutzer erstellen
- Der Port 8000 wird für Edge-Agenten verwendet (optional)
- Portainer ist sehr nützlich zum Überprüfen von Logs, Starten/Stoppen von Containern und zur Fehlersuche

## Weitere Informationen

- [Offizielle Dokumentation](https://docs.portainer.io/)
- [GitHub Repository](https://github.com/portainer/portainer)
