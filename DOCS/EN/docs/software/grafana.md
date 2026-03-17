# Grafana

[Grafana](https://grafana.com/) is a powerful data visualization tool. It is commonly used for dashboards with time-series data (e.g., sensor data).

!!!tip "Choosing a Data Source"
    Grafana supports many data sources: **PostgreSQL** (recommended), MySQL, InfluxDB, Prometheus, and many more. For new projects, I recommend **PostgreSQL** with the TimescaleDB extension. For existing installations with [InfluxDB](influx.md), everything continues to work.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

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

## First Start

1. After starting, you can access Grafana at `http://[IP]:3000`
2. Login with **admin** / **admin** (or the password set in docker-compose)
3. On first login, you will be prompted to set a new password

## Add Data Source

The most common combination is Grafana with InfluxDB:

1. Go to **Connections** → **Data Sources**
2. Click **Add data source**
3. Select **InfluxDB**
4. Configure the connection:
    - **URL**: `http://influxdb:8086` (if InfluxDB runs in Docker)
    - **Database**: Your InfluxDB database (e.g., `homeassistant`)
    - **User/Password**: If configured

!!!tip "Home Assistant Data"
    If you use Home Assistant with InfluxDB, you can visualize all sensor data in Grafana.

## Create Dashboards

Grafana offers two ways to create dashboards:

### Import Community Dashboards

1. Go to **Dashboards** → **New** → **Import**
2. Enter a dashboard ID (e.g., from [grafana.com/grafana/dashboards](https://grafana.com/grafana/dashboards/))
3. Select your data source and click **Import**

### Create Your Own Dashboard

1. Click **+** → **Create new dashboard**
2. Add panels and configure queries
3. Save the dashboard

## Recommended Dashboards

| ID | Name | Description |
|----|------|-------------|
| 11074 | Home Assistant | All HA sensors |
| 9096 | System Metrics | CPU, RAM, Disk |
| 12065 | Docker Metrics | Container status |

## Notes

- Data is stored in `./volumes/grafana/`
- Dashboards can be exported/imported as JSON
- Grafana supports alerts via email, Telegram, Discord, etc.
- The default port is 3000

## Further Information

- [Official Documentation](https://grafana.com/docs/grafana/)
- [Dashboard Collection](https://grafana.com/grafana/dashboards/)
- [GitHub Repository](https://github.com/grafana/grafana)
