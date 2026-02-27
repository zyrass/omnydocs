---
description: "Maîtriser HTML5 & CSS3 : Portfolio Professionnel Responsive avec Tailwind CSS"
icon: fontawesome/brands/html5
tags: ["HTML5", "CSS3", "RESPONSIVE", "FLEXBOX", "GRID", "TAILWIND"]
status: production
---

# HTML5 & CSS3

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="HTML5 & CSS3 Modern"
  data-time="16-18 heures">
</div>

## Introduction au Projet Portfolio Professionnel Responsive

!!! quote "Analogie pédagogique"
    _Imaginez construire une maison **sans connaître la maçonnerie** : vous embaucheriez des ouvriers sans comprendre leurs techniques, impossible de diagnostiquer un problème ou proposer des améliorations. **HTML/CSS sont les fondations du web** : HTML = structure (murs, pièces), CSS = décoration (peinture, agencement). Les frameworks comme Bootstrap/Tailwind sont des **kits préfabriqués** qui accélèrent la construction, mais sans maîtriser HTML/CSS pur, vous ne comprenez pas ce qu'ils font. Un `<div class="flex justify-center">` Tailwind cache `display: flex; justify-content: center;` CSS. Ce guide vous enseigne les fondamentaux pour comprendre TOUS les frameworks._

> Ce guide vous accompagne dans la création d'un **Portfolio Professionnel** complet en HTML5 et CSS3 moderne. Vous construirez un site responsive avec Hero section animée, compteurs dynamiques, galerie projets filtrée, testimonials carrousel, formulaire contact, smooth scroll, et animations CSS. CHAQUE propriété CSS sera expliquée en détail (pourquoi, comment, quand). Puis vous refactoriserez le tout avec Tailwind CSS pour comprendre la différence. Ce guide couvre TOUS les fondamentaux HTML/CSS ET les dernières nouveautés CSS 2024-2025.

!!! info "Pourquoi ce projet ?"
    - **Projet concret** : Portfolio utilisable réellement
    - **Responsive design** : Mobile-first approach
    - **CSS moderne** : Grid, Flexbox, Variables, Animations
    - **Explications exhaustives** : CHAQUE ligne commentée
    - **Tailwind CSS** : Comparaison CSS pur vs framework
    - **Dernières nouveautés** : Container queries, :has(), accent-color

### Objectifs Pédagogiques

À la fin de ce guide, vous saurez :

- ✅ HTML5 sémantique complet
- ✅ CSS Box Model (margin, padding, border)
- ✅ Flexbox maîtrisé (justify, align, wrap)
- ✅ Grid Layout complet (template, areas)
- ✅ Responsive design (media queries, mobile-first)
- ✅ Variables CSS (custom properties)
- ✅ Animations & Transitions
- ✅ CSS moderne (container queries, :has(), scroll-snap)
- ✅ Tailwind CSS integration

### Aperçu Portfolio Final

```
┌────────────────────────────────────────────────┐
│ 🌟 HERO SECTION (viewport height)            │
│ ───────────────────────────────────────────   │
│    John Doe                                   │
│    Full-Stack Developer                       │
│    [Voir mes projets] [Me contacter]          │
│                                        ↓      │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ 📊 COMPTEURS (animated on scroll)            │
│ ───────────────────────────────────────────   │
│  150+        500+        50+        98%       │
│ Projets     Cafés     Clients   Satisfaction  │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ 💼 CE QUE JE PROPOSE (Grid 3 cols)           │
│ ───────────────────────────────────────────   │
│ [🎨 Design]  [💻 Dev]  [🚀 Deploy]           │
│  Card hover   Card hover  Card hover          │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ 🎨 MES PROJETS (Filtres + Grid)              │
│ ───────────────────────────────────────────   │
│ [Tous] [Web] [Mobile] [Design]               │
│                                               │
│ [Projet 1]  [Projet 2]  [Projet 3]           │
│ [Projet 4]  [Projet 5]  [Projet 6]           │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ 💬 TÉMOIGNAGES (Carrousel)                   │
│ ───────────────────────────────────────────   │
│  " Excellent travail... "                     │
│  - Client Name, CEO Company                   │
│  ● ○ ○ (dots navigation)                     │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ 📧 CONTACT (Form + Infos)                    │
│ ───────────────────────────────────────────   │
│ Formulaire      |    Coordonnées              │
│ [Nom]           |    📧 email@example.com     │
│ [Email]         |    📱 +33 6 12 34 56 78     │
│ [Message]       |    📍 Paris, France          │
│ [Envoyer]       |                             │
└────────────────────────────────────────────────┘
```

### Structure Projet

```
portfolio/
├── index.html
├── css/
│   ├── reset.css          # Normalisation navigateurs
│   ├── variables.css      # Variables CSS
│   ├── base.css           # Styles de base
│   ├── layout.css         # Grid & Flexbox
│   ├── components.css     # Boutons, cards, etc.
│   ├── sections.css       # Hero, About, etc.
│   └── responsive.css     # Media queries
├── css-tailwind/
│   └── styles.css         # Version Tailwind (Phase 8)
├── js/
│   ├── main.js            # Interactions
│   └── filters.js         # Filtres projets
├── assets/
│   ├── images/
│   └── icons/
└── README.md
```

### Phases de Développement

| Phase | Titre | Durée | Concepts |
|-------|-------|-------|----------|
| 1 | HTML5 Sémantique | 2h | Structure, balises, accessibilité |
| 2 | CSS Fondamentaux | 2h | Box model, typography, colors |
| 3 | Flexbox Détaillé | 2h30 | justify, align, wrap, gap |
| 4 | Grid Layout Complet | 2h30 | template, areas, auto-fit |
| 5 | Responsive Design | 2h | Media queries, mobile-first |
| 6 | CSS Moderne & Animations | 2h | Variables, transforms, keyframes |
| 7 | Portfolio Complet | 2h | Assemblage final |
| 8 | Tailwind CSS Refactor | 2h | Comparaison framework |

**Durée totale : 17h**

---

## Phase 1 : HTML5 Sémantique (2h)

<div class="omny-meta" data-level="🟢 Débutant" data-time="2 heures"></div>

### Objectifs Phase 1

- ✅ Comprendre HTML = contenu structuré
- ✅ Balises sémantiques (header, nav, main, section, article)
- ✅ Accessibilité (ARIA, alt, labels)
- ✅ SEO-friendly structure

### 1.1 Pourquoi HTML Sémantique ?

**❌ HTML non sémantique (ancien) :**

```html
<div class="header">
  <div class="nav">
    <div class="menu-item">Accueil</div>
  </div>
</div>
<div class="content">
  <div class="article">...</div>
</div>
```

**✅ HTML5 sémantique (moderne) :**

```html
<header>
  <nav>
    <a href="#home">Accueil</a>
  </nav>
</header>
<main>
  <article>...</article>
</main>
```

**Avantages sémantique :**
- ✅ **SEO** : Google comprend la structure
- ✅ **Accessibilité** : Lecteurs d'écran naviguent mieux
- ✅ **Maintenance** : Code auto-documenté
- ✅ **Standards** : Bonne pratique universelle

### 1.2 Structure HTML Complète

**Fichier :** `index.html`

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <!-- Métadonnées essentielles -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO -->
    <meta name="description" content="Portfolio de John Doe - Développeur Full-Stack spécialisé en PHP, Python et JavaScript">
    <meta name="keywords" content="développeur, full-stack, portfolio, php, python">
    <meta name="author" content="John Doe">
    
    <!-- Open Graph (réseaux sociaux) -->
    <meta property="og:title" content="John Doe - Portfolio">
    <meta property="og:description" content="Découvrez mes projets web">
    <meta property="og:image" content="assets/images/og-image.jpg">
    
    <title>John Doe - Portfolio Professionnel</title>
    
    <!-- CSS -->
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/variables.css">
    <link rel="stylesheet" href="css/base.css">
    <link rel="stylesheet" href="css/layout.css">
    <link rel="stylesheet" href="css/components.css">
    <link rel="stylesheet" href="css/sections.css">
    <link rel="stylesheet" href="css/responsive.css">
</head>
<body>
    
    <!-- Navigation fixe -->
    <nav class="navbar" id="navbar">
        <div class="container">
            <a href="#home" class="logo">JD</a>
            
            <ul class="nav-menu">
                <li><a href="#home">Accueil</a></li>
                <li><a href="#about">À propos</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#portfolio">Portfolio</a></li>
                <li><a href="#testimonials">Témoignages</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
            
            <!-- Menu burger mobile -->
            <button class="burger" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </nav>
    
    <!-- Contenu principal -->
    <main>
        
        <!-- Section Hero -->
        <section id="home" class="hero">
            <div class="container">
                <h1 class="hero-title">
                    Bonjour, je suis <span class="highlight">John Doe</span>
                </h1>
                <p class="hero-subtitle">
                    Développeur Full-Stack passionné par la création d'expériences web exceptionnelles
                </p>
                
                <div class="hero-cta">
                    <a href="#portfolio" class="btn btn-primary">Voir mes projets</a>
                    <a href="#contact" class="btn btn-secondary">Me contacter</a>
                </div>
            </div>
            
            <!-- Scroll indicator -->
            <a href="#stats" class="scroll-indicator" aria-label="Scroll down">
                <span>↓</span>
            </a>
        </section>
        
        <!-- Section Compteurs -->
        <section id="stats" class="stats">
            <div class="container">
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-number" data-target="150">0</span>
                        <span class="stat-label">Projets Réalisés</span>
                    </div>
                    
                    <div class="stat-item">
                        <span class="stat-number" data-target="500">0</span>
                        <span class="stat-label">Cafés Bus</span>
                    </div>
                    
                    <div class="stat-item">
                        <span class="stat-number" data-target="50">0</span>
                        <span class="stat-label">Clients Satisfaits</span>
                    </div>
                    
                    <div class="stat-item">
                        <span class="stat-number" data-target="98">0</span>
                        <span class="stat-label">% Satisfaction</span>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Section Services -->
        <section id="services" class="services">
            <div class="container">
                <h2 class="section-title">Ce que je propose</h2>
                <p class="section-subtitle">
                    Des solutions complètes pour vos projets web
                </p>
                
                <div class="services-grid">
                    <article class="service-card">
                        <div class="service-icon">🎨</div>
                        <h3>Design UI/UX</h3>
                        <p>
                            Création d'interfaces modernes et intuitives 
                            pour une expérience utilisateur optimale.
                        </p>
                    </article>
                    
                    <article class="service-card">
                        <div class="service-icon">💻</div>
                        <h3>Développement Web</h3>
                        <p>
                            Applications web performantes avec PHP, Python 
                            et JavaScript (React, Vue, Angular).
                        </p>
                    </article>
                    
                    <article class="service-card">
                        <div class="service-icon">🚀</div>
                        <h3>Déploiement & DevOps</h3>
                        <p>
                            Mise en production avec Docker, CI/CD et 
                            monitoring pour une disponibilité maximale.
                        </p>
                    </article>
                </div>
            </div>
        </section>
        
        <!-- Section Portfolio -->
        <section id="portfolio" class="portfolio">
            <div class="container">
                <h2 class="section-title">Mes Projets</h2>
                
                <!-- Filtres -->
                <div class="portfolio-filters">
                    <button class="filter-btn active" data-filter="all">Tous</button>
                    <button class="filter-btn" data-filter="web">Web</button>
                    <button class="filter-btn" data-filter="mobile">Mobile</button>
                    <button class="filter-btn" data-filter="design">Design</button>
                </div>
                
                <!-- Grille projets -->
                <div class="portfolio-grid">
                    <article class="project-card" data-category="web">
                        <div class="project-image">
                            <img src="assets/images/project1.jpg" alt="E-commerce Platform">
                            <div class="project-overlay">
                                <h3>E-commerce Platform</h3>
                                <p>Laravel + Vue.js</p>
                                <a href="#" class="btn-view">Voir le projet</a>
                            </div>
                        </div>
                    </article>
                    
                    <article class="project-card" data-category="mobile">
                        <div class="project-image">
                            <img src="assets/images/project2.jpg" alt="Fitness App">
                            <div class="project-overlay">
                                <h3>Fitness App</h3>
                                <p>React Native</p>
                                <a href="#" class="btn-view">Voir le projet</a>
                            </div>
                        </div>
                    </article>
                    
                    <!-- Répéter pour 6 projets -->
                </div>
            </div>
        </section>
        
        <!-- Section Témoignages -->
        <section id="testimonials" class="testimonials">
            <div class="container">
                <h2 class="section-title">Ce que disent mes clients</h2>
                
                <div class="testimonials-slider">
                    <div class="testimonial-card active">
                        <div class="testimonial-content">
                            <p class="testimonial-text">
                                "John a transformé notre vision en une application web 
                                incroyable. Son expertise technique et sa créativité 
                                ont dépassé nos attentes."
                            </p>
                        </div>
                        <div class="testimonial-author">
                            <img src="assets/images/client1.jpg" alt="Marie Dupont">
                            <div>
                                <h4>Marie Dupont</h4>
                                <p>CEO, TechStart</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 2 autres témoignages -->
                </div>
                
                <!-- Navigation carrousel -->
                <div class="testimonials-dots">
                    <button class="dot active"></button>
                    <button class="dot"></button>
                    <button class="dot"></button>
                </div>
            </div>
        </section>
        
        <!-- Section Contact -->
        <section id="contact" class="contact">
            <div class="container">
                <h2 class="section-title">Travaillons ensemble</h2>
                
                <div class="contact-wrapper">
                    <!-- Formulaire -->
                    <form class="contact-form">
                        <div class="form-group">
                            <label for="name">Nom complet</label>
                            <input 
                                type="text" 
                                id="name" 
                                name="name" 
                                required
                                placeholder="John Doe"
                            >
                        </div>
                        
                        <div class="form-group">
                            <label for="email">Email</label>
                            <input 
                                type="email" 
                                id="email" 
                                name="email" 
                                required
                                placeholder="john@example.com"
                            >
                        </div>
                        
                        <div class="form-group">
                            <label for="message">Message</label>
                            <textarea 
                                id="message" 
                                name="message" 
                                rows="5" 
                                required
                                placeholder="Décrivez votre projet..."
                            ></textarea>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">
                            Envoyer le message
                        </button>
                    </form>
                    
                    <!-- Coordonnées -->
                    <div class="contact-info">
                        <div class="contact-item">
                            <span class="contact-icon">📧</span>
                            <div>
                                <h4>Email</h4>
                                <a href="mailto:john@example.com">john@example.com</a>
                            </div>
                        </div>
                        
                        <div class="contact-item">
                            <span class="contact-icon">📱</span>
                            <div>
                                <h4>Téléphone</h4>
                                <a href="tel:+33612345678">+33 6 12 34 56 78</a>
                            </div>
                        </div>
                        
                        <div class="contact-item">
                            <span class="contact-icon">📍</span>
                            <div>
                                <h4>Localisation</h4>
                                <p>Paris, France</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
    </main>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 John Doe. Tous droits réservés.</p>
            <div class="social-links">
                <a href="#" aria-label="GitHub">GitHub</a>
                <a href="#" aria-label="LinkedIn">LinkedIn</a>
                <a href="#" aria-label="Twitter">Twitter</a>
            </div>
        </div>
    </footer>
    
    <!-- JavaScript -->
    <script src="js/main.js"></script>
    <script src="js/filters.js"></script>
