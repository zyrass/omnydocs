---
description: "Déploiement en production de l'API Laravel sur un VPS (via Laravel Forge), configuration de Redis et hébergement du client Angular sur Vercel."
icon: lucide/book-open-check
tags: ["DEPLOYMENT", "VPS", "FORGE", "VERCEL", "PRODUCTION"]
---

# Phase 8 : Déploiement Production

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2h - 3h">
</div>

## Objectif de la Phase

> Notre jeu "Dungeon RPG" est terminé et optimisé en local. Il est temps de le rendre accessible au monde entier. Comme l'architecture est totalement découplée (API Stateless + Client SPA), nous allons utiliser deux stratégies d'hébergement différentes : un serveur dédié **VPS (Linux)** géré par **Laravel Forge** pour le backend (qui a besoin de PHP, MySQL et Redis), et une plateforme **Serverless CDN (Vercel ou Netlify)** pour distribuer les fichiers statiques de notre Frontend Angular.

## Étape 8.1 : Déploiement du Backend (Laravel Forge)

**Laravel Forge** est un service créé par Taylor Otwell (créateur de Laravel) qui permet d'approvisionner et de gérer des serveurs VPS (DigitalOcean, AWS, Linode) sans avoir à être un expert en administration système (DevOps).

### 1. Provisionner le Serveur
Sur l'interface de Forge, connectez votre compte DigitalOcean et créez un nouveau serveur (ex: 2GB RAM pour supporter confortablement MySQL + Redis + PHP-FPM).
*Forge installe automatiquement : Nginx, PHP 8.x, MySQL, Redis, et Composer.*

### 2. Connecter le Dépôt GitHub
Ajoutez un nouveau "Site" dans Forge (ex: `api.dungeon-rpg.com`).
Connectez ce site à votre dépôt GitHub contenant l'API Laravel.

### 3. Configurer l'Environnement (.env)
Dans l'onglet "Environment" de Forge, modifiez le `.env` de production :

```bash title=".env (Production)"
APP_ENV=production
APP_DEBUG=false
APP_URL=https://api.dungeon-rpg.com

DB_CONNECTION=mysql
# Renseignez les identifiants BDD fournis par Forge
DB_DATABASE=forge
DB_USERNAME=forge
DB_PASSWORD=votre_mot_de_passe_complexe

# Activation de Redis pour le cache (Leaderboard)
CACHE_STORE=redis
SESSION_DRIVER=database # Ou redis (bien que nous utilisions Sanctum)

# CORS & Sanctum
# L'URL où sera hébergé votre Frontend Angular
SANCTUM_STATEFUL_DOMAINS=app.dungeon-rpg.com
```

### 4. Certificat SSL (HTTPS)
Allez dans l'onglet "SSL" et générez un certificat **Let's Encrypt** gratuit. C'est indispensable pour sécuriser les Tokens Sanctum en transit.

### 5. Script de Déploiement (CI/CD simple)
Forge permet d'exécuter un script bash à chaque "git push" (Push to Deploy).
```bash title="Forge Deploy Script"
cd /home/forge/api.dungeon-rpg.com
git pull origin main
composer install --no-interaction --prefer-dist --optimize-autoloader
echo "" | sudo -S service php8.2-fpm reload

# Optimisations Laravel
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Migrations BDD
php artisan migrate --force
```

## Étape 8.2 : Déploiement du Frontend (Vercel)

Le client Angular, une fois compilé, n'est constitué que de fichiers statiques (HTML/JS/CSS). Il n'a besoin ni de PHP, ni de base de données. L'héberger sur un VPS classique serait du gâchis. Les CDN comme Vercel sont gratuits, infiniment scalables, et déploient l'app au plus près des joueurs géographiquement.

### 1. Build de Production (Local)
Vérifiez que votre application compile sans erreur.
```bash
ng build --configuration production
```
Vérifiez également que votre fichier `environment.prod.ts` pointe bien vers votre API de production (et non localhost) :
```typescript title="src/environments/environment.prod.ts"
export const environment = {
  production: true,
  apiUrl: 'https://api.dungeon-rpg.com/api'
};
```

### 2. Déploiement sur Vercel
Le plus simple est d'utiliser la ligne de commande (Vercel CLI).
```bash
npm i -g vercel
vercel
```
Répondez aux questions :
- Framework preset : Angular
- Build Command : `ng build`
- Output Directory : `dist/dungeon-rpg-client/browser`

Vercel vous fournira immédiatement une URL sécurisée (HTTPS) (ex: `https://dungeon-rpg.vercel.app`).

*(Note : N'oubliez pas d'ajouter ce nom de domaine dans le `config/cors.php` de votre API Laravel !)*

## Étape 8.3 : Gestion des Erreurs de Routage (SPA Fallback)

Sur Vercel (ou Nginx), un problème courant avec les SPA Angular est l'erreur 404 lors du rafraîchissement manuel d'une page (ex: `/game`). Le serveur web cherche un fichier `game.html` qui n'existe pas.

Pour corriger cela sur Vercel, ajoutez un fichier `vercel.json` à la racine de votre projet Angular :

```json title="vercel.json"
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```
*Cela indique à Vercel de rediriger toutes les requêtes entrantes vers `index.html`, laissant le Router Angular gérer l'affichage.*

## Étape 8.4 : Scalabilité et Futur (WebSockets)

Votre jeu tourne actuellement via des requêtes HTTP courtes (REST). Si le jeu devient très populaire, le modèle "Pull" (le client demande les infos en permanence) a ses limites.

L'évolution naturelle (Niveau 4 !) serait de passer au modèle "Push" avec les **WebSockets (Laravel Reverb / Pusher)**. Au lieu d'attendre la réponse d'une requête HTTP, le serveur "pousserait" instantanément l'action du monstre au client, permettant du véritable temps réel (Multijoueur coopératif, Chat global).

## Conclusion de la Phase 8

Votre jeu vidéo en ligne est désormais "Live" !
- ✅ **API Backend** propulsée par Nginx, PHP-FPM, MySQL et Redis sur un VPS dédié.
- ✅ **Infrastructure gérée** élégamment grâce à Laravel Forge (SSL auto, Déploiement auto).
- ✅ **Frontend Angular** distribué mondialement sur le réseau Vercel (Serverless Edge).
- ✅ **CORS** correctement configuré entre les deux environnements.

Rendez-vous à la conclusion du projet Sanctum pour clôturer ce passionnant Laravel Lab !
