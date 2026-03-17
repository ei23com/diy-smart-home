# n8n

!!!tip "Persönliche Empfehlung: Node-RED"
    Ich persönlich nutze [Node-RED](nodered.md) statt n8n für Automatisierungen. Node-RED ist mein Lieblingsprogramm - es ist mächtiger, besser mit Home Assistant integrierbar und hat eine riesige Community. n8n ist aber auch eine gute Wahl, besonders wenn du eine grafischere Oberfläche bevorzugst.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

!!!warning "Umgebungsdatei erforderlich"
    Lege eine Datei `ei23-docker/env/n8n.env` mit den Datenbank-Zugangsdaten an.

### Umgebungsdatei erstellen

Erstelle die Datei `/home/[user]/ei23-docker/env/n8n.env` mit folgendem Inhalt (Passe Passwörter an!):

```env
POSTGRES_USER=n8n
POSTGRES_PASSWORD=DEIN_PASSWORT
POSTGRES_DB=n8n
POSTGRES_NON_ROOT_USER=n8n_user
POSTGRES_NON_ROOT_PASSWORD=DEIN_PASSWORT
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

## Hinweise

- Nach dem Start erreichst du n8n unter `http://[IP]:5678`
- Beim ersten Start musst du einen Account erstellen
- n8n verwendet eine PostgreSQL-Datenbank für die Speicherung der Workflows
- Integriert mit Home Assistant, MQTT und vielen anderen Diensten
- Workflows können per Cron, Webhook oder manuell getriggert werden

## Weitere Informationen

- [Offizielle Dokumentation](https://docs.n8n.io/)
- [GitHub Repository](https://github.com/n8n-io/n8n)
- [Integrationsübersicht](https://n8n.io/integrations/)
