# first get script: wget -q "https://ei23.de/softwarehub/smarthome/USERID/ei23.sh" -O ei23.sh
# then run script: bash ei23.sh
#
IAM=$(whoami)
OS="$(cat /etc/[A-Za-z]*[_-][rv]e[lr]* | grep "^ID=" | cut -d= -f2 | uniq | tr '[:upper:]' '[:lower:]' | tr -d '"')"
ARCHITECTURE="$(uname -m)"
ARCHITECTURE_DPKG="$(dpkg --print-architecture)"
DOCKER_COMPOSE="docker compose"

LANGFILE_PLACEHOLDER

SCRIPT_VERSION=0
NOLOGNODE="-s"
DOCKERDIR="$HOME/ei23-docker"
FIRSTFILE="$HOME/ei23-docker/firstinstall.txt"
OPTIONS=$1


# Colors
CRed='\e[0;91m'        # Red
CGreen='\e[0;92m'      # Green
CYellow='\e[0;93m'     # Yellow
CBlue='\e[0;94m'       # Blue
CMagenta='\e[0;95m'    # Purple
CCyan='\e[0;96m'       # Cyan
CWhite='\e[0;97m'      # White

sshlogo=$(cat <<EOF
           _ ___ ____
       ___(_)_  )__ /
      / -_) |/ / |_ \\ 
      \___|_/___|___/
     Smart Home Server
EOF
)

printmsg() {
    printf "${CWhite}===================================================\n"
    printf "${CWhite}//// $1\n"
    printf "${CWhite}===================================================\n${CGreen}"
}   

printstatus() {
    array=( '\e[30m' '\e[30m' '\e[30m' '\e[30m' '\e[30m' '\e[30m' '\e[30m' '\e[30m''\e[30m' '\e[30m' '\e[30m' '\e[30m''\e[30m' '\e[30m' '\e[30m' '\e[30m''\e[30m' '\e[30m' '\e[30m' '\e[30m''\e[30m' '\e[30m' '\e[30m' '\e[30m' '\e[0;97m' )
	clear
    index=$2
    if [ -z "$2" ]; then 
        index=20
    fi
	printf "\n${CWhite}"
	printf "${array[$index+0]}                .,:cc:'                 \n"
	printf "${array[$index+1]}             .ckXWMMMMNd.               \n"
	printf "${array[$index+2]}           .c0WMMMMMMMNd.  ..           \n"
	printf "${array[$index+3]}          'kWMMMWXOxol,   'kk'          \n"
	printf "${array[$index+4]}         ;KMMNkl,.    ..:xXMMK;         \n"
	printf "${array[$index+5]}        :XMMK;   .;ldx0NWMMMMMX:        \n"
	printf "${array[$index+6]}       ;KMMNc  .xXWMMMMMMMMMMMMK;       \n"
	printf "${array[$index+7]}      .OMMMX;  .,;;;;;;;;;;dNMMMO.      \n"
	printf "${array[$index+8]}      lWMMMNo''..........'.lNMMMWl      \n"
	printf "${array[$index+9]}     .OMMMMMWNNNNNNNNNNNNNNWMMMMMO.     \n"
	printf "${array[$index+10]}     ;XMMMMMMMWX0kxxxxk0NWMMMMMMMX;     \n"
	printf "${array[$index+11]}     :NMMMMMWOc.       ..cOWMMMMMN:     \n"
	printf "${array[$index+12]}     ,KMMMMMk.  'lxxxxl.  .kMMMMMK,     \n"
	printf "${array[$index+13]}     .xMMMMWOoldKMMMMMMx.  lWMMMMx.     \n"
	printf "${array[$index+14]}      '0MMMMMMMMWKOOOOd' .:0MMMM0'      \n"
	printf "${array[$index+15]}       'OWMMMMMMX: .     ;OWMMWO'       \n"
	printf "${array[$index+16]}        .oXMMMMMW0kkkkd:. .oXXo.        \n"
	printf "${array[$index+17]}          .l0NMMMMMMMMMN:  .,'          \n"
	printf "${array[$index+18]}             'cdkO0000Ol.               \n"
	printf "${array[$index+19]}                 .....                  \n"
	printf "${CBlue}===================================================\n"
    printf "${CCyan}//// $1\n"
 	printf "${CBlue}===================================================\n${CGreen}"      
}

printerror(){
    printf "${CWhite}===================================================\n"
    printf "${CRed}//// $1\n"
 	printf "${CWhite}===================================================\n${CGreen}"      
}

printwarn(){
    printf "${CWhite}===================================================\n"
    printf "${CYellow}//// $1\n"
 	printf "${CWhite}===================================================\n${CGreen}"      
}

system_32bit(){
# Check for 32Bit
    if [[ "$ARCHITECTURE" == "armv7"* ]] || [[ "$ARCHITECTURE" == "i686" ]] || [[ "$ARCHITECTURE" == "i386" ]] || [[ "$ARCHITECTURE_DPKG" == "armhf" ]]; then
        DOCKER_COMPOSE="docker-compose"
        printwarn "32Bit OS $L_DEPRECATED"
        if [[ $MYMENU != *"nodocker"* ]]; then
            MYMENU="$MYMENU nodocker"
        fi
        return 0
    fi
    return 1
}

