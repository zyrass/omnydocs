---
description: "Vitest 04 — Coverage & CI/CD : générer des rapports de couverture, seuils, intégration GitHub Actions et GitLab CI."
icon: lucide/bar-chart-3
tags: ["VITEST", "COVERAGE", "CICD", "GITHUB_ACTIONS", "GITLAB", "TESTING"]
---

# Module 04 — Coverage & CI/CD

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Vitest 1.x"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Bilan de Santé Automatisé"
    Un médecin ne se contente pas de soigner les patients malades : il organise des bilans de santé préventifs pour détecter les problèmes avant qu'ils deviennent critiques. Le CI/CD avec tests et coverage, c'est ce bilan automatisé pour votre code : à chaque push, un examen complet, des résultats chiffrés, et un signal d'alerte si quelque chose ne va pas. Sans attendre qu'un bug atteigne la production.

Ce module couvre la génération de rapports de coverage Vitest et leur intégration dans les pipelines CI/CD GitHub Actions et GitLab CI.

<br>

---

## 1. Configurer le Coverage

```bash title="Bash — Installer le provider de coverage"
# V8 (recommandé — rapide, natif Node.js, aucune dépendance)
npm install -D @vitest/coverage-v8

# Istanbul (alternative — plus de métriques, compatible Jest)
npm install -D @vitest/coverage-istanbul
```

```typescript title="TypeScript — vite.config.ts : configuration coverage complète"
import { defineConfig } from 'vite';

export default defineConfig({
    test: {
        coverage: {
            // ─── Provider ─────────────────────────────────────────────────────
            provider: 'v8',                // 'v8' ou 'istanbul'

            // ─── Fichiers à analyser ───────────────────────────────────────────
            include: [
                'src/**/*.{js,ts,vue,jsx,tsx}',
            ],
            exclude: [
                'src/main.{js,ts}',        // Point d'entrée
                'src/**/*.d.ts',           // Types TypeScript
                'src/**/*.config.{js,ts}', // Fichiers de config
                'src/**/__mocks__/**',      // Dossiers de mocks
                'src/**/*.stories.{js,ts}', // Storybook
            ],

            // ─── Rapports générés ──────────────────────────────────────────────
            reporter: [
                'text',     // Résumé terminale
                'html',     // Rapport visuel → coverage/index.html
                'lcov',     // Format CI (Codecov, Coveralls, SonarQube)
                'json',     // Pour les outils tiers
            ],

            // ─── Répertoire de sortie ──────────────────────────────────────────
            reportsDirectory: './coverage',

            // ─── Seuils minimaux (build échoue si en dessous) ──────────────────
            thresholds: {
                lines:      80,
                functions:  80,
                branches:   70,
                statements: 80,

                // Seuils par fichier spécifique (plus strict sur le code critique)
                'src/services/payment.ts': {
                    lines:     100,
                    functions: 100,
                },
            },

            // ─── Inclure les fichiers non couverts dans le rapport ─────────────
            all: true,     // Montre les fichiers sans aucun test (coverage 0%)
        },
    },
});
```

<br>

---

## 2. Lancer et Lire le Coverage

```bash title="Bash — Générer le coverage"
# Coverage en mode run (une seule fois)
npm run test:coverage
# ou : npx vitest run --coverage

# Coverage en mode watch (se met à jour à chaque modification)
npx vitest --coverage

# Ouvrir le rapport HTML
# Windows : start coverage/index.html
# macOS   : open coverage/index.html
# Linux   : xdg-open coverage/index.html
```

```
Rapport terminal (résumé) :
────────────────────────────────────────────────────────────
 Coverage report from v8
────────────────────────────────────────────────────────────
File                   | % Stmts | % Branch | % Funcs | % Lines |
-----------------------|---------|----------|---------|---------|
All files              |   84.21 |    72.50 |   90.00 |   84.21 |
 src/services          |   91.30 |    80.00 |   95.00 |   91.30 |
  api.ts               |   95.00 |    90.00 |  100.00 |   95.00 |
  payment.ts           |   87.50 |    70.00 |   90.00 |   87.50 |
 src/utils             |   72.73 |    60.00 |   80.00 |   72.73 | ← Sous le seuil !
  currency.ts          |   72.73 |    60.00 |   80.00 |   72.73 |
────────────────────────────────────────────────────────────
```

```
Coverage HTML (lecture ligne par ligne) :
🟢 Vert  → Ligne exécutée par les tests
🔴 Rouge → Ligne jamais exécutée (risque non testé)
🟡 Jaune → Branche partiellement couverte (ex: if sans else testé)
```

<br>

---

## 3. Intégration GitHub Actions

```yaml title="YAML — .github/workflows/test.yml : Vitest + Coverage + Codecov"
name: Tests & Coverage

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: ['18.x', '20.x']   # Tester sur plusieurs versions Node

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Installer les dépendances
        run: npm ci                        # ci (pas install) = reproductible en CI

      - name: Lancer les tests avec coverage
        run: npx vitest run --coverage
        env:
          NODE_ENV: test
          VITE_API_URL: http://localhost:3000

      - name: Upload coverage sur Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info     # Rapport LCOV généré par Vitest
          fail_ci_if_error: true
          token: ${{ secrets.CODECOV_TOKEN }}

      - name: Upload rapport HTML (artifact)
        uses: actions/upload-artifact@v4
        if: always()                       # Même si les tests échouent
        with:
          name: coverage-report-node-${{ matrix.node-version }}
          path: coverage/
          retention-days: 7
```

