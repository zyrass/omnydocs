---
description: "Déploiement de l'application Breeze sur un VPS Linux : configuration Nginx, PHP-FPM, SSL Let's Encrypt et automatisation Git."
icon: lucide/book-open-check
tags: ["LARAVEL", "BREEZE", "PROJET GUIDÉ"]
---

# Phase 7 — Déploiement Production

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Laravel 11"
  data-time="~1 heure">
</div>

## Objectifs de la Phase 7

!!! info "Ce que vous allez faire"
    - Configurer un VPS Ubuntu 24.04 (Nginx + PHP 8.3 + MySQL)
    - Cloner et configurer le projet Laravel en production
    - Configurer un Virtual Host Nginx pour le domaine
    - Générer un certificat SSL avec Let's Encrypt (Certbot)
    - Automatiser les déploiements via Git (optional)

## 1. Serveur — Dépendances

```bash title="Sur le VPS — Installation LEMP"
# Mise à jour et dépendances
sudo apt update && sudo apt upgrade -y
sudo apt install -y nginx mysql-server php8.3-fpm php8.3-cli     php8.3-mbstring php8.3-xml php8.3-curl php8.3-pdo php8.3-mysql     composer git unzip certbot python3-certbot-nginx
```

## 2. Configuration Nginx

```nginx title="/etc/nginx/sites-available/projet-breeze"
server {
    listen 80;
    server_name mondomaine.com www.mondomaine.com;
    root /var/www/projet-breeze/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/projet-breeze /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# SSL avec Let's Encrypt
sudo certbot --nginx -d mondomaine.com -d www.mondomaine.com
```

## 3. Déploiement du Code

```bash title="Sur le VPS — Premier déploiement"
cd /var/www
git clone https://github.com/username/projet-breeze.git
cd projet-breeze

composer install --no-dev --optimize-autoloader
cp .env.example .env
php artisan key:generate

# Configurer .env avec les variables de production
nano .env

php artisan migrate --force
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Permissions
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
```

!!! warning "Variables d'environnement en production"
    - `APP_ENV=production`
    - `APP_DEBUG=false`
    - Configurer `MAIL_*` pour les emails de réinitialisation de mot de passe


<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le déploiement n'est pas la fin du projet — c'est le début de la responsabilité de production. Les commandes `config:cache`, `route:cache` et `view:cache` sont les trois optimisations essentielles à exécuter sur chaque déploiement Laravel en production. Elles peuvent réduire le temps de réponse de 30 à 50% en éliminant les recalculs à chaque requête.

> [Conclusion du projet Breeze →](./conclusion.md)
