# Hardware Watchdog with SSH Check on Debian

This guide configures the hardware watchdog on Debian. It ensures the server performs a hard reboot automatically if the system freezes completely **or** if essential services like SSH (Port 22) become unresponsive (even if pings still go through).

---

### Manual Setup Guide

#### Step 0: Avoid Conflicts (Disable Systemd Watchdog)
Since only one application can claim the hardware interface `/dev/watchdog` at a time, the built-in systemd watchdog must be disabled.

1. Open systemd configuration:
   ```bash
   sudo nano /etc/systemd/system.conf
   ```
2. Ensure the `RuntimeWatchdogSec` line is commented out or set to `0`:
   ```ini
   #RuntimeWatchdogSec=0
   ```
3. Reload systemd configuration:
   ```bash
   sudo systemctl daemon-reload
   ```

#### Step 1: Install Required Packages
Install the watchdog daemon and `netcat` (needed for testing the SSH port):
```bash
sudo apt update
sudo apt install watchdog netcat-openbsd -y
```

#### Step 2: Enable Intel Hardware Watchdog
For systems with Intel processors, the hardware watchdog is controlled by the `iTCO_wdt` kernel module.

1. Check if the watchdog device exists:
   ```bash
   ls -l /dev/watchdog*
   ```
2. If not found, load the module manually and add it for boot persistence:
   ```bash
   sudo modprobe iTCO_wdt
   echo "iTCO_wdt" | sudo tee -a /etc/modules
   ```

#### Step 3: Configure Watchdog Daemon
Open the main daemon configuration:
```bash
sudo nano /etc/watchdog.conf
```
Enable/adjust the following settings:
```ini
watchdog-device = /dev/watchdog
interval = 10
watchdog-timeout = 60
max-load-1 = 24
min-memory = 25600
test-directory = /etc/watchdog.d
```

#### Step 4: Configure SSH Check Script
1. Create the test script:
   ```bash
   sudo nano /etc/watchdog.d/ssh_check
   ```
2. Paste the following contents (tests locally if port 22 responds within 3 seconds):
   ```bash
   #!/bin/sh
   nc -z -w 3 localhost 22
   ```
3. Make it executable:
   ```bash
   sudo chmod +x /etc/watchdog.d/ssh_check
   ```

> ⚠️ **IMPORTANT (Dry Run):** Execute the script manually (`/etc/watchdog.d/ssh_check`) before starting the service. Check the exit code with `echo $?`. The output **must be 0**, otherwise your system will enter an immediate reboot loop!

#### Step 5: Enable & Start Service
```bash
sudo systemctl enable watchdog
sudo systemctl start watchdog
sudo systemctl status watchdog
```

---

### Automated Setup Scripts (EN)

#### Script 1: Intel CPU

