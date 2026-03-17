# ei23 Smart Home Installationsskript

Hi und danke für dein Interesse an der Dokumentation! Damit du dir schnell einen Überblick verschaffen kannst, habe ich den bisherigen Stand meines Smart Home Skripts in einem Video zusammengefasst:
[![YT](https://ei23.de/bilder/ei23-dashboard.jpg)](https://www.youtube.com/watch?v=pKUv_rXONas)

## Warum brauchst du das Skript?

Zuerst zur Motivation hinter meinem Skript und seiner Veröffentlichung:

Um das Jahr 2017 plante ich die Installation eines Smart Home Systems. Es gab verschiedene Optionen zur Auswahl, und ich war unsicher, welches Programm das Richtige für mich war. Es war auch klar, dass ich einen Computer, in diesem Fall einen Raspberry Pi, dauerhaft betreiben würde. Es wäre schade gewesen, wenn darauf nur eine einzige Anwendung laufen würde. Zu diesem Zeitpunkt hatte ich bereits einige Experimente mit NodeRED durchgeführt und die Vorteile der GPIOs des Raspberry Pi geschätzt.

Obwohl mir das [Home Assistant System](https://home-assistant.io) insgesamt gut gefiel, bedeutete die Verwendung davon, dass ich die Flexibilität eines herkömmlichen Linux-Systems aufgeben musste. Deshalb habe ich einen Kompromiss gefunden: Mein Installations-Skript übernimmt die Installation und Einrichtung aller erforderlichen Programme und Einstellungen, und wenn möglich, werden alle Programme in Docker-Containern betrieben. Dies erleichtert die Wartung und Experimente am System erheblich und bietet mehr Komfort.

Das Skript entstand also aus der Notwendigkeit heraus, mehr Flexibilität, Anpassungsmöglichkeiten und Programme anzubieten als das Home Assistant Betriebssystem. Für diejenigen, die ihr System selbst erweitern möchten, ohne einen weiteren Server / Raspberry Pi oder virtuelle Maschinen parallel zu betreiben, bietet dieses Skript eine Lösung. Zuerst werden notwendige und nützliche Programme und Frameworks wie Docker, Python, etc. auf dem rohen Raspbian OS oder auch Debian installiert. Anschließend wird NodeRED in nativer Form installiert, nicht als Docker-Container. Dies bietet zusätzliche Funktionen und eine einfachere Konfiguration ohne lästige Workarounds. Darüber hinaus können Log2Ram (um SD-Karten-Schreibvorgänge zu reduzieren), RTL_SDR Software (zum Beispiel für 433MHz Sensoren) und rpiClone (für einfache Backups) direkt mit installiert werden. Das Skript automatisiert derzeit die Installation der folgenden Programme und enthält teilweise auch bereits einige Addons (eigene Erweiterungen sind natürlich möglich).

## Automatisierte Installation mit dem ei23 Smart Home Installationsskript

![ei23 terminal](https://ei23.de/bilder/ei23-terminal.gif)

Ursprünglich war das System nur für den Raspberry Pi (armv7) verfügbar. Inzwischen empfehle ich jedoch die Verwendung eines 64-Bit-Systems (arm64). Das Skript ist auch auf Debian 12 und AMD64-Architekturen (einschließlich der meisten Docker-Container) funktionsfähig.

Du kannst das Skript ausschließlich über [meinen Newsletter](https://ei23.de/newsletter) beziehen. Dies ermöglicht es mir, einerseits einen kleinen Marketingeffekt zu erzielen und andererseits die Möglichkeit, dich zeitnah über Änderungen oder Sicherheitslücken zu informieren.

## Installation

Die Installation ist **selbsterklärend**. Nach der [Anmeldung zum Newsletter](https://ei23.de/newsletter) bekommst du zwei Kommandozeilen zugeschickt, die du über die Eingabekonsole oder SSH ausführen musst. Die erste Zeile lädt das Skript (Bash-Skript) herunter, und mit der zweiten Zeile führst du es aus.

## Unterstützung

Die Weiterentwicklung, Wartung und der Support von Softwareprojekten kosten viel Arbeit und Zeit. Zu erwarten, dass es kostenlos ist, ist falsch. Forderungen ohne Gegenleistung akzeptiere auch ich nicht auf Dauer.

Denkt daher also über selbstlose Unterstützung dieses (oder anderer) Projekte nach. Das kann in Form von nützlichen Beiträgen, Hinweisen oder auch einfach in finanzieller Form passieren. [Das geht hier](https://ei23.de/donate/).

---

## 🏠 Alles kann automatisiert werden

Was ist überhaupt möglich mit einem Smart Home? Hier ein paar Beispiele:

- 🚗 Garagentor öffnet sich, wenn sich das Auto nähert
- 🔔 Türklingel lässt Telefone klingeln und öffnet optional die Haustür
- 📬 Nachricht mit Bild aufs Handy, wenn die Post da war
- 👕 Nachricht, wenn die Waschmaschine fertig ist (über Stromverbrauchsmessung)
- ⏰ Lichter mit dem Handy-Wecker koppeln
- ☀️ Lichthelligkeit an die Photovoltaik-Erzeugung anpassen
- 👤 Lichter über Anwesenheit steuern
- 📹 Kameras als Bewegungsmelder nutzen
- ⚡ Wenn der Stromzähler zu viel Verbrauch zeigt – Licht zur Warnung anschalten (und noch mehr Strom verbrauchen 😄)

Ja, jede noch so dämliche Spielerei ist denkbar. Oder wie ich gerne scherze – **die moderne Modelleisenbahn im Keller**.

### Ist das alles nötig?

Auf keinen Fall. Nur wenn es wirklich Energie oder Zeit spart – und damit auch Geld.

**Werde nicht zum Feature-Creep.** Die Dinge einfach zu halten, ist eine Kunst. Wenn dir etwas ständig Probleme macht, verlierst du die Lust. Aber wenn du bereit bist, ein bisschen Zeit zu investieren und dir ein paar neue Dinge beizubringen, ist **unendlich viel möglich**.

Und du wirst smart und unabhängig. Das ist sehr wertvoll.

---

## 🔓 Warum das alles wichtig ist

Mir geht es nicht nur um coole Spielereien. Mir geht es darum, ein bestimmtes Szenario zu **verhindern**.

Schaut euch an, was gerade passiert: Smarte Lautsprecher, smarte Thermostate, smarte Kameras – alles wird über die Cloud von wenigen großen Konzernen betrieben. Amazon, Google, Apple. Die haben die Kontrolle, die bekommen die Daten und haben die Macht. Wir werden immer mehr abhängig davon.

**Das ist der Weg in ein Cyberpunk-Szenario.** Megacorps, die über die Infrastruktur deines Alltags bestimmen. Features, die einfach verschwinden. Preise, die steigen. Daten, die du nicht kontrollierst. Dienste, die plötzlich eingestellt werden.

Das können wir nur verhindern, wenn **so viele wie möglich smart und unabhängig werden**. Mit eigener Hardware. Mit Open Source Software. Ohne monatliche Gebühren. Ohne Cloud-Zwang. Ohne Big Tech.

**Dein Zuhause gehört dir. Deine Daten gehören dir. Deine Automatisierungen gehören dir.**

Und genau dafür steht ei23.

---

## Statistik

![ei23 Counter](https://ei23.de/bilder/svg-stats.svg)

*Viel Spaß beim Tüfteln – und lasst euch die Kontrolle nicht wegnehmen!* 🏠🔓

```
Viele Grüße
Felix von ei23
```

---