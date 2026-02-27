---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 4

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Collapse : accordéon propre (UX + accessibilité)

### Objectif de la leçon

À la fin, tu sauras :

* construire un accordéon “pro” sans glitch
* comprendre pourquoi les accordéons sont souvent mal faits
* utiliser le plugin **Collapse** d’Alpine
* gérer :

  * animation fluide
  * ouverture/fermeture propre
  * UX claire
  * accessibilité minimale (clavier + structure)

Ce plugin est une pépite parce qu’il te permet de faire un accordéon sans bricoler des hauteurs en CSS.

---

## 1) C’est quoi un accordéon ?

Un accordéon, c’est une UI où tu as :

* une liste de sections
* chaque section a un titre (cliquable)
* le contenu s’ouvre et se ferme

Exemples classiques :

* FAQ
* settings
* panneau d’aide
* menu mobile

---

## 2) Le problème classique : les accordéons glitchent

Accordéon mal fait = tu vois souvent :

* animation cassée (saut)
* contenu qui “clignote”
* hauteur qui ne s’anime pas
* texte qui dépasse pendant l’animation

Pourquoi ?
Parce que animer `height: auto` est un cauchemar en CSS pur.

Et beaucoup de gens bricolent avec :

* `max-height: 9999px`
* transitions bancales
* hacks pas maintenables

---

# 3) Ce que fait Collapse

Le plugin Collapse gère pour toi :

* la transition d’ouverture/fermeture
* la hauteur dynamique
* l’animation fluide

Donc tu peux faire :

```html
<div x-show="open" x-collapse>
  Contenu
</div>
```

Et ça marche proprement.

---

# 4) Installation du plugin Collapse (CDN)

Tu charges :

1. Alpine core
2. Collapse plugin

```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
```

---

# 5) Exemple 1 : Accordéon simple (1 section)

### Objectif

Une section qui s’ouvre et se ferme.

---

## Code complet (copie-colle)

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Plugin Collapse — Accordéon simple</h2>

  <div x-data="{ open: false }" style="margin-top:12px; border:1px solid #eee; border-radius:16px; background:#fff;">
    <button
      type="button"
      @click="open = !open"
      style="width:100%; text-align:left; padding:14px; border:none; background:transparent; cursor:pointer;"
    >
      <strong>Section : Pourquoi Alpine.js ?</strong>
      <div style="color:#666; margin-top:6px;">
        Clique pour ouvrir/fermer
      </div>
    </button>

    <div x-show="open" x-collapse style="padding:0 14px 14px;">
      <p style="margin:0; color:#666;">
        Alpine.js est parfait pour enrichir une UI sans basculer dans un framework lourd.
        C’est simple, lisible, et très rapide à intégrer dans des pages existantes.
      </p>
    </div>
  </div>
</div>
```

---

# 6) Explication formateur : ce qu’il faut retenir

## A) `x-show` gère la visibilité

Tu ouvres/fermes via `open`.

## B) `x-collapse` gère l’animation de hauteur

Sans lui, tu aurais une ouverture instantanée ou glitchée.

---

# 7) Exemple 2 : Accordéon multi-sections (FAQ)

### Objectif

* plusieurs sections
* une seule ouverte à la fois (pattern courant)

---

## Code complet

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Collapse — FAQ (1 seule ouverte)</h2>

  <div x-data="FaqAccordion()" style="margin-top:12px; display:flex; flex-direction:column; gap:10px;">
    <template x-for="item in items" :key="item.id">
      <div style="border:1px solid #eee; border-radius:16px; background:#fff;">
        <button
          type="button"
          @click="toggle(item.id)"
          style="width:100%; text-align:left; padding:14px; border:none; background:transparent; cursor:pointer; display:flex; justify-content:space-between; gap:10px;"
        >
          <div>
            <strong x-text="item.title"></strong>
            <div style="color:#666; margin-top:6px;" x-text="item.subtitle"></div>
          </div>

          <span style="font-size:18px;" x-text="openId === item.id ? '−' : '+'"></span>
        </button>

        <div x-show="openId === item.id" x-collapse style="padding:0 14px 14px;">
          <p style="margin:0; color:#666;" x-text="item.content"></p>
        </div>
      </div>
    </template>
  </div>
</div>

<script>
  function FaqAccordion() {
    return {
      openId: 1,

      items: [
        {
          id: 1,
          title: "Est-ce qu'Alpine remplace React/Vue ?",
          subtitle: "Non, c'est un outil différent.",
          content:
            "Alpine est excellent pour des composants UI simples et rapides. Pour des apps énormes, Vue/React restent plus adaptés.",
        },
        {
          id: 2,
          title: "Est-ce que c'est compatible Laravel ?",
          subtitle: "Oui, très utilisé dans Blade.",
          content:
            "Alpine fonctionne parfaitement avec Blade. Il est souvent utilisé dans les stacks TALL.",
        },
        {
          id: 3,
          title: "Pourquoi Collapse plutôt que du CSS ?",
          subtitle: "Parce que height:auto est pénible.",
          content:
            "Collapse gère proprement la transition de hauteur sans hacks CSS, donc ton code reste propre et stable.",
        },
      ],

      toggle(id) {
        this.openId = this.openId === id ? null : id;
      },
    };
  }
</script>
```

---

# 8) Accessibilité minimale (ce qu’on doit respecter)

Un accordéon “pro” doit :

* utiliser un bouton `<button>` (pas un `<div>`)
* être utilisable au clavier
* avoir un état visible

Bonus accessibilité (recommandé) :

* `aria-expanded="true/false"`
* `aria-controls="id"`

On peut l’ajouter.

---

## Version améliorée (ARIA)

```html
<button
  type="button"
  @click="toggle(item.id)"
  :aria-expanded="openId === item.id"
  :aria-controls="'panel-' + item.id"
>
  ...
</button>

<div
  :id="'panel-' + item.id"
  x-show="openId === item.id"
  x-collapse
>
  ...
</div>
```

Ce n’est pas “du détail”.
C’est ce qui te fait passer en mode entreprise.

---

# 9) Pièges fréquents

## Piège A — utiliser `x-if` au lieu de `x-show`

Avec `x-if`, tu détruis/recrées le DOM.
Ça peut casser :

* focus
* formulaires internes
* transitions

Pour un accordéon :

> `x-show` est souvent meilleur

---

## Piège B — ouvrir 5 sections sans logique

Parfois c’est voulu (FAQ libre).
Mais souvent UX :

* une seule ouverte = plus clair

Donc pattern `openId`.

---

## Piège C — pas de feedback visuel

Toujours afficher :

* “+” / “−”
* flèche
* style actif

Sinon l’utilisateur ne comprend pas l’état.

---

# 10) Mini exercice (obligatoire)

### Exercice A — Accordéon multi-ouvert

Transforme `openId` en tableau `openIds`.

Objectif :

* plusieurs sections ouvertes

### Exercice B — Accordéon “settings”

Ajoute :

* checkbox “notifications”
* select “langue”
  Dans le panel.

### Exercice C — Accordéon + Persist

Persiste la section ouverte :

* `openId: Alpine.$persist(1).as('...')`

---

## Résumé de la leçon

* Collapse rend l’accordéon fluide et propre
* `x-show + x-collapse` = combo standard
* bouton + ARIA = accessibilité
* pattern `openId` = UX claire

---

### Étape suivante logique

Chapitre 11 — Plugins officiels & Accessibilité
**Leçon 5 — Mask : inputs contrôlés (téléphone, date, formats)**
On va faire du formulaire “pro” sans se tirer une balle dans le pied.
