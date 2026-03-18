# Sicherheitsaudit: ei23.sh Smart Home Server Installationsskript

## ⚠️ WICHTIGER SICHERHEITSHINWEIS

Dieses Skript wurde für **vertrauenswürdige Umgebungen** entwickelt, in denen der Nutzer die Sicherheitsimplikationen vollständig versteht. Es ist **NICHT** für den Einsatz in produktiven oder öffentlich zugänglichen Umgebungen ohne zusätzliche Sicherheitsmaßnahmen geeignet.

---

## 1. Zusammenfassung der Sicherheitsprobleme

| Kategorie | Schweregrad | Status |
|-----------|-------------|--------|
| SSH Root-Login | 🔴 KRITISCH | Designentscheidung |
| Sudo ohne Passwort | 🔴 KRITISCH | Designentscheidung |
| Passwort-Generierung | 🟠 MITTEL | Verbesserungsbedürftig |
| Netzwerk-Exposition | 🟠 MITTEL | Konfigurationssache |
| Container-Isolation | 🟡 NIEDRIG | Docker-abhängig |

---

## 2. Kritische Sicherheitsprobleme im Detail

### 2.1 SSH Root-Login aktiviert

**Zeile 780-783:**
```bash
# Enable SSH root-login
if [ -f "/etc/ssh/sshd_config" ]; then
    sudo sed -i -e 's#\#PermitRootLogin prohibit-password#PermitRootLogin yes#' /etc/ssh/sshd_config
fi
```

**Problem:**
- Root-Login via SSH wird explizit aktiviert
- Ermöglicht direkten Zugriff auf den Superuser-Account
- Erhöht das Risiko von Brute-Force-Angriffen

**Risiko:** 🔴 **KRITISCH**
- Vollständige Systemübernahme bei kompromittierten Credentials
- Umgehung von Audit-Trails (wer hat was als root getan?)

**Designentscheidung:**
> Diese Funktion wurde bewusst implementiert für einfache Erstinstallationen in isolierten Labornetzwerken. Der Nutzer muss sich der Risiken bewusst sein.

**Empfehlung:**
```bash
# Nach der Installation deaktivieren:
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Stattdessen SSH-Keys verwenden:
sudo mkdir -p /root/.ssh
sudo cp /home/$IAM/.ssh/authorized_keys /root/.ssh/
```

---

### 2.2 Sudo ohne Passwort

**Zeile 661-670:**
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
- Der Benutzer erhält sudo-Rechte **ohne Passwortabfrage**
- Datei: `/etc/sudoers.d/010_$IAM-nopasswd`
- Jede beliebige Anwendung des Benutzers kann Root-Befehle ausführen

**Risiko:** 🔴 **KRITISCH**
- Malware kann sich unbemerkt sudo-Rechte verschaffen
- Kein Schutz vor versehentlichen destruktiven Befehlen
- Umgehung von Sicherheitskontrollen

**Designentscheidung:**
> Für Automatisierungszwecke und einfache Bedienung in vertrauenswürdigen Umgebungen. Der Nutzer akzeptiert das Risiko.

**Empfehlung:**
```bash
# Nach Installation Passwort-Schutz aktivieren:
sudo rm /etc/sudoers.d/010_$IAM-nopasswd
# Oder zumindest Passwort für kritische Befehle erzwingen
```

---

### 2.3 Passwort-Generierung

**Zeile 358-370:**
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
- Verwendung von `$RANDOM` (nicht kryptografisch sicher)
- 12 Zeichen Länge ist minimal
- `sort -R` verwendet nicht-kryptografischen Zufallsgenerator

**Risiko:** 🟠 **MITTEL**
- Passwörter sind theoretisch vorhersagbar
- Ausreichend für lokale/isolierte Netzwerke
- Nicht geeignet für öffentlich zugängliche Dienste

**Empfehlung:**
```bash
# Bessere Alternative:
generate_password(){
    openssl rand -base64 16 | tr -d '\n'
}
# Oder:
generate_password(){
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1
}
```

---

### 2.4 Netzwerk-Exposition

**Docker-Container ohne Netzwerk-Isolation:**

Viele Container exponieren Ports direkt:
- Home Assistant: 8123
- Node-RED: 1880
- Mosquitto: 1883, 9001
- Pi-hole: 80, 443
- Nextcloud: 80/443

