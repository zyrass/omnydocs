---
description: "Vitest 03 — Mocking & Spies : vi.fn(), vi.mock(), vi.spyOn(), timers, modules, variables d'environnement."
icon: lucide/ghost
tags: ["VITEST", "MOCKING", "SPIES", "VI_FN", "VI_MOCK", "TESTING"]
---

# Module 03 — Mocking & Spies

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Vitest 1.x"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Les Comédiens Doublures"
    Au cinéma, les scènes dangereuses utilisent des doublures : même costume, mêmes mouvements, mais sans le risque réel. Le mocking fonctionne pareil : vous remplacez les dépendances réelles (appels API, base de données, emails) par des "doublures" contrôlées — elles se comportent exactement comme prévu, sans les effets de bord. Vos tests restent isolés, reproductibles, rapides.

Le mocking dans Vitest utilise l'objet global `vi` (équivalent de `jest` dans Jest). Il permet de :
- Remplacer des fonctions par des **spies** (espionner les appels)
- **Mocker des modules** entiers (axios, fs, votre propre service)
- Contrôler les **timers** (setTimeout, Date.now)
- Simuler les **variables d'environnement**

<br>

---

## 1. vi.fn() — Fonctions Mock

```javascript title="JavaScript — vi.fn() : créer et contrôler une fonction mock"
import { vi, describe, it, expect, beforeEach } from 'vitest';

describe('vi.fn() — base', () => {

    it('crée une fonction mock appelable', () => {
        const mockFn = vi.fn();

        mockFn('hello', 42);

        expect(mockFn).toHaveBeenCalled();
        expect(mockFn).toHaveBeenCalledWith('hello', 42);
        expect(mockFn).toHaveBeenCalledTimes(1);
        expect(mockFn.mock.calls).toEqual([['hello', 42]]);
        expect(mockFn.mock.results[0].value).toBeUndefined();  // Retourne undefined par défaut
    });

    it('retourne une valeur définie', () => {
        const mockFetch = vi.fn().mockResolvedValue({
            json: () => Promise.resolve({ id: 1, name: 'Alice' })
        });

        // La fonction retournera toujours cette valeur
        return expect(mockFetch('/api/user')).resolves.toBeDefined();
    });

    it('retourne des valeurs différentes à chaque appel', () => {
        const mockRandom = vi.fn()
            .mockReturnValueOnce(0.1)   // 1er appel → 0.1
            .mockReturnValueOnce(0.5)   // 2ème appel → 0.5
            .mockReturnValue(0.9);      // Tous les suivants → 0.9

        expect(mockRandom()).toBe(0.1);
        expect(mockRandom()).toBe(0.5);
        expect(mockRandom()).toBe(0.9);
        expect(mockRandom()).toBe(0.9);
    });

    it('simule une erreur', async () => {
        const mockFn = vi.fn().mockRejectedValue(new Error('Timeout'));

        await expect(mockFn()).rejects.toThrow('Timeout');
    });
});

// Réinitialiser les mocks entre les tests
describe('avec réinitialisation', () => {
    const mockCallback = vi.fn();

    beforeEach(() => {
        mockCallback.mockClear();    // Efface les appels enregistrés
        // vi.clearAllMocks()        // Efface tous les mocks
        // vi.resetAllMocks()        // Reset les implémentations + appels
        // vi.restoreAllMocks()      // Restore les originaux (après spyOn)
    });

    it('ne retient pas les appels du test précédent', () => {
        expect(mockCallback).not.toHaveBeenCalled();
    });
});
```

<br>

---

## 2. vi.spyOn() — Espionner des Méthodes Réelles

