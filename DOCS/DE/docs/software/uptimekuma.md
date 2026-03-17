# Uptime Kuma

[Uptime Kuma](https://uptime.kuma.pet/) ist ein modernes, selbstehostes Monitoring-Tool. Es überwacht deine Dienste und sendet Benachrichtigungen bei Ausfällen.

[![YT](https://ei23.de/bilder/YTthumbs/Nr-re1kszvk.webp)](https://www.youtube.com/watch?v=Nr-re1kszvk)

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - 3001:3001
    volumes:
      - ./volumes/uptime-kuma:/app/data
```

## Erster Start

1. Nach dem Start erreichst du Uptime Kuma unter `http://[IP]:3001`
2. Erstelle beim ersten Start einen Admin-Account
3. Füge deine ersten Monitore hinzu

## Monitor-Typen

Uptime Kuma unterstützt viele verschiedene Monitor-Typen:

| Typ | Beschreibung | Beispiel |
|-----|--------------|----------|
| **HTTP(s)** | Webseiten überwachen | `https://ei23.de` |
| **TCP** | Port-Überwachung | `192.168.1.1:22` |
| **Ping** | Host-Erreichbarkeit | `192.168.1.1` |
| **DNS** | DNS-Auflösung prüfen | `ei23.de` |
| **Docker** | Container-Status | Container-Namen |
| **Push** | Empfängt Heartbeats | Eigene URL |
| **Keyword** | Webseite nach Wort durchsuchen | "Willkommen" |

## Benachrichtigungen einrichten

Uptime Kuma unterstützt über 90 Benachrichtigungsdienste:

### Telegram

1. Erstelle einen Bot mit [@BotFather](https://t.me/BotFather)
2. Kopiere den Bot-Token
3. Finde deine Chat-ID mit [@userinfobot](https://t.me/userinfobot)
4. In Uptime Kuma: **Settings** → **Notifications** → **Telegram**

### Discord

1. Gehe zu **Server-Einstellungen** → **Integrationen** → **Webhooks**
2. Erstelle einen neuen Webhook
3. Kopiere die Webhook-URL
4. In Uptime Kuma: **Settings** → **Notifications** → **Discord**

### Weitere Optionen

- Email (SMTP)
- Pushover
- Gotify
- Signal
- Slack
- Matrix
- Ntfy
- und viele mehr...

## Dashboard

Uptime Kuma bietet ein öffentliches Status-Dashboard:

1. Gehe zu **Settings** → **Status Pages**
2. Erstelle eine neue Status-Seite
3. Füge Monitore hinzu
4. Teile die URL mit deinen Nutzern

## Docker-Container überwachen

So überwachst du den Status deiner Docker-Container:

1. Binde den Docker-Socket ein (optional):

```yaml
volumes:
  - ./volumes/uptime-kuma:/app/data
  - /var/run/docker.sock:/var/run/docker.sock:ro
```

2. Wähle beim Erstellen eines Monitors **Docker** als Typ
3. Gib den Container-Namen ein

## Hinweise

- Die Daten werden in `./volumes/uptime-kuma/` gespeichert
- Der Port ist standardmäßig 3001
- Uptime Kuma ist sehr ressourcenschonend
- Ideal für die Überwachung aller ei23-Dienste

## Weitere Informationen

- [Offizielle Dokumentation](https://uptime.kuma.pet/)
- [GitHub Repository](https://github.com/louislam/uptime-kuma)
- [Demo](https://demo.uptime.kuma.pet/)
