# Lyrion Music Server (LMS)

[Lyrion Music Server](https://lyrion.org/) (formerly Logitech Media Server) is an open-source multi-room audio system. Combined with Squeezelite players, you can play music synchronously in multiple rooms.

[![YT](https://ei23.de/bilder/YTthumbs/DwotxrCvHTA.webp)](https://www.youtube.com/watch?v=DwotxrCvHTA)

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

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
      - 9000:9000/tcp   # Web Interface
      - 9090:9090/tcp   # CLI Interface
      - 3483:3483/tcp   # SlimProto
      - 3483:3483/udp   # SlimProto
    restart: always
```

!!!note "Adjust Music Path"
    Adjust the volume mounts for your music and playlists to match your directories.

## Features

- **Multi-Room Audio** - Synchronized playback in multiple rooms
- **Internet Radio** - Thousands of radio stations
- **Spotify Integration** - Use Spotify Premium
- **Tidal/Qobuz** - HiFi Streaming
- **Podcasts** - Automatic downloads
- **Playlists** - Local and online playlists
- **Home Assistant** - Full integration

## First Start

1. After startup, you can access LMS at `http://[IP]:9000`
2. Select your music library
3. Wait for the music scan to complete
4. Set up your players

## Squeezelite Player

Squeezelite is a software player for LMS:

### Install on the Server

```bash
sudo apt-get install squeezelite -y
```

### As Docker Container

```yaml
  squeezelite:
    image: giof71/squeezelite
    container_name: squeezelite
    restart: unless-stopped
    network_mode: host
    environment:
      - SERVER_NAME=192.168.178.20
      - SOUND_DEVICE=default
      - PLAYER_NAME=Kitchen
```

### Hardware Players

- **Raspberry Pi + HiFiBerry** - Excellent quality
- **Squeezebox** - Original hardware (used)
- **Raspberry Pi + IQaudio** - Good and affordable

## Home Assistant Integration

LMS can be perfectly integrated into Home Assistant:

```yaml
# configuration.yaml
media_player:
  - platform: squeezebox
    host: 192.168.178.20
    port: 9000
```

### Automations

```yaml
automation:
  - alias: "Music on Wake Up"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      service: media_player.play_media
      target:
        entity_id: media_player.kitchen
      data:
        media_content_id: "http://radio-url"
        media_content_type: music
```

## Set Up Spotify

1. Install the **Spotify Protocol Handler** plugin in LMS
2. Configure your Spotify credentials
3. Spotify content will appear in the LMS interface

## Plugins

LMS supports plugins for extended functionality:

| Plugin | Description |
|--------|-------------|
| **Spotty** | Spotify integration |
| **Material Skin** | Modern web interface |
| **Radio Paradise** | HiFi Radio |
| **CD-Sync** | CD Ripping |
| **Don't Stop The Music** | Random playlists |

### Install Plugins

1. Go to **Settings** → **Plugins**
2. Search for the desired plugin
3. Click **Install**
4. Restart LMS

## Multi-Room Setup

### Synchronized Zones

1. Set up multiple Squeezelite players
2. In the web interface: select **Synchronize Players**
3. All synchronized players play identically

### Example Setup

| Room | Hardware | Cost |
|------|----------|------|
| **Living Room** | RPi 4 + HiFiBerry DAC | ~€80 |
| **Kitchen** | Squeezelite Docker | €0 |
| **Bedroom** | RPi Zero W + IQaudio | ~€40 |
| **Bathroom** | Bluetooth Speaker + Squeezelite | ~€30 |

## Notes

- Configuration is located in `./volumes/lyrionmusicserver/config/`
- Port 9000 is the web interface
- Port 9090 is for CLI/scripting
- Ports 3483 (TCP/UDP) for player communication
- LMS is very resource-efficient

## Further Information

- [Official Website](https://lyrion.org/)
- [LMS Documentation](https://lyrion.org/lms-server-documentation/)
- [Community Forum](https://forums.slimdevices.com/)
- [Material Skin Plugin](https://github.com/CDrumkin/lms-material)
