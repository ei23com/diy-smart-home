# Vaultwarden (Bitwarden)

[Vaultwarden](https://github.com/dani-garcia/vaultwarden) ist eine alternative Server-Implementierung für den [Bitwarden](https://bitwarden.com/) Passwort-Manager. Es ist kompatibel mit allen offiziellen Bitwarden-Clients (Browser, Desktop, Mobile), bietet aber deutlich geringeren Ressourcenverbrauch.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

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
      - ADMIN_TOKEN=DEIN_ADMIN_TOKEN
```

!!!warning "Admin Token"
    Ersetze `DEIN_ADMIN_TOKEN` mit einem sicheren Token. Dieser wird für die Admin-Oberfläche benötigt. Generiere einen mit: `openssl rand -base64 48`

## Erster Start

1. Nach dem Start erreichst du Vaultwarden unter `http://[IP]:8812`
2. Erstelle deinen ersten Account (falls `SIGNUPS_ALLOWED=true`)
3. Richte die Browser-Erweiterung oder Mobile-App ein
4. **Wichtig:** Nach dem Einrichten setze `SIGNUPS_ALLOWED=false`!

## Clients einrichten

### Browser-Erweiterung

1. Installiere die [Bitwarden Browser-Erweiterung](https://bitwarden.com/download/)
2. Klicke auf das Einstellungen-Icon (Zahnrad)
3. Ändere die **Server-URL** zu `http://[IP]:8812`
4. Melde dich mit deinem Account an

### Mobile App

1. Installiere die Bitwarden App
2. Tippe oben auf das Einstellungs-Icon
3. Ändere die **Server-URL** zu `http://[IP]:8812` oder `https://vaultwarden.deinedomain.de`
4. Melde dich mit deinem Account an

### Desktop App

1. Installiere die [Bitwarden Desktop-App](https://bitwarden.com/download/)
2. Gehe zu **Einstellungen** → **Selbst-gehostet**
3. Gib die Server-URL ein

## Admin-Oberfläche

Die Admin-Oberfläche erreichst du unter `http://[IP]:8812/admin` mit dem `ADMIN_TOKEN`.

Hier kannst du:
- Benutzer verwalten
- Organisationen erstellen
- Registrierung deaktivieren
- SMTP-Einstellungen konfigurieren

## SMTP konfigurieren (E-Mail)

Für Passwort-Zurücksetzung und 2FA-E-Mails:

```yaml
environment:
  - SMTP_HOST=smtp.gmail.com
  - SMTP_FROM=vault@deinedomain.de
  - SMTP_PORT=587
  - SMTP_SECURITY=starttls
  - SMTP_USERNAME=deine@email.de
  - SMTP_PASSWORD=DEIN_APP_PASSWORT
```

!!!note "Gmail"
    Für Gmail musst du ein App-Passwort erstellen. Die normale Passwort-Authentifizierung funktioniert nicht.

## Sicherheitsempfehlungen

1. **Registrierung deaktivieren** nach dem Einrichten
2. **2FA aktivieren** für alle Accounts
3. **HTTPS nutzen** mit [Traefik](traefik.md) oder [Nginx Proxy Manager](nginxproxy.md)
4. **Regelmäßige Backups** erstellen
5. **Admin Token** sicher aufbewahren

## HTTPS mit Reverse Proxy

!!!tip "Empfohlen"
    Für die Nutzung außerhalb des Heimnetzes ist HTTPS zwingend erforderlich!

Beispiel mit Traefik:

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.vaultwarden.rule=Host(`vault.deinedomain.de`)
  - traefik.http.routers.vaultwarden.entrypoints=web-secured
  - traefik.http.routers.vaultwarden.tls=true
  - traefik.http.routers.vaultwarden.tls.certresolver=letsEncrypt
```

## Hinweise

- Die Daten werden in `./volumes/vaultwarden/` gespeichert
- Vaultwarden ist kompatibel mit ALLEN offiziellen Bitwarden-Clients
- Regelmäßige Backups des `/data` Ordners sind essentiell!
- Die Websocket-Verbindung ermöglicht Echtzeit-Sync zwischen Geräten

## Weitere Informationen

- [GitHub Repository](https://github.com/dani-garcia/vaultwarden)
- [Wiki](https://github.com/dani-garcia/vaultwarden/wiki)
- [Bitwarden Clients](https://bitwarden.com/download/)
