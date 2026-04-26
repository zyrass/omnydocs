---
description: "Code Coverage — Mesurer la couverture de tests : outils (Xdebug, PCOV), seuils, rapports HTML, intégration CI/CD Laravel."
icon: lucide/book-open-check
tags: ["COVERAGE", "TESTING", "XDEBUG", "PCOV", "CICD", "PHPUNIT", "PEST"]
---

# Code Coverage — Couverture de Tests

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2024"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Carte et le Territoire"
    Un cartographe sait que sa carte n'est pas parfaite : certaines zones sont bien détaillées, d'autres à peine esquissées. Le code coverage est votre carte du territoire testé. 80% de coverage signifie que 80% des chemins d'exécution sont validés — mais ça ne dit pas si les 80% testés le sont *bien*. La carte vous guide, elle ne remplace pas l'exploration.

Le **code coverage** mesure la proportion de code source réellement exécutée par les tests. C'est un indicateur de risque, pas une garantie de qualité.

!!! warning "L'erreur courante"
    Un coverage à 100% ne prouve pas que votre code est correct — seulement que chaque ligne a été exécutée **au moins une fois**. Un test vide ou sans assertion peut atteindre 100%. Le coverage est un plancher, pas un plafond.

<br>

---

## 1. Outils de Coverage PHP

| Outil | Méthode | Performance | Précision | Recommandé pour |
|---|---|---|---|---|
| **Xdebug** | Interprétation | Lente | Très précise (line/branch/path) | Développement local |
| **PCOV** | Extension légère | Rapide | Ligne uniquement | CI/CD en production |
| **phpdbg** | Binaire PHP | Moyenne | Ligne uniquement | Alternative sans extension |

```bash title="Bash — Installer les outils de coverage"
# ─── Xdebug (local — le plus complet) ────────────────────────────────────────
# Ubuntu : sudo apt install php-xdebug
# macOS  : pecl install xdebug
# Vérifier : php -v → "with Xdebug v3.x"

# ─── PCOV (CI — plus rapide) ──────────────────────────────────────────────────
pecl install pcov
# php.ini : extension=pcov.so
# Vérifier : php -m | grep pcov

# ─── Docker (CI) ──────────────────────────────────────────────────────────────
# Image avec PCOV : ghcr.io/roadrunner-server/roadrunner ou php:8.3-cli + PCOV
```

<br>

---

## 2. Générer un Rapport de Coverage

### PHPUnit

```bash title="Bash — PHPUnit : générer le coverage"
# ─── Rapport HTML (ouvrir coverage-report/index.html) ────────────────────────
XDEBUG_MODE=coverage php artisan test --coverage-html coverage-report

# ─── Rapport en ligne de commande (résumé) ────────────────────────────────────
XDEBUG_MODE=coverage php artisan test --coverage

# ─── Avec PCOV (plus rapide en CI) ────────────────────────────────────────────
php -d pcov.enabled=1 artisan test --coverage

# ─── Rapport Clover XML (pour SonarQube, Codecov, CI) ─────────────────────────
XDEBUG_MODE=coverage php artisan test --coverage-clover coverage.xml

# ─── Rapport Cobertura XML (GitLab CI) ────────────────────────────────────────
XDEBUG_MODE=coverage php artisan test --coverage-cobertura coverage.xml

# ─── Seuil minimum (fail si < 80%) ────────────────────────────────────────────
XDEBUG_MODE=coverage php artisan test --coverage --min=80
# → Si coverage < 80% : exit code 1, build échoue
```

### Pest

```bash title="Bash — Pest : générer le coverage"
# Coverage HTML
XDEBUG_MODE=coverage ./vendor/bin/pest --coverage-html coverage-report

# Coverage en ligne de commande avec seuil
XDEBUG_MODE=coverage ./vendor/bin/pest --coverage --min=80

# Coverage Clover pour CI
XDEBUG_MODE=coverage ./vendor/bin/pest --coverage-clover coverage.xml
```

### Configuration phpunit.xml

```xml title="XML — phpunit.xml : configurer le coverage"
<?xml version="1.0" encoding="UTF-8"?>
<phpunit>
    <coverage processUncoveredFiles="true">
        <!-- Répertoires à analyser (code de production) -->
        <include>
            <directory suffix=".php">./app</directory>
        </include>

        <!-- Répertoires à exclure -->
        <exclude>
            <directory>./app/Http/Middleware</directory>
            <file>./app/Http/Kernel.php</file>
        </exclude>

        <!-- Rapports générés -->
        <report>
            <html outputDirectory="coverage-report"/>
            <clover outputFile="coverage.xml"/>
            <text outputFile="php://stdout" showUncoveredFiles="false"/>
        </report>
    </coverage>
</phpunit>
```

<br>

---

## 3. Lire un Rapport Coverage