</body>
</html>
```

### 1.3 Points Clés HTML

**Balises sémantiques utilisées :**

| Balise | Rôle | Pourquoi |
|--------|------|----------|
| `<nav>` | Navigation | SEO + Accessibilité (lecteurs d'écran) |
| `<main>` | Contenu principal | 1 seul par page, contient le cœur |
| `<section>` | Section thématique | Groupe contenu lié (Hero, Services, etc.) |
| `<article>` | Contenu indépendant | Project card, testimonial (autonome) |
| `<header>` | En-tête | Top de page ou de section |
| `<footer>` | Pied de page | Bottom page avec infos annexes |

**Attributs accessibilité :**

```html
<!-- ARIA label pour éléments sans texte -->
<button aria-label="Toggle menu">☰</button>

<!-- Alt text obligatoire pour images -->
<img src="photo.jpg" alt="Description précise">

<!-- Labels pour inputs (screen readers) -->
<label for="email">Email</label>
<input type="email" id="email">
```

### Checkpoint Phase 1

- ✅ HTML structure sémantique créée
- ✅ Toutes sections présentes
- ✅ Accessibilité intégrée
- ✅ SEO meta tags ajoutés

---

## Phase 2 : CSS Fondamentaux (2h)

<div class="omny-meta" data-level="🟢 Débutant" data-time="2 heures"></div>

### Objectifs Phase 2

- ✅ Comprendre CSS = présentation
- ✅ Box Model (margin, padding, border)
- ✅ Sélecteurs CSS
- ✅ Typography & colors
- ✅ CSS Reset & Variables

### 2.1 CSS Reset (Normalisation)

**Pourquoi un reset CSS ?**
- Chaque navigateur a des styles par défaut DIFFÉRENTS
- Chrome : `<h1>` = 32px
- Firefox : `<h1>` = 33px
- Safari : marges différentes

**❌ Sans reset :** Design incohérent entre navigateurs  
**✅ Avec reset :** Base propre identique partout

**Fichier :** `css/reset.css`

```css
/**
 * Reset CSS - Normalisation navigateurs
 * 
 * POURQUOI : Supprimer styles par défaut incohérents
 * QUAND : Toujours en premier CSS chargé
 */

/* 
 * Box-sizing: border-box
 * POURQUOI : width inclut padding + border (calcul plus simple)
 * AVANT : width: 300px + padding: 20px = 340px total
 * APRÈS : width: 300px (padding inclus) = 300px total
 */
*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* 
 * HTML & Body
 * POURQUOI : Base pour calculs de hauteur (100vh)
 */
html {
    /* 
     * scroll-behavior: smooth
     * POURQUOI : Scroll fluide sur ancres (#home, #contact)
     * ALTERNATIVE : JavaScript scrollIntoView({behavior: 'smooth'})
     */
    scroll-behavior: smooth;
    
    /* 
     * Font-size base = 16px (1rem = 16px)
     * POURQUOI : Permet calculs relatifs (1.5rem = 24px)
     */
    font-size: 16px;
}

