# Traefik Reverse Proxy - HTTPS Webservices selber hosten

Um Web-Services, die bei uns zu Hause laufen, aus dem Internet zu erreichen, gibt es viele Möglichkeiten. Die schlechteste Möglichkeit wäre die Portfreigabe und Weiterleitung auf ein Gerät mit unverschlüsseltem Protokoll wie beispielsweise das HTTP oder FTP. *Versuche es unbedingt zu vermeiden, eine einfache Portfreigabe auf HTTP oder FTP zu nutzen!*

Besser wäre da schon das SFTP und bzw. oder ein VPN. Beide verlangen Zertifikate um Clients zu autorisieren und die Daten werden anschließend verschlüsselt übertragen.

Bei vielen Routern und Endgeräten ist die Einrichtung jedoch aufwendig und beispielsweise ist das Hauseigene VPN einer FritzBox, welches auf IPSec setzt, ist nicht besonders modern oder schnell.

Abhilfe schafft da [WG-Easy](https://github.com/wg-easy/wg-easy) (siehe Compose Templates) oder [PiVPN](https://www.pivpn.io/), womit sich einfach WireGuard oder OpenVPN installieren lässt. Dazu habe ich bereits ein [Video Tutorial](https://www.youtube.com/watch?v=QwC5ndEIMZs) erstellt, wie dies mit dem ei23 Smart Home Server funktioniert.

**Ein VPN löst nicht alle Probleme**

Was ist aber wenn unbestimmte viele Clients auf unser System zugreifen sollen, oder wir nicht jedem Nutzer ein Zertifikat zur Verfügung stellen möchten? Oder was ist wenn wir einen Service betreiben, der zeitweise mehr Ressourcen benötigt, als beispielsweise ein kleiner Raspberry Pi zur Verfügung stellen kann?

Hier kommen Reverse Proxies und SSL Zertifikate ins Spiel. Mit einem Reverse Proxy kann beispielsweise eine Domain oder Subdomain aufgerufen werden, und der Reverse-Proxy entscheidet dann, welcher Inhalt dem Nutzer zugänglich gemacht wird. Zusätzlich kann der Inhalt über SSL verschlüsselt werden. So ist es beispielsweise möglich, eine IP hinter mehreren Domains zu verstecken und trotzdem mehrere Services aufzurufen.

![Traefik Architecture](https://ei23.de/wp-content/uploads/sites/4/2021/04/traefik-architecture-1024x535.png)

*Traefik Architecture (Quelle: [traefik.io](https://traefik.io))*

Es gibt natürlich auch andere Lösungen, wie z.B. Nginx. Da der [ei23 Smart Home Server](https://ei23.de/diy-smarthome) jedoch viele Programme als Docker-Container betreibt, nutzen wir Traefik, welches für Programme im Docker nochmal einige Vorteile bringt und zu dem eine gutes visuelles Interface hat.

## Proxy Konfiguration von Docker-Containern

Um einen Docker Container für Traefik zu konfigurieren, ist es lediglich notwendig die `/home/pi/ei23-docker/docker-compose.yaml` anzupassen. Wie das geht, zeige ich im [Video zu Version 1 vom Smart Home Skript](https://www.youtube.com/watch?v=QKjSvH40Pic).

**Beispiel docker-compose Bitwarden**

```yaml
bitwarden:
  image: bitwardenrs/server:latest
  container_name: bitwarden
  restart: unless-stopped
  # ports:*
      # - 2223:80
  labels:
      - traefik.enable=true
      - traefik.http.routers.bitwarden.rule=Host(`example.com`)
      - traefik.http.routers.bitwarden.entrypoints=web-secured
      - traefik.http.routers.bitwarden.tls=true
      - traefik.http.routers.bitwarden.tls.certresolver=letsEncrypt
  volumes:
      - ./volumes/bitwarden:/data
```

Mit Traefik ist es nicht zwingend notwendig die *Ports über Docker freizugeben, so lange Traefik sich im gleichen Dockernetzwerk wie die Container befindet. Daher sind diese im Beispiel oben mit # auskommentiert.

**Beispiel: Webseite im LAN (in diesem Fall das ei23 Dashboard)**

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.ei23-lan.rule=(Host(`192.168.178.10`) || Host(`smarthome`))
  - traefik.http.routers.ei23-lan.priority=1
  - traefik.http.routers.ei23-lan.entrypoints=lan
```

**Beispiel docker-compose Grafana**

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.grafana.rule=Host(`grafana.example.com`)
  - traefik.http.services.grafana.loadbalancer.server.port=3000
  - traefik.http.routers.grafana.entrypoints=web-secured
  - traefik.http.routers.grafana.tls=true
  - traefik.http.routers.grafana.tls.certresolver=letsEncrypt
```

**Beispiel docker-compose Nextcloud**

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

Wie man erkennen kann, gibt es für Traefik "Router, Services und Middlewares". Jeder Dienst benötigt mindestens einen eigenen Traefik-Router.

## Proxy Konfiguration von LoadBalancern / externen (IP) Adressen und weiteren Geräten im Netzwerk

In `/home/pi/ei23-docker/volumes/traefik/traefik/dynamic/config.yml` ist beispielsweise ein externer "Loadbalancer" für Home Assistant erstellt, da Home Assistant nicht innerhalb des Dockernetzwerks, sondern im Hostnetzwerk läuft. (Achtung! Die Zeileneinrückung muss stimmen - der Yaml Parser will das so)

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
          - url: http://172.17.0.1:8123 # 172.17.0.1 ist das Standard Docker Gateway
```

Dieser verweist statt auf einen Docker Container auf eine http-URL. Diese wird über den "certresolver" anschließend auch über SSL verschlüsselt.

## Inbetriebnahme von Traefik / SSL Zertifikate erstellen

Traefik selbst wird als Docker Container betrieben und in der aktuellen Version des ei23 Smart Home Servers ist Traefik bereits vorkonfiguriert, es müssen nur noch kleine Änderungen vorgenommen werden.

**Docker-Compose für Traefik**

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

Unter `/home/pi/ei23-docker/volumes/traefik/traefik/` befindet sich die `traefik.yaml`.

```yaml
[...]
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
      caserver: https://acme-staging-v02.api.letsencrypt.org/directory # Dies ist der caserver zum Testen
      # caserver: https://acme-v02.api.letsencrypt.org/directory
      httpChallenge:
        entryPoint: web
[...]
```

Hier sind drei Eingangspunkte, die so genannten Entrypoints, definiert:
- **Port 80** (lan) ist für HTTP im Heimnetz (LAN) reserviert.
- **Port 591** (web) ist für HTTP nach außen (WAN) reserviert - Der externe Port 80 muss auf den internen Port 591 des Raspberry Pi weitergeleitet werden. Da wir ausschließlich verschlüsselte Verbindungen nutzen wollen, erzwingen wir mit Traefik eine Weiterleitung auf den web-secured Entrypoint (443).
- **Port 443** (web-secured) ist schließlich der Port für HTTPS. Dieser muss nach außen am Router freigegeben und eine Weiterleitung zum Raspberry Pi auf der Port 443 eingerichtet werden.

Die Verschlüsselung wird realisiert mit SSL.

Nach Ausführen von Docker Compose (`ei23 dc`) und einem Neustart von Traefik werden die Labels von Traefik eingelesen und die Zertifikate erstellt.

Bevor aber ein Zertifikat erstellt werden kann, sollte eine Email Adresse hinterlegt werden. Darüber wird man ggf. über den Ablauf eines Zertifikates oder andere Warnungen bezüglich der Sicherheit informiert.

Der Dienst Let’s Encrypt ist so freundlich uns die sonst sehr teuren Zertifikate kostenlos zur Verfügung zu stellen. Allerdings gibt es ein Tages- und Wochenlimit, solange wir nur testen, ob alles klappt, sollten wir den “staging” caserver nutzen; hier wird kein offizielles Zertifikat ausgestellt.

Ein guter Webbrowser gibt beim Aufruf einer Adresse eine Warnung aus, wenn das Zertifikat nicht sicher bzw. echt ist. Wenn man diese Warnung akzeptiert und alle gewünschten Dienste dennoch erreichbar sind, dann kann man vom staging caserver zum offiziellen wechseln. Anschließend werden offizielle Zertifikate erstellt und die Webdienste sind nach kurzer Zeit offiziell verschlüsselt erreichbar.

Wenn Traefik und die Portweiterleitungen gemäß dieser Anleitung richtig konfiguriert worden sind, dann tauchen in der Datei `/home/pi/ei23-docker/volumes/traefik/letsencrypt/acme.json` nach und nach die Zeilen mit den Schlüsseln zu deinen verschiedenen Domains / Subdomains auf.

Diese Basis Konfiguration sollte für den Heimserver bereits mehr als genug Funktionalität bieten. Wer dennoch weiter in die Materie einsteigen will: Traefik hat eine sehr gute Dokumentation: [doc.traefik.io/traefik](https://doc.traefik.io/traefik).