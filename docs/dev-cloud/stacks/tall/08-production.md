---
description: "Module 9 : Étape 4 - Déploiement en Production. Optimisation Laravel, configuration serveur Nginx + PHP-FPM, migration SQLite vers MySQL/PostgreSQL, monitoring, backup/restore, et déploiement automatisé avec rollback."
icon: lucide/book-open-check
tags: ["TALL", "PRODUCTION", "DEPLOYMENT", "NGINX", "MYSQL", "OPTIMIZATION", "MONITORING", "BACKUP"]
---

# Production

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="120-150 minutes">
</div>

## Introduction

Après avoir maîtrisé les **trois architectures réactives** (Livewire Module 6, Alpine Module 7, Hybride Module 8), il est temps de franchir l'**étape finale critique** : déployer votre application en production. Ce module transforme votre **application de développement** en **système production-ready** capable de servir des milliers d'utilisateurs avec performance, sécurité et fiabilité.

Imaginez que vous avez construit une voiture de course (Modules 1-8) : moteur puissant (Stack TALL), châssis solide (architecture hybride), design élégant (Tailwind CSS). Maintenant, le Module 9 est l'**homologation pour la route** : contrôle technique (optimisations), équipements obligatoires (sécurité), assurance (backup), carte grise (configuration serveur). **Sans cette étape, votre voiture reste dans le garage.**

**Qu'est-ce que le déploiement en production change concrètement ?**

En développement (Modules 1-8), vous aviez :
- SQLite (fichier unique, mono-utilisateur)
- `php artisan serve` (serveur dev, 1 requête/fois)
- Debug activé (erreurs détaillées visibles)
- Assets non minifiés (~3MB Tailwind CSS)
- Aucune sauvegarde, aucun monitoring

