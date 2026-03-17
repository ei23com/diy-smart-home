# Das ei23 Dashboard / Der Supervisor

![ei23 Dashboard](https://ei23.de/bilder/dashboard01.jpg)

Das ei23 Dashboard ist mehr als nur eine Anzeige - es ist ein vollwertiger **Server-Supervisor**. Es bietet Live-Monitoring, einen Programme-Editor, Template-Management und Server-Aktionen mit Echtzeit-Terminal-Output.

## Übersicht

Das Dashboard besteht aus vier Hauptseiten:

| Seite | URL | Beschreibung |
|-------|-----|--------------|
| **Dashboard** | `/` | Programme-Übersicht mit Icons |
| **Netzwerk** | `/localnet` | Netzwerk-Scanner |
| **Server** | `/server` | Server-Administration |
| **Speicher** | `/tree` | Ordnergrößen-Analyse |

## Dashboard-Seite (/)

Die Startseite zeigt alle aktiven Programme als Kacheln. Jede Kachel ist verlinkt und kann mit einem Klick geöffnet werden.

## Server-Seite (/server)

Die Server-Seite ist das Herzstück der Administration:

### Live Ressourcen-Anzeige

Oben siehst du in Echtzeit:

- **CPU** - Aktuelle CPU-Auslastung in Prozent
- **RAM** - Belegter und gesamter Arbeitsspeicher
- **Disk** - Belegter und gesamter Festplattenspeicher

Die Balken aktualisieren sich alle 5 Sekunden automatisch.

### Server-Aktionen

Mit einem Klick kannst du wichtige Server-Befehle ausführen:

| Aktion | Beschreibung | Befehl |
|--------|--------------|--------|
| 📊 **Docker Status** | Zeigt alle Container an | `docker ps -a` |
| 🔄 **Docker Compose** | Startet/Restartet alle Container | `ei23 dc` |
| ⬆️ **Docker Update** | Updated alle Docker-Images | `ei23 du` |
| 🧹 **Aufräumen** | Löscht ungenutzte Images | `docker image prune -a -f` |
| 📄 **Docs erzeugen** | Baut die Dokumentation | `ei23 docs` |
| 🏠 **HA Addons** | Updated Home Assistant Addons | `ei23 ha-addons` |
| 📦 **APT Update** | Updated System-Pakete | `apt-get update && upgrade` |
| 🔧 **ei23 Update** | Updated nur das ei23-Skript | `ei23 ei23update` |
| 🚀 **Full Update** | Komplettes System-Update | `ei23 update` |
| ⚡ **Neustart** | Startet den Server neu | `sudo reboot` |

#### Terminal-Output

Nach dem Start einer Aktion öffnet sich ein Terminal-Fenster mit Echtzeit-Output:

- **Auto-Scroll** kann an/ausgeschaltet werden
- Fehlerzeilen werden rot markiert
- Erfolgreiche Zeilen werden grün markiert
- Warnungen werden cyan markiert

#### Session-Badges

Laufende Aktionen zeigen einen animierten Punkt ● neben dem Button. Nach Abschluss wird kurz ✓ (Erfolg) oder ✗ (Fehler) angezeigt.

!!!tip "Aktionen laufen weiter"
    Server-Aktionen laufen auch weiter, wenn du die Seite verlässt. Nach dem Zurückkehren siehst du den aktuellen Status.

### Docker Container

Alle Container aus der docker-compose.yml werden als Karten angezeigt:

| Status | Farbe | Bedeutung |
|--------|-------|-----------|
| **HTTP Available** | 🟢 Grün | Weboberfläche erreichbar |
| **Host Mode** | 🟣 Lila | Host-Netzwerk-Modus |
| **Port Active** | 🔵 Blau | Port ist geöffnet |
| **Internal** | ⚫ Grau | Nur intern erreichbar |

Klicke auf **"Container scannen"** um den Status zu aktualisieren.

### Docker Programme hinzufügen

!!!tip "Neues Feature"
    Programme können jetzt direkt über das Dashboard hinzugefügt werden!

Das Template-Panel ist einklappbar (klicke auf die Überschrift):

1. Klappe das Panel auf
2. Alle verfügbaren Templates werden angezeigt
3. Bereits installierte Templates sind ausgegraut
4. Klicke **"+ Hinzufügen"** um ein Template anzuhängen
5. Führe anschließend **"Docker Compose"** aus um den Container zu starten

!!!warning "Hinweis"
    Duplikate und Port-Konflikte können zu Fehlern führen. Überprüfe die docker-compose.yml bei Bedarf manuell.

### Dashboard-Verknüpfungen bearbeiten

Der Programme-Editor bietet volle Kontrolle über das Dashboard:

#### Programme hinzufügen

1. Klicke auf **"+ Neu"**
2. Fülle die Felder aus:
    - **Name*** (Pflichtfeld)
    - **Titel** (Untertitel)
    - **Port** (z.B. 8080)
    - **Icon** (z.B. `img/nodered.png`)
    - **Eigene URL** (optional, überschreibt Port)
    - **Aktiv** (Sichtbar im Dashboard)
3. Klicke auf **"Hinzufügen"**
4. **"Speichern"** nicht vergessen!

#### Programme bearbeiten

- **Aktiv/Inaktiv**: Schalter umschalten
- **Felder**: Direkt im Formular bearbeiten
- **Sortieren**: Drag & Drop mit ⋮⋮ Handle
- **Löschen**: ✕ Button (mit Bestätigung)

#### Vorlagen importieren

Klicke auf **"Vorlagen"** um fehlende Programme aus `programs_templates.json` hinzuzufügen. Diese werden als inaktiv importiert.

### Erklärung der `programs.json`

Die Datei befindet sich unter `/home/[user]/ei23-docker/volumes/ei23/web/static/programs.json`

```json
{"programs": [
{"active": true,    "port": "",     "custom_url": "http://10.1.1.11:1880",  "name": "NodeRED",          "title": "Garage",              "img": "img/nodered.png"},
{"active": true,    "port": "4004", "custom_url": "",                       "name": "MQTT-Explorer",    "title": "MQTT-Explorer",       "img": "img/mqtt-explorer.png"},
{"active": false,   "port": "",     "custom_url": "http://10.1.1.12",       "name": "Kamera Garten",    "title": "Schöner Garten",      "img": "img/camera.png"},
{"active": true,    "port": "3000", "custom_url": "",                       "name": "Grafana",          "title": "Datenvisualisierung", "img": "img/grafana.png"}
]}
```

1. `"http://10.1.1.11:1880"` ist eine Custom URL - kann auch eine externe Adresse sein
2. Ohne Custom URL wird der Port mit der IP-Adresse kombiniert (z.B. `http://10.1.1.2:4004`)
3. `"active": false` blendet den Eintrag aus
4. Das letzte Element darf kein Komma am Ende haben

## Netzwerk-Seite (/localnet)

![ei23 Dashboard](https://ei23.de/bilder/dashboard02.jpg)

Der Netzwerk-Scanner zeigt alle Geräte im lokalen Netzwerk:

- **Hostname** - Gerätename (wenn auflösbar)
- **IP-Adresse** - Direkt verlinkt wenn Weboberfläche erkannt
- **MAC-Adresse** - Hardware-Adresse
- **Hersteller** - Gerätehersteller

!!!tip "HTTP-Erkennung"
    Wenn ein Gerät Port 80 offen hat, wird es blau markiert und die IP ist direkt verlinkt.

Klicke auf **"Scannen"** um das Netzwerk neu zu scannen.

## Speicher-Seite (/tree)

Zeigt die Speicherbelegung nach Ordnern an - praktisch um große Verzeichnisse zu finden.

## Konfiguration

### Port ändern

Erstelle/Editiere `/home/[user]/ei23-docker/volumes/ei23/config.ini`:

```ini
[DEFAULT]
Port = 80
PeriodicScan = true
```

Dann den Supervisor neustarten:

```bash
sudo systemctl restart ei23.service
```

### Status prüfen

```bash
# Service-Status
sudo systemctl status ei23.service

# Logs anzeigen
journalctl -u ei23.service -f
```

## Hinweise

- Das Dashboard läuft als Python-Flask-Server mit Waitress
- Der Service startet automatisch beim Boot (`ei23.service`)
- Das Dashboard erreichst du über Port 80 (konfigurierbar)
- Programme-Icons liegen unter `/home/[user]/ei23-docker/volumes/ei23/web/static/img/`
- Eigene Icons: 128x128 PNG mit transparentem Hintergrund
