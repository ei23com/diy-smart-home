# Backup & Restore

Regular backups are essential to avoid data loss. Here you'll learn how to back up your data and restore it in an emergency.

[![YT](https://ei23.de/bilder/YTthumbs/_yG0uWeRCDI.webp)](https://www.youtube.com/watch?v=_yG0uWeRCDI)

## Automatic Backup with the ei23 Script

The ei23 script provides a backup function:

```bash
ei23 backup
```

This creates a backup under `/home/[user]/Backup/`.

!!!warning "Check Backup"
    The script backup covers most programs, but not all. Check the backup folder and supplement if needed.

## What Gets Backed Up?

| Program | Folder | Backup included? |
|---------|--------|------------------|
| **Home Assistant** | `volumes/homeassistant/config` | ✅ |
| **NodeRED** | `~/.node-red/` | ✅ |
| **Grafana** | `volumes/grafana` | ✅ |
| **InfluxDB** | `volumes/influxdb` | ✅ |
| **Nextcloud** | `volumes/nextcloud` | ⚠️ Manual |
| **Vaultwarden** | `volumes/vaultwarden` | ✅ |
| **Docker Compose** | `docker-compose.yml` | ✅ |

## Manual Backup

### Full Backup

```bash
cd ~/ei23-docker/

# Create backup folder
BACKUP_DIR=~/Backup/manual_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Back up Docker Compose
cp docker-compose.yml $BACKUP_DIR/

# Back up important volumes
sudo tar -czf $BACKUP_DIR/homeassistant.tar.gz volumes/homeassistant/config/
sudo tar -czf $BACKUP_DIR/grafana.tar.gz volumes/grafana/
sudo tar -czf $BACKUP_DIR/vaultwarden.tar.gz volumes/vaultwarden/

# Back up NodeRED
sudo tar -czf $BACKUP_DIR/nodered.tar.gz ~/.node-red/

echo "Backup created: $BACKUP_DIR"
```

### Home Assistant Only

```bash
cd ~/ei23-docker/
docker compose exec -u www-data homeassistant tar -czf /config/backup.tar.gz /config
cp volumes/homeassistant/config/backup.tar.gz ~/Backup/
```

### InfluxDB

```bash
cd ~/ei23-docker/
docker compose exec influxdb influxd backup /tmp/influx-backup
docker cp influxdb:/tmp/influx-backup ~/Backup/influxdb_$(date +%Y%m%d)
```

### Nextcloud

```bash
cd ~/ei23-docker/

# Enable maintenance mode
docker compose exec -u www-data nextcloud php occ maintenance:mode --on

# Back up database
docker compose exec nextcloud_db mysqldump -u nextcloud -p nextcloud > ~/Backup/nextcloud_db.sql

# Back up files
sudo tar -czf ~/Backup/nextcloud_files.tar.gz volumes/nextcloud/html/

# Disable maintenance mode
docker compose exec -u www-data nextcloud php occ maintenance:mode --off
```

## Automation with Cron

### Daily Backup at 3 AM

```bash
sudo crontab -e
```

Add:

```bash
0 3 * * * bash /home/[user]/ei23-docker/backup.sh >> /home/[user]/backup.log 2>&1
```

### Create Backup Script

Create `~/ei23-docker/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR=~/Backup/$(date +%Y%m%d)
mkdir -p $BACKUP_DIR

cd ~/ei23-docker/

# Home Assistant
docker compose exec -u www-data homeassistant tar -czf /config/backup.tar.gz /config
cp volumes/homeassistant/config/backup.tar.gz $BACKUP_DIR/homeassistant.tar.gz

# Vaultwarden
sudo tar -czf $BACKUP_DIR/vaultwarden.tar.gz volumes/vaultwarden/

# Docker Compose
cp docker-compose.yml $BACKUP_DIR/

# Delete old backups (older than 30 days)
find ~/Backup -type d -mtime +30 -exec rm -rf {} +

echo "Backup completed: $BACKUP_DIR"
```

```bash
chmod +x ~/ei23-docker/backup.sh
```

## External Backup

!!!warning "Offsite Backup"
    A backup on the same server doesn't help with hard drive failure or hardware defects. Store backups externally!

### Options for External Storage

| Target | Tool | Cost |
|--------|------|------|
| **USB hard drive** | rsync, SCP | One-time ~50€ |
| **NAS (Synology/QNAP)** | rsync | Already available |
| **Cloud (encrypted)** | rclone + Crypt | ~5-10€/month |
| **2nd Server** | rsync over VPN | Variable |

### Auto-mount USB Hard Drive

```bash
# Backup to USB
rsync -av ~/Backup/ /media/usb-backup/

# Automate in Cron
0 4 * * * rsync -av ~/Backup/ /media/usb-backup/
```

### Cloud Backup with rclone

```bash
# Install rclone
sudo apt install rclone

# Configure (one-time)
rclone config

# Upload encrypted backup
rclone sync ~/Backup encrypted-gdrive:ei23-backup
```

## Restore

### Home Assistant

```bash
cd ~/ei23-docker/

# Stop container
docker compose stop homeassistant

# Back up and clear old directory
sudo mv volumes/homeassistant/config volumes/homeassistant/config_old
sudo mkdir -p volumes/homeassistant/config

# Extract backup
sudo tar -xzf ~/Backup/homeassistant.tar.gz -C volumes/homeassistant/config/

# Start container
docker compose start homeassistant
```

### Vaultwarden

```bash
cd ~/ei23-docker/
docker compose stop vaultwarden

sudo rm -rf volumes/vaultwarden/
sudo tar -xzf ~/Backup/vaultwarden.tar.gz

docker compose start vaultwarden
```

### InfluxDB

```bash
cd ~/ei23-docker/
docker compose stop influxdb

# Restore backup
docker cp ~/Backup/influxdb influxdb:/tmp/restore
docker compose start influxdb
docker compose exec influxdb influxd restore /tmp/restore
```

### Nextcloud

```bash
cd ~/ei23-docker/
docker compose stop nextcloud

# Restore files
sudo rm -rf volumes/nextcloud/
sudo tar -xzf ~/Backup/nextcloud_files.tar.gz

# Restore database
docker compose start nextcloud_db
docker compose exec -T nextcloud_db mysql -u nextcloud -p nextcloud < ~/Backup/nextcloud_db.sql

docker compose start nextcloud
docker compose exec -u www-data nextcloud php occ maintenance:mode --off
```

## Backup Checklist

- [ ] Backup script created
- [ ] Cron job for automatic backups set up
- [ ] External backup configured
- [ ] Restore procedure tested
- [ ] Backup size monitored
- [ ] Regular backup integrity checks

## More Information

- [RPI-Clone](https://github.com/billw2/rpi-clone) - Complete system backup for Raspberry Pi
- [Duplicati](../software/docker-compose) - Backup software as Docker
- [BorgBackup](https://www.borgbackup.org/) - Efficient backups
