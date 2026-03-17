# Vaultwarden (Bitwarden)

[Vaultwarden](https://github.com/dani-garcia/vaultwarden) is an alternative server implementation for the [Bitwarden](https://bitwarden.com/) password manager. It is compatible with all official Bitwarden clients (browser, desktop, mobile), but uses significantly fewer resources.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    ports:
      - 8812:80
    volumes:
      - ./volumes/vaultwarden:/data
    environment:
      - SIGNUPS_ALLOWED=true
      - WEBSOCKET_ENABLED=true
      - ADMIN_TOKEN=YOUR_ADMIN_TOKEN
```

!!!warning "Admin Token"
    Replace `YOUR_ADMIN_TOKEN` with a secure token. This is required for the admin interface. Generate one with: `openssl rand -base64 48`

## First Start

1. After startup, you can access Vaultwarden at `http://[IP]:8812`
2. Create your first account (if `SIGNUPS_ALLOWED=true`)
3. Set up the browser extension or mobile app
4. **Important:** After setup, set `SIGNUPS_ALLOWED=false`!

## Set Up Clients

### Browser Extension

1. Install the [Bitwarden Browser Extension](https://bitwarden.com/download/)
2. Click on the settings icon (gear)
3. Change the **Server URL** to `http://[IP]:8812`
4. Log in with your account

### Mobile App

1. Install the Bitwarden app
2. Tap the settings icon at the top
3. Change the **Server URL** to `http://[IP]:8812` or `https://vaultwarden.yourdomain.com`
4. Log in with your account

### Desktop App

1. Install the [Bitwarden Desktop App](https://bitwarden.com/download/)
2. Go to **Settings** → **Self-hosted**
3. Enter the server URL

## Admin Interface

You can access the admin interface at `http://[IP]:8812/admin` with the `ADMIN_TOKEN`.

Here you can:
- Manage users
- Create organizations
- Disable registration
- Configure SMTP settings

## Configure SMTP (Email)

For password reset and 2FA emails:

```yaml
environment:
  - SMTP_HOST=smtp.gmail.com
  - SMTP_FROM=vault@yourdomain.com
  - SMTP_PORT=587
  - SMTP_SECURITY=starttls
  - SMTP_USERNAME=your@email.com
  - SMTP_PASSWORD=YOUR_APP_PASSWORD
```

!!!note "Gmail"
    For Gmail, you need to create an app password. Regular password authentication does not work.

## Security Recommendations

1. **Disable registration** after setup
2. **Enable 2FA** for all accounts
3. **Use HTTPS** with [Traefik](traefik.md) or [Nginx Proxy Manager](nginxproxy.md)
4. **Create regular backups**
5. **Keep admin token** secure

## HTTPS with Reverse Proxy

!!!tip "Recommended"
    For use outside the home network, HTTPS is absolutely required!

Example with Traefik:

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.vaultwarden.rule=Host(`vault.yourdomain.com`)
  - traefik.http.routers.vaultwarden.entrypoints=web-secured
  - traefik.http.routers.vaultwarden.tls=true
  - traefik.http.routers.vaultwarden.tls.certresolver=letsEncrypt
```

## Notes

- Data is stored in `./volumes/vaultwarden/`
- Vaultwarden is compatible with ALL official Bitwarden clients
- Regular backups of the `/data` folder are essential!
- The websocket connection enables real-time sync between devices

## Further Information

- [GitHub Repository](https://github.com/dani-garcia/vaultwarden)
- [Wiki](https://github.com/dani-garcia/vaultwarden/wiki)
- [Bitwarden Clients](https://bitwarden.com/download/)
