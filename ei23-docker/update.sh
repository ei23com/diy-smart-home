cd ~
getData(){ 
    wget "https://ei23.de/softwarehub/smarthome/USERID/DEVICEID/VERSIONNR/ei23.sh" -O ei23.sh
    wget "https://ei23.de/softwarehub/smarthome/USERID/DEVICEID/VERSIONNR/ei23-update.zip" -O ei23-update.zip
    sudo unzip -o ei23-update.zip -d $HOME/ei23-docker/
    sudo systemctl stop ei23.service; sudo systemctl start ei23.service
}
if [[ $1 == "nodockerupdate" ]]; then
    getData
    bash ei23.sh "no-docker-update"
    exit 1
fi
if [[ $1 == "fullupdate" ]] || [[ $1 == "" ]]; then
    [[ $1 == "fullupdate" ]] && command="fullup2" || command="part2"
    getData
    bash $HOME/ei23-docker/update.sh $command
    exit 1
fi
if [[ $1 == "part2" ]] || [[ $1 == "fullup2" ]]; then
    # DONTCHANGE
    sudo mkdir --parents $HOME/.node-red/lib/flows/ei23/
    sudo mv $HOME/ei23-docker/flows/* $HOME/.node-red/lib/flows/ei23/
    sudo rm -r $HOME/ei23-docker/flows/
    sudo chown -R $(whoami) $HOME/.node-red/lib/
    if [[ $1 == "fullup2" ]]; then
        cd ~
        bash ei23.sh "fullupdate"
    fi
    sudo rm ei23-update.zip
    exit 1
fi
