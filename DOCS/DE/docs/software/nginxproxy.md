# Nginx Proxy Manager

[Nginx Proxy Manager](https://nginxproxymanager.com/) ist ein einfacher Reverse Proxy mit Weboberfläche. Er ermöglicht es dir, lokale Dienste über HTTPS mit automatischen SSL-Zertifikaten (Let's Encrypt) erreichbar zu machen.

!!!tip "Einfache Alternative zu Traefik"
    Der Nginx Proxy Manager ist deutlich einfacher einzurichten als [Traefik](traefik.md), bietet aber weniger Automatisierung.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

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

## Erster Start

1. Nach dem Start erreichst du die Admin-Oberfläche unter `http://[IP]:81`
2. Login mit den Standard-Zugangsdaten:
   - **Email:** `admin@example.com`
   - **Password:** `changeme`
3. Ändere sofort das Passwort!

## Reverse Proxy einrichten

### Beispiel: Home Assistant

1. Gehe zu **Hosts** → **Proxy Hosts**
2. Klicke auf **Add Proxy Host**
3. Einstellungen:

| Feld | Wert |
|------|------|
| **Domain Names** | `home.deinedomain.de` |
| **Scheme** | `http` |
| **Forward Hostname / IP** | `172.17.0.1` (Docker Gateway) |
| **Forward Port** | `8123` |
| **Block Common Exploits** | ✅ |
| **Websockets Support** | ✅ |

4. Reiter **SSL**:
   - **SSL Certificate** → **Request a new SSL Certificate**
   - **Force SSL** ✅
   - **HTTP/2 Support** ✅
   - **Email** → Deine Email
   - **I Agree** ✅

### Beispiel: Nextcloud

| Feld | Wert |
|------|------|
| **Domain Names** | `nextcloud.deinedomain.de` |
| **Scheme** | `http` |
| **Forward Hostname / IP** | `172.17.0.1` |
| **Forward Port** | `8080` |

### Beispiel: Grafana

| Feld | Wert |
|------|------|
| **Domain Names** | `grafana.deinedomain.de` |
| **Scheme** | `http` |
| **Forward Hostname / IP** | `grafana` (Container-Name) |
| **Forward Port** | `3000` |

## SSL-Zertifikate

### Automatisch (Let's Encrypt)

1. In den Proxy Host Einstellungen
2. Reiter **SSL** → **Request a new SSL Certificate**
3. Email eingeben und Bedingungen akzeptieren
4. Zertifikat wird automatisch erstellt und erneuert

### Manuell

1. Gehe zu **SSL Certificates**
2. Klicke **Add SSL Certificate**
3. **Upload** oder **Let's Encrypt**

## Access Lists

Um Dienste mit Passwörter zu schützen:

1. Gehe zu **Access Lists**
2. Klicke **Add Access List**
3. **HTTP Basic Auth** konfigurieren
4. Weise die Liste einem Proxy Host zu

## Router-Konfiguration

!!!warning "Portfreigabe am Router nötig"
    Für HTTPS musst du am Router die Ports **80** und **443** auf deinen Server weiterleiten.

### Fritz!Box

1. **Internet** → **Freigaben** → **Neue Portfreigabe**
2. **Portfreigabe für Anwendungen:**
   - HTTP (Port 80)
   - HTTPS (Port 443)
3. An IP-Adresse des Servers

## Nginx Proxy Manager vs. Traefik

| Feature | Nginx Proxy Manager | Traefik |
|---------|---------------------|---------|
| **Weboberfläche** | ✅ Einfach | ⚠️ Komplexer |
| **Einrichtung** | ✅ Sehr einfach | ⚠️ YAML-Konfiguration |
| **Docker-Integration** | ⚠️ Manuell | ✅ Automatisch |
| **Automatische Erkennung** | ❌ Nein | ✅ Ja |
| **Let's Encrypt** | ✅ Einfach | ✅ Automatisch |
| **Middleware** | ⚠️ Eingeschränkt | ✅ Sehr flexibel |

!!!tip "Empfehlung"
    - **Nginx Proxy Manager**: Ideal für Einsteiger, wenige Dienste
    - **Traefik**: Ideal für viele Docker-Container, Automatisierung

## Hinweise

- Die Daten liegen in `./volumes/nginx-proxy-manager/`
- Admin-Oberfläche auf Port 81
- Port 80 (HTTP) und 443 (HTTPS) für Proxy
- Die Ports 80/443 müssen am Router weitergeleitet werden

## Weitere Informationen

- [Offizielle Dokumentation](https://nginxproxymanager.com/guide/)
- [GitHub Repository](https://github.com/NginxProxyManager/nginx-proxy-manager)
- [Let's Encrypt](https://letsencrypt.org/)