body {
    /* 
     * line-height: 1.6
     * POURQUOI : Espacement vertical confortable
     * DÉFAUT navigateur : ~1.2 (trop serré)
     * RECOMMANDÉ : 1.5-1.8
     */
    line-height: 1.6;
    
    /* 
     * -webkit-font-smoothing: antialiased
     * POURQUOI : Polices plus nettes sur macOS/iOS
     */
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* 
 * Supprimer styles listes
 * POURQUOI : Listes menu (nav) sans puces
 */
ul, ol {
    list-style: none;
}

/* 
 * Liens sans soulignement
 * POURQUOI : Design moderne (on stylera nous-mêmes)
 */
a {
    text-decoration: none;
    color: inherit; /* Hérite couleur parent */
}

/* 
 * Images responsives
 * POURQUOI : Ne dépassent jamais container
 */
img {
    max-width: 100%;
    height: auto;
    display: block; /* Supprime espace sous image (inline) */
}

/* 
 * Boutons cohérents
 * POURQUOI : Reset styles navigateur
 */
button {
    font-family: inherit;
    font-size: inherit;
    border: none;
    background: none;
    cursor: pointer;
}

/* 
 * Inputs & textarea cohérents
 */
input, textarea, select {
    font-family: inherit;
    font-size: inherit;
}
```

**CHAQUE propriété expliquée :**

| Propriété | Valeur | Pourquoi |
|-----------|--------|----------|
| `box-sizing` | `border-box` | Width inclut padding/border |
| `scroll-behavior` | `smooth` | Scroll fluide sur ancres |
| `line-height` | `1.6` | Lisibilité (espacement lignes) |
| `-webkit-font-smoothing` | `antialiased` | Polices nettes macOS |
| `list-style` | `none` | Supprimer puces listes |
| `text-decoration` | `none` | Liens sans soulignement |
| `max-width` | `100%` | Images ne débordent pas |
| `display: block` | Images | Supprime espace inline |

### 2.2 Variables CSS (Custom Properties)

**POURQUOI les variables CSS ?**
- ✅ Modifier couleur globale en 1 ligne
- ✅ Thème dark mode facile
- ✅ Maintenance simplifiée
- ✅ Calculs dynamiques

**Fichier :** `css/variables.css`

```css
/**
 * Variables CSS (Custom Properties)
 * 
 * SYNTAXE : --nom-variable: valeur;
 * USAGE : var(--nom-variable)
 * 
 * POURQUOI : Centraliser valeurs réutilisées
 * AVANTAGE : Modifier 1 variable = tout change
 */

:root {
    /* 
     * COULEURS PRIMAIRES
     * POURQUOI primary/secondary : Design cohérent
     * USAGE : Boutons, liens, accents
     */
    --color-primary: #6366f1;      /* Indigo moderne */
    --color-secondary: #8b5cf6;    /* Violet */
    --color-accent: #ec4899;       /* Rose */
    
    /* 
     * COULEURS NEUTRES
     * POURQUOI échelle gris : Textes, backgrounds
     * 50 = très clair, 900 = très foncé
     */
    --color-gray-50: #f9fafb;
    --color-gray-100: #f3f4f6;
    --color-gray-200: #e5e7eb;
    --color-gray-300: #d1d5db;
    --color-gray-500: #6b7280;
    --color-gray-700: #374151;
    --color-gray-900: #111827;
    
    /* 
     * COULEURS SÉMANTIQUES
     * POURQUOI : Feedback utilisateur
     * success = validation, danger = erreur
     */
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-danger: #ef4444;
    
    /* 
     * COULEURS TEXTE
     * POURQUOI plusieurs niveaux : Hiérarchie visuelle
     * primary = titres, secondary = paragraphes, muted = légendes
     */
    --color-text-primary: var(--color-gray-900);
    --color-text-secondary: var(--color-gray-700);
    --color-text-muted: var(--color-gray-500);
    
    /* 
     * COULEURS BACKGROUND
     */
    --color-bg-primary: #ffffff;
    --color-bg-secondary: var(--color-gray-50);
    
    /* 
     * TYPOGRAPHIE
     * POURQUOI font-family variables : Changement global facile
     * system-ui = police système (rapide à charger)
     */
    --font-primary: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
                    "Helvetica Neue", Arial, sans-serif;
    --font-heading: "Poppins", sans-serif;
    
    /* 
     * TAILLES POLICE
     * POURQUOI rem : Relatif à html font-size (16px)
     * 1rem = 16px, 1.5rem = 24px, 2rem = 32px
     * AVANTAGE : Accessibilité (users peuvent zoomer)
     */
    --font-size-xs: 0.75rem;    /* 12px */
    --font-size-sm: 0.875rem;   /* 14px */
    --font-size-base: 1rem;     /* 16px */
    --font-size-lg: 1.125rem;   /* 18px */
    --font-size-xl: 1.25rem;    /* 20px */
    --font-size-2xl: 1.5rem;    /* 24px */
    --font-size-3xl: 1.875rem;  /* 30px */
    --font-size-4xl: 2.25rem;   /* 36px */
    --font-size-5xl: 3rem;      /* 48px */
    
    /* 
     * ESPACEMENTS
     * POURQUOI échelle 4px : Cohérence visuelle
     * 4, 8, 12, 16, 20, 24, 32, 40, 48, 64
     */
    --spacing-1: 0.25rem;   /* 4px */
    --spacing-2: 0.5rem;    /* 8px */
    --spacing-3: 0.75rem;   /* 12px */
    --spacing-4: 1rem;      /* 16px */
    --spacing-5: 1.25rem;   /* 20px */
    --spacing-6: 1.5rem;    /* 24px */
    --spacing-8: 2rem;      /* 32px */
    --spacing-10: 2.5rem;   /* 40px */
    --spacing-12: 3rem;     /* 48px */
    --spacing-16: 4rem;     /* 64px */
    
    /* 
     * BORDER RADIUS
     * POURQUOI : Coins arrondis modernes
     * sm = boutons, md = cards, lg = modals, full = cercles
     */
    --radius-sm: 0.25rem;   /* 4px */
    --radius-md: 0.5rem;    /* 8px */
    --radius-lg: 1rem;      /* 16px */
    --radius-full: 9999px;  /* Cercle parfait */
    
    /* 
     * OMBRES
     * POURQUOI : Profondeur, élévation cards
     * sm = subtle, md = cards, lg = modals, xl = popups
     */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    
    /* 
     * TRANSITIONS
     * POURQUOI : Animations fluides
     * fast = 150ms (hover), base = 300ms, slow = 500ms (slides)
     */
    --transition-fast: 150ms ease-in-out;
    --transition-base: 300ms ease-in-out;
    --transition-slow: 500ms ease-in-out;
    
    /* 
     * Z-INDEX
     * POURQUOI : Empilage cohérent
     * navbar > modal > overlay > content
     */
    --z-dropdown: 1000;
    --z-sticky: 1020;
    --z-fixed: 1030;
    --z-modal-backdrop: 1040;
    --z-modal: 1050;
    --z-tooltip: 1070;
}
```

**USAGE des variables :**

```css
/* ❌ AVANT (valeurs en dur) */
.button {
    background: #6366f1;
    padding: 16px 32px;
    border-radius: 8px;
}

/* ✅ APRÈS (variables) */
.button {
    background: var(--color-primary);
    padding: var(--spacing-4) var(--spacing-8);
    border-radius: var(--radius-md);
}

/* 
 * AVANTAGE : Modifier --color-primary = tous boutons changent
 */
```

### Checkpoint Phase 2

- ✅ Reset CSS appliqué
- ✅ Variables CSS centralisées
- ✅ Comprendre box-sizing
- ✅ Échelle couleurs/espacements

---

*Je continue avec les Phases 3-8 dans le prochain message...*

## Phase 3 : Flexbox Détaillé (2h30)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2h30"></div>

### Objectifs Phase 3

- ✅ Comprendre Flexbox = layout 1D (ligne OU colonne)
- ✅ justify-content (axe principal)
- ✅ align-items (axe secondaire)
- ✅ flex-wrap, gap, order
- ✅ Cas d'usage réels (navbar, cards)

### 3.1 Flexbox : Concepts Fondamentaux

**QUOI :** Flexbox = système layout 1 dimension  
**POURQUOI :** Aligner éléments facilement (avant = float compliqué)  
**QUAND :** Navigation, cards row, centrage, distribution espacée

**Anatomie Flexbox :**

```
┌─────────────────────────────────────┐
│ FLEX CONTAINER (parent)             │ ← display: flex
│                                     │
│  ┌──────┐  ┌──────┐  ┌──────┐     │
│  │ ITEM │  │ ITEM │  │ ITEM │     │ ← FLEX ITEMS (enfants)
│  └──────┘  └──────┘  └──────┘     │
│                                     │
│  ←──────  MAIN AXIS  ──────→      │ justify-content
│      ↑   CROSS AXIS   ↓           │ align-items
└─────────────────────────────────────┘
```

**Fichier :** `css/layout.css`

```css
/**
 * FLEXBOX COMPLET
 * 
 * RÈGLE 1 : display: flex sur PARENT
 * RÈGLE 2 : Propriétés justify/align sur PARENT
 * RÈGLE 3 : Propriétés flex/order sur ENFANTS
 */

/* ====================================
   NAVBAR (Flexbox horizontal)
   ==================================== */

.navbar {
    /* 
     * display: flex
     * POURQUOI : Activer Flexbox
     * EFFET : Enfants deviennent flex items (alignés horizontal par défaut)
     * ALTERNATIVE : display: grid (pour layout 2D)
     */
    display: flex;
    
    /* 
     * justify-content: space-between
     * POURQUOI : Distribuer espace sur axe principal (horizontal)
     * VALEURS POSSIBLES :
     * - flex-start : Début (défaut)
     * - flex-end : Fin
     * - center : Centré
     * - space-between : Espacement entre items (pas sur bords)
     * - space-around : Espacement autour items (sur bords aussi)
     * - space-evenly : Espacement égal partout
     * 
     * USAGE ICI : Logo gauche, menu droite
     */
    justify-content: space-between;
    
    /* 
     * align-items: center
     * POURQUOI : Aligner sur axe secondaire (vertical)
     * VALEURS POSSIBLES :
     * - stretch : Étirer hauteur (défaut)
     * - flex-start : Haut
     * - flex-end : Bas
     * - center : Milieu
     * - baseline : Aligner baseline texte
     * 
     * USAGE ICI : Logo et menu centrés verticalement
     */
    align-items: center;
    
    /* 
     * gap: 2rem
     * POURQUOI : Espacement entre items (modern, remplace margin)
     * AVANT : .item + .item { margin-left: 2rem; }
     * APRÈS : gap: 2rem; (plus simple)
     * 
     * SUPPORT : Chrome 84+, Firefox 63+, Safari 14.1+
     */
    gap: 2rem;
    
    /* 
     * padding: 1rem 2rem
     * SYNTAXE : padding: [vertical] [horizontal]
     * ÉQUIVALENT : padding-top/bottom: 1rem, padding-left/right: 2rem
     * POURQUOI : Espace intérieur navbar
     */
    padding: 1rem 2rem;
    
    /* 
     * background: white
     * position: sticky, top: 0
     * POURQUOI : Navbar fixe en haut lors scroll
     * ALTERNATIVE : position: fixed (sort du flow, peut cacher contenu)
     */
    background: white;
    position: sticky;
    top: 0;
    
    /* 
     * z-index: 1000
     * POURQUOI : Au-dessus du contenu
     * VALEUR : Plus haut = plus devant
     */
    z-index: var(--z-sticky);
    
    /* 
     * box-shadow: 0 2px 10px rgba(0,0,0,0.1)
     * POURQUOI : Profondeur visuelle
     * SYNTAXE : offset-x offset-y blur spread color
     */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* ====================================
   NAV MENU (Flexbox liste)
   ==================================== */

.nav-menu {
    /* 
     * Flex items dans navbar
     * flex-direction par défaut = row (horizontal)
     */
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav-menu a {
    /* 
     * Styles liens navbar
     */
    color: var(--color-text-secondary);
    font-weight: 500;
    
    /* 
     * transition: color 0.3s
     * POURQUOI : Animation smooth hover
     * SYNTAXE : property duration timing-function
     */
    transition: color var(--transition-fast);
}

.nav-menu a:hover {
    color: var(--color-primary);
}

/* ====================================
   CONTAINER (Centrage + Max-width)
   ==================================== */

.container {
    /* 
     * max-width: 1200px
     * POURQUOI : Limite largeur contenu (lisibilité)
     * RECOMMANDÉ : 1200px - 1400px
     * TROP LARGE : Lignes texte difficiles à lire
     */
    max-width: 1200px;
    
    /* 
     * margin: 0 auto
     * POURQUOI : Centrer horizontalement
     * SYNTAXE : margin: [vertical] [horizontal]
     * 0 = pas de margin top/bottom
     * auto = margin left/right égaux (centrage)
     */
    margin: 0 auto;
    
    /* 
     * padding: 0 2rem
     * POURQUOI : Espace sur mobiles (éviter texte collé bords)
     */
    padding: 0 2rem;
}

/* ====================================
   HERO CTA BUTTONS (Flexbox row)
   ==================================== */

.hero-cta {
    display: flex;
    
    /* 
     * gap: 1rem
     * POURQUOI : Espacement entre boutons
     */
    gap: 1rem;
    
    /* 
     * flex-wrap: wrap
     * POURQUOI : Boutons passent à la ligne sur mobile
     * DÉFAUT : nowrap (1 ligne)
     * VALEURS :
     * - nowrap : Pas de retour ligne
     * - wrap : Retour ligne si besoin
     * - wrap-reverse : Retour ligne inversé
     */
    flex-wrap: wrap;
}

/* ====================================
   STATS GRID (Flexbox row)
   ==================================== */

.stats-grid {
    display: flex;
    justify-content: space-around;
    gap: 2rem;
    
    /* 
     * Sur mobile : column (Phase 5)
     */
}

.stat-item {
    /* 
     * flex: 1
     * SYNTAXE COMPLÈTE : flex: [grow] [shrink] [basis]
     * flex: 1 = flex: 1 1 0% (grow=1, shrink=1, basis=0%)
     * 
     * POURQUOI :
     * - grow=1 : Prend espace disponible
     * - shrink=1 : Se réduit si nécessaire
     * - basis=0% : Base de calcul
     * 
     * EFFET : Items prennent largeur égale
     */
    flex: 1;
    
    /* 
     * text-align: center
     * POURQUOI : Centrer texte dans item
     */
    text-align: center;
}

/* ====================================
   SERVICES CARDS (Flexbox row)
   ==================================== */

.services-grid {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}

.service-card {
    /* 
     * flex: 1 1 300px
     * POURQUOI :
     * - grow=1 : Grandit si espace
     * - shrink=1 : Rétrécit si petit
     * - basis=300px : Largeur min 300px
     * 
     * EFFET : Cards largeur égale, min 300px
     * Si espace < 300px → wrap (retour ligne)
     */
    flex: 1 1 300px;
    
    /* 
     * Card styling
     */
    background: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    
    /* 
     * transition: transform 0.3s, box-shadow 0.3s
     * POURQUOI : Animation hover
     * SYNTAXE : property1 duration, property2 duration
     */
    transition: transform var(--transition-base),
                box-shadow var(--transition-base);
}

.service-card:hover {
    /* 
     * transform: translateY(-10px)
     * POURQUOI : Effet "soulevé" au hover
     * VALEURS :
     * - translateX(10px) : Déplace droite
     * - translateY(-10px) : Déplace haut
     * - scale(1.1) : Agrandit 110%
     * - rotate(45deg) : Rotation 45°
     */
    transform: translateY(-10px);
    
    /* 
     * box-shadow plus intense au hover
     */
    box-shadow: var(--shadow-xl);
}

/* ====================================
   FLEXBOX PATTERNS COMMUNS
   ==================================== */

/* Pattern 1 : Centrage absolu */
.center-absolute {
    display: flex;
    justify-content: center;  /* Horizontal */
    align-items: center;      /* Vertical */
}

/* Pattern 2 : Espace entre 2 éléments */
.space-between {
    display: flex;
    justify-content: space-between;
}

/* Pattern 3 : Colonne verticale */
.flex-column {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* Pattern 4 : Items égaux */
.flex-equal {
    display: flex;
    gap: 1rem;
}
.flex-equal > * {
    flex: 1;
}
```

### 3.2 Tableau Récapitulatif Flexbox

| Propriété | Cible | Valeurs | Usage |
|-----------|-------|---------|-------|
| `display: flex` | Container | - | Active Flexbox |
| `flex-direction` | Container | row, column, row-reverse, column-reverse | Axe principal |
| `justify-content` | Container | flex-start, center, flex-end, space-between, space-around | Alignement axe principal |
| `align-items` | Container | flex-start, center, flex-end, stretch, baseline | Alignement axe secondaire |
| `gap` | Container | 1rem, 20px, etc. | Espacement items |
| `flex-wrap` | Container | nowrap, wrap, wrap-reverse | Retour ligne |
| `flex` | Item | 1, 0 1 auto, 1 1 300px | Grow/Shrink/Basis |
| `order` | Item | 0, 1, -1, etc. | Ordre affichage |
| `align-self` | Item | auto, flex-start, center, etc. | Override align-items |

### 3.3 Exercice Pratique Flexbox

!!! question "Mission : Créer Footer Flexbox"
    Créez un footer avec :
    - Logo gauche
    - Liens centrés
    - Socials droite
    - Responsive (colonne sur mobile)

??? success "Solution"
    ```css
    .footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 2rem;
        background: var(--color-gray-900);
        color: white;
    }
    
    .footer-links {
        display: flex;
        gap: 2rem;
    }
    
    /* Mobile */
    @media (max-width: 768px) {
        .footer {
            flex-direction: column;
            gap: 1.5rem;
            text-align: center;
        }
    }
    ```

### Checkpoint Phase 3

- ✅ Flexbox container/items compris
- ✅ justify-content maîtrisé
- ✅ align-items maîtrisé
- ✅ Patterns communs appliqués

---

## Phase 4 : Grid Layout Complet (2h30)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2h30"></div>

### Objectifs Phase 4

- ✅ Comprendre Grid = layout 2D (lignes ET colonnes)
- ✅ grid-template-columns/rows
- ✅ grid-area & grid-template-areas
- ✅ auto-fit, minmax (responsive)
- ✅ Différence Grid vs Flexbox

### 4.1 Grid : Concepts Fondamentaux

**QUOI :** Grid = système layout 2 dimensions  
**POURQUOI :** Layouts complexes (dashboard, galerie)  
**QUAND :** Grilles régulières, layouts imbriqués

**Grid vs Flexbox :**

```
FLEXBOX (1D)          GRID (2D)
┌───┬───┬───┐         ┌───┬───┬───┐
│ 1 │ 2 │ 3 │         │ 1 │ 2 │ 3 │
└───┴───┴───┘         ├───┼───┼───┤
                      │ 4 │ 5 │ 6 │
Ligne OU colonne      ├───┼───┼───┤
                      │ 7 │ 8 │ 9 │
                      └───┴───┴───┘
                      Lignes ET colonnes
```

**Fichier :** `css/layout.css` (suite)

```css
/* ====================================
   PORTFOLIO GRID (Grid 3 colonnes)
   ==================================== */

.portfolio-grid {
    /* 
     * display: grid
     * POURQUOI : Activer CSS Grid
     * EFFET : Enfants deviennent grid items
     */
    display: grid;
    
    /* 
     * grid-template-columns: repeat(3, 1fr)
     * DÉCOMPOSITION :
     * - repeat(3, ...) : Répéter 3 fois
     * - 1fr : 1 fraction de l'espace disponible
     * ÉQUIVALENT : grid-template-columns: 1fr 1fr 1fr
     * 
     * POURQUOI 1fr :
     * - fr = unité flexible (comme flex: 1)
     * - 1fr 1fr 1fr = 3 colonnes égales
     * - 2fr 1fr 1fr = col1 double largeur
     * 
     * EFFET : 3 colonnes largeur égale
     */
    grid-template-columns: repeat(3, 1fr);
    
    /* 
     * gap: 2rem
     * POURQUOI : Espacement entre items (lignes ET colonnes)
     * AVANT : grid-row-gap + grid-column-gap
     * MAINTENANT : gap (shorthand)
     * 
     * SYNTAXE :
     * - gap: 2rem (ligne et colonne identiques)
     * - gap: 2rem 1rem (ligne 2rem, colonne 1rem)
     */
    gap: 2rem;
    
    /* 
     * Sur mobile : 1 colonne (Phase 5)
     */
}

/* ====================================
   CONTACT LAYOUT (Grid 2 colonnes)
   ==================================== */

.contact-wrapper {
    display: grid;
    
    /* 
     * grid-template-columns: 2fr 1fr
     * POURQUOI :
     * - 2fr = Formulaire prend 2/3 largeur
     * - 1fr = Coordonnées prend 1/3 largeur
     * 
     * CALCUL :
     * Total = 2fr + 1fr = 3fr
     * Col1 = 2/3 = 66.66%
     * Col2 = 1/3 = 33.33%
     */
    grid-template-columns: 2fr 1fr;
    gap: 3rem;
    
    /* 
     * align-items: start
     * POURQUOI : Items alignés en haut (pas stretch)
     * VALEURS :
     * - start : Haut
     * - center : Milieu
     * - end : Bas
     * - stretch : Étirer (défaut)
     */
    align-items: start;
}

/* ====================================
   GRID AUTO-FIT (Responsive sans media queries)
   ==================================== */

.services-grid {
    display: grid;
    
    /* 
     * grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))
     * 
     * DÉCOMPOSITION :
     * 
     * 1. minmax(300px, 1fr)
     *    POURQUOI : Largeur min 300px, max 1fr
     *    - Si espace > 300px : 1fr (flex)
     *    - Si espace < 300px : 300px (fixe)
     * 
     * 2. repeat(auto-fit, ...)
     *    POURQUOI : Nombre colonnes automatique
     *    - auto-fit : Fit items dans espace disponible
     *    - auto-fill : Crée colonnes vides aussi
     * 
     * EFFET MAGIQUE :
     * - Large écran : 3-4 colonnes
     * - Tablette : 2 colonnes
     * - Mobile : 1 colonne
     * TOUT AUTOMATIQUE sans media queries !
     */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

/* ====================================
   GRID TEMPLATE AREAS (Layout nommé)
   ==================================== */

.dashboard {
    display: grid;
    
    /* 
     * grid-template-areas: "header header header"
     *                      "sidebar main main"
     *                      "sidebar footer footer"
     * 
     * POURQUOI : Layout lisible avec noms
     * SYNTAXE : Chaque ligne = 1 string
     * 
     * EFFET :
     * header prend 3 colonnes (ligne 1)
     * sidebar prend 1 col sur 2 lignes
     * main prend 2 colonnes
     * footer prend 2 colonnes
     */
    grid-template-areas:
        "header header header"
        "sidebar main main"
        "sidebar footer footer";
    
    /* 
     * grid-template-columns: 250px 1fr 1fr
     * POURQUOI : Définir largeurs colonnes
     * - 250px : Sidebar fixe
     * - 1fr 1fr : Main + footer flexibles
     */
    grid-template-columns: 250px 1fr 1fr;
    
    /* 
     * grid-template-rows: auto 1fr auto
     * POURQUOI : Définir hauteurs lignes
     * - auto : Header hauteur contenu
     * - 1fr : Main prend espace restant
     * - auto : Footer hauteur contenu
     */
    grid-template-rows: auto 1fr auto;
    
    gap: 1rem;
    min-height: 100vh;
}

/* Placer éléments dans zones nommées */
.dashboard-header {
    /* 
     * grid-area: header
     * POURQUOI : Placer dans zone "header"
     * ALTERNATIVE : grid-column: 1 / 4; grid-row: 1;
     */
    grid-area: header;
}

.dashboard-sidebar {
    grid-area: sidebar;
}

.dashboard-main {
    grid-area: main;
}

.dashboard-footer {
    grid-area: footer;
}

/* ====================================
   GRID PLACEMENT MANUEL
   ==================================== */

.grid-manual {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(3, 100px);
    gap: 1rem;
}

.item-1 {
    /* 
     * grid-column: 1 / 3
     * SYNTAXE : grid-column: [start] / [end]
     * POURQUOI : Item occupe colonnes 1 à 3 (2 colonnes)
     * 
     * ÉQUIVALENT : 
     * grid-column-start: 1;
     * grid-column-end: 3;
     * 
     * SHORTHAND : grid-column: 1 / span 2 (occupe 2 colonnes)
     */
    grid-column: 1 / 3;
    
    /* 
     * grid-row: 1 / 2
     * POURQUOI : Item occupe ligne 1 (1 ligne)
     */
    grid-row: 1 / 2;
}

.item-2 {
    /* 
     * Occupe 2 colonnes et 2 lignes
     */
    grid-column: 3 / 5;
    grid-row: 1 / 3;
}

/* ====================================
   GRID PATTERNS COMMUNS
   ==================================== */

/* Pattern 1 : Grid égale */
.grid-equal-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}

/* Pattern 2 : Grid asymétrique */
.grid-asymmetric {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
}

/* Pattern 3 : Grid responsive auto */
.grid-responsive-auto {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}

/* Pattern 4 : Grid dense (comble trous) */
.grid-dense {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    
    /* 
     * grid-auto-flow: dense
     * POURQUOI : Combler espaces vides
     * DÉFAUT : row (ordre normal)
     * VALEURS :
     * - row : Remplir ligne par ligne
     * - column : Remplir colonne par colonne
     * - dense : Combler trous (réorganise items)
     */
    grid-auto-flow: dense;
    gap: 1rem;
}
```

### 4.2 Tableau Récapitulatif Grid

| Propriété | Valeurs | Usage |
|-----------|---------|-------|
| `display: grid` | - | Active Grid |
| `grid-template-columns` | 1fr 1fr, repeat(3, 1fr), 200px auto 1fr | Colonnes |
| `grid-template-rows` | auto 1fr auto, repeat(3, 100px) | Lignes |
| `grid-template-areas` | "header header" "sidebar main" | Layout nommé |
| `gap` | 1rem, 2rem 1rem | Espacement |
| `grid-column` | 1 / 3, span 2 | Placement colonne item |
| `grid-row` | 1 / 3, span 2 | Placement ligne item |
| `grid-area` | header, main | Placement dans zone nommée |
| `minmax()` | minmax(200px, 1fr) | Taille min/max |
| `auto-fit` | repeat(auto-fit, ...) | Nombre colonnes auto |

### 4.3 Différence Flexbox vs Grid

| Critère | Flexbox | Grid |
|---------|---------|------|
| **Dimensions** | 1D (ligne OU colonne) | 2D (lignes ET colonnes) |
| **Usage** | Navigation, cards row, centrage | Layouts complexes, galeries |
| **Ordre** | Contrôle order | Placement précis |
| **Responsive** | flex-wrap | auto-fit, minmax |
| **Exemple** | Navbar, footer, buttons | Dashboard, galerie photos |

**RÈGLE SIMPLE :**
- Items dans 1 direction ? → **Flexbox**
- Layout grille régulière ? → **Grid**

### Checkpoint Phase 4

- ✅ Grid container/items compris
- ✅ grid-template-columns maîtrisé
- ✅ auto-fit + minmax (responsive)
- ✅ Différence Grid/Flexbox claire

---

## Phase 5 : Responsive Design (2h)

### 5.1 Mobile-First Approach

**PRINCIPE :** Commencer par mobile, puis ajouter styles desktop

```css
/* ❌ DESKTOP-FIRST (mauvais) */
.container {
    width: 1200px; /* Desktop */
}
@media (max-width: 768px) {
    .container {
        width: 100%; /* Override pour mobile */
    }
}

/* ✅ MOBILE-FIRST (recommandé) */
.container {
    width: 100%; /* Mobile d'abord */
}
@media (min-width: 768px) {
    .container {
        width: 1200px; /* Ajouter desktop */
    }
}
```

**Fichier :** `css/responsive.css`

```css
/**
 * RESPONSIVE DESIGN
 * 
 * BREAKPOINTS :
 * - 640px : Tablette portrait
 * - 768px : Tablette landscape
 * - 1024px : Desktop small
 * - 1280px : Desktop large
 */

/* Mobile (défaut, pas de media query) */

/* ====================================
   NAVBAR RESPONSIVE
   ==================================== */

/* Burger menu (mobile seulement) */
.burger {
    display: none; /* Caché sur desktop */
    flex-direction: column;
    gap: 0.25rem;
}

.burger span {
    width: 25px;
    height: 3px;
    background: var(--color-gray-900);
    transition: var(--transition-base);
}

/* Sur mobile : Afficher burger, cacher menu */
@media (max-width: 768px) {
    .burger {
        display: flex;
    }
    
    .nav-menu {
        /* 
         * position: fixed
         * POURQUOI : Menu overlay plein écran
         */
        position: fixed;
        top: 60px;
        left: 0;
        right: 0;
        
        /* 
         * flex-direction: column
         * POURQUOI : Menu vertical mobile
         */
        flex-direction: column;
        
        background: white;
        padding: 2rem;
        
        /* 
         * transform: translateX(-100%)
         * POURQUOI : Menu hors écran par défaut
         * JavaScript toggle class "active"
         */
        transform: translateX(-100%);
        transition: transform var(--transition-base);
    }
    
    .nav-menu.active {
        transform: translateX(0);
    }
}

/* ====================================
   HERO RESPONSIVE
   ==================================== */

.hero {
    /* Mobile : padding réduit */
    padding: 4rem 0;
}

.hero-title {
    /* Mobile : taille réduite */
    font-size: var(--font-size-3xl);
}

/* Tablette et desktop */
@media (min-width: 768px) {
    .hero {
        padding: 8rem 0;
    }
    
    .hero-title {
        font-size: var(--font-size-5xl);
    }
}

/* ====================================
   STATS GRID RESPONSIVE
   ==================================== */

.stats-grid {
    /* Mobile : colonne */
    flex-direction: column;
}

@media (min-width: 640px) {
    .stats-grid {
        /* Tablette : 2 colonnes */
        flex-direction: row;
        flex-wrap: wrap;
    }
    
    .stat-item {
        flex: 1 1 calc(50% - 1rem);
    }
}

@media (min-width: 1024px) {
    .stats-grid {
        /* Desktop : 4 colonnes */
        flex-wrap: nowrap;
    }
    
    .stat-item {
        flex: 1;
    }
}

/* ====================================
   PORTFOLIO GRID RESPONSIVE
   ==================================== */

.portfolio-grid {
    /* Mobile : 1 colonne */
    grid-template-columns: 1fr;
}

@media (min-width: 640px) {
    .portfolio-grid {
        /* Tablette : 2 colonnes */
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1024px) {
    .portfolio-grid {
        /* Desktop : 3 colonnes */
        grid-template-columns: repeat(3, 1fr);
    }
}

/* ====================================
   CONTACT WRAPPER RESPONSIVE
   ==================================== */

.contact-wrapper {
    /* Mobile : 1 colonne */
    grid-template-columns: 1fr;
}

@media (min-width: 768px) {
    .contact-wrapper {
        /* Desktop : 2 colonnes */
        grid-template-columns: 2fr 1fr;
    }
}
```

### Checkpoint Phase 5

- ✅ Mobile-first compris
- ✅ Media queries maîtrisées
- ✅ Breakpoints définis
- ✅ Responsive complet

---

## Phase 6-8 : CSS Moderne, Animations & Tailwind

*Contenu complet dans le guide (animations, variables, Tailwind refactor)...*

---

## Phase 6 : CSS Moderne & Animations (2h)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2 heures"></div>

### Objectifs Phase 6

- ✅ Animations CSS (@keyframes)
- ✅ Transitions (hover effects)
- ✅ Transforms (translate, scale, rotate)
- ✅ CSS nouveautés 2024-2025
- ✅ Scroll animations JavaScript

### 6.1 Transitions vs Animations

**DIFFÉRENCE CLÉS :**

| Critère | Transition | Animation |
|---------|-----------|-----------|
| **Déclenchement** | Événement (hover, focus) | Automatique (load, loop) |
| **États** | 2 états (début → fin) | Multiple états (0% → 50% → 100%) |
| **Contrôle** | Simple | Avancé (keyframes) |
| **Usage** | Hover effects, focus | Loaders, pulse, rotate |

**Fichier :** `css/components.css`

```css
/* ====================================
   TRANSITIONS (Hover Effects)
   ==================================== */

.btn {
    /* 
     * Styles de base bouton
     */
    padding: 1rem 2rem;
    background: var(--color-primary);
    color: white;
    border-radius: var(--radius-md);
    font-weight: 600;
    
    /* 
     * transition: all 0.3s ease-in-out
     * 
     * SYNTAXE COMPLÈTE :
     * transition: [property] [duration] [timing-function] [delay]
     * 
     * DÉCOMPOSITION :
     * - property : Propriété animée
     *   all = toutes propriétés (pratique mais moins performant)
     *   background, transform = spécifique (plus performant)
     * 
     * - duration : 0.3s = 300ms
     *   0.15s = rapide (hover subtil)
     *   0.3s = standard (hover visible)
     *   0.5s = lent (animations importantes)
     * 
     * - timing-function : Courbe accélération
     *   ease : Lent→Rapide→Lent (défaut)
     *   ease-in : Lent→Rapide
     *   ease-out : Rapide→Lent
     *   ease-in-out : Lent→Rapide→Lent (smooth)
     *   linear : Vitesse constante
     *   cubic-bezier(0.4, 0, 0.2, 1) : Personnalisé
     * 
     * - delay : 0.1s = attente avant démarrage
     * 
     * POURQUOI ease-in-out :
     * Animation naturelle (accélération douce)
     */
    transition: all 0.3s ease-in-out;
    
    /* 
     * ALTERNATIVE (plus performant) :
     * transition: background 0.3s, transform 0.3s;
     * POURQUOI : Anime seulement propriétés nécessaires
     */
}

.btn:hover {
    /* 
     * background: var(--color-primary-dark)
     * POURQUOI : Feedback visuel hover
     * TRANSITION : Couleur change en 0.3s smooth
     */
    background: #4f46e5; /* Primary dark */
    
    /* 
     * transform: translateY(-2px)
     * POURQUOI : Effet "soulevé"
     * TRANSITION : Position change en 0.3s smooth
     */
    transform: translateY(-2px);
    
    /* 
     * box-shadow: 0 8px 16px rgba(0,0,0,0.2)
     * POURQUOI : Ombre plus intense (élévation)
     */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.btn:active {
    /* 
     * transform: translateY(0)
     * POURQUOI : Effet "pressé" au clic
     */
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* ====================================
   SERVICE CARD HOVER
   ==================================== */

.service-card {
    background: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    
    /* 
     * transition: transform 0.3s, box-shadow 0.3s
     * POURQUOI : Animer 2 propriétés spécifiques
     * PERFORMANCE : Mieux que "all"
     */
    transition: transform var(--transition-base),
                box-shadow var(--transition-base);
}

.service-card:hover {
    /* 
     * transform: translateY(-10px) scale(1.02)
     * DÉCOMPOSITION :
     * - translateY(-10px) : Monte de 10px
     * - scale(1.02) : Agrandi 2%
     * 
     * POURQUOI plusieurs transforms :
     * Effet combiné (soulevé + léger zoom)
     */
    transform: translateY(-10px) scale(1.02);
    box-shadow: var(--shadow-xl);
}

/* ====================================
   PROJECT CARD IMAGE ZOOM
   ==================================== */

.project-card {
    /* 
     * overflow: hidden
     * POURQUOI : Cache dépassement image zoomée
     * SANS : Image zoom dépasse card
     * AVEC : Image zoom reste dans card
     */
    overflow: hidden;
    border-radius: var(--radius-lg);
}

.project-image img {
    /* 
     * width: 100%, height: 100%
     * object-fit: cover
     * POURQUOI :
     * - width/height : Remplir container
     * - object-fit: cover : Crop intelligent (centre image)
     * 
     * ALTERNATIVES object-fit :
     * - contain : Image entière visible (peut avoir espaces)
     * - cover : Remplir, crop si nécessaire
     * - fill : Étirer (déformation possible)
     */
    width: 100%;
    height: 100%;
    object-fit: cover;
    
    /* 
     * transition: transform 0.5s ease-out
     * POURQUOI : Zoom image au hover card
     */
    transition: transform 0.5s ease-out;
}

.project-card:hover .project-image img {
    /* 
     * transform: scale(1.1)
     * POURQUOI : Zoom 10% au hover
     * EFFET : Image grandit, overflow hidden la coupe
     */
    transform: scale(1.1);
}

.project-overlay {
    /* 
     * position: absolute
     * inset: 0 (équivalent top/right/bottom/left: 0)
     * POURQUOI : Overlay plein écran sur image
     * 
     * inset: 0 (CSS moderne, équivalent à :)
     * top: 0; right: 0; bottom: 0; left: 0;
     */
    position: absolute;
    inset: 0;
    
    /* 
     * background: rgba(0, 0, 0, 0.8)
     * POURQUOI : Fond noir 80% opacité
     * RGBA : Red Green Blue Alpha (transparence)
     */
    background: rgba(0, 0, 0, 0.8);
    
    /* 
     * display: flex
     * justify-content/align-items: center
     * POURQUOI : Centrer contenu overlay
     */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    
    /* 
     * opacity: 0
     * POURQUOI : Caché par défaut
     * HOVER : opacity 1 (visible)
     */
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
}

.project-card:hover .project-overlay {
    opacity: 1;
}

/* ====================================
   @KEYFRAMES ANIMATIONS
   ==================================== */

/* 
 * Animation 1 : Fade In Up
 * USAGE : Apparition éléments avec montée
 */
@keyframes fadeInUp {
    /* 
     * 0% : État initial (invisible en bas)
     */
    0% {
        opacity: 0;
        transform: translateY(30px);
    }
    
    /* 
     * 100% : État final (visible position normale)
     */
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-title {
    /* 
     * animation: fadeInUp 1s ease-out
     * 
     * SYNTAXE :
     * animation: [name] [duration] [timing-function] [delay] [iteration] [direction]
     * 
     * DÉCOMPOSITION :
     * - name : fadeInUp (nom keyframes)
     * - duration : 1s
     * - timing-function : ease-out (rapide→lent)
     * - delay : 0s (immédiat)
     * - iteration-count : 1 (1 fois, défaut)
     * - direction : normal (0%→100%)
     * 
     * ALTERNATIVES iteration-count :
     * - 1 : Une fois
     * - 3 : 3 fois
     * - infinite : Boucle infinie
     * 
     * ALTERNATIVES direction :
     * - normal : 0%→100%
     * - reverse : 100%→0%
     * - alternate : 0%→100%→0%→100% (yoyo)
     */
    animation: fadeInUp 1s ease-out;
}

.hero-subtitle {
    /* 
     * animation-delay: 0.2s
     * POURQUOI : Décalage animation (effet cascade)
     * hero-title apparaît, PUIS hero-subtitle 0.2s après
     */
    animation: fadeInUp 1s ease-out 0.2s;
    
    /* 
     * animation-fill-mode: backwards
     * POURQUOI : Appliquer état 0% pendant delay
     * SANS : Élément visible puis disparaît pendant 0.2s
     * AVEC : Élément reste état 0% (invisible) pendant 0.2s
     * 
     * VALEURS :
     * - none : Aucun style keyframes avant/après
     * - forwards : Garde état 100% après animation
     * - backwards : Applique état 0% pendant delay
     * - both : forwards + backwards
     */
    animation-fill-mode: backwards;
}

/* 
 * Animation 2 : Pulse (Scale loop)
 * USAGE : Attirer attention (boutons, badges)
 */
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

.scroll-indicator {
    /* 
     * animation: pulse 2s ease-in-out infinite
     * POURQUOI : Boucle infinie (attire œil)
     */
    animation: pulse 2s ease-in-out infinite;
}

/* 
 * Animation 3 : Rotate (Loader)
 * USAGE : Spinners, loaders
 */
@keyframes rotate {
    from {
        /* 
         * transform: rotate(0deg)
         * DÉPART : Pas de rotation
         */
        transform: rotate(0deg);
    }
    to {
        /* 
         * transform: rotate(360deg)
         * ARRIVÉE : Tour complet
         */
        transform: rotate(360deg);
    }
}

.loader {
    /* 
     * animation: rotate 1s linear infinite
     * POURQUOI :
     * - linear : Vitesse constante (pas d'accélération)
     * - infinite : Boucle sans fin
     * - 1s : 1 tour par seconde
     */
    animation: rotate 1s linear infinite;
}

/* 
 * Animation 4 : Slide In (Lateral)
 * USAGE : Menus, modals
 */
@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.modal {
    animation: slideInRight 0.4s ease-out;
}

/* ====================================
   TRANSFORM COMPLET
   ==================================== */

/* 
 * transform: translate(x, y)
 * POURQUOI : Déplacer élément sans affecter layout
 * AVANTAGE : Performant (GPU accéléré)
 */
.translate-example {
    /* 
     * translateX(100px) : Droite 100px
     * translateY(-50px) : Haut 50px
     * translate(100px, -50px) : Droite 100px + Haut 50px
     */
    transform: translate(100px, -50px);
}

/* 
 * transform: scale(x, y)
 * POURQUOI : Agrandir/rétrécir
 */
.scale-example {
    /* 
     * scale(1.5) : Agrandit 150%
     * scale(0.5) : Rétrécit 50%
     * scale(1.2, 0.8) : Largeur 120%, Hauteur 80%
     */
    transform: scale(1.5);
}

/* 
 * transform: rotate(angle)
 * POURQUOI : Rotation
 */
.rotate-example {
    /* 
     * rotate(45deg) : 45 degrés sens horaire
     * rotate(-45deg) : 45 degrés sens antihoraire
     * rotate(180deg) : Demi-tour
     */
    transform: rotate(45deg);
}

/* 
 * transform: skew(x, y)
 * POURQUOI : Distorsion (peu utilisé)
 */
.skew-example {
    transform: skew(20deg, 10deg);
}

/* 
 * COMBINER TRANSFORMS
 * ORDRE IMPORTANT : translate → rotate → scale
 */
.transform-combined {
    /* 
     * POURQUOI cet ordre :
     * 1. translate : Déplace
     * 2. rotate : Pivote autour nouveau centre
     * 3. scale : Agrandi depuis nouveau centre
     */
    transform: translate(50px, -20px) rotate(15deg) scale(1.2);
}

/* ====================================
   CSS NOUVEAUTÉS 2024-2025
   ==================================== */

/* 
 * 1. CONTAINER QUERIES (alternative media queries)
 * POURQUOI : Responsive basé sur container parent, pas viewport
 * SUPPORT : Chrome 105+, Firefox 110+, Safari 16+
 */
.container-query-example {
    /* 
     * container-type: inline-size
     * POURQUOI : Active container queries sur cet élément
     * inline-size = largeur (horizontal)
     */
    container-type: inline-size;
}

/* 
 * @container (min-width: 400px)
 * POURQUOI : Style si CONTAINER > 400px (pas viewport)
 * USAGE : Component responsive indépendant du viewport
 */
@container (min-width: 400px) {
    .card-inside-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
    }
}

/* 
 * 2. :HAS() - "Parent selector"
 * POURQUOI : Styler parent selon enfant
 * SUPPORT : Chrome 105+, Firefox 121+, Safari 15.4+
 */

/* 
 * Exemple : Card avec image OU sans image
 */
.card:has(img) {
    /* 
     * Si card CONTIENT img → padding différent
     * AVANT : Impossible en CSS pur (fallait JS)
     * MAINTENANT : :has() le fait
     */
    padding: 0;
}

.card:not(:has(img)) {
    /* 
     * Si card N'A PAS img → padding standard
     */
    padding: 2rem;
}

/* 
 * Exemple : Form validation visuelle
 */
.form-group:has(input:invalid) label {
    /* 
     * Si input invalide → label rouge
     * POURQUOI : Feedback visuel parent selon enfant
     */
    color: var(--color-danger);
}

/* 
 * 3. ACCENT-COLOR (Inputs natifs)
 * POURQUOI : Colorer checkboxes/radios/range sans CSS complexe
 * SUPPORT : Chrome 93+, Firefox 92+, Safari 15.4+
 */
input[type="checkbox"],
input[type="radio"],
input[type="range"] {
    /* 
     * accent-color: var(--color-primary)
     * POURQUOI : Checkbox/radio couleur brand
     * AVANT : Custom CSS complexe
     * MAINTENANT : 1 ligne
     */
    accent-color: var(--color-primary);
}

/* 
 * 4. SCROLL-SNAP (Carousel smooth)
 * POURQUOI : Snap scroll sur éléments (slider natif)
 * SUPPORT : Tous navigateurs modernes
 */
.testimonials-slider {
    /* 
     * scroll-snap-type: x mandatory
     * DÉCOMPOSITION :
     * - x : Axe horizontal
     * - mandatory : Force snap (toujours aligné)
     * 
     * ALTERNATIVES :
     * - proximity : Snap si proche
     * - mandatory : Force snap
     */
    scroll-snap-type: x mandatory;
    
    /* 
     * overflow-x: scroll
     * scrollbar-width: none (Firefox)
     * POURQUOI : Scroll horizontal sans scrollbar visible
     */
    overflow-x: scroll;
    scrollbar-width: none; /* Firefox */
    
    display: flex;
    gap: 2rem;
}

.testimonials-slider::-webkit-scrollbar {
    /* 
     * Cacher scrollbar Chrome/Safari
     */
    display: none;
}

.testimonial-card {
    /* 
     * scroll-snap-align: center
     * POURQUOI : Card s'aligne au centre lors scroll
     * VALEURS :
     * - start : Align début
     * - center : Align centre
     * - end : Align fin
     */
    scroll-snap-align: center;
    
    /* 
     * scroll-snap-stop: always
     * POURQUOI : Force arrêt sur chaque card
     * DÉFAUT : normal (peut skip cards)
     */
    scroll-snap-stop: always;
    
    flex: 0 0 80%; /* Largeur fixe 80% */
}

/* 
 * 5. ASPECT-RATIO (Ratio image/video)
 * POURQUOI : Maintenir ratio sans padding-bottom hack
 * SUPPORT : Tous navigateurs modernes
 */
.project-image {
    /* 
     * aspect-ratio: 16 / 9
     * POURQUOI : Force ratio 16:9
     * AVANT : padding-bottom: 56.25% (hack)
     * MAINTENANT : aspect-ratio (natif)
     * 
     * EXEMPLES :
     * - 16/9 : Vidéo landscape
     * - 4/3 : Photo classique
     * - 1/1 : Carré (Instagram)
     * - 9/16 : Vidéo portrait (TikTok)
     */
    aspect-ratio: 16 / 9;
    object-fit: cover;
}

/* 
 * 6. CLAMP() - Responsive fluide
 * POURQUOI : Taille min/préférée/max en 1 ligne
 * SUPPORT : Tous navigateurs modernes
 */
.hero-title {
    /* 
     * font-size: clamp(2rem, 5vw, 4rem)
     * SYNTAXE : clamp(MIN, PRÉFÉRÉ, MAX)
     * 
     * DÉCOMPOSITION :
     * - MIN : 2rem (32px) - Mobile
     * - PRÉFÉRÉ : 5vw (5% viewport width) - Fluide
     * - MAX : 4rem (64px) - Desktop
     * 
     * EFFET :
     * - Viewport 320px : 2rem (min)
     * - Viewport 800px : 5vw = 40px (entre min/max)
     * - Viewport 1920px : 4rem (max)
     * 
     * AVANT : Media queries multiples
     * MAINTENANT : 1 ligne clamp()
     */
    font-size: clamp(2rem, 5vw, 4rem);
}

.section-title {
    /* 
     * Responsive spacing fluide
     */
    margin-bottom: clamp(1.5rem, 3vw, 3rem);
}
```

### 6.2 Compteurs Animés JavaScript

**Fichier :** `js/main.js`

```javascript
/**
 * Compteurs animés avec Intersection Observer
 * POURQUOI : Anime compteurs quand visibles
 */

// Fonction animation compteur
function animateCounter(element) {
    // Target final
    const target = parseInt(element.dataset.target);
    
    // Durée animation (2 secondes)
    const duration = 2000;
    
    // Nombre steps (60 FPS = 120 steps pour 2s)
    const steps = 120;
    
    // Incrément par step
    const increment = target / steps;
    
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, duration / steps);
}

// Intersection Observer pour détecter scroll
const observerOptions = {
    threshold: 0.5  // 50% visible
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Élément visible → animer
            const counters = entry.target.querySelectorAll('.stat-number');
            counters.forEach(counter => animateCounter(counter));
            
            // Observer une seule fois
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observer section stats
const statsSection = document.querySelector('.stats');
if (statsSection) {
    observer.observe(statsSection);
}
```

### Checkpoint Phase 6

- ✅ Transitions maîtrisées (hover effects)
- ✅ @keyframes animations créées
- ✅ Transform complet (translate, scale, rotate)
- ✅ CSS nouveautés 2024-2025
- ✅ Compteurs animés JavaScript

---

## Phase 7 : Portfolio Complet & JavaScript (2h)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2 heures"></div>

### Objectifs Phase 7

- ✅ Sections CSS complètes
- ✅ Burger menu mobile
- ✅ Filtres projets JavaScript
- ✅ Carrousel testimonials
- ✅ Form validation

### 7.1 Sections CSS Complètes

**Fichier :** `css/sections.css`

```css
/* ====================================
   HERO SECTION
   ==================================== */

.hero {
    /* 
     * min-height: 100vh
     * POURQUOI : Prend toute hauteur viewport
     * vh = viewport height (100vh = 100% écran)
     */
    min-height: 100vh;
    
    /* 
     * display: flex
     * POURQUOI : Centrer contenu verticalement
     */
    display: flex;
    align-items: center;
    justify-content: center;
    
    /* 
     * background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
     * POURQUOI : Fond dégradé moderne
     * SYNTAXE : linear-gradient(angle, color1 stop%, color2 stop%)
     * 
     * ANGLES :
     * - 0deg : Bas→Haut
     * - 90deg : Gauche→Droite
     * - 135deg : Diagonale
     * - 180deg : Haut→Bas
     */
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    
    /* 
     * position: relative
     * POURQUOI : Positionner scroll indicator en absolu
     */
    position: relative;
    
    color: white;
    text-align: center;
}

.hero-title {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    margin-bottom: 1.5rem;
    
    /* 
     * Animation cascade (Phase 6)
     */
    animation: fadeInUp 1s ease-out;
}

.highlight {
    /* 
     * background: linear-gradient(...)
     * -webkit-background-clip: text
     * -webkit-text-fill-color: transparent
     * 
     * POURQUOI : Texte gradient (effet moderne)
     * TRICK : Background clip sur texte + fill transparent
     */
    background: linear-gradient(90deg, #ffd700 0%, #ff6b6b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: clamp(1rem, 2vw, 1.25rem);
    margin-bottom: 2rem;
    opacity: 0.9;
    animation: fadeInUp 1s ease-out 0.2s backwards;
}

.hero-cta {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    animation: fadeInUp 1s ease-out 0.4s backwards;
}

.scroll-indicator {
    /* 
     * position: absolute
     * bottom: 2rem
     * left: 50%
     * transform: translateX(-50%)
     * POURQUOI : Centrer horizontalement en absolute
     */
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    
    font-size: 2rem;
    color: white;
    
    /* 
     * Animation pulse (Phase 6)
     */
    animation: pulse 2s ease-in-out infinite;
}

/* ====================================
   STATS SECTION
   ==================================== */

.stats {
    padding: 4rem 0;
    background: var(--color-gray-50);
}

.stat-number {
    /* 
     * font-size: 3rem
     * font-weight: 700
     * POURQUOI : Gros chiffres impactants
     */
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    color: var(--color-primary);
    display: block;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: var(--font-size-sm);
    color: var(--color-text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ====================================
   SERVICES SECTION
   ==================================== */

.services {
    padding: 6rem 0;
}

.section-title {
    font-size: clamp(2rem, 4vw, 3rem);
    text-align: center;
    margin-bottom: 1rem;
}

.section-subtitle {
    text-align: center;
    color: var(--color-text-secondary);
    margin-bottom: 4rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.service-icon {
    /* 
     * font-size: 3rem
     * POURQUOI : Emoji icône grosse visible
     */
    font-size: 3rem;
    margin-bottom: 1rem;
}

/* ====================================
   PORTFOLIO SECTION
   ==================================== */

.portfolio {
    padding: 6rem 0;
    background: var(--color-gray-50);
}

.portfolio-filters {
    /* 
     * display: flex
     * justify-content: center
     * POURQUOI : Centrer boutons filtres
     */
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}

.filter-btn {
    padding: 0.75rem 1.5rem;
    background: white;
    border: 2px solid var(--color-gray-200);
    border-radius: var(--radius-md);
    font-weight: 500;
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.filter-btn:hover {
    border-color: var(--color-primary);
    color: var(--color-primary);
}

.filter-btn.active {
    background: var(--color-primary);
    border-color: var(--color-primary);
    color: white;
}

.project-card {
    /* 
     * transition: opacity 0.3s, transform 0.3s
     * POURQUOI : Animation filtres (fade out/in)
     */
    transition: opacity 0.3s, transform 0.3s;
}

.project-card.hidden {
    /* 
     * opacity: 0
     * transform: scale(0.8)
     * POURQUOI : Cache projets filtrés avec animation
     */
    opacity: 0;
    transform: scale(0.8);
    
    /* 
     * pointer-events: none
     * POURQUOI : Désactive interactions
     */
    pointer-events: none;
}

/* ====================================
   TESTIMONIALS SECTION
   ==================================== */

.testimonials {
    padding: 6rem 0;
}

.testimonial-card {
    background: white;
    padding: 3rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-lg);
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
}

.testimonial-text {
    font-size: var(--font-size-lg);
    font-style: italic;
    color: var(--color-text-secondary);
    margin-bottom: 2rem;
    line-height: 1.8;
}

.testimonial-author {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}

.testimonial-author img {
    /* 
     * width/height: 60px
     * border-radius: 50%
     * POURQUOI : Photo circulaire auteur
     */
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
}

.testimonials-dots {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 2rem;
}

.dot {
    /* 
     * width/height: 12px
     * border-radius: 50%
     * POURQUOI : Dots navigation carrousel
     */
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--color-gray-300);
    border: none;
    cursor: pointer;
    transition: background var(--transition-fast);
}

.dot.active {
    background: var(--color-primary);
    
    /* 
     * transform: scale(1.2)
     * POURQUOI : Dot actif plus gros
     */
    transform: scale(1.2);
}

/* ====================================
   CONTACT SECTION
   ==================================== */

.contact {
    padding: 6rem 0;
    background: var(--color-gray-50);
}

.contact-form {
    background: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    /* 
     * display: block
     * POURQUOI : Label sur ligne complète
     */
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--color-text-primary);
}

.form-group input,
.form-group textarea {
    /* 
     * width: 100%
     * POURQUOI : Input pleine largeur
     */
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid var(--color-gray-200);
    border-radius: var(--radius-md);
    font-family: inherit;
    font-size: var(--font-size-base);
    transition: border-color var(--transition-fast);
}

.form-group input:focus,
.form-group textarea:focus {
    /* 
     * outline: none
     * border-color: var(--color-primary)
     * POURQUOI : Focus visible sans outline navigateur
     */
    outline: none;
    border-color: var(--color-primary);
}

.form-group input:invalid:not(:placeholder-shown) {
    /* 
     * :invalid:not(:placeholder-shown)
     * POURQUOI : Rouge seulement si rempli ET invalide
     * ÉVITE : Rouge avant saisie
     */
    border-color: var(--color-danger);
}

.contact-info {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.contact-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.contact-icon {
    font-size: 2rem;
}
```

### 7.2 JavaScript Interactions

**Fichier :** `js/main.js` (complet)

```javascript
/**
 * BURGER MENU MOBILE
 */
const burger = document.querySelector('.burger');
const navMenu = document.querySelector('.nav-menu');

if (burger && navMenu) {
    burger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        burger.classList.toggle('active');
    });
    
    // Fermer menu au clic lien
    navMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            burger.classList.remove('active');
        });
    });
}

/**
 * SMOOTH SCROLL
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/**
 * NAVBAR STICKY AVEC OMBRE
 */
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});
```

**Fichier :** `js/filters.js`

```javascript
/**
 * FILTRES PROJETS
 */
const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Activer bouton
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        // Filtrer projets
        const filter = button.dataset.filter;
        
        projectCards.forEach(card => {
            if (filter === 'all' || card.dataset.category === filter) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    });
});

