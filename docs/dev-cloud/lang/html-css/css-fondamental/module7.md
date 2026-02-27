---
description: "Découvrir CSS : syntaxe, intégration, cascade, spécificité, couleurs, unités, propriétés de base"
icon: lucide/book-open-check
tags: ["CSS", "STYLES", "COULEURS", "UNITÉS", "CASCADE", "SPÉCIFICITÉ"]
---

# VII - Introduction CSS

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="4-6 heures">
</div>

## Introduction : Donner Vie au Contenu

!!! quote "Analogie pédagogique"
    _Imaginez construire une **maison**. Le **HTML** est la structure : murs, fenêtres, portes, plomberie. Le **CSS** est la **décoration intérieure** : couleur des murs, style des meubles, éclairage, agencement. Sans HTML, pas de maison (pas de contenu). Sans CSS, maison grise et moche (contenu sans style). HTML dit "voici un titre", CSS dit "ce titre est en rouge, taille 32px, centré". HTML crée une liste, CSS la transforme en menu horizontal avec survol. Avant CSS (1996), les styles étaient dans HTML (`<font color="red">`). Résultat : code sale, impossible à maintenir. CSS sépare **contenu** (HTML) et **présentation** (CSS). Un fichier CSS peut styler 1000 pages ! Modifier une couleur dans le CSS = 1000 pages mises à jour instantanément. Ce module vous enseigne les fondations CSS : syntaxe, intégration, cascade, couleurs, unités. Préparez-vous à transformer vos pages HTML brutes en designs professionnels._

**CSS (Cascading Style Sheets)** = Langage de feuilles de style pour décrire la présentation de documents HTML.

**Pourquoi CSS est essentiel ?**

✅ **Séparation** : Contenu (HTML) séparé de présentation (CSS)  
✅ **Réutilisabilité** : Un CSS pour multiples pages  
✅ **Maintenance** : Modification globale en un seul endroit  
✅ **Performance** : CSS caché une fois, utilisé partout  
✅ **Responsive** : Adaptation mobile/desktop  
✅ **Design** : Créativité illimitée (animations, transitions, layouts)  

**Avant CSS vs Après CSS :**

```html
<!-- ❌ AVANT CSS (années 90) : Styles dans HTML -->
<font color="red" size="5" face="Arial">
    <center>
        <b>Titre Important</b>
    </center>
</font>
<table width="800" bgcolor="#cccccc">
    <tr>
        <td>Contenu...</td>
    </tr>
</table>
<!-- Code illisible, impossible à maintenir -->

<!-- ✅ APRÈS CSS (1996+) : Séparation claire -->
<h1>Titre Important</h1>
<div class="content">Contenu...</div>

<!-- CSS (fichier séparé) -->
h1 {
    color: red;
    font-size: 32px;
    text-align: center;
}
.content {
    max-width: 800px;
    background-color: #cccccc;
}
```

**Ce module pose les fondations de votre apprentissage CSS.**

---

## 1. Qu'est-ce que CSS ?

### 1.1 Définition et Histoire

**CSS = Cascading Style Sheets (Feuilles de Style en Cascade)**

```
HTML  →  Structure et contenu (squelette)
CSS   →  Présentation et design (peinture, décoration)
JS    →  Comportement et interactivité (électricité, automatisation)
```

**Chronologie CSS :**

| Année | Version | Nouveautés majeures |
|-------|---------|---------------------|
| 1996 | CSS1 | Propriétés de base (couleur, police, marges) |
| 1998 | CSS2 | Positionnement, z-index, media types |
| 1999 | CSS2.1 | Corrections et clarifications CSS2 |
| 2011+ | CSS3 | Modules (Flexbox, Grid, Animations, Transforms) |
| Aujourd'hui | CSS4+ | Variables CSS, Container Queries, :has() |

**CSS3+ = Approche modulaire** (pas de "CSS4" officiel, mais modules évoluant indépendamment)

### 1.2 Rôle du CSS

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rôle du CSS</title>
    <style>
        /* CSS transforme le HTML brut */
        h1 {
            color: #2c3e50;              /* Couleur texte */
            font-size: 36px;             /* Taille police */
            text-align: center;          /* Alignement */
            margin-bottom: 20px;         /* Marge bas */
        }
        
        p {
            color: #34495e;              /* Couleur paragraphe */
            line-height: 1.6;            /* Hauteur ligne */
            max-width: 600px;            /* Largeur max */
            margin: 0 auto;              /* Centrage */
        }
        
        .highlight {
            background-color: #f1c40f;   /* Fond jaune */
            padding: 2px 4px;            /* Espacement interne */
        }
    </style>
</head>
<body>
    <h1>Le pouvoir du CSS</h1>
    <p>
        Ce texte est <span class="highlight">stylé avec CSS</span>.
        Sans CSS, ce serait noir sur blanc, Times New Roman, 16px.
    </p>
</body>
</html>
```

**Rendu SANS CSS :**
```
Le pouvoir du CSS

Ce texte est stylé avec CSS. Sans CSS, ce serait noir sur blanc, Times New Roman, 16px.
```

**Rendu AVEC CSS :**
```
        Le pouvoir du CSS
        (bleu foncé, 36px, centré)

Ce texte est stylé avec CSS (fond jaune). Sans CSS...
(gris foncé, 16px * 1.6 interligne, max 600px centré)
```

---

## 2. Intégration CSS

### 2.1 CSS Inline (Dans la Balise)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>CSS Inline</title>
</head>
<body>
    <!-- CSS dans l'attribut style -->
    <h1 style="color: red; font-size: 32px; text-align: center;">
        Titre avec CSS inline
    </h1>
    
    <p style="color: blue; background-color: #f0f0f0; padding: 10px;">
        Paragraphe avec CSS inline
    </p>
    
    <div style="width: 300px; height: 200px; background-color: #3498db; margin: 20px;">
        Boîte bleue
    </div>
</body>
</html>
```

**Syntaxe CSS inline :**
```html
<balise style="propriété: valeur; propriété2: valeur2;">
```

**❌ Inconvénients CSS inline :**
- Pas de réutilisabilité (répétition)
- Code HTML encombré
- Difficile à maintenir
- Priorité maximale (écrase tout)
- Pas de pseudo-classes (:hover impossible)

**✅ Quand utiliser CSS inline :**
- Emails HTML (clients email limitent CSS externe)
- Tests rapides (debugging)
- Styles JavaScript dynamiques
- CMS avec éditeur WYSIWYG

