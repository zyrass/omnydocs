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

## Intersect : lazy load / animations au scroll (UI moderne sans perf-kill)

### Objectif de la leçon

À la fin, tu sauras :

* ce que fait le plugin **Intersect**
* comprendre le concept d’**Intersection Observer** (sans jargon inutile)
* déclencher des actions quand un élément entre dans l’écran
* créer des effets modernes :

  * reveal au scroll
  * lazy loading simple
  * compteur animé
* éviter les pièges :

  * animations agressives
  * logique qui se relance 50 fois
  * effets inutiles qui détruisent les performances

Intersect est l’arme parfaite pour faire du “moderne” sans framework lourd.

---

## 1) C’est quoi Intersect ?

Intersect permet de détecter :

> quand un élément devient visible dans la zone affichée (viewport)

Le viewport = ce que tu vois à l’écran.

Donc quand tu scroll :

* certains blocs apparaissent
* Intersect peut déclencher un événement

---

## 2) Analogie simple

Imagine que tu es dans un magasin.

* Les rayons sont longs.
* Tu ne regardes pas tout en même temps.
* Tu ne t’intéresses qu’à ce qui est devant toi.

Intersect, c’est comme une caméra qui dit :

> “ce produit vient d’entrer dans ton champ de vision”

Et tu peux déclencher une action :

* animation
* chargement
* compteur
* etc.

---

# 3) Pourquoi c’est utile ?

Sans Intersect, beaucoup de dev font :

* `window.addEventListener('scroll', ...)`
* calculs en boucle
* 200 conditions
* performance détruite

Intersect s’appuie sur une API native du navigateur :

* propre
* optimisée
* stable

Donc :

> Intersect = scroll propre, sans bricolage

---

# 4) Installation du plugin Intersect (CDN)

Tu charges :

1. Alpine
2. Intersect

```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/intersect@3.x.x/dist/cdn.min.js"></script>
```

---

# 5) Les directives importantes

## A) `x-intersect`

Déclenche quand l’élément devient visible.

Exemple :

```html
<div x-intersect="visible = true"></div>
```

---

## B) `x-intersect.once`

Déclenche une seule fois.

C’est souvent ce que tu veux, sinon tu spam.

---

## C) `x-intersect:enter`

Quand l’élément entre dans le viewport.

---

## D) `x-intersect:leave`

Quand il sort.

---

# 6) Exemple 1 : Reveal au scroll (simple et propre)

### Objectif

Quand une section apparaît :

* elle fade + slide
* et ne se relance pas 10 fois

---

## Code complet (copie-colle)

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Plugin Intersect — Reveal au scroll</h2>
  <p style="color:#666;">
    Scroll vers le bas : les sections apparaissent.
  </p>

  <div style="height: 40vh; border:1px dashed #ddd; border-radius:14px; display:flex; align-items:center; justify-content:center;">
    <span style="color:#666;">Zone vide pour scroller</span>
  </div>

  <div x-data="{ shown: false }" style="margin-top: 16px;">
    <section
      x-intersect.once="shown = true"
      x-bind:style="shown
        ? 'opacity:1; transform: translateY(0); transition: 400ms ease;'
        : 'opacity:0; transform: translateY(18px);'"
      style="border:1px solid #eee; border-radius:16px; padding:16px; background:#fff;"
    >
      <h3 style="margin:0;">Section 1</h3>
      <p style="margin-top:10px; color:#666;">
        Apparition contrôlée par x-intersect.once.
      </p>
    </section>
  </div>

  <div style="height: 30vh;"></div>

  <div x-data="{ shown: false }">
    <section
      x-intersect.once="shown = true"
      x-bind:style="shown
        ? 'opacity:1; transform: translateY(0); transition: 400ms ease;'
        : 'opacity:0; transform: translateY(18px);'"
      style="border:1px solid #eee; border-radius:16px; padding:16px; background:#fff;"
    >
      <h3 style="margin:0;">Section 2</h3>
      <p style="margin-top:10px; color:#666;">
        Même pattern, réutilisable partout.
      </p>
    </section>
  </div>
