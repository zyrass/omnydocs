---
description: "Vitest 02 — Écrire des tests : matchers, structure describe/it, lifecycle hooks, tests async, snapshots et data-driven tests."
icon: lucide/pencil-line
tags: ["VITEST", "MATCHERS", "DESCRIBE", "SNAPSHOT", "ASYNC", "TESTING"]
---

# Module 02 — Écrire des Tests

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Vitest 1.x"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Recette de Cuisine"
    Une recette bien écrite ne dit pas juste "faire cuire" : elle précise la température, le temps, la texture attendue. Un bon test ne dit pas juste "ça marche" : il précise exactement quel résultat est attendu, dans quelles conditions, avec quels ingrédients de départ. Plus le test est précis, plus il détecte les régressions tôt.

Ce module couvre les outils pour écrire des tests expressifs, précis et maintenables avec Vitest.

<br>

---

## 1. Structure de Base

```javascript title="JavaScript — Structure describe / it / expect"
import { describe, it, expect, beforeEach, afterEach, beforeAll, afterAll } from 'vitest';

// describe() : groupe logique de tests (peut être imbriqué)
describe('ShoppingCart', () => {

    // beforeAll  : exécuté UNE FOIS avant tous les tests du groupe
    // afterAll   : exécuté UNE FOIS après tous les tests du groupe
    // beforeEach : exécuté AVANT CHAQUE test
    // afterEach  : exécuté APRÈS CHAQUE test

    let cart;

    beforeEach(() => {
        cart = new ShoppingCart();    // Réinitialiser pour chaque test
    });

    // it() / test() : identiques, préférence stylistique
    it('démarre vide', () => {
        expect(cart.count()).toBe(0);
    });

    it('ajoute un produit', () => {
        cart.add({ id: 1, name: 'Livre', price: 29.99 });
        expect(cart.count()).toBe(1);
        expect(cart.total()).toBe(29.99);
    });

    // Tests imbriqués
    describe('removing items', () => {
        beforeEach(() => {
            cart.add({ id: 1, name: 'Livre', price: 29.99 });
        });

        it('supprime un produit existant', () => {
            cart.remove(1);
            expect(cart.count()).toBe(0);
        });

        it('ignore la suppression d\'un produit absent', () => {
            expect(() => cart.remove(999)).not.toThrow();
            expect(cart.count()).toBe(1);   // Toujours 1 item
        });
    });
});
```

<br>

---

## 2. Matchers Vitest — Référence Complète

```javascript title="JavaScript — Matchers : égalité, types, valeurs"
// ─── Égalité ──────────────────────────────────────────────────────────────────
expect(2 + 2).toBe(4);               // Égalité stricte (===)
expect({ a: 1 }).toEqual({ a: 1 }); // Égalité profonde (objets/tableaux)
expect({ a: 1 }).toStrictEqual({ a: 1 }); // Comme toEqual + vérifie les sparse arrays

expect(42).not.toBe(43);            // Négation avec .not

// ─── Valeurs spéciales ────────────────────────────────────────────────────────
expect(null).toBeNull();
expect(undefined).toBeUndefined();
expect('hello').toBeDefined();
expect(true).toBeTruthy();
expect(0).toBeFalsy();
expect(NaN).toBeNaN();

// ─── Nombres ──────────────────────────────────────────────────────────────────
expect(3).toBeGreaterThan(2);
expect(3).toBeGreaterThanOrEqual(3);
expect(2).toBeLessThan(3);
expect(3.14159).toBeCloseTo(3.14, 2);  // Précision de 2 décimales

// ─── Chaînes ──────────────────────────────────────────────────────────────────
expect('Hello World').toContain('World');
expect('hello@example.com').toMatch(/^[\w.]+@[\w.]+\.\w+$/);
expect('Hello').toHaveLength(5);

// ─── Tableaux ─────────────────────────────────────────────────────────────────
expect([1, 2, 3]).toContain(2);
expect([1, 2, 3]).toHaveLength(3);
expect([{ id: 1 }, { id: 2 }]).toContainEqual({ id: 1 });
expect([1, 2, 3]).toEqual(expect.arrayContaining([1, 3])); // Contient au moins ces éléments

// ─── Objets ───────────────────────────────────────────────────────────────────
expect({ a: 1, b: 2 }).toHaveProperty('a');
expect({ a: 1, b: 2 }).toHaveProperty('a', 1);
expect({ user: { name: 'Alice' }}).toHaveProperty('user.name', 'Alice');
expect({ a: 1, b: 2, c: 3 }).toMatchObject({ a: 1, b: 2 }); // Sous-ensemble

// ─── Exceptions ───────────────────────────────────────────────────────────────
expect(() => JSON.parse('invalid')).toThrow();
expect(() => JSON.parse('invalid')).toThrow(SyntaxError);
expect(() => { throw new Error('oops') }).toThrow('oops');

// ─── Fonctions et spies ───────────────────────────────────────────────────────
const fn = vi.fn();
fn('hello');
expect(fn).toHaveBeenCalled();
expect(fn).toHaveBeenCalledWith('hello');
expect(fn).toHaveBeenCalledTimes(1);
```

