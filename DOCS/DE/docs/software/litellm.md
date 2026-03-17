# LiteLLM

[LiteLLM](https://litellm.ai/) ist ein Proxy-Server, der verschiedene LLM-APIs (OpenAI, Anthropic, Ollama, etc.) unter einer einheitlichen OpenAI-kompatiblen API zusammenfasst. Ideal wenn du mehrere KI-Modelle zentral verwalten und über eine einzige Schnittstelle bereitstellen möchtest.

!!!tip "Für Fortgeschrittene"
    LiteLLM ist ideal, wenn du mehrere KI-Anbieter oder lokale Modelle über eine einheitliche API nutzen möchtest. Für die meisten Nutzer reicht [llama-swap](llama-swap.md) oder [Ollama](ollama.md) für lokale Modelle.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Konfigurationsdatei erforderlich"
    Erstelle die Datei `ei23-docker/volumes/litellm/config.yaml` vor dem Start.

## Template

```yaml
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: litellm
    restart: always
    ports:
      - "4000:4000"
    volumes:
      - ./volumes/litellm/config.yaml:/app/config.yaml
    environment:
        DATABASE_URL: "postgresql://llmproxy:dbpassword9090@litellm-db:5432/litellm"
        STORE_MODEL_IN_DB: "True"
    command: --config /app/config.yaml --detailed_debug
    depends_on:
      - litellm-db

  litellm-db:
    image: postgres:16
    container_name: litellm-db
    restart: always
    environment:
      POSTGRES_DB: litellm
      POSTGRES_USER: llmproxy
      POSTGRES_PASSWORD: dbpassword9090
    volumes:
      - ./volumes/litellm/postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -d litellm -U llmproxy"]
      interval: 1s
      timeout: 5s
      retries: 10
```

## Konfiguration

Erstelle `/home/[user]/ei23-docker/volumes/litellm/config.yaml`:

```yaml
model_list:
  # Lokales Modell über llama-swap/Ollama
  - model_name: local-llama
    litellm_params:
      model: openai/llama3
      api_base: http://llama-swap:8080/v1
      api_key: none

  # OpenAI (falls API-Key vorhanden)
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4
      api_key: os.environ/OPENAI_API_KEY

  # Anthropic Claude (falls API-Key vorhanden)
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-3-sonnet-20240229
      api_key: os.environ/ANTHROPIC_API_KEY
```

## Verwendung

Die API ist kompatibel mit der OpenAI-API:

```bash
# Test-Anfrage
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-llama",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Anwendungsfälle

- **Einheitliche API** - Ein Endpunkt für alle Modelle
- **Fallback** - Automatisch zum nächsten verfügbaren Modell
- **Load Balancing** - Verteile Anfragen auf mehrere Instanzen
- **Kosten-Tracking** - Überwache API-Nutzung und Kosten

## Hinweise

- Die API erreichst du unter `http://[IP]:4000`
- Die Konfiguration liegt in `./volumes/litellm/config.yaml`
- Datenbank-Daten in `./volumes/litellm/postgres_data/`
- Kompatibel mit OpenAI-API-Clients

## Weitere Informationen

- [GitHub Repository](https://github.com/BerriAI/litellm)
- [Dokumentation](https://docs.litellm.ai/)
