# Internet Access to Home Services: Traefik and SSL Certificates

There are various ways to reach web services running at home from the internet. The least secure method involves port forwarding with unencrypted protocols like HTTP or FTP. <em>Avoid using simple port forwarding for HTTP or FTP!</em> A more secure option is SFTP and/or a VPN, both requiring certificates for client authorization and encrypted data transmission.

For easy setup, especially for Docker containers, consider using [WG-Easy](https://github.com/wg-easy/wg-easy) or [PiVPN](https://www.pivpn.io/) to install WireGuard or OpenVPN. Check out the [video tutorial](https://www.youtube.com/watch?v=QwC5ndEIMZs) demonstrating this on the ei23 Smart Home Server.

**VPN Doesn't Solve Everything**

But what if numerous clients need access, or we don't want to provide certificates to each user? What if a service requires more resources than a small Raspberry Pi can provide? This is where reverse proxies and SSL certificates come in.

A reverse proxy can route traffic based on domains or subdomains, deciding which content to make accessible to users. Additionally, it can encrypt the content with SSL. This allows hiding an IP behind multiple domains while accessing several services.

![Traefik Architecture](https://ei23.de/wp-content/uploads/sites/4/2021/04/traefik-architecture-1024x535.png)

*Traefik Architecture (Source: [traefik.io](https://traefik.io))*

While other solutions like Nginx exist, we use Traefik for the [ei23 Smart Home Server](https://ei23.de/diy-smarthome) due to its advantages for Docker programs and its user-friendly visual interface.

## Docker Container Proxy Configuration with Traefik

To configure a Docker container for Traefik, modify the `/home/pi/ei23-docker/docker-compose.yaml`. For details, refer to [Smart Home Script Version 1 Video](https://www.youtube.com/watch?v=QKjSvH40Pic).

**Example docker-compose Bitwarden**
```yaml
bitwarden:
  image: bitwardenrs/server:latest
  container_name: bitwarden
  restart: unless-stopped
  # ports:
  #   - 2223:80
  labels:
    - traefik.enable=true
    - traefik.http.routers.bitwarden.rule=Host(`example.com`)
    - traefik.http.routers.bitwarden.entrypoints=web-secured
    - traefik.http.routers.bitwarden.tls=true
    - traefik.http.routers.bitwarden.tls.certresolver=letsEncrypt
  volumes:
    - ./volumes/bitwarden:/data
```
With Traefik, it's not mandatory to expose *ports via Docker as long as Traefik is in the same Docker network as the containers, as shown in the example above (ports are commented with #).

**Example: LAN Website (in this case, the ei23 Dashboard)**
```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.ei23-lan.rule=(Host(`192.168.178.10`) || Host(`smarthome`))
  - traefik.http.routers.ei23-lan.priority=1
  - traefik.http.routers.ei23-lan.entrypoints=lan
```
**Example docker-compose Grafana**
```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.grafana.rule=Host(`grafana.example.com`)
  - traefik.http.services.grafana.loadbalancer.server.port=3000
  - traefik.http.routers.grafana.entrypoints=web-secured
  - traefik.http.routers.grafana.tls=true
  - traefik.http.routers.grafana.tls.certresolver=letsEncrypt
```
**Example docker-compose Nextcloud**
```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.nextcloud.middlewares=nextcloud,nextcloud_redirect
  - traefik.http.routers.nextcloud.tls.certresolver=letsEncrypt
  - traefik.http.routers.nextcloud.rule=Host(`nextcloud.example.com`)
  - traefik.http.routers.nextcloud.entrypoints=web, web-secured
  - traefik.http.routers.nextcloud.tls=true
  - traefik.http.middlewares.nextcloud.headers.stsSeconds=15552000
  - traefik.http.middlewares.nextcloud.headers.stsPreload=true
  - traefik.http.middlewares.nextcloud_redirect.redirectregex.permanent=true
  - traefik.http.middlewares.nextcloud_redirect.redirectregex.regex=^https://(.*)/.well-known/(card|cal)dav
  - traefik.http.middlewares.nextcloud_redirect.redirectregex.replacement=https://$${1}/remote.php/dav/
```

Traefik uses "Routers, Services, and Middlewares" for each service, requiring at least one Traefik Router.

## Load Balancers / External (IP) Addresses and Devices in the Network

In `/home/pi/ei23-docker/volumes/traefik/traefik/dynamic/config.yml`, an external "Loadbalancer" is created for Home Assistant since it runs outside the Docker network. (Note: Correct indentation is crucial - the Yaml Parser expects it.)

```yaml
http:
  routers:
    home-assistant:
      rule: Host(`homeassistant.example.com`)
      service: home-assistant
      tls:
        certresolver: letsEncrypt
        
  services:
    home-assistant:
      loadBalancer:
        servers:
          - url: http://172.17.0.1:8123
```

This points to an HTTP URL instead of a Docker container. The URL is then encrypted using the "certresolver."

## Traefik Setup / Creating SSL Certificates

Traefik itself runs as a Docker container. In the current version of the ei23 Smart Home Server, Traefik is pre-configured, requiring only minor adjustments.

Docker-Compose for Traefik

```yaml
traefik:
  image: traefik:v2.4
  container_name: traefik
  ports:
    - "80:80" # as internal http
    - "591:591" # as external http
    - "2280:8080" # config port
    - "443:443"
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
    - ./volumes/traefik/traefik/:/etc/traefik/
    - ./volumes/traefik/letsencrypt:/letsencrypt
  restart: unless-stopped
```

In `/home/pi/ei23-docker/volumes/traefik/traefik/traefik.yaml`:

```yaml

entryPoints:
  lan:
    address: :80
  web:
    address: :591
    http:
      redirections:
        entrypoint:
          to: web-secured
          scheme: https
 

 web-secured:
    address: :443

certificatesResolvers:
  letsEncrypt:
    acme:
      email: mail@example.com
      storage: /letsencrypt/acme.json
      caserver: https://acme-staging-v02.api.letsencrypt.org/directory # Testing caserver
      # caserver: https://acme-v02.api.letsencrypt.org/directory
      httpChallenge:
        entryPoint: web
```



Three entry points (lan, web, web-secured) are defined, each serving different purposes. Port 80 is reserved for internal HTTP (lan), port 591 is for external HTTP (web), and port 443 is for HTTPS (web-secured). SSL is used for encryption.

After running Docker Compose (`ei23 dc`) and restarting Traefik, Traefik reads the labels, and certificates are generated. Before creating a certificate, ensure to provide an email address for receiving certificate expiration or security-related warnings.

Let's Encrypt kindly provides free certificates, but there are daily and weekly limits on their usage. During testing, use the "staging" caserver, which issues unofficial certificates.

A good web browser issues a warning when accessing an address with an insecure or fake certificate. Accept the warning, verify that all desired services are reachable, then switch from the staging caserver to the official one. Official certificates are generated, and the web services are officially accessible after a short time.

If Traefik and port forwarding are correctly configured according to this guide, the file `/home/pi/ei23-docker/volumes/traefik/letsencrypt/acme.json` gradually contains lines with keys for different domains/subdomains.

This basic configuration should provide more than enough functionality for a home server. For further exploration, Traefik has excellent documentation: [doc.traefik.io/traefik](https://doc.traefik.io/traefik).