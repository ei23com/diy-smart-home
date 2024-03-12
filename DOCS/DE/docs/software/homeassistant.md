# Home Assistant
(Noch im Aufbau)

## Home Assistant Docker vs. Supervised Home Assistant

Es gibt zwei Versionen von Home Assistant:<br>
1. Home Assistant Docker<br>
2. Supervised Home Assistant (auch bekannt als Home Assistant OS)<br>

In diesem Skript verwenden wir Home Assistant Docker. Das hat zwar Nachteile auf der einen Seite, bietet jedoch auf der anderen Seite deutlich mehr Vorteile. Die "Nachteile" beinhalten das Fehlen von "Addons" im Sinne von Home Assistant OS und die notwendige Konfiguration von Hardware über die [docker-compose.yml](/start/docker-compose). Es ist wichtig zu erwähnen, dass die Addons technisch gesehen vorkonfigurierte Docker Container sind. Der Supervisor übernimmt lediglich einen Teil der Konfiguration. Dieses Skript bietet jedoch die [docker-compose Templates](/start/docker-compose), die die Konfiguration vereinfachen.
Das [Einbinden von Hardware](#hardware) ist mit ein paar Anweisungen außerdem nicht kompliziert.

Ein Nachteil von Home Assistant OS ist, dass wenn ein "Addon" nicht für Home Assistant OS verfügbar ist, man darauf angewiesen ist, dass die Entwickler oder die Community ein solches erstellen. Die Anzahl der verfügbaren Docker Images hingegen ist unverhältnismäßig größer, was einen großen Vorteil darstellt. Außerdem ist es nicht sehr schwierig, eigene Docker Images zu erstellen oder notfalls native Programme auf dem Linux-Host-Betriebssystem zu installieren. Die Installation von Software auf dem Host-System wird jedoch nur eingeschränkt empfohlen.

Es gibt gelegentlich ein Missverständnis, dass die Docker-Version von Home Assistant weniger Möglichkeiten bietet. Das ist nur der Fall, wenn man nicht weiß, wie man sie richtig nutzt. Tatsächlich schränkt Home Assistant OS diese Möglichkeiten aus Gründen der Nutzerfreundlichkeit aktiv ein. Oder man könnte es bei Apple ausdrücken: "think different" ;-)

Deshalb nutzen wir Home Assistant Docker.

## Einbinden von Hardware
Bereits teilweise in [docker-compose](/start/docker-compose) beschrieben.

## Home Assistant über HTTPS absichern
Siehe Reverse Proxy mit Traefik [Reverse Proxy mit Traefik](/software/traefik)