---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 1

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## `localStorage` : stockage manuel (sauvegarder / restaurer proprement)

### Objectif de la leçon

À la fin, tu sauras :

* comprendre ce qu’est `localStorage`
* sauvegarder un état (store) dans le navigateur
* restaurer cet état au chargement
* éviter les pièges classiques :

  * données corrompues
  * JSON invalide
  * reset impossible
  * incompatibilité de version (migration)
* faire une persistance “projet réel” sans plugin

Ici, on fait le niveau “fondation”.
Le plugin Persist viendra ensuite pour simplifier.

---

## 1) Pourquoi persister des données ?

Sans persistance, ton app est amnésique.

Tu ajoutes 20 items dans ta liste de courses…
Tu refresh…
Tout disparaît.

En projet réel, c’est inacceptable.

Donc on veut :

* survivre au refresh
* garder les favoris
* garder les settings
* garder les tickets

---

# 2) C’est quoi `localStorage` ?

`localStorage` est un stockage simple intégré au navigateur.

Caractéristiques :

* stocke des paires clé/valeur (key/value)
* la valeur est **toujours une chaîne de caractères**
* persiste même si tu fermes l’onglet
* accessible via JavaScript :

  * `localStorage.setItem(key, value)`
  * `localStorage.getItem(key)`
  * `localStorage.removeItem(key)`

---

## 3) Analogie simple (pour comprendre)

Imagine `localStorage` comme :

* un petit tiroir dans le navigateur
* tu peux y mettre des post-it (texte)
* tu peux les relire plus tard

Mais attention :

* tu ne peux pas mettre un objet directement
* tu dois écrire en texte

Donc :

> objets → JSON.stringify
> texte → JSON.parse

---

# 4) Règle pro : ne jamais stocker en vrac

Tu dois définir une clé stable, exemple :

* `alpine:grocery:v1`

Pourquoi ?
Parce que tu peux versionner.
Et éviter les conflits.

---

# 5) Exemple complet : persister le store grocery

On va reprendre notre store “courses”.

### Ce qu’on veut

* à chaque modification de la liste → sauvegarde
* au démarrage → restauration
* bouton reset → suppression localStorage + reset state

---

## Code complet (copie-colle)

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Persistance — localStorage (manuel)</h2>
  <p style="color:#666;">
    On persiste la liste de courses dans le navigateur.
  </p>

  <!-- Ajout -->
  <div x-data="GroceryAddPersist()" style="border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Ajouter</h3>

    <form @submit.prevent="submit()" style="display:flex; gap:10px; margin-top:10px;">
      <input
        type="text"
        x-model="label"
        placeholder="Ex: Pain"
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

  <!-- Liste -->
  <div x-data style="margin-top: 14px; border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Liste</h3>

    <p style="margin-top:10px; color:#666;">
      Total : <strong x-text="$store.grocery.totalCount"></strong>
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
        @click="$store.grocery.resetStorage()"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Reset + effacer stockage
      </button>
    </div>
  </div>
</div>

<script>
  document.addEventListener('alpine:init', () => {
    const STORAGE_KEY = 'alpine:grocery:v1';

    Alpine.store('grocery', {
      items: [],

      get totalCount() {
        return this.items.length;
      },

      // --- Persistance ---
      save() {
        try {
          const payload = {
            version: 1,
            items: this.items,
            savedAt: new Date().toISOString(),
          };

          localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
        } catch (err) {
          console.error('Erreur sauvegarde localStorage:', err);
        }
      },

      load() {
        try {
          const raw = localStorage.getItem(STORAGE_KEY);
          if (!raw) return;

          const parsed = JSON.parse(raw);

          // Validation minimale
          if (!parsed || parsed.version !== 1 || !Array.isArray(parsed.items)) {
            console.warn('Stockage invalide, reset automatique.');
            return;
          }

          // On restaure uniquement ce qu'on attend
          this.items = parsed.items.map(i => ({
            id: i.id,
            label: String(i.label ?? ''),
            done: Boolean(i.done),
          }));
        } catch (err) {
          console.error('Erreur lecture localStorage (JSON invalide ?):', err);
        }
      },

      resetStorage() {
        localStorage.removeItem(STORAGE_KEY);
        this.items = [];
      },

      // --- Actions ---
      addItem(label) {
        const value = String(label ?? '').trim();
        if (!value) return;

        this.items.unshift({
          id: Date.now() + Math.random(),
          label: value,
          done: false,
        });

        this.save();
      },

      removeItem(id) {
        this.items = this.items.filter(i => i.id !== id);
        this.save();
      },

      toggleDone(id) {
        const item = this.items.find(i => i.id === id);
        if (!item) return;
        item.done = !item.done;
        this.save();
      },

      clearDone() {
        this.items = this.items.filter(i => !i.done);
        this.save();
      },
    });

    // Chargement initial au démarrage
    Alpine.store('grocery').load();
  });

  function GroceryAddPersist() {
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

# 6) Explication formateur : ce qui est important ici

## A) `localStorage` stocke du texte

Donc on fait :

* `JSON.stringify(payload)` pour écrire
* `JSON.parse(raw)` pour lire

---

## B) On stocke un objet “versionné”

On stocke :

```js
{
  version: 1,
  items: [...],
  savedAt: "..."
}
```

Pourquoi ?
Parce que demain tu peux faire une version 2.

C’est exactement comme une API.

---

## C) On valide avant de restaurer

On vérifie :

* version attendue
* items est bien un tableau

Sinon :

* on ignore
* on évite de casser l’app

---

## D) On sauvegarde après chaque action

C’est la stratégie simple et efficace :

* add → save
* remove → save
* toggle → save

---

# 7) Pièges fréquents (à connaître)

## Piège 1 — JSON corrompu

Si le JSON est invalide :

* `JSON.parse()` crash

Donc tu dois toujours `try/catch`.

---

## Piège 2 — stocker trop de choses

`localStorage` n’est pas une base de données.

Tu stockes :

* un état léger
* des préférences
* des listes simples

Pas :

* des vidéos
* des milliers d’objets lourds

---

## Piège 3 — pas de bouton reset

En prod tu veux toujours :

* pouvoir réinitialiser l’état
* corriger un bug utilisateur

---

## Piège 4 — migration ignorée

Si demain tu changes la structure d’un item, tu dois prévoir une migration.

On va voir ça dans la leçon 3 du chapitre 10.

---

# 8) Mini exercice (obligatoire)

### Exercice A — Ajouter `updatedAt`

À chaque action, mets à jour un champ `updatedAt` dans le payload.

### Exercice B — Empêcher les labels vides ou trop longs

Refuse si `label.length > 40`.

### Exercice C — Ajouter un export JSON

Ajoute un bouton qui fait :

```js
navigator.clipboard.writeText(localStorage.getItem(STORAGE_KEY))
```

(avec un try/catch + toast si tu veux)

---

## Résumé de la leçon

* `localStorage` = persistance simple intégrée au navigateur
* stockage texte → JSON stringify/parse
* persistance pro = version + validation + reset
* sauvegarde après chaque action = cohérent et simple

---

### Étape suivante logique

**Leçon 2 — Persist plugin : `$persist` (simplifier, standardiser)**
Là tu vas voir pourquoi le plugin est une arme de confort énorme.