setsshlogo(){
    echo "$sshlogo" | sudo tee /etc/motd
}

noderedUpdate(){
    what=$1
    cd ~
    sudo npm install -g npm
    printstatus "$what NodeJS $L_AND NodeRed"
    # Documentation - https://nodered.org/docs/getting-started/raspberrypi
    bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) --confirm-install --confirm-pi --node18 --update-nodes
    printstatus "$what Nodes $L_PLEASEWAIT"
    cd ~/.node-red/
    # Update preselected Addons
    for addonnodes in moment node-red-contrib-boolean-logic node-red-contrib-config node-red-contrib-counter node-red-contrib-dwd-local-weather node-red-contrib-eztimer node-red-contrib-ftp node-red-contrib-home-assistant-websocket node-red-contrib-ical-events node-red-contrib-influxdb node-red-contrib-looptimer2 node-red-contrib-smartmeter node-red-contrib-sunpos node-red-contrib-telegrambot node-red-contrib-time-range-switch node-red-contrib-timerswitch node-red-contrib-ui-level node-red-contrib-vcgencmd node-red-dashboard node-red-node-email node-red-node-pi-gpio node-red-node-ping node-red-node-random node-red-node-serialport node-red-node-smooth node-red-contrib-postgresql; do
        printstatus "$what node ${addonnodes}"
        # npm -s install --no-audit --no-update-notifier --no-fund --save --save-prefix="~" --production node-red-contrib-config@latest
        npm $NOLOGNODE install --no-audit --no-update-notifier --no-fund --save --save-prefix="~" --production ${addonnodes}@latest
    done
    printstatus "$what node bcryptjs"
    sudo npm $NOLOGNODE install bcryptjs

    # Node-RED Settings
    cd ~/.node-red/
    npm $NOLOGNODE audit fix
    cd ~
    sudo service nodered restart
}

install-ha-addons(){
    # $1 name / $2 url / $3 topfolder / $4 addonfolder
    printmsg "$L_INSTALLING $1"
    haPath="$DOCKERDIR/volumes/homeassistant/config"
    wget "$2" -O $1.zip
    if [ -d "$haPath/custom_components/$4" ]; then
        printmsg "$L_UPDATING $1"
        sudo rm -R "$haPath/custom_components/$4"
    fi
    sudo mkdir -p "$haPath/custom_components/$4"

    if [ "$4" != "hacs" ]; then
        # run this when not "hacs"
        sudo unzip "$1.zip" "$3/custom_components/$4/*" -d "$haPath/custom_components/$4" >/dev/null 2>&1
        sudo cp -r "$haPath/custom_components/$4/$3/custom_components/$4" "$haPath/custom_components/"
        sudo rm -R "$haPath/custom_components/$4/$3"
    else
        # special cake for hacs -.-
        sudo unzip "$1.zip" "*" -d "$haPath/custom_components/$4" >/dev/null 2>&1
    fi
    rm $1.zip
}

custom-ha-addons(){
    if [ "$(docker ps -a | grep homeassistant)" ]; then
        # $1 name / $2 url / $3 topfolder / $4 addonfolder
        install-ha-addons "ha-node-red" "https://codeload.github.com/zachowj/hass-node-red/zip/refs/heads/main" "hass-node-red-main" "nodered"
        install-ha-addons "hacs" "https://github.com/hacs/integration/releases/latest/download/hacs.zip" "integration-main" "hacs"
        install-ha-addons "ha-ical" "https://codeload.github.com/tybritten/ical-sensor-homeassistant/zip/refs/heads/master" "ical-sensor-homeassistant-master" "ical"
        source $HOME/ei23-docker/custom_ha_addons.sh # Add your own addons here!
        docker restart homeassistant
    fi
}

nextcloud-upgrade(){
    if [ "$(docker ps -a | grep nextcloud)" ]; then
        docker exec -u www-data nextcloud php occ upgrade;
    fi
}

installPackages(){
    sudo apt-get install -y arp-scan autoconf build-essential cmake curl rsync expect ffmpeg gcc git htop btop imagemagick imagemagick-doc jq libcurl4-openssl-dev libfftw3-dev libimage-exiftool-perl libtool libusb-1.0 mkdocs mosquitto-clients mpg123 ncdu ncftp netdiscover nmap parted pkg-config pv python3-full python3-venv screen ssh sshpass sysfsutils tcpdump telnet ufw unzip usbutils virtualenv wireguard zsh
}

aptUpdate(){
    what=$1
    printstatus "$what... $L_PLEASEWAIT"
    sudo apt -y remove needrestart
    sudo apt-get clean -y
    sudo apt-get autoremove -y
    sudo apt-get update -y
    sudo dpkg --configure -a
    sudo apt-get upgrade -y
    # sudo apt-get dist-upgrade # Kernel Upgrade

}

