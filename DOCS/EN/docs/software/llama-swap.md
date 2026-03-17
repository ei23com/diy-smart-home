# llama-swap

[llama-swap](https://github.com/mostlygeek/llama-swap) is an efficient LLM inference server based on [llama.cpp](https://github.com/ggerganov/llama.cpp). Unlike Ollama, it offers more control over model configuration, supports [HuggingFace](https://huggingface.co/) models directly, and is often significantly more performant.

!!!tip "Recommendation for Linux/AMD64 Users"
    If you are running a Linux server with AMD64 architecture and want maximum performance, **llama-swap** is the better choice over Ollama.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "GPU Required"
    This template is configured for NVIDIA GPUs. Without a GPU, inference will be very slow.

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

## Configuration

Create the configuration file `/home/[user]/ei23-docker/volumes/llama-swap/config.yaml`:

```yaml
# Example configuration for llama-swap
# Documentation: https://github.com/mostlygeek/llama-swap

models:
  # Example: Mistral 7B
  - name: mistral
    model: /models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
    context_length: 8192
    gpu_layers: 99  # All layers on GPU (nvidia)
    
  # Example: Llama 3 8B
  - name: llama3
    model: /models/llama-3-8b-instruct.Q4_K_M.gguf
    context_length: 8192
    gpu_layers: 99

# Swap configuration: Models are loaded/unloaded on demand
swap:
  strategy: timeout
  timeout: 300  # Seconds until an unused model is unloaded
```

### Download Models

Download GGUF models from HuggingFace to the models folder:

```bash
# Create folder
mkdir -p ~/ei23-docker/volumes/llama-swap/models

# Example: Download Qwen3.5-9B Instruct
cd ~/ei23-docker/volumes/llama-swap/models
wget https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/resolve/main/Qwen3.5-9B-UD-Q4_K_XL.gguf?download=true
```

!!!tip "Where to find models?"
    - [Unsloth on HuggingFace](https://huggingface.co/unsloth) - Many quantized models
    - [gguf-my-repo](https://huggingface.co/spaces/ggml-org/gguf-my-repo) - Convert your own model
    - For 8GB VRAM: Q4_K_M quantizations recommended
    - For 4GB VRAM: Q3_K_M or Q2_K quantizations

## Notes

- After startup, the API is available at `http://[IP]:9292`
- The API is compatible with the OpenAI API interface
- **Advantages over Ollama:**
    - Direct support for HuggingFace GGUF models
    - Finer control over context length and GPU layers
    - Lower memory consumption through intelligent swapping
    - Often faster inference
- Combine with [Open WebUI](open-webui.md) for a chat interface
- Port 10008 is reserved for internal purposes

Or configure the connection in the Open WebUI settings under "Connections".

## Further Information

- [GitHub Repository](https://github.com/mostlygeek/llama-swap)
- [llama.cpp Documentation](https://github.com/ggerganov/llama.cpp)
- [HuggingFace](https://huggingface.co/) - Model Repository
