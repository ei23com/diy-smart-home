# PairDrop

[PairDrop](https://pairdrop.net/) is an open-source alternative to AirDrop for all platforms. Share files easily and quickly on the local network - no installation, no account, just use the browser.

!!!tip "Perfect for everyday use"
    PairDrop is ideal for quickly sharing files between PC, smartphone, and tablet on your home network.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

## Template

```yaml
  pairdrop:
    container_name: pairdrop
    image: lscr.io/linuxserver/pairdrop:latest
    hostname: pairdrop
    restart: unless-stopped
    ports:
      - 3010:3000
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Berlin
      - RATE_LIMIT=false
      - WS_FALLBACK=false
      - DEBUG_MODE=false
```

## Usage

1. Open `http://[IP]:3010` in the browser
2. Other devices on the network open the same address
3. Click on a device and select files
4. The recipient must confirm the transfer

### On Smartphone

1. Open `http://[IP]:3010` in the browser
2. Add the page to your home screen (PWA)
3. Works like a native app

## Features

- **No Installation** - Runs entirely in the browser
- **No Account** - Just share files
- **P2P** - Files go directly between devices
- **Local** - No data leaves your network
- **Encrypted** - WebRTC with end-to-end encryption
- **Cross-Platform** - Works on all devices with a browser

## Notes

- Port 3010 is configured by default
- PairDrop uses WebRTC for direct P2P transfer
- Devices on the same WLAN are automatically discovered
- External devices can be temporarily connected via QR code

## Further Information

- [Official Website](https://pairdrop.net/)
- [GitHub Repository](https://github.com/schlagmichdoch/PairDrop)