En production (Module 9), **transformation complète** :
- **MySQL/PostgreSQL** (serveur BDD, multi-utilisateurs, transactions)
- **Nginx + PHP-FPM** (serveur web pro, 100+ requêtes simultanées)
- **Debug désactivé** (pages d'erreur génériques, logs sécurisés)
- **Assets optimisés** (~10KB Tailwind CSS purgé et minifié)
- **Backup automatique**, **monitoring 24/7**, **rollback rapide**

Ce module vous guidera pas à pas pour :

- **Optimiser Laravel** : Cache config/routes/vues, autoloader optimisé
- **Configurer Nginx** : Reverse proxy, compression gzip, HTTPS, cache headers
- **Tuner PHP-FPM** : Workers, memory limits, OPcache, performance
- **Compiler assets** : Vite build production, Tailwind purge CSS, minification
- **Migrer vers MySQL** : Remplacement SQLite, migration données, configuration
- **Implémenter monitoring** : Logs Laravel, erreurs, alertes, métriques
- **Automatiser backup** : Scripts sauvegarde BDD, restauration, cron
- **Déployer avec Git** : Workflow production, rollback, zero-downtime

!!! quote "Principe du Module 9"
    "Une application non déployée est une application qui n'existe pas. Le déploiement en production est la validation ultime de votre maîtrise de la Stack TALL."

---

## Objectifs d'Apprentissage

À la fin de ce module, **vous serez capable de** :

### Objectifs Techniques

- [ ] Configurer Laravel pour la production (APP_ENV, APP_DEBUG, APP_KEY)
- [ ] Optimiser Laravel avec cache (config, routes, vues, autoloader)
- [ ] Installer et configurer Nginx comme reverse proxy
- [ ] Configurer PHP-FPM pour performance optimale
- [ ] Compiler assets avec Vite (build production)
- [ ] Purger Tailwind CSS (~10KB au lieu de 3MB)
- [ ] Migrer de SQLite vers MySQL/MariaDB
- [ ] Configurer les logs Laravel (daily, syslog, stack)
- [ ] Implémenter backup automatique BDD avec cron
- [ ] Créer script de déploiement avec rollback
- [ ] Configurer HTTPS avec Let's Encrypt (optionnel)

### Objectifs Conceptuels

- [ ] Comprendre différences dev vs production
- [ ] Visualiser architecture serveur web (Nginx → PHP-FPM → Laravel)
- [ ] Maîtriser le cycle de déploiement (build, migrate, deploy, rollback)
- [ ] Saisir importance optimisations (cache, OPcache, assets)
- [ ] Comprendre stratégies backup (full, incrémental, fréquence)
- [ ] Anticiper les pannes et préparer recovery
- [ ] Comparer SQLite vs MySQL en production
- [ ] Choisir stack infrastructure selon trafic/budget

---

## Prérequis

Avant de commencer ce module, **assurez-vous d'avoir** :

- [ ] **Modules 1-8 complétés** : Application TALL Stack fonctionnelle
- [ ] **Serveur Linux** : Ubuntu 22.04+ ou Debian 11+ (VPS, Cloud, ou VM locale)
- [ ] **Accès SSH** : Connexion root ou sudo au serveur
- [ ] **Nom de domaine** : Optionnel mais recommandé (ex: tall-tasks.com)
- [ ] **Connaissances Linux de base** : Commandes bash, fichiers config, permissions
- [ ] **120-150 minutes** devant vous sans interruption

!!! warning "Serveur Linux Requis"
    **Ce module nécessite un serveur Linux**. Options :
    
    - **VPS Cloud** : DigitalOcean ($6/mois), Linode, Vultr, AWS Lightsail
    - **Serveur dédié** : OVH, Hetzner
    - **VM locale** : VirtualBox, VMware avec Ubuntu Server
    
    **Configuration minimale** : 1 CPU, 1GB RAM, 10GB disque

!!! danger "Commandes Destructrices"
    **Certaines commandes sont DESTRUCTRICES** (suppriment données, redémarrent services). **Lisez attentivement** avant d'exécuter. **Testez d'abord sur VM** avant serveur production réel.

---

## Comprendre Avant d'Agir : Architecture Production

Avant de déployer, comprenons **l'architecture complète** d'un serveur web production.

### Architecture Dev vs Production

**Tableau comparatif détaillé :**

| Composant | Développement | Production | Raison |
|-----------|--------------|------------|--------|
| **Serveur web** | `php artisan serve` | **Nginx** | Performance, concurrence, HTTPS |
| **PHP** | CLI intégré | **PHP-FPM** | Processus workers, gestion mémoire |
| **Base de données** | SQLite (fichier) | **MySQL/PostgreSQL** | Multi-utilisateurs, transactions, performance |
| **Assets** | CDN Tailwind (~3MB) | **Compilés Vite (~10KB)** | Bande passante, vitesse chargement |
| **Cache** | ❌ Aucun | **Config, Routes, Vues** | Réduction temps réponse 50-80% |
| **Debug** | `APP_DEBUG=true` | **`APP_DEBUG=false`** | Sécurité (masquer erreurs internes) |
| **Logs** | Console | **Fichiers + Rotation** | Persistance, analyse, alertes |
| **Backup** | ❌ Aucun | **Automatisé quotidien** | Recovery après panne/erreur |
| **Monitoring** | ❌ Aucun | **Logs + Alertes** | Détection incidents temps réel |
| **Déploiement** | Git pull | **Script automatisé** | Cohérence, rollback, zero-downtime |

### Diagramme Architecture Serveur Production

Ce diagramme montre **comment une requête traverse l'infrastructure** en production.

**Comment lire ce diagramme ?**

- Les **rectangles** représentent les composants serveur
- Les **flèches pleines** montrent le flux de requête
- Les **chiffres** indiquent l'ordre d'exécution

```mermaid
---
config:
    theme: 'base'
---
flowchart LR
    User[Utilisateur<br/>navigateur] -->|1. HTTPS request<br/>tall-tasks.com| Nginx[Nginx<br/>:443]
    
    Nginx -->|2. Reverse proxy<br/>127.0.0.1:9000| FPM[PHP-FPM<br/>Workers pool]
    
    FPM -->|3. Execute| Laravel[Laravel<br/>Application]
    
    Laravel -->|4a. Read cache| Cache[(Config/Routes<br/>Cache)]
    Laravel -->|4b. Query| MySQL[(MySQL<br/>Database)]
    Laravel -->|4c. Log| Logs[/var/log/nginx<br/>/var/log/php-fpm<br/>storage/logs]
    
    Laravel -->|5. Response HTML| FPM
    FPM -->|6. Return| Nginx
    Nginx -->|7. HTTPS response<br/>+ gzip| User
    
    Backup[Backup Script<br/>cron daily] -.->|Dump| MySQL
    Monitor[Monitoring<br/>Logs analysis] -.->|Read| Logs

    style User fill:#e3f3e3
    style Nginx fill:#e3e3f3
    style FPM fill:#f3e3e3
    style Laravel fill:#e3f3e3
    style MySQL fill:#e3f3e3
    style Cache fill:#f3f3e3
    style Logs fill:#e3e3f3
    style Backup fill:#fff3e3
    style Monitor fill:#fff3e3
```

<small>*Ce diagramme illustre le flux complet requête/réponse en production. Étape 1 : L'utilisateur envoie requête HTTPS vers tall-tasks.com:443. Étape 2 : Nginx (reverse proxy) transfère vers PHP-FPM sur port 9000. Étape 3 : PHP-FPM exécute Laravel dans worker pool (plusieurs processus). Étape 4 : Laravel lit cache config/routes (performance), query MySQL (données), écrit logs (monitoring). Étape 5-7 : Laravel retourne HTML → PHP-FPM → Nginx (compression gzip) → Utilisateur. En parallèle : Script backup quotidien dump MySQL, système monitoring analyse logs pour alertes.*</small>

### Pourquoi Nginx + PHP-FPM ?

**Tableau comparatif serveurs web :**

| Serveur | Avantages | Inconvénients | Usage |
|---------|-----------|---------------|-------|
| **php artisan serve** | Simple, rapide setup dev | ❌ 1 requête/fois, pas HTTPS, pas production | Développement uniquement |
| **Apache + mod_php** | Historique, compatible | ⚠️ Lourd, consommation mémoire | Legacy, hébergement partagé |
| **Nginx + PHP-FPM** | ✅ Performance, léger, scalable | Setup initial complexe | **Production moderne** |
| **Caddy** | HTTPS auto, simple config | Moins mature, communauté petite | Projets personnels |

!!! tip "Nginx + PHP-FPM = Standard Industrie"
    **90% des applications Laravel en production** utilisent Nginx + PHP-FPM car :
    
    - **Performance** : Gère 10 000+ connexions simultanées
    - **Légèreté** : ~10MB RAM vs ~50MB Apache
    - **Flexibilité** : Reverse proxy, load balancer, cache
    - **Scalabilité** : Horizontal scaling facile

---

## Phase 1 — Optimisations Laravel (Étapes 1 à 4)

### Étape 1 : Configuration Environnement Production

Commençons par configurer **l'environnement Laravel pour la production**.

**Fichier :** `.env` (production)

```bash
# ENVIRONNEMENT
APP_NAME="TALL Tasks"
APP_ENV=production          # ✅ production (pas local)
APP_KEY=base64:VOTRE_CLE    # ✅ Générée avec php artisan key:generate
APP_DEBUG=false             # ✅ CRITIQUE : false en production (sécurité)
APP_URL=https://tall-tasks.com  # ✅ URL production avec HTTPS

# LOGS
LOG_CHANNEL=daily           # ✅ Rotation quotidienne (pas stack)
LOG_LEVEL=error             # ✅ Seulement erreurs (pas debug/info)
LOG_DEPRECATIONS_CHANNEL=null  # ✅ Désactiver warnings deprecated

# BASE DE DONNÉES (MySQL en production)
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=tall_tasks_prod
DB_USERNAME=tall_tasks_user
DB_PASSWORD=MOT_DE_PASSE_FORT_SECURISE

# CACHE (Redis recommandé si disponible, sinon file)
CACHE_DRIVER=file
SESSION_DRIVER=file
QUEUE_CONNECTION=sync

# AUTRES
BROADCAST_DRIVER=log
FILESYSTEM_DISK=local
```

!!! danger "APP_DEBUG=false EST CRITIQUE"
    **`APP_DEBUG=true` en production est une FAILLE DE SÉCURITÉ MAJEURE**.
    
    **Pourquoi ?**
    
    - Expose chemins serveur : `/var/www/html/app/Models/User.php`
    - Expose clés API, mots de passe BDD dans stack traces
    - Expose structure application (modèles, contrôleurs)
    - Donne informations précieuses aux attaquants
    
    **TOUJOURS `APP_DEBUG=false` en production.**

**Vérifier la configuration :**

```bash
# Vérifier que APP_DEBUG est false
php artisan tinker
>>> config('app.debug')
=> false  # ✅ Correct

# Vérifier que APP_ENV est production
>>> config('app.env')
=> "production"  # ✅ Correct
```

---

### Étape 2 : Cache des Configurations

**Pourquoi cacher les configurations ?**

Laravel charge **~50 fichiers PHP** (config/*.php) à chaque requête en dev.
Le cache config **compile tout en 1 fichier** → **Gain 50-80% performance**.

**Générer le cache config :**

```bash
# Générer le cache de configuration
php artisan config:cache

# Résultat attendu :
# Configuration cache cleared successfully.
# Configuration cached successfully.
```

**Ce qui se passe :**

1. Laravel lit tous les fichiers `config/*.php`
2. Compile en un seul fichier `bootstrap/cache/config.php`
3. Toutes les requêtes lisent **ce fichier unique** (ultra rapide)

**Fichier généré :** `bootstrap/cache/config.php`

```php
<?php return array (
  'app' => array (
    'name' => 'TALL Tasks',
    'env' => 'production',
    'debug' => false,
    // ... toute la config compilée en 1 fichier
  ),
  'database' => array ( /* ... */ ),
  'cache' => array ( /* ... */ ),
  // ...
);
```

!!! warning "Modifier .env Nécessite Rebuild Cache"
    **Après modification du `.env`**, vous **DEVEZ** reconstruire le cache :
    
    ```bash
    php artisan config:clear   # Supprimer cache
    php artisan config:cache   # Régénérer cache
    ```
    
    **Sinon**, Laravel continue d'utiliser l'ancienne config cachée.

---

### Étape 3 : Cache des Routes et Vues

**Cache des routes :**

```bash
# Générer le cache des routes
php artisan route:cache

