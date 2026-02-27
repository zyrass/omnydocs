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

## Pattern “bus d’événements léger” (architecture simple sans framework lourd)

### Objectif de la leçon

À la fin, tu sauras :

* structurer une communication inter-composants propre
* créer un “bus d’événements” léger basé sur `$dispatch` + `.window`
* éviter le chaos quand tu as beaucoup de composants
* mettre en place une convention :

  * événements
  * payloads
  * responsabilités
* comprendre quand ce pattern suffit, et quand il faut passer au store (Chapitre 9)

Cette leçon, c’est le pont entre “petite UI” et “mini app”.

---

## 1) Pourquoi parler de “bus d’événements” ?

Un bus d’événements, c’est un système où :

* des composants émettent des messages (events)
* d’autres composants les reçoivent
* sans dépendance directe entre eux

C’est exactement ce qu’on fait avec :

* `$dispatch(...)`
* `@event.window="..."`

Mais si tu le fais “au hasard”, tu obtiens vite un projet illisible.

Donc on va formaliser une méthode simple.

---

# 2) Le bus d’événements Alpine : la version propre

## Les 3 règles d’or

### Règle 1 — Les composants ne se connaissent pas

Ils ne s’appellent pas entre eux directement.

Ils communiquent via events.

---

### Règle 2 — Les listeners globaux sont centralisés

Tu ne veux pas 25 composants qui écoutent `.window`.

Tu veux des “managers” :

* ToastManager
* ModalManager
* RouterManager (si besoin)
* ThemeManager

---

### Règle 3 — Un événement = une intention claire

Tu n’envoies pas “update”.
Tu envoies “ui:toast”, “ui:modal:open”, “blog:post:favorite”.

---

# 3) Convention de nommage recommandée (simple mais solide)

Voici une convention utilisable en production :

| Domaine | Exemple              | But               |
| ------- | -------------------- | ----------------- |
| UI      | `ui:toast`           | notifications     |
| UI      | `ui:modal:open`      | ouvrir une modal  |
| UI      | `ui:modal:close`     | fermer une modal  |
| Blog    | `blog:post:preview`  | preview d’un post |
| Blog    | `blog:post:favorite` | favoris           |
| Auth    | `auth:login`         | login (concept)   |

C’est verbeux.
Mais c’est clair.
Et surtout : ça évite les collisions.

---

# 4) Convention de payloads (contrats stables)

Un payload doit être :

* minimal
* stable
* explicite

Exemples :

### Toast

```js
{ type: 'success', message: '...' }
```

### Modal open

```js
{ name: 'confirm-delete', data: { id: 123 } }
```

### Favorite toggle

```js
{ postId: 3, favorite: true }
```

---

# 5) Exemple complet : mini app avec bus d’événements

On va faire une mini architecture :

* BlogList (émet des events)
* ToastManager (écoute ui:toast)
* ModalManager (écoute ui:modal:open)
* Un “logger” (optionnel) pour debug

Tout est découplé.

---

