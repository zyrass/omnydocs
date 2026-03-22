---
description: "Le strict minimum pour comprendre le rôle de Javascript, comment l'exécuter, et comment dialoguer en secret avec la console du navigateur."
icon: lucide/book-open-check
tags: ["JAVASCRIPT", "CONSOLE", "HELLO-WORLD", "INTRO"]
---

# Introduction et Console

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="30 Minutes">
</div>

## Introduction

!!! warning "Pré-requis Indispensables"
    Si vous n'avez jamais écrit une seule ligne d'algorithmique de votre vie, lisez cette introduction, mais sachez que vous ressentirez un immense vide si vous n'avez pas validé la section **[1. Fondamentaux Techniques](../../../../../bases/fondamentaux/index.md)**. Ce cours JS propose un *rappel extrêmement bref* de ces notions, il ne les remplace en aucun cas.

JavaScript (JS) est le **seul langage compris nativement par tous les navigateurs Web de la planète**. 
Contrairement au HTML (qui affiche l'architecture) et au CSS (qui affiche les couleurs), le JS apporte de **l'intelligence et de la logique**. Il calcule, il décide, il récupère des données invisibles, et il réagit aux actions du visiteur.

<br>

---

## Où vit le JavaScript ?

Exactement comme le CSS et sa balise `<style>`, le JavaScript historique pouvait s'écrire directement dans votre fichier HTML.

```html title="HTML — Le JS intégré (très basique)"
<body>
    <h1>Titre de mon site</h1>

    <!-- La balise script ouvre les portes du moteur JS -->
    <script>
        alert("Bonjour le monde !"); // Fait apparaitre une modale intrusive (à bannir)
    </script>
</body>
```

Aujourd'hui, pour des raisons de propreté et de maintenance, on sépare le JavaScript dans ses propres fichiers (terminant par `.js`).

```html title="HTML — Le JS Externalisé"
<head>
    <!-- Le fichier logique.js sera exécuté automatiquement -->
    <script src="logique.js" defer></script>
</head>
```
!!! note "_**Note** : L'attribut `defer` signale au navigateur de ne pas bloquer l'affichage visuel de la page pendant qu'il télécharge le script._"

<br>

---

## L'Outil n°1 du Développeur : La Console

En programmation, on se trompe souvent. Si vous demandez à JS de diviser 10 par 0, où affiche-t-il l'erreur ? Pas sur l'écran du visiteur (ce serait laid), mais caché dans la **Console Développeur**.

> Pressez la touche <kbd>F12</kbd> sur votre clavier ou <kbd>Cmd</kbd> + <kbd>Option</kbd> + <kbd>I</kbd> sur Mac. Dans votre navigateur, faites un Clic droit > Inspecter, puis choisissez l'onglet **Console**.

### `console.log()`

C'est votre stéthoscope. Cette commande permet au JavaScript de vous murmurer des informations invisibles pour le visiteur normal.

```javascript title="JavaScript — L'interface de débogage"
// Un commentaire (ignoré par le navigateur) commence par deux slashs

// J'affiche du texte dans ma console F12
console.log("Système initialisé avec succès.");

// Je peux aussi vérifier le résultat d'un calcul
console.log(10 + 5); // Affichera 15 dans la console
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le JavaScript s'intègre via des balises `<script>` ou depuis des fichiers externes `.js`. Votre unique lien de communication avec le fonctionnement interne et les erreurs de votre programme est la commande vitale `console.log()`, visible exclusivement depuis l'outil de développement (`F12`).

> À présent, le canal de communication est ouvert. Profitons-en pour faire un retour asynchrone ultra-rapide sur la grammaire fondamentale que nous exigeons pour la suite : [Les Variables et les Boucles](./02-bases-algorithmiques.md).

<br>