</div>
```

---

# 7) Explication : pourquoi `.once` est important

Sans `.once`, si tu scroll :

* l’élément sort
* l’élément revient
* l’animation peut se relancer

Et ça peut devenir :

* agressif
* fatiguant
* instable

Donc :

> `.once` = UX stable

---

# 8) Exemple 2 : Lazy load “fake” (chargement progressif)

### Objectif

Quand un bloc devient visible :

* on simule un chargement
* puis on affiche le contenu

C’est utile pour :

* gros blocs
* sections lourdes
* charts
* UI complexes

---

## Code complet

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Intersect — Lazy load (simulation)</h2>

  <div style="height: 35vh;"></div>

  <div x-data="LazyBlock()" style="border:1px solid #eee; border-radius:16px; padding:16px; background:#fff;">
    <div x-intersect.once="load()">
      <h3 style="margin:0;">Bloc lazy</h3>

      <p x-show="loading" x-cloak style="margin-top:10px; color:#666;">
        Chargement...
      </p>

      <div x-show="loaded" x-cloak style="margin-top:10px;">
        <p style="color:#666; margin:0;">
          Contenu affiché seulement quand le bloc entre dans le viewport.
        </p>
      </div>
    </div>
  </div>
</div>

<script>
  function LazyBlock() {
    return {
      loading: false,
      loaded: false,

      load() {
        if (this.loaded || this.loading) return;

        this.loading = true;

        // Simulation d'une requête
        setTimeout(() => {
          this.loading = false;
          this.loaded = true;
        }, 600);
      },
    };
  }
</script>
```

---

# 9) Exemple 3 : Compteur animé au scroll (effet “stats”)

### Objectif

Quand le bloc apparaît :

* on anime un compteur de 0 → target

C’est classique dans les pages marketing.

---

## Code complet

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Intersect — Compteur animé</h2>

  <div style="height: 35vh;"></div>

  <div x-data="CounterOnView(1185)" style="border:1px solid #eee; border-radius:16px; padding:16px; background:#fff;">
    <div x-intersect.once="start()">
      <h3 style="margin:0;">Heures de formation</h3>

      <p style="margin-top:10px; color:#666;">
        Valeur : <strong x-text="value"></strong>
      </p>
    </div>
  </div>
</div>

<script>
  function CounterOnView(target) {
    return {
      value: 0,
      started: false,

      start() {
        if (this.started) return;
        this.started = true;

        const duration = 700;
        const startTime = performance.now();

        const tick = (now) => {
          const progress = Math.min((now - startTime) / duration, 1);
          this.value = Math.floor(progress * target);

          if (progress < 1) {
            requestAnimationFrame(tick);
          } else {
            this.value = target;
          }
        };

        requestAnimationFrame(tick);
      },
    };
  }
</script>
```

---

# 10) Pièges fréquents (et comment les éviter)

## Piège A — animation partout

Si tu mets un reveal sur 100 sections :

* ça devient lourd
* ça fatigue l’utilisateur

Règle :

> animation = parcimonie

---

## Piège B — pas de `.once`

Tu déclenches 20 fois le même code.

Règle :

> `.once` pour 80% des cas

---

## Piège C — “scroll event” fait maison

Ne refais pas ce que le navigateur fait déjà mieux.

Intersect est plus propre.

---

## Piège D — pas de fallback

Dans 99% des navigateurs modernes, ça marche.
Mais en environnement ultra vieux, tu peux prévoir :

* affichage direct
* pas d’animation

---

# 11) Mini exercice (obligatoire)

### Exercice A — Reveal en cascade

Ajoute un `delay` différent selon l’index.

Indice :

* `x-for`
* `:style="'transition-delay:' + index*80 + 'ms'"`

### Exercice B — Lazy load d’un tableau

Quand visible :

* tu charges une liste d’items (fake)
* tu affiches un tableau

### Exercice C — Stats dashboard

Crée 3 compteurs :

* capital
* tickets joués
* ROI

Déclenchés à l’entrée dans la vue.

---

## Résumé de la leçon

* Intersect détecte quand un élément devient visible
* parfait pour reveal, lazy load, stats
* `.once` = UX stable
* évite les scroll listeners maison

---

### Étape suivante logique

Chapitre 11 — Plugins officiels & Accessibilité
**Leçon 4 — Collapse : accordéon propre (UX + accessibilité)**
On va construire un accordéon réutilisable, propre et agréable.
