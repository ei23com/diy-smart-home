#Noch im Aufbau

Ich verweise zunächst auf die [Häufigen Fragen - FAQ](/start/faq)

``` yaml
  uptime-kuma:
    image: louislam/uptime-kuma
    container_name: uptime-kuma
    restart: unless-stopped # (1)
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /etc/timezone:/etc/timezone:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./volumes/uptime-kuma:/app/data

1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be written in Markdown.
```