```bash
#!/bin/bash

# --- OUTPUT COLORS ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Watchdog Installation Script for Debian (Intel CPU) ===${NC}"

# 1. Root Check
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Please run this script as root (or with sudo)!${NC}"
  exit 1
fi

# 2. Disable systemd Watchdog (Prevent Conflicts)
echo -e "${YELLOW}[1/6] Disabling systemd internal watchdog...${NC}"
if [ -f /etc/systemd/system.conf ]; then
  cp /etc/systemd/system.conf /etc/systemd/system.conf.bak
  sed -i -E 's/^[#]?\s*RuntimeWatchdogSec\s*=.*/#RuntimeWatchdogSec=0/g' /etc/systemd/system.conf
  systemctl daemon-reload
  echo -e "${GREEN}[OK] systemd internal watchdog disabled.${NC}"
else
  echo -e "${YELLOW}[INFO] /etc/systemd/system.conf not found. Skipping.${NC}"
fi

# 3. Install Packages
echo -e "${YELLOW}[2/6] Installing packages (watchdog, netcat-openbsd)...${NC}"
apt-get update -qq
apt-get install -y watchdog netcat-openbsd > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Packages installed successfully.${NC}"
else
  echo -e "${RED}[ERROR] Package installation failed!${NC}"
  exit 1
fi

# 4. Load & Register Kernel Module
echo -e "${YELLOW}[3/6] Configuring Intel hardware module (iTCO_wdt)...${NC}"
modprobe iTCO_wdt 2>/dev/null
if [ $? -eq 0 ]; then
  if ! grep -qxF "iTCO_wdt" /etc/modules; then
    echo "iTCO_wdt" >> /etc/modules
  fi
  echo -e "${GREEN}[OK] Module iTCO_wdt loaded and registered permanently.${NC}"
else
  echo -e "${YELLOW}[WARNING] Module iTCO_wdt could not be loaded.${NC}"
  echo -e "          (Ignore this if you are not using an Intel system).${NC}"
fi

# 5. Configure watchdog.conf
echo -e "${YELLOW}[4/6] Configuring /etc/watchdog.conf...${NC}"

set_watchdog_option() {
  local key=$1
  local value=$2
  local file="/etc/watchdog.conf"
  if grep -qE "^#?\s*$key\s*=" "$file"; then
    sed -i -E "s|^#?\s*$key\s*=.*|$key = $value|" "$file"
  else
    echo "$key = $value" >> "$file"
  fi
}

cp /etc/watchdog.conf /etc/watchdog.conf.bak

set_watchdog_option "watchdog-device" "/dev/watchdog"
set_watchdog_option "interval" "10"
set_watchdog_option "watchdog-timeout" "60"
set_watchdog_option "max-load-1" "24"
set_watchdog_option "min-memory" "25600"
set_watchdog_option "test-directory" "/etc/watchdog.d"

echo -e "${GREEN}[OK] /etc/watchdog.conf configured (Backup created at .bak).${NC}"

# 6. Create SSH Check Script
echo -e "${YELLOW}[5/6] Creating SSH check script...${NC}"
mkdir -p /etc/watchdog.d

cat << 'EOF' > /etc/watchdog.d/ssh_check
#!/bin/sh
# Checks if local port 22 responds within 3 seconds.
nc -z -w 3 localhost 22
EOF

chmod +x /etc/watchdog.d/ssh_check
echo -e "${GREEN}[OK] Check script created at /etc/watchdog.d/ssh_check.${NC}"

# 7. Safety Dry Run
echo -e "${YELLOW}[6/6] Executing safety dry run...${NC}"
/etc/watchdog.d/ssh_check
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Dry run successful! SSH responded as expected.${NC}"
  echo -e "${YELLOW}Enabling and starting watchdog service...${NC}"
  systemctl enable watchdog
  systemctl start watchdog
  echo -e "${GREEN}=== INSTALLATION COMPLETED SUCCESSFULLY! ===${NC}"
else
  echo -e "${RED}[WARNING] Safety dry run failed!${NC}"
  echo -e "${RED}          Local SSH port (22) did not respond.${NC}"
  echo -e "${YELLOW}Possible reasons:${NC}"
  echo -e " - Your SSH service runs on a port other than 22."
  echo -e " - The SSH service is currently not active."
  echo -e ""
  echo -e "${RED}The watchdog was NOT enabled to prevent a reboot loop!${NC}"
  echo -e "${YELLOW}Please fix the issue and enable the service manually:${NC}"
  echo -e "sudo systemctl enable --now watchdog"
fi
```

#### Script 2: Raspberry Pi

