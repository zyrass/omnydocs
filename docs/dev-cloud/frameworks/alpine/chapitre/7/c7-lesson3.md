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

## Modal production-ready (UX) : overlay, fermeture propre, focus, scroll lock (concept)

### Objectif de la leçon

À la fin, tu sauras construire une modal qui fait “vrai produit” :

* ouverture/fermeture stable
* overlay cliquable (clic extérieur)
* fermeture avec Escape
* transitions propres (entrée/sortie)
* focus automatique dans la modal
* accessibilité de base (aria)
* comprendre le concept de **scroll lock** (bloquer le scroll derrière)

Une modal mal faite, c’est un piège UX classique :

* l’utilisateur se perd
* le clavier devient incohérent
* le scroll derrière bouge
* le focus n’est pas clair

On va faire ça proprement.

---

## 1) C’est quoi une modal, au niveau UI ?

Une modal est une “fenêtre au-dessus du contenu”.

Elle impose une action ou une lecture.

### Exemples typiques

* confirmation suppression
* formulaire d’ajout
* détails d’un article
* login

### Règle UX

Quand une modal est ouverte :

* tu dois comprendre que tu es “dans un autre contexte”
* tu dois pouvoir la fermer facilement
* le clavier doit rester utilisable

---

# 2) Les exigences minimum d’une modal sérieuse

Une modal “production-ready” doit gérer :

1. Un overlay (fond assombri)
2. Fermeture au clic extérieur
3. Fermeture avec Escape
4. Focus visible (clavier)
5. Focus initial (sur le champ ou le bouton principal)
6. Transition d’entrée/sortie
7. Optionnel mais important : scroll lock

---

## 3) Exemple complet : Modal propre avec Alpine (CDN)

Copie-colle tel quel.

```html
<div x-data="modalDemo()" @keydown.escape.window="close()">
  <button
    type="button"
    @click="openModal()"
    style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
  >
    Ouvrir modal
  </button>

  <!-- Overlay -->
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
    <!-- Modal -->
    <div
      x-show="open"
      x-transition.opacity.scale
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
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
      <div style="display:flex; justify-content:space-between; gap:10px; align-items:flex-start;">
        <div>
          <h2 id="modal-title" style="margin:0; font-size:18px;">
            Modal — Ajout d’article
          </h2>
          <p style="margin:6px 0 0; color:#666; font-size:14px;">
            Exemple réaliste : formulaire + fermeture propre + focus.
          </p>
        </div>

        <button
          type="button"
          @click="close()"
          aria-label="Fermer la modal"
          style="padding:8px 10px; border-radius:10px; border:1px solid #ddd; background:#fff;"
        >
          ✕
        </button>
      </div>

      <form @submit.prevent="submit()" style="margin-top: 12px; display:flex; flex-direction:column; gap:10px;">
        <label style="display:flex; flex-direction:column; gap:6px;">
          <span style="font-size:14px;">Titre</span>
          <input
            x-ref="title"
            type="text"
            x-model="form.title"
            placeholder="Ex: Comprendre x-for"
            style="padding:10px; border:1px solid #ddd; border-radius:10px;"
          />
        </label>

        <label style="display:flex; flex-direction:column; gap:6px;">
          <span style="font-size:14px;">Catégorie</span>
          <select
            x-model="form.category"
            style="padding:10px; border:1px solid #ddd; border-radius:10px; background:#fff;"
          >
            <option value="frontend">Frontend</option>
            <option value="backend">Backend</option>
            <option value="security">Security</option>
          </select>
        </label>

        <label style="display:flex; flex-direction:column; gap:6px;">
          <span style="font-size:14px;">Résumé</span>
          <textarea
            x-model="form.excerpt"
            rows="3"
            placeholder="Résumé rapide..."
            style="padding:10px; border:1px solid #ddd; border-radius:10px; resize: vertical;"
          ></textarea>
        </label>

        <div style="display:flex; gap:10px; justify-content:flex-end; margin-top: 6px;">
          <button
            type="button"
            class="secondary"
            @click="close()"
            style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
          >
            Annuler
          </button>

          <button
            type="submit"
            style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
          >
            Ajouter
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<script>
  function modalDemo() {
    return {
      open: false,

      form: {
        title: '',
        category: 'frontend',
        excerpt: '',
      },

      openModal() {
        this.open = true;

        // Focus propre après rendu
        this.$nextTick(() => {
          this.$refs.title.focus();
        });

        // Scroll lock (simple)
        document.body.style.overflow = 'hidden';
      },

      close() {
        this.open = false;

        // Restore scroll
        document.body.style.overflow = '';
      },

      submit() {
        // Validation simple
        if (!this.form.title.trim()) {
          alert('Le titre est obligatoire.');
          this.$nextTick(() => this.$refs.title.focus());
          return;
        }

        console.log('Article ajouté (mock):', this.form);
        alert('Article ajouté (mock)');

        // reset
        this.form.title = '';
        this.form.category = 'frontend';
        this.form.excerpt = '';

        this.close();
      },
    };
  }
</script>
```

