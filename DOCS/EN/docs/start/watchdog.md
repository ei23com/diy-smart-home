# Hardware Watchdog with SSH Check (Debian & Raspberry Pi)

This guide configures a hardware watchdog. It ensures the system performs a hard reboot automatically if the operating system freezes completely **or** if essential services like SSH (Port 22) become unresponsive (even if pings still go through).

There are two variants:

- **Debian / Intel machine (x86 PC):** hardware watchdog via the kernel module `iTCO_wdt` (fallback: `softdog`)
- **Raspberry Pi:** hardware watchdog via the firmware (`dtparam=watchdog=on`)

!!! info "Safety mechanisms (prevent reboot loops)"
    - **`retry-timeout`**: 120 seconds of fault tolerance on PCs, 60 seconds on the Pi
    - **`min-memory` disabled**: prevents false positives caused by the Linux RAM cache
    - **5 minute grace period** after boot: during the first 300 seconds the check script always reports success
    - **Dry run** before enabling: if SSH does not answer, the service is not started at all
    - **systemd dependency**: the watchdog only starts after `ssh.service`
    - **`systemctl unmask watchdog`**: lifts an emergency mask that may still be active

---

### Manual Setup Guide

#### Step 0: Lift Emergency Mask & Disable Systemd Watchdog
Since only one application can claim the hardware interface `/dev/watchdog` at a time, the built-in systemd watchdog must be disabled.

```bash
# Lift a possibly active mask (e.g. after a reboot loop)
sudo systemctl unmask watchdog 2>/dev/null
sudo systemctl stop watchdog 2>/dev/null
```

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

#### Step 2: Provide the Hardware Watchdog

**Intel / x86 PC (iTCO)**

The hardware watchdog is controlled by the kernel module `iTCO_wdt` (with support from `iTCO_vendor_support`).

1. Load the modules:
   ```bash
   sudo modprobe iTCO_vendor_support
   sudo modprobe iTCO_wdt
   ```
2. Check if the device exists:
   ```bash
   ls -l /dev/watchdog*
   ```
3. Register the modules for the next boot:
   ```bash
   grep -qxF "iTCO_vendor_support" /etc/modules || echo "iTCO_vendor_support" | sudo tee -a /etc/modules
   grep -qxF "iTCO_wdt" /etc/modules || echo "iTCO_wdt" | sudo tee -a /etc/modules
   ```
4. **No `/dev/watchdog`?** Then your mainboard does not support the iTCO watchdog or it is disabled in the BIOS. Load the software watchdog as a fallback:
   ```bash
   sudo modprobe softdog
   grep -qxF "softdog" /etc/modules || echo "softdog" | sudo tee -a /etc/modules
   ```

**Raspberry Pi (firmware)**

On the Pi the watchdog is enabled through the firmware boot configuration. The path depends on the OS version:

- `/boot/firmware/config.txt` (Bookworm and newer)
- `/boot/config.txt` (Buster / Bullseye)

```bash
echo "dtparam=watchdog=on" | sudo tee -a /boot/firmware/config.txt
```

> ⚠️ **Reboot required:** `/dev/watchdog` is only provided by the kernel after a reboot. The service becomes active automatically afterwards.

#### Step 3: Configure Watchdog Daemon
Open `/etc/watchdog.conf`:
```bash
sudo nano /etc/watchdog.conf
```

Set (or comment out) these values:

| Parameter | Intel / x86 PC | Raspberry Pi | Meaning |
|---|---|---|---|
| `watchdog-device` | `/dev/watchdog` | `/dev/watchdog` | hardware interface |
| `interval` | `10` | `4` | check interval in seconds |
| `watchdog-timeout` | `60` | `15` | hardware timeout (Pi limit: 15 s) |
| `retry-timeout` | `120` | `60` | fault tolerance before a reboot |
| `max-load-1` | `24` | `24` | reboot on excessive load |
| `test-directory` | `/etc/watchdog.d` | `/etc/watchdog.d` | custom check scripts |
| `min-memory` | **commented out** | **commented out** | prevents false positives from the RAM cache |

```ini
watchdog-device = /dev/watchdog
interval = 10
watchdog-timeout = 60
retry-timeout = 120
max-load-1 = 24
test-directory = /etc/watchdog.d

# IMPORTANT: disabled, otherwise the Linux page cache causes false positives
#min-memory = 25600
```

#### Step 4: Configure SSH Check Script with Grace Period
1. Create the test script:
   ```bash
   sudo nano /etc/watchdog.d/ssh_check
   ```
2. Paste the following contents (5 minute grace period after boot, then an IPv4 check of port 22):
   ```bash
   #!/bin/sh
   # 1. Grace period: if the system has been running for less than 300 seconds (5 min),
   # always report success (0) to prevent boot loops during startup.
   UPTIME=$(awk '{print int($1)}' /proc/uptime)
   if [ "$UPTIME" -lt 300 ]; then
       exit 0
   fi

   # 2. Explicitly check IPv4 (127.0.0.1) with a 2 second timeout
   nc -z -w 2 127.0.0.1 22
   ```
