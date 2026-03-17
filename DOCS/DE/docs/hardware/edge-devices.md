# Edge Devices (Sensoren & Aktoren)

Edge Devices sind die "Sinne und Muskeln" deines Smart Home Systems. Sie messen Werte, erkennen Ereignisse und schalten Geräte. Hier erfährst du, welche Geräte es gibt und wie du sie einbindest.

## Kommunikationsprotokolle

| Protokoll | Reichweite | Strom | Vorteile | Nachteile |
|-----------|------------|-------|----------|-----------|
| **WLAN** | 30-50m | Hoch | Einfach, Internet | Viele Geräte überlasten WLAN |
| **Zigbee** | 10-20m | Niedrig | Mesh-Netzwerk, Batterie | Benötigt Gateway |
| **Z-Wave** | 30m | Niedrig | Keine WLAN-Interferenz | Teuer, weniger Auswahl |
| **433MHz** | 50-100m | Sehr niedrig | Günstig, Reichweite | Kein Feedback, unsicher |
| **BLE (Bluetooth)** | 10m | Sehr niedrig | Einfach, günstig | Begrenzte Reichweite |
| **ESPHome (WLAN)** | 30-50m | Hoch | Vollständig anpassbar | WLAN-Last |

## WLAN-Geräte

### Shelly

