docker-compose.md
##  Wie passe ich die Startseite mit den Programmen an, kann ich eigene Programme hinzufügen?</strong>
Ja, du kannst eigene Programme oder Netzwerkgeräte zur Startseite hinzufügen.
Dazu musst du die Datei `/home/pi/ei23-docker/volumes/ei23/web/programs.json` zeilenweise anpassen:
Unter `/home/pi/ei23-docker/volumes/ei23/web/programs_templates.json` findest du auch neu hinzugefügte Programme nach einem Update.
Es lassen sich auch externe Seiten ins Dashboard aufnehmen - als Beispiel die IP 192.168.0.1:
`{"active":true, "port" : "", "custom_url":"http://192.168.0.1", "name": "Router", "title": "Router", "img":"img/router.png"},`
Achtung! Die letzte dieser Art von Zeilen darf nicht mit einem Komma enden.
Die Seite wird in der Regel vom Browser im Cache gespeichert, also kann es nötig sein diesen vorher zu leeren (Mit Strg-F5 oder in den Browser-Chronik Einstellungen)
Im Video erkläre ich es auch kurz: [Video zu Skript v0.9](https://www.youtube.com/watch?v=pKUv_rXONas&t=140s)

##  Wie führe ich Updates für Programme durch?</strong>
Im SSH-Terminal `bash ei23.sh` und dann "Komplettes Update" auswählen und Enter drücken. Ganz einfach.

##  Ich möchte Programme nachträglich installieren oder entfernen</strong>
siehe [Programme Installieren](docker-compose.md)


##  Programm XY funktioniert nicht, wie setze ich es ohne Neuinstallation zurück?</strong>
Portainer wird beispielsweise mit folgendem Befehl zurückgesetzt (Das klappt analog mit allen anderen Programmen <strong>außer</strong> mit dem ei23-Dashboard, Home Assistant, Mosquitto und NodeRED):
`cd ei23-docker/; docker-compose stop portainer; docker-compose rm -f portainer; sudo rm -r volumes/portainer/; docker-compose up -d`
Für NextcloudPi sähe es so aus
`cd ei23-docker/; docker-compose stop nextcloudpi; docker-compose rm -f nextcloudpi; sudo rm -r volumes/nextcloudpi/; docker-compose up -d`
Home Assistant wird wie folgt zurückgesetzt:
`cd ei23-docker/; docker-compose stop homeassistant; docker-compose rm -f homeassistant; sudo rm -r volumes/homeassistant/config/.storage; sudo rm -r volumes/homeassistant/config/.cloud; sudo rm -r volumes/homeassistant/config/deps; sudo rm -r volumes/homeassistant/config/.storage; sudo rm -r volumes/homeassistant/config/tts; sudo rm volumes/homeassistant/config/home-assistant_v2.db; docker-compose up -d`
Sollte beispielsweise NodeRED nicht funktionieren liegt wahrscheinlich ein anderes Problem vor. Siehe "Welche Geräte und Betriebssysteme werde unterstützt?"

##  Wie kann ich einen Zigbee / ConBee 2 Stick ingegrieren oder einen USB-Stick mounten</strong>
Da der großteil der Programme als Docker Container installiert sind, muss dafür die docker-compose.yml (unter `/home/[user]/ei23-dockerdocker-compose.md.yml` ) bearbeitet werden.

Eine Beschreibung wie man Geräte (Devices) und Ordner (Volumes) des Host-Systems in einen Docker-Container einbindet, findest du hier [Programme Installieren](docker-compose.md) 

##  Welche Geräte und Betriebssysteme werden unterstützt?</strong>
Offiziell teste und entwickle ich mit einem Raspberry Pi 4 (min 2GB) mit einem frisch installiertem Raspberry Pi OS und dazu noch einer Virtuellem Maschine mit Debian 12 64Bit.
Auf Grund der vielen Variationen, die allein durch Verschiedene Spracheinstellungen auftreten können. Kann es hier und da zu kleinen Fehlern kommen.
Dafür biete ich keine kostenlose Hilfe und Lösungen an, denn es ist und bleibt ein DIY-Projekt und keine Dienstleistung mit Garantieansprüchen.

##  Ich habe selbst ein Programm installiert, jetzt geht ein anderes nicht mehr!</strong>
Es kann zu Portüberlagerungen kommen - beispielsweise dazu mal die docker-compose.yml (in home/pi/ei23-docker) untersuchen.
siehe [Programme Installieren](docker-compose.md)
Grundsätzlich kann alles, was nicht über das Skript oder nach einer ei23 Anleitung installiert wird, zu Problemen führen und selbst dann kann es zu Problemen kommen. Hier gilt DIY!

##  Es gibt den Befehl grafana-cli nicht! / Ich finde den apache / nginx nicht im / var/www/Verzeichnis ( Befehle in Docker Containern ausführen )</strong>
Alle Programme die in einem Docker Container laufen sind logischerweise nicht direkt über den Terminal erreichbar und die Verzeichnisse sind ebenfalls vom Hostsystem abgekapselt.
Um Befehle in einem Docker Container auszuführen muss Folgendes vor den Befehl angefügt werden:
`docker exec -it Containername Befehl` also bei Grafana beispielsweise `docker exec -it grafana /bin/bash`
/bin/bash ist der Befehl mit dem eine bash Sitzung gestartet wird.
`docker exec -it grafana grafana-cli` geht natürlich auch.
Alternativ kannst du über Portainer auch eine Terminalsitzung für den jeweiligen Container starten.

##  Ich kann NodeRED und die Software für den RTL-SDR DVB-T Stick nicht in der Docker-Compose.yml oder in den Templates finden!</strong>
Das ist richtig. NodeRED und auch die Software für den RTL-SDR DVB-T Stick werden bei der Erstinstallation nativ, also nicht als Docker Container installiert. NodeRED nicht zu installieren ist im ei23-Skript übrigens keine Option, da man NodeRED in der Regel sowieso früher nutzen sollte. Es ist einfach sehr gut.

##  Kannst du Programm XY auch in das Skript einbauen?</strong>
Möglicherweise, wenn es nicht zu Konflikten mit anderen Programmen kommt und ich die Zeit dafür finde ja.
Es ist allerdings Ratsam nicht gleich alle Programme die das Skript bietet, auch gleichzeitig laufen zu haben. Es wird fast niemanden geben, der OpenHAB, IOBroker, FHEM und HomeAssistant gleichzeitig braucht und dann kommt der Pi auch nicht so ins Schwitzen ;-)

