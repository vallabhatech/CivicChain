# Deployment Guide

## Overview

This guide covers the deployment of the Decentralized Online Voting System in production environments. It includes infrastructure setup, security configurations, performance optimization, and monitoring strategies.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Infrastructure Setup](#infrastructure-setup)
3. [Application Deployment](#application-deployment)
4. [Database Configuration](#database-configuration)
5. [Security Configuration](#security-configuration)
6. [Performance Optimization](#performance-optimization)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Backup and Recovery](#backup-and-recovery)
9. [Scaling Strategies](#scaling-strategies)
10. [Maintenance](#maintenance)

## Prerequisites

### System Requirements

#### Minimum Requirements
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 100GB SSD
- **Network**: 100 Mbps
- **OS**: Ubuntu 20.04 LTS / CentOS 8 / RHEL 8

#### Recommended Requirements
- **CPU**: 8 cores
- **RAM**: 16GB
- **Storage**: 500GB SSD
- **Network**: 1 Gbps
- **OS**: Ubuntu 22.04 LTS

### Software Requirements
- **Python**: 3.10+
- **MySQL**: 8.0+
- **Nginx**: 1.18+
- **Redis**: 6.0+
- **Docker**: 20.10+ (optional)
- **Kubernetes**: 1.20+ (optional)

## Infrastructure Setup

### 1. Server Architecture

#### Single Server Setup
```
┌─────────────────────────────────────┐
│           Production Server          │
├─────────────────────────────────────┤
│  Nginx (Reverse Proxy)              │
│  Django Application (Gunicorn)       │
│  MySQL Database                     │
│  Redis (Cache & Sessions)           │
│  File Storage (Local)                │
└─────────────────────────────────────┘
```

#### Multi-Server Setup
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Web Server │  │ App Server  │ │ DB Server   │
│   (Nginx)    │  │ (Django)    │ │ (MySQL)     │
└─────────────┘  └─────────────┘  └─────────────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
              ┌─────────────┐
              │ Redis Cache  │
              └─────────────┘
```

### 2. Network Configuration

#### Firewall Setup
```bash
# Ubuntu UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3306/tcp  # MySQL (internal only)
sudo ufw allow 6379/tcp  # Redis (internal only)
```

#### Load Balancer Configuration (Nginx)
```nginx
upstream voting_app {
    server 10.0.1.10:8000;
    server 10.0.1.11:8000;
    server 10.0.1.12:8000;
}

server {
    listen 80;
    server_name vote.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name vote.yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/voting-system.crt;
    ssl_certificate_key /etc/ssl/private/voting-system.key;
    
    location / {
        proxy_pass http://voting_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /var/www/voting-system/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /var/www/voting-system/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Application Deployment

### 1. Environment Setup

#### Create Deployment Directory
```bash
sudo mkdir -p /var/www/voting-system
sudo chown $USER:$USER /var/www/voting-system
cd /var/www/voting-system
```

#### Clone Repository
```bash
git clone https://github.com/yourusername/DECENTRALIZED-ONLINE-VOTING-SYSTEM-USING-BLOCKCHAIN.git .
```

#### Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Production Settings

#### Create Production Settings File
```python
# decentralizedvoting/settings_production.py
from .settings import *
import os

# Security
DEBUG = False
ALLOWED_HOSTS = ['vote.yourdomain.com', 'www.vote.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 60,
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Static Files
STATIC_ROOT = '/var/www/voting-system/static/'
MEDIA_ROOT = '/var/www/voting-system/media/'

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/voting-system/django.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/voting-system/django-error.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'error_file'],
        'level': 'INFO',
    },
}
```

#### Environment Variables
```bash
# /var/www/voting-system/.env
SECRET_KEY=your-super-secret-key-here
DB_NAME=decentralized_voting
DB_USER=voting_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=3306
REDIS_URL=redis://localhost:6379/1
```

### 3. Gunicorn Configuration

#### Create Gunicorn Service File
```ini
# /etc/systemd/system/voting-system.service
[Unit]
Description=Voting System Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
EnvironmentFile=/var/www/voting-system/.env
WorkingDirectory=/var/www/voting-system
ExecStart=/var/www/voting-system/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --bind unix:/run/gunicorn/voting-system.sock \
    decentralizedvoting.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### Create Gunicorn Socket File
```ini
# /etc/systemd/system/voting-system.socket
[Unit]
Description=Voting System Socket

[Socket]
ListenStream=/run/gunicorn/voting-system.sock
SocketMode=660
SocketUser=www-data
SocketGroup=www-data

[Install]
WantedBy=sockets.target
```

#### Enable and Start Services
```bash
sudo systemctl enable voting-system.socket
sudo systemctl enable voting-system.service
sudo systemctl start voting-system.socket
sudo systemctl start voting-system.service
```

## Database Configuration

### 1. MySQL Production Setup

#### Install MySQL Server
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server mysql-client

# CentOS/RHEL
sudo yum install mysql-server mysql-client
```

#### Secure MySQL Installation
```bash
sudo mysql_secure_installation
```

#### Create Database and User
```sql
CREATE DATABASE decentralized_voting CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'voting_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON decentralized_voting.* TO 'voting_user'@'localhost';
FLUSH PRIVILEGES;
```

#### MySQL Configuration
```ini
# /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
# General Settings
user = mysql
pid-file = /var/run/mysqld/mysqld.pid
socket = /var/run/mysqld/mysqld.sock
port = 3306
basedir = /usr
datadir = /var/lib/mysql
tmpdir = /tmp
lc-messages-dir = /usr/share/mysql

# Performance Settings
innodb_buffer_pool_size = 4G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT
innodb_file_per_table = 1

# Connection Settings
max_connections = 500
max_connect_errors = 10000
wait_timeout = 600
interactive_timeout = 600

# Security Settings
skip-show-database
local-infile = 0
```

### 2. Database Migration and Setup

#### Run Migrations
```bash
cd /var/www/voting-system
source venv/bin/activate
python manage.py migrate --settings=decentralizedvoting.settings_production
```

#### Create Superuser
```bash
python manage.py createsuperuser --settings=decentralizedvoting.settings_production
```

#### Collect Static Files
```bash
python manage.py collectstatic --settings=decentralizedvoting.settings_production --noinput
```

## Security Configuration

### 1. SSL/TLS Setup

#### Obtain SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain Certificate
sudo certbot --nginx -d vote.yourdomain.com -d www.vote.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Manual SSL Configuration
```bash
# Generate Private Key
sudo openssl genrsa -out /etc/ssl/private/voting-system.key 2048

# Generate CSR
sudo openssl req -new -key /etc/ssl/private/voting-system.key -out /etc/ssl/certs/voting-system.csr

# Generate Self-Signed Certificate (for testing)
sudo openssl x509 -req -days 365 -in /etc/ssl/certs/voting-system.csr -signkey /etc/ssl/private/voting-system.key -out /etc/ssl/certs/voting-system.crt
```

### 2. Application Security

#### File Permissions
```bash
# Set proper permissions
sudo chown -R www-data:www-data /var/www/voting-system
sudo chmod -R 755 /var/www/voting-system
sudo chmod -R 777 /var/www/voting-system/media
sudo chmod 600 /var/www/voting-system/.env
```

#### Security Headers
```nginx
# Add to Nginx configuration
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

### 3. Firewall and Network Security

#### Fail2Ban Configuration
```ini
# /etc/fail2ban/jail.local
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 3
```

## Performance Optimization

### 1. Database Optimization

#### MySQL Query Cache
```ini
# Add to MySQL configuration
query_cache_type = 1
query_cache_size = 64M
query_cache_limit = 2M
```

#### Database Indexing
```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_voter_aadhar ON voters_details(aadhar);
CREATE INDEX idx_election_date ON elction_detials(election_date);
CREATE INDEX idx_vote_election ON votes(election_id);
CREATE INDEX idx_vote_voter ON votes(voter_id);
```

### 2. Application Caching

#### Redis Configuration
```ini
# /etc/redis/redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

#### Django Cache Configuration
```python
# Add to settings_production.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'RETRY_ON_TIMEOUT': True,
        }
    }
}

# Session cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### 3. Web Server Optimization

#### Nginx Performance Tuning
```nginx
# Worker processes
worker_processes auto;
worker_connections 1024;

# Gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Client timeouts
client_body_timeout 12;
client_header_timeout 12;
keepalive_timeout 15;
send_timeout 10;
```

## Monitoring and Logging

### 1. Application Monitoring

#### Create Log Directory
```bash
sudo mkdir -p /var/log/voting-system
sudo chown www-data:www-data /var/log/voting-system
```

#### Log Rotation
```bash
# /etc/logrotate.d/voting-system
/var/log/voting-system/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload voting-system
    endscript
}
```

### 2. System Monitoring

#### Install Monitoring Tools
```bash
# Install Prometheus
sudo apt install prometheus

# Install Grafana
sudo apt install grafana

# Install Node Exporter
sudo apt install prometheus-node-exporter
```

#### Prometheus Configuration
```yaml
# /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'voting-system'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

### 3. Health Checks

#### Create Health Check Endpoint
```python
# mainapp/views.py
from django.http import JsonResponse
from django.db import connection
import redis

def health_check(request):
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    try:
        # Check Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        redis_status = "healthy"
    except:
        redis_status = "unhealthy"
    
    overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy"
    
    return JsonResponse({
        "status": overall_status,
        "database": db_status,
        "redis": redis_status,
        "timestamp": timezone.now().isoformat()
    })
```

## Backup and Recovery

### 1. Database Backup

#### Automated Backup Script
```bash
#!/bin/bash
# /usr/local/bin/backup-voting-system.sh

BACKUP_DIR="/var/backups/voting-system"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="decentralized_voting"
DB_USER="voting_user"
DB_PASSWORD="secure_password"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /var/www/voting-system/media/

# Remove old backups (keep 30 days)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

#### Schedule Backups
```bash
# Add to crontab
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-voting-system.sh
```

### 2. Application Backup

#### Code Backup
```bash
#!/bin/bash
# /usr/local/bin/backup-code.sh

BACKUP_DIR="/var/backups/voting-system"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup application code
tar -czf $BACKUP_DIR/code_backup_$DATE.tar.gz /var/www/voting-system/

# Backup configuration files
tar -czf $BACKUP_DIR/config_backup_$DATE.tar.gz /etc/nginx/sites-available/voting-system /etc/systemd/system/voting-system.*
```

### 3. Recovery Procedures

#### Database Recovery
```bash
# Stop application
sudo systemctl stop voting-system

# Restore database
gunzip < /var/backups/voting-system/db_backup_20240101_020000.sql.gz | mysql -u voting_user -p decentralized_voting

# Restore media files
tar -xzf /var/backups/voting-system/media_backup_20240101_020000.tar.gz -C /

# Start application
sudo systemctl start voting-system
```

## Scaling Strategies

### 1. Horizontal Scaling

#### Multiple Application Servers
```nginx
# Load balancer configuration
upstream voting_app {
    least_conn;
    server 10.0.1.10:8000 weight=1 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:8000 weight=1 max_fails=3 fail_timeout=30s;
    server 10.0.1.12:8000 weight=1 max_fails=3 fail_timeout=30s;
}
```

#### Database Replication
```sql
-- Master server configuration
SET GLOBAL server_id = 1;
SET GLOBAL log_bin = 'mysql-bin';
SET GLOBAL binlog_format = 'ROW';

-- Slave server configuration
SET GLOBAL server_id = 2;
CHANGE MASTER TO MASTER_HOST='10.0.1.20', MASTER_USER='replication_user', MASTER_PASSWORD='password';
START SLAVE;
```

### 2. Container Deployment

#### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "decentralizedvoting.wsgi:application"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: decentralized_voting
      MYSQL_USER: voting_user
      MYSQL_PASSWORD: secure_password
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  redis:
    image: redis:6.2-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 decentralizedvoting.wsgi:application
    volumes:
      - static_volume:/app/static
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/1

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/static
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  mysql_data:
  static_volume:
  media_volume:
```

### 3. Kubernetes Deployment

#### Deployment Manifest
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: voting-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: voting-system
  template:
    metadata:
      labels:
        app: voting-system
    spec:
      containers:
      - name: voting-system
        image: voting-system:latest
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          value: "mysql-service"
        - name: REDIS_URL
          value: "redis://redis-service:6379/1"
```

## Maintenance

### 1. Regular Maintenance Tasks

#### Daily Tasks
- Check system logs
- Monitor disk space
- Verify backup completion
- Check application health

#### Weekly Tasks
- Update security patches
- Review performance metrics
- Clean up old log files
- Test backup recovery

#### Monthly Tasks
- Database optimization
- Security audit
- Performance tuning
- Capacity planning

### 2. Update Procedures

#### Application Updates
```bash
# Backup current version
sudo cp -r /var/www/voting-system /var/backups/voting-system-$(date +%Y%m%d)

# Update code
cd /var/www/voting-system
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
python manage.py migrate --settings=decentralizedvoting.settings_production

# Collect static files
python manage.py collectstatic --settings=decentralizedvoting.settings_production --noinput

# Restart services
sudo systemctl restart voting-system
```

### 3. Troubleshooting

#### Common Issues and Solutions

**Application Not Responding**
```bash
# Check service status
sudo systemctl status voting-system

# Check logs
sudo journalctl -u voting-system -f

# Restart service
sudo systemctl restart voting-system
```

**Database Connection Issues**
```bash
# Check MySQL status
sudo systemctl status mysql

# Test database connection
mysql -u voting_user -p decentralized_voting

# Check MySQL logs
sudo tail -f /var/log/mysql/error.log
```

**High Memory Usage**
```bash
# Check memory usage
free -h
top

# Restart services if needed
sudo systemctl restart voting-system
sudo systemctl restart mysql
```

---

**Note**: This deployment guide is for production environments. Always test in a staging environment before deploying to production.
