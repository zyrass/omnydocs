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

## Focus : navigation clavier sérieuse (focus trap, focus restore)

### Objectif de la leçon

À la fin, tu sauras :

* pourquoi l’accessibilité clavier est obligatoire (même sur des “petites UI”)
* ce que veut dire :

  * **focus**
  * **focus trap**
  * **focus restore**
* utiliser le plugin **Focus** d’Alpine proprement
* construire une **modal accessible** :

  * fermeture Escape
  * fermeture clic extérieur
  * focus bloqué dans la modal
  * retour du focus sur le bouton d’ouverture

Cette leçon est un gros niveau.
C’est là que tu passes du “ça marche” au “c’est pro”.

---

## 1) Comprendre le focus (simple et clair)

Le **focus**, c’est l’élément qui reçoit les actions clavier.

Exemples :

* quand tu appuies sur `Tab`, tu changes le focus
* quand tu appuies sur `Enter`, c’est l’élément focus qui est activé
* quand tu tapes du texte, c’est l’input focus qui le reçoit

Tu peux le voir dans le navigateur :

* un bouton entouré
* un input actif

---

## 2) Pourquoi c’est critique en accessibilité ?

Parce que certaines personnes naviguent :

* sans souris (clavier uniquement)
* avec des outils d’assistance
* sur mobile avec clavier externe
* avec des limitations motrices

Si ton site n’est pas utilisable au clavier :

* tu bloques des utilisateurs
* tu es hors des bonnes pratiques
* et en entreprise, ça peut devenir un problème légal / contractuel

---

# 3) Le problème classique des modals (UX + accessibilité)

Une modal non accessible fait ça :

* tu ouvres la modal
* tu appuies sur `Tab`
* et le focus part derrière la modal (sur le site)
* tu peux cliquer derrière
* tu peux “perdre” la navigation

C’est une expérience mauvaise.

---

# 4) Focus trap : définition

**Focus trap** = “piège à focus”.

Ça veut dire :

> tant que la modal est ouverte, le focus reste à l’intérieur.

Donc si tu fais `Tab` 20 fois :

* tu tournes dans la modal
* tu ne sors pas dehors

C’est exactement ce que font les UI pro.

---

# 5) Focus restore : définition

Quand tu fermes la modal, tu dois :

> remettre le focus là où il était avant

Exemple :

* tu cliques sur “Ouvrir la modal”
* la modal s’ouvre
* tu la fermes
* le focus revient sur le bouton “Ouvrir”

Sinon tu crées un “trou noir” :

* l’utilisateur clavier ne sait plus où il est

---

# 6) Installation du plugin Focus (CDN)

Tu dois charger :

1. Alpine core
2. Focus plugin

Exemple :

```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js"></script>
```

Encore une fois :

* ordre important
* `defer` obligatoire

---

# 7) Exemple complet : Modal accessible avec Focus plugin

### Objectif

On veut une modal qui :

* s’ouvre au clic
* se ferme :

  * au clic extérieur
  * avec Escape
  * avec un bouton “Fermer”
* bloque le focus dedans
* restaure le focus sur le bouton d’ouverture

---