<br>

---

## 3. Tests Asynchrones

```javascript title="JavaScript — Tests async : Promises, async/await, rejections"
import { describe, it, expect } from 'vitest';
import { fetchUser, fetchWithTimeout } from './api';

describe('API async tests', () => {

    // ─── async/await (recommandé) ──────────────────────────────────────────────
    it('retourne un utilisateur valide', async () => {
        const user = await fetchUser(1);

        expect(user).toMatchObject({
            id:    1,
            name:  expect.any(String),
            email: expect.stringMatching(/@/),
        });
    });

    // ─── Tester une Promise rejetée ────────────────────────────────────────────
    it('rejette si l\'utilisateur n\'existe pas', async () => {
        await expect(fetchUser(9999)).rejects.toThrow('User not found');
        // ou :
        await expect(fetchUser(9999)).rejects.toMatchObject({ status: 404 });
    });

    // ─── Résolution attendue ──────────────────────────────────────────────────
    it('résout avec les bonnes données', async () => {
        await expect(fetchUser(1)).resolves.toHaveProperty('name');
    });

    // ─── Timers : vi.useFakeTimers ─────────────────────────────────────────────
    it('exécute le callback après le délai', () => {
        vi.useFakeTimers();
        const callback = vi.fn();

        setTimeout(callback, 1000);

        expect(callback).not.toHaveBeenCalled();
        vi.advanceTimersByTime(1000);
        expect(callback).toHaveBeenCalledTimes(1);

        vi.useRealTimers();   // Restaurer les vrais timers
    });

    // ─── Timeout personnalisé ─────────────────────────────────────────────────
    it('timeout long pour une opération réseau réelle', async () => {
        const result = await fetchWithTimeout(30_000);
        expect(result).toBeDefined();
    }, 35_000);  // Timeout du test : 35 secondes
});
```

<br>

---

## 4. Tests Data-Driven : `it.each`

```javascript title="JavaScript — it.each : tester de multiples cas avec le même test"
// ─── Tableau de tuples ────────────────────────────────────────────────────────
it.each([
    [0,   0,   0  ],
    [1,   2,   3  ],
    [100, 50,  150],
    [-1,  1,   0  ],
])('add(%i, %i) retourne %i', (a, b, expected) => {
    expect(add(a, b)).toBe(expected);
});

// ─── Tableau d'objets (plus lisible) ─────────────────────────────────────────
it.each([
    { input: 100, percent: 20,  expected: 80  },
    { input: 100, percent: 0,   expected: 100 },
    { input: 100, percent: 100, expected: 0   },
    { input: 50,  percent: 10,  expected: 45  },
])('applyDiscount($input, $percent%) → $expected', ({ input, percent, expected }) => {
    expect(applyDiscount(input, percent)).toBe(expected);
});

// ─── Template literal (nommage dans le titre) ─────────────────────────────────
describe.each([
    ['production', { debug: false, logLevel: 'error' }],
    ['development', { debug: true,  logLevel: 'debug' }],
    ['test',        { debug: false, logLevel: 'silent' }],
])('Config dans l\'environnement %s', (env, expectedConfig) => {
    it('a les bons paramètres', () => {
        process.env.NODE_ENV = env;
        expect(getConfig()).toMatchObject(expectedConfig);
    });
});
```

