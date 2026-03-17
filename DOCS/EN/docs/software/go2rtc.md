# go2rtc

[go2rtc](https://github.com/AlexxIT/go2rtc) is a universal RTSP, RTMP, HLS, and WebRTC streaming server. It is frequently used with Frigate and Home Assistant to provide cameras across various protocols.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

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

## Notes

- After starting, you can access the web interface at `http://[IP]:1984`
- `network_mode: host` is important for WebRTC and HomeKit support
- Configuration can be done via the web interface or the `go2rtc.yaml` file
- Ideal for Frigate installations as a stream proxy
- Supports RTSP, RTMP, HTTP-FLV, HLS, WebRTC, MP4, and HomeKit

## Further Information

- [GitHub Repository](https://github.com/AlexxIT/go2rtc)
- [Documentation](https://github.com/AlexxIT/go2rtc#readme)
