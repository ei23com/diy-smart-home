# Open WebUI

[Open WebUI](https://openwebui.com/) is a user-friendly chat interface for Large Language Models (LLMs). It is compatible with [Ollama](ollama.md), [llama-swap](llama-swap.md), and the OpenAI API.

!!!note "This is ONLY the Web Interface"
    Open WebUI is just a user interface. You additionally need an LLM server like Ollama or llama-swap to load models and process requests.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "LLM Server Required"
    First install either [Ollama](ollama.md) or [llama-swap](llama-swap.md).

## Template

```yaml
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: always
    ports:
      - 2280:8080
    environment:
      - OLLAMA_BASE_URL=http://llama-swap:8080  # or http://ollama:11434
    volumes:
      - ./volumes/open-webui:/app/backend/data
```

## Configure LLM Server

Depending on which LLM server you use, adjust the `OLLAMA_BASE_URL`:

| LLM Server | OLLAMA_BASE_URL | Port in Template |
|------------|-----------------|------------------|
| **llama-swap** (recommended) | `http://llama-swap:8080` | 9292 |
| Ollama | `http://ollama:11434` | 11434 |

!!!tip "llama-swap Recommended"
    For better performance and more flexibility, we recommend [llama-swap](llama-swap.md) over Ollama.

## Features

- **Chat Interface** - Modern, intuitive user interface
- **Multi-User Support** - Multiple users with individual settings
- **Chat History** - Conversations are saved and searchable
- **Prompt Templates** - Reusable system prompts
- **RAG (Retrieval Augmented Generation)** - Upload documents and ask questions about them
- **Model Selection** - Switch between different models
- **OpenAI Compatible** - Works with all OpenAI API-compatible servers

## First Start

1. After startup, you can access Open WebUI at `http://[IP]:2280`
2. Create an account (the first account automatically becomes admin)
3. Go to **Settings** → **Connections** and check the LLM server URL
4. Select a model from the dropdown menu and start chatting

!!!note "Models Must Be Downloaded First"
    Models are downloaded in the respective LLM server (Ollama/llama-swap), not in Open WebUI.

## Upload Documents (RAG)

Open WebUI supports uploading documents to answer questions with context from your files:

1. Click the 📎 icon in the chat
2. Upload PDFs, text files, or Markdown files
3. Ask questions about the content - the AI uses the documents as context

## Notes

- Data is stored in `./volumes/open-webui/`
- Port 2280 is configured by default - adjust if needed
- Open WebUI also works with remote servers (cloud GPUs, etc.)
- For best RAG results: Use a model with a large context length

## Further Information

- [Official Website](https://openwebui.com/)
- [GitHub Repository](https://github.com/open-webui/open-webui)
- [Documentation](https://docs.openwebui.com/)
