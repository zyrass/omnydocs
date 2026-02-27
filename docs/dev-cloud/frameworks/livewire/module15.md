---
description: "Docker, CI/CD avancé, zero-downtime deployment, monitoring, i18n, a11y, PWA, troubleshooting, migration strategies"
icon: lucide/book-open-check
tags: ["LIVEWIRE", "DEVOPS", "DOCKER", "CI-CD", "I18N", "A11Y", "PWA", "PRODUCTION"]
---

# XV — Production Ready & DevOps

<div
  class="omny-meta"
  data-level="🔴 Expert"
  data-duration="9-10 heures"
  data-lessons="9">
</div>

## Vue d'ensemble

!!! quote "Analogie pédagogique"
    _Imaginez un **lancement spatial professionnel NASA** : vous construisez fusée (application Livewire) avec **protocoles rigoureux multi-niveaux** garantissant mission réussie. **Phase développement** : ingénieurs construisent composants laboratoire (environnement local Docker), tests unitaires chaque pièce, simulateurs environnement (CI/CD pipeline). **Phase pré-lancement** : inspections qualité automatisées (tests automatiques), vérifications checklist exhaustives (security audit, performance benchmarks), simulations conditions extrêmes (load testing). **Lancement zero-downtime** : systèmes redondants actifs simultanément (blue-green deployment), ancien vaisseau reste opérationnel pendant nouveau décolle, transition imperceptible (zero interruption service). **Monitoring temps réel** : centre contrôle surveille TOUTES métriques (APM, logs, traces), alertes automatiques si anomalie (Sentry, New Relic), télémétrie complète (OpenTelemetry). **Support international** : traductions multiples langues (i18n), adaptation culturelle (localization), accessibilité universelle (a11y WCAG 2.1). **Capacités autonomes** : fonctionnement hors-ligne (PWA service workers), synchronisation automatique reconnexion, installation app native (manifest.json). **Troubleshooting expert** : procédures diagnostic précises (debugging avancé), plans contingence (rollback strategies), documentation incidents (post-mortems). **Production Ready Livewire fonctionne exactement pareil** : **Docker multi-stage** (images optimisées production), **CI/CD GitHub Actions** (tests automatiques, deploy automatique), **Zero-downtime deployment** (Deployer PHP, Envoyer), **Monitoring 360°** (Telescope, Horizon, Sentry, Pulse), **i18n Laravel** (traductions, pluralization, fallback), **a11y ARIA** (navigation keyboard, screen readers, focus management), **PWA Workbox** (offline, caching strategies, install prompt), **Troubleshooting méthodique** (Debugbar, Ray, query profiling), **Migration strategies** (feature flags, database migrations safe). C'est la **différence prototype vs production-grade** : même fonctionnalités, mais prototype crash production, application NASA tourne 24/7/365 sans interruption._

**Production Ready nécessite stack DevOps complète :**

- ✅ **Docker** = Containerization multi-stage optimisée
- ✅ **CI/CD avancé** = Pipelines automatisés complexes
- ✅ **Zero-downtime** = Déploiement sans interruption
- ✅ **Monitoring** = Observability complète (metrics, logs, traces)
- ✅ **i18n** = Internationalisation multi-langues
- ✅ **a11y** = Accessibilité WCAG 2.1 AA
- ✅ **PWA** = Progressive Web App features
- ✅ **Troubleshooting** = Debugging avancé production
- ✅ **Migration** = Strategies upgrade safe

**Ce module couvre :**

1. Docker containerization production
2. CI/CD pipelines avancés
3. Zero-downtime deployment strategies
4. Monitoring et observability
5. Internationalization (i18n)
6. Accessibility (a11y)
7. Progressive Web App (PWA)
8. Advanced troubleshooting
9. Migration et upgrade strategies

---

## Leçon 1 : Docker Containerization Production

### 1.1 Dockerfile Multi-Stage

**Dockerfile optimisé production :**

```dockerfile
# Stage 1: Composer dependencies
FROM composer:2.6 AS composer

WORKDIR /app

COPY composer.json composer.lock ./

# Install dependencies (production only, optimized)
RUN composer install \
    --no-dev \
    --no-scripts \
    --no-interaction \
    --prefer-dist \
    --optimize-autoloader

# Stage 2: Node dependencies & build assets
FROM node:20-alpine AS node

WORKDIR /app

COPY package.json package-lock.json ./
COPY resources ./resources
COPY vite.config.js ./

RUN npm ci --only=production
RUN npm run build

# Stage 3: Final production image
FROM php:8.2-fpm-alpine

# Install system dependencies
RUN apk add --no-cache \
    nginx \
    supervisor \
    postgresql-dev \
    libzip-dev \
    libpng-dev \
    libjpeg-turbo-dev \
    freetype-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install \
        pdo \
        pdo_pgsql \
        zip \
        gd \
        opcache

# Configure opcache for production
RUN { \
        echo 'opcache.enable=1'; \
        echo 'opcache.memory_consumption=256'; \
        echo 'opcache.interned_strings_buffer=16'; \
        echo 'opcache.max_accelerated_files=10000'; \
        echo 'opcache.validate_timestamps=0'; \
        echo 'opcache.save_comments=1'; \
        echo 'opcache.fast_shutdown=1'; \
    } > /usr/local/etc/php/conf.d/opcache.ini

# Configure PHP-FPM
RUN { \
        echo 'pm = dynamic'; \
        echo 'pm.max_children = 50'; \
        echo 'pm.start_servers = 10'; \
        echo 'pm.min_spare_servers = 5'; \
        echo 'pm.max_spare_servers = 20'; \
        echo 'pm.max_requests = 500'; \
    } > /usr/local/etc/php-fpm.d/zz-docker.conf

WORKDIR /var/www/html

# Copy application files
COPY --chown=www-data:www-data . .

# Copy vendor from composer stage
COPY --from=composer --chown=www-data:www-data /app/vendor ./vendor

# Copy built assets from node stage
COPY --from=node --chown=www-data:www-data /app/public/build ./public/build

# Setup permissions
RUN chown -R www-data:www-data \
    /var/www/html/storage \
    /var/www/html/bootstrap/cache

# Copy Nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Copy Supervisor configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port
EXPOSE 80

# Start Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

### 1.2 Nginx Configuration

```nginx
# docker/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 2048;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log warn;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
    limit_req_status 429;

    server {
        listen 80;
        server_name _;
        root /var/www/html/public;
        index index.php;

        charset utf-8;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;

        # Static files cache
        location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Main location
        location / {
            try_files $uri $uri/ /index.php?$query_string;
            
            # Rate limiting
            limit_req zone=one burst=20 nodelay;
        }

        # PHP-FPM
        location ~ \.php$ {
            fastcgi_pass 127.0.0.1:9000;
            fastcgi_index index.php;
            fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
            include fastcgi_params;
            
            # Livewire optimization
            fastcgi_buffer_size 32k;
            fastcgi_buffers 8 16k;
        }

        # Deny access to hidden files
        location ~ /\.(?!well-known).* {
            deny all;
        }
    }
}
```

### 1.3 Supervisor Configuration

```ini
# docker/supervisord.conf

[supervisord]
nodaemon=true
user=root
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid

[program:nginx]
command=nginx -g 'daemon off;'
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:php-fpm]
command=php-fpm
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:horizon]
process_name=%(program_name)s
command=php /var/www/html/artisan horizon
autostart=true
autorestart=true
user=www-data
redirect_stderr=true
stdout_logfile=/var/www/html/storage/logs/horizon.log
stopwaitsecs=3600

[program:schedule]
process_name=%(program_name)s
command=/bin/sh -c "while true; do php /var/www/html/artisan schedule:run --verbose --no-interaction & sleep 60; done"
autostart=true
autorestart=true
user=www-data
redirect_stderr=true
stdout_logfile=/var/www/html/storage/logs/schedule.log
```

### 1.4 Docker Compose Production

```yaml
# docker-compose.prod.yml

version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: myapp:latest
    container_name: myapp-app
    restart: unless-stopped
    environment:
      - APP_ENV=production
      - APP_DEBUG=false
    volumes:
      - ./storage:/var/www/html/storage
      - ./bootstrap/cache:/var/www/html/bootstrap/cache
    networks:
      - app-network
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine
    container_name: myapp-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_DATABASE}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USERNAME}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx-proxy:
    image: nginx:alpine
    container_name: myapp-proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/proxy-nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    networks:
      - app-network
    depends_on:
      - app

volumes:
  postgres-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

### 1.5 Build et Deploy

```bash
#!/bin/bash
# deploy-docker.sh

set -e

echo "🐳 Building Docker image..."

# Build production image
docker build \
  --target production \
  --tag myapp:latest \
  --tag myapp:$(git rev-parse --short HEAD) \
  .

echo "📦 Pushing to registry..."

# Push to registry
docker tag myapp:latest registry.example.com/myapp:latest
docker push registry.example.com/myapp:latest

echo "🚀 Deploying to production..."

# Deploy via docker-compose
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --remove-orphans

echo "🧹 Cleanup..."

# Remove old images
docker image prune -f

echo "✅ Deployment completed!"
```

