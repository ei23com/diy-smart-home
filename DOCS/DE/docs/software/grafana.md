# Grafana

[Grafana](https://grafana.com/) ist ein leistungsstarkes Tool zur Visualisierung von Daten. Es wird häufig für Dashboards mit Zeitreihendaten (z.B. Sensordaten) verwendet.

!!!tip "Datenquelle wählen"
    Grafana unterstützt viele Datenquellen: **PostgreSQL** (empfohlen), MySQL, InfluxDB, Prometheus, und viele mehr. Für neue Projekte empfehle ich **PostgreSQL** mit der TimescaleDB-Erweiterung. Für Bestandsinstallationen mit [InfluxDB](influx.md) funktioniert alles weiterhin.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - ./volumes/grafana:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=password_placeholder
    restart: unless-stopped
```

## Erster Start

1. Nach dem Start erreichst du Grafana unter `http://[IP]:3000`
2. Login mit **admin** / **admin** (oder dem in der docker-compose gesetzten Passwort)
3. Beim ersten Login wirst du aufgefordert, ein neues Passwort zu setzen

## Datenquelle hinzufügen

Die häufigste Kombination ist Grafana mit InfluxDB:

1. Gehe zu **Connections** → **Data Sources**
2. Klicke auf **Add data source**
3. Wähle **InfluxDB**
4. Konfiguriere die Verbindung:
    - **URL**: `http://influxdb:8086` (falls InfluxDB im Docker läuft)
    - **Database**: Deine InfluxDB-Datenbank (z.B. `homeassistant`)
    - **User/Password**: Falls konfiguriert

!!!tip "Home Assistant Daten"
    Wenn du Home Assistant mit InfluxDB nutzt, kannst du alle Sensordaten in Grafana visualisieren.

## Dashboards erstellen

Grafana bietet zwei Wege Dashboards zu erstellen:

### Community Dashboards importieren

1. Gehe zu **Dashboards** → **New** → **Import**
2. Gib eine Dashboard-ID ein (z.B. von [grafana.com/grafana/dashboards](https://grafana.com/grafana/dashboards/))
3. Wähle deine Datenquelle und klicke **Import**

### Eigenes Dashboard erstellen

1. Klicke auf **+** → **Create new dashboard**
2. Füge Panels hinzu und konfiguriere Queries
3. Speichere das Dashboard

## Empfohlene Dashboards

| ID | Name | Beschreibung |
|----|------|--------------|
| 11074 | Home Assistant | Alle HA-Sensoren |
| 9096 | System Metrics | CPU, RAM, Disk |
| 12065 | Docker Metrics | Container-Status |

## Hinweise

- Die Daten werden in `./volumes/grafana/` gespeichert
- Dashboards können als JSON exportiert/importiert werden
- Grafana unterstützt Alerts per Email, Telegram, Discord, etc.
- Die Portnummer ist standardmäßig 3000

## Weitere Informationen

- [Offizielle Dokumentation](https://grafana.com/docs/grafana/)
- [Dashboard-Sammlung](https://grafana.com/grafana/dashboards/)
- [GitHub Repository](https://github.com/grafana/grafana)