### 2.2 CSS Internal (Dans `<style>`)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>CSS Internal</title>
    
    <!-- CSS dans <style> dans <head> -->
    <style>
        /* Styles pour toute la page */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #ecf0f1;
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        
        p {
            color: #34495e;
            line-height: 1.6;
            max-width: 600px;
            margin: 20px auto;
        }
        
        .box {
            width: 300px;
            height: 200px;
            background-color: #3498db;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px auto;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <h1>CSS Internal</h1>
    <p>
        Les styles sont définis dans la balise &lt;style&gt; 
        dans le &lt;head&gt; du document.
    </p>
    <div class="box">Boîte stylée</div>
</body>
</html>
```

**✅ Avantages CSS internal :**
- Styles centralisés dans la page
- Réutilisables dans toute la page
- Pseudo-classes possibles (:hover, :focus)
- Bon pour pages uniques (landing page)

**❌ Inconvénients CSS internal :**
- Pas de réutilisation entre pages
- Page plus lourde (CSS dans HTML)
- Pas de cache navigateur pour CSS

**✅ Quand utiliser CSS internal :**
- Page unique isolée (landing page)
- Prototypage rapide
- Styles spécifiques à une page (avec external global)

### 2.3 CSS External (Fichier Séparé) ⭐ RECOMMANDÉ

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>CSS External</title>
    
    <!-- Lien vers fichier CSS externe -->
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Mon Site Web</h1>
        <nav>
            <ul>
                <li><a href="/">Accueil</a></li>
                <li><a href="/about">À propos</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <article>
            <h2>Article principal</h2>
            <p>Contenu de l'article...</p>
        </article>
    </main>
    
    <footer>
        <p>&copy; 2024 Mon Site</p>
    </footer>
</body>
</html>
```

```css
/* styles.css (fichier séparé) */

/* Reset de base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}

/* Header */
header {
    background-color: #2c3e50;
    color: white;
    padding: 20px;
}

header h1 {
    margin-bottom: 10px;
}

/* Navigation */
nav ul {
    list-style: none;
    display: flex;
    gap: 20px;
}

nav a {
    color: white;
    text-decoration: none;
}

nav a:hover {
    text-decoration: underline;
}

/* Main content */
main {
    max-width: 1200px;
    margin: 40px auto;
    padding: 0 20px;
}

article {
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

/* Footer */
footer {
    background-color: #34495e;
    color: white;
    text-align: center;
    padding: 20px;
    margin-top: 40px;
}
```

**Balise `<link>` expliquée :**

```html
<link rel="stylesheet" href="styles.css">
       ↑                    ↑
       |                    |
   Relation          Chemin fichier CSS
   (feuille style)
```

**Attributs `<link>` :**

| Attribut | Valeurs | Description |
|----------|---------|-------------|
| `rel` | `stylesheet` | Type de relation (obligatoire) |
| `href` | URL/chemin | Chemin vers fichier CSS (obligatoire) |
| `type` | `text/css` | Type MIME (optionnel, obsolète en HTML5) |
| `media` | `screen`, `print` | Type de média (optionnel) |

**✅ Avantages CSS external (MEILLEURE PRATIQUE) :**
- **Réutilisable** : Un CSS pour 1000 pages
- **Maintenance** : Modification globale instantanée
- **Cache** : Navigateur cache le CSS (performance)
- **Organisation** : Code propre et séparé
- **Collaboration** : Plusieurs développeurs simultanés

**❌ Inconvénients CSS external :**
- Requête HTTP supplémentaire (négligeable)
- Fichier séparé à gérer

**Organisation fichiers recommandée :**

```
mon-site/
├── index.html
├── about.html
├── contact.html
├── css/
│   ├── styles.css       (styles principaux)
│   ├── responsive.css   (media queries)
│   └── print.css        (impression)
├── js/
│   └── script.js
└── images/
    └── logo.png
```

### 2.4 Multiples Feuilles CSS

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Multiples CSS</title>
    
    <!-- CSS dans l'ordre de chargement -->
    <link rel="stylesheet" href="css/reset.css">        <!-- 1. Reset navigateur -->
    <link rel="stylesheet" href="css/typography.css">   <!-- 2. Typographie -->
    <link rel="stylesheet" href="css/layout.css">       <!-- 3. Layout général -->
    <link rel="stylesheet" href="css/components.css">   <!-- 4. Composants -->
    <link rel="stylesheet" href="css/responsive.css">   <!-- 5. Responsive -->
    
    <!-- CSS pour impression -->
    <link rel="stylesheet" href="css/print.css" media="print">
</head>
<body>
    <!-- Contenu -->
</body>
</html>
```

---

## 3. Syntaxe CSS

### 3.1 Anatomie d'une Règle CSS

```css
/* Règle CSS complète */
sélecteur {
    propriété: valeur;
    propriété2: valeur2;
}

/* Exemple concret */
h1 {
    color: blue;
    font-size: 32px;
    text-align: center;
}

/* Décortiqué */
h1                     → Sélecteur (quoi cibler)
{                      → Accolade ouvrante
    color: blue;       → Déclaration 1
    ↑      ↑    ↑
    |      |    |
    Prop  Val  Point-virgule
    
    font-size: 32px;   → Déclaration 2
    text-align: center; → Déclaration 3
}                      → Accolade fermante
```

**Vocabulaire CSS :**

```css
h1 {                        /* ← RÈGLE CSS */
    color: red;             /* ← DÉCLARATION */
    ↑      ↑
    |      └── VALEUR
    └── PROPRIÉTÉ
}
↑
SÉLECTEUR
```

**Exemples de règles CSS :**

```css
/* Sélecteur d'élément */
p {
    color: #333;
    line-height: 1.6;
}

/* Sélecteur de classe */
.button {
    background-color: blue;
    color: white;
    padding: 10px 20px;
}

/* Sélecteur d'ID */
#header {
    background-color: black;
    height: 80px;
}

/* Sélecteur multiple */
h1, h2, h3 {
    font-family: Arial, sans-serif;
    color: #2c3e50;
}

/* Sélecteur descendant */
article p {
    font-size: 16px;
    margin-bottom: 15px;
}
```

### 3.2 Commentaires CSS

```css
/* Commentaire CSS sur une ligne */

/*
Commentaire CSS
sur plusieurs lignes
pour expliquer du code complexe
*/

/* ========================================
   SECTION : NAVIGATION
   ======================================== */
nav {
    /* Styles de navigation */
}

/* TODO : Ajouter styles responsive */
/* FIXME : Corriger bug padding */
/* NOTE : Compatible IE11+ */

/*
❌ MAUVAIS : Commentaires inutiles
*/
.button {
    color: red; /* Couleur rouge */
    /* ↑ Évident, inutile */
}

/*
✅ BON : Commentaires utiles
*/
.button {
    color: red; /* Rouge brand identity (voir charte graphique) */
    /* ↑ Explique POURQUOI, pas QUOI */
}

/* Hack pour IE11 */
.box {
    display: flex; /* Modern browsers */
    display: -ms-flexbox; /* IE10-11 */
}
```

**⚠️ Attention : Pas de `//` en CSS !**

```css
/* ✅ BON : Commentaire valide */
/* Ce commentaire fonctionne */

/* ❌ MAUVAIS : Syntaxe invalide */
// Ce commentaire ne fonctionne PAS en CSS
// (fonctionne en JavaScript, pas CSS)
```

### 3.3 Regroupement de Sélecteurs

