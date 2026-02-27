---
description: "Maîtriser tous les sélecteurs CSS : éléments, classes, IDs, attributs, pseudo-classes, pseudo-éléments, combinateurs"
icon: lucide/book-open-check
tags: ["CSS", "SÉLECTEURS", "PSEUDO-CLASSES", "PSEUDO-ÉLÉMENTS", "COMBINATEURS", "CIBLAGE"]
---

# VIII - Sélecteurs CSS

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="6-8 heures">
</div>

## Introduction : Cibler avec Précision

!!! quote "Analogie pédagogique"
    _Imaginez une **ville** avec des bâtiments. Vous voulez peindre certains bâtiments en rouge. Comment les désigner ? **"Toutes les maisons"** (sélecteur d'élément : `house { }`), **"Les maisons avec balcon"** (sélecteur de classe : `.balcony { }`), **"La mairie"** (sélecteur ID : `#city-hall { }`), **"La première maison de chaque rue"** (pseudo-classe : `:first-child`), **"Les bâtiments de plus de 3 étages"** (sélecteur d'attribut : `[floors>3]`). Les **sélecteurs CSS**, c'est pareil : ils permettent de **cibler précisément** quels éléments HTML doivent recevoir quels styles. Sans sélecteurs, impossible de dire "ce paragraphe en bleu, cet autre en rouge". Les sélecteurs sont la **base de tout CSS** : plus vous maîtrisez les sélecteurs, plus vous pouvez créer des styles sophistiqués sans polluer le HTML avec des classes partout. Ce module vous transforme en sniper du ciblage CSS : vous apprendrez à atteindre N'IMPORTE QUEL élément avec précision chirurgicale._

**Sélecteurs CSS** = Patterns définissant **quels éléments HTML** recevoir les styles.

**Pourquoi maîtriser les sélecteurs ?**

✅ **Précision** : Cibler exactement ce dont vous avez besoin  
✅ **Efficacité** : Moins de classes HTML inutiles  
✅ **Maintenabilité** : Code CSS plus propre  
✅ **Puissance** : Styles complexes sans JavaScript  
✅ **Performance** : Sélecteurs rapides = rendu rapide  
✅ **Créativité** : Effets avancés (hover, animations, etc.)  

**Hiérarchie des sélecteurs :**

```css
/* Du plus général au plus spécifique */
*           { }  /* Tous les éléments (universel) */
p           { }  /* Tous les <p> (élément) */
.texte      { }  /* Tous les .texte (classe) */
#titre      { }  /* L'unique #titre (ID) */
p.texte     { }  /* <p> avec classe texte (combiné) */
p:hover     { }  /* <p> au survol (pseudo-classe) */
p::first-line { } /* Première ligne de <p> (pseudo-élément) */
```

**Ce module couvre TOUS les sélecteurs CSS du plus basique au plus avancé.**

---

## 1. Sélecteurs de Base

### 1.1 Sélecteur Universel (*)

```css
/* Sélectionne TOUS les éléments */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* ⚠️ Attention : Impacte TOUS les éléments (performance) */
/* Utiliser pour reset CSS ou propriétés universelles uniquement */

/* Exemple reset complet */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

*::before,
*::after {
    box-sizing: border-box;
}
```

**Quand utiliser * :**
- ✅ Reset CSS (margin, padding, box-sizing)
- ✅ Propriétés universelles (box-sizing)
- ❌ Styles visuels (couleur, police) → trop large

### 1.2 Sélecteur d'Élément (Type)

```css
/* Sélectionne TOUS les éléments d'un type */

p {
    color: #333;
    line-height: 1.6;
}

h1 {
    font-size: 2.5rem;
    color: #2c3e50;
}

a {
    color: blue;
    text-decoration: none;
}

/* Exemple complet */
body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
}

header {
    background-color: #2c3e50;
    padding: 20px;
}

nav {
    display: flex;
    gap: 20px;
}

article {
    max-width: 800px;
    margin: 40px auto;
}

footer {
    text-align: center;
    padding: 20px;
    background-color: #34495e;
    color: white;
}
```

**Avantages sélecteur d'élément :**
- Simple et lisible
- Pas besoin de classes
- Bon pour styles globaux

**Inconvénients :**
- Cible TOUS les éléments du type
- Peu spécifique
- Difficile de faire exceptions

### 1.3 Sélecteur de Classe (.)

```css
/* Sélectionne éléments avec classe spécifique */

.button {
    padding: 10px 20px;
    background-color: blue;
    color: white;
    border: none;
    border-radius: 5px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

/* Multiples classes sur un élément */
/* HTML : <div class="card featured"> */

.card {
    background-color: white;
}

.featured {
    border: 2px solid gold;
}

/* Classes avec préfixes (BEM) */
.product-card { }
.product-card__title { }
.product-card__image { }
.product-card__price { }
.product-card--sale { }

/* Exemple complet */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.text-center {
    text-align: center;
}

.text-bold {
    font-weight: bold;
}

.bg-primary {
    background-color: #3498db;
}

.bg-secondary {
    background-color: #95a5a6;
}
```

**HTML correspondant :**

```html
<button class="button">Cliquez-moi</button>

<div class="card">
    <h3>Titre</h3>
    <p>Contenu</p>
</div>

<div class="card featured">
    <h3>Article vedette</h3>
    <p>Contenu spécial</p>
</div>

<div class="container text-center">
    <h1 class="text-bold">Titre centré et gras</h1>
</div>
```

**✅ Classes = MEILLEURE PRATIQUE pour la plupart des styles**

### 1.4 Sélecteur d'ID (#)

```css
/* Sélectionne l'élément avec ID spécifique */
/* ⚠️ ID = UNIQUE dans la page */

#header {
    background-color: #2c3e50;
    height: 80px;
}

#main-content {
    max-width: 1200px;
    margin: 0 auto;
}

#footer {
    background-color: #34495e;
    color: white;
}

/* Ancre de navigation */
#section-about {
    padding-top: 100px;
}
```

**HTML correspondant :**

```html
<header id="header">
    <h1>Mon Site</h1>
</header>

<main id="main-content">
    <article>...</article>
</main>

<section id="section-about">
    <h2>À propos</h2>
</section>

<footer id="footer">
    <p>&copy; 2024</p>
</footer>
```

**⚠️ Problèmes avec IDs en CSS :**

```css
/* ❌ Spécificité trop forte (100 points) */
#titre {
    color: blue;
}

/* Impossible de surcharger avec classe (10 points) */
.titre-rouge {
    color: red; /* Ne fonctionne PAS si élément a aussi ID #titre */
}

/* ✅ Préférer classes pour styles */
.header {
    background-color: #2c3e50;
}
```

**Quand utiliser IDs :**
- ✅ Ancres de navigation (`<a href="#section">`)
- ✅ Références JavaScript (`document.getElementById()`)
- ✅ Labels formulaires (`<label for="email">`)
- ❌ **Éviter pour styles CSS** (préférer classes)

---

## 2. Sélecteurs d'Attributs

### 2.1 Présence d'Attribut [attr]

