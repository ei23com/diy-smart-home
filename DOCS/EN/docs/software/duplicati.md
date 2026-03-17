# Duplicati

[Duplicati](https://www.duplicati.com/) is a free backup tool for encrypted online backups. It supports many storage destinations and offers space-saving, encrypted backups.

!!!tip "Complement to ei23 Backup"
    Duplicati is excellent for encrypted offsite backups (cloud, NAS, etc.), while the [ei23 backup](../start/backuprestore.md) is designed for local backups.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  duplicati:
    image: duplicati/duplicati:latest
    container_name: duplicati
    hostname: HomePi
    ports:
      - "8200:8200"
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Berlin
    volumes:
      - ./volumes/duplicati/appdata/config:/config
      - ./volumes/duplicati/backups:/backups
      - ./volumes/duplicati/source:/source
```

## First Start

1. After starting, access Duplicati at `http://[IP]:8200`
2. Set a password (optional but recommended)
3. Create your first backup job

## Create Backup

1. Click **Add backup** → **Configure a new backup**
2. Enter name and description
3. Set an **encryption password** (don't lose it!)
4. Choose the **destination** (where to store the backup)
5. Choose the **source** (what to back up)
6. Configure the **schedule**
7. Save and start the backup

## Backup Destinations

Duplicati supports many destinations:

| Destination | Description |
|-------------|-------------|
| **Local Folder** | `/source` or `/backups` |
| **FTP/SFTP** | Remote server |
| **WebDAV** | Nextcloud, etc. |
| **Google Drive** | Cloud storage |
| **OneDrive** | Cloud storage |
| **Dropbox** | Cloud storage |
| **Amazon S3** | Object storage |
| **B2 Backblaze** | Affordable cloud storage |
| **Rclone** | Almost anything |

### Backing up ei23 Folder

To back up the ei23 folder:

1. **Source**: `/source` (which is `./volumes/duplicati/source`)
2. Link ei23 folder:

```yaml
volumes:
  - ./volumes/duplicati/source:/source
  - /home/user/ei23-docker:/source/ei23-docker:ro
```

## Encryption

!!!warning "Secure Password"
    Without the encryption password, backups cannot be restored! Store it in [Vaultwarden](vaultwarden.md).

Duplicati uses AES-256 encryption:

- **AES-256** - Standard, very secure
- **GPG** - Alternative

## Restore

1. Go to **Restore** → **Direct restore**
2. Select the backup destination
3. Enter the encryption password
4. Select files or everything
5. Start the restore

## Notes

- Admin interface on port 8200
- Configuration in `./volumes/duplicati/appdata/config/`
- Backups in `./volumes/duplicati/backups/`
- Source files in `./volumes/duplicati/source/`
- Duplicati automatically compresses and deduplicates backups

## Further Information

- [Official Website](https://www.duplicati.com/)
- [GitHub Repository](https://github.com/duplicati/duplicati)
- [Documentation](https://duplicati.readthedocs.io/)