/**
 * CARROUSEL TESTIMONIALS
 */
const testimonials = document.querySelectorAll('.testimonial-card');
const dots = document.querySelectorAll('.dot');
let currentIndex = 0;

function showTestimonial(index) {
    // Cacher tous
    testimonials.forEach(t => t.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));
    
    // Afficher actuel
    testimonials[index].classList.add('active');
    dots[index].classList.add('active');
}

// Navigation dots
dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        currentIndex = index;
        showTestimonial(currentIndex);
    });
});

// Auto-rotate (optionnel)
setInterval(() => {
    currentIndex = (currentIndex + 1) % testimonials.length;
    showTestimonial(currentIndex);
}, 5000); // 5 secondes
```

### Checkpoint Phase 7

- ✅ Toutes sections CSS complètes
- ✅ Burger menu fonctionnel
- ✅ Filtres projets JavaScript
- ✅ Carrousel testimonials
- ✅ Smooth scroll implémenté

---

*Je continue avec Phase 8 (Tailwind) dans le prochain message...*

## Phase 8 : Tailwind CSS Refactor (2h)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2 heures"></div>

### Objectifs Phase 8

- ✅ Comprendre Tailwind = utility-first CSS
- ✅ Installation & configuration
- ✅ Comparaison CSS pur vs Tailwind
- ✅ Refactor portfolio complet
- ✅ Avantages & inconvénients

### 8.1 Tailwind CSS : Concept

**QUOI :** Tailwind = framework CSS utility-first  
**POURQUOI :** Classes utilitaires au lieu de CSS custom  
**PHILOSOPHIE :** Composer styles avec classes atomiques

**Comparaison :**

```html
<!-- CSS PUR (Phase 1-7) -->
<div class="service-card">
    <h3>Design UI/UX</h3>
