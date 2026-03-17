# Paperless-ngx

[Paperless-ngx](https://docs.paperless-ngx.com/) is a free document management system with OCR (Optical Character Recognition). It digitizes physical documents and makes them searchable.

[![YT](https://ei23.de/bilder/YTthumbs/qyXz5gJnu_8.webp)](https://www.youtube.com/watch?v=qyXz5gJnu_8)

## Installation

Add the following template to your [docker-compose.yml](/start/docker-compose/) and then run `ei23 dc`.

!!!warning "Environment file required"
    Create the file `ei23-docker/env/paperless.env` before starting.

## Create Environment File

Create `/home/[user]/ei23-docker/env/paperless.env`:

```env
PAPERLESS_SECRET=YOUR_SECRET_TOKEN
PAPERLESS_TIMEZONE=Europe/Berlin
PAPERLESS_OCR_LANGUAGE=eng
PAPERLESS_ADMIN_USER=admin
PAPERLESS_ADMIN_PASSWORD=YOUR_PASSWORD
PAPERLESS_URL=http://your-ip:8010
```

!!!warning "Secret Token"
    Generate a secure token: `openssl rand -base64 32`

## Template

```yaml
  paperlessngx-redis:
    image: redis:7
    container_name: paperlessngx-redis
    restart: unless-stopped
    volumes:
      - ./volumes/paperless/redis:/data

  paperlessngx-db:
    image: postgres:15
    container_name: paperlessngx-db
    restart: unless-stopped
    volumes:
      - ./volumes/paperless/db:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: paperless
      POSTGRES_USER: paperless
      POSTGRES_PASSWORD: paperless

  paperlessngx:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    container_name: paperlessngx
    restart: unless-stopped
    depends_on:
      - paperlessngx-redis
      - paperlessngx-db
    ports:
      - "8010:8000"
    volumes:
      - ./volumes/paperless/data:/usr/src/paperless/data
      - ./volumes/paperless/media:/usr/src/paperless/media
      - ./volumes/paperless/export:/usr/src/paperless/export
      - ./volumes/paperless/consume:/usr/src/paperless/consume
    env_file:
      - ./env/paperless.env
    environment:
      PAPERLESS_REDIS: redis://paperlessngx-redis:6379
      PAPERLESS_DBHOST: paperlessngx-db
      PAPERLESS_DBNAME: paperless
      PAPERLESS_DBUSER: paperless
      PAPERLESS_DBPASS: paperless
```

## Features

- **OCR Text Recognition** - Searchable PDFs from scans
- **Automatic Categorization** - Tags, correspondents, document types
- **Full-text Search** - Search in all documents
- **Email Import** - Receive documents via email
- **Mobile App** - Upload documents on the go
- **REST API** - Automation possible
- **Export/Import** - Backup and migration

## First Start

1. After starting, Paperless is accessible at `http://[IP]:8010`
2. Log in with the credentials configured in the env file
3. Start uploading documents

## Importing Documents

### Manually via Web Interface

1. Click **Upload**
2. Select PDF, JPEG, or PNG files
3. Paperless processes the document automatically

### Via the Consume Folder

Place files in the folder `./volumes/paperless/consume/`:

```bash
# Copy documents to consume folder
cp ~/scans/*.pdf ~/ei23-docker/volumes/paperless/consume/
```

Paperless monitors this folder and automatically processes new files.

### Via Mobile App

1. Install the **Paperless Mobile** app
2. Configure the server URL
3. Scan documents directly with your phone

### Via Email (optional)

Configure in `paperless.env`:

```env
PAPERLESS_EMAIL_HOST=imap.gmail.com
PAPERLESS_EMAIL_PORT=993
PAPERLESS_EMAIL_USER=your@email.com
PAPERLESS_EMAIL_PASS=YOUR_PASSWORD
PAPERLESS_EMAIL_INBOX=INBOX
```

## Organization

### Tags

Tags are freely definable labels:

- **Taxes** - Tax documents
- **Insurance** - Insurance policies
- **Invoice** - Invoices
- **Important** - Particularly important documents

### Correspondents

Correspondents are senders/recipients:

- **Tax Office**
- **Health Insurance**
- **Utility Company**
- **Employer**

### Document Types

- **Invoice**
- **Contract**
- **Notice**
- **Letter**
- **Pay Slip**

### Automatic Rules

Paperless can automatically categorize documents:

1. Go to **Settings** → **Rules**
2. Create a new rule
3. Define conditions (e.g. text contains "Invoice")
4. Assign tags/correspondents

## Backup

### Via the ei23 Script

```bash
ei23 backup
```

### Manually

```bash
cd ~/ei23-docker/

# Backup database
docker compose exec paperlessngx-db pg_dump -U paperless paperless > ~/Backup/paperless_db.sql

# Backup data
sudo tar -czf ~/Backup/paperless_data.tar.gz volumes/paperless/data/ volumes/paperless/media/
```

### Restore

```bash
cd ~/ei23-docker/

# Stop container
docker compose stop paperlessngx

# Restore database
cat ~/Backup/paperless_db.sql | docker compose exec -T paperlessngx-db psql -U paperless paperless

# Restore data
sudo tar -xzf ~/Backup/paperless_data.tar.gz

# Start container
docker compose start paperlessngx
```

## Tips

- **Scan resolution**: 300 DPI for good OCR results
- **File format**: PDF preferred, TIFF also good
- **Languages**: Configure `PAPERLESS_OCR_LANGUAGE=eng+deu` for English+German
- **Storage**: OCR and thumbnails require storage space

## Notes

- Data is located in `./volumes/paperless/`
- Consume folder: `./volumes/paperless/consume/`
- Port: 8010
- Paperless requires PostgreSQL and Redis
- For large archives: 4GB+ RAM recommended

## Further Information

- [Official Documentation](https://docs.paperless-ngx.com/)
- [GitHub Repository](https://github.com/paperless-ngx/paperless-ngx)
- [Mobile App](https://github.com/astubenbord/paperless-mobile)
- [Reddit Community](https://www.reddit.com/r/paperlessngx/)
