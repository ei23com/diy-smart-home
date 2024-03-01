# Home Assistant
(Noch im Aufbau)
## Home Assistant Docker vs. Supervised Home Assistant
Home Assistant gibt es in zwei verschiedenen Versionen:<br>
1. Home Assistant Docker<br>
2. Supervised Home Assistant (aka. Home Assistant OS)<br>

In diesem Skript nutzen wir Home Assistant Docker. Das hat zwar Nachteile auf der einen Seite, dafür aber deutlich mehr Vorteile auf der anderen.
Die "Nachteile" sind, dass es keine "Addons" im Sinne Home Assistant OS gibt und man Hardware über die [docker-compose.yml](start/docker-compose) konfigurieren muss. Dazu muss man allerdings direkt erwähnen, dass die Addons technisch nichts anderes sind vorkonfigurierte Docker Container. Der Supervisor übernimmt lediglich einiges der Konfiguration.
Dafür bietet dieses Skript die [docker-compose Templates](start/docker-compose), welches die Konfiguration auch einfach ermöglicht.
Das [Einbinden von Hardware](#hardware) ist mit ein paar Anweisungen außerdem nicht komplitziert

Der Nachteil vom Home Assistant OS ist: Gibt es ein "Addon" nicht für das Home Assistant OS, ist man darauf angewiesen, dass die Entwickler oder die Community ein Solches erstellen.
Die Anzahl der verfügbaren Docker Images hingegen ist unverhältnismäßig größer und das ist der wohl größte Vorteil. Außerdem ist so gar nicht sehr schwierig eigene Docker Images zu erstellen oder notfalls nativ Programme auf dem Linux Host Betriebsystem zu installieren. Die Installation von Software auf dem Host System empfehle ich aber nur eingeschränkt.

Es gibt hin und wieder ein Missverständnis, dass die Docker Version vom Home Assistant die Version sei, die weniger Möglichkeiten bietet. Das ist nur der Fall, wenn man nicht weiß wie man sie richtig ausschöpft.
Tatsächlich schränkt das Home Assistant OS aus Gründen der Nutzerfreundlichkeit diese Möglichkeiten aktiv ein. Oder man bei Apple agen würde "think different" ;-)

Darum nutzen wir Home Assistant Docker.

## Einbiden von Hardware
Bereits Teilweise in [docker-compose](start/docker-compose) beschrieben.

## Home Assistant über HTTPS absichern
Siehe Reverse Proxy mit Traefik [Reverse Proxy mit Traefik](software/traefik)