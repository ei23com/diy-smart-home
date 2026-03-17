# Home Assistant

[Home Assistant](https://www.home-assistant.io/) is the most popular open-source smart home platform. It connects thousands of devices and services and enables complex automations.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable
    container_name: homeassistant
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./volumes/homeassistant/config:/config
      - /run/dbus:/run/dbus:ro
    environment:
      - TZ=Europe/Berlin
```

!!!note "Network Mode"
    The template uses `network_mode: host` for best compatibility with local device discovery (mDNS, SSDP, etc.).

## First Start

1. After starting, you can access Home Assistant at `http://[IP]:8123`
2. Create an admin account
3. Configure your location data
4. Start adding integrations

## Integrations

Home Assistant connects with many devices and services:

### Local Integrations

| Integration | Description |
|-------------|-------------|
| **MQTT** | Connection with MQTT broker |
| **ESPHome** | ESPHome devices automatically detected |
| **Shelly** | WLAN devices from Shelly |
| **Zigbee2MQTT** | Zigbee devices via MQTT |
| **InfluxDB** | Export data |
| **NodeRED** | Complex automations |

### Cloud Integrations

| Integration | Description |
|-------------|-------------|
| **Alexa** | Amazon voice control |
| **Google Assistant** | Google voice control |
| **Spotify** | Music control |
| **Weather** | Weather data |

## HACS (Home Assistant Community Store)

HACS allows installing community integrations:

### Installation

The ei23 script installs HACS automatically. Manual installation:

1. Download HACS: [hacs.xyz](https://hacs.xyz/)
2. Copy the `hacs` folder to `/config/custom_components/`
3. Restart Home Assistant
4. Go to **Settings** → **Integrations** → **HACS**

### Popular HACS Integrations

| Integration | Description |
|-------------|-------------|
| **hass-node-red** | NodeRED in HA |
| **Mushroom** | Modern UI cards |
| **Button Card** | Customizable buttons |
| **ApexCharts** | Advanced charts |
| **Auto Entities** | Dynamic lists |

## Automations

### Example: Light on Motion

```yaml
automation:
  - alias: "Light on Motion in Hallway"
    trigger:
      platform: state
      entity_id: binary_sensor.motion_hallway
      to: "on"
    condition:
      condition: time
      after: "07:00:00"
      before: "22:00:00"
    action:
      service: light.turn_on
      target:
        entity_id: light.hallway
```

### Example: Heating in the Morning

```yaml
automation:
  - alias: "Heating Up in the Morning"
    trigger:
      platform: time
      at: "06:30:00"
    condition:
      condition: time
      weekday:
        - mon
        - tue
        - wed
        - thu
        - fri
    action:
      service: climate.set_temperature
      target:
        entity_id: climate.living_room
      data:
        temperature: 21
```

## Dashboards

Home Assistant offers customizable dashboards:

### Lovelace (Default)

The default dashboard can be customized via the web interface:

1. Click the three dots in the top right
2. **Edit Dashboard**
3. Add cards:

| Card | Description |
|------|-------------|
| **Entities** | List of devices |
| **Button** | Single switch |
| **Glance** | Quick overview |
| **History** | History chart |
| **Weather** | Weather forecast |
| **Map** | Location map |

### Custom Dashboards

With HACS and Mushroom/Button Cards, you can create modern UIs.

## Backups

### Automatic Backup

Add to your `configuration.yaml`:

```yaml
backup:
```

### Manual Backup

```bash
# Create backup
cd ~/ei23-docker/
docker compose exec homeassistant tar -czf /config/backup-$(date +%Y%m%d).tar.gz /config
```

### Migrating from Home Assistant OS

!!!note "Restore Backup from HA OS"
    Home Assistant OS is [somewhat different](#home-assistant-docker-vs-supervised-home-assistant) in structure, but ultimately runs the exact same version of Home Assistant as in this script.

1. Create a backup with Home Assistant OS via the backup function in the web interface
2. Save the *.tar file
3. Copy the contents to this folder: `/home/user/ei23-docker/volumes/homeassistant/config`
4. Restart Home Assistant: `docker restart homeassistant`
5. The backup will be imported

## Connecting Hardware

### USB Devices

Add devices in docker-compose.yml:

```yaml
devices:
  - /dev/ttyUSB0:/dev/ttyUSB0  # Zigbee stick
  - /dev/ttyACM0:/dev/ttyACM0  # ConBee
```

### GPIO (Raspberry Pi)

For GPIO access on the Raspberry Pi:

```yaml
devices:
  - /dev/gpiomem:/dev/gpiomem
volumes:
  - /sys:/sys
```

## Home Assistant Docker vs. Supervised

There are two versions of Home Assistant:

| Feature | Docker (ei23) | Supervised/OS |
|---------|---------------|---------------|
| **Flexibility** | ✅ Maximum | ⚠️ Limited |
| **Docker Images** | ✅ All available | ⚠️ Only Addons |
| **Addons** | ⚠️ As separate containers | ✅ Integrated |
| **Hardware** | ⚠️ Manual configuration | ✅ Automatic |
| **Updates** | Via docker compose | Via HA Supervisor |

!!!success "Why Docker?"
    In this script, we use Home Assistant Docker. This offers significantly more flexibility and access to all Docker images, not just the official addons. Technically, addons are also just pre-configured Docker containers.

## Secure with HTTPS

See:
- [Reverse Proxy with Traefik](traefik.md)
- [Reverse Proxy with Nginx Proxy Manager](nginxproxy.md)

## Notes

- The configuration is located in `./volumes/homeassistant/config/`
- The main configuration file is `configuration.yaml`
- Automations in `automations.yaml`
- Custom components in `custom_components/`
- Minimum 2GB RAM recommended

## Further Information

- [Official Documentation](https://www.home-assistant.io/docs/)
- [Home Assistant Community](https://community.home-assistant.io/)
- [GitHub Repository](https://github.com/home-assistant/core)
- [Integrations Overview](https://www.home-assistant.io/integrations/)
