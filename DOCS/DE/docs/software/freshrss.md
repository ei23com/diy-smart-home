# FreshRSS

[FreshRSS](https://freshrss.org/) ist ein selbst gehosteter RSS-Feed-Leser. Er ermöglicht es dir, News und Blogbeiträge von vielen Webseiten an einem Ort zu sammeln und zu lesen.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

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
      TZ: Europe/Berlin # AN DEINE ZEITZONE ANPASSEN
      CRON_MIN: 5
```

## Hinweise

- Nach dem Start erreichst du FreshRSS unter `http://[IP]:2224`
- Beim ersten Start wird der Installationsassistent gestartet
- `CRON_MIN: 5` bedeutet, dass Feeds alle 5 Minuten aktualisiert werden
- Unterstützt OPML-Import/-Export zum Umziehen von anderen Readern
- Kompatibel mit Feedly, Inoreader und anderen Apps via API
- Ideal als Grundlage für Automatisierungen in n8n oder Node-RED

## Weitere Informationen

- [Offizielle Dokumentation](https://freshrss.github.io/FreshRSS/en/)
- [GitHub Repository](https://github.com/FreshRSS/FreshRSS)
