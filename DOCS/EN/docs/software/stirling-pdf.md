# Stirling-PDF

[Stirling-PDF](https://github.com/Frooodle/Stirling-PDF) is a powerful, self-hosted PDF toolkit with over 50 functions for editing, converting, and managing PDF files - completely offline and privacy-friendly.

!!!tip "Alternative to Adobe Acrobat"
    Stirling-PDF offers almost all features of Adobe Acrobat, but runs on your own server and doesn't send data to third parties.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

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

### Page Operations
- Extract, merge, reorder pages
- Rotate and scale pages
- Add/remove blank pages

### Conversion
- PDF ↔ Word/Excel/PowerPoint
- PDF ↔ Images (JPG, PNG)
- HTML/URL → PDF
- Markdown → PDF

### Editing
- Add/edit text
- Insert images
- Watermarks
- Stamps
- Signatures

### Security
- Encrypt/decrypt PDFs
- Set/remove passwords
- Configure permissions
- Verify digital signatures

### OCR (Text Recognition)
- Make scans searchable
- Extract text from images
- Multi-language OCR (including German)

## Notes

- Accessible at `http://[IP]:2223`
- All processing is done locally - no data goes outside
- For OCR, language data is stored in `trainingData`
- Very resource-efficient

## Further Information

- [GitHub Repository](https://github.com/Frooodle/Stirling-PDF)
- [Documentation](https://github.com/Frooodle/Stirling-PDF/blob/main/README.md)