```css
/* Sélectionne éléments AVEC attribut (peu importe valeur) */

a[target] {
    color: red;
}
/* Cible : <a href="..." target="_blank"> */
/* Ignore : <a href="..."> */

input[required] {
    border: 2px solid red;
}
/* Cible : <input type="text" required> */

img[alt] {
    border: 2px solid green;
}
/* Bonnes pratiques : images avec alt */

/* Exemple complet */
a[href] {
    color: blue;
    text-decoration: underline;
}

button[disabled] {
    opacity: 0.5;
    cursor: not-allowed;
}

input[readonly] {
    background-color: #f0f0f0;
}
```

### 2.2 Valeur Exacte [attr="valeur"]

```css
/* Sélectionne éléments avec valeur EXACTE */

input[type="text"] {
    border: 1px solid #ccc;
}

input[type="email"] {
    border: 1px solid blue;
}

input[type="password"] {
    border: 1px solid red;
}

a[target="_blank"] {
    color: red;
}

a[target="_blank"]::after {
    content: " ↗";  /* Icône lien externe */
}

/* Langues */
p[lang="fr"] {
    quotes: "« " " »";
}

p[lang="en"] {
    quotes: """ """;
}

/* Classes (attention : préférer sélecteur .classe) */
div[class="container"] {
    /* Fonctionne mais .container préféré */
}
```

### 2.3 Contient Mot [attr~="valeur"]

```css
/* Sélectionne si attribut contient MOT (séparé par espaces) */

/* HTML : <div class="button primary large"> */

div[class~="primary"] {
    background-color: blue;
}
/* Équivalent : .primary */

/* HTML : <a title="Lien externe important"> */
a[title~="externe"] {
    color: red;
}
/* Cible si "externe" est un MOT complet */
```

### 2.4 Commence par [attr^="valeur"]

```css
/* Sélectionne si attribut COMMENCE par valeur */

/* Liens externes (commence par http) */
a[href^="http"] {
    color: blue;
}

a[href^="https"] {
    color: green;
}

/* Liens internes (commence par #) */
a[href^="#"] {
    color: purple;
}

/* Liens email (commence par mailto:) */
a[href^="mailto:"] {
    color: orange;
}

a[href^="mailto:"]::before {
    content: "📧 ";
}

/* Liens téléphone (commence par tel:) */
a[href^="tel:"] {
    color: #2ecc71;
}

a[href^="tel:"]::before {
    content: "📞 ";
}

/* Classes avec préfixes */
div[class^="btn-"] {
    padding: 10px 20px;
    border-radius: 5px;
}
/* Cible : btn-primary, btn-secondary, btn-danger */

/* Images par dossier */
img[src^="/images/icons/"] {
    width: 24px;
    height: 24px;
}
```

### 2.5 Finit par [attr$="valeur"]

```css
/* Sélectionne si attribut FINIT par valeur */

/* Liens PDF */
a[href$=".pdf"] {
    color: red;
}

a[href$=".pdf"]::after {
    content: " 📄";
}

/* Liens différents types fichiers */
a[href$=".doc"]::after,
a[href$=".docx"]::after {
    content: " 📝";
}

a[href$=".xls"]::after,
a[href$=".xlsx"]::after {
    content: " 📊";
}

a[href$=".zip"]::after,
a[href$=".rar"]::after {
    content: " 📦";
}

/* Images par extension */
img[src$=".svg"] {
    /* SVG spécifiques */
}

img[src$=".png"] {
    /* PNG spécifiques */
}

/* Classes avec suffixes */
div[class$="-container"] {
    max-width: 1200px;
    margin: 0 auto;
}
```

### 2.6 Contient Sous-chaîne [attr*="valeur"]

```css
/* Sélectionne si attribut CONTIENT valeur (n'importe où) */

/* Liens contenant "youtube" */
a[href*="youtube"] {
    color: red;
}

a[href*="youtube"]::before {
    content: "▶️ ";
}

/* Liens réseaux sociaux */
a[href*="facebook"] {
    color: #3b5998;
}

a[href*="twitter"] {
    color: #1da1f2;
}

a[href*="linkedin"] {
    color: #0077b5;
}

a[href*="github"] {
    color: #333;
}

/* Classes contenant mot-clé */
div[class*="card"] {
    /* Cible : .card, .product-card, .card-container */
}

/* Images contenant mot */
img[src*="logo"] {
    max-width: 200px;
}

img[src*="banner"] {
    width: 100%;
    height: auto;
}

/* Alt contenant mot */
img[alt*="portrait"] {
    border-radius: 50%;
}
```

### 2.7 Commence par ou Tiret [attr|="valeur"]

```css
/* Sélectionne si attribut = "valeur" OU commence par "valeur-" */
/* Principalement pour langues */

/* HTML : <p lang="fr">, <p lang="fr-FR">, <p lang="fr-CA"> */

p[lang|="fr"] {
    quotes: "« " " »";
}
/* Cible : lang="fr", lang="fr-FR", lang="fr-CA" */

p[lang|="en"] {
    quotes: """ """;
}
/* Cible : lang="en", lang="en-US", lang="en-GB" */

/* Classes avec namespace */
div[class|="btn"] {
    /* Cible : class="btn", class="btn-primary" */
}
```

### 2.8 Tableau Récapitulatif Sélecteurs Attributs

| Sélecteur | Signification | Exemple | Cible |
|-----------|---------------|---------|-------|
| `[attr]` | A l'attribut | `a[target]` | `<a target="_blank">` |
| `[attr="val"]` | Valeur exacte | `input[type="text"]` | `<input type="text">` |
| `[attr~="val"]` | Contient mot | `div[class~="primary"]` | `<div class="btn primary">` |
| `[attr^="val"]` | Commence par | `a[href^="https"]` | `<a href="https://...">` |
| `[attr$="val"]` | Finit par | `a[href$=".pdf"]` | `<a href="doc.pdf">` |
| `[attr*="val"]` | Contient | `a[href*="youtube"]` | `<a href="...youtube...">` |
| `[attr\|="val"]` | Commence ou tiret | `p[lang\|="fr"]` | `<p lang="fr-FR">` |

---

## 3. Pseudo-classes

### 3.1 Pseudo-classes de Lien et Interaction

```css
/* États des liens */

/* :link = Lien non visité */
a:link {
    color: blue;
    text-decoration: none;
}

/* :visited = Lien visité */
a:visited {
    color: purple;
}

/* :hover = Survol souris */
a:hover {
    color: red;
    text-decoration: underline;
}

/* :active = Clic en cours */
a:active {
    color: orange;
}

/* ⚠️ ORDRE IMPORTANT : LVHA (LoVe HAte) */
/* L = Link, V = Visited, H = Hover, A = Active */

a:link    { color: blue; }
a:visited { color: purple; }
a:hover   { color: red; }
a:active  { color: orange; }

/* Boutons avec hover */
.button {
    background-color: #3498db;
    color: white;
    padding: 10px 20px;
    transition: background-color 0.3s ease;
}

.button:hover {
    background-color: #2980b9;
    cursor: pointer;
}

.button:active {
    background-color: #21618c;
    transform: scale(0.98);
}

/* Cartes interactives */
.card {
    background-color: white;
    padding: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}
```

### 3.2 Pseudo-classes de Formulaire

