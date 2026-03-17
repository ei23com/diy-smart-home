# Sicherheit & Monitoring

Sicherheit ist ein wichtiges Thema für deinen Smart Home Server. Hier findest du die wichtigsten Maßnahmen und Best Practices.

## Grundprinzipien

!!!tip "Sicherheits-Motto"
    **Nur so viel wie nötig und so wenig wie möglich.**

### Grundregeln

- Öffne Ports nach außen nur wenn du weißt, was du tust
- Nutze immer HTTPS für öffentliche Dienste
- Starke Passwörter und 2FA wo möglich
- Regelmäßige Updates einspielen
- Backups sind dein Sicherheitsnetz

## Netzwerk-Sicherheit

### Firewall

Der ei23-Server nutzt standardmäßig **UFW** (Uncomplicated Firewall):

```bash
# Status prüfen
sudo ufw status

# Firewall aktivieren
sudo ufw enable

# Standard: eingehend blockieren
sudo ufw default deny incoming

# Standard: ausgehend erlauben
sudo ufw default allow outgoing

# SSH erlauben (wichtig vor dem Aktivieren!)
sudo ufw allow ssh

# Bestimmte Ports erlauben
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8123/tcp  # Home Assistant (optional)
```

!!!warning "SSH nicht vergessen"
    Aktiviere UFW erst NACHDEM du SSH erlaubt hast, sonst sperst du dich aus!

### Portfreigabe am Router

Öffne am Router **nur notwendige Ports**:

| Dienst | Port | Empfehlung |
|--------|------|------------|
| **WireGuard VPN** | 51820/udp | ✅ Empfohlen |
| **HTTPS** | 443/tcp | ✅ Mit Reverse Proxy |
| **HTTP** | 80/tcp | ⚠️ Nur für SSL-Weiterleitung |
| **SSH** | 22/tcp | ❌ Nicht empfohlen (nutze VPN) |
| **Home Assistant** | 8123/tcp | ❌ Nicht direkt öffnen |
| **Node-RED** | 1880/tcp | ❌ Nicht öffnen |
| **MQTT** | 1883/tcp | ❌ Nicht öffnen |

!!!danger "Niemals direkt öffnen"
    Öffne niemals unverschlüsselte Dienste oder Admin-Oberflächen direkt ins Internet! Nutze immer ein VPN oder Reverse Proxy mit HTTPS.

### Reverse Proxy mit SSL

Für öffentliche Dienste nutze [Traefik](../software/traefik.md) oder [Nginx Proxy Manager](../software/nginxproxy.md):

```
Internet → Router (443) → Reverse Proxy (SSL) → Lokaler Dienst
```

Vorteile:
- ✅ Automatische SSL-Zertifikate
- ✅ Zentraler Zugriffspunkt
- ✅ Authentifizierung möglich

## SSH absichern

### Key-Authentifizierung

Passwort-Authentifizierung deaktivieren und SSH-Keys nutzen:

```bash
# Key auf Client generieren
ssh-keygen -t ed25519

# Key auf Server kopieren
ssh-copy-id user@server-ip

# Auf dem Server: Passwort-Login deaktivieren
sudo nano /etc/ssh/sshd_config
```

In `/etc/ssh/sshd_config`:

```
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
```

```bash
# SSH neu starten
sudo systemctl restart sshd
```

### SSH auf anderen Port

```bash
# Port ändern in /etc/ssh/sshd_config
Port 22222

# Firewall anpassen
sudo ufw allow 22222/tcp
sudo ufw delete allow ssh
sudo systemctl restart sshd
```

## Passwort-Sicherheit

### Sichere Passwörter

| Länge | Empfehlung |
|-------|------------|
| **Minimum** | 12 Zeichen |
| **Empfohlen** | 16+ Zeichen |
| **Ideal** | 20+ Zeichen |

### Passwort-Manager

Nutze [Vaultwarden](../software/vaultwarden.md) für sichere Passwörter:

- Zufällige Passwörter generieren
- Ein Passwort pro Dienst
- 2FA aktivieren

### Passwörter ändern

```bash
# Über das ei23-Skript
ei23
# Wähle "Neue Passwörter setzen"
```

## Zwei-Faktor-Authentifizierung (2FA)

### Home Assistant

1. Gehe zu **Profil** → **Zwei-Faktor-Authentifizierung**
2. Klicke **Einrichten**
3. Scanne QR-Code mit Authentikator-App

### Vaultwarden

1. Gehe zu **Einstellungen** → **Zwei-Schritt-Login**
2. Wähle **Authentikator-App** oder **FIDO2**
3. Konfiguriere deine bevorzugte Methode

### Empfohlene Apps