# Résultat attendu :
# Routes cached successfully.
```

**Gain de performance :**

- **Sans cache** : Laravel parse `routes/web.php`, `routes/api.php` à chaque requête
- **Avec cache** : Laravel lit `bootstrap/cache/routes-v7.php` (fichier compilé)

**Cache des vues Blade :**

```bash
# Générer le cache des vues
php artisan view:cache

# Résultat attendu :
# Blade templates cached successfully.
```

**Gain de performance :**

- **Sans cache** : Blade compile `.blade.php` → PHP à chaque modification
- **Avec cache** : Blade utilise fichiers compilés `storage/framework/views/*.php`

!!! tip "Commande All-in-One"
    **Optimiser tout en une commande** :
    
    ```bash
    php artisan optimize
    
    # Équivaut à :
    # php artisan config:cache
    # php artisan route:cache
    # php artisan view:cache
    ```

---

### Étape 4 : Optimiser l'Autoloader Composer

**Pourquoi optimiser l'autoloader ?**

Composer génère **une map de classes** pour accélérer le chargement.

**Optimiser l'autoloader :**

```bash
# Générer l'autoloader optimisé (production)
composer install --optimize-autoloader --no-dev

# Options expliquées :
# --optimize-autoloader : Génère classmap optimisée
# --no-dev : N'installe pas les dépendances dev (phpunit, etc.)
```

**Gain de performance :**

- **Sans optimisation** : Composer cherche fichiers dynamiquement (lent)
- **Avec optimisation** : Composer a une map directe classe → fichier (rapide)

!!! info "Différence dev vs production"
    **En développement** :
    
    ```bash
    composer install  # Installe tout (dev + prod)
    ```
    
    **En production** :
    
    ```bash
    composer install --optimize-autoloader --no-dev
    ```

**Vérifier les gains :**

```bash
# Tester temps de réponse AVANT optimisations
time php artisan route:list > /dev/null

# Optimiser
php artisan optimize
composer install --optimize-autoloader --no-dev

# Tester temps de réponse APRÈS optimisations
time php artisan route:list > /dev/null

# Gain typique : 50-80% plus rapide
```

> Ainsi s'achève la Phase 1 - Optimisations Laravel (Étapes 1-4)

---

## Phase 2 — Configuration Serveur Web (Étapes 5 à 7)

### Étape 5 : Installer Nginx et PHP-FPM

**Sur Ubuntu 22.04+ / Debian 11+ :**

```bash
# Mettre à jour les paquets
sudo apt update

# Installer Nginx
sudo apt install -y nginx

# Installer PHP 8.3 et extensions (ajuster version si nécessaire)
sudo apt install -y php8.3-fpm php8.3-mysql php8.3-mbstring \
    php8.3-xml php8.3-curl php8.3-zip php8.3-gd php8.3-bcmath

# Vérifier installations
nginx -v         # nginx version: nginx/1.22.x
php-fpm8.3 -v    # PHP 8.3.x (fpm-fcgi)
```

**Démarrer les services :**

```bash
# Démarrer et activer Nginx (auto-start au boot)
sudo systemctl start nginx
sudo systemctl enable nginx

# Démarrer et activer PHP-FPM
sudo systemctl start php8.3-fpm
sudo systemctl enable php8.3-fpm

# Vérifier statut
sudo systemctl status nginx
sudo systemctl status php8.3-fpm
```

!!! success "Services Installés"
    Si les commandes retournent "active (running)", les services sont opérationnels !

---

### Étape 6 : Configurer Nginx pour Laravel

Créons un **virtual host Nginx** pour l'application TALL Tasks.

**Fichier :** `/etc/nginx/sites-available/tall-tasks`

```nginx
# Virtual Host Nginx pour TALL Tasks (Production)
server {
    # Port d'écoute (HTTP)
    listen 80;
    listen [::]:80;

    # Nom de domaine (ajuster selon votre domaine)
    server_name tall-tasks.com www.tall-tasks.com;

    # Racine du site (dossier public de Laravel)
    root /var/www/tall-tasks/public;

    # Index par défaut
    index index.php index.html;

    # Charset
    charset utf-8;

    # Logs spécifiques à ce site
    access_log /var/log/nginx/tall-tasks-access.log;
    error_log /var/log/nginx/tall-tasks-error.log;

    # Règle principale : Tout passe par index.php (Laravel routing)
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # Bloquer accès aux fichiers cachés (.env, .git, etc.)
    location ~ /\. {
        deny all;
    }

    # Configuration PHP-FPM
    location ~ \.php$ {
        # Vérifier que le fichier existe (éviter injection)
        try_files $uri =404;

        # FastCGI params
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;

        # Timeouts (ajuster selon besoins)
        fastcgi_read_timeout 300;
        fastcgi_send_timeout 300;

        # Buffer sizes (optimisation)
        fastcgi_buffer_size 128k;
        fastcgi_buffers 4 256k;
        fastcgi_busy_buffers_size 256k;
    }

    # Compression gzip (réduire bande passante)
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss 
               application/rss+xml font/truetype font/opentype 
               application/vnd.ms-fontobject image/svg+xml;

    # Cache statique (images, CSS, JS)
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Sécurité headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
```

**Activer le site :**

```bash
# Créer lien symbolique vers sites-enabled
sudo ln -s /etc/nginx/sites-available/tall-tasks /etc/nginx/sites-enabled/

# Tester la configuration Nginx (IMPORTANT avant reload)
sudo nginx -t

# Résultat attendu :
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# Recharger Nginx (appliquer changements)
sudo systemctl reload nginx
```

!!! warning "Ajuster les Chemins"
    **Ajustez ces valeurs selon votre serveur** :
    
    - `server_name` : Votre domaine (tall-tasks.com)
    - `root` : Chemin vers `/public` de Laravel
    - `fastcgi_pass` : Socket PHP-FPM (vérifier version PHP)

---

### Étape 7 : Configurer PHP-FPM pour Performance

**Fichier :** `/etc/php/8.3/fpm/pool.d/www.conf`

```ini
; Pool PHP-FPM pour TALL Tasks (optimisé)

[www]
; Utilisateur/Groupe
user = www-data
group = www-data

; Socket (communication Nginx ↔ PHP-FPM)
listen = /var/run/php/php8.3-fpm.sock
listen.owner = www-data
listen.group = www-data
listen.mode = 0660

; Gestion des processus (CRITIQUE pour performance)
pm = dynamic                  ; Gestionnaire dynamique (recommandé)
pm.max_children = 20          ; Maximum 20 workers simultanés
pm.start_servers = 4          ; Démarrer avec 4 workers
pm.min_spare_servers = 2      ; Minimum 2 workers en attente
pm.max_spare_servers = 6      ; Maximum 6 workers en attente
pm.max_requests = 500         ; Recycler worker après 500 requêtes

; Timeouts
request_terminate_timeout = 300  ; Timeout requête (5 minutes)

; Logs
php_admin_value[error_log] = /var/log/php-fpm/www-error.log
php_admin_flag[log_errors] = on

; Limites mémoire (ajuster selon RAM disponible)
php_admin_value[memory_limit] = 256M
```

**Explication des valeurs `pm.*` :**

| Paramètre | Valeur | Explication |
|-----------|--------|-------------|
| `pm.max_children` | 20 | Maximum 20 requêtes PHP simultanées |
| `pm.start_servers` | 4 | 4 workers prêts au démarrage |
| `pm.min_spare_servers` | 2 | Toujours 2 workers disponibles minimum |
| `pm.max_spare_servers` | 6 | Maximum 6 workers en attente (pas plus) |
| `pm.max_requests` | 500 | Recycler worker après 500 requêtes (éviter memory leaks) |

!!! tip "Calculer pm.max_children"
    **Formule :**
    
    ```
    pm.max_children = RAM_disponible / Mémoire_par_worker
    ```
    
    **Exemple :**
    
    - Serveur 2GB RAM
    - Système + MySQL = ~500MB
    - RAM disponible PHP = 1.5GB = 1500MB
    - Mémoire par worker = ~50MB (Laravel moyen)
    - **pm.max_children = 1500 / 50 = 30**

**Activer les changements :**

```bash
# Redémarrer PHP-FPM
sudo systemctl restart php8.3-fpm

# Vérifier statut
sudo systemctl status php8.3-fpm
```

---

### Étape 8 : Activer OPcache (Performance PHP)

**OPcache** cache le bytecode PHP compilé → **Gain 30-50% performance**.

**Fichier :** `/etc/php/8.3/fpm/conf.d/10-opcache.ini`

```ini
; Configuration OPcache pour production

; Activer OPcache
opcache.enable=1
opcache.enable_cli=0  ; Désactiver pour CLI (artisan)

; Mémoire allouée (ajuster selon RAM)
opcache.memory_consumption=256
opcache.interned_strings_buffer=16
opcache.max_accelerated_files=10000

; Validation (optimisation production)
opcache.validate_timestamps=0  ; Ne PAS revalider fichiers (performance)
opcache.revalidate_freq=0      ; Fréquence revalidation (0 = jamais)

; Performance
opcache.fast_shutdown=1
opcache.enable_file_override=1

; Optimisations
opcache.optimization_level=0x7FFFFFFF
```

!!! danger "validate_timestamps=0 en Production"
    **`opcache.validate_timestamps=0`** signifie que PHP **ne vérifie JAMAIS** si fichiers ont changé.
    
    **Avantage** : Performance maximale (pas de stat() sur fichiers)
    **Inconvénient** : Après déploiement, **VOUS DEVEZ** vider le cache OPcache
    
    ```bash
    sudo systemctl reload php8.3-fpm  # Recharger pour vider OPcache
    ```

**Vérifier OPcache :**

```bash
# Vérifier que OPcache est activé
php -r "echo opcache_get_status()['opcache_enabled'] ? 'Enabled' : 'Disabled';"

# Résultat attendu : Enabled
```

> Ainsi s'achève la Phase 2 - Configuration Serveur Web (Étapes 5-8)

---

## Phase 3 — Compilation Assets Production (Étapes 9 à 10)

### Étape 9 : Installer Node.js et Dépendances

**Installer Node.js 20 LTS (via NVM) :**

```bash
# Installer NVM (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Recharger shell
source ~/.bashrc

# Installer Node.js 20 LTS
nvm install 20
nvm use 20

# Vérifier versions
node -v   # v20.x.x
npm -v    # 10.x.x
```

**Installer dépendances NPM :**

```bash
# Naviguer vers le projet
cd /var/www/tall-tasks

# Installer dépendances (package.json)
npm install

# Résultat attendu :
# added XXX packages in Xs
```

---

### Étape 10 : Build Production avec Vite

**Pourquoi un build production ?**

| Aspect | Développement (CDN) | Production (Build) |
|--------|:-------------------:|:------------------:|
| **Tailwind CSS** | ~3MB (toutes classes) | **~10KB** (classes utilisées) |
| **JavaScript** | Non minifié | **Minifié + uglify** |
| **Fichiers** | Multiples (app.js, app.css) | **1 fichier versioned** (app.abc123.js) |
| **Cache** | Pas de cache | **Cache navigateur 1 an** |
| **Performance** | ⚠️ Lent (3MB+ à charger) | ✅ **Rapide (10KB)** |

**Configurer Tailwind pour purge CSS :**

**Fichier :** `tailwind.config.js`

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  // Fichiers à scanner pour classes utilisées
  content: [
    "./resources/**/*.blade.php",
    "./resources/**/*.js",
    "./resources/**/*.vue",
    "./app/Livewire/**/*.php",  // Composants Livewire
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Compiler les assets pour production :**