</div>

<style>
.service-card {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
</style>

<!-- TAILWIND CSS -->
<div class="bg-white p-8 rounded-2xl shadow-md">
    <h3>Design UI/UX</h3>
</div>

<!-- AUCUN CSS custom nécessaire -->
```

**Avantages Tailwind :**
- ✅ Pas de naming CSS (plus de `.service-card`)
- ✅ Pas de context switching (HTML → CSS → HTML)
- ✅ Purge automatique (supprime classes non utilisées)
- ✅ Cohérence design (palette prédéfinie)
- ✅ Responsive facile (`md:flex lg:grid`)

**Inconvénients Tailwind :**
- ❌ HTML "verbeux" (beaucoup de classes)
- ❌ Courbe apprentissage (mémoriser classes)
- ❌ Répétition (même classes partout)
- ❌ Debug difficile (classes longues)

### 8.2 Installation Tailwind

**Via CDN (développement rapide) :**

```html
<!-- index-tailwind.html -->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio - Tailwind CSS</title>
    
    <!-- Tailwind CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Configuration inline -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#6366f1',
                        secondary: '#8b5cf6'
                    }
                }
            }
        }
    </script>
</head>
<body>
    <!-- Contenu Tailwind -->
</body>
</html>
```

**Via NPM (production) :**

```bash
# 1. Initialiser projet
npm init -y

