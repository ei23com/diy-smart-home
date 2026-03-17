# Lyrion Music Server (LMS)

[Lyrion Music Server](https://lyrion.org/) (ehemals Logitech Media Server) ist ein Open-Source-Multi-Room-Audiosystem. Kombiniert mit Squeezelite-Playern kannst du Musik in mehreren Räumen synchronisiert abspielen.

[![YT](https://ei23.de/bilder/YTthumbs/DwotxrCvHTA.webp)](https://www.youtube.com/watch?v=DwotxrCvHTA)

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  lyrionmusicserver:
    container_name: lyrionmusicserver
    hostname: ei23
    image: lmscommunity/lyrionmusicserver:stable
    volumes:
      - ./volumes/lyrionmusicserver/config:/config:rw
      - /home/pi/media/Playlist:/playlist:rw
      - /home/pi/media/Musik:/music:ro
      - /etc/localtime:/etc/localtime:ro
      - /etc/timezone:/etc/timezone:ro
    ports:
      - 9000:9000/tcp   # Web-Interface
      - 9090:9090/tcp   # CLI Interface
      - 3483:3483/tcp   # SlimProto
      - 3483:3483/udp   # SlimProto
    restart: always
```

!!!note "Musik-Pfad anpassen"
    Passe die Volume-Mounts für deine Musik und Playlists an deine Verzeichnisse an.

## Features

- **Multi-Room Audio** - Synchronisierte Wiedergabe in mehreren Räumen
- **Internetradio** - Tausende Radiosender
- **Spotify-Integration** - Spotify Premium nutzen
- **Tidal/Qobuz** - HiFi-Streaming
- **Podcasts** - Automatische Downloads
- **Playlists** - Lokale und Online-Playlists
- **Home Assistant** - Vollständige Integration

## Erster Start

1. Nach dem Start erreichst du LMS unter `http://[IP]:9000`
2. Wähle deine Musik-Bibliothek
3. Warte, bis der Musik-Scan abgeschlossen ist
4. Richte deine Player ein

## Squeezelite Player

Squeezelite ist ein Software-Player für LMS:

### Auf dem Server installieren

```bash
sudo apt-get install squeezelite -y
```

### Als Docker Container

```yaml
  squeezelite:
    image: giof71/squeezelite
    container_name: squeezelite
    restart: unless-stopped
    network_mode: host
    environment:
      - SERVER_NAME=192.168.178.20
      - SOUND_DEVICE=default
      - PLAYER_NAME=Küche
```

### Hardware-Player

- **Raspberry Pi + HiFiBerry** - Hervorragende Qualität
- **Squeezebox** - Originale Hardware (gebraucht)
- **Raspberry Pi + IQaudio** - Gut und günstig

## Home Assistant Integration

LMS lässt sich perfekt in Home Assistant integrieren:

```yaml
# configuration.yaml
media_player:
  - platform: squeezebox
    host: 192.168.178.20
    port: 9000
```

### Automatisierungen

```yaml
automation:
  - alias: "Musik beim Aufstehen"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      service: media_player.play_media
      target:
        entity_id: media_player.kuche
      data:
        media_content_id: "http://radio-url"
        media_content_type: music
```

## Spotify einrichten

1. Installiere das **Spotify Protocol Handler** Plugin in LMS
2. Konfiguriere deine Spotify-Anmeldedaten
3. Spotify-Inhalte erscheinen in der LMS-Oberfläche

## Plugins

LMS unterstützt Plugins für erweiterte Funktionen:

| Plugin | Beschreibung |
|--------|--------------|
| **Spotty** | Spotify-Integration |
| **Material Skin** | Moderne Weboberfläche |
| **Radio Paradise** | HiFi-Radio |
| **CD-Sync** | CD-Ripping |
| **Don't Stop The Music** | Zufalls-Playlisten |

### Plugins installieren

1. Gehe zu **Einstellungen** → **Plugins**
2. Suche das gewünschte Plugin
3. Klicke auf **Installieren**
4. Starte LMS neu

## Multi-Room Setup

### Synchronisierte Zonen

1. Richte mehrere Squeezelite-Player ein
2. In der Weboberfläche: **Player synchronisieren** wählen
3. Alle synchronisierten Player spielen identisch

### Beispiel-Setup

| Raum | Hardware | Kosten |
|------|----------|--------|
| **Wohnzimmer** | RPi 4 + HiFiBerry DAC | ~80€ |
| **Küche** | Squeezelite Docker | 0€ |
| **Schlafzimmer** | RPi Zero W + IQaudio | ~40€ |
| **Bad** | Bluetooth-Box + Squeezelite | ~30€ |

## Hinweise

- Die Konfiguration liegt in `./volumes/lyrionmusicserver/config/`
- Der Port 9000 ist das Web-Interface
- Port 9090 ist für CLI/Scripting
- Ports 3483 (TCP/UDP) für Player-Kommunikation
- LMS ist sehr ressourcenschonend

## Weitere Informationen

- [Offizielle Website](https://lyrion.org/)
- [LMS Dokumentation](https://lyrion.org/lms-server-documentation/)
- [Community-Forum](https://forums.slimdevices.com/)
- [Material Skin Plugin](https://github.com/CDrumkin/lms-material)
