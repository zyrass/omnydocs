---
description: "Vitest 01 — Introduction et configuration : installer Vitest dans un projet Vite, configurer vitest.config.ts, comprendre le mode watch."
icon: lucide/settings
tags: ["VITEST", "VITE", "CONFIGURATION", "SETUP", "JAVASCRIPT"]
---

# Module 01 — Introduction & Configuration

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Vitest 1.x"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Filet de Sécurité du Trapéziste"
    Un trapéziste professionnel travaille toujours avec un filet — pas parce qu'il compte tomber, mais parce que le filet lui permet d'essayer des figures plus audacieuses. Vitest est ce filet pour votre code JavaScript : il vous permet de refactoriser, d'ajouter des fonctionnalités, de modifier des algorithmes sans craindre de casser ce qui fonctionnait. Sans filet, on ne tente rien de risqué.

**Vitest** est un framework de tests unitaires construit sur **Vite**. Il partage la configuration (`vite.config.ts`) et le pipeline de transformation du projet — pas de config séparée à maintenir. Il est compatible avec l'API Jest : si vous connaissez Jest, vous êtes opérationnel en 10 minutes.

<br>

---

## 1. Installation

```bash title="Bash — Ajouter Vitest à un projet Vite existant"
# Dans un projet Vite existant (Vue, React, ou Vanilla)
npm install -D vitest

# Avec les extensions recommandées :
npm install -D vitest @vitest/ui happy-dom

# @vitest/ui  → Interface graphique (http://localhost:51204)
# happy-dom   → Émulation DOM légère pour les tests de composants
# jsdom       → Alternative à happy-dom, plus complète (React)

# Pour les tests de composants Vue :
npm install -D @vue/test-utils

# Pour les tests de composants React :
npm install -D @testing-library/react @testing-library/jest-dom
```

```bash title="Bash — Structure recommandée"
# Les fichiers de tests cohabitent avec le code :
src/
├── utils/
│   ├── currency.js
│   └── currency.test.js     ← Test colocalisé
├── services/
│   ├── api.js
│   └── api.test.js
└── components/
    ├── Button.vue
    └── Button.test.js

# Ou dans un dossier séparé :
tests/
├── unit/
│   ├── currency.test.js
│   └── api.test.js
└── integration/
    └── checkout.test.js
```

<br>

---

## 2. Configuration

```typescript title="TypeScript — vite.config.ts : ajouter Vitest à la config Vite"
// vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';     // ou react(), etc.

export default defineConfig({
    plugins: [vue()],

    test: {
        // ─── Environnement DOM ─────────────────────────────────────────────────
        environment: 'happy-dom',          // 'jsdom' ou 'node' (défaut)

        // ─── Globals : describe/it/expect disponibles sans import ──────────────
        globals: true,                     // Évite d'importer describe, it, expect

        // ─── Setup files (exécutés avant chaque fichier test) ─────────────────
        setupFiles: ['./tests/setup.ts'],

        // ─── Fichiers à inclure / exclure ─────────────────────────────────────
        include: ['src/**/*.{test,spec}.{js,ts}', 'tests/**/*.{test,spec}.{js,ts}'],
        exclude: ['node_modules', 'dist', 'e2e/**'],

        // ─── Coverage ─────────────────────────────────────────────────────────
        coverage: {
            provider: 'v8',                 // 'v8' (rapide) ou 'istanbul'
            reporter: ['text', 'html', 'lcov'],
            include: ['src/**/*.{js,ts,vue}'],
            exclude: ['src/main.ts', 'src/**/*.d.ts'],
            thresholds: {
                lines:     80,
                functions: 80,
                branches:  70,
                statements: 80,
            }
        },

        // ─── Timeout ──────────────────────────────────────────────────────────
        testTimeout: 10_000,               // 10 secondes max par test
        hookTimeout:  5_000,
    },
});
```

```typescript title="TypeScript — tests/setup.ts : configuration globale des tests"
// tests/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { cleanup } from '@testing-library/react';  // Si React
// import { config } from '@vue/test-utils';       // Si Vue

// Nettoyage du DOM après chaque test (React)
afterEach(() => cleanup());

// Variables d'environnement pour les tests
beforeAll(() => {
    process.env.VITE_API_URL = 'http://localhost:3000';
});
```

```json title="JSON — package.json : scripts Vitest"
{
    "scripts": {
        "test":           "vitest",
        "test:run":       "vitest run",
        "test:watch":     "vitest --watch",
        "test:ui":        "vitest --ui",
        "test:coverage":  "vitest run --coverage",
        "test:changed":   "vitest run --changed HEAD~1"
    }
}
```

<br>

---

## 3. Modes d'Exécution

```bash title="Bash — Lancer Vitest selon le contexte"
# ─── Mode watch (développement) ───────────────────────────────────────────────
npm test
# ou : npx vitest
# Relance automatiquement les tests affectés par vos modifications.

# ─── Mode run (CI/CD, une seule exécution) ────────────────────────────────────
npm run test:run
# ou : npx vitest run
# Pas de mode watch — s'arrête après les tests.

# ─── Interface graphique ──────────────────────────────────────────────────────
npm run test:ui
# Ouvre http://localhost:51204 : vue graphique des tests, coverage, etc.

# ─── Filtrer les tests ────────────────────────────────────────────────────────
npx vitest run currency          # Seulement les fichiers matchant "currency"
npx vitest run --testNamePattern "format"  # Seulement les tests dont le nom contient "format"

# ─── Coverage ─────────────────────────────────────────────────────────────────
npm run test:coverage
# Génère coverage/index.html (ouvrir dans le navigateur)
```

### Mode Watch — Navigation

```
Mode Watch Vitest :
┌─────────────────────────────────────────────────────────┐
│  WATCH Usage                                            │
│                                                         │
│  › Press a to run all tests.                            │
│  › Press f to run only failed tests.                    │
│  › Press p to filter by a filename /regex/.             │
│  › Press t to filter by a test name /regex/.            │
│  › Press u to update snapshots.                         │
│  › Press q to quit.                                     │
└─────────────────────────────────────────────────────────┘
```

<br>

---

## 4. Premier Test

```javascript title="JavaScript — Premier test Vitest (avec globals: true)"
// src/utils/currency.js
export function formatPrice(amount, currency = 'EUR') {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency,
        minimumFractionDigits: 2,
    }).format(amount);
}

export function applyDiscount(price, discountPercent) {
    if (discountPercent < 0 || discountPercent > 100) {
        throw new RangeError('Le pourcentage doit être entre 0 et 100');
    }
    return Math.round(price * (1 - discountPercent / 100) * 100) / 100;
}
```

```javascript title="JavaScript — currency.test.js : premiers tests Vitest"
// src/utils/currency.test.js
// Avec globals: true dans vitest.config.ts, pas besoin d'importer describe/it/expect
import { formatPrice, applyDiscount } from './currency';

describe('formatPrice()', () => {
    it('formate un montant en euros par défaut', () => {
        expect(formatPrice(1234.5)).toBe('1 234,50 €');
    });

    it('formate en dollars USD', () => {
        expect(formatPrice(99.99, 'USD')).toContain('99,99');
    });

    it('gère zéro correctement', () => {
        expect(formatPrice(0)).toBe('0,00 €');
    });
});

describe('applyDiscount()', () => {
    it('applique une réduction de 20%', () => {
        expect(applyDiscount(100, 20)).toBe(80);
    });

    it('ne modifie pas le prix à 0%', () => {
        expect(applyDiscount(100, 0)).toBe(100);
    });

    it('retourne 0 pour une réduction de 100%', () => {
        expect(applyDiscount(100, 100)).toBe(0);
    });

    it('lève une erreur si la réduction est négative', () => {
        expect(() => applyDiscount(100, -10)).toThrow(RangeError);
        expect(() => applyDiscount(100, -10)).toThrow('entre 0 et 100');
    });

    it('lève une erreur si la réduction dépasse 100%', () => {
        expect(() => applyDiscount(100, 101)).toThrow(RangeError);
    });

    it('arrondit à 2 décimales', () => {
        expect(applyDiscount(100, 33)).toBe(67);
        expect(applyDiscount(10,  3)).toBe(9.7);
    });
});
```

```bash title="Bash — Lancer et lire le résultat"
npm test

# Output attendu :
# ✓ src/utils/currency.test.js (8)
#   ✓ formatPrice() (3)
#     ✓ formate un montant en euros par défaut
#     ✓ formate en dollars USD
#     ✓ gère zéro correctement
#   ✓ applyDiscount() (5)
#     ✓ applique une réduction de 20%
#     ...
#
# Test Files  1 passed (1)
# Tests       8 passed (8)
# Duration    312ms
```

<br>

---

## 5. Configuration TypeScript

```typescript title="TypeScript — currency.ts + currency.test.ts"
// src/utils/currency.ts
export function applyDiscount(price: number, discountPercent: number): number {
    if (discountPercent < 0 || discountPercent > 100) {
        throw new RangeError('Le pourcentage doit être entre 0 et 100');
    }
    return Math.round(price * (1 - discountPercent / 100) * 100) / 100;
}

// src/utils/currency.test.ts
// Vitest est TypeScript-first : aucune config supplémentaire nécessaire
import { describe, it, expect } from 'vitest';  // Ou globals: true
import { applyDiscount }         from './currency';

describe('applyDiscount()', () => {
    it('applique une réduction', () => {
        const result: number = applyDiscount(100, 20);
        expect(result).toBe(80);
    });
});
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Setup complet**

```bash title="Bash — Exercice 1 : configurer Vitest sur un projet existant"
# 1. Créer un projet Vite vanilla :
npm create vite@latest vitest-practice -- --template vanilla

# 2. Installer Vitest avec globals et happy-dom
# 3. Configurer vite.config.js (environment: 'happy-dom', globals: true)
# 4. Créer src/utils/math.js avec 4 fonctions : add, subtract, multiply, divide
# 5. Écrire les tests pour chaque fonction (au moins 3 cas par fonction)
# 6. Vérifier que npm test passe tout au vert
```

**Exercice 2 — Cas limites**

```javascript title="JavaScript — Exercice 2 : tester des cas limites difficiles"
// Pour la fonction slugify(text: string): string qui convertit un titre en slug :
// - "Hello World" → "hello-world"
// - "L'été en France !" → "l-ete-en-france"
// - "  Espaces  " → "espaces"
// Testez au moins 8 cas : accents, apostrophes, chiffres, caractères spéciaux,
// chaîne vide, chaîne uniquement d'espaces, chaîne avec emojis.
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Vitest s'installe en une commande et partage la config Vite existante — pas de double configuration. `globals: true` évite les imports répétés dans chaque fichier. Le **mode watch** est le mode de travail normal : il relance uniquement les tests affectés par vos changements. TypeScript fonctionne nativement sans configuration supplémentaire.

> Module suivant : [Écrire des Tests →](./02-ecrire-des-tests.md) — `describe`, `it`, `expect`, matchers avancés, `beforeEach`, snapshots.

<br>
