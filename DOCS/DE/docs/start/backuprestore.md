# Backup & Restore

Regelmäßige Backups sind essentiell, um Datenverlust zu vermeiden. Hier erfährst du, wie du deine Daten sicherst und im Notfall wiederherstellst.

[![YT](https://ei23.de/bilder/YTthumbs/_yG0uWeRCDI.webp)](https://www.youtube.com/watch?v=_yG0uWeRCDI)

## Automatisches Backup mit dem ei23-Skript

Das ei23-Skript bietet eine Backup-Funktion:

```bash
ei23 backup
```

Dies erstellt ein Backup unter `/home/[user]/Backup/`.

!!!warning "Backup prüfen"
    Das Skript-Backup deckt die meisten Programme ab, aber nicht alle. Prüfe den Backup-Ordner und ergänze bei Bedarf.

## Was wird gesichert?

| Programm | Ordner | Backup enthalten? |
|----------|--------|-------------------|
| **Home Assistant** | `volumes/homeassistant/config` | ✅ |
| **NodeRED** | `~/.node-red/` | ✅ |
| **Grafana** | `volumes/grafana` | ✅ |
| **InfluxDB** | `volumes/influxdb` | ✅ |
| **Nextcloud** | `volumes/nextcloud` | ⚠️ Manuell |
| **Vaultwarden** | `volumes/vaultwarden` | ✅ |
| **Docker Compose** | `docker-compose.yml` | ✅ |

## Manuelles Backup

### Vollständiges Backup

```bash
cd ~/ei23-docker/

# Backup-Ordner erstellen
BACKUP_DIR=~/Backup/manual_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Docker Compose sichern
cp docker-compose.yml $BACKUP_DIR/

# Wichtige Volumes sichern
sudo tar -czf $BACKUP_DIR/homeassistant.tar.gz volumes/homeassistant/config/
sudo tar -czf $BACKUP_DIR/grafana.tar.gz volumes/grafana/
sudo tar -czf $BACKUP_DIR/vaultwarden.tar.gz volumes/vaultwarden/

# NodeRED sichern
sudo tar -czf $BACKUP_DIR/nodered.tar.gz ~/.node-red/

echo "Backup erstellt: $BACKUP_DIR"
```

### Nur Home Assistant

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

# Wartungsmodus aktivieren
docker compose exec -u www-data nextcloud php occ maintenance:mode --on

# Datenbank sichern
docker compose exec nextcloud_db mysqldump -u nextcloud -p nextcloud > ~/Backup/nextcloud_db.sql

# Dateien sichern
sudo tar -czf ~/Backup/nextcloud_files.tar.gz volumes/nextcloud/html/

# Wartungsmodus deaktivieren
docker compose exec -u www-data nextcloud php occ maintenance:mode --off
```

## Automatisierung mit Cron

### Tägliches Backup um 3 Uhr morgens

```bash
sudo crontab -e
```

Füge hinzu:

```bash
0 3 * * * bash /home/[user]/ei23-docker/backup.sh >> /home/[user]/backup.log 2>&1
```

### Backup-Skript erstellen

Erstelle `~/ei23-docker/backup.sh`:

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

# Alte Backups löschen (älter als 30 Tage)
find ~/Backup -type d -mtime +30 -exec rm -rf {} +

echo "Backup abgeschlossen: $BACKUP_DIR"
```

```bash
chmod +x ~/ei23-docker/backup.sh
```

## Externes Backup

!!!warning "Offsite-Backup"
    Ein Backup auf dem gleichen Server hilft nicht bei Festplattenausfall oder Hardware-Defekt. Sichere Backups extern!

### Optionen für externe Speicherung

| Ziel | Tool | Kosten |
|------|------|--------|
| **USB-Festplatte** | rsync, SCP | Einmalig ~50€ |
| **NAS (Synology/QNAP)** | rsync | Bereits vorhanden |
| **Cloud (encrypted)** | rclone + Crypt | ~5-10€/Monat |
| **2. Server** | rsync über VPN | Variabel |

### USB-Festplatte automatisch mounten

```bash
# Backup auf USB
rsync -av ~/Backup/ /media/usb-backup/

# In Cron automatisieren
0 4 * * * rsync -av ~/Backup/ /media/usb-backup/
```

### Cloud-Backup mit rclone

```bash
# rclone installieren
sudo apt install rclone

# Konfigurieren (einmalig)
rclone config

# Backup verschlüsselt hochladen
rclone sync ~/Backup encrypted-gdrive:ei23-backup
```

## Restore (Wiederherstellung)

### Home Assistant

```bash
cd ~/ei23-docker/

# Container stoppen
docker compose stop homeassistant

# Altes Verzeichnis sichern und leeren
sudo mv volumes/homeassistant/config volumes/homeassistant/config_old
sudo mkdir -p volumes/homeassistant/config

# Backup entpacken
sudo tar -xzf ~/Backup/homeassistant.tar.gz -C volumes/homeassistant/config/

# Container starten
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

# Backup wiederherstellen
docker cp ~/Backup/influxdb influxdb:/tmp/restore
docker compose start influxdb
docker compose exec influxdb influxd restore /tmp/restore
```

### Nextcloud

```bash
cd ~/ei23-docker/
docker compose stop nextcloud

# Dateien wiederherstellen
sudo rm -rf volumes/nextcloud/
sudo tar -xzf ~/Backup/nextcloud_files.tar.gz

# Datenbank wiederherstellen
docker compose start nextcloud_db
docker compose exec -T nextcloud_db mysql -u nextcloud -p nextcloud < ~/Backup/nextcloud_db.sql

docker compose start nextcloud
docker compose exec -u www-data nextcloud php occ maintenance:mode --off
```

## Backup-Checkliste

- [ ] Backup-Skript erstellt
- [ ] Cron-Job für automatische Backups eingerichtet
- [ ] Externes Backup konfiguriert
- [ ] Restore-Prozedur getestet
- [ ] Backup-Größe im Auge behalten
- [ ] Regelmäßige Prüfung der Backup-Integrität

## Weitere Informationen

- [RPI-Clone](https://github.com/billw2/rpi-clone) - Komplettes System-Backup für Raspberry Pi
- [Duplicati](../software/docker-compose) - Backup-Software als Docker
- [BorgBackup](https://www.borgbackup.org/) - Effiziente Backups
