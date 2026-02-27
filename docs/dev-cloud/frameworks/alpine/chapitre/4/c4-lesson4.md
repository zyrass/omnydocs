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

## `.window` / `.document` : écoute globale, pièges et bonnes pratiques

### Objectif de la leçon

À la fin, tu sauras :

* ce que font `.window` et `.document`
* quand tu dois écouter globalement (et quand tu ne dois pas)
* éviter les bugs classiques :

  * événements qui se déclenchent “trop souvent”
  * composants qui se gênent entre eux
  * UI qui réagit alors qu’elle ne devrait pas
* appliquer ces concepts sur des cas réels :

  * Escape global
  * raccourcis clavier
  * scroll / resize
  * tracking simple

Cette leçon est importante parce que l’écoute globale, c’est puissant… et donc dangereux si tu le fais n’importe comment.

---

## 1) Définition simple

### `.window`

Écoute l’événement au niveau de la fenêtre du navigateur.

Exemple :

```html
<div x-data="{ open: true }" @keydown.escape.window="open = false">
  ...
</div>
```

Même si ton composant n’a pas le focus, Escape sera capturé.

### `.document`

Écoute l’événement au niveau du document HTML.

Exemple :

```html
<div x-data="{ }" @click.document="console.log('clic dans le document')">
  ...
</div>
```

---

## 2) Différence pratique entre `.window` et `.document`

Dans beaucoup de cas, les deux peuvent sembler similaires.

Mais en UI, on retient une règle simple :

* `.window` = très utile pour le clavier et les événements globaux
* `.document` = utile pour des clics globaux, mais souvent `.outside` est meilleur

En Alpine, tu vas majoritairement utiliser `.window`.

---

# 3) Cas réel #1 — Escape global (standard pro)

On l’a déjà vu, mais ici on le formalise :

```html
<div x-data="{ open: false }" @keydown.escape.window="open = false">
  <button @click="open = true">Ouvrir</button>

  <div x-show="open" x-cloak style="margin-top: 10px; border: 1px solid #ddd; padding: 12px;">
    <p>Modal / menu / dropdown</p>
  </div>
</div>
```

Pourquoi c’est “pro” ?
Parce que l’utilisateur s’attend à ce que Escape fonctionne partout.

---

# 4) Cas réel #2 — Raccourcis clavier globaux (Ctrl+K)

Un raccourci doit marcher peu importe où tu es dans la page.

Donc `.window`.

```html
<div x-data="{
  open: false,
  toggle() { this.open = !this.open; }
}" @keydown.window="
  if ($event.ctrlKey && $event.key === 'k') {
    $event.preventDefault();
    toggle();
  }
">
  <button @click="toggle()">Recherche</button>

  <div x-show="open" x-cloak style="margin-top: 10px;">
    <input type="text" placeholder="Rechercher..." />
  </div>
</div>
```

---

# 5) Cas réel #3 — Scroll global (attention, piège performance)

Tu peux écouter le scroll global :

```html
<div x-data="{ scrolled: false }"
     @scroll.window="scrolled = window.scrollY > 50">
  <p x-text="scrolled ? 'Scroll > 50px' : 'Top page'"></p>
</div>
```

### Attention : performance

Le scroll déclenche énormément d’événements.

Si tu mets une logique lourde dedans, tu vas ralentir la page.

Règle pro :

> Un handler scroll doit être ultra léger.

Et si tu fais du gros traitement :

* throttle (on arrive juste après)
* ou Intersection Observer (plugin Intersect Chapitre 11)

---

# 6) Cas réel #4 — Resize global (responsive logique)

Exemple : fermer un menu mobile si on repasse en desktop.

```html
<div x-data="{
  open: false,

  closeOnLargeScreen() {
    if (window.innerWidth >= 1024) {
      this.open = false;
    }
  }
}" @resize.window="closeOnLargeScreen()">
  <button @click="open = !open">Menu</button>
  <div x-show="open" x-cloak>Navigation</div>
</div>
```

C’est utile, mais attention : le resize peut aussi spammer.

---

# 7) Le vrai danger : les composants qui se gênent entre eux

### Exemple du bug

Tu as 2 modals dans la page.

Chaque modal écoute Escape global :

```html
@keydown.escape.window="open = false"
```

Si les deux sont ouvertes (ou mal gérées), Escape peut fermer plusieurs choses en même temps.

### Pattern pro : priorité et contrôle

Tu dois fermer uniquement ce qui est actif.

Exemple :

* si dropdown ouvert → fermer dropdown
* sinon si modal ouverte → fermer modal
* sinon rien

C’est une logique d’ordre.

---

# 8) `.document` : quand ça peut être utile (mais à utiliser avec prudence)

Exemple : log “clic global” :

```html
<div x-data="{ clicks: 0 }" @click.document="clicks++">
  <p x-text="`Clics globaux : ${clicks}`"></p>
</div>
```

Mais en UI réelle, tu veux rarement ça.

Pourquoi ?
Parce que ça déclenche pour tout et n’importe quoi.

Pour fermer un menu, préfère :

* `@click.outside`
* ou `@click.self` (overlay modal)

---

# 9) Bonnes pratiques (très importantes)

## Bonne pratique A — garder le handler minimal

Mauvais :

```html
@scroll.window="doSomethingHeavy()"
```

Bon :

* juste mettre à jour un state simple
* déclencher une méthode légère

## Bonne pratique B — éviter les side effects non contrôlés

Si ton handler global modifie 15 variables, tu vas créer des bugs.

## Bonne pratique C — préférer `.outside` pour les fermetures

`.outside` est plus précis et plus lisible.

---

# 10) Résumé clair

| Modificateur | Quand l’utiliser               | Exemple        |
| ------------ | ------------------------------ | -------------- |
| `.window`    | clavier global, scroll, resize | Escape, Ctrl+K |
| `.document`  | cas spéciaux globaux           | tracking clics |
| `.outside`   | fermeture “clic dehors”        | dropdown, menu |
| `.self`      | overlay modal                  | clic sur fond  |

---

## Mini exercice (obligatoire)

### Exercice A — Menu + Escape global

* menu s’ouvre
* Escape ferme menu
* clic outside ferme menu

### Exercice B — Scroll state

* afficher “Tu as scrollé” si scrollY > 100
* sinon “Top page”
* garder la logique légère

### Exercice C — Resize

* si largeur >= 1024 → forcer menu fermé

---

Prochaine leçon : **Leçon 5 — debounce / throttle : recherche live, champs, scroll (UX + performance)**
Là on va faire du concret : rendre une recherche fluide sans spam d’événements.
