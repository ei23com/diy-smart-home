# Syncthing

[Syncthing](https://syncthing.net/) ist ein freier, dezentraler Dateisynchronisationsdienst. Es synchronisiert Dateien zwischen mehreren Geräten ohne zentrale Cloud - deine Daten bleiben auf deinen Geräten.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  syncthing:
    image: syncthing/syncthing
    container_name: syncthing
    hostname: syncthing-server
    environment:
      - PUID=33
      - PGID=33
    volumes:
      - ./volumes/syncthing:/var/syncthing
    ports:
      - 8384:8384 # Web UI
      - 22000:22000/tcp # TCP file transfers
      - 22000:22000/udp # QUIC file transfers
      - 21027:21027/udp # Receive local discovery broadcasts
    restart: unless-stopped
```

## Hinweise

- Nach dem Start erreichst du die Weboberfläche unter `http://[IP]:8384`
- Beim ersten Start wird eine Passwortsperre angezeigt - setze ein Passwort unter "Einstellungen"
- Verbinde deine Geräte über die Device-ID
- Syncthing funktioniert auch über das Internet, NAT-Traversal ist eingebaut
- Ideal für Backups und Datensynchronisation zwischen Server und Desktop/Laptop

## Weitere Informationen

- [Offizielle Dokumentation](https://docs.syncthing.net/)
- [GitHub Repository](https://github.com/syncthing/syncthing)
