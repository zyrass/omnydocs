---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Ateliers UI #9

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Page “AAA Theme Test”

## Objectif : tester une UI “production-ready” (accessibilité + plugins + cohérence)

### Pourquoi cet atelier existe (et pourquoi il est crucial)

Cet atelier, c’est ton “banc d’essai”.

Tu vas construire une page unique qui sert à :

* tester ton thème (contraste, lisibilité, focus)
* tester tes composants (modal, tabs, accordéon, formulaire)
* vérifier que tout est utilisable :

  * au clavier
  * sans souris
  * avec des états visibles
* vérifier que ton code est cohérent (naming, store, architecture)

En entreprise, c’est exactement ce qu’on appelle un **UI QA playground**.

---

# 1) Livrables attendus (ce que tu dois obtenir à la fin)

Une page qui contient :

1. Un switch thème Light/Dark (persisté)
2. Une Navbar (simple)
3. Un menu dropdown (fermeture outside + Escape)
4. Un système de tabs (horizontales)
5. Une modal accessible (focus trap + restore)
6. Un accordéon FAQ (collapse)
7. Un formulaire avec mask (téléphone + date)
8. Une section “intersect reveal” au scroll
9. Une checklist AAA (à cocher) persistée

Le but n’est pas “faire joli”.
Le but est “faire solide”.

---

# 2) Architecture recommandée (propre et maintenable)

Tu vas utiliser :

* `store ui` : thème + checklist + état global minimal
* `composants x-data` : menu, tabs, modal, form
* plugins : Persist + Focus + Intersect + Collapse + Mask

Tu ne mets pas tout dans un store.
Tu fais un mix intelligent.

---

# 3) Installation (CDN) — obligatoire pour l’atelier

Tu dois charger :

* Alpine core
* Persist
* Focus
* Intersect
* Collapse
* Mask

Exemple :

```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/persist@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/intersect@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/mask@3.x.x/dist/cdn.min.js"></script>
```

---

# 4) Page complète “AAA Theme Test” (copie-colle)

Tu peux prendre ce fichier tel quel et le mettre dans ton playground.

