# Sicherheitsaudit: ei23.sh

**Datum:** 20. Februar 2026  
**Skript-Version:** v0 (SCRIPT_VERSION=0)  
**Auditor:** Automated Security Audit

---

## Zusammenfassung

Das Skript `ei23.sh` dient zur Installation und Verwaltung eines DIY Smart Home Servers mit Docker-Containern. Es wurden **mehrere kritische und hohe Sicherheitsrisiken** identifiziert, die dringend behoben werden sollten.

---

## Kritische Sicherheitsprobleme

### 1. Hardcodierte URLs und externe Abhängigkeiten

**Zeile 875:**
```bash
sudo wget "https://ei23.de/softwarehub/smarthome/USERID/$card/$SCRIPT_VERSION/ei23-docker.zip" -O ei23-docker.zip
```

**Risiko:**
- Download von Skripten/Archiven von externer Quelle ohne Integritätsprüfung
- Keine Signatur- oder Hash-Verifikation
- Man-in-the-Middle-Angriffe möglich
- Abhängigkeit von Single Point of Failure

**Empfehlung:**
- SHA256-Hash-Prüfung implementieren
- GPG-Signaturen verwenden
- Lokale/offline Installationsoption bereitstellen
- Multiple Mirror-Server unterstützen

---

### 2. Root-SSH-Login wird aktiviert

**Zeile 759:**
```bash
sudo sed -i -e 's#\#PermitRootLogin prohibit-password#PermitRootLogin yes#' /etc/ssh/sshd_config
```

**Risiko:**
- Ermöglicht direkte Root-Anmeldung per SSH
- Erhöht Angriffsfläche für Brute-Force-Angriffe
- Entspricht nicht Security-Best-Practices

**Empfehlung:**
- Root-Login deaktiviert lassen (`PermitRootLogin no`)
- SSH-Key-basierte Authentifizierung erzwingen
- Fail2Ban installieren und konfigurieren

---

### 3. Passwort-Handling im Klartext

**Zeilen 823-844:**
```bash
adminpass=$(whiptail --passwordbox "$L_PASSWORDFOR NodeRED" 8 60 3>&1 1>&2 2>&3)
# ...
bcryptadminpass=$(node -e "console.log(require('bcryptjs').hashSync(process.argv[1], 8));" $adminpass)
```

**Risiko:**
- Passwörter temporär im Klartext in Shell-Variablen
- Passwörter in Prozessliste sichtbar (ps aux)
- history-Einträge möglich

**Empfehlung:**
- `read -s` für Passworteingabe verwenden
- Variablen sofort nach Verwendung unsetten
- History für sensible Befehle deaktivieren

---

### 4. Unsichere Passwort-Generierung

**Zeilen 334-346:**
```bash
generate_password(){
   chars() { echo ${1:RANDOM%${#1}:1}; }
   # ...
}
```

**Risiko:**
- `RANDOM` ist kryptografisch nicht sicher
- Vorhersehbare Passwörter bei bekanntem Seed
- Zu schwach für sensible Anwendungen

**Empfehlung:**
```bash
generate_password(){
    openssl rand -base64 16
    # oder
    tr -dc 'A-Za-z0-9!@#$%' < /dev/urandom | head -c 16
}
```

---

### 5. Fehlende Input-Validierung

**Mehrfach im Skript, z.B. Zeile 688:**
```bash
program=$2
cd ~/ei23-docker/
composeCMD "stop $program"
```

**Risiko:**
- Command-Injection möglich
- Keine Validierung von Benutzereingaben
- Pfad-Traversierung möglich

**Empfehlung:**
- Whitelist für erlaubte Werte
- Input-Sanitization durchführen
- Keine ungeprüften Variablen in Befehlen

---

## Hohe Sicherheitsprobleme

### 6. Sudo ohne Passwort für Benutzer

**Zeile 706:**
```bash
echo '$IAM ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/010_$IAM-nopasswd
```

**Risiko:**
- Benutzer kann alle Befehle ohne Authentifizierung ausführen
- Erhöhtes Risiko bei kompromittiertem Account
- Entspricht nicht dem Prinzip der geringsten Rechte

**Empfehlung:**
- Sudo mit Passwort erzwingen
- Nur spezifische Befehle ohne Passwort erlauben
- Sudo-Logging aktivieren

---

### 7. Fehlende Berechtigungsprüfungen

**Zeile 699-705:**
```bash
if [ $EUID -eq 0 ]; then
  echo "do not use sudo and make sure you are not logged in as root"
  exit 0
fi
```

**Risiko:**
- Skript kann trotzdem mit Root-Rechten gestartet werden
- Keine strikte Verhinderung

**Empfehlung:**
- Exit mit Fehlercode bei Root-Ausführung
- Keine stillschweigende Fortsetzung

---

### 8. Unsichere Docker-Konfiguration

**Zeile 733 (auskommentiert, aber problematisch):**
```bash
# echo -e "{\n\t\t\"dns\": [\"$default_gateway\", \"208.67.222.222\"]\n}" | sudo tee /etc/docker/daemon.json
```

**Risiko:**
- Docker Daemon Konfiguration ohne Sicherheitsaudits
- Keine Netzwerk-Isolation zwischen Containern
- Fehlende Resource-Limits

