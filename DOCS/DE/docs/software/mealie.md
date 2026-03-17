# Mealie

[Mealie](https://mealie.io/) ist ein Rezept-Manager und Mahlzeitenplaner. Es ermöglicht dir, Rezepte zu sammeln, Wochenpläne zu erstellen und automatisch Einkaufslisten zu generieren.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  mealie:
    image: ghcr.io/mealie-recipes/mealie:nightly
    container_name: mealie
    ports:
      - "9925:9000"
    deploy:
      resources:
        limits:
          memory: 1000M
    volumes:
      - ./volumes/mealie-data:/app/data/
    environment:
      - ALLOW_SIGNUP=true
      - PUID=1000
      - PGID=1000
      - MAX_WORKERS=1
      - WEB_CONCURRENCY=1
    restart: always
```

## Hinweise

- Nach dem Start erreichst du Mealie unter `http://[IP]:9925`
- Rezepte können per URL importiert werden (unterstützt viele gängige Kochwebseiten)
- `ALLOW_SIGNUP=true` erlaubt die Registrierung neuer Benutzer - setze auf `false` wenn nur du Zugang haben sollst
- Die Mahlzeitenplanung erstellt automatisch Einkaufslisten

## Weitere Informationen

- [Offizielle Dokumentation](https://docs.mealie.io/)
- [GitHub Repository](https://github.com/mealie-recipes/mealie)
