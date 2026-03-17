# ESPHome

[ESPHome](https://esphome.io/) is a system for easily configuring ESP8266/ESP32 microcontrollers. It allows you to create your own sensors, actuators, and smart home devices - without any programming knowledge.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  esphome:
    image: ghcr.io/esphome/esphome:latest
    container_name: esphome
    restart: unless-stopped
    ports:
      - "6052:6052"
    volumes:
      - ./volumes/esphome:/config
    environment:
      - TZ=Europe/Berlin
```

## First Start

1. After starting, you can access ESPHome at `http://[IP]:6052`
2. On first start, you need to set up authentication
3. Create a new device with **+ NEW DEVICE**

## Create Configuration

ESPHome uses YAML files for configuration:

```yaml
# Example: Temperature sensor
esphome:
  name: temperature-sensor
  platform: ESP32
  board: esp32dev

wifi:
  ssid: "YOUR_WIFI"
  password: "YOUR_PASSWORD"

# Enable logging
logger:

# Enable Home Assistant API
api:
  encryption:
    key: "YOUR_API_KEY"

ota:
  - platform: esphome
    password: "YOUR_OTA_PASSWORD"

sensor:
  - platform: dht
    pin: GPIO14
    temperature:
      name: "Room Temperature"
    humidity:
      name: "Room Humidity"
    update_interval: 60s
```

## Home Assistant Integration

ESPHome devices are automatically detected by Home Assistant:

1. Make sure the Home Assistant API is enabled
2. The device will automatically appear under **Settings** → **Devices**
3. No additional configuration needed!

!!!tip "Automatic Detection"
    ESPHome uses mDNS for automatic detection. Your device must be on the same network as Home Assistant.

## Popular Applications

| Application | Hardware | Description |
|-----------|----------|-------------|
| **Temperature** | DHT22, BME280 | Measure room climate |
| **Presence** | LD2410 | Detect people |
| **LED** | WS2812B | Control RGB LED strips |
| **Relay** | Relay module | Switch devices |
| **Button** | Push button | Physical switches |
| **Motor** | Servo, stepper motor | Blinds, garage door |
| **Energy** | CT sensor | Measure power consumption |

## OTA Updates (Over The Air)

After the initial USB installation, updates can be performed via the web interface:

1. Compile the configuration in ESPHome
2. Click **INSTALL** → **Wirelessly**
3. The device will be automatically updated

## Notes

- Configuration files are stored in `./volumes/esphome/`
- A USB connection is required for initial installation
- ESPHome supports ESP8266 and ESP32 chips
- Configuration is purely YAML-based - no programming required
- Many ready-made configurations available in the [ESPHome Gallery](https://esphome.io/guides/diy)

## Hardware Recommendations

| Chip | Price | Recommendation |
|------|-------|----------------|
| **ESP32** | ~€5 | ✅ Recommended |
| **ESP8266** | ~€3 | Good for simple projects |
| **ESP32-S3** | ~€8 | For complex projects |

## Further Information

- [Official Documentation](https://esphome.io/)
- [GitHub Repository](https://github.com/esphome/esphome)
- [ESPHome Gallery](https://esphome.io/guides/diy)
- [Home Assistant Community](https://community.home-assistant.io/tag/esphome)
