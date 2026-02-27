---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 5

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Accessibilité finale : modals / tabs / menu (ARIA, focus, navigation clavier)

### Objectif de la leçon

À la fin, tu vas savoir rendre tes composants Alpine :

* utilisables **au clavier** (sans souris)
* compréhensibles par les technologies d’assistance (lecteurs d’écran)
* cohérents en UX (comportement attendu)
* “production-ready” dans une vraie entreprise

Et surtout tu vas comprendre un truc fondamental :

> Une UI qui marche à la souris mais pas au clavier, ce n’est pas “presque bon”.
> C’est cassé.

---

# 1) Accessibilité : définition simple (sans blabla)

L’accessibilité (a11y) c’est :

* permettre à tout le monde d’utiliser ton site
* y compris :

  * personnes avec handicap moteur
  * personnes malvoyantes
  * personnes qui naviguent au clavier
  * personnes sur appareils limités

Mais même sans parler de handicap :

* un utilisateur power-user utilise souvent le clavier
* un bon focus visible aide tout le monde

Donc c’est aussi du confort.

---

# 2) Les 3 règles d’or “composants accessibles”

## Règle 1 — Focus visible

Tu dois toujours voir où tu es.

Donc :

* pas de `outline: none` sans remplacement
* `:focus-visible` obligatoire

## Règle 2 — Navigation clavier

Tu dois pouvoir :

* tabuler
* activer avec Enter/Space
* fermer avec Escape (menus/modals)
* rester “piégé” dans une modal ouverte (focus trap)

## Règle 3 — Sémantique HTML correcte

Le HTML a déjà des super pouvoirs.

Exemples :

* un bouton doit être un `<button>`
* un lien doit être un `<a>`
* pas de `<div @click>` pour faire un bouton

---

# 3) Le vocabulaire (expliqué clairement)

## ARIA

ARIA = attributs qui expliquent le rôle d’un élément à un lecteur d’écran.

Exemples :

* `aria-expanded="true"`
* `aria-controls="id-panel"`

## Focus trap

Quand une modal est ouverte, le focus ne doit pas sortir.
Sinon l’utilisateur clavier se perd derrière.

Alpine Focus plugin te donne `x-trap`.

## Focus restore

Quand tu fermes une modal, tu dois remettre le focus là où il était.
Sinon l’utilisateur “perd sa position”.

---

# 4) Menu / Dropdown accessible (pattern final)

### Objectif

* bouton correct
* `aria-expanded`
* `aria-controls`
* fermeture Escape + outside

---

## Exemple complet

```html
<div x-data="AccessibleDropdown()" style="position:relative;">
  <button
    type="button"
    @click="toggle()"
    :aria-expanded="open"
    :aria-controls="panelId"
    x-ref="trigger"
    style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff; cursor:pointer;"
  >
    Menu
  </button>

  <div
    :id="panelId"
    x-show="open"
    x-cloak
    x-transition.opacity.scale
    @click.outside="close()"
    @keydown.escape.window="close()"
    style="position:absolute; top:44px; left:0; width:260px; border:1px solid #eee; border-radius:14px; padding:12px; background:#fff;"
  >
    <button type="button" @click="select('Dashboard')" style="display:block; width:100%; text-align:left; padding:10px; border:none; background:transparent; cursor:pointer;">
      Dashboard
    </button>

    <button type="button" @click="select('Settings')" style="display:block; width:100%; text-align:left; padding:10px; border:none; background:transparent; cursor:pointer;">
      Settings
    </button>

    <button type="button" @click="select('Logout')" style="display:block; width:100%; text-align:left; padding:10px; border:none; background:transparent; cursor:pointer;">
      Logout
    </button>
  </div>
</div>

<script>
  function AccessibleDropdown() {
    return {
      open: false,
      panelId: 'dropdown-panel',

      toggle() {
        this.open = !this.open;
      },

      close() {
        this.open = false;
        // Restore focus
        this.$nextTick(() => this.$refs.trigger?.focus());
      },

      select(value) {
        alert('Choix : ' + value);
        this.close();
      },
    };
  }
</script>
```

### Ce qui est pro ici

* bouton réel
* aria correct
* focus restore
* outside + Escape

---

# 5) Tabs accessibles (pattern final)

Les tabs sont souvent mal faites.

Objectif minimal :

* boutons tab
* état actif visible
* aria-selected
* aria-controls

---

## Exemple tabs accessibles

