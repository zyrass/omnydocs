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

## Reset / migration / export-import : bonnes pratiques “projet réel”

### Objectif de la leçon

À la fin, tu sauras :

* gérer un **reset** propre (utilisateur + debug)
* gérer une **migration** quand ton modèle de données évolue
* proposer un **export/import JSON** (feature “pro”)
* éviter les pièges :

  * données cassées après mise à jour
  * import invalide
  * perte de compatibilité
  * stockage qui devient un bazar

C’est cette leçon qui transforme ton mini projet en “app sérieuse”.

---

## 1) Pourquoi reset + migration sont obligatoires en vrai projet

Dans une formation, tu fais évoluer ton code.

Dans un produit réel, c’est encore pire :

* tu ajoutes des champs
* tu changes des structures
* tu modifies la logique

Mais l’utilisateur, lui, a déjà des données stockées.

Donc tu dois anticiper :

* “mes données v1 existent”
* “mon code est maintenant en v2”
* “je dois adapter sans casser”

---

# 2) Reset propre : pas juste “vider le tableau”

Un reset “pro” doit :

* vider les données
* effacer la persistance (localStorage)
* remettre l’app dans un état initial stable

Sinon tu as :

* état incohérent
* stockage qui reste rempli
* bug après refresh

---

# 3) Migration : définition simple

Une migration, c’est :

> transformer des données anciennes (v1) vers un format nouveau (v2)

Analogie simple :

* tu as un vieux fichier Word (.doc)
* ton logiciel veut maintenant du .docx
* tu convertis

Même idée.

---

# 4) Export / Import : pourquoi c’est une feature “pro”

Export/import sert à :

* sauvegarder ses données
* transférer entre navigateurs
* partager une configuration
* debug rapidement

Exemples :

* liste de courses
* favoris
* settings
* tracker paris

C’est très utile dans tes projets fil rouge.

---

# 5) On va construire un store persistant “versionné” + import/export

On va faire une structure propre :

* clé : `alpine:grocery:pack`
* contenu :

```js
{
  version: 2,
  items: [...],
  updatedAt: "...",
}
```

Et on gère :

* migration v1 → v2
* export JSON
* import JSON (avec validation)

---

## Code complet (copie-colle)

Ce code fonctionne en mode **persist manuel** (localStorage), car c’est plus clair pour la migration.

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Persistance pro — Reset + Migration + Export/Import</h2>
  <p style="color:#666;">
    Store versionné, migration automatique, export/import JSON.
  </p>

  <div x-data="GroceryAddV2()" style="border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Ajouter</h3>

    <form @submit.prevent="submit()" style="display:flex; gap:10px; margin-top:10px;">
      <input
        type="text"
        x-model="label"
        placeholder="Ex: Tomates"
        style="flex:1; padding:10px; border:1px solid #ddd; border-radius:10px;"
      />
      <select
        x-model="priority"
        style="padding:10px; border:1px solid #ddd; border-radius:10px; background:#fff;"
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>

      <button
        type="submit"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
      >
        Ajouter
      </button>
    </form>
  </div>

  <div x-data style="margin-top: 14px; border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Liste</h3>

    <p style="margin-top:10px; color:#666;">
      Total : <strong x-text="$store.grocery.totalCount"></strong>
    </p>

    <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
      <template x-for="item in $store.grocery.items" :key="item.id">
        <div style="border:1px solid #eee; border-radius:12px; padding:12px; display:flex; justify-content:space-between; gap:10px; align-items:center;">
          <label style="display:flex; gap:10px; align-items:center; flex:1;">
            <input type="checkbox" :checked="item.done" @change="$store.grocery.toggleDone(item.id)" />
            <span
              x-text="item.label + ' (' + item.priority + ')'"
              :style="item.done ? 'text-decoration: line-through; color:#999;' : 'color:#111;'"
            ></span>
          </label>

          <button
            type="button"
            @click="$store.grocery.removeItem(item.id)"
            style="padding:8px 10px; border-radius:10px; border:1px solid #ddd; background:#fff;"
          >
            Supprimer
          </button>
        </div>
      </template>
    </div>

    <div style="display:flex; flex-wrap:wrap; justify-content:flex-end; gap:10px; margin-top:12px;">
      <button
        type="button"
        @click="$store.grocery.clearDone()"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Supprimer terminés
      </button>

      <button
        type="button"
        @click="$store.grocery.resetAll()"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Reset complet
      </button>

      <button
        type="button"
        @click="$store.grocery.exportToClipboard()"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
      >
        Export JSON (clipboard)
      </button>
    </div>

    <div x-data="{ json: '' }" style="margin-top:12px;">
      <textarea
        x-model="json"
        rows="4"
        placeholder="Colle ici un JSON exporté pour importer..."
        style="width:100%; padding:10px; border:1px solid #ddd; border-radius:10px; resize: vertical;"
      ></textarea>

      <div style="display:flex; justify-content:flex-end; margin-top:10px;">
        <button
          type="button"
          @click="$store.grocery.importFromJSON(json)"
          style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
        >
          Import JSON
        </button>
      </div>
    </div>
  </div>
