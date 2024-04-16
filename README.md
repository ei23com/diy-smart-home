# The ei23 DIY Smart Home (Server)
This project is a dead-easy, clean and slim **installation** and **maintenance** tool for a huge amount of mostly Docker-based home automation and media software, easily accessible on a clean, slim and customizable web dashboard.
Made for Debian and Raspberry OS, working on most architectures.
Maybe it's not as easy to configure as the Home Assisstant OS, for example, but you get a lot more customization options and get in touch with the docker-compose.yml notation, which is also a great tool.
And you don't even have to use Home Assistant if you prefer OpenHAB or IObroker for example. All on one system.

Have fun, get smart and independent!

![ei23 Dashboard](https://ei23.de/bilder/ei23-terminal.gif)

![ei23 Counter](https://ei23.de/bilder/svg-stats.svg)

## What's included
Have a loook in the **[compose_templates](ei23-docker/compose_templates)** and the **[ei23.sh](ei23.sh)** script itself.
Batteries are not included.

![ei23 Dashboard](https://ei23.de/bilder/ei23-dashboard.jpg)

## Documentation and official website
- [[DE] DOCS - diy-smart-home.ei23.de](https://diy-smart-home.ei23.de)
- [[EN] DOCS - diy-smart-home.ei23.com](https://diy-smart-home.ei23.com)

You should find much more about this project there. 
If you want to edit pages or add stuff [read the guidelines](DOCS/guidelines.md)

## Introduction
In 2017, I planned to install a self-built smart home system that would control some retrofit devices. There were various options to choose from, and I was unsure about which program was right for me. It was also clear that I would be running a computer 24/7, in this case a Raspberry Pi. It would have been a shame if only a single application ran on it. At that time, I had already conducted some experiments with NodeRED and appreciated the advantages of the Raspberry Pi's GPIOs.

[You can watch a video about my journey back then](https://www.youtube.com/watch?v=6FkINyLcLnU)
[![YT](https://ei23.de/bilder/YTthumbs/6FkINyLcLnU.webp)](https://www.youtube.com/watch?v=6FkINyLcLnU)

Although I liked the Home Assistant OS overall, using it meant giving up the flexibility of a conventional Linux system. Therefore, I created a compromise: My installation script takes care of installing and configuring all necessary programs and settings. When possible, all programs run in Docker containers. This significantly simplifies system maintenance and experiments while providing more convenience.

So, the script originated from the need to offer more flexibility, customization options, and programs than the Home Assistant operating system. For those who want to expand their system without running another server/Raspberry Pi or virtual machines in parallel, this script provides a solution. First, necessary and useful programs and frameworks like Docker, Python, etc., are installed on the raw Raspbian OS or Debian. Then, NodeRED is installed in its native form, not as a Docker container. This offers additional features and easier configuration without cumbersome workarounds. Additionally, Log2Ram (to reduce SD card write operations), RTL_SDR software (for example, for 433MHz sensors), and rpiClone (for easy backups) can be installed directly. The script currently automates the installation of those programs and also includes some addons (custom extensions are, of course, possible).

## System requirements
Originally, the system was only available for the Raspberry Pi (armv7 / 32-bit). In the meantime, however, I recommend using a 64-bit system (arm64). The script is also functional on Debian 12 (tested) and AMD64 architectures.
(Docker images may not be available for all system architectures)

If you only plan to run home automation software like [Home Assistant Docker](https://github.com/home-assistant/docker), [NodeRED](https://github.com/node-red/node-red) and a password manager like [Vaultwarden / Bitwarden](https://github.com/dani-garcia/vaultwarden), a Raspberry Pi 4 with 2GB is already sufficient.
If you also want to run compute-intensive software like a media center or photo cloud apps like [Immich](https://immich.app/) or [Nextcloud](https://nextcloud.com/), consider using an low-end thinclient with an Intel i5 and 8GB RAM or similar.

SSD storage may works best for you.
Always backup important data.

## Installation

### Easy installation:
The easy-installation is self-explanatory. 
After registering for the newsletter ([ENGLISH NEWSLETTER](https://ei23.com/newsletter) / [GERMAN NEWSLETTER](https://ei23.de/newsletter)), you will receive two command lines, which you must execute via the input console or over SSH. 
The first line downloads the script (bash script) and the second line executes it.

*C'mon! Why newsletter?*
1. I can inform you quickly about security vulnerabilities and interesting new features
2. Community building gets easier
3. Some advertising for my work and the project itself is possible
4. And I can secretly inject malicious code on your script and create a botnet from a large number of servers... NOT! - seriously! I won't do that, or do you think i would? I'm confused... Why should i do that, should I do it? Now you're confused? Just don't make trouble! Ok back to topic xD

The files are identical to ones you see here with the exeption of a uniqe USERID for downloading files from my server and automatically set LANGFILE dependent on which newsletter you choose.
Also I won't bother you unnecessarily, if you think you can use a trash mail.

### Manual installation:
1. Clone the files to a folder.
2. Insert the language file of your choice (de-file.txt / en-file.txt) into [ei23.sh](ei23.sh) and replace "LANGFILE_PLACEHOLDER"
3. Install a fresh Debian / Rasbian system, login via ssh or terminal and create a user like this "useradd -m ei23" (or another name)
4. Copy the entire "ei23-docker" folder into your users home directory (with root privileges)
5. Copy the [ei23.sh](ei23.sh) into your user home directory
6. run "bash [ei23.sh](ei23.sh) part1"
7. follow instructions
8. after you done the reboot, run "ei23", the script then will finish the installation


- ei23 updates won't work with manual installation (USERID from newsletter is needed)
- you won't see a version number and will not get info about new versions (USERID from newsletter is needed)
- everything else works like normal

## Reporting issues
Please use the [issues](https://github.com/ei23com/diy-smart-home/issues) tab to report issues or make suggestions for new features or containers.
Or reach out to the [Community (see below)](#community)

## Contribution
Thanks for asking!

If you want, you can pull request and edit or add doc files [(read guidelines)](DOCS/guidelines.md) or edit and add [compose_templates](ei23-docker/compose_templates)
or any other files as well.
If you want to have icons added for the dashboard, have a look [here](ei23-docker/volumes/ei23/web/img). Please use 128x128 PNG with transparent background.

## Great Open Source Projects
I love open source projects - [here is my best of list](https://ei23.com/opensource/)
Consider supporting them!

## Community
[YouTube](https://youtube.com/ei23-de)<br>
[Discord](https://discord.gg/pS9cZTBUfs)<br>
[Telegram (DE)](https://t.me/ei23de)<br>
[Forum (DE)](https://forum.ei23.de/)<br>


## Donations
[(EN) ei23.com/donate](https://ei23.com/donate/)<br>
[(DE) ei23.de/donate](https://ei23.de/donate/)<br>
You can expect special percs there.


Thanks!