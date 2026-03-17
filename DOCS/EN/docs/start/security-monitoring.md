# Security & Monitoring

Security is an important topic for your Smart Home Server. Here you'll find the most important measures and best practices.

## Basic Principles

!!!tip "Security Motto"
    **Only as much as necessary and as little as possible.**

### Basic Rules

- Only open ports to the outside if you know what you're doing
- Always use HTTPS for public services
- Strong passwords and 2FA where possible
- Install updates regularly
- Backups are your safety net

## Network Security

### Firewall

The ei23 server uses **UFW** (Uncomplicated Firewall) by default:

```bash
# Check status
sudo ufw status

# Enable firewall
sudo ufw enable

# Default: block incoming
sudo ufw default deny incoming

# Default: allow outgoing
sudo ufw default allow outgoing

# Allow SSH (important before enabling!)
sudo ufw allow ssh

# Allow specific ports
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8123/tcp  # Home Assistant (optional)
```

!!!warning "Don't forget SSH"
    Only enable UFW AFTER you've allowed SSH, otherwise you'll lock yourself out!

### Port Forwarding on Router

Only open **necessary ports** on your router:

| Service | Port | Recommendation |
|---------|------|----------------|
| **WireGuard VPN** | 51820/udp | ✅ Recommended |
| **HTTPS** | 443/tcp | ✅ With Reverse Proxy |
| **HTTP** | 80/tcp | ⚠️ Only for SSL redirect |
| **SSH** | 22/tcp | ❌ Not recommended (use VPN) |
| **Home Assistant** | 8123/tcp | ❌ Don't open directly |
| **Node-RED** | 1880/tcp | ❌ Don't open |
| **MQTT** | 1883/tcp | ❌ Don't open |

!!!danger "Never open directly"
    Never open unencrypted services or admin interfaces directly to the internet! Always use a VPN or Reverse Proxy with HTTPS.

### Reverse Proxy with SSL

For public services use [Traefik](../software/traefik.md) or [Nginx Proxy Manager](../software/nginxproxy.md):

```
Internet → Router (443) → Reverse Proxy (SSL) → Local Service
```

Benefits:
- ✅ Automatic SSL certificates
- ✅ Central access point
- ✅ Authentication possible

## Secure SSH

### Key Authentication

Disable password authentication and use SSH keys:

```bash
# Generate key on client
ssh-keygen -t ed25519

# Copy key to server
ssh-copy-id user@server-ip

# On server: disable password login
sudo nano /etc/ssh/sshd_config
```

In `/etc/ssh/sshd_config`:

```
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
```

```bash
# Restart SSH
sudo systemctl restart sshd
```

### SSH on Different Port

```bash
# Change port in /etc/ssh/sshd_config
Port 22222

# Adjust firewall
sudo ufw allow 22222/tcp
sudo ufw delete allow ssh
sudo systemctl restart sshd
```

## Password Security

### Strong Passwords

| Length | Recommendation |
|--------|----------------|
| **Minimum** | 12 characters |
| **Recommended** | 16+ characters |
| **Ideal** | 20+ characters |

### Password Manager

Use [Vaultwarden](../software/vaultwarden.md) for secure passwords:

- Generate random passwords
- One password per service
- Enable 2FA

### Change Passwords

```bash
# Via the ei23 script
ei23
# Select "Set new passwords"
```

## Two-Factor Authentication (2FA)

### Home Assistant

1. Go to **Profile** → **Two-Factor Authentication**
2. Click **Setup**
3. Scan QR code with authenticator app

### Vaultwarden

1. Go to **Settings** → **Two-Step Login**
2. Choose **Authenticator App** or **FIDO2**
3. Configure your preferred method

### Recommended Apps

| App | Platform |
|-----|----------|
| **Aegis** | Android (Open Source) |
| **Raivo OTP** | iOS (Open Source) |
| **Authy** | Multi-platform |

## Monitoring

### Uptime Kuma

[Uptime Kuma](../software/uptimekuma.md) monitors your services:

```yaml
# In docker-compose.yml
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    ports:
      - 3001:3001
    volumes:
      - ./volumes/uptime-kuma:/app/data
```

Monitor:
- ✅ Home Assistant (HTTP)
- ✅ Node-RED (HTTP)
- ✅ Vaultwarden (HTTP)
- ✅ Server reachability (Ping)
- ✅ Docker containers

### Notifications

Set up notifications for:

| Channel | Benefits |
|---------|----------|
| **Telegram** | Fast, free |
| **Discord** | Community overview |
| **Email** | Official, documented |
| **Pushover** | Push notifications |
| **Ntfy** | Open source, simple |

### Monitor Docker Containers

```yaml
# Uptime Kuma with Docker socket
volumes:
  - /var/run/docker.sock:/var/run/docker.sock:ro
```

Then in Uptime Kuma: Select **Docker Container** as monitor type.

### Server Resources

The [ei23 Dashboard](../start/ei23-dashboard/) shows live:
- CPU usage
- RAM usage
- Disk usage

For more detailed monitoring use [Grafana](../software/grafana.md) + [InfluxDB](../software/influx.md).

## Log Monitoring

### Check Important Logs

```bash
# ei23 Supervisor
journalctl -u ei23.service -f

# Node-RED
journalctl -u nodered.service -f

# Docker containers
docker compose logs -f [container_name]

# SSH login attempts
sudo journalctl -u ssh -f
sudo grep "Failed password" /var/log/auth.log
```

### Fail2Ban (optional)

Install Fail2Ban for automatic IP blocking:

```bash
sudo apt install fail2ban

# Configure
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

## Backup Security

### Backup Checklist

- [ ] Regular automatic backups
- [ ] Backups stored externally (USB/NAS/Cloud)
- [ ] Backup encryption for cloud
- [ ] Restore procedure tested
- [ ] Passwords backed up separately

### Encrypted Backups

```bash
# Backup encrypted
tar -czf - /home/user/ei23-docker/ | gpg -c > backup.tar.gz.gpg

# Decrypt
gpg -d backup.tar.gz.gpg | tar -xzf -
```

## Updates

### Regular Updates

!!!tip "Update Routine"
    Perform regular updates: `ei23 update`

| Update Type | Frequency | Command |
|-------------|-----------|---------|
| **System** | Weekly | `ei23 update` |
| **Docker** | Weekly | `ei23 du` |
| **ei23 Script** | When available | `ei23 ei23update` |

### Automatic Updates (optional)

```bash
# Cron job for automatic Docker updates
sudo crontab -e
```

```bash
# Sunday at 4 AM
0 4 * * 0 cd /home/user/ei23-docker && docker compose pull && docker compose up -d
```

## Security Checklist

### Basic Protection

- [ ] SSH Key authentication enabled
- [ ] Password login disabled
- [ ] Firewall (UFW) enabled
- [ ] Only necessary ports open
- [ ] VPN for remote access configured

### Services

- [ ] HTTPS for public services
- [ ] Strong passwords everywhere
- [ ] 2FA enabled (HA, Vaultwarden)
- [ ] Regular updates

### Monitoring

- [ ] Uptime Kuma installed
- [ ] Notifications configured
- [ ] Logs checked regularly

### Backup

- [ ] Automatic backups
- [ ] External backup copy
- [ ] Restore tested

## Remote Access

See [Remote Access](remote-access.md) for secure remote access options.

!!!tip "Recommendation"
    The most secure method for remote access is **WireGuard VPN**. See [WireGuard](../software/wireguard.md).
