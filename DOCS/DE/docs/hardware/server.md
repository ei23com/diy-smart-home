# Server / Mini-PC Hardware

Die Wahl der richtigen Hardware ist entscheidend für deinen Smart Home Server. Hier erfährst du, welche Optionen es gibt und welche für dich am besten geeignet ist.

!!!tip "Mini-PCs / ThinClients empfohlen"
    Obwohl der Raspberry Pi einen sehr geringen Stromverbrauch hat, ist die **Performance pro Watt** bei gebrauchten Mini-PCs und ThinClients oft deutlich besser. Für um die 50-100€ erhältst du gebrauchte Systeme mit x86-Architektur, die mehr Leistung und bessere Docker-Unterstützung bieten.

## Hardware-Vergleich

| Hardware | Preis | Stromverbrauch | Leistung | Docker-Unterstützung | Empfehlung |
|----------|-------|----------------|----------|---------------------|------------|
| **Raspberry Pi 4** | ~50€ | 3-5W | Gut | Eingeschränkt (ARM) | ✅ Für Einsteiger |
| **Raspberry Pi 5** | ~80€ | 5-8W | Sehr gut | Eingeschränkt (ARM) | ✅ Für leichte Nutzung |
| **Intel N100 Mini-PC** | ~150€ | 6-10W | Sehr gut | ✅ Perfekt | ✅ **Empfohlen** |
| **HP/Lenovo/Dell ThinClient** | 50-100€ | 10-25W | Exzellent | ✅ Perfekt | ✅ **Bestes Preis-Leistungs-Verhältnis** |
| **Intel NUC (i3/i5)** | 200-400€ | 15-35W | Überlegen | ✅ Perfekt | Für hohe Anforderungen |
| **Alt-PC** | ~0€ | 30-80W | Variabel | ✅ Perfekt | Zum Testen |

## Empfohlene Hardware

### Einsteiger: Raspberry Pi 4/5

**Vorteile:**
- Sehr geringer Stromverbrauch (3-8W)
- Kleine Bauform
- Niedrige Anschaffungskosten

**Nachteile:**
- Eingeschränkte Docker-Unterstützung (nicht alle Images für ARM verfügbar)
- Begrenzter RAM (max. 8GB)
- SD-Karte als Hauptstorage (langsam, weniger zuverlässig)

**Ideal für:**
- Nur Home Assistant + NodeRED
- Bis zu 5-8 Docker-Container
- Leichte Nutzung ohne Media-Server

!!!tip "Empfehlung"
    Mindestens **4GB RAM**, besser **8GB**. Nutze eine SSD statt SD-Karte (über USB).

---

### Empfohlen: Mini-PCs / ThinClients

!!!success "Beste Empfehlung"
    Gebrauchte ThinClients bieten das **beste Preis-Leistungs-Verhältnis** für Smart Home Server.

**Beispiele:**

| Modell | Preis (gebraucht) | CPU | RAM | Vorteile |
|--------|-------------------|-----|-----|----------|
| **HP T620** | ~40€ | AMD GX-415GA | 4-8GB | Sehr günstig, leise |
| **HP T630** | ~60€ | AMD GX-420GI | 4-8GB | Mehr Leistung |
| **Lenovo ThinkCentre M700** | ~80€ | i3-6100T | 8GB | Intel QuickSync |
| **Dell Wyse 5070** | ~50€ | J5005 | 4-8GB | Niedriger Verbrauch |
| **Intel N100 Mini-PC** | ~150€ | N100 | 8-16GB | Aktuell, effizient |
| **HP ProDesk 400 G6** | ~150€ | i3-10100T | 8-16GB | Sehr leistungsfähig |

**Vorteile von Mini-PCs:**
- ✅ x86-Architektur - Alle Docker-Images funktionieren
- ✅ Mehr Leistung pro Watt
- ✅ SSD-Support (SATA/NVMe)
- ✅ Mehr RAM erweiterbar
- ✅ Intel QuickSync für Hardware-Transkodierung (Jellyfin, Plex)
- ✅ Langlebiger als SD-Karten

**Ideal für:**
- Alle Docker-Container des ei23-Skripts
- Media-Server (Jellyfin, Plex)
- Nextcloud mit vielen Nutzern
- KI/LLM (mit dedizierter GPU)
- Frigate mit mehreren Kameras

---

### Fortgeschritten: Eigener PC / Server

Für sehr hohe Anforderungen:

- **Proxmox** als Hypervisor
- **Mehrere VMs** für verschiedene Dienste
- **Dedizierte GPU** für KI/LLM
- **RAID-Storage** für Datensicherheit
- Stromverbrauch: 30-100W

## Stromverbrauch im Vergleich

| System | Leerlauf | Last | Kosten/Jahr* |
|--------|----------|------|--------------|
| Raspberry Pi 4 | 3W | 6W | ~10€ |
| Intel N100 Mini-PC | 6W | 15W | ~20€ |
| HP ThinClient i3 | 12W | 35W | ~40€ |
| Alter Desktop-PC | 40W | 120W | ~140€ |

*Bei 30ct/kWh, 24/7 Betrieb

!!!note "Performance pro Watt"
    Der Raspberry Pi verbraucht zwar am wenigsten Strom, aber ein Intel N100 bietet bei doppeltem Stromverbrauch die **5-10-fache Leistung**. Für Docker-Workloads ist ein Mini-PC oft die effizientere Wahl.

## Storage-Empfehlungen

| Typ | Preis | Vorteile | Nachteile |
|-----|-------|----------|-----------|
| **SD-Karte** | ~15€ | Günstig | Langsam, weniger haltbar |
| **USB-SSD** | ~30€ | Schneller, haltbarer | USB-Bandbreite |
| **SATA-SSD** | ~40€ | Schnell, zuverlässig | Nur bei Mini-PCs |
| **NVMe-SSD** | ~50€ | Am schnellsten | Nur bei neueren Systemen |

!!!warning "SD-Karten"
    SD-Karten haben eine begrenzte Lebensdauer bei vielen Schreibvorgängen. Nutze **Log2RAM** (im ei23-Skript verfügbar) oder besser eine SSD.

## Meine Empfehlungen

| Nutzung | Empfehlung | Budget |
|---------|------------|--------|
| **Nur Home Assistant + NodeRED** | Raspberry Pi 4 4GB | ~70€ |
| **Home Assistant + 5-10 Container** | HP T630 oder Dell Wyse 5070 | ~60-80€ |
| **Alles + Media-Server** | Intel N100 Mini-PC | ~150€ |
| **KI/LLM + viele Container** | i5/i7 Mini-PC mit GPU | ~300€+ |

## Wo kaufen?

- **eBay Kleinanzeigen / eBay** - Gebrauchte ThinClients
- **refurbed.de** - Aufbereitete Mini-PCs mit Garantie
- **Amazon** - Neue Intel N100 Systeme
- **Raspberry Pi Shops** - Für RPis und Zubehör
