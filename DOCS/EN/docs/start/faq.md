## How to Customize the Homepage with Programs and Add Your Own Programs?

Yes, you can add your own programs or network devices to the homepage. To do this, you need to modify the file `/home/pi/ei23-docker/volumes/ei23/web/static/programs.json` line by line. You can also find newly added programs after an update under `/home/pi/ei23-docker/volumes/ei23/web/static/programs_templates.json`. External pages can also be added to the dashboard, for example, the IP `192.168.0.1`:

```json
{"active":true, "port" : "", "custom_url":"http://192.168.0.1", "name": "Router", "title": "Router", "img":"img/router.png"}
```

Caution! The last line of this kind should not end with a comma. The page is usually cached by the browser, so you may need to clear it beforehand (with Ctrl-F5 or in the browser history settings). I also briefly explain this in the video: [Video zu Skript v0.9](https://www.youtube.com/watch?v=pKUv_rXONas&t=140s)

## How to Perform Updates for Programs?

In the SSH terminal, run `bash ei23.sh` and then choose "Complete Update" and press Enter. It's that simple.

## How to Install or Remove Programs Later?

See [install programs](docker-compose.md)

## Program XYZ is not Working, How Do I Reset It Without Reinstalling?

For example, to reset Portainer, you can use the following command (this works similarly for all other programs except for the ei23-Dashboard, Home Assistant, Mosquitto, and NodeRED):

```bash
cd ei23-docker/; docker-compose stop portainer; docker-compose rm -f portainer; sudo rm -r volumes/portainer/; docker-compose up -d
```

For NextcloudPi, it would look like this:

```bash
cd ei23-docker/; docker-compose stop nextcloudpi; docker-compose rm -f nextcloudpi; sudo rm -r volumes/nextcloudpi/; docker-compose up -d
```

Home Assistant can be reset as follows:

```bash
cd ei23-docker/; docker-compose stop homeassistant; docker-compose rm -f homeassistant; sudo rm -r volumes/homeassistant/config/.storage; sudo rm -r volumes/homeassistant/config/.cloud; sudo rm -r volumes/homeassistant/config/deps; sudo rm -r volumes/homeassistant/config/.storage; sudo rm -r volumes/homeassistant/config/tts; sudo rm volumes/homeassistant/config/home-assistant_v2.db; docker-compose up -d
```

If, for example, NodeRED is not working, there is likely another issue. See "Which devices and operating systems are supported?"

## How to Integrate a Zigbee/ConBee 2 Stick or Mount a USB Stick?

Since most programs are installed as Docker containers, you need to edit the docker-compose.yml (located under `/home/[user]/ei23-docker/docker-compose.yml`). For a description of how to include devices (Devices) and folders (Volumes) of the host system in a Docker container, see [install programs](docker-compose.md)

## Which Devices and Operating Systems Are Supported?

Officially, I test and develop with a Raspberry Pi 4 (min 2GB) with a freshly installed Raspberry Pi OS and also with a virtual machine with Debian 12 64Bit. Due to the many variations that can arise through different language settings alone, there may be some small errors here and there. I do not offer free help and solutions for this because it remains a DIY project and not a service with warranty claims.

## I Installed a Program Myself, Now Another One Doesn't Work!

There may be port overlaps - for example, examine the docker-compose.yml (in home/pi/ei23-docker). See [install programs](docker-compose.md) Generally, anything not installed via the script or following an ei23 guide can lead to problems, and even then, issues may arise. DIY rules here!

## The Command "grafana-cli" Doesn't Exist! / I Can't Find Apache/Nginx in the /var/www/ Directory (Running Commands in Docker Containers)

All programs running in a Docker container are logically not directly accessible via the terminal, and the directories are also encapsulated from the host system. To run commands in a Docker container, the following must be added before the command: `docker exec -it Containername Command`. For example, for Grafana: `docker exec -it grafana /bin/bash`. `/bin/bash` is the command to start a bash session. `docker exec -it grafana grafana-cli` works as well. Alternatively, you can also start a terminal session for the respective container via Portainer.

## I Can't Find NodeRED and the Software for the RTL-SDR DVB-T Stick in the Docker-Compose.yml or in the Templates!

That's correct. NodeRED and the software for the RTL-SDR DVB-T stick are installed natively, not as Docker containers, during the initial installation. Not installing NodeRED is not an option in the ei23 script because NodeRED should generally be used earlier. It is just very good.

## Can You Include Program XYZ in the Script?

Possibly, if it doesn't conflict with other programs, and I find the time, yes. However, it is advisable not to have all programs offered by the script running simultaneously. Almost no one will need OpenHAB, IOBroker, FHEM, and HomeAssistant all at once, and then the Pi won't sweat so much ;-)

