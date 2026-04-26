---
description: "Phase 1 : Révolution de l'environnement de travail. Migration d'un site statique classique vers un bundler industriel (Vite.js) et configuration d'un module d'entrée ES6."
icon: lucide/box
tags: ["JAVASCRIPT", "VITE", "NPM", "MODULES"]
status: stable
---

# Phase 1 : Migration & Environnement Vite.js

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le premier choc d'un développeur junior arrivant en entreprise, c'est de découvrir qu'aucun site professionnel n'est codé avec un simple fichier `index.html` ouvert dans le navigateur. On utilise des "Bundlers" (Webpack, Vite, Turbopack) pour minifier, modulariser et recharger le code quasi instantanément. Votre mission : transplanter le projet HTML/CSS du client dans un moteur de Formule 1.

## 1. Initialiser le Projet Vite Vanilla

Assurez-vous d'avoir Node.js installé (`node -v` dans votre terminal). Ouvrez un nouveau dossier vide et lancez la commande magique de scaffolding (génération d'échafaudage logiciel) :

```bash
# Crée un nouveau projet Vite
npm create vite@latest
```

Le CLI va vous poser trois questions :
1. **Nom du projet** : `vitrine-js-moderne`
2. **Framework** : Choisissez `Vanilla` (Vous maîtrisez les bases avant d'apprendre React !).
3. **Variant** : Choisissez `JavaScript` (Pas de TypeScript pour le moment).

Une fois généré, déplacez-vous dans le dossier et installez les paquets (dependencies) :

```bash
cd vitrine-js-moderne
npm install      # Télécharge le moteur Vite dans node_modules/
npm run dev      # Démarre le serveur local de l'usine (localhost:5173)
```

!!! tip "Pourquoi ce serveur est-il 'Magique' ?"
    Allez sur `http://localhost:5173`. Contrairement à l'extension standard LiveServer, Vite intègre le **HMR (Hot Module Replacement)**. Si vous modifiez une fonction JavaScript, seule cette fonction est ré-injectée dans la page sans scroller et sans recharger quoi que ce soit. C'est l'expérience développeur ultime.

## 2. Le Nettoyage de Printemps et l'Import

Vite a créé des fichiers d'exemple (`counter.js`, etc.). Supprimez tout sauf `index.html`, `main.js`, `style.css` et le dossier `public/`.

Maintenant, l'opération à cœur ouvert : **copiez-collez l'intégralité du code de votre précédent projet "HTML/CSS Site Vitrine" dans cet environnement Vite.**

1. Collez le HTML de l'ancien `index.html` dans le nouveau `index.html` de Vite (Gardez la balise `<script type="module" src="/main.js"></script>` tout en bas).
2. Vérifiez que `<link rel="stylesheet" href="./style.css">` pointe bien vers la racine (ou `src/style.css` si vous avez isolé vos sources).
3. Placez vos images de l'ancien dossier `assets/` dans le dossier `public/`.

## 3. L'Essence de l'ES Module (ES6)

Le fichier `main.js` est l'alpha et l'omega de votre application. C'est le "Point d'entrée" (Entry point). Vous ne coderez **jamais** 500 lignes de JavaScript ici. Ce fichier ne servira qu'à importer et lancer d'autres petits composants métiers.

C'est ce qu'on appelle la **Separation of Concerns (SoC)**. 

Testons l'architecture ES6 en créant le module qui servira pour la suite du projet.
Dans le même dossier que `main.js`, créez le sous-répertoire `/src`.
Créez un fichier `src/menuHandler.js`.

```javascript
/* Fichier: src/menuHandler.js */

// Une fonction isolée qui ne fait qu'une seule chose (SRP)
export function initMenu() {
    console.log("Le moteur du Menu Mobile est chargé et prêt.");
    
    // Le futur code d'écoute des clics ira ici
}
```

Importons ce composant détaché dans notre chef d'orchestre `main.js` :

```javascript
/* Fichier: main.js */
import './style.css'; // Vite peut importer du CSS dans du JS, c'est puissant.
import { initMenu } from './src/menuHandler.js';

// Au démarrage, j'ordonne l'exécution du comportement métier
initMenu();
```

## Checklist de la Phase 1

- [ ] Inspectez la console (F12 > Console). Vous devez y lire : "Le moteur du Menu Mobile est chargé et prêt." sans la moindre erreur 404.
- [ ] Le site s'affiche parfaitement, avec ses couleurs et ses Grilles (Grid/Flexbox) originelles. L'habillage statique est indemne.
- [ ] Votre balise `<script>` dans `index.html` a **OBLIGATOIREMENT** l'attribut `type="module"`. Sans cela, la fonction `import {}` lèverait une erreur fatale native dans Chrome.

**Votre usine à gaz est opérationnelle.** Nous avons quitté l'âge de pierre (Fichier HTML basique) pour l'ère industrielle (Dossier Vite compilé). Il est temps de manipuler notre premier élément du DOM en direct : le Menu Burger.

[Passer à la Phase 2 : Refactoring du Menu Mobile →](phase2.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
