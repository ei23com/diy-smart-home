# Syncthing

[Syncthing](https://syncthing.net/) is a free, decentralized file synchronization service. It synchronizes files between multiple devices without a central cloud - your data stays on your devices.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  syncthing:
    image: syncthing/syncthing
    container_name: syncthing
    hostname: syncthing-server
    environment:
      - PUID=33
      - PGID=33
    volumes:
      - ./volumes/syncthing:/var/syncthing
    ports:
      - 8384:8384 # Web UI
      - 22000:22000/tcp # TCP file transfers
      - 22000:22000/udp # QUIC file transfers
      - 21027:21027/udp # Receive local discovery broadcasts
    restart: unless-stopped
```

## Notes

- After startup, you can access the web interface at `http://[IP]:8384`
- On first start, a password lock is displayed - set a password under "Settings"
- Connect your devices via the device ID
- Syncthing also works over the internet, NAT traversal is built-in
- Ideal for backups and data synchronization between server and desktop/laptop

## Further Information

- [Official Documentation](https://docs.syncthing.net/)
- [GitHub Repository](https://github.com/syncthing/syncthing)
