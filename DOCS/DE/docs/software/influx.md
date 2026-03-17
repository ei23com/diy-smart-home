# InfluxDB

[InfluxDB](https://www.influxdata.com/) ist eine Time-Series-Datenbank. Sie wird häufig verwendet, um Sensordaten, Metriken und andere zeitbasierte Daten zu speichern.

!!!warning "InfluxDB - Projekt in ungewisser Zukunft"
    InfluxDB hat mit Version 3 einige Breaking Changes eingeführt und das Projekt zeigt Anzeichen von Nachlässigkeit (AGPL-Lizenz-Wechsel, Community-Edition eingeschränkt). Die Zukunft ist ungewiss. 
    
    **Empfehlung:** Für neue Projekte nutze besser **[PostgreSQL](../start/docker-compose)** mit TimescaleDB-Erweiterung. PostgreSQL ist ein bewährtes, zukunftssicheres Datenbank-System und viele Home-Automations-Tools unterstützen es nativ. Für Bestandsinstallationen mit InfluxDB funktioniert alles weiterhin.
    
    Siehe auch: ["Postgres for Everything"](https://www.amazingcto.com/postgres-for-everything/) - Warum PostgreSQL die beste Wahl für die meisten Anwendungsfälle ist.

## Versionen

Es gibt verschiedene Versionen von InfluxDB:

| Version | Status | Empfehlung |
|---------|--------|------------|
| **InfluxDB 1.8** | Stabil, einfacher | ✅ Für Home Assistant |
| **InfluxDB 2.x** | Neuere API, Flux-Query | Für fortgeschrittene Anwendungsfälle |

!!!note "Home Assistant Kompatibilität"
    Home Assistant arbeitet standardmäßig am besten mit InfluxDB 1.8. Für InfluxDB 2.x wird das InfluxDB v2 Addon benötigt.

## Installation - InfluxDB 1.8 (empfohlen)

```yaml
  influxdb:
    image: influxdb:1.8
    container_name: influxdb
    restart: unless-stopped
    ports:
      - "8086:8086"
    volumes:
      - ./volumes/influxdb:/var/lib/influxdb
    environment:
      - INFLUXDB_DB=homeassistant
      - INFLUXDB_ADMIN_USER=admin
      - INFLUXDB_ADMIN_PASSWORD=password_placeholder
```

## Installation - InfluxDB 2.x

```yaml
  influxdb2:
    image: influxdb:2
    container_name: influxdb2
    restart: unless-stopped
    ports:
      - "8086:8086"
    volumes:
      - ./volumes/influxdb2:/var/lib/influxdb2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=password_placeholder
      - DOCKER_INFLUXDB_INIT_ORG=ei23
      - DOCKER_INFLUXDB_INIT_BUCKET=homeassistant
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=DEIN_TOKEN
```

## Home Assistant verbinden

Füge folgende Konfiguration in die `configuration.yaml` von Home Assistant ein:

```yaml
influxdb:
  host: 172.17.0.1  # Docker Gateway IP
  port: 8086
  database: homeassistant
  username: admin
  password: !secret influxdb_password
  default_measurement: state
```

!!!tip "Docker Gateway IP"
    Die IP `172.17.0.1` ist die Standard-Docker-Gateway-IP. Alternativ kannst du `influxdb` als Hostnamen verwenden, wenn Home Assistant im gleichen Docker-Netzwerk läuft.

## Hinweise

- Die Daten werden in `./volumes/influxdb/` gespeichert
- Die API erreichst du unter `http://[IP]:8086`
- Kombiniere mit [Grafana](grafana.md) für Visualisierungen
- Regelmäßige Backups empfohlen - Sensordaten gehen schnell verloren!
- Für automatische Datenbereinigung setze Retention Policies

## CLI nutzen

```bash
# InfluxDB Shell öffnen
docker exec -it influxdb influx

# Datenbanken anzeigen
SHOW DATABASES

# Daten abfragen (Beispiel)
USE homeassistant
SELECT * FROM "°C" LIMIT 10
```

## Weitere Informationen

- [InfluxDB 1.8 Dokumentation](https://docs.influxdata.com/influxdb/v1.8/)
- [InfluxDB 2.x Dokumentation](https://docs.influxdata.com/influxdb/v2/)
- [GitHub Repository](https://github.com/influxdata/influxdb)