---

## Leçon 2 : CI/CD Pipelines Avancés

### 2.1 GitHub Actions Multi-Environment

```yaml
# .github/workflows/deploy.yml

name: Deploy Application

on:
  push:
    branches: [main, staging, develop]
  pull_request:
    branches: [main]

env:
  PHP_VERSION: '8.2'
  NODE_VERSION: '20'

jobs:
  tests:
    name: Run Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testing
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ env.PHP_VERSION }}
          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_pgsql, redis
          coverage: xdebug

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Cache Composer dependencies
        uses: actions/cache@v3
        with:
          path: vendor
          key: composer-${{ hashFiles('**/composer.lock') }}

      - name: Install Composer dependencies
        run: composer install --prefer-dist --no-interaction --no-progress

      - name: Install NPM dependencies
        run: npm ci

      - name: Build assets
        run: npm run build

      - name: Prepare Laravel Application
        run: |
          cp .env.ci .env
          php artisan key:generate
          php artisan migrate --force

      - name: Run PHPStan
        run: ./vendor/bin/phpstan analyse --memory-limit=2G

      - name: Run PHP CS Fixer
        run: ./vendor/bin/php-cs-fixer fix --dry-run --diff

      - name: Run Pest tests
        run: ./vendor/bin/pest --coverage --min=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  security:
    name: Security Audit
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Composer Audit
        run: composer audit

      - name: NPM Audit
        run: npm audit --audit-level=high

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [tests, security]
    if: github.ref == 'refs/heads/staging'
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to Staging
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          script: |
            cd /var/www/staging
            git pull origin staging
            composer install --optimize-autoloader --no-dev
            npm ci && npm run build
            php artisan migrate --force
            php artisan config:cache
            php artisan route:cache
            php artisan view:cache
            php artisan queue:restart

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [tests, security]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy via Deployer
        uses: deployphp/action@v1
        with:
          private-key: ${{ secrets.DEPLOY_SSH_KEY }}
          deployer-version: "7.0.0"
          dep: deploy production

      - name: Notify Slack
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Production deployment completed!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### 2.2 GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml

stages:
  - build
  - test
  - security
  - deploy

variables:
  PHP_VERSION: "8.2"
  POSTGRES_DB: testing
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: password
  REDIS_HOST: redis

.php-base:
  image: php:${PHP_VERSION}-fpm
  before_script:
    - apt-get update -yqq
    - apt-get install -yqq git libpq-dev libzip-dev zip unzip
    - docker-php-ext-install pdo_pgsql zip
    - curl -sS https://getcomposer.org/installer | php
    - php composer.phar install --prefer-dist --no-progress

build:
  extends: .php-base
  stage: build
  script:
    - php composer.phar install --optimize-autoloader --no-dev
    - npm ci
    - npm run build
  artifacts:
    paths:
      - vendor/
      - public/build/
    expire_in: 1 hour
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - vendor/
      - node_modules/

test:unit:
  extends: .php-base
  stage: test
  services:
    - postgres:16
    - redis:7-alpine
  script:
    - cp .env.ci .env
    - php artisan key:generate
    - php artisan migrate
    - ./vendor/bin/pest --coverage --min=80
  coverage: '/^\s*Lines:\s*\d+.\d+\%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

test:phpstan:
  extends: .php-base
  stage: test
  script:
    - ./vendor/bin/phpstan analyse --memory-limit=2G

test:php-cs-fixer:
  extends: .php-base
  stage: test
  script:
    - ./vendor/bin/php-cs-fixer fix --dry-run --diff

security:composer:
  extends: .php-base
  stage: security
  script:
    - composer audit

security:npm:
  image: node:20
  stage: security
  script:
    - npm audit --audit-level=high

deploy:staging:
  stage: deploy
  only:
    - staging
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - 'which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )'
    - eval $(ssh-agent -s)
    - echo "$STAGING_SSH_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
    - ssh-keyscan $STAGING_HOST >> ~/.ssh/known_hosts
    - chmod 644 ~/.ssh/known_hosts
    - ssh $STAGING_USER@$STAGING_HOST "cd /var/www/staging && ./deploy.sh"

deploy:production:
  stage: deploy
  only:
    - main
  when: manual
  environment:
    name: production
    url: https://example.com
  script:
    - apt-get update -y && apt-get install -y rsync
    - eval $(ssh-agent -s)
    - echo "$PRODUCTION_SSH_KEY" | tr -d '\r' | ssh-add -
    - dep deploy production
```

### 2.3 Deployer Configuration

```php
<?php

// deploy.php

namespace Deployer;

require 'recipe/laravel.php';

// Config
set('application', 'myapp');
set('repository', 'git@github.com:username/myapp.git');
set('keep_releases', 5);

// Shared files/dirs
add('shared_files', ['.env']);
add('shared_dirs', ['storage']);
add('writable_dirs', ['storage', 'bootstrap/cache']);

// Hosts
host('production')
    ->setHostname('example.com')
    ->setRemoteUser('deployer')
    ->setDeployPath('/var/www/production')
    ->set('branch', 'main')
    ->set('http_user', 'www-data');

host('staging')
    ->setHostname('staging.example.com')
    ->setRemoteUser('deployer')
    ->setDeployPath('/var/www/staging')
    ->set('branch', 'staging')
    ->set('http_user', 'www-data');

// Tasks
desc('Build assets');
task('npm:build', function () {
    run('cd {{release_path}} && npm ci && npm run build');
});

desc('Restart Horizon');
task('horizon:restart', function () {
    run('cd {{release_path}} && php artisan horizon:terminate');
});

desc('Restart PHP-FPM');
task('php-fpm:restart', function () {
    run('sudo systemctl reload php8.2-fpm');
});

// Hooks
after('deploy:update_code', 'npm:build');
after('deploy:symlink', 'php-fpm:restart');
after('deploy:symlink', 'horizon:restart');

// Healthcheck
desc('Check application health');
task('healthcheck', function () {
    $response = run('curl -s -o /dev/null -w "%{http_code}" https://{{hostname}}/health');
    
    if ($response !== '200') {
        throw new \Exception('Healthcheck failed: HTTP ' . $response);
    }
    
    writeln('<info>✓ Healthcheck passed</info>');
});

after('deploy:success', 'healthcheck');

// Rollback on failure
fail('deploy', 'deploy:unlock');
```

---

## Leçon 3 : Zero-Downtime Deployment

### 3.1 Blue-Green Deployment

**Structure serveurs :**

```
Load Balancer (Nginx)
    ↓
    ├─ Blue Environment (production active)
    │   └─ app-blue.example.com
    │
    └─ Green Environment (nouvelle version)
        └─ app-green.example.com
```

**Script deployment blue-green :**

```bash
#!/bin/bash
# deploy-blue-green.sh

set -e

CURRENT_ENV=$(cat /var/www/current-env.txt) # "blue" ou "green"
NEW_ENV=$([ "$CURRENT_ENV" = "blue" ] && echo "green" || echo "blue")

APP_PATH="/var/www/${NEW_ENV}"
NGINX_CONFIG="/etc/nginx/sites-available/app"

echo "🔵🟢 Current environment: $CURRENT_ENV"
echo "🔵🟢 Deploying to: $NEW_ENV"

# 1. Deploy to inactive environment
echo "📦 Deploying application to $NEW_ENV environment..."
cd $APP_PATH

git pull origin main
composer install --optimize-autoloader --no-dev
npm ci && npm run build
php artisan migrate --force
php artisan config:cache
php artisan route:cache
php artisan view:cache

# 2. Warm up cache
echo "🔥 Warming up cache..."
curl -s http://app-${NEW_ENV}.example.com/health > /dev/null
curl -s http://app-${NEW_ENV}.example.com > /dev/null

# 3. Run smoke tests
echo "🧪 Running smoke tests..."
./vendor/bin/pest --filter=Smoke

if [ $? -ne 0 ]; then
    echo "❌ Smoke tests failed, aborting deployment"
    exit 1
fi

# 4. Switch load balancer
echo "🔄 Switching load balancer to $NEW_ENV..."

sed -i "s/app-${CURRENT_ENV}/app-${NEW_ENV}/g" $NGINX_CONFIG
sudo nginx -t && sudo systemctl reload nginx

# 5. Update current environment marker
echo $NEW_ENV > /var/www/current-env.txt

# 6. Wait and monitor
echo "⏳ Monitoring new environment for 30 seconds..."
sleep 30

# 7. Check health
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://app-${NEW_ENV}.example.com/health)

if [ "$HEALTH_STATUS" != "200" ]; then
    echo "❌ Health check failed, rolling back..."
    
    # Rollback
    sed -i "s/app-${NEW_ENV}/app-${CURRENT_ENV}/g" $NGINX_CONFIG
    sudo systemctl reload nginx
    echo $CURRENT_ENV > /var/www/current-env.txt
    
    exit 1
fi

echo "✅ Deployment to $NEW_ENV successful!"
echo "🔵🟢 $CURRENT_ENV environment is now idle (available for next deployment)"
```

