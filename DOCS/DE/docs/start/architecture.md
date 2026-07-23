# Vergleich: Smart Home Server Architekturen

Diese Übersicht vergleicht die drei gängigsten Betriebskonzepte für einen privaten Smart Home Server (z. B. auf Basis eines AMD64 MiniPC oder ARM64 Raspberry Pi).

## 1. Schnellübersicht (Vergleichstabelle)

| Kriterium | `ei23` Roh (Debian Bare Metal) | `HAOS` Roh (Home Assistant OS) | Proxmox VE (HAOS VM + `ei23` LXC) |
| :--- | :--- | :--- | :--- |
| **Ressourcen-Overhead** | Minimal (~0%) | Minimal (~0%) | Gering bis Mittel (Hardware-abhängig) |
| **System-Isolation** | **Manuell:** Ohne konfigurierten Watchdog können Fehler in einem Dienst können den Host einfrieren. | **Gut:** Isolierte Docker-Add-ons, aber nur im HA-Universum. | **Hervorragend:** Volle Kapselung von VMs und LXCs. |
| **Backups & Rollbacks** | Manuell / Skript-basiert. Keine System-Snapshots. | HA-Backups (Teil-Backups über die UI). | **Hervorragend:** Instant-Snapshots und automatisierte Voll-Backups. |
| **Hardware-Zugriff (USB)** | Direkt & unkompliziert ohne Konfiguration. | Direkt & unkompliziert. | Erfordert Durchreichen (USB-Passthrough) im Hypervisor. |
| **HA Add-on Store** | Nein (Dienste müssen manuell via Docker-Compose gepflegt werden). | Ja (Vollständig integrierter Supervisor-Store). | **Ja** (durch den Betrieb von HAOS in einer eigenen VM). |
| **Lernkurve / Komplexität**| Mittel (Linux- & Docker-Grundwissen nötig). | Sehr gering (Plug-and-Play-Konsole wird kaum benötigt). | Hoch (Verständnis von Virtualisierung, Bridges und Speicher nötig). |
| **Hardware-Ausnutzung** | Sehr gut (perfekt für schwächere Hardware). | Mäßig (starke Hardware liegt oft brach, da keine Drittsysteme erlaubt sind). | **Hervorragend** (starke Hardware kann optimal aufgeteilt werden). |

---

## 2. Detaillierte Pro & Kontra Analyse

### Konzept 1: `ei23` Roh (Debian Bare Metal)
*Debian wird direkt auf der Hardware installiert. Das `ei23`-Skript richtet Docker, Portainer und die Smart-Home-Dienste als Container-Landschaft ein.*

#### **Pro**

  * **Maximale Effizienz:** Keine Virtualisierungsschicht. Nahezu 100 % der CPU-Leistung und des RAMs stehen den Anwendungen zur Verfügung.
  * **Einfacher Hardware-Zugriff:** USB-Sticks (Zigbee, Z-Wave), Bluetooth-Module oder physische Watchdogs (`/dev/watchdog`) funktionieren direkt out-of-the-box ohne Routing.
  * **Volle Linux-Freiheit:** Da ein Standard-Debian läuft, können beliebige eigene Hintergrund-Skripte, Crontabs oder System-Tools direkt auf dem Host installiert werden.
  * **Docker-Compose nützlich:** Perfekt für Entwickler und Bastler, die YAML-Dateien lieben und schnell neue Docker-Dienste testen wollen.

#### **Kontra**

  * **Mangelnde Isolation:** Hat ein Dienst ein Speicherleck, kann er den Arbeitsspeicher des gesamten Servers leersaugen. Das System gerät in das "Swapping-Koma" und wird komplett unerreichbar.
  * **Kein HA-Supervisor:** Home Assistant läuft als Core-Container. Es gibt keinen integrierten "Add-on Store" in der HA-Oberfläche; alle Zusatzdienste müssen manuell in der `docker-compose.yml` gepflegt werden.

---