**Risiko:** 🟠 **MITTEL**
- Alle Dienste sind im lokalen Netzwerk erreichbar
- Keine Firewall-Konfiguration im Skript
- UFW wird installiert aber nicht konfiguriert

**Empfehlung:**
```bash
# Firewall nach Installation konfigurieren:
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 8123/tcp  # Home Assistant (nur wenn benötigt)
sudo ufw enable
```

---

### 2.5 Container-Sicherheit

**Problem:**
- Container laufen standardmäßig als root
- Keine Resource-Limits konfiguriert
- Keine Security-Options (AppArmor, Seccomp)

**Risiko:** 🟡 **NIEDRIG**
- Bei Container-Escape volles System kompromittierbar
- Ressourcen-Missbrauch möglich

---

## 3. Weitere Sicherheitsaspekte

### 3.1 Installierte Pakete

**Zeile 214:**
```bash
sudo apt-get install -y arp-scan autoconf build-essential cmake curl rsync expect ffmpeg gcc git htop btop imagemagick imagemagick-doc jq libcurl4-openssl-dev libfftw3-dev libimage-exiftool-perl libtool libusb-1.0 mkdocs mosquitto-clients mpg123 ncdu ncftp netdiscover nmap parted pkg-config pv python3-full python3-venv screen ssh sshpass sysfsutils tcpdump telnet ufw unzip usbutils virtualenv wireguard zsh
```

**Kritische Werkzeuge:**
- `sshpass` - Passwort-basierte SSH-Authentifizierung
- `tcpdump` - Netzwerk-Traffic-Analyse
- `nmap` - Netzwerk-Scanner
- `netdiscover` - Netzwerk-Erkennung
- `expect` - Automatisierung von Passwort-Eingaben

**Risiko:** 🟡 **NIEDRIG**
- Diese Tools können für Angriffe missbraucht werden
- In vertrauenswürdigen Umgebungen akzeptabel

---

### 3.2 Standard-DNS für Docker

**Zeile 732-736 (auskommentiert):**
```bash
# set OpenDNS as default DNS for Docker-Containers
# default_gateway=$(ip route | grep default | awk '{print $3}')
# echo -e "{\n\t\t\"dns\": [\"$default_gateway\", \"208.67.222.222\"]\n}" | sudo tee /etc/docker/daemon.json
```

**Hinweis:**
- DNS-Konfiguration ist auskommentiert
- Container verwenden Host-DNS oder eigene Konfiguration
- DNS-Leaking möglich

---

### 3.3 Dateiberechtigungen

**Mehrere Stellen im Skript:**
```bash
sudo chown -R 1883:1883 $DOCKERDIR/volumes/mosquitto/
sudo chown -R $IAM $HOME/.node-red/lib/
```

**Problem:**
- Volume-Berechtigungen werden gesetzt
- Container-spezifische User-IDs (z.B. 1883 für Mosquitto)
- Potenzial für Berechtigungsprobleme

---

### 3.4 Externe Skript-Downloads

**Zeile 859:**
```bash
sudo wget "https://ei23.de/softwarehub/smarthome/USERID/$card/$SCRIPT_VERSION/ei23-docker.zip" -O ei23-docker.zip
```

**Risiko:** 🟠 **MITTEL**
- Download von externer Quelle
- Abhängigkeit von ei23.de-Server
- Kein Hash-Check der Downloads

**Empfehlung:**
- SHA256-Prüfsummen implementieren
- Signaturen für Updates verwenden

---

### 3.5 Node-RED npm-Pakete

**Zeile 113-119:**
```bash
for addonnodes in moment node-red-contrib-boolean-logic ...; do
    npm $NOLOGNODE install --no-audit --no-update-notifier --no-fund --save --save-prefix="~" --production ${addonnodes}@latest
done
```

**Problem:**
- `--no-audit` überspringt Sicherheitsprüfungen
- Viele Drittanbieter-Pakete
- Supply-Chain-Angriffe möglich

---

## 4. Sicherheits-Checkliste nach Installation

### 🔴 Sofortmaßnahmen (KRITISCH)

