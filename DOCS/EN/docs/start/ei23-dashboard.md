# The ei23 Dashboard / The Supervisor
![ei23 Dashboard](https://ei23.de/bilder/dashboard01.jpg)

Since version 1.1 of the ei23 Smart Home Server, the Dashboard has changed fundamentally. 
It is now not only a display of available programs, but also a supervisor. At least the foundation is already in place. This means that you can soon install some programs via the Dashboard and manage system functions as well.

## Adapting Programs in the Dashboard

To link programs and external links such as cameras or other devices or websites on the Dashboard, you can modify the `programs.json`.
The file is located at `/home/[user]/ei23-docker/volumes/ei23/web/static/programs.json`
!!!note
    [user] must be replaced with your username in this place.

### Explanation of `programs.json`
```json
{"programs": [
{"active": true,    "port": "",     "custom_url": "http://10.1.1.11:1880",  "name": "NodeRED",          "title": "Garage",              "img": "img/nodered.png"}, // (1)
{"active": true,    "port": "4004", "custom_url": "",                       "name": "MQTT-Explorer",    "title": "MQTT-Explorer",       "img": "img/mqtt-explorer.png"}, // (2)
{"active": false,   "port": "",     "custom_url": "http://10.1.1.12",       "name": "Garden Camera",    "title": "Beautiful Garden",    "img": "img/camera.png"}, // (3)
{"active": true,    "port": "3000", "custom_url": "",                       "name": "Grafana",          "title": "Data Visualization",  "img": "img/grafana.png"} // (4)
]}
```

1. Here "http://10.1.1.11:1880" is a custom URL, which can also be an external address.
2. If no custom URL is set, the port is combined with the IP address of the device. For example http://10.1.1.2:4004
3. Since Active is set to False, this entry will not be displayed. A generic icon is also used here. Some are available in the img folder.
4. In the last entry, it is important that no comma is placed after the curly brace.

!!!note
    1. Here "http://10.1.1.11:1880" is a custom URL, which can also be an external address.
    2. If no custom URL is set, the port is combined with the IP address of the device. For example http://10.1.1.2:4004
    3. Since Active is set to False, this entry will not be displayed. A generic icon is also used here. Some are available in the img folder.
    4. In the last entry, it is important that no comma is placed after the curly brace.



## Network: List and Control Network Devices

![ei23 Dashboard](https://ei23.de/bilder/dashboard02.jpg)
The network page allows you to scan devices on the network, display their hostname, IP address, MAC address, and manufacturer information. If a web port 80 is detected, it means the device has a web interface available, which will be directly linked and the device marked blue.

## Server: Check installed Docker Compose Programs

![ei23 Dashboard](https://ei23.de/bilder/dashboard03.jpg)
This view automatically searches the [docker-compose.yml](docker-compose.md) file for installed and running containers or programs, creating and displaying a list. 
If a web port is detected, the program is marked accordingly and can also be accessed directly.
This can be practical to quickly get an overview of the configured programs and their ports, or to directly reach the web interface or check if the program is running.
Even though it happens automatically, it can be helpful to use the update button. This will re-read and check the programs.

Furthermore, under this view, you can quickly regenerate your own documentation for the home server. 