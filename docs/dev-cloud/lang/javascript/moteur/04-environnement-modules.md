---
description: "Initialiser un projet Front-End moderne : la fin de l'ère <script>, l'arrivée des modules MJS et le bundler Vite.js"
icon: lucide/book-open-check
tags: ["JAVASCRIPT", "VITE", "BUNDLER", "ES-MODULES", "ENVIRONNEMENT"]
---

# Environnement & Modules

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="2 Heures">
</div>

## Introduction

!!! quote "Analogie Pédagogique"
    _Au début des années 2010, coder en JavaScript consistait à ouvrir un fichier texte, taper trois lignes de code, et rafraichir son navigateur (`F5`). C'était comme faire un feu de camp : simple, rapide, mais dangereux pour cuire un banquet de 500 personnes._
    
    _Aujourd'hui, coder une interface Web s'apparente à diriger **une cuisine industrielle**. Vous avez besoin de camions de livraison (NPM), de robots pour couper les légumes à la chaîne (Minification), de serveurs qui goutent le plat toutes les millisecondes (Hot Reload), et d'équipes séparées dans des conteneurs qui ne se crient pas dessus (les Modules). C'est ce qu'on appelle "L'Outillage Moderne" (Tooling)._

Dans ce module, nous allons poser les bases d'un environnement professionnel. Avant même d'apprendre la grammaire du langage, vous devez savoir **comment l'installer et le compiler**.

<br>

---

## Le Cauchemar historique : la balise `<script>`

Si vous avez déjà lu un très vieux tutoriel, l'intégration du JavaScript au HTML s'effectuait toujours en bas de la balise `<body>` :

```html title="HTML — L'ancienne méthode (à bannir sur de gros projets)"
<body>
    <h1>Mon vieux site</h1>

    <!-- Chargement bloquant et global -->
    <script src="jquery.js"></script>
    <script src="monSlider.js"></script>
    <script src="maLogique.js"></script>
</body>
```

### Les trois problèmes majeurs

1. **Variables Globales** : Le code de `monSlider.js` et celui de `maLogique.js` partagent **le même espace mémoire**. Si une variable `const compteur = 0;` existe dans les deux fichiers, le navigateur hurlera son désespoir et crashera : **Conflit de noms**.
2. **Ordre de chargement strict** : Si `maLogique.js` utilise un outil fourni par `jquery.js`, mais tombe en premier dans l'ordre de chargement du HTML... tout casse. La maintenance de dizaines de scripts devenait impossible.
3. **Poids et Performance** : Télécharger 10 fichiers séparés ralentit considérablement la connexion réseau.

<br>

---

## La Révolution : Les ES Modules (MJS)

Pour résoudre ces immenses conflits, la norme ECMAScript a officialisé en 2015 le système de **Modules**. 

Le principe est simple : chaque fichier JavaScript devient **un silo hermétique**. Ses variables naissent et meurent à l'intérieur de ce fichier. Personne ne peut les lire depuis l'extérieur... sauf s'il décide consciemment de les `export`er.

### Export et Import (`.mjs` ou type module)

```javascript title="JavaScript — L'export (mathUtils.js / .mjs)"
/* Ce fichier est un module. La Constante "PI" n'est pas globale. */
const PI = 3.14159;

/* J'autorise consciemment les autres fichiers à utiliser cette fonction */
export function calculerAire(rayon) {
    return PI * (rayon * rayon);
}
```

```javascript title="JavaScript — L'import (app.js)"
/* J'invoque mon collègue depuis l'autre fichier */
import { calculerAire } from './mathUtils.js';

console.log(calculerAire(10));
```

### Côté HTML : L'attribut vital `type="module"`

Pour que le navigateur comprenne que vos fichiers ne sont plus de simples vieux scripts mais des silos sécurisés utilisant les imports/exports :

```html title="HTML — Appel moderne d'un point d'entrée"
<head>
    <!-- Chargement non bloquant (defer implicite) et isolé en mémoire -->
    <script type="module" src="app.js"></script>
</head>
```

