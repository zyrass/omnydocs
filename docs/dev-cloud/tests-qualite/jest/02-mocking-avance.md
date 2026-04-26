---
description: "Jest 02 — Mocking avancé : jest.fn(), jest.mock(), jest.spyOn(), timers virtuels et isolation de modules."
icon: lucide/book-open-check
tags: ["JEST", "MOCKING", "SPIES", "MODULES", "TIMERS", "ISOLATION"]
---

# Module 02 — Mocking Avancé

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Jest 29.x"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Les Doublures de Cinéma"
    Dans un film d'action, le héros ne saute pas vraiment d'un immeuble — une doublure le fait. Les mocks Jest fonctionnent de la même façon : ce sont des **doublures** de vos dépendances réelles (base de données, API, système de fichiers). Elles jouent le rôle de la vraie dépendance sans les risques et la lenteur. Vous contrôlez ce que la doublure "retourne" et vous pouvez vérifier si elle a été "appelée en scène".

<br>

---

## 1. `jest.fn()` — Fonctions Mockées

```javascript title="JavaScript — jest.fn() : créer et contrôler une fonction mock"
describe('jest.fn() — Fonctions mock', () => {

    // ─── Créer un mock ────────────────────────────────────────────────────────
    test('crée une fonction mock basique', () => {
        const mockFn = jest.fn();

        mockFn('arg1', 'arg2');

        expect(mockFn).toHaveBeenCalled();
        expect(mockFn).toHaveBeenCalledTimes(1);
        expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
    });

    // ─── Retourner une valeur ─────────────────────────────────────────────────
    test('retourne une valeur définie', () => {
        const getUser = jest.fn().mockReturnValue({ id: 1, name: 'Alice' });

        const user = getUser();
        expect(user).toEqual({ id: 1, name: 'Alice' });
    });

    // ─── Implémenter une logique ──────────────────────────────────────────────
    test('implémenter une logique personnalisée', () => {
        const add = jest.fn().mockImplementation((a, b) => a + b);

        expect(add(2, 3)).toBe(5);
        expect(add).toHaveBeenCalledWith(2, 3);
    });

    // ─── Retours multiples ────────────────────────────────────────────────────
    test('valeurs de retour différentes à chaque appel', () => {
        const fetchData = jest.fn()
            .mockReturnValueOnce({ status: 'loading' })  // 1er appel
            .mockReturnValueOnce({ status: 'success' })  // 2ème appel
            .mockReturnValue(  { status: 'idle' });       // Appels suivants

        expect(fetchData()).toEqual({ status: 'loading' });
        expect(fetchData()).toEqual({ status: 'success' });
        expect(fetchData()).toEqual({ status: 'idle' });
    });

    // ─── Mock async ───────────────────────────────────────────────────────────
    test('mock d\'une fonction asynchrone', async () => {
        const fetchUser = jest.fn()
            .mockResolvedValueOnce({ id: 1, name: 'Alice' })   // Résolution
            .mockRejectedValueOnce(new Error('Not found'));      // Rejet

        await expect(fetchUser(1)).resolves.toEqual({ id: 1, name: 'Alice' });
        await expect(fetchUser(999)).rejects.toThrow('Not found');
    });

    // ─── Vérifier les appels ──────────────────────────────────────────────────
    test('inspécter les appels d\'un mock', () => {
        const logger = jest.fn();
        logger('info', 'Message 1');
        logger('error', 'Message 2');

        // Tous les appels
        expect(logger.mock.calls).toEqual([
            ['info',  'Message 1'],
            ['error', 'Message 2'],
        ]);

        // Réinitialiser le mock entre les tests
        logger.mockClear();     // Remet à zéro calls, instances, results
        logger.mockReset();     // + Supprime les implémentations mockées
        logger.mockRestore();   // + Restaure l'implémentation originale (spyOn)
    });
});
```

<br>

---

## 2. `jest.mock()` — Mocker des Modules

```javascript title="JavaScript — jest.mock() : remplacer un module entier"
// src/__tests__/userService.test.js

// IMPORTANT : jest.mock() est hissé (hoisted) en haut du fichier par Babel/Jest
jest.mock('../services/emailService');
jest.mock('axios');

import emailService from '../services/emailService';
import axios        from 'axios';
import { createUser } from '../userService';

describe('UserService', () => {

    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('envoie un email à la création d\'utilisateur', async () => {
        // Configurer le comportement des mocks
        axios.post.mockResolvedValue({ data: { id: 1, email: 'alice@example.com' } });
        emailService.sendWelcome.mockResolvedValue(true);

        // Exécuter le code à tester
        const user = await createUser({ name: 'Alice', email: 'alice@example.com' });

        // Vérifier que les dépendances ont été appelées correctement
        expect(axios.post).toHaveBeenCalledWith('/api/users', {
            name:  'Alice',
            email: 'alice@example.com',
        });
        expect(emailService.sendWelcome).toHaveBeenCalledWith('alice@example.com');
        expect(user.id).toBe(1);
    });

    test('lève une erreur si l\'API est indisponible', async () => {
        axios.post.mockRejectedValue(new Error('Network error'));

        await expect(createUser({ name: 'Bob', email: 'bob@example.com' }))
            .rejects.toThrow('Network error');

        expect(emailService.sendWelcome).not.toHaveBeenCalled();
    });
});
```