</div>

<script>
  document.addEventListener('alpine:init', () => {
    const STORAGE_KEY = 'alpine:grocery:pack';
    const CURRENT_VERSION = 2;

    Alpine.store('grocery', {
      items: [],

      get totalCount() {
        return this.items.length;
      },

      // --- Persistance versionnée ---
      savePack() {
        try {
          const pack = {
            version: CURRENT_VERSION,
            items: this.items,
            updatedAt: new Date().toISOString(),
          };

          localStorage.setItem(STORAGE_KEY, JSON.stringify(pack));
        } catch (err) {
          console.error('Erreur sauvegarde pack:', err);
        }
      },

      loadPack() {
        try {
          const raw = localStorage.getItem(STORAGE_KEY);
          if (!raw) return;

          const parsed = JSON.parse(raw);

          // Si pas de version => on suppose v1 (ancien format)
          const version = parsed?.version ?? 1;

          if (version === 1) {
            const migrated = this.migrateV1ToV2(parsed);
            this.items = migrated.items;
            this.savePack();
            return;
          }

          if (version === 2) {
            if (!Array.isArray(parsed.items)) return;

            this.items = parsed.items.map(i => ({
              id: i.id,
              label: String(i.label ?? ''),
              done: Boolean(i.done),
              priority: ['low', 'medium', 'high'].includes(i.priority) ? i.priority : 'medium',
            }));
            return;
          }

          console.warn('Version inconnue du pack:', version);
        } catch (err) {
          console.error('Erreur lecture pack:', err);
        }
      },

      migrateV1ToV2(packV1) {
        // v1 supposé : { items: [{id,label,done}] }
        const items = Array.isArray(packV1?.items) ? packV1.items : [];

        return {
          version: 2,
          items: items.map(i => ({
            id: i.id ?? (Date.now() + Math.random()),
            label: String(i.label ?? ''),
            done: Boolean(i.done),
            priority: 'medium', // champ ajouté en v2
          })),
        };
      },

      resetAll() {
        localStorage.removeItem(STORAGE_KEY);
        this.items = [];
      },

      // --- Export / Import ---
      exportJSON() {
        const pack = {
          version: CURRENT_VERSION,
          items: this.items,
          exportedAt: new Date().toISOString(),
        };

        return JSON.stringify(pack, null, 2);
      },

      async exportToClipboard() {
        try {
          const json = this.exportJSON();
          await navigator.clipboard.writeText(json);
          alert('Export copié dans le presse-papiers.');
        } catch (err) {
          console.error('Clipboard export failed:', err);
          alert("Impossible de copier (droits navigateur).");
        }
      },

      importFromJSON(raw) {
        try {
          const parsed = JSON.parse(raw);

          if (!parsed || parsed.version !== CURRENT_VERSION) {
            alert('JSON invalide ou version non supportée.');
            return;
          }

          if (!Array.isArray(parsed.items)) {
            alert('JSON invalide : items manquant.');
            return;
          }

          // Validation stricte
          const items = parsed.items.map(i => ({
            id: i.id ?? (Date.now() + Math.random()),
            label: String(i.label ?? '').trim(),
            done: Boolean(i.done),
            priority: ['low', 'medium', 'high'].includes(i.priority) ? i.priority : 'medium',
          })).filter(i => i.label.length > 0);

          this.items = items;
          this.savePack();

          alert('Import terminé.');
        } catch (err) {
          console.error('Import JSON failed:', err);
          alert('JSON invalide (parse error).');
        }
      },

      // --- Actions ---
      addItem(label, priority = 'medium') {
        const value = String(label ?? '').trim();
        if (!value) return;

        const prio = ['low', 'medium', 'high'].includes(priority) ? priority : 'medium';

        this.items.unshift({
          id: Date.now() + Math.random(),
          label: value,
          done: false,
          priority: prio,
        });

        this.savePack();
      },

      removeItem(id) {
        this.items = this.items.filter(i => i.id !== id);
        this.savePack();
      },

      toggleDone(id) {
        const item = this.items.find(i => i.id === id);
        if (!item) return;
        item.done = !item.done;
        this.savePack();
      },

      clearDone() {
        this.items = this.items.filter(i => !i.done);
        this.savePack();
      },
    });

    // Chargement initial + migration si besoin
    Alpine.store('grocery').loadPack();
  });

  function GroceryAddV2() {
    return {
      label: '',
      priority: 'medium',

      submit() {
        const value = this.label.trim();
        if (!value) return;

        this.$store.grocery.addItem(value, this.priority);
        this.label = '';
        this.priority = 'medium';
      },
    };
  }
