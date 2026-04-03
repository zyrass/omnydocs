---
description: "Préparer l'environnement multi-système : SQLite, MySQL/MariaDB ou PostgreSQL"
icon: lucide/hard-drive
tags: ["LARAVEL", "DATABASE", "SQLITE", "MYSQL", "POSTGRESQL"]
---

# Configuration Multi-SGBD

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="30 Minutes">
</div>

## 1. Pourquoi des connecteurs abstraits ?

**Scénario typique :**

- **Développement local** : SQLite (zéro config, fichier unique, volatile)
- **Staging/Production** : MySQL ou PostgreSQL (robustesse, performance, concurrencé)

En PHP Procédural classique, modifier son système de base de données oblige a revoir la structure de tout le site web pour y insérer diverses requêtes PDO personnalisées et des mots de passes brutes. L'abstraction qu'est Laravel permet de **switcher facilement sans changer de code** entre SGBD via le simple fichier `.env`.

### 1.1 Déroulement des hostilités SQLite (Test)

**Avantages :** Strictement aucun serveur à configurer. Volatile, on peut recommencer un test en 1 seconde en supprimant le fichier. 

```bash
# Crée le dossier et la DB.
touch database/database.sqlite
```

**Configuration `.env` :**
```env
DB_CONNECTION=sqlite
# Pas besoin de DB_HOST, DB_PORT, ni de mdp, le fichier sqlite est autonome.
```

### 1.2 Déroulement des hostilités MySQL / MariaDB (Production classique)

On part du postulat que votre MariaDB est en cours d'exécution sur votre serveur.

**Configuration `.env` :**
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=blog_laravel
DB_USERNAME=root
DB_PASSWORD=votre_mot_de_passe
```

Le code et vos routes ne changeront pas !

**En base du fichier de configuration global : `config/database.php`**
(A ne toucher éventuellement que si l'administrateur système de la base de donnée exige un driver / port non standard).
```php
'mysql' => [
    'driver' => 'mysql',
    'host' => env('DB_HOST', '127.0.0.1'),
    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'forge'),
    'username' => env('DB_USERNAME', 'forge'),
    'password' => env('DB_PASSWORD', ''),
    'charset' => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'prefix' => '',
    'strict' => true,
    'engine' => null,
],
```

### 1.3 Déroulement des hostilités PostgreSQL (Production lourde)

Vous ne remplacez encore une fois que vos variables d'environnement. Laravel fera le reste et ré-éxecutera les SQL abstrait en dialecte PostgreSQL une fois migré.

```env
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=blog_laravel
DB_USERNAME=postgres
DB_PASSWORD=votre_mot_de_passe
```

<br>

---

## 2. Tableau comparatif décisif

| SGBD | Avantages | Inconvénients | Cas d'usage |
|------|-----------|---------------|-------------|
| **SQLite** | Zéro config, portable, rapide | Pas de concurrence, limité en volume | Dev local, prototypes, tests unitaires |
| **MySQL** | Populaire, bien documenté, mature | Performances moyennes en écriture très lourde (Comparé à PgSQL) | Applications web standard |
| **MariaDB** | Fork MySQL, compatible, open-source | Moins en vue sur l'image publicataire que MySQL | Alternative à MySQL |
| **PostgreSQL** | Robuste, SQL avancé, JSONB | Courbe d'apprentissage, Paramétrages fins | Apps complexes, données géolocalisées complexes + JSON massif |

<br>

---

## Conclusion

L'environnement DB est une question de choix et vous laisse libre de migrer ce que l'on appelle les Datasources très rapidement. Le prochain document passe aux travaux pratiques en vous exposant la syntaxe Eloquent pour réaliser l'intégralité du cycle de vie du Back-Office.
