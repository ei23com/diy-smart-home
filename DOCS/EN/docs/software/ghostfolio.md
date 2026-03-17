# Ghostfolio

[Ghostfolio](https://ghostfol.io/) is an open-source wealth management tool. It helps you track your investments, stocks, and cryptocurrencies and analyze the performance of your portfolio.

!!!tip "Personal Recommendation: Portfolio Performance"
    I personally use [Portfolio Performance](https://www.portfolio-performance.info/) instead of Ghostfolio. It's a desktop tool (Java) that offers even more detailed analysis and runs completely offline. Ghostfolio is a good choice if you prefer a web interface and multi-device access.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "Change Passwords"
    Change all passwords and secrets before starting the container!

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

## Notes

- After starting, you can access Ghostfolio at `http://[IP]:3333`
- **Important:** Change all `change_this_*` passwords before starting!
- The template includes Ghostfolio, PostgreSQL, and Redis
- Supports stocks, ETFs, cryptocurrencies, and commodities
- Data can be retrieved from Yahoo Finance and other sources
- Ideal for long-term wealth and portfolio analysis

## Further Information

- [Official Website](https://ghostfol.io/)
- [GitHub Repository](https://github.com/ghostfolio/ghostfolio)
- [Documentation](https://ghostfol.io/en/resources)
