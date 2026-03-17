# InfluxDB

[InfluxDB](https://www.influxdata.com/) is a time-series database. It is commonly used to store sensor data, metrics, and other time-based data.

!!!warning "InfluxDB - Project in Uncertain Future"
    InfluxDB has introduced breaking changes with version 3 and the project shows signs of neglect (AGPL license change, community edition limited). The future is uncertain.
    
    **Recommendation:** For new projects, use **[PostgreSQL](../start/docker-compose)** with the TimescaleDB extension instead. PostgreSQL is a proven, future-proof database system and many home automation tools support it natively. For existing InfluxDB installations, everything continues to work.
    
    See also: ["Postgres for Everything"](https://www.amazingcto.com/postgres-for-everything/) - Why PostgreSQL is the best choice for most use cases.

## Versions

There are different versions of InfluxDB:

| Version | Status | Recommendation |
|---------|--------|----------------|
| **InfluxDB 1.8** | Stable, simpler | ✅ For Home Assistant |
| **InfluxDB 2.x** | Newer API, Flux query | For advanced use cases |

!!!note "Home Assistant Compatibility"
    Home Assistant works best by default with InfluxDB 1.8. For InfluxDB 2.x, the InfluxDB v2 addon is required.

## Installation - InfluxDB 1.8 (Recommended)

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
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=YOUR_TOKEN
```

## Connect Home Assistant

Add the following configuration to your Home Assistant `configuration.yaml`:

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
    The IP `172.17.0.1` is the default Docker gateway IP. Alternatively, you can use `influxdb` as the hostname if Home Assistant runs in the same Docker network.

## Notes

- Data is stored in `./volumes/influxdb/`
- The API is accessible at `http://[IP]:8086`
- Combine with [Grafana](grafana.md) for visualizations
- Regular backups recommended - sensor data can be lost quickly!
- Set retention policies for automatic data cleanup

## Using the CLI

```bash
# Open InfluxDB Shell
docker exec -it influxdb influx

# Show databases
SHOW DATABASES

# Query data (example)
USE homeassistant
SELECT * FROM "°C" LIMIT 10
```

## Further Information

- [InfluxDB 1.8 Documentation](https://docs.influxdata.com/influxdb/v1.8/)
- [InfluxDB 2.x Documentation](https://docs.influxdata.com/influxdb/v2/)
- [GitHub Repository](https://github.com/influxdata/influxdb)
