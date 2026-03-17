# Frigate

[Frigate](https://frigate.video/) ist ein Open-Source NVR (Network Video Recorder) mit KI-basierter Objekterkennung in Echtzeit. Es funktioniert hervorragend mit Home Assistant und erkennt Personen, Fahrzeuge und andere Objekte.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Hardware beachten"
    Frigate profitiert stark von Hardware-Beschleunigung. Für Intel CPUs nutze das Device `/dev/dri/renderD128`.

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

## Hinweise

- Die Konfigurationsdatei liegt unter `./volumes/frigate/config/config.yml`
- Nach dem Start erreichst du Frigate unter `http://[IP]:5000`
- `FRIGATE_RTSP_PASSWORD` unbedingt ändern!
- Für GPU-Beschleunigung bei NVIDIA musst du das Device anpassen
- Integration mit Home Assistant über die Frigate-Integration oder MQTT
- Die `shm_size` muss je nach Anzahl und Auflösung der Kameras angepasst werden

## Weitere Informationen

- [Offizielle Dokumentation](https://docs.frigate.video/)
- [GitHub Repository](https://github.com/blakeblackshear/frigate)
- [Home Assistant Integration](https://github.com/blakeblackshear/frigate-hass-integration)
