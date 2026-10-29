# Whisper API Proxy

[WhisperAPIProxy](https://github.com/ei23fxg/WhisperAPIProxy) is an OpenAI-compatible proxy for audio transcription. It accepts requests just like the OpenAI Whisper API (`POST /v1/audio/transcriptions`) and uses a local [Whisper-WebUI](https://github.com/jhj0517/Whisper-WebUI) first. If that service is unavailable or returns nothing, local CPU engines take over; OpenAI is only used as the last option and only for clients that are explicitly allowed to use it.

!!!tip "Perfect for Home Assistant Assist"
    With the HACS integration [ha-openai-whisper-stt-api](https://github.com/fabio-garavini/ha-openai-whisper-stt-api) you can use the proxy as the speech-to-text engine in your Assist pipeline. Transcription runs entirely on your server; Home Assistant only has to forward the audio.

## How it works

The proxy uses this fallback chain (the order can be adjusted via `fallback_order`):

```text
Whisper-WebUI (local, GPU recommended)  →  Parakeet (CPU)  →  Whistle (CPU)  →  OpenAI (optional)
```

- **Whisper-WebUI** – fast GPU transcription when the service is reachable at `whisper_webui_host`.
- **Parakeet** – local CPU engine (ONNX), more accurate with numbers and technical terms, about 640 MB.
- **Whistle** – local CPU engine, only about 17 MB, very fast, 7 languages.
- **OpenAI** – only used when `allow_openai = True` is set for the client and an API key is configured.

!!!tip "Local voice control without a GPU"
    Parakeet and Whistle are excellent for CPU execution and do not need a graphics card. This enables local voice control even on simple devices such as mini PCs or thin clients – depending on the hardware, transcription takes a little longer than on a GPU.

Usage is tracked per client in `client_logs/`. Optionally, the proxy stores recordings as Opus files together with their transcripts.

## Requirements

- The proxy runs as a Docker container. You do not need to prepare a `config.py`: if it is missing, the container creates a default configuration from `config.example.py` on first start.
- Optional: a running **Whisper-WebUI** on port `7860` (see the [project link](https://github.com/jhj0517/Whisper-WebUI)). Without it, the proxy keeps working through the CPU engines, just more slowly.
- On first start the proxy downloads the local models in the background (about 660 MB in total). You can trigger this beforehand with `warmup_models.py`.
- `ffmpeg` is already included in the image.

## Installation

### 1. Create directories

```bash
cd ~/ei23-docker

mkdir -p volumes/whisper-proxy/{config,recordings,client_logs,proxy_logs,models/hf,models/cactus}
```

The `config.py` is created automatically in `volumes/whisper-proxy/config/` on first start.

### 2. Add the template and start

Add the template to your [docker-compose.yml](/start/docker-compose/) and start the container with `ei23 dc` (or `docker compose up -d`). Follow the logs with `docker logs -f whisper-api-proxy`.

!!!warning "Adjust the generated configuration"
    The automatically generated `config.py` contains demo clients and placeholder keys. Change them before productive use – at least the API keys in `api_clients`.

### 3. Adjust the configuration

```bash
sudo nano ~/ei23-docker/volumes/whisper-proxy/config/config.py
```

Adjust `whisper_webui_host`, the `api_clients` and optionally the OpenAI key (see [Configuration](#configuration)). Then restart the container:

```bash
cd ~/ei23-docker
docker compose restart whisper-proxy
```

Alternatively, run `ei23 dc`, which restarts all containers.

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

## Configuration

Open `~/ei23-docker/volumes/whisper-proxy/config/config.py` (created automatically on first start) and adjust the important values. You can keep the rest of the file – especially `whisper_predict_config` – unchanged for now.

```python
# Address of the local Whisper-WebUI
whisper_webui_host = "http://192.168.1.10:7860/"

# Local CPU engines as fallback
fallback_order = ["parakeet", "whistle"]
parakeet_enabled = True
whistle_enabled = True
whistle_language = "de"   # None = automatic language detection

# How often the Whisper-WebUI is checked in the background (seconds)
local_check_interval = 30

# OpenAI is only needed if a client has allow_openai = True
openai_api_key = "sk-proj-..."
openai_api_url = "https://api.openai.com/v1/audio/transcriptions"

# Clients: the key is the client ID used in logs and file names
api_clients = {
    "homeassistant": {
        "api_key": "sk-whisper-ha",
        "save_recordings": False,
        "allow_openai": False,
    },
}
```

| Setting | Meaning |
|---------|---------|
| `whisper_webui_host` | URL of the Whisper-WebUI. **Important:** inside the container, `localhost` is the proxy itself – use the server's LAN IP, e.g. `http://192.168.1.10:7860/`. |
| `fallback_order` | Order in which the local engines are tried before OpenAI. |
| `parakeet_enabled` / `whistle_enabled` | Individual engines can be disabled. |
| `whistle_language` | Language for Whistle, e.g. `"de"`. `None` = automatic detection. |
| `local_check_interval` | Check interval for the Whisper-WebUI. Determines how quickly the proxy switches back to the WebUI after an outage. |
| `openai_api_key` | Only required if a client is allowed to use OpenAI. |
| `api_clients` | API keys and permissions per client. `save_recordings` stores the recording and transcript, `allow_openai` permits the paid fallback. |

!!!note "Language"
    The proxy does not evaluate the `language` field sent by the Home Assistant integration. Set the language in the Whisper-WebUI or via `whistle_language` in `config.py`. Parakeet detects the language automatically.

## Models and testing

The models are loaded in the background on first start. You can preload them so the first request does not have to wait:

```bash
docker exec whisper-api-proxy python warmup_models.py
```

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check, no API key required |
| `POST /v1/audio/transcriptions` | Transcription (Bearer API key required) |
| `GET /v1/local_service_status` | Status of Whisper-WebUI, Parakeet and Whistle (API key required) |
| `GET /usage` | Daily usage statistics per client |

### Test it

```bash
# Health check
curl http://192.168.1.10:5431/health

# Transcription
curl http://192.168.1.10:5431/v1/audio/transcriptions \
  -H "Authorization: Bearer sk-whisper-ha" \
  -F "file=@recording.wav" \
  -F "model=whisper-1"
```

The response looks like the OpenAI API:

```json
{"text": "Turn on the living room light, please."}
```

## Integrating into Home Assistant

The **OpenAI Whisper Cloud** integration by [fabio-garavini](https://github.com/fabio-garavini/ha-openai-whisper-stt-api) supports OpenAI, GroqCloud and Mistral as well as any custom OpenAI-compatible endpoint – which is exactly what the Whisper API Proxy provides.

!!!note "Integration, not an add-on"
    This extension is a HACS integration and runs directly inside Home Assistant. That is why it also works with the ei23 Docker installation, which does not use Supervisor add-ons.

### 1. Install the integration

The easiest way is via HACS:

1. **HACS** → three-dot menu in the top right → **Custom repositories**
2. Add `https://github.com/fabio-garavini/ha-openai-whisper-stt-api` with category **Integration**
3. Search for **OpenAI Whisper Cloud** and install it
4. Restart Home Assistant

Alternatively, copy the `custom_components/openai_whisper_cloud` folder from the repository into `~/ei23-docker/volumes/homeassistant/config/custom_components/` and restart HA.

### 2. Set up the integration

1. **Settings** → **Devices & services** → **Add integration**
2. Search for **OpenAI Whisper Cloud**
3. Choose **Custom** as the provider
4. Enter the following values:

| Field | Value |
|-------|-------|
| **Name** | e.g. `Whisper Proxy` |
| **URL** | `http://192.168.1.10:5431` |
| **API key** | the key from `api_clients`, e.g. `sk-whisper-ha` |
| **Model** | `whisper-1` |
| **Temperature** | `0` |
| **Prompt** | leave empty |
| **Streaming upload** | keep enabled |
| **File field** | `file` |

The URL without a path is correct: the integration appends `/v1/audio/transcriptions` automatically. A full endpoint URL is used unchanged – both work.

!!!note "Model name"
    The proxy only uses the model name for the OpenAI fallback. `whisper-1` is the default and always fits.

!!!note "Temperature and prompt"
    The **Temperature** and **Prompt** fields of the integration are not evaluated by the proxy. They only affect providers that support these parameters themselves.

!!!note "Streaming upload"
    The integration uploads audio while it is still being recorded. The proxy processes the completed upload normally afterwards. If this causes problems with your setup, disable **Streaming upload** in the integration options.

### 3. Switch the Assist pipeline

1. **Settings** → **Voice assistants**
2. Select your pipeline (or create a new one)
3. Under **Speech-to-text**, select the newly created `Whisper Proxy` entity
4. Save and test the pipeline

From now on, every voice command from Assist is sent to the proxy. Recognition runs on your server; OpenAI is only contacted if you explicitly allowed it for the client.

!!!tip "Home Assistant on the host network"
    The ei23 HA template uses `network_mode: host`, so `http://127.0.0.1:5431` works as well. The LAN IP is still the more robust choice if you run HA differently later.

## Data and logs

| Path | Content |
|------|---------|
| `volumes/whisper-proxy/config/config.py` | Configuration with API keys and clients (created on first start) |
| `volumes/whisper-proxy/recordings/` | Recordings as `.opus` and transcripts as `.txt` (if `save_recordings` is enabled) |
| `volumes/whisper-proxy/client_logs/` | Usage statistics per client |
| `volumes/whisper-proxy/proxy_logs/error.log` | Proxy error log |
| `volumes/whisper-proxy/models/hf/` | Parakeet model (~640 MB) |
| `volumes/whisper-proxy/models/cactus/` | Whistle model (~17 MB) |

For a backup, `config/config.py`, `client_logs/` and optionally the recordings are enough. The models are downloaded again when needed.

## Notes

- Port `5431` is reachable on all network interfaces. Restrict it within your LAN via firewall and do not expose it to the internet without protection.
- The automatically generated `config.py` contains demo clients and placeholder keys. Change it before productive use.
- The container runs as root; files it creates – including `config/config.py` – will be owned by root afterwards. Edit the file with `sudo` (e.g. `sudo nano ~/ei23-docker/volumes/whisper-proxy/config/config.py`). Alternatively, take over the folder with `sudo chown -R $USER:$USER volumes/whisper-proxy/config`; restart the container afterwards if needed.
- `NEEDLE_TELEMETRY=0` disables telemetry of the Whistle engine.
- Without a GPU, the proxy is still perfectly usable for dictation and Assist; the CPU engines take over automatically.
- The proxy is not a replacement for the Whisper-WebUI but the unified API in front of it. The WebUI can keep running in parallel at `http://[IP]:7860`.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `401 Invalid API Key` | The API key in HA must exactly match an entry in `api_clients` – not the demo key from the template. |
| `500 Transcription failed` | All engines failed. Check `docker logs whisper-api-proxy` and whether the models have been loaded. |
| Connection error while setting up in HA | Is the container running? Test `curl http://[IP]:5431/health`, check the firewall and port. |
| First request takes a long time | The models are loaded once (about 660 MB). Run `warmup_models.py` beforehand. |
| `config.py` is not created | Check that `volumes/whisper-proxy/config/` exists and is writable. The container log shows the path in use after `Config:`. |
| Changes to `config.py` have no effect | Restart the container: `docker compose restart whisper-proxy`. |
| Old `volumes/whisper-proxy/config.py` directory | May be left over from an earlier file mount. Delete it – the template now uses `config/config.py`. |
| Whisper-WebUI is not used | `whisper_webui_host` is set to `localhost`. Inside the container it must point to the server's LAN IP. |
| No recordings | Enable `save_recordings` for the client and check write permissions of the folders. |
| HA reports `connection_error` | Use the URL without a path (`http://[IP]:5431`) and check the key. The proxy has no `/v1/models`; the integration accepts that. |

## Further information

- [WhisperAPIProxy GitHub repository](https://github.com/ei23fxg/WhisperAPIProxy)
- [OpenAI Whisper Cloud GitHub repository (HA)](https://github.com/fabio-garavini/ha-openai-whisper-stt-api)
- [Whisper-WebUI](https://github.com/jhj0517/Whisper-WebUI)
- [Home Assistant Assist](https://www.home-assistant.io/voice_control/)
