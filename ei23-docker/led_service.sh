# Raspberry Pi LED Controller by ei23
# this service can be edited with sudo crontab -e 
# the line is "@reboot bash /home/pi/ei23-docker/led_service.sh &"

# --- blink styles --- (echo "timer" | sudo tee /sys/class/leds/led[1,0]/trigger)
# - gpio - controlled through GPIO (off by default)
# - heartbeat - heartbeat-like pulse
# - timer - pulse every second
# - input - under-voltage detection
# - mmc0 - memory I/O
# - cpu0 - CPU activity

# --- on/of --- (echo 0 | sudo tee /sys/class/leds/led[1,0]/brightness)
# - 0 - turn off
# - 1 - turn on

# --- example ---
# blink GREEN LED
# echo "timer" | sudo tee /sys/class/leds/led0/trigger
# blink RED LED
# echo "timer" | sudo tee /sys/class/leds/led1/trigger

#   - Programmstart: blinkt rot + dauer grün
#   - rot aus wenn docker start
#   - blinkt grün wenn netzwerk (bei kunden über nodered / feste ip)
#   - while schleifen
#   - (bei kunden) heartbeat pro minute (cronjob +1 minütlich, log und reset stündlich)

# 1: fully turn on green led and blink red led at boot
echo "none" | sudo tee /sys/class/leds/led0/trigger
echo 1 | sudo tee /sys/class/leds/led0/brightness
echo "timer" | sudo tee /sys/class/leds/led1/trigger

docker_state=false
network_state=false

while true
do
    if [[ $EI23_PING_IP ]] ; then
        # Set your custom ping ip with (cat /etc/environment | grep -v "EI23_PING_IP"); echo "EI23_PING_IP=10.8.0.1" | sudo tee -a /etc/environment
        ipadress=$EI23_PING_IP
    else
        # Default Gateway
        ipadress=$(ip route | grep default | awk '{print $3}') 
    fi
    
    # 2: stop red led blinking if default gateway is pingable
    if ping -c 1 $ipadress > /dev/null; then network=true; else network=false; fi
    if [ "$network" != "$network_state" ] ; then
        if $network; then 
            echo "none" | sudo tee /sys/class/leds/led1/trigger
            echo 0 | sudo tee /sys/class/leds/led1/brightness
        else    
            echo "timer" | sudo tee /sys/class/leds/led1/trigger
        fi
        network_state=$network
    fi

    # 3: heartbeat green led if ei23 docker is working
    if docker ps --filter "name=ei23" | grep "ei23" > /dev/null; then docker=true; else docker=false; fi
    if [ "$docker" != "$docker_state" ]  ; then
        if $docker; then 
            echo "heartbeat" | sudo tee /sys/class/leds/led0/trigger; 
        else    
            echo "none" | sudo tee /sys/class/leds/led0/trigger
            echo 1 | sudo tee /sys/class/leds/led0/brightness
        fi
        docker_state=$docker
    fi
    sleep 30
done