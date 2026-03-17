# MQTT Explorer

[MQTT Explorer](https://mqtt-explorer.com/) is a graphical MQTT client for desktop and browser. It allows you to monitor, analyze, and debug MQTT messages.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!note "Mosquitto Required"
    MQTT Explorer requires an MQTT broker. By default, [Mosquitto](../start/faq) is installed with the ei23 script.

## Template

```yaml
  mqtt-explorer:
    image: sapk/mqtt-explorer
    container_name: mqtt-explorer
    restart: unless-stopped
    ports:
      - "4004:4004"
```

## First Start

1. After startup, you can access MQTT Explorer at `http://[IP]:4004`
2. Click on **+** to create a new connection
3. Enter the IP address of your MQTT broker (e.g., `mosquitto` or `192.168.1.x`)
4. Default port: `1883`

## Configure Connection

| Field | Value |
|-------|-------|
| **Host** | `mosquitto` (Docker) or IP address |
| **Port** | `1883` |
| **Username** | Your MQTT username |
| **Password** | Your MQTT password |

## Features

- **Real-time Monitoring** - See all MQTT messages live
- **Topic Tree** - Clear hierarchy of all topics
- **Send Messages** - Manually publish messages
- **Statistics** - Message history and graphs
- **Filter** - Search for topics and messages
- **Export** - Export messages as JSON

## MQTT with Home Assistant

Home Assistant uses MQTT for many integrations:

### Example Topics

| Topic | Description |
|-------|-------------|
| `homeassistant/#` | Home Assistant Discovery |
| `zigbee2mqtt/#` | Zigbee2MQTT Devices |
| `rtl_433/#` | 433MHz Sensors |
| `esphome/#` | ESPHome Devices |

### Home Assistant Discovery

ESPHome and Zigbee2MQTT use Home Assistant Discovery:

```yaml
# Automatically configured devices appear under:
homeassistant/sensor/[device_name]/config
```

## MQTT with ESPHome

ESPHome communicates by default via the Home Assistant API, but can also use MQTT:

```yaml
mqtt:
  broker: 192.168.1.x
  username: mqtt_user
  password: !secret mqtt_password
```

## Debugging with MQTT Explorer

How to find MQTT issues:

1. Open MQTT Explorer
2. Filter by the relevant topic
3. Check if messages are being sent/received
4. Analyze the message structure
5. Test sending messages manually

## Notes

- The port is 4004 by default
- MQTT Explorer is also available as a desktop app
- Ideal for troubleshooting MQTT problems
- Can also be used for Node-RED debugging

## Further Information

- [Official Website](https://mqtt-explorer.com/)
- [GitHub Repository](https://github.com/thomasnordquist/MQTT-Explorer)
- [MQTT Documentation](https://mqtt.org/documentation)