```html
<div x-data="AccessibleTabs()" style="max-width:920px; margin:0 auto; padding:16px;">
  <h2>Tabs accessibles</h2>

  <div role="tablist" aria-label="Sections" style="display:flex; gap:10px; flex-wrap:wrap;">
    <button
      type="button"
      role="tab"
      :aria-selected="active === 'overview'"
      :tabindex="active === 'overview' ? 0 : -1"
      :aria-controls="'panel-overview'"
      @click="set('overview')"
      style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff; cursor:pointer;"
    >
      Overview
    </button>

    <button
      type="button"
      role="tab"
      :aria-selected="active === 'security'"
      :tabindex="active === 'security' ? 0 : -1"
      :aria-controls="'panel-security'"
      @click="set('security')"
      style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff; cursor:pointer;"
    >
      Security
    </button>

    <button
      type="button"
      role="tab"
      :aria-selected="active === 'a11y'"
      :tabindex="active === 'a11y' ? 0 : -1"
      :aria-controls="'panel-a11y'"
      @click="set('a11y')"
      style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff; cursor:pointer;"
    >
      A11Y
    </button>
  </div>

  <div style="margin-top:14px; border:1px solid #eee; border-radius:14px; padding:12px;">
    <div
      role="tabpanel"
      id="panel-overview"
      x-show="active === 'overview'"
      x-cloak
    >
      <p style="margin:0; color:#666;">
        Overview content.
      </p>
    </div>

    <div
      role="tabpanel"
      id="panel-security"
      x-show="active === 'security'"
      x-cloak
    >
      <p style="margin:0; color:#666;">
        Security content.
      </p>
    </div>

    <div
      role="tabpanel"
      id="panel-a11y"
      x-show="active === 'a11y'"
      x-cloak
    >
      <p style="margin:0; color:#666;">
        A11Y content.
      </p>
    </div>
  </div>
</div>

<script>
  function AccessibleTabs() {
    return {
      active: 'overview',

      set(tab) {
        this.active = tab;
      },
    };
  }
</script>
```

### Pourquoi on met `tabindex`

Ça évite que les tabs inactives soient focusables dans le mauvais ordre.
C’est un détail “pro”.

---

# 6) Modal accessible (pattern final)

Une modal pro doit faire :

* ouverture
* focus trap
* fermeture Escape
* fermeture outside
* focus restore

Alpine Focus plugin te donne `x-trap`.

---

## Exemple modal pro (avec Focus plugin)

```html
<div x-data="AccessibleModal()">
  <button type="button" @click="open()" x-ref="trigger">
    Ouvrir modal
  </button>

  <div
    x-show="isOpen"
    x-cloak
    x-transition.opacity
    @keydown.escape.window="close()"
    @click.self="close()"
    style="position:fixed; inset:0; background:rgba(0,0,0,0.55); display:flex; align-items:center; justify-content:center; padding:16px;"
  >
    <div
      x-trap="isOpen"
      style="width:min(520px, 100%); background:#fff; border-radius:16px; padding:16px;"
      role="dialog"
      aria-modal="true"
      aria-label="Fenêtre modale"
    >
      <h2 style="margin:0;">Modal</h2>
      <p style="color:#666; margin-top:6px;">
        Focus trap actif. Escape/outside pour fermer.
      </p>

      <label style="display:flex; flex-direction:column; gap:6px; margin-top:12px;">
        <strong>Nom</strong>
        <input type="text" placeholder="Tape..." />
      </label>

      <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:14px;">
        <button type="button" @click="close()">Fermer</button>
        <button type="button" @click="confirm()">Confirmer</button>
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
        this.$nextTick(() => this.$refs.trigger?.focus());
      },

      confirm() {
        alert('Confirmé');
        this.close();
      },
    };
  }
</script>
```

---

# 7) Pièges fréquents en accessibilité (à éviter)

## Piège A — “outline none”

Beaucoup de devs font ça pour “faire joli”.

Résultat :

* l’utilisateur clavier est perdu

Donc si tu supprimes l’outline :

* tu remplaces par un focus visible propre

## Piège B — modal sans trap

Sans trap, tu peux tabuler derrière la modal.
C’est un bug.

## Piège C — fermeture impossible

Une modal doit pouvoir se fermer :

* Escape
* bouton close
* outside click (souvent)

## Piège D — utiliser `div` cliquable

Un `<div @click>` n’a pas les comportements natifs du bouton.

Donc :

* mauvais pour clavier
* mauvais pour lecteur d’écran

---

# 8) Checklist finale (prête pour la prod)

### Menu / Dropdown

* bouton réel
* aria-expanded
* escape/outside
* focus restore

### Tabs

* role tablist/tab/tabpanel
* aria-selected
* tabindex cohérent

### Modal

* role dialog
* aria-modal
* x-trap
* escape/outside
* focus restore

---

# 9) Mini exercice (obligatoire)

### Exercice A — rendre ton menu responsive accessible

Ajoute :

* fermeture Escape
* focus restore sur bouton burger

### Exercice B — tabs clavier (bonus)

Ajoute gestion flèches :

* ArrowLeft / ArrowRight pour changer d’onglet

### Exercice C — modal confirmation

Crée une modal “confirmation delete” :

* Cancel / Delete
* focus par défaut sur Cancel

---

## Résumé de la leçon

* accessibilité = clavier + focus + sémantique
* ARIA = info pour lecteurs d’écran
* modal = focus trap + restore
* tabs = roles + aria-selected + tabindex

---

### Étape suivante logique

Chapitre 12 — Production Ready
**Leçon 6 — Checklist “avant prod” : qualité, debug, cohérence**
On va formaliser une checklist finale pour livrer proprement (et éviter les bugs idiots).
