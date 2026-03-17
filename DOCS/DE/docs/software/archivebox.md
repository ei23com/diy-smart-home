# ArchiveBox

[ArchiveBox](https://archivebox.io/) ist ein leistungsstarkes Tool zum lokalen Archivieren von Webseiten. Es speichert URLs als HTML, PDF, Screenshots und vieles mehr - ideal um wichtige Inhalte dauerhaft zu sichern.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  archivebox:
    image: archivebox/archivebox
    container_name: archivebox
    command: server --quick-init 0.0.0.0:8000
    ports:
      - 8085:8000
    volumes:
      - ./volumes/archivebox/data/:/data
    environment:
      - ALLOWED_HOSTS=*
      - PUBLIC_INDEX=True
      - PUBLIC_SNAPSHOTS=True
      # - PUBLIC_ADD_VIEW=False
      - ADMIN_USERNAME=admin
      - ADMIN_PASSWORD=SomeSecretPassword
```

## Hinweise

- Nach dem Start erreicht du ArchiveBox unter `http://[IP]:8085`
- **Wichtig:** Ändere `ADMIN_PASSWORD` und passe `ALLOWED_HOSTS` an deine Domain/IP an
- Setze `PUBLIC_INDEX=False` und `PUBLIC_SNAPSHOTS=False`, um deine Archive privat zu halten
- Für automatisches Archivieren kann ein Cronjob eingerichtet werden (siehe Template-Kommentare)

## Weitere Informationen

- [Offizielle Dokumentation](https://github.com/ArchiveBox/ArchiveBox/wiki)
- [GitHub Repository](https://github.com/ArchiveBox/ArchiveBox)