### 3.2 Canary Deployment

**Nginx configuration canary :**

```nginx
# /etc/nginx/sites-available/app-canary

upstream app_stable {
    server app-stable-1.example.com:80 weight=9;
    server app-stable-2.example.com:80 weight=9;
}

upstream app_canary {
    server app-canary-1.example.com:80;
}

# Split configuration
split_clients "${remote_addr}${http_user_agent}${date_gmt}" $upstream_variant {
    10%     "canary";  # 10% traffic vers canary
    *       "stable";  # 90% traffic vers stable
}

server {
    listen 80;
    server_name example.com;

    location / {
        if ($upstream_variant = "canary") {
            proxy_pass http://app_canary;
        }
        
        proxy_pass http://app_stable;
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Script progression canary :**

```bash
#!/bin/bash
# deploy-canary.sh

set -e

# Phases: 10% → 25% → 50% → 100%
CANARY_STAGES=(10 25 50 100)

echo "🐦 Starting canary deployment..."

for STAGE in "${CANARY_STAGES[@]}"; do
    echo "📊 Deploying to $STAGE% of traffic..."
    
    # Update Nginx split percentage
    sed -i "s/[0-9]\+%/${STAGE}%/g" /etc/nginx/sites-available/app-canary
    sudo nginx -t && sudo systemctl reload nginx
    
    # Monitor for 5 minutes
    echo "⏳ Monitoring metrics for 5 minutes..."
    
    for i in {1..5}; do
        sleep 60
        
        # Check error rate
        ERROR_RATE=$(curl -s http://monitoring.example.com/api/metrics/error-rate)
        
        if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
            echo "❌ Error rate too high ($ERROR_RATE), rolling back..."
            
            # Rollback to 0%
            sed -i "s/[0-9]\+%/0%/g" /etc/nginx/sites-available/app-canary
            sudo systemctl reload nginx
            
            exit 1
        fi
        
        echo "✓ Minute $i: Error rate OK ($ERROR_RATE)"
    done
    
    echo "✅ Stage $STAGE% successful"
done

echo "🎉 Canary deployment completed! 100% traffic on new version."
```

### 3.3 Rolling Deployment

```bash
#!/bin/bash
# deploy-rolling.sh

set -e

SERVERS=(
    "app-1.example.com"
    "app-2.example.com"
    "app-3.example.com"
    "app-4.example.com"
)

DEPLOY_USER="deployer"
APP_PATH="/var/www/production"

echo "🔄 Starting rolling deployment across ${#SERVERS[@]} servers..."

for SERVER in "${SERVERS[@]}"; do
    echo ""
    echo "📦 Deploying to $SERVER..."
    
    # 1. Remove from load balancer
    echo "  ⏸️  Removing $SERVER from load balancer..."
    ssh lb.example.com "sudo /usr/local/bin/remove-backend.sh $SERVER"
    
    # 2. Wait for connections to drain
    echo "  ⏳ Draining connections (30s)..."
    sleep 30
    
    # 3. Deploy to server
    echo "  🚀 Deploying application..."
    ssh ${DEPLOY_USER}@${SERVER} << 'ENDSSH'
        cd /var/www/production
        git pull origin main
        composer install --optimize-autoloader --no-dev
        npm ci && npm run build
        php artisan migrate --force
        php artisan config:cache
        php artisan route:cache
        php artisan view:cache
        php artisan queue:restart
        sudo systemctl reload php8.2-fpm
ENDSSH
    
    # 4. Health check
    echo "  🏥 Running health check..."
    HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://${SERVER}/health)
    
    if [ "$HEALTH_STATUS" != "200" ]; then
        echo "  ❌ Health check failed on $SERVER, aborting deployment"
        exit 1
    fi
    
    # 5. Add back to load balancer
    echo "  ✅ Adding $SERVER back to load balancer..."
    ssh lb.example.com "sudo /usr/local/bin/add-backend.sh $SERVER"
    
    # 6. Monitor briefly
    echo "  📊 Monitoring for 30s..."
    sleep 30
    
    echo "  ✓ $SERVER deployed successfully"
done

echo ""
echo "🎉 Rolling deployment completed across all servers!"
```

---

## Leçon 4 : Monitoring et Observability

### 4.1 Laravel Pulse Configuration

```bash
# Install Pulse
composer require laravel/pulse
php artisan pulse:install
php artisan migrate
```

```php
<?php

// config/pulse.php

return [
    'domain' => env('PULSE_DOMAIN'),
    
    'path' => env('PULSE_PATH', 'pulse'),
    
    'enabled' => env('PULSE_ENABLED', true),

    'storage' => [
        'driver' => env('PULSE_STORAGE_DRIVER', 'database'),
    ],

    'ingest' => [
        'driver' => env('PULSE_INGEST_DRIVER', 'storage'),
        'buffer' => env('PULSE_INGEST_BUFFER', 5000),
        'trim' => [
            'keep' => env('PULSE_TRIM_KEEP', '7 days'),
            'lottery' => [1, 1000],
        ],
    ],

    'recorders' => [
        \Laravel\Pulse\Recorders\CacheInteractions::class => [
            'enabled' => env('PULSE_CACHE_INTERACTIONS_ENABLED', true),
            'sample_rate' => env('PULSE_CACHE_INTERACTIONS_SAMPLE_RATE', 1),
        ],

        \Laravel\Pulse\Recorders\Exceptions::class => [
            'enabled' => env('PULSE_EXCEPTIONS_ENABLED', true),
            'sample_rate' => env('PULSE_EXCEPTIONS_SAMPLE_RATE', 1),
            'ignore' => [
                // ...
            ],
        ],

        \Laravel\Pulse\Recorders\Queues::class => [
            'enabled' => env('PULSE_QUEUES_ENABLED', true),
            'sample_rate' => env('PULSE_QUEUES_SAMPLE_RATE', 1),
        ],

        \Laravel\Pulse\Recorders\SlowJobs::class => [
            'enabled' => env('PULSE_SLOW_JOBS_ENABLED', true),
            'sample_rate' => env('PULSE_SLOW_JOBS_SAMPLE_RATE', 1),
            'threshold' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
        ],

        \Laravel\Pulse\Recorders\SlowQueries::class => [
            'enabled' => env('PULSE_SLOW_QUERIES_ENABLED', true),
            'sample_rate' => env('PULSE_SLOW_QUERIES_SAMPLE_RATE', 1),
            'threshold' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
            'location' => env('PULSE_SLOW_QUERIES_LOCATION', true),
        ],

        \Laravel\Pulse\Recorders\SlowRequests::class => [
            'enabled' => env('PULSE_SLOW_REQUESTS_ENABLED', true),
            'sample_rate' => env('PULSE_SLOW_REQUESTS_SAMPLE_RATE', 1),
            'threshold' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
        ],

        \Laravel\Pulse\Recorders\Servers::class => [
            'server_name' => env('PULSE_SERVER_NAME', gethostname()),
            'directories' => ['/'],
        ],
    ],
];
```

### 4.2 Sentry Integration

```bash
composer require sentry/sentry-laravel
php artisan sentry:publish --dsn
```

```php
<?php

// config/sentry.php

return [
    'dsn' => env('SENTRY_LARAVEL_DSN'),

    'breadcrumbs' => [
        'logs' => true,
        'cache' => true,
        'livewire' => true,
        'sql_queries' => true,
        'sql_bindings' => true,
        'sql_transaction' => true,
        'queue_info' => true,
        'command_info' => true,
    ],

    'tracing' => [
        'enabled' => true,
        'sample_rate' => env('SENTRY_TRACES_SAMPLE_RATE', 0.2),
        'queue_job_transactions' => true,
        'queue_jobs' => true,
        'sql_queries' => true,
        'sql_origin' => true,
        'livewire' => true,
    ],

    'send_default_pii' => false,

    'traces_sampler' => function (\Sentry\Tracing\SamplingContext $context): float {
        // Sample 100% of errors
        if ($context->getParentSampled()) {
            return 1.0;
        }

        // Sample 20% of normal requests
        return 0.2;
    },

    'before_send' => function (\Sentry\Event $event): ?\Sentry\Event {
        // Filter sensitive data
        if ($event->getRequest()) {
            $request = $event->getRequest();
            
            // Remove passwords
            $request['data'] = array_filter(
                $request['data'] ?? [],
                fn($key) => !str_contains(strtolower($key), 'password'),
                ARRAY_FILTER_USE_KEY
            );
        }

        return $event;
    },
];
```

**Custom Sentry context Livewire :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Sentry\State\Scope;

class BaseComponent extends Component
{
    public function boot(): void
    {
        // Add Livewire context to Sentry
        \Sentry\configureScope(function (Scope $scope): void {
            $scope->setContext('livewire', [
                'component' => static::class,
                'id' => $this->getId(),
                'properties' => $this->all(),
            ]);
        });
    }
}
```

### 4.3 Custom Metrics

```php
<?php

namespace App\Services;

use Illuminate\Support\Facades\Redis;

class MetricsService
{
    /**
     * Increment counter metric
     */
    public function increment(string $metric, int $value = 1, array $tags = []): void
    {
        $key = $this->buildKey($metric, $tags);
        
        Redis::incrby($key, $value);
        Redis::expire($key, 86400); // 24h retention
    }

    /**
     * Record gauge metric
     */
    public function gauge(string $metric, float $value, array $tags = []): void
    {
        $key = $this->buildKey($metric, $tags);
        
        Redis::set($key, $value);
        Redis::expire($key, 86400);
    }

    /**
     * Record timing metric
     */
    public function timing(string $metric, float $milliseconds, array $tags = []): void
    {
        $key = $this->buildKey($metric, $tags);
        
        Redis::zadd($key, time(), $milliseconds);
        Redis::expire($key, 86400);
    }

    /**
     * Get metric value
     */
    public function get(string $metric, array $tags = []): mixed
    {
        $key = $this->buildKey($metric, $tags);
        
        return Redis::get($key);
    }

    /**
     * Build metric key with tags
     */
    protected function buildKey(string $metric, array $tags): string
    {
        $tagString = '';
        
        if (!empty($tags)) {
            ksort($tags);
            $tagString = '.' . implode('.', array_map(
                fn($k, $v) => "{$k}={$v}",
                array_keys($tags),
                $tags
            ));
        }

        return "metrics:{$metric}{$tagString}";
    }
}
```

**Usage dans Livewire :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Services\MetricsService;

class ProductSearch extends Component
{
    public string $query = '';

    protected MetricsService $metrics;

    public function boot(MetricsService $metrics): void
    {
        $this->metrics = $metrics;
    }

    public function search(): void
    {
        $startTime = microtime(true);

        $results = Product::where('name', 'like', "%{$this->query}%")->get();

        $duration = (microtime(true) - $startTime) * 1000;

        // Record metrics
        $this->metrics->increment('search.requests', 1, [
            'component' => 'product-search',
        ]);

        $this->metrics->timing('search.duration', $duration, [
            'component' => 'product-search',
        ]);

        $this->metrics->gauge('search.results', $results->count(), [
            'component' => 'product-search',
        ]);
    }

    public function render()
    {
        return view('livewire.product-search');
    }
}
```

### 4.4 Health Checks

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Redis;

class HealthController extends Controller
{
    public function index()
    {
        $checks = [
            'database' => $this->checkDatabase(),
            'redis' => $this->checkRedis(),
            'queue' => $this->checkQueue(),
            'storage' => $this->checkStorage(),
        ];

        $healthy = collect($checks)->every(fn($check) => $check['status'] === 'ok');

        return response()->json([
            'status' => $healthy ? 'ok' : 'degraded',
            'timestamp' => now()->toIso8601String(),
            'checks' => $checks,
        ], $healthy ? 200 : 503);
    }

    protected function checkDatabase(): array
    {
        try {
            DB::connection()->getPdo();
            
            return [
                'status' => 'ok',
                'message' => 'Database connection successful',
            ];
        } catch (\Exception $e) {
            return [
                'status' => 'error',
                'message' => 'Database connection failed: ' . $e->getMessage(),
            ];
        }
    }

    protected function checkRedis(): array
    {
        try {
            Redis::ping();
            
            return [
                'status' => 'ok',
                'message' => 'Redis connection successful',
            ];
        } catch (\Exception $e) {
            return [
                'status' => 'error',
                'message' => 'Redis connection failed: ' . $e->getMessage(),
            ];
        }
    }

    protected function checkQueue(): array
    {
        try {
            $size = Redis::llen('queues:default');
            
            return [
                'status' => $size < 1000 ? 'ok' : 'warning',
                'message' => "Queue size: {$size}",
                'queue_size' => $size,
            ];
        } catch (\Exception $e) {
            return [
                'status' => 'error',
                'message' => 'Queue check failed: ' . $e->getMessage(),
            ];
        }
    }

    protected function checkStorage(): array
    {
        try {
            $diskSpace = disk_free_space('/');
            $diskTotal = disk_total_space('/');
            $percentFree = ($diskSpace / $diskTotal) * 100;
            
            return [
                'status' => $percentFree > 10 ? 'ok' : 'warning',
                'message' => sprintf('Disk space: %.2f%% free', $percentFree),
                'disk_free' => $diskSpace,
                'disk_total' => $diskTotal,
            ];
        } catch (\Exception $e) {
            return [
                'status' => 'error',
                'message' => 'Storage check failed: ' . $e->getMessage(),
            ];
        }
    }
}
```

---

## Leçon 5 : Internationalization (i18n)

### 5.1 Configuration i18n

```php
<?php

// config/app.php

return [
    'locale' => 'fr',
    'fallback_locale' => 'en',
    'available_locales' => ['en', 'fr', 'es', 'de'],
];
```

**Translation files :**

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application',
    'greeting' => 'Hello, :name!',
    'items_count' => '{0} No items|{1} One item|[2,*] :count items',
    'login' => 'Log in',
    'register' => 'Register',
];

