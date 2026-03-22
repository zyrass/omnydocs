---
description: "Phase 3 : Conception de la bannière d'accueil, positionnement en Absolute, et typographie d'impact."
icon: lucide/image
tags: ["CSS", "HERO", "BACKGROUND", "ABSOLUTE"]
status: stable
---

# Phase 3 : Accueil & Hero Banner

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="1h00">
</div>

!!! quote "Le Défi du Client"
    "Les visiteurs décident en 3 secondes s'ils restent ou non sur notre site. Je veux une image pleine largeur de Vancouver en arrière-plan, sombre, avec notre phrase d'accroche en gros blanc éclatant au centre de l'écran. Et un bouton Call To Action."

La section **Hero** est la zone critique d'un `index.html`. Elle est visuellement écrasante (`height: 100vh`) et impose souvent des défis de lisibilité à cause des photographies d'arrière-plan complexes.

## 1. La Sémantique Principale

Dans votre fichier `index.html`, après avoir fermé la balise `</header>`, nous allons enfin entrer dans le `<main>` du site, son contenu principal.

```html
<main class="content">

  <!-- La bannière hero plein écran -->
  <section class="hero" id="home">
    <div class="hero-content">
      <h1>Nous Forgeons Vos Idées Digitales</h1>
      <p>L'agence web spécialisée dans l'architecture sur-mesure pour les pure players.</p>
      
      <!-- Notre bouton réutilisable -->
      <a href="#services" class="btn btn-primary">Découvrir nos services</a>
    </div>
  </section>

</main>
```

Le `<main>` est unique sur une page HTML5. Il dit au moteur Google : "Le vrai contenu démarre ici". 
Le code interne est ultra-léger : un titre profond (`h1`), un paragraphe (`p`), et un bouton ancré (`a.btn`).

## 2. L'Arrière-Plan (Background Image)

Ouvrez `style.css`. La section `.hero` ne contiendra pas d'image `<img>` dans le code HTML. Nous allons utiliser la propriété logicielle `background-image` de la balise section parce que *l'image est purement décorative* (inutile pour le sens du texte).

```css
/* --- HERO BANNER --- */
.hero {
  /* On génère une hauteur écran moins le Header collant */
  min-height: calc(100vh - 70px); 
  
  /* L'image décorative depuis le web (ou de votre dossier assets) */
  background-image: url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1920&q=80');
  background-size: cover; /* Ne jamais déformer = cover */
  background-position: center; /* Centrer la zone focusée */
  background-repeat: no-repeat;
  
  /* Flexbox magique pour centrer les éléments enfants en 1D ! */
  display: flex;
  align-items: center; /* Axe secondaire (Vertical) */
  justify-content: center; /* Axe principal (Horizontal) */
  
  position: relative; /* Prépare le terrain pour le filtre noir */
}
```

!!! note "L'enfer de la lisibilité"
    Si vous regardez votre résultat, le texte "Nous Forgeons..." noir sur l'image d'ordinateur ou de ville est illisible. La solution "rapide" est de modifier l'image dans Photoshop. La solution d'ingénieur est de générer un filtre (`overlay`) directement en CSS pour assombrir dynamiquement n'importe quelle photo fournie par le client.

## 3. L'Overlay Noir et la Position Relative / Absolue

C'est ici que l'on manipule la profondeur de l'écran (L'axe Z). On va utiliser une "pseudo-racine" invisible CSS `::before` pour peindre un carré de noir transparent par-dessus l'arrière plan, mais **sous** le texte.

```css
/* Le filtre sombre CSS en position absolue */
.hero::before {
  content: "";       /* Obligatoire pour exister ! */
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.6); /* Noir à 60% d'opacité */
  z-index: 1; /* Il passe par-dessus le background */
}

/* Le contenu texte DOIT repasser devant ! */
.hero-content {
  position: relative; /* Reprend la main sur le flux */
  z-index: 2; /* S'affiche devant le filtre sombre */
  
  text-align: center;
  color: var(--color-light); /* Texte blanc ! */
  max-width: 800px;
  padding: var(--spacing-lg);
}
```

## 4. Le Design "Composant" du Bouton

Remarquez la double classe dans le HTML : `class="btn btn-primary"`. C'est l'essence du frameworking (comme Bootstrap/Tailwind). Vous codez un socle dur (`.btn`), et un variant modificateur de couleur (`.btn-primary`).

```css
/* La carcasse de tout un bouton */
.btn {
  display: inline-block; /* Pour accepter padding et width ! */
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: transform 0.2s, background-color 0.2s;
  cursor: pointer;
  border: 2px solid transparent;
}

/* LE design du Bouton principal Bleu Electrique */
.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-light);
}

.btn-primary:hover {
  background-color: var(--color-dark); /* Survol assombri */
  transform: translateY(-3px); /* Lévite très légèrement */
}
```

## Checklist de la Phase 3

- [ ] L'image charge bien (il pleut ou il y a du code).
- [ ] Le texte n'est plus mangé visuellement grâce à l'overlay translucide de `.hero::before`.
- [ ] Le bouton `Découvrir nos services` a bien sa couleur d'origine HSL (Variable).
- [ ] Le `a.btn` lévite très légèrement au passage de votre souris.
- [ ] Sur un téléphone (F12 Inspecteur), le titre H1 rétrécit harmonieusement s'il a été bien déclaré (N'hésitez pas à rajouter un media query pour abaisser son `font-size` si nécessaire !).

La section Accueil est spectaculaire. Passons au vrai défi de la structuration complexe native : la construction de la **Grille des services**.

[Passer à la Phase 4 : Cartes & CSS Grids →](phase4.md)
