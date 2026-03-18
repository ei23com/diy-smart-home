# Security Audit: ei23.sh Smart Home Server Installation Script

## ⚠️ IMPORTANT SECURITY NOTICE

**This script was developed for trusted environments** where the user fully understands the security implications. It is **NOT suitable** for use in production or publicly accessible environments without additional security measures.

---

## 1. Summary of Security Issues

| Category | Severity | Status |
|----------|----------|--------|
| SSH Root Login | 🔴 CRITICAL | Design Decision |
| Sudo Without Password | 🔴 CRITICAL | Design Decision |
| Password Generation | 🟠 MEDIUM | Needs Improvement |
| Network Exposure | 🟠 MEDIUM | Configuration Dependent |
| Container Isolation | 🟡 LOW | Docker Dependent |

---

## 2. Critical Security Issues in Detail

### 2.1 SSH Root Login Enabled

**Lines 780-783:**
```bash
# Enable SSH root-login
if [ -f "/etc/ssh/sshd_config" ]; then
    sudo sed -i -e 's#\#PermitRootLogin prohibit-password#PermitRootLogin yes#' /etc/ssh/sshd_config
fi
```

**Problem:**
- Root login via SSH is explicitly enabled
- Allows direct access to the superuser account
- Increases risk of brute-force attacks

**Risk:** 🔴 **CRITICAL**
- Complete system compromise if credentials are leaked
- Bypass of audit trails (who did what as root?)

**Design Decision:**
> This feature was intentionally implemented for easy initial installations in isolated lab networks. The user must be aware of the risks.

**Recommendation:**
```bash
# Disable after installation:
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Use SSH keys instead:
sudo mkdir -p /root/.ssh
sudo cp /home/$IAM/.ssh/authorized_keys /root/.ssh/
```

---

### 2.2 Sudo Without Password

**Lines 661-670:**
```bash
# Check for sudo
if sudo -lU "$IAM" | grep -q "(ALL) NOPASSWD: ALL"; then
  echo "$IAM sudo checked"
else
  if ! sudo -v &> /dev/null; then
    echo "Please login root"
    su -c "apt-get install sudo -y; echo '$IAM ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/010_$IAM-nopasswd; sudo adduser $IAM sudo; chown 1000:1000 /home/$IAM"
  else
    echo "User already has sudo rights"
  fi
fi
```

**Problem:**
- User receives sudo privileges **without password prompt**
- File: `/etc/sudoers.d/010_$IAM-nopasswd`
- Any application run by the user can execute root commands

**Risk:** 🔴 **CRITICAL**
- Malware can silently obtain sudo privileges
- No protection against accidental destructive commands
- Bypass of security controls

**Design Decision:**
> For automation purposes and ease of use in trusted environments. The user accepts the risk.

**Recommendation:**
```bash
# Enable password protection after installation:
sudo rm /etc/sudoers.d/010_$IAM-nopasswd
# Or at least require password for critical commands
```

---

### 2.3 Password Generation

**Lines 358-370:**
```bash
generate_password(){
   chars() { echo ${1:RANDOM%${#1}:1}; }
   {
      chars '0123456789'
      chars 'abcdefghijklmnopqrstuvwxyz'
      chars 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      for i in $( seq 1 $(( 12 )) )
      do
         chars '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
      done
   } | sort -R | tr -d '\n'
   echo ""
}
```

**Problem:**
- Uses `$RANDOM` (not cryptographically secure)
- 12 character length is minimal
- `sort -R` uses non-cryptographic random generator

**Risk:** 🟠 **MEDIUM**
- Passwords are theoretically predictable
- Sufficient for local/isolated networks
- Not suitable for publicly accessible services

**Recommendation:**
```bash
# Better alternative:
generate_password(){
    openssl rand -base64 16 | tr -d '\n'
}
# Or:
generate_password(){
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1
}
```

---

### 2.4 Network Exposure

**Docker containers without network isolation:**

Many containers expose ports directly:
- Home Assistant: 8123
- Node-RED: 1880
- Mosquitto: 1883, 9001
- Pi-hole: 80, 443
- Nextcloud: 80/443

**Risk:** 🟠 **MEDIUM**
- All services are reachable in the local network
- No firewall configuration in the script
- UFW is installed but not configured

**Recommendation:**
```bash
# Configure firewall after installation:
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 8123/tcp  # Home Assistant (only if needed)
sudo ufw enable
```

---

### 2.5 Container Security

**Problem:**
- Containers run as root by default
- No resource limits configured
- No security options (AppArmor, Seccomp)

**Risk:** 🟡 **LOW**
- Full system compromise possible on container escape
- Resource abuse possible

---

## 3. Additional Security Aspects

### 3.1 Installed Packages

**Line 214:**
```bash
sudo apt-get install -y arp-scan autoconf build-essential cmake curl rsync expect ffmpeg gcc git htop btop imagemagick imagemagick-doc jq libcurl4-openssl-dev libfftw3-dev libimage-exiftool-perl libtool libusb-1.0 mkdocs mosquitto-clients mpg123 ncdu ncftp netdiscover nmap parted pkg-config pv python3-full python3-venv screen ssh sshpass sysfsutils tcpdump telnet ufw unzip usbutils virtualenv wireguard zsh
```

