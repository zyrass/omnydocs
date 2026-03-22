---
description: "Phase 4 : Modélisation des Services avec CSS Grid. Comprendre l'avantage de Grid vis à vis de Flexbox pour une liste d'éléments homogènes, et concevoir les cartes 'Cards'."
icon: lucide/layout-grid
tags: ["CSS", "GRID", "CARDS", "MODULARITY"]
status: stable
---

# Phase 4 : Grilles & Cartes de Services

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1h00">
</div>

!!! quote "Le Défi du Client"
    "C'est parfait, l'image héros attire l'œil. Mais le client doit tout de suite comprendre ce que l'on vend. Nous voulons nos 3 piliers (Design, Développement, Marketing) clairement affichés côte à côte sur ordinateur, mais mis les uns sous les autres sur un téléphone."

C'est ici que le grand duel **Flexbox VS Grid** entre en jeu. 
Vous pourriez utiliser Flexbox avec `flex-wrap: wrap`, mais la largeur des éléments enfants risquerait de devenir imprédictible (la dernière ligne pourrait avoir un seul élément étiré au maximum).
Avec **CSS Grid**, vous définissez la logique d'agencement sur le *Parent Container*. L'enfant (la Carte) n'a plus son mot à dire, il se conforme à la grille imposée.

## 1. Structure HTML Sémantique de la Section

Ceci se place toujours dans `index.html`, juste en dessous de la `<section class="hero">`.

```html
<!-- La balise section regroupe un thème -->
<section id="services" class="services section-padding">
  
  <div class="container">
    <div class="section-title">
      <h2>Nos Expertises</h2>
      <p>Des solutions sur mesure pour votre architecture digitale.</p>
    </div>

    <!-- LE CONTAINER GRID -->
    <div class="services-grid">
      
      <!-- CARTE N°1 -->
      <article class="card">
        <div class="card-icon">
          <!-- Icône SVG ou Image -->
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <h3>Design UX/UI</h3>
        <p>Interfaces pensées pour l'utilisateur, pixel-perfect et accessibles.</p>
      </article>

      <!-- CARTE N°2 -->
      <article class="card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M16 18L22 12 16 6M8 6L2 12 8 18"/>
          </svg>
        </div>
        <h3>Ingénierie Web</h3>
        <p>Architectures robustes Vanilla JS, React ou écosystèmes Vue.js.</p>
      </article>

      <!-- CARTE N°3 -->
      <article class="card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
          </svg>
        </div>
        <h3>Audit & SEO</h3>
        <p>Optimisation drastique des Core Web Vitals pour positionnement naturel.</p>
      </article>

    </div> <!-- /services-grid -->
  </div> <!-- /container -->
</section>
```

Remarquez les classes utilitaires : `.section-padding` et `.container`. Nous allons les coder dans CSS une seule fois pour garantir que plus jamais le texte ne touchera l'écran sur Mobile.

## 2. Définition des Utilitaires

Allez dans `style.css`. 

```css
/* --- UTILITAIRES DE STRUCTURE --- */

/* Appliqué à toutes les sections : un espace respire en haut et en bas */
.section-padding {
  padding: var(--spacing-xl) var(--spacing-lg);
}

/* Appliqué dans les sections : centre le bloc et évite de dépasser sur les grands écrans */
.container {
  max-width: 1200px; /* Sur un écran 4k, votre site ne s'étirera pas indéfiniment */
  margin: 0 auto; /* Magie : auto à gauche, auto à droite = Centrage */
}

/* Un titre de section universel */
.section-title {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}
.section-title h2 {
  font-size: 2.5rem;
  color: var(--color-dark);
  margin-bottom: var(--spacing-sm);
}
```

## 3. Le Container Grid (La Formule Magique 2D)

C'est là que réside le miracle mathématique de CSS Grid `repeat(auto-fit, minmax(...))`.

```css
/* --- LA GRILLE DES SERVICES --- */
.services-grid {
  display: grid;
  
  /* 
   * La Ligne Ultime :
   * Répète (repeat) des colonnes automatiquement selon l'espace (auto-fit).
   * Chaque colonne ne peut PAS faire moins de 300px, 
   * et ne peut PAS faire plus de 1 Fraction d'espace (1fr).
   * Résultat : Sur Téléphone, 300px prend presque tout l'écran => 1 colonne.
   * Sur Tablette (800px) => 2 colonnes rentrent.
   * Sur PC (1200px) => 3 colonnes rentrent. Zéro Media Queries !
   */
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  
  gap: var(--spacing-lg); /* Écarte uniformément les cartes */
}
```

## 4. Le Design des Composants (Les Cards)

Si la Grid est le chef d'orchestre, la Card est le musicien. Nous devons lui donner du volume et de l'intérêt visuel.

```css
/* LE SOCLE D'UNE CARTE GLOABALE */
.card {
  background-color: var(--color-light); /* Notre blanc cassé */
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  
  /* Lévitation douce lors du survol de la souris */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  
  /* On utilise un mini-flex interne si on veut pousser le texte en bas */
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--spacing-sm);
}

.card:hover {
  transform: translateY(-5px); /* Monte sur l'axe Y */
  box-shadow: 0 10px 15px rgba(0,0,0,0.1); /* Ombre plus diffuse */
}

/* Le design du bloc icône SVG */
.card-icon {
  width: 50px;
  height: 50px;
  background-color: var(--color-primary); /* Bleu fond */
  color: var(--color-light); /* SVG Dessin Blanc */
  border-radius: var(--radius-md);
  padding: 10px;
  margin-bottom: var(--spacing-sm);
}

.card h3 {
  font-size: 1.25rem;
  color: var(--color-dark);
}
```

## Checklist de la Phase 4

- [ ] Rétrécissez agressivement la fenêtre de votre navigateur Firefox / Chrome. Les cartes doivent passer d'un affichage de `3 -> 2 -> 1` colonne naturellement, **SANS le moindre défilement horizontal (scroll en bas)**.
- [ ] Survolez une des 3 cartes avec la souris. La carte lévite de `5px` vers le haut et l'ombre s'agrandit, créant la profondeur.
- [ ] La hiérarchie est respectée : Vous avez bien enveloppé vos 3 balises `article` à l'intérieur de LA balise div `.services-grid`.

**Félicitations.** Vous venez de valider que la Grid est idéale pour les **patterns réguliers**. Dans la phase suivante, nous affronterons le Portfolio et le Footer final, nécessitant l'utilisation du **CSS Object-Fit** pour détruire le cauchemar des images distordues.

[Passer à la Phase 5 : Portfolio & Résolution Finale →](phase5.md)
