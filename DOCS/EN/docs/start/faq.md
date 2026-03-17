##  How do I customize the start page with the programs, can I add my own programs?</strong>
Yes, you can add your own programs or network devices to the start page.
To do this, you need to edit the file `/home/pi/ei23-docker/volumes/ei23/web/static/programs.json` line by line:
Under `/home/pi/ei23-docker/volumes/ei23/web/static/programs_templates.json` you can also find newly added programs after an update.
You can also add external pages to the dashboard — for example the IP 192.168.0.1:
`{"active":true, "port" : "", "custom_url":"http://192.168.0.1", "name": "Router", "title": "Router", "img":"img/router.png"},`
Note! The last line of this type must not end with a comma.
The page is usually cached by the browser, so you may need to clear it first (with Ctrl-F5 or in the browser history settings).
I also explain it briefly in the video: [Video about script v0.9](https://www.youtube.com/watch?v=pKUv_rXONas&t=140s)

##  How do I perform updates for programs?</strong>
In the SSH terminal, run `bash ei23.sh` and then select "Complete Update" and press Enter. Very simple.

##  I want to install or remove programs afterwards</strong>
See [Install Programs](docker-compose.md)


##  Program XY doesn't work, how do I reset it without reinstalling?</strong>

!!!tip "Use Shortcuts"
    You can also use the simple command `ei23 fullreset X`, where X is the container name. Example: `ei23 fullreset portainer`

For example, Portainer is reset with the following command (this works analogously with all other programs **except** the ei23 Dashboard, Home Assistant, Mosquitto, and NodeRED):
```bash
cd ei23-docker/
docker compose stop portainer
docker compose rm -f portainer
sudo rm -r volumes/portainer/
docker compose up -d
```
For NextcloudPi it would look like this:
```bash
cd ei23-docker/
docker compose stop nextcloudpi
docker compose rm -f nextcloudpi
sudo rm -r volumes/nextcloudpi/
docker compose up -d
```
Home Assistant is reset as follows:
```bash
cd ei23-docker/
docker compose stop homeassistant
docker compose rm -f homeassistant
sudo rm -r volumes/homeassistant/config/.storage
sudo rm -r volumes/homeassistant/config/.cloud
sudo rm -r volumes/homeassistant/config/deps
sudo rm -r volumes/homeassistant/config/tts
sudo rm volumes/homeassistant/config/home-assistant_v2.db
docker compose up -d
```
If NodeRED, for example, doesn't work, there's probably a different problem. See "Which devices and operating systems are supported?"

##  How can I integrate a Zigbee / ConBee 2 stick or mount a USB stick?</strong>
Since most programs are installed as Docker containers, the docker-compose.yml (under `/home/[user]/ei23-docker/docker-compose.yml`) must be edited for this.

A description of how to bind devices and folders of the host system into a Docker container can be found here: [Install Programs](docker-compose.md)

##  Which devices and operating systems are supported?</strong>

The script supports the following operating systems:

| Operating System | Architectures | Status |
|------------------|---------------|--------|
| Raspberry Pi OS | armv7, arm64 | ✅ Tested |
| Debian 12 | arm64, amd64 | ✅ Tested |
| Ubuntu / Pop!_OS | arm64, amd64 | ✅ Tested |
| Fedora | amd64 | ✅ Tested |
| Arch / Manjaro | amd64 | ✅ Tested |
| CentOS / Rocky | amd64 | ✅ Tested |

I officially test and develop with a Raspberry Pi 4 (min 2GB) and a Virtual Machine with Debian 12 64-bit. The distributions listed above have been successfully tested.

!!!note "Docker Images"
    Due to the many variations, not all Docker images may be available for all architectures. Check this if necessary on [hub.docker.com](https://hub.docker.com/).

!!!note "32-Bit Systems"
    For 32-bit systems (armv7), the `docker-compose` command is used instead of `docker compose`. Some newer Docker images may not be available.

I do not offer free help and solutions for this, because it remains a DIY project and not a service with warranty claims.

##  I installed a program myself, now another one doesn't work!</strong>
There may be port overlaps — for example, check the docker-compose.yml (in home/pi/ei23-docker).
See [Install Programs](docker-compose.md)
In principle, anything that is not installed via the script or following an ei23 guide can cause problems, and even then problems can arise. DIY applies here!

##  The command grafana-cli doesn't exist! / I can't find apache / nginx in the /var/www/ directory (Running commands in Docker containers)</strong>
All programs running in a Docker container are logically not directly accessible via the terminal and the directories are also encapsulated from the host system.
To run commands in a Docker container, the following must be prepended to the command:
`docker exec -it containername command` — for Grafana, for example, `docker exec -it grafana /bin/bash`
/bin/bash is the command that starts a bash session.
`docker exec -it grafana grafana-cli` also works.
Alternatively, you can also start a terminal session for the respective container via Portainer.

##  I can't find NodeRED and the software for the RTL-SDR DVB-T stick in the Docker-Compose.yml or in the templates!</strong>
That's correct. NodeRED and the software for the RTL-SDR DVB-T stick are installed natively during the initial installation, i.e. not as Docker containers. By the way, not installing NodeRED is not an option in the ei23 script, since you should use NodeRED sooner or later anyway. It's simply very good.

##  Can you also integrate program XY into the script?</strong>
Possibly, if it doesn't conflict with other programs and I have the time for it, yes.
However, it is advisable not to run all programs that the script offers at the same time. There will hardly be anyone who needs OpenHAB, IOBroker, FHEM, and HomeAssistant simultaneously, and then the Pi won't get so hot either ;-)

##  How do I change the passwords and usernames?</strong>
You can do that with the script. Just run `ei23`.

##  Are there shortcuts?</strong>
Yes! Just run `ei23 -h`.

##  Which weather stations and 433MHz devices can I integrate with the RTL-SDR DVB-T stick?</strong>
You can find a list on the [project page](https://github.com/merbanan/rtl_433).
Most unencrypted 433MHz devices should work.

##  Is transmission over unencrypted 433MHz secure? What is the range?</strong>
No, unencrypted 433MHz should only be used for temperature sensors, weather stations, or contact sensors in non-critical areas, and you should be aware that the neighbor could theoretically log or clone/fake signals.
So: Know your neighbor ;-)
The big advantage is especially the price and the widespread availability.
The range of 433MHz devices is unfortunately usually only marginally better than WiFi with 2.4GHz.
WiFi, on the other hand, is usually encrypted, but requires more power (for battery operation) and is more expensive.

##  Where do I find the configuration files for Home Assistant?</strong>
The folder with the configuration files and the database of Home Assistant has the path:
`/home/[user]/ei23-docker/volumes/homeassistant/config`
If Home Assistant doesn't start properly because, for example, the "automations.yml" is missing, you can create the file with the following command and restart Home Assistant:
`sudo echo "" > /home/pi/ei23-docker/volumes/homeassistant/config/automations.yml; cd ei23-docker/; docker-compose restart homeassistant; cd ~`

##  How do I install AddOns in Home Assistant?</strong>
First, you must distinguish between Integrations / Frontend Addons and third-party Program Addons (like NodeRED, InfluxDB, Grafana, etc.):
Integrations / Frontend Addons can be installed just like in HassIO via the [Community Store (HACS)](https://hacs.xyz/) or manually in `/home/pi/ei23-docker/volumes/homeassistant/config`.
As mentioned before: The script originated from the need to offer more flexibility and customization options than the HassIO operating system. HassIO uses the Home Assistant Supervisor for installing third-party Program Addons. This type of addons are also typically installed as Docker containers in HassIO.
Since the script largely takes over the functions of the Home Assistant Supervisor, the supervisor is not included for reasons of redundancy and compatibility. Instead, the script installs Home Assistant Core, and the script's functions serve as the supervisor. See also [Install Programs](docker-compose.md)

##  How do I connect Home Assistant with NodeRED?</strong>
The pre-installed Home Assistant Addon for NodeRED simply needs to be configured.
To do this, a long-lived token (Access Token) must be created in Home Assistant in the user settings, and this can then be used for the NodeRED Home Assistant Addon.
As the URL, you should enter http://localhost:8123.

##  How do I integrate cameras into MotionEYE and which cameras work</strong>
On [ispyconnect.com](https://www.ispyconnect.com/sources.aspx) there is a list of cameras with the corresponding URL for the video stream. This URL must be inserted into MotionEYE.
If there is a URL for the video stream, the probability is very high that you can also integrate the camera into MotionEYE.
There are good guides online, but I'll also make a video about it soon.

##  Why don't you create an image, wouldn't that be easier?</strong>
No!

##  When will a video about voice control / Axel come?</strong>
It's here!
[![YT](https://ei23.de/bilder/YTthumbs/xYB2sl9Sav8.webp)](https://www.youtube.com/watch?v=xYB2sl9Sav8)