<br>

---

## 5. Snapshots

```javascript title="JavaScript — Snapshots : capturer et comparer des sorties complexes"
import { expect, it, describe } from 'vitest';
import { renderArticleHTML, buildNavMenu } from './renderer';

describe('Snapshot tests', () => {

    // Premier lancement : crée le fichier *.snap
    // Lancement suivants : compare avec le snapshot existant
    it('génère le bon HTML pour un article', () => {
        const html = renderArticleHTML({
            title:   'Mon Article',
            content: 'Contenu de l\'article.',
            author:  'Alice',
        });

        expect(html).toMatchSnapshot();
    });

    // Snapshot inline (dans le fichier test lui-même)
    it('génère le menu de navigation', () => {
        const menu = buildNavMenu(['Accueil', 'Blog', 'Contact']);

        expect(menu).toMatchInlineSnapshot(`
            "<nav>
              <a href='/'>Accueil</a>
              <a href='/blog'>Blog</a>
              <a href='/contact'>Contact</a>
            </nav>"
        `);
    });
});
```

```bash title="Bash — Gérer les snapshots"
# Mettre à jour les snapshots (après un changement intentionnel)
npx vitest --update-snapshots
# ou dans le mode watch : appuyer sur 'u'

# Les snapshots sont stockés dans :
# src/utils/__snapshots__/renderer.test.js.snap
```

<br>

---

## 6. Tests Conditionnels et Skip

```javascript title="JavaScript — Contrôle d'exécution des tests"
// ─── Skip : ignorer temporairement ───────────────────────────────────────────
it.skip('ce test est en cours de développement', () => {
    // Ne sera pas exécuté — mais apparaît dans le rapport comme "skipped"
});

// ─── Only : exécuter seulement ce test ────────────────────────────────────────
it.only('je debug uniquement ce test', () => {
    // En mode watch, seul ce test tourne
    // ATTENTION : ne jamais committer avec .only
});

// ─── Conditional skip ─────────────────────────────────────────────────────────
it.skipIf(process.env.CI === 'true')('test local seulement', () => {
    // Ignoré en CI, lancé en local
});

it.runIf(process.platform === 'win32')('test Windows seulement', () => {
    // Lancé uniquement sur Windows
});

// ─── todo : marquer un test à écrire ─────────────────────────────────────────
it.todo('vérifier la pagination au-delà de 1000 items');
it.todo('tester avec des caractères Unicode exotiques');
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Suite de tests complète**

```javascript title="JavaScript — Exercice 1 : écrire une suite complète pour FormValidator"
// Créez un FormValidator avec les méthodes :
// - validate(field, value, rules) → { valid: bool, errors: string[] }
// - Règles : required, minLength(n), maxLength(n), email, numeric

// Écrivez les tests avec :
// 1. describe imbriqués (un par règle)
// 2. beforeEach pour réinitialiser le validator
// 3. it.each pour les cas valides et invalides de chaque règle
// 4. Tests pour les combinaisons de règles
// 5. Au moins 20 assertions au total
```

**Exercice 2 — Tests asynchrones**

```javascript title="JavaScript — Exercice 2 : tester un client API avec fetch mocké"
// Créez un ApiClient avec getUser(id), createPost(data)
// Utilisez vi.fn() pour mocker fetch
// Testez :
// 1. Succès HTTP 200 → retourne les données
// 2. Erreur HTTP 404 → rejette avec le bon message
// 3. Erreur réseau (fetch throw) → rejette correctement
// 4. Headers d'authentification correctement ajoutés
// Utilisez vi.useFakeTimers() pour tester un retry automatique
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La structure **describe → it → expect** est universelle (même API que Jest). Les **matchers** couvrent tous les cas courants — ne pas réinventer avec des assertions manuelles. **it.each** élimine les tests copié-collé pour les cas multiples. Les tests **async/await** s'écrivent exactement comme du code asynchrone normal. Les **snapshots** sont puissants pour les sorties complexes mais doivent être révisés à chaque mise à jour intentionnelle.

> Module suivant : [Mocking & Spies →](./03-mocking.md) — isoler les dépendances (API, modules, timers, Window).

<br>
