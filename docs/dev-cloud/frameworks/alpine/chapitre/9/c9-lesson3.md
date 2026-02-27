---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 3

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Séparer UI store / Data store (lisibilité & maintenance)

### Objectif de la leçon

À la fin, tu sauras :

* structurer une application Alpine en séparant :

  * l’état UI (interface)
  * l’état Data (données)
* éviter de transformer ton store en “monstre”
* décider quoi mettre dans un store, et quoi laisser dans `x-data`
* créer plusieurs stores propres, au lieu d’un seul store géant
* préparer le terrain pour :

  * persistance (Chapitre 10)
  * plugins (Chapitre 11)
  * app complète (Projet fil rouge)

---

## 1) Le problème classique : le store devient un fourre-tout

Quand tu découvres les stores, tu as un réflexe naturel :

> “Cool, je vais tout mettre dans le store.”

Et tu finis avec :

* `items`
* `openModal`
* `activeTab`
* `searchQuery`
* `theme`
* `toastQueue`
* `selectedItemId`
* etc.

Résultat :

* store énorme
* difficile à lire
* difficile à maintenir
* responsabilités mélangées

Donc on doit structurer.

---

# 2) Règle simple : UI state ≠ Data state

## A) UI state (interface)

C’est ce qui concerne l’affichage, les interactions, la présentation.

Exemples :

* dropdown ouvert ou non
* onglet actif
* modal ouverte ou non
* filtre “favoris seulement”
* input focus
* animations / transitions flags

Ce state est souvent :

* temporaire
* local
* spécifique à un composant

Donc :

> UI state = `x-data` (dans 80% des cas)

---

## B) Data state (données)

C’est ce qui représente ton application.

Exemples :

* liste de courses
* posts
* favoris
* tickets de paris
* stats
* utilisateur

Ce state doit être :

* cohérent
* partagé
* réutilisable

Donc :

> Data state = store global

---

# 3) Exemple concret : Blog mock

Tu as :

### Data state (store)

* `posts[]`
* `favorites[]` ou `favorite` dans chaque post
* actions :

  * `toggleFavorite(id)`
  * `removePost(id)`

### UI state (local)

* `searchQuery`
* `selectedCategory`
* `favoritesOnly`
* `sortBy`

Pourquoi ?
Parce que :

* la recherche et les filtres sont des “vues”
* les posts sont des “données”

---

# 4) Exemple concret : Tracker de paris (ton cas réel)

### Data state

* tickets
* résultats
* capital
* historique

### UI state

* filtre “safe / montante / mega”
* tri “cote / date”
* modal “détails ticket”
* affichage mobile/desktop

Ce découpage rend ton app clean.

---

# 5) Pattern pro : plusieurs stores spécialisés

Tu peux avoir :

* `Alpine.store('grocery', ...)`
* `Alpine.store('theme', ...)`
* `Alpine.store('ui', ...)` (optionnel)

### Pourquoi “ui store” est optionnel ?

Parce que beaucoup de UI state peut rester local.

Mais parfois tu as un UI state global :

* thème dark/light
* langue
* layout global
* sidebar ouverte dans tout le site

Dans ce cas, un store UI global est justifié.

---

# 6) Exemple complet : 2 stores séparés (data + ui)

On va faire :

* store `grocery` (data)
* store `ui` (UI globale)

