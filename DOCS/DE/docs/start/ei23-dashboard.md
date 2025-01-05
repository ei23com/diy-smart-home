# Das ei23 Dashboard / Der Supervisor
![ei23 Dashboard](https://ei23.de/bilder/dashboard01.jpg)
Seit der Version 1.1 Von ei23 Smart Home Server hat sich das Dashboard grundlegend verändert. 
Jetzt ist es nicht nur mehr die Anzeige der verfügbaren Programme, sondern auch ein Supervisor. Zumindest ist der Unterbau schon mal so weit. Das heißt, mit dem Dashboard kann man bald auch einige Programme nachinstallieren und auch Systemfunktionen verwalten.

## Programme im Dashboard anpassen

Um Programme und externe Links wie z.B. Kameras oder andere Geräte oder auch Webseiten auf dem Dashboard zu verknüpfen, gibt es die Möglichkeit, die programs.json anzupassen.
Die Datei befindet sich unter `/home/[user]/ei23-docker/volumes/ei23/web/static/programs.json`
!!!note
    [user] muss an dieser Stelle durch deinen Nutzernamen ersetzt werden.

### Erklärung der `programs.json`

```json
{"programs": [
{"active": true,    "port": "",     "custom_url": "http://10.1.1.11:1880",  "name": "NodeRED",          "title": "Garage",              "img": "img/nodered.png"}, // (1)
{"active": true,    "port": "4004", "custom_url": "",                       "name": "MQTT-Explorer",    "title": "MQTT-Explorer",       "img": "img/mqtt-explorer.png"}, // (2)
{"active": false,   "port": "",     "custom_url": "http://10.1.1.12",       "name": "Kamera Garten",    "title": "Schöner Garten",      "img": "img/camera.png"}, // (3)
{"active": true,    "port": "3000", "custom_url": "",                       "name": "Grafana",          "title": "Datenvisualisierung", "img": "img/grafana.png"} // (4)
]}
```

1.   Hier ist "http://10.1.1.11:1880" eine Custom URL, diese kann auch eine externe Adresse sein.
2.   Wenn keine Custom URL gesetzt ist, wird der Port mit IP-Adresse des Geräts kombiniert. Beispielsweise http://10.1.1.2:4004
3.   Da Active auf False gesetzt ist, wird dieser Eintrag nicht gezeigt. Außerdem wird hier ein generisches Icon genutzt. Davon stehen einige im img Ordner zur Verfügung.
4.   Im letzten Eintrag ist es wichtig, dass kein Komma hinter der geschweiften Klammer angehängt wird.

!!!note
    1. Hier ist "http://10.1.1.11:1880" eine Custom URL, diese kann auch eine externe Adresse sein.
    2. Wenn keine Custom URL gesetzt ist, wird der Port mit IP-Adresse des Geräts kombiniert. Beispielsweise http://10.1.1.2:4004
    3. Da Active auf False gesetzt ist, wird dieser Eintrag nicht gezeigt. Außerdem wird hier ein generisches Icon genutzt. Davon stehen einige im img Ordner zur Verfügung.
    4. Im letzten Eintrag ist es wichtig, dass kein Komma hinter der geschweiften Klammer angehängt wird.


## Netzwerk: Geräte im Netzwerk auflisten und kontrollieren

![ei23 Dashboard](https://ei23.de/bilder/dashboard02.jpg)
Auf der Netzwerkseite gibt es die Möglichkeit, Geräte im Netzwerk zu scannen, deren Hostname, IP-Adresse, MAC-Adresse anzuzeigen und eine Herstellerinfo. Wenn ein Webport 80 erkannt wird, das heißt, dass das Gerät eine Weboberfläche zur Verfügung stellt, wird diese direkt verlinkt und das Gerät blau markiert.

## Server: Installierte Docker Compose Programme überprüfen

![ei23 Dashboard](https://ei23.de/bilder/dashboard03.jpg)
In dieser Ansicht wird automatisch die [docker-compose.yml](docker-compose.md) nach installierten und laufenden Containern bzw. Programmen durchsucht und damit eine Liste erstellt und angezeigt.
Ist ein Webport erkannt worden, wird das Programm dementsprechend markiert und kann auch direkt aufgerufen werden.
Dies kann praktisch sein, um einen schnellen Überblick der konfigurierten Programme und deren Ports zu bekommen oder die Weboberfläche direkt zu erreichen oder zu prüfen, ob das Programm läuft.
Auch wenn es automatisch passiert, kann es hilfreich sein, den Button für die Aktualisierung zu nutzen. So werden die Programme neu eingelesen und geprüft.

Außerdem kann unter dieser Ansicht auf die Schnelle die eigene Dokumentation für den Home-Server neu generiert werden.