```css
/* :focus = Élément a le focus (clavier/souris) */
input:focus {
    outline: 2px solid blue;
    border-color: blue;
}

textarea:focus {
    outline: 2px solid blue;
}

/* :focus-visible = Focus clavier uniquement (pas souris) */
button:focus-visible {
    outline: 2px solid blue;
}

/* :focus-within = Parent a enfant avec focus */
form:focus-within {
    background-color: #f0f8ff;
}

/* :checked = Checkbox/radio coché */
input[type="checkbox"]:checked {
    accent-color: green;
}

input[type="radio"]:checked + label {
    font-weight: bold;
    color: blue;
}

/* :disabled = Élément désactivé */
input:disabled {
    background-color: #e0e0e0;
    cursor: not-allowed;
    opacity: 0.6;
}

button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

/* :enabled = Élément activé */
input:enabled {
    background-color: white;
}

/* :required = Champ obligatoire */
input:required {
    border-left: 3px solid red;
}

/* :optional = Champ optionnel */
input:optional {
    border-left: 3px solid green;
}

/* :valid = Validation réussie */
input:valid {
    border-color: green;
}

/* :invalid = Validation échouée */
input:invalid {
    border-color: red;
}

/* :in-range = Valeur dans range (min/max) */
input[type="number"]:in-range {
    border-color: green;
}

/* :out-of-range = Valeur hors range */
input[type="number"]:out-of-range {
    border-color: red;
}

/* :placeholder-shown = Placeholder affiché (champ vide) */
input:placeholder-shown {
    font-style: italic;
}

/* Exemple complet formulaire */
input[type="text"],
input[type="email"] {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    transition: border-color 0.3s ease;
}

input[type="text"]:focus,
input[type="email"]:focus {
    border-color: #3498db;
    outline: none;
}

input[type="text"]:valid,
input[type="email"]:valid {
    border-color: #2ecc71;
}

input[type="text"]:invalid,
input[type="email"]:invalid {
    border-color: #e74c3c;
}
```

### 3.3 Pseudo-classes Structurelles

```css
/* :first-child = Premier enfant */
p:first-child {
    margin-top: 0;
}

li:first-child {
    border-top: none;
}

/* :last-child = Dernier enfant */
p:last-child {
    margin-bottom: 0;
}

li:last-child {
    border-bottom: none;
}

/* :nth-child(n) = Nième enfant */

/* Nombres spécifiques */
li:nth-child(1) { /* Premier */ }
li:nth-child(2) { /* Deuxième */ }
li:nth-child(3) { /* Troisième */ }

/* Mots-clés */
li:nth-child(odd) {
    background-color: #f9f9f9; /* Impairs : 1, 3, 5... */
}

li:nth-child(even) {
    background-color: white; /* Pairs : 2, 4, 6... */
}

/* Formules an+b */
li:nth-child(2n) {
    /* Pairs : 2, 4, 6, 8... */
    background-color: #f0f0f0;
}

li:nth-child(2n+1) {
    /* Impairs : 1, 3, 5, 7... */
    background-color: white;
}

li:nth-child(3n) {
    /* Multiples de 3 : 3, 6, 9... */
    font-weight: bold;
}

li:nth-child(3n+1) {
    /* 1, 4, 7, 10... */
    color: red;
}

li:nth-child(3n+2) {
    /* 2, 5, 8, 11... */
    color: blue;
}

/* Premiers X éléments */
li:nth-child(-n+3) {
    /* 3 premiers : 1, 2, 3 */
    color: gold;
}

/* À partir du Xième */
li:nth-child(n+4) {
    /* À partir du 4ème : 4, 5, 6... */
    opacity: 0.7;
}

/* :nth-last-child(n) = Nième depuis la fin */
li:nth-last-child(1) {
    /* Dernier */
}

li:nth-last-child(2) {
    /* Avant-dernier */
}

li:nth-last-child(-n+3) {
    /* 3 derniers */
    font-style: italic;
}

/* :first-of-type = Premier de son type */
p:first-of-type {
    font-size: 1.2rem;
}

/* :last-of-type = Dernier de son type */
p:last-of-type {
    margin-bottom: 0;
}

/* :nth-of-type(n) = Nième de son type */
p:nth-of-type(2) {
    /* Deuxième paragraphe */
}

img:nth-of-type(odd) {
    /* Images impaires */
    float: left;
}

img:nth-of-type(even) {
    /* Images paires */
    float: right;
}

/* :only-child = Enfant unique */
p:only-child {
    text-align: center;
}

/* :only-of-type = Seul de son type */
img:only-of-type {
    display: block;
    margin: 0 auto;
}

/* :empty = Élément vide (pas de contenu) */
p:empty {
    display: none;
}

div:empty {
    min-height: 50px;
    background-color: #f0f0f0;
}
```

**Exemples pratiques nth-child :**

```html
<ul>
    <li>Item 1</li>  <!-- :nth-child(1) -->
    <li>Item 2</li>  <!-- :nth-child(2) -->
    <li>Item 3</li>  <!-- :nth-child(3) -->
    <li>Item 4</li>  <!-- :nth-child(4) -->
    <li>Item 5</li>  <!-- :nth-child(5) -->
    <li>Item 6</li>  <!-- :nth-child(6) -->
</ul>
```

```css
/* Alterner couleurs */
li:nth-child(odd) { background: #f9f9f9; }  /* 1, 3, 5 */
li:nth-child(even) { background: white; }   /* 2, 4, 6 */

/* 3 premiers en gras */
li:nth-child(-n+3) { font-weight: bold; }   /* 1, 2, 3 */

/* Tous sauf 3 premiers */
li:nth-child(n+4) { opacity: 0.7; }         /* 4, 5, 6 */

/* Un sur trois */
li:nth-child(3n) { color: red; }            /* 3, 6 */
li:nth-child(3n+1) { color: blue; }         /* 1, 4 */
li:nth-child(3n+2) { color: green; }        /* 2, 5 */
```

### 3.4 Pseudo-classes de Négation et Logique

```css
/* :not() = Négation (inverse) */

/* Tous les paragraphes SAUF celui avec classe .intro */
p:not(.intro) {
    color: #666;
}

/* Tous les liens SAUF ceux dans footer */
a:not(footer a) {
    color: blue;
}

/* Inputs SAUF disabled */
input:not(:disabled) {
    background-color: white;
}

/* Tous les enfants SAUF premier */
li:not(:first-child) {
    border-top: 1px solid #ccc;
}

/* Multiples négations */
button:not(.primary):not(.secondary) {
    background-color: gray;
}

/* :is() = OU logique (sélection multiple simplifiée) */

/* Avant (répétitif) */
header h1,
header h2,
header h3 {
    color: white;
}

/* Après (simplifié avec :is) */
header :is(h1, h2, h3) {
    color: white;
}

/* Exemple complexe */
article :is(h2, h3, h4):hover {
    color: blue;
}

/* :where() = Comme :is() mais spécificité 0 */

/* :is() = Spécificité du sélecteur le plus spécifique */
:is(.class, #id) { } /* Spécificité = 100 (ID) */

/* :where() = Spécificité toujours 0 */
:where(.class, #id) { } /* Spécificité = 0 */

/* Utile pour reset sans augmenter spécificité */
:where(h1, h2, h3) {
    margin: 0;
}

/* :has() = Sélecteur parent (révolutionnaire !) */

/* Div contenant une image */
div:has(img) {
    border: 2px solid blue;
}

/* Article contenant h2 ET p */
article:has(h2):has(p) {
    background-color: #f9f9f9;
}

/* Carte avec bouton */
.card:has(.button) {
    padding-bottom: 60px;
}

/* Label avec checkbox coché */
label:has(input:checked) {
    font-weight: bold;
    color: green;
}
```

