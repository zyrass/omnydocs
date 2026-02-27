---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 2

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Persist plugin : `$persist` (simplifier, standardiser)

### Objectif de la leçon

À la fin, tu sauras :

* ce que fait exactement le plugin Persist
* pourquoi il est utile (même en production)
* comment l’utiliser proprement avec Alpine
* persister un state sans écrire toi-même :

  * `save()`
  * `load()`
  * `try/catch`
  * `localStorage.getItem()`
* éviter les pièges :

  * persistance trop large
  * données sensibles
  * collisions de clés

Cette leçon est importante car elle te fait gagner du temps, et rend ton code plus propre.

---

## 1) Pourquoi Persist est utile alors qu’on sait faire “à la main” ?

Oui, tu peux persister manuellement.

Mais ça te force à :

* écrire `save()` partout
* écrire `load()` partout
* penser à sauvegarder après chaque action
* gérer la clé localStorage
* gérer les erreurs

Le plugin Persist te donne une solution “standard”.

C’est comme passer de “je gère mon auth à la main” à “j’utilise une lib propre”.

---

# 2) C’est quoi `$persist` ?

`$persist` est une fonction fournie par le plugin Persist qui permet de rendre une variable :

* persistée automatiquement
* synchronisée avec `localStorage`

Exemple :

```js
items: $persist([])
```

Ça veut dire :

* `items` démarre avec `[]`
* si tu modifies `items`, Alpine sauvegarde automatiquement
* au refresh, Alpine recharge automatiquement

C’est exactement ce qu’on veut.

---

## 3) Installation du plugin Persist (CDN)

Dans ton HTML, tu dois charger :

1. Alpine core
2. Persist plugin

Exemple :

```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/persist@3.x.x/dist/cdn.min.js"></script>
```

Important :

* l’ordre compte
* les deux doivent être `defer`

---

# 4) Exemple complet : store grocery persisté avec `$persist`

On va refaire la liste de courses, mais cette fois :

* pas de `save()`
* pas de `load()`
* pas de `localStorage.getItem()`
* juste `$persist`

### Code complet (copie-colle)

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Persistance — Persist plugin ($persist)</h2>
  <p style="color:#666;">
    Ici la persistance est automatique, sans save/load manuels.
  </p>

  <div x-data="GroceryAddPersistPlugin()" style="border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Ajouter</h3>

    <form @submit.prevent="submit()" style="display:flex; gap:10px; margin-top:10px;">
      <input
        type="text"
        x-model="label"
        placeholder="Ex: Fromage"
        style="flex:1; padding:10px; border:1px solid #ddd; border-radius:10px;"
      />
      <button
        type="submit"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
      >
        Ajouter
      </button>
    </form>
  </div>

  <div x-data style="margin-top: 14px; border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Liste</h3>

    <p style="margin-top:10px; color:#666;">
      Total : <strong x-text="$store.grocery.items.length"></strong>
    </p>

    <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
      <template x-for="item in $store.grocery.items" :key="item.id">
        <div style="border:1px solid #eee; border-radius:12px; padding:12px; display:flex; justify-content:space-between; gap:10px; align-items:center;">
          <label style="display:flex; gap:10px; align-items:center; flex:1;">
            <input type="checkbox" :checked="item.done" @change="$store.grocery.toggleDone(item.id)" />
            <span
              x-text="item.label"
              :style="item.done ? 'text-decoration: line-through; color:#999;' : 'color:#111;'"
            ></span>
          </label>

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

    <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:12px;">
      <button
        type="button"
        @click="$store.grocery.clearDone()"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Supprimer terminés
      </button>

      <button
        type="button"
        @click="$store.grocery.reset()"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Reset
      </button>
    </div>
  </div>
</div>

<script>
  document.addEventListener('alpine:init', () => {
    Alpine.store('grocery', {
      // Persist automatique
      items: Alpine.$persist([]).as('alpine:grocery:items:v1'),

      addItem(label) {
        const value = String(label ?? '').trim();
        if (!value) return;

        this.items.unshift({
          id: Date.now() + Math.random(),
          label: value,
          done: false,
        });
      },

      removeItem(id) {
        this.items = this.items.filter(i => i.id !== id);
      },

      toggleDone(id) {
        const item = this.items.find(i => i.id === id);
        if (!item) return;
        item.done = !item.done;
      },

      clearDone() {
        this.items = this.items.filter(i => !i.done);
      },

      reset() {
        this.items = [];
      },
    });
  });

  function GroceryAddPersistPlugin() {
    return {
      label: '',

      submit() {
        const value = this.label.trim();
        if (!value) return;

        this.$store.grocery.addItem(value);
        this.label = '';
      },
    };
  }
</script>
```

---

# 5) Explication : ce que fait `.as('clé')`

Quand tu fais :

```js
items: Alpine.$persist([]).as('alpine:grocery:items:v1')
```

Tu définis explicitement la clé localStorage.

C’est une bonne pratique.

Sinon Alpine générera une clé automatiquement, mais tu perds le contrôle.

---

# 6) Ce que tu gagnes par rapport au stockage manuel

| Aspect      | Manuel                   | Persist plugin |
| ----------- | ------------------------ | -------------- |
| Sauvegarde  | tu dois appeler `save()` | automatique    |
| Chargement  | tu dois appeler `load()` | automatique    |
| Clé         | tu dois gérer            | `.as('...')`   |
| Maintenance | plus lourde              | très légère    |
| Lisibilité  | moyenne                  | excellente     |

---

# 7) Pièges fréquents avec Persist (important)

## Piège A — persister trop large

Si tu persist tout ton store :

* tu risques de stocker des données inutiles
* tu peux stocker des choses instables

Règle :

> persiste uniquement ce qui doit survivre au refresh

Exemples OK :

* items
* favoris
* settings

Exemples à éviter :

* flags de transitions
* open/close de dropdown

---

## Piège B — stocker des données sensibles

Ne persiste pas :

* token JWT
* infos personnelles
* données sensibles

localStorage est accessible au JS.
Donc en cas de XSS, c’est exposé.

C’est un point sécurité très important.

---

## Piège C — casser ton app avec une nouvelle structure

Si tu changes la structure des items (ex: tu ajoutes `priority`), tu dois prévoir une migration.

On va voir ça dans la leçon 3.

---

# 8) Mini exercice (obligatoire)

### Exercice A — Persister un thème

Crée un store `ui` :

* `theme: Alpine.$persist('light').as('alpine:ui:theme:v1')`
* bouton toggle

### Exercice B — Empêcher les doublons

Dans `addItem`, refuse les doublons.

### Exercice C — Ajouter un export JSON

Ajoute un bouton “Export JSON” qui affiche :

```js
console.log(JSON.stringify(this.items, null, 2));
```

---

## Résumé de la leçon

* Persist plugin rend la persistance automatique
* `$persist` est parfait pour garder un state stable
* `.as()` permet de contrôler la clé
* attention aux données sensibles et à la structure future

---

### Étape suivante logique

**Leçon 3 — Reset / migration / export import : bonnes pratiques “projet réel”**
Là on fait la vraie différence entre un tuto et une application sérieuse.
