# Jellyfin

[Jellyfin](https://jellyfin.org/) ist ein freier Open-Source-Medienserver, der es dir ermöglicht, deine Filme, Musik, Serien und Fotos zu organisieren, zu verwalten und auf all deinen Geräten zu streamen.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    user: 0:0 # UserID:GroupID
    network_mode: 'host'
    volumes:
      - ./volumes/jellyfin/config:/config
      - ./volumes/jellyfin/cache:/cache
      - ./volumes/jellyfin/media:/media
      # - ./volumes/immich/fotos/library:/photos:ro
    restart: 'unless-stopped'
    # Optional - alternative address used for autodiscovery
    # environment:
    #   - JELLYFIN_PublishedServerUrl=http://example.com
```

## Hinweise

- Das Template verwendet `network_mode: 'host'` für bessere Kompatibilität mit DLNA und automatischer Geräteerkennung
- Lege deine Medien in den Ordner `./volumes/jellyfin/media/` oder passe die Volume-Mappings an
- Die Konfigurationsdateien werden in `./volumes/jellyfin/config/` gespeichert

## Weitere Informationen

- [Offizielle Dokumentation](https://jellyfin.org/docs/)
- [GitHub Repository](https://github.com/jellyfin/jellyfin)