```bash
# Build production avec Vite
npm run build

# Résultat attendu :
# vite v5.x.x building for production...
# ✓ XXX modules transformed.
# dist/assets/app-abc123.js    15.42 kB │ gzip: 5.12 kB
# dist/assets/app-def456.css   8.73 kB  │ gzip: 2.34 kB
# ✓ built in 2.45s
```

**Ce qui se passe :**

1. **Tailwind CSS** : Scanne tous les fichiers `.blade.php`, `.js`, `.php`
2. **Purge** : Garde UNIQUEMENT les classes utilisées (ex: `bg-blue-600`, `text-white`)
3. **Minification** : Supprime espaces, commentaires, raccourcit noms variables
4. **Versioning** : Ajoute hash au nom fichier (`app.abc123.js`) pour cache-busting
5. **Génération** : Crée fichiers dans `public/build/`

**Fichiers générés :**

```
public/build/
├── assets/
│   ├── app-abc123.js       # JavaScript minifié + versioned
│   ├── app-def456.css      # CSS puré + minifié + versioned
│   └── livewire-ghi789.js  # Livewire assets
└── manifest.json           # Mapping fichiers sources → compilés
```

**Modifier le layout pour utiliser assets compilés :**

**Fichier :** `resources/views/layouts/app.blade.php`

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    
    <title>@yield('title', 'TALL Tasks - Gestion de Tâches')</title>
    
    {{-- 
        DÉVELOPPEMENT : CDN Tailwind (~3MB)
        <script src="https://cdn.tailwindcss.com"></script>
    --}}
    
    {{-- 
        PRODUCTION : Assets compilés Vite (~10KB)
        @vite génère automatiquement les balises <link> et <script>
    --}}
    @vite(['resources/css/app.css', 'resources/js/app.js'])
    
    @livewireStyles
    
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <!-- Contenu -->
    
    @livewireScripts