```css
/* ❌ MAUVAIS : Répétition */
h1 {
    color: #2c3e50;
    font-family: Arial, sans-serif;
}

h2 {
    color: #2c3e50;
    font-family: Arial, sans-serif;
}

h3 {
    color: #2c3e50;
    font-family: Arial, sans-serif;
}

/* ✅ BON : Regroupement */
h1, h2, h3 {
    color: #2c3e50;
    font-family: Arial, sans-serif;
}

/* Styles spécifiques ensuite */
h1 {
    font-size: 36px;
}

h2 {
    font-size: 28px;
}

h3 {
    font-size: 22px;
}

/* Regroupement de classes */
.button-primary,
.button-secondary,
.button-danger {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}

/* Couleurs spécifiques */
.button-primary {
    background-color: blue;
    color: white;
}

.button-secondary {
    background-color: gray;
    color: white;
}

.button-danger {
    background-color: red;
    color: white;
}
```

---

## 4. Couleurs en CSS

### 4.1 Noms de Couleurs

```css
/* 140 noms de couleurs prédéfinis */
h1 {
    color: red;              /* Rouge */
    background-color: blue;  /* Bleu */
}

p {
    color: black;            /* Noir */
    background-color: white; /* Blanc */
}

/* Couleurs courantes */
.couleurs-base {
    color: black;            /* Noir */
    color: white;            /* Blanc */
    color: red;              /* Rouge */
    color: green;            /* Vert */
    color: blue;             /* Bleu */
    color: yellow;           /* Jaune */
    color: orange;           /* Orange */
    color: purple;           /* Violet */
    color: pink;             /* Rose */
    color: gray;             /* Gris */
}

/* Nuances de gris */
.nuances-gris {
    color: black;            /* #000000 */
    color: darkgray;         /* #A9A9A9 */
    color: gray;             /* #808080 */
    color: lightgray;        /* #D3D3D3 */
    color: white;            /* #FFFFFF */
}

/* Autres couleurs */
.autres {
    color: tomato;           /* #FF6347 */
    color: coral;            /* #FF7F50 */
    color: crimson;          /* #DC143C */
    color: gold;             /* #FFD700 */
    color: turquoise;        /* #40E0D0 */
    color: navy;             /* #000080 */
}
```

**❌ Inconvénients noms de couleurs :**
- Limité à 140 couleurs
- Noms pas toujours précis
- Pas de nuances fines

**✅ Quand utiliser noms :**
- Prototypage rapide
- Tests simples
- Couleurs évidentes (white, black)

### 4.2 Hexadécimal (Hex)

```css
/* Format : #RRGGBB (Red Green Blue) */
/* Chaque composante : 00 (0) à FF (255) */

h1 {
    color: #FF0000;          /* Rouge pur (255, 0, 0) */
    color: #00FF00;          /* Vert pur (0, 255, 0) */
    color: #0000FF;          /* Bleu pur (0, 0, 255) */
}

/* Noir et blanc */
.noir-blanc {
    color: #000000;          /* Noir (0, 0, 0) */
    color: #FFFFFF;          /* Blanc (255, 255, 255) */
}

/* Nuances de gris (R=G=B) */
.gris {
    color: #333333;          /* Gris très foncé */
    color: #666666;          /* Gris moyen */
    color: #999999;          /* Gris clair */
    color: #CCCCCC;          /* Gris très clair */
}

/* Couleurs web courantes */
.couleurs-web {
    color: #2C3E50;          /* Bleu marine foncé */
    color: #3498DB;          /* Bleu ciel */
    color: #E74C3C;          /* Rouge */
    color: #2ECC71;          /* Vert */
    color: #F39C12;          /* Orange */
    color: #9B59B6;          /* Violet */
}

/* Format court : #RGB (si doublons) */
h2 {
    color: #F00;             /* = #FF0000 (rouge) */
    color: #0F0;             /* = #00FF00 (vert) */
    color: #00F;             /* = #0000FF (bleu) */
    color: #FFF;             /* = #FFFFFF (blanc) */
    color: #000;             /* = #000000 (noir) */
    color: #CCC;             /* = #CCCCCC (gris clair) */
}
```

**Conversion hex ↔ décimal :**

```
Hexadécimal : 0 1 2 3 4 5 6 7 8 9 A  B  C  D  E  F
Décimal     : 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15

#FF0000
 ↑↑ ↑↑ ↑↑
 RR GG BB
 
FF = 15×16 + 15 = 255
00 = 0
00 = 0

→ rgb(255, 0, 0) = Rouge pur
```

**Outils pour choisir couleurs hex :**
- Color picker navigateur (DevTools)
- Adobe Color
- Coolors.co
- Paletton.com

### 4.3 RGB et RGBA

```css
/* RGB : Red Green Blue (0-255) */
h1 {
    color: rgb(255, 0, 0);       /* Rouge */
    color: rgb(0, 255, 0);       /* Vert */
    color: rgb(0, 0, 255);       /* Bleu */
}

/* Noir et blanc */
.noir-blanc {
    color: rgb(0, 0, 0);         /* Noir */
    color: rgb(255, 255, 255);   /* Blanc */
}

/* Gris (R=G=B) */
.gris {
    color: rgb(51, 51, 51);      /* #333333 */
    color: rgb(128, 128, 128);   /* #808080 */
    color: rgb(204, 204, 204);   /* #CCCCCC */
}

/* RGBA : RGB + Alpha (transparence 0-1) */
.transparence {
    background-color: rgba(255, 0, 0, 1);    /* Rouge opaque (100%) */
    background-color: rgba(255, 0, 0, 0.8);  /* Rouge 80% */
    background-color: rgba(255, 0, 0, 0.5);  /* Rouge 50% */
    background-color: rgba(255, 0, 0, 0.2);  /* Rouge 20% */
    background-color: rgba(255, 0, 0, 0);    /* Transparent (0%) */
}

/* Overlay semi-transparent */
.overlay {
    background-color: rgba(0, 0, 0, 0.7);    /* Noir 70% opacité */
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

/* Bouton avec hover transparent */
.button {
    background-color: rgb(52, 152, 219);
}

.button:hover {
    background-color: rgba(52, 152, 219, 0.8); /* 80% opacité au survol */
}
```

**Alpha (transparence) :**

```
alpha: 1   = 100% opaque (solide)
alpha: 0.8 = 80% opaque, 20% transparent
alpha: 0.5 = 50% opaque, 50% transparent
alpha: 0.2 = 20% opaque, 80% transparent
alpha: 0   = 0% opaque (invisible)
```

### 4.4 HSL et HSLA

