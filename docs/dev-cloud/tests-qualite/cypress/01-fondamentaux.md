---
description: "Cypress 01 — Fondamentaux : installation, Structure des tests, sélecteurs, commandes de base et assertions."
icon: lucide/book-open-check
tags: ["CYPRESS", "E2E", "TESTS", "SELECTEURS", "ASSERTIONS", "JAVASCRIPT"]
---

# Module 01 — Fondamentaux Cypress

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Cypress 13.x"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Pilote de Test"
    Un pilote de chasse ne valide pas un avion avec des vérifications manuelles une par une — il embarque dans le cockpit et exécute une série de manœuvres dans l'ordre. Cypress est ce cockpit : il ouvre votre application dans un vrai navigateur et exécute un scénario complet (connexion → navigation → clic → vérification du résultat). Si l'avion ne répond pas comme prévu à n'importe quelle étape, le test s'arrête immédiatement avec une capture d'écran.

<br>

---

## 1. Installation & Configuration

```bash title="Bash — Installer Cypress dans un projet existant"
# Installation (télécharge ~300 Mo de binaires)
npm install --save-dev cypress

# Ouvrir l'interface graphique (première fois : configure automatiquement)
npx cypress open

# Exécuter les tests en mode headless (CI/CD)
npx cypress run

# Exécuter un fichier spécifique
npx cypress run --spec "cypress/e2e/login.cy.js"

# Choisir le navigateur
npx cypress run --browser chrome
npx cypress run --browser firefox
```

```javascript title="JavaScript — cypress.config.js : configuration principale"
const { defineConfig } = require('cypress');

module.exports = defineConfig({
    e2e: {
        baseUrl:        'http://localhost:3000',   // URL de base (évite de la répéter)
        specPattern:    'cypress/e2e/**/*.cy.{js,ts}',
        viewportWidth:  1280,
        viewportHeight: 720,
        video:          true,                      // Enregistrer vidéo en CI
        screenshotOnRunFailure: true,              // Screenshot si échec
        defaultCommandTimeout: 4000,               // Timeout par défaut (ms)
        requestTimeout:        10000,              // Timeout des requêtes réseau

        // Variables d'environnement
        env: {
            apiUrl: 'http://localhost:3000/api',
        },

        setupNodeEvents(on, config) {
            // Plugins et tâches Node.js ici
            return config;
        },
    },
    component: {
        // Component Testing (React/Vue)
        devServer: {
            framework: 'react',
            bundler:   'vite',
        },
    },
});
```

```
Structure du projet Cypress :
cypress/
├── e2e/                    ← Fichiers de tests E2E (*.cy.js)
│   ├── auth/
│   │   ├── login.cy.js
│   │   └── register.cy.js
│   └── blog/
│       └── articles.cy.js
├── fixtures/               ← Données de test JSON
│   ├── user.json
│   └── articles.json
├── support/
│   ├── commands.js         ← Commandes Cypress personnalisées
│   └── e2e.js              ← Import global (exécuté avant chaque test)
└── downloads/              ← Fichiers téléchargés pendant les tests
```

<br>

---

## 2. Structure des Tests

```javascript title="JavaScript — cypress/e2e/auth/login.cy.js : test complet de connexion"
describe('Page de Connexion', () => {

    // Exécuté avant chaque test it()
    beforeEach(() => {
        cy.visit('/login');   // Navigue vers http://localhost:3000/login
    });

    it('affiche le formulaire de connexion', () => {
        cy.get('h1').should('contain.text', 'Connexion');
        cy.get('[data-cy="email"]').should('be.visible');
        cy.get('[data-cy="password"]').should('be.visible');
        cy.get('[data-cy="submit-btn"]').should('be.visible').and('not.be.disabled');
    });

    it('se connecte avec des identifiants valides', () => {
        cy.get('[data-cy="email"]').type('alice@example.com');
        cy.get('[data-cy="password"]').type('password123');
        cy.get('[data-cy="submit-btn"]').click();

        // Vérifier la redirection après connexion
        cy.url().should('include', '/dashboard');
        cy.get('[data-cy="welcome-message"]').should('contain.text', 'Bonjour Alice');
    });

    it('affiche une erreur avec des identifiants invalides', () => {
        cy.get('[data-cy="email"]').type('wrong@example.com');
        cy.get('[data-cy="password"]').type('wrongpassword');
        cy.get('[data-cy="submit-btn"]').click();

        cy.get('[data-cy="error-message"]')
            .should('be.visible')
            .and('contain.text', 'Identifiants incorrects');

        cy.url().should('include', '/login');   // Toujours sur la page login
    });

    it('requiert un email valide', () => {
        cy.get('[data-cy="email"]').type('email-invalide');
        cy.get('[data-cy="submit-btn"]').click();

        cy.get('[data-cy="email"]').then(($input) => {
            expect($input[0].validity.valid).to.be.false;
        });
    });
});
```

_La convention `[data-cy="xxx"]` est le **sélecteur recommandé Cypress** : il est stable (pas lié au style CSS), sémantique, et clairement identifié comme "pour les tests"._

<br>

---

## 3. Sélecteurs