</script>
```

---

# 6) Explication formateur : ce qu’il faut retenir

## A) On a une clé unique

`alpine:grocery:pack`

Donc tout est centralisé.

---

## B) On a une version

`CURRENT_VERSION = 2`

Ça permet d’évoluer sans casser.

---

## C) Migration automatique

Si les données sont en v1 :

* on migre
* on sauvegarde en v2
* et c’est fini

L’utilisateur ne voit rien, mais l’app reste stable.

---

## D) Import / export sécurisé

On valide :

* JSON parse OK
* version OK
* items tableau
* chaque item est nettoyé

C’est obligatoire sinon tu peux casser ton UI avec un import mauvais.

---

# 7) Pièges fréquents (vraiment importants)

## Piège A — importer sans validation

Tu te retrouves avec :

* `label: null`
* `priority: "SUPERHIGH"`
* `items: "hello"`

Ton app explose.

Donc validation stricte.

---

## Piège B — pas de version

Tu changes ton code…
les utilisateurs ont un ancien format…
tout casse.

Toujours versionner.

---

## Piège C — persister des données sensibles

Encore une fois :
localStorage = accessible au JS.
Donc XSS = fuite.

Pas de token, pas de données perso.

---

# 8) Mini exercice (obligatoire)

### Exercice A — Ajouter une migration v2 → v3

Ajoute un champ `createdAt`.

Migration :

* si absent, set `createdAt = now`

### Exercice B — Import “merge”

Au lieu de remplacer :

* fusionne les items existants + importés
* évite doublons par label

### Exercice C — Export “items only”

Ajoute un bouton qui export uniquement le tableau `items`.

---

## Résumé de la leçon

* reset complet = effacer stockage + reset state
* migration = compatibilité ascendante
* export/import = feature pro + debug + partage
* validation stricte = stabilité

---

### Étape suivante logique

Chapitre 11 — Plugins officiels & Accessibilité avancée
Leçon 1 : Persist (standardiser les données)
Puis Focus, Intersect, Collapse, Mask… et on passe en mode AAA mindset.