```css
/* HSL : Hue Saturation Lightness */
/* Hue (Teinte) : 0-360° (roue chromatique) */
/* Saturation : 0-100% (intensité couleur) */
/* Lightness : 0-100% (luminosité) */

h1 {
    /* Hue (teinte) */
    color: hsl(0, 100%, 50%);      /* Rouge (0°) */
    color: hsl(120, 100%, 50%);    /* Vert (120°) */
    color: hsl(240, 100%, 50%);    /* Bleu (240°) */
}

/* Roue chromatique */
.teintes {
    color: hsl(0, 100%, 50%);      /* Rouge */
    color: hsl(30, 100%, 50%);     /* Orange */
    color: hsl(60, 100%, 50%);     /* Jaune */
    color: hsl(120, 100%, 50%);    /* Vert */
    color: hsl(180, 100%, 50%);    /* Cyan */
    color: hsl(240, 100%, 50%);    /* Bleu */
    color: hsl(300, 100%, 50%);    /* Magenta */
}

/* Saturation (intensité) */
.saturation {
    color: hsl(240, 100%, 50%);    /* Bleu saturé */
    color: hsl(240, 75%, 50%);     /* Bleu moins saturé */
    color: hsl(240, 50%, 50%);     /* Bleu délavé */
    color: hsl(240, 25%, 50%);     /* Bleu grisâtre */
    color: hsl(240, 0%, 50%);      /* Gris (pas de couleur) */
}

/* Luminosité (clarté) */
.luminosite {
    color: hsl(240, 100%, 0%);     /* Noir */
    color: hsl(240, 100%, 25%);    /* Bleu très foncé */
    color: hsl(240, 100%, 50%);    /* Bleu standard */
    color: hsl(240, 100%, 75%);    /* Bleu clair */
    color: hsl(240, 100%, 100%);   /* Blanc */
}

/* HSLA : HSL + Alpha */
.transparence-hsl {
    background-color: hsla(240, 100%, 50%, 1);    /* Bleu opaque */
    background-color: hsla(240, 100%, 50%, 0.8);  /* Bleu 80% */
    background-color: hsla(240, 100%, 50%, 0.5);  /* Bleu 50% */
    background-color: hsla(240, 100%, 50%, 0.2);  /* Bleu 20% */
}

/* Palette de couleurs harmonieuse */
:root {
    --primary: hsl(220, 90%, 56%);         /* Bleu principal */
    --primary-light: hsl(220, 90%, 70%);   /* Bleu clair */
    --primary-dark: hsl(220, 90%, 40%);    /* Bleu foncé */
}
```

**Avantages HSL :**
- Plus intuitif que RGB
- Facile de créer variations (éclaircir/assombrir)
- Palettes harmonieuses (même teinte, différentes saturations/luminosités)

**Comparaison formats couleurs :**

| Format | Syntaxe | Transparence | Usage |
|--------|---------|--------------|-------|
| Nom | `red` | ❌ | Prototypage rapide |
| Hex | `#FF0000` | ❌ | Standard web |
| RGB | `rgb(255, 0, 0)` | ✅ rgba() | Précision valeurs |
| HSL | `hsl(0, 100%, 50%)` | ✅ hsla() | Palettes harmonieuses |

---

## 5. Unités CSS

### 5.1 Unités Absolues

```css
/* PX (Pixels) : Unité absolue fixe */
h1 {
    font-size: 32px;         /* 32 pixels */
    width: 800px;            /* 800 pixels */
    margin: 20px;            /* 20 pixels */
}

/* PT (Points) : Impression (1pt = 1/72 inch) */
@media print {
    p {
        font-size: 12pt;     /* Pour impression */
    }
}

/* CM, MM, IN : Rarement utilisées web */
.print-only {
    width: 21cm;             /* 21 centimètres */
    height: 29.7cm;          /* A4 */
}
```

**Pixels (px) :**
- Unité la plus courante
- Précise et prévisible
- ❌ Ne s'adapte pas au zoom navigateur (accessibilité)
- ✅ Bon pour bordures, ombres, petits détails

### 5.2 Unités Relatives

```css
/* EM : Relatif à la taille de police du PARENT */
body {
    font-size: 16px;         /* Base */
}

.container {
    font-size: 20px;         /* Parent = 20px */
}

.text {
    font-size: 1.5em;        /* 1.5 × 20px = 30px */
    margin: 2em;             /* 2 × 30px (sa propre taille) = 60px */
}

/* Cascade EM (attention !) */
body {
    font-size: 16px;
}

article {
    font-size: 1.2em;        /* 1.2 × 16px = 19.2px */
}

article p {
    font-size: 1.2em;        /* 1.2 × 19.2px = 23.04px (effet cascade) */
}

/* REM : Relatif à la taille de police ROOT (html) */
html {
    font-size: 16px;         /* Base globale */
}

.text {
    font-size: 1.5rem;       /* 1.5 × 16px = 24px (TOUJOURS) */
    margin: 2rem;            /* 2 × 16px = 32px */
}

/* ✅ REM préféré à EM (pas d'effet cascade) */
h1 {
    font-size: 2rem;         /* 32px */
}

h2 {
    font-size: 1.5rem;       /* 24px */
}

p {
    font-size: 1rem;         /* 16px */
    line-height: 1.5;        /* 1.5 × taille police (sans unité) */
}
```

**EM vs REM :**

```css
/* EM : Relatif au parent */
html { font-size: 16px; }
body { font-size: 20px; }    /* Parent */
p { font-size: 1.5em; }      /* 1.5 × 20px = 30px */

/* REM : Relatif à html (root) */
html { font-size: 16px; }
body { font-size: 20px; }    /* Ignoré pour rem */
p { font-size: 1.5rem; }     /* 1.5 × 16px = 24px (TOUJOURS) */
```

### 5.3 Pourcentage (%)

```css
/* Pourcentage : Relatif au PARENT */

/* Largeur */
.container {
    width: 1200px;           /* Parent */
}

.sidebar {
    width: 25%;              /* 25% de 1200px = 300px */
}

.content {
    width: 75%;              /* 75% de 1200px = 900px */
}

/* Hauteur (parent doit avoir hauteur définie) */
.parent {
    height: 500px;
}

.child {
    height: 50%;             /* 50% de 500px = 250px */
}

/* Font-size */
body {
    font-size: 16px;
}

h1 {
    font-size: 200%;         /* 200% de 16px = 32px */
}

/* Padding/Margin : % de la LARGEUR du parent */
.box {
    width: 500px;
}

.element {
    padding: 10%;            /* 10% de 500px = 50px (même vertical) */
    margin-left: 25%;        /* 25% de 500px = 125px */
}
```

### 5.4 Unités Viewport (vw, vh, vmin, vmax)

```css
/* VW : 1% de la largeur du viewport */
.full-width {
    width: 100vw;            /* 100% largeur écran */
}

.half-width {
    width: 50vw;             /* 50% largeur écran */
}

/* VH : 1% de la hauteur du viewport */
.hero {
    height: 100vh;           /* Plein écran vertical */
    background-color: #3498db;
}

.section {
    height: 50vh;            /* Moitié hauteur écran */
}

/* Hero section plein écran */
.hero-section {
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Font responsive avec vw */
h1 {
    font-size: 5vw;          /* S'adapte à la largeur écran */
    /* ⚠️ Limiter avec min/max */
    font-size: clamp(24px, 5vw, 72px);
}

/* VMIN : Plus petit entre vw et vh */
.square {
    width: 50vmin;           /* 50% du plus petit côté */
    height: 50vmin;          /* Toujours carré */
}

/* VMAX : Plus grand entre vw et vh */
.diagonal {
    width: 100vmax;          /* 100% du plus grand côté */
}
```

**Comparaison unités viewport :**

```
Écran 1920×1080 (desktop) :
1vw = 19.2px  (1% de 1920px)
1vh = 10.8px  (1% de 1080px)

Écran 375×667 (mobile) :
1vw = 3.75px  (1% de 375px)
1vh = 6.67px  (1% de 667px)
```

### 5.5 Tableau Récapitulatif Unités

