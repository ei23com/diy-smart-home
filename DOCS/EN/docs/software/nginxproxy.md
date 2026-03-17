# Nginx Proxy Manager

[Nginx Proxy Manager](https://nginxproxymanager.com/) is a simple reverse proxy with a web interface. It allows you to make local services accessible via HTTPS with automatic SSL certificates (Let's Encrypt).

!!!tip "Simple Alternative to Traefik"
    The Nginx Proxy Manager is significantly easier to set up than [Traefik](traefik.md), but offers less automation.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  nginxproxymanger:
    image: jc21/nginx-proxy-manager:latest
    container_name: nginxproxymanger
    restart: unless-stopped
    ports:
      - "80:80"    # HTTP
      - "81:81"    # Admin Interface
      - "443:443"  # HTTPS
    volumes:
      - ./volumes/nginx-proxy-manager/data:/data
      - ./volumes/nginx-proxy-manager/letsencrypt:/etc/letsencrypt
```

## First Start

1. After startup, you can access the admin interface at `http://[IP]:81`
2. Log in with the default credentials:
   - **Email:** `admin@example.com`
   - **Password:** `changeme`
3. Change the password immediately!

## Set Up Reverse Proxy

### Example: Home Assistant

1. Go to **Hosts** → **Proxy Hosts**
2. Click **Add Proxy Host**
3. Settings:

| Field | Value |
|-------|-------|
| **Domain Names** | `home.yourdomain.com` |
| **Scheme** | `http` |
| **Forward Hostname / IP** | `172.17.0.1` (Docker Gateway) |
| **Forward Port** | `8123` |
| **Block Common Exploits** | ✅ |
| **Websockets Support** | ✅ |

4. **SSL** tab:
   - **SSL Certificate** → **Request a new SSL Certificate**
   - **Force SSL** ✅
   - **HTTP/2 Support** ✅
   - **Email** → Your email
   - **I Agree** ✅

### Example: Nextcloud

| Field | Value |
|-------|-------|
| **Domain Names** | `nextcloud.yourdomain.com` |
| **Scheme** | `http` |
| **Forward Hostname / IP** | `172.17.0.1` |
| **Forward Port** | `8080` |

### Example: Grafana

| Field | Value |
|-------|-------|
| **Domain Names** | `grafana.yourdomain.com` |
| **Scheme** | `http` |
| **Forward Hostname / IP** | `grafana` (Container name) |
| **Forward Port** | `3000` |

## SSL Certificates

### Automatic (Let's Encrypt)

1. In the proxy host settings
2. **SSL** tab → **Request a new SSL Certificate**
3. Enter email and accept conditions
4. Certificate is automatically created and renewed

### Manual

1. Go to **SSL Certificates**
2. Click **Add SSL Certificate**
3. **Upload** or **Let's Encrypt**

## Access Lists

To protect services with passwords:

1. Go to **Access Lists**
2. Click **Add Access List**
3. Configure **HTTP Basic Auth**
4. Assign the list to a proxy host

## Router Configuration

!!!warning "Port Forwarding on Router Required"
    For HTTPS, you need to forward ports **80** and **443** on your router to your server.

### Fritz!Box

1. **Internet** → **Permit Access** → **New Port Forwarding**
2. **Port sharing for applications:**
   - HTTP (Port 80)
   - HTTPS (Port 443)
3. To the IP address of the server

## Nginx Proxy Manager vs. Traefik

| Feature | Nginx Proxy Manager | Traefik |
|---------|---------------------|---------|
| **Web Interface** | ✅ Simple | ⚠️ More complex |
| **Setup** | ✅ Very easy | ⚠️ YAML configuration |
| **Docker Integration** | ⚠️ Manual | ✅ Automatic |
| **Automatic Detection** | ❌ No | ✅ Yes |
| **Let's Encrypt** | ✅ Easy | ✅ Automatic |
| **Middleware** | ⚠️ Limited | ✅ Very flexible |

!!!tip "Recommendation"
    - **Nginx Proxy Manager**: Ideal for beginners, few services
    - **Traefik**: Ideal for many Docker containers, automation

## Notes

- Data is stored in `./volumes/nginx-proxy-manager/`
- Admin interface on port 81
- Port 80 (HTTP) and 443 (HTTPS) for proxy
- Ports 80/443 must be forwarded on the router

## Further Information

- [Official Documentation](https://nginxproxymanager.com/guide/)
- [GitHub Repository](https://github.com/NginxProxyManager/nginx-proxy-manager)
- [Let's Encrypt](https://letsencrypt.org/)