pipUpdate(){ # TODO REFACTOR
    what=$1
    printstatus "$what... $L_PLEASEWAIT"
    # pip3 install --upgrade pip
    sudo apt-get install python3-rpi.gpio -y
}

ei23_supervisor(){
    # if system_32bit; then
    #     exit 1
    # fi
    system_32bit
    sudo apt-get update
    docker stop ei23; cd ~/ei23-docker/; 
    # composeCMD "rm -f ei23"
    sudo apt-get install python3-venv -y
    sudo mkdir -p $DOCKERDIR/volumes/ei23/web/static/
    sudo mv -f $DOCKERDIR/volumes/ei23/web/dist $DOCKERDIR/volumes/ei23/web/static
    sudo mv -f $DOCKERDIR/volumes/ei23/web/img $DOCKERDIR/volumes/ei23/web/static
    cd $DOCKERDIR/volumes/ei23/
    sudo python3 -m venv .venv
    sudo .venv/bin/pip3 install --upgrade pip
    sudo .venv/bin/pip3 install flask waitress mkdocs-material ruamel.yaml psutil asyncio humanize
    # sudo arp-scan --plain --ignoredups --resolve -l --format='${ip} ${Name} ${mac} ${vendor}'
    # move files
    cd ~
    # replace all "username" in each line
    if [ ! -f "$DOCKERDIR/volumes/ei23/web/static/programs.json" ]; then
        sudo cp "$DOCKERDIR/volumes/ei23/web/programs.json" "$DOCKERDIR/volumes/ei23/web/static/programs.json"
    fi
    sudo sed -i -e "s#username#$IAM#g" $DOCKERDIR/volumes/ei23/ei23.service
    sudo mv $DOCKERDIR/volumes/ei23/ei23.service /usr/lib/systemd/system/ei23.service
    # cd ei23-docker/volumes/ei23/; sudo .venv/bin/python3 ei23-supervisor.py
    sudo systemctl enable ei23.service
    sudo systemctl start ei23.service
    sudo systemctl restart ei23.service
}