3. Make it executable:
   ```bash
   sudo chmod +x /etc/watchdog.d/ssh_check
   ```

> ⚠️ **IMPORTANT (Dry Run):** Execute the script manually (`/etc/watchdog.d/ssh_check`) before starting the service. Check the exit code with `echo $?`. The output **must be 0**, otherwise your system will enter an immediate reboot loop!

#### Step 5: Start Only After SSH (systemd Dependency)
```bash
sudo mkdir -p /etc/systemd/system/watchdog.service.d
sudo tee /etc/systemd/system/watchdog.service.d/override.conf > /dev/null << 'EOF'
[Unit]
After=ssh.service
Wants=ssh.service
EOF
sudo systemctl daemon-reload
```

#### Step 6: Enable & Start Service
```bash
sudo systemctl enable watchdog
sudo systemctl restart watchdog
sudo systemctl status watchdog
```

On the Raspberry Pi: if `dtparam=watchdog=on` was added, **a reboot is required**. The service is then active automatically (`systemctl enable`), but it can only be started once `/dev/watchdog` exists.

---

### When Things Go Wrong (Emergency)

| Problem | Solution |
|---|---|
| System keeps rebooting | Stop and mask the watchdog immediately: `sudo systemctl stop watchdog && sudo systemctl mask watchdog` |
| SSH listens on a different port | Adjust `nc -z -w 2 127.0.0.1 <PORT>` in the check script |
| `watchdog.service` does not start | Run `/etc/watchdog.d/ssh_check` manually and check `echo $?` (must be `0`) |
| No `/dev/watchdog` on the PC | Check the BIOS setting, otherwise load `softdog` as a fallback |
| Revert the changes | Backups are stored at `/etc/watchdog.conf.bak`, `/etc/systemd/system.conf.bak` and `/boot/firmware/config.txt.bak` |

---

### Automated Setup Scripts (EN)

Both scripts perform all steps automatically, including backups, hardware detection, dry run and activation. They have to be run as `root` or with `sudo`.

#### Script 1: Debian / Intel Machine (x86 PC)

