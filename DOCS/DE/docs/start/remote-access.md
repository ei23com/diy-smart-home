#Noch im Aufbau

Ich verweise zunächst auf die [Häufigen Fragen - FAQ](/start/faq)

## VPN
Über ein VPN wie [Wireguard](/software/wireguard) kannst du ein virtuelles Kabel in dein Heimnetz legen und so von überall sicher (getunnelt) auf dein Heimnetz zugreifen.

## Reverse Proxy
Über einen Reverse Proxy kannst du all deine Programme die lokal beispielsweise auf http://192.168.178.20:3000 auf eine Domain https://deinprogramm.deine-domain.de umleiten

### NGinx Proxy Manager
Der [NGinx Proxy Manager](https://nginxproxymanager.com/) ist eine einfache Möglichkeit so einen Proxy einzurichten. Die Installation läuft über Docker und ein Template wird über das Skript zur Verfügung gestellt

### Traefik
Der [Traefik Reverse Proxy](/software/traefik) ist in der Einrichtung etwas komplitzierter, lässt sich jedoch sehr gut automatisieren. Ich habe dazu eine Anleitung geschrieben


## SSH
[SSH-Verbindungen mit Public Key (Schlüsseldatei) absichern](https://ei23.de/smarthome/ssh-verbindungen-mit-public-key-verfahren-absichern/)
