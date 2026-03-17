# Hardware Structure

This page explains the typical hardware structure of an ei23 Smart Home Server and which components you need.

## Basic Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                │
│                             │                                   │
│                             ▼                                   │
│                    ┌─────────────────┐                          │
│                    │     Router      │                          │
│                    │  (FritzBox etc) │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Smart Home  │    │   Edge      │    │  Clients    │         │
│  │   Server    │◄──►│  Devices    │    │ (Phone,PC)  │         │
│  │ (ei23.sh)   │    │ (Sensors)   │    │             │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                                                          │
│         ▼                                                          │
│  ┌─────────────────────────────────────────────┐                 │
│  │              Docker Container               │                 │
│  │  ┌─────────┐ ┌──────────┐ ┌─────────────┐  │                 │
│  │  │ Home    │ │ NodeRED  │ │ Grafana     │  │                 │
│  │  │Assistant│ │          │ │             │  │                 │
│  │  └─────────┘ └──────────┘ └─────────────┘  │                 │
│  │  ┌─────────┐ ┌──────────┐ ┌─────────────┐  │                 │
│  │  │MQTT     │ │InfluxDB  │ │Vaultwarden  │  │                 │
│  │  │Broker   │ │          │ │             │  │                 │
│  │  └─────────┘ └──────────┘ └─────────────┘  │                 │
│  └─────────────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Smart Home Server (Central Hub)

The [Server](server.md) is the heart of your Smart Home:

| Task | Software |
|------|----------|
| Central Control | Home Assistant, ioBroker, OpenHAB |
| Automation | NodeRED, n8n |
| Database | InfluxDB, PostgreSQL |
| Visualization | Grafana |
| Password Manager | Vaultwarden |
| Cloud Storage | Nextcloud |

!!!tip "Hardware Choice"
    See [Server / Mini-PC Hardware](server.md) for detailed recommendations.

### 2. Edge Devices (Sensors / Actuators)

[Edge Devices](edge-devices.md) are devices that interact with your environment:

| Type | Examples | Protocol |
|------|----------|----------|
| **Temperature** | DHT22, BME280, Shelly | WiFi, Zigbee, ESPHome |
| **Light** | Philips Hue, IKEA | Zigbee |
| **Switches** | Shelly, Sonoff | WiFi, Zigbee |
| **Cameras** | Reolink, TP-Link | RTSP, ONVIF |
| **433MHz** | Weather stations | RTL-SDR |
| **Presence** | Aqara, LD2410 | Zigbee, ESPHome |

### 3. Network

The network connects everything:

```
Router (DHCP, DNS)
    │
    ├── WiFi (Sensors, Phones)
    │
    ├── LAN (Server, PCs)
    │
    └── Zigbee (separate radio network)
            │
            └── Zigbee2MQTT / ConBee
```

## Communication Paths

### MQTT (Message Queue Telemetry Transport)

MQTT is the standard protocol for Smart Home:

```
Sensors ──► MQTT Broker (Mosquitto) ──► Home Assistant
                     │
                     ├──► NodeRED
                     │
                     └──► Grafana / InfluxDB
```

### Zigbee

For battery-powered devices:

```
Zigbee Stick ──► Zigbee2MQTT ──► MQTT Broker ──► Home Assistant
      │
      ├──► Motion sensors
      ├──► Door contacts
      └──► Temperature sensors
```

### WiFi

For mains-powered devices:

```
WiFi Devices ──► Router ──► Home Assistant (Shelly, Sonoff, etc.)
```

### 433MHz (RTL-SDR)

For affordable sensors:

```
RTL-SDR Stick ──► rtl_433 ──► MQTT ──► Home Assistant
      │
      ├──► Weather stations
      └──► Door contacts
```

## Typical Setups

### Minimal Setup (Beginners)

- **Server:** Raspberry Pi 4 (4GB) - ~€70
- **Sensors:** 2-3 Shelly WiFi - ~€30
- **Total:** ~€100

```
Raspberry Pi 4
    │
    └── WiFi
        ├── Shelly 1 (Light switch)
        ├── Shelly Plus H&T (Temperature)
        └── Shelly Plus Plug S (Socket)
```

### Standard Setup (Recommended)

- **Server:** Intel N100 Mini-PC - ~€150
- **Zigbee Stick:** Sonoff Zigbee 3.0 - ~€10
- **Sensors:** 10-20 Zigbee devices - ~€100
- **Total:** ~€260

```
Intel N100 Mini-PC
    │
    ├── Zigbee Stick
    │   ├── 10x Temperature sensors
    │   ├── 5x Door contacts
    │   ├── 3x Motion sensors
    │   └── 10x IKEA/Philips lights
    │
    └── WiFi
        ├── Cameras
        └── Shelly switches
```

### Extended Setup

- **Server:** i5 Mini-PC with GPU - ~€400
- **Edge Devices:** 50+ devices - ~€300
- **Media:** Jellyfin with hardware transcoding
- **AI:** Local LLMs with Ollama/llama-swap
- **Surveillance:** Frigate with 4+ cameras

## Security Architecture

```
Internet
    │
    ▼
┌──────────────┐
│  Firewall    │ (Router)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Reverse Proxy │ (Traefik/Nginx)
│  with SSL    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Docker      │
│  Network     │
└──────────────┘
```

!!!warning "Security"
    - Always use HTTPS with [Traefik](../software/traefik.md) or [Nginx Proxy Manager](../software/nginxproxy.md)
    - Only open necessary ports on the router
    - Use [WireGuard VPN](../software/wireguard.md) for remote access
    - Strong passwords everywhere!

## Further Information

- [Server / Mini-PC Hardware](server.md)
- [Edge Devices](edge-devices.md)
- [Installing Programs](../start/docker-compose.md)