// lang/fr/messages.php

return [
    'welcome' => 'Bienvenue dans notre application',
    'greeting' => 'Bonjour, :name !',
    'items_count' => '{0} Aucun élément|{1} Un élément|[2,*] :count éléments',
    'login' => 'Se connecter',
    'register' => 'S\'inscrire',
];
```

### 5.2 Locale Switcher Livewire

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Illuminate\Support\Facades\App;

class LocaleSwitcher extends Component
{
    public string $currentLocale;
    public array $availableLocales;

    public function mount(): void
    {
        $this->currentLocale = App::getLocale();
        $this->availableLocales = config('app.available_locales');
    }

    public function switchLocale(string $locale): void
    {
        if (!in_array($locale, $this->availableLocales)) {
            return;
        }

        // Update session
        session(['locale' => $locale]);

        // Update user preference (if authenticated)
        if (auth()->check()) {
            auth()->user()->update(['locale' => $locale]);
        }

        // Set application locale
        App::setLocale($locale);

        $this->currentLocale = $locale;

        // Refresh page to apply locale
        $this->redirect(request()->url(), navigate: true);
    }

    public function render()
    {
        return view('livewire.locale-switcher');
    }
}
```

```blade
{{-- resources/views/livewire/locale-switcher.blade.php --}}

<div class="locale-switcher">
    <select wire:model.live="currentLocale" wire:change="switchLocale($event.target.value)">
        @foreach($availableLocales as $locale)
            <option value="{{ $locale }}" @selected($locale === $currentLocale)>
                {{ strtoupper($locale) }}
            </option>
        @endforeach
    </select>
</div>
```

### 5.3 Middleware Locale

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\App;

class SetLocale
{
    public function handle(Request $request, Closure $next)
    {
        // Priority: URL param > User preference > Session > Browser > Default
        
        // 1. URL parameter
        if ($request->has('locale')) {
            $locale = $request->get('locale');
            session(['locale' => $locale]);
        }
        
        // 2. User preference (authenticated)
        elseif (auth()->check() && auth()->user()->locale) {
            $locale = auth()->user()->locale;
        }
        
        // 3. Session
        elseif (session()->has('locale')) {
            $locale = session('locale');
        }
        
        // 4. Browser Accept-Language
        else {
            $locale = $this->parseAcceptLanguage($request);
        }

        // Validate locale
        if (!in_array($locale, config('app.available_locales'))) {
            $locale = config('app.fallback_locale');
        }

        App::setLocale($locale);
        
        // Set Carbon locale for date formatting
        setlocale(LC_TIME, $locale);

        return $next($request);
    }

    protected function parseAcceptLanguage(Request $request): string
    {
        $acceptLanguage = $request->header('Accept-Language');
        
        if (!$acceptLanguage) {
            return config('app.fallback_locale');
        }

        // Parse "en-US,en;q=0.9,fr;q=0.8"
        $languages = explode(',', $acceptLanguage);
        $preferred = explode(';', $languages[0])[0];
        $locale = substr($preferred, 0, 2); // Extract "en" from "en-US"

        return $locale;
    }
}
```

### 5.4 Translatable Models

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Spatie\Translatable\HasTranslations;

class Product extends Model
{
    use HasTranslations;

    public $translatable = ['name', 'description'];

    protected $fillable = ['name', 'description', 'price'];
}
```

