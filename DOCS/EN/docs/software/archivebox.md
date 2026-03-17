# ArchiveBox

[ArchiveBox](https://archivebox.io/) is a powerful tool for locally archiving web pages. It saves URLs as HTML, PDF, screenshots, and more - ideal for permanently backing up important content.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  archivebox:
    image: archivebox/archivebox
    container_name: archivebox
    command: server --quick-init 0.0.0.0:8000
    ports:
      - 8085:8000
    volumes:
      - ./volumes/archivebox/data/:/data
    environment:
      - ALLOWED_HOSTS=*
      - PUBLIC_INDEX=True
      - PUBLIC_SNAPSHOTS=True
      # - PUBLIC_ADD_VIEW=False
      - ADMIN_USERNAME=admin
      - ADMIN_PASSWORD=SomeSecretPassword
```

## Notes

- After starting, you can access ArchiveBox at `http://[IP]:8085`
- **Important:** Change `ADMIN_PASSWORD` and adjust `ALLOWED_HOSTS` to your domain/IP
- Set `PUBLIC_INDEX=False` and `PUBLIC_SNAPSHOTS=False` to keep your archives private
- A cronjob can be set up for automatic archiving (see template comments)

## Further Information

- [Official Documentation](https://github.com/ArchiveBox/ArchiveBox/wiki)
- [GitHub Repository](https://github.com/ArchiveBox/ArchiveBox)