```bash
#!/bin/bash

# --- OUTPUT COLORS ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No color

echo -e "${YELLOW}=== Watchdog Installation Script for Debian (Intel/x86 PC) ===${NC}"

# 1. Root Check (script must run as root)
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Please run this script as root (or with sudo)!${NC}"
  exit 1
fi

# 2. Unmask the watchdog upfront (in case an emergency mask was active)
systemctl unmask watchdog 2>/dev/null
systemctl stop watchdog 2>/dev/null

# 3. Disable the systemd watchdog (avoid conflicts)
echo -e "${YELLOW}[1/7] Disabling systemd-internal watchdog...${NC}"
if [ -f /etc/systemd/system.conf ]; then
  cp /etc/systemd/system.conf /etc/systemd/system.conf.bak
  sed -i -E 's/^[#]?\s*RuntimeWatchdogSec\s*=.*/#RuntimeWatchdogSec=0/g' /etc/systemd/system.conf
  systemctl daemon-reload
  echo -e "${GREEN}[OK] systemd-internal watchdog disabled.${NC}"
else
  echo -e "${YELLOW}[INFO] /etc/systemd/system.conf not found. Skipping.${NC}"
fi

# 4. Install packages
echo -e "${YELLOW}[2/7] Installing packages (watchdog, netcat-openbsd)...${NC}"
apt-get update -qq
apt-get install -y watchdog netcat-openbsd > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Packages installed successfully.${NC}"
else
  echo -e "${RED}[ERROR] Package installation failed!${NC}"
  exit 1
fi

# 5. Load the hardware module & register it permanently
echo -e "${YELLOW}[3/7] Configuring hardware watchdog module...${NC}"

# Try to load the Intel iTCO watchdog
modprobe iTCO_vendor_support 2>/dev/null
modprobe iTCO_wdt 2>/dev/null

if [ -e /dev/watchdog ]; then
  echo -e "${GREEN}[OK] /dev/watchdog hardware device is present.${NC}"
  # Register the modules for the next boot
  grep -qxF "iTCO_vendor_support" /etc/modules 2>/dev/null || echo "iTCO_vendor_support" >> /etc/modules
  grep -qxF "iTCO_wdt" /etc/modules 2>/dev/null || echo "iTCO_wdt" >> /etc/modules
else
  echo -e "${YELLOW}[WARNING] No /dev/watchdog found.${NC}"
  echo -e "          The mainboard may not support the iTCO watchdog or it is disabled in the BIOS."
  echo -e "          Loading the kernel software watchdog (softdog) as fallback..."
  modprobe softdog
  grep -qxF "softdog" /etc/modules 2>/dev/null || echo "softdog" >> /etc/modules
fi

# 6. Configure watchdog.conf
echo -e "${YELLOW}[4/7] Configuring /etc/watchdog.conf...${NC}"

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

[ -f /etc/watchdog.conf ] && cp /etc/watchdog.conf /etc/watchdog.conf.bak

set_watchdog_option "watchdog-device" "/dev/watchdog"
set_watchdog_option "interval" "10"
set_watchdog_option "watchdog-timeout" "60"         # Intel TCO supports longer timeouts than the Pi (60s is optimal)
set_watchdog_option "retry-timeout" "120"           # IMPORTANT: 2 minutes of fault tolerance on PCs
set_watchdog_option "max-load-1" "24"
set_watchdog_option "test-directory" "/etc/watchdog.d"

# IMPORTANT: disable min-memory (prevents false positives caused by the Linux RAM cache)
sed -i -E 's/^[#]?\s*min-memory\s*=.*/#min-memory = 25600/' /etc/watchdog.conf

echo -e "${GREEN}[OK] /etc/watchdog.conf configured.${NC}"

# 7. Create a boot-safe SSH check script
echo -e "${YELLOW}[5/7] Creating boot-safe SSH check script...${NC}"
mkdir -p /etc/watchdog.d

cat << 'EOF' > /etc/watchdog.d/ssh_check
#!/bin/sh
# 1. Grace period: if the system has been running for less than 300 seconds (5 min),
# always report success (0) to prevent boot loops during startup.
UPTIME=$(awk '{print int($1)}' /proc/uptime)
if [ "$UPTIME" -lt 300 ]; then
    exit 0
fi

# 2. Explicitly check IPv4 (127.0.0.1) with a 2 second timeout
nc -z -w 2 127.0.0.1 22
EOF

chmod +x /etc/watchdog.d/ssh_check
echo -e "${GREEN}[OK] Check script created at /etc/watchdog.d/ssh_check.${NC}"

# 8. Create the systemd dependency (start only after SSH)
mkdir -p /etc/systemd/system/watchdog.service.d
cat << 'EOF' > /etc/systemd/system/watchdog.service.d/override.conf
[Unit]
After=ssh.service
Wants=ssh.service
EOF
systemctl daemon-reload

# 9. Safety dry run & start
echo -e "${YELLOW}[6/7] Running safety dry run...${NC}"
/etc/watchdog.d/ssh_check
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Dry run successful! SSH responds as expected.${NC}"
  echo -e "${YELLOW}[7/7] Enabling and starting the watchdog service...${NC}"
  systemctl enable watchdog
  systemctl restart watchdog
  echo -e "${GREEN}=== INSTALLATION COMPLETED SUCCESSFULLY! ===${NC}"
else
  echo -e "${RED}[WARNING] Safety dry run failed!${NC}"
  echo -e "${RED}          The local SSH port (22) did not respond.${NC}"
  echo -e "${RED}The watchdog was NOT started to prevent a boot loop!${NC}"
  exit 1
fi
```

#### Script 2: Raspberry Pi

