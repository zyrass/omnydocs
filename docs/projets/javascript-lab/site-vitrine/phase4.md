---
description: "Phase 4 : Remplacement de l'HTML statique du Portfolio par une injection dynamique JavaScript depuis un tableau d'objets (Array) et création d'un système de filtres."
icon: lucide/filter
tags: ["JAVASCRIPT", "ARRAY", "MAP", "DOM", "TEMPLATES"]
status: stable
---

# Phase 4 : Injection DOM & Filtres Portfolio

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le client ajoute de nouveaux projets chaque mois à son Portfolio. En HTML statique, il faut copier-coller un bloc de 10 lignes à chaque fois pour l'ajouter, ce qui augmente le risque d'erreur humaine pour un Rédacteur Web. En JavaScript moderne, la donnée ("Data") est séparée de l'affichage ("Vue"). Nous allons détruire notre HTML pour laisser le JS peindre l'écran automatiquement à partir d'une liste de données.

## 1. Séparation de la Donnée (Les Datas)

Créez un dossier `src/data/` et ajoutez-y un fichier `projects.js`.
Ce fichier simulera le retour d'une base de données ou d'une API de Back-End Laravel.

```javascript
/* src/data/projects.js */

export const portfolioData = [
    {
        id: 1,
        title: "Plateforme SaaS B2B",
        category: "dev",
        image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=500&q=80",
    },
    {
        id: 2,
        title: "Identité Visuelle Startup",
        category: "design",
        image: "https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=500&q=80",
    },
    {
        id: 3,
        title: "Application Mobile Santé",
        category: "app",
        image: "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=500&q=80",
    },
    // Ajoutez-en 3 autres pour remplir la grille !
];
```

## 2. Nettoyage de la zone d'atterrissage (Landing Zone)

Allez dans `index.html`. Repérez votre section `#portfolio` et **supprimez toutes les balises internes `.portfolio-item`** ! Vous devez laisser absolument vierge le conteneur principal.
Rajoutons aussi des boutons pour notre futur filtre en haut de la grille.

```html
<!-- DANS INDEX.HTML -->
<div class="portfolio-filters">
    <!-- Le data-filter permettra à JS de savoir sur quoi l'humain a cliqué -->
    <button class="filter-btn active" data-filter="all">Tout</button>
    <button class="filter-btn" data-filter="design">Design</button>
    <button class="filter-btn" data-filter="dev">Développement</button>
    <button class="filter-btn" data-filter="app">Mobile</button>
</div>

<!-- LA ZONE VIDE QUE JS DOIT REMPLIR -->
<div class="portfolio-grid" id="portfolio-container">
    <!-- Le JS va injecter les cards ICI -->
</div>
```

## 3. Le Traceur : PortfolioManager.js

Dans `src/`, créez le module métier `portfolioHandler.js`.
Nous allons utiliser la boucle magique `.map()` couplée aux littéraux de gabarit (les backticks `` ` ``) inventés en ES6.

```javascript
/* src/portfolioHandler.js */
import { portfolioData } from './data/projects.js';

export function initPortfolio() {
    const container = document.getElementById('portfolio-container');
    const filterBtns = document.querySelectorAll('.filter-btn');

    if (!container) return; // Si la page n'a pas de portfolio, arrêt propre.

    // 1. Fonction Maîtresse : Dessiner depuis un tableau
    const renderProjects = (projectsArray) => {
        // La fonction .map() parcours le tableau d'Objets.
        // À chaque tour, (project) représente Un seul objet.
        const htmlContent = projectsArray.map(project => `
            <div class="portfolio-item">
                <img src="${project.image}" alt="${project.title}">
                <div class="portfolio-overlay">
                    <h3>${project.title}</h3>
                </div>
            </div>
        `).join(''); // Colle tous les morceaux HTML sans virgule séparatrice !

        // On écrase le contenu du DOM par notre String fraîchement construite
        container.innerHTML = htmlContent;
    };

    // 2. Affichage initial avec 100% de la donnée
    renderProjects(portfolioData);

    // 3. Écoute des Boutons de Filtre (L'Effet Wow SPA)
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Nettoyage de la classe "active" du design
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Récupère ce qui a été cliqué : 'all', 'dev', 'design'...
            const filterValue = btn.dataset.filter; 

            if (filterValue === 'all') {
                // S'il clique sur TOUT, on repeint l'écran avec le tableau complet
                renderProjects(portfolioData);
            } else {
                // S'il clique sur autre chose, on donne un SOUS-TABLEAU (.filter) à repeindre
                const filteredData = portfolioData.filter(item => item.category === filterValue);
                renderProjects(filteredData);
            }
        });
    });
}
```

Importez `initPortfolio()` et exécutez-la dans `main.js`.

## L'Avance Systémique : Pourquoi est-ce si puissant ?

Auparavant, si le client vous appelait en disant : _"Je veux qu'on ne puisse voir que les projets Mobiles"_, cela nécessitait le rechargement d'une page PHP vers le serveur, qui faisait une requête SQL `WHERE category="app"`, puis vous renvoyait un nouveau `index.html`. Environ **0.8 seconde** de temps perdu.

Ici, avec `.filter()`, le tableau est recalculé dans la puce RAM de l'ordinateur du visiteur, et l'écran est repeint en **3 ou 4 millisecondes**, procurant l'expérience fluide d'une application native Apple ou Android. Ce principe fondamental s'appelle la **Single Source of Truth** régissant les Frameworks. L'État (le tableau `portfolioData`) dicte la loi, L'UI (Le DOM) s'y soumet aveuglément.

## Checklist de la Phase 4

- [ ] L'écran de votre navigateur affiche à nouveau vos 6 projets.
- [ ] Le `index.html` est vide entre les balises du `#portfolio-container`.
- [ ] Lorsque vous cliquez sur `Design`, l'écran écarte instantanément tous les autres projets.
- [ ] Si j'ajoute un nouvel objet dans `projects.js`, l'interface se recrée toute seule au rafraîchissement sans que je n'écrive la moindre ligne HTML !

Le code Source est impeccable. C'est l'heure de fermer la boîte et d'expédier ce produit fini sur les serveurs du monde entier : la ligne d'assemblage (Build Phase).

[Passer à la Phase 5 : Compilation & Déploiement →](phase5.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