| Unité | Type | Relatif à | Usage | Exemple |
|-------|------|-----------|-------|---------|
| `px` | Absolue | Écran | Bordures, détails fixes | `border: 1px` |
| `em` | Relative | Taille police parent | Espacement local | `margin: 1em` |
| `rem` | Relative | Taille police root (html) | Tout (préféré) | `font-size: 1.5rem` |
| `%` | Relative | Parent | Largeurs responsive | `width: 50%` |
| `vw` | Relative | Largeur viewport | Layouts responsive | `width: 80vw` |
| `vh` | Relative | Hauteur viewport | Hero sections | `height: 100vh` |
| `vmin` | Relative | Plus petit côté | Éléments carrés | `width: 50vmin` |
| `vmax` | Relative | Plus grand côté | Diagonales | `width: 100vmax` |

---

## 6. Propriétés de Base

### 6.1 Couleur et Arrière-plan

```css
/* COLOR : Couleur du texte */
p {
    color: #333;             /* Hex */
    color: rgb(51, 51, 51);  /* RGB */
    color: hsl(0, 0%, 20%);  /* HSL */
}

/* BACKGROUND-COLOR : Couleur fond */
body {
    background-color: #f0f0f0;
}

.box {
    background-color: white;
    color: black;
}

/* BACKGROUND-IMAGE : Image fond */
.hero {
    background-image: url('hero.jpg');
    background-size: cover;        /* Couvre tout */
    background-position: center;   /* Centré */
    background-repeat: no-repeat;  /* Pas de répétition */
}

/* Dégradé linéaire */
.gradient {
    background: linear-gradient(to right, #3498db, #2ecc71);
}

/* Dégradé radial */
.gradient-radial {
    background: radial-gradient(circle, #3498db, #2ecc71);
}

/* Couleur + Image */
.overlay {
    background-color: rgba(0, 0, 0, 0.5); /* Noir transparent */
    background-image: url('pattern.png');
    background-blend-mode: multiply;       /* Mélange */
}
```

### 6.2 Typographie

```css
/* FONT-FAMILY : Police de caractères */
body {
    font-family: Arial, Helvetica, sans-serif;
    /* ↑ Liste de secours (si Arial absent, Helvetica, sinon sans-serif générique) */
}

h1 {
    font-family: 'Georgia', 'Times New Roman', serif;
}

code {
    font-family: 'Courier New', Courier, monospace;
}

/* FONT-SIZE : Taille police */
h1 {
    font-size: 32px;
    font-size: 2rem;         /* Préféré */
}

p {
    font-size: 16px;
    font-size: 1rem;
}

small {
    font-size: 14px;
    font-size: 0.875rem;
}

/* FONT-WEIGHT : Graisse police */
p {
    font-weight: normal;     /* 400 */
    font-weight: bold;       /* 700 */
    font-weight: 300;        /* Light */
    font-weight: 600;        /* Semi-bold */
    font-weight: 900;        /* Black */
}

/* FONT-STYLE : Style police */
em {
    font-style: italic;      /* Italique */
}

.normal {
    font-style: normal;      /* Normal */
}

/* TEXT-ALIGN : Alignement texte */
h1 {
    text-align: center;      /* Centré */
}

p {
    text-align: left;        /* Gauche (défaut) */
    text-align: right;       /* Droite */
    text-align: justify;     /* Justifié */
}

/* TEXT-DECORATION : Décoration texte */
a {
    text-decoration: none;             /* Pas de soulignement */
    text-decoration: underline;        /* Souligné */
    text-decoration: line-through;     /* Barré */
    text-decoration: overline;         /* Ligne au-dessus */
}

/* TEXT-TRANSFORM : Transformation casse */
.uppercase {
    text-transform: uppercase;   /* MAJUSCULES */
}

.lowercase {
    text-transform: lowercase;   /* minuscules */
}

.capitalize {
    text-transform: capitalize;  /* Première Lettre Majuscule */
}

/* LINE-HEIGHT : Hauteur de ligne (interligne) */
p {
    line-height: 1.6;            /* 1.6 × taille police (sans unité recommandé) */
    line-height: 24px;           /* Fixe en pixels */
}

/* LETTER-SPACING : Espacement lettres */
h1 {
    letter-spacing: 2px;         /* Aéré */
    letter-spacing: -1px;        /* Condensé */
}

/* WORD-SPACING : Espacement mots */
p {
    word-spacing: 5px;
}
```

### 6.3 Marges et Espacement (Aperçu)

```css
/* MARGIN : Marge externe (espace autour élément) */
.box {
    margin: 20px;                /* Tous côtés */
    margin: 10px 20px;           /* Vertical | Horizontal */
    margin: 10px 20px 30px 40px; /* Haut Droite Bas Gauche (sens horaire) */
    
    margin-top: 10px;
    margin-right: 20px;
    margin-bottom: 30px;
    margin-left: 40px;
}

/* PADDING : Espacement interne (espace dans élément) */
.button {
    padding: 10px 20px;          /* Vertical Horizontal */
    padding: 15px;               /* Tous côtés */
    
    padding-top: 10px;
    padding-right: 20px;
    padding-bottom: 10px;
    padding-left: 20px;
}

/* WIDTH et HEIGHT : Largeur et hauteur */
.container {
    width: 800px;
    width: 80%;
    width: 80vw;
    max-width: 1200px;           /* Largeur max */
    min-width: 320px;            /* Largeur min */
    
    height: 500px;
    height: 100vh;
    max-height: 800px;
    min-height: 200px;
}
```

---

## 7. Cascade et Spécificité (Introduction)

### 7.1 La Cascade CSS

```css
/* CSS = Cascading Style Sheets (Feuilles de Style EN CASCADE) */
/* Plusieurs règles peuvent s'appliquer au même élément */
/* L'ordre compte ! */

/* Exemple cascade */
p {
    color: blue;             /* Règle 1 */
}

p {
    color: red;              /* Règle 2 : GAGNE (plus récente) */
    font-size: 16px;
}

/* Résultat : paragraphe ROUGE 16px */

/* Cascade avec spécificité */
p {
    color: blue;             /* Spécificité : 1 */
}

.texte {
    color: red;              /* Spécificité : 10 (plus fort) */
}

/* HTML : <p class="texte"> */
/* Résultat : paragraphe ROUGE (classe gagne sur élément) */
```

### 7.2 Spécificité (Poids des Sélecteurs)

```css
/* Spécificité = Poids du sélecteur */
/* Plus spécifique = Plus prioritaire */

/* Hiérarchie spécificité (du plus faible au plus fort) */

/* 1. Sélecteur élément : 1 point */
p {
    color: blue;
}

/* 2. Sélecteur classe : 10 points */
.texte {
    color: red;              /* Gagne sur élément */
}

/* 3. Sélecteur ID : 100 points */
#titre {
    color: green;            /* Gagne sur classe */
}

/* 4. Inline style : 1000 points */
/* <p style="color: purple;"> */
/* Gagne sur tout (sauf !important) */

/* 5. !important : 10000 points (éviter !) */
p {
    color: orange !important; /* Gagne sur tout */
}

/* Calcul spécificité complexe */
/* Format : (inline, IDs, classes, éléments) */

p {                          /* (0, 0, 0, 1) = 1 */
    color: blue;
}

.container p {               /* (0, 0, 1, 1) = 11 */
    color: red;
}

#header .container p {       /* (0, 1, 1, 1) = 111 */
    color: green;            /* ← GAGNE */
}

/* Exemple HTML */
/* <div id="header">
       <div class="container">
           <p>Texte</p>
       </div>
   </div> */
/* Résultat : texte VERT */
```

