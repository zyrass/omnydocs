---
description: "SAST — Analyse statique de code PHP : PHPStan, Psalm, Larastan. Détecter les bugs et erreurs de type sans exécuter le code."
icon: lucide/scan-search
tags: ["SAST", "PHPSTAN", "PSALM", "LARASTAN", "QUALITE", "PHP", "LARAVEL"]
---

# SAST — Analyse Statique de Code

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2024"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Correcteur Orthographique pour le Code"
    Un correcteur orthographique lit votre texte sans le prononcer et détecte les fautes de frappe, les accords incorrects, les tournures ambiguës — avant même que vous cliquiez sur "Imprimer". SAST fonctionne pareil : il analyse le code source sans l'exécuter et détecte les bugs de type, les variables non initialisées, les méthodes inexistantes, les failles potentielles. Certains bugs sont détectés dès l'écriture, sans lancer un seul test.

**SAST (Static Application Security Testing)** désigne l'analyse du code source *sans exécution*. En PHP, cela couvre principalement la vérification de types, la détection d'erreurs logiques et les problèmes de sécurité structurels.

<br>

---

## 1. Les Outils SAST PHP

| Outil | Focus | Configuration | Popularité |
|---|---|---|---|
| **PHPStan** | Types, logique, erreurs | `phpstan.neon` | ⭐⭐⭐⭐⭐ |
| **Psalm** | Types, sécurité, taint | `psalm.xml` | ⭐⭐⭐⭐ |
| **Larastan** | PHPStan + Laravel magics | Extension PHPStan | ⭐⭐⭐⭐⭐ |
| **PHP-CS-Fixer** | Style de code | `.php-cs-fixer.php` | ⭐⭐⭐⭐ |
| **Rector** | Refactoring automatisé | `rector.php` | ⭐⭐⭐⭐ |

<br>

---

## 2. PHPStan — Analyse de Types

PHPStan analyse le code PHP et détecte les erreurs à compile-time : types incorrects, méthodes inexistantes, propriétés non déclarées, null non gérés.

```bash title="Bash — Installer et configurer PHPStan"
# Installation
composer require --dev phpstan/phpstan

# Pour Laravel : Larastan (PHPStan + connaissance des magics Laravel)
composer require --dev nunomaduro/larastan

# Lancer l'analyse
./vendor/bin/phpstan analyse

# Avec niveau de rigueur (0 = laxiste, 10 = max)
./vendor/bin/phpstan analyse --level=8

# Sur des dossiers spécifiques
./vendor/bin/phpstan analyse app/Services app/Models --level=6
```

```ini title="INI — phpstan.neon : configuration recommandée Laravel"
includes:
    - ./vendor/nunomaduro/larastan/extension.neon

parameters:
    paths:
        - app

    level: 8                    # Niveau de rigueur (0-10, 8 recommandé)

    ignoreErrors:
        # Ignorer les faux positifs connus
        - '#Call to an undefined method Illuminate\\Database\\Eloquent#'

    excludePaths:
        - app/Http/Middleware/TrustProxies.php   # Legacy auto-généré

    checkMissingIterableValueType: false     # Évite les faux positifs sur les collections
    treatPhpDocTypesAsCertain: false         # Cohérence avec les types déclarés
```

### Ce que PHPStan Détecte

```php title="PHP — Exemples d'erreurs détectées par PHPStan"
<?php

class UserService
{
    // ─── Erreur : Méthode inexistante ──────────────────────────────────────────
    public function getFullName(User $user): string
    {
        return $user->fullName();  // ❌ PHPStan : Method fullName() not found
    }

    // ─── Erreur : Null non géré ────────────────────────────────────────────────
    public function getUserEmail(int $id): string
    {
        $user = User::find($id);
        return $user->email;  // ❌ PHPStan : Cannot access -> on ?User (peut être null)
    }

    // ✅ Version corrigée
    public function getUserEmailSafe(int $id): string
    {
        $user = User::findOrFail($id);  // Lance ModelNotFoundException si absent
        return $user->email;
    }

    // ─── Erreur : Type de retour incorrect ────────────────────────────────────
    public function getAge(User $user): int
    {
        return $user->birthdate->age;  // ❌ Retourne float|int selon Carbon
    }

    // ─── Erreur : Propriété non initialisée ───────────────────────────────────
    class Report
    {
        private string $title;  // ❌ PHPStan level 8 : propriété jamais assignée
                                 //    avant premier accès possible

        public function getTitle(): string
        {
            return $this->title;  // Risque de TypeError si constructeur oublié
        }
    }
}
```

### Niveaux PHPStan — Guide

```
Niveau 0 : Erreurs basiques (classes inexistantes, syntaxe)
Niveau 1 : + Arguments incorrects, appels de méthodes inconnues
Niveau 2 : + Propriétés inconnues
Niveau 3 : + Types de retour
Niveau 4 : + Variables potentiellement non définies
Niveau 5 : + Méthodes et propriétés sur des types mixtes
Niveau 6 : + Types de paramètres nécessaires
Niveau 7 : + Union types stricts
Niveau 8 : + null strict (cannot access on nullable) ← RECOMMANDÉ Laravel
Niveau 9 : + PHPDoc types aussi stricts que les déclarations
Niveau 10 : Maximum — très peu de code le passe sans annotations
```

<br>

---

## 3. Psalm — Analyse de Types + Sécurité

Psalm est plus strict que PHPStan sur les types et propose une fonctionnalité unique : **Taint Analysis** (analyse de contamination).

