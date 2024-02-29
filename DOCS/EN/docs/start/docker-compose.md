## Installing Programs as Containers

Familiarize yourself with editing the [docker-compose.yml/](https://docs.docker.com/compose/compose-file/compose-file-v3/), which you can find at `/home/[user]/ei23-docker/docker-compose.yml`. For editing, you need to be logged in as the "root" user or use a command like `sudo nano /home/[user]/ei23-docker/docker-compose.yml` to gain write permissions.

Templates, or "installation templates," for subsequent installations are available at `/home/pi/ei23-docker/compose_templates`. You can use them and copy them accordingly into the docker-compose.yml.

Once you have adjusted the docker-compose.yml (Caution: incorrect line indentation may result in the installation not being executed correctly), you only need to run `ei23` and then "Docker Compose" or `ei23 dc`.

Depending on the architecture (armv7/arm64/amd64), it may happen that there is no current image of the container. You can check this on [hub.docker.com](https://hub.docker.com/). If necessary, you may have to resort to an older image - in the example below, `:1.24.0` was appended.

It is also possible that a port is already in use. Docker routing works similarly to port forwarding on a regular router. The notation is as follows (also for volumes and devices):

```
Host System:Container
```

You can easily forward any ports - in the example below, `8080` represents the external port, i.e., the port accessible on the computer. The rear port is only accessible internally to Docker. This works similarly for folders, devices, etc., in the host system - very convenient and secure!

Example:

```yaml
  image: nginx:1.24.0
  volumes:
   - ./volumes/nginx:/etc/nginx/templates
  ports:
   - 8080:80
  devices:
   - /dev/video0:/dev/video0
```