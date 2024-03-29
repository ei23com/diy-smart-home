# Home Assistant
(Still under construction)

## Switching from Home Assistant OS to Home Assistant Docker using the ei23 script
Home Assistant OS is [somewhat different](/software/homeassistant/#home-assistant-docker-vs-supervised-home-assistant) in structure, but ultimately runs the exact same version of Home Assistant as in my script. To restore a backup from Home Assistant OS to Home Assistant Docker using the ei23 script, follow these steps:

1. Create a backup with Home Assistant OS using the backup function of the web interface.
2. Save the *.tar file. The structure is as follows: `backup.tar\homeassistant.tar.gz\homeassistant.tar\data\`
3. Copy the contents into this folder on my system: `/home/user/ei23-docker/volumes/homeassistant/config`
4. Restart your System or the Home Assistant Docker Container with `docker restart homeassistant`
5. After restarting Home Assistant Docker, the backup will be read, and you should find your familiar system again.

## Home Assistant Docker vs. Supervised Home Assistant

There are two versions of Home Assistant:

1. Home Assistant Docker
2. Supervised Home Assistant (also known as Home Assistant OS)

In this script, we use Home Assistant Docker. While this has disadvantages on one side, it offers significantly more advantages on the other. The "disadvantages" include the absence of "Addons" in the sense of Home Assistant OS and the necessary configuration of hardware via the [docker-compose.yml](/start/docker-compose). It is important to mention that technically, the addons are pre-configured Docker containers. The Supervisor only takes care of part of the configuration. However, this script provides the [docker-compose Templates](/start/docker-compose), which simplify the configuration. 
Moreover, [integrating hardware](#hardware) is not complicated with a few instructions.

A disadvantage of Home Assistant OS is that if an "Addon" is not available for Home Assistant OS, one relies on developers or the community to create one. However, the number of available Docker images is disproportionately larger, which is a major advantage. Additionally, creating custom Docker images or installing native programs on the Linux host operating system is not very difficult. However, installing software on the host system is only recommended to a limited extent.

There is occasionally a misconception that the Docker version of Home Assistant offers fewer capabilities. This is only the case if one does not know how to use them correctly. In fact, Home Assistant OS actively restricts these capabilities for the sake of user-friendliness. Or one could express it in Apple terms: "think different" ;-)

Therefore, we use Home Assistant Docker.

## Integrating Hardware
Partially described in [docker-compose](/start/docker-compose).

## Securing Home Assistant over HTTPS
See [Reverse Proxy with Traefik](/software/traefik) or [Reverse Proxy with Nginx](/software/nginxproxy)