### 3.5 Autres Pseudo-classes Utiles

```css
/* :target = Élément ciblé par URL (#ancre) */

/* URL : page.html#section-about */
#section-about:target {
    background-color: yellow;
    padding: 20px;
}

/* Smooth scroll + highlight */
:target {
    animation: highlight 2s ease;
}

@keyframes highlight {
    0% { background-color: yellow; }
    100% { background-color: transparent; }
}

/* :lang() = Langue de l'élément */
:lang(fr) {
    quotes: "« " " »";
}

:lang(en) {
    quotes: """ """;
}

p:lang(fr) {
    hyphens: auto;
}

/* :root = Élément racine (html) */
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    font-size: 16px;
}

/* :defined = Custom elements définis */
custom-element:defined {
    display: block;
}

custom-element:not(:defined) {
    display: none;
}
```

---

## 4. Pseudo-éléments

### 4.1 ::before et ::after

```css
/* Pseudo-éléments = Création de contenu CSS */
/* ⚠️ Syntaxe : :: (double deux-points) */

/* ::before = Insérer contenu AVANT l'élément */
.quote::before {
    content: "« ";
    color: #999;
    font-size: 1.5em;
}

/* ::after = Insérer contenu APRÈS l'élément */
.quote::after {
    content: " »";
    color: #999;
    font-size: 1.5em;
}

/* Icônes de liens externes */
a[href^="http"]::after {
    content: " ↗";
    font-size: 0.8em;
    color: #999;
}

a[href^="mailto:"]::before {
    content: "✉ ";
}

a[href^="tel:"]::before {
    content: "☎ ";
}

/* Compteurs CSS */
body {
    counter-reset: section;
}

h2::before {
    counter-increment: section;
    content: "Section " counter(section) ": ";
    color: #999;
}

/* Décorations */
.title::before {
    content: "";
    display: inline-block;
    width: 50px;
    height: 3px;
    background-color: #3498db;
    margin-right: 10px;
    vertical-align: middle;
}

/* Clearfix (ancienne technique) */
.clearfix::after {
    content: "";
    display: table;
    clear: both;
}

/* Overlay sur image */
.image-container {
    position: relative;
}

.image-container::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.image-container:hover::after {
    opacity: 1;
}

/* Tooltips */
.tooltip {
    position: relative;
}

.tooltip::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background-color: #333;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
}

.tooltip:hover::after {
    opacity: 1;
}

/* Badges */
.notification {
    position: relative;
}

.notification::after {
    content: "3";
    position: absolute;
    top: -8px;
    right: -8px;
    background-color: red;
    color: white;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75em;
}
```

### 4.2 ::first-line et ::first-letter

```css
/* ::first-line = Première ligne de texte */
p::first-line {
    font-weight: bold;
    font-size: 1.2em;
    color: #2c3e50;
}

article p:first-of-type::first-line {
    text-transform: uppercase;
}

/* ::first-letter = Première lettre (lettrine) */
p::first-letter {
    font-size: 3em;
    float: left;
    margin-right: 10px;
    line-height: 0.8;
    color: #3498db;
}

.drop-cap::first-letter {
    font-size: 4em;
    font-weight: bold;
    float: left;
    margin: 0 10px 0 0;
    line-height: 1;
    color: #e74c3c;
}

/* Style magazine */
article p:first-of-type::first-letter {
    font-size: 5em;
    font-family: Georgia, serif;
    float: left;
    margin: 0.1em 0.1em 0 0;
    line-height: 0.8;
}

/* Limitations ::first-line et ::first-letter */
/* Propriétés limitées applicables : */
/* - Police (font-*, color) */
/* - Arrière-plan (background-*) */
/* - Marges, padding (partiellement) */
/* - Texte (text-*, line-height) */
```

### 4.3 ::selection

```css
/* ::selection = Texte sélectionné par utilisateur */

::selection {
    background-color: #3498db;
    color: white;
}

/* Firefox nécessite préfixe */
::-moz-selection {
    background-color: #3498db;
    color: white;
}

/* Spécifique à un élément */
p::selection {
    background-color: yellow;
    color: black;
}

code::selection {
    background-color: #2c3e50;
    color: #f1c40f;
}

/* Limitations ::selection */
/* Propriétés applicables : */
/* - color */
/* - background-color */
/* - text-shadow */
/* - cursor (partiellement) */
```

### 4.4 ::placeholder

```css
/* ::placeholder = Texte placeholder des inputs */

input::placeholder {
    color: #999;
    font-style: italic;
    opacity: 0.7;
}

textarea::placeholder {
    color: #aaa;
    font-size: 0.9em;
}

/* Focus = placeholder disparaît */
input:focus::placeholder {
    opacity: 0;
    transition: opacity 0.3s ease;
}

/* Préfixes navigateurs (anciennes versions) */
input::-webkit-input-placeholder { /* Chrome/Safari */
    color: #999;
}

input::-moz-placeholder { /* Firefox 19+ */
    color: #999;
}

input:-ms-input-placeholder { /* IE 10+ */
    color: #999;
}
```

### 4.5 Autres Pseudo-éléments

```css
/* ::marker = Puce/numéro de liste */
li::marker {
    color: #3498db;
    font-weight: bold;
    font-size: 1.2em;
}

ul li::marker {
    content: "→ ";
}

ol li::marker {
    content: counter(list-item) "➤ ";
}

/* ::backdrop = Arrière-plan dialog/fullscreen */
dialog::backdrop {
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
}

:fullscreen::backdrop {
    background-color: black;
}

/* ::cue = Sous-titres vidéo */
::cue {
    color: yellow;
    background-color: rgba(0, 0, 0, 0.8);
}

/* ::file-selector-button = Bouton input file */
input[type="file"]::file-selector-button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
}

input[type="file"]::file-selector-button:hover {
    background-color: #2980b9;
}
```

**Tableau Récapitulatif Pseudo-éléments :**

| Pseudo-élément | Description | Propriétés limitées |
|----------------|-------------|---------------------|
| `::before` | Contenu avant | Toutes |
| `::after` | Contenu après | Toutes |
| `::first-line` | Première ligne | Police, couleur, fond |
| `::first-letter` | Première lettre | Police, couleur, fond, marges |
| `::selection` | Texte sélectionné | color, background-color |
| `::placeholder` | Placeholder input | Police, couleur |
| `::marker` | Puce/numéro liste | Police, couleur, content |

---

## 5. Combinateurs

### 5.1 Combinateur Descendant (espace)

```css
/* Sélectionne descendants (enfants, petits-enfants, etc.) */

/* Tous les <p> dans <article> (à n'importe quel niveau) */
article p {
    color: #333;
    line-height: 1.6;
}

/* Tous les <a> dans <nav> */
nav a {
    color: white;
    text-decoration: none;
}

/* Tous les <li> dans <ul> dans <nav> */
nav ul li {
    display: inline-block;
    margin-right: 20px;
}

/* Exemple HTML */
/*
<article>
    <p>Paragraphe direct</p>
    <div>
        <p>Paragraphe dans div (toujours ciblé)</p>
    </div>
</article>
*/

/* Limiter profondeur (meilleure pratique) */
.container p {              /* ✅ 2 niveaux */
    /* Bon */
}

.page .content .article .text p {  /* ❌ Trop profond */
    /* Éviter */
}
```

