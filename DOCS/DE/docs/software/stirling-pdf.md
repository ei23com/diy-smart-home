# Stirling-PDF

[Stirling-PDF](https://github.com/Frooodle/Stirling-PDF) ist ein leistungsstarkes, selbstgehostetes PDF-Werkzeug mit über 50 Funktionen zum Bearbeiten, Konvertieren und Verwalten von PDF-Dateien - komplett offline und datenschutzfreundlich.

!!!tip "Alternative zu Adobe Acrobat"
    Stirling-PDF bietet fast alle Funktionen von Adobe Acrobat, läuft aber auf deinem eigenen Server und sendet keine Daten an Dritte.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

## Template

```yaml
  stirling-pdf:
    container_name: stirling-pdf
    image: frooodle/s-pdf:latest
    ports:
      - 2223:8080
    volumes:
      - ./volumes/stirling-pdf/trainingData:/usr/share/tesseract-ocr/5/tessdata
      - ./volumes/stirling-pdf/extraConfigs:/configs
    environment:
      - DOCKER_ENABLE_SECURITY=false
```

## Features

### Seiten-Operationen
- Seiten extrahieren, zusammenfügen, neu anordnen
- Seiten drehen und skalieren
- Leere Seiten hinzufügen/entfernen

### Konvertierung
- PDF ↔ Word/Excel/PowerPoint
- PDF ↔ Bilder (JPG, PNG)
- HTML/URL → PDF
- Markdown → PDF

### Bearbeitung
- Text hinzufügen/bearbeiten
- Bilder einfügen
- Wasserzeichen
- Stempel
- Unterschriften

### Sicherheit
- PDF verschlüsseln/entschlüsseln
- Passwörter setzen/entfernen
- Berechtigungen konfigurieren
- Digitale Signaturen prüfen

### OCR (Texterkennung)
- Scans durchsuchbar machen
- Text aus Bildern extrahieren
- Mehrsprachige OCR (inkl. Deutsch)

## Hinweise

- Erreichbar unter `http://[IP]:2223`
- Alle Verarbeitung erfolgt lokal - keine Daten gehen nach außen
- Für OCR werden Sprachdaten in `trainingData` gespeichert
- Sehr ressourcenschonend

## Weitere Informationen

- [GitHub Repository](https://github.com/Frooodle/Stirling-PDF)
- [Dokumentation](https://github.com/Frooodle/Stirling-PDF/blob/main/README.md)
