# ESPHome

[ESPHome](https://esphome.io/) ist ein System zur einfachen Konfigurierung von ESP8266/ESP32-Mikrocontrollern. Es ermöglicht dir, eigene Sensoren, Aktoren und Smart-Home-Geräte zu erstellen - ohne Programmierkenntnisse.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

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

## Erster Start

1. Nach dem Start erreichst du ESPHome unter `http://[IP]:6052`
2. Beim ersten Start musst du einen Zugang einrichten
3. Erstelle ein neues Gerät mit **+ NEW DEVICE**

## Konfiguration erstellen

ESPHome nutzt YAML-Dateien für die Konfiguration:

```yaml
# Beispiel: Temperatursensor
esphome:
  name: temperatur-sensor
  platform: ESP32
  board: esp32dev

wifi:
  ssid: "DEIN_WLAN"
  password: "DEIN_PASSWORT"

# Enable logging
logger:

# Enable Home Assistant API
api:
  encryption:
    key: "DEIN_API_KEY"

ota:
  - platform: esphome
    password: "DEIN_OTA_PASSWORT"

sensor:
  - platform: dht
    pin: GPIO14
    temperature:
      name: "Raumtemperatur"
    humidity:
      name: "Raumfeuchte"
    update_interval: 60s
```

## Home Assistant Integration

ESPHome Geräte werden automatisch in Home Assistant erkannt:

1. Stelle sicher, dass die Home Assistant API aktiviert ist
2. Das Gerät erscheint automatisch unter **Einstellungen** → **Geräte**
3. Keine weitere Konfiguration nötig!

!!!tip "Automatische Erkennung"
    ESPHome nutzt mDNS für die automatische Erkennung. Dein Gerät muss im gleichen Netzwerk wie Home Assistant sein.

## Beliebte Anwendungen

| Anwendung | Hardware | Beschreibung |
|-----------|----------|--------------|
| **Temperatur** | DHT22, BME280 | Raumklima messen |
| **Präsenz** | LD2410 | Personen erkennen |
| **LED** | WS2812B | RGB-LED-Streifen steuern |
| **Relais** | Relais-Modul | Geräte schalten |
| **Taster** | Taster | Physische Schalter |
| **Motor** | Servo, Schrittmotor | Jalousien, Garagentor |
| **Energie** | CT-Sensor | Stromverbrauch messen |

## OTA-Updates (Over The Air)

Nach der Erstinstallation per USB können Updates über die Weboberfläche erfolgen:

1. Kompiliere die Konfiguration in ESPHome
2. Klicke auf **INSTALL** → **Wirelessly**
3. Das Gerät wird automatisch aktualisiert

## Hinweise

- Die Konfigurationsdateien werden in `./volumes/esphome/` gespeichert
- Für die Erstinstallation ist ein USB-Anschluss nötig
- ESPHome unterstützt ESP8266 und ESP32 Chips
- Die Konfiguration ist rein YAML-basiert - kein Programmieren nötig
- Viele fertige Konfigurationen in der [ESPHome Gallery](https://esphome.io/guides/diy)

## Hardware-Empfehlungen

| Chip | Preis | Empfehlung |
|------|-------|------------|
| **ESP32** | ~5€ | ✅ Empfohlen |
| **ESP8266** | ~3€ | Gut für einfache Projekte |
| **ESP32-S3** | ~8€ | Für komplexe Projekte |

## Weitere Informationen

- [Offizielle Dokumentation](https://esphome.io/)
- [GitHub Repository](https://github.com/esphome/esphome)
- [ESPHome Gallery](https://esphome.io/guides/diy)
- [Home Assistant Community](https://community.home-assistant.io/tag/esphome)
