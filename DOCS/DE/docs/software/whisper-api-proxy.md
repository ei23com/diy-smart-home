# Whisper API Proxy

[WhisperAPIProxy](https://github.com/ei23fxg/WhisperAPIProxy) ist ein OpenAI-kompatibler Proxy für Audio-Transkription. Er nimmt Anfragen wie die OpenAI Whisper API entgegen (`POST /v1/audio/transcriptions`) und nutzt zuerst eine lokale [Whisper-WebUI](https://github.com/jhj0517/Whisper-WebUI). Ist diese nicht erreichbar oder liefert kein Ergebnis, übernehmen lokale CPU-Engines; OpenAI wird nur als letzte Option und nur für freigegebene Clients verwendet.

!!!tip "Perfekt für Home Assistant Assist"
    Mit der HACS-Integration [ha-openai-whisper-stt-api](https://github.com/fabio-garavini/ha-openai-whisper-stt-api) bindest du den Proxy als Speech-to-Text-Engine in die Assist-Pipeline ein. Die Transkription läuft komplett auf deinem Server, Home Assistant muss nur das Audio weiterreichen.

## Funktionsweise

Der Proxy arbeitet mit dieser Fallback-Kette (Reihenfolge über `fallback_order` anpassbar):

```text
Whisper-WebUI (lokal, idealerweise GPU)  →  Parakeet (CPU)  →  Whistle (CPU)  →  OpenAI (optional)
```

- **Whisper-WebUI** – schnelle Transkription auf der GPU, sofern der Dienst unter `whisper_webui_host` erreichbar ist.
- **Parakeet** – lokale CPU-Engine (ONNX), genauer bei Zahlen und Fachbegriffen, ca. 640 MB.
- **Whistle** – lokale CPU-Engine, nur ca. 17 MB, sehr schnell, 7 Sprachen.
- **OpenAI** – wird nur genutzt, wenn für den Client `allow_openai = True` gesetzt ist und ein API-Key hinterlegt wurde.

!!!tip "Lokale Sprachsteuerung ohne GPU"
    Parakeet und Whistle eignen sich hervorragend für die Ausführung auf der CPU und benötigen keine Grafikkarte. Damit ermöglichen sie lokale Sprachsteuerung auch auf einfachen Geräten wie Mini-PCs oder Thin Clients – je nach Hardware dauert die Transkription etwas länger als auf einer GPU.

Die Nutzung wird pro Client in `client_logs/` statistisch erfasst. Auf Wunsch speichert der Proxy die Aufnahmen als Opus-Datei inklusive Transkript.

## Voraussetzungen

- Der Proxy läuft als Docker-Container. Eine `config.py` musst du nicht vorbereiten: Fehlt sie, erzeugt der Container beim ersten Start automatisch eine Standardkonfiguration aus `config.example.py`.
- Optional: eine laufende **Whisper-WebUI** auf Port `7860` (siehe [Projektlink](https://github.com/jhj0517/Whisper-WebUI)). Ohne sie funktioniert der Proxy über die CPU-Engines weiter, nur langsamer.
- Beim ersten Start lädt der Proxy die lokalen Modelle im Hintergrund (zusammen ca. 660 MB). Mit `warmup_models.py` lässt sich das vorher anstoßen.
- `ffmpeg` ist bereits im Image enthalten.

## Installation

### 1. Ordner anlegen

```bash
cd ~/ei23-docker

mkdir -p volumes/whisper-proxy/{config,recordings,client_logs,proxy_logs,models/hf,models/cactus}
```

Die `config.py` wird beim ersten Start automatisch in `volumes/whisper-proxy/config/` erzeugt.

### 2. Template hinzufügen und starten

Füge das Template in deine [docker-compose.yml](/start/docker-compose/) ein und starte den Container mit `ei23 dc` (oder `docker compose up -d`). Logs verfolgen mit `docker logs -f whisper-api-proxy`.

!!!warning "Erzeugte Konfiguration anpassen"
    Die automatisch erzeugte `config.py` enthält Demo-Clients und Platzhalter-Keys. Ändere sie vor dem produktiven Einsatz – mindestens die API-Keys in `api_clients`.

### 3. Konfiguration anpassen

```bash
sudo nano ~/ei23-docker/volumes/whisper-proxy/config/config.py
```

Passe `whisper_webui_host`, die `api_clients` und optional den OpenAI-Key an (siehe [Konfiguration](#konfiguration)). Danach den Container neu starten:

```bash
cd ~/ei23-docker
docker compose restart whisper-proxy
```

Alternativ kannst du `ei23 dc` ausführen, das startet alle Container neu.

## Template

```yaml
  whisper-proxy:
    image: ghcr.io/ei23fxg/whisperapiproxy
    container_name: whisper-api-proxy
    restart: unless-stopped
    ports:
      - "5431:5431"
    environment:
      NEEDLE_TELEMETRY: "0"
      TZ: Europe/Berlin
      # Directory mount: the container writes config.py itself on first start.
      CONFIG_PATH: /app/config/config.py
    volumes:
      - ./volumes/whisper-proxy/config:/app/config
      - ./volumes/whisper-proxy/recordings:/app/recordings
      - ./volumes/whisper-proxy/client_logs:/app/client_logs
      - ./volumes/whisper-proxy/proxy_logs:/app/logs
      - ./volumes/whisper-proxy/models/hf:/root/.cache/huggingface
      - ./volumes/whisper-proxy/models/cactus:/root/.cache/cactus-needle
```

## Konfiguration

Öffne `~/ei23-docker/volumes/whisper-proxy/config/config.py` (wird beim ersten Start automatisch erzeugt) und passe die wichtigsten Werte an. Den Rest der Datei – insbesondere `whisper_predict_config` – kannst du zunächst unverändert übernehmen.

```python
# Adresse der lokalen Whisper-WebUI
whisper_webui_host = "http://192.168.1.10:7860/"

# Lokale CPU-Engines als Fallback
fallback_order = ["parakeet", "whistle"]
parakeet_enabled = True
whistle_enabled = True
whistle_language = "de"   # None = automatische Spracherkennung

# Wie oft die Whisper-WebUI im Hintergrund geprüft wird (Sekunden)
local_check_interval = 30

# OpenAI nur nötig, wenn ein Client allow_openai = True hat
openai_api_key = "sk-proj-..."
openai_api_url = "https://api.openai.com/v1/audio/transcriptions"

# Clients: der Schlüssel ist die Client-ID für Logs und Dateinamen
api_clients = {
    "homeassistant": {
        "api_key": "sk-whisper-ha",
        "save_recordings": False,
        "allow_openai": False,
    },
}
```

| Einstellung | Bedeutung |
|-------------|-----------|
| `whisper_webui_host` | URL der Whisper-WebUI. **Wichtig:** Im Container ist `localhost` der Proxy selbst – nutze die LAN-IP des Servers, z. B. `http://192.168.1.10:7860/`. |
| `fallback_order` | Reihenfolge der lokalen Engines, bevor OpenAI genutzt wird. |
| `parakeet_enabled` / `whistle_enabled` | Einzelne Engines lassen sich abschalten. |
| `whistle_language` | Sprache für Whistle, z. B. `"de"`. `None` = automatische Erkennung. |
| `local_check_interval` | Prüfintervall der Whisper-WebUI. Bestimmt, wie schnell nach einem Ausfall wieder auf die WebUI umgeschaltet wird. |
| `openai_api_key` | Nur erforderlich, wenn ein Client OpenAI nutzen darf. |
| `api_clients` | API-Keys und Rechte pro Client. `save_recordings` speichert Aufnahme + Transkript, `allow_openai` erlaubt den kostenpflichtigen Fallback. |

!!!note "Sprache"
    Das `language`-Feld der Home-Assistant-Integration wird vom Proxy nicht ausgewertet. Die Sprache stellst du in der Whisper-WebUI bzw. über `whistle_language` in der `config.py` ein. Parakeet erkennt die Sprache automatisch.

## Modelle und Test

Die Modelle werden beim ersten Start im Hintergrund geladen. Du kannst sie vorab laden, damit die erste Anfrage nicht warten muss:

```bash
docker exec whisper-api-proxy python warmup_models.py
```

### Endpunkte

| Endpunkt | Zweck |
|----------|-------|
| `GET /health` | Healthcheck, ohne API-Key |
| `POST /v1/audio/transcriptions` | Transkription (Bearer-API-Key erforderlich) |
| `GET /v1/local_service_status` | Status von Whisper-WebUI, Parakeet und Whistle (API-Key erforderlich) |
| `GET /usage` | Tagesstatistik pro Client |

### Funktion testen

```bash
# Healthcheck
curl http://192.168.1.10:5431/health

# Transkription
curl http://192.168.1.10:5431/v1/audio/transcriptions \
  -H "Authorization: Bearer sk-whisper-ha" \
  -F "file=@aufnahme.wav" \
  -F "model=whisper-1"
```

Die Antwort sieht wie bei der OpenAI-API aus:

```json
{"text": "Schalte bitte das Licht im Wohnzimmer ein."}
```

## In Home Assistant einbinden

Die Integration **OpenAI Whisper Cloud** von [fabio-garavini](https://github.com/fabio-garavini/ha-openai-whisper-stt-api) unterstützt neben OpenAI, GroqCloud und Mistral auch beliebige eigene OpenAI-kompatible Endpunkte – genau dafür ist der Whisper API Proxy gedacht.

!!!note "Integration statt Add-on"
    Die Erweiterung ist eine HACS-Integration und läuft direkt in Home Assistant. Sie funktioniert deshalb auch mit der Docker-Installation von ei23, die keine Supervisor-Add-ons verwendet.

### 1. Integration installieren

Am einfachsten über HACS:

1. **HACS** → oben rechts die drei Punkte → **Benutzerdefinierte Repositories**
2. URL `https://github.com/fabio-garavini/ha-openai-whisper-stt-api` eintragen, Kategorie **Integration**
3. Nach **OpenAI Whisper Cloud** suchen und installieren
4. Home Assistant neu starten

Alternativ den Ordner `custom_components/openai_whisper_cloud` aus dem Repository nach `~/ei23-docker/volumes/homeassistant/config/custom_components/` kopieren und HA neu starten.

### 2. Integration einrichten

1. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
2. Nach **OpenAI Whisper Cloud** suchen
3. Als Anbieter **Custom** wählen
4. Folgende Werte eintragen:

| Feld | Wert |
|------|------|
| **Name** | z. B. `Whisper Proxy` |
| **URL** | `http://192.168.1.10:5431` |
| **API-Key** | der Key aus `api_clients`, z. B. `sk-whisper-ha` |
| **Modell** | `whisper-1` |
| **Temperatur** | `0` |
| **Prompt** | leer lassen |
| **Streaming Upload** | eingeschaltet lassen |
| **File Field** | `file` |

Die URL ohne Pfad ist richtig: Die Integration hängt `/v1/audio/transcriptions` automatisch an. Eine vollständige Endpoint-URL wird dagegen unverändert verwendet – beides funktioniert.

!!!note "Modellname"
    Der Proxy nutzt den Modellnamen nur für den OpenAI-Fallback. `whisper-1` ist der Standardwert und passt immer.

!!!note "Temperatur und Prompt"
    Die Felder **Temperatur** und **Prompt** der Integration werden vom Proxy nicht ausgewertet. Sie wirken sich nur auf Anbieter aus, die diese Parameter selbst unterstützen.

!!!note "Streaming Upload"
    Die Integration lädt das Audio bereits während der Aufnahme hoch. Der Proxy verarbeitet den vollständigen Upload anschließend normal. Falls es mit deinem Setup Probleme gibt, schalte **Streaming Upload** in den Integrationsoptionen aus.

### 3. Assist-Pipeline umstellen

1. **Einstellungen** → **Sprachassistenten**
2. Deine Pipeline auswählen (oder eine neue anlegen)
3. Unter **Speech-to-Text** die gerade angelegte Entität `Whisper Proxy` auswählen
4. Speichern und die Pipeline testen

Ab jetzt geht jede Sprachaufnahme aus Assist an den Proxy. Die Erkennung läuft auf deinem Server; OpenAI wird nur kontaktiert, wenn du es für den Client ausdrücklich erlaubt hast.

!!!tip "Home Assistant im Host-Netzwerk"
    Das HA-Template von ei23 nutzt `network_mode: host`. Damit funktioniert auch `http://127.0.0.1:5431` als URL. Die LAN-IP ist trotzdem die robustere Wahl, falls du HA später anders betreibst.

## Daten und Logs

| Pfad | Inhalt |
|------|--------|
| `volumes/whisper-proxy/config/config.py` | Konfiguration mit API-Keys und Clients (wird beim ersten Start erzeugt) |
| `volumes/whisper-proxy/recordings/` | Aufnahmen als `.opus` und Transkripte als `.txt` (wenn `save_recordings` aktiv) |
| `volumes/whisper-proxy/client_logs/` | Usage-Statistik je Client |
| `volumes/whisper-proxy/proxy_logs/error.log` | Fehler-Log des Proxys |
| `volumes/whisper-proxy/models/hf/` | Parakeet-Modell (~640 MB) |
| `volumes/whisper-proxy/models/cactus/` | Whistle-Modell (~17 MB) |

Für ein Backup reichen `config/config.py`, `client_logs/` und optional die Aufnahmen. Die Modelle werden bei Bedarf erneut heruntergeladen.

## Hinweise

- Der Port `5431` ist auf allen Netzwerk-Schnittstellen erreichbar. Beschränke ihn im LAN per Firewall und exponiere ihn nicht ungeschützt ins Internet.
- Die automatisch erzeugte `config.py` enthält Demo-Clients und Platzhalter-Keys. Passe sie vor dem produktiven Einsatz an.
- Der Container läuft als root; die von ihm erzeugten Dateien – auch `config/config.py` – gehören danach root. Bearbeite die Datei mit `sudo` (z. B. `sudo nano ~/ei23-docker/volumes/whisper-proxy/config/config.py`). Alternativ kannst du den Ordner mit `sudo chown -R $USER:$USER volumes/whisper-proxy/config` übernehmen; danach muss der Container ggf. neu gestartet werden.
- `NEEDLE_TELEMETRY=0` deaktiviert die Telemetrie der Whistle-Engine.
- Ohne GPU ist der Proxy für Diktat und Assist weiterhin gut nutzbar; die CPU-Engines übernehmen dann automatisch.
- Der Proxy ist kein Ersatz für die Whisper-WebUI, sondern die einheitliche API davor. Die WebUI kann parallel unter `http://[IP]:7860` weiterlaufen.

## Fehlerbehebung

| Problem | Lösung |
|---------|--------|
| `401 Invalid API Key` | Der API-Key in HA muss exakt einem Eintrag in `api_clients` entsprechen – nicht der Demo-Key aus der Vorlage. |
| `500 Transcription failed` | Alle Engines sind fehlgeschlagen. Prüfe `docker logs whisper-api-proxy` und ob die Modelle geladen wurden. |
| Verbindungsfehler beim Einrichten in HA | Läuft der Container? `curl http://[IP]:5431/health` testen, Firewall und Port prüfen. |
| Erste Anfrage dauert lange | Die Modelle werden einmalig geladen (ca. 660 MB). Vorher `warmup_models.py` ausführen. |
| `config.py` wird nicht erzeugt | Prüfe, ob `volumes/whisper-proxy/config/` existiert und beschreibbar ist. Im Container-Log steht der verwendete Pfad hinter `Config:`. |
| Änderungen an der `config.py` wirken nicht | Container neu starten: `docker compose restart whisper-proxy`. |
| Altes Verzeichnis `volumes/whisper-proxy/config.py` | Kann von einem früheren Datei-Mount übrig sein. Löschen – das Template nutzt jetzt `config/config.py`. |
| Whisper-WebUI wird nicht genutzt | `whisper_webui_host` steht auf `localhost`. Im Container muss dort die LAN-IP des Servers stehen. |
| Keine Aufnahmen | `save_recordings` für den Client aktivieren und Schreibrechte der Ordner prüfen. |
| HA meldet `connection_error` | URL ohne Pfad verwenden (`http://[IP]:5431`) und den Key prüfen. Der Proxy hat kein `/v1/models`; die Integration akzeptiert das. |

## Weitere Informationen

- [GitHub Repository WhisperAPIProxy](https://github.com/ei23fxg/WhisperAPIProxy)
- [GitHub Repository OpenAI Whisper Cloud (HA)](https://github.com/fabio-garavini/ha-openai-whisper-stt-api)
- [Whisper-WebUI](https://github.com/jhj0517/Whisper-WebUI)
- [Home Assistant Assist](https://www.home-assistant.io/voice_control/)
