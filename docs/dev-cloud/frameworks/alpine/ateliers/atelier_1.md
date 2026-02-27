---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Ateliers UI #1

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Menu responsive complet (production-ready)

## Objectif de l’atelier

Construire un menu responsive utilisable en production, avec :

* burger menu (mobile)
* sous-menu (dropdown)
* fermeture au clic extérieur
* fermeture avec Escape
* navigation clavier simple (focus visible + tabulation)
* attributs ARIA cohérents
* structure lisible et maintenable

Cet atelier est volontairement “niveau pro” : le but n’est pas juste que ça marche, mais que ce soit propre, compréhensible, et réutilisable.

---

## 1) Spécification fonctionnelle (ce que le menu doit faire)

### Comportement attendu

Sur mobile :

* un bouton “Menu” (burger) ouvre/ferme la navigation
* quand le menu est ouvert :

  * un clic en dehors ferme le menu
  * Escape ferme le menu
  * la navigation est visible et utilisable au clavier

Sous-menu :

* un bouton “Produits” ouvre/ferme un dropdown
* le dropdown se ferme :

  * si on clique ailleurs
  * si on appuie sur Escape
  * si on ferme le menu principal

### Contraintes UX minimales

* le bouton burger doit refléter l’état (`aria-expanded`)
* le dropdown doit refléter l’état (`aria-expanded`)
* `x-cloak` doit empêcher tout flash au chargement
* focus visible (au moins via CSS)

---

## 2) Structure technique (pattern Alpine propre)

On va suivre le pattern “pro” :

* un état global pour le menu : `isOpen`
* un état pour le sous-menu : `isProductsOpen`
* des méthodes : `toggleMenu`, `closeMenu`, `toggleProducts`, `closeProducts`
* une gestion d’événements globale : Escape + outside
* un reset contrôlé : fermer le sous-menu quand on ferme le menu principal

---

## 3) Version Vanilla (CDN) — livrable complet prêt à coller

