# MQTT Explorer

[MQTT Explorer](https://mqtt-explorer.com/) ist ein grafischer MQTT-Client für Desktop und Browser. Er ermöglicht es dir, MQTT-Nachrichten zu überwachen, zu analysieren und zu debuggen.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!note "Mosquitto erforderlich"
    MQTT Explorer benötigt einen MQTT-Broker. Standardmäßig wird [Mosquitto](../start/faq) mit dem ei23-Skript installiert.

## Template

```yaml
  mqtt-explorer:
    image: sapk/mqtt-explorer
    container_name: mqtt-explorer
    restart: unless-stopped
    ports:
      - "4004:4004"
```

## Erster Start

1. Nach dem Start erreichst du MQTT Explorer unter `http://[IP]:4004`
2. Klicke auf **+** um eine neue Verbindung zu erstellen
3. Gib die IP-Adresse deines MQTT-Brokers ein (z.B. `mosquitto` oder `192.168.1.x`)
4. Standard-Port: `1883`

## Verbindung konfigurieren

| Feld | Wert |
|------|------|
| **Host** | `mosquitto` (Docker) oder IP-Adresse |
| **Port** | `1883` |
| **Username** | Dein MQTT-Username |
| **Password** | Dein MQTT-Passwort |

## Features

- **Echtzeit-Überwachung** - Alle MQTT-Nachrichten live sehen
- **Topic-Baum** - Übersichtliche Hierarchie aller Topics
- **Nachrichten senden** - Manuell Nachrichten publishen
- **Statistiken** - Nachrichtenhistorie und Grafiken
- **Filter** - Suche nach Topics und Nachrichten
- **Export** - Nachrichten als JSON exportieren

## MQTT mit Home Assistant

Home Assistant nutzt MQTT für viele Integrationen:

### Beispiel-Topics

| Topic | Beschreibung |
|-------|--------------|
| `homeassistant/#` | Home Assistant Discovery |
| `zigbee2mqtt/#` | Zigbee2MQTT Geräte |
| `rtl_433/#` | 433MHz Sensoren |
| `esphome/#` | ESPHome Geräte |

### Home Assistant Discovery

ESPHome und Zigbee2MQTT nutzen Home Assistant Discovery:

```yaml
# Automatisch konfigurierte Geräte erscheinen unter:
homeassistant/sensor/[device_name]/config
```

## MQTT mit ESPHome

ESPHome kommuniziert standardmäßig über die Home Assistant API, kann aber auch MQTT nutzen:

```yaml
mqtt:
  broker: 192.168.1.x
  username: mqtt_user
  password: !secret mqtt_password
```

## Debuggen mit MQTT Explorer

So findest du Probleme mit MQTT:

1. Öffne MQTT Explorer
2. Filtere nach dem relevanten Topic
3. Prüfe ob Nachrichten gesendet/empfangen werden
4. Analysiere die Nachrichtenstruktur
5. Teste manuelles Senden von Nachrichten

## Hinweise

- Der Port ist standardmäßig 4004
- MQTT Explorer ist auch als Desktop-App verfügbar
- Ideal für die Fehlersuche bei MQTT-Problemen
- Kann auch für Node-RED-Debugging genutzt werden

## Weitere Informationen

- [Offizielle Website](https://mqtt-explorer.com/)
- [GitHub Repository](https://github.com/thomasnordquist/MQTT-Explorer)
- [MQTT Dokumentation](https://mqtt.org/documentation)