### 5.2 Combinateur Enfant Direct (>)

```css
/* Sélectionne enfants DIRECTS uniquement (pas petits-enfants) */

/* Paragraphes enfants DIRECTS de article */
article > p {
    font-size: 1.1em;
}

/* Items de liste enfants DIRECTS de nav ul */
nav > ul > li {
    display: inline-block;
}

/* Comparaison descendant vs enfant */

/* Descendant (espace) : TOUS les p */
article p {
    /* Cible p à TOUS les niveaux */
}

/* Enfant direct (>) : p DIRECTS uniquement */
article > p {
    /* Cible SEULEMENT p directs */
}

/* Exemple HTML */
/*
<article>
    <p>Ciblé par article > p ✅</p>
    <div>
        <p>PAS ciblé par article > p ❌</p>
    </div>
</article>
*/

/* Cas d'usage enfant direct */
.menu > li {
    /* Premier niveau menu */
}

.menu li {
    /* TOUS les niveaux (sous-menus aussi) */
}

/* Liste imbriquée */
ul > li {
    font-weight: bold; /* Premier niveau */
}

ul > li > ul > li {
    font-weight: normal; /* Deuxième niveau */
}
```

### 5.3 Combinateur Frère Adjacent (+)

```css
/* Sélectionne frère IMMÉDIATEMENT APRÈS */

/* <p> immédiatement après <h2> */
h2 + p {
    font-size: 1.2em;
    font-weight: bold;
    margin-top: 0;
}

/* Label immédiatement après input checked */
input:checked + label {
    color: green;
    font-weight: bold;
}

/* Exemple HTML */
/*
<h2>Titre</h2>
<p>Premier paragraphe (ciblé) ✅</p>
<p>Deuxième paragraphe (pas ciblé) ❌</p>
*/

/* Checkbox custom */
input[type="checkbox"] {
    display: none;
}

input[type="checkbox"] + label::before {
    content: "☐ ";
    font-size: 1.5em;
}

input[type="checkbox]:checked + label::before {
    content: "☑ ";
    color: green;
}

/* Accordéon */
.accordion-header {
    cursor: pointer;
}

.accordion-content {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
}

.accordion-header.active + .accordion-content {
    max-height: 500px;
}

/* Espacement entre sections */
section + section {
    margin-top: 40px;
}

h2 + h3 {
    margin-top: -10px; /* Réduire espace si h3 suit h2 */
}
```

### 5.4 Combinateur Frères Généraux (~)

```css
/* Sélectionne TOUS les frères APRÈS (pas juste adjacent) */

/* Tous les <p> après <h2> (même niveau) */
h2 ~ p {
    color: #666;
}

/* Exemple HTML */
/*
<h2>Titre</h2>
<p>Premier paragraphe ✅</p>
<div>Autre contenu</div>
<p>Deuxième paragraphe ✅</p>
<p>Troisième paragraphe ✅</p>
*/

/* Comparaison + vs ~ */

/* + (adjacent) : SEULEMENT le suivant immédiat */
h2 + p {
    /* Seul le 1er p après h2 */
}

/* ~ (général) : TOUS les suivants */
h2 ~ p {
    /* TOUS les p après h2 */
}

/* Toggle avec checkbox */
#toggle-menu {
    display: none;
}

#toggle-menu:checked ~ .menu {
    display: block;
}

#toggle-menu:checked ~ label {
    background-color: blue;
}

/* Désactiver éléments suivants */
.disabled ~ .form-field {
    opacity: 0.5;
    pointer-events: none;
}

/* Highlight éléments suivants au hover */
li:hover ~ li {
    opacity: 0.5;
}
```

### 5.5 Tableau Récapitulatif Combinateurs

| Combinateur | Nom | Syntaxe | Description | Exemple |
|-------------|-----|---------|-------------|---------|
| ` ` (espace) | Descendant | `A B` | B descendant de A | `article p` |
| `>` | Enfant direct | `A > B` | B enfant direct de A | `ul > li` |
| `+` | Frère adjacent | `A + B` | B immédiatement après A | `h2 + p` |
| `~` | Frères généraux | `A ~ B` | Tous les B après A | `h2 ~ p` |

**Exemples combinés :**

```css
/* Combinaisons complexes */

/* Liens dans nav > ul > li */
nav > ul > li > a {
    color: white;
}

/* Premier paragraphe après h2 dans article */
article h2 + p {
    font-size: 1.2em;
}

/* Images dans div.gallery qui sont enfants directs */
div.gallery > img {
    width: 200px;
}

/* Tous les p dans section SAUF premier */
section p:not(:first-child) {
    margin-top: 15px;
}

/* Label adjacent à checkbox checked */
input[type="checkbox"]:checked + label {
    font-weight: bold;
}
```

---

## 6. Spécificité Détaillée

### 6.1 Calcul de la Spécificité

```css
/* Format : (inline, IDs, classes/attributs/pseudo-classes, éléments/pseudo-éléments) */

/* Exemples */

* {                          /* (0, 0, 0, 0) = 0 */
    margin: 0;
}

p {                          /* (0, 0, 0, 1) = 1 */
    color: blue;
}

.texte {                     /* (0, 0, 1, 0) = 10 */
    color: red;
}

#titre {                     /* (0, 1, 0, 0) = 100 */
    color: green;
}

p.texte {                    /* (0, 0, 1, 1) = 11 */
    color: orange;
}

div p.texte {                /* (0, 0, 1, 2) = 12 */
    color: purple;
}

#header .nav a {             /* (0, 1, 1, 1) = 111 */
    color: yellow;
}

/* Style inline */
/* <p style="color: pink;"> */ /* (1, 0, 0, 0) = 1000 */

/* !important */
p {
    color: black !important;  /* (1, 0, 0, 0, 1) = 10000+ */
}

/* Exemples détaillés */

/* (0, 0, 0, 1) = 1 */
h1 { }

/* (0, 0, 0, 2) = 2 */
article p { }

/* (0, 0, 1, 0) = 10 */
.button { }

/* (0, 0, 1, 1) = 11 */
p.intro { }

/* (0, 0, 2, 0) = 20 */
.container .text { }

/* (0, 0, 2, 1) = 21 */
.container p.intro { }

/* (0, 1, 0, 0) = 100 */
#header { }

/* (0, 1, 1, 0) = 110 */
#header .nav { }

/* (0, 1, 1, 1) = 111 */
#header .nav a { }

/* (0, 0, 1, 0) = 10 - Pseudo-classe compte comme classe */
a:hover { }

/* (0, 0, 1, 1) = 11 */
p:first-child { }

/* (0, 0, 0, 2) = 2 - Pseudo-élément compte comme élément */
p::before { }

/* (0, 0, 1, 2) = 12 */
p.intro::first-line { }

/* (0, 0, 2, 0) = 20 - Attribut compte comme classe */
input[type="text"] { }
```

### 6.2 Règles de Priorité

