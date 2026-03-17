# Immich - Lokale Foto-Cloud

[Immich](https://immich.app/) ist eine Open-Source-Alternative zu Google Photos und iCloud. Es ermöglicht dir, deine Fotos und Videos sicher auf deinem eigenen Server zu speichern und von überall darauf zuzugreifen.

[![YT](https://ei23.de/bilder/YTthumbs/8IWbTQAdxZ8.webp)](https://www.youtube.com/watch?v=8IWbTQAdxZ8)

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Umgebungsdatei erforderlich"
    Erstelle die Datei `ei23-docker/env/immich.env` vor dem Start.

## Umgebungsdatei erstellen

Erstelle `/home/[user]/ei23-docker/env/immich.env`:

```env
# Du kannst die Location des Upload-Ordners ändern
UPLOAD_LOCATION=./volumes/immich/upload

# Pfade
IMMICH_VERSION=release

# Datenbank
DB_PASSWORD=DEIN_SICHERES_PASSWORT
DB_USERNAME=postgres
DB_DATABASE_NAME=immich

# Redis (nicht ändern)
REDIS_HOSTNAME=immich_redis

# Log Level (optional)
LOG_LEVEL=verbose
```

## Template

```yaml
  immich-server:
    container_name: immich_server
    image: ghcr.io/immich-app/immich-server:${IMMICH_VERSION:-release}
    command: [ "start.sh", "immich" ]
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
    env_file:
      - ./env/immich.env
    ports:
      - 2283:3001
    depends_on:
      - redis
      - database
    restart: always

  immich-microservices:
    container_name: immich_microservices
    image: ghcr.io/immich-app/immich-server:${IMMICH_VERSION:-release}
    command: [ "start.sh", "microservices" ]
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
    env_file:
      - ./env/immich.env
    depends_on:
      - redis
      - database
    restart: always

  immich-machine-learning:
    container_name: immich_machine_learning
    image: ghcr.io/immich-app/immich-machine-learning:${IMMICH_VERSION:-release}
    volumes:
      - ./volumes/immich/model-cache:/cache
    env_file:
      - ./env/immich.env
    restart: always

  redis:
    container_name: immich_redis
    image: redis:6.2-alpine
    restart: always

  database:
    container_name: immich_postgres
    image: tensorchord/pgvecto-rs:pg14-v0.2.0
    env_file:
      - ./env/immich.env
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_DB: ${DB_DATABASE_NAME}
      PG_DATA: /var/lib/postgresql/data
    volumes:
      - ./volumes/immich/pgdata:/var/lib/postgresql/data
    restart: always
```

## Features

- **Automatischer Upload** - Fotos vom Handy automatisch hochladen
- **Gesichtserkennung** - Personen automatisch erkennen und gruppieren
- **Suche** - Suche nach Objekten, Orten, Personen
- **Alben** - Gemeinsame Alben mit Familie/Freunden
- **Karte** - Fotos auf einer Karte anzeigen
- **Timeline** - Chronologische Übersicht
- **Gemeinsame Bibliotheken** - Mit anderen teilen
- **RAW-Support** - Auch RAW-Bilder verarbeiten

## Mobile Apps

Installiere die Immich App auf deinem Smartphone:

- [Android](https://play.google.com/store/apps/details?id=app.alextran.immich)
- [iOS](https://apps.apple.com/app/immich/id1613945652)

### App konfigurieren

1. Öffne die App
2. Gib die Server-URL ein: `http://[IP]:2283`
3. Melde dich mit deinem Account an
4. Aktiviere den **Auto-Upload** für gewünschte Alben

## Erster Start

1. Nach dem Start erreichst du Immich unter `http://[IP]:2283`
2. Erstelle einen Admin-Account
3. Richte die mobile App ein
4. Starte den ersten Upload

## Backup & Restore

!!!warning "Wichtig"
    Regelmäßige Backups sind essentiell! Fotos sind unersetzlich.

```bash
# Backup erstellen
cd ~/ei23-docker/
docker compose exec immich_postgres pg_dump -U postgres immich > immich_db_backup.sql
sudo tar -czf immich_upload_backup.tar.gz volumes/immich/upload/
```

## Empfehlung für Hardware

Immich profitiert stark von leistungsfähiger Hardware:

| Komponente | Minimum | Empfohlen |
|------------|---------|-----------|
| **RAM** | 4GB | 8GB+ |
| **CPU** | 2 Kerne | 4+ Kerne |
| **Storage** | SSD | NVMe SSD |
| **GPU** | - | Für ML-Beschleunigung |

!!!tip "Mini-PC empfohlen"
    Für Immich ist ein Mini-PC mit Intel i3/i5 und 8GB+ RAM empfohlen. Siehe [Hardware-Empfehlungen](/hardware/server/).

## Hinweise

- Die Daten werden in `./volumes/immich/` gespeichert
- Fotos im `upload` Ordner speichern
- Machine Learning für Gesichtserkennung braucht viel RAM
- Für große Bibliotheken: Geduld beim ersten Scan
- Immich ist noch in aktiver Entwicklung - Updates regelmäßig prüfen

## Weitere Informationen

- [Offizielle Dokumentation](https://immich.app/docs/)
- [GitHub Repository](https://github.com/immich-app/immich)
- [Demo](https://demo.immich.app/)
