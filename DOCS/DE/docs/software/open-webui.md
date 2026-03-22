# Open WebUI

[Open WebUI](https://openwebui.com/) ist eine benutzerfreundliche Chat-Oberfläche für Large Language Models (LLMs). Sie ist kompatibel mit [Ollama](ollama.md), [llama-swap/llama.cpp](llama-swap.md) und der OpenAI-API.

!!!note "Dies ist NUR die Weboberfläche"
    Open WebUI ist nur eine Benutzeroberfläche. Du benötigst zusätzlich einen LLM-Server wie Ollama oder llama-swap, um Modelle zu laden und Anfragen zu verarbeiten.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "LLM-Server erforderlich"
    Installiere zuerst entweder [Ollama](ollama.md) oder [llama-swap](llama-swap.md).

## Template

```yaml
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: always
    ports:
      - 2280:8080
    environment:
      - OLLAMA_BASE_URL=http://llama-swap:8080  # oder http://ollama:11434
    volumes:
      - ./volumes/open-webui:/app/backend/data
```

## LLM-Server konfigurieren

Je nachdem welchen LLM-Server du nutzst, passe die `OLLAMA_BASE_URL` an:

| LLM-Server | OLLAMA_BASE_URL | Port im Template |
|------------|-----------------|------------------|
| **llama-swap** (empfohlen) | `http://llama-swap:8080` | 9292 |
| Ollama | `http://ollama:11434` | 11434 |

!!!tip "llama-swap empfohlen"
    Für bessere Performance und mehr Flexibilität empfehlen wir [llama-swap](llama-swap.md) anstelle von Ollama.

## Features

- **Chat-Oberfläche** - Moderne, intuitive Benutzeroberfläche
- **Multi-User-Support** - Mehrere Benutzer mit individuellen Einstellungen
- **Chat-Historie** - Gespräche werden gespeichert und durchsuchbar
- **Prompt-Vorlagen** - Wiederverwendbare System-Prompts
- **RAG (Retrieval Augmented Generation)** - Dokumente hochladen und Fragen dazu stellen
- **Modell-Auswahl** - Zwischen verschiedenen Modellen wechseln
- **OpenAI-kompatibel** - Funktioniert mit allen OpenAI-API-kompatiblen Servern

## Erster Start

1. Nach dem Start erreichst du Open WebUI unter `http://[IP]:2280`
2. Erstelle einen Account (der erste Account wird automatisch Admin)
3. Gehe zu den **Einstellungen** → **Verbindungen** und prüfe die LLM-Server URL
4. Wähle ein Modell aus dem Dropdown-Menü und starte zu chatten

!!!note "Modelle müssen vorher heruntergeladen werden"
    Die Modelle werden im jeweiligen LLM-Server (Ollama/llama-swap) heruntergeladen, nicht in Open WebUI.

## Dokumente hochladen (RAG)

Open WebUI unterstützt das Hochladen von Dokumenten, um Fragen mit Kontext aus deinen Dateien zu beantworten:

1. Klicke auf das 📎 Symbol im Chat
2. Lade PDFs, Textdateien oder Markdown-Dateien hoch
3. Stelle Fragen zum Inhalt - die KI nutzt die Dokumente als Kontext

## Hinweise

- Die Daten werden in `./volumes/open-webui/` gespeichert
- Der Port 2280 ist standardmäßig konfiguriert - passe bei Bedarf an
- Open WebUI funktioniert auch mit entfernten Servern (Cloud-GPUs, etc.)
- Für beste RAG-Ergebnisse: Nutze ein Modell mit großer Kontextlänge

## Weitere Informationen

- [Offizielle Website](https://openwebui.com/)
- [GitHub Repository](https://github.com/open-webui/open-webui)
- [Dokumentation](https://docs.openwebui.com/)
