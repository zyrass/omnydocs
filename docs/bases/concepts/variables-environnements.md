---
description: "Isoler la configuration de l'application du code source grâce aux variables d'environnement (.env)."
icon: lucide/book-open-check
tags: ["ENV", "SECURITE", "CONFIGURATION", "12FACTOR", "DEPLOIEMENT"]
---

# Variables d'Environnement (.env)

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>

!!! quote "Le troisième principe du Twelve-Factor App"
    _La méthodologie **Twelve-Factor App** est un ensemble de bonnes pratiques pour créer des applications web modernes (SaaS). Le troisième facteur stipule : **Stockez la configuration dans l'environnement**. Une application doit séparer strictement son code (qui est le même pour tout le monde) de sa configuration (qui change selon l'environnement : local, staging, production)._

## Le Problème du Code en Dur (Hardcoding)

Imaginez que vous connectiez votre application à une base de données. L'approche du développeur débutant est d'écrire les identifiants directement dans le code :

```php
// MAUVAIS (Hardcoded)
$conn = new PDO('mysql:host=127.0.0.1;dbname=mon_site', 'root', 'monSuperMotDePasseSecret');
```

**Pourquoi c'est une catastrophe ?**
1. **Sécurité** : Si vous poussez ce code sur GitHub (même privé), tout membre de l'équipe (ou un pirate ayant accès au dépôt) voit votre mot de passe de production en clair.
2. **Flexibilité** : Sur votre PC, la BDD s'appelle `mon_site`. Mais sur le serveur de production, elle s'appelle `prod_db_v2`. Vous devrez modifier le code à chaque fois que vous déployez.

## La Solution : Le fichier `.env`

Le fichier `.env` (DotEnv) est un fichier texte brut, caché à la racine de votre projet, qui contient des paires **Clé=Valeur**. 

```bash title=".env"
# Environnement de développement
APP_ENV=local
APP_DEBUG=true

# Identifiants Base de données
DB_HOST=127.0.0.1
DB_NAME=mon_site
DB_USER=root
DB_PASSWORD=monSuperMotDePasseSecret

# Clé secrète de paiement (Stripe)
STRIPE_API_KEY=sk_test_123456789
```

Désormais, dans votre code, vous appelez simplement ces variables via des fonctions natives ou des helpers fournis par votre framework (comme Laravel, Symfony ou Node.js).

```php title="En PHP (Laravel)"
// BON
$dbUser = env('DB_USER'); // Retourne 'root'
```

```javascript title="En Node.js"
// BON
const dbUser = process.env.DB_USER;
```

## Les 3 Règles d'Or des Variables d'Environnement

<div class="grid cards" markdown>

-   :lucide-git-merge:{ .lg .middle } **1. Jamais dans Git**

    ---
    Le fichier `.env` **NE DOIT JAMAIS** être versionné. Il doit toujours figurer dans votre fichier `.gitignore`. S'il est poussé sur GitHub, considérez que tous vos mots de passe sont compromis.

-   :lucide-copy:{ .lg .middle } **2. Toujours un fichier .env.example**

    ---
    Puisque le `.env` n'est pas poussé, comment un nouveau développeur sait-il quelles variables configurer ? Vous devez toujours versionner un fichier `.env.example` contenant les clés, mais avec des valeurs vides ou fictives (`DB_PASSWORD=`).

-   :lucide-server:{ .lg .middle } **3. Une configuration par Environnement**

    ---
    Sur votre machine (Local), vous avez votre `.env` pointant vers `localhost`. Sur le serveur de Production (VPS ou Vercel), vous définirez d'autres valeurs directement dans le panneau de contrôle de l'hébergeur (ex: `DB_HOST=10.0.2.45`). Le code source reste 100% identique.

</div>

## Syntaxe et Bonnes Pratiques

Bien que ce soit du texte simple, il y a des conventions à respecter :

1. **Majuscules et Underscores** : Les clés doivent toujours être en majuscules, séparées par des underscores (`MA_CLE_SECRETE`).
2. **Pas d'espaces autour du égal** : Écrivez `KEY=value`, pas `KEY = value`.
3. **Guillemets pour les chaînes complexes** : Si votre valeur contient des espaces ou des caractères spéciaux, entourez-la de guillemets doubles.
   ```bash
   APP_NAME="Mon Super Projet"
   PASSWORD="UnM0tDePasse#TresComplexe!"
   ```
4. **Booléens** : Préférez `true` / `false` en minuscules.

## Comment ça marche en coulisses ?

Historiquement, les variables d'environnement étaient définies directement dans le système d'exploitation du serveur (Windows ou Linux). 

Exemple sous Linux Bash :
```bash
export DB_USER="root"
php index.php
```

Le fichier `.env` est en réalité un "Hack" moderne. Des librairies comme `vlucas/phpdotenv` (en PHP) ou `dotenv` (en Node.js) viennent lire ce fichier texte lors du démarrage de l'application et injectent temporairement ces valeurs dans l'environnement virtuel du programme, simulant des variables système.

## Conclusion

Le fichier `.env` est la première ligne de défense de votre application. C'est lui qui sépare votre code (public ou partagé) de vos secrets (strictement confidentiels). Adopter cette pratique dès le premier jour est la marque d'un développeur consciencieux.