```html
<!doctype html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AAA Theme Test — Alpine.js</title>

  <style>
    /* Thème minimaliste, focus visible, lisible */
    :root {
      --bg: #ffffff;
      --text: #111111;
      --muted: #666666;
      --card: #ffffff;
      --border: #eaeaea;
      --btn: #111111;
      --btnText: #ffffff;
      --shadow: 0 10px 30px rgba(0,0,0,0.08);
      --ring: 0 0 0 3px rgba(0,0,0,0.18);
    }

    [data-theme="dark"] {
      --bg: #0b0c0f;
      --text: #f2f2f2;
      --muted: #b7b7b7;
      --card: #12141a;
      --border: #242834;
      --btn: #f2f2f2;
      --btnText: #0b0c0f;
      --shadow: 0 10px 30px rgba(0,0,0,0.35);
      --ring: 0 0 0 3px rgba(255,255,255,0.22);
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    .container {
      max-width: 980px;
      margin: 0 auto;
      padding: 16px;
    }

    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px;
      box-shadow: var(--shadow);
    }

    .muted {
      color: var(--muted);
    }

    .row {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }

    .btn {
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: var(--btn);
      color: var(--btnText);
      cursor: pointer;
      font-weight: 600;
    }

    .btn.secondary {
      background: transparent;
      color: var(--text);
    }

    .btn:focus-visible,
    input:focus-visible,
    textarea:focus-visible {
      outline: none;
      box-shadow: var(--ring);
      border-color: transparent;
    }

    input, textarea {
      width: 100%;
      padding: 10px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
    }

    .tabs {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 10px;
    }

    .tab {
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
      cursor: pointer;
      font-weight: 600;
    }

    .tab.active {
      background: var(--btn);
      color: var(--btnText);
    }

    .divider {
      height: 1px;
      background: var(--border);
      margin: 14px 0;
    }

    [x-cloak] { display: none !important; }
  </style>

  <!-- Alpine + plugins -->
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/persist@3.x.x/dist/cdn.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/intersect@3.x.x/dist/cdn.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/mask@3.x.x/dist/cdn.min.js"></script>
</head>

<body x-data x-bind:data-theme="$store.ui.theme">
  <div class="container">
    <header class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <h1 style="margin:0;">AAA Theme Test</h1>
          <p class="muted" style="margin:6px 0 0;">
            Playground de test : accessibilité, plugins, composants, cohérence UI.
          </p>
        </div>

        <div class="row">
          <button type="button" class="btn secondary" @click="$store.ui.toggleTheme()">
            Thème : <span x-text="$store.ui.theme"></span>
          </button>

          <button type="button" class="btn" @click="$dispatch('ui:open-modal')">
            Ouvrir modal
          </button>
        </div>
      </div>

      <div class="divider"></div>

      <!-- Dropdown menu -->
      <div x-data="DropdownMenu()" style="position:relative;">
        <button type="button" class="btn secondary" @click="toggle()" x-ref="btn">
          Menu
        </button>

        <div
          x-show="open"
          x-cloak
          x-transition.opacity.scale
          @click.outside="close()"
          @keydown.escape.window="close()"
          style="position:absolute; top:46px; left:0; width: 260px;"
          class="card"
        >
          <strong>Navigation</strong>
          <p class="muted" style="margin-top:8px;">
            Fermeture outside + Escape.
          </p>

          <div class="divider"></div>

          <button type="button" class="btn secondary" style="width:100%; text-align:left;" @click="action('Dashboard')">
            Dashboard
          </button>
          <button type="button" class="btn secondary" style="width:100%; text-align:left; margin-top:8px;" @click="action('Settings')">
            Settings
          </button>
          <button type="button" class="btn secondary" style="width:100%; text-align:left; margin-top:8px;" @click="action('Logout')">
            Logout
          </button>
        </div>
      </div>
    </header>

    <main style="margin-top: 14px; display:flex; flex-direction:column; gap:14px;">
      <!-- Tabs -->
      <section class="card" x-data="Tabs()">
        <h2 style="margin:0;">Tabs</h2>
        <p class="muted" style="margin-top:6px;">
          Test d’un composant simple et stable.
        </p>

        <div class="tabs">
          <button type="button" class="tab" :class="active === 'overview' ? 'active' : ''" @click="active='overview'">
            Overview
          </button>
          <button type="button" class="tab" :class="active === 'security' ? 'active' : ''" @click="active='security'">
            Security
          </button>
          <button type="button" class="tab" :class="active === 'a11y' ? 'active' : ''" @click="active='a11y'">
            A11Y
          </button>
        </div>

        <div class="divider"></div>

        <div x-show="active === 'overview'" x-cloak>
          <p class="muted" style="margin:0;">
            Ici tu vérifies la cohérence UI et la structure globale.
          </p>
        </div>

        <div x-show="active === 'security'" x-cloak>
          <p class="muted" style="margin:0;">
            Ici tu peux rappeler : pas de données sensibles en localStorage.
          </p>
        </div>

        <div x-show="active === 'a11y'" x-cloak>
          <p class="muted" style="margin:0;">
            Ici tu testes navigation clavier, focus visible, modals, etc.
          </p>
        </div>
      </section>

      <!-- Accordéon -->
      <section class="card" x-data="FaqAccordionAAA()">
        <h2 style="margin:0;">FAQ / Accordéon (Collapse)</h2>
        <p class="muted" style="margin-top:6px;">
          Test d’animation fluide + UX claire.
        </p>

        <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
          <template x-for="item in items" :key="item.id">
            <div style="border:1px solid var(--border); border-radius:14px; padding:12px;">
              <button
                type="button"
                class="btn secondary"
                style="width:100%; text-align:left; display:flex; justify-content:space-between; align-items:center;"
                @click="toggle(item.id)"
                :aria-expanded="openId === item.id"
                :aria-controls="'panel-' + item.id"
              >
                <span x-text="item.title"></span>
                <span x-text="openId === item.id ? '−' : '+'"></span>
              </button>

              <div
                :id="'panel-' + item.id"
                x-show="openId === item.id"
                x-collapse
                x-cloak
                style="margin-top:10px;"
              >
                <p class="muted" style="margin:0;" x-text="item.content"></p>
              </div>
            </div>
          </template>
        </div>
      </section>

      <!-- Formulaire Mask -->
      <section class="card" x-data="MaskedForm()">
        <h2 style="margin:0;">Formulaire (Mask)</h2>
        <p class="muted" style="margin-top:6px;">
          Masque = aide de saisie. Validation backend toujours obligatoire.
        </p>

        <div style="display:grid; grid-template-columns: 1fr; gap:10px; margin-top:10px;">
          <label style="display:flex; flex-direction:column; gap:6px;">
            <strong>Nom</strong>
            <input type="text" x-model="name" placeholder="Ex: Alain" />
          </label>

          <label style="display:flex; flex-direction:column; gap:6px;">
            <strong>Téléphone</strong>
            <input
              type="text"
              x-model="phone"
              x-mask="99 99 99 99 99"
              inputmode="numeric"
              placeholder="06 12 34 56 78"
            />
          </label>

          <label style="display:flex; flex-direction:column; gap:6px;">
            <strong>Date</strong>
            <input
              type="text"
              x-model="date"
              x-mask="99/99/9999"
              inputmode="numeric"
              placeholder="31/12/2026"
            />
          </label>
        </div>

        <div class="divider"></div>

        <div class="row" style="justify-content:flex-end;">
          <button type="button" class="btn secondary" @click="reset()">
            Reset
          </button>
          <button type="button" class="btn" @click="submit()">
            Submit
          </button>
        </div>

        <pre class="card" style="margin-top:12px; overflow:auto;" x-text="output"></pre>
      </section>

      <!-- Intersect reveal -->
      <section style="height: 30vh; display:flex; align-items:center; justify-content:center;">
        <span class="muted">Scroll encore un peu</span>
      </section>

      <section class="card" x-data="{ shown: false }">
        <div
          x-intersect.once="shown = true"
          x-bind:style="shown
            ? 'opacity:1; transform: translateY(0); transition: 420ms ease;'
            : 'opacity:0; transform: translateY(18px);'"
        >
          <h2 style="margin:0;">Intersect reveal</h2>
          <p class="muted" style="margin-top:6px;">
            Déclenché uniquement à l’entrée dans le viewport.
          </p>
        </div>
      </section>

      <!-- Checklist AAA persistée -->
      <section class="card">
        <h2 style="margin:0;">Checklist AAA (persistée)</h2>
        <p class="muted" style="margin-top:6px;">
          Tu coches, tu refresh, ça reste. Objectif : discipline qualité.
        </p>

        <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
          <template x-for="check in $store.ui.checklist" :key="check.id">
            <label style="display:flex; gap:10px; align-items:flex-start;">
              <input type="checkbox" :checked="check.done" @change="$store.ui.toggleCheck(check.id)" />
              <div>
                <strong x-text="check.label"></strong>
                <div class="muted" style="margin-top:4px;" x-text="check.desc"></div>
              </div>
            </label>
          </template>
        </div>

        <div class="divider"></div>

        <div class="row" style="justify-content:flex-end;">
          <button type="button" class="btn secondary" @click="$store.ui.resetChecklist()">
            Reset checklist
          </button>
        </div>
      </section>
    </main>
  </div>

  <!-- Modal accessible globale (Focus plugin) -->
  <div x-data="GlobalModal()" x-on:ui:open-modal.window="open()" x-cloak>
    <div
      x-show="openState"
      x-transition.opacity
      style="position:fixed; inset:0; background:rgba(0,0,0,0.55); display:flex; align-items:center; justify-content:center; padding:16px;"
      @click.self="close()"
      @keydown.escape.window="close()"
    >
      <div
        class="card"
        style="width:min(520px, 100%);"
        x-trap="openState"
      >
        <h2 style="margin:0;">Modal accessible</h2>
        <p class="muted" style="margin-top:6px;">
          Focus trap actif + fermeture Escape/outside.
        </p>

        <div class="divider"></div>

        <label style="display:flex; flex-direction:column; gap:6px;">
          <strong>Feedback</strong>
          <textarea rows="3" placeholder="Tape un message..."></textarea>
        </label>

        <div class="divider"></div>

        <div class="row" style="justify-content:flex-end;">
          <button type="button" class="btn secondary" @click="close()">
            Fermer
          </button>
          <button type="button" class="btn" @click="confirm()">
            Confirmer
          </button>
        </div>
      </div>
    </div>
  </div>

  <script>
    document.addEventListener('alpine:init', () => {
      Alpine.store('ui', {
        theme: Alpine.$persist('light').as('alpine:aaa:ui:theme:v1'),

        checklist: Alpine.$persist([
          {
            id: 1,
            label: 'Focus visible',
            desc: 'Chaque élément interactif doit avoir un focus clair.',
            done: false,
          },
          {
            id: 2,
            label: 'Navigation clavier',
            desc: 'Tout doit être utilisable au Tab / Shift+Tab / Enter.',
            done: false,
          },
          {
            id: 3,
            label: 'Modal accessible',
            desc: 'Escape, outside click, focus trap, focus restore.',
            done: false,
          },
          {
            id: 4,
            label: 'Formulaire propre',
            desc: 'Labels, mask utile, validation minimale.',
            done: false,
          },
          {
            id: 5,
            label: 'Animations raisonnables',
            desc: 'Pas d’animations agressives, usage de .once.',
            done: false,
          },
        ]).as('alpine:aaa:ui:checklist:v1'),

        toggleTheme() {
          this.theme = this.theme === 'light' ? 'dark' : 'light';
        },

        toggleCheck(id) {
          const item = this.checklist.find(c => c.id === id);
          if (!item) return;
          item.done = !item.done;
        },

        resetChecklist() {
          this.checklist = this.checklist.map(c => ({ ...c, done: false }));
        },
      });
    });

    function DropdownMenu() {
      return {
        open: false,

        toggle() {
          this.open = !this.open;
        },

        close() {
          this.open = false;
        },

        action(name) {
          alert('Action : ' + name);
          this.close();
        },
      };
    }

    function Tabs() {
      return {
        active: 'overview',
      };
    }

    function FaqAccordionAAA() {
      return {
        openId: 1,
        items: [
          {
            id: 1,
            title: 'Pourquoi focus visible ?',
            content:
              'Sans focus visible, l’utilisateur clavier est aveugle. C’est un point critique.',
          },
          {
            id: 2,
            title: 'Pourquoi éviter localStorage pour un token ?',
            content:
              'Parce qu’en cas de XSS, le token est récupérable. On évite.',
          },
          {
            id: 3,
            title: 'Pourquoi Intersect .once ?',
            content:
              'Pour éviter que l’animation se relance en boucle et fatigue l’utilisateur.',
          },
        ],

        toggle(id) {
          this.openId = this.openId === id ? null : id;
        },
      };
    }

    function MaskedForm() {
      return {
        name: '',
        phone: '',
        date: '',
        output: '',

        reset() {
          this.name = '';
          this.phone = '';
          this.date = '';
          this.output = '';
        },

        submit() {
          const payload = {
            name: this.name.trim(),
            phone: this.phone.replaceAll(' ', ''),
            date: this.date.trim(),
          };

          this.output = JSON.stringify(payload, null, 2);
        },
      };
    }

    function GlobalModal() {
      return {
        openState: false,

        open() {
          this.openState = true;
        },

        close() {
          this.openState = false;
        },

        confirm() {
          alert('Confirmé.');
          this.close();
        },
      };
    }
  </script>
</body>
</html>
```

