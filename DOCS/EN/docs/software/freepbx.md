# FreePBX / Asterisk

[FreePBX](https://www.freepbx.org/) with [Asterisk](https://www.asterisk.org/) is an open-source phone system (PBX). With it, you can operate VoIP phones, automate calls, and build a professional telephony infrastructure.

!!!warning "For Advanced Users"
    FreePBX requires VoIP knowledge. You need a SIP provider or VoIP phones for meaningful use.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  freepbx-app:
    image: epandi/asterisk-freepbx-arm:17.15-latest
    container_name: freepbx-app
    restart: unless-stopped
    ports:
      - 2233:80           # Web interface
      - 5060:5060/udp     # SIP
      - 5160:5160/udp     # SIP Alt
      - 18000-18100:18000-18100/udp  # RTP (call data)
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

## First Start

1. After starting, access FreePBX at `http://[IP]:2233`
2. Follow the setup wizard
3. Create an admin password

## Basic Configuration

### SIP Trunk (SIP Provider)

1. Go to **Connectivity** → **Trunks**
2. Click **Add Trunk** → **Add SIP (chan_pjsip) Trunk**
3. Configure:
    - **Trunk Name**: Provider name
    - **Outbound CallerID**: Your phone number
    - **SIP Settings**: Server, user, password from provider

### Extensions

1. **Applications** → **Extensions**
2. **Add Extension** → **Add New Chan_PJSIP Extension**
3. Configure:
    - **Extension Number**: e.g., 1001
    - **Display Name**: Name
    - **Secret**: Password for the phone

### Inbound Routes

1. **Connectivity** → **Inbound Routes**
2. Define what happens on incoming calls
3. Destination: Extension, IVR, Voicemail, etc.

### Outbound Routes

1. **Connectivity** → **Outbound Routes**
2. Configure which extensions use which trunks

## Use Cases

| Application | Description |
|-------------|-------------|
| **Home Office** | Own phone system for home office |
| **Door Intercom** | Connect SIP intercom |
| **Emergency Phones** | Old landline phones via SIP |
| **Voicemail** | Set up answering machine |
| **IVR** | Voice menu "Press 1 for..." |

## Notes

- FreePBX accessible on port 2233
- SIP ports 5060/5160 may need port forwarding on router
- RTP ports 18000-18100 for voice data
- Data in `./volumes/asterisk17/`
- Image optimized for ARM (Raspberry Pi)

!!!note "Alternatives"
    For simple SIP use, a simple SIP client is often sufficient. FreePBX is worthwhile with multiple phones or complex call routes.

## Further Information

- [FreePBX Documentation](https://wiki.freepbx.org/)
- [Asterisk Documentation](https://www.asterisk.org/docs/)
- [FreePBX Community](https://community.freepbx.org/)
