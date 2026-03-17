# llama-swap

[llama-swap](https://github.com/mostlygeek/llama-swap) ist ein effizienter LLM-Inference-Server auf Basis von [llama.cpp](https://github.com/ggerganov/llama.cpp). Im Gegensatz zu Ollama bietet es mehr Kontrolle über die Modellkonfiguration, unterstützt [HuggingFace](https://huggingface.co/) Modelle direkt und ist oft deutlich performanter.

!!!tip "Empfehlung für Linux/AMD64 Nutzer"
    Wenn du auf einem Linux-Server mit AMD64-Architektur betreibst und maximale Performance möchtest, ist **llama-swap** die bessere Wahl gegenüber Ollama.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "GPU erforderlich"
    Dieses Template ist für NVIDIA-GPUs konfiguriert. Ohne GPU wird die Inferenz sehr langsam sein.

## Template

```yaml
  llama-swap:
    image: ghcr.io/mostlygeek/llama-swap:cuda
    container_name: llama-swap
    restart: unless-stopped
    ports:
      - 9292:8080
      - 10008:10008
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ./volumes/llama-swap/config.yaml:/app/config.yaml
      - ./volumes/llama-swap/models:/models:ro
```

## Konfiguration

Erstelle die Konfigurationsdatei `/home/[user]/ei23-docker/volumes/llama-swap/config.yaml`:

```yaml
# Beispiel Konfiguration für llama-swap
# Dokumentation: https://github.com/mostlygeek/llama-swap

models:
  # Beispiel: Mistral 7B
  - name: mistral
    model: /models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
    context_length: 8192
    gpu_layers: 99  # Alle Layer auf GPU (nvidia)
    
  # Beispiel: Llama 3 8B
  - name: llama3
    model: /models/llama-3-8b-instruct.Q4_K_M.gguf
    context_length: 8192
    gpu_layers: 99

# Swap-Konfiguration: Modelle werden bei Bedarf geladen/entladen
swap:
  strategy: timeout
  timeout: 300  # Sekunden bis zum Entladen eines ungenutzten Modells
```

### Modelle herunterladen

Lade GGUF-Modelle von HuggingFace in den models-Ordner:

```bash
# Ordner erstellen
mkdir -p ~/ei23-docker/volumes/llama-swap/models

# Beispiel: Qwen3.5-9B Instruct herunterladen
cd ~/ei23-docker/volumes/llama-swap/models
wget https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/resolve/main/Qwen3.5-9B-UD-Q4_K_XL.gguf?download=true
```

!!!tip "Wo finde ich Modelle?"
    - [Unsloth auf HuggingFace](https://huggingface.co/unsloth) - Viele quantisierte Modelle
    - [gguf-my-repo](https://huggingface.co/spaces/ggml-org/gguf-my-repo) - Eigenes Model konvertieren
    - Für 8GB VRAM: Q4_K_M Quantisierungen empfohlen
    - Für 4GB VRAM: Q3_K_M oder Q2_K Quantisierungen

## Hinweise

- Nach dem Start erreichst du die API unter `http://[IP]:9292`
- Die API ist kompatibel mit der OpenAI-API-Schnittstelle
- **Vorteile gegenüber Ollama:**
    - Direkte Unterstützung von HuggingFace GGUF-Modellen
    - Feinere Kontrolle über Kontextlänge und GPU-Layer
    - Geringerer Speicherverbrauch durch intelligentes Swapping
    - Oft schnellere Inferenz
- Kombiniere mit [Open WebUI](open-webui.md) für eine Chat-Oberfläche
- Die 10008 Port ist für interne Zwecke reserviert
Oder konfiguriere die Verbindung in den Open WebUI Einstellungen unter "Verbindungen".

## Weitere Informationen

- [GitHub Repository](https://github.com/mostlygeek/llama-swap)
- [llama.cpp Dokumentation](https://github.com/ggerganov/llama.cpp)
- [HuggingFace](https://huggingface.co/) - Modell-Repository
