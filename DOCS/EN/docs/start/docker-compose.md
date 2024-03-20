# Installing Programs as Containers

Get familiar with editing the [docker-compose.yml](https://docs.docker.com/compose/compose-file/compose-file-v3/). You can find it under `/home/[user]/ei23-docker/docker-compose.yml`.

**I have created a detailed video on this (it's german audio but english subtitles):**
[![YT](https://ei23.de/bilder/YTthumbs/teV-yfBoTuA.webp)](https://www.youtube.com/watch?v=teV-yfBoTuA)

For editing, you need to be logged in as the "root" user, or use something like `sudo nano /home/[user]/ei23-docker/docker-compose.yml` to gain write permissions. Alternatively, you can also edit the file in a web browser using [VSCode](/software/vscode/). There are templates, or "installation templates," available for later installation in `/home/pi/ei23-docker/compose_templates`. You can use them and copy them accordingly into the docker-compose.yml.

After adjusting the docker-compose.yml (Note: incorrect indentation can cause the installation to not execute correctly), you only need to run `ei23` and then "Docker Compose" or `ei23 dc`.

Depending on the architecture (armv7/arm64/amd64), there might not be a current image of the container. You can check this for example on [hub.docker.com](https://hub.docker.com/). If necessary, you may need to revert to an older image - in the example below, `:1.24.0` was appended.

It's also possible that a port is already in use. Docker's routing works similarly to port forwarding on a regular router. The notation is as follows (also for volumes and devices):

```yaml
Host system:Container
```

You can easily forward any ports. In the example below, `8080` represents the external port, the one accessible on the computer. The back port is only accessible internally within Docker. This works similarly for folders, devices, etc., on the host system - very convenient and secure!

Example:
```yaml
  image: nginx:1.24.0
  volumes:
   - ./volumes/nginx:/etc/nginx/templates
  ports:
   - 8080:80 #(1)
  devices:
   - /dev/video0:/dev/video0
```

1.   `8080` is the external port (host) here, and `80` is the internal port (container). Essentially, similar to a router/modem.