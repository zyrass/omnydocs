---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 10

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Installation avec Laravel (version simplifiée avec `laravel new` + `php artisan serve`)

Tu as raison de le demander : pour une formation vendable, il faut une installation **simple, fiable, reproductible**.
Et aujourd’hui, la façon la plus “clean” de démarrer Laravel rapidement, c’est :

* soit avec **Laravel Installer** (`laravel new`)
* soit avec **Composer**
* soit avec **Laravel Herd** (sur certains OS)
* soit avec **Laravel Sail** (Docker)

Mais toi tu veux une installation simple, directe, pédagogique : on va faire la méthode “classique pro” :

1. création du projet en 1 commande
2. serveur local simple
3. intégration Alpine dans Blade
4. premier composant

---

# 1) Prérequis (clairs et sans pièges)

Avant tout, Laravel a besoin de 3 choses :

* PHP (version récente)
* Composer
* Node.js (pour Vite, Tailwind, Alpine)

### Vérification rapide (terminal)

```bash
php -v
composer -V
node -v
npm -v
```

Si tu as tout ça, tu peux avancer sans douleur.

---

# 2) Créer un projet Laravel “en 1 commande”

## Option A — La méthode simple et officielle : `laravel new`

Tu dois d’abord installer l’outil Laravel Installer.

### Installation de Laravel Installer

```bash
composer global require laravel/installer
```

Ensuite, tu dois t’assurer que Composer global est bien dans ton PATH.

En général, le chemin est :

* Linux/macOS : `~/.composer/vendor/bin` ou `~/.config/composer/vendor/bin`
* Windows : `%APPDATA%\Composer\vendor\bin`

Pour vérifier que `laravel` est disponible :

```bash
laravel --version
```

### Création du projet

```bash
laravel new alpine-laravel
cd alpine-laravel
```

Laravel va te demander quelques options selon la version (auth, DB, etc.).
Pour notre formation Alpine, tu peux rester minimal.

---

## Option B — Si `laravel new` n’est pas dispo : Composer direct

Si tu ne veux pas gérer l’installer global, tu fais :

```bash
composer create-project laravel/laravel alpine-laravel
cd alpine-laravel
```

C’est très fiable aussi.

---

# 3) Démarrer Laravel localement (mode simple)

Tu as 2 serveurs à lancer :

1. Laravel (backend)
2. Vite (assets JS/CSS)

### Terminal 1 — serveur Laravel

```bash
php artisan serve
```

Ça te donne une URL du type :

* `http://127.0.0.1:8000`

### Terminal 2 — serveur Vite

```bash
npm install
npm run dev
```

Vite va compiler tes assets.

---

# 4) Où est Alpine dans Laravel ?

Dans un Laravel moderne, Alpine est souvent déjà présent (selon starter kit).

Le point important à comprendre pour l’étudiant :

Laravel ne met pas Alpine “dans Blade” automatiquement.

Laravel utilise Vite, donc Alpine doit être :

* installé via npm
* importé dans `resources/js/app.js`
* démarré

---

# 5) Installer Alpine (si pas déjà présent)

Dans le dossier du projet :

```bash
npm install alpinejs
```

---

# 6) Activer Alpine dans `resources/js/app.js`

Ouvre :

* `resources/js/app.js`

Et mets ce code :

```js
import "./bootstrap";
import Alpine from "alpinejs";

window.Alpine = Alpine;

Alpine.start();
```

### Explication pédagogique

* `import "./bootstrap";` : fichier Laravel par défaut (axios, etc.)
* `import Alpine from "alpinejs";` : on récupère Alpine
* `window.Alpine = Alpine;` : pratique pour debug/plugins
* `Alpine.start();` : démarre Alpine dans le DOM

---

# 7) Vérifier que Blade charge bien le JS (très important)

Dans Laravel, le layout principal se trouve souvent dans :

* `resources/views/welcome.blade.php`
  ou
* `resources/views/layouts/app.blade.php` (si starter kit)

Dans un fichier Blade, tu dois avoir :

```blade
@vite(['resources/css/app.css', 'resources/js/app.js'])
```

C’est ce qui dit :

> “Charge le CSS et le JS gérés par Vite”

Sans ça, Alpine ne marchera pas.

---

# 8) Premier composant Alpine dans Blade (test réel)

Ouvre :

* `resources/views/welcome.blade.php`

Et mets un bloc simple :

```blade
<div style="padding: 16px;">
  <h1>Laravel + Alpine</h1>

  <div x-data="{ count: 0 }" style="border: 1px solid #ddd; padding: 12px; border-radius: 8px; max-width: 360px;">
    <p>
      Compteur :
      <strong x-text="count"></strong>
    </p>

    <button @click="count++" style="padding: 6px 10px;">
      +1
    </button>

    <button @click="count = 0" style="padding: 6px 10px;">
      Reset
    </button>
  </div>
</div>
```

Recharge la page :
si le compteur fonctionne, ton installation est validée.

---

# 9) Le piège numéro 1 en Laravel : “ça marche pas” (diagnostic)

Si Alpine ne marche pas, voici le protocole pro.

## Étape 1 — vérifier que Vite tourne

Tu dois avoir :

```bash
npm run dev
```

en cours.

Si tu l’arrêtes, ton JS ne se met plus à jour.

## Étape 2 — vérifier `@vite(...)`

Dans Blade, tu dois avoir `@vite(...)`.

Sinon ton `app.js` n’est pas chargé.

## Étape 3 — vérifier la console navigateur

Tu peux avoir :

* erreur import
* fichier non trouvé
* erreur JS bloquante

## Étape 4 — vérifier que Alpine démarre

Dans `app.js` tu dois avoir :

```js
Alpine.start();
```

---

# 10) Installation “encore plus simple” (cas pédagogique)

Si tu veux une version “ultra simple” pour les étudiants, tu peux même faire :

* Laravel minimal
* un seul fichier Blade
* Alpine juste pour des composants UI

Mais dans un projet pro, tu restes sur Vite, car c’est le standard moderne Laravel.

---

# 11) Mini exercice (spécial Laravel + Blade)

Objectif : prouver que tu maîtrises le setup.

### Exercice A — Toggle panel

Dans `welcome.blade.php`, ajoute un composant :

* bouton “Ouvrir/Fermer”
* un texte caché/visible avec `x-show`

### Exercice B — Mini formulaire

Ajoute un champ input avec :

* `x-model="name"`
* affichage live “Bonjour {name}”

---

# Résumé de la leçon

Tu sais maintenant :

* créer un Laravel rapidement avec `laravel new` (ou composer)
* lancer Laravel (`php artisan serve`)
* lancer Vite (`npm run dev`)
* installer Alpine via npm
* l’activer dans `resources/js/app.js`
* l’utiliser directement dans Blade

C’est exactement le workflow pro Laravel moderne.

---

## Prochaine leçon : Leçon 11 — Présentation des projets d’apprentissage (Ateliers UI + fil rouge)

Là on va cadrer ton parcours comme une vraie formation vendable :

* comment un étudiant suit les chapitres
* comment on fait les ateliers
* comment on avance sur les projets A/B/C sans se perdre

Avant ça, je te propose un mini check :
dans ton Laravel, tu veux partir sur un projet minimal (juste Blade + Alpine) ou tu veux que j’intègre directement Tailwind et qu’on parte sur une base TALL “propre” ?
