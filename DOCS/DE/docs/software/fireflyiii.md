# Firefly III

[Firefly III](https://www.firefly-iii.org/) ist ein freier und Open-Source Finanzmanager. Er hilft dir, deine Ausgaben und Einnahmen zu verfolgen, Budgets zu erstellen und einen Überblick über deine Finanzen zu behalten.

## Installation

Füge das folgende Template in deine [docker-compose.yml](/start/docker-compose/) ein und führe anschließend `ei23 dc` aus.

!!!warning "Netzwerk beachten"
    Füge zuerst das benötigte Netzwerk zur docker-compose.yml hinzu.

## Template

```yaml
  fireflyiii:
    image: fireflyiii/core:latest
    container_name: fireflyiii
    volumes:
      - ./volumes/firefly_iii/upload:/var/www/html/storage/upload
    environment:
      - APP_KEY=ei23password1_placeholderpassword_placeholderei23
      - DB_HOST=fireflyiiidb
      - DB_PORT=3306
      - DB_CONNECTION=mysql 
      - DB_DATABASE=firefly
      - DB_USERNAME=firefly
      - DB_PASSWORD=password_placeholder
    ports:
      - 2225:8080
    depends_on:
      - fireflyiiidb
    networks:
      - default
      - fireflyiii
    logging:
      options:
        max-size: "5m"
        max-file: "3"

  fireflyiiidb:
    image: yobasystems/alpine-mariadb
    container_name: fireflyiiidb
    environment:
      - MYSQL_RANDOM_ROOT_PASSWORD=yes
      - MYSQL_USER=firefly
      - MYSQL_PASSWORD=password_placeholder
      - MYSQL_DATABASE=firefly
    volumes:
      - ./volumes/firefly_iii/db:/var/lib/mysql
    networks:
      - fireflyiii
    logging:
      options:
        max-size: "5m"
        max-file: "3"
```

Füge zusätzlich dieses Netzwerk hinzu (z.B. am Ende der docker-compose.yml):

```yaml
  fireflyiii:
    driver: bridge
    internal: true
```

## Hinweise

- Nach dem Start erreichst du Firefly III unter `http://[IP]:2225`
- Beim ersten Start musst du einen Account erstellen
- Das Template erstellt automatisch die notwendige Datenbank
- Passwörter werden automatisch generiert
- Firefly III unterstützt Import von Bank-CSV-Dateien und SEPA-Überweisungen

## Weitere Informationen

- [Offizielle Dokumentation](https://docs.firefly-iii.org/)
- [GitHub Repository](https://github.com/firefly-iii/firefly-iii)
