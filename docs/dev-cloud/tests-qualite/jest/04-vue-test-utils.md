---
description: "Jest — Vue Test Utils : Tester des composants Vue.js de manière isolée avec le framework officiel."
icon: lucide/book-open-check
tags: ["JEST", "VUEJS", "TEST UTILS", "FRONTEND", "JAVASCRIPT"]
---

# 04 — Vue Test Utils + Jest

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Jest 29.x / Vue Test Utils 2.x"
  data-time="~3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    Tester un composant Vue sans outil dédié, c'est comme essayer d'inspecter un moteur en marche en se pendant par la fenêtre de la voiture. **Vue Test Utils** est votre banc de diagnostic : il extrait le moteur (le composant), le place sur un socle stable, vous permet de le démarrer (`mount`), de tourner les boutons (props/slots), et d'écouter les bruits (emits) de manière isolée et sécurisée.

**Vue Test Utils (VTU)** est la bibliothèque officielle pour tester des composants Vue.js. Contrairement à React Testing Library qui interdit l'accès à l'implémentation interne, Vue Test Utils offre une approche plus hybride : vous pouvez tester comme un utilisateur (ce qui est rendu dans le DOM), mais vous pouvez aussi inspecter directement l'instance Vue (les variables internes, les événements émis).

Combiné à Jest, VTU permet des tests rapides, fiables et complets pour vos composants Vue 3 (Composition API & Options API).

---

## 1. Installation et Configuration

Pour Vue 3 :

```bash
npm install --save-dev @vue/test-utils@next vue-jest@next
```

**Configuration de Jest (`jest.config.js`) :**

Il faut indiquer à Jest comment transformer les fichiers `.vue` (qui ne sont pas du JavaScript standard) en JS compréhensible.

```javascript title="jest.config.js"
module.exports = {
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['js', 'json', 'vue'],
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.js$': 'babel-jest'
  }
}
```

---

## 2. Principes de Base : `mount` vs `shallowMount`

- **`mount`** : Rend le composant **ET tous ses enfants**. C'est le comportement le plus proche de la réalité (test d'intégration).
- **`shallowMount`** : Rend le composant mais "stub" (remplace par un faux tag) tous les composants enfants. C'est le vrai test unitaire, utile si le composant a de très gros enfants complexes (ex: graphiques, appels API enfants).

*Recommandation : Utilisez `mount` par défaut, passez à `shallowMount` si le test devient trop lourd ou que les enfants posent problème.*

---

## 3. Exemple Complet : Composant Todo Item

Voici un composant Vue 3 (Composition API) qui accepte une prop, réagit au clic, et émet un événement.

```vue title="TodoItem.vue"
<template>
  <div class="todo-item" :class="{ completed: isDone }">
    <span class="title">{{ title }}</span>
    <button @click="toggleStatus" class="toggle-btn">
      {{ isDone ? 'Annuler' : 'Terminer' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['status-changed'])
const isDone = ref(false)

const toggleStatus = () => {
  isDone.value = !isDone.value
  emit('status-changed', { title: props.title, done: isDone.value })
}
</script>
```

### Le test associé avec Vue Test Utils

```javascript title="TodoItem.spec.js"
import { mount } from '@vue/test-utils'
import TodoItem from './TodoItem.vue'

describe('Composant TodoItem.vue', () => {

  it('affiche correctement le titre via la prop', () => {
    // 1. Monter le composant avec des props
    const wrapper = mount(TodoItem, {
      props: {
        title: 'Faire les courses'
      }
    })

    // 2. Vérifier le DOM
    expect(wrapper.find('.title').text()).toBe('Faire les courses')
    expect(wrapper.find('.toggle-btn').text()).toBe('Terminer')
    
    // Vérifier l'absence de classe initiale
    expect(wrapper.classes()).not.toContain('completed')
  })

  it('change d\'état et émet un événement au clic', async () => {
    const wrapper = mount(TodoItem, {
      props: { title: 'Apprendre Vue' }
    })

    // 1. Simuler l'action utilisateur
    // Note: await est obligatoire car Vue met à jour le DOM de façon asynchrone (nextTick)
    await wrapper.find('.toggle-btn').trigger('click')

    // 2. Vérifier que le DOM a bien été mis à jour
    expect(wrapper.find('.toggle-btn').text()).toBe('Annuler')
    expect(wrapper.classes()).toContain('completed')

    // 3. Vérifier les "Emits" (Les événements propagés vers le parent)
    expect(wrapper.emitted()).toHaveProperty('status-changed')
    
    // Le premier événement [0], premier argument [0] envoyé
    const eventPayload = wrapper.emitted('status-changed')[0][0]
    expect(eventPayload).toEqual({ title: 'Apprendre Vue', done: true })
  })
})
```

---

## 4. Concepts Avancés

### 4.1 Tester les Slots

Si vous développez des composants Layout ou UI (ex: Modal), vous devez tester l'insertion de contenu dans les slots.

```javascript
const wrapper = mount(Modal, {
  slots: {
    default: '<p>Contenu principal</p>',
    header: '<h1>Titre du Modal</h1>'
  }
})

expect(wrapper.html()).toContain('<p>Contenu principal</p>')
```

### 4.2 Mocker le Router Vue ou Pinia (Vuex)

Dans un composant réel, vous utilisez souvent `$route`, `$router` ou des stores globaux. Vous devez les mocker (les simuler) lors du montage pour éviter des erreurs "undefined is not an object".

```javascript
import { createTestingPinia } from '@pinia/testing'

const wrapper = mount(ProfileView, {
  global: {
    // 1. Mocker le store global (Pinia)
    plugins: [createTestingPinia({
      initialState: {
        user: { name: 'Admin', role: 'admin' }
      }
    })],
    // 2. Mocker les propriétés globales (Vue Router)
    mocks: {
      $route: {
        params: { id: '123' }
      },
      $router: {
        push: jest.fn() // On utilise un jest.fn() pour vérifier s'il est appelé !
      }
    }
  }
})

// Plus loin dans le test :
await wrapper.find('.btn-save').trigger('click')
expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/dashboard')
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Avec **Vue Test Utils**, la clé est de se concentrer sur l'API externe de votre composant : **ce qui rentre (Props, Slots)** et **ce qui sort (Emits, rendu DOM)**. Ne passez pas votre temps à tester que `ref(false)` devient `true`. Testez que quand l'utilisateur clique, la classe `.completed` apparaît bien dans le HTML. Utilisez `trigger()` et n'oubliez jamais le `await` pour attendre le prochain cycle de rendu de Vue.

<br>