composeCMD(){
    cmd=$1
    cd $DOCKERDIR
    env_dir="env"
    env_files=()
    if ! system_32bit; then
        # Check if there are any .env files in the directory
        if [ -n "$(find "$env_dir" -maxdepth 1 -name '*.env' -print -quit)" ]; then
            # Loop through each .env file in the directory
            for env_file in "$env_dir"/*.env; do
                env_files+=("--env-file" "$env_file")
            done
        fi
        if [ -f .env ]; then
            DC="$DOCKER_COMPOSE --env-file .env "${env_files[@]}" $cmd"
        else
            DC="$DOCKER_COMPOSE "${env_files[@]}" $cmd"
        fi
    else
        DC="$DOCKER_COMPOSE $cmd"
    fi
    if ! $DC; then 
        printwarn "$L_COMPOSE_ERROR"
        exit 1
    fi
    cd ~
}

dockerCompose(){
    composeCMD "up -d"
    sleep 10
    cleanDockerImages
    printmsg "$L_DOCKERSUCCESS"
    if [[ $1 != "first" ]]; then
        exit 0
    fi
}

dockerUpdate(){
    composeCMD "pull --ignore-pull-failures"
    dockerCompose "first"
    custom-ha-addons
    nextcloud-upgrade
}

containerStatus(){
    printmsg "Docker Container Status"
    docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
}

addaliases(){
    if [ ! -f "~/.bash_aliases" ];then
        touch ~/.bash_aliases
    fi
    if ! cat ~/.bash_aliases | grep -q ei23.sh; then
        echo "alias ei23='bash ~/ei23.sh'" >> ~/.bash_aliases
        echo "alias dockerexec='docker exec -it'" >> ~/.bash_aliases
        echo "alias foldersizes='sudo du -h --max-depth=1'" >> ~/.bash_aliases
        source ~/.bashrc
    fi
}

add_new_functions(){
    # setsshlogo
    system_32bit
    # install_docker "${OS}"
}

set_ip() {
    (cat /etc/environment | grep -v "EI23_PING_IP"); echo "EI23_PING_IP=$1" | sudo tee -a /etc/environment
}

generate_password(){
   chars() { echo ${1:RANDOM%${#1}:1}; }
   {
      chars '0123456789'
      chars 'abcdefghijklmnopqrstuvwxyz'
      chars 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      for i in $( seq 1 $(( 12 )) ) # password has 12 chars
      do
         chars '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
      done
   } | sort -R | tr -d '\n'
   echo ""
}

buildDocs(){
    sudo bash -c 'cd /home/'$IAM'/ei23-docker/volumes/ei23/; source .venv/bin/activate; cd docs/; mkdocs build; deactivate'
}

fullUpdate() {
    echo "$(date +%Y%m%d)" > update_ei23_date.log
    echo "$(date +%Y-%m-%d_%T) - full update started" >> update_ei23.log
    aptUpdate $L_UPDATING
    add_new_functions
    if [ -d "$HOME/.node-red/" ]; then
        noderedUpdate $L_UPDATING
        sudo service nodered restart
    fi
    pipUpdate $L_UPDATING
    if [[ $1 == "" ]]; then # don't if nodocker set
        dockerUpdate
    fi
    echo "$(date +%Y-%m-%d_%T) - full update finished" >> update_ei23.log
    exit 0
}


install_docker() {
  local os="${1}"

  if [[ "${os}" == "debian" ]]; then
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl gnupg lsb-release
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
    sudo DEBIAN_FRONTEND=noninteractive apt-get update -y
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    return 0
  elif [[ "${os}" == "ubuntu" || "${os}" == "pop" ]]; then
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl gnupg lsb-release
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
    sudo DEBIAN_FRONTEND=noninteractive apt-get update -y
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    return 0
  elif [[ "${os}" == "centos" ]]; then
    sudo yum install -y yum-utils
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install -y --allowerasing docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo systemctl start docker
    sudo systemctl enable docker
    return 0
  elif [[ "${os}" == "rocky" ]]; then
    sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo systemctl start docker
    sudo systemctl enable docker
    return 0
  elif [[ "${os}" == "fedora" ]]; then
    sudo dnf -y install dnf-plugins-core
    sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
    sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo systemctl start docker
    sudo systemctl enable docker
    return 0
  elif [[ "${os}" == "arch" || "${os}" == "manjaro" ]]; then
    sudo pacman -Sy --noconfirm docker docker-compose
    sudo systemctl start docker.service
    sudo systemctl enable docker.service
    return 0
  else
    return 1
  fi
}

cleanDockerImages(){
# /usr/bin/expect<<EOF
#     spawn docker image prune -a -f
#     expect "*continue*"
#     send -- "y\r"
#     expect eof
# EOF
    # cd ~/ei23-docker/; $DOCKER_COMPOSE up -d --remove-orphans; cd ~
    docker image prune -a -f
    printmsg "$L_DOCKERDELETE"
}

rootanduserpassword() {
	    printmsg "$L_PASSWORDFOR $IAM"
        sudo passwd $IAM
        printmsg "$L_PASSWORDFOR root"
        sudo passwd root
}

install-rtl-sdr() {
        printstatus "$L_INSTALLING SDR-Stick"
        sudo rm -r $HOME/wrk/rtl_433
        sudo rm -r $HOME/wrk/rtl-sdr
        mkdir ~/wrk && cd ~/wrk
        git clone git://git.osmocom.org/rtl-sdr.git
        cd rtl-sdr/
        mkdir build
        cd build
        cmake ../ -DINSTALL_UDEV_RULES=ON
        make
        sudo make install
        sudo ldconfig
        sudo cp ../rtl-sdr.rules /etc/udev/rules.d/
        echo "blacklist dvb_usb_rtl28xxu" | sudo tee /etc/modprobe.d/blacklist-rtl.conf
        sudo udevadm control --reload-rules && udevadm trigger
        cd ~/wrk
        git clone https://github.com/merbanan/rtl_433.git
        cd rtl_433/ && mkdir build && cd build && cmake ../ && make
        sudo make install
        sudo rm -r $HOME/wrk/
}

mosquittopassword() {
    adminname=$(whiptail --inputbox "$L_MQTTADMIN" 8 60 $adminname 3>&1 1>&2 2>&3)
    if [[ -z "${adminname// }" ]]; then
        adminname="admin"
    fi
    clear
    printmsg "$L_CONFIGURE Mosquitto / MQTT $L_PLEASEWAIT"
    cd ~/ei23-docker/
    sudo chown -R 1883:1883 $DOCKERDIR/volumes/mosquitto/
    sudo sed -i -e "s#\# password_file#password_file#" $DOCKERDIR/volumes/mosquitto/config/mosquitto.conf
    sudo sed -i -e "s#\password_file#\# password_file#" $DOCKERDIR/volumes/mosquitto/config/mosquitto.conf
    $DOCKER_COMPOSE restart mosquitto
    printmsg "$L_PASSWORDFOR Mosquitto / MQTT..."
    docker exec -it mosquitto mosquitto_passwd -c /mosquitto/config/pwfile $adminname
    # set passwordline in mosquitto conf
    sudo sed -i -e "s#\# password_file#password_file#" $DOCKERDIR/volumes/mosquitto/config/mosquitto.conf
    $DOCKER_COMPOSE restart mosquitto
    cd ~
}

piholepassword(){
    if [ -d "$DOCKERDIR/volumes/pihole/etc-pihole" ]; then
        printmsg "$L_PASSWORDFOR PiHole"
        docker exec -it pihole pihole -a -p
    fi
}

noderedpassword(){
        cd ~/.node-red/
        adminpass=$(whiptail --passwordbox "$L_PASSWORDFOR NodeRED" 8 60 3>&1 1>&2 2>&3)
        if [[ -z "${adminpass// }" ]]; then
            printerror "$L_NOPASSWD"; exit
        fi
        bcryptadminpass=$(node -e "console.log(require('bcryptjs').hashSync(process.argv[1], 8));" $adminpass)
        clear
        printmsg "$L_NODEREDSETTINGS"
        cd ~
        echo ""
        echo $bcryptadminpass
        echo ""
}

command_exists() {
	command -v "$@" >/dev/null 2>&1
}

showTermsOfUse(){
    # Terms of use
    whiptail --title "$L_TERMSOFUSE1" --ok-button "$L_TERMSOFUSE1OK" --msgbox "$L_TERMSOFUSE1TEXT" 20 78
    if (whiptail --title "$L_TERMSOFUSE2" --yesno --no-button "$L_TERMSOFUSE2ACCEPT" --yes-button "$L_TERMSOFUSE2DECLINE" "$L_TERMSOFUSE2TEXT" 20 78); then
        exit 0
    fi
}

otherappsinfo(){
    # Other Apps
    whiptail --title "INFO" --ok-button "OK COOL!" --msgbox "$L_OTHERAPPSINFO" 20 78
}

show_shortcuts(){
    echo "You can use this shortcuts"
    echo "--------------------------"
    echo "ei23 backup            - creates a backup"
    echo "ei23 dc                - runs Docker compose"
    echo "ei23 docs              - builds your own docs"
    echo "ei23 dstats            - show Docker status"
    echo "ei23 du                - updates Docker images"
    echo "ei23 ei23update        - updates ei23-script only"
    echo "ei23 fullreset X       - reinstall container X and delete all its data"
    echo "ei23 ha-addons         - updates Home Assistant custom addons"
    echo "ei23 install-rtl-sdr   - install RTL-SDR software"
    echo "ei23 newfunctions      - add new functions from script-updates"
    echo "ei23 setip             - set new default IP"
    echo "ei23 update            - run full update"
}


# Short Commands
if [[ $1 == "backup" ]]; then
    bash "$DOCKERDIR/backup.sh"
    exit 0
fi

if [[ $1 == "dc" ]]; then
    dockerCompose
fi

if [[ $1 == "docs" ]]; then
    buildDocs
    exit 0
fi

if [[ $1 == "dstats" ]]; then
    containerStatus
    exit 0
fi

if [[ $1 == "du" ]]; then
    dockerUpdate
    exit 0
fi

if [[ $1 == "ei23update" ]]; then
    bash "$DOCKERDIR/update.sh"
    exit 0
fi

if [[ $1 == "ei23upgrade" ]]; then
    ei23_supervisor
    exit 0
fi

if [[ $1 == "fullreset" ]]; then
    program="X"
    program=$2
    cd ~/ei23-docker/
    composeCMD "stop $program"
    composeCMD "rm -f $program"
    sudo rm -r volumes/$program
    dockerCompose
    exit 0
fi

if [[ $1 == "ha-addons" ]]; then
    custom-ha-addons
    exit 0
fi

if [[ $1 == "install-rtl-sdr" ]]; then
    install-rtl-sdr
    exit 0
fi

if [[ $1 == "newfunctions" ]]; then
    add_new_functions
    exit 0
fi

if [[ $1 == "nodockerupdate" ]]; then
    bash "$DOCKERDIR/update.sh" "nodockerupdate"
    exit 0
fi

if [[ $1 == "no-docker-update" ]]; then
    fullUpdate "nodocker"
    exit 0
fi

if [[ $1 == "setip" ]]; then
    set_ip $2
    exit 0
fi

if [[ $1 == "update" ]]; then
    bash "$DOCKERDIR/update.sh" "fullupdate"
    exit 0
fi

if [[ $1 == "-h" ]]; then
    show_shortcuts
    exit 0
fi

for i in {0..20}
do
   printstatus "ei23.de - DIY Smart Home Server v$SCRIPT_VERSION" $i
   sleep 0.02
done

printstatus "ei23.de - DIY Smart Home Server v$SCRIPT_VERSION"

# test internet connection
# sudo chmod u+s /bin/ping
# if ! ping -c 1 ei23.de &> /dev/null; then
#     printerror "$L_NOINTERNET"
#     exit 1
# fi

tmp=$(ip addr | grep "state UP" | awk '{print $2}' | cut -d ':' -f 1)
tmp=$(cat /sys/class/net/$tmp/address)
tmp=$(echo -n $tmp | md5sum)
card=${tmp::-3}


# check for root - do not use root!
if [ $EUID -eq 0 ]; then
  echo "do not use sudo and make sure you are not logged in as root"
  exit 0
elif [ $(ps -o comm= -p $PPID) = "su" ]; then
  echo "do not use su"
  exit 0
else
  echo "user ok"
fi

# Check for sudo
if sudo -lU "$IAM" | grep -q "(ALL) NOPASSWD: ALL"; then
  echo "$IAM sudo checked"
else
  # if user has no sudo
  if ! sudo -v &> /dev/null; then
    echo "Please login root"
    su -c "apt-get install sudo -y; echo '$IAM ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/010_$IAM-nopasswd; sudo adduser $IAM sudo; chown 1000:1000 /home/$IAM"
  else
    echo "User already has sudo rights"
  fi
fi

if [[ $1 == *"fullupdate"* ]]; then
    fullUpdate
    exit 0
fi

# menu if already installed
if [ -d "$DOCKERDIR" ] && [ ! -f "$FIRSTFILE" ] && [[ $1 != "part1" ]] && [[ $1 != "part2" ]]; then
    mainmenu_selection=$(whiptail --title "ei23 SmartHome-Server v$SCRIPT_VERSION" --menu --notags \
        "" 20 78 10 -- \
        "ei23update" "$L_UPDATEEI    [ei23 ei23update]" \
        "update" "$L_UPDATE         [ei23 update]" \
        "backup" "$L_BACKUPDATA              [ei23 backup]" \
        "dc" "Docker Compose            [ei23 dc]" \
        "du" "Docker Update             [ei23 du]" \
        "docs" "Build Docs                [ei23 docs]" \
        "dstats" "Docker Container Status   [ei23 dstats]" \
        "help" "$L_HELP           [ei23 -h]" \
        "restore" "$L_RESTOREDATA" \
        "installapps" "$L_INSTALLAPPS" \
        "removeapps" "$L_REMOVEAPPS" \
        "passwords" "$L_PASSWORDFORALL" \
        3>&1 1>&2 2>&3)
    exitstatus=$?
    if [ $exitstatus != 0 ]; then
        exit 1
    fi
    if [[ $mainmenu_selection == "dc" ]]; then
        dockerCompose
    fi
    if [[ $mainmenu_selection == "du" ]]; then
        dockerUpdate
    fi
    if [[ $mainmenu_selection == "docs" ]]; then
        buildDocs
    fi
    if [[ $mainmenu_selection == "dstats" ]]; then
        containerStatus
    fi
    if [[ $mainmenu_selection == "help" ]]; then
        show_shortcuts
    fi
    if [[ $mainmenu_selection == "restore" ]]; then
        whiptail --title "RESTORE" --ok-button "OK" --msgbox "$L_RESTOREDATATEXT" 20 78
    fi
    if [[ $mainmenu_selection == "installapps" ]]; then
        whiptail --title "INFO" --ok-button "OK" --msgbox "$L_INSTALLAPPSTEXT" 20 78
    fi
    if [[ $mainmenu_selection == "removeapps" ]]; then
        whiptail --title "INFO" --ok-button "OK" --msgbox "$L_INSTALLAPPSTEXT" 20 78
    fi
    if [[ $mainmenu_selection == "update" ]]; then
        bash "$DOCKERDIR/update.sh" "fullupdate"
        exit 0
    fi
    if [[ $mainmenu_selection == "ei23update" ]]; then
        bash "$DOCKERDIR/update.sh"
        exit 0
    fi
    if [[ $mainmenu_selection == "backup" ]]; then
        whiptail --title "BACKUP" --ok-button "OK" --msgbox "$L_BACKUPDATATEXT" 20 78
        bash "$DOCKERDIR/backup.sh"
        exit 0
    fi
    if [[ $mainmenu_selection == "passwords" ]]; then
        rootanduserpassword
        mosquittopassword
        piholepassword
        noderedpassword
        exit 0
    fi
fi

# Installation Part 2 - after reboot
if [[ ( -f "$FIRSTFILE" || $1 == "part2" ) && $1 != "part1" ]]; then
    dockerCompose "first"
    custom-ha-addons
    
    # set OpenDNS as default DNS for Docker-Containers
    # default_gateway=$(ip route | grep default | awk '{print $3}')
    # echo -e "{\n\t\t\"dns\": [\"$default_gateway\", \"208.67.222.222\"]\n}" | sudo tee /etc/docker/daemon.json

    mosquittopassword
    piholepassword
    sudo rm $FIRSTFILE
    # finished installation
    printstatus "$L_INSTALLCOMPLETE"
    exit 0
fi

# Installation Part 1 - fresh install
if [ ! -d "$DOCKERDIR" ] || [[ $1 == "part1" ]]; then
    # install dependencies
    sudo apt-get update
    [ ! -x /usr/bin/sudo ] && apt-get -y update > /dev/null 2>&1 && apt-get -y install sudo
    sudo apt-get -y install whiptail ccze net-tools
    
    addaliases
    # Check for Raspberry System
    if [ -f "/boot/cmdline.txt" ]; then
        (sudo crontab -l | grep -v "@reboot bash /home/$IAM/ei23-docker/led_service.sh &"; echo "@reboot bash /home/$IAM/ei23-docker/led_service.sh &") | sudo crontab -
    fi

    setsshlogo
    
    showTermsOfUse
    otherappsinfo
    # newhostname=$(whiptail --title "Server Hostname" --inputbox "$L_CHOOSESERVERNAME" 8 60 $newhostname 3>&1 1>&2 2>&3)

    # Enable SSH root-login
    if [ -f "/etc/ssh/sshd_config" ]; then
        sudo sed -i -e 's#\#PermitRootLogin prohibit-password#PermitRootLogin yes#' /etc/ssh/sshd_config
    fi

    MYMENU=$(whiptail --title "ei23 SmartHome-Server" --notags --separate-output --checklist \
        "\n$L_MENUMANUAL" 20 78 12 \
        "passwords1" "$L_PASSWORDFOR NodeRED" ON \
        "dashpassword" "$L_PASSWORDFOR NodeRED-Dashboard    " OFF \
        "passwords2" "$L_NEWROOTANDUSER" ON \
        "dockertext" "_________Docker Container" ON \
        "bitwarden" "Bitwarden" ON \
        "esphome" "ESPHome" ON \
        "grafana" "Grafana" ON \
        "homeassistant" "HomeAssistant" ON \
        "influxdb18" "InfluxDB 1.8" OFF \
        "influxdb2" "InfluxDB 2" OFF \
        "motioneye" "MotionEye" OFF \
        "mqtt-explorer" "MQTT-explorer" ON \
        "nextcloudofficial" "Nextcloud" OFF \
        "nginxproxymanger" "NGINX Proxymanager" OFF \
        "paperlessngx" "PaperlessNGX" OFF \
        "pihole" "Pihole" OFF \
        "portainer" "Portainer" ON \
        "tasmoadmin" "Tasmoadmin" OFF \
        "timescaledb" "Timescaledb" OFF \
        "traefik" "Traefik SSL Proxy " OFF \
        "vscode" "VSCode ConfigEditor" ON \
        "wireguard" "Wireguard VPN-Server" OFF \
        "stufftext" "_________Extras" ON \
        "log2ram" "Log2RAM (SD-Card)" OFF \
        "nonodered" "No-NodeRED" OFF \
        "nodocker" "No-Docker" OFF \
        "rpiclone" "RPI-clone" OFF \
        "sdr" "SDR DVB-T Stick" OFF \
        3>&1 1>&2 2>&3)
        exitstatus=$?
        if [ $exitstatus != 0 ]; then
            exit 0
        fi


    # Passwords ------------------------
    if [[ $MYMENU == *"passwords1"* ]]; then
        if [[ $MYMENU == *"dashpassword"* ]]; then
            username=$(whiptail --inputbox "$L_USERNAMEFOR NodeRED Dashboard" 8 60 $username 3>&1 1>&2 2>&3)
            if [[ -z "${username// }" ]]; then
                printmsg "$L_NONAMEABORT"; 
                exit 1
            fi
            
            userpass=$(whiptail --passwordbox "$L_PASSWORDFOR NodeRED Dashboard" 8 60 3>&1 1>&2 2>&3)
            if [[ -z "${userpass// }" ]]; then
                printerror "$L_NOPASSWD"; 
                exit 1
            fi
            
            userpass2=$(whiptail --passwordbox "$L_CONFIRMPASSWORD" 8 60 3>&1 1>&2 2>&3)
            if  [ $userpass2 == "" ]; then
                printerror "$L_NOPASSWD"; 
                exit 1
            fi
            if  [ $userpass != $userpass2 ]
            then
                printerror "$L_PASSWDMATCH"; 
                exit 1
            fi
        fi
        adminname=$(whiptail --inputbox "$L_USERNAMEFOR NodeRED" 8 60 $adminname 3>&1 1>&2 2>&3)
        if [[ -z "${adminname// }" ]]; then
            printerror "$L_NONAMEABORT"
            exit 1
        fi
        
        adminpass=$(whiptail --passwordbox "$L_PASSWORDFOR NodeRED" 8 60 3>&1 1>&2 2>&3)
        if [[ -z "${adminpass// }" ]]; then
            printerror "$L_NOPASSWD"; 
            exit 1
        fi
        
        adminpass2=$(whiptail --passwordbox "$L_CONFIRMPASSWORD" 8 60 3>&1 1>&2 2>&3)
        if  [ $adminpass2 == "" ]; then
            printerror "$L_NOPASSWD"; 
            exit 1
        fi
        if  [ $adminpass != $adminpass2 ]; then
            printerror "$L_PASSWDMATCH"; 
            exit 1
        fi
    fi


    if [[ $MYMENU == *"passwords2"* ]]; then
        rootanduserpassword
    fi

    # Passwords ------------------------

    aptUpdate $L_INSTALLING

    installPackages

    sudo wget "https://ei23.de/softwarehub/smarthome/USERID/$card/$SCRIPT_VERSION/ei23-docker.zip" -O ei23-docker.zip
    sudo unzip ei23-docker.zip -d $HOME/ei23-docker/
    sudo rm ei23-docker.zip

    ei23_supervisor

    pipUpdate $L_INSTALLING

    # RTL-SDR
    if [[ $MYMENU == *"sdr"* ]]; then
        install-rtl-sdr
    fi

    # NODE RED ---------------------------
    if [[ $MYMENU != *"nonodered"* ]]; then
        mkdir $HOME/.node-red/
        sudo mv $HOME/ei23-docker/settings.txt $HOME/.node-red/settings.js
        noderedUpdate $L_INSTALLING
        cd ~/.node-red/
        if [[ $MYMENU == *"passwords1"* ]]; then
            bcryptadminpass=$(node -e "console.log(require('bcryptjs').hashSync(process.argv[1], 8));" $adminpass)
            bcryptuserpass=$(node -e "console.log(require('bcryptjs').hashSync(process.argv[1], 8));" $userpass)
            cp settings.js settings.js.bak-pre-crypt

            sed -i -e "s#\/\/adminAuth#adminAuth#" $HOME/.node-red/settings.js
            sed -i -e "s#NRUSERNAMEA#$adminname#" $HOME/.node-red/settings.js
            sed -i -e "s#NRPASSWORDA#$bcryptadminpass#" $HOME/.node-red/settings.js
            if [[ $MYMENU == *"dashpassword"* ]]; then
                sed -i -e "s#\/\/httpNodeAuth#httpNodeAuth#" $HOME/.node-red/settings.js
                sed -i -e "s#NRUSERNAMEU#$username#" $HOME/.node-red/settings.js
                sed -i -e "s#NRPASSWORDU#$bcryptuserpass#" $HOME/.node-red/settings.js
            fi
        fi

        # install ei23 NodeRED Flow Library
        sudo mkdir --parents $HOME/.node-red/lib/flows/ei23/
        sudo mv $HOME/ei23-docker/flows/* $HOME/.node-red/lib/flows/ei23/
        sudo rm -r $HOME/ei23-docker/flows/
        sudo chown -R $IAM $HOME/.node-red/lib/

        
        sudo systemctl enable nodered.service
        cd ~
        sudo rm update-nodejs-and-nodered
    fi
    # NODE RED ---------------------------

    if [[ $MYMENU == *"log2ram"* ]]; then
        printstatus "$L_INSTALLING Log2Ram"
        cd
        git clone https://github.com/azlux/log2ram.git
        cd log2ram
        chmod +x install.sh
        sudo ./install.sh
        cd
        sudo sed -i -e 's#SIZE=40M#SIZE=96M#' /etc/log2ram.conf 
    fi

    if [[ $MYMENU == *"rpiclone"* ]]; then
        printstatus "$L_INSTALLING RPI-Clone"
        cd
        sudo git clone https://github.com/billw2/rpi-clone.git
        cd rpi-clone
        sudo cp rpi-clone /usr/local/sbin
        cd
        sudo rm -r rpi-clone
    fi

    system_32bit

    if [[ $MYMENU != *"nodocker"* ]]; then
        yml_build(){
            printf "\n\n" >> "$DOCKERDIR/docker-compose.yml"
            cat "$DOCKERDIR/compose_templates/$1.yml" >> "$DOCKERDIR/docker-compose.yml"
            sudo sed -i -e "/$1/s/\"active\":false,/\"active\":true, /" $DOCKERDIR/volumes/ei23/web/static/programs.json
            if [[ "$1" == *"nextcloudofficial"* ]]; then
                sudo sed -i '/# custom_networks_here/ r '$DOCKERDIR/compose_templates/nextcloud-network.yml $DOCKERDIR/docker-compose.yml
            fi
        }

        for dockercontainer in awtrix bitwarden deconz domoticz duplicati ei23 esphome fhem fireflyiii gotify grafana grocy homeassistant homebridge influxdb18 influxdb2 iobroker mosquitto motioneye mqtt-explorer nextcloudofficial nextcloudpi nginxproxymanger octoprint openhab paperlessngx pihole portainer rhasspy tasmoadmin teamspeak timescaledb traefik vscode wireguard zigbee2mqtt; do
            if [[ $MYMENU == *"${dockercontainer}"* ]]; then
                yml_build "${dockercontainer}"
            fi
        done

        # set random generated passwords
        while cat "$DOCKERDIR/docker-compose.yml" | grep -q "password_placeholder"; do
            sudo sed -i -e '0,/password_placeholder/s//'$(generate_password)'/' "$DOCKERDIR/docker-compose.yml" # different passwords
        done
        sudo sed -i -e 's/password1_placeholder/'$(generate_password)'/' "$DOCKERDIR/docker-compose.yml" # same passwords

        # set new hostname
        # sudo sed -i -e "s#HomePi#$newhostname#" $DOCKERDIR/docker-compose

        printstatus "$L_INSTALLING Docker"
        if command_exists docker; then
            printstatus "docker $L_ALREADYINSTALLED"
        else
            printstatus "$L_INSTALLING Docker"
            install_docker "${OS}"
            sudo usermod -aG docker $IAM
        fi

        if (whiptail --title "$L_REBOOT" --yesno "$L_REBOOTTEXT" 20 78); then
            sudo reboot
        fi
    fi

    if [[ $MYMENU == *"nodocker"* ]]; then
        sudo rm $FIRSTFILE
        printstatus "RESTART IN 10 SEC"
        sleep 10
        sudo reboot
    fi

fi
