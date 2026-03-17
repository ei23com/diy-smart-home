# WireGuard VPN

[WireGuard](https://www.wireguard.com/) is a modern, fast, and secure VPN protocol. With the [wg-easy](https://github.com/wg-easy/wg-easy) Docker image, setup is particularly easy.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "Router Configuration Required"
    After installation, you need to forward port **51820 UDP** on your router to the server.

## Template

```yaml
  wireguard:
    image: ghcr.io/wg-easy/wg-easy
    container_name: wireguard
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - LANG=en
      - WG_HOST=your-domain-or-ip.org
      - PASSWORD=yourpassword
      - PORT=51821
      - WG_PORT=51820
      - WG_DEFAULT_ADDRESS=10.8.8.x
      - WG_DEFAULT_DNS=
      - WG_ALLOWED_IPS=0.0.0.0/1, 128.0.0.0/1, ::/1 # Full VPN
      # - WG_ALLOWED_IPS=10.8.8.0/24, 172.18.0.0/24 # only local VPN
    volumes:
      - ./volumes/wireguard:/etc/wireguard
    ports:
      - "51820:51820/udp"
      - "51821:51821/tcp"
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
```

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `WG_HOST` | Your domain or public IP | `mydomain.com` or `85.123.45.67` |
| `PASSWORD` | Password for the web interface | `SecurePassword123!` |
| `WG_PORT` | WireGuard port (UDP) | `51820` |
| `PORT` | Web interface port (TCP) | `51821` |
| `WG_DEFAULT_ADDRESS` | IP range for clients | `10.8.8.x` |
| `WG_ALLOWED_IPS` | Routes through VPN | See below |

### WG_ALLOWED_IPS Options

```yaml
# Option 1: Full VPN (all traffic through the tunnel)
WG_ALLOWED_IPS=0.0.0.0/1, 128.0.0.0/1, ::/1

# Option 2: Only home network through VPN (rest of internet directly)
WG_ALLOWED_IPS=10.8.8.0/24, 192.168.178.0/24
```

!!!tip "Recommended"
    For Smart Home use: Use **Option 2** (home network only) for better everyday speed.

## Configure Router

### Fritz!Box

1. Go to **Internet** → **Permit Access**
2. Click **New Port Forwarding**
3. Settings:
   - **Protocol:** UDP
   - **Port:** 51820
   - **To IP:** IP of your server
   - **Description:** WireGuard

### Other Routers

Forward the following ports:
- **51820 UDP** → Your server (WireGuard)
- **51821 TCP** → Your server (Web interface, optional)

## First Start

1. After startup, you can access the web interface at `http://[IP]:51821`
2. Log in with the configured `PASSWORD`
3. Create a new client:
   - Click **+ New Client**
   - Enter a name (e.g., "My Phone")
4. Download the configuration or scan the QR code

## Set Up Client

### Smartphone (Android/iOS)

1. Install the WireGuard app:
   - [Android](https://play.google.com/store/apps/details?id=com.wireguard.android)
   - [iOS](https://apps.apple.com/app/wireguard/id1441195209)
2. In the wg-easy interface, click the QR code icon
3. Scan the QR code with the app
4. Activate the VPN

### Desktop (Windows/macOS/Linux)

1. Install the WireGuard client:
   - [Windows](https://www.wireguard.com/install/)
   - [macOS](https://apps.apple.com/app/wireguard/id1451685025)
   - Linux: `sudo apt install wireguard`
2. Download the configuration file (.conf)
3. Import the file in the client
4. Activate the VPN

## VPN Types Explained

### Full VPN

```
Smartphone → Internet → Your Server → Internet
                 ↑
        Everything through VPN
```

**Advantages:** Maximum privacy, ad blocking (with Pi-hole)
**Disadvantages:** Slower, server bandwidth limited

### Split Tunnel (Home Network Only)

```
Smartphone → Internet (direct) → Destination
         ↘
          → Your Server → Home Network
```

**Advantages:** Faster in everyday use
**Disadvantages:** Only home network services protected

## Notes

- Data is stored in `./volumes/wireguard/`
- The web interface is accessible on port 51821
- **WG_HOST** must be your public IP or domain
- For dynamic IPs, use [Dynamic DNS](../start/remote-access#dynamic-dns-ddns)
- WireGuard is significantly faster than OpenVPN

## Security

- The `PASSWORD` only protects the web interface
- Each client has its own key
- Deactivate unused clients in the interface
- Regular updates of the Docker image

## Troubleshooting

### VPN Won't Connect

1. Check port forwarding on the router (UDP 51820)
2. Check `WG_HOST` - must be public IP/domain
3. Check firewall on the server
4. Test with `ping 10.8.8.1` to see if the tunnel works

### Slow Connection

1. Use split tunnel (`WG_ALLOWED_IPS` home network only)
2. Check upload speed of your internet connection
3. Change `WG_MTU=1280` if there are fragmentation issues

## Further Information

- [wg-easy GitHub](https://github.com/wg-easy/wg-easy)
- [WireGuard Documentation](https://www.wireguard.com/quickstart/)
- [WireGuard Configuration](https://www.wireguard.com/configuration/)