</body>
</html>
```

**Vérifier les assets compilés :**

```bash
# Vérifier taille CSS compilé
ls -lh public/build/assets/*.css

# Résultat attendu : ~10KB au lieu de 3MB
# -rw-r--r-- 1 www-data www-data 8.7K Dec 08 15:30 app-def456.css
```

!!! success "Assets Optimisés"
    Si la taille CSS est **~10KB** (au lieu de 3MB), le purge Tailwind fonctionne correctement !

> Ainsi s'achève la Phase 3 - Compilation Assets Production (Étapes 9-10)

---

## Phase 4 — Migration SQLite → MySQL (Étapes 11 à 13)

### Étape 11 : Installer MySQL/MariaDB

**Installer MariaDB (fork open-source MySQL) :**

```bash
# Installer MariaDB Server
sudo apt install -y mariadb-server mariadb-client

# Démarrer et activer MariaDB
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Sécuriser l'installation
sudo mariadb-secure-installation
```

**Réponses recommandées pour `mariadb-secure-installation` :**

```
Switch to unix_socket authentication? [Y/n] n
Change the root password? [Y/n] Y
  → Enter new password: MOT_DE_PASSE_ROOT_FORT
Remove anonymous users? [Y/n] Y
Disallow root login remotely? [Y/n] Y
Remove test database? [Y/n] Y
Reload privilege tables now? [Y/n] Y
```

---

### Étape 12 : Créer Base de Données et Utilisateur

**Connexion à MariaDB :**

```bash
# Connexion root
sudo mariadb -u root -p
# Enter password: (mot de passe défini à l'étape précédente)
```

**Créer BDD et utilisateur (SQL) :**

```sql
-- Créer la base de données
CREATE DATABASE tall_tasks_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Créer utilisateur dédié (PAS root en production)
CREATE USER 'tall_tasks_user'@'localhost' IDENTIFIED BY 'MOT_DE_PASSE_FORT_SECURISE';

-- Donner tous les privilèges sur la BDD
GRANT ALL PRIVILEGES ON tall_tasks_prod.* TO 'tall_tasks_user'@'localhost';

-- Appliquer les changements
FLUSH PRIVILEGES;

-- Vérifier
SHOW DATABASES;
-- Doit afficher : tall_tasks_prod

-- Quitter
EXIT;
```

!!! danger "Mot de Passe Sécurisé Obligatoire"
    **Utilisez un mot de passe FORT** (16+ caractères, alphanumérique + symboles).
    
    **Générer mot de passe aléatoire** :
    
    ```bash
    openssl rand -base64 32
    # Résultat : xK8vL9mN2qR4sT6wY8zA1bC3dE5fG7hI9jK0lM1nO2pQ3rS=
    ```

**Vérifier connexion utilisateur :**

```bash
# Tester connexion avec utilisateur dédié
mariadb -u tall_tasks_user -p tall_tasks_prod

# Enter password: (mot de passe créé ci-dessus)

# Si connexion réussie, vous voyez :
# MariaDB [tall_tasks_prod]>

# Quitter
EXIT;
```

---

### Étape 13 : Migrer Données SQLite → MySQL

**Mettre à jour `.env` pour MySQL :**

**Fichier :** `.env`

```bash
# BASE DE DONNÉES (MySQL en production)
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=tall_tasks_prod
DB_USERNAME=tall_tasks_user
DB_PASSWORD=MOT_DE_PASSE_FORT_SECURISE
```

**Exécuter les migrations :**

```bash
# Vérifier connexion MySQL
php artisan config:clear  # Vider cache config (lecture nouveau .env)
php artisan tinker
>>> DB::connection()->getPDO();
# Si pas d'erreur, connexion OK

# Exécuter migrations sur MySQL
php artisan migrate

# Résultat attendu :
#   INFO  Running migrations.
#
#   2014_10_12_000000_create_users_table ........ DONE
#   2014_10_12_100000_create_password_resets_table ... DONE
#   2019_08_19_000000_create_failed_jobs_table ... DONE
#   2019_12_14_000001_create_personal_access_tokens_table ... DONE
#   YYYY_MM_DD_XXXXXX_create_tasks_table ......... DONE
```

**Migrer données existantes (si nécessaire) :**

Si vous avez des **données dans SQLite** à migrer vers MySQL :

```bash
# Option 1 : Export SQLite → Import MySQL (manuel)

# 1. Exporter données SQLite en SQL
sqlite3 database/database.sqlite .dump > sqlite_dump.sql

# 2. Importer dans MySQL (nécessite conversion format)
# Note : Format SQLite ≠ MySQL, nécessite édition manuelle ou outil

# Option 2 : Utiliser package Laravel (recommandé)
# https://github.com/spatie/laravel-db-snapshots

# Option 3 : Recreate via seeders (si peu de données)
php artisan db:seed
```

!!! tip "Méthode Recommandée : Fresh Migration"
    Si vous êtes **encore en développement**, la méthode la plus simple :
    
    ```bash
    # Recréer toutes les tables (supprime données)
    php artisan migrate:fresh
    
    # Puis recréer données de test avec seeders
    php artisan db:seed
    ```

**Vérifier tables MySQL :**

```bash
# Connexion MySQL
mariadb -u tall_tasks_user -p tall_tasks_prod

# Lister tables
SHOW TABLES;

# Résultat attendu :
# +----------------------------+
# | Tables_in_tall_tasks_prod  |
# +----------------------------+
# | failed_jobs                |
# | migrations                 |
# | password_resets            |
# | personal_access_tokens     |
# | tasks                      |
# | users                      |
# +----------------------------+

# Vérifier structure table tasks
DESCRIBE tasks;

# Quitter
EXIT;
```

> Ainsi s'achève la Phase 4 - Migration SQLite → MySQL (Étapes 11-13)

---

## Phase 5 — Monitoring et Backup (Étapes 14 à 16)

### Étape 14 : Configuration Logs Laravel

**Fichier :** `config/logging.php` (vérifier)

```php
<?php

return [
    // Canal par défaut (défini dans .env)
    'default' => env('LOG_CHANNEL', 'daily'),

    'channels' => [
        // Logs quotidiens (recommandé production)
        'daily' => [
            'driver' => 'daily',
            'path' => storage_path('logs/laravel.log'),
            'level' => env('LOG_LEVEL', 'error'),  // Seulement erreurs
            'days' => 14,  // Conserver 14 jours
        ],

        // Logs simples (1 fichier, peut devenir énorme)
        'single' => [
            'driver' => 'single',
            'path' => storage_path('logs/laravel.log'),
            'level' => env('LOG_LEVEL', 'debug'),
        ],

        // Syslog (système Linux, recommandé pour centralisation)
        'syslog' => [
            'driver' => 'syslog',
            'level' => env('LOG_LEVEL', 'error'),
            'facility' => LOG_USER,
        ],
    ],
];
```

**Dans `.env` :**

```bash
LOG_CHANNEL=daily    # Rotation quotidienne
LOG_LEVEL=error      # Seulement erreurs (pas debug/info)
```

**Tester les logs :**

```php
// Dans n'importe quel contrôleur/composant
use Illuminate\Support\Facades\Log;

Log::error('Test erreur production', [
    'user_id' => auth()->id(),
    'context' => 'test_logging'
]);
```

**Vérifier le fichier log :**

```bash
# Voir dernières lignes du log
tail -f storage/logs/laravel.log

# Résultat attendu :
# [2024-12-08 15:45:32] production.ERROR: Test erreur production {"user_id":null,"context":"test_logging"}
```

---

### Étape 15 : Script Backup Automatisé

**Créer script backup BDD :**

**Fichier :** `/usr/local/bin/backup-tall-tasks.sh`

```bash
#!/bin/bash

# Script backup automatisé pour TALL Tasks
# Usage: /usr/local/bin/backup-tall-tasks.sh

# Configuration
DB_NAME="tall_tasks_prod"
DB_USER="tall_tasks_user"
DB_PASSWORD="MOT_DE_PASSE_FORT_SECURISE"  # ⚠️ Sécuriser ce fichier (chmod 700)
BACKUP_DIR="/var/backups/tall-tasks"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/tall_tasks_$DATE.sql.gz"

# Logs
LOG_FILE="$BACKUP_DIR/backup.log"

# Créer dossier backup si n'existe pas
mkdir -p "$BACKUP_DIR"

# Fonction log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Début backup
log "Début backup de $DB_NAME"

# Dump MySQL compressé
if mysqldump -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" | gzip > "$BACKUP_FILE"; then
    log "✅ Backup réussi : $BACKUP_FILE"
    
    # Taille du fichier
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log "   Taille : $SIZE"
    
    # Supprimer backups de plus de 30 jours
    find "$BACKUP_DIR" -name "tall_tasks_*.sql.gz" -mtime +30 -delete
    log "   Anciens backups supprimés (>30 jours)"
else
    log "❌ ERREUR backup $DB_NAME"
    exit 1
fi

log "Fin backup"
```

**Rendre le script exécutable :**

```bash
# Rendre exécutable
sudo chmod 700 /usr/local/bin/backup-tall-tasks.sh

# Propriétaire root (sécurité)
sudo chown root:root /usr/local/bin/backup-tall-tasks.sh

# Créer dossier backups
sudo mkdir -p /var/backups/tall-tasks
sudo chmod 700 /var/backups/tall-tasks
```

**Tester le script :**

```bash
# Exécuter manuellement
sudo /usr/local/bin/backup-tall-tasks.sh

# Vérifier backup créé
ls -lh /var/backups/tall-tasks/

# Résultat attendu :
# -rw-r--r-- 1 root root 2.4K Dec 08 16:00 tall_tasks_20241208_160000.sql.gz
```

---

### Étape 16 : Automatiser avec Cron

**Créer tâche cron (backup quotidien 3h du matin) :**

```bash
# Éditer crontab root
sudo crontab -e

# Ajouter cette ligne (backup quotidien 3h00)
0 3 * * * /usr/local/bin/backup-tall-tasks.sh >> /var/backups/tall-tasks/cron.log 2>&1

# Sauvegarder et quitter
```

**Explication syntaxe cron :**

```
0 3 * * *  /chemin/script.sh
│ │ │ │ │
│ │ │ │ └─── Jour semaine (0-7, 0=dimanche)
│ │ │ └───── Mois (1-12)
│ │ └─────── Jour mois (1-31)
│ └───────── Heure (0-23)
└─────────── Minute (0-59)

0 3 * * * = Tous les jours à 3h00
```

**Autres exemples cron :**

```bash
# Toutes les heures
0 * * * * /chemin/script.sh

# Toutes les 6 heures
0 */6 * * * /chemin/script.sh

