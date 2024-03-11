#Noch im Aufbau

Ich verweise zunächst auf die [Häufigen Fragen - FAQ](/start/faq)


```php
<?php echo "hallo"; ?> # (1)
```

2. okokok

<?php echo "hallo";?>
hallo2

``` { .yaml .annotate .select}
uptime-kuma:
  image: louislam/uptime-kuma
  container_name: uptime-kuma
  restart: unless-stopped # (1)
  volumes:
    - /etc/localtime:/etc/localtime:ro
    - /etc/timezone:/etc/timezone:ro
    - /var/run/docker.sock:/var/run/docker.sock:ro
    - ./volumes/uptime-kuma:/app/data

```

1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be written in Markdown.

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

```

1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be written in Markdown.

``` yaml
theme:
  features:
    - content.code.annotate # (1)
```

1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be written in Markdown.

``` yaml
theme:
  features:
    - content.code.annotate # (1)
    - content.code.yaaa
```

1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be written in Markdown.

Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.
{ .annotate }

1.  irgendwas