# Ollama

[Ollama](https://ollama.ai/) ermöglicht es dir, Large Language Models (LLMs) lokal auf deinem Server laufen zu lassen.

!!!tip "Persönliche Empfehlung: llama-swap"
    Ich persönlich nutze [llama-swap](llama-swap.md) statt Ollama. Es bietet bessere Performance, direkten HuggingFace-Support und feinere Kontrolle über die Modelle. Ollama ist aber einfacher für Einsteiger.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  ollama:
    image: ollama/ollama
    container_name: ollama
    restart: unless-stopped
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_ORIGINS=moz-extension://*'
    ports:
      - 11434:11434
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]
    volumes:
      - ./volumes/ollama:/root/.ollama
```

## Modelle herunterladen

Nach dem Start kannst du Modelle herunterladen:

```bash
# Über das Terminal
docker exec ollama ollama pull llama3
docker exec ollama ollama pull mistral
docker exec ollama ollama pull codellama

# Oder über die API
curl http://localhost:11434/api/pull -d '{"name": "llama3"}'
```

### Empfohlene Modelle

| Modell | Größe | RAM | Beschreibung |
|--------|-------|-----|--------------|
| **llama3** | 4.7GB | 8GB | Allgemeine Aufgaben, guter Kompromiss |
| **llama3:70b** | 40GB | 64GB | Sehr leistungsfähig, braucht viel RAM |
| **mistral** | 4.1GB | 8GB | Gut füreuropäische Sprachen |
| **codellama** | 3.8GB | 8GB | Optimiert für Code-Generierung |
| **phi3** | 2.2GB | 4GB | Kompaktes, effizientes Modell |
| **gemma:2b** | 1.4GB | 2GB | Sehr leicht, für schwache Hardware |

!!!note "GPU-Empfehlung"
    Für schnelle Inferenz ist eine GPU empfohlen. Entkommentiere den `deploy`-Abschnitt für NVIDIA-GPUs.

## Chat-Oberfläche

In Kombination mit **[Open WebUI](open-webui.md)** erhältst du eine bequeme Browser-Oberfläche.

Setze die Umgebungsvariable in Open WebUI:

```yaml
environment:
  - OLLAMA_BASE_URL=http://ollama:11434
```

## Ollama vs. llama-swap

| Feature | Ollama | [llama-swap](llama-swap.md) |
|---------|--------|------------------------------|
| **Einfachheit** | ✅ Sehr einfach | ⚠️ Etwas Konfiguration nötig |
| **Performance** | Gut | ✅ Besser (llama.cpp) |
| **HuggingFace** | ❌ Eigenes Format | ✅ GGUF direkt |
| **Konfiguration** | Eingeschränkt | ✅ Detailliert |
| **Swapping** | Nein | ✅ Automatisch |
| **Modell-Management** | ✅ `ollama pull` | Manuell downloaden |

!!!tip "Empfehlung"
    - **Ollama**: Ideal für Einsteiger, die schnell starten wollen
    - **llama-swap**: Ideal für fortgeschrittene Nutzer, die maximale Performance und Kontrolle wollen

## API

Ollama bietet eine REST-API:

```bash
# Chat-Anfrage senden
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Warum ist der Himmel blau?"
}'

# Verfügbare Modelle auflisten
curl http://localhost:11434/api/tags
```

Die API ist kompatibel mit der OpenAI-API-Schnittstelle und kann mit [n8n](n8n.md), [NodeRED](nodered.md) und anderen Tools verwendet werden.

## Hinweise

- Die Modelle werden in `./volumes/ollama/` gespeichert
- Die API erreichst du unter `http://[IP]:11434`
- Für Home Assistant Integration nutze die Ollama-Integration
- Modelle lassen sich auch über die API herunterladen

## Weitere Informationen

- [Ollama Dokumentation](https://github.com/ollama/ollama)
- [GitHub Repository](https://github.com/ollama/ollama)
- [Verfügbare Modelle](https://ollama.ai/library)