---

# 4) Explication formateur : ce qui rend cette modal “pro”

## A) Overlay + fermeture au clic extérieur

On utilise :

```html
@click.self="close()"
```

Ça veut dire :

* si tu cliques sur l’overlay lui-même → fermeture
* si tu cliques dans la modal → ça ne ferme pas

C’est le comportement attendu.

---

## B) Fermeture Escape

On utilise :

```html
@keydown.escape.window="close()"
```

Pourquoi `.window` ?
Parce que tu veux capter Escape même si le focus est dans un input.

---

## C) Transitions

* overlay : `x-transition.opacity`
* modal : `x-transition.opacity.scale`

Donc tu as :

* fond qui apparaît en douceur
* modal qui “pop” légèrement

C’est propre, discret.

---

## D) Focus automatique (UX)

On fait :

```js
this.$nextTick(() => this.$refs.title.focus());
```

Sans ça :

* l’utilisateur doit cliquer dans le champ
* au clavier c’est mauvais

---

## E) Scroll lock (concept important)

Quand la modal est ouverte, tu ne veux pas scroller la page derrière.

La version simple :

```js
document.body.style.overflow = 'hidden';
```

Et quand tu fermes :

```js
document.body.style.overflow = '';
```

### Pourquoi c’est important ?

Sans scroll lock :

* tu scrolls derrière la modal
* tu perds ton contexte
* c’est un comportement “site cheap”

---

# 5) Pièges fréquents sur les modals

## Piège 1 — fermeture au clic n’importe où

Si tu fais :

```html
@click="close()"
```

sur l’overlay, tu fermes même quand tu cliques dans la modal.
C’est mauvais.

Tu dois faire `.self`.

---

## Piège 2 — oublier `x-cloak`

Sans `x-cloak`, tu peux voir la modal “flash” avant Alpine init.

---

## Piège 3 — pas de focus visible

Si tu n’as pas de style `:focus-visible`, le clavier est inutilisable.

Une modal sans navigation clavier, c’est une modal “pas finie”.

---

## Piège 4 — focus trap (avancé)

Le focus trap = empêcher l’utilisateur de sortir de la modal avec Tab.

C’est un sujet d’accessibilité avancée.
On le fera plus tard avec le plugin **Focus** (Chapitre 11).

Ici on fait déjà le minimum propre.

---

# 6) Mini exercice (obligatoire)

### Exercice A — Confirmation modal

Crée une modal “Confirmer suppression” avec :

* message
* bouton Annuler
* bouton Supprimer

### Exercice B — Focus initial différent

Au lieu de focus le titre :

* focus le bouton “Ajouter”

### Exercice C — Fermeture en cliquant sur X uniquement

Optionnel :

* supprime `@click.self`
* et garde fermeture X + Escape
  Compare l’UX.

---

## Résumé de la leçon

Une modal “production-ready” =

* overlay
* fermeture outside + Escape
* transition
* focus initial
* scroll lock (au minimum)

C’est exactement le genre de détail qui fait la différence entre :

* un code “qui marche”
* et un produit utilisable.

---

### Étape suivante logique

Chapitre 8 — Communication inter-composants (events custom)
Leçon 1 : `$dispatch` : envoyer un événement custom (toast, modal, tabs).
