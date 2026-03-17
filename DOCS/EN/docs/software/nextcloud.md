# Nextcloud

[Nextcloud](https://nextcloud.com/) is an open-source alternative to Dropbox, Google Drive, and iCloud. You can sync files, manage calendars and contacts, and much more - all on your own server.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "Change Passwords!"
    Change all passwords (`password_placeholder`, `password1_placeholder`) before starting!

!!!warning "Network Required"
    Add the Nextcloud network to the docker-compose.yml.

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

### Add Network

Add this network to your docker-compose.yml (e.g., under `networks:`):

```yaml
  nextcloud:
    driver: bridge
    internal: true
```

## First Start

1. After startup, you can access Nextcloud at `http://[IP]:8080`
2. Create an admin account
3. Wait for the installation to complete

## Set Up HTTPS (Recommended)

!!!tip "Use Reverse Proxy"
    For HTTPS, use [Traefik](traefik.md) or [Nginx Proxy Manager](nginxproxy.md).

### With Traefik

Uncomment and adjust the labels in the template:

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.nextcloud.rule=Host(`nextcloud.yourdomain.com`)
  - traefik.http.routers.nextcloud.entrypoints=web-secured
  - traefik.http.routers.nextcloud.tls=true
  - traefik.http.routers.nextcloud.tls.certresolver=letsEncrypt
  - traefik.http.middlewares.nextcloud.headers.stsSeconds=15552000
```

### Environment Variables for HTTPS

```yaml
environment:
  - OVERWRITEPROTOCOL=https
  - OVERWRITEHOST=nextcloud.yourdomain.com
```

## Clients

### Desktop Sync (Windows/macOS/Linux)

1. Install the [Nextcloud Desktop Client](https://nextcloud.com/install/#install-clients)
2. Enter the server URL: `http://[IP]:8080` or `https://nextcloud.yourdomain.com`
3. Log in
4. Select the folders to sync

### Mobile App (Android/iOS)

1. Install the Nextcloud app:
   - [Android](https://play.google.com/store/apps/details?id=com.nextcloud.client)
   - [iOS](https://apps.apple.com/app/nextcloud/id1125420102)
2. Enter the server URL
3. Log in

## Apps & Extensions

Nextcloud can be extended through apps:

### Recommended Apps

| App | Description |
|-----|-------------|
| **Calendar** | Calendar with CalDAV sync |
| **Contacts** | Contacts with CardDAV sync |
| **Deck** | Project management (Kanban) |
| **Notes** | Notes |
| **Talk** | Video calls and chat |
| **Files PDF Viewer** | PDF preview |
| **Preview Generator** | Pre-generate thumbnails |

### Install Apps

1. Click on your profile in the top right
2. Go to **Apps**
3. Search for and install the desired app

## Sync Calendar & Contacts

Nextcloud offers CalDAV and CardDAV for synchronization:

### Android (with DAVx⁵)

1. Install [DAVx⁵](https://www.davx5.com/)
2. Add an account → **Login with URL and username**
3. URL: `http://[IP]:8080/remote.php/dav`
4. Sync calendars and contacts

### iOS

1. Go to **Settings** → **Calendar** → **Accounts**
2. **Other Account** → **CalDAV Account**
3. Server: `[IP]:8080`
4. Enter your credentials

## Backup & Restore

### Backup

```bash
# Backup data
cd ~/ei23-docker/
docker compose exec -u www-data nextcloud php occ maintenance:mode --on
sudo tar -czf nextcloud_backup.tar.gz volumes/nextcloud/
docker compose exec -u www-data nextcloud php occ maintenance:mode --off
```

### Restore

```bash
# Restore data
docker compose stop nextcloud
sudo rm -rf volumes/nextcloud/
sudo tar -xzf nextcloud_backup.tar.gz
docker compose start nextcloud
```

## OCC Command Line

Nextcloud has a useful CLI tool:

```bash
# General
docker compose exec -u www-data nextcloud php occ [command]

# Example: Upgrade after update
docker compose exec -u www-data nextcloud php occ upgrade

# Example: Scan files
docker compose exec -u www-data nextcloud php occ files:scan --all

# Example: Maintenance mode
docker compose exec -u www-data nextcloud php occ maintenance:mode --on/off
```

## Performance Tips

### Enable Caching

Add to `config.php` (under `volumes/nextcloud/html/config/`):

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

For faster thumbnails:

```bash
docker compose exec -u www-data nextcloud php occ preview:generate-all
```

## Notes

- Data is stored in `./volumes/nextcloud/`
- The MariaDB database runs as a separate container
- Regular database backups are essential!
- Nextcloud can consume a lot of RAM - at least 2GB recommended

## Further Information

- [Official Documentation](https://docs.nextcloud.com/)
- [Nextcloud Apps](https://apps.nextcloud.com/)
- [GitHub Repository](https://github.com/nextcloud/server)
- [Client Download](https://nextcloud.com/install/#install-clients)
