# Paperless-ngx

[Paperless-ngx](https://docs.paperless-ngx.com/) ist eine freie Dokumentenverwaltungssoftware mit Texterkennung (OCR). Sie digitalisiert physische Dokumente und macht sie durchsuchbar.

[![YT](https://ei23.de/bilder/YTthumbs/qyXz5gJnu_8.webp)](https://www.youtube.com/watch?v=qyXz5gJnu_8)

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Umgebungsdatei erforderlich"
    Erstelle die Datei `ei23-docker/env/paperless.env` vor dem Start.

## Umgebungsdatei erstellen

Erstelle `/home/[user]/ei23-docker/env/paperless.env`:

```env
PAPERLESS_SECRET=DEIN_GEHEIMES_TOKEN
PAPERLESS_TIMEZONE=Europe/Berlin
PAPERLESS_OCR_LANGUAGE=deu
PAPERLESS_ADMIN_USER=admin
PAPERLESS_ADMIN_PASSWORD=DEIN_PASSWORT
PAPERLESS_URL=http://deine-ip:8010
```

!!!warning "Secret Token"
    Generiere ein sicheres Token: `openssl rand -base64 32`

## Template

```yaml
  paperlessngx-redis:
    image: redis:7
    container_name: paperlessngx-redis
    restart: unless-stopped
    volumes:
      - ./volumes/paperless/redis:/data

  paperlessngx-db:
    image: postgres:15
    container_name: paperlessngx-db
    restart: unless-stopped
    volumes:
      - ./volumes/paperless/db:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: paperless
      POSTGRES_USER: paperless
      POSTGRES_PASSWORD: paperless

  paperlessngx:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    container_name: paperlessngx
    restart: unless-stopped
    depends_on:
      - paperlessngx-redis
      - paperlessngx-db
    ports:
      - "8010:8000"
    volumes:
      - ./volumes/paperless/data:/usr/src/paperless/data
      - ./volumes/paperless/media:/usr/src/paperless/media
      - ./volumes/paperless/export:/usr/src/paperless/export
      - ./volumes/paperless/consume:/usr/src/paperless/consume
    env_file:
      - ./env/paperless.env
    environment:
      PAPERLESS_REDIS: redis://paperlessngx-redis:6379
      PAPERLESS_DBHOST: paperlessngx-db
      PAPERLESS_DBNAME: paperless
      PAPERLESS_DBUSER: paperless
      PAPERLESS_DBPASS: paperless
```

## Features

- **OCR-Texterkennung** - Durchsuchbare PDFs aus Scans
- **Automatische Kategorisierung** - Tags, Korrespondenten, Dokumenttypen
- **Volltextsuche** - Suche in allen Dokumenten
- **E-Mail-Import** - Dokumente per E-Mail empfangen
- **Mobile App** - Unterwegs Dokumente hochladen
- **REST-API** - Automatisierung möglich
- **Export/Import** - Backup und Migration

## Erster Start

1. Nach dem Start erreichst du Paperless unter `http://[IP]:8010`
2. Login mit den in der env-Datei konfigurierten Zugangsdaten
3. Beginne mit dem Hochladen von Dokumenten

## Dokumente importieren

### Manuell über die Weboberfläche

1. Klicke auf **Hochladen** (Upload-Button)
2. Wähle PDF, JPEG oder PNG Dateien
3. Paperless verarbeitet das Dokument automatisch

### Über den Consume-Ordner

Lege Dateien in den Ordner `./volumes/paperless/consume/`:

```bash
# Dokumente in den Consume-Ordner kopieren
cp ~/scans/*.pdf ~/ei23-docker/volumes/paperless/consume/
```

Paperless überwacht diesen Ordner und verarbeitet neue Dateien automatisch.

### Über die Mobile App

1. Installiere die **Paperless Mobile** App
2. Konfiguriere die Server-URL
3. Scanne Dokumente direkt mit dem Handy

### Per E-Mail (optional)

Konfiguriere in der `paperless.env`:

```env
PAPERLESS_EMAIL_HOST=imap.gmail.com
PAPERLESS_EMAIL_PORT=993
PAPERLESS_EMAIL_USER=deine@email.de
PAPERLESS_EMAIL_PASS=DEIN_PASSWORT
PAPERLESS_EMAIL_INBOX=INBOX
```

## Organisation

### Tags

Tags sind frei definierbare Labels:

- **Steuern** - Steuerliche Dokumente
- **Versicherung** - Versicherungspolicen
- **Rechnung** - Rechnungen
- **Wichtig** - Besonders wichtige Dokumente

### Korrespondenten

Korrespondenten sind Absender/Empfänger:

- **Finanzamt**
- **AOK Krankenkasse**
- **Stadtwerke**
- **Arbeitgeber**

### Dokumenttypen

- **Rechnung**
- **Vertrag**
- **Bescheid**
- **Brief**
- **Lohnabrechnung**

### Automatische Regeln

Paperless kann Dokumente automatisch kategorisieren:

1. Gehe zu **Einstellungen** → **Regeln**
2. Erstelle eine neue Regel
3. Definiere Bedingungen (z.B. Text enthält "Rechnung")
4. Weise Tags/Korrespondenten zu

## Backup

### Über das ei23-Skript

```bash
ei23 backup
```

### Manuell

```bash
cd ~/ei23-docker/

# Datenbank sichern
docker compose exec paperlessngx-db pg_dump -U paperless paperless > ~/Backup/paperless_db.sql

# Daten sichern
sudo tar -czf ~/Backup/paperless_data.tar.gz volumes/paperless/data/ volumes/paperless/media/
```

### Restore

```bash
cd ~/ei23-docker/

# Container stoppen
docker compose stop paperlessngx

# Datenbank wiederherstellen
cat ~/Backup/paperless_db.sql | docker compose exec -T paperlessngx-db psql -U paperless paperless

# Daten wiederherstellen
sudo tar -xzf ~/Backup/paperless_data.tar.gz

# Container starten
docker compose start paperlessngx
```

## Tipps

- **Scanauflösung**: 300 DPI für gute OCR-Ergebnisse
- **Dateiformat**: PDF bevorzugt, TIFF auch gut
- **Sprachen**: Konfiguriere `PAPERLESS_OCR_LANGUAGE=deu+eng` für Deutsch+Englisch
- **Speicherplatz**: OCR und Thumbnails brauchen Speicher

## Hinweise

- Die Daten liegen in `./volumes/paperless/`
- Consume-Ordner: `./volumes/paperless/consume/`
- Port: 8010
- Paperless benötigt PostgreSQL und Redis
- Für große Archive: 4GB+ RAM empfohlen

## Weitere Informationen

- [Offizielle Dokumentation](https://docs.paperless-ngx.com/)
- [GitHub Repository](https://github.com/paperless-ngx/paperless-ngx)
- [Mobile App](https://github.com/astubenbord/paperless-mobile)
- [Reddit Community](https://www.reddit.com/r/paperlessngx/)