# 2. Installer Tailwind
npm install -D tailwindcss

# 3. Initialiser config
npx tailwindcss init

# 4. Configurer tailwind.config.js
# 5. Créer input.css avec @tailwind directives
# 6. Compiler : npx tailwindcss -i input.css -o output.css --watch
```

**Fichier :** `tailwind.config.js`

```javascript
module.exports = {
    // Fichiers à scanner pour classes
    content: ["./src/**/*.{html,js}"],
    
    theme: {
        extend: {
            // Colors custom
            colors: {
                primary: {
                    DEFAULT: '#6366f1',
                    dark: '#4f46e5',
                    light: '#818cf8'
                }
            },
            
            // Spacing custom
            spacing: {
                '128': '32rem'
            },
            
            // Fonts custom
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif']
            }
        }
    },
    
    plugins: []
}
```

### 8.3 Comparaison CSS Pur vs Tailwind

**Exemple 1 : Navbar**

```html
<!-- ====================================
     CSS PUR (Phase 3)
     ==================================== -->

<nav class="navbar">
    <div class="container">
        <a href="#home" class="logo">JD</a>
        <ul class="nav-menu">
            <li><a href="#about">À propos</a></li>
            <li><a href="#services">Services</a></li>
        </ul>
    </div>
</nav>

