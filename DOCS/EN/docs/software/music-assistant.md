# Music Assistant

[Music Assistant](https://music-assistant.io/) is an open-source music server that unifies various music sources (local, Spotify, Tidal, etc.) and streams to any player in the house. Perfect for multi-room audio with Home Assistant.

!!!tip "Complement for Home Assistant"
    Music Assistant integrates seamlessly with Home Assistant and offers a modern interface for multi-room audio.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!note "Host Network"
    Music Assistant requires `network_mode: host` for automatic player discovery on the network.

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

## First Start

1. After starting, access Music Assistant at `http://[IP]:8095`
2. Follow the setup wizard
3. Add music sources
4. Select your players/targets

## Music Sources

Music Assistant supports many sources:

| Source | Type | Description |
|--------|------|-------------|
| **Local Files** | Filesystem | Mount music folder |
| **Spotify** | Streaming | Spotify Premium required |
| **Tidal** | Streaming | HiFi quality |
| **Qobuz** | Streaming | HiRes audio |
| **Deezer** | Streaming | |
| **TuneIn** | Radio | Internet radio |
| **YouTube Music** | Streaming | |

### Mount Local Music Folder

```yaml
volumes:
  - ./volumes/music-assistant-server/data:/data/
  - /home/user/media/Music:/music:ro
```

## Players/Targets

Music Assistant automatically discovers:

| Player | Description |
|--------|-------------|
| **AirPlay** | Apple devices |
| **Google Cast** | Chromecast, Google Home |
| **UPnP/DLNA** | DLNA-capable speakers |
| **Snapcast** | Multi-room with Snapcast |
| **Squeezebox** | Compatible with LMS |
| **Home Assistant** | HA Media Player |

## Home Assistant Integration

1. Install the **Music Assistant** integration in HA
2. Or use the HACS addon
3. All players and sources appear in HA

### Example Automation

```yaml
automation:
  - alias: "Music on wake up"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      - service: media_player.play_media
        target:
          entity_id: media_player.music_assistant_living_room
        data:
          media_content_id: "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M"
          media_content_type: music
```

## Multi-Room

### Group Players

1. In web interface: Select players
2. Click **Sync**
3. All synchronized players play identically

### Independent Control

Each room can be controlled independently:
- Own queue
- Own volume
- Own source

## Notes

- Web interface on port 8095
- Data in `./volumes/music-assistant-server/data/`
- Automatically discovers players on the network
- Host network required for player discovery
- Requires some system capabilities (SYS_ADMIN, DAC_READ_SEARCH)

!!!tip "Prepare Music Folder"
    Make sure your music folder is well organized: `Artist/Album/Track.mp3`

## Further Information

- [Official Website](https://music-assistant.io/)
- [GitHub Repository](https://github.com/music-assistant)
- [Documentation](https://music-assistant.io/docs/)
- [Home Assistant Addon](https://github.com/music-assistant/hass-music-assistant)