## Code complet (copie-colle)

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">

  <h2>Mini App — Event Bus Alpine</h2>
  <p style="color:#666;">
    BlogList dispatch des événements, ToastManager et ModalManager écoutent globalement.
  </p>

  <!-- BLOG LIST (émetteur) -->
  <div x-data="blogListBus()" style="border:1px solid #eee; background:#fff; padding:14px; border-radius:14px;">
    <h3 style="margin:0;">Articles</h3>

    <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
      <template x-for="post in posts" :key="post.id">
        <div style="border:1px solid #eee; border-radius:12px; padding:12px;">
          <div style="display:flex; justify-content:space-between; gap:10px;">
            <strong x-text="post.title"></strong>

            <button
              type="button"
              @click="toggleFavorite(post.id)"
              style="padding:8px 10px; border-radius:10px; border:1px solid #ddd; background:#fff;"
            >
              <span x-show="!post.favorite">☆</span>
              <span x-show="post.favorite" x-cloak>★</span>
            </button>
          </div>

          <p style="margin:8px 0 0; color:#666;" x-text="post.excerpt"></p>

          <div style="display:flex; gap:10px; margin-top:10px;">
            <button
              type="button"
              @click="preview(post.id)"
              style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
            >
              Lire (preview)
            </button>

            <button
              type="button"
              @click="confirmDelete(post.id)"
              style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
            >
              Supprimer (mock)
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>

  <!-- TOAST MANAGER (listener global) -->
  <div
    x-data="toastManagerBus()"
    @ui:toast.window="push($event.detail)"
    style="
      position: fixed;
      right: 16px;
      bottom: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 999;
    "
  >
    <template x-for="toast in toasts" :key="toast.id">
      <div
        x-show="!toast.closed"
        x-transition.opacity.scale
        style="
          width: 320px;
          background: #fff;
          border: 1px solid #eee;
          border-radius: 14px;
          padding: 12px;
          box-shadow: 0 10px 20px rgba(0,0,0,0.10);
          display: flex;
          justify-content: space-between;
          gap: 10px;
          align-items: flex-start;
        "
      >
        <div style="min-width:0;">
          <strong x-text="toast.type.toUpperCase()"></strong>
          <p style="margin:6px 0 0; color:#666;" x-text="toast.message"></p>
        </div>

        <button
          type="button"
          @click="close(toast.id)"
          aria-label="Fermer la notification"
          style="padding:6px 8px; border-radius:10px; border:1px solid #ddd; background:#fff;"
        >
          ✕
        </button>
      </div>
    </template>
  </div>

  <!-- MODAL MANAGER (listener global) -->
  <div
    x-data="modalManagerBus()"
    @ui:modal:open.window="openModal($event.detail)"
    @ui:modal:close.window="close()"
    @keydown.escape.window="close()"
  >
    <div
      x-show="open"
      x-cloak
      x-transition.opacity
      @click.self="close()"
      style="
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.55);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        z-index: 50;
      "
    >
      <div
        x-show="open"
        x-transition.opacity.scale
        role="dialog"
        aria-modal="true"
        style="
          width: 100%;
          max-width: 520px;
          background: #fff;
          border-radius: 16px;
          border: 1px solid #eee;
          padding: 16px;
          box-shadow: 0 20px 40px rgba(0,0,0,0.12);
        "
      >
        <div style="display:flex; justify-content:space-between; gap:10px;">
          <div>
            <h3 style="margin:0;">
              Modal : <span x-text="modalName"></span>
            </h3>
            <p style="margin:6px 0 0; color:#666; font-size:14px;">
              <strong>Données :</strong>
              <span x-text="JSON.stringify(modalData)"></span>
            </p>
          </div>

          <button
            type="button"
            @click="close()"
            style="padding:8px 10px; border-radius:10px; border:1px solid #ddd; background:#fff;"
          >
            ✕
          </button>
        </div>

        <div style="margin-top: 12px; display:flex; justify-content:flex-end; gap:10px;">
          <button
            type="button"
            @click="close()"
            style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
          >
            Fermer
          </button>

          <button
            type="button"
            @click="action()"
            style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
          >
            Action
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- DEBUG LOGGER (optionnel) -->
  <div
    x-data="{ last: '' }"
    @blog:event.window="last = JSON.stringify($event.detail)"
    style="margin-top: 14px; color:#666;"
  >
    Dernier event blog : <strong x-text="last"></strong>
  </div>
</div>

