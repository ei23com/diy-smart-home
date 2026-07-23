# Hardware-Watchdog mit SSH-Prüfung unter Debian

Diese Anleitung beschreibt die Konfiguration eines Hardware-Watchdogs unter Debian. Das System führt automatisch einen harten Neustart durch, wenn das Betriebssystem einfriert **oder** wichtige Dienste wie SSH (Port 22) nicht mehr reagieren.

---

### Manuelle Einrichtung (Debian)

#### Schritt 0: Konflikte vermeiden (Systemd-Watchdog deaktivieren)
Da sich nur ein einziges Programm die Hardware-Schnittstelle `/dev/watchdog` reservieren darf, muss der eingebaute Systemd-Watchdog deaktiviert werden.

1. Datei öffnen:
   ```bash
   sudo nano /etc/systemd/system.conf
   ```
2. Sicherstellen, dass die Zeile `RuntimeWatchdogSec` auskommentiert oder auf `0` gesetzt ist:
   ```ini
   #RuntimeWatchdogSec=0
   ```
3. Systemd-Konfiguration neu laden:
   ```bash
   sudo systemctl daemon-reload
   ```

#### Schritt 1: Benötigte Pakete installieren
```bash
sudo apt update
sudo apt install watchdog netcat-openbsd -y
```

#### Schritt 2: Intel-Hardware-Watchdog aktivieren
Für Systeme mit Intel-Prozessoren wird der Hardware-Watchdog über das Kernel-Modul `iTCO_wdt` gesteuert.

1. Prüfen, ob das Gerät existiert:
   ```bash
   ls -l /dev/watchdog*
   ```
2. Falls nicht vorhanden, Modul manuell laden und dauerhaft eintragen:
   ```bash
   sudo modprobe iTCO_wdt
   echo "iTCO_wdt" | sudo tee -a /etc/modules
   ```

#### Schritt 3: Watchdog-Daemon konfigurieren
Öffnen Sie `/etc/watchdog.conf`:
```bash
sudo nano /etc/watchdog.conf
```
Aktivieren / Ergänzen Sie folgende Parameter:
```ini
watchdog-device = /dev/watchdog
interval = 10
watchdog-timeout = 60
max-load-1 = 24
min-memory = 25600
test-directory = /etc/watchdog.d
```

#### Schritt 4: SSH-Antwort-Test einrichten
1. Test-Skript erstellen:
   ```bash
   sudo nano /etc/watchdog.d/ssh_check
   ```
2. Inhalt einfügen:
   ```bash
   #!/bin/sh
   nc -z -w 3 localhost 22
   ```
3. Ausführbar machen:
   ```bash
   sudo chmod +x /etc/watchdog.d/ssh_check
   ```

> ⚠️ **WICHTIG (Trockenlauf):** Führen Sie das Skript manuell aus (`/etc/watchdog.d/ssh_check`), bevor Sie den Dienst aktivieren. Prüfen Sie den Exit-Code mit `echo $?`. Das Ergebnis **muss 0 sein**, da der PC sonst direkt nach dem Start in eine Reboot-Schleife gerät.

#### Schritt 5: Dienst aktivieren & starten
```bash
sudo systemctl enable watchdog
sudo systemctl start watchdog
sudo systemctl status watchdog
```

---

### Automatisierungs-Skripte (DE)

#### Skript 1: Intel CPU