## How Do I Change Passwords and Usernames?

This can be done with the script. Simply run `ei23`.

## Are There Shortcuts?

Yes! Just run `ei23 -h`.

## Which Weather Stations and 433MHz Devices Can I Integrate with the RTL-SDR DVB Stick?

You can find a list on the [project page](https://github.com/merbanan/rtl_433). Most unencrypted 433MHz devices should work.

## Is Transmission over Unencrypted 433MHz Secure? What Is the Range?

No, unencrypted 433MHz should be used at most for temperature sensors, weather stations, or contact sensors in non-critical areas. One should be aware that neighbors could theoretically log or clone/fake signals. So, know your neighbor ;-) The big advantage is mainly the price and distribution. The range of 433MHz devices is unfortunately usually only slightly better than with 2.4GHz WLAN. In contrast, WLAN is usually encrypted but requires more power (for battery operation) and is more expensive.

## Where Can I Find the Configuration Files for Home Assistant?

The folder with the configuration files and the database for Home Assistant has the path: `/home/[user]/ei23-docker/volumes/homeassistant/config`. If Home Assistant does not start correctly because, for example, "automations.yml" is missing, you can create the file with the following command line command and restart Home Assistant:

```bash
sudo echo "" > /home/pi/ei23-docker/volumes/homeassistant/config/automations.yml; cd ei23-docker/; docker-compose restart homeassistant; cd ~
```

## How Do I Install Add-On

s in Home Assistant?

First, a distinction must be made between integrations/frontend addons and third-party program addons (such as NodeRED, InfluxDB, Grafana, etc.): Integrations/frontend addons can be installed, as in HassIO, via the [Community Store (HACS)](https://hacs.xyz/) or manually in `/home/pi/ei23-docker/volumes/homeassistant/config`. As mentioned before: The script originated from the need to offer more flexibility and customization options than the HassIO operating system. HassIO uses the Home Assistant Supervisor for the installation of third-party program addons. These types of addons are usually installed as Docker containers, even in HassIO. Since the script largely takes over the functions of the Home Assistant Supervisor, it is not included for redundancy and compatibility reasons. See also [install programs](docker-compose.md)

## How Do I Connect Home Assistant with NodeRED?

The pre-installed Home Assistant addon for NodeRED just needs to be configured. For this, a long-term token (Access Token) must be created in Home Assistant in the user settings, and this token can then be used for the NodeRED Home Assistant addon. The URL should be entered as http://localhost:8123.

## How Do I Integrate Cameras in MotionEYE, and Which Cameras Work?

On [ispyconnect.com](https://www.ispyconnect.com/sources.aspx), there is a list of cameras with the corresponding URL for the video stream. This URL must be inserted into MotionEYE. If there is a URL for the video stream, there is a very high probability that you can also integrate the camera into MotionEYE. There are good tutorials online, but I will also make a video about it soon.

## Why Don't You Create an Image, Wouldn't That Be Easier?

No!

## When Will a Video on Voice Control / Axel Be Released?

It's here! [![YT](https://ei23.de/bilder/YTthumbs/xYB2sl9Sav8.webp)](https://www.youtube.com/watch?v=xYB2sl9Sav8)