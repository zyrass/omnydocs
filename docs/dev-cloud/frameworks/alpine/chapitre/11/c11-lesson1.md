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

## Persist : standardiser les données (bon usage, vrai projet)

### Objectif de la leçon

À la fin, tu sauras :

* utiliser Persist proprement dans un vrai projet
* décider quoi persister et quoi ne pas persister
* standardiser tes clés de stockage
* éviter les erreurs classiques :

  * persister du state UI inutile
  * persister des données sensibles
  * collisions entre projets
* appliquer Persist sur :

  * une liste (courses)
  * des favoris (blog)
  * un thème (UI globale)

Ici on ne réexplique pas `$persist` comme un tuto basique.
On le met au niveau “architecture propre”.

---

## 1) Persist en production : ce que tu dois comprendre

Persist est une solution rapide et efficace.
Mais il faut le traiter comme une vraie décision d’architecture.

### Persist est parfait pour :

* settings utilisateur (thème)
* préférences (filtres par défaut)
* données locales (liste courses, favoris)
* mode offline simple

### Persist est dangereux pour :

* tokens JWT
* données personnelles
* secrets
* infos sensibles

Pourquoi ?
Parce que `localStorage` est lisible par JavaScript.
Et si un jour tu as une faille XSS, c’est récupérable.

Tu vois le lien avec la sécurité :
c’est exactement ce que tu enseignes déjà en cybersécurité.

---

# 2) Convention de clés (standard pro)

Tu dois standardiser tes clés, sinon tu vas te perdre.

Format recommandé :

```
alpine:<app>:<store>:<field>:v<version>
```

Exemples :

* `alpine:omnydocs:grocery:items:v1`
* `alpine:omnydocs:ui:theme:v1`
* `alpine:blog:favorites:ids:v1`

Même si c’est long :

* c’est clair
* ça évite les collisions
* ça te permet de migrer

---

# 3) Exemple complet : 3 persistences utiles dans une app

On va faire :

1. store `grocery` : persister `items`
2. store `blog` : persister `favoriteIds`
3. store `ui` : persister `theme`

---

## Code complet (copie-colle)

Ce code suppose que tu as bien installé Persist plugin.

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Persist — Usage pro (liste + favoris + thème)</h2>
  <p style="color:#666;">
    3 stores, 3 persistences utiles, clés standardisées.
  </p>

  <!-- UI -->
  <div x-data style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom: 12px;">
    <button
      type="button"
      @click="$store.ui.toggleTheme()"
      style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
    >
      Thème : <strong x-text="$store.ui.theme"></strong>
    </button>
  </div>

  <!-- Grocery -->
  <div x-data="GroceryAddPersistPro()" style="border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Liste de courses (persistée)</h3>

    <form @submit.prevent="submit()" style="display:flex; gap:10px; margin-top:10px;">
      <input
        type="text"
        x-model="label"
        placeholder="Ex: Lait"
        style="flex:1; padding:10px; border:1px solid #ddd; border-radius:10px;"
      />
      <button
        type="submit"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
      >
        Ajouter
      </button>
    </form>

    <div style="display:flex; flex-direction:column; gap:10px; margin-top:12px;">
      <template x-for="item in $store.grocery.items" :key="item.id">
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

  <!-- Blog favoris -->
  <div x-data style="margin-top: 14px; border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Blog (favoris persistés)</h3>

    <div style="display:flex; flex-direction:column; gap:10px; margin-top:12px;">
      <template x-for="post in $store.blog.posts" :key="post.id">
        <div style="border:1px solid #eee; border-radius:12px; padding:12px; display:flex; justify-content:space-between; gap:10px;">
          <div style="min-width:0;">
            <strong x-text="post.title"></strong>
            <p style="margin:6px 0 0; color:#666;" x-text="post.excerpt"></p>
          </div>

          <button
            type="button"
            @click="$store.blog.toggleFavorite(post.id)"
            style="padding:8px 10px; border-radius:10px; border:1px solid #ddd; background:#fff;"
          >
            <span x-show="!$store.blog.isFavorite(post.id)">☆</span>
            <span x-show="$store.blog.isFavorite(post.id)" x-cloak>★</span>
          </button>
        </div>
      </template>
    </div>
  </div>
</div>

<script>
  document.addEventListener('alpine:init', () => {
    Alpine.store('ui', {
      theme: Alpine.$persist('light').as('alpine:omnydocs:ui:theme:v1'),

      toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
      },
    });

    Alpine.store('grocery', {
      items: Alpine.$persist([]).as('alpine:omnydocs:grocery:items:v1'),

      addItem(label) {
        const value = String(label ?? '').trim();
        if (!value) return;

        this.items.unshift({
          id: Date.now() + Math.random(),
          label: value,
        });
      },

      removeItem(id) {
        this.items = this.items.filter(i => i.id !== id);
      },
    });

    Alpine.store('blog', {
      posts: [
        { id: 1, title: 'x-for + key', excerpt: 'Listes stables et propres.' },
        { id: 2, title: '$dispatch', excerpt: 'Communication inter-composants.' },
        { id: 3, title: 'Stores Alpine', excerpt: 'Architecture légère.' },
      ],

      // On persiste seulement les IDs favoris, pas tout le post
      favoriteIds: Alpine.$persist([]).as('alpine:omnydocs:blog:favorites:ids:v1'),

      isFavorite(id) {
        return this.favoriteIds.includes(id);
      },

      toggleFavorite(id) {
        if (this.isFavorite(id)) {
          this.favoriteIds = this.favoriteIds.filter(x => x !== id);
          return;
        }

        this.favoriteIds = [...this.favoriteIds, id];
      },
    });
  });

  function GroceryAddPersistPro() {
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

# 4) Explication : pourquoi on persiste “favoriteIds” et pas les posts

C’est une décision pro.

Les posts peuvent venir :

* d’une API
* d’un fichier
* d’un build

Donc les persister est inutile.

Ce que tu veux persister :

* le choix utilisateur (favoris)

Donc on stocke seulement :

* `[1, 3]`

C’est léger, stable, maintenable.

---

# 5) Pièges fréquents (niveau sérieux)

## Piège A — persister un store complet “par facilité”

Tu vas persister :

* du bruit
* des données inutiles
* parfois des données qui changent de structure

Et ton app devient fragile.

---

## Piège B — pas de version dans la clé

Si tu changes le format :

* tu dois migrer
* sinon ça casse

Donc version dans la clé = bon réflexe.

---

## Piège C — persister des données sensibles

Je le répète parce que c’est important :

* pas de JWT
* pas de tokens
* pas de secrets

Même si ça “marche”.

---

# 6) Mini exercice (obligatoire)

### Exercice A — Ajouter une persistance “filter”

Dans le store blog, ajoute :

* `favoritesOnly: Alpine.$persist(false).as('...')`

Puis dans un composant UI, fais un toggle.

### Exercice B — Reset ciblé

Ajoute une action `resetFavorites()` qui remet `favoriteIds = []`.

### Exercice C — Migration légère

Change la clé version :

* `...:v1` → `...:v2`
  Observe : ça reset automatiquement car clé différente.

---

## Résumé de la leçon

* Persist est excellent mais doit être utilisé avec discipline
* standardise tes clés
* persiste uniquement ce qui doit survivre
* évite les données sensibles
* stocke le minimum utile (IDs, settings)

---

### Étape suivante logique

Chapitre 11 — Plugins & Accessibilité
**Leçon 2 — Focus : navigation clavier sérieuse (focus trap, focus restore)**
Là on entre dans le niveau “AAA mindset” pour de vrai.