```javascript title="JavaScript — Sélecteurs Cypress : les différentes stratégies"
// ─── Recommandé : data-* attributes ──────────────────────────────────────────
cy.get('[data-cy="submit-btn"]')      // data-cy (convention Cypress)
cy.get('[data-testid="search-input"]') // data-testid (React Testing Library)
cy.get('[data-test="modal"]')         // data-test (alternative)

// ─── Sélecteurs CSS ────────────────────────────────────────────────────────
cy.get('#main-content')               // ID
cy.get('.btn-primary')                // Classe (fragile si le style change)
cy.get('button[type="submit"]')       // Attribut
cy.get('nav a.active')                // Descendant

// ─── Par contenu textuel ──────────────────────────────────────────────────
cy.contains('Connexion')              // Texte exact ou partiel
cy.contains('button', 'Valider')      // <button> contenant "Valider"
cy.contains('h1', /^Mon Blog/)        // Regex

// ─── Trouver dans un parent ───────────────────────────────────────────────
cy.get('.article-list')
    .find('.article-item')            // Chercher à l'intérieur
    .first()                          // Premier élément
    .find('h2')
    .should('be.visible');

// ─── Navigation dans le DOM ────────────────────────────────────────────────
cy.get('[data-cy="article"]').eq(2)   // 3ème élément (index 0)
cy.get('li').last()                   // Dernier élément
cy.get('li').first()                  // Premier élément
cy.get('input').parent()              // Parent direct
cy.get('input').siblings('label')     // Éléments frères
```

<br>

---

## 4. Commandes de Base

```javascript title="JavaScript — Commandes Cypress : interactions utilisateur"
// ─── Navigation ───────────────────────────────────────────────────────────
cy.visit('/articles');                // Naviguer vers une URL
cy.go('back');                        // Naviguer en arrière
cy.go('forward');                     // Naviguer en avant
cy.reload();                          // Recharger la page

// ─── Interactions ─────────────────────────────────────────────────────────
cy.get('[data-cy="name"]').type('Alice Dupont');   // Taper du texte
cy.get('[data-cy="name"]').type('{selectall}Bob'); // Sélectionner tout puis taper
cy.get('[data-cy="name"]').clear();                // Vider le champ
cy.get('[data-cy="submit"]').click();              // Cliquer
cy.get('[data-cy="submit"]').dblclick();           // Double-clic
cy.get('[data-cy="submit"]').rightclick();         // Clic droit

// ─── Formulaires ──────────────────────────────────────────────────────────
cy.get('select[name="country"]').select('France');         // Sélectionner une option
cy.get('[data-cy="active"]').check();                      // Cocher une checkbox
cy.get('[data-cy="active"]').uncheck();                    // Décocher
cy.get('[data-cy="theme-dark"]').check();                  // Radio button

// ─── Fichiers ─────────────────────────────────────────────────────────────
cy.get('[data-cy="upload"]').selectFile('cypress/fixtures/photo.jpg');

// ─── Scroll ───────────────────────────────────────────────────────────────
cy.scrollTo('bottom');              // Défiler en bas de page
cy.get('[data-cy="lazy-section"]').scrollIntoView();

// ─── Focus & Hover ────────────────────────────────────────────────────────
cy.get('[data-cy="email"]').focus();
cy.get('[data-cy="tooltip"]').trigger('mouseover');

// ─── Clavier ──────────────────────────────────────────────────────────────
cy.get('[data-cy="email"]').type('{enter}');        // Touche Entrée
cy.get('body').type('{ctrl+s}');                    // Ctrl+S
```

<br>

---

## 5. Assertions

```javascript title="JavaScript — Assertions Cypress avec .should()"
// ─── Visibilité ───────────────────────────────────────────────────────────
cy.get('[data-cy="modal"]').should('be.visible');
cy.get('[data-cy="spinner"]').should('not.exist');    // N'existe pas dans le DOM
cy.get('[data-cy="dropdown"]').should('be.hidden');

// ─── Contenu ──────────────────────────────────────────────────────────────
cy.get('h1').should('have.text', 'Connexion');         // Texte exact
cy.get('p').should('contain.text', 'Bienvenue');       // Texte partiel
cy.get('[data-cy="count"]').should('contain.text', '3 articles');

// ─── Attributs & Classes ──────────────────────────────────────────────────
cy.get('input[name="email"]').should('have.attr', 'type', 'email');
cy.get('[data-cy="btn"]').should('have.class', 'active');
cy.get('[data-cy="btn"]').should('not.have.class', 'disabled');
cy.get('[data-cy="link"]').should('have.attr', 'href').and('include', '/articles');

// ─── État ─────────────────────────────────────────────────────────────────
cy.get('[data-cy="submit"]').should('be.disabled');
cy.get('[data-cy="input"]').should('be.focused');
cy.get('[data-cy="checkbox"]').should('be.checked');

// ─── URL ──────────────────────────────────────────────────────────────────
cy.url().should('eq', 'http://localhost:3000/dashboard');
cy.url().should('include', '/dashboard');
cy.location('pathname').should('eq', '/dashboard');

// ─── Chaîner plusieurs assertions ─────────────────────────────────────────
cy.get('[data-cy="article-title"]')
    .should('be.visible')
    .and('have.class', 'featured')
    .and('contain.text', 'Astro');
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Cypress suit une syntaxe **chainée** : chaque commande retourne un "sujet" sur lequel vous enchaînez des commandes ou assertions. `cy.get()` sélectionne, `.click()/.type()/.select()` interagit, `.should()` assert. Cypress **attend automatiquement** (retry-ability) que les éléments apparaissent et que les assertions passent — pas besoin de `wait()` arbitraires. Utilisez **`[data-cy="xxx"]`** pour des sélecteurs stables qui ne cassent pas quand vous refactorisez le CSS. `beforeEach(() => cy.visit(...))` garantit un point de départ propre.

> Module suivant : [Tests Avancés →](./02-tests-avances.md) — intercept réseau, fixtures, commandes personnalisées, CI/CD.

<br>