Copie-colle tel quel dans un fichier `index.html`.

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Atelier #1 — Menu Responsive Alpine</title>

    <script defer src="https://unpkg.com/alpinejs"></script>

    <style>
      [x-cloak] {
        display: none !important;
      }

      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        line-height: 1.4;
      }

      /* Layout minimal (pas de design fancy, juste propre) */
      .header {
        border-bottom: 1px solid #e5e5e5;
        padding: 12px 16px;
      }

      .container {
        max-width: 980px;
        margin: 0 auto;
      }

      .row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
      }

      .brand {
        font-weight: 700;
      }

      .btn {
        border: 1px solid #ddd;
        background: #fff;
        border-radius: 8px;
        padding: 8px 12px;
        cursor: pointer;
      }

      /* Focus visible : obligatoire en UI pro */
      .btn:focus-visible,
      a:focus-visible {
        outline: 3px solid #111;
        outline-offset: 2px;
      }

      .nav {
        margin-top: 12px;
        border-top: 1px solid #eee;
        padding-top: 12px;
      }

      .nav a,
      .nav button {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-right: 10px;
        text-decoration: none;
        color: #111;
      }

      .nav a:hover {
        text-decoration: underline;
      }

      .dropdown {
        position: relative;
        display: inline-block;
      }

      .dropdown-panel {
        position: absolute;
        top: calc(100% + 8px);
        left: 0;
        min-width: 220px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background: #fff;
        padding: 8px;
      }

      .dropdown-panel a {
        display: block;
        padding: 8px;
        border-radius: 8px;
      }

      .dropdown-panel a:hover {
        background: #f5f5f5;
      }

      /* Simu responsive : on considère mobile par défaut */
      /* (Dans une vraie UI, on ferait un menu desktop différent)
         Ici l’objectif est le comportement, pas le design */
    </style>
  </head>

  <body>
    <header
      class="header"
      x-data="menuComponent()"
      @keydown.escape.window="onEscape()"
    >
      <div class="container">
        <div class="row">
          <div class="brand">OmnyUI</div>

          <!-- Bouton burger -->
          <button
            type="button"
            class="btn"
            @click="toggleMenu()"
            :aria-expanded="isOpen.toString()"
            aria-controls="main-nav"
          >
            <span x-text="isOpen ? 'Fermer' : 'Menu'"></span>
          </button>
        </div>

        <!-- Navigation (mobile) -->
        <nav
          id="main-nav"
          class="nav"
          x-show="isOpen"
          x-cloak
          @click.outside="closeMenu()"
        >
          <a href="#home">Accueil</a>
          <a href="#services">Services</a>

          <!-- Dropdown Produits -->
          <div class="dropdown">
            <button
              type="button"
              class="btn"
              @click="toggleProducts()"
              :aria-expanded="isProductsOpen.toString()"
              aria-controls="products-panel"
            >
              <span>Produits</span>
              <span aria-hidden="true" x-text="isProductsOpen ? '▲' : '▼'"></span>
            </button>

            <div
              id="products-panel"
              class="dropdown-panel"
              x-show="isProductsOpen"
              x-cloak
              @click.outside="closeProducts()"
            >
              <a href="#p1" @click="onNavigate()">Produit A</a>
              <a href="#p2" @click="onNavigate()">Produit B</a>
              <a href="#p3" @click="onNavigate()">Produit C</a>
            </div>
          </div>

          <a href="#contact">Contact</a>
        </nav>
      </div>
    </header>

    <main class="container" style="padding: 16px;">
      <h1>Atelier #1 — Menu Responsive Alpine</h1>
      <p>
        Objectif : comportement propre (menu + dropdown), fermeture outside,
        fermeture Escape, ARIA de base, focus visible.
      </p>

      <section style="margin-top: 24px;">
        <h2>Contenu</h2>
        <p>
          Clique sur “Menu”, puis teste : clic en dehors, Escape, ouverture du
          dropdown “Produits”, etc.
        </p>
      </section>
    </main>

    <script>
      /**
       * menuComponent()
       * Composant Alpine "pro" : état + méthodes + règles UX.
       */
      function menuComponent() {
        return {
          // State
          isOpen: false,
          isProductsOpen: false,

          // Actions principales
          toggleMenu() {
            this.isOpen = !this.isOpen;

            // Règle UX : si on ferme le menu principal,
            // on ferme aussi le sous-menu pour éviter un état incohérent.
            if (!this.isOpen) {
              this.isProductsOpen = false;
            }
          },

          closeMenu() {
            this.isOpen = false;
            this.isProductsOpen = false;
          },

          toggleProducts() {
            // Si menu fermé, on l’ouvre automatiquement (option UX)
            if (!this.isOpen) {
              this.isOpen = true;
            }

            this.isProductsOpen = !this.isProductsOpen;
          },

          closeProducts() {
            this.isProductsOpen = false;
          },

          // Gestion Escape globale
          onEscape() {
            // Priorité : fermer d’abord le sous-menu, sinon le menu
            if (this.isProductsOpen) {
              this.isProductsOpen = false;
              return;
            }

            if (this.isOpen) {
              this.closeMenu();
            }
          },

          // Navigation : si on clique un lien du dropdown, on ferme tout
          onNavigate() {
            this.closeMenu();
          },
        };
      }
    </script>
  </body>
