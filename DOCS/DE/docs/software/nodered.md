# Node-RED

[Node-RED](https://nodered.org/) ist eine visuelle Programmierumgebung für die Verdrahtung von Hardware-Geräten, APIs und Online-Diensten. Es ist das Schweizer Taschenmesser der Automatisierung.

## Installation

Node-RED wird beim ei23-Skript **nativ** installiert (nicht als Docker Container). Dies bietet Vorteile bei der GPIO-Nutzung und der Performance.

!!!note "Bereits vorinstalliert"
    Node-RED wird automatisch mit dem ei23-Skript installiert. Du musst nichts weiter tun!

## Zugriff

Node-RED erreichst du unter `http://[IP]:1880`

## Nodes

Nodes sind die zentralen Komponenten von Node-RED. Sie werden per Drag & Drop auf die Arbeitsfläche gezogen und miteinander verbunden.

### Vorinstallierte Nodes

Das ei23-Skript installiert folgende Nodes automatisch:

| Node | Beschreibung |
|------|--------------|
| **node-red-dashboard** | Web-Dashboard für UI-Elemente |
| **node-red-contrib-home-assistant-websocket** | Home Assistant Integration |
| **node-red-contrib-boolean-logic** | Logische Operationen |
| **node-red-contrib-config** | Konfigurationsknoten |
| **node-red-contrib-counter** | Zähler |
| **node-red-contrib-dwd-local-weather** | Deutscher Wetterdienst |
| **node-red-contrib-eztimer** | Zeitsteuerung |
| **node-red-contrib-influxdb** | InfluxDB Integration |
| **node-red-contrib-looptimer2** | Schleifen-Timer |
| **node-red-contrib-sunpos** | Sonnenposition |
| **node-red-contrib-telegrambot** | Telegram Bot |
| **node-red-contrib-time-range-switch** | Zeitbereich-Schalter |
| **node-red-contrib-timerswitch** | Zeitschalter |
| **node-red-node-email** | E-Mail versenden |
| **node-red-node-ping** | Ping-Test |
| **node-red-node-serialport** | Serielle Schnittstelle |
| **node-red-node-smooth** | Daten glätten |
| **node-red-contrib-postgresql** | PostgreSQL Integration |

### Weitere Nodes installieren

Über die Palette (Hamburger-Menü → Palette verwalten) können weitere Nodes installiert werden.

## Einrichtung

### MQTT Node konfigurieren

1. Ziehe einen **mqtt in** Node auf die Arbeitsfläche
2. Doppelklicke den Node
3. Bei **Server** klicke auf den Stift ✏️
4. Konfiguriere:
    - **Server**: `localhost` oder IP des MQTT-Brokers
    - **Port**: `1883`
    - **Username/Password**: Falls konfiguriert
5. Klicke **Verbinden** → **Fertig**
6. Gib ein **Topic** ein (z.B. `home/temperature/#`)

### Home Assistant Node konfigurieren

1. Ziehe einen **server** Config-Node auf die Arbeitsfläche
2. Oder erstelle ihn über einen HA-Node
3. Konfiguriere:
    - **Base URL**: `http://localhost:8123` (oder IP)
    - **Access Token**: In HA unter Profil → Langzeit-Token erstellen

### Inject Node

Der **Inject** Node triggert Flows manuell oder zeitgesteuert:

- **Einmalig**: Klick auf den Button
- **Zeitgesteuert**: Repeat-Intervall konfigurieren
- **Zeitplan**: Zu bestimmten Uhrzeiten

### Debug Node

Der **Debug** Node zeigt Daten im Debug-Panel:

- Im Sidebar-Reiter "Debug" werden alle Ausgaben angezeigt
- Nützlich zum Testen und Fehler finden

## Flows

### Seiten (Tabs)

Flows können in Seiten organisiert werden:

1. Klicke auf **+** neben dem Tab-Namen
2. Benenne die Seite (z.B. "Heizung", "Licht", "Sensoren")
3. Organisiere deine Nodes thematisch

### Subflows

Subflows sind wiederverwendbare Gruppen von Nodes:

1. Wähle Nodes aus
2. Rechtsklick → **Auswahl in Subflow umwandeln**
3. Der Subflow erscheint als eigener Node im Panel

!!!tip "Subflows sind mächtig"
    Subflows können Parameter haben und werden als einzelner Node dargestellt. Ideal für sich wiederholende Logik.

### Flow-Bibliothek

Flows können in der Bibliothek gespeichert werden:

1. Nodes auswählen
2. Rechtsklick → **Auswahl in Bibliothek speichern**
3. Wiederverwendung über Bibliothek

## Variablen und Kontext

Node-RED bietet drei Kontext-Ebenen:

| Ebene | Gültigkeit | Beispiel |
|-------|------------|----------|
| **Flow** | Innerhalb eines Tabs | `flow.get("counter")` |
| **Global** | Überall | `global.get("lastUpdate")` |
| **Node** | Nur dieser Node | `node.get("state")` |

### Beispiel: Zähler

```javascript
// Counter erhöhen
let count = flow.get("counter") || 0;
count++;
flow.set("counter", count);
msg.payload = count;
return msg;
```

## Dashboard

Das vorinstallierte **node-red-dashboard** bietet eine Weboberfläche für UI-Elemente:

### Zugriff

Das Dashboard erreichst du unter `http://[IP]:1880/ui`

### Verfügbare UI-Elemente

| Element | Beschreibung |
|---------|--------------|
| **ui_button** | Schaltfläche |
| **ui_slider** | Schieberegler |
| **ui_switch** | Schalter |
| **ui_text** | Textanzeige |
| **ui_gauge** | Messinstrument |
| **ui_chart** | Diagramm |
| **ui_dropdown** | Auswahlmenü |
| **ui_text_input** | Texteingabe |

### Konfiguration

1. Doppelklicke ein UI-Element
2. Wähle die **Group** und **Tab**
3. Konfiguriere Größe und Position

## Passwort schützen

### Über das ei23-Skript

```bash
ei23
# Wähle "Neue Passwörter setzen"
```

### Manuell

Editiere `/home/[user]/.node-red/settings.js`:

```javascript
adminAuth: {
    type: "credentials",
    users: [{
        username: "admin",
        password: "$2a$08$...", // bcrypt hash
        permissions: "*"
    }]
}
```

!!!tip "Hash generieren"
    ```bash
    cd ~/.node-red/
    node -e "console.log(require('bcryptjs').hashSync('DEIN_PASSWORT', 8));"
    ```

## Backup

Node-RED Daten werden beim ei23 Backup gesichert. Manuell:

```bash
# Backup
sudo tar -czf ~/nodered_backup.tar.gz ~/.node-red/

# Restore
sudo tar -xzf ~/nodered_backup.tar.gz -C ~/
sudo service nodered restart
```

## Updates

Node-RED wird mit dem ei23-Update aktualisiert:

```bash
ei23 update
```

Oder manuell:

```bash
# Node-RED und Nodes updaten
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) --confirm-install --update-nodes
```

## Home Assistant Integration

Das vorinstallierte **hass-node-red** Addon ermöglicht die Integration in Home Assistant:

1. In Node-RED: Home Assistant Server konfigurieren
2. In Home Assistant: Langzeit-Token erstellen
3. URL: `http://localhost:8123` (wenn HA im Docker)

### Beispiel: Licht bei Bewegung

```
[HA: Bewegung Sensor] → [Switch] → [HA: Licht an]
                         ↓
                    [Delay 5min] → [HA: Licht aus]
```

## Hinweise

- Node-RED läuft auf Port **1880**
- Konfiguration: `/home/[user]/.node-red/settings.js`
- Flows: `/home/[user]/.node-red/flows.json`
- Service: `sudo systemctl status nodered`
- Logs: `journalctl -u nodered -f`

## Weitere Informationen

- [Offizielle Dokumentation](https://nodered.org/docs/)
- [Flow Library](https://flows.nodered.org/)
- [Node-RED Forum](https://discourse.nodered.org/)
- [YouTube Tutorials](https://www.youtube.com/c/NodeRED)
