# FreePBX / Asterisk

[FreePBX](https://www.freepbx.org/) mit [Asterisk](https://www.asterisk.org/) ist eine Open-Source-Telefonanlage (PBX). Damit kannst du VoIP-Telefone betreiben, Anrufe automatisieren und eine professionelle Telefonie-Infrastruktur aufbauen.

!!!warning "Für Fortgeschrittene"
    FreePBX erfordert VoIP-Kenntnisse. Du benötigst einen SIP-Provider oder VoIP-Telefone für sinnvollen Einsatz.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  freepbx-app:
    image: epandi/asterisk-freepbx-arm:17.15-latest
    container_name: freepbx-app
    restart: unless-stopped
    ports:
      - 2233:80           # Web-Oberfläche
      - 5060:5060/udp     # SIP
      - 5160:5160/udp     # SIP Alt
      - 18000-18100:18000-18100/udp  # RTP (Anruf-Daten)
      - 4445:4445         # Flash Operator Panel
    volumes:
      - ./volumes/asterisk17/certs:/certs
      - ./volumes/asterisk17/data:/data
      - ./volumes/asterisk17/logs:/var/log
      - ./volumes/asterisk17/data/www:/var/www/html
      - ./volumes/asterisk17/db:/var/lib/mysql
    environment:
      - VIRTUAL_HOST=asterisk.local
      - VIRTUAL_PORT=80
      - ZABBIX_HOSTNAME=freepbx-app
      - RTP_START=18000
      - RTP_FINISH=18100
      - DB_EMBEDDED=TRUE
    cap_add:
      - NET_ADMIN
```

## Erster Start

1. Nach dem Start erreichst du FreePBX unter `http://[IP]:2233`
2. Folge dem Installationsassistenten
3. Erstelle ein Admin-Passwort

## Grundkonfiguration

### SIP-Trunk (SIP-Provider)

1. Gehe zu **Connectivity** → **Trunks**
2. Klicke **Add Trunk** → **Add SIP (chan_pjsip) Trunk**
3. Konfiguriere:
    - **Trunk Name**: Name des Providers
    - **Outbound CallerID**: Deine Rufnummer
    - **SIP Settings**: Server, Benutzer, Passwort des Providers

### Extensions (Nebenstellen)

1. **Applications** → **Extensions**
2. **Add Extension** → **Add New Chan_PJSIP Extension**
3. Konfiguriere:
    - **Extension Number**: z.B. 1001
    - **Display Name**: Name
    - **Secret**: Passwort für das Telefon

### Inbound Routes (Eingehende Anrufe)

1. **Connectivity** → **Inbound Routes**
2. Definiere was bei eingehenden Anrufen passiert
3. Ziel: Extension, IVR, Voicemail, etc.

### Outbound Routes (Ausgehende Anrufe)

1. **Connectivity** → **Outbound Routes**
2. Konfiguriere welche Nebenstellen welche Trunks nutzen

## Anwendungsfälle

| Anwendung | Beschreibung |
|-----------|--------------|
| **Home-Office** | Eigene Telefonanlage für Home-Office |
| **Haustür-Sprechanlage** | SIP-Intercom anbinden |
| **Notfalltelefone** | Alte Festnetztelefone über SIP |
| **Anrufbeantworter** | Voicemail einrichten |
| **IVR** | Sprachmenü "Drücken Sie 1 für..." |

## Hinweise

- FreePBX erreichbar auf Port 2233
- SIP Ports 5060/5160 müssen bei Bedarf am Router weitergeleitet werden
- RTP-Ports 18000-18100 für Sprach-Daten
- Daten in `./volumes/asterisk17/`
- Das Image ist für ARM optimiert (Raspberry Pi)

!!!note "Alternativen"
    Für einfache SIP-Nutzung reicht oft ein simpler SIP-Client. FreePBX lohnt sich bei mehreren Telefonen oder komplexen Anruf-Routen.

## Weitere Informationen

- [FreePBX Dokumentation](https://wiki.freepbx.org/)
- [Asterisk Dokumentation](https://www.asterisk.org/docs/)
- [FreePBX Community](https://community.freepbx.org/)
