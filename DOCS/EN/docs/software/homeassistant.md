# Home Assistant
(Still under construction)

## Home Assistant Docker vs. Supervised Home Assistant
There are two versions of Home Assistant:<br>
1. Home Assistant Docker<br>
2. Supervised Home Assistant (also known as Home Assistant OS)<br>

In this script, we use Home Assistant Docker. While it has drawbacks on one side, it offers significantly more advantages on the other. The "drawbacks" include the absence of "Addons" in the Home Assistant OS sense and the necessary configuration of hardware via the [docker-compose.yml](/start/docker-compose). It's important to mention that technically, the Addons are pre-configured Docker containers. The Supervisor only takes care of part of the configuration. However, this script provides [docker-compose templates](/start/docker-compose) that simplify the configuration.
Moreover, [integrating hardware](#hardware) is not complicated with a few instructions.

A disadvantage of Home Assistant OS is that if an "Addon" is not available for Home Assistant OS, one relies on developers or the community to create it. The number of available Docker images, on the other hand, is disproportionately larger, which is a significant advantage. Additionally, creating custom Docker images or installing native programs on the Linux host operating system is not very difficult. However, installing software on the host system is only recommended to a limited extent.

There is occasionally a misunderstanding that the Docker version of Home Assistant offers fewer possibilities. This is only the case if one doesn't know how to use them properly. In fact, Home Assistant OS actively restricts these possibilities for user-friendliness reasons. Or, as one might express it with Apple: "think different" ;-)

That's why we use Home Assistant Docker.

## Integrating Hardware
Partly described in [docker-compose](/start/docker-compose).

## Securing Home Assistant over HTTPS
See Reverse Proxy with Traefik or Nginx - [Reverse Proxy with Traefik](/software/traefik) [Reverse Proxy with Nginx](/software/nginxproxy)