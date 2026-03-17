# Ollama

[Ollama](https://ollama.ai/) allows you to run Large Language Models (LLMs) locally on your server.

!!!tip "Personal Recommendation: llama-swap"
    I personally use [llama-swap](llama-swap.md) instead of Ollama. It offers better performance, direct HuggingFace support, and finer control over models. However, Ollama is easier for beginners.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

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

## Download Models

After startup, you can download models:

```bash
# Via terminal
docker exec ollama ollama pull llama3
docker exec ollama ollama pull mistral
docker exec ollama ollama pull codellama

# Or via API
curl http://localhost:11434/api/pull -d '{"name": "llama3"}'
```

### Recommended Models

| Model | Size | RAM | Description |
|-------|------|-----|-------------|
| **llama3** | 4.7GB | 8GB | General tasks, good compromise |
| **llama3:70b** | 40GB | 64GB | Very powerful, needs lots of RAM |
| **mistral** | 4.1GB | 8GB | Good for European languages |
| **codellama** | 3.8GB | 8GB | Optimized for code generation |
| **phi3** | 2.2GB | 4GB | Compact, efficient model |
| **gemma:2b** | 1.4GB | 2GB | Very lightweight, for weak hardware |

!!!note "GPU Recommendation"
    A GPU is recommended for fast inference. Uncomment the `deploy` section for NVIDIA GPUs.

## Chat Interface

In combination with **[Open WebUI](open-webui.md)**, you get a convenient browser interface.

Set the environment variable in Open WebUI:

```yaml
environment:
  - OLLAMA_BASE_URL=http://ollama:11434
```

## Ollama vs. llama-swap

| Feature | Ollama | [llama-swap](llama-swap.md) |
|---------|--------|------------------------------|
| **Simplicity** | ✅ Very easy | ⚠️ Some configuration needed |
| **Performance** | Good | ✅ Better (llama.cpp) |
| **HuggingFace** | ❌ Own format | ✅ GGUF directly |
| **Configuration** | Limited | ✅ Detailed |
| **Swapping** | No | ✅ Automatic |
| **Model Management** | ✅ `ollama pull` | Manual download |

!!!tip "Recommendation"
    - **Ollama**: Ideal for beginners who want to start quickly
    - **llama-swap**: Ideal for advanced users who want maximum performance and control

## API

Ollama provides a REST API:

```bash
# Send chat request
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'

# List available models
curl http://localhost:11434/api/tags
```

The API is compatible with the OpenAI API interface and can be used with [n8n](n8n.md), [NodeRED](nodered.md), and other tools.

## Notes

- Models are stored in `./volumes/ollama/`
- The API is available at `http://[IP]:11434`
- For Home Assistant integration, use the Ollama integration
- Models can also be downloaded via the API

## Further Information

- [Ollama Documentation](https://github.com/ollama/ollama)
- [GitHub Repository](https://github.com/ollama/ollama)
- [Available Models](https://ollama.ai/library)
