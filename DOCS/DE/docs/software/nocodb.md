# NocoDB

[NocoDB](https://nocodb.com/) ist eine Open-Source-Alternative zu Airtable. Es verwandelt jede Datenbank in eine smarte Tabellen-Oberfläche und ermöglicht es dir, Datenbanken ohne SQL-Kenntnisse zu nutzen.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Umgebungsvariable für Passwort"
    Setze die Variable `${PW}` in deiner `.env` Datei (im ei23-docker Ordner).

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

### .env Datei erstellen

Erstelle oder ergänze die Datei `/home/[user]/ei23-docker/.env`:

```env
PW=DEIN_SICHERES_PASSWORT
```

!!!warning "Passwort ändern"
    Ersetze `DEIN_SICHERES_PASSWORT` mit einem sicheren, zufälligen Passwort!

## Features

- **Tabellen-Oberfläche** - Datenbanken wie Excel/Google Sheets bearbeiten
- **Automatische REST-API** - Jede Tabelle bekommt eine eigene API
- **Mehrere Ansichten** - Grid, Gallery, Kanban, Calendar, Form
- **Zusammenarbeit** - Mehrere Benutzer mit verschiedenen Berechtigungen
- **Import/Export** - CSV, Excel, JSON
- **Webhooks** - Automatisierungen bei Datenänderungen
- **Rollups & Lookups** - Verknüpfungen zwischen Tabellen

## Erster Start

1. Nach dem Start erreichst du NocoDB unter `http://[IP]:2289`
2. Erstelle beim ersten Start einen Admin-Account
3. Starte ein neues Projekt oder importiere bestehende Daten

## Use Cases

| Anwendung | Beschreibung |
|-----------|--------------|
| **Projektmanagement** | Aufgaben, Tickets, Sprints verwalten |
| **CRM** | Kunden und Kontakte verwalten |
| **Inventar** | Bestandslisten und Assets tracken |
| **Rezepte** | Essensplanung und Zutaten |
| **Home Assistant** | Sensordaten strukturiert speichern |

## API nutzen

NocoDB stellt automatisch eine REST-API für jede Tabelle bereit:

```
http://[IP]:2289/api/v1/db/data/v1/[project]/[table]
```

Die API kann z.B. in [n8n](n8n.md), [NodeRED](nodered.md) oder Home Assistant verwendet werden.

## Hinweise

- Die Datenbank läuft als separater PostgreSQL-Container
- Daten werden in `./volumes/nocodb/` gespeichert
- Für die API ist ein Auth-Token nötig (in den NocoDB-Einstellungen erstellen)
- NocoDB ist als Airtable-Open-Source-Alternative gedacht

## Weitere Informationen

- [Offizielle Dokumentation](https://docs.nocodb.com/)
- [GitHub Repository](https://github.com/nocodb/nocodb)
- [API Dokumentation](https://docs.nocodb.com/developer-resources/rest-apis)
