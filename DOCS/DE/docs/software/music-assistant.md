# Music Assistant

[Music Assistant](https://music-assistant.io/) ist ein Open-Source-Musik-Server, der verschiedene Musik-Quellen (lokal, Spotify, Tidal, etc.) vereint und auf beliebige Player im Haus streamt. Perfekt für Multi-Room-Audio mit Home Assistant.

!!!tip "Ergänzung für Home Assistant"
    Music Assistant integriert sich nahtlos in Home Assistant und bietet ein modernes Interface für Multi-Room-Audio.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!note "Host-Netzwerk"
    Music Assistant benötigt `network_mode: host` für die automatische Erkennung von Playern im Netzwerk.

## Template

```yaml
  music-assistant-server:
    image: ghcr.io/music-assistant/server:latest
    container_name: music-assistant-server
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./volumes/music-assistant-server/data:/data/
    cap_add:
      - SYS_ADMIN
      - DAC_READ_SEARCH
    security_opt:
      - apparmor:unconfined
    environment:
      - LOG_LEVEL=info
```

## Erster Start

1. Nach dem Start erreichst du Music Assistant unter `http://[IP]:8095`
2. Folge dem Setup-Assistenten
3. Füge Musik-Quellen hinzu
4. Wähle deine Player/Targets

## Musik-Quellen

Music Assistant unterstützt viele Quellen:

| Quelle | Typ | Beschreibung |
|--------|-----|--------------|
| **Lokale Dateien** | Filesystem | Musik-Ordner einbinden |
| **Spotify** | Streaming | Spotify Premium benötigt |
| **Tidal** | Streaming | HiFi-Qualität |
| **Qobuz** | Streaming | HiRes-Audio |
| **Deezer** | Streaming | |
| **TuneIn** | Radio | Internetradio |
| **YouTube Music** | Streaming | |

### Lokalen Musik-Ordner einbinden

```yaml
volumes:
  - ./volumes/music-assistant-server/data:/data/
  - /home/user/media/Musik:/music:ro
```

## Player/Targets

Music Assistant erkennt automatisch:

| Player | Beschreibung |
|--------|--------------|
| **AirPlay** | Apple-Devices |
| **Google Cast** | Chromecast, Google Home |
| **UPnP/DLNA** | DLNA-fähige Lautsprecher |
| **Snapcast** | Multi-Room mit Snapcast |
| **Squeezebox** | Kompatibel mit LMS |
| **Home Assistant** | HA Media Player |

## Home Assistant Integration

1. Installiere die **Music Assistant** Integration in HA
2. Oder nutze das HACS Addon
3. Alle Player und Quellen erscheinen in HA

### Beispiel-Automatisierung

```yaml
automation:
  - alias: "Musik beim Aufstehen"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      - service: media_player.play_media
        target:
          entity_id: media_player.music_assistant_wohnzimmer
        data:
          media_content_id: "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M"
          media_content_type: music
```

## Multi-Room

### Player gruppieren

1. In der Weboberfläche: Player auswählen
2. Auf **Sync** klicken
3. Alle synchronisierten Player spielen identisch

### Unabhängig steuern

Jeder Raum kann unabhängig gesteuert werden:
- Eigene Warteschlange
- Eigene Lautstärke
- Eigene Quelle

## Hinweise

- Web-Interface auf Port 8095
- Daten in `./volumes/music-assistant-server/data/`
- Erkennt Player automatisch im Netzwerk
- Host-Netzwerk erforderlich für Player-Erkennung
- Benötigt einige System-Capabilities (SYS_ADMIN, DAC_READ_SEARCH)

!!!tip "Musik-Ordner vorbereiten"
    Stelle sicher, dass dein Musik-Ordner gut organisiert ist: `Künstler/Album/Track.mp3`

## Weitere Informationen

- [Offizielle Website](https://music-assistant.io/)
- [GitHub Repository](https://github.com/music-assistant)
- [Dokumentation](https://music-assistant.io/docs/)
- [Home Assistant Addon](https://github.com/music-assistant/hass-music-assistant)
