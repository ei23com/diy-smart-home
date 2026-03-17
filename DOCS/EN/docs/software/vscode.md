# VSCode Server

[VSCode Server](https://github.com/coder/code-server) allows you to use Visual Studio Code in the browser. Ideal for editing configuration files, docker-compose.yml, or even programming directly on the server.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  vscode:
    image: codercom/code-server:latest
    container_name: vscode
    restart: unless-stopped
    ports:
      - 8443:8080
    volumes:
      - ./volumes/vscode:/home/coder/project
      - /home:/home:ro  # Optional: Bind home directories
    environment:
      - PASSWORD=YOUR_PASSWORD
      - SUDO_PASSWORD=YOUR_SUDO_PASSWORD
```

!!!warning "Set Password"
    Replace `YOUR_PASSWORD` with a secure password!

## First Start

1. After startup, you can access VSCode at `http://[IP]:8443`
2. Log in with the configured password
3. You now see VSCode in the browser

## Usage

### Edit Configuration Files

Perfect for editing:
- `docker-compose.yml`
- Home Assistant configuration
- Traefik settings
- All other text files

### Bind Home Directories

With the volume mount `/home:/home:ro`, you can view all user directories read-only.

For full access:

```yaml
volumes:
  - ./volumes/vscode:/home/coder/project
  - /home:/home  # Without :ro for full access
```

### Install Extensions

VSCode Server supports extensions:

1. Click on the extensions icon (four squares)
2. Search for and install extensions such as:
    - YAML
    - Docker
    - Git Graph
    - Remote SSH
    - Python

## Tips for the ei23 Setup

| Task | Path |
|------|------|
| Docker Compose | `/home/[user]/ei23-docker/docker-compose.yml` |
| Home Assistant | `/home/[user]/ei23-docker/volumes/homeassistant/config/` |
| Traefik | `/home/[user]/ei23-docker/volumes/traefik/` |
| ei23 Dashboard | `/home/[user]/ei23-docker/volumes/ei23/web/` |

!!!tip "YAML Support"
    Install the YAML extension by Red Hat for autocompletion and validation in docker-compose.yml files.

## Security Notes

- VSCode Server provides full access to the mounted files
- Use a **strong password**
- Use HTTPS with [Traefik](traefik.md) or [Nginx Proxy Manager](nginxproxy.md)
- Port 8443 should **not** be exposed to the internet

## Notes

- Data is stored in `./volumes/vscode/`
- The port is 8443 by default
- VSCode Server runs in the container and does not have direct access to host commands

## Further Information

- [GitHub Repository](https://github.com/coder/code-server)
- [VSCode Documentation](https://code.visualstudio.com/docs)