</html>
```

---

## 4) Explication pédagogique (ce que l’étudiant doit comprendre)

Le menu est un cas parfait pour apprendre Alpine, car il combine :

* un état booléen (`isOpen`)
* une UI conditionnelle (`x-show`)
* des événements (`@click`, `@click.outside`, `@keydown.escape.window`)
* une discipline “pro” : méthodes claires, reset d’état

Le point clé : **cohérence d’état**.
Un sous-menu ne doit pas rester “ouvert” quand le menu principal est fermé, sinon tu obtiens des bugs invisibles.

---

## 5) Pièges fréquents (et comment les éviter)

### Piège A — `@click.outside` ferme tout dès que tu cliques sur un lien

C’est normal : cliquer sur un lien est un clic “dans” le menu, donc pas outside.
Mais si tu mets `@click.outside` trop haut ou mal placé, tu peux fermer au mauvais moment.

Règle : `@click.outside` doit être sur le conteneur du bloc à fermer, pas sur toute la page.

### Piège B — état incohérent

Tu oublies de fermer le dropdown quand tu fermes le menu.
Résultat : réouverture bizarre ou UI incohérente.

Solution : `closeMenu()` ferme tout.

### Piège C — flash au chargement

Sans `x-cloak` + CSS `[x-cloak]{display:none}`, le menu peut clignoter.

---

## 6) Exercices (pour valider la compétence)

### Exercice 1 — Ajoute un 2ème dropdown “Ressources”

Même logique que Produits, mais avec son propre état.
Important : quand tu ouvres l’un, ferme l’autre (sinon UX confuse).

### Exercice 2 — Ajoute “Fermer au clic sur un lien principal”

Quand on clique “Accueil”, “Services” ou “Contact”, ferme le menu.

Astuce : ajoute `@click="closeMenu()"` sur ces liens.

### Exercice 3 — Ajoute une gestion simple du focus (niveau intermédiaire)

À l’ouverture du menu, focus le premier lien (“Accueil”).

Tu as deux façons :

* version simple (inline) : `$nextTick(() => $refs.firstLink.focus())`
* version structurée : `openMenu()` + `$refs`

On détaillera `$refs` au Chapitre 6, mais tu peux déjà le faire.

---

## 7) Version “Vite pro” (même menu, composant dans un fichier JS)

Comme tu veux une formation complète et cohérente : voici la transposition propre “projet moderne”.

### `src/components/menu.js`

```js
export function menuComponent() {
  return {
    isOpen: false,
    isProductsOpen: false,

    toggleMenu() {
      this.isOpen = !this.isOpen;
      if (!this.isOpen) this.isProductsOpen = false;
    },

    closeMenu() {
      this.isOpen = false;
      this.isProductsOpen = false;
    },

    toggleProducts() {
      if (!this.isOpen) this.isOpen = true;
      this.isProductsOpen = !this.isProductsOpen;
    },

    closeProducts() {
      this.isProductsOpen = false;
    },

    onEscape() {
      if (this.isProductsOpen) {
        this.isProductsOpen = false;
        return;
      }
      if (this.isOpen) this.closeMenu();
    },

    onNavigate() {
      this.closeMenu();
    },
  };
}
```

### `src/main.js`

```js
import Alpine from "alpinejs";
import { menuComponent } from "./components/menu.js";

window.Alpine = Alpine;

Alpine.data("menu", menuComponent);

Alpine.start();
```

### HTML

```html
<header x-data="menu" @keydown.escape.window="onEscape()">
  ...
</header>
```

Même comportement, mais architecture plus propre.

---

## Livrable attendu (ce que l’étudiant doit pouvoir montrer)

À la fin, l’étudiant doit avoir :

* un menu responsive fonctionnel
* un dropdown propre
* fermeture outside + Escape
* `aria-expanded` correct
* `x-cloak` installé
* code lisible (méthodes, pas du spaghetti)

---

### Suite logique

On attaque maintenant **Chapitre 3 — Binding & Formulaires** avec :

* `x-bind (:)`
* `x-on (@)`
* `x-model`
* `@submit.prevent`

Puis **Atelier UI #2 — Todo list (simple)**

Avant d’enchaîner : tu veux que je t’écrive la version **MDX “Atelier”** de ce livrable (format doc vendable), ou on continue directement le Chapitre 3, Leçon 1 ?
