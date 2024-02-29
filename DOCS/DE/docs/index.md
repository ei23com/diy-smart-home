# ei23 Smart Home Installationsskript

<span style="color:red">**Die Dokumentation befindet sich gerade um Aufbau**</span>

Hi und danke für dein Interesse an der Dokumentation!
Damit du dir schnell einen Überblick verschaffen kannst, habe ich den bisherigen Stand von meinem Smart Home Skript in einem Video:
[![YT](https://ei23.de/bilder/YTthumbs/pKUv_rXONas.webp)](https://www.youtube.com/watch?v=pKUv_rXONas)

## Warum brauchst du das Skript?

Zuerst zur Motivation hinter meinem Skript und seiner Veröffentlichung:

Um das Jahr 2017 herum plante ich die Installation eines Smart Home Systems. Es gab verschiedene Optionen zur Auswahl, und ich war unsicher, welches Programm das Richtige für mich war. Es war auch klar, dass ich einen Computer, in diesem Fall einen Raspberry Pi, dauerhaft betreiben würde. Es wäre schade gewesen, wenn darauf nur eine einzige Anwendung laufen würde. Zu diesem Zeitpunkt hatte ich bereits einige Experimente mit NodeRED durchgeführt und die Vorteile der GPIOs des Raspberry Pi geschätzt.

Obwohl mir das [Home Assistant System](https://home-assistant.io) insgesamt gut gefiel, bedeutete die Verwendung davon, dass ich die Flexibilität eines herkömmlichen Linux-Systems aufgeben musste. Deshalb habe ich einen Kompromiss gefunden: Mein Installations-Skript übernimmt die Installation und Einrichtung aller erforderlichen Programme und Einstellungen, und wenn möglich, werden alle Programme in Docker-Containern betrieben. Dies erleichtert die Wartung und Experimente am System erheblich und bietet mehr Komfort.

Das Skript entstand also aus der Notwendigkeit heraus, mehr Flexibilität, Anpassungsmöglichkeiten und Programme anzubieten als das Home Assistant Betriebssystem. Für diejenigen, die ihr System selbst erweitern möchten, ohne einen weiteren Server / Raspberry Pi oder virtuelle Maschinen parallel zu betreiben, bietet dieses Skript eine Lösung. Zuerst werden notwendige und nützliche Programme und Frameworks wie Docker, Python, etc. auf dem rohen Raspbian OS oder auch Debian installiert. Anschließend wird NodeRED in nativer Form installiert, nicht als Docker-Container. Dies bietet zusätzliche Funktionen und eine einfachere Konfiguration ohne lästige Workarounds. Darüber hinaus können Log2Ram (um SD-Karten-Schreibvorgänge zu reduzieren), RTL_SDR Software (zum Beispiel für 433MHz Sensoren) und rpiClone (für einfache Backups) direkt mit installiert werden. Das Skript automatisiert derzeit die Installation der folgenden Programme und enthält teilweise auch bereits einige Addons (eigene Erweiterungen sind natürlich möglich).

## Automatisierte Installation mit dem ei23 Smart Home Installationsskript

Ursprünglich war das System nur für den Raspberry Pi (armv7) verfügbar. Inzwischen empfehle ich jedoch die Verwendung eines 64-Bit-Systems (arm64). Das Skript ist auch auf Debian 12 und AMD64-Architekturen (einschließlich der meisten Docker-Container) funktionsfähig.

Du kannst das Skript ausschließlich über [meinen Newsletter](https://ei23.de/newsletter) beziehen. Dies ermöglicht es mir, einerseits einen kleinen Marketingeffekt zu erzielen und andererseits die Möglichkeit, dich zeitnah über Änderungen oder Sicherheitslücken zu informieren.

## Installation

Die Installation ist **selbsterklärend**.
Nach der [Anmeldung Newsletter](https://ei23.de/newsletter) bekommst du zwei Kommandozeilen zugeschickt, welche du über die Eingabekonsole oder SSH ausführen musst.

Die erste Zeile läd das Skript (Bash-Skript) herunter und mit der zweiten Zeile führst du es aus.

## Unterstützung

Die weiterentwicklung, Wartung und der Support von Software Projekten kosten viel Arbeit und Zeit.
Zu erwarten, dass es kostenlos ist, ist falsch.
Forderungen ohne Gegenleistung akzeptiere auch ich nicht auf dauer.

Denkt daher also über selbstlose Unterstüzung dieses (oder anderer) Projekte nach.
Das kann in Form von nützlichen Beiträgen, Hinweisen oder auch einfach in finanzieller Form passieren.
[Das geht hier](https://ei23.de/donate/)


Viel Spaß beim Tüfteln und unabhängig bleiben!
```
Viele Grüße
Felix von ei23
```

---