```php
<?php

// Usage

// Set translations
$product = new Product;
$product->setTranslation('name', 'en', 'Product Name');
$product->setTranslation('name', 'fr', 'Nom du produit');
$product->setTranslation('description', 'en', 'Product description');
$product->setTranslation('description', 'fr', 'Description du produit');
$product->save();

// Get translation (current locale)
$product->name; // Returns current locale translation

// Get specific locale
$product->getTranslation('name', 'fr'); // "Nom du produit"
```

**Livewire avec translatable models :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Product;

class ProductForm extends Component
{
    public Product $product;
    public array $availableLocales;

    public function mount(?int $productId = null): void
    {
        $this->product = $productId 
            ? Product::findOrFail($productId) 
            : new Product;
            
        $this->availableLocales = config('app.available_locales');
    }

    public function save(): void
    {
        foreach ($this->availableLocales as $locale) {
            $this->validate([
                "product.name.{$locale}" => 'required|min:3',
                "product.description.{$locale}" => 'required|min:10',
            ]);
        }

        $this->product->save();

        session()->flash('message', __('messages.product_saved'));
    }

    public function render()
    {
        return view('livewire.product-form');
    }
}
```

```blade
<div>
    <form wire:submit.prevent="save">
        @foreach($availableLocales as $locale)
            <div class="locale-section">
                <h3>{{ strtoupper($locale) }}</h3>
                
                <label>{{ __('messages.name') }} ({{ $locale }})</label>
                <input 
                    type="text" 
                    wire:model="product.name.{{ $locale }}"
                >
                @error("product.name.{$locale}") 
                    <span class="error">{{ $message }}</span> 
                @enderror

                <label>{{ __('messages.description') }} ({{ $locale }})</label>
                <textarea wire:model="product.description.{{ $locale }}"></textarea>
                @error("product.description.{$locale}") 
                    <span class="error">{{ $message }}</span> 
                @enderror
            </div>
        @endforeach

        <button type="submit">{{ __('messages.save') }}</button>
    </form>
</div>
```

### 5.5 Date/Number Localization

```php
<?php

namespace App\Services;

use Carbon\Carbon;

class LocalizationService
{
    /**
     * Format date according to locale
     */
    public function formatDate(Carbon $date, string $format = 'long'): string
    {
        $locale = app()->getLocale();

        return match($format) {
            'short' => $date->locale($locale)->format('d/m/Y'),
            'long' => $date->locale($locale)->isoFormat('LL'),
            'full' => $date->locale($locale)->isoFormat('LLLL'),
            'relative' => $date->locale($locale)->diffForHumans(),
            default => $date->locale($locale)->format($format),
        };
    }

    /**
     * Format number according to locale
     */
    public function formatNumber(float $number, int $decimals = 2): string
    {
        $locale = app()->getLocale();

        return match($locale) {
            'fr' => number_format($number, $decimals, ',', ' '),
            'de' => number_format($number, $decimals, ',', '.'),
            default => number_format($number, $decimals, '.', ','),
        };
    }

    /**
     * Format currency
     */
    public function formatCurrency(float $amount, string $currency = 'EUR'): string
    {
        $locale = app()->getLocale();

        $formatter = new \NumberFormatter($locale, \NumberFormatter::CURRENCY);
        
        return $formatter->formatCurrency($amount, $currency);
    }
}
```

---

## Leçon 6 : Accessibility (a11y)

### 6.1 ARIA Attributes Livewire

```blade
{{-- Accessible form with ARIA --}}
<form wire:submit.prevent="save" aria-labelledby="form-title">
    <h2 id="form-title">{{ __('User Registration') }}</h2>

    <div class="form-group">
        <label for="name">
            {{ __('Name') }}
            <span aria-label="required">*</span>
        </label>
        <input 
            type="text"
            id="name"
            wire:model="name"
            aria-required="true"
            aria-invalid="{{ $errors->has('name') ? 'true' : 'false' }}"
            aria-describedby="{{ $errors->has('name') ? 'name-error' : '' }}"
        >
        @error('name')
            <span id="name-error" role="alert" class="error">
                {{ $message }}
            </span>
        @enderror
    </div>

    <button 
        type="submit" 
        aria-busy="{{ $loading ? 'true' : 'false' }}"
        :disabled="$loading"
    >
        {{ __('Register') }}
        <span wire:loading wire:target="save" aria-live="polite">
            {{ __('Processing...') }}
        </span>
    </button>
</form>
```

### 6.2 Keyboard Navigation

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class AccessibleModal extends Component
{
    public bool $open = false;
    public ?string $focusTrapId = null;

    public function openModal(): void
    {
        $this->open = true;
        $this->focusTrapId = uniqid('modal-');
        
        // Dispatch browser event pour focus trap
        $this->dispatch('modal-opened', id: $this->focusTrapId);
    }

    public function closeModal(): void
    {
        $this->open = false;
        $this->focusTrapId = null;
        
        $this->dispatch('modal-closed');
    }

    public function render()
    {
        return view('livewire.accessible-modal');
    }
}
```

```blade
<div x-data="accessibleModal()" 
     @keydown.escape.window="$wire.closeModal()"
     @modal-opened.window="trapFocus($event.detail.id)"
     @modal-closed.window="restoreFocus()">
    
    {{-- Trigger button --}}
    <button 
        wire:click="openModal"
        aria-haspopup="dialog"
        aria-expanded="{{ $open ? 'true' : 'false' }}"
    >
        Open Modal
    </button>

    {{-- Modal --}}
    @if($open)
        <div 
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            id="{{ $focusTrapId }}"
            class="modal-overlay"
        >
            <div class="modal-content">
                <h2 id="modal-title">Modal Title</h2>
                
                <div class="modal-body">
                    <p>Modal content...</p>
                </div>

                <div class="modal-actions">
                    <button wire:click="closeModal" autofocus>
                        Close
                    </button>
                </div>
            </div>
        </div>
    @endif
</div>

<script>
function accessibleModal() {
    return {
        previousFocus: null,
        
        trapFocus(modalId) {
            // Save previous focus
            this.previousFocus = document.activeElement;
            
            // Focus first focusable element in modal
            const modal = document.getElementById(modalId);
            const focusable = modal.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            
            if (focusable.length) {
                focusable[0].focus();
            }
            
            // Trap focus within modal
            modal.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    const firstFocusable = focusable[0];
                    const lastFocusable = focusable[focusable.length - 1];
                    
                    if (e.shiftKey && document.activeElement === firstFocusable) {
                        e.preventDefault();
                        lastFocusable.focus();
                    } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                        e.preventDefault();
                        firstFocusable.focus();
                    }
                }
            });
        },
        
        restoreFocus() {
            // Restore focus to previous element
            if (this.previousFocus) {
                this.previousFocus.focus();
            }
        }
    }
}
</script>
```

### 6.3 Screen Reader Announcements

```blade
{{-- Live region for screen reader announcements --}}
<div 
    aria-live="polite" 
    aria-atomic="true"
    class="sr-only"
    wire:key="sr-announcements"
>
    @if(session('message'))
        {{ session('message') }}
    @endif
    
    @if($loading)
        {{ __('Loading content, please wait...') }}
    @endif
</div>

{{-- Visually hidden utility class --}}
<style>
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
</style>
```

### 6.4 Skip Links

```blade
<!DOCTYPE html>
<html lang="{{ app()->getLocale() }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ config('app.name') }}</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    {{-- Skip links (appear on focus) --}}
    <a href="#main-content" class="skip-link">
        {{ __('Skip to main content') }}
    </a>
    
    <a href="#main-navigation" class="skip-link">
        {{ __('Skip to navigation') }}
    </a>

    <nav id="main-navigation">
        {{-- Navigation --}}
    </nav>

    <main id="main-content" tabindex="-1">
        {{ $slot }}
    </main>

    <style>
    .skip-link {
        position: absolute;
        top: -40px;
        left: 0;
        background: #000;
        color: #fff;
        padding: 8px;
        text-decoration: none;
        z-index: 100;
    }
    
    .skip-link:focus {
        top: 0;
    }
    </style>
</body>
</html>
```