```bash
#!/bin/bash

# --- OUTPUT COLORS ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Watchdog Installation Script for RASPBERRY PI ===${NC}"

# 1. Root Check
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Please run this script as root (or with sudo)!${NC}"
  exit 1
fi

# 2. Disable systemd Watchdog
echo -e "${YELLOW}[1/7] Disabling systemd internal watchdog...${NC}"
if [ -f /etc/systemd/system.conf ]; then
  cp /etc/systemd/system.conf /etc/systemd/system.conf.bak
  sed -i -E 's/^[#]?\s*RuntimeWatchdogSec\s*=.*/#RuntimeWatchdogSec=0/g' /etc/systemd/system.conf
  systemctl daemon-reload
  echo -e "${GREEN}[OK] systemd internal watchdog disabled.${NC}"
fi

# 3. Enable Hardware Watchdog in Pi Firmware
echo -e "${YELLOW}[2/7] Enabling hardware watchdog in Pi boot config...${NC}"
CONFIG_FILE=""
if [ -f /boot/firmware/config.txt ]; then
  CONFIG_FILE="/boot/firmware/config.txt"  # New path (Bookworm)
elif [ -f /boot/config.txt ]; then
  CONFIG_FILE="/boot/config.txt"           # Old path (Buster/Bullseye)
fi

if [ -n "$CONFIG_FILE" ]; then
  if ! grep -q "dtparam=watchdog=on" "$CONFIG_FILE"; then
    cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    echo "dtparam=watchdog=on" >> "$CONFIG_FILE"
    echo -e "${GREEN}[OK] Watchdog enabled in $CONFIG_FILE. (Backup created).${NC}"
    REBOOT_NEEDED=true
  else
    echo -e "${GREEN}[OK] Watchdog is already active in $CONFIG_FILE.${NC}"
    REBOOT_NEEDED=false
  fi
else
  echo -e "${RED}[ERROR] No config.txt found! Is this Raspberry Pi OS?${NC}"
  exit 1
fi

# 4. Install Packages
echo -e "${YELLOW}[3/7] Installing packages (watchdog, netcat-openbsd)...${NC}"
apt-get update -qq
apt-get install -y watchdog netcat-openbsd > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Packages installed successfully.${NC}"
else
  echo -e "${RED}[ERROR] Package installation failed!${NC}"
  exit 1
fi

# 5. Configure watchdog.conf (Raspberry Pi specific settings)
echo -e "${YELLOW}[4/7] Configuring /etc/watchdog.conf for Raspberry Pi...${NC}"

set_watchdog_option() {
  local key=$1
  local value=$2
  local file="/etc/watchdog.conf"
  if grep -qE "^#?\s*$key\s*=" "$file"; then
    sed -i -E "s|^#?\s*$key\s*=.*|$key = $value|" "$file"
  else
    echo "$key = $value" >> "$file"
  fi
}

cp /etc/watchdog.conf /etc/watchdog.conf.bak

# Specific Pi values (Maximum timeout is 15s for Pi hardware)
set_watchdog_option "watchdog-device" "/dev/watchdog"
set_watchdog_option "interval" "5"                # Check every 5 seconds
set_watchdog_option "watchdog-timeout" "15"        # Raspberry Pi hardware limit!
set_watchdog_option "max-load-1" "24"
set_watchdog_option "min-memory" "12800"
set_watchdog_option "test-directory" "/etc/watchdog.d"

echo -e "${GREEN}[OK] /etc/watchdog.conf configured.${NC}"

# 6. Create SSH Check Script
echo -e "${YELLOW}[5/7] Creating SSH check script...${NC}"
mkdir -p /etc/watchdog.d

cat << 'EOF' > /etc/watchdog.d/ssh_check
#!/bin/sh
# Checks if port 22 responds locally.
nc -z -w 3 localhost 22
EOF

chmod +x /etc/watchdog.d/ssh_check
echo -e "${GREEN}[OK] Check script created at /etc/watchdog.d/ssh_check.${NC}"

# 7. Safety Dry Run
echo -e "${YELLOW}[6/7] Executing safety dry run...${NC}"
/etc/watchdog.d/ssh_check
SSH_OK=$?

if [ $SSH_OK -ne 0 ]; then
  echo -e "${RED}[ERROR] Safety dry run failed! SSH did not respond.${NC}"
  echo -e "${RED}        Service will not be started for protection.${NC}"
  exit 1
fi
echo -e "${GREEN}[OK] Dry run successful! SSH responded.${NC}"

# 8. Finalize Setup
echo -e "${YELLOW}[7/7] Finalizing installation...${NC}"
if [ "$REBOOT_NEEDED" = true ]; then
  echo -e "${YELLOW}------------------------------------------------------------${NC}"
  echo -e "${YELLOW}ATTENTION: You must REBOOT the Raspberry Pi once!${NC}"
  echo -e "${YELLOW}The hardware watchdog (/dev/watchdog) will only be exposed${NC}"
  echo -e "${YELLOW}by the kernel after a reboot. Service will auto-start afterwards.${NC}"
  echo -e "${YELLOW}------------------------------------------------------------${NC}"
  systemctl enable watchdog
else
  echo -e "${YELLOW}Enabling and starting watchdog service...${NC}"
  systemctl enable watchdog
  systemctl start watchdog
  echo -e "${GREEN}=== DONE! Watchdog is running and protecting the Pi. ===${NC}"
fi
```