##  Wie ändere ich die Passwörter und Nutzernamen?</strong>
Das geht mit dem Skript. Einfach `ei23` ausführen.

##  Gibt es Kurzbefehle?</strong>
Ja! Einfach `ei23 -h` ausführen.

##  Welche Wetterstationen und 433Mhz kann ich mit dem RTL-SDR DVB-Stick einbinden?</strong>
Du findest auf der [Projektseite](https://github.com/merbanan/rtl_433) eine Auflistung.
Die meisten unverschlüsselten 433Mhz Geräte sollten funktionieren.

##  Ist die Übertragung über unverschlüsseltes 433Mhz sicher? Wie ist die Reichweite?</strong>
Nein, unverschlüsseltes 433Mhz sollte maximal für Temperatursensoren, Wetterstationen, oder für Kontaktsensoren in unkritischen Bereichen genutzt werden und man sollte sich bewusst sein, dass der Nachbar theoretisch mitprotokollieren oder Signale klonen/fälschen kann.
Also: Kenne deinen Nachbarn ;-)
Der große Vorteil ist vor allem der Preis und die Verbreitung.
Die Reichweite von 433Mhz Geräten ist leider meist nur geringfügig besser als bei WLAN mit 2.4Ghz.
W-LAN ist dagegen in der Regel verschlüsselt, aber braucht mehr Strom (bei Batteriebetrieb) und ist teurer.

##  Wo finde ich die Konfigurationsdateien von Home Assistant?</strong>
Der Ordner mit den Konfigurationsdateien und der Datenbank von Home Assistant hat den Pfad:
`/home/[user]/ei23-docker/volumes/homeassistant/config`
Wenn Home Assistant nicht richtig startet weil beispielsweise die "automations.yml" fehlt, kann man die Datei mit folgendem Kommandozeilenbefehl erstellen und Home Assistant neu starten.
`sudo echo "" > /home/pi/ei23-docker/volumes/homeassistant/config/automations.yml; cd ei23-docker/; docker-compose restart homeassistant; cd ~`

##  Wie installiere ich AddOns in Home Assistant?</strong>
Zunächst muss zwischen Integrationen / Frontend-Addons und Drittanbieter Programm-Addons (wie NodeRED, InfluxDB, Grafana etc.) unterscheiden werden: 
Integrationen / Frontend-Addons können wie auch in HassIO über den [Community Store (HACS)](https://hacs.xyz/) oder manuell in den `/home/pi/ei23-docker/volumes/homeassistant/config` installiert werden.
Wie bereits erwähnt: Das Skript ist aus der Notwendigkeit entstanden mehr Flexibilität und Anpassungsmöglichkeiten als das HassIO Betriebssystem zu bieten. HassIO nutzt für die Installation von Drittanbieter Programm-Addons den Home Assistant Supervisor. Diese Art von Addons werden auch in HassIO in der Regel als Docker Container installiert.
Da das Skript in großen Teilen die von Funktion vom Home Assistant Supervisor übernimmt, ist dieser aus Redudanz- und Kompatiblitätsgrunden nicht enthalten, stattdessen installiert das Skript Home Assistant Core und als Supervisor dienen hier die Funktionen des Skriptes. Siehe auch [Programme Installieren](docker-compose.md)

##  Wie verbinde ich Home Assistant mit NodeRED?</strong>
Das vorinstallierte Home Assistant Addon für NodeRED muss lediglich konfiguriert werden.
Dazu muss in Home Assistant in den Benutzereinstellungen ein Langzeittoken (Access Token) erstellt werden und dieser kann dann für das NodeRED Home Assistant Addon genutzt werden.
Als Url sollte dort http://localhost:8123 eingetragen werden.

##  Wie binde ich Kameras in MotionEYE ein und welche Kameras funktionieren</strong>
Auf [ispyconnect.com](https://www.ispyconnect.com/sources.aspx) gibt es eine Liste von Kameras mit der dazugehörige URL für den Videostream. Diese URL muss in MotionEYE eingefügt werden.
Wenn es eine URL zum Video Stream gibt, ist die Wahrscheinlichkeit sehr hoch, dass man die Kamera auch in MotionEYE einbinden kann.
Es gibt dazu gute Anleitungen im Netz, aber ich mache dazu auch noch ein Video demnächst.

##  Warum erstellst du kein Image, wäre das nicht einfacher?</strong>
Nein!

##  Wann kommt ein Video zur Sprachsteuerung / Axel!</strong>
Ist da!
[![YT](https://ei23.de/bilder/YTthumbs/xYB2sl9Sav8.webp)](https://www.youtube.com/watch?v=xYB2sl9Sav8)