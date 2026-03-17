# Remote Access

To access your Smart Home server from anywhere, there are various options. Here you'll learn which options are available and which is best suited for you.

## Overview

| Method | Security | Simplicity | Recommendation |
|--------|----------|------------|----------------|
| **WireGuard VPN** | ✅✅✅ Very secure | ✅ Good | ⭐ **Recommended** |
| **Reverse Proxy (HTTPS)** | ✅✅ Secure | ✅ Good | For public services |
| **SSH Tunnel** | ✅✅✅ Very secure | ⚠️ Complex | For experts |
| **Port Forwarding** | ❌ Insecure | ✅ Simple | **Not recommended!** |

!!!warning "Avoid Port Forwarding"
    **Never** expose unencrypted services (HTTP, MQTT, etc.) directly to the internet! Always use VPN or HTTPS with a reverse proxy.

---

## VPN (Recommended)

A VPN is the most secure method for remote access. It creates an encrypted "virtual cable" into your home network.

### WireGuard

[WireGuard](../software/wireguard.md) is a modern, fast VPN protocol. With the `wg-easy` template, setup is very simple.

**Advantages:**
- ✅ Very secure (state-of-the-art encryption)
- ✅ Very fast (low latency)
- ✅ Easy setup with wg-easy
- ✅ Apps for all platforms
- ✅ Access to ALL devices in your home network

**Disadvantages:**
- ⚠️ Requires a static IP or Dynamic DNS
- ⚠️ Port forwarding on router needed (UDP)

### Setup

1. Install [WireGuard](../software/wireguard.md) via the template
2. Configure your router:
   - **Port 51820 UDP** → Your server
3. Set up clients in the wg-easy web interface
4. Download the config or scan the QR code with the app

### Clients

| Platform | App |
|----------|-----|
| **Android** | [WireGuard App](https://play.google.com/store/apps/details?id=com.wireguard.android) |
| **iOS** | [WireGuard App](https://apps.apple.com/app/wireguard/id1441195209) |
| **Windows** | [WireGuard for Windows](https://www.wireguard.com/install/) |
| **macOS** | [WireGuard for macOS](https://apps.apple.com/app/wireguard/id1451685025) |
| **Linux** | `sudo apt install wireguard` |

---

## Reverse Proxy

A reverse proxy makes local services accessible via HTTPS. Ideal for services that should also be used by others (e.g. family).

### Nginx Proxy Manager

The [Nginx Proxy Manager](../software/nginxproxy.md) is the easiest starting point:

**Advantages:**
- ✅ Simple web interface
- ✅ Automatic SSL certificates (Let's Encrypt)
- ✅ User-friendly

**Setup:**
1. Install Nginx Proxy Manager
2. Set up a domain/subdomain (e.g. `home.mydomain.com`)
3. Port forwarding: Port 80 + 443 → Your server
4. Let the SSL certificate be created automatically

### Traefik

[Traefik](../software/traefik.md) is more powerful, but more complex to set up:

**Advantages:**
- ✅ Automatic Docker container detection
- ✅ Very flexible
- ✅ Well documented

**Disadvantages:**
- ⚠️ Steeper learning curve

---

## Dynamic DNS (DDNS)

Without a static IP address from your provider, you need Dynamic DNS:

### Free DDNS Providers

| Provider | Website | Notes |
|----------|---------|-------|
| **DuckDNS** | duckdns.org | Simple, free |
| **No-IP** | noip.com | Free (confirm every 30 days) |
| **Dynv6** | dynv6.com | Free, supports IPv6 |
| **Cloudflare** | cloudflare.com | Own domain required |

### Fritz!Box DDNS

The Fritz!Box has a built-in DDNS service:
1. Go to **Internet** → **Sharing** → **Dynamic DNS**
2. Select your provider
3. Enter your credentials

---

## SSH (For Experts)

SSH tunnels provide secure access, but are more complex:

### Create SSH Tunnel

```bash
# Forward local port to remote
ssh -L 8123:localhost:8123 user@your-server.com

# Home Assistant is now accessible at http://localhost:8123
```

### SSH with Public Key

Secure SSH connections with key files:
[Secure SSH connections with Public Key authentication](https://ei23.de/smarthome/ssh-verbindungen-mit-public-key-verfahren-absichern/)

---

## Security Checklist

- [ ] Use **VPN** or **Reverse Proxy with HTTPS**
- [ ] Use **strong passwords** everywhere
- [ ] Enable **2FA** where possible (Home Assistant, Vaultwarden)
- [ ] Apply **updates** regularly
- [ ] Configure **firewall** on the router
- [ ] Only forward **necessary ports**
- [ ] Check **logs** regularly (Uptime Kuma)

## My Recommendation

| Situation | Recommendation |
|-----------|----------------|
| **Only you** access it | WireGuard VPN |
| **Family** uses services | WireGuard VPN + individual Reverse Proxy entries |
| **Public website** | Reverse Proxy (Traefik/Nginx) with HTTPS |
| **Best security** | WireGuard VPN + SSH as backup |

!!!tip "Combination"
    The best solution is often a combination: **WireGuard VPN** for you and **Reverse Proxy** for services that must be accessible without VPN (e.g. Nextcloud for family).

## More Information

- [WireGuard Documentation](../software/wireguard.md)
- [Nginx Proxy Manager](../software/nginxproxy.md)
- [Traefik](../software/traefik.md)
