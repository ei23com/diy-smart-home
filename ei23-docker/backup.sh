#!/bin/bash
#
# THIS FILE GETS OVERWRITTEN WITH EVERY ei23 UPDATE
# YOUR OWN CHANGES CAN BE FOUND IN YOUR LAST BACKUP OR THEY ARE LOST
#
backuppfad="$HOME/backup"
volumes="$HOME/ei23-docker/volumes"
backupfile=HomeServerBackup-$(date +"%Y-%m-%d_%H-%M").tar.gz
# Backup InfluxDB
sudo mkdir -p $HOME/ei23-docker/backups/influxdb/db
sudo rm $HOME/ei23-docker/backups/influxdb/db/*
docker exec influxdb influxd backup -portable /var/lib/influxdb/backup
cd ~
mkdir -p $backuppfad/temp/node-red
mkdir -p $backuppfad/temp/volumes/ei23/web/
mkdir -p $backuppfad/temp/backups/influxdb/db
mkdir -p $backuppfad/temp/volumes/motioneye/
mkdir -p $backuppfad/temp/volumes/nextcloud/html/data
# Backup NodeRED
sudo rsync -a --exclude 'node_modules' $HOME/.node-red/ $backuppfad/temp/node-red/
# Backup Docker-Compose file
sudo cp $HOME/ei23-docker/docker-compose.yml $backuppfad/temp/docker-compose.yml
# Backup some essential Docker volumes
sudo rsync -a $HOME/ei23-docker/backups/influxdb/db/ $backuppfad/temp/backups/influxdb/db
sudo rsync -a --max-size=20k $volumes/motioneye/data/ $backuppfad/temp/volumes/motioneye/data
nextcloud_data=$(sudo ls $volumes/nextcloud/html/data/ | grep "^appdata_" | head -n 1)
sudo rsync -a --include={"config", "$volumes/nextcloud/html/data/"{"owncloud.db","$nextcloud_data/"{"appstore","theming","identityproof"}}} --exclude="*" $volumes/nextcloud/html/ $backuppfad/temp/volumes/nextcloud/html/
sudo rsync -a $volumes/grafana/ $backuppfad/temp/volumes/grafana
sudo rsync -a $volumes/wireguard/ $backuppfad/temp/volumes/wireguard
sudo rsync -a $volumes/tasmoadmin/ $backuppfad/temp/volumes/tasmoadmin
sudo rsync -a $volumes/bitwarden/ $backuppfad/temp/volumes/bitwarden
sudo rsync -a $volumes/ei23/web/programs.json $backuppfad/temp/volumes/ei23/web/programs.json
sudo rsync -a --exclude '*.log*' $volumes/mosquitto/ $backuppfad/temp/volumes/mosquitto
sudo rsync -a --exclude '*.log*' $volumes/traefik/ $backuppfad/temp/volumes/traefik
sudo rsync -a --exclude '*.db' $volumes/pihole/ $backuppfad/temp/volumes/pihole
sudo rsync -a --exclude '*.db' --exclude 'core' --exclude 'backups' --exclude '*.log' $volumes/homeassistant/ $backuppfad/temp/volumes/homeassistant
sudo rsync -a --max-size=50k $volumes/rhasspy/ $backuppfad/temp/volumes/rhasspy
sudo cp /etc/samba/smb.conf $backuppfad/temp/smb.conf
sudo cp /boot/config.txt $backuppfad/temp/bootconfig.txt
sudo cp /boot/cmdline.txt $backuppfad/temp/bootcmdline.txt
# your custom backup
source $HOME/ei23-docker/custom_backup.sh
# Backup Backup File
sudo cp $HOME/ei23-docker/backup.sh $backuppfad/temp/backup.sh
# Backup Terminal History
sudo cp .bash_history $backuppfad/temp/history.txt
cd $backuppfad/temp
sudo tar -cvzf ../$backupfile *
cd ~
sudo rm -r $backuppfad/temp
sudo chmod -R 777 $backuppfad/