- [ ] SSH Root-Login deaktivieren (wenn nicht explizit benötigt)
- [ ] Sudo-Passwortabfrage aktivieren
- [ ] Standardpasswörter aller Dienste ändern
- [ ] Firewall (UFW) konfigurieren und aktivieren

### 🟠 Kurzfristig (MITTEL)

- [ ] SSH auf Key-basierte Authentifizierung umstellen
- [ ] Nicht benötigte Dienste deaktivieren
- [ ] Regelmäßige Updates einplanen
- [ ] Backup-Strategie implementieren

### 🟡 Langfristig (NIEDRIG)

- [ ] Container-Security-Options prüfen
- [ ] Netzwerk-Segmentierung erwägen
- [ ] Monitoring einrichten
- [ ] Security-Audits automatisieren

---

## 5. Sicherheitsempfehlungen

### 5.1 Für Produktionsumgebungen

```bash
#!/bin/bash
# NACH der Installation ausführen:

# 1. SSH härten
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# 2. Sudo schützen
sudo rm /etc/sudoers.d/010_*-nopasswd

# 3. Firewall aktivieren
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw enable

# 4. Fail2Ban installieren
sudo apt-get install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 5.2 Für Testumgebungen

- Nur in isolierten Netzwerken betreiben
- Kein Port-Forwarding im Router
- Regelmäßige Sicherheitsupdates durchführen
- Netzwerk-Traffic überwachen

---

## 6. Fazit

### Designentscheidungen vs. Sicherheitslücken

| Feature | Entscheidung | Risiko |
|---------|--------------|--------|
| SSH Root-Login | ✅ Bewusst | Hoch |
| Sudo NOPASSWD | ✅ Bewusst | Hoch |
| $RANDOM Passwörter | ⚠️ Bequemlichkeit | Mittel |
| --no-audit npm | ⚠️ Bequemlichkeit | Mittel |
| UFW ohne Regeln | ⚠️ Unvollständig | Mittel |

### Zielgruppe

Dieses Skript richtet sich an:
- ✅ Erfahrene Nutzer in Labornetzwerken
- ✅ Entwickler für lokale Tests
- ✅ Smart-Home-Enthusiasten mit Sicherheitsbewusstsein

**NICHT geeignet für:**
- ❌ Öffentlich zugängliche Server
- ❌ Produktionsumgebungen ohne Nachhärtung
- ❌ Nutzer ohne Sicherheitsgrundwissen

---

## 7. Haftungsausschluss

> **WICHTIG:** Der Nutzer ist selbst verantwortlich für die Sicherheit seines Systems. Dieses Skript wird "as-is" bereitgestellt. Der Autor übernimmt keine Haftung für Sicherheitsvorfälle, Datenverlust oder Schäden, die durch die Verwendung entstehen.

**Vor der Installation sicherstellen:**
1. Vollständiges Verständnis der Sicherheitsimplikationen
2. Isolierte Testumgebung vorhanden
3. Backup-Strategie implementiert
4. Regelmäßige Wartung eingeplant

---

## 8. Anhang: Sicherheits-Härtungsskript

```bash
#!/bin/bash
# security-hardening.sh - NACH der Installation ausführen

echo "=== Sicherheits-Härtung für ei23 Smart Home Server ==="

# 1. SSH Root-Login deaktivieren
echo "[1/5] Deaktiviere SSH Root-Login..."
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# 2. SSH Passwort-Auth deaktivieren (nur Keys)
echo "[2/5] Aktiviere nur SSH Key-Authentifizierung..."
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# 3. Sudo-Passwort erzwingen
echo "[3/5] Aktiviere Sudo-Passwortabfrage..."
sudo rm -f /etc/sudoers.d/010_*-nopasswd

# 4. Firewall konfigurieren
echo "[4/5] Konfiguriere UFW Firewall..."
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
# Nur benötigte Ports freigeben:
# sudo ufw allow 8123/tcp  # Home Assistant
# sudo ufw allow 1880/tcp  # Node-RED
sudo ufw --force enable

# 5. Fail2Ban installieren
echo "[5/5] Installiere Fail2Ban..."
sudo apt-get install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# SSH neu starten
sudo systemctl restart sshd

echo "=== Härtung abgeschlossen! System neu starten empfohlen ==="
```