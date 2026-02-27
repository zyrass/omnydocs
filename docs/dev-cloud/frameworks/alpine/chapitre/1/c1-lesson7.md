---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 7

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Préparer l’environnement (setup pro + habitudes de debug)

### Objectif de la leçon

À la fin, tu auras un environnement propre et efficace pour travailler avec Alpine.js :

* un navigateur bien configuré
* des DevTools maîtrisés (au moins les fonctions utiles)
* un VSCode optimisé
* une méthode de debug simple et professionnelle

L’objectif ici n’est pas “installer 50 outils”.
L’objectif c’est d’être opérationnel, rapide, et de ne pas perdre 2 heures sur des erreurs basiques.

---

## 1) Le navigateur : ton vrai IDE quand tu fais du front

Tu peux coder Alpine sur n’importe quel navigateur moderne, mais pour une formation sérieuse je recommande :

* Chrome
* ou Firefox

Les deux sont très bons.

### Pourquoi c’est important ?

Parce qu’Alpine vit dans le navigateur.

Quand un truc ne marche pas, ton premier réflexe doit être :

* ouvrir la console
* inspecter le DOM
* vérifier ton état
* comprendre l’erreur

---

## 2) DevTools : les 4 panneaux que tu dois maîtriser

Les DevTools (Developer Tools) sont les outils intégrés au navigateur pour analyser ton site.

Tu n’as pas besoin de tout connaître.
Mais tu dois maîtriser 4 onglets.

---

### 2.1 Onglet “Elements” (DOM + HTML réel)

C’est ici que tu vois :

* le HTML final
* les classes
* les attributs
* les éléments affichés/cachés

Pourquoi c’est crucial avec Alpine ?

Parce que parfois tu crois que ton HTML est correct…
mais en réalité Alpine ne s’est pas initialisé, ou ton `x-show` cache le bloc.

Tu dois savoir vérifier :

* si ton élément est bien présent
* si `x-show` est actif
* si ton composant est au bon endroit

---

### 2.2 Onglet “Console” (erreurs + logs)

La console, c’est ton détecteur de mensonges.

Si Alpine ne marche pas, la console te dira souvent :

* variable non définie
* erreur de syntaxe
* erreur JS bloquante
* problème de chargement

#### Exemple d’erreur classique

Tu écris :

```html
<div x-data="{ open: false }">
  <button @click="opne = !opne">Toggle</button>
</div>
```

Tu as fait une faute (`opne` au lieu de `open`).

Sans console, tu vas chercher 20 minutes.
Avec console, tu vois directement :

* `opne is not defined`

Règle : **console ouverte = cerveau tranquille**.

---

### 2.3 Onglet “Network” (chargements)

C’est ici que tu vérifies si Alpine est bien chargé.

Tu dois être capable de répondre à :

* le script Alpine est-il téléchargé ?
* est-ce qu’il est bloqué ?
* est-ce que le fichier existe ?

Très utile quand tu passes sur Vite, ou quand tu bosses avec un CDN.

---

### 2.4 Onglet “Application” (localStorage)

Cet onglet devient essentiel dès qu’on touche :

* la persistance
* les stores
* le plugin Persist
* les préférences utilisateur

Tu pourras y voir :

* ce que ton application stocke
* si ça se sauvegarde bien
* si ça se restaure correctement

---

## 3) VSCode : configuration minimale mais efficace

VSCode est parfait pour Alpine, surtout si tu fais :

* HTML
* Tailwind
* Laravel Blade

### Extensions recommandées (vraiment utiles)

#### 1) Live Server (ou équivalent)

Permet de lancer une page HTML rapidement.

Pourquoi c’est utile ?
Parce que pour les premiers chapitres, on veut :

* un fichier HTML
* un navigateur
* Alpine via CDN
* zéro friction

#### 2) Prettier

Formate ton code automatiquement.

Ça évite les fichiers illisibles et les erreurs de structure.

#### 3) Tailwind CSS IntelliSense

Même si on ne l’utilise pas encore à fond, tu vas l’utiliser dans Bloc 2.

Ça te donne :

* autocomplete des classes
* suggestions
* validation

#### 4) ESLint (utile plus tard)

Pas obligatoire au début, mais utile en mode projet.

---

