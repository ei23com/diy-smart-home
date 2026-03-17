# Uptime Kuma

[Uptime Kuma](https://uptime.kuma.pet/) is a modern, self-hosted monitoring tool. It monitors your services and sends notifications on outages.

[![YT](https://ei23.de/bilder/YTthumbs/Nr-re1kszvk.webp)](https://www.youtube.com/watch?v=Nr-re1kszvk)

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

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

## First Start

1. After startup, you can access Uptime Kuma at `http://[IP]:3001`
2. Create an admin account on first start
3. Add your first monitors

## Monitor Types

Uptime Kuma supports many different monitor types:

| Type | Description | Example |
|------|-------------|---------|
| **HTTP(s)** | Monitor websites | `https://ei23.de` |
| **TCP** | Port monitoring | `192.168.1.1:22` |
| **Ping** | Host reachability | `192.168.1.1` |
| **DNS** | Check DNS resolution | `ei23.de` |
| **Docker** | Container status | Container names |
| **Push** | Receives heartbeats | Custom URL |
| **Keyword** | Search webpage for word | "Welcome" |

## Set Up Notifications

Uptime Kuma supports over 90 notification services:

### Telegram

1. Create a bot with [@BotFather](https://t.me/BotFather)
2. Copy the bot token
3. Find your chat ID with [@userinfobot](https://t.me/userinfobot)
4. In Uptime Kuma: **Settings** → **Notifications** → **Telegram**

### Discord

1. Go to **Server Settings** → **Integrations** → **Webhooks**
2. Create a new webhook
3. Copy the webhook URL
4. In Uptime Kuma: **Settings** → **Notifications** → **Discord**

### More Options

- Email (SMTP)
- Pushover
- Gotify
- Signal
- Slack
- Matrix
- Ntfy
- and many more...

## Dashboard

Uptime Kuma offers a public status dashboard:

1. Go to **Settings** → **Status Pages**
2. Create a new status page
3. Add monitors
4. Share the URL with your users

## Monitor Docker Containers

How to monitor the status of your Docker containers:

1. Bind the Docker socket (optional):

```yaml
volumes:
  - ./volumes/uptime-kuma:/app/data
  - /var/run/docker.sock:/var/run/docker.sock:ro
```

2. When creating a monitor, select **Docker** as the type
3. Enter the container name

## Notes

- Data is stored in `./volumes/uptime-kuma/`
- The port is 3001 by default
- Uptime Kuma is very resource-efficient
- Ideal for monitoring all ei23 services

## Further Information

- [Official Documentation](https://uptime.kuma.pet/)
- [GitHub Repository](https://github.com/louislam/uptime-kuma)
- [Demo](https://demo.uptime.kuma.pet/)