| App | Plattform |
|-----|-----------|
| **Aegis** | Android (Open Source) |
| **Raivo OTP** | iOS (Open Source) |
| **Authy** | Multi-Plattform |

## Monitoring

### Uptime Kuma

[Uptime Kuma](../software/uptimekuma.md) überwacht deine Dienste:

```yaml
# In docker-compose.yml
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    ports:
      - 3001:3001
    volumes:
      - ./volumes/uptime-kuma:/app/data
```

Überwache:
- ✅ Home Assistant (HTTP)
- ✅ Node-RED (HTTP)
- ✅ Vaultwarden (HTTP)
- ✅ Server-Erreichbarkeit (Ping)
- ✅ Docker-Container

### Benachrichtigungen

Richte Benachrichtigungen ein für:

| Kanal | Vorteile |
|-------|----------|
| **Telegram** | Schnell, kostenlos |
| **Discord** | Community-Übersicht |
| **Email** | Offiziell, dokumentiert |
| **Pushover** | Push-Benachrichtigungen |
| **Ntfy** | Open Source, einfach |

### Docker-Container überwachen

```yaml
# Uptime Kuma mit Docker-Socket
volumes:
  - /var/run/docker.sock:/var/run/docker.sock:ro
```

Dann in Uptime Kuma: **Docker-Container** als Monitor-Typ wählen.

### Server-Ressourcen

Das [ei23 Dashboard](../start/ei23-dashboard/) zeigt live:
- CPU-Auslastung
- RAM-Nutzung
- Disk-Belegung

Für detaillierteres Monitoring nutze [Grafana](../software/grafana.md) + [InfluxDB](../software/influx.md).

## Log-Überwachung

### Wichtige Logs prüfen

```bash
# ei23 Supervisor
journalctl -u ei23.service -f

# Node-RED
journalctl -u nodered.service -f

# Docker Container
docker compose logs -f [container_name]

# SSH Login-Versuche
sudo journalctl -u ssh -f
sudo grep "Failed password" /var/log/auth.log
```

### Fail2Ban (optional)

Installiere Fail2Ban für automatische IP-Sperren:

```bash
sudo apt install fail2ban

# Konfigurieren
sudo nano /etc/fail2ban/jail.local
```

```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Backup-Sicherheit

### Backup-Checkliste

- [ ] Regelmäßige automatische Backups
- [ ] Backups extern speichern (USB/NAS/Cloud)
- [ ] Backup-Verschlüsselung für Cloud
- [ ] Restore-Prozedur getestet
- [ ] Passwörter separat gesichert

### Verschlüsselte Backups

```bash
# Verschlüsselt sichern
tar -czf - /home/user/ei23-docker/ | gpg -c > backup.tar.gz.gpg

# Entschlüsseln
gpg -d backup.tar.gz.gpg | tar -xzf -
```

## Updates

### Regelmäßige Updates

!!!tip "Update-Routine"
    Führe regelmäßig Updates durch: `ei23 update`

| Update-Typ | Häufigkeit | Befehl |
|------------|------------|--------|
| **System** | Wöchentlich | `ei23 update` |
| **Docker** | Wöchentlich | `ei23 du` |
| **ei23-Script** | Bei Verfügbarkeit | `ei23 ei23update` |

### Automatische Updates (optional)

```bash
# Cron-Job für automatische Docker-Updates
sudo crontab -e
```

```bash
# Sonntag um 4 Uhr morgens
0 4 * * 0 cd /home/user/ei23-docker && docker compose pull && docker compose up -d
```

## Sicherheits-Checkliste

### Grundschutz

- [ ] SSH Key-Authentifizierung aktiviert
- [ ] Passwort-Login deaktiviert
- [ ] Firewall (UFW) aktiviert
- [ ] Nur notwendige Ports geöffnet
- [ ] VPN für Remote-Zugriff eingerichtet

### Dienste

- [ ] HTTPS für öffentliche Dienste
- [ ] Starke Passwörter überall
- [ ] 2FA aktiviert (HA, Vaultwarden)
- [ ] Regelmäßige Updates

### Monitoring

- [ ] Uptime Kuma installiert
- [ ] Benachrichtigungen konfiguriert
- [ ] Logs regelmäßig prüfen

### Backup

- [ ] Automatische Backups
- [ ] Externe Backup-Kopie
- [ ] Restore getestet

## Fernzugriff

Siehe [Fernzugriff](remote-access.md) für sichere Remote-Zugriffs-Optionen.

!!!tip "Empfehlung"
    Die sicherste Methode für Fernzugriff ist **WireGuard VPN**. Siehe [WireGuard](../software/wireguard.md).
