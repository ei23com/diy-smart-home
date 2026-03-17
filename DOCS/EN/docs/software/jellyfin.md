# Jellyfin

[Jellyfin](https://jellyfin.org/) is a free open-source media server that allows you to organize, manage, and stream your movies, music, TV shows, and photos to all your devices.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    user: 0:0 # UserID:GroupID
    network_mode: 'host'
    volumes:
      - ./volumes/jellyfin/config:/config
      - ./volumes/jellyfin/cache:/cache
      - ./volumes/jellyfin/media:/media
      # - ./volumes/immich/fotos/library:/photos:ro
    restart: 'unless-stopped'
    # Optional - alternative address used for autodiscovery
    # environment:
    #   - JELLYFIN_PublishedServerUrl=http://example.com
```

## Notes

- The template uses `network_mode: 'host'` for better compatibility with DLNA and automatic device discovery
- Place your media in the folder `./volumes/jellyfin/media/` or adjust the volume mappings
- Configuration files are stored in `./volumes/jellyfin/config/`

## Further Information

- [Official Documentation](https://jellyfin.org/docs/)
- [GitHub Repository](https://github.com/jellyfin/jellyfin)