<script>
  function blogListBus() {
    return {
      posts: [
        { id: 1, title: "x-for + key", excerpt: "Liste stable et propre.", favorite: false },
        { id: 2, title: "$dispatch + events", excerpt: "Découpler les composants.", favorite: true },
        { id: 3, title: "Modal UX pro", excerpt: "Overlay, Escape, focus.", favorite: false },
      ],

      toggleFavorite(id) {
        const post = this.posts.find(p => p.id === id);
        if (!post) return;

        post.favorite = !post.favorite;

        // Event blog (debug)
        this.$dispatch('blog:event', {
          type: 'favorite:toggled',
          postId: id,
          favorite: post.favorite
        });

        // Toast global
        this.$dispatch('ui:toast', {
          type: post.favorite ? 'success' : 'info',
          message: post.favorite ? 'Ajouté aux favoris' : 'Retiré des favoris'
        });
      },

      preview(id) {
        const post = this.posts.find(p => p.id === id);
        if (!post) return;

        this.$dispatch('ui:modal:open', {
          name: 'post-preview',
          data: { id: post.id, title: post.title }
        });
      },

      confirmDelete(id) {
        this.$dispatch('ui:modal:open', {
          name: 'confirm-delete',
          data: { id }
        });
      }
    };
  }

  function toastManagerBus() {
    return {
      nextId: 1,
      toasts: [],

      push(payload) {
        const toast = {
          id: this.nextId++,
          type: payload.type ?? 'info',
          message: payload.message ?? 'Notification',
          closed: false,
        };

        this.toasts.unshift(toast);

        setTimeout(() => {
          this.close(toast.id);
        }, 2500);
      },

      close(id) {
        const toast = this.toasts.find(t => t.id === id);
        if (!toast) return;

        toast.closed = true;

        setTimeout(() => {
          this.toasts = this.toasts.filter(t => t.id !== id);
        }, 220);
      },
    };
  }

  function modalManagerBus() {
    return {
      open: false,
      modalName: '',
      modalData: null,

      openModal(payload) {
        this.modalName = payload?.name ?? 'unknown';
        this.modalData = payload?.data ?? null;

        this.open = true;
        document.body.style.overflow = 'hidden';
      },

      close() {
        this.open = false;
        document.body.style.overflow = '';
      },

      action() {
        // Exemple : action différente selon modalName
        if (this.modalName === 'confirm-delete') {
          alert('Mock: suppression confirmée');
        } else {
          alert('Mock: action modal');
        }

        this.close();
      }
    };
  }
</script>
```

---

# 6) Explication formateur : pourquoi c’est une mini architecture propre

## A) BlogList ne “connaît” pas ToastManager

Il dispatch `ui:toast`.

Le ToastManager écoute.

Découplage.

---

## B) BlogList ne “connaît” pas ModalManager

Il dispatch `ui:modal:open`.

Le ModalManager gère l’ouverture.

Découplage.

---

## C) Tu peux ajouter 10 composants

Ils peuvent tous :

* dispatch des toasts
* ouvrir des modals
  sans dépendance directe

C’est scalable.

---

# 7) Quand ce bus devient insuffisant ?

Ce pattern est excellent pour :

* UI events
* interactions globales
* petites apps

Mais si tu dois gérer un état partagé complexe :

* panier
* utilisateur connecté
* permissions
* données persistées
* synchronisation entre 5 composants

Alors le bus devient un patchwork.

À ce moment-là :

> tu passes au store global (Chapitre 9).

---

# 8) Pièges fréquents

## Piège A — tout passer en events

Si tu utilises des events pour gérer ton state principal, tu vas souffrir.

Events = déclencheurs d’actions UI
Store = état global partagé

---

## Piège B — listeners globaux partout

Centralise dans des managers.

---

## Piège C — event names incohérents

Si tu as :

* `toast`
* `uiToast`
* `UI:TOAST`
  Tu crées un enfer.

Reste strict :

* `ui:toast`
* `ui:modal:open`

---

# 9) Résumé de la leçon

* Le bus d’événements Alpine = `$dispatch` + `.window`
* Structure pro :

  * events nommés proprement
  * payload stable
  * managers centralisés
* C’est parfait avant d’introduire un store

---

## Mini exercice (obligatoire)

### Exercice A — Blog mock + toast

Dans ton atelier Blog mock :

* au clic favori → dispatch `ui:toast`

### Exercice B — Preview modal

Au clic “Lire” → dispatch `ui:modal:open`

### Exercice C — Event logger

Ajoute un composant qui écoute `blog:event.window`
et affiche le dernier event

---

### Étape suivante logique

On attaque **Chapitre 9 — Stores & architecture**
Leçon 1 : Pourquoi un store ? (éviter le chaos des states)