```bash title="Bash — Installer et configurer Psalm"
composer require --dev vimeo/psalm

# Initialiser la configuration
./vendor/bin/psalm --init app 4   # Niveau 4 pour commencer

# Lancer l'analyse
./vendor/bin/psalm

# Analyse de sécurité (taint) — détecter les injections
./vendor/bin/psalm --taint-analysis
```

```xml title="XML — psalm.xml : configuration Psalm"
<?xml version="1.0"?>
<psalm
    errorLevel="4"
    resolveFromConfigFile="true"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="https://getpsalm.org/schema/config"
>
    <projectFiles>
        <directory name="app" />
        <ignoreFiles>
            <directory name="vendor" />
        </ignoreFiles>
    </projectFiles>

    <issueHandlers>
        <!-- Ignorer les faux positifs sur les collections Laravel -->
        <MixedReturnStatement errorLevel="info" />
        <PropertyNotSetInConstructor errorLevel="info" />
    </issueHandlers>
</psalm>
```

### Taint Analysis — Détecter les Injections

```php title="PHP — Psalm Taint : détecter les failles XSS et injection SQL"
<?php

// ❌ Psalm détecte la vulnérabilité XSS :
function displayName(Request $request): string
{
    $name = $request->input('name');  // Source "taintée" (user input)
    return "<h1>Bonjour $name</h1>"; // ❌ Psalm : TaintedHtml — XSS possible
}

// ✅ Version sécurisée :
function displayNameSafe(Request $request): string
{
    $name = e($request->input('name'));  // e() = htmlspecialchars — assainit
    return "<h1>Bonjour $name</h1>";    // ✅ Plus de contamination
}

// ❌ Psalm détecte l'injection SQL :
function searchUsers(Request $request): Collection
{
    $search = $request->input('search');
    return DB::select("SELECT * FROM users WHERE name = '$search'");
    // ❌ Psalm : TaintedSql — injection SQL possible
}

// ✅ Version sécurisée :
function searchUsersSafe(Request $request): Collection
{
    return DB::select("SELECT * FROM users WHERE name = ?", [$request->input('search')]);
    // ✅ Paramètre lié — plus de contamination
}
```

<br>

---

## 4. Intégration CI/CD

```yaml title="YAML — GitHub Actions : PHPStan + Psalm en pipeline CI"
name: SAST

on: [push, pull_request]

jobs:
  phpstan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'

      - run: composer install --no-interaction

      - name: Analyse PHPStan (niveau 8)
        run: ./vendor/bin/phpstan analyse --no-progress --error-format=github

  psalm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'

      - run: composer install --no-interaction

      - name: Analyse Taint Psalm
        run: ./vendor/bin/psalm --taint-analysis --output-format=github
```

<br>

---

## 5. Rector — Refactoring Automatique

```bash title="Bash — Rector : moderniser automatiquement le codebase"
composer require --dev rector/rector

# Initialiser
./vendor/bin/rector init

# Prévisualiser les changements (dry-run)
./vendor/bin/rector process --dry-run

# Appliquer les refactorings
./vendor/bin/rector process
```

```php title="PHP — rector.php : règles de modernisation PHP 8.x"
<?php

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use Rector\Set\ValueObject\SetList;

return RectorConfig::configure()
    ->withPaths([__DIR__ . '/app'])
    ->withSets([
        LevelSetList::UP_TO_PHP_83,     // Moderniser vers PHP 8.3
        SetList::DEAD_CODE,              // Supprimer le code mort
        SetList::STRICT_BOOLEANS,       // Comparaisons strictes
        SetList::TYPE_DECLARATION,       // Ajouter les déclarations de type
    ]);
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Installation et premier rapport**

```bash title="Bash — Exercice 1 : installer PHPStan/Larastan sur votre projet"
# 1. Installer Larastan
composer require --dev nunomaduro/larastan

# 2. Créer phpstan.neon avec niveau 5
# 3. Lancer l'analyse : ./vendor/bin/phpstan analyse
# 4. Corriger les 3 premières erreurs reportées
# 5. Monter au niveau 6, relancer, corriger encore
# 6. Atteindre niveau 8 sans erreur sur app/Services/
```

**Exercice 2 — Taint Analysis**

```php title="PHP — Exercice 2 : identifier et corriger des vulnérabilités avec Psalm"
// Installez Psalm et lancez --taint-analysis sur ce code :

class SearchController
{
    public function search(Request $request)
    {
        $term = $request->input('q');
        $results = DB::select("SELECT * FROM products WHERE name LIKE '%$term%'");
        echo "<h2>Résultats pour : $term</h2>";
        return view('search', compact('results'));
    }
}

// 1. Psalm doit reporter au moins 2 contaminations (SQL + XSS)
// 2. Corriger les deux vulnérabilités
// 3. Vérifier que Psalm ne reporte plus d'erreur
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    **PHPStan + Larastan** est le duo de référence pour les projets Laravel — commencez au niveau 5, montez progressivement vers 8. **Psalm** ajoute la taint analysis pour détecter les vulnérabilités XSS et injection SQL structurellement, sans exécuter le code. Ces outils ne remplacent pas les tests — ils les **complètent** en attrapant des bugs différents : les erreurs de type et les chemins de contamination que les tests unitaires peuvent manquer. Intégrer SAST en CI/CD bloque les régressions de typage dès la PR.

> Prochaine étape : [DAST →](./dast.md) — les tests dynamiques qui analysent l'application en cours d'exécution.

<br>