**Empfehlung:**
- Docker Bench for Security ausführen
- Netzwerk-Policies definieren
- Container mit minimalen Rechten betreiben

---

### 9. Sensible Daten in Docker-Compose

**Zeile 903:**
```bash
sudo sed -i -e 's/password_placeholder/'$(generate_password)'/' "$DOCKERDIR/docker-compose.yml"
```

**Risiko:**
- Passwörter im Klartext in docker-compose.yml
- Keine Verschlüsselung sensibler Daten
- Versionierung sensibler Daten möglich

**Empfehlung:**
- Docker Secrets verwenden
- Externe Secret-Management-Lösungen (Vault)
- .env-Dateien mit restriktiven Berechtigungen

---

## Mittlere Sicherheitsprobleme

### 10. Fehlende Rate-Limiting Konfiguration

**Mosquitto MQTT Installation ohne Security-Hardening**

**Empfehlung:**
- Rate-Limiting für MQTT-Clients
- TLS-Verschlüsselung erzwingen
- Client-Zertifikate verwenden

---

### 11. UFW Firewall nicht konfiguriert

**Zeile 231:** UFW wird installiert, aber nicht konfiguriert
```bash
sudo apt-get install -y ... ufw ...
```

**Risiko:**
- Offene Ports ohne Filterung
- Keine Netzwerk-Segmentierung

**Empfehlung:**
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (nur wenn benötigt)
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

### 12. Fehlende Security-Headers

**Web-Anwendungen ohne Security-Hardening**

**Empfehlung:**
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security

---

### 13. Veraltete Software-Kanäle

**Zeile 113:** Node-RED Installation von GitHub
```bash
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```

**Risiko:**
- Ausführung von Skripten aus dem Internet
- Keine Versionskontrolle
- Supply-Chain-Angriffe möglich

**Empfehlung:**
- Feste Versionen verwenden
- Skripte lokal speichern und hashen
- Regelmäßige Updates durchführen

---

## Niedrige Sicherheitsprobleme

### 14. Fehlendes Logging und Monitoring

- Keine zentrale Logging-Lösung
- Keine Alerting-Mechanismen
- Keine Audit-Trails

### 15. Hardcodierte Pfade

- Eingeschränkte Portabilität
- Probleme bei Multi-User-Systemen

### 16. Fehlende Fehlerbehandlung

- Viele Befehle ohne Fehlerprüfung
- Unklares Fehlerverhalten

---

## Positive Aspekte

✅ Root-Ausführung wird grundsätzlich erkannt und abgelehnt  
✅ Passwort-Bestätigung wird implementiert  
✅ bcrypt für Passwort-Hashing wird verwendet  
✅ Docker-Isolation wird genutzt  
✅ Backup-Funktionalität vorhanden  
✅ UFW ist als Dependency enthalten  

---

## Priorisierte Empfehlungen

### Sofort (Kritisch)

1. **Externe Downloads signieren** - GPG/SHA256-Prüfung implementieren
2. **SSH Root-Login deaktivieren** - Konfiguration ändern
3. **Passwort-Generierung verbessern** - Kryptografisch sichere Zufallswerte
4. **Input-Validierung hinzufügen** - Alle Benutzereingaben prüfen

### Kurzfristig (Hoch)

5. **Sudo-Rechte einschränken** - Minimal Required Privileges
6. **Firewall konfigurieren** - UFW mit sinnvollen Regeln
7. **Docker-Security hardening** - Benchmarks anwenden
8. **Secret-Management** - Docker Secrets oder Vault

### Mittelfristig (Mittel)

9. **TLS-Verschlüsselung** - Für alle Dienste erzwingen
10. **Monitoring implementieren** - Security-Events loggen
11. **Regelmäßige Updates** - Automatisierte Security-Patches
12. **Network Segmentation** - VLANs für IoT-Geräte

---

## Checkliste für Sicherheitsverbesserungen

- [ ] GPG-Signatur für externe Downloads
- [ ] SSH Root-Login deaktivieren
- [ ] Fail2Ban installieren
- [ ] UFW-Regeln konfigurieren
- [ ] Passwort-Generator ersetzen
- [ ] Sudo-Rechte minimieren
- [ ] Docker Security Benchmarks
- [ ] TLS für alle Dienste
- [ ] Security-Headers implementieren
- [ ] Audit-Logging aktivieren
- [ ] Input-Validierung überall
- [ ] Rate-Limiting konfigurieren

---

## Fazit

Das Skript bietet umfangreiche Funktionalität für Smart-Home-Installationen, weist jedoch **erhebliche Sicherheitsmängel** auf. Die kritischen Punkte sollten **vor einem Produktiveinsatz unbedingt behoben** werden. Besonders die Kombination aus externem Download ohne Integritätsprüfung, aktiviertem Root-SSH-Login und schwacher Passwort-Generierung stellt ein inakzeptables Risiko dar.

**Gesamtbewertung:** 🔴 **Kritisch** - Nicht für Produktiveinsatz ohne Nachbesserungen

---

*Dieses Audit basiert auf statischer Code-Analyse. Ein vollständiges Security-Assessment sollte auch Penetration-Testing und dynamische Analyse umfassen.*