!!! info "La différence `.js` vs `.mjs`"
    Historiquement, NodeJS (le JavaScript tournant côté serveur backend) utilisait un tout autre outil appelé CommonJS (`require()`). Pour forcer les moteurs backend à utiliser le standard moderne universel du module plutôt que leur vieux système, on a inventé l'extension **`.mjs`** (Module JS). Aujourd'hui, on l'utilise souvent pour bien distinguer un module pur d'un simple script, mais l'attribut `type="module"` suffit généralement côté web Frontend.

<br />

---

## Le Bundler moderne : Vite.js

*"Même avec les modules, je dois quand même envoyer 50 fichiers `.js` au navigateur du visiteur ?"*
Oui. Et c'est justement là qu'interviennent les **Bundlers** (Empaqueteurs).

Un Bundler est un logiciel conçu pour analyser toute l'arborescence de vos 50 fichiers, et **les fusionner (fusion+compression) en un seul énorme fichier ultra-léger** et obfusqué, que le navigateur téléchargera en une frappe !

### Pourquoi Vite.js a tué Webpack

Longtemps dominé par un ogre lent et complexe nommé `Webpack`, l'écosystème web est aujourd'hui propulsé à 90 % par **Vite.js** (créé par le concepteur du framework Vue.js). Vite.js est incroyablement rapide car il ne compile pas le code tout le temps pendant que vous travaillez.

!!! tip "Les superpouvoirs de Vite.js"

    1. **Serveur Local (Dev Server)** : Il crée une fausse URL `http://localhost:5173` sur votre PC avec des comportements ultra-sécurisés (CORS).
    2. **HMR (Hot Module Replacement)** : Si vous modifiez un bout de texte en JS ou CSS dans votre code et sauvegardez (`Ctrl+S`), **seule cette ligne est mise à jour sur votre écran en 10 millisecondes**, sans perdre l'état du navigateur, et **sans rechargement manuel de la page !**
    3. **Support natif** : Il compile le Typescript, le SASS (SCSS), le CSS Moderne, sans la moindre ligne de configuration.
    4. **Build Industriel** : À la fin de votre projet, la commande de build écrasera tous vos espaces, vos longs noms de variables, et optimisera vos images SVG, transformant un projet de 10 Mo en un fichier pesant 50 Ko.

### Installer Vite.js

!!! info "**Pré-requis** : le logiciel NodeJS doit être présent sur la machine, pour accéder au gestionnaire de paquets "npm"."

Ouvrez un terminal, et tapez :

```bash title="Terminal — Initialiser un projet vierge avec Vite"
npm create vite@latest mon-premier-projet -- --template vanilla
```
_Le template `vanilla` signifie : JavaScript brut, sans les immenses frameworks réactifs comme React ou Vue._

Ensuite :
```bash title="Terminal — Lancement"
cd mon-premier-projet
npm install   # Télécharge les camions de livraison
npm run dev   # Démarre le serveur magique HMR !
```

!!! note "Si l'usage du terminal et des commandes (npm, cd, etc.) vous semble encore mystérieux, nous vous conseillons de consulter la section **[Outils de Développement](../../../../../bases/outils/index.md)** dans les fondamentaux IT pour acquérir ces bases indispensables."

<br />

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Aujourd'hui, plus personne n'insère de code applicatif via un attribut de bouton (`onclick="alert()"`) ni ne balance des scripts en vrac sans `type="module"`. **Vite.js** est devenu le standard de l'industrie pour initialiser un dossier de travail. Il vous offre le confort du rafraîchissement au quart de seconde, la sécurité des modules isolés, et une optimisation drastique du code de production final.

> Votre cuisine opérationnelle (Vite) est montée. Vos plaques chauffent (HMR). Il est maintenant temps d'aborder **les ingrédients modernes** : l'évolution vitale de la syntaxe introduite par l'ES6, et ses immenses raccourcis d'écriture.  
**Moteur : [Chapitre 05 : Moteur Moderne et ES6+](./05-syntaxe-moderne-es6.md)**

<br />