## Code complet (copie-colle)

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Plugin Focus — Modal accessible</h2>
  <p style="color:#666;">
    Teste au clavier : Tab, Shift+Tab, Escape.
  </p>

  <div x-data="AccessibleModal()" style="margin-top:12px;">
    <!-- Bouton d'ouverture -->
    <button
      type="button"
      x-ref="openBtn"
      @click="open()"
      style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
    >
      Ouvrir la modal
    </button>

    <!-- Overlay + modal -->
    <div
      x-show="isOpen"
      x-cloak
      x-transition.opacity
      style="position:fixed; inset:0; display:flex; align-items:center; justify-content:center; padding:16px; background:rgba(0,0,0,0.55);"
      @keydown.escape.window="close()"
      @click.self="close()"
    >
      <div
        x-trap="isOpen"
        x-transition.scale
        style="width:min(520px, 100%); background:#fff; border-radius:16px; padding:16px; border:1px solid #eee;"
      >
        <h3 style="margin:0;">Modal accessible</h3>
        <p style="margin-top:10px; color:#666;">
          Le focus est piégé ici. Tu ne peux pas tabuler sur le site derrière.
        </p>

        <div style="display:flex; flex-direction:column; gap:10px; margin-top:12px;">
          <label style="display:flex; flex-direction:column; gap:6px;">
            <span>Nom</span>
            <input
              type="text"
              placeholder="Ex: Alain"
              style="padding:10px; border:1px solid #ddd; border-radius:10px;"
            />
          </label>

          <label style="display:flex; flex-direction:column; gap:6px;">
            <span>Email</span>
            <input
              type="email"
              placeholder="Ex: alain@mail.fr"
              style="padding:10px; border:1px solid #ddd; border-radius:10px;"
            />
          </label>

          <div style="display:flex; gap:10px; justify-content:flex-end; margin-top:10px;">
            <button
              type="button"
              @click="close()"
              style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
            >
              Fermer
            </button>

            <button
              type="button"
              @click="confirm()"
              style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
            >
              Confirmer
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  function AccessibleModal() {
    return {
      isOpen: false,

      open() {
        this.isOpen = true;
      },

      close() {
        this.isOpen = false;
        // Restore focus (retour sur le bouton d'ouverture)
        this.$nextTick(() => {
          this.$refs.openBtn.focus();
        });
      },

      confirm() {
        alert('Action confirmée.');
        this.close();
      },
    };
  }
</script>
```

---

# 8) Explication formateur : ce qui rend cette modal “pro”

## A) `x-trap="isOpen"`

C’est le plugin Focus en action.

Il piège le focus à l’intérieur tant que `isOpen` est vrai.

---

## B) Fermeture `Escape`

```html
@keydown.escape.window="close()"
```

Important :

* `.window` permet d’écouter même si le focus est dans un input

---

## C) Fermeture au clic extérieur

```html
@click.self="close()"
```

Ça veut dire :

* si tu cliques sur l’overlay (le fond)
* tu fermes
* si tu cliques dans la modal, ça ne ferme pas

---

## D) Focus restore

On utilise :

```js
this.$refs.openBtn.focus();
```

Mais attention :
on le fait dans un `$nextTick()`.

Pourquoi ?
Parce que quand tu fermes la modal, le DOM change.
Donc tu attends le tick suivant pour être sûr que le bouton existe et est visible.

---

# 9) Pièges fréquents (très important)

## Piège A — oublier `x-cloak`

Sans `x-cloak`, tu vas voir la modal apparaître 0.2 secondes au chargement.

C’est moche et pas pro.

---

## Piège B — modal sans focus trap

Tu peux avoir une modal “jolie”…
mais inutilisable au clavier.

Donc : `x-trap` obligatoire.

---

## Piège C — focus restore oublié

Tu fermes la modal, l’utilisateur est perdu.

Ça fait “bug” même si techniquement tout marche.

---

## Piège D — pas de bouton de fermeture

Tu dois toujours fournir un bouton clair “Fermer”.
Tout le monde ne pense pas à Escape.

---

# 10) Mini exercice (obligatoire)

### Exercice A — Auto-focus dans la modal

Quand la modal s’ouvre, focus sur le premier input.

Indice :

* `x-ref="firstInput"`
* `$nextTick(() => this.$refs.firstInput.focus())`

### Exercice B — Modal “confirmation”

Crée une modal qui demande :

* “Tu es sûr ?”
  Boutons :
* Annuler
* Supprimer

### Exercice C — Modal multi-step

Ajoute un état `step = 1 | 2`
Et fais un mini wizard.

---

## Résumé de la leçon

* focus = navigation clavier
* focus trap = empêcher le focus de sortir
* focus restore = remettre le focus au bon endroit
* plugin Focus + `x-trap` = modal accessible et pro

---

### Étape suivante logique

Chapitre 11 — Plugins officiels & Accessibilité
**Leçon 3 — Intersect : lazy load / animations au scroll sans perf-kill**
On va faire du moderne, mais propre et performant.
