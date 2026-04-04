---
description: "Cypress 02 — Tests avancés : cy.intercept(), fixtures, custom commands, Page Object Model et CI/CD GitHub Actions."
icon: lucide/book-open-check
tags: ["CYPRESS", "E2E", "INTERCEPT", "FIXTURES", "CUSTOM-COMMANDS", "CICD"]
---

# Module 02 — Tests Avancés Cypress

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Cypress 13.x"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Simulateur de Vol"
    Les pilotes s'entraînent sur simulateur avant de piloter de vrais avions : le simulateur reproduit fidèlement les conditions réelles sans les risques. `cy.intercept()` est votre simulateur réseau : vous interceptez les requêtes HTTP de votre application et retournez des réponses fictives (fixtures), permettant de tester n'importe quel scénario (API lente, erreur serveur, données vides) sans dépendre d'une vraie API.

<br>

---

## 1. `cy.intercept()` — Intercepter les Requêtes Réseau

```javascript title="JavaScript — cy.intercept() : mock des appels API"
describe('Articles API', () => {

    // ─── Intercepter et retourner des données fictives ────────────────────────
    it('affiche les articles depuis l\'API', () => {
        cy.intercept('GET', '/api/articles', {
            statusCode: 200,
            body: [
                { id: 1, title: 'Introduction à Astro', tags: ['astro'] },
                { id: 2, title: 'Fondamentaux Django',  tags: ['python'] },
            ],
        }).as('getArticles');  // Alias pour référencer l'interception

        cy.visit('/articles');

        cy.wait('@getArticles');  // Attendre que la requête soit interceptée

        cy.get('[data-cy="article-list"]').children().should('have.length', 2);
        cy.get('[data-cy="article-title"]').first().should('contain.text', 'Introduction à Astro');
    });

    // ─── Tester l'état de chargement ──────────────────────────────────────────
    it('affiche un spinner pendant le chargement', () => {
        cy.intercept('GET', '/api/articles', (req) => {
            req.reply((res) => {
                res.setDelay(2000);   // Simuler une API lente (2 secondes)
                res.send({ body: [] });
            });
        }).as('slowRequest');

        cy.visit('/articles');
        cy.get('[data-cy="spinner"]').should('be.visible');  // Spinner visible pendant le chargement
        cy.wait('@slowRequest');
        cy.get('[data-cy="spinner"]').should('not.exist');   // Spinner disparu après
    });

    // ─── Tester la gestion d'erreurs ──────────────────────────────────────────
    it('affiche un message d\'erreur si l\'API échoue', () => {
        cy.intercept('GET', '/api/articles', {
            statusCode: 500,
            body: { error: 'Internal Server Error' },
        }).as('failedRequest');

        cy.visit('/articles');
        cy.wait('@failedRequest');

        cy.get('[data-cy="error-banner"]')
            .should('be.visible')
            .and('contain.text', 'Impossible de charger les articles');
    });

    // ─── Intercepter un POST ──────────────────────────────────────────────────
    it('crée un article et recharge la liste', () => {
        cy.intercept('POST', '/api/articles', {
            statusCode: 201,
            body: { id: 42, title: 'Nouvel Article', created: true },
        }).as('createArticle');

        cy.intercept('GET', '/api/articles').as('refreshList');

        cy.visit('/articles/creer');
        cy.get('[data-cy="title"]').type('Nouvel Article');
        cy.get('[data-cy="submit"]').click();

        cy.wait('@createArticle').its('request.body').should('deep.include', {
            title: 'Nouvel Article',
        });

        cy.url().should('include', '/articles');
        cy.wait('@refreshList');
    });
});
```

<br>

---

## 2. Fixtures — Données de Test Externes

```json title="JSON — cypress/fixtures/articles.json : données de test"
[
    {
        "id":        1,
        "title":     "Introduction à Astro",
        "content":   "Astro est un framework web...",
        "author":    "Alice Dupont",
        "tags":      ["astro", "web"],
        "published": true,
        "date":      "2024-03-15"
    },
    {
        "id":        2,
        "title":     "Fondamentaux Django",
        "content":   "Django suit le pattern MVT...",
        "author":    "Bob Martin",
        "tags":      ["python", "django"],
        "published": true,
        "date":      "2024-02-28"
    }
]
```

```javascript title="JavaScript — Utiliser les fixtures dans les tests"
describe('Articles avec Fixtures', () => {

    beforeEach(() => {
        // Charger la fixture avant chaque test
        cy.fixture('articles').as('articlesData');
    });

    it('affiche les articles depuis la fixture', function () {
        // Utiliser function() (pas arrow) pour accéder à this.articlesData
        cy.intercept('GET', '/api/articles', { body: this.articlesData }).as('getArticles');

        cy.visit('/articles');
        cy.wait('@getArticles');

        cy.get('[data-cy="article-list"]')
            .children()
            .should('have.length', this.articlesData.length);
    });

    it('affiche le titre du premier article', function () {
        cy.intercept('GET', '/api/articles', { body: this.articlesData });
        cy.visit('/articles');

        cy.get('[data-cy="article-title"]').first()
            .should('contain.text', this.articlesData[0].title);
    });
});

// ─── Alternative : cy.fixture() dans le test ──────────────────────────────────
it('charge une fixture directement', () => {
    cy.fixture('articles').then((articles) => {
        cy.intercept('GET', '/api/articles', articles);
        cy.visit('/articles');
        expect(articles).to.have.length.greaterThan(0);
    });
});
```

<br>

---

## 3. Commandes Personnalisées