```css
/* Ordre de priorité (du plus faible au plus fort) */

/* 1. Sélecteur universel : 0 */
* {
    margin: 0;
}

/* 2. Sélecteur élément : 1 */
p {
    color: blue;
}

/* 3. Sélecteur classe : 10 */
.texte {
    color: red;              /* Gagne sur élément */
}

/* 4. Sélecteur ID : 100 */
#titre {
    color: green;            /* Gagne sur classe */
}

/* 5. Style inline : 1000 */
/* <p style="color: purple;"> */ /* Gagne sur ID */

/* 6. !important : 10000 */
p {
    color: orange !important; /* Gagne sur tout (éviter !) */
}

/* Règle égalité : Dernier gagne */
p {
    color: blue;
}

p {
    color: red;              /* ← Gagne (même spécificité, plus récent) */
}

/* Exemple conflit résolu */

/* HTML : <p id="intro" class="texte">Contenu</p> */

p {                          /* (0, 0, 0, 1) = 1 */
    color: blue;
}

.texte {                     /* (0, 0, 1, 0) = 10 */
    color: red;              /* ← Gagne */
}

#intro {                     /* (0, 1, 0, 0) = 100 */
    color: green;            /* ← Gagne */
}

p.texte {                    /* (0, 0, 1, 1) = 11 */
    color: orange;           /* Perd contre ID */
}

/* Résultat : vert (ID gagne) */
```

### 6.3 Éviter les Guerres de Spécificité

```css
/* ❌ MAUVAIS : Guerre de spécificité */

#header .nav ul li a {       /* (0, 1, 1, 3) = 113 */
    color: blue;
}

/* Pour override, besoin de spécificité supérieure */
#header .nav ul li a.active { /* (0, 1, 2, 3) = 123 */
    color: red;
}

/* ✅ BON : Utiliser classes */

.nav-link {                  /* (0, 0, 1, 0) = 10 */
    color: blue;
}

.nav-link--active {          /* (0, 0, 1, 0) = 10 */
    color: red;
}

/* Même spécificité, ordre compte (dernier gagne) */

/* ❌ MAUVAIS : Abus !important */

.button {
    background-color: blue !important;
}

.button-red {
    background-color: red !important; /* Guerre !important */
}

/* ✅ BON : Spécificité raisonnable */

.button {
    background-color: blue;
}

.button--red {
    background-color: red;   /* Même spécificité, ordre gère */
}

/* Techniques pour réduire spécificité */

/* Utiliser :where() (spécificité 0) */
:where(#header, .header) {   /* (0, 0, 0, 0) = 0 */
    padding: 20px;
}

/* Facilite override sans guerre */
.custom-header {             /* (0, 0, 1, 0) = 10 */
    padding: 40px;           /* Gagne facilement */
}
```

---

## 7. Exercices Pratiques

### Exercice 1 : Menu de Navigation Stylé

**Objectif :** Utiliser pseudo-classes et combinateurs.

**Consigne :** Créer un menu avec :
- Liens avec hover effect
- Premier lien différent
- Dernier lien différent
- Liens pairs avec fond gris clair

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu Navigation</title>
    <link rel="stylesheet" href="menu.css">
</head>
<body>
    <nav class="main-nav">
        <ul>
            <li><a href="#home">Accueil</a></li>
            <li><a href="#about">À propos</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#portfolio">Portfolio</a></li>
            <li><a href="#blog">Blog</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>
</body>
</html>
```

```css
/* menu.css */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    padding: 40px;
}

.main-nav {
    background-color: #2c3e50;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.main-nav ul {
    list-style: none;
    display: flex;
}

/* Tous les liens */
.main-nav a {
    display: block;
    padding: 20px 30px;
    color: white;
    text-decoration: none;
    transition: background-color 0.3s ease;
}

/* Hover sur tous les liens */
.main-nav a:hover {
    background-color: #34495e;
}

/* Premier lien (Accueil) */
.main-nav li:first-child a {
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
    background-color: #3498db;
}

.main-nav li:first-child a:hover {
    background-color: #2980b9;
}

/* Dernier lien (Contact) */
.main-nav li:last-child a {
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    background-color: #e74c3c;
}

.main-nav li:last-child a:hover {
    background-color: #c0392b;
}

/* Liens pairs (2, 4, 6) */
.main-nav li:nth-child(even) {
    background-color: rgba(255, 255, 255, 0.05);
}

/* Active state */
.main-nav a:active {
    transform: scale(0.98);
}
```

</details>

### Exercice 2 : Liste Alternée avec Icônes

**Objectif :** Utiliser ::before et nth-child.

**Consigne :** Créer une liste avec :
- Icônes différentes via ::before
- Couleurs alternées (odd/even)
- Hover effect
- Premier élément en gras

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Liste avec Icônes</title>
    <link rel="stylesheet" href="list.css">
</head>
<body>
    <div class="container">
        <h1>Ma Liste de Tâches</h1>
        <ul class="task-list">
            <li>Apprendre HTML</li>
            <li>Apprendre CSS</li>
            <li>Apprendre JavaScript</li>
            <li>Créer un portfolio</li>
            <li>Postuler pour des jobs</li>
            <li>Devenir développeur web</li>
        </ul>
    </div>
</body>
</html>
```

```css
/* list.css */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.container {
    background-color: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    max-width: 600px;
    width: 100%;
}

h1 {
    color: #2c3e50;
    margin-bottom: 30px;
    text-align: center;
}

.task-list {
    list-style: none;
}

.task-list li {
    padding: 15px 20px 15px 50px;
    margin-bottom: 10px;
    border-radius: 10px;
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Icône ::before */
.task-list li::before {
    content: "✓";
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    width: 25px;
    height: 25px;
    background-color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

/* Couleurs alternées */
.task-list li:nth-child(odd) {
    background-color: #3498db;
    color: white;
}

.task-list li:nth-child(odd)::before {
    color: #3498db;
}

.task-list li:nth-child(even) {
    background-color: #2ecc71;
    color: white;
}

.task-list li:nth-child(even)::before {
    color: #2ecc71;
}

/* Premier élément spécial */
.task-list li:first-child {
    font-weight: bold;
    font-size: 1.1em;
    background-color: #e74c3c;
}

.task-list li:first-child::before {
    content: "★";
    color: #e74c3c;
}

/* Hover effect */
.task-list li:hover {
    transform: translateX(10px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Dernier élément */
.task-list li:last-child {
    margin-bottom: 0;
}
```

</details>

### Exercice 3 : Formulaire Avancé

**Objectif :** Utiliser pseudo-classes de formulaire.

**Consigne :** Créer un formulaire avec :
- Styles :focus
- Validation :valid/:invalid
- Required avec indicateur
- Checkbox custom avec ::before

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulaire Avancé</title>
    <link rel="stylesheet" href="form.css">
</head>
<body>
    <div class="container">
        <h1>Inscription</h1>
        <form>
            <div class="form-group">
                <label for="name">Nom complet <span class="required">*</span></label>
                <input type="text" id="name" required>
            </div>
            
            <div class="form-group">
                <label for="email">Email <span class="required">*</span></label>
                <input type="email" id="email" required>
            </div>
            
            <div class="form-group">
                <label for="age">Âge <span class="required">*</span></label>
                <input type="number" id="age" min="18" max="120" required>
            </div>
            
            <div class="form-group">
                <label for="website">Site web (optionnel)</label>
                <input type="url" id="website">
            </div>
            
            <div class="form-group checkbox-group">
                <input type="checkbox" id="terms" required>
                <label for="terms">J'accepte les conditions d'utilisation <span class="required">*</span></label>
            </div>
            
            <div class="form-group checkbox-group">
                <input type="checkbox" id="newsletter">
                <label for="newsletter">Je souhaite recevoir la newsletter</label>
            </div>
            
            <button type="submit">S'inscrire</button>
        </form>
    </div>
