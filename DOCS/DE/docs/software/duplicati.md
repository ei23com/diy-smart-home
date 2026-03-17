# Duplicati

[Duplicati](https://www.duplicati.com/) ist ein freies Backup-Tool für verschlüsselte Online-Backups. Es unterstützt viele Speicherziele und bietet platzsparende, verschlüsselte Backups.

!!!tip "Ergänzung zum ei23-Backup"
    Duplicati eignet sich hervorragend für verschlüsselte Offsite-Backups (Cloud, NAS, etc.), während das [ei23-Backup](../start/backuprestore.md) für lokale Sicherungen gedacht ist.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

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

## Erster Start

1. Nach dem Start erreichst du Duplicati unter `http://[IP]:8200`
2. Richte ein Passwort ein (optional, aber empfohlen)
3. Erstelle deinen ersten Backup-Job

## Backup erstellen

1. Klicke auf **Add backup** → **Configure a new backup**
2. Gib Name und Beschreibung ein
3. Setze ein **Verschlüsselungspasswort** (nicht verlieren!)
4. Wähle das **Ziel** (wo das Backup gespeichert wird)
5. Wähle die **Quelle** (was gesichert werden soll)
6. Konfiguriere den **Zeitplan**
7. Speichere und starte das Backup

## Backup-Ziele

Duplicati unterstützt viele Ziele:

| Ziel | Beschreibung |
|------|--------------|
| **Lokaler Ordner** | `/source` oder `/backups` |
| **FTP/SFTP** | Remote-Server |
| **WebDAV** | Nextcloud, etc. |
| **Google Drive** | Cloud-Speicher |
| **OneDrive** | Cloud-Speicher |
| **Dropbox** | Cloud-Speicher |
| **Amazon S3** | Object Storage |
| **B2 Backblaze** | Günstiger Cloud-Speicher |
| **Rclone** | Fast alles |

### ei23-Ordner sichern

Um den ei23-Ordner zu sichern:

1. **Quelle**: `/source` (ist `./volumes/duplicati/source`)
2. Verlinke ei23-Ordner:

```yaml
volumes:
  - ./volumes/duplicati/source:/source
  - /home/user/ei23-docker:/source/ei23-docker:ro
```

## Verschlüsselung

!!!warning "Passwort sichern"
    Ohne das Verschlüsselungspasswort sind die Backups nicht wiederherstellbar! Speichere es in [Vaultwarden](vaultwarden.md).

Duplicati nutzt AES-256 Verschlüsselung:

- **AES-256** - Standard, sehr sicher
- **GPG** - Alternative

## Restore

1. Gehe zu **Restore** → **Direct restore**
2. Wähle das Backup-Ziel
3. Gib das Verschlüsselungspasswort ein
4. Wähle Dateien oder Alles
5. Starte die Wiederherstellung

## Hinweise

- Admin-Oberfläche auf Port 8200
- Konfiguration in `./volumes/duplicati/appdata/config/`
- Backups in `./volumes/duplicati/backups/`
- Quelldateien in `./volumes/duplicati/source/`
- Duplicati komprimiert und dedupliziert Backups automatisch

## Weitere Informationen

- [Offizielle Website](https://www.duplicati.com/)
- [GitHub Repository](https://github.com/duplicati/duplicati)
- [Dokumentation](https://duplicati.readthedocs.io/)