```javascript title="JavaScript — cypress/support/commands.js : commandes réutilisables"
// ─── Commande de connexion ───────────────────────────────────────────────────
// Utilisation : cy.login('alice@example.com', 'password123')
Cypress.Commands.add('login', (email, password) => {
    cy.session(
        [email, password],    // Clé de cache de session
        () => {
            cy.visit('/login');
            cy.get('[data-cy="email"]').type(email);
            cy.get('[data-cy="password"]').type(password);
            cy.get('[data-cy="submit"]').click();
            cy.url().should('include', '/dashboard');
        },
        {
            validate: () => {
                cy.getCookie('auth-token').should('exist');
            },
        }
    );
});

// ─── Commande d'API directe (byasser l'UI) ────────────────────────────────────
// Utilisation : cy.loginViaApi('alice@example.com', 'password123')
Cypress.Commands.add('loginViaApi', (email, password) => {
    cy.request('POST', '/api/auth/login', { email, password }).then((response) => {
        window.localStorage.setItem('auth-token', response.body.token);
    });
});

// ─── Commande pour créer un article via l'API ────────────────────────────────
// Utilisation : cy.createArticle({ title: '...', content: '...' })
Cypress.Commands.add('createArticle', (article) => {
    cy.request({
        method: 'POST',
        url:    '/api/articles',
        headers: {
            Authorization: `Bearer ${window.localStorage.getItem('auth-token')}`,
        },
        body: article,
    }).then((response) => {
        expect(response.status).to.eq(201);
        return response.body;
    });
});

// ─── Commande pour vider la base de données de test ──────────────────────────
Cypress.Commands.add('resetDatabase', () => {
    cy.request('POST', '/api/test/reset').its('status').should('eq', 200);
});
```

```javascript title="JavaScript — Utiliser les commandes personnalisées dans les tests"
describe('Gestion des articles (authentifié)', () => {

    beforeEach(() => {
        cy.login('alice@example.com', 'AlicePass123!');
    });

    it('crée un article via l\'API puis le vérifie dans l\'UI', () => {
        cy.createArticle({
            title:   'Article de Test Cypress',
            content: 'Contenu généré par Cypress pour les tests E2E.',
        }).then((article) => {
            cy.visit(`/articles/${article.id}`);
            cy.get('h1').should('contain.text', 'Article de Test Cypress');
        });
    });

    it('supprime un article depuis l\'interface', () => {
        cy.visit('/articles/1');
        cy.get('[data-cy="delete-btn"]').click();
        cy.get('[data-cy="confirm-delete"]').click();
        cy.url().should('include', '/articles');
        cy.get('[data-cy="article-list"]').should('not.contain', 'Article supprimé');
    });
});
```

<br>

---

## 4. Page Object Model (POM)

```javascript title="JavaScript — cypress/pages/LoginPage.js : Page Object"
/**
 * Page Object pour la page de connexion.
 * Centralise tous les sélecteurs et actions de la page.
 */
class LoginPage {
    visit() {
        cy.visit('/login');
        return this;
    }

    fillEmail(email) {
        cy.get('[data-cy="email"]').clear().type(email);
        return this;   // Retourner this pour chaîner
    }

    fillPassword(password) {
        cy.get('[data-cy="password"]').clear().type(password);
        return this;
    }

    submit() {
        cy.get('[data-cy="submit-btn"]').click();
        return this;
    }

    assertErrorMessage(message) {
        cy.get('[data-cy="error-message"]').should('contain.text', message);
        return this;
    }

    assertRedirectedTo(url) {
        cy.url().should('include', url);
        return this;
    }
}

export const loginPage = new LoginPage();
```

```javascript title="JavaScript — Utiliser le Page Object dans les tests"
import { loginPage } from '../pages/LoginPage';

describe('Connexion', () => {

    beforeEach(() => loginPage.visit());

    it('se connecte avec succès', () => {
        loginPage
            .fillEmail('alice@example.com')
            .fillPassword('AlicePass123!')
            .submit()
            .assertRedirectedTo('/dashboard');
    });

    it('affiche une erreur si mot de passe incorrect', () => {
        loginPage
            .fillEmail('alice@example.com')
            .fillPassword('mauvaismdp')
            .submit()
            .assertErrorMessage('Identifiants incorrects');
    });
});
```

<br>

---

## 5. CI/CD GitHub Actions

```yaml title="YAML — .github/workflows/cypress.yml : E2E en CI"
name: Cypress E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  cypress-run:
    runs-on: ubuntu-latest

    services:
      # Démarrer la base de données (si nécessaire)
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB:       test_db
          POSTGRES_USER:     test_user
          POSTGRES_PASSWORD: test_password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: npm

      - name: Installer les dépendances
        run: npm ci

      - name: Build l'application
        run: npm run build

      - name: Démarrer le serveur (arrière-plan)
        run: npm start &

      - name: Attendre que le serveur soit prêt
        run: npx wait-on http://localhost:3000 --timeout 60000

      - name: Lancer Cypress (parallèle avec Cypress Cloud)
        uses: cypress-io/github-action@v6
        with:
          record:    true     # Enregistrer sur Cypress Cloud (optionnel)
          parallel:  true     # Parallélisation
        env:
          CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}

      - name: Upload artifacts si échec
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: cypress-artifacts
          path: |
            cypress/screenshots
            cypress/videos
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    `cy.intercept()` intercepte les requêtes réseau et retourne des **fixtures** — éliminez la dépendance à une vraie API dans les tests. Les **commandes personnalisées** (`Cypress.Commands.add()`) factorisent les actions répétitives (connexion, création de données). `cy.session()` met en cache la session entre les tests, accélérant considérablement la suite. Le **Page Object Model** centralise les sélecteurs et actions par page — quand l'UI change, n'adaptez que le POM. En CI/CD, `npx wait-on` garantit que le serveur est prêt avant de lancer Cypress.

> **Formation Cypress complète.** Retour à l'[index Tests →](../index.md).

<br>
