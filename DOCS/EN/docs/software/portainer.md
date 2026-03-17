# Portainer

[Portainer](https://www.portainer.io/) is a graphical management interface for Docker. It allows you to conveniently manage containers, images, volumes, and networks through the browser.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  portainer:
    container_name: portainer
    image: portainer/portainer-ce
    restart: unless-stopped
    ports:
      - "8000:8000"
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./volumes/portainer/data:/data
```

## Notes

- After startup, you can access Portainer at `http://[IP]:9000`
- On first start, you need to create an admin user
- Port 8000 is used for edge agents (optional)
- Portainer is very useful for checking logs, starting/stopping containers, and troubleshooting

## Further Information

- [Official Documentation](https://docs.portainer.io/)
- [GitHub Repository](https://github.com/portainer/portainer)
