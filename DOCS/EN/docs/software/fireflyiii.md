# Firefly III

[Firefly III](https://www.firefly-iii.org/) is a free and open-source finance manager. It helps you track your expenses and income, create budgets, and keep an overview of your finances.

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "Note the Network"
    First add the required network to docker-compose.yml.

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

Additionally, add this network (e.g., at the end of docker-compose.yml):

```yaml
  fireflyiii:
    driver: bridge
    internal: true
```

## Notes

- After starting, you can access Firefly III at `http://[IP]:2225`
- On first start, you need to create an account
- The template automatically creates the required database
- Passwords are automatically generated
- Firefly III supports importing bank CSV files and SEPA transfers

## Further Information

- [Official Documentation](https://docs.firefly-iii.org/)
- [GitHub Repository](https://github.com/firefly-iii/firefly-iii)
