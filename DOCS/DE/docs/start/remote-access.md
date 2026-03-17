# Fernzugriff

Um von unterwegs auf deinen Smart Home Server zuzugreifen, gibt es verschiedene Möglichkeiten. Hier erfährst du, welche Optionen es gibt und welche für dich am besten geeignet ist.

## Übersicht

| Methode | Sicherheit | Einfachheit | Empfehlung |
|---------|------------|-------------|------------|
| **WireGuard VPN** | ✅✅✅ Sehr sicher | ✅ Gut | ⭐ **Empfohlen** |
| **Reverse Proxy (HTTPS)** | ✅✅ Sicher | ✅ Gut | Für öffentliche Dienste |
| **SSH Tunnel** | ✅✅✅ Sehr sicher | ⚠️ Komplex | Für Experten |
| **Portfreigabe** | ❌ Unsicher | ✅ Einfach | **Nicht empfohlen!** |

!!!warning "Portfreigabe vermeiden"
    Öffne **niemals** unverschlüsselte Dienste (HTTP, MQTT, etc.) direkt ins Internet! Nutze immer VPN oder HTTPS mit Reverse Proxy.

---

## VPN (Empfohlen)

Ein VPN ist die sicherste Methode für den Fernzugriff. Es erstellt ein verschlüsseltes "virtuelles Kabel" in dein Heimnetz.

### WireGuard

[WireGuard](../software/wireguard.md) ist ein modernes, schnelles VPN-Protokoll. Mit dem Template `wg-easy` ist die Einrichtung sehr einfach.

**Vorteile:**
- ✅ Sehr sicher (modernste Verschlüsselung)
- ✅ Sehr schnell (niedrige Latenz)
- ✅ Einfache Einrichtung mit wg-easy
- ✅ Apps für alle Plattformen
- ✅ Zugriff auf ALLE Geräte im Heimnetz

**Nachteile:**
- ⚠️ Benötigt eine feste IP oder Dynamic DNS
- ⚠️ Portfreigabe am Router nötig (UDP)

### Einrichtung

1. Installiere [WireGuard](../software/wireguard.md) über das Template
2. Konfiguriere deine Router:
   - **Port 51820 UDP** → Dein Server
3. Richte die Clients in der wg-easy Weboberfläche ein
4. Lade die Config oder scanne den QR-Code mit der App

### Clients

| Plattform | App |
|-----------|-----|
| **Android** | [WireGuard App](https://play.google.com/store/apps/details?id=com.wireguard.android) |
| **iOS** | [WireGuard App](https://apps.apple.com/app/wireguard/id1441195209) |
| **Windows** | [WireGuard für Windows](https://www.wireguard.com/install/) |
| **macOS** | [WireGuard für macOS](https://apps.apple.com/app/wireguard/id1451685025) |
| **Linux** | `sudo apt install wireguard` |

---

## Reverse Proxy

Ein Reverse Proxy macht lokale Dienste über HTTPS erreichbar. Ideal für Dienste, die auch von anderen (z.B. Familie) genutzt werden sollen.

### Nginx Proxy Manager

Der [Nginx Proxy Manager](../software/nginxproxy.md) ist der einfachste Einstieg:

**Vorteile:**
- ✅ Einfache Weboberfläche
- ✅ Automatische SSL-Zertifikate (Let's Encrypt)
- ✅ Nutzerfreundlich

**Einrichtung:**
1. Installiere Nginx Proxy Manager
2. Richtige eine Domain/Subdomain ein (z.B. `home.meinedomain.de`)
3. Portfreigabe: Port 80 + 443 → Dein Server
4. SSL-Zertifikat automatisch erstellen lassen

### Traefik

[Traefik](../software/traefik.md) ist mächtiger, aber komplexer in der Einrichtung:

**Vorteile:**
- ✅ Automatische Docker-Container-Erkennung
- ✅ Sehr flexibel
- ✅ Gut dokumentiert

**Nachteile:**
- ⚠️ Steilere Lernkurve

---

## Dynamic DNS (DDNS)

Ohne feste IP-Adresse vom Provider benötigst du Dynamic DNS:

### Kostenlose DDNS-Anbieter

| Anbieter | Website | Notiz |
|----------|---------|-------|
| **DuckDNS** | duckdns.org | Einfach, kostenlos |
| **No-IP** | noip.com | Kostenlos (alle 30 Tage bestätigen) |
| **Dynv6** | dynv6.com | Kostenlos, unterstützt IPv6 |
| **Cloudflare** | cloudflare.com | Eigene Domain nötig |

### Fritz!Box DDNS

Die Fritz!Box hat einen integrierten DDNS-Service:
1. Gehe zu **Internet** → **Freigaben** → **Dynamic DNS**
2. Wähle deinen Anbieter
3. Trage deine Zugangsdaten ein

---

## SSH (für Experten)

SSH-Tunnel bieten sicheren Zugriff, sind aber komplexer:

### SSH-Tunnel erstellen

```bash
# Lokalen Port auf Remote weiterleiten
ssh -L 8123:localhost:8123 user@dein-server.de

# Jetzt ist Home Assistant unter http://localhost:8123 erreichbar
```

### SSH mit Public Key

Sichere SSH-Verbindungen mit Schlüsseldateien:
[SSH-Verbindungen mit Public Key absichern](https://ei23.de/smarthome/ssh-verbindungen-mit-public-key-verfahren-absichern/)

---

## Sicherheitscheckliste

- [ ] **VPN** oder **Reverse Proxy mit HTTPS** nutzen
- [ ] **Starke Passwörter** überall
- [ ] **2FA aktivieren** wo möglich (Home Assistant, Vaultwarden)
- [ ] **Updates** regelmäßig einspielen
- [ ] **Firewall** am Router konfigurieren
- [ ] **Nur notwendige Ports** freigeben
- [ ] **Logs** regelmäßig prüfen (Uptime Kuma)

## Meine Empfehlung

| Situation | Empfehlung |
|-----------|------------|
| **Nur du** greifst zu | WireGuard VPN |
| **Familie** nutzt Dienste | WireGuard VPN + einzelne Reverse Proxy Einträge |
| **Öffentliche Website** | Reverse Proxy (Traefik/Nginx) mit HTTPS |
| **Beste Sicherheit** | WireGuard VPN + SSH als Backup |

!!!tip "Kombination"
    Die beste Lösung ist oft eine Kombination: **WireGuard VPN** für dich und **Reverse Proxy** für Dienste, die auch ohne VPN erreichbar sein müssen (z.B. Nextcloud für Familie).

## Weitere Informationen

- [WireGuard Dokumentation](../software/wireguard.md)
- [Nginx Proxy Manager](../software/nginxproxy.md)
- [Traefik](../software/traefik.md)