### Badge Coverage dans le README

```markdown title="Markdown — Ajouter un badge Codecov au README"
[![Coverage](https://codecov.io/gh/user/repo/graph/badge.svg?token=TOKEN)](https://codecov.io/gh/user/repo)
[![Tests](https://github.com/user/repo/actions/workflows/test.yml/badge.svg)](https://github.com/user/repo/actions/workflows/test.yml)
```

<br>

---

## 4. Intégration GitLab CI

```yaml title="YAML — .gitlab-ci.yml : Vitest avec rapport coverage GitLab"
image: node:20-alpine

cache:
  paths:
    - node_modules/

stages:
  - test
  - report

test:
  stage: test
  script:
    - npm ci
    - npx vitest run --coverage --reporter=verbose
  coverage: '/^All files\s+\|\s+(\d+\.?\d+)/'  # Regex extraction % pour GitLab
  artifacts:
    when: always
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml   # Requiert reporter: 'cobertura'
    paths:
      - coverage/
    expire_in: 30 days

# Job séparé pour déployer le rapport HTML sur GitLab Pages
pages:
  stage: report
  dependencies:
    - test
  script:
    - mv coverage public
  artifacts:
    paths:
      - public
  only:
    - main
```

```typescript title="TypeScript — vite.config.ts : ajouter Cobertura pour GitLab"
// Ajouter 'cobertura' aux reporters pour GitLab CI :
coverage: {
    reporter: ['text', 'html', 'lcov', 'cobertura'],  // ← Ajout
}
```

<br>

---

## 5. Bonnes Pratiques CI

```javascript title="JavaScript — Organiser les tests pour la CI"
// ─── Marquer les tests lents pour les exclure en CI rapide ─────────────────
describe('tests critiques (toujours en CI)', () => {
    it('calcule le prix correctement', () => {
        expect(applyDiscount(100, 20)).toBe(80);
    });
});

describe('tests d\'intégration (CI nightly uniquement)', () => {
    it.skipIf(process.env.CI === 'fast')('génère un PDF réel', async () => {
        const pdf = await generateRealPdf(invoice);
        expect(pdf.pages).toBe(2);
    });
});

// ─── Variables d'environnement en CI ─────────────────────────────────────────
// vite.config.ts : via env files
// tests/setup.ts :
import { config } from 'dotenv';
config({ path: '.env.test' });           // Charger .env.test pour les tests
```

```bash title="Bash — Scripts npm optimisés CI vs Dev"
# package.json
# "test"          : "vitest"                         ← Mode watch dev
# "test:run"      : "vitest run"                     ← CI, une passe
# "test:fast"     : "vitest run --threads=4"         ← CI rapide, parallèle
# "test:coverage" : "vitest run --coverage"          ← CI avec rapport
# "test:changed"  : "vitest run --changed"           ← Seulement les fichiers modifiés

# En CI, bannir les .only oubliés :
# npx vitest run --forbid-only
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Pipeline CI complet**

```yaml title="YAML — Exercice 1 : créer un workflow GitHub Actions pour votre projet"
# 1. Créer .github/workflows/test.yml
# 2. Configurer :
#    - Déclenchement sur push (main) et pull_request
#    - Node.js 20 avec cache npm
#    - npm ci + vitest run --coverage
#    - Seuils : 80% lignes, 70% branches
#    - Upload du rapport HTML en artifact
# 3. Pusher et vérifier que la CI passe
# 4. Ajouter un badge dans README.md
# 5. Introduire un bug volontaire → vérifier que la CI échoue
```

**Exercice 2 — Seuils par fichier**

```typescript title="TypeScript — Exercice 2 : stratégie de seuils différenciée"
// 1. Configurez des seuils stricts (100%) sur src/services/payment.ts
// 2. Seuil standard (80%) sur le reste
// 3. Vérifiez que retirer un test du fichier payment.ts
//    fait échouer le build même si le seuil global est ok
// 4. Ajoutez un -- fichier src/utils/debug.ts contenant du code de debug
//    et configurez-le pour l'exclure du coverage
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La configuration coverage se fait dans `vite.config.ts` avec le provider **v8** (rapide, aucune dépendance externe). Les **seuils** (`thresholds`) bloquent le build si la couverture descend trop bas — les définir par fichier pour le code critique. En CI, toujours utiliser **`vitest run`** (pas `vitest` en mode watch) avec `npm ci` (pas `npm install`). Le rapport **LCOV** s'intègre avec Codecov, Coveralls et SonarQube. Le rapport **Cobertura** est le format natif de GitLab CI. Activer `all: true` dans coverage pour voir les fichiers avec 0% de couverture — souvent révélateur.

> **Formation Vitest complète.** Retour à l'[index Tests & Qualité →](../index.md) ou continuer avec [Cypress →](../cypress/index.md).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La maîtrise de ces concepts de développement moderne est cruciale pour construire des applications scalables, maintenables et sécurisées.

> [Retour à l'index →](./index.md)
