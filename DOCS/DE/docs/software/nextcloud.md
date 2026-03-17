# Nextcloud

[Nextcloud](https://nextcloud.com/) ist eine Open-Source-Alternative zu Dropbox, Google Drive und iCloud. Du kannst Dateien synchronisieren, Kalender und Kontakte verwalten und vieles mehr - alles auf deinem eigenen Server.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Passwörter ändern!"
    Ändere alle Passwörter (`password_placeholder`, `password1_placeholder`) vor dem Start!

!!!warning "Netzwerk erforderlich"
    Füge das Nextcloud-Netzwerk zur docker-compose.yml hinzu.

## Template

```yaml
  nextcloud:
    image: nextcloud
    container_name: nextcloud
    ports:
      - "8080:80"
    volumes:
      - ./volumes/nextcloud/html:/var/www/html
    restart: unless-stopped
    depends_on: 
      - nextcloud_db
    links:
      - nextcloud_db
    networks:
      - default
      - nextcloud
    environment:
      - MYSQL_HOST=nextcloud_db
      - MYSQL_PASSWORD=password1_placeholder
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - TRUSTED_PROXIES=172.18.0.0/16
      # - OVERWRITEPROTOCOL=https
      # - OVERWRITEHOST=example.com
    logging:
      options:
        max-size: "5m"
        max-file: "3"

  nextcloud_db:
    image: yobasystems/alpine-mariadb:10.4.17
    container_name: nextcloud_db
    volumes:
      - ./volumes/nextcloud/db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=password_placeholder
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_PASSWORD=password1_placeholder
    restart: unless-stopped
    networks:
      - nextcloud
    logging:
      options:
        max-size: "5m"
        max-file: "3"
```

### Netzwerk hinzufügen

Füge dieses Netzwerk in deiner docker-compose.yml hinzu (z.B. unter `networks:`):

```yaml
  nextcloud:
    driver: bridge
    internal: true
```

## Erster Start

1. Nach dem Start erreichst du Nextcloud unter `http://[IP]:8080`
2. Erstelle einen Admin-Account
3. Warte, bis die Installation abgeschlossen ist

## HTTPS einrichten (Empfohlen)

!!!tip "Reverse Proxy nutzen"
    Für HTTPS nutze [Traefik](traefik.md) oder [Nginx Proxy Manager](nginxproxy.md).

### Mit Traefik

Entkommentiere und passe die Labels im Template an:

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.nextcloud.rule=Host(`nextcloud.deinedomain.de`)
  - traefik.http.routers.nextcloud.entrypoints=web-secured
  - traefik.http.routers.nextcloud.tls=true
  - traefik.http.routers.nextcloud.tls.certresolver=letsEncrypt
  - traefik.http.middlewares.nextcloud.headers.stsSeconds=15552000
```

### Umgebungsvariablen für HTTPS

```yaml
environment:
  - OVERWRITEPROTOCOL=https
  - OVERWRITEHOST=nextcloud.deinedomain.de
```

## Clients

### Desktop-Sync (Windows/macOS/Linux)

1. Installiere den [Nextcloud Desktop-Client](https://nextcloud.com/install/#install-clients)
2. Gib die Server-URL ein: `http://[IP]:8080` oder `https://nextcloud.deinedomain.de`
3. Melde dich an
4. Wähle die zu synchronisierenden Ordner

### Mobile App (Android/iOS)

1. Installiere die Nextcloud App:
   - [Android](https://play.google.com/store/apps/details?id=com.nextcloud.client)
   - [iOS](https://apps.apple.com/app/nextcloud/id1125420102)
2. Gib die Server-URL ein
3. Melde dich an

## Apps & Erweiterungen

Nextcloud kann durch Apps erweitert werden:

### Empfohlene Apps

| App | Beschreibung |
|-----|--------------|
| **Calendar** | Kalender mit CalDAV-Sync |
| **Contacts** | Kontakte mit CardDAV-Sync |
| **Deck** | Projektmanagement (Kanban) |
| **Notes** | Notizen |
| **Talk** | Videoanrufe und Chat |
| **Files PDF Viewer** | PDF-Vorschau |
| **Preview Generator** | Vorschaubilder vorab erstellen |

### Apps installieren

1. Klicke oben rechts auf dein Profil
2. Gehe zu **Apps**
3. Suche und installiere die gewünschte App

## Kalender & Kontakte synchronisieren

Nextcloud bietet CalDAV und CardDAV für die Synchronisation:

### Android (mit DAVx⁵)

1. Installiere [DAVx⁵](https://www.davx5.com/)
2. Füge ein Konto hinzu → **Anmelden mit URL und Benutzername**
3. URL: `http://[IP]:8080/remote.php/dav`
4. Synchronisiere Kalender und Kontakte

### iOS

1. Gehe zu **Einstellungen** → **Kalender** → **Konten**
2. **Andere Konto** → **CalDAV-Konto**
3. Server: `[IP]:8080`
4. Gib deine Zugangsdaten ein

## Backup & Restore

### Backup

```bash
# Daten sichern
cd ~/ei23-docker/
docker compose exec -u www-data nextcloud php occ maintenance:mode --on
sudo tar -czf nextcloud_backup.tar.gz volumes/nextcloud/
docker compose exec -u www-data nextcloud php occ maintenance:mode --off
```

### Restore

```bash
# Daten wiederherstellen
docker compose stop nextcloud
sudo rm -rf volumes/nextcloud/
sudo tar -xzf nextcloud_backup.tar.gz
docker compose start nextcloud
```

## OCC-Kommandozeile

Nextcloud hat ein nützliches CLI-Werkzeug:

```bash
# Allgemein
docker compose exec -u www-data nextcloud php occ [command]

# Beispiel: Upgrade nach Update
docker compose exec -u www-data nextcloud php occ upgrade

# Beispiel: Dateien scannen
docker compose exec -u www-data nextcloud php occ files:scan --all

# Beispiel: Wartungsmodus
docker compose exec -u www-data nextcloud php occ maintenance:mode --on/off
```

## Performance-Tipps

### Caching aktivieren

Füge in der `config.php` (unter `volumes/nextcloud/html/config/`) hinzu:

```php
'memcache.local' => '\OC\Memcache\APCu',
'memcache.distributed' => '\OC\Memcache\Redis',
'memcache.locking' => '\OC\Memcache\Redis',
'redis' => [
  'host' => 'redis',
  'port' => 6379,
],
```

### Preview Generator

Für schnellere Vorschaubilder:

```bash
docker compose exec -u www-data nextcloud php occ preview:generate-all
```

## Hinweise

- Die Daten werden in `./volumes/nextcloud/` gespeichert
- Die MariaDB-Datenbank läuft als separater Container
- Regelmäßige Backups der Datenbank sind essentiell!
- Nextcloud kann viel RAM verbrauchen - mindestens 2GB empfohlen

## Weitere Informationen

- [Offizielle Dokumentation](https://docs.nextcloud.com/)
- [Nextcloud Apps](https://apps.nextcloud.com/)
- [GitHub Repository](https://github.com/nextcloud/server)
- [Client-Download](https://nextcloud.com/install/#install-clients)
