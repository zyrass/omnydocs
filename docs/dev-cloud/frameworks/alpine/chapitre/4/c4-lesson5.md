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

## `Debounce` / `Throttle` : recherche live, champs, scroll (UX + performance)

### Objectif de la leçon

À la fin, tu sauras :

* comprendre la différence entre **debounce** et **throttle**
* choisir la bonne stratégie selon le cas
* utiliser `debounce` dans Alpine (ex: recherche live)
* utiliser `throttle` pour éviter de tuer les performances (scroll, resize)
* éviter les erreurs classiques : UI lente, spam d’événements, expérience “lag”

Cette leçon est fondamentale parce que dans une UI moderne, tu as souvent :

* des champs qui déclenchent une action à chaque saisie
* du scroll qui déclenche des actions en continu
* du resize qui spamme des événements

Sans contrôle, ton app devient lourde et instable.

---

## 1) Définition simple (avec analogies)

### Debounce (anti-spam)

Debounce signifie :

> “Attends que l’utilisateur ait fini avant d’agir.”

Analogie :
Tu parles à quelqu’un au téléphone.
Tant qu’il parle, tu ne réponds pas.
Tu réponds seulement quand il s’arrête.

Cas typique :

* recherche live
* auto-save après saisie
* validation après arrêt de frappe

---

### Throttle (limite de vitesse)

Throttle signifie :

> “Tu peux agir, mais pas plus d’une fois toutes les X ms.”

Analogie :
Un radar automatique.
Tu peux passer, mais si tu vas trop vite, ça bloque.

Cas typique :

* scroll
* resize
* événements très fréquents

---

## 2) Différence visuelle (très clair)

| Technique | Comportement              | Utilisation      |
| --------- | ------------------------- | ---------------- |
| Debounce  | attend la fin de l’action | input, recherche |
| Throttle  | limite la fréquence       | scroll, resize   |

---

# 3) Debounce dans Alpine (la version simple et efficace)

Alpine supporte un modificateur `.debounce`.

### Exemple : recherche live avec debounce

```html
<div x-data="{ query: '' }">
  <input
    type="text"
    placeholder="Rechercher..."
    x-model="query"
    @input.debounce.400ms="console.log('Recherche :', query)"
  />

  <p>Query : <strong x-text="query"></strong></p>
</div>
```

### Ce que ça fait

* l’utilisateur tape
* Alpine attend 400ms après la dernière frappe
* puis déclenche l’action

Ça évite :

* 30 actions par seconde
* des recherches inutiles

---

## 4) Cas réel : filtrer une liste (pattern Todo avancée)

On simule une liste et on filtre.

```html
<div x-data="{
  query: '',
  items: ['Angular', 'Alpine.js', 'Laravel', 'Tailwind', 'Node.js'],

  get filtered() {
    const q = this.query.trim().toLowerCase();
    if (q.length === 0) return this.items;

    return this.items.filter(item => item.toLowerCase().includes(q));
  }
}">
  <input
    type="text"
    x-model="query"
    placeholder="Tape pour filtrer..."
    @input.debounce.300ms="query = query"
    style="padding: 10px; border: 1px solid #ddd; border-radius: 10px; width: 100%;"
  />

  <ul style="margin-top: 10px;">
    <template x-for="item in filtered" :key="item">
      <li x-text="item"></li>
    </template>
  </ul>
</div>
```

### Point important

Ici le filtrage est fait via un getter `filtered`.

Donc la UI reste cohérente, et le debounce sert surtout à limiter les recalculs inutiles.

---

# 5) Throttle (quand tu dois limiter un événement continu)

Sur scroll, tu ne veux pas déclencher 200 fois par seconde.

### Exemple : afficher un “Back to top” après 200px

```html
<div x-data="{ showTop: false }"
     @scroll.window.throttle.200ms="showTop = window.scrollY > 200"
     style="min-height: 200vh; padding: 16px; border: 1px solid #eee;">
  <p>Scroll pour tester</p>

  <button
    x-show="showTop"
    x-cloak
    @click="window.scrollTo({ top: 0, behavior: 'smooth' })"
    style="position: fixed; bottom: 16px; right: 16px; padding: 10px 12px; border-radius: 10px; border: 1px solid #ddd; background: #111; color: #fff;"
  >
    Haut
  </button>
</div>
```

Ici :

* l’état se met à jour au maximum toutes les 200ms
* pas de spam
* UX fluide

---

## 6) Debounce vs Throttle : comment choisir sans se tromper ?

### Si tu veux attendre la fin d’une action utilisateur → Debounce

Exemples :

* l’utilisateur tape dans une recherche
* l’utilisateur modifie un champ
* tu veux faire une requête API après la saisie

### Si tu veux limiter une action continue → Throttle

Exemples :

* scroll
* resize
* drag / move

---

# 7) Pièges fréquents (et comment les éviter)

## Piège A — Debounce trop long

Si tu mets 1500ms, l’utilisateur pense que ça ne marche pas.

Bon ordre d’idée :

* 200ms à 400ms : très bien pour recherche
* 500ms : encore acceptable
* au-delà : ça devient lent

---

## Piège B — Throttle trop court

Si tu throttles à 10ms, tu throttles presque rien.

Bon ordre d’idée :

* 100ms à 250ms pour scroll/resize

---

## Piège C — Mettre debounce sur le mauvais événement

Exemple :

* debounce sur click → aucun intérêt
* throttle sur input → parfois mauvais UX (sensation “bloquée”)

---

## Piège D — Faire des actions lourdes dans le handler

Debounce/throttle ne remplace pas le fait d’avoir une logique légère.

Exemple mauvais :

* faire un tri complexe + DOM heavy dans un scroll handler

---

# 8) Mini exercice (obligatoire)

### Exercice A — Recherche debounce

* input recherche
* affiche en dessous : “Recherche lancée : X”
* utilise `@input.debounce.300ms`

### Exercice B — Scroll throttle

* si scrollY > 150 → afficher “Tu as scrollé”
* throttle 200ms

### Exercice C — Resize throttle

* afficher la largeur écran (`window.innerWidth`)
* mettre à jour max toutes les 300ms

---

## Résumé de la leçon

* Debounce = attendre la fin (input, recherche)
* Throttle = limiter la fréquence (scroll, resize)
* Alpine permet `.debounce.XXXms` et `.throttle.XXXms`
* objectif : UX fluide + performance stable

---

### Étape suivante logique

On a terminé le Chapitre 4.

Prochaine étape : **Atelier UI #3 — Todo list (filtres + animation + recherche debounce)**
On va assembler :

* filtres All/Done/Active
* recherche debounce
* transitions sur ajout/suppression
* UX propre (outside, Escape si nécessaire)

Quand tu me dis “go”, je le rédige complet comme livrable pro.
