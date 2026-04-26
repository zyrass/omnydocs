---
description: "Phase 1 : Conception de l'Interface Utilisateur (UI). Mise en place du formulaire de capture, et du conteneur de liste vide prêt à être peuplé par la logique Javascript."
icon: lucide/layout-template
tags: ["HTML", "CSS", "FORM", "UI"]
status: stable
---

# Phase 1 : Interface et Layout

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Une aplication dynamique nécessite une "Zone de Capture" (un formulaire) pour que l'utilisateur puisse parler à la machine, et une "Zone de Rendu" (une liste) pour que la machine puisse répondre à l'utilisateur. Nous allons construire cette arène en HTML simple et lui donner de l'allure avec CSS Flexbox.

## 1. Structure HTML Sémantique (L'Arène)

Ouvrez votre fichier `index.html`. 
Remarquez l'usage intelligent de la balise `<form>`. Même si nous n'envoyons rien à un serveur PHP, utiliser un vrai formulaire permet de bénéficier nativement de la validation HTML5 (`required`) et de l'envoi via la touche ENTRÉE du clavier.

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Courses Digitales</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="app-container">
        
        <header class="app-header">
            <h1>Mes Courses</h1>
            <!-- Affichage dynamique du total (Optionnel mais classe) -->
            <p id="total-items">0 article(s)</p>
        </header>

        <!-- ZONE DE CAPTURE -->
        <form id="item-form" class="input-section">
            <input 
                type="text" 
                id="item-input" 
                placeholder="Ex: Lait demi-écrémé..." 
                required 
                autocomplete="off"
            >
            <button type="submit" class="btn-add">Ajouter</button>
        </form>

        <!-- ZONE DE RENDU -->
        <!-- Elle est Vierge de tout Li. C'est voulu. -->
        <ul id="shopping-list" class="shopping-list">
            <!-- La magie JavaScript dessinera ici -->
        </ul>

    </main>

    <script src="script.js"></script>
</body>
</html>
```

## 2. Poudrage CSS (Le Design)

Créez `style.css`.
Assurons-nous que cette liste ait l'air d'une véritable application Mobile, centrée au milieu de l'écran avec une belle ombre portée, afin d'inciter l'utilisateur à interagir.

```css
/* RESET UNIVERSEL */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

body {
    background-color: #f1f5f9; /* Slate 100 */
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start; /* Ne pas centrer parfaitement verticalement pour laisser respirer */
    padding-top: 5vh;
}

/* LE CONTENEUR PRINCIPAL (L'App Mobile) */
.app-container {
    background: white;
    width: 100%;
    max-width: 500px; /* Sur ordinateur, ça s'arrête à 500px ! */
    border-radius: 12px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    overflow: hidden; /* Tout ce qui dépasse du border radius disparait */
}

/* L'ENTÊTE */
.app-header {
    background-color: #3b82f6; /* Bleu électrique Tailwind */
    color: white;
    padding: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* LA ZONE DE FORMULAIRE FLEXBOX */
.input-section {
    display: flex;
    padding: 1rem;
    gap: 0.5rem;
    background-color: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
}

.input-section input {
    flex-grow: 1; /* Le champ texte prend toute la place restante ! */
    padding: 0.75rem;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 1rem;
}

.btn-add {
    background-color: #10b981; /* Vert Émeraude */
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0 1.5rem;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
}

.btn-add:hover {
    background-color: #059669; /* Vert Foncé */
}

/* LA ZONE DE LISTE (Préparation des futurs Li injectés) */
.shopping-list {
    list-style: none; /* Disparition des puces noires HTML */
    max-height: 60vh; /* Permet un scroll interne s'il y a 100 articles */
    overflow-y: auto;
}
```

## Checklist de la Phase 1

- [ ] L'application ressemble grossièrement à l'écran d'un smartphone, centrée verticalement.
- [ ] Le champ de texte (Input) pousse vigoureusement le bouton vert vers la droite grâce à son `flex-grow: 1`.
- [ ] Taper dans le champ texte puis appuyer sur "Entrée" ne fait rien... si ce n'est rafraichir la page brutalement (Comportement normal d'un formulaire sans JavaScript. Nous allons le tuer en Phase 2).

Ce décor statique est dressé. Les acteurs peuvent entrer en scène.
Dans la phase suivante, nous brancherons le "Cerveau" de l'application via JavaScript.

[Passer à la Phase 2 : Logique Algorithmique CRUD →](phase2.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
