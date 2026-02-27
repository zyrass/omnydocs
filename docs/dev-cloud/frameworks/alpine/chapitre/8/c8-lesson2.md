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

## Écoute des custom events (`.window`) : découplage propre

### Objectif de la leçon

À la fin, tu sauras :

* écouter des événements custom de manière propre et robuste
* comprendre la différence entre :

  * écoute locale
  * écoute globale (`.window`)
* structurer tes événements comme une mini-architecture
* éviter les collisions et le chaos (noms, payloads, responsabilités)
* appliquer ça à des cas réels :

  * ouvrir une modal depuis n’importe où
  * déclencher une notification globale
  * mettre à jour une UI multi-composants

---

## 1) Pourquoi “écouter proprement” est aussi important que dispatch

Si tu dispatches partout, mais que tes listeners sont :

* mal placés
* mal nommés
* trop nombreux
* trop génériques

Tu obtiens une application qui ressemble à :

* un réseau de câbles entremêlés
* où personne ne sait qui déclenche quoi

Le but ici : garder Alpine léger, mais structuré.

---

# 2) Écoute locale vs écoute globale

## A) Écoute locale (sans `.window`)

Exemple :

```html
<div @toast="...">
```

Tu écoutes uniquement les événements qui “bubblent” dans ce composant.

En clair :

* ça marche si l’émetteur est dans la même zone DOM
* sinon tu ne reçois rien

---

## B) Écoute globale (`.window`)

Exemple :

```html
<div @toast.window="...">
```

Tu écoutes sur la fenêtre.
Donc :

* n’importe quel composant peut dispatch
* le listener reçoit l’event

C’est la méthode la plus simple pour du cross-composants.

---

## 3) Exemple pédagogique : même événement, 2 listeners

### Code complet

```html
<div style="display:flex; gap:20px; flex-wrap:wrap;">

  <!-- Zone A -->
  <div x-data style="border:1px solid #ddd; padding:12px; border-radius:12px;">
    <strong>Zone A</strong>

    <button
      style="margin-top:10px; padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
      @click="$dispatch('ping', { from: 'Zone A' })"
    >
      Dispatch ping
    </button>

    <!-- Listener local -->
    <p style="margin-top:10px; color:#666;"
       @ping="console.log('LOCAL listener (Zone A) =>', $event.detail)">
      Listener local (ne reçoit pas forcément)
    </p>
  </div>

  <!-- Zone B -->
  <div x-data style="border:1px solid #ddd; padding:12px; border-radius:12px;">
    <strong>Zone B</strong>

    <button
      style="margin-top:10px; padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      @click="$dispatch('ping', { from: 'Zone B' })"
    >
      Dispatch ping
    </button>

    <!-- Listener global -->
    <p style="margin-top:10px; color:#666;"
       @ping.window="console.log('WINDOW listener =>', $event.detail)">
      Listener global (reçoit tout)
    </p>
  </div>

</div>
```

### Ce que tu dois observer

* le listener `.window` reçoit tous les `ping`
* le listener local reçoit seulement si l’event passe dans sa zone DOM

Conclusion :

> Pour un bus d’événements global simple : utilise `.window`.

---

# 4) Naming pro : comment éviter les collisions

Si tu nommes tes events :

* `open`
* `update`
* `change`
* `notify`

Tu vas finir avec :

* des collisions
* des comportements imprévisibles

## Convention recommandée

Utilise un namespace :

* `ui:toast`
* `ui:modal:open`
* `ui:modal:close`
* `blog:favorite:toggled`
* `cart:item:added`

Même si c’est “long”, c’est clair.

---

# 5) Payload pro : structure stable

Tu veux que tes listeners sachent exactement quoi attendre.

### Exemple “modal open”

Payload stable :

```js
{
  name: 'post-preview',
  data: { id: 3 }
}
```

### Exemple “toast”

Payload stable :

```js
{
  type: 'success',
  message: 'Ajouté'
}
```

Règle :

> un événement = un contrat.

---

# 6) Cas réel : ouvrir une modal depuis un autre composant

Tu veux un composant “ModalManager” qui écoute `ui:modal:open`.

Et n’importe quel composant peut l’ouvrir.

### Code complet

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">

  <!-- Boutons partout -->
  <div style="display:flex; gap:10px; flex-wrap:wrap;">
    <div x-data>
      <button
        @click="$dispatch('ui:modal:open', { name: 'post-preview', data: { id: 3 } })"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
      >
        Ouvrir preview post #3
      </button>
    </div>

    <div x-data>
      <button
        @click="$dispatch('ui:modal:open', { name: 'confirm-delete', data: { id: 99 } })"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Ouvrir confirm delete #99
      </button>
    </div>
  </div>

  <!-- Modal Manager -->
  <div
    x-data="modalManager()"
    @ui:modal:open.window="openModal($event.detail)"
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
        "
      >
        <div style="display:flex; justify-content:space-between; gap:10px; align-items:flex-start;">
          <div>
            <h2 style="margin:0; font-size:18px;">
              Modal : <span x-text="modalName"></span>
            </h2>
            <p style="margin:6px 0 0; color:#666; font-size:14px;">
              Payload : <strong x-text="JSON.stringify(modalData)"></strong>
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

        <div style="margin-top: 12px;">
          <button
            type="button"
            @click="close()"
            style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  function modalManager() {
    return {
      open: false,
      modalName: '',
      modalData: null,

      openModal(payload) {
        this.modalName = payload?.name ?? 'unknown';
        this.modalData = payload?.data ?? null;

        this.open = true;

        // scroll lock simple
        document.body.style.overflow = 'hidden';
      },

      close() {
        this.open = false;
        document.body.style.overflow = '';
      },
    };
  }
</script>
```

### Pourquoi c’est puissant

* aucun composant n’a besoin d’importer “la modal”
* tu peux ouvrir une modal depuis n’importe où
* ton UI reste découplée

---

# 7) Pièges fréquents (et comment éviter)

## Piège A — un seul event “ui:update” pour tout

Ça devient vite impossible à maintenir.

Préférer des events explicites.

---

## Piège B — payload “magique”

Si tu dispatch :

```js
$dispatch('ui:modal:open', post)
```

Tu envoies un objet complet, parfois énorme, parfois instable.
Mauvais.

Préférer :

* `id`
* ou un payload minimal stable

---

## Piège C — trop de listeners `.window`

Tu peux écouter `.window` partout… mais ce n’est pas une architecture.

Règle :

> Centralise les listeners globaux dans des “managers” (toast manager, modal manager).

---

# 8) Résumé de la leçon

* `.window` permet la communication globale entre composants
* structure tes events :

  * noms explicites (namespace)
  * payload stable
* centralise les listeners globaux dans un composant manager
* tu obtiens une mini architecture sans store

---

## Mini exercice (obligatoire)

### Exercice A — `ui:toast`

* dispatch `ui:toast` depuis 2 composants différents
* toast manager écoute `.window`

### Exercice B — `ui:modal:open`

* bouton dans Blog mock “Lire”
* dispatch open modal avec `{ id }`

### Exercice C — convention naming

Renomme tes events :

* `toast` → `ui:toast`
* `notify` → `ui:notify`
  Et vérifie que tout marche

---

### Étape suivante logique

**Leçon 3 — Pattern “bus d’événements léger” (sans framework lourd)**
On va formaliser une méthode simple pour que ton projet reste clean même avec 10+ composants.