```javascript title="JavaScript — vi.spyOn() : surveiller sans remplacer"
import { vi, describe, it, expect, afterEach } from 'vitest';
import { UserService } from './userService';
import * as api from './api';

describe('vi.spyOn()', () => {

    afterEach(() => vi.restoreAllMocks());  // Restaurer les méthodes originales

    it('espionne sans modifier le comportement', () => {
        const spy = vi.spyOn(Math, 'random');

        const result = Math.random();

        // La vraie fonction s'est exécutée
        expect(typeof result).toBe('number');
        expect(result).toBeGreaterThanOrEqual(0);
        expect(result).toBeLessThan(1);

        // Mais on a pu l'espionner
        expect(spy).toHaveBeenCalledTimes(1);
    });

    it('remplace le comportement temporairement', async () => {
        // Mocker une méthode d'un module importé
        const fetchSpy = vi.spyOn(api, 'fetchUser')
                           .mockResolvedValue({ id: 1, name: 'Alice Mocked' });

        const user = await api.fetchUser(1);

        expect(user.name).toBe('Alice Mocked');
        expect(fetchSpy).toHaveBeenCalledWith(1);
    });

    it('espionne une méthode d\'instance', () => {
        const service = new UserService();
        const spy = vi.spyOn(service, 'sendWelcomeEmail').mockImplementation(() => {});

        service.register({ name: 'Alice', email: 'alice@example.com' });

        expect(spy).toHaveBeenCalledWith('alice@example.com');
    });
});
```

<br>

---

## 3. vi.mock() — Mocker des Modules Entiers

```javascript title="JavaScript — vi.mock() : remplacer un module importé"
import { vi, describe, it, expect } from 'vitest';

// ─── Mocker axios ─────────────────────────────────────────────────────────────
vi.mock('axios');                      // Remplace tout le module par des mocks vides

import axios from 'axios';
import { getUser }  from './userService';

describe('UserService avec axios mocké', () => {
    it('retourne les données de l\'utilisateur', async () => {
        // Configurer le retour du mock
        axios.get.mockResolvedValue({
            data: { id: 1, name: 'Alice', email: 'alice@example.com' }
        });

        const user = await getUser(1);

        expect(user.name).toBe('Alice');
        expect(axios.get).toHaveBeenCalledWith('/api/users/1');
    });

    it('propage l\'erreur réseau', async () => {
        axios.get.mockRejectedValue(new Error('Network Error'));

        await expect(getUser(1)).rejects.toThrow('Network Error');
    });
});
```

```javascript title="JavaScript — vi.mock() avec factory : contrôle total"
// ─── Factory : définir exactement ce que le module exporte ───────────────────
vi.mock('./emailService', () => ({
    default: {
        sendEmail: vi.fn().mockResolvedValue({ messageId: 'mock-id-123' }),
        sendBulk:  vi.fn().mockResolvedValue({ sent: 10, failed: 0 }),
    }
}));

vi.mock('./config', () => ({
    default: {
        apiUrl:    'http://localhost:3000',
        apiKey:    'test-api-key',
        timeout:   5000,
    }
}));

// ─── Mocker partiellement (garder cer­taines fonctions réelles) ────────────
vi.mock('./utils', async (importOriginal) => {
    const original = await importOriginal();   // Importe le vrai module
    return {
        ...original,                            // Garde toutes les fonctions réelles
        generateSlug: vi.fn().mockReturnValue('mocked-slug'),  // Mock seulement celle-ci
    };
});
```

<br>

---

## 4. Mocker `fetch` natif

```javascript title="JavaScript — Mocker fetch avec vi.fn()"
import { vi, beforeEach, afterEach, describe, it, expect } from 'vitest';
import { ApiClient } from './apiClient';

// Mocker fetch globalement
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('ApiClient', () => {
    let client;

    beforeEach(() => {
        client = new ApiClient('https://api.example.com');
        mockFetch.mockClear();
    });

    afterEach(() => vi.clearAllMocks());

    // ─── Helper pour créer une réponse fetch réaliste ─────────────────────────
    function mockFetchResponse(data, options = {}) {
        return mockFetch.mockResolvedValue({
            ok:     options.ok ?? true,
            status: options.status ?? 200,
            json:   () => Promise.resolve(data),
            text:   () => Promise.resolve(JSON.stringify(data)),
            headers: new Headers(options.headers ?? {}),
        });
    }

    it('GET /users retourne la liste des utilisateurs', async () => {
        mockFetchResponse([{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }]);

        const users = await client.get('/users');

        expect(users).toHaveLength(2);
        expect(mockFetch).toHaveBeenCalledWith(
            'https://api.example.com/users',
            expect.objectContaining({ method: 'GET' })
        );
    });

    it('POST /users envoie le bon body', async () => {
        mockFetchResponse({ id: 3, name: 'Carol' }, { status: 201 });

        const user = await client.post('/users', { name: 'Carol' });

        expect(mockFetch).toHaveBeenCalledWith(
            'https://api.example.com/users',
            expect.objectContaining({
                method:  'POST',
                headers: expect.objectContaining({ 'Content-Type': 'application/json' }),
                body:    JSON.stringify({ name: 'Carol' }),
            })
        );
        expect(user.id).toBe(3);
    });

    it('lève une erreur pour les réponses HTTP 4xx/5xx', async () => {
        mockFetchResponse({ message: 'Not Found' }, { ok: false, status: 404 });

        await expect(client.get('/ghost')).rejects.toThrow('HTTP 404');
    });
});
```

