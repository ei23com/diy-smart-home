# Hardware-Watchdog mit SSH-Prüfung (Debian & Raspberry Pi)

Diese Anleitung beschreibt die Konfiguration eines Hardware-Watchdogs. Das System führt automatisch einen harten Neustart durch, wenn das Betriebssystem einfriert **oder** wichtige Dienste wie SSH (Port 22) nicht mehr reagieren – auch wenn Ping noch antwortet.

Es gibt zwei Varianten:

- **Debian / Intel-Rechner (x86 PC):** Hardware-Watchdog über das Kernel-Modul `iTCO_wdt` (Fallback: `softdog`)
- **Raspberry Pi:** Hardware-Watchdog über die Firmware (`dtparam=watchdog=on`)

!!! info "Sicherheitsmechanismen (verhindern Reboot-Schleifen)"
    - **`retry-timeout`**: 120 Sekunden Fehlertoleranz auf PCs, 60 Sekunden auf dem Pi
    - **`min-memory` deaktiviert**: verhindert Fehlalarme durch den Linux-RAM-Cache
    - **5-Minuten-Schonfrist** nach dem Boot: In den ersten 300 Sekunden meldet das Prüfskript immer Erfolg
    - **Trockenlauf** vor dem Aktivieren: Antwortet SSH nicht, wird der Dienst gar nicht erst gestartet
    - **systemd-Abhängigkeit**: Der Watchdog startet erst nach `ssh.service`
    - **`systemctl unmask watchdog`**: hebt eine eventuell aktive Notfall-Maskierung wieder auf

---

### Manuelle Einrichtung

#### Schritt 0: Notfall-Maskierung aufheben & systemd-Watchdog deaktivieren
Da sich nur ein einziges Programm die Hardware-Schnittstelle `/dev/watchdog` reservieren darf, muss der eingebaute systemd-Watchdog deaktiviert werden.

```bash
# Eventuell aktive Maskierung aufheben (z.B. nach einer Reboot-Schleife)
sudo systemctl unmask watchdog 2>/dev/null
sudo systemctl stop watchdog 2>/dev/null
```

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

#### Schritt 2: Hardware-Watchdog bereitstellen

**Intel / x86 PC (iTCO)**

Der Hardware-Watchdog wird über das Kernel-Modul `iTCO_wdt` gesteuert (Unterstützung: `iTCO_vendor_support`).

1. Module laden:
   ```bash
   sudo modprobe iTCO_vendor_support
   sudo modprobe iTCO_wdt
   ```
2. Prüfen, ob das Gerät existiert:
   ```bash
   ls -l /dev/watchdog*
   ```
3. Module für den nächsten Start vormerken:
   ```bash
   grep -qxF "iTCO_vendor_support" /etc/modules || echo "iTCO_vendor_support" | sudo tee -a /etc/modules
   grep -qxF "iTCO_wdt" /etc/modules || echo "iTCO_wdt" | sudo tee -a /etc/modules
   ```
4. **Kein `/dev/watchdog` vorhanden?** Dann unterstützt das Mainboard keinen iTCO-Watchdog oder er ist im BIOS deaktiviert. Als Fallback den Software-Watchdog laden:
   ```bash
   sudo modprobe softdog
   grep -qxF "softdog" /etc/modules || echo "softdog" | sudo tee -a /etc/modules
   ```

**Raspberry Pi (Firmware)**

Beim Pi wird der Watchdog über die Boot-Konfiguration der Firmware aktiviert. Der Pfad unterscheidet sich je nach OS-Version:

- `/boot/firmware/config.txt` (ab Bookworm)
- `/boot/config.txt` (Buster / Bullseye)

```bash
echo "dtparam=watchdog=on" | sudo tee -a /boot/firmware/config.txt
```

> ⚠️ **Neustart erforderlich:** `/dev/watchdog` wird erst nach einem Reboot vom Kernel bereitgestellt. Der Dienst wird danach automatisch aktiv.

#### Schritt 3: Watchdog-Daemon konfigurieren
Öffnen Sie `/etc/watchdog.conf`:
```bash
sudo nano /etc/watchdog.conf
```

Diese Werte setzen (bzw. auskommentieren):