<style>
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.nav-menu {
    display: flex;
    gap: 2rem;
}

.nav-menu a {
    color: #374151;
    font-weight: 500;
    transition: color 0.3s;
}

.nav-menu a:hover {
    color: #6366f1;
}
</style>

<!-- ====================================
     TAILWIND CSS
     ==================================== -->

<nav class="flex justify-between items-center px-8 py-4 bg-white shadow-md">
    <a href="#home" class="text-2xl font-bold text-primary">JD</a>
    <ul class="flex gap-8">
        <li>
            <a href="#about" 
               class="text-gray-700 font-medium hover:text-primary transition">
                À propos
            </a>
        </li>
        <li>
            <a href="#services" 
               class="text-gray-700 font-medium hover:text-primary transition">
                Services
            </a>
        </li>
    </ul>
</nav>

<!-- AUCUN CSS custom ! -->
```

**Décodage classes Tailwind :**

| Classe Tailwind | Équivalent CSS | Explication |
|-----------------|---------------|-------------|
| `flex` | `display: flex` | Active Flexbox |
| `justify-between` | `justify-content: space-between` | Espace entre items |
| `items-center` | `align-items: center` | Centre vertical |
| `px-8` | `padding-left/right: 2rem` | Padding horizontal |
| `py-4` | `padding-top/bottom: 1rem` | Padding vertical |
| `bg-white` | `background: white` | Fond blanc |
| `shadow-md` | `box-shadow: 0 4px 6px rgba(0,0,0,0.1)` | Ombre moyenne |
| `text-gray-700` | `color: #374151` | Texte gris |
| `font-medium` | `font-weight: 500` | Poids moyen |
| `hover:text-primary` | `.hover:text-primary:hover { color: primary }` | Hover couleur |
| `transition` | `transition: all 0.3s` | Transition |

**Exemple 2 : Hero Section**

```html
<!-- ====================================
     CSS PUR
     ==================================== -->

<section class="hero">
    <div class="container">
        <h1 class="hero-title">
            Bonjour, je suis <span class="highlight">John Doe</span>
        </h1>
        <p class="hero-subtitle">
            Développeur Full-Stack
        </p>
        <div class="hero-cta">
            <a href="#portfolio" class="btn btn-primary">Voir mes projets</a>
            <a href="#contact" class="btn btn-secondary">Me contacter</a>
        </div>
    </div>
</section>

<style>
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
}

.hero-title {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    margin-bottom: 1.5rem;
}

.btn {
    padding: 1rem 2rem;
    border-radius: 0.5rem;
    font-weight: 600;
    transition: all 0.3s;
}

.btn-primary {
    background: #6366f1;
    color: white;
}

.btn-primary:hover {
    background: #4f46e5;
    transform: translateY(-2px);
}
</style>

<!-- ====================================
     TAILWIND CSS
     ==================================== -->

<section class="min-h-screen flex items-center justify-center 
                bg-gradient-to-br from-indigo-500 to-purple-600 
                text-white text-center">
    <div class="container mx-auto px-8">
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
            Bonjour, je suis 
            <span class="bg-gradient-to-r from-yellow-400 to-red-400 
                         bg-clip-text text-transparent">
                John Doe
            </span>
        </h1>
        
        <p class="text-lg md:text-xl mb-8 opacity-90">
            Développeur Full-Stack
        </p>
        
        <div class="flex gap-4 justify-center flex-wrap">
            <a href="#portfolio" 
               class="px-8 py-4 bg-indigo-600 rounded-lg font-semibold
                      hover:bg-indigo-700 hover:-translate-y-1 
                      transition transform">
                Voir mes projets
            </a>
            
            <a href="#contact" 
               class="px-8 py-4 bg-white text-indigo-600 rounded-lg font-semibold
                      hover:bg-gray-100 hover:-translate-y-1 
                      transition transform">
                Me contacter
            </a>
        </div>
    </div>
</section>
```

**Classes Tailwind responsive :**

| Classe | Breakpoint | CSS équivalent |
|--------|-----------|---------------|
| `text-4xl` | Mobile | `font-size: 2.25rem` |
| `md:text-5xl` | ≥768px | `font-size: 3rem` |
| `lg:text-6xl` | ≥1024px | `font-size: 3.75rem` |

**Préfixes Tailwind :**

| Préfixe | Usage | Exemple |
|---------|-------|---------|
| `hover:` | Hover | `hover:bg-blue-600` |
| `focus:` | Focus | `focus:ring-2` |
| `active:` | Active | `active:scale-95` |
| `md:` | Tablette (≥768px) | `md:flex` |
| `lg:` | Desktop (≥1024px) | `lg:grid-cols-3` |
| `dark:` | Dark mode | `dark:bg-gray-900` |

**Exemple 3 : Services Grid**

```html
<!-- ====================================
     CSS PUR
     ==================================== -->

<div class="services-grid">
    <article class="service-card">
        <div class="service-icon">🎨</div>
        <h3>Design UI/UX</h3>
        <p>Interfaces modernes et intuitives</p>
    </article>
    
    <!-- 2 autres cards -->
</div>

<style>
.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.service-card {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.service-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 25px rgba(0,0,0,0.1);
}
</style>

<!-- ====================================
     TAILWIND CSS
     ==================================== -->

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
    <article class="bg-white p-8 rounded-2xl shadow-md 
                    hover:-translate-y-3 hover:shadow-xl 
                    transition-all duration-300">
        <div class="text-5xl mb-4">🎨</div>
        <h3 class="text-xl font-bold mb-2">Design UI/UX</h3>
        <p class="text-gray-600">Interfaces modernes et intuitives</p>
    </article>
    
    <!-- 2 autres cards identiques -->
</div>
```

**Grid Tailwind :**

| Classe | CSS équivalent | Usage |
|--------|---------------|-------|
| `grid` | `display: grid` | Active Grid |
| `grid-cols-1` | `grid-template-columns: repeat(1, 1fr)` | 1 colonne mobile |
| `md:grid-cols-2` | `grid-template-columns: repeat(2, 1fr)` | 2 colonnes tablette |
| `lg:grid-cols-3` | `grid-template-columns: repeat(3, 1fr)` | 3 colonnes desktop |
| `gap-8` | `gap: 2rem` | Espacement 2rem |

### 8.4 Portfolio Complet Tailwind