**Règles de spécificité :**

| Sélecteur | Spécificité | Exemple |
|-----------|-------------|---------|
| Élément | 1 | `p`, `h1`, `div` |
| Classe | 10 | `.button`, `.text` |
| ID | 100 | `#header`, `#main` |
| Inline | 1000 | `<p style="...">` |
| !important | 10000 | `color: red !important` |

### 7.3 Héritage

```css
/* Certaines propriétés CSS sont HÉRITÉES du parent */

body {
    color: #333;             /* Hérité par TOUS les éléments */
    font-family: Arial;      /* Hérité */
    font-size: 16px;         /* Hérité */
}

/* Tous les éléments dans body héritent ces propriétés */

/* Propriétés HÉRITÉES (principalement typographie) */
/* - color */
/* - font-family */
/* - font-size */
/* - font-weight */
/* - line-height */
/* - text-align */

/* Propriétés NON HÉRITÉES (principalement layout) */
/* - margin */
/* - padding */
/* - border */
/* - width */
/* - height */
/* - background */

/* Exemple héritage */
div {
    color: blue;             /* Hérité par enfants */
    border: 1px solid black; /* PAS hérité */
}

/* HTML : <div><p>Texte</p></div> */
/* <p> sera BLEU (hérité) mais sans bordure */

/* Forcer l'héritage */
.element {
    border: inherit;         /* Hérite bordure du parent */
}

/* Réinitialiser héritage */
.element {
    color: initial;          /* Valeur initiale navigateur */
    all: unset;              /* Reset toutes propriétés */
}
```

---

## 8. Exercices Pratiques

### Exercice 1 : Styliser une Page Simple

**Objectif :** Appliquer les bases CSS.

**Consigne :** Créer une page HTML et CSS avec :
- Body : fond gris clair, police Arial
- h1 : couleur bleu foncé, taille 36px, centré
- p : couleur gris foncé, taille 16px, interligne 1.6
- Liens : bleu, pas de soulignement, souligné au survol

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ma Première Page Stylée</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Bienvenue sur mon site</h1>
    <p>
        Ceci est mon premier site web avec CSS. Le CSS (Cascading Style Sheets) 
        permet de styliser les pages HTML et de les rendre plus attractives.
    </p>
    <p>
        Visitez <a href="https://www.mozilla.org/fr/firefox/">Mozilla Firefox</a> 
        pour en savoir plus sur le développement web.
    </p>
</body>
</html>
```

```css
/* style.css */

/* Reset de base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Body */
body {
    font-family: Arial, Helvetica, sans-serif;
    background-color: #f5f5f5;
    padding: 40px 20px;
}

/* Titre principal */
h1 {
    color: #2c3e50;
    font-size: 36px;
    text-align: center;
    margin-bottom: 30px;
}

/* Paragraphes */
p {
    color: #34495e;
    font-size: 16px;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto 20px;
}

/* Liens */
a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
```

</details>

### Exercice 2 : Palette de Couleurs

**Objectif :** Maîtriser les formats de couleurs.

**Consigne :** Créer une page avec 3 sections :
- Section 1 : Fond hex, texte rgba
- Section 2 : Fond rgb, texte hsl
- Section 3 : Fond hsla transparent, texte hex

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Palette de Couleurs</title>
    <link rel="stylesheet" href="colors.css">
</head>
<body>
    <section class="section-1">
        <h2>Section 1 : Hex & RGBA</h2>
        <p>
            Fond en hexadécimal (#3498db) et texte en RGBA 
            pour démontrer les différents formats de couleurs CSS.
        </p>
    </section>
    
    <section class="section-2">
        <h2>Section 2 : RGB & HSL</h2>
        <p>
            Fond en RGB (46, 204, 113) et texte en HSL 
            pour une approche plus intuitive des couleurs.
        </p>
    </section>
    
    <section class="section-3">
        <h2>Section 3 : HSLA transparent</h2>
        <p>
            Fond semi-transparent en HSLA permettant de voir 
            l'arrière-plan à travers la section.
        </p>
    </section>
</body>
</html>
```

```css
/* colors.css */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 40px 20px;
}

section {
    max-width: 800px;
    margin: 0 auto 30px;
    padding: 40px;
    border-radius: 10px;
}

h2 {
    margin-bottom: 15px;
    font-size: 28px;
}

p {
    font-size: 16px;
    line-height: 1.6;
}

/* Section 1 : Hex + RGBA */
.section-1 {
    background-color: #3498db;           /* Hex */
    color: rgba(255, 255, 255, 0.95);    /* RGBA */
}

/* Section 2 : RGB + HSL */
.section-2 {
    background-color: rgb(46, 204, 113); /* RGB */
    color: hsl(220, 13%, 18%);           /* HSL */
}

/* Section 3 : HSLA transparent + Hex */
.section-3 {
    background-color: hsla(280, 80%, 60%, 0.7); /* HSLA semi-transparent */
    color: #FFFFFF;                              /* Hex */
    border: 2px solid white;
}
```

</details>

### Exercice 3 : Unités Responsive

**Objectif :** Utiliser différentes unités CSS.

**Consigne :** Créer une page avec :
- Hero section : hauteur 100vh
- Conteneur : largeur 80vw, max 1200px
- Titres : tailles en rem
- Espacements : mix em, rem, px

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unités Responsive</title>
    <link rel="stylesheet" href="units.css">
</head>
<body>
    <section class="hero">
        <div class="hero-content">
            <h1>Unités CSS Responsive</h1>
            <p>Découvrez la puissance des unités relatives</p>
        </div>
    </section>
    
    <main class="container">
        <article>
            <h2>Pourquoi utiliser des unités relatives ?</h2>
            <p>
                Les unités relatives comme rem, em, vw et vh permettent 
                de créer des designs qui s'adaptent automatiquement à 
                différentes tailles d'écran et préférences utilisateur.
            </p>
            
            <h3>Unités viewport</h3>
            <p>
                Les unités vw (viewport width) et vh (viewport height) 
                sont particulièrement utiles pour les sections plein écran 
                et les éléments qui doivent s'adapter à la taille du navigateur.
            </p>
            
            <h3>Unités em et rem</h3>
            <p>
                Rem est relatif à la taille de police root (html), 
                tandis que em est relatif au parent. Rem est généralement 
                préféré pour éviter l'effet cascade.
            </p>
        </article>
    </main>
</body>
</html>
```

```css
/* units.css */

/* Reset et base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 16px;  /* Base pour rem */
}

body {
    font-family: Arial, sans-serif;
    color: #333;
    line-height: 1.6;
}

/* Hero section : 100vh */
.hero {
    height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    text-align: center;
}

.hero-content h1 {
    font-size: 3rem;      /* 48px (3 × 16px) */
    margin-bottom: 1rem;  /* 16px */
}

.hero-content p {
    font-size: 1.25rem;   /* 20px */
}

