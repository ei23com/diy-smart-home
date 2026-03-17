# Home Assistant

[Home Assistant](https://www.home-assistant.io/) ist die beliebteste Open-Source-Plattform für Smart Home. Sie verbindet tausende von Geräten und Diensten und ermöglicht komplexe Automatisierungen.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

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
    Das Template verwendet `network_mode: host` für beste Kompatibilität mit lokaler Geräteerkennung (mDNS, SSDP, etc.).

## Erster Start

1. Nach dem Start erreichst du Home Assistant unter `http://[IP]:8123`
2. Erstelle einen Admin-Account
3. Konfiguriere deine Standortdaten
4. Beginne mit dem Hinzufügen von Integrationen

## Integrationen

Home Assistant verbindet sich mit vielen Geräten und Diensten:

### Lokale Integrationen

| Integration | Beschreibung |
|-------------|--------------|
| **MQTT** | Verbindung mit MQTT-Broker |
| **ESPHome** | ESPHome-Geräte automatisch erkannt |
| **Shelly** | WLAN-Geräte von Shelly |
| **Zigbee2MQTT** | Zigbee-Geräte über MQTT |
| **InfluxDB** | Daten exportieren |
| **NodeRED** | Komplexe Automatisierungen |

### Cloud-Integrationen

| Integration | Beschreibung |
|-------------|--------------|
| **Alexa** | Amazon Sprachsteuerung |
| **Google Assistant** | Google Sprachsteuerung |
| **Spotify** | Musik-Steuerung |
| **Weather** | Wetterdaten |

## HACS (Home Assistant Community Store)

HACS ermöglicht das Installieren von Community-Integrationen:

### Installation

Das ei23-Skript installiert HACS automatisch. Manuelle Installation:

1. Lade HACS herunter: [hacs.xyz](https://hacs.xyz/)
2. Kopiere den `hacs` Ordner in `/config/custom_components/`
3. Starte Home Assistant neu
4. Gehe zu **Einstellungen** → **Integrationen** → **HACS**

### Beliebte HACS-Integrationen

| Integration | Beschreibung |
|-------------|--------------|
| **hass-node-red** | NodeRED in HA |
| **Mushroom** | Moderne UI-Karten |
| **Button Card** | Anpassbare Buttons |
| **ApexCharts** | Erweiterte Diagramme |
| **Auto Entities** | Dynamische Listen |

## Automatisierungen

### Beispiel: Licht bei Bewegung

```yaml
automation:
  - alias: "Licht bei Bewegung Flur"
    trigger:
      platform: state
      entity_id: binary_sensor.bewegung_flur
      to: "on"
    condition:
      condition: time
      after: "07:00:00"
      before: "22:00:00"
    action:
      service: light.turn_on
      target:
        entity_id: light.flur
```

### Beispiel: Heizung morgens

```yaml
automation:
  - alias: "Heizung morgens hoch"
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
        entity_id: climate.wohnzimmer
      data:
        temperature: 21
```

## Dashboards

Home Assistant bietet anpassbare Dashboards:

### Lovelace (Standard)

Der Standard-Dashboard kann über die Weboberfläche angepasst werden:

1. Klicke auf die drei Punkte oben rechts
2. **Dashboard anpassen**
3. Füge Karten hinzu:

| Karte | Beschreibung |
|-------|--------------|
| **Entities** | Liste von Geräten |
| **Button** | Einzelner Schalter |
| **Glance** | Schnellübersicht |
| **History** | Verlaufsdiagramm |
| **Weather** | Wettervorhersage |
| **Map** | Standortkarte |

### Custom Dashboards

Mit HACS und Mushroom/CButton Cards kannst du moderne UIs erstellen.

## Backups

### Automatisches Backup

Füge in deine `configuration.yaml` ein:

```yaml
backup:
```

### Manuelles Backup

```bash
# Backup erstellen
cd ~/ei23-docker/
docker compose exec homeassistant tar -czf /config/backup-$(date +%Y%m%d).tar.gz /config
```

### Von Home Assistant OS wechseln

!!!note "Backup von HA OS wiederherstellen"
    Home Assistant OS ist [etwas anders](#home-assistant-docker-vs-supervised-home-assistant) aufgebaut, aber letztlich läuft exakt die selbe Version vom Home Assistant wie in diesem Skript.

1. Erstelle mit Home Assistant OS ein Backup über die Backupfunktion der Weboberfläche
2. Speichere die *.tar Datei
3. Kopiere die Inhalte in diesen Ordner: `/home/user/ei23-docker/volumes/homeassistant/config`
4. Starte Home Assistant neu: `docker restart homeassistant`
5. Das Backup wird eingelesen

## Einbinden von Hardware

### USB-Geräte

Füge Devices in der docker-compose.yml hinzu:

```yaml
devices:
  - /dev/ttyUSB0:/dev/ttyUSB0  # Zigbee-Stick
  - /dev/ttyACM0:/dev/ttyACM0  # ConBee
```

### GPIO (Raspberry Pi)

Für GPIO-Zugriff auf dem Raspberry Pi:

```yaml
devices:
  - /dev/gpiomem:/dev/gpiomem
volumes:
  - /sys:/sys
```

## Home Assistant Docker vs. Supervised

Es gibt zwei Versionen von Home Assistant:

| Feature | Docker (ei23) | Supervised/OS |
|---------|---------------|---------------|
| **Flexibilität** | ✅ Maximum | ⚠️ Eingeschränkt |
| **Docker Images** | ✅ Alle verfügbar | ⚠️ Nur Addons |
| **Addons** | ⚠️ Als separate Container | ✅ Integriert |
| **Hardware** | ⚠️ Manuell konfigurieren | ✅ Automatisch |
| **Updates** | Über docker compose | Über HA Supervisor |

!!!success "Warum Docker?"
    In diesem Skript verwenden wir Home Assistant Docker. Das bietet deutlich mehr Flexibilität und Zugriff auf alle Docker-Images, nicht nur die offiziellen Addons. Technisch gesehen sind Addons auch nur vorkonfigurierte Docker Container.

## HTTPS absichern

Siehe:
- [Reverse Proxy mit Traefik](traefik.md)
- [Reverse Proxy mit Nginx Proxy Manager](nginxproxy.md)

## Hinweise

- Die Konfiguration liegt in `./volumes/homeassistant/config/`
- Die Hauptkonfigurationsdatei ist `configuration.yaml`
- Automatisierungen in `automations.yaml`
- Custom Components in `custom_components/`
- Mindestens 2GB RAM empfohlen

## Weitere Informationen

- [Offizielle Dokumentation](https://www.home-assistant.io/docs/)
- [Home Assistant Community](https://community.home-assistant.io/)
- [GitHub Repository](https://github.com/home-assistant/core)
- [Integrations-Übersicht](https://www.home-assistant.io/integrations/)
