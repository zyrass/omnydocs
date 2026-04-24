---
description: "Cypress — Accessibility Testing : Automatiser la détection des problèmes d'accessibilité (a11y) web avec cypress-axe."
icon: lucide/book-open-check
tags: ["CYPRESS", "A11Y", "ACCESSIBILITÉ", "TESTS", "AXE"]
---

# 05 — Accessibility Testing (a11y)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Cypress 13.x / cypress-axe"
  data-time="~2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    Tester l'accessibilité manuellement, c'est comme corriger l'orthographe d'un livre de 500 pages en le lisant mot par mot : c'est très long et l'erreur humaine est inévitable. Les tests d'accessibilité automatisés agissent comme un correcteur orthographique : ils parcourent vos pages à la vitesse de l'éclair pour repérer toutes les fautes flagrantes (contrastes, labels manquants, attributs ARIA erronés).

L'accessibilité web (souvent abrégée **a11y**, pour *accessibility* = a + 11 lettres + y) n'est plus une option, c'est une exigence légale (RGAA en France, ADA aux US) et éthique.

Bien que 100% de l'accessibilité ne puisse pas être testée de façon automatisée (l'automatisation couvre généralement environ 30% à 40% des règles), l'intégration de tests a11y dans Cypress empêche l'introduction de régressions évidentes.

Le standard de l'industrie pour les tests a11y automatisés est le moteur **axe-core** de Deque Systems, que nous allons intégrer via `cypress-axe`.

---

## 1. Installation de cypress-axe

Pour ajouter l'analyse d'accessibilité à Cypress :

```bash
npm install --save-dev cypress-axe axe-core
```

**Configuration dans `cypress/support/e2e.js` :**

Pour rendre les commandes disponibles globalement :

```javascript title="cypress/support/e2e.js"
import 'cypress-axe'

// Exemple d'ajout d'une commande personnalisée si on veut loguer proprement en console
// (La configuration de base suffit souvent)
```

---

## 2. Écrire son premier test d'accessibilité

Le workflow avec `cypress-axe` nécessite toujours 3 étapes :
1. `cy.visit()` pour aller sur la page.
2. `cy.injectAxe()` pour charger le moteur d'analyse dans la page.
3. `cy.checkA11y()` pour exécuter l'analyse et échouer le test s'il y a des violations.

```javascript title="cypress/e2e/accessibility.cy.js"
describe('Tests Accessibilité (a11y)', () => {
  it('La page d\'accueil respecte le standard WCAG 2.1 AA', () => {
    // 1. Visiter la page
    cy.visit('http://localhost:3000/')
    
    // 2. Injecter le moteur axe-core
    cy.injectAxe()
    
    // 3. Analyser et vérifier toute la page
    cy.checkA11y()
  })
})
```

S'il manque un attribut `alt` sur une image, ou si le contraste d'un bouton est trop faible, le test échouera et Cypress affichera l'erreur précise avec un lien vers la documentation Deque expliquant comment la corriger.

---

## 3. Paramètres Avancés

### 3.1 Cibler des éléments spécifiques

Parfois, on ne veut tester qu'une modale, un menu, ou au contraire exclure un widget tiers non maîtrisé (comme un iframe YouTube).

```javascript
it('La modale de login est accessible', () => {
  cy.visit('/login')
  cy.injectAxe()
  
  // N'analyser que la div avec la classe .login-modal
  cy.checkA11y('.login-modal')
})

it('La page exclut les widgets externes', () => {
  cy.visit('/home')
  cy.injectAxe()
  
  // Analyser toute la page SAUF l'élément .twitter-feed
  cy.checkA11y({ exclude: ['.twitter-feed'] })
})
```

### 3.2 Désactiver des règles spécifiques

Si une règle bloque temporairement votre pipeline CI et que vous prévoyez de la corriger plus tard, vous pouvez la désactiver temporairement.

```javascript
it('Passe l\'accessibilité, en ignorant temporairement le contraste', () => {
  cy.visit('/')
  cy.injectAxe()
  
  cy.checkA11y(null, {
    rules: {
      'color-contrast': { enabled: false }, // Ignorer le contraste
      'link-name': { enabled: false }       // Ignorer les liens vides
    }
  })
})
```

### 3.3 Personnaliser le Logging dans la CI

Par défaut, `cypress-axe` affiche les erreurs dans la console Cypress. Pour les logs CI (Terminal), il est recommandé d'ajouter une fonction de formatage pour lister clairement les violations.

```javascript title="cypress/support/e2e.js"
import 'cypress-axe'

// Fonction pour un affichage terminal propre
function terminalLog(violations) {
  cy.task(
    'log',
    `${violations.length} violations d'accessibilité détectées`
  )
  
  // Créer un tableau propre des erreurs
  const violationData = violations.map(
    ({ id, impact, description, nodes }) => ({
      id,
      impact,
      description,
      nodes: nodes.length
    })
  )

  cy.task('table', violationData)
}

// Remplacer cy.checkA11y() par défaut par une commande qui utilise le logger
Cypress.Commands.add('checkA11yConsole', (context, options) => {
  cy.checkA11y(context, options, terminalLog)
})
```

---

## 4. Intégration dans un flux de travail Cypress standard

Le meilleur moyen d'intégrer l'a11y n'est pas d'avoir un fichier dédié, mais de glisser les vérifications *à l'intérieur* de vos tests E2E existants pour chaque état de la page (ex: avant modale, pendant modale).

```javascript
describe('Flux de paiement', () => {
  beforeEach(() => {
    cy.visit('/checkout')
    cy.injectAxe()
  })

  it('peut passer commande en toute accessibilité', () => {
    // Vérifier l'état initial
    cy.checkA11y()
    
    // Remplir le formulaire
    cy.get('#name').type('Jean')
    cy.get('#card').type('4111...')
    
    // Ouvrir popup confirmation
    cy.get('button[type="submit"]').click()
    cy.get('.confirmation-modal').should('be.visible')
    
    // RE-VÉRIFIER l'accessibilité dans le NOUVEL état de la page
    // (pour s'assurer que le focus trap de la modale est ok, etc.)
    cy.checkA11y()
  })
})
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Avec `cypress-axe`, les tests d'accessibilité automatisés coûtent environ **zéro effort supplémentaire** une fois configurés. En ajoutant un simple `cy.checkA11y()` dans vos tests E2E, vous garantissez immédiatement que chaque nouvelle vue ajoutée ou modifiée sur votre application est utilisable par tous, respecte les normes de base (contraste, lecteur d'écran, navigation clavier) et vous évitez une énorme dette technique "a11y" pour plus tard.

<br>