```bash
#!/bin/bash

# --- OUTPUT COLORS ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No color

echo -e "${YELLOW}=== Watchdog Installation Script for RASPBERRY PI ===${NC}"

# 1. Root check
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Please run this script as root (or with sudo)!${NC}"
  exit 1
fi

# 2. Unmask the watchdog upfront (in case an emergency mask was active)
systemctl unmask watchdog 2>/dev/null
systemctl stop watchdog 2>/dev/null

# 3. Disable the systemd watchdog (avoid conflicts)
echo -e "${YELLOW}[1/7] Disabling systemd-internal watchdog...${NC}"
if [ -f /etc/systemd/system.conf ]; then
  cp /etc/systemd/system.conf /etc/systemd/system.conf.bak
  sed -i -E 's/^[#]?\s*RuntimeWatchdogSec\s*=.*/#RuntimeWatchdogSec=0/g' /etc/systemd/system.conf
  systemctl daemon-reload
  echo -e "${GREEN}[OK] systemd-internal watchdog disabled.${NC}"
fi

# 4. Enable the hardware watchdog in the Raspberry Pi firmware
echo -e "${YELLOW}[2/7] Enabling hardware watchdog in the Pi boot configuration...${NC}"
CONFIG_FILE=""
if [ -f /boot/firmware/config.txt ]; then
  CONFIG_FILE="/boot/firmware/config.txt"  # New path (Bookworm)
elif [ -f /boot/config.txt ]; then
  CONFIG_FILE="/boot/config.txt"           # Old path (Buster/Bullseye)
fi

REBOOT_NEEDED=false
if [ -n "$CONFIG_FILE" ]; then
  if ! grep -q "^dtparam=watchdog=on" "$CONFIG_FILE"; then
    cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    echo "dtparam=watchdog=on" >> "$CONFIG_FILE"
    echo -e "${GREEN}[OK] Watchdog enabled in $CONFIG_FILE. (Backup created).${NC}"
    REBOOT_NEEDED=true
  else
    echo -e "${GREEN}[OK] Watchdog already active in $CONFIG_FILE.${NC}"
  fi
else
  echo -e "${RED}[ERROR] No config.txt found! Is this Raspberry Pi OS?${NC}"
  exit 1
fi

# 5. Install packages
echo -e "${YELLOW}[3/7] Installing packages (watchdog, netcat-openbsd)...${NC}"
apt-get update -qq
apt-get install -y watchdog netcat-openbsd > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Packages installed successfully.${NC}"
else
  echo -e "${RED}[ERROR] Package installation failed!${NC}"
  exit 1
fi

# 6. Configure watchdog.conf (Raspberry Pi specific values!)
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

[ -f /etc/watchdog.conf ] && cp /etc/watchdog.conf /etc/watchdog.conf.bak

# Specific Raspberry Pi settings
set_watchdog_option "watchdog-device" "/dev/watchdog"
set_watchdog_option "interval" "4"                 # Check every 4 seconds
set_watchdog_option "watchdog-timeout" "15"         # Raspberry Pi hardware limit (max 15s)
set_watchdog_option "retry-timeout" "60"            # IMPORTANT: 60s of fault tolerance against boot loops
set_watchdog_option "max-load-1" "24"
set_watchdog_option "test-directory" "/etc/watchdog.d"

# IMPORTANT: disable min-memory (risk of false positives from the Linux page cache)
sed -i -E 's/^[#]?\s*min-memory\s*=.*/#min-memory = 12800/' /etc/watchdog.conf

echo -e "${GREEN}[OK] /etc/watchdog.conf configured safely.${NC}"

# 7. Create a boot-safe script that checks the SSH port
echo -e "${YELLOW}[5/7] Creating boot-safe SSH check script...${NC}"
mkdir -p /etc/watchdog.d

cat << 'EOF' > /etc/watchdog.d/ssh_check
#!/bin/sh
# 1. Grace period: always report success during the first 5 minutes after boot,
# to reliably rule out endless reboots while the system is starting up.
UPTIME=$(awk '{print int($1)}' /proc/uptime)
if [ "$UPTIME" -lt 300 ]; then
    exit 0
fi

# 2. Explicitly check IPv4 (127.0.0.1) with a 1 second timeout
nc -z -w 1 127.0.0.1 22
EOF

chmod +x /etc/watchdog.d/ssh_check
echo -e "${GREEN}[OK] Check script created at /etc/watchdog.d/ssh_check.${NC}"

# 8. Create the systemd dependency (start only after SSH)
mkdir -p /etc/systemd/system/watchdog.service.d
cat << 'EOF' > /etc/systemd/system/watchdog.service.d/override.conf
[Unit]
After=ssh.service
Wants=ssh.service
EOF
systemctl daemon-reload

# 9. Safety dry run
echo -e "${YELLOW}[6/7] Running safety dry run...${NC}"
/etc/watchdog.d/ssh_check
SSH_OK=$?

if [ "$SSH_OK" -ne 0 ]; then
  echo -e "${RED}[ERROR] Safety dry run failed! SSH is not responding.${NC}"
  echo -e "${RED}         The service will not be started as a precaution.${NC}"
  exit 1
fi
echo -e "${GREEN}[OK] Dry run successful! SSH responds.${NC}"

# 10. Start or print the reboot notice
echo -e "${YELLOW}[7/7] Finalizing installation...${NC}"
if [ "$REBOOT_NEEDED" = true ]; then
  echo -e "${YELLOW}------------------------------------------------------------${NC}"
  echo -e "${YELLOW}ATTENTION: You have to REBOOT the Raspberry Pi once!${NC}"
  echo -e "${YELLOW}The hardware watchdog (/dev/watchdog) is only provided by the${NC}"
  echo -e "${YELLOW}kernel after a reboot. The service becomes active automatically.${NC}"
  echo -e "${YELLOW}------------------------------------------------------------${NC}"
  systemctl enable watchdog
else
  echo -e "${YELLOW}Enabling and starting the watchdog service...${NC}"
  systemctl enable watchdog
  systemctl restart watchdog
  echo -e "${GREEN}=== DONE! The watchdog is running and protects the Pi. ===${NC}"
fi
```

!!! tip "Store the script as a file"
    ```bash
    sudo nano /root/watchdog-install.sh
    sudo chmod +x watchdog-install.sh
    sudo ./watchdog-install.sh
    ```