**Fichier :** `index-tailwind.html` (extrait)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio - Tailwind CSS</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="font-sans text-gray-900">
    
    <!-- NAVBAR TAILWIND -->
    <nav class="sticky top-0 z-50 bg-white shadow-md">
        <div class="container mx-auto px-8 py-4 flex justify-between items-center">
            <a href="#home" class="text-2xl font-bold text-indigo-600">JD</a>
            
            <ul class="hidden md:flex gap-8">
                <li>
                    <a href="#home" 
                       class="text-gray-700 font-medium hover:text-indigo-600 transition">
                        Accueil
                    </a>
                </li>
                <li>
                    <a href="#services" 
                       class="text-gray-700 font-medium hover:text-indigo-600 transition">
                        Services
                    </a>
                </li>
                <li>
                    <a href="#portfolio" 
                       class="text-gray-700 font-medium hover:text-indigo-600 transition">
                        Portfolio
                    </a>
                </li>
                <li>
                    <a href="#contact" 
                       class="text-gray-700 font-medium hover:text-indigo-600 transition">
                        Contact
                    </a>
                </li>
            </ul>
            
            <!-- Burger mobile -->
            <button class="md:hidden flex flex-col gap-1">
                <span class="w-6 h-0.5 bg-gray-900"></span>
                <span class="w-6 h-0.5 bg-gray-900"></span>
                <span class="w-6 h-0.5 bg-gray-900"></span>
            </button>
        </div>
    </nav>
    
    <!-- HERO SECTION TAILWIND -->
    <section id="home" 
             class="min-h-screen flex items-center justify-center 
                    bg-gradient-to-br from-indigo-500 via-purple-500 to-purple-700 
                    text-white text-center">
        <div class="container mx-auto px-8">
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 
                       animate-fade-in-up">
                Bonjour, je suis 
                <span class="bg-gradient-to-r from-yellow-300 to-red-400 
                             bg-clip-text text-transparent">
                    John Doe
                </span>
            </h1>
            
            <p class="text-lg md:text-xl lg:text-2xl mb-8 opacity-90 
                      animate-fade-in-up animation-delay-200">
                Développeur Full-Stack passionné par la création d'expériences web exceptionnelles
            </p>
            
            <div class="flex gap-4 justify-center flex-wrap 
                        animate-fade-in-up animation-delay-400">
                <a href="#portfolio" 
                   class="px-8 py-4 bg-indigo-600 rounded-lg font-semibold 
                          hover:bg-indigo-700 hover:-translate-y-1 
                          transition-all transform shadow-lg">
                    Voir mes projets
                </a>
                
                <a href="#contact" 
                   class="px-8 py-4 bg-white text-indigo-600 rounded-lg font-semibold 
                          hover:bg-gray-100 hover:-translate-y-1 
                          transition-all transform shadow-lg">
                    Me contacter
                </a>
            </div>
        </div>
    </section>
    
    <!-- STATS SECTION TAILWIND -->
    <section class="py-16 bg-gray-50">
        <div class="container mx-auto px-8">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
                <div>
                    <div class="text-4xl md:text-5xl font-bold text-indigo-600 mb-2">
                        150+
                    </div>
                    <div class="text-sm text-gray-600 uppercase tracking-wide">
                        Projets Réalisés
                    </div>
                </div>
                
                <div>
                    <div class="text-4xl md:text-5xl font-bold text-indigo-600 mb-2">
                        500+
                    </div>
                    <div class="text-sm text-gray-600 uppercase tracking-wide">
                        Cafés Bus
                    </div>
                </div>
                
                <div>
                    <div class="text-4xl md:text-5xl font-bold text-indigo-600 mb-2">
                        50+
                    </div>
                    <div class="text-sm text-gray-600 uppercase tracking-wide">
                        Clients Satisfaits
                    </div>
                </div>
                
                <div>
                    <div class="text-4xl md:text-5xl font-bold text-indigo-600 mb-2">
                        98%
                    </div>
                    <div class="text-sm text-gray-600 uppercase tracking-wide">
                        Satisfaction
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- SERVICES SECTION TAILWIND -->
    <section id="services" class="py-24">
        <div class="container mx-auto px-8">
            <h2 class="text-3xl md:text-4xl font-bold text-center mb-4">
                Ce que je propose
            </h2>
            <p class="text-center text-gray-600 mb-16 max-w-2xl mx-auto">
                Des solutions complètes pour vos projets web
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Service Card 1 -->
                <article class="bg-white p-8 rounded-2xl shadow-md 
                                hover:-translate-y-3 hover:shadow-xl 
                                transition-all duration-300">
                    <div class="text-5xl mb-4">🎨</div>
                    <h3 class="text-xl font-bold mb-2">Design UI/UX</h3>
                    <p class="text-gray-600">
                        Création d'interfaces modernes et intuitives 
                        pour une expérience utilisateur optimale.
                    </p>
                </article>
                
                <!-- Service Card 2 -->
                <article class="bg-white p-8 rounded-2xl shadow-md 
                                hover:-translate-y-3 hover:shadow-xl 
                                transition-all duration-300">
                    <div class="text-5xl mb-4">💻</div>
                    <h3 class="text-xl font-bold mb-2">Développement Web</h3>
                    <p class="text-gray-600">
                        Applications web performantes avec PHP, Python 
                        et JavaScript (React, Vue, Angular).
                    </p>
                </article>
                
                <!-- Service Card 3 -->
                <article class="bg-white p-8 rounded-2xl shadow-md 
                                hover:-translate-y-3 hover:shadow-xl 
                                transition-all duration-300">
                    <div class="text-5xl mb-4">🚀</div>
                    <h3 class="text-xl font-bold mb-2">Déploiement & DevOps</h3>
                    <p class="text-gray-600">
                        Mise en production avec Docker, CI/CD et 
                        monitoring pour une disponibilité maximale.
                    </p>
                </article>
            </div>
        </div>
    </section>
    
    <!-- PORTFOLIO SECTION TAILWIND -->
    <section id="portfolio" class="py-24 bg-gray-50">
        <div class="container mx-auto px-8">
            <h2 class="text-3xl md:text-4xl font-bold text-center mb-16">
                Mes Projets
            </h2>
            
            <!-- Filtres -->
            <div class="flex justify-center gap-4 mb-12 flex-wrap">
                <button class="px-6 py-2 bg-indigo-600 text-white rounded-lg 
                               font-medium hover:bg-indigo-700 transition">
                    Tous
                </button>
                <button class="px-6 py-2 bg-white border-2 border-gray-200 rounded-lg 
                               font-medium hover:border-indigo-600 hover:text-indigo-600 transition">
                    Web
                </button>
                <button class="px-6 py-2 bg-white border-2 border-gray-200 rounded-lg 
                               font-medium hover:border-indigo-600 hover:text-indigo-600 transition">
                    Mobile
                </button>
                <button class="px-6 py-2 bg-white border-2 border-gray-200 rounded-lg 
                               font-medium hover:border-indigo-600 hover:text-indigo-600 transition">
                    Design
                </button>
            </div>
            
            <!-- Grille projets -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Project Card -->
                <article class="group relative overflow-hidden rounded-2xl shadow-lg 
                                hover:shadow-2xl transition-shadow cursor-pointer">
                    <img src="https://via.placeholder.com/600x400" 
                         alt="Projet" 
                         class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-500">
                    
                    <div class="absolute inset-0 bg-black bg-opacity-80 
                                flex flex-col items-center justify-center 
                                opacity-0 group-hover:opacity-100 transition-opacity">
                        <h3 class="text-white text-2xl font-bold mb-2">E-commerce Platform</h3>
                        <p class="text-gray-300 mb-4">Laravel + Vue.js</p>
                        <a href="#" 
                           class="px-6 py-2 bg-indigo-600 text-white rounded-lg 
                                  hover:bg-indigo-700 transition">
                            Voir le projet
                        </a>
                    </div>
                </article>
                
                <!-- Répéter pour 6 projets -->
            </div>
        </div>
    </section>
    
    <!-- CONTACT SECTION TAILWIND -->
    <section id="contact" class="py-24">
        <div class="container mx-auto px-8">
            <h2 class="text-3xl md:text-4xl font-bold text-center mb-16">
                Travaillons ensemble
            </h2>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-12 max-w-6xl mx-auto">
                <!-- Formulaire -->
                <form class="lg:col-span-2 bg-white p-8 rounded-2xl shadow-lg">
                    <div class="mb-6">
                        <label class="block text-gray-700 font-medium mb-2">
                            Nom complet
                        </label>
                        <input type="text" 
                               class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg 
                                      focus:border-indigo-600 focus:outline-none transition"
                               placeholder="John Doe">
                    </div>
                    
                    <div class="mb-6">
                        <label class="block text-gray-700 font-medium mb-2">
                            Email
                        </label>
                        <input type="email" 
                               class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg 
                                      focus:border-indigo-600 focus:outline-none transition"
                               placeholder="john@example.com">
                    </div>
                    
                    <div class="mb-6">
                        <label class="block text-gray-700 font-medium mb-2">
                            Message
                        </label>
                        <textarea rows="5" 
                                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg 
                                         focus:border-indigo-600 focus:outline-none transition"
                                  placeholder="Décrivez votre projet..."></textarea>
                    </div>
                    
                    <button type="submit" 
                            class="w-full px-8 py-4 bg-indigo-600 text-white rounded-lg font-semibold 
                                   hover:bg-indigo-700 transition">
                        Envoyer le message
                    </button>
                </form>
                
                <!-- Coordonnées -->
                <div class="flex flex-col gap-8">
                    <div class="flex items-start gap-4">
                        <div class="text-4xl">📧</div>
                        <div>
                            <h4 class="font-bold mb-1">Email</h4>
                            <a href="mailto:john@example.com" 
                               class="text-indigo-600 hover:underline">
                                john@example.com
                            </a>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-4">
                        <div class="text-4xl">📱</div>
                        <div>
                            <h4 class="font-bold mb-1">Téléphone</h4>
                            <a href="tel:+33612345678" 
                               class="text-indigo-600 hover:underline">
                                +33 6 12 34 56 78
                            </a>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-4">
                        <div class="text-4xl">📍</div>
                        <div>
                            <h4 class="font-bold mb-1">Localisation</h4>
                            <p class="text-gray-600">Paris, France</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- FOOTER TAILWIND -->
    <footer class="bg-gray-900 text-white py-8">
        <div class="container mx-auto px-8 flex flex-col md:flex-row 
                    justify-between items-center gap-4">
            <p>&copy; 2025 John Doe. Tous droits réservés.</p>
            
            <div class="flex gap-6">
                <a href="#" class="hover:text-indigo-400 transition">GitHub</a>
                <a href="#" class="hover:text-indigo-400 transition">LinkedIn</a>
                <a href="#" class="hover:text-indigo-400 transition">Twitter</a>
            </div>
        </div>
    </footer>
    
</body>
</html>
```

### 8.5 Avantages & Inconvénients

**✅ AVANTAGES Tailwind :**

1. **Rapidité développement**
   - Pas de naming CSS (.card-title vs text-xl font-bold)
   - Pas de context switching (HTML ↔ CSS)
   - Prototypage ultra-rapide

2. **Cohérence design**
   - Palette couleurs prédéfinie (gray-50 à gray-900)
   - Échelle spacing cohérente (4, 8, 12, 16...)
   - Impossible de créer `padding: 23px` (force cohérence)

3. **Responsive facile**
   - `md:flex lg:grid` = 1 ligne vs media queries
   - Mobile-first natif

4. **Performance**
   - Purge automatique (supprime classes non utilisées)
   - CSS final léger (souvent < 10KB avec purge)

5. **Maintenance**
   - Modifier classe = changement immédiat
   - Pas de CSS "mort" (classes inutilisées)

**❌ INCONVÉNIENTS Tailwind :**

1. **HTML verbeux**
   ```html
   <!-- Beaucoup de classes -->
   <div class="flex items-center justify-between px-8 py-4 
               bg-white rounded-lg shadow-md hover:shadow-xl 
               transition-all duration-300">
   ```

2. **Courbe apprentissage**
   - Mémoriser 100+ classes
   - `justify-content: space-between` → `justify-between`

3. **Répétition**
   - Même classes sur chaque card
   - Solution : `@apply` (mais perd avantage Tailwind)

4. **Debug difficile**
   - Classes longues dans DevTools
   - Identifier problème moins évident

5. **Composants dupliqués**
   - Boutons identiques partout → répéter classes
   - Solution : Composants (React, Vue, Livewire)

### 8.6 Quand Utiliser CSS Pur vs Tailwind ?

| Critère | CSS Pur | Tailwind |
|---------|---------|----------|
| **Projet taille** | Petits projets | Moyens/Gros projets |
| **Équipe** | Solo/Petite | Grande équipe |
| **Design custom** | Très custom | Design system |
| **Rapidité** | Lent (nommer classes) | Rapide (utility classes) |
| **Maintenance** | Difficile (CSS mort) | Facile (purge auto) |
| **Apprentissage** | Besoin maîtriser CSS | Besoin apprendre Tailwind |

**RECOMMANDATION :**

- ✅ **CSS Pur** : Apprendre fondamentaux (ce guide !)
- ✅ **Tailwind** : Production avec équipe
- ✅ **Hybride** : CSS pur pour custom, Tailwind pour commun

### Checkpoint Phase 8

- ✅ Tailwind installé et configuré
- ✅ Comparaison CSS pur vs Tailwind
- ✅ Portfolio refactorisé en Tailwind
- ✅ Avantages/inconvénients compris
- ✅ Choix CSS pur vs Tailwind clair

---

## Conclusion

!!! success "HTML5 & CSS3 Maîtrisé - Portfolio Professionnel Complet"
    
    **17h formation • 8 phases • Portfolio responsive production-ready**
    
    Vous avez créé un portfolio complet avec TOUTES les explications CSS détaillées !

### Récapitulatif Compétences

**Phase 1 : HTML5 Sémantique**
- ✅ Structure complète (header, nav, main, section, article, footer)
- ✅ SEO meta tags
- ✅ Accessibilité (ARIA, alt, labels)

**Phase 2 : CSS Fondamentaux**
- ✅ Reset CSS (box-sizing, scroll-behavior)
- ✅ Variables CSS (custom properties)
- ✅ Échelles couleurs/espacements

**Phase 3 : Flexbox Expert**
- ✅ justify-content, align-items
- ✅ flex-wrap, gap, order
- ✅ Patterns communs (navbar, cards, centrage)

**Phase 4 : Grid Maître**
- ✅ grid-template-columns/rows
- ✅ grid-template-areas (layout nommé)
- ✅ auto-fit + minmax (responsive magique)

**Phase 5 : Responsive Design**
- ✅ Media queries maîtrisées
- ✅ Mobile-first approach
- ✅ Breakpoints cohérents

**Phase 6 : CSS Moderne & Animations**
- ✅ @keyframes animations
- ✅ transform (translate, scale, rotate)
- ✅ CSS 2024-2025 (container queries, :has(), aspect-ratio)
- ✅ Compteurs animés JavaScript

**Phase 7 : Portfolio Complet**
- ✅ Toutes sections CSS
- ✅ Burger menu mobile
- ✅ Filtres projets JavaScript
- ✅ Carrousel testimonials
- ✅ Form validation

**Phase 8 : Tailwind CSS**
- ✅ Comparaison CSS pur vs Tailwind
- ✅ Portfolio refactorisé
- ✅ Avantages/inconvénients
- ✅ Utility-first CSS

### Vous Êtes Prêt Pour

✅ **Tous les frameworks CSS** : Bootstrap, Bulma, etc.  
✅ **Frameworks JavaScript** : React, Vue, Angular (vous connaissez le CSS)  
✅ **Laravel + Tailwind** : Stack moderne  
✅ **Livewire** : Components Tailwind  
✅ **Projets professionnels** : Portfolio utilisable  

## Conclusion

!!! success "HTML/CSS Maîtrisé avec Portfolio Professionnel"
    Vous avez créé un portfolio responsive complet avec TOUTES les explications CSS détaillées !

### Compétences Acquises

✅ HTML5 sémantique complet  
✅ CSS Box Model maîtrisé  
✅ Flexbox expert (justify, align, wrap, gap)  
✅ Grid Layout complet (template, areas, auto-fit)  
✅ Responsive design mobile-first  
✅ Variables CSS (custom properties)  
✅ Animations & Transitions  
✅ CSS moderne 2025  
✅ Tailwind CSS integration  

**Vous êtes prêt pour TOUS les frameworks !** 🎨🚀

---

*Guide rédigé avec ❤️ pour la communauté web*  
*Version 1.0 - HTML5/CSS3 Modern - Décembre 2025*