### Konzept 2: `HAOS` Roh (Home Assistant OS direkt auf Hardware)
*Das offizielle, minimale Betriebssystem von Home Assistant wird direkt auf die Festplatte des PCs oder die SD-Karte des Pi geflasht.*

#### **Pro**

  * **Die "Sorglos-Blackbox":** Extrem einfache Installation und absolut wartungsarm. Updates des OS, des HA-Cores und der Add-ons erfolgen per Klick in der UI.
  * **Integrierter Supervisor:** Voller Zugriff auf den Add-on-Store (Node-RED, Mosquitto, InfluxDB etc. mit einem Klick installieren und vorkonfiguriert nutzen).
  * **Eingebaute Watchdogs:** Exzellentes automatisiertes Fehler-Handling. Stürzt ein Add-on oder Core ab, startet der Supervisor den Container sofort neu.
  * **Hohe Sicherheit:** Das zugrunde liegende Linux ist minimal und schreibgeschützt (*Read-Only*), was Angriffsflächen minimiert.

#### **Kontra**

  * **Kompletter Lock-in:** Es ist ein geschlossenes System. Es ist extrem schwierig oder unmöglich, Anwendungen zu betreiben, die nicht als HA-Add-on existieren (z. B. ein vollwertiges Nextcloud, eigene Webserver oder Custom-Docker-Compose-Stacks).
  * **Ressourcenverschwendung bei starker Hardware:** Wenn HAOS auf einem Mini-PC mit i5-Prozessor und 16 GB RAM läuft, langweilt sich die Hardware meistens zu 90 %, darf aber nicht für andere Server-Dienste genutzt werden.
  * **Inflexibel für Bastler:** Kein normaler SSH-Zugriff auf das Host-System, keine eigene Paketverwaltung (`apt`), keine Möglichkeit für tiefe System-Anpassungen.

---

### Konzept 3: Proxmox VE (HAOS VM + `ei23` LXC)
*Auf der Hardware läuft der Bare-Metal-Hypervisor Proxmox VE. Home Assistant OS wird in einer isolierten VM betrieben (inkl. Supervisor), während `ei23` und andere Dienste in einem leichtgewichtigen LX-Container (mit Docker-Nesting) laufen.*

#### **Pro**

  * **Perfekte Crash-Sicherheit:** Läuft der Arbeitsspeicher im `ei23`-LXC voll (z. B. durch InfluxDB), stürzt ausschließlich dieser LXC ab. Proxmox selbst und Ihre HAOS-VM laufen völlig unbeeindruckt und ohne Ausfallzeit weiter.
  * **Snapshots & schmerzfreie Upgrades:** Vor jedem riskanten Update (sei es ein Debian-Upgrade im LXC oder ein HA-Core-Update in der VM) wird ein Snapshot erstellt. Bei Fehlern erfolgt ein Rollback in 5 Sekunden.
  * **Das Beste aus beiden Welten:** Sie erhalten den Komfort von HAOS-Add-ons in der VM **und** die volle Flexibilität von Docker-Compose im `ei23`-LXC.
  * **Überragende Disaster Recovery:** Vollständige Backups der gesamten VMs/LXCs können automatisiert im laufenden Betrieb auf ein NAS oder eine externe Platte gesichert werden. Bei Hardware-Defekt ist das System auf jedem anderen Proxmox-PC in Minuten wiederhergestellt.

#### **Kontra**

  * **Virtualisierungs-Overhead:** Proxmox und die VMs benötigen permanent CPU-Zyklen und RAM. Für Systeme mit $\le$ 8 GB RAM oft zu schwer. Empfohlen ab 16 GB RAM.
  * **Zusätzliche Komplexitätsebene:** Der Anwender muss ein weiteres Betriebssystem (Proxmox VE) pflegen und Konzepte wie Virtual Bridges, LXCs, VMs und Storage-Typen verstehen.
  * **Hardware-Passthrough nötig:** USB-Geräte müssen in der Proxmox-Oberfläche manuell der jeweiligen VM oder dem LXC durchgereicht werden.