# AdGuard Home

[AdGuard Home](https://adguard.com/en/adguard-home/overview.html) is a network-wide ad blocker and DNS server. It blocks ads, trackers, and malware for all devices on your network - without software on individual devices.

!!!tip "Alternative to Pi-hole"
    AdGuard Home is a modern alternative to [Pi-hole](../start/docker-compose) with a nicer web interface and easier configuration.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "Port 53 conflict"
    Port 53 (DNS) must not already be in use (e.g., by systemd-resolved or Pi-hole).

## Template

```yaml
  adguardhome:
    image: adguard/adguardhome
    container_name: adguardhome
    ports:
      - 53:53/tcp
      - 53:53/udp
      - 784:784/udp
      - 853:853/tcp
      - 3001:3000/tcp # Admin interface
      - 2229:80/tcp   # Alternative admin port
    volumes:
      - ./volumes/adguardhome/workdir:/opt/adguardhome/work
      - ./volumes/adguardhome/confdir:/opt/adguardhome/conf
    restart: unless-stopped
```

## First Start

1. After starting, access setup at `http://[IP]:3001`
2. Follow the installation wizard
3. Configure:
    - **Admin Interface**: Port 3001
    - **DNS Server**: Port 53
4. Create your admin password

## Set DNS on Devices

### Router (recommended)

Change the DNS server in your router to your server's IP:

1. Open router interface (e.g., Fritz!Box)
2. **Internet** → **Account Information** → **DNS Server**
3. Set DNS to server IP (e.g., `192.168.178.20`)

→ All devices on the network automatically use AdGuard

### Individual Devices

Alternatively, configure DNS per device:

| Device | Procedure |
|--------|-----------|
| **Windows** | Network adapter → IPv4 → DNS Server |
| **macOS** | System Preferences → Network → DNS |
| **Android** | WLAN → Advanced → DNS |
| **iOS** | WLAN → i → Configure DNS |

## Adding Blocklists

### Recommended Lists

1. Go to **Filters** → **DNS blocklists**
2. Click **Add blocklist** → **Choose from the list**

| List | Description |
|------|-------------|
| **AdGuard DNS filter** | Standard ad blocker |
| **Steven Black's List** | Ads + Malware |
| **OISD** | Very good all-round list |
| **Annoyances** | Cookie banners, etc. |

### Whitelist

Some services need to be allowed:

1. **Filters** → **DNS allowlists**
2. Add domain (e.g., `analytics.google.com` if needed)

## Notes

- Admin interface on port 3001
- DNS server on port 53
- DNS-over-TLS on port 853
- DNS-over-HTTPS on port 784
- Configuration in `./volumes/adguardhome/`

## Further Information

- [Official Website](https://adguard.com/en/adguard-home/overview.html)
- [GitHub Repository](https://github.com/AdguardTeam/AdGuardHome)
- [Documentation](https://github.com/AdguardTeam/AdGuardHome/wiki)
