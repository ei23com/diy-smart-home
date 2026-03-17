# AdGuard Home

[AdGuard Home](https://adguard.com/de/adguard-home/overview.html) ist ein Netzwerk-weiter Werbeblocker und DNS-Server. Er blockiert Werbung, Tracker und Malware für alle Geräte in deinem Netzwerk - ohne Software auf den einzelnen Geräten.

!!!tip "Alternative zu Pi-hole"
    AdGuard Home ist eine moderne Alternative zu [Pi-hole](../start/docker-compose) mit einer schöneren Weboberfläche und einfacherer Konfiguration.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Port 53 beachten"
    Port 53 (DNS) darf nicht bereits belegt sein (z.B. durch systemd-resolved oder Pi-hole).

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
      - 3001:3000/tcp # Admin-Oberfläche
      - 2229:80/tcp   # Alternative Admin-Port
    volumes:
      - ./volumes/adguardhome/workdir:/opt/adguardhome/work
      - ./volumes/adguardhome/confdir:/opt/adguardhome/conf
    restart: unless-stopped
```

## Erster Start

1. Nach dem Start erreichst du das Setup unter `http://[IP]:3001`
2. Folge dem Installationsassistenten
3. Konfiguriere:
    - **Admin-Oberfläche**: Port 3001
    - **DNS-Server**: Port 53
4. Erstelle dein Admin-Passwort

## DNS auf Geräten einrichten

### Router (empfohlen)

Ändere den DNS-Server im Router auf die IP deines Servers:

1. Router-Oberfläche öffnen (z.B. Fritz!Box)
2. **Internet** → **Zugangsdaten** → **DNS-Server**
3. DNS auf Server-IP setzen (z.B. `192.168.178.20`)

→ Alle Geräte im Netzwerk nutzen automatisch AdGuard

### Einzelne Geräte

Alternativ DNS pro Gerät konfigurieren:

| Gerät | Vorgehen |
|-------|----------|
| **Windows** | Netzwerkadapter → IPv4 → DNS-Server |
| **macOS** | Systemeinstellungen → Netzwerk → DNS |
| **Android** | WLAN → Erweitert → DNS |
| **iOS** | WLAN → i → DNS konfigurieren |

## Blocklisten hinzufügen

### Empfohlene Listen

1. Gehe zu **Filters** → **DNS blocklists**
2. Klicke **Add blocklist** → **Choose from the list**

| Liste | Beschreibung |
|-------|--------------|
| **AdGuard DNS filter** | Standard-Werbeblocker |
| **Steven Black's List** | Werbung + Malware |
| **OISD** | Sehr gute Allround-Liste |
| **Annoyances** | Cookie-Banner, etc. |

### Whitelist

Manche Dienste müssen erlaubt werden:

1. **Filters** → **DNS allowlists**
2. Domain hinzufügen (z.B. `analytics.google.com` falls benötigt)

## Hinweise

- Admin-Oberfläche auf Port 3001
- DNS-Server auf Port 53
- DNS-over-TLS auf Port 853
- DNS-over-HTTPS auf Port 784
- Konfiguration in `./volumes/adguardhome/`

## Weitere Informationen

- [Offizielle Website](https://adguard.com/de/adguard-home/overview.html)
- [GitHub Repository](https://github.com/AdguardTeam/AdGuardHome)
- [Dokumentation](https://github.com/AdguardTeam/AdGuardHome/wiki)