**Critical Tools:**
- `sshpass` - Password-based SSH authentication
- `tcpdump` - Network traffic analysis
- `nmap` - Network scanner
- `netdiscover` - Network discovery
- `expect` - Automation of password prompts

**Risk:** 🟡 **LOW**
- These tools can be misused for attacks
- Acceptable in trusted environments

---

### 3.2 Default DNS for Docker

**Lines 732-736 (commented out):**
```bash
# set OpenDNS as default DNS for Docker-Containers
# default_gateway=$(ip route | grep default | awk '{print $3}')
# echo -e "{\n\t\t\"dns\": [\"$default_gateway\", \"208.67.222.222\"]\n}" | sudo tee /etc/docker/daemon.json
```

**Note:**
- DNS configuration is commented out
- Containers use host DNS or their own configuration
- DNS leaking possible

---

### 3.3 File Permissions

**Multiple locations in script:**
```bash
sudo chown -R 1883:1883 $DOCKERDIR/volumes/mosquitto/
sudo chown -R $IAM $HOME/.node-red/lib/
```

**Problem:**
- Volume permissions are set
- Container-specific user IDs (e.g., 1883 for Mosquitto)
- Potential for permission issues

---

### 3.4 External Script Downloads

**Line 859:**
```bash
sudo wget "https://ei23.de/softwarehub/smarthome/USERID/$card/$SCRIPT_VERSION/ei23-docker.zip" -O ei23-docker.zip
```

**Risk:** 🟠 **MEDIUM**
- Download from external source
- Dependency on ei23.de server
- No hash check of downloads

**Recommendation:**
- Implement SHA256 checksums
- Use signatures for updates

---

### 3.5 Node-RED npm Packages

**Lines 113-119:**
```bash
for addonnodes in moment node-red-contrib-boolean-logic ...; do
    npm $NOLOGNODE install --no-audit --no-update-notifier --no-fund --save --save-prefix="~" --production ${addonnodes}@latest
done
```

**Problem:**
- `--no-audit` skips security checks
- Many third-party packages
- Supply chain attacks possible

---

## 4. Security Checklist After Installation

### 🔴 Immediate Actions (CRITICAL)

- [ ] Disable SSH root login (if not explicitly needed)
- [ ] Enable sudo password prompt
- [ ] Change default passwords of all services
- [ ] Configure and enable firewall (UFW)

### 🟠 Short Term (MEDIUM)

- [ ] Switch SSH to key-based authentication
- [ ] Disable unnecessary services
- [ ] Plan regular updates
- [ ] Implement backup strategy

### 🟡 Long Term (LOW)

- [ ] Review container security options
- [ ] Consider network segmentation
- [ ] Set up monitoring
- [ ] Automate security audits

---

## 5. Security Recommendations

### 5.1 For Production Environments

```bash
#!/bin/bash
# Run AFTER installation:

# 1. Harden SSH
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# 2. Protect sudo
sudo rm /etc/sudoers.d/010_*-nopasswd

# 3. Enable firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw enable

# 4. Install Fail2Ban
sudo apt-get install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 5.2 For Test Environments

- Operate only in isolated networks
- No port forwarding on router
- Perform regular security updates
- Monitor network traffic

---

## 6. Conclusion

### Design Decisions vs. Security Vulnerabilities

| Feature | Decision | Risk |
|---------|----------|------|
| SSH Root Login | ✅ Intentional | High |
| Sudo NOPASSWD | ✅ Intentional | High |
| $RANDOM Passwords | ⚠️ Convenience | Medium |
| --no-audit npm | ⚠️ Convenience | Medium |
| UFW without rules | ⚠️ Incomplete | Medium |

### Target Audience

This script is intended for:
- ✅ Experienced users in lab networks
- ✅ Developers for local testing
- ✅ Smart home enthusiasts with security awareness

**NOT suitable for:**
- ❌ Publicly accessible servers
- ❌ Production environments without hardening
- ❌ Users without basic security knowledge

---

## 7. Disclaimer

> **IMPORTANT:** The user is solely responsible for the security of their system. This script is provided "as-is". The author assumes no liability for security incidents, data loss, or damages resulting from its use.

**Before installation, ensure:**
1. Full understanding of security implications
2. Isolated test environment available
3. Backup strategy implemented
4. Regular maintenance planned

---

## 8. Appendix: Security Hardening Script

```bash
#!/bin/bash
# security-hardening.sh - Run AFTER installation

echo "=== Security Hardening for ei23 Smart Home Server ==="

# 1. Disable SSH root login
echo "[1/5] Disabling SSH Root Login..."
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# 2. Disable SSH password authentication (keys only)
echo "[2/5] Enabling SSH Key-Only Authentication..."
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# 3. Enforce sudo password
echo "[3/5] Enabling Sudo Password Prompt..."
sudo rm -f /etc/sudoers.d/010_*-nopasswd

# 4. Configure firewall
echo "[4/5] Configuring UFW Firewall..."
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
# Only open needed ports:
# sudo ufw allow 8123/tcp  # Home Assistant
# sudo ufw allow 1880/tcp  # Node-RED
sudo ufw --force enable

# 5. Install Fail2Ban
echo "[5/5] Installing Fail2Ban..."
sudo apt-get install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Restart SSH
sudo systemctl restart sshd

echo "=== Hardening Complete! System reboot recommended ==="
```