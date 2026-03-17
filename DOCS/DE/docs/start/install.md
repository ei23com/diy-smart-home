## Installation

Dieses Projekt ist ein super einfaches, sauberes und schlankes Installations- und Wartungstool für eine große Anzahl von meist Docker-basierter Home-Automation- und Medien-Software, die leicht über ein sauberes, schlankes und anpassbares Web-Dashboard zugänglich ist.

## Unterstützte Systeme

Das Skript funktioniert auf den folgenden Betriebssystemen und Architekturen:

- **Raspberry Pi OS** (armv7, arm64) - Getestet
- **Debian 12** (arm64, amd64) - Getestet  
- **Ubuntu / Pop!_OS** (arm64, amd64) - Getestet
- **Fedora** (amd64) - Getestet
- **Arch / Manjaro** (amd64) - Getestet
- **CentOS / Rocky** (amd64) - Getestet

!!!note "32-Bit Systeme"
    Für 32-Bit Systeme (armv7) wird das `docker-compose` Kommando anstelle von `docker compose` verwendet. Einige neuere Docker-Images sind möglicherweise nicht verfügbar.

Vielleicht ist es nicht ganz so einfach zu konfigurieren wie zum Beispiel Home Assistant OS, aber dafür bietet es deutlich mehr Anpassungsoptionen und ermöglicht dir den Umgang mit der docker-compose.yml-Syntax zu erlernen, was ebenfalls ein großartiges Werkzeug ist. Und du musst nicht einmal Home Assistant verwenden, wenn du lieber OpenHAB oder IObroker nutzen möchtest – alles auf einem System.

## Hardware-Empfehlung

!!!tip "Mini-PCs / ThinClients empfohlen"
    Obwohl der Raspberry Pi einen sehr geringen Stromverbrauch hat, ist die **Performance pro Watt** bei gebrauchten Mini-PCs und ThinClients oft deutlich besser. Für um die 50-100€ erhältst du gebrauchte x86-Systeme, die alle Docker-Images unterstützen und mehr Leistung bieten.
    
    Beispiele: **HP T620/T630**, **Dell Wyse 5070**, **Lenovo ThinkCentre M700** oder ein **Intel N100 Mini-PC**.
    
    [Mehr Details auf der Hardware-Seite](/hardware/server/)

Viel Spaß, werde smart und unabhängig!

### Einfache Installation:

Die einfache Installation ist selbsterklärend.
Nach der Anmeldung für den Newsletter ([ENGLISCHER NEWSLETTER](https://ei23.com/newsletter) / [DEUTSCHER NEWSLETTER](https://ei23.de/newsletter)) erhältst du zwei Befehlszeilen, die du über die Konsole oder SSH ausführen musst.
Die erste Zeile lädt das Skript (bash script) herunter, und die zweite Zeile führt es aus.

*Warum Newsletter?*

1. Ich kann dich schnell über Sicherheitslücken und interessante neue Features informieren.
2. Der Aufbau einer Community wird einfacher.
3. Ein wenig Werbung für meine Arbeit und das Projekt ist möglich.
4. Und ich könnte heimlich bösartigen Code in dein Skript einfügen und ein Botnetz aus einer großen Anzahl von Servern erstellen! - Natürlich mache ich das nicht! Oder glaubst du, ich würde das tun? Jetzt bin ich verwirrt... Warum sollte ich das tun, sollte ich es tun? Jetzt bist du verwirrt? Mach einfach keinen Ärger! Ok, zurück zum Thema xD

Die Dateien vom Newsletter sind identisch mit denen von Github, mit der Ausnahme einer eindeutigen USERID zum Herunterladen von Dateien von meinem Server und dem automatischen Setzen der LANGFILE, abhängig davon, welche Sprache vom Newsletter du wählst.
Außerdem werde ich dich nicht unnötig belästigen, wenn du bedenken hast nutze halt eine Wegwerf-Mail... Dann bin ich allerdings traurig.

### Manuelle Installation:

1. Klone die Dateien in einen Ordner `git clone https://github.com/ei23com/diy-smart-home.git`
2. Füge die Sprachdatei deiner Wahl (de-file.txt / en-file.txt) in die ei23.sh ein und ersetze den Platzhalter "LANGFILE_PLACEHOLDER".
3. Installiere ein frisches Debian / Rasbian-System, melde dich per SSH oder Terminal an und erstelle einen Benutzer wie folgt: "useradd -m ei23" (oder einen anderen Namen).
4. Kopiere den gesamten Ordner "ei23-docker" in das Home-Verzeichnis des Benutzers (mit Root-Rechten).
5. Kopiere die ei23.sh in das Home-Verzeichnis des Benutzers.
6. Führe "bash ei23.sh part1" aus.
7. Folge den Anweisungen.
8. Nach dem Neustart führe "ei23" aus, das Skript wird dann die Installation abschließen.

- Updates von ei23 funktionieren nicht bei manueller Installation (USERID aus dem Newsletter wird benötigt).
- Du wirst keine Versionsnummer sehen und keine Informationen über neue Versionen erhalten (USERID aus dem Newsletter wird benötigt).
- Alles andere funktioniert wie gewohnt.

## Nach der Installation

Nach der Installation findest du auf dem http Port und der IP Adresse deines Servers das [ei23-Dashboard](/start/ei23-dashboard).
Du kannst außerdem nun weitere Programme als [Docker Container installieren](/start/docker-compose)

## Weitere Fragen?

Für alles weitere verweise ich auf die [Häufigen Fragen - FAQ](/start/faq)
