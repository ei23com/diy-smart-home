## Installation

This project is a super easy, clean, and lightweight installation and maintenance tool for a large number of mostly Docker-based home automation and media software, easily accessible through a clean, lightweight, and customizable web dashboard.

## Supported Systems

The script works on the following operating systems and architectures:

- **Raspberry Pi OS** (armv7, arm64) - Tested
- **Debian 12** (arm64, amd64) - Tested
- **Ubuntu / Pop!_OS** (arm64, amd64) - Tested
- **Fedora** (amd64) - Tested
- **Arch / Manjaro** (amd64) - Tested
- **CentOS / Rocky** (amd64) - Tested

!!!note "32-Bit Systems"
    For 32-bit systems (armv7), the `docker-compose` command is used instead of `docker compose`. Some newer Docker images may not be available.

Perhaps it's not quite as easy to configure as, for example, Home Assistant OS, but it offers significantly more customization options and allows you to learn how to work with docker-compose.yml syntax, which is also a great tool. And you don't even have to use Home Assistant if you prefer to use OpenHAB or IOBroker — all on one system.

## Hardware Recommendation

!!!tip "Mini-PCs / ThinClients Recommended"
    Although the Raspberry Pi has very low power consumption, the **performance per watt** of used Mini-PCs and ThinClients is often significantly better. For around 50-100€ you can get used x86 systems that support all Docker images and offer more performance.
    
    Examples: **HP T620/T630**, **Dell Wyse 5070**, **Lenovo ThinkCentre M700** or an **Intel N100 Mini-PC**.
    
    [More details on the hardware page](/hardware/server/)

Have fun, get smart and independent!

### Simple Installation:

The simple installation is self-explanatory.
After signing up for the newsletter ([ENGLISH NEWSLETTER](https://ei23.com/newsletter) / [GERMAN NEWSLETTER](https://ei23.de/newsletter)), you will receive two command lines that you need to execute via console or SSH.
The first line downloads the script (bash script), and the second line executes it.

*Why a newsletter?*

1. I can quickly inform you about security vulnerabilities and interesting new features.
2. Building a community becomes easier.
3. A little advertising for my work and the project is possible.
4. And I could secretly insert malicious code into your script and create a botnet from a large number of servers! — Of course I won't do that! Or do you think I would? Now I'm confused... Why would I do that, should I do it? Now you're confused? Just don't cause trouble! Ok, back to the topic xD

The files from the newsletter are identical to those from Github, with the exception of a unique USERID for downloading files from my server and automatically setting the LANGFILE depending on which newsletter language you choose.
Also, I won't bother you unnecessarily — if you have concerns, just use a disposable email... Then I'll be sad though.

### Manual Installation:

1. Clone the files into a folder `git clone https://github.com/ei23com/diy-smart-home.git`
2. Add the language file of your choice (de-file.txt / en-file.txt) into ei23.sh and replace the placeholder "LANGFILE_PLACEHOLDER".
3. Install a fresh Debian / Raspberry Pi OS system, log in via SSH or terminal, and create a user as follows: "useradd -m ei23" (or another name).
4. Copy the entire "ei23-docker" folder to the user's home directory (with root privileges).
5. Copy the ei23.sh to the user's home directory.
6. Run "bash ei23.sh part1".
7. Follow the instructions.
8. After the restart, run "ei23" — the script will then complete the installation.

- Updates from ei23 do not work with manual installation (USERID from the newsletter is required).
- You will not see a version number and will not receive information about new versions (USERID from the newsletter is required).
- Everything else works as usual.

## After Installation

After installation, you will find the [ei23 Dashboard](/start/ei23-dashboard) on the HTTP port and IP address of your server.
You can also now install additional programs as [Docker containers](/start/docker-compose).

## More Questions?

For everything else, I refer you to the [Frequently Asked Questions - FAQ](/start/faq)