/* Container : 80vw max 1200px */
.container {
    width: 80vw;
    max-width: 1200px;
    margin: 4rem auto;    /* 64px haut/bas, centré */
    padding: 0 2rem;      /* 32px gauche/droite */
}

/* Article */
article {
    background-color: white;
    padding: 3rem;        /* 48px */
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Titres en rem */
h2 {
    font-size: 2rem;      /* 32px */
    margin-bottom: 1.5rem; /* 24px */
    color: #2c3e50;
}

h3 {
    font-size: 1.5rem;    /* 24px */
    margin-top: 2rem;     /* 32px */
    margin-bottom: 1rem;  /* 16px */
    color: #34495e;
}

/* Paragraphes */
p {
    font-size: 1rem;      /* 16px */
    margin-bottom: 1em;   /* 1em = 16px (taille police de p) */
    text-align: justify;
}
```

</details>

---

## 9. Projet du Module : Page Portfolio Simple

### 9.1 Cahier des Charges

**Créer une page portfolio avec CSS complet :**

**Spécifications techniques :**
- ✅ Hero section plein écran (100vh)
- ✅ Section À propos avec photo
- ✅ Section Compétences (3 cartes)
- ✅ Section Contact
- ✅ Palette de couleurs cohérente
- ✅ Typographie harmonieuse (rem)
- ✅ Responsive (unités relatives)
- ✅ CSS externe séparé
- ✅ Code validé W3C

### 9.2 Solution Complète

<details>
<summary>Voir la solution complète du projet</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alice Dupont - Développeuse Web</title>
    <link rel="stylesheet" href="portfolio.css">
</head>
<body>
    <header class="hero">
        <div class="hero-content">
            <h1>Alice Dupont</h1>
            <p class="subtitle">Développeuse Web Frontend</p>
            <p class="description">
                Passionnée par la création d'interfaces web modernes et accessibles
            </p>
            <a href="#contact" class="cta-button">Me contacter</a>
        </div>
    </header>
    
    <main>
        <section class="about" id="about">
            <div class="container">
                <h2>À propos</h2>
                <div class="about-content">
                    <div class="about-text">
                        <p>
                            Bonjour ! Je suis Alice, développeuse web frontend avec 5 ans d'expérience 
                            dans la création d'applications web modernes et performantes.
                        </p>
                        <p>
                            Je maîtrise HTML5, CSS3, JavaScript et les frameworks modernes comme 
                            React et Vue.js. Mon objectif est de créer des expériences utilisateur 
                            exceptionnelles tout en respectant les standards d'accessibilité et de performance.
                        </p>
                        <p>
                            Quand je ne code pas, j'aime contribuer à des projets open source 
                            et partager mes connaissances à travers des articles de blog.
                        </p>
                    </div>
                </div>
            </div>
        </section>
        
        <section class="skills" id="skills">
            <div class="container">
                <h2>Compétences</h2>
                <div class="skills-grid">
                    <div class="skill-card">
                        <h3>Frontend</h3>
                        <ul>
                            <li>HTML5 & CSS3</li>
                            <li>JavaScript (ES6+)</li>
                            <li>React & Vue.js</li>
                            <li>Responsive Design</li>
                            <li>Accessibilité (WCAG)</li>
                        </ul>
                    </div>
                    
                    <div class="skill-card">
                        <h3>Outils</h3>
                        <ul>
                            <li>Git & GitHub</li>
                            <li>VS Code</li>
                            <li>Webpack & Vite</li>
                            <li>Figma</li>
                            <li>DevTools</li>
                        </ul>
                    </div>
                    
                    <div class="skill-card">
                        <h3>Méthodologies</h3>
                        <ul>
                            <li>Agile / Scrum</li>
                            <li>Mobile First</li>
                            <li>Performance Web</li>
                            <li>SEO</li>
                            <li>Tests (Jest, Vitest)</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
        
        <section class="contact" id="contact">
            <div class="container">
                <h2>Contact</h2>
                <p class="contact-intro">
                    Vous avez un projet ou souhaitez discuter ? N'hésitez pas à me contacter !
                </p>
                <div class="contact-links">
                    <a href="mailto:alice@example.com" class="contact-link">
                        Email : alice@example.com
                    </a>
                    <a href="tel:+33612345678" class="contact-link">
                        Téléphone : 06 12 34 56 78
                    </a>
                    <a href="https://github.com/alice" class="contact-link">
                        GitHub : @alice
                    </a>
                    <a href="https://linkedin.com/in/alice" class="contact-link">
                        LinkedIn : Alice Dupont
                    </a>
                </div>
            </div>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; 2024 Alice Dupont. Tous droits réservés.</p>
        </div>
    </footer>
</body>
</html>
```

```css
/* portfolio.css */

/* ========================================
   RESET & BASE
   ======================================== */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 16px;
    scroll-behavior: smooth;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

/* ========================================
   TYPOGRAPHIE
   ======================================== */

h1 {
    font-size: 3rem;        /* 48px */
    font-weight: 700;
    margin-bottom: 1rem;
}

h2 {
    font-size: 2.5rem;      /* 40px */
    font-weight: 600;
    margin-bottom: 2rem;
    text-align: center;
    color: #2c3e50;
}

h3 {
    font-size: 1.5rem;      /* 24px */
    font-weight: 600;
    margin-bottom: 1rem;
    color: #34495e;
}

p {
    font-size: 1rem;        /* 16px */
    margin-bottom: 1rem;
}

/* ========================================
   LAYOUT
   ======================================== */

.container {
    width: 90vw;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

section {
    padding: 5rem 0;
}

/* ========================================
   HERO SECTION
   ======================================== */

.hero {
    height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.hero-content {
    max-width: 800px;
    padding: 2rem;
}

.subtitle {
    font-size: 1.5rem;      /* 24px */
    font-weight: 300;
    margin-bottom: 1.5rem;
    opacity: 0.95;
}

.description {
    font-size: 1.125rem;    /* 18px */
    margin-bottom: 2rem;
    opacity: 0.9;
}

.cta-button {
    display: inline-block;
    padding: 1rem 2.5rem;
    background-color: white;
    color: #667eea;
    text-decoration: none;
    font-size: 1.125rem;
    font-weight: 600;
    border-radius: 50px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

/* ========================================
   ABOUT SECTION
   ======================================== */

.about {
    background-color: white;
}

.about-content {
    max-width: 800px;
    margin: 0 auto;
}

.about-text p {
    font-size: 1.125rem;    /* 18px */
    color: #555;
    text-align: justify;
    margin-bottom: 1.5rem;
}

/* ========================================
   SKILLS SECTION
   ======================================== */

.skills {
    background-color: #f8f9fa;
}

.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}

.skill-card {
    background-color: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.skill-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.skill-card h3 {
    color: #667eea;
    margin-bottom: 1.5rem;
}

.skill-card ul {
    list-style: none;
}

.skill-card li {
    padding: 0.5rem 0;
    color: #555;
    border-bottom: 1px solid #e9ecef;
}

.skill-card li:last-child {
    border-bottom: none;
}

.skill-card li::before {
    content: "✓ ";
    color: #667eea;
    font-weight: bold;
    margin-right: 0.5rem;
}

/* ========================================
   CONTACT SECTION
   ======================================== */

.contact {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.contact h2 {
    color: white;
}

.contact-intro {
    text-align: center;
    font-size: 1.25rem;
    margin-bottom: 3rem;
    opacity: 0.95;
}

.contact-links {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    max-width: 600px;
    margin: 0 auto;
}

.contact-link {
    display: block;
    padding: 1.5rem;
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    text-decoration: none;
    text-align: center;
    border-radius: 10px;
    font-size: 1.125rem;
    transition: background-color 0.3s ease, transform 0.3s ease;
    border: 2px solid rgba(255, 255, 255, 0.2);
}

.contact-link:hover {
    background-color: rgba(255, 255, 255, 0.2);
    transform: translateX(5px);
}

/* ========================================
   FOOTER
   ======================================== */

footer {
    background-color: #2c3e50;
    color: white;
    padding: 2rem 0;
    text-align: center;
}

footer p {
    margin: 0;
    opacity: 0.8;
}
```

</details>

### 9.3 Checklist de Validation

Avant de considérer votre projet terminé, vérifiez :

- [ ] CSS externe séparé (portfolio.css)
- [ ] Hero section 100vh avec dégradé
- [ ] Palette de couleurs cohérente (3-4 couleurs)
- [ ] Typographie en rem (h1: 3rem, h2: 2.5rem, h3: 1.5rem, p: 1rem)
- [ ] Container responsive (90vw max 1200px)
- [ ] Grid pour compétences (3 cartes)
- [ ] Cartes avec hover effect (transform, box-shadow)
- [ ] Section contact avec liens stylés
- [ ] Footer avec copyright
- [ ] Commentaires CSS organisés (sections)
- [ ] Code indenté proprement
- [ ] Validé W3C (HTML + CSS)

---

## 10. Best Practices CSS

### 10.1 Organisation du Code

```css
/* ✅ BON : Organisation claire */

/* ========================================
   TABLE DES MATIÈRES
   1. Reset & Base
   2. Typographie
   3. Layout
   4. Components
   5. Utilities
   ======================================== */

/* 1. Reset & Base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 16px;
}

/* 2. Typographie */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}

h1 { font-size: 3rem; }
h2 { font-size: 2.5rem; }

/* 3. Layout */
.container {
    max-width: 1200px;
    margin: 0 auto;
}

/* 4. Components */
.button {
    padding: 10px 20px;
    background-color: blue;
}

/* 5. Utilities */
.text-center { text-align: center; }
```

### 10.2 Nommage et Convention

```css
/* BEM (Block Element Modifier) - Recommandé */

/* Block */
.card { }

/* Element (enfant du block) */
.card__title { }
.card__content { }
.card__button { }

/* Modifier (variation du block ou element) */
.card--featured { }
.card__button--primary { }
.card__button--disabled { }

/* Exemple concret */
.product-card { }
.product-card__image { }
.product-card__title { }
.product-card__price { }
.product-card__button { }
.product-card--sale { }
.product-card__button--buy-now { }
```

### 10.3 Performance et Maintenance

```css
/* ✅ BON : Préférer classes aux IDs */
.header { }        /* Réutilisable */
#header { }        /* ❌ Spécificité trop forte, pas réutilisable */

/* ✅ BON : Éviter sélecteurs trop profonds */
.card .content { } /* 2 niveaux OK */

/* ❌ MAUVAIS : Cascade trop profonde */
.page .container .sidebar .widget .title { } /* Trop spécifique */

/* ✅ BON : Regrouper propriétés similaires */
.button {
    /* Positionnement */
    display: inline-block;
    position: relative;
    
    /* Box model */
    padding: 10px 20px;
    margin: 10px;
    
    /* Typographie */
    font-size: 16px;
    color: white;
    
    /* Visuel */
    background-color: blue;
    border-radius: 5px;
    
    /* Autres */
    cursor: pointer;
    transition: all 0.3s ease;
}

/* ✅ BON : Utiliser rem pour typographie */
html {
    font-size: 16px; /* Base */
}

h1 {
    font-size: 2rem; /* 32px */
}

/* ❌ ÉVITER : !important (sauf cas extrême) */
.text {
    color: red !important; /* Éviter */
}
```

---

## 11. Checkpoint de Progression

### À la fin de ce Module 7, vous maîtrisez :

**Fondations CSS :**

- [x] Qu'est-ce que CSS (définition, histoire, rôle)
- [x] Séparation contenu/présentation
- [x] CSS vs HTML (responsabilités)

**Intégration CSS :**

- [x] CSS inline (dans balise)
- [x] CSS internal (balise `<style>`)
- [x] CSS external (fichier séparé) ⭐
- [x] Multiples feuilles CSS

**Syntaxe CSS :**

- [x] Anatomie règle CSS (sélecteur, propriété, valeur)
- [x] Commentaires CSS
- [x] Regroupement sélecteurs

**Couleurs :**

- [x] Noms de couleurs (140 prédéfinis)
- [x] Hexadécimal (#RRGGBB)
- [x] RGB et RGBA (transparence)
- [x] HSL et HSLA (teinte, saturation, luminosité)

**Unités :**

- [x] Absolues (px, pt, cm)
- [x] Relatives (em, rem, %)
- [x] Viewport (vw, vh, vmin, vmax)
- [x] Quand utiliser chaque unité

**Propriétés de base :**

- [x] Couleurs (color, background-color)
- [x] Typographie (font-family, font-size, font-weight, text-align)
- [x] Espacement (margin, padding, width, height)

**Concepts avancés :**

- [x] Cascade CSS
- [x] Spécificité (1, 10, 100, 1000)
- [x] Héritage

**Best practices :**

- [x] Organisation code
- [x] Nommage (BEM)
- [x] Performance

### Prochaine Étape

**Direction le Module 8** où vous allez :

- Maîtriser tous les sélecteurs CSS
- Sélecteurs d'éléments, classes, IDs
- Sélecteurs d'attributs
- Pseudo-classes (:hover, :focus, :nth-child)
- Pseudo-éléments (::before, ::after)
- Combinateurs (descendant, enfant, adjacent)
- Ciblage précis des éléments

---

**Module 7 Terminé - Bravo ! 🎉 🎨**

**Vous avez appris :**

- ✅ Fondations CSS (définition, histoire, rôle)
- ✅ 3 méthodes d'intégration CSS (inline, internal, external)
- ✅ Syntaxe CSS complète (règle, déclaration, commentaires)
- ✅ 4 formats de couleurs (noms, hex, rgb/rgba, hsl/hsla)
- ✅ 8+ unités CSS (px, em, rem, %, vw, vh, vmin, vmax)
- ✅ 20+ propriétés de base maîtrisées
- ✅ Cascade, spécificité, héritage
- ✅ Best practices CSS professionnelles

**Statistiques Module 7 :**

- 1 projet complet (Portfolio simple)
- 3 exercices progressifs avec solutions
- 100+ exemples de code
- Fondations CSS solides

**Prochain objectif : Maîtriser les sélecteurs CSS (Module 8)**

**Félicitations pour avoir posé les bases du CSS ! 🚀🎨**