</body>
</html>
```

```css
/* form.css */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.container {
    background-color: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    max-width: 500px;
    width: 100%;
}

h1 {
    color: #2c3e50;
    margin-bottom: 30px;
    text-align: center;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
    color: #34495e;
    font-weight: 500;
}

.required {
    color: #e74c3c;
}

input[type="text"],
input[type="email"],
input[type="number"],
input[type="url"] {
    width: 100%;
    padding: 12px 15px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

/* Focus state */
input[type="text"]:focus,
input[type="email"]:focus,
input[type="number"]:focus,
input[type="url"]:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

/* Required inputs */
input:required {
    border-left: 4px solid #e74c3c;
}

/* Valid state */
input:valid:not(:placeholder-shown) {
    border-color: #2ecc71;
    border-left-color: #2ecc71;
}

/* Invalid state (après interaction) */
input:invalid:not(:placeholder-shown):not(:focus) {
    border-color: #e74c3c;
}

/* Out of range */
input:out-of-range {
    border-color: #e67e22;
    background-color: #ffeaa7;
}

/* Checkbox custom */
.checkbox-group {
    display: flex;
    align-items: center;
}

.checkbox-group input[type="checkbox"] {
    appearance: none;
    width: 24px;
    height: 24px;
    border: 2px solid #ddd;
    border-radius: 4px;
    margin-right: 10px;
    cursor: pointer;
    position: relative;
    transition: all 0.3s ease;
}

.checkbox-group input[type="checkbox"]:hover {
    border-color: #3498db;
}

.checkbox-group input[type="checkbox"]:checked {
    background-color: #3498db;
    border-color: #3498db;
}

.checkbox-group input[type="checkbox"]:checked::before {
    content: "✓";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-weight: bold;
    font-size: 16px;
}

.checkbox-group label {
    margin-bottom: 0;
    cursor: pointer;
}

/* Bouton submit */
button[type="submit"] {
    width: 100%;
    padding: 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.1s ease;
}

button[type="submit"]:hover {
    background-color: #2980b9;
}

button[type="submit"]:active {
    transform: scale(0.98);
}

/* Disabled state */
button[type="submit"]:disabled {
    background-color: #bdc3c7;
    cursor: not-allowed;
}
```

</details>

---

## 8. Projet du Module : Carte Produit Interactive

### 8.1 Cahier des Charges

**Créer une carte produit e-commerce avec tous les sélecteurs maîtrisés :**

**Spécifications techniques :**
- ✅ Structure HTML sémantique
- ✅ Hover effects (pseudo-classe)
- ✅ Badge "Nouveau" (::before ou ::after)
- ✅ Étoiles de notation (::before avec content)
- ✅ Bouton avec états (hover, active, focus)
- ✅ Première image agrandie (nth-child)
- ✅ Prix barré pour promotion (combinateur)
- ✅ CSS externe, code validé

### 8.2 Solution Complète

<details>
<summary>Voir la solution complète du projet</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carte Produit Interactive</title>
    <link rel="stylesheet" href="product-card.css">
</head>
<body>
    <div class="container">
        <div class="product-card">
            <div class="product-badge">Nouveau</div>
            
            <div class="product-image">
                <img src="https://via.placeholder.com/300x300/3498db/ffffff?text=Produit" alt="Produit">
            </div>
            
            <div class="product-content">
                <h2 class="product-title">Casque Audio Premium</h2>
                
                <div class="product-rating">
                    <span class="stars" data-rating="4">★★★★★</span>
                    <span class="reviews">(127 avis)</span>
                </div>
                
                <p class="product-description">
                    Casque audio haute qualité avec réduction de bruit active, 
                    autonomie 30 heures, Bluetooth 5.0 et son immersif.
                </p>
                
                <div class="product-features">
                    <ul>
                        <li>Réduction de bruit active</li>
                        <li>Autonomie 30h</li>
                        <li>Bluetooth 5.0</li>
                        <li>Pliable et léger</li>
                    </ul>
                </div>
                
                <div class="product-price">
                    <span class="price-old">199,99 €</span>
                    <span class="price-current">149,99 €</span>
                    <span class="price-discount">-25%</span>
                </div>
                
                <div class="product-actions">
                    <button class="btn btn-primary">Ajouter au panier</button>
                    <button class="btn btn-secondary">Liste de souhaits</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

```css
/* product-card.css */

/* ========================================
   RESET & BASE
   ======================================== */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.container {
    max-width: 400px;
    width: 100%;
}

/* ========================================
   PRODUCT CARD
   ======================================== */

.product-card {
    background-color: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
}

/* ========================================
   BADGE (::before)
   ======================================== */

.product-badge {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: #e74c3c;
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: bold;
    z-index: 10;
    box-shadow: 0 4px 10px rgba(231, 76, 60, 0.4);
}

.product-badge::before {
    content: "🎉 ";
}

/* ========================================
   IMAGE
   ======================================== */

.product-image {
    position: relative;
    overflow: hidden;
    background-color: #f8f9fa;
}

.product-image img {
    width: 100%;
    height: 300px;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.product-card:hover .product-image img {
    transform: scale(1.1);
}

/* Overlay au hover */
.product-image::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        to bottom,
        transparent 0%,
        rgba(0, 0, 0, 0.3) 100%
    );
    opacity: 0;
    transition: opacity 0.3s ease;
}

.product-card:hover .product-image::after {
    opacity: 1;
}

/* ========================================
   CONTENT
   ======================================== */

.product-content {
    padding: 30px;
}

.product-title {
    font-size: 1.5rem;
    color: #2c3e50;
    margin-bottom: 15px;
}

/* ========================================
   RATING (::before avec étoiles)
   ======================================== */

.product-rating {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
}

.stars {
    color: #ffd700;
    font-size: 1.2rem;
    letter-spacing: 2px;
    position: relative;
}

/* Étoiles vides (background) */
.stars::before {
    content: "★★★★★";
    position: absolute;
    top: 0;
    left: 0;
    color: #ddd;
}

/* Étoiles pleines (overlay) */
.stars::after {
    content: "★★★★★";
    position: absolute;
    top: 0;
    left: 0;
    color: #ffd700;
    overflow: hidden;
    width: 80%; /* 4 étoiles sur 5 = 80% */
}

.reviews {
    color: #7f8c8d;
    font-size: 0.9rem;
}

/* ========================================
   DESCRIPTION
   ======================================== */

.product-description {
    color: #555;
    line-height: 1.6;
    margin-bottom: 20px;
}

/* ========================================
   FEATURES (Liste avec ::before)
   ======================================== */

.product-features {
    margin-bottom: 20px;
}

.product-features ul {
    list-style: none;
}

.product-features li {
    padding: 8px 0;
    color: #555;
    position: relative;
    padding-left: 25px;
}

.product-features li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #2ecc71;
    font-weight: bold;
}

/* Hover sur items */
.product-features li:hover {
    color: #2c3e50;
}

/* Premier item en gras */
.product-features li:first-child {
    font-weight: bold;
    color: #3498db;
}

.product-features li:first-child::before {
    color: #3498db;
}

/* ========================================
   PRICE (Combinateur + pour prix barré)
   ======================================== */

.product-price {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
}

.price-old {
    font-size: 1.1rem;
    color: #95a5a6;
    text-decoration: line-through;
}

