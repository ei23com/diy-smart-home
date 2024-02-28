# 1.00
    sudo sed -i -e "s#image: influxdb:latest#image: influxdb:1.8.4#" $HOME/ei23-docker/docker-compose.yml
    sudo sed -i -e "s#image: influxdb:1.8.2#image: influxdb:1.8.4#" $HOME/ei23-docker/docker-compose.yml
    sudo sed -i -e "s#      - ./volumes/ei23/web:/www#      - ./volumes/ei23/web:/www\n      - ./volumes/ei23/docs/site:/www/docs#" $HOME/ei23-docker/docker-compose.yml
    sudo apt-get install -y nmap netdiscover sysfsutils tcpdump wget ssh unzip build-essential git python-serial libcurl4-openssl-dev libusb-dev python-dev cmake curl telnet usbutils jq pv parted gcc python3-pip htop python-smbus mpg123 screen imagemagick arp-scan imagemagick-doc raspberrypi-kernel-headers libimage-exiftool-perl ffmpeg libusb-1.0-0-dev zsh virtualenv libtool autoconf pkg-config libxml2-dev ncdu libfftw3-dev ncftp mosquitto-clients expect mkdocs
    sudo pip3 install mkdocs-material