### 6.5 Accessibility Testing

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class AccessibilityTest extends TestCase
{
    /** @test */
    public function form_inputs_have_labels()
    {
        $response = $this->get('/register');

        // Check all inputs have associated labels
        $html = $response->getContent();
        
        preg_match_all('/<input[^>]*id=["\']([^"\']*)["\']/', $html, $inputs);
        
        foreach ($inputs[1] as $inputId) {
            $this->assertStringContainsString(
                "for=\"{$inputId}\"",
                $html,
                "Input #{$inputId} missing associated label"
            );
        }
    }

    /** @test */
    public function buttons_have_accessible_text()
    {
        $response = $this->get('/dashboard');

        $html = $response->getContent();
        
        // Check no buttons with only icons
        $this->assertStringNotContainsString(
            '<button></button>',
            $html
        );
        
        // Check buttons have text or aria-label
        preg_match_all('/<button[^>]*>([^<]*)<\/button>/', $html, $buttons);
        
        foreach ($buttons[0] as $index => $button) {
            $hasText = !empty(trim($buttons[1][$index]));
            $hasAriaLabel = str_contains($button, 'aria-label=');
            
            $this->assertTrue(
                $hasText || $hasAriaLabel,
                "Button without accessible text: {$button}"
            );
        }
    }

    /** @test */
    public function images_have_alt_text()
    {
        $response = $this->get('/products');

        $html = $response->getContent();
        
        preg_match_all('/<img[^>]*>/', $html, $images);
        
        foreach ($images[0] as $img) {
            $this->assertStringContainsString(
                'alt=',
                $img,
                "Image missing alt attribute: {$img}"
            );
        }
    }
}
```

---

## Leçon 7 : Progressive Web App (PWA)

### 7.1 Service Worker

```javascript
// public/sw.js

const CACHE_VERSION = 'v1.0.0';
const CACHE_NAME = `myapp-${CACHE_VERSION}`;

const STATIC_CACHE_URLS = [
    '/',
    '/offline',
    '/css/app.css',
    '/js/app.js',
    '/images/logo.png',
];

// Install event
self.addEventListener('install', (event) => {
    console.log('Service Worker installing...');
    
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_CACHE_URLS);
        })
    );
    
    self.skipWaiting();
});

// Activate event
self.addEventListener('activate', (event) => {
    console.log('Service Worker activating...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    self.clients.claim();
});

// Fetch event - Network First strategy
self.addEventListener('fetch', (event) => {
    const { request } = event;
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip Livewire requests
    if (request.url.includes('/livewire/')) {
        return;
    }
    
    event.respondWith(
        fetch(request)
            .then((response) => {
                // Clone response before caching
                const responseClone = response.clone();
                
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(request, responseClone);
                });
                
                return response;
            })
            .catch(() => {
                // Fallback to cache
                return caches.match(request).then((cachedResponse) => {
                    if (cachedResponse) {
                        return cachedResponse;
                    }
                    
                    // Fallback to offline page
                    if (request.mode === 'navigate') {
                        return caches.match('/offline');
                    }
                });
            })
    );
});

// Background sync
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-forms') {
        event.waitUntil(syncForms());
    }
});

async function syncForms() {
    const db = await openIndexedDB();
    const forms = await db.getAll('pending-forms');
    
    for (const form of forms) {
        try {
            await fetch('/api/forms', {
                method: 'POST',
                body: JSON.stringify(form.data),
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            await db.delete('pending-forms', form.id);
        } catch (error) {
            console.error('Failed to sync form:', error);
        }
    }
}
```

### 7.2 Manifest.json

```json
{
  "name": "MyApp - Full Application Name",
  "short_name": "MyApp",
  "description": "MyApp is an awesome Livewire application",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4F46E5",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/images/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/images/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/images/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/images/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/images/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/images/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/images/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/images/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable any"
    }
  ],
  "screenshots": [
    {
      "src": "/images/screenshots/desktop-1.png",
      "sizes": "1920x1080",
      "type": "image/png",
      "form_factor": "wide"
    },
    {
      "src": "/images/screenshots/mobile-1.png",
      "sizes": "750x1334",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ],
  "categories": ["productivity", "business"],
  "share_target": {
    "action": "/share",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "title": "title",
      "text": "text",
      "url": "url"
    }
  }
}
```

### 7.3 Install Prompt

```javascript
// resources/js/pwa.js

let deferredPrompt;
const installButton = document.getElementById('install-pwa');

// Capture beforeinstallprompt event
window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent default prompt
    e.preventDefault();
    
    // Store event for later use
    deferredPrompt = e;
    
    // Show custom install button
    if (installButton) {
        installButton.style.display = 'block';
    }
});

// Handle install button click
if (installButton) {
    installButton.addEventListener('click', async () => {
        if (!deferredPrompt) {
            return;
        }
        
        // Show install prompt
        deferredPrompt.prompt();
        
        // Wait for user response
        const { outcome } = await deferredPrompt.userChoice;
        
        console.log(`User response: ${outcome}`);
        
        // Clear deferredPrompt
        deferredPrompt = null;
        
        // Hide button
        installButton.style.display = 'none';
    });
}

// Detect if already installed
window.addEventListener('appinstalled', () => {
    console.log('PWA installed successfully');
    
    // Hide install button
    if (installButton) {
        installButton.style.display = 'none';
    }
    
    // Send analytics event
    if (window.gtag) {
        gtag('event', 'pwa_install', {
            event_category: 'engagement',
        });
    }
});

// Check if running as PWA
function isPWA() {
    return window.matchMedia('(display-mode: standalone)').matches ||
           window.navigator.standalone === true;
}

if (isPWA()) {
    console.log('Running as PWA');
    document.body.classList.add('pwa-mode');
}
```

### 7.4 Offline Support Livewire

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class OfflineForm extends Component
{
    public string $name = '';
    public string $email = '';
    public string $message = '';

    public function save(): void
    {
        $this->validate([
            'name' => 'required|min:3',
            'email' => 'required|email',
            'message' => 'required|min:10',
        ]);

        // Save to database
        ContactForm::create([
            'name' => $this->name,
            'email' => $this->email,
            'message' => $this->message,
        ]);

        session()->flash('message', __('Form submitted successfully'));
        
        $this->reset();
    }

    public function render()
    {
        return view('livewire.offline-form');
    }
}
```

```blade
<div x-data="offlineForm()" @online.window="handleOnline()" @offline.window="handleOffline()">
    @if(session('message'))
        <div class="alert-success">{{ session('message') }}</div>
    @endif

    <div x-show="!online" class="alert-warning">
        {{ __('You are offline. Form will be submitted when connection is restored.') }}
    </div>

    <form wire:submit.prevent="save" @submit="handleSubmit($event)">
        <input type="text" wire:model="name" placeholder="{{ __('Name') }}">
        @error('name') <span class="error">{{ $message }}</span> @enderror

        <input type="email" wire:model="email" placeholder="{{ __('Email') }}">
        @error('email') <span class="error">{{ $message }}</span> @enderror

        <textarea wire:model="message" placeholder="{{ __('Message') }}"></textarea>
        @error('message') <span class="error">{{ $message }}</span> @enderror

        <button type="submit" :disabled="!online">
            {{ __('Submit') }}
        </button>
    </form>
</div>

<script>
function offlineForm() {
    return {
        online: navigator.onLine,
        
        handleOnline() {
            this.online = true;
            console.log('Back online');
            
            // Try to sync pending forms
            if ('serviceWorker' in navigator && 'sync' in navigator.serviceWorker) {
                navigator.serviceWorker.ready.then((registration) => {
                    return registration.sync.register('sync-forms');
                });
            }
        },
        
        handleOffline() {
            this.online = false;
            console.log('Gone offline');
        },
        
        handleSubmit(event) {
            if (!this.online) {
                event.preventDefault();
                
                // Store in IndexedDB for later sync
                const formData = new FormData(event.target);
                const data = Object.fromEntries(formData.entries());
                
                this.storeOfflineForm(data);
                
                alert('Form saved offline. Will be submitted when connection is restored.');
            }
        },
        
        async storeOfflineForm(data) {
            const db = await openIndexedDB();
            await db.add('pending-forms', {
                data: data,
                timestamp: Date.now(),
            });
        }
    }
}

async function openIndexedDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('OfflineFormsDB', 1);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('pending-forms')) {
                db.createObjectStore('pending-forms', { autoIncrement: true });
            }
        };
    });
}
</script>
```

---

## Leçon 8 : Advanced Troubleshooting

### 8.1 Laravel Debugbar

```bash
composer require barryvdh/laravel-debugbar --dev
```

**Custom Debugbar collectors :**

```php
<?php

namespace App\Debug;

use DebugBar\DataCollector\DataCollector;
use DebugBar\DataCollector\Renderable;

class LivewireCollector extends DataCollector implements Renderable
{
    protected array $components = [];

    public function addComponent(string $name, array $data): void
    {
        $this->components[] = [
            'name' => $name,
            'data' => $data,
            'memory' => memory_get_usage(true),
            'time' => microtime(true),
        ];
    }

    public function collect(): array
    {
        return [
            'count' => count($this->components),
            'components' => $this->components,
            'total_memory' => array_sum(array_column($this->components, 'memory')),
        ];
    }

    public function getName(): string
    {
        return 'livewire';
    }

    public function getWidgets(): array
    {
        return [
            'livewire' => [
                'icon' => 'bolt',
                'widget' => 'PhpDebugBar.Widgets.VariableListWidget',
                'map' => 'livewire.components',
                'default' => '[]',
            ],
            'livewire:badge' => [
                'map' => 'livewire.count',
                'default' => 0,
            ],
        ];
    }
}
```