.price-current {
    font-size: 2rem;
    font-weight: bold;
    color: #2ecc71;
}

.price-discount {
    background-color: #2ecc71;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 0.9rem;
    font-weight: bold;
}

/* ========================================
   ACTIONS (Boutons avec pseudo-classes)
   ======================================== */

.product-actions {
    display: flex;
    gap: 10px;
}

.btn {
    flex: 1;
    padding: 15px;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

/* Bouton primary */
.btn-primary {
    background-color: #3498db;
    color: white;
}

.btn-primary:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
}

.btn-primary:active {
    transform: translateY(0);
}

.btn-primary:focus {
    outline: 3px solid rgba(52, 152, 219, 0.5);
}

/* Bouton secondary */
.btn-secondary {
    background-color: white;
    color: #3498db;
    border: 2px solid #3498db;
}

.btn-secondary:hover {
    background-color: #3498db;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
}

.btn-secondary:active {
    transform: translateY(0);
}

.btn-secondary:focus {
    outline: 3px solid rgba(52, 152, 219, 0.5);
}

/* Icône cœur pour wishlist (::before) */
.btn-secondary::before {
    content: "♡ ";
    font-size: 1.2em;
}

.btn-secondary:hover::before {
    content: "♥ ";
}

/* ========================================
   RESPONSIVE
   ======================================== */

@media (max-width: 480px) {
    .product-content {
        padding: 20px;
    }
    
    .product-title {
        font-size: 1.3rem;
    }
    
    .price-current {
        font-size: 1.7rem;
    }
    
    .product-actions {
        flex-direction: column;
    }
}
```

</details>

### 8.3 Checklist de Validation

Avant de considérer votre projet terminé, vérifiez :

- [ ] Carte produit complète avec image
- [ ] Badge "Nouveau" avec ::before
- [ ] Étoiles de notation avec ::before/::after
- [ ] Liste features avec icônes ::before
- [ ] Prix barré (text-decoration: line-through)
- [ ] 2 boutons (primary, secondary) avec hover/active/focus
- [ ] Overlay image au hover (::after)
- [ ] Premier élément liste en gras (:first-child)
- [ ] Transition smooth sur tous les hovers
- [ ] Code CSS externe validé W3C
- [ ] Responsive (media query mobile)

---

## 9. Best Practices Sélecteurs

### 9.1 Hiérarchie de Préférence

```css
/* 1. ✅ PRÉFÉRER : Classes (réutilisables, spécificité raisonnable) */
.button { }
.card { }
.text-center { }

/* 2. ✅ OK : Éléments (styles globaux) */
p { }
h1 { }
article { }

/* 3. ⚠️ AVEC MODÉRATION : Combinateurs (max 2-3 niveaux) */
.card .title { }          /* OK */
.page .content .card { }  /* Limite */

/* 4. ❌ ÉVITER : IDs pour styles */
#header { }               /* Préférer .header */

/* 5. ❌ ÉVITER : Sélecteurs trop complexes */
#page > div.container > section.content > article:nth-child(2) > p:first-of-type {
    /* Trop spécifique, impossible à override */
}

/* 6. ❌❌ ÉVITER ABSOLUMENT : !important */
.text {
    color: red !important; /* Guerre de spécificité */
}
```

### 9.2 Performance

```css
/* ✅ RAPIDE : Classes simples */
.button { }

/* ✅ RAPIDE : Sélecteurs courts */
.card .title { }

/* ⚠️ MOYEN : Sélecteurs d'attributs */
a[href^="https"] { }

/* ⚠️ MOYEN : Pseudo-classes complexes */
li:nth-child(3n+2) { }

/* ❌ LENT : Sélecteur universel dans combinateur */
.container * { }          /* Éviter */

/* ❌ LENT : Descendant profond */
div div div div p { }     /* Très lent */

/* ✅ Optimisation : Préférer enfant direct */
.container > .item { }    /* Plus rapide que .container .item */
```

### 9.3 Maintenabilité

```css
/* ✅ BON : Nomenclature BEM */
.product-card { }
.product-card__title { }
.product-card__image { }
.product-card--featured { }

/* ✅ BON : Sélecteurs auto-documentés */
.is-active { }
.has-dropdown { }
.is-disabled { }

/* ❌ MAUVAIS : Noms vagues */
.box { }
.item { }
.thing { }

/* ✅ BON : Groupement logique */
/* Boutons */
.btn { }
.btn--primary { }
.btn--secondary { }

/* Navigation */
.nav { }
.nav__link { }
.nav__link--active { }

/* ❌ MAUVAIS : Tout mélangé */
.btn { }
.nav { }
.btn-primary { }
.nav-link { }
```

---

## 10. Checkpoint de Progression

### À la fin de ce Module 8, vous maîtrisez :

**Sélecteurs de base :**

- [x] Universel (*)
- [x] Élément (p, div, h1)
- [x] Classe (.)
- [x] ID (#)

**Sélecteurs d'attributs :**

- [x] Présence [attr]
- [x] Valeur exacte [attr="val"]
- [x] Contient mot [attr~="val"]
- [x] Commence par [attr^="val"]
- [x] Finit par [attr$="val"]
- [x] Contient [attr*="val"]
- [x] Commence ou tiret [attr|="val"]

**Pseudo-classes :**

- [x] Liens (:link, :visited, :hover, :active)
- [x] Formulaires (:focus, :checked, :disabled, :valid, :invalid)
- [x] Structurelles (:first-child, :last-child, :nth-child, :nth-of-type)
- [x] Logiques (:not, :is, :where, :has)

**Pseudo-éléments :**

- [x] ::before et ::after
- [x] ::first-line et ::first-letter
- [x] ::selection
- [x] ::placeholder
- [x] ::marker

**Combinateurs :**

- [x] Descendant (espace)
- [x] Enfant direct (>)
- [x] Frère adjacent (+)
- [x] Frères généraux (~)

**Spécificité :**

- [x] Calcul (inline, IDs, classes, éléments)
- [x] Règles de priorité
- [x] Éviter guerres de spécificité

**Best practices :**

- [x] Hiérarchie de préférence
- [x] Performance
- [x] Maintenabilité (BEM)

### Prochaine Étape

**Direction le Module 9** où vous allez :

- Maîtriser le Box Model CSS
- Comprendre margin, padding, border
- Gérer width, height, box-sizing
- Maîtriser margin collapsing
- Calculer dimensions précises
- Créer layouts avec box model

---

**Module 8 Terminé - Bravo ! 🎉 🎯**

**Vous avez appris :**

- ✅ 50+ sélecteurs CSS maîtrisés
- ✅ Tous les sélecteurs d'attributs (7 types)
- ✅ 20+ pseudo-classes (:hover, :nth-child, :has, etc.)
- ✅ 8+ pseudo-éléments (::before, ::after, etc.)
- ✅ 4 combinateurs (descendant, enfant, adjacent, général)
- ✅ Spécificité complète (calcul et priorités)
- ✅ Best practices (performance, maintenabilité)

**Statistiques Module 8 :**

- 1 projet complet (Carte produit interactive)
- 3 exercices progressifs avec solutions
- 150+ exemples de code
- Sélecteurs CSS maîtrisés

**Prochain objectif : Maîtriser le Box Model CSS (Module 9)**

**Félicitations pour cette maîtrise des sélecteurs CSS ! 🚀🎯**
