# LiteLLM

[LiteLLM](https://litellm.ai/) is a proxy server that unifies various LLM APIs (OpenAI, Anthropic, Ollama, etc.) under a single OpenAI-compatible API. Ideal when you want to manage multiple AI models centrally and provide them through one interface.

!!!tip "For Advanced Users"
    LiteLLM is ideal when you want to use multiple AI providers or local models through a unified API. For most users, [llama-swap](llama-swap.md) or [Ollama](ollama.md) is sufficient for local models.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "Configuration file required"
    Create the file `ei23-docker/volumes/litellm/config.yaml` before starting.

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

## Configuration

Create `/home/[user]/ei23-docker/volumes/litellm/config.yaml`:

```yaml
model_list:
  # Local model via llama-swap/Ollama
  - model_name: local-llama
    litellm_params:
      model: openai/llama3
      api_base: http://llama-swap:8080/v1
      api_key: none

  # OpenAI (if API key available)
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4
      api_key: os.environ/OPENAI_API_KEY

  # Anthropic Claude (if API key available)
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-3-sonnet-20240229
      api_key: os.environ/ANTHROPIC_API_KEY
```

## Usage

The API is compatible with the OpenAI API:

```bash
# Test request
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-llama",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Use Cases

- **Unified API** - One endpoint for all models
- **Fallback** - Automatically switch to next available model
- **Load Balancing** - Distribute requests across multiple instances
- **Cost Tracking** - Monitor API usage and costs

## Notes

- API accessible at `http://[IP]:4000`
- Configuration in `./volumes/litellm/config.yaml`
- Database data in `./volumes/litellm/postgres_data/`
- Compatible with OpenAI API clients

## Further Information

- [GitHub Repository](https://github.com/BerriAI/litellm)
- [Documentation](https://docs.litellm.ai/)
