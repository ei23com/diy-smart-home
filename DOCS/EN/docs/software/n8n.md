# n8n

[n8n](https://n8n.io/) is a powerful workflow automation platform. It allows you to connect APIs and services with each other - similar to Zapier or IFTTT, but self-hosted.

!!!tip "Personal Recommendation: Node-RED"
    I personally use [Node-RED](nodered.md) instead of n8n for automations. Node-RED is my favorite program - it's more powerful, better integrated with Home Assistant, and has a huge community. n8n is also a good choice, especially if you prefer a more graphical interface.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

!!!warning "Environment File Required"
    Create a file `ei23-docker/env/n8n.env` with the database credentials.

### Create Environment File

Create the file `/home/[user]/ei23-docker/env/n8n.env` with the following content (adjust passwords!):

```env
POSTGRES_USER=n8n
POSTGRES_PASSWORD=YOUR_PASSWORD
POSTGRES_DB=n8n
POSTGRES_NON_ROOT_USER=n8n_user
POSTGRES_NON_ROOT_PASSWORD=YOUR_PASSWORD
```

### Docker-Compose Template

```yaml
  n8n-postgres:
    image: postgres:16
    container_name: n8n-postgres
    restart: always
    env_file:
      - ./env/n8n.env
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_NON_ROOT_USER=${POSTGRES_NON_ROOT_USER}
      - POSTGRES_NON_ROOT_PASSWORD=${POSTGRES_NON_ROOT_PASSWORD}
    volumes:
      - ./volumes/n8n/db_storage:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 5s
      timeout: 5s
      retries: 10

  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    restart: always
    env_file:
      - ./env/n8n.env
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=n8n-postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      # - N8N_HOST=example.com
      # - NODE_ENV=production
      # - WEBHOOK_URL=https://example.com
    ports:
      - 5678:5678
    links:
      - n8n-postgres
    user: 0:0
    volumes:
      - ./volumes/n8n/n8n:/home/node/.n8n
    depends_on:
      n8n-postgres:
        condition: service_healthy
```

## Notes

- After startup, you can access n8n at `http://[IP]:5678`
- On first start, you need to create an account
- n8n uses a PostgreSQL database for storing workflows
- Integrates with Home Assistant, MQTT, and many other services
- Workflows can be triggered via Cron, webhook, or manually

## Further Information

- [Official Documentation](https://docs.n8n.io/)
- [GitHub Repository](https://github.com/n8n-io/n8n)
- [Integrations Overview](https://n8n.io/integrations/)
