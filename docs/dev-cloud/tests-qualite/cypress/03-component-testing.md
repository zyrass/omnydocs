---
description: "Cypress — Component Testing : Tester vos composants React et Vue en isolation directement dans le navigateur."
icon: lucide/book-open-check
tags: ["CYPRESS", "COMPONENT TESTING", "REACT", "VUE", "JAVASCRIPT"]
---

# 03 — Component Testing

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Cypress 13.x"
  data-time="~4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    Si les tests E2E vérifient que la voiture roule bien sur l'autoroute, le Component Testing vérifie que l'autoradio, pris isolément, fonctionne parfaitement sur un établi d'essai. Vous testez le composant dans un "vrai" environnement visuel (le navigateur), mais sans charger toute l'application.

Jusqu'à récemment, les composants frontend (React, Vue, Angular) étaient testés avec Node.js via jsdom (ex: Jest + Testing Library). Le problème ? jsdom n'est pas un vrai navigateur : pas de vrai rendu CSS, comportements d'événements approximatifs.

**Cypress Component Testing** résout cela : il monte vos composants dans un **vrai navigateur Chromium/Firefox**. Vous voyez visuellement le composant et testez ses interactions exactement comme l'utilisateur.

---

## 1. Différence entre E2E et Component Testing

| Caractéristique | E2E Testing | Component Testing |
|-----------------|-------------|-------------------|
| **Portée** | L'application entière (frontend + backend) | Un composant React/Vue isolé |
| **Point d'entrée** | `cy.visit('/login')` | `cy.mount(<LoginBox />)` |
| **Réseau** | Vraies requêtes API (ou mock global) | Requêtes mockées (`cy.intercept`) |
| **Vitesse** | Lent (plusieurs secondes par test) | Rapide (quelques millisecondes) |
| **Dépendances** | Besoin de la DB et du backend | Aucune (mocks/props) |

---

## 2. Installation et Configuration

Pour ajouter le Component Testing à un projet Cypress existant :

```bash
# Ouvrir l'interface Cypress
npx cypress open
```

Dans l'interface, choisissez **Component Testing** au lieu de **E2E Testing**. Cypress détectera automatiquement votre framework (React, Vue, etc.) et votre bundler (Vite, Webpack) et générera la configuration nécessaire.

**Structure des dossiers :**

Cypress recommande de placer les tests de composants **à côté** des composants eux-mêmes, pas dans un dossier `cypress/` séparé :

```text
src/
├── components/
│   ├── Button/
│   │   ├── Button.jsx
│   │   ├── Button.css
│   │   └── Button.cy.jsx  <-- Test du composant
```

---

## 3. Exemple React

### 3.1 Un composant simple

```jsx title="src/components/Stepper.jsx"
import { useState } from 'react'

export default function Stepper({ initial = 0 }) {
  const [count, setCount] = useState(initial)

  return (
    <div>
      <button data-cy="decrement" onClick={() => setCount(count - 1)}>-</button>
      <span data-cy="counter">{count}</span>
      <button data-cy="increment" onClick={() => setCount(count + 1)}>+</button>
    </div>
  )
}
```

### 3.2 Le test Cypress

```jsx title="src/components/Stepper.cy.jsx"
import Stepper from './Stepper'

describe('<Stepper />', () => {
  it('sert de valeur par défaut', () => {
    // 1. Monter le composant
    cy.mount(<Stepper />)
    
    // 2. Asserter l'état initial
    cy.get('[data-cy=counter]').should('have.text', '0')
  })

  it('utilise la prop initial', () => {
    cy.mount(<Stepper initial={100} />)
    cy.get('[data-cy=counter]').should('have.text', '100')
  })

  it('incrémente et décrémente correctement', () => {
    cy.mount(<Stepper />)
    
    // Test d'interaction
    cy.get('[data-cy=increment]').click()
    cy.get('[data-cy=counter]').should('have.text', '1')
    
    cy.get('[data-cy=decrement]').click().click()
    cy.get('[data-cy=counter]').should('have.text', '-1')
  })
})
```

---

## 4. Exemple Vue.js (Vue 3)

### 4.1 Un composant avec événements

```vue title="src/components/AlertBox.vue"
<template>
  <div v-if="isVisible" class="alert-box">
    <p>{{ message }}</p>
    <button @click="dismiss">Fermer</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  message: String
})

const emit = defineEmits(['closed'])
const isVisible = ref(true)

const dismiss = () => {
  isVisible.value = false
  emit('closed')
}
</script>
```

### 4.2 Le test Cypress

Pour vérifier les événements émis (emits) dans Vue, on utilise les Spies (Espions) de Cypress via `cy.spy()`.

```javascript title="src/components/AlertBox.cy.js"
import AlertBox from './AlertBox.vue'

describe('<AlertBox />', () => {
  it('affiche le message passé en prop', () => {
    cy.mount(AlertBox, {
      props: {
        message: 'Alerte de sécurité'
      }
    })
    
    cy.contains('Alerte de sécurité').should('be.visible')
  })

  it('émet l\'événement closed lors de la fermeture', () => {
    // Créer un espion Cypress
    const onClosedSpy = cy.spy().as('closedSpy')
    
    cy.mount(AlertBox, {
      props: { message: 'Test' },
      // Intercepter l'événement Vue 'closed'
      on: {
        closed: onClosedSpy
      }
    })
    
    cy.contains('Fermer').click()
    
    // Le composant doit disparaître
    cy.get('.alert-box').should('not.exist')
    
    // L'espion doit avoir été appelé
    cy.get('@closedSpy').should('have.been.calledOnce')
  })
})
```

---

## 5. Mocker le contexte (Providers, Routers)

Très souvent, vos composants dépendent de contextes globaux (Redux, Vuex, Vue Router, React Router). Si vous essayez de monter un composant isolé contenant un `<Link>`, cela plantera.

Vous devez créer une commande `cy.mount()` personnalisée qui enveloppe votre composant avec les providers nécessaires.

```javascript title="cypress/support/component.js (React)"
import { mount } from 'cypress/react'
import { MemoryRouter } from 'react-router-dom'
import { ThemeProvider } from '../src/theme'

// Écraser cy.mount pour injecter le Router et le Theme
Cypress.Commands.add('mount', (component, options = {}) => {
  const { initialEntries = ['/'], ...mountOptions } = options

  const wrapped = (
    <ThemeProvider>
      <MemoryRouter initialEntries={initialEntries}>
        {component}
      </MemoryRouter>
    </ThemeProvider>
  )

  return mount(wrapped, mountOptions)
})
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Cypress Component Testing remplace avantageusement Jest/jsdom pour les composants qui reposent fortement sur le CSS, le DOM, ou des événements complexes. En testant le composant dans un vrai navigateur, vous voyez exactement ce que voit l'utilisateur. La règle d'or : utilisez le Component Testing pour tester la **logique visuelle isolée**, et utilisez le E2E Testing pour tester les **workflows complets**.

<br>
