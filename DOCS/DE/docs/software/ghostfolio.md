# Ghostfolio

[Ghostfolio](https://ghostfol.io/) ist ein Open-Source Vermögensverwaltungs-Tool. Es hilft dir, deine Anlagen, Aktien und Kryptowährungen zu tracken und die Performance deines Portfolios zu analysieren.

!!!tip "Persönliche Empfehlung: Portfolio Performance"
    Ich persönlich nutze [Portfolio Performance](https://www.portfolio-performance.info/) statt Ghostfolio. Es ist ein Desktop-Tool (Java), das noch detailliertere Analysen bietet und komplett offline läuft. Ghostfolio ist aber eine gute Wahl, wenn du eine Web-Oberfläche und Multi-Device-Zugriff bevorzugst.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Passwörter anpassen"
    Ändere alle Passwörter und Secrets bevor du den Container startest!

## Template

```yaml
  ghostfolio:
    image: ghostfolio/ghostfolio:latest
    container_name: ghostfolio
    restart: unless-stopped
    ports:
      - "3333:3333"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Berlin
      - REDIS_HOST=ghostfolio-redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=change_this_redis_password
      - ACCESS_TOKEN_SALT=change_this_salt_string
      - JWT_SECRET_KEY=change_this_jwt_secret_key
      - DATABASE_URL=postgresql://gf_user:change_this_db_password@ghostfolio-db:5432/gf_db?connect_timeout=300&sslmode=prefer
    volumes:
      - ./volumes/ghostfolio/app:/app/data
    depends_on:
      ghostfolio-db:
        condition: service_healthy
      ghostfolio-redis:
        condition: service_started

  ghostfolio-db:
    image: postgres:15-alpine
    container_name: ghostfolio-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=gf_db
      - POSTGRES_USER=gf_user
      - POSTGRES_PASSWORD=change_this_db_password
    volumes:
      - ./volumes/ghostfolio/postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gf_user -d gf_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  ghostfolio-redis:
    image: redis:alpine
    container_name: ghostfolio-redis
    restart: unless-stopped
    environment:
      - REDIS_PASSWORD=change_this_redis_password
    command: redis-server --requirepass change_this_redis_password
    volumes:
      - ./volumes/ghostfolio/redis:/data
```

## Hinweise

- Nach dem Start erreichst du Ghostfolio unter `http://[IP]:3333`
- **Wichtig:** Ändere alle `change_this_*` Passwörter vor dem Start!
- Das Template umfasst Ghostfolio, PostgreSQL und Redis
- Unterstützt Aktien, ETFs, Kryptowährungen und Rohstoffe
- Daten können von Yahoo Finance und anderen Quellen bezogen werden
- Ideal für langfristige Vermögens- und Depotauswertung

## Weitere Informationen

- [Offizielle Website](https://ghostfol.io/)
- [GitHub Repository](https://github.com/ghostfolio/ghostfolio)
- [Dokumentation](https://ghostfol.io/en/resources)