```javascript title="JavaScript — jest.mock() avec factory : contrôle total sur le module"
// Mocker avec une factory function (contrôle précis des exports)
jest.mock('../database', () => ({
    query: jest.fn(),
    connect: jest.fn().mockResolvedValue(true),
    disconnect: jest.fn().mockResolvedValue(true),
}));

// Ou pour un module avec default export
jest.mock('../utils/logger', () => ({
    __esModule: true,   // Important pour les modules ES
    default: {
        info:  jest.fn(),
        error: jest.fn(),
        warn:  jest.fn(),
    },
}));
```

<br>

---

## 3. `jest.spyOn()` — Espionner des Méthodes

```javascript title="JavaScript — jest.spyOn() : spy sans supprimer l'implémentation réelle"
describe('jest.spyOn()', () => {

    test('espionner une méthode réelle', () => {
        const calculator = { add: (a, b) => a + b };

        // spyOn : observe + garde l'implémentation réelle
        const spy = jest.spyOn(calculator, 'add');

        const result = calculator.add(2, 3);  // Utilise la vraie implémentation !

        expect(result).toBe(5);               // La vraie valeur
        expect(spy).toHaveBeenCalledWith(2, 3);

        spy.mockRestore();   // Restaurer l'original après le test
    });

    test('mocker une méthode d\'objet avec spyOn', () => {
        const userRepo = { findById: (id) => ({ id, name: 'Real User' }) };

        const spy = jest.spyOn(userRepo, 'findById').mockReturnValue({ id: 1, name: 'Mock User' });

        const user = userRepo.findById(1);
        expect(user.name).toBe('Mock User');   // Valeur mockée

        spy.mockRestore();
        expect(userRepo.findById(1).name).toBe('Real User');  // Original restauré
    });

    // ─── Espionner console.error ───────────────────────────────────────────────
    test('espionner console pour vérifier les logs', () => {
        const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

        someCodeThatLogsErrors();

        expect(consoleSpy).toHaveBeenCalledWith('Expected error message');
        consoleSpy.mockRestore();
    });

    // ─── Espionner les méthodes globales ──────────────────────────────────────
    test('espionner Date.now()', () => {
        const dateSpy = jest.spyOn(Date, 'now').mockReturnValue(1704067200000); // 2024-01-01

        const timestamp = Date.now();
        expect(timestamp).toBe(1704067200000);

        dateSpy.mockRestore();
    });
});
```

<br>

---

## 4. Timers Virtuels

```javascript title="JavaScript — jest.useFakeTimers() : contrôler setTimeout, setInterval, Date"
describe('Timers virtuels', () => {

    // Activer les faux timers AVANT les tests
    beforeEach(() => { jest.useFakeTimers(); });
    afterEach(()  => { jest.useRealTimers(); });

    // ─── setTimeout ───────────────────────────────────────────────────────────
    test('setTimeout s\'exécute après le délai', () => {
        const callback = jest.fn();
        setTimeout(callback, 1000);

        expect(callback).not.toHaveBeenCalled();  // Pas encore exécuté

        jest.advanceTimersByTime(1000);   // Avancer le temps de 1 seconde

        expect(callback).toHaveBeenCalledTimes(1);
    });

    // ─── setInterval ──────────────────────────────────────────────────────────
    test('setInterval s\'exécute à intervalles réguliers', () => {
        const callback = jest.fn();
        setInterval(callback, 500);

        jest.advanceTimersByTime(2000);   // Avancer de 2 secondes = 4 appels

        expect(callback).toHaveBeenCalledTimes(4);
    });

    // ─── Exécuter tous les timers en attente ──────────────────────────────────
    test('runAllTimers exécute tous les timers', () => {
        const callback = jest.fn();
        setTimeout(callback, 100);
        setTimeout(callback, 200);
        setTimeout(callback, 300);

        jest.runAllTimers();

        expect(callback).toHaveBeenCalledTimes(3);
    });

    // ─── Date fictive ─────────────────────────────────────────────────────────
    test('Date fictive pour tester des fonctions temporelles', () => {
        jest.setSystemTime(new Date('2024-01-15T10:00:00Z'));

        const now = new Date();
        expect(now.getFullYear()).toBe(2024);
        expect(now.getMonth()).toBe(0);    // Janvier = 0
        expect(now.getDate()).toBe(15);
    });
});
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    `jest.fn()` crée une **fonction doublure** : vous contrôlez ce qu'elle retourne et vous pouvez vérifier comment elle a été appelée. `jest.mock('module')` remplace **un module entier** par des mocks automatiques. `jest.spyOn()` observe une méthode existante sans supprimer son implémentation réelle. Les **timers virtuels** (`jest.useFakeTimers()`) permettent de tester `setTimeout`, `setInterval` et `Date` sans attendre. La règle d'or : **mocker aux frontières** (API, BDD, filesystem, timers) et tester la **logique business** avec de vraies valeurs.

> **Formation Jest complète.** Retour à l'[index Tests →](../index.md).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La maîtrise de ces concepts de développement moderne est cruciale pour construire des applications scalables, maintenables et sécurisées.

> [Retour à l'index →](./index.md)
