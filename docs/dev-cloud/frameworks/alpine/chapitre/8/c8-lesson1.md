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

## `$dispatch` : envoyer un événement custom (toast, modal, tabs)

### Objectif de la leçon

À la fin, tu sauras :

* comprendre ce qu’est un événement custom
* utiliser `$dispatch()` pour envoyer un événement
* écouter cet événement dans un autre composant
* découpler tes composants (architecture propre)
* appliquer ce pattern à des cas réels :

  * toast notifications
  * ouverture de modal depuis un autre composant
  * tabs qui notifient un parent
  * UI multi-composants sans store

Ici on passe d’un Alpine “mono composant” à un Alpine “app”.

---

## 1) Le problème réel : les composants doivent communiquer

Quand ton UI grandit, tu as vite ce scénario :

* composant A : bouton “Ajouter”
* composant B : liste
* composant C : toast
* composant D : modal

Et tu veux que :

* A déclenche une action dans C
* B déclenche une action dans C
* D déclenche une action dans C

Sans architecture, tu finis avec :

* des variables globales
* du code fragile
* des dépendances partout

---

## 2) Définition simple : événement custom

Un événement custom, c’est comme un message.

* un composant “parle” : il envoie un événement
* un autre composant “écoute” : il réagit

### Analogie simple

Imagine une entreprise :

* le service “Ventes” envoie une notification : “Commande validée”
* le service “Logistique” écoute et prépare l’envoi
* le service “Support” écoute et ouvre un ticket

Ils ne se connaissent pas directement.
Ils parlent via un message standard.

---

# 3) `$dispatch` : comment ça marche

Syntaxe :

```js
$dispatch('event-name', { data: '...' })
```

* premier paramètre : nom de l’événement
* deuxième paramètre : payload (données)

---

## 4) Exemple minimal : envoyer + écouter

### Code complet

```html
<div style="display:flex; gap:20px; flex-wrap:wrap;">
  <!-- Composant A : émetteur -->
  <div x-data>
    <button
      @click="$dispatch('notify', { message: 'Hello depuis A' })"
      style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
    >
      Envoyer notification
    </button>
  </div>

  <!-- Composant B : récepteur -->
  <div
    x-data="{ last: '' }"
    @notify.window="last = $event.detail.message"
    style="border:1px solid #ddd; padding:12px; border-radius:12px; min-width:260px;"
  >
    <strong>Récepteur</strong>
    <p style="margin:8px 0 0; color:#666;">
      Dernier message :
      <span style="color:#111;" x-text="last"></span>
    </p>
  </div>
</div>
```

### Explication

* A envoie `notify`
* B écoute `@notify.window`
* `$event.detail` contient les données envoyées

---

# 5) Comprendre `$event.detail`

Quand tu dispatch un événement avec un payload :

```js
$dispatch('notify', { message: '...' })
```

Le récepteur récupère :

```js
$event.detail.message
```

Donc :

* `$event` = événement DOM
* `.detail` = ton payload

---

# 6) Pourquoi `.window` ?

Quand tu fais :

```html
@notify.window="..."
```

Tu dis :

* “écoute cet événement au niveau global de la fenêtre”
* donc même si l’événement est dispatch depuis un autre composant, ça marche

Sans `.window`, tu écoutes seulement dans la hiérarchie locale du DOM.

Règle pro :

> Pour communiquer entre composants séparés : `.window` est ton ami.

---

# 7) Cas réel #1 : Toast notifications (mini système propre)

On va faire un vrai mini système de toast :

* un composant “ToastManager” écoute `toast`
* n’importe quel composant peut dispatch `toast`

### Code complet (copie-colle)

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">

  <!-- Émetteurs -->
  <div style="display:flex; gap:10px; flex-wrap:wrap;">
    <div x-data>
      <button
        @click="$dispatch('toast', { type: 'success', message: 'Article ajouté !' })"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
      >
        Toast success
      </button>
    </div>

    <div x-data>
      <button
        @click="$dispatch('toast', { type: 'error', message: 'Erreur : champ manquant.' })"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Toast error
      </button>
    </div>

    <div x-data>
      <button
        @click="$dispatch('toast', { type: 'info', message: 'Info : sauvegarde en cours…' })"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Toast info
      </button>
    </div>
  </div>

  <!-- Toast Manager -->
  <div
    x-data="toastManager()"
    @toast.window="push($event.detail)"
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
</div>

<script>
  function toastManager() {
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

        // Auto close
        setTimeout(() => {
          this.close(toast.id);
        }, 2500);
      },

      close(id) {
        const toast = this.toasts.find(t => t.id === id);
        if (!toast) return;

        toast.closed = true;

        // remove after transition
        setTimeout(() => {
          this.toasts = this.toasts.filter(t => t.id !== id);
        }, 220);
      },
    };
  }
</script>
```

### Pourquoi c’est “pro”

* n’importe quel composant peut déclencher un toast
* le toast manager est unique
* transitions propres
* suppression propre (pattern de liste animée)
* pas de dépendance directe entre composants

---

# 8) Pièges fréquents avec `$dispatch`

## Piège A — nom d’événement trop générique

Si tu dispatch `update` ou `change`, tu vas créer des collisions.

Préférer :

* `toast`
* `modal:open`
* `blog:add`
* `cart:updated`

---

## Piège B — oublier `.window`

Si ton listener est :

```html
@toast="..."
```

Il écoutera seulement dans son scope DOM local.
Donc tu vas croire que “ça marche pas”.

Pour cross-composants :

* `@toast.window`

---

## Piège C — payload mal structuré

Tu veux un payload stable.

Exemple toast :

```js
{ type: 'success', message: '...' }
```

Ne change pas la forme toutes les 2 minutes.

---

# 9) Résumé de la leçon

* `$dispatch` permet d’envoyer un événement custom
* le listener récupère les données via `$event.detail`
* `.window` permet de communiquer entre composants séparés
* c’est une solution légère et clean pour :

  * toasts
  * modals
  * actions globales
    avant d’introduire un store (Chapitre 9)

---

## Mini exercice (obligatoire)

### Exercice A — Toast depuis le Blog mock

Dans ton atelier Blog :

* quand tu cliques “favori”
* dispatch un toast :

  * “Ajouté aux favoris”
  * ou “Retiré des favoris”

### Exercice B — Event “post:preview”

Quand tu cliques “Lire (mock)” :

* dispatch `post:preview` avec `{ id, title }`
* un composant récepteur affiche le dernier preview

### Exercice C — Event naming

Renomme `toast` en `ui:toast`
et adapte les listeners.

---

### Étape suivante logique

**Leçon 2 — Écoute custom events (`.window`) : découplage propre**
On va renforcer le pattern : qui écoute quoi, comment structurer tes événements comme une mini-architecture.