```bash
#!/bin/bash

# --- FARBEN FÜR DIE AUSGABE ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Keine Farbe

echo -e "${YELLOW}=== Watchdog Installations-Script für Debian (Intel CPU) ===${NC}"

# 1. Root-Check (Script muss als root laufen)
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[FEHLER] Bitte führen Sie dieses Script als root (oder mit sudo) aus!${NC}"
  exit 1
fi

# 2. systemd Watchdog deaktivieren (Konfliktvermeidung)
echo -e "${YELLOW}[1/6] Deaktiviere systemd-internen Watchdog...${NC}"
if [ -f /etc/systemd/system.conf ]; then
  # Erstellt ein Backup
  cp /etc/systemd/system.conf /etc/systemd/system.conf.bak
  # Kommentiert die Einstellung aus
  sed -i -E 's/^[#]?\s*RuntimeWatchdogSec\s*=.*/#RuntimeWatchdogSec=0/g' /etc/systemd/system.conf
  systemctl daemon-reload
  echo -e "${GREEN}[OK] systemd-interner Watchdog deaktiviert.${NC}"
else
  echo -e "${YELLOW}[INFO] /etc/systemd/system.conf nicht gefunden. Überspringe.${NC}"
fi

# 3. Pakete installieren
echo -e "${YELLOW}[2/6] Installiere Pakete (watchdog, netcat-openbsd)...${NC}"
apt-get update -qq
apt-get install -y watchdog netcat-openbsd > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Pakete erfolgreich installiert.${NC}"
else
  echo -e "${RED}[FEHLER] Paket-Installation fehlgeschlagen!${NC}"
  exit 1
fi

# 4. Hardware-Modul laden & permanent eintragen
echo -e "${YELLOW}[3/6] Konfiguriere Intel Hardware-Modul (iTCO_wdt)...${NC}"
modprobe iTCO_wdt 2>/dev/null
if [ $? -eq 0 ]; then
  # In /etc/modules eintragen, falls noch nicht vorhanden
  if ! grep -qxF "iTCO_wdt" /etc/modules; then
    echo "iTCO_wdt" >> /etc/modules
  fi
  echo -e "${GREEN}[OK] Modul iTCO_wdt geladen und permanent registriert.${NC}"
else
  echo -e "${YELLOW}[WARNUNG] Modul iTCO_wdt konnte nicht geladen werden.${NC}"
  echo -e "          (Ignorieren Sie dies, falls kein Intel-Mainboard verwendet wird).${NC}"
fi

# 5. watchdog.conf konfigurieren
echo -e "${YELLOW}[4/6] Konfiguriere /etc/watchdog.conf...${NC}"

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

echo -e "${GREEN}[OK] /etc/watchdog.conf konfiguriert (Backup unter .bak erstellt).${NC}"

# 6. Test-Skript für SSH-Port-Prüfung erstellen
echo -e "${YELLOW}[5/6] Erstelle SSH-Prüfskript...${NC}"
mkdir -p /etc/watchdog.d

cat << 'EOF' > /etc/watchdog.d/ssh_check
#!/bin/sh
# Prüft, ob Port 22 lokal antwortet. Timeout nach 3 Sekunden.
nc -z -w 3 localhost 22
EOF

chmod +x /etc/watchdog.d/ssh_check
echo -e "${GREEN}[OK] Prüfskript unter /etc/watchdog.d/ssh_check erstellt.${NC}"

# 7. Sicherheits-Trockenlauf
echo -e "${YELLOW}[6/6] Führe Sicherheits-Trockenlauf durch...${NC}"
/etc/watchdog.d/ssh_check
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Trockenlauf erfolgreich! SSH antwortet wie erwartet.${NC}"
  echo -e "${YELLOW}Aktiviere und starte den Watchdog-Dienst...${NC}"
  systemctl enable watchdog
  systemctl start watchdog
  echo -e "${GREEN}=== INSTALLATION ERFOLGREICH BEENDET! ===${NC}"
else
  echo -e "${RED}[WARNUNG] Sicherheits-Trockenlauf fehlgeschlagen!${NC}"
  echo -e "${RED}          Der lokale SSH-Port (22) hat nicht geantwortet.${NC}"
  echo -e "${YELLOW}Mögliche Gründe:${NC}"
  echo -e " - Ihr SSH-Dienst läuft auf einem anderen Port als 22."
  echo -e " - Der SSH-Dienst ist gerade nicht aktiv."
  echo -e ""
  echo -e "${RED}Der Watchdog wurde NICHT aktiviert, um eine Reboot-Schleife zu verhindern!${NC}"
  echo -e "${YELLOW}Bitte korrigieren Sie das Problem und starten Sie den Dienst danach manuell mit:${NC}"
  echo -e "sudo systemctl enable --now watchdog"
fi
```

#### Skript 2: Raspberry Pi

