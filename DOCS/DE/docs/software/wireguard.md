# WireGuard VPN

[WireGuard](https://www.wireguard.com/) ist ein modernes, schnelles und sicheres VPN-Protokoll. Mit dem [wg-easy](https://github.com/wg-easy/wg-easy) Docker-Image ist die Einrichtung besonders einfach.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Router-Konfiguration nötig"
    Nach der Installation musst du Port **51820 UDP** an deinem Router auf den Server weiterleiten.

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
      - LANG=de
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

## Konfiguration

### Umgebungsvariablen

| Variable | Beschreibung | Beispiel |
|----------|--------------|----------|
| `WG_HOST` | Deine Domain oder öffentliche IP | `meinedomain.de` oder `85.123.45.67` |
| `PASSWORD` | Passwort für die Weboberfläche | `SicheresPasswort123!` |
| `WG_PORT` | WireGuard Port (UDP) | `51820` |
| `PORT` | Weboberfläche Port (TCP) | `51821` |
| `WG_DEFAULT_ADDRESS` | IP-Bereich für Clients | `10.8.8.x` |
| `WG_ALLOWED_IPS` | Routen durch VPN | Siehe unten |

### WG_ALLOWED_IPS Optionen

```yaml
# Option 1: Vollständiges VPN (alle Daten durch den Tunnel)
WG_ALLOWED_IPS=0.0.0.0/1, 128.0.0.0/1, ::/1

# Option 2: Nur Heimnetz durch VPN (restliches Internet direkt)
WG_ALLOWED_IPS=10.8.8.0/24, 192.168.178.0/24
```

!!!tip "Empfohlen"
    Für Smart Home Nutzung: Nutze **Option 2** (nur Heimnetz) für bessere Geschwindigkeit im Alltag.

## Router konfiguriere

### Fritz!Box

1. Gehe zu **Internet** → **Freigaben**
2. Klicke auf **Neue Portfreigabe**
3. Einstellungen:
   - **Protokoll:** UDP
   - **Port:** 51820
   - **An IP:** IP deines Servers
   - **Bezeichnung:** WireGuard

### Andere Router

Leite folgende Ports weiter:
- **51820 UDP** → Dein Server (WireGuard)
- **51821 TCP** → Dein Server (Weboberfläche, optional)

## Erster Start

1. Nach dem Start erreichst du die Weboberfläche unter `http://[IP]:51821`
2. Melde dich mit dem konfigurierten `PASSWORD` an
3. Erstelle einen neuen Client:
   - Klicke auf **+ New Client**
   - Gib einen Namen ein (z.B. "Mein Handy")
4. Lade die Konfiguration herunter oder scanne den QR-Code

## Client einrichten

### Smartphone (Android/iOS)

1. Installiere die WireGuard App:
   - [Android](https://play.google.com/store/apps/details?id=com.wireguard.android)
   - [iOS](https://apps.apple.com/app/wireguard/id1441195209)
2. Klicke in der wg-easy Oberfläche auf das QR-Code-Icon
3. Scanne den QR-Code mit der App
4. Aktiviere das VPN

### Desktop (Windows/macOS/Linux)

1. Installiere den WireGuard Client:
   - [Windows](https://www.wireguard.com/install/)
   - [macOS](https://apps.apple.com/app/wireguard/id1451685025)
   - Linux: `sudo apt install wireguard`
2. Lade die Konfigurationsdatei (.conf) herunter
3. Importiere die Datei im Client
4. Aktiviere das VPN

## VPN-Typen erklärt

### Vollständiges VPN

```
Smartphone → Internet → Dein Server → Internet
                 ↑
        Alles durch VPN
```

**Vorteile:** Maximale Privatsphäre, Ad-Blocking (mit Pi-hole)
**Nachteile:** Langsamer, Server-Bandbreite begrenzt

### Split-Tunnel (nur Heimnetz)

```
Smartphone → Internet (direkt) → Ziel
         ↘
          → Dein Server → Heimnetz
```

**Vorteile:** Schneller im Alltag
**Nachteile:** Nur Heimnetz-Dienste geschützt

## Hinweise

- Die Daten werden in `./volumes/wireguard/` gespeichert
- Die Weboberfläche ist unter Port 51821 erreichbar
- **WG_HOST** muss deine öffentliche IP oder Domain sein
- Für dynamische IPs nutze [Dynamic DNS](../start/remote-access#dynamic-dns-ddns)
- WireGuard ist deutlich schneller als OpenVPN

## Sicherheit

- Das `PASSWORD` schützt nur die Weboberfläche
- Jeder Client hat seinen eigenen Schlüssel
- Deaktiviere nicht genutzte Clients in der Oberfläche
- Regelmäßige Updates des Docker-Images

## Troubleshooting

### VPN verbindet nicht

1. Prüfe Port-Freigabe am Router (UDP 51820)
2. Prüfe `WG_HOST` - muss öffentliche IP/Domain sein
3. Prüfe Firewall am Server
4. Teste mit `ping 10.8.8.1` ob der Tunnel funktioniert

### Langsame Verbindung

1. Nutze Split-Tunnel (`WG_ALLOWED_IPS` nur Heimnetz)
2. Prüfe Upload-Geschwindigkeit deines Internetanschlusses
3. Ändere `WG_MTU=1280` bei Problemen mit Fragmentierung

## Weitere Informationen

- [wg-easy GitHub](https://github.com/wg-easy/wg-easy)
- [WireGuard Dokumentation](https://www.wireguard.com/quickstart/)
- [WireGuard Konfiguration](https://www.wireguard.com/configuration/)