<br>

---

## 5. Timers et Date

```javascript title="JavaScript — vi.useFakeTimers() : contrôler le temps"
import { vi, describe, it, expect, afterEach } from 'vitest';
import { debounce, scheduleReminder } from './utils';

describe('Timers virtuels', () => {
    afterEach(() => vi.useRealTimers());

    it('le debounce attend le délai avant d\'appeler', () => {
        vi.useFakeTimers();
        const fn = vi.fn();
        const debounced = debounce(fn, 300);

        debounced('a');
        debounced('b');
        debounced('c');

        // Pas encore appelé
        expect(fn).not.toHaveBeenCalled();

        vi.advanceTimersByTime(300);

        // Appelé une seule fois avec le dernier argument
        expect(fn).toHaveBeenCalledTimes(1);
        expect(fn).toHaveBeenCalledWith('c');
    });

    it('contrôle Date.now() pour une fonction time-sensitive', () => {
        vi.useFakeTimers();
        vi.setSystemTime(new Date('2024-01-01T00:00:00Z'));

        const reminder = scheduleReminder({ in: 24 * 60 * 60 * 1000 });  // Dans 24h

        expect(reminder.scheduledAt).toEqual(new Date('2024-01-02T00:00:00Z'));
    });

    it('avance le temps de 1 heure', () => {
        vi.useFakeTimers();
        const start = Date.now();

        vi.advanceTimersByTime(60 * 60 * 1000);   // 1 heure en ms

        expect(Date.now() - start).toBe(60 * 60 * 1000);
    });
});
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Mocker une dépendance API**

```javascript title="JavaScript — Exercice 1 : NotificationService"
// Créez un NotificationService qui dépend de :
// - EmailService.send(to, subject, body)
// - SMSService.send(phone, message)
// - LogService.log(event, data)

// Mockez ces 3 dépendances avec vi.fn() et testez que :
// 1. notifyUser(user, 'welcome') appelle EmailService.send avec les bons args
// 2. notifyUser(user, 'sms-verify') appelle SMSService.send
// 3. Chaque notification est loggée dans LogService
// 4. En cas d'erreur EmailService, le log enregistre l'échec
// 5. SMSService n'est PAS appelé si l'utilisateur n'a pas de téléphone
```

**Exercice 2 — Module partiel et timers**

```javascript title="JavaScript — Exercice 2 : mocker partiellement + timers"
// 1. Utilisez vi.mock() avec importOriginal pour mocker
//    uniquement la fonction generateId() dans un module utils,
//    en gardant toutes les autres fonctions réelles.
// 2. Écrivez un test pour une fonction retryWith(fn, maxAttempts, delay)
//    qui appelle fn jusqu'à ce qu'elle réussisse ou dépasse maxAttempts.
//    Utilisez vi.useFakeTimers() pour ne pas attendre les vrais délais.
//    Testez : 1 échec puis succès, 3 échecs consécutifs (throw final).
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    **`vi.fn()`** crée une doublure contrôlable. **`vi.spyOn()`** espionne (et peut remplacer) une méthode existante — toujours restaurer avec `afterEach(() => vi.restoreAllMocks())`. **`vi.mock()`** remplace un module entier avant son import : à déclarer en haut du fichier (hoisting). Les **fake timers** sont indispensables pour tester debounce, throttle, setTimeout ou tout code time-sensitive sans attendre réellement. Réinitialiser les mocks dans `beforeEach/afterEach` pour éviter les interférences entre tests.

> Module suivant : [Coverage & CI/CD →](./04-coverage-cicd.md) — mesurer la couverture et intégrer Vitest dans une pipeline CI.

<br>