## 4) Les habitudes pro qui évitent 80% des galères

Ici c’est la partie la plus importante de la leçon.

### Habitude 1 — Toujours tester Alpine avec un “Hello Alpine”

Quand tu démarres un nouveau fichier ou projet, teste d’abord ça :

```html
<div x-data="{ test: 'Alpine OK' }">
  <p x-text="test"></p>
</div>
```

Si ça ne marche pas, inutile d’aller plus loin.
Tu corriges d’abord le chargement Alpine.

---

### Habitude 2 — Debug avec `console.log()` dans x-data

Oui, tu peux logger depuis Alpine.

Exemple :

```html
<div x-data="{
  count: 0,
  increment() {
    this.count++;
    console.log('count =', this.count);
  }
}">
  <button @click="increment()">+1</button>
  <span x-text="count"></span>
</div>
```

C’est simple, efficace, universel.

---

### Habitude 3 — Ne pas “deviner”, vérifier le DOM

Quand tu utilises `x-show`, n’oublie pas :

* l’élément existe toujours dans le DOM
* il est juste caché (souvent via `display: none`)

Donc tu dois vérifier si :

* ton HTML est bien rendu
* ton état change réellement
* le style n’écrase pas ton rendu

---

### Habitude 4 — Toujours vérifier le scope

Si une variable n’est pas trouvée, 90% du temps c’est :

* `x-data` placé au mauvais endroit
* ou un composant enfant qui n’a pas accès à l’état

Rappel simple :

> Un composant Alpine ne “voit” que ce qui est dans son `x-data` ou ses parents.

---

## 5) Les erreurs de setup les plus fréquentes (et solutions)

### Erreur 1 — Alpine chargé après ton HTML sans defer

Si tu charges Alpine comme ça :

```html
<script src="https://unpkg.com/alpinejs"></script>
```

Parfois Alpine se charge trop tard ou pas comme tu veux.

Bonne pratique :

```html
<script defer src="https://unpkg.com/alpinejs"></script>
```

`defer` = “charge le script mais exécute-le après le parsing HTML”.

---

### Erreur 2 — Tu fais du file:// et certains trucs bug

Quand tu ouvres un fichier directement depuis ton disque, certaines fonctionnalités peuvent être limitées.

Solution : utiliser Live Server, ou un serveur local.

---

### Erreur 3 — Ton CSS masque ton composant

Exemple : tu as un container `display: none` quelque part, ou un overlay mal géré.

Solution : inspecter dans “Elements” et regarder les styles appliqués.

---

## 6) Mini exemple : “setup check” complet

Ce fichier te permet de vérifier que tout est OK :

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>Alpine Playground</title>

    <!-- Alpine.js via CDN -->
    <script defer src="https://unpkg.com/alpinejs"></script>

    <style>
      body {
        font-family: Arial, sans-serif;
        padding: 16px;
      }
      button {
        padding: 8px 12px;
        cursor: pointer;
      }
    </style>
  </head>

  <body>
    <h1>Playground Alpine</h1>

    <div x-data="{ count: 0 }">
      <p>Compteur : <span x-text="count"></span></p>

      <button @click="count++">+1</button>
      <button @click="count = 0">Reset</button>
    </div>
  </body>
</html>
```

Si ce fichier fonctionne :

* ton navigateur est OK
* Alpine est bien chargé
* ton environnement est prêt

---

## Résumé de la leçon

Un environnement pro pour Alpine, c’est :

* Chrome ou Firefox
* DevTools : Elements + Console + Network + Application
* VSCode avec quelques extensions utiles
* des habitudes de debug simples : “Hello Alpine”, console.log, scope, DOM

Tu ne dois pas “espérer que ça marche”.
Tu dois être capable de diagnostiquer en 30 secondes.

---

## Mini exercice (rapide)

1. Crée un fichier `index.html`
2. Mets Alpine via CDN avec `defer`
3. Ajoute un compteur avec +1 / reset
4. Ouvre la console et log le compteur à chaque clic

---

Prochaine leçon : **Leçon 8 — Installation en Vanilla JavaScript (CDN)**
Et là on passe à l’action : on fait le vrai “Playground Alpine” qui servira pour tout le Chapitre 2 et 3. On va faire une base propre, réutilisable, et prête pour les ateliers.