[Shelly](https://www.shelly.com/) bietet WLAN-basierte Schalter, Sensoren und Aktoren:

| Gerät | Preis | Funktion |
|-------|-------|----------|
| **Shelly 1** | ~10€ | Relais-Schalter |
| **Shelly Plus 1** | ~15€ | Relais-Schalter (neu) |
| **Shelly Plus H&T** | ~20€ | Temperatur & Feuchte |
| **Shelly Plus Plug S** | ~18€ | Smarte Steckdose |
| **Shelly Plus 2PM** | ~22€ | 2x Relais + Energie |
| **Shelly Plus i4** | ~20€ | 4x Taster-Eingang |
| **Shelly Plus Smoke** | ~30€ | Rauchmelder |
| **Shelly Plus Motion** | ~25€ | Bewegungsmelder |

**Vorteile:** Kein Gateway nötig, lokale API, MQTT-Support

!!!tip "Shelly Firmware"
    Shelly-Geräte unterstützen MQTT nativ. Konfiguriere die MQTT-Verbindung in der Shelly-Weboberfläche.

### Sonoff

| Gerät | Preis | Funktion |
|-------|-------|----------|
| **Sonoff Mini** | ~8€ | Relais-Schalter |
| **Sonoff TH16** | ~12€ | Temperatur-Schalter |
| **Sonoff POW** | ~15€ | Energiemessung |
| **Sonoff 4CH Pro** | ~20€ | 4x Relais |

### Tapo / Kasa

| Gerät | Preis | Funktion |
|-------|-------|----------|
| **Tapo P110** | ~15€ | Smarte Steckdose |
| **Tapo T310** | ~25€ | Temperatur & Feuchte |
| **Tapo C110** | ~25€ | Kamera |

## Zigbee-Geräte

Zigbee bildet ein Mesh-Netzwerk - perfekt für batteriebetriebene Sensoren.

### Gateway / Stick

| Gerät | Preis | Beschreibung |
|-------|-------|--------------|
| **Sonoff Zigbee 3.0 Dongle Plus** | ~10€ | **Empfohlen** - CC2652 |
| **ConBee II** | ~35€ | Beliebt, gut unterstützt |
| **SkyConnect** | ~30€ | Offizielles HA-Addon |
| **ZBDongle-E** | ~15€ | E1652 Chip |

### Sensoren

| Gerät | Preis | Funktion |
|-------|-------|----------|
| **Aqara Temperatur** | ~10€ | Temp & Feuchte |
| **Aqara Türkontakt** | ~12€ | Tür/Fenster |
| **Aqara Bewegungsmelder** | ~15€ | Bewegung |
| **Aqara Wasser Sensor** | ~12€ | Wassererkennung |
| **IKEA VALLHORN** | ~10€ | Bewegungsmelder |
| **IKEA PARASOLL** | ~10€ | Türkontakt |

### Schalter & Aktoren

| Gerät | Preis | Funktion |
|-------|-------|----------|
| **IKEA TRÅDFRI** | ~8€ | LED-Controller |
| **IKEA INSPELNING** | ~10€ | Smarte Steckdose |
| **Sonoff ZBMINI** | ~12€ | Relais-Schalter |
| **Aqara Smart Plug** | ~15€ | Steckdose mit Messung |

## ESPHome

[ESPHome](../software/esphome.md) ermöglicht eigene Sensoren mit ESP8266/ESP32 Chips:

### Fertige ESP-Module

| Gerät | Preis | Funktion |
|-------|-------|----------|
| **ESP32 Dev Board** | ~5€ | Universell einsetzbar |
| **ESP8266 (Wemos D1)** | ~3€ | Günstig für einfache Aufgaben |
| **ESP32-S3** | ~8€ | Mehr GPIO, BLE5 |
| **ESP32-CAM** | ~10€ | Mini-Kamera |

### Beliebte ESPHome-Projekte

| Projekt | Hardware | Funktion |
|---------|----------|----------|
| **Temperatur-Station** | ESP32 + BME280 | Raumklima |
| **Präsenz-Erkennung** | ESP32 + LD2410 | mmWave Personenerkennung |
| **CO2-Monitor** | ESP32 + SCD40 | Luftqualität |
| **LED-Controller** | ESP32 + WS2812B | RGB-LEDs |
| **Garagentor** | ESP32 + Relais | Tor-Steuerung |
| **Taster-Eingang** | ESP32 + Taster | Physische Schalter |

### Beispiel-Konfiguration

```yaml
esphome:
  name: klimasensor
  platform: ESP32
  board: esp32dev

wifi:
  ssid: "DEIN_WLAN"
  password: "DEIN_PASSWORT"

sensor:
  - platform: bme280
    temperature:
      name: "Raumtemperatur"
    humidity:
      name: "Raumfeuchte"
    address: 0x76
```

## 433MHz (RTL-SDR)

Mit einem DVB-T Stick und rtl_433 kannst du 433MHz-Geräte empfangen:

### Hardware

| Gerät | Preis | Beschreibung |
|-------|-------|--------------|
| **RTL-SDR Stick** | ~25€ | DVB-T USB-Stick |
| **433MHz Antenne** | ~5€ | Bessere Reichweite |

### Unterstützte Geräte

- Wetterstationen (Bresser, Auriol, etc.)
- 433MHz Türkontakte
- 433MHz Bewegungsmelder
- Funksteckdosen
- (Nur empfangen, nicht senden!)

!!!warning "Sicherheit"
    433MHz ist unverschlüsselt. Nutze es nur für unkritische Sensoren.

## Übersicht: Empfohlene Starter-Pakete

### Einsteiger (~50€)

```
1x Sonoff Zigbee 3.0 Dongle Plus     10€
3x Aqara Temperatursensor            30€
1x Aqara Türkontakt                  12€
────────────────────────────────────────
Gesamt                               ~52€
```

### Standard (~150€)

```
1x Sonoff Zigbee 3.0 Dongle Plus     10€
5x Aqara Temperatursensor            50€
3x Aqara Türkontakt                  36€
2x Aqara Bewegungsmelder             30€
1x IKEA INSPELNING Steckdose         10€
────────────────────────────────────────
Gesamt                               ~136€
```

### Erweitert (~300€)

```
1x Sonoff Zigbee 3.0 Dongle Plus     10€
10x Aqara Temperatursensor          100€
5x Aqara Türkontakt                  60€
5x Aqara Bewegungsmelder             75€
5x IKEA Smarte Lampen                50€
2x Shelly Plus 1                     30€
1x ESP32 Dev Board + Sensoren        20€
────────────────────────────────────────
Gesamt                               ~345€
```

## Weitere Informationen

- [Zigbee2MQTT Kompatibilität](https://zigbee.blakadder.com/)
- [ESPHome Projekte](https://esphome.io/guides/diy)
- [Shelly Dokumentation](https://www.shelly.com/de/support)
- [rtl_433 Geräteliste](https://github.com/merbanan/rtl_433)
