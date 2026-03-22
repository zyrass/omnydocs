---
description: "Phase 3 : Synthèse DOM & Persistance. Injection dynamique de l'interface en réagissant aux données, et encodage JSON vers l'API LocalStorage du navigateur."
icon: lucide/database
tags: ["JAVASCRIPT", "DOM", "LOCALSTORAGE", "JSON", "EVENTS"]
status: stable
---

# Phase 3 : Rendu Visuel & Sauvegarde

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1h00">
</div>

!!! quote "Objectif de la Phase"
    Le "Cerveau" de notre application (Le tableau `courses` de la Phase 2) fonctionne parfaitement dans l'ombre. Maintenant, nous allons lui ordonner de dessiner une interface (Les balises `<li>` HTML) fidèlement, et de mémoriser ce tableau sur le Disque Dur de l'utilisateur pour qu'il résiste à l'actualisation de la page.

## 1. La Fonction de Rendu (UI Render)

Chaque fois que l'utilisateur modifie le tableau (Ajouter, Supprimer, Cocher), l'interface visuelle est techniquement "périmée". La fonction `afficherCourses()` a un rôle radical : **effacer 100% de l'écran local, et repeindre tout en se basant sur le nouveau tableau.**

Dans `script.js` :

```javascript
/* --- LA COUCHE VISUELLE (VUE DOM) --- */
const listElement = document.getElementById('shopping-list');
const totalElement = document.getElementById('total-items');

function afficherCourses() {
    // 1. Destruction brutale de l'ancien affichage (Nettoyage)
    listElement.innerHTML = "";
    
    // 2. Mise à jour du petit compteur visuel en haut
    totalElement.textContent = `${courses.length} article(s)`;

    // 3. Boucler sur notre "Cerveau" (Le tableau) et fabriquer du HTML !
    courses.forEach(course => {
        // A. Création des balises à la volée (Non insérées dans la page encore)
        const li = document.createElement('li');
        // Si la propriété 'terminee' est true, je lui ajoute une classe CSS spéciale
        li.className = `todo-item ${course.terminee ? 'checked' : ''}`;
        
        // B. Injection du contenu textuel (Le label "Pommes")
        li.innerHTML = `
            <span class="text">${course.label}</span>
            <button class="btn-delete">×</button>
        `;
        
        // C. ÉCOUTEURS DÉDIÉS : On lie des actions au clic direct sur CET élément !
        
        // Clic sur l'article entier = Barrer le texte
        li.addEventListener('click', function(e) {
            // Sécurité : Ne barre pas le texte s'il a cliqué sur la croix de suppression !
            if(e.target.tagName !== 'BUTTON') { 
                basculerEtat(course.id);
                sauvegarderLocal(); // On verra ça au chapitre d'en-dessous !
                afficherCourses();  // On relance la peinture complète (L'élément grisera)
            }
        });
        
        // Clic sur le Bouton [X] = Supprimer
        const btnDelete = li.querySelector('.btn-delete');
        btnDelete.addEventListener('click', function() {
            supprimerCourse(course.id);
            sauvegarderLocal();
            afficherCourses();
        });

        // D. L'insertion FINALE dans le document HTML (L'apparition physique)
        listElement.appendChild(li);
    });
}
```

Prenez conscience de cette boucle : L'utilisateur *Ajoute* -> Modifie Le Tableau -> Lance `afficherCourses()` -> Le DOM est repeint instantanément. C'est l'ADN du métier de développeur Front-End Moderne (Vue.js, React).

Modifiez votre fonction de capture (Phase 2) pour invoquer l'affichage :
```javascript
formElement.addEventListener('submit', function(event) {
    event.preventDefault();
    const valeurTapee = inputElement.value.trim();
    if (valeurTapee !== "") {
        ajouterCourse(valeurTapee);
        sauvegarderLocal(); // NOUVEAU !
        inputElement.value = "";
        
        afficherCourses(); // NOUVEAU ! Je repeins l'écran de l'utilisateur !
    }
});
```

Rajoutez le CSS final dans `style.css` :
```css
/* DESIGN DES ELEMENTS DE LA LISTE */
.todo-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #f1f5f9;
    cursor: pointer;
    transition: background 0.2s;
}

.todo-item:hover {
    background: #f8fafc; /* Survol gris très léger */
}

/* LE MODE BARRÉ (Checked) */
.todo-item.checked .text {
    text-decoration: line-through; /* Barre le texte Mots-Clés ! */
    color: #94a3b8; /* Gris pâle Slate 400 */
}

.btn-delete {
    background: none;
    border: none;
    color: #ef4444; /* Rouge Alerte */
    font-size: 1.5rem;
    cursor: pointer;
    border-radius: 4px;
    padding: 0 0.5rem;
}
.btn-delete:hover {
    background: #fee2e2;
}
```

## 2. Le Disque Dur : Le Graal du LocalStorage

S'il rafraîchit la page, votre Cerveau en mémoire courte (RAM) s'efface... `let courses = []` recommence à zéro.
Pour sauver l'Humanité, nous appellerons le `localStorage`.

Tout en haut de votre `script.js` !
```javascript
// La Clé (Le nom de notre tiroir mémoire dans l'ordinateur de l'utilisateur)
const STORAGE_KEY = 'mes_courses_digitales';

// On force le chargement du tiroir AU DÉMARRAGE !
// Si le tiroir est vide (null), on prend un tableau vide [].
// ATTENTION: JSON.parse re-transforme le Texte mort en Tableau Vivant !
let courses = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];

// Dès que la page s'ouvre, on force le dessin de base de l'écran HTML.
afficherCourses();
```

La fonction de Sauvegarde universelle, à mettre au milieu de votre code JS :
```javascript
function sauvegarderLocal() {
    // Le navigateur NE PEUT PAS stocker un [Objet]. Seulement du 'Texte'.
    // JSON.stringify transforme le vivant en écriture inerte universelle.
    localStorage.setItem(STORAGE_KEY, JSON.stringify(courses));
}
```

## 🏁 Checklist Initiale de Validation Totale

Si vous avez respecté le code intégral...
- [ ] J'écris "Lait" et "Café", je tape Entrée. Ils s'affichent sous forme de liste. Le compteur dit `2 article(s)`.
- [ ] Je clique sur "Café" : le texte devient gris pâle et se fait barrer d'un trait.
- [ ] Je clique sur la croix Rouge `×` du "Lait" : Il disparaît instantanément.
- [ ] LE TEST SUPRÊME : Je rafraîchis sauvagement le navigateur (`F5`). Mon fameux "Café" est toujours là, et il est TOUJOURS barré. Le navigateur "se souvient".

**Mission Accomplie**. Vous maîtrisez officiellement l'Architecture DOM Dynamique. 
Vous êtes prêt à augmenter le niveau cérébral en passant à des logiques mathématiques en dimensions (Les grilles à axes X/Y), nécessaires pour le légendaire jeu **Puissance 4**, notre prochain projet. 
Respirez, un grand défi mathématique vous attend.