| Parameter | Intel / x86 PC | Raspberry Pi | Bedeutung |
|---|---|---|---|
| `watchdog-device` | `/dev/watchdog` | `/dev/watchdog` | Hardware-Schnittstelle |
| `interval` | `10` | `4` | Prüfintervall in Sekunden |
| `watchdog-timeout` | `60` | `15` | Hardware-Timeout (Pi-Limit: 15 s) |
| `retry-timeout` | `120` | `60` | Fehlertoleranz vor dem Reboot |
| `max-load-1` | `24` | `24` | Reboot bei zu hoher Last |
| `test-directory` | `/etc/watchdog.d` | `/etc/watchdog.d` | Eigene Prüfskripte |
| `min-memory` | **auskommentiert** | **auskommentiert** | verhindert Fehlalarme durch RAM-Cache |

```ini
watchdog-device = /dev/watchdog
interval = 10
watchdog-timeout = 60
retry-timeout = 120
max-load-1 = 24
test-directory = /etc/watchdog.d

# WICHTIG: deaktiviert, sonst Fehlalarme durch den Linux-Page-Cache
#min-memory = 25600
```

#### Schritt 4: SSH-Prüfskript mit Schonfrist einrichten
1. Test-Skript erstellen:
   ```bash
   sudo nano /etc/watchdog.d/ssh_check
   ```
2. Inhalt einfügen (Schonfrist von 5 Minuten nach dem Boot, danach IPv4-Prüfung von Port 22):
   ```bash
   #!/bin/sh
   # 1. Grace-Period: Wenn das System weniger als 300 Sek. (5 Min.) läuft,
   # immer Erfolg (0) melden, um Bootschleifen beim Hochfahren zu verhindern.
   UPTIME=$(awk '{print int($1)}' /proc/uptime)
   if [ "$UPTIME" -lt 300 ]; then
       exit 0
   fi

   # 2. Explizit IPv4 (127.0.0.1) mit 2 Sekunden Timeout prüfen
   nc -z -w 2 127.0.0.1 22
   ```
3. Ausführbar machen:
   ```bash
   sudo chmod +x /etc/watchdog.d/ssh_check
   ```

> ⚠️ **WICHTIG (Trockenlauf):** Führen Sie das Skript manuell aus (`/etc/watchdog.d/ssh_check`), bevor Sie den Dienst aktivieren. Prüfen Sie den Exit-Code mit `echo $?`. Das Ergebnis **muss 0 sein**, da das System sonst direkt nach dem Start in eine Reboot-Schleife gerät.

#### Schritt 5: Start erst nach SSH (systemd-Abhängigkeit)
```bash
sudo mkdir -p /etc/systemd/system/watchdog.service.d
sudo tee /etc/systemd/system/watchdog.service.d/override.conf > /dev/null << 'EOF'
[Unit]
After=ssh.service
Wants=ssh.service
EOF
sudo systemctl daemon-reload
```

#### Schritt 6: Dienst aktivieren & starten
```bash
sudo systemctl enable watchdog
sudo systemctl restart watchdog
sudo systemctl status watchdog
```

Auf dem Raspberry Pi gilt: Wurde `dtparam=watchdog=on` neu gesetzt, ist **ein Reboot nötig**. Der Dienst ist danach automatisch aktiv (`systemctl enable`), gestartet werden kann er erst, wenn `/dev/watchdog` existiert.

---

### Wenn etwas schiefgeht (Notfall)

| Problem | Lösung |
|---|---|
| System startet ständig neu | Watchdog sofort stoppen und maskieren: `sudo systemctl stop watchdog && sudo systemctl mask watchdog` |
| SSH antwortet auf einem anderen Port | `nc -z -w 2 127.0.0.1 <PORT>` im Prüfskript anpassen |
| `watchdog.service` startet nicht | `/etc/watchdog.d/ssh_check` manuell ausführen und `echo $?` prüfen (muss `0` sein) |
| Kein `/dev/watchdog` auf dem PC | BIOS-Einstellung prüfen, sonst `softdog` als Fallback laden |
| Änderungen zurücknehmen | Backups liegen unter `/etc/watchdog.conf.bak`, `/etc/systemd/system.conf.bak` und `/boot/firmware/config.txt.bak` |

---

