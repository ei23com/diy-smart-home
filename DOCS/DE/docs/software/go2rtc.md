# go2rtc

[go2rtc](https://github.com/AlexxIT/go2rtc) ist ein universeller RTSP-, RTMP-, HLS- und WebRTC-Streaming-Server. Er wird häufig mit Frigate und Home Assistant verwendet, um Kameras in verschiedenen Protokollen bereitzustellen.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  go2rtc:
    image: alexxit/go2rtc
    container_name: go2rtc
    network_mode: host       # important for WebRTC, HomeKit, UDP cameras
    privileged: true         # only for FFmpeg hardware transcoding
    restart: unless-stopped  # autorestart on fail or config change from WebUI
    environment:
      - TZ=Europe/Berlin  # timezone in logs
    volumes:
      - "./volumes/go2rtc:/config"   # folder for go2rtc.yaml file (edit from WebUI)
```

## Hinweise

- Nach dem Start erreichst du die Weboberfläche unter `http://[IP]:1984`
- `network_mode: host` ist wichtig für WebRTC und HomeKit-Unterstützung
- Konfiguration kann über die Weboberfläche oder die `go2rtc.yaml` erfolgen
- Ideal für Frigate-Installationen als Stream-Proxy
- Unterstützt RTSP, RTMP, HTTP-FLV, HLS, WebRTC, MP4 und HomeKit

## Weitere Informationen

- [GitHub Repository](https://github.com/AlexxIT/go2rtc)
- [Dokumentation](https://github.com/AlexxIT/go2rtc#readme)
