# NocoDB

[NocoDB](https://nocodb.com/) is an open-source alternative to Airtable. It transforms any database into a smart spreadsheet interface and allows you to use databases without SQL knowledge.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "Environment Variable for Password"
    Set the variable `${PW}` in your `.env` file (in the ei23-docker folder).

## Template

```yaml
  nocodb: 
    container_name: nocodb
    depends_on: 
      noco_rootdb: 
        condition: service_healthy
    environment: 
      NC_DB: pg://noco_rootdb:5432?u=postgres&p=${PW}&d=noco_rootdb
    image: "nocodb/nocodb:latest"
    ports: 
      - "2289:8080"
    restart: always
    volumes: 
      - "./volumes/nocodb/nc_data:/usr/app/data"
      
  noco_rootdb: 
    container_name: noco_rootdb
    environment: 
      POSTGRES_DB: noco_rootdb
      POSTGRES_PASSWORD: ${PW}
      POSTGRES_USER: postgres
    healthcheck: 
      interval: 10s
      retries: 10
      test: "pg_isready -U \"$$POSTGRES_USER\" -d \"$$POSTGRES_DB\""
      timeout: 2s
    image: postgres:latest
    restart: always
    volumes: 
      - "./volumes/nocodb/db_data:/var/lib/postgresql/data"
```

### Create .env File

Create or add to the file `/home/[user]/ei23-docker/.env`:

```env
PW=YOUR_SECURE_PASSWORD
```

!!!warning "Change Password"
    Replace `YOUR_SECURE_PASSWORD` with a secure, random password!

## Features

- **Spreadsheet Interface** - Edit databases like Excel/Google Sheets
- **Automatic REST API** - Each table gets its own API
- **Multiple Views** - Grid, Gallery, Kanban, Calendar, Form
- **Collaboration** - Multiple users with different permissions
- **Import/Export** - CSV, Excel, JSON
- **Webhooks** - Automations on data changes
- **Rollups & Lookups** - Links between tables

## First Start

1. After startup, you can access NocoDB at `http://[IP]:2289`
2. Create an admin account on first start
3. Start a new project or import existing data

## Use Cases

| Application | Description |
|-------------|-------------|
| **Project Management** | Manage tasks, tickets, sprints |
| **CRM** | Manage customers and contacts |
| **Inventory** | Track stock lists and assets |
| **Recipes** | Meal planning and ingredients |
| **Home Assistant** | Store sensor data in a structured way |

## Use the API

NocoDB automatically provides a REST API for each table:

```
http://[IP]:2289/api/v1/db/data/v1/[project]/[table]
```

The API can be used, for example, in [n8n](n8n.md), [NodeRED](nodered.md), or Home Assistant.

## Notes

- The database runs as a separate PostgreSQL container
- Data is stored in `./volumes/nocodb/`
- An auth token is required for the API (create in NocoDB settings)
- NocoDB is intended as an Airtable open-source alternative

## Further Information

- [Official Documentation](https://docs.nocodb.com/)
- [GitHub Repository](https://github.com/nocodb/nocodb)
- [API Documentation](https://docs.nocodb.com/developer-resources/rest-apis)