# Tous les lundis 8h
0 8 * * 1 /chemin/script.sh

# Tous les 1er du mois minuit
0 0 1 * * /chemin/script.sh
```

**Vérifier tâches cron :**

```bash
# Lister tâches cron
sudo crontab -l

# Voir logs cron
tail -f /var/backups/tall-tasks/cron.log
```

**Script de restauration (optionnel) :**

**Fichier :** `/usr/local/bin/restore-tall-tasks.sh`

```bash
#!/bin/bash

# Script restauration backup TALL Tasks
# Usage: /usr/local/bin/restore-tall-tasks.sh /chemin/backup.sql.gz

if [ $# -eq 0 ]; then
    echo "Usage: $0 /chemin/backup.sql.gz"
    exit 1
fi

BACKUP_FILE=$1
DB_NAME="tall_tasks_prod"
DB_USER="tall_tasks_user"
DB_PASSWORD="MOT_DE_PASSE_FORT_SECURISE"

echo "⚠️  ATTENTION : Cette opération va ÉCRASER la base de données actuelle !"
echo "   Base de données : $DB_NAME"
echo "   Backup : $BACKUP_FILE"
read -p "Continuer ? (yes/no) " -r
if [[ ! $REPLY =~ ^yes$ ]]; then
    echo "Annulé."
    exit 0
fi

echo "Restauration en cours..."

# Décompresser et restaurer
if gunzip < "$BACKUP_FILE" | mysql -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME"; then
    echo "✅ Restauration réussie"
else
    echo "❌ ERREUR restauration"
    exit 1
fi
```

```bash
# Rendre exécutable
sudo chmod 700 /usr/local/bin/restore-tall-tasks.sh

# Utilisation
sudo /usr/local/bin/restore-tall-tasks.sh /var/backups/tall-tasks/tall_tasks_20241208_160000.sql.gz
```

> Ainsi s'achève la Phase 5 - Monitoring et Backup (Étapes 14-16)

---

## Phase 6 — Déploiement Automatisé (Étapes 17 à 18)

### Étape 17 : Script de Déploiement

**Créer script déploiement automatisé :**

**Fichier :** `/var/www/tall-tasks/deploy.sh`

```bash
#!/bin/bash

# Script déploiement TALL Tasks (production)
# Usage: ./deploy.sh

set -e  # Arrêter sur première erreur

# Configuration
PROJECT_DIR="/var/www/tall-tasks"
GIT_BRANCH="main"

# Couleurs output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction log
log() {
    echo -e "${GREEN}[DEPLOY]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Début déploiement
log "Début déploiement TALL Tasks"
log "==========================================="

# 1. Activer mode maintenance
log "Étape 1/10 : Activation mode maintenance"
php artisan down || warn "Mode maintenance déjà actif"

# 2. Git pull
log "Étape 2/10 : Mise à jour code (Git)"
git fetch origin
git reset --hard origin/$GIT_BRANCH || error "Git pull échoué"

# 3. Composer install
log "Étape 3/10 : Installation dépendances Composer"
composer install --optimize-autoloader --no-dev || error "Composer install échoué"

# 4. NPM install et build
log "Étape 4/10 : Installation dépendances NPM"
npm install || error "NPM install échoué"

log "Étape 5/10 : Build assets production"
npm run build || error "NPM build échoué"

# 5. Migrations BDD
log "Étape 6/10 : Exécution migrations"
php artisan migrate --force || error "Migrations échouées"

# 6. Cache
log "Étape 7/10 : Optimisation Laravel"
php artisan config:clear
php artisan config:cache
php artisan route:clear
php artisan route:cache
php artisan view:clear
php artisan view:cache

# 7. Permissions
log "Étape 8/10 : Ajustement permissions"
chown -R www-data:www-data storage bootstrap/cache
chmod -R 775 storage bootstrap/cache

# 8. Redémarrage services
log "Étape 9/10 : Redémarrage PHP-FPM"
sudo systemctl reload php8.3-fpm || warn "Reload PHP-FPM échoué"

# 9. Désactiver mode maintenance
log "Étape 10/10 : Désactivation mode maintenance"
php artisan up

log "==========================================="
log "✅ Déploiement terminé avec succès !"
log "   URL : https://tall-tasks.com"
```

**Rendre exécutable :**

```bash
# Rendre exécutable
chmod +x /var/www/tall-tasks/deploy.sh

# Propriétaire www-data
sudo chown www-data:www-data /var/www/tall-tasks/deploy.sh

# Exécuter déploiement
cd /var/www/tall-tasks
./deploy.sh
```

---

### Étape 18 : Script Rollback

**Créer script rollback (annuler déploiement) :**

**Fichier :** `/var/www/tall-tasks/rollback.sh`

```bash
#!/bin/bash

# Script rollback TALL Tasks
# Usage: ./rollback.sh

set -e

# Configuration
PROJECT_DIR="/var/www/tall-tasks"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[ROLLBACK]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

log "Début rollback"
log "================================"

# 1. Mode maintenance
log "Étape 1/6 : Activation mode maintenance"
php artisan down

# 2. Git rollback (commit précédent)
log "Étape 2/6 : Rollback Git (commit précédent)"
git reset --hard HEAD~1 || error "Git rollback échoué"

# 3. Composer install
log "Étape 3/6 : Réinstallation dépendances"
composer install --optimize-autoloader --no-dev

# 4. Rollback migrations (1 batch)
log "Étape 4/6 : Rollback migrations"
php artisan migrate:rollback --step=1 --force || warn "Rollback migrations échoué"

# 5. Cache
log "Étape 5/6 : Rebuild cache"
php artisan config:cache
php artisan route:cache
php artisan view:cache

# 6. Désactiver mode maintenance
log "Étape 6/6 : Désactivation mode maintenance"
php artisan up

log "================================"
log "✅ Rollback terminé"
```

```bash
# Rendre exécutable
chmod +x /var/www/tall-tasks/rollback.sh

# Utilisation en cas de problème après déploiement
cd /var/www/tall-tasks
./rollback.sh
```

> Ainsi s'achève la Phase 6 - Déploiement Automatisé (Étapes 17-18)

---

## Le Mot de la Fin

### FÉLICITATIONS ! Votre application est production-ready.

!!! success "Application Déployée en Production"

**Compétences Techniques Acquises :**

- ✅ **Configuration production** : APP_ENV, APP_DEBUG, logs optimisés
- ✅ **Optimisations Laravel** : Cache config/routes/vues, autoloader
- ✅ **Nginx configuré** : Virtual host, gzip, cache statique, headers sécurité
- ✅ **PHP-FPM tuné** : Workers pool, OPcache, memory limits
- ✅ **Assets optimisés** : Vite build, Tailwind purge (~10KB), minification
- ✅ **MySQL en production** : Migration SQLite, BDD dédiée, utilisateur sécurisé
- ✅ **Monitoring** : Logs Laravel daily, rotation 14 jours
- ✅ **Backup automatisé** : Script quotidien cron, restauration
- ✅ **Déploiement** : Script automatisé, rollback, zero-downtime

**Compétences Conceptuelles Acquises :**

- ✅ **Architecture serveur** : Nginx → PHP-FPM → Laravel → MySQL
- ✅ **Différences dev/prod** : Debug, cache, assets, BDD
- ✅ **Optimisations critiques** : OPcache, purge CSS, cache config
- ✅ **Stratégies backup** : Quotidien, rétention 30 jours, restauration
- ✅ **Cycle déploiement** : Maintenance → Git → Composer → NPM → Migrate → Cache → Up
- ✅ **Recovery** : Rollback Git, migrations, cron backup
- ✅ **Sécurité** : APP_DEBUG=false, permissions, utilisateur BDD dédié
- ✅ **Scalabilité** : pm.max_children, OPcache, Nginx workers

### Points Clés à Retenir

Retenez ces **8 principes fondamentaux** du déploiement production :

1. **APP_DEBUG=false OBLIGATOIRE** : Sécurité critique (masquer stack traces)
2. **Cache TOUT** : Config, routes, vues, autoloader, OPcache (+50-80% performance)
3. **Nginx + PHP-FPM = Standard** : Performance, scalabilité, HTTPS
4. **Assets compilés Vite** : Purge Tailwind 3MB → 10KB (~300x plus léger)
5. **MySQL en production** : SQLite OK dev, MySQL/PostgreSQL obligatoire prod
6. **Backup quotidien automatisé** : Cron 3h, rétention 30 jours, script restore
7. **Logs rotatifs** : Daily channel, 14 jours, LOG_LEVEL=error
8. **Script déploiement** : Automatisation complète, rollback rapide

### Tableau Comparaison Avant/Après Module 9

| Aspect | Avant Module 9 (Dev) | Après Module 9 (Production) |
|--------|:--------------------:|:---------------------------:|
| **Serveur web** | php artisan serve | **Nginx + PHP-FPM** |
| **Base de données** | SQLite fichier | **MySQL serveur** |
| **Assets** | CDN Tailwind ~3MB | **Vite build ~10KB** |
| **Cache** | ❌ Aucun | **Config/Routes/Vues/OPcache** |
| **Debug** | APP_DEBUG=true | **APP_DEBUG=false** |
| **Logs** | Console | **Fichiers rotatifs 14j** |
| **Backup** | ❌ Aucun | **Cron quotidien 30j** |
| **Déploiement** | Git pull manuel | **Script automatisé** |
| **Performance** | ⚠️ Développement | ✅ **Optimale production** |
| **Sécurité** | ⚠️ Debug exposé | ✅ **Sécurisée** |

### Checklist Finale Avant Mise en Production

Avant de mettre votre application en ligne, **vérifiez TOUS ces points** :

**Configuration :**

- [ ] `APP_ENV=production` dans `.env`
- [ ] `APP_DEBUG=false` dans `.env`
- [ ] `APP_KEY` générée et unique
- [ ] `APP_URL` correcte (https://votre-domaine.com)
- [ ] `LOG_CHANNEL=daily` et `LOG_LEVEL=error`

**Base de Données :**

- [ ] MySQL/PostgreSQL installé et démarré
- [ ] BDD créée avec utilisateur dédié (pas root)
- [ ] `.env` configuré avec identifiants MySQL
- [ ] Migrations exécutées (`php artisan migrate`)
- [ ] Données migrées depuis SQLite (si nécessaire)

**Optimisations :**

- [ ] `php artisan optimize` exécuté
- [ ] `composer install --optimize-autoloader --no-dev`
- [ ] `npm run build` exécuté (assets compilés)
- [ ] OPcache activé (`opcache.enable=1`)
- [ ] Permissions correctes (`storage/` et `bootstrap/cache/` 775)

**Serveur :**

- [ ] Nginx installé et configuré
- [ ] PHP-FPM installé et configuré
- [ ] Virtual host Nginx créé et activé
- [ ] `nginx -t` passe (configuration valide)
- [ ] Services démarrés et activés (nginx, php-fpm, mysql)

**Backup & Monitoring :**

- [ ] Script backup créé et testé
- [ ] Cron backup configuré (quotidien 3h)
- [ ] Logs Laravel rotatifs (daily, 14j)
- [ ] Script restauration testé au moins une fois

**Sécurité :**

- [ ] `.env` dans `.gitignore` (ne PAS commiter)
- [ ] Permissions fichiers correctes (644 fichiers, 755 dossiers)
- [ ] Headers sécurité Nginx (X-Frame-Options, etc.)
- [ ] HTTPS configuré (optionnel mais recommandé)

**Tests :**

- [ ] Application accessible via domaine
- [ ] Créer/Modifier/Supprimer tâche fonctionne
- [ ] Logs écrits dans `storage/logs/`
- [ ] Assets chargent correctement (pas d'erreurs 404)
- [ ] Performance acceptable (temps réponse <500ms)

### Ressources Complémentaires

**Documentation officielle :**

- [Laravel Deployment](https://laravel.com/docs/deployment)
- [Laravel Optimization](https://laravel.com/docs/deployment#optimization)
- [Nginx Official Docs](https://nginx.org/en/docs/)
- [PHP-FPM Tuning](https://www.php.net/manual/en/install.fpm.configuration.php)

**Outils recommandés :**

- **Forge** : Déploiement Laravel automatisé (payant)
- **Envoyer** : Déploiement zero-downtime (payant)
- **Supervisor** : Gestion queues Laravel
- **Certbot** : Certificats HTTPS Let's Encrypt gratuits

**Prochaines étapes (hors module) :**

- **HTTPS avec Let's Encrypt** : Certificat SSL gratuit
- **Redis** : Cache avancé, sessions, queues
- **Queue Workers** : Jobs asynchrones avec Supervisor
- **CDN** : Distribuer assets (Cloudflare, AWS CloudFront)
- **Load Balancing** : Scalabilité horizontale
- **CI/CD** : GitLab CI, GitHub Actions, Jenkins

<br>

---

## Conclusion

!!! quote "La production : là où le code rencontre la réalité"
    Déployer en production, c'est transformer un projet de formation en application vivante. Nginx, PHP-FPM, OPcache, les caches Laravel, MariaDB configuré et les backups automatisés : chaque élément de ce module est une couche de blindage supplémentaire pour que votre TALL Stack tourne sans faille, 24h/24.

<br>

---

[^1]: **Nginx** : Serveur web haute performance créé par Igor Sysoev (2004). Architecture événementielle asynchrone (vs Apache thread/process). Gère 10 000+ connexions simultanées. Fonctionnalités : reverse proxy, load balancer, cache HTTP. Configuration `/etc/nginx/`. Utilisé par 40% des sites web les plus visités (2024).

[^2]: **PHP-FPM** : FastCGI Process Manager pour PHP. Gère pool de workers PHP pour traiter requêtes. Configuration : `pm` (static/dynamic/ondemand), `pm.max_children` (workers max), `pm.start_servers` (workers démarrage). Socket Unix ou TCP. Logs `/var/log/php-fpm/`. Performance supérieure à mod_php Apache.

[^3]: **OPcache** : Cache bytecode PHP compilé en mémoire. Évite recompilation fichiers PHP à chaque requête. Gain 30-50% performance. Configuration : `opcache.memory_consumption` (RAM allouée), `opcache.validate_timestamps` (0 prod = jamais revalider). Vider cache : reload PHP-FPM. Inclus PHP 5.5+.

[^4]: **Vite** : Build tool JavaScript moderne remplaçant Webpack/Laravel Mix. Hot Module Replacement (HMR) ultra-rapide. Build production : minification, tree-shaking, code splitting. Laravel 9+ utilise Vite par défaut. Configuration `vite.config.js`. Commandes : `npm run dev` (dev), `npm run build` (prod).

[^5]: **Purge CSS** : Technique supprimant classes CSS non utilisées. Tailwind CSS génère ~3MB (toutes classes). Purge scanne fichiers (`tailwind.config.js` content), garde classes utilisées → ~10KB. Configuration : `content: ["./resources/**/*.blade.php"]`. Gain : 99.7% réduction taille, vitesse chargement page.

[^6]: **Cron** : Démon Unix planifiant tâches récurrentes. Syntaxe : `minute heure jour mois jour_semaine commande`. Fichier : `crontab -e`. Logs : `/var/log/syslog`. Exemples : `0 3 * * *` (quotidien 3h), `*/5 * * * *` (toutes 5 min). Usage : backups, maintenance, cleanups.

[^7]: **Mode Maintenance** : Feature Laravel désactivant application temporairement. Commande : `php artisan down` (activer), `php artisan up` (désactiver). Affiche page maintenance personnalisable. Utilisé pendant déploiements, migrations BDD critiques. Évite incohérences données pendant mise à jour.

[^8]: **Zero-Downtime Deployment** : Stratégie déploiement sans interruption service. Techniques : blue-green deployment (2 environnements, switch instant), rolling updates (mise à jour progressive), symlink swap (atomic). Laravel Forge/Envoyer automatisent. Critique applications 24/7. Complexe à implémenter manuellement.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La TALL stack (Tailwind, Alpine, Laravel, Livewire) offre une alternative puissante aux SPAs (Single Page Applications) lourdes en JavaScript. Elle permet de construire des interfaces réactives tout en gardant la logique métier solidement ancrée côté serveur.

> [Retourner à l'index TALL →](../index.md)
