# Mealie

[Mealie](https://mealie.io/) is a recipe manager and meal planner. It allows you to collect recipes, create weekly plans, and automatically generate shopping lists.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

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

## Notes

- After startup, you can access Mealie at `http://[IP]:9925`
- Recipes can be imported via URL (supports many popular cooking websites)
- `ALLOW_SIGNUP=true` allows registration of new users - set to `false` if only you should have access
- Meal planning automatically creates shopping lists

## Further Information

- [Official Documentation](https://docs.mealie.io/)
- [GitHub Repository](https://github.com/mealie-recipes/mealie)