### 8.2 Spatie Ray

```bash
composer require spatie/laravel-ray --dev
```

**Usage Ray dans Livewire :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class ProductSearch extends Component
{
    public string $query = '';
    public array $results = [];

    public function search(): void
    {
        ray('Search triggered', $this->query);
        
        $startTime = microtime(true);

        $this->results = Product::where('name', 'like', "%{$this->query}%")
            ->get()
            ->toArray();

        $duration = (microtime(true) - $startTime) * 1000;

        ray('Search completed')
            ->orange()
            ->label('Results: ' . count($this->results))
            ->measure('duration', $duration);

        if (count($this->results) === 0) {
            ray('No results found')->red();
        }
    }

    public function render()
    {
        ray()->showQueries();
        
        return view('livewire.product-search');
    }
}
```

**Ray useful methods :**

```php
<?php

ray($variable);                    // Basic output
ray()->green();                    // Color output
ray()->large();                    // Large font
ray()->small();                    // Small font
ray()->label('Debug info');        // Add label
ray()->caller();                   // Show caller info
ray()->trace();                    // Stack trace
ray()->pause();                    // Pause execution
ray()->showQueries();              // Show SQL queries
ray()->showEvents();               // Show events
ray()->showJobs();                 // Show queued jobs
ray()->ban();                      // Stop sending to Ray
ray()->charles();                  // Continue sending
ray()->clearAll();                 // Clear all output
ray()->measure();                  // Measure performance
ray()->table($data);               // Table output
ray()->json($data);                // JSON output
ray()->xml($data);                 // XML output
ray()->if($condition, $value);     // Conditional output
ray()->die();                      // Die and halt
```

### 8.3 Query Profiling

```php
<?php

namespace App\Services;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class QueryProfiler
{
    protected array $queries = [];

    public function start(): void
    {
        DB::enableQueryLog();
    }

    public function stop(): array
    {
        $queries = DB::getQueryLog();
        
        $this->analyze($queries);
        
        DB::disableQueryLog();
        
        return $this->queries;
    }

    protected function analyze(array $queries): void
    {
        foreach ($queries as $query) {
            $analysis = [
                'sql' => $query['query'],
                'bindings' => $query['bindings'],
                'time' => $query['time'],
                'slow' => $query['time'] > 100, // > 100ms
                'n_plus_one' => $this->detectNPlusOne($query['query']),
            ];

            $this->queries[] = $analysis;

            // Log slow queries
            if ($analysis['slow']) {
                Log::warning('Slow query detected', $analysis);
            }

            // Log N+1
            if ($analysis['n_plus_one']) {
                Log::warning('Potential N+1 query detected', $analysis);
            }
        }
    }

    protected function detectNPlusOne(string $sql): bool
    {
        // Detect patterns like: SELECT * FROM table WHERE id = ?
        // Repeated in loop = potential N+1
        
        $pattern = '/SELECT .* FROM \w+ WHERE \w+\.?\w* = \?/i';
        
        return preg_match($pattern, $sql) === 1;
    }

    public function report(): void
    {
        $totalTime = array_sum(array_column($this->queries, 'time'));
        $slowQueries = array_filter($this->queries, fn($q) => $q['slow']);
        $nPlusOne = array_filter($this->queries, fn($q) => $q['n_plus_one']);

        ray('Query Profiler Report')
            ->table([
                'Total Queries' => count($this->queries),
                'Total Time' => round($totalTime, 2) . 'ms',
                'Slow Queries' => count($slowQueries),
                'Potential N+1' => count($nPlusOne),
            ]);

        if (count($slowQueries) > 0) {
            ray('Slow Queries')->orange()->table($slowQueries);
        }

        if (count($nPlusOne) > 0) {
            ray('Potential N+1 Queries')->red()->table($nPlusOne);
        }
    }
}
```

**Usage dans Livewire :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Services\QueryProfiler;

class ProductList extends Component
{
    protected QueryProfiler $profiler;

    public function boot(QueryProfiler $profiler): void
    {
        $this->profiler = $profiler;
    }

    public function render()
    {
        $this->profiler->start();

        $products = Product::with('category', 'brand')->paginate(20);

        $this->profiler->stop();
        $this->profiler->report();

        return view('livewire.product-list', [
            'products' => $products
        ]);
    }
}
```

### 8.4 Common Issues Troubleshooting

**Checklist problèmes fréquents :**

```markdown
## Livewire ne met pas à jour

❓ wire:model ne fonctionne pas
✓ Vérifier propriété publique
✓ Vérifier wire:key unique sur éléments boucle
✓ Vérifier .live/.blur/.debounce modifiers
✓ Vérifier console navigateur erreurs JS

❓ Méthode non appelée
✓ Vérifier méthode publique
✓ Vérifier wire:click syntax correcte
✓ Vérifier pas d'erreur PHP (logs)
✓ Vérifier CSRF token présent

## Performance lente

❓ Render lent
✓ Activer query log détecter N+1
✓ Vérifier eager loading relations
✓ Vérifier cache queries lourdes
✓ Vérifier select colonnes spécifiques

❓ Trop de requêtes
✓ Utiliser wire:poll.keep-alive
✓ Limiter listeners events
✓ Vérifier pas boucle infinie updates

## Erreurs validation

❓ Validation ne déclenche pas
✓ Vérifier $rules défini
✓ Vérifier validate() appelé
✓ Vérifier messages erreur affichés Blade

❓ Validation temps réel
✓ Vérifier updated{Property}() hook
✓ Vérifier validateOnly() utilisé
✓ Vérifier debounce sur inputs

## File uploads

❓ Upload ne fonctionne pas
✓ Vérifier WithFileUploads trait
✓ Vérifier config livewire.php
✓ Vérifier permissions storage/livewire-tmp
✓ Vérifier max upload size PHP/Nginx

## Tests échouent

❓ Tests Livewire fail
✓ Vérifier RefreshDatabase trait
✓ Vérifier factories définies
✓ Vérifier setup DB testing
✓ Vérifier mocks services externes
```

---

## Leçon 9 : Migration et Upgrade Strategies

### 9.1 Feature Flags

```php
<?php

namespace App\Services;

use Illuminate\Support\Facades\Cache;

class FeatureFlagService
{
    /**
     * Check if feature enabled
     */
    public function isEnabled(string $feature, ?int $userId = null): bool
    {
        // Check override in config
        if (config("features.{$feature}") !== null) {
            return config("features.{$feature}");
        }

        // Check user-specific flags
        if ($userId && $this->isEnabledForUser($feature, $userId)) {
            return true;
        }

        // Check percentage rollout
        if ($percentage = $this->getPercentage($feature)) {
            return $this->isInPercentage($percentage, $userId);
        }

        // Default disabled
        return false;
    }

    protected function isEnabledForUser(string $feature, int $userId): bool
    {
        $enabledUsers = Cache::remember(
            "feature-flag:{$feature}:users",
            3600,
            fn() => config("features.users.{$feature}", [])
        );

        return in_array($userId, $enabledUsers);
    }

    protected function getPercentage(string $feature): ?int
    {
        return Cache::remember(
            "feature-flag:{$feature}:percentage",
            3600,
            fn() => config("features.percentage.{$feature}")
        );
    }

    protected function isInPercentage(int $percentage, ?int $userId): bool
    {
        if (!$userId) {
            return rand(1, 100) <= $percentage;
        }

        // Deterministic based on user ID
        return ($userId % 100) < $percentage;
    }
}
```

**Configuration :**

```php
<?php

// config/features.php

return [
    // Global toggles
    'new_dashboard' => env('FEATURE_NEW_DASHBOARD', false),
    'ai_suggestions' => env('FEATURE_AI_SUGGESTIONS', false),

    // User-specific
    'users' => [
        'beta_features' => [1, 2, 3, 10], // User IDs
    ],

    // Percentage rollout
    'percentage' => [
        'new_checkout' => 25, // 25% of users
        'dark_mode' => 50,    // 50% of users
    ],
];
```

**Usage dans Livewire :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Services\FeatureFlagService;

class Dashboard extends Component
{
    protected FeatureFlagService $features;

    public function boot(FeatureFlagService $features): void
    {
        $this->features = $features;
    }