### Code complet

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Architecture — Data store + UI store</h2>

  <!-- UI globale -->
  <div x-data style="display:flex; gap:10px; align-items:center; margin-bottom: 12px;">
    <button
      type="button"
      @click="$store.ui.toggleTheme()"
      style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
    >
      Thème : <strong x-text="$store.ui.theme"></strong>
    </button>

    <button
      type="button"
      @click="$store.ui.toggleSidebar()"
      style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
    >
      Sidebar : <strong x-text="$store.ui.sidebarOpen ? 'open' : 'closed'"></strong>
    </button>
  </div>

  <div style="display:flex; gap:12px; align-items:flex-start;">
    <!-- Sidebar UI -->
    <div
      x-data
      x-show="$store.ui.sidebarOpen"
      x-transition.opacity.scale
      style="width: 240px; border:1px solid #eee; border-radius:14px; padding:12px; background:#fff;"
    >
      <strong>Sidebar</strong>
      <p style="margin-top:8px; color:#666;">
        UI globale contrôlée par store "ui".
      </p>
    </div>

    <!-- Main -->
    <div style="flex:1; border:1px solid #eee; border-radius:14px; padding:12px; background:#fff;">
      <h3 style="margin:0;">Liste de courses</h3>

      <!-- UI locale (search) -->
      <div x-data="{ query: '' }" style="margin-top:10px;">
        <input
          type="text"
          x-model="query"
          placeholder="Recherche locale..."
          style="width:100%; padding:10px; border:1px solid #ddd; border-radius:10px;"
        />

        <div style="display:flex; gap:10px; margin-top:10px;">
          <input
            type="text"
            x-model="$store.grocery.input"
            placeholder="Ajouter un item..."
            style="flex:1; padding:10px; border:1px solid #ddd; border-radius:10px;"
          />
          <button
            type="button"
            @click="$store.grocery.addFromInput()"
            style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
          >
            Ajouter
          </button>
        </div>

        <div style="display:flex; flex-direction:column; gap:10px; margin-top:12px;">
          <template
            x-for="item in $store.grocery.items.filter(i => i.label.toLowerCase().includes(query.toLowerCase()))"
            :key="item.id"
          >
            <div style="border:1px solid #eee; border-radius:12px; padding:12px; display:flex; justify-content:space-between; align-items:center;">
              <span x-text="item.label"></span>
              <button
                type="button"
                @click="$store.grocery.removeItem(item.id)"
                style="padding:8px 10px; border-radius:10px; border:1px solid #ddd; background:#fff;"
              >
                Supprimer
              </button>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  document.addEventListener('alpine:init', () => {
    // UI store (global interface state)
    Alpine.store('ui', {
      theme: 'light',
      sidebarOpen: true,

      toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
      },

      toggleSidebar() {
        this.sidebarOpen = !this.sidebarOpen;
      },
    });

    // Data store (application data)
    Alpine.store('grocery', {
      input: '',
      items: [],

      addFromInput() {
        const value = this.input.trim();
        if (!value) return;

        this.items.unshift({
          id: Date.now() + Math.random(),
          label: value,
        });

        this.input = '';
      },

      removeItem(id) {
        this.items = this.items.filter(i => i.id !== id);
      },
    });
  });
</script>
```

---

# 7) Explication : pourquoi c’est une architecture saine

## A) Le store `ui` ne touche pas aux données

Il gère :

* thème
* sidebar

C’est de l’interface.

---

## B) Le store `grocery` gère les données

Il gère :

* items
* ajout/suppression

C’est du “métier”.

---

## C) La recherche reste locale

La recherche (`query`) n’a pas besoin d’être globale.

C’est juste une vue.

Donc :

* `x-data="{ query: '' }"`

C’est propre et logique.

---

# 8) Pièges fréquents (et décisions pro)

## Piège A — mettre la recherche dans le store data

Tu peux, mais ça pollue ton store.

Si tu as 5 pages différentes, tu vas te retrouver avec :

* `queryPageA`
* `queryPageB`
* etc.

Mauvais.

---

## Piège B — un store “app” gigantesque

Tu peux faire :

```js
Alpine.store('app', {...})
```

Mais tu vas le regretter.

Meilleure pratique :

* stores spécialisés
* responsabilités claires

---

## Piège C — UI state global inutile

Si ton sidebar n’est visible que dans un composant, pas besoin de store.

Règle :

> store UI global seulement si plusieurs composants en dépendent.

---

# 9) Résumé de la leçon

* sépare UI state et Data state
* data partagée → store
* UI locale → x-data
* plusieurs stores spécialisés > un store monolithe

---

## Mini exercice (obligatoire)

### Exercice A — Découpage Blog mock

Fais 2 listes :

* ce qui doit aller dans un store data
* ce qui doit rester en UI local

### Exercice B — Tracker paris

Découpe ton projet en :

* store `tickets`
* store `bankroll`
* UI local “filtre/tri”

---

### Étape suivante logique

**Leçon 4 — Utiliser le store dans plusieurs composants : patterns propres**
On va faire un vrai exemple multi-composants propre et lisible, avec des actions bien nommées et des composants spécialisés.