```
coverage-report/
├── index.html          ← Vue globale par répertoire
├── app/
│   ├── Services/
│   │   └── PriceCalculator.php.html  ← Vue ligne par ligne
│   └── Models/
│       └── User.php.html
```

**Lecture du rapport HTML (ligne par ligne) :**

```
Vert  → Ligne exécutée par les tests
Rouge → Ligne jamais exécutée (risque non testé)
Jaune → Branche partiellement couverte (ex: IF sans ELSE testé)
```

**Métriques disponibles :**

| Métrique | Description | Seuil conseillé |
|---|---|---|
| **Line Coverage** | % de lignes exécutées | ≥ 80% |
| **Branch Coverage** | % de branches (if/else, ternaires) | ≥ 70% |
| **Path Coverage** | % de chemins complets possibles | ≥ 60% |
| **Method Coverage** | % de méthodes appelées | ≥ 90% |
| **Class Coverage** | % de classes testées | ≥ 85% |

<br>

---

## 4. Annotations de Coverage

```php title="PHP — Ignorer du code du coverage avec des annotations"
<?php

use PHPUnit\Framework\Attributes\CodeCoverageIgnore;

class UserController
{
    /**
     * Méthode critique — DOIT être couverte.
     */
    public function store(Request $request): JsonResponse
    {
        // Ce code doit être testé
        $user = User::create($request->validated());
        return response()->json($user, 201);
    }

    /**
     * Code généré automatiquement — inutile de le tester.
     */
    #[CodeCoverageIgnore]
    public function __debugInfo(): array
    {
        return ['id' => $this->id];
    }
}

// En commentaire (style PHPDoc, compatible PHPUnit 9) :
/** @codeCoverageIgnore */
class LegacyAdapter
{
    // Classe legacy non testable — exclue du rapport
}

// Exclure une région :
// @codeCoverageIgnoreStart
$debug = true; // Ligne de debug jamais exécutée en prod
// @codeCoverageIgnoreEnd
```

<br>

---

## 5. Intégration CI/CD

### GitHub Actions

```yaml title="YAML — GitHub Actions : coverage + badge Codecov"
name: Tests

on: [push, pull_request]

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP avec PCOV
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          coverage: pcov          # Plus rapide que Xdebug en CI

      - name: Installer les dépendances
        run: composer install --no-interaction

      - name: Lancer les tests avec coverage
        run: |
          php artisan test \
            --coverage-clover coverage.xml \
            --min=80
        env:
          DB_CONNECTION: sqlite
          DB_DATABASE: ':memory:'

      - name: Upload sur Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### GitLab CI

```yaml title="YAML — GitLab CI : coverage avec rapport Cobertura"
test:
  image: php:8.3-cli
  before_script:
    - pecl install pcov
    - composer install
  script:
    - php -d pcov.enabled=1 artisan test
        --coverage-cobertura coverage.xml
        --min=80
  coverage: '/^\s*Lines:\s*\d+.\d+\%/'   # Regex pour extraire le % affiché
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

<br>

---

## 6. Stratégie Coverage Recommandée

```
Priorité de coverage par type de code :

🔴 CRITIQUE — Couvrir à 100% :
   • Classes de service (logique métier)
   • Validators
   • Calculs financiers
   • Authentification / Autorisation

🟡 IMPORTANT — Couvrir à 80%+ :
   • Controllers (tests Feature)
   • Models Eloquent (scopes, accessors, mutators)
   • Jobs / Queues

🟢 OPTIONNEL — Couvrir selon effort :
   • Config files
   • Providers
   • Migrations (non testées directement)
   • Middleware (testé via Feature tests)

⚫ EXCLURE du rapport :
   • Generated code (Breeze, etc.)
   • Interfaces pures
   • DTOs simples sans logique
```

```php title="PHP — Pest : marquer des tests comme slow/skip pour CI"
it('generates a PDF invoice', function () {
    // Test lourd — exclure du coverage rapide
    $invoice = Invoice::factory()->create();
    $pdf = app(InvoiceService::class)->generatePdf($invoice);
    expect($pdf)->toBeInstanceOf(PDF::class);
})->group('slow');  // Exclure avec --exclude-group=slow en CI rapide
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le coverage est un **indicateur de risque**, pas de qualité. Un seuil de **80% de line coverage** est un consensus raisonnable pour les projets Laravel — assez strict pour forcer les tests critiques, assez souple pour ne pas tester le boilerplate. **PCOV** est recommandé en CI/CD pour sa rapidité. Intégrez le rapport Clover dans votre pipeline CI pour visualiser les tendances et bloquer les PR qui font chuter le coverage. Ne laissez jamais le coverage descendre sous votre seuil sans décision consciente.

> Prochaine étape : [SAST →](./sast.md) — l'analyse statique qui détecte les bugs sans exécuter le code.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La maîtrise de ces concepts de développement moderne est cruciale pour construire des applications scalables, maintenables et sécurisées.

> [Retour à l'index →](./index.md)