### Automatisierungs-Skripte (DE)

Beide Skripte erledigen alle Schritte automatisch inklusive Backup, Hardware-Erkennung, Trockenlauf und Aktivierung. Sie müssen als `root` bzw. mit `sudo` ausgeführt werden.

#### Skript 1: Debian / Intel-Rechner (x86 PC)

```bash
#!/bin/bash

# --- FARBEN FÜR DIE AUSGABE ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Keine Farbe

echo -e "${YELLOW}=== Watchdog Installations-Script für Debian (Intel/x86 PC) ===${NC}"

# 1. Root-Check (Script muss als root laufen)
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[FEHLER] Bitte führen Sie dieses Script als root (oder mit sudo) aus!${NC}"
  exit 1
fi

# 2. Watchdog vorab entmaskieren (falls Notfall-Maskierung aktiv war)
systemctl unmask watchdog 2>/dev/null
systemctl stop watchdog 2>/dev/null

# 3. systemd Watchdog deaktivieren (Konfliktvermeidung)
echo -e "${YELLOW}[1/7] Deaktiviere systemd-internen Watchdog...${NC}"
if [ -f /etc/systemd/system.conf ]; then
  cp /etc/systemd/system.conf /etc/systemd/system.conf.bak
  sed -i -E 's/^[#]?\s*RuntimeWatchdogSec\s*=.*/#RuntimeWatchdogSec=0/g' /etc/systemd/system.conf
  systemctl daemon-reload
  echo -e "${GREEN}[OK] systemd-interner Watchdog deaktiviert.${NC}"
else
  echo -e "${YELLOW}[INFO] /etc/systemd/system.conf nicht gefunden. Überspringe.${NC}"
fi

# 4. Pakete installieren
echo -e "${YELLOW}[2/7] Installiere Pakete (watchdog, netcat-openbsd)...${NC}"
apt-get update -qq
apt-get install -y watchdog netcat-openbsd > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Pakete erfolgreich installiert.${NC}"
else
  echo -e "${RED}[FEHLER] Paket-Installation fehlgeschlagen!${NC}"
  exit 1
fi

# 5. Hardware-Modul laden & permanent eintragen
echo -e "${YELLOW}[3/7] Konfiguriere Hardware-Watchdog Modul...${NC}"

# Versuche Intel iTCO Watchdog zu laden
modprobe iTCO_vendor_support 2>/dev/null
modprobe iTCO_wdt 2>/dev/null

if [ -e /dev/watchdog ]; then
  echo -e "${GREEN}[OK] /dev/watchdog Hardware-Device ist vorhanden.${NC}"
  # Module für den Neustart vormerken
  grep -qxF "iTCO_vendor_support" /etc/modules 2>/dev/null || echo "iTCO_vendor_support" >> /etc/modules
  grep -qxF "iTCO_wdt" /etc/modules 2>/dev/null || echo "iTCO_wdt" >> /etc/modules
else
  echo -e "${YELLOW}[WARNUNG] Kein /dev/watchdog gefunden.${NC}"
  echo -e "          Das Mainboard unterstützt evtl. keinen iTCO-Watchdog oder er ist im BIOS deaktiviert."
  echo -e "          Lade Kernel-Software-Watchdog (softdog) als Fallback..."
  modprobe softdog
  grep -qxF "softdog" /etc/modules 2>/dev/null || echo "softdog" >> /etc/modules
fi

# 6. watchdog.conf konfigurieren
echo -e "${YELLOW}[4/7] Konfiguriere /etc/watchdog.conf...${NC}"

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
set_watchdog_option "watchdog-timeout" "60"         # Intel TCO unterstützt längere Timeouts als der Pi (60s ist optimal)
set_watchdog_option "retry-timeout" "120"           # WICHTIG: 2 Minuten Fehlertoleranz auf PCs
set_watchdog_option "max-load-1" "24"
set_watchdog_option "test-directory" "/etc/watchdog.d"

# WICHTIG: min-memory deaktivieren (verhindert False-Positives durch Linux-RAM-Cache)
sed -i -E 's/^[#]?\s*min-memory\s*=.*/#min-memory = 25600/' /etc/watchdog.conf

echo -e "${GREEN}[OK] /etc/watchdog.conf konfiguriert.${NC}"

# 7. Boot-sicheres SSH-Prüfskript anlegen
echo -e "${YELLOW}[5/7] Erstelle boot-sicheres SSH-Prüfskript...${NC}"
mkdir -p /etc/watchdog.d

cat << 'EOF' > /etc/watchdog.d/ssh_check
#!/bin/sh
# 1. Grace-Period: Wenn das System weniger als 300 Sek. (5 Min.) läuft,
# immer Erfolg (0) melden, um Bootschleifen beim Hochfahren zu verhindern.
UPTIME=$(awk '{print int($1)}' /proc/uptime)
if [ "$UPTIME" -lt 300 ]; then
    exit 0
fi

# 2. Explizit IPv4 (127.0.0.1) mit 2 Sekunden Timeout prüfen
nc -z -w 2 127.0.0.1 22
EOF

chmod +x /etc/watchdog.d/ssh_check
echo -e "${GREEN}[OK] Prüfskript unter /etc/watchdog.d/ssh_check erstellt.${NC}"

# 8. systemd-Dienstabhängigkeit anlegen (Start erst nach SSH)
mkdir -p /etc/systemd/system/watchdog.service.d
cat << 'EOF' > /etc/systemd/system/watchdog.service.d/override.conf
[Unit]
After=ssh.service
Wants=ssh.service
EOF
systemctl daemon-reload

# 9. Sicherheits-Trockenlauf & Start
echo -e "${YELLOW}[6/7] Führe Sicherheits-Trockenlauf durch...${NC}"
/etc/watchdog.d/ssh_check
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Trockenlauf erfolgreich! SSH antwortet wie erwartet.${NC}"
  echo -e "${YELLOW}[7/7] Aktiviere und starte den Watchdog-Dienst...${NC}"
  systemctl enable watchdog
  systemctl restart watchdog
  echo -e "${GREEN}=== INSTALLATION ERFOLGREICH BEENDET! ===${NC}"
else
  echo -e "${RED}[WARNUNG] Sicherheits-Trockenlauf fehlgeschlagen!${NC}"
  echo -e "${RED}          Der lokale SSH-Port (22) hat nicht geantwortet.${NC}"
  echo -e "${RED}Der Watchdog wurde NICHT gestartet, um eine Bootschleife zu verhindern!${NC}"
  exit 1
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

# 2. Watchdog vorab entmaskieren (falls Notfall-Maskierung aktiv war)
systemctl unmask watchdog 2>/dev/null
systemctl stop watchdog 2>/dev/null

# 3. systemd Watchdog deaktivieren (Konfliktvermeidung)
echo -e "${YELLOW}[1/7] Deaktiviere systemd-internen Watchdog...${NC}"
if [ -f /etc/systemd/system.conf ]; then
  cp /etc/systemd/system.conf /etc/systemd/system.conf.bak
  sed -i -E 's/^[#]?\s*RuntimeWatchdogSec\s*=.*/#RuntimeWatchdogSec=0/g' /etc/systemd/system.conf
  systemctl daemon-reload
  echo -e "${GREEN}[OK] systemd-interner Watchdog deaktiviert.${NC}"
fi

# 4. Hardware-Watchdog in Raspberry Pi Firmware aktivieren
echo -e "${YELLOW}[2/7] Aktiviere Hardware-Watchdog in der Pi-Boot-Konfiguration...${NC}"
CONFIG_FILE=""
if [ -f /boot/firmware/config.txt ]; then
  CONFIG_FILE="/boot/firmware/config.txt"  # Neuer Pfad (Bookworm)
elif [ -f /boot/config.txt ]; then
  CONFIG_FILE="/boot/config.txt"           # Alter Pfad (Buster/Bullseye)
fi

REBOOT_NEEDED=false
if [ -n "$CONFIG_FILE" ]; then
  if ! grep -q "^dtparam=watchdog=on" "$CONFIG_FILE"; then
    cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    echo "dtparam=watchdog=on" >> "$CONFIG_FILE"
    echo -e "${GREEN}[OK] Watchdog in $CONFIG_FILE aktiviert. (Backup erstellt).${NC}"
    REBOOT_NEEDED=true
  else
    echo -e "${GREEN}[OK] Watchdog bereits in $CONFIG_FILE aktiv.${NC}"
  fi
else
  echo -e "${RED}[FEHLER] Keine config.txt gefunden! Ist dies ein Raspberry Pi OS?${NC}"
  exit 1
fi

# 5. Pakete installieren
echo -e "${YELLOW}[3/7] Installiere Pakete (watchdog, netcat-openbsd)...${NC}"
apt-get update -qq
apt-get install -y watchdog netcat-openbsd > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}[OK] Pakete erfolgreich installiert.${NC}"
else
  echo -e "${RED}[FEHLER] Paket-Installation fehlgeschlagen!${NC}"
  exit 1
fi

# 6. watchdog.conf konfigurieren (Spezielle Pi-Werte!)
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

[ -f /etc/watchdog.conf ] && cp /etc/watchdog.conf /etc/watchdog.conf.bak

# Spezifische Raspberry Pi Einstellungen
set_watchdog_option "watchdog-device" "/dev/watchdog"
set_watchdog_option "interval" "4"                 # Prüfe alle 4 Sekunden
set_watchdog_option "watchdog-timeout" "15"         # Raspberry Pi Hardware-Limit (max 15s)
set_watchdog_option "retry-timeout" "60"            # WICHTIG: 60s Fehlertoleranz gegen Boot-Loops
set_watchdog_option "max-load-1" "24"
set_watchdog_option "test-directory" "/etc/watchdog.d"

# WICHTIG: min-memory deaktivieren (Fehlalarm-Risiko durch Linux-Page-Cache)
sed -i -E 's/^[#]?\s*min-memory\s*=.*/#min-memory = 12800/' /etc/watchdog.conf

echo -e "${GREEN}[OK] /etc/watchdog.conf sicher konfiguriert.${NC}"

# 7. Boot-sicheres Test-Skript für SSH-Port-Prüfung erstellen
echo -e "${YELLOW}[5/7] Erstelle boot-sicheres SSH-Prüfskript...${NC}"
mkdir -p /etc/watchdog.d

cat << 'EOF' > /etc/watchdog.d/ssh_check
#!/bin/sh
# 1. Grace-Period: In den ersten 5 Minuten nach dem Booten immer Erfolg melden,
# um Endlos-Reboots während des Hochfahrens sicher auszuschließen.
UPTIME=$(awk '{print int($1)}' /proc/uptime)
if [ "$UPTIME" -lt 300 ]; then
    exit 0
fi

# 2. Explizit IPv4 (127.0.0.1) mit 1 Sekunde Timeout prüfen
nc -z -w 1 127.0.0.1 22
EOF

chmod +x /etc/watchdog.d/ssh_check
echo -e "${GREEN}[OK] Prüfskript unter /etc/watchdog.d/ssh_check erstellt.${NC}"

# 8. systemd-Dienstabhängigkeit anlegen (Start erst nach SSH)
mkdir -p /etc/systemd/system/watchdog.service.d
cat << 'EOF' > /etc/systemd/system/watchdog.service.d/override.conf
[Unit]
After=ssh.service
Wants=ssh.service
EOF
systemctl daemon-reload

# 9. Sicherheits-Trockenlauf
echo -e "${YELLOW}[6/7] Führe Sicherheits-Trockenlauf durch...${NC}"
/etc/watchdog.d/ssh_check
SSH_OK=$?

if [ "$SSH_OK" -ne 0 ]; then
  echo -e "${RED}[FEHLER] Sicherheits-Trockenlauf fehlgeschlagen! SSH antwortet nicht.${NC}"
  echo -e "${RED}         Dienst wird zum Schutz nicht gestartet.${NC}"
  exit 1
fi
echo -e "${GREEN}[OK] Trockenlauf erfolgreich! SSH antwortet.${NC}"

# 10. Starten oder Reboot-Hinweis
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
  systemctl restart watchdog
  echo -e "${GREEN}=== FERTIG! Der Watchdog läuft und schützt den Pi. ===${NC}"
fi
```

!!! tip "Skript als Datei ablegen"
    ```bash
    sudo nano /root/watchdog-install.sh
    sudo chmod +x watchdog-install.sh
    sudo ./watchdog-install.sh
    ```