```bash
#!/bin/bash

# --- FARBEN FÜR DIE AUSGABE ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Keine Farbe

echo -e "${YELLOW}=== Watchdog Installations-Script für RASPBERRY PI ===${NC}"

# 1. Root-Check
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[FEHLER] Bitte führen Sie dieses Script als root (oder mit sudo) aus!${NC}"
  exit 1
fi

# 2. systemd Watchdog deaktivieren (Konfliktvermeidung)
echo -e "${YELLOW}[1/7] Deaktiviere systemd-internen Watchdog...${NC}"
if [ -f /etc/systemd/system.conf ]; then
  cp /etc/systemd/system.conf /etc/systemd/system.conf.bak
  sed -i -E 's/^[#]?\s*RuntimeWatchdogSec\s*=.*/#RuntimeWatchdogSec=0/g' /etc/systemd/system.conf
  systemctl daemon-reload
  echo -e "${GREEN}[OK] systemd-interner Watchdog deaktiviert.${NC}"
fi

# 3. Hardware-Watchdog in Raspberry Pi Firmware aktivieren
echo -e "${YELLOW}[2/7] Aktiviere Hardware-Watchdog in der Pi-Boot-Konfiguration...${NC}"
CONFIG_FILE=""
if [ -f /boot/firmware/config.txt ]; then
  CONFIG_FILE="/boot/firmware/config.txt"  # Neuer Pfad (Bookworm)
elif [ -f /boot/config.txt ]; then
  CONFIG_FILE="/boot/config.txt"           # Alter Pfad (Buster/Bullseye)
fi

if [ -n "$CONFIG_FILE" ]; then
  if ! grep -q "dtparam=watchdog=on" "$CONFIG_FILE"; then
    cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    echo "dtparam=watchdog=on" >> "$CONFIG_FILE"
    echo -e "${GREEN}[OK] Watchdog in $CONFIG_FILE aktiviert. (Backup erstellt).${NC}"
    REBOOT_NEEDED=true
  else
    echo -e "${GREEN}[OK] Watchdog bereits in $CONFIG_FILE aktiv.${NC}"
    REBOOT_NEEDED=false
  fi
else
  echo -e "${RED}[FEHLER] Keine config.txt gefunden! Ist dies ein Raspberry Pi OS?${NC}"
  exit 1
fi

# 4. Pakete installieren
echo -e "${YELLOW}[3/7] Installiere Pakete (watchdog, netcat-openbsd)...${NC}"
apt-get update -qq
apt-get install -y watchdog netcat-openbsd > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Pakete erfolgreich installiert.${NC}"
else
  echo -e "${RED}[FEHLER] Paket-Installation fehlgeschlagen!${NC}"
  exit 1
fi

# 5. watchdog.conf konfigurieren (Spezielle Pi-Werte!)
echo -e "${YELLOW}[4/7] Konfiguriere /etc/watchdog.conf für Raspberry Pi...${NC}"

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

# Spezifische Raspberry Pi Einstellungen (Timeout maximal 15)
set_watchdog_option "watchdog-device" "/dev/watchdog"
set_watchdog_option "interval" "5"                # Prüfe alle 5 Sekunden
set_watchdog_option "watchdog-timeout" "15"        # Raspberry Pi Hardware-Limit!
set_watchdog_option "max-load-1" "24"
set_watchdog_option "min-memory" "12800"             # Etwas weniger auf dem Pi
set_watchdog_option "test-directory" "/etc/watchdog.d"

echo -e "${GREEN}[OK] /etc/watchdog.conf konfiguriert.${NC}"

# 6. Test-Skript für SSH-Port-Prüfung erstellen
echo -e "${YELLOW}[5/7] Erstelle SSH-Prüfskript...${NC}"
mkdir -p /etc/watchdog.d

cat << 'EOF' > /etc/watchdog.d/ssh_check
#!/bin/sh
# Prüft, ob Port 22 lokal antwortet.
nc -z -w 3 localhost 22
EOF

chmod +x /etc/watchdog.d/ssh_check
echo -e "${GREEN}[OK] Prüfskript unter /etc/watchdog.d/ssh_check erstellt.${NC}"

# 7. Sicherheits-Trockenlauf
echo -e "${YELLOW}[6/7] Führe Sicherheits-Trockenlauf durch...${NC}"
/etc/watchdog.d/ssh_check
SSH_OK=$?

if [ SSH_OK -ne 0 ]; then
  echo -e "${RED}[FEHLER] Sicherheits-Trockenlauf fehlgeschlagen! SSH antwortet nicht.${NC}"
  echo -e "${RED}         Dienst wird zum Schutz nicht gestartet.${NC}"
  exit 1
fi
echo -e "${GREEN}[OK] Trockenlauf erfolgreich! SSH antwortet.${NC}"

# 8. Starten oder Reboot-Hinweis
echo -e "${YELLOW}[7/7] Finalisiere Installation...${NC}"
if [ "$REBOOT_NEEDED" = true ]; then
  echo -e "${YELLOW}------------------------------------------------------------${NC}"
  echo -e "${YELLOW}ACHTUNG: Sie müssen den Raspberry Pi einmal NEU STARTEN!${NC}"
  echo -e "${YELLOW}Der Hardware-Watchdog (/dev/watchdog) wird erst nach einem${NC}"
  echo -e "${YELLOW}Reboot vom Kernel bereitgestellt. Der Dienst wird danach automatisch aktiv.${NC}"
  echo -e "${YELLOW}------------------------------------------------------------${NC}"
  systemctl enable watchdog
else
  echo -e "${YELLOW}Aktiviere und starte den Watchdog-Dienst...${NC}"
  systemctl enable watchdog
  systemctl start watchdog
  echo -e "${GREEN}=== FERTIG! Der Watchdog läuft und schützt den Pi. ===${NC}"
fi
```