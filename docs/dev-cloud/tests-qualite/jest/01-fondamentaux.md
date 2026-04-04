---
description: "Jest 01 — Fondamentaux : installation, describe/test/expect, matchers, setup/teardown, tests async, coverage."
icon: lucide/book-open-check
tags: ["JEST", "JAVASCRIPT", "TESTS-UNITAIRES", "MATCHERS", "COVERAGE", "ASYNC"]
---

# Module 01 — Fondamentaux Jest

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Jest 29.x / Node.js 18+"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Technicien Qualité"
    Dans une usine automobile, un technicien QA vérifie chaque composant avant l'assemblage : le moteur démarre-t-il ? Les freins répondent-ils correctement ? Chaque test Jest est une vérification de ce type : isolée, précise, reproductible. Avant que l'assemblage complet (l'intégration) soit testé, chaque pièce doit être validée individuellement. Jest est le technicien QA de votre code JavaScript.

<br>

---

## 1. Installation

```bash title="Bash — Installer Jest dans un projet JavaScript"
# Projet Node.js
npm install --save-dev jest

# Avec support TypeScript
npm install --save-dev jest @types/jest ts-jest typescript

# Avec support ESM (modules modernes)
npm install --save-dev jest babel-jest @babel/preset-env
```

```json title="JSON — package.json : configuration Jest de base"
{
  "scripts": {
    "test":          "jest",
    "test:watch":    "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "testEnvironment": "node",
    "transform": {
      "^.+\\.ts$": "ts-jest"
    },
    "coverageDirectory": "coverage",
    "collectCoverageFrom": ["src/**/*.{js,ts}", "!src/**/*.d.ts"]
  }
}
```

```javascript title="JavaScript — jest.config.js : configuration avancée"
/** @type {import('jest').Config} */
const config = {
    // Environnement d'exécution
    testEnvironment:   'node',     // 'node' ou 'jsdom' (pour React/DOM)

    // Patterns de fichiers de test
    testMatch: [
        '**/__tests__/**/*.{js,ts}',
        '**/*.{spec,test}.{js,ts}'
    ],

    // Transform (TypeScript)
    transform: {
        '^.+\\.tsx?$': 'ts-jest',
    },

    // Alias de modules (@/ → src/)
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/src/$1',
    },

    // Setup avant chaque fichier de test
    setupFilesAfterFramework: ['<rootDir>/jest.setup.js'],

    // Couverture
    collectCoverageFrom: ['src/**/*.{js,ts}'],
    coverageThreshold: {
        global: {
            branches:   80,
            functions:  80,
            lines:      80,
            statements: 80,
        },
    },
};

module.exports = config;
```

<br>

---

## 2. Structure : `describe`, `test`, `it`

```javascript title="JavaScript — Structure de base d'un fichier de test"
// src/__tests__/calculatrice.test.js

// describe() : groupe logique de tests (une classe, une fonction, un module)
describe('Calculatrice', () => {

    // test() et it() sont identiques — utilisez celui que vous préférez
    test('additionne deux nombres positifs', () => {
        expect(add(2, 3)).toBe(5);
    });

    it('soustrait correctement', () => {
        expect(subtract(10, 4)).toBe(6);
    });

    // describe imbriqué : sous-groupe
    describe('division', () => {

        test('divise correctement', () => {
            expect(divide(10, 2)).toBe(5);
        });

        test('lève une erreur si division par zéro', () => {
            expect(() => divide(10, 0)).toThrow('Division par zéro');
        });
    });
});
```

```javascript title="JavaScript — Code source à tester : src/calculatrice.js"
/**
 * Addition de deux nombres.
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    if (b === 0) throw new Error('Division par zéro');
    return a / b;
}

module.exports = { add, subtract, multiply, divide };
```

<br>

---

## 3. Matchers — Les Assertions

```javascript title="JavaScript — Matchers Jest : égalité, valeurs, tableaux, objets"
describe('Matchers Jest', () => {

    // ─── Égalité ──────────────────────────────────────────────────────────────
    test('égalité stricte', () => {
        expect(2 + 2).toBe(4);              // Strictement égal (===)
        expect({ a: 1 }).toEqual({ a: 1 }); // Égalité profonde (différent de toBe pour les objets)
        expect([1, 2, 3]).toEqual([1, 2, 3]);
    });

    // ─── Valeurs spéciales ────────────────────────────────────────────────────
    test('valeurs truthy/falsy', () => {
        expect(null).toBeNull();
        expect(undefined).toBeUndefined();
        expect('hello').toBeDefined();
        expect(1).toBeTruthy();
        expect(0).toBeFalsy();
        expect(null).toBeFalsy();
    });

    // ─── Nombres ──────────────────────────────────────────────────────────────
    test('comparaisons numériques', () => {
        expect(10).toBeGreaterThan(5);
        expect(5).toBeLessThan(10);
        expect(10).toBeGreaterThanOrEqual(10);
        // Float : utiliser toBeCloseTo (évite les erreurs de précision)
        expect(0.1 + 0.2).toBeCloseTo(0.3, 5);
    });

    // ─── Chaînes ──────────────────────────────────────────────────────────────
    test('chaînes de caractères', () => {
        expect('Hello World').toContain('World');
        expect('user@example.com').toMatch(/^[\w.]+@[\w.]+\.\w+$/);
        expect('Hello').toHaveLength(5);
    });

    // ─── Tableaux ─────────────────────────────────────────────────────────────
    test('tableaux', () => {
        const fruits = ['apple', 'banana', 'orange'];
        expect(fruits).toContain('banana');
        expect(fruits).toHaveLength(3);
        expect(fruits).toEqual(expect.arrayContaining(['apple', 'orange']));
    });

    // ─── Objets ───────────────────────────────────────────────────────────────
    test('objets', () => {
        const user = { id: 1, name: 'Alice', role: 'admin' };
        expect(user).toHaveProperty('name');
        expect(user).toHaveProperty('role', 'admin');      // Valeur précise
        expect(user).toMatchObject({ name: 'Alice' });     // Sous-ensemble
    });

    // ─── Exceptions ───────────────────────────────────────────────────────────
    test('exceptions', () => {
        expect(() => { throw new Error('Oops !'); }).toThrow();
        expect(() => { throw new Error('Oops !'); }).toThrow('Oops !');
        expect(() => { throw new Error('Oops !'); }).toThrow(Error);
    });

    // ─── Négation ─────────────────────────────────────────────────────────────
    test('négation avec .not', () => {
        expect(5).not.toBe(10);
        expect('hello').not.toContain('world');
        expect([]).not.toContain('apple');
    });
});
```

<br>

---

## 4. Setup & Teardown

```javascript title="JavaScript — Hooks Jest : beforeAll, beforeEach, afterEach, afterAll"
describe('Base de données', () => {
    let db;

    // Exécuté UNE FOIS avant tous les tests du describe
    beforeAll(async () => {
        db = await Database.connect('sqlite::memory:');
        await db.migrate();
    });

    // Exécuté avant CHAQUE test
    beforeEach(async () => {
        await db.seed();    // Remettre des données propres avant chaque test
    });

    // Exécuté après CHAQUE test
    afterEach(async () => {
        await db.clean();   // Nettoyer après chaque test
    });

    // Exécuté UNE FOIS après tous les tests du describe
    afterAll(async () => {
        await db.disconnect();
    });

    test('trouve un utilisateur par ID', async () => {
        const user = await db.users.findById(1);
        expect(user).toMatchObject({ id: 1, name: 'Alice' });
    });

    test('liste tous les utilisateurs', async () => {
        const users = await db.users.findAll();
        expect(users).toHaveLength(3);
    });
});
```

<br>

---

## 5. Tests Asynchrones

```javascript title="JavaScript — Tester du code asynchrone (async/await, Promises)"
// ─── Async/Await (méthode recommandée) ───────────────────────────────────────
describe('API Utilisateurs', () => {

    test('récupère un utilisateur', async () => {
        const user = await fetchUser(1);
        expect(user).toMatchObject({ id: 1, name: 'Alice' });
    });

    test('lève une exception si utilisateur introuvable', async () => {
        await expect(fetchUser(999)).rejects.toThrow('User not found');
    });
});

// ─── Promises (alternative) ──────────────────────────────────────────────────
test('résout correctement (Promise)', () => {
    // IMPORTANT : retourner la Promise, sinon Jest n'attend pas
    return expect(fetchUser(1)).resolves.toMatchObject({ id: 1 });
});

// ─── done callback (legacy, à éviter) ────────────────────────────────────────
test('callback (legacy)', (done) => {
    fetchUserCallback(1, (error, user) => {
        expect(error).toBeNull();
        expect(user.id).toBe(1);
        done();   // Signaler à Jest que le test est terminé
    });
});
```

<br>

---

## 6. Coverage

```bash title="Bash — Générer le rapport de couverture"
# Rapport dans le terminal
npx jest --coverage

# Rapport HTML (ouvrir coverage/lcov-report/index.html)
npx jest --coverage --coverageReporters=lcov

# Sortie Console :
# ------------------|---------|----------|---------|---------|
# File              | % Stmts | % Branch | % Funcs | % Lines |
# ------------------|---------|----------|---------|---------|
# calculatrice.js   |   95.23 |    87.50 |     100 |   95.23 |
# ------------------|---------|----------|---------|---------|
```

!!! tip "Interprétation de la couverture"
    - **Statements** : lignes de code exécutées
    - **Branches** : chemins conditionnels (if/else, ternaire) couverts
    - **Functions** : fonctions appelées au moins une fois
    - **Lines** : lignes exécutées (souvent proche de Statements)
    
    Une couverture à **80%** est l'objectif minimum professionnel. 100% n'est pas toujours réaliste ni utile.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un test Jest suit la structure **AAA** : **Arrange** (préparer les données), **Act** (exécuter la fonction), **Assert** (vérifier le résultat). `describe()` groupe les tests, `test()` / `it()` définit un cas de test. `expect(valeur).matcher()` est la syntaxe d'assertion. Pour l'async : **toujours** utiliser `async/await` ou retourner la Promise. Les hooks `beforeAll/beforeEach/afterAll/afterEach` gèrent le cycle de vie des tests.

> Module suivant : [Mocking Avancé →](./02-mocking-avance.md) — `jest.fn()`, `jest.mock()`, spies, timers et modules.

<br>