---

# 5) Comment tester comme un vrai QA (méthode pro)

Tu fais 4 passes.

## Pass 1 — Clavier uniquement

* `Tab` partout
* `Shift+Tab`
* `Enter` sur boutons
* `Escape` ferme la modal
* dropdown ferme avec Escape

## Pass 2 — Focus visible

Tu vérifies que tu vois toujours où tu es.
Si tu ne vois pas le focus :

* c’est non conforme

## Pass 3 — Persist

* tu changes le thème
* tu coches checklist
* tu refresh
* ça doit rester

## Pass 4 — Comportements UX

* dropdown ferme outside
* accordéon fluide
* modal ne laisse pas interagir derrière

---

# 6) Pièges à éviter (et pourquoi)

## Piège A — “je fais du AAA mais je n’ai pas de focus”

Sans focus visible :

* AAA = mensonge

## Piège B — animations qui donnent la nausée

Tu veux du moderne, pas du cirque.

## Piège C — masquer ≠ valider

Mask guide la saisie.
Mais backend validation obligatoire.

---

# 7) Extension “pro” (bonus atelier)

Tu peux ajouter :

* un composant Toast (Chapitre 8)
* une DataTable simple (Chapitre final)
* un test de contraste (manuel)

---

# Résultat final attendu

Tu as une page qui prouve que :

* ton Alpine est structuré
* tes plugins sont maîtrisés
* ton accessibilité est prise au sérieux
* ton code est prêt pour une vraie app

---

## Étape suivante logique (après l’atelier)

Chapitre 12 — Production Ready (Vite + Tailwind + qualité)
On passe du “Playground HTML” au starter clonable, clean et industrialisable.
