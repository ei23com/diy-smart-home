# Frigate

[Frigate](https://frigate.video/) is an open-source NVR (Network Video Recorder) with AI-based real-time object detection. It works excellently with Home Assistant and detects people, vehicles, and other objects.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "Note Hardware Requirements"
    Frigate benefits greatly from hardware acceleration. For Intel CPUs, use the device `/dev/dri/renderD128`.

## Template

```yaml
  frigate:
    container_name: frigate
    # privileged: true # this may not be necessary for all setups
    restart: unless-stopped
    image: ghcr.io/blakeblackshear/frigate:stable
    shm_size: "256mb" # update for your cameras based on calculation
    devices:
    #   - /dev/bus/usb:/dev/bus/usb
      - /dev/dri/renderD128 # for intel hwaccel, needs to be updated for your hardware
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./volumes/frigate/config:/config
      - ./volumes/frigate/storage:/media/frigate
      - ./volumes/frigate/db:/db      
      - type: tmpfs # Optional: 1GB of memory, reduces SSD/SD Card wear
        target: /tmp/cache
        tmpfs:
          size: 1000000000
    ports:
      - "5000:5000"
      - "8554:8554" # RTSP feeds
      - "8555:8555/tcp" # WebRTC over tcp
      - "8555:8555/udp" # WebRTC over udp
      - "1984:1984" # go2rtc for home assistant
    environment:
      FRIGATE_RTSP_PASSWORD: changeme!
```

## Notes

- The configuration file is located at `./volumes/frigate/config/config.yml`
- After starting, you can access Frigate at `http://[IP]:5000`
- **Important:** Change `FRIGATE_RTSP_PASSWORD`!
- For NVIDIA GPU acceleration, you need to adjust the device
- Integration with Home Assistant via the Frigate integration or MQTT
- The `shm_size` must be adjusted based on the number and resolution of cameras

## Further Information

- [Official Documentation](https://docs.frigate.video/)
- [GitHub Repository](https://github.com/blakeblackshear/frigate)
- [Home Assistant Integration](https://github.com/blakeblackshear/frigate-hass-integration)
