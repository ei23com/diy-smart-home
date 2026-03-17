# Edge Devices (Sensors & Actuators)

Edge Devices are the "senses and muscles" of your Smart Home system. They measure values, detect events, and control devices. Here you'll learn about the available devices and how to integrate them.

## Communication Protocols

| Protocol | Range | Power | Advantages | Disadvantages |
|----------|-------|-------|------------|---------------|
| **WiFi** | 30-50m | High | Simple, Internet | Many devices overload WiFi |
| **Zigbee** | 10-20m | Low | Mesh network, Battery | Requires gateway |
| **Z-Wave** | 30m | Low | No WiFi interference | Expensive, less selection |
| **433MHz** | 50-100m | Very low | Affordable, Range | No feedback, insecure |
| **BLE (Bluetooth)** | 10m | Very low | Simple, affordable | Limited range |
| **ESPHome (WiFi)** | 30-50m | High | Fully customizable | WiFi load |

## WiFi Devices

### Shelly

[Shelly](https://www.shelly.com/) offers WiFi-based switches, sensors, and actuators:

| Device | Price | Function |
|--------|-------|----------|
| **Shelly 1** | ~€10 | Relay switch |
| **Shelly Plus 1** | ~€15 | Relay switch (new) |
| **Shelly Plus H&T** | ~€20 | Temperature & humidity |
| **Shelly Plus Plug S** | ~€18 | Smart socket |
| **Shelly Plus 2PM** | ~€22 | 2x Relay + Energy |
| **Shelly Plus i4** | ~€20 | 4x Button input |
| **Shelly Plus Smoke** | ~€30 | Smoke detector |
| **Shelly Plus Motion** | ~€25 | Motion sensor |

**Advantages:** No gateway required, local API, MQTT support

!!!tip "Shelly Firmware"
    Shelly devices support MQTT natively. Configure the MQTT connection in the Shelly web interface.

### Sonoff

| Device | Price | Function |
|--------|-------|----------|
| **Sonoff Mini** | ~€8 | Relay switch |
| **Sonoff TH16** | ~€12 | Temperature switch |
| **Sonoff POW** | ~€15 | Energy monitoring |
| **Sonoff 4CH Pro** | ~€20 | 4x Relay |

### Tapo / Kasa

| Device | Price | Function |
|--------|-------|----------|
| **Tapo P110** | ~€15 | Smart socket |
| **Tapo T310** | ~€25 | Temperature & humidity |
| **Tapo C110** | ~€25 | Camera |

## Zigbee Devices

Zigbee forms a mesh network - perfect for battery-powered sensors.

### Gateway / Stick

| Device | Price | Description |
|--------|-------|-------------|
| **Sonoff Zigbee 3.0 Dongle Plus** | ~€10 | **Recommended** - CC2652 |
| **ConBee II** | ~€35 | Popular, well supported |
| **SkyConnect** | ~€30 | Official HA addon |
| **ZBDongle-E** | ~€15 | E1652 Chip |

### Sensors

| Device | Price | Function |
|--------|-------|----------|
| **Aqara Temperature** | ~€10 | Temp & Humidity |
| **Aqara Door Contact** | ~€12 | Door/Window |
| **Aqara Motion Sensor** | ~€15 | Motion |
| **Aqara Water Sensor** | ~€12 | Water detection |
| **IKEA VALLHORN** | ~€10 | Motion sensor |
| **IKEA PARASOLL** | ~€10 | Door contact |

### Switches & Actuators

| Device | Price | Function |
|--------|-------|----------|
| **IKEA TRÅDFRI** | ~€8 | LED controller |
| **IKEA INSPELNING** | ~€10 | Smart socket |
| **Sonoff ZBMINI** | ~€12 | Relay switch |
| **Aqara Smart Plug** | ~€15 | Socket with monitoring |

## ESPHome

[ESPHome](../software/esphome.md) enables custom sensors with ESP8266/ESP32 chips:

### Ready-Made ESP Modules

| Device | Price | Function |
|--------|-------|----------|
| **ESP32 Dev Board** | ~€5 | Universally usable |
| **ESP8266 (Wemos D1)** | ~€3 | Affordable for simple tasks |
| **ESP32-S3** | ~€8 | More GPIO, BLE5 |
| **ESP32-CAM** | ~€10 | Mini camera |

### Popular ESPHome Projects

| Project | Hardware | Function |
|---------|----------|----------|
| **Temperature Station** | ESP32 + BME280 | Room climate |
| **Presence Detection** | ESP32 + LD2410 | mmWave person detection |
| **CO2 Monitor** | ESP32 + SCD40 | Air quality |
| **LED Controller** | ESP32 + WS2812B | RGB LEDs |
| **Garage Door** | ESP32 + Relay | Gate control |
| **Button Input** | ESP32 + Buttons | Physical switches |

### Example Configuration

```yaml
esphome:
  name: climate_sensor
  platform: ESP32
  board: esp32dev

wifi:
  ssid: "YOUR_WIFI"
  password: "YOUR_PASSWORD"

sensor:
  - platform: bme280
    temperature:
      name: "Room Temperature"
    humidity:
      name: "Room Humidity"
    address: 0x76
```

## 433MHz (RTL-SDR)

With a DVB-T stick and rtl_433, you can receive 433MHz devices:

### Hardware

| Device | Price | Description |
|--------|-------|-------------|
| **RTL-SDR Stick** | ~€25 | DVB-T USB stick |
| **433MHz Antenna** | ~€5 | Better range |

### Supported Devices

- Weather stations (Bresser, Auriol, etc.)
- 433MHz door contacts
- 433MHz motion sensors
- Radio-controlled sockets
- (Receive only, not transmit!)

!!!warning "Security"
    433MHz is unencrypted. Use it only for non-critical sensors.

## Overview: Recommended Starter Packages

### Beginner (~€50)

```
1x Sonoff Zigbee 3.0 Dongle Plus     €10
3x Aqara Temperature sensor          €30
1x Aqara Door contact                €12
────────────────────────────────────────
Total                                ~€52
```

### Standard (~€150)

```
1x Sonoff Zigbee 3.0 Dongle Plus     €10
5x Aqara Temperature sensor          €50
3x Aqara Door contact                €36
2x Aqara Motion sensor               €30
1x IKEA INSPELNING Socket            €10
────────────────────────────────────────
Total                                ~€136
```

### Extended (~€300)

```
1x Sonoff Zigbee 3.0 Dongle Plus     €10
10x Aqara Temperature sensor         €100
5x Aqara Door contact                €60
5x Aqara Motion sensor               €75
5x IKEA Smart Lights                 €50
2x Shelly Plus 1                     €30
1x ESP32 Dev Board + Sensors         €20
────────────────────────────────────────
Total                                ~€345
```

## Further Information

- [Zigbee2MQTT Compatibility](https://zigbee.blakadder.com/)
- [ESPHome Projects](https://esphome.io/guides/diy)
- [Shelly Documentation](https://www.shelly.com/de/support)
- [rtl_433 Device List](https://github.com/merbanan/rtl_433)