    public function render()
    {
        $useNewDashboard = $this->features->isEnabled(
            'new_dashboard',
            auth()->id()
        );

        return view($useNewDashboard ? 'livewire.dashboard-v2' : 'livewire.dashboard');
    }
}
```

### 9.2 Database Migrations Safe

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run migrations (zero-downtime strategy)
     */
    public function up(): void
    {
        // Step 1: Add new column (nullable)
        Schema::table('users', function (Blueprint $table) {
            $table->string('new_email')->nullable()->after('email');
            $table->index('new_email'); // Add index immediately
        });

        // Step 2: Backfill data (chunk to avoid timeout)
        DB::table('users')
            ->whereNull('new_email')
            ->chunkById(1000, function ($users) {
                foreach ($users as $user) {
                    DB::table('users')
                        ->where('id', $user->id)
                        ->update(['new_email' => $user->email]);
                }
            });

        // Step 3: Make NOT NULL (after backfill complete)
        Schema::table('users', function (Blueprint $table) {
            $table->string('new_email')->nullable(false)->change();
        });

        // Step 4: Drop old column (after deploy code using new column)
        // Schema::table('users', function (Blueprint $table) {
        //     $table->dropColumn('email');
        // });

        // Step 5: Rename new column (separate migration)
        // Schema::table('users', function (Blueprint $table) {
        //     $table->renameColumn('new_email', 'email');
        // });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('new_email');
        });
    }
};
```

### 9.3 Blue-Green Database Migration

```bash
#!/bin/bash
# migrate-blue-green.sh

set -e

CURRENT_DB="myapp_production"
NEW_DB="myapp_production_new"

echo "🔵🟢 Blue-Green Database Migration"

# 1. Create new database (green)
echo "📦 Creating new database..."
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS ${NEW_DB};"

# 2. Copy structure
echo "📋 Copying database structure..."
mysqldump -u root -p --no-data ${CURRENT_DB} | mysql -u root -p ${NEW_DB}

# 3. Copy data (online)
echo "📊 Copying data (this may take a while)..."
mysqldump -u root -p ${CURRENT_DB} | mysql -u root -p ${NEW_DB}

# 4. Run migrations on new database
echo "🔄 Running migrations on new database..."
php artisan migrate --database=mysql_new --force

# 5. Verify data integrity
echo "✅ Verifying data integrity..."
CURRENT_COUNT=$(mysql -u root -p -e "USE ${CURRENT_DB}; SELECT COUNT(*) FROM users;" -N)
NEW_COUNT=$(mysql -u root -p -e "USE ${NEW_DB}; SELECT COUNT(*) FROM users;" -N)

if [ "$CURRENT_COUNT" != "$NEW_COUNT" ]; then
    echo "❌ Data integrity check failed!"
    exit 1
fi

# 6. Switch application to new database
echo "🔄 Switching to new database..."
sed -i "s/DB_DATABASE=${CURRENT_DB}/DB_DATABASE=${NEW_DB}/g" .env

# 7. Reload application
php artisan config:cache
sudo systemctl reload php8.2-fpm

# 8. Monitor for issues (30 seconds)
echo "⏳ Monitoring new database for 30 seconds..."
sleep 30

# 9. Check application health
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health)

if [ "$HEALTH_STATUS" != "200" ]; then
    echo "❌ Health check failed, rolling back..."
    
    # Rollback
    sed -i "s/DB_DATABASE=${NEW_DB}/DB_DATABASE=${CURRENT_DB}/g" .env
    php artisan config:cache
    sudo systemctl reload php8.2-fpm
    
    exit 1
fi

echo "✅ Migration successful!"
echo "🗑️  Old database ${CURRENT_DB} can be dropped after verification period"
```

### 9.4 Livewire Version Upgrade

```bash
#!/bin/bash
# upgrade-livewire.sh

set -e

echo "📦 Upgrading Livewire..."

# 1. Backup current version
CURRENT_VERSION=$(composer show livewire/livewire --format=json | jq -r '.versions[0]')
echo "Current version: ${CURRENT_VERSION}"

# 2. Create git branch
git checkout -b upgrade-livewire-3

# 3. Update composer.json
composer require livewire/livewire:^3.0

# 4. Run automated fixes
php artisan livewire:upgrade

# 5. Manual changes checklist
echo "
⚠️  Manual changes required:

1. Replace @livewireStyles with @livewireScripts in layout
2. Update wire:key to use new syntax
3. Replace \$emitTo with \$dispatch
4. Update lifecycle hooks (booted instead of mount for some cases)
5. Review breaking changes: https://livewire.laravel.com/docs/upgrading

Run tests after changes:
./vendor/bin/pest
"

# 6. Run tests
./vendor/bin/pest

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please fix before proceeding."
    exit 1
fi

echo "✅ Upgrade completed. Review changes and commit."
```

### 9.5 Rollback Strategy

```bash
#!/bin/bash
# rollback.sh

set -e

ROLLBACK_TO=${1:-"previous"}

echo "🔙 Rolling back to ${ROLLBACK_TO}..."

# 1. Git rollback
if [ "$ROLLBACK_TO" == "previous" ]; then
    git reset --hard HEAD^
else
    git reset --hard $ROLLBACK_TO
fi

# 2. Reinstall dependencies
composer install --no-dev --optimize-autoloader
npm ci && npm run build

# 3. Rollback database
LAST_BATCH=$(php artisan migrate:status --format=json | jq -r '.[0].batch')
php artisan migrate:rollback --batch=$LAST_BATCH

# 4. Clear caches
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# 5. Rebuild caches
php artisan config:cache
php artisan route:cache
php artisan view:cache

# 6. Restart services
php artisan queue:restart
sudo systemctl reload php8.2-fpm

# 7. Health check
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health)

if [ "$HEALTH_STATUS" == "200" ]; then
    echo "✅ Rollback successful!"
else
    echo "❌ Rollback failed. Manual intervention required."
    exit 1
fi
```

---

## Projet 1 : Production-Ready SaaS Platform

**Objectif :** Plateforme SaaS complète production-ready

**Stack DevOps :**

- Docker multi-stage optimisé
- CI/CD GitHub Actions (tests, security, deploy)
- Zero-downtime deployment (blue-green)
- Monitoring complet (Pulse, Sentry, custom metrics)
- i18n (FR/EN/ES)
- a11y WCAG 2.1 AA compliant
- PWA avec offline support

**Code disponible repository.**

---

## Projet 2 : E-commerce Progressive Web App

**Objectif :** E-commerce PWA haute performance

**Features :**

- Service worker caching strategies
- Offline cart (IndexedDB)
- Background sync orders
- Push notifications
- Install prompt
- i18n multi-devises
- a11y keyboard navigation
- Performance budgets (<2s TTI)

**Code disponible repository.**

---

## Projet 3 : DevOps Automation Suite

**Objectif :** Suite automation déploiement

**Tools :**

- Deployer scripts (blue-green, canary, rolling)
- Health check monitoring
- Automated rollback
- Database migration safe
- Feature flags system
- Metrics dashboard
- Alert system (Slack/Email)

**Code disponible repository.**

---

## Checklist Module XV

- [ ] Docker multi-stage configuré
- [ ] CI/CD pipeline tests automatiques
- [ ] Zero-downtime deployment strategy
- [ ] Monitoring APM activé (Pulse/Sentry)
- [ ] Custom metrics tracking
- [ ] Health checks endpoint
- [ ] i18n multi-langues configuré
- [ ] Locale middleware actif
- [ ] a11y ARIA attributes
- [ ] Keyboard navigation support
- [ ] Screen reader compatible
- [ ] Service worker configured
- [ ] Manifest.json PWA
- [ ] Offline support implemented
- [ ] Install prompt functional
- [ ] Debugbar/Ray debugging tools
- [ ] Query profiling activé
- [ ] Feature flags système
- [ ] Migration strategies safe
- [ ] Rollback procedures documentées

**Concepts clés maîtrisés :**

✅ Docker containerization production
✅ CI/CD automation complète
✅ Zero-downtime deployment
✅ Monitoring et observability 360°
✅ Internationalization complète
✅ Accessibility WCAG compliant
✅ Progressive Web App
✅ Advanced troubleshooting
✅ Migration strategies safe
✅ Production best practices

---

**Module XV terminé ! 🎉**

**🏆 FORMATION LIVEWIRE COMPLÈTE - 15 MODULES TERMINÉS ! 🏆**

**FÉLICITATIONS ! Tu as maintenant une formation Livewire EXHAUSTIVE, PROFESSIONNELLE et PRODUCTION-READY couvrant :**

✅ **Fondamentaux** (Modules I-III)
✅ **Concepts avancés** (Modules IV-VI)
✅ **Features essentielles** (Modules VII-IX)
✅ **Real-time & Testing** (Modules X-XI)
✅ **Sécurité & Performance** (Modules XII-XIII)
✅ **Architecture & DevOps** (Modules XIV-XV)

**Tu maîtrises maintenant Livewire du niveau débutant au niveau expert production avec DevOps !** 🚀

Veux-tu que je crée :

- **Index final complet** de toute la formation ?
- **Cheat sheets** condensées ?
- **Quick reference guide** ?

Dis-moi ce que tu préfères ! 💪