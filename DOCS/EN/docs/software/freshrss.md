# FreshRSS

[FreshRSS](https://freshrss.org/) is a self-hosted RSS feed reader. It allows you to collect and read news and blog posts from many websites in one place.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  freshrss:
    image: freshrss/freshrss:latest
    container_name: freshrss
    hostname: freshrss
    restart: unless-stopped
    volumes:
      - ./volumes/freshrss/data:/var/www/FreshRSS/data
      - ./volumes/freshrss/extensions:/var/www/FreshRSS/extensions
    ports:
      - "2224:80"
    environment:
      TZ: Europe/Berlin # ADJUST TO YOUR TIMEZONE
      CRON_MIN: 5
```

## Notes

- After starting, you can access FreshRSS at `http://[IP]:2224`
- On first start, the installation wizard will launch
- `CRON_MIN: 5` means feeds are updated every 5 minutes
- Supports OPML import/export for migrating from other readers
- Compatible with Feedly, Inoreader, and other apps via API
- Ideal as a basis for automations in n8n or Node-RED

## Further Information

- [Official Documentation](https://freshrss.github.io/FreshRSS/en/)
- [GitHub Repository](https://github.com/FreshRSS/FreshRSS)
