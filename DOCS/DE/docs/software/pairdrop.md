# PairDrop

[PairDrop](https://pairdrop.net/) ist ein Open-Source-Alternative zu AirDrop für alle Plattformen. Teile Dateien einfach und schnell im lokalen Netzwerk - ohne Installation, ohne Account, einfach über den Browser.

!!!tip "Perfekt für den Alltag"
    PairDrop ist ideal um schnell Dateien zwischen PC, Smartphone und Tablet im Heimnetz zu teilen.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  pairdrop:
    container_name: pairdrop
    image: lscr.io/linuxserver/pairdrop:latest
    hostname: pairdrop
    restart: unless-stopped
    ports:
      - 3010:3000
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Berlin
      - RATE_LIMIT=false
      - WS_FALLBACK=false
      - DEBUG_MODE=false
```

## Verwendung

1. Öffne `http://[IP]:3010` im Browser
2. Andere Geräte im Netzwerk öffnen dieselbe Adresse
3. Klicke auf ein Gerät und wähle Dateien aus
4. Der Empfänger muss den Transfer bestätigen

### Auf dem Smartphone

1. Öffne `http://[IP]:3010` im Browser
2. Füge die Seite zum Homescreen hinzu (PWA)
3. Funktioniert wie eine native App

## Features

- **Keine Installation** - Läuft komplett im Browser
- **Kein Account** - Einfach Dateien teilen
- **P2P** - Dateien gehen direkt zwischen Geräten
- **Lokal** - Keine Daten verlassen dein Netzwerk
- **Verschlüsselt** - WebRTC mit Ende-zu-Ende-Verschlüsselung
- **Cross-Platform** - Funktioniert auf allen Geräten mit Browser

## Hinweise

- Port 3010 ist standardmäßig konfiguriert
- PairDrop nutzt WebRTC für direkte P2P-Übertragung
- Im gleichen WLAN werden Geräte automatisch erkannt
- Über QR-Code können auch externe Geräte temporär verbunden werden

## Weitere Informationen

- [Offizielle Website](https://pairdrop.net/)
- [GitHub Repository](https://github.com/schlagmichdoch/PairDrop)
