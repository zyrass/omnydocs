---
description: "Maîtriser les formulaires HTML : input, label, textarea, select et les types de données modernes."
icon: lucide/book-open-check
tags: ["HTML", "FORMULAIRES", "INPUT", "INTERACTION", "ACCESSIBILITÉ"]
---

# Les Formulaires

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - La Communication Bidirectionnelle"
    Jusqu'à présent, vos sites Web étaient des monuments statiques : l'utilisateur consomme ce que vous lui donnez, sans jamais pouvoir interagir. Le **Formulaire HTML** casse ce mur. C'est l'outil universel qui permet à votre visiteur de vous **envoyer** de la donnée (un mail de contact, une création de compte, un paiement bancaire).
    
    Cependant, la création d'un formulaire exige une rigueur militaire côté développeur. Si vos étiquettes (`<label>`) sont mal configurées, les visiteurs aveugles ne sauront pas quoi remplir. Si vous choisissez le mauvais type de champ (`type="text"` au lieu de `type="email"`), les smartphones de vos lecteurs n'afficheront pas le raccourci `@` sur leur clavier natif, ruinant l'ergonomie (UX).

Ce module vous apprend à créer des formulaires professionnels, hautement accessibles, clairs et exploitables.

<br />

---

## La balise maîtresse `<form>`

Tout formulaire doit être enveloppé dans la balise englobante `<form>`. Elle agit comme une grosse enveloppe postale destinée à votre serveur Web : c'est elle qui contient les **champs** et décide **comment** envoyer le tout.

```html title="Code HTML - Structure fondamentale d'un formulaire"
<!-- Un formulaire de recherche archétypique -->
<form action="/recherche-produit" method="GET">
    <!-- C'est ici que l'on placera nos boutons et champs de texte ! -->
</form>
```

### GET vs POST (La méthode d'envoi)

L'attribut `method` est vital. Il dicte comment les données vont transiter de l'ordinateur du client vers votre serveur distant.

| Méthode | Visibilité | Usage strict |
|---------|------------|--------------|
| `GET` | **Visible** dans l'URL (`?recherche=chaussure`) | Uniquement pour des **Filtres** ou de la **Recherche**. |
| `POST` | **Invisible** et sécurisé (Dans le corps de requête) | Données sensibles (Mots de passe, Inscriptions, Paiements). |

<br />

---

## Le duo indispensable : Label et Input

Une immense erreur de débutant consiste à jeter un champ de saisie vide sur l'écran en le précédant d'un simple paragraphe de texte. L'accessibilité est alors de zéro.
Chaque champ de saisie (`<input>`) **doit** avoir une étiquette officielle associable formellement (`<label>`).

### Comment lier un Label à un Input ?

L'astuce consiste à donner un identifiant unique `id="X"` à l'Input, puis de dire au Label "Tu représentes le champ X" via `for="X"`.

```html title="Code HTML - Laison Label et Input via l'ID"
<form action="/contact" method="POST">
    <!-- 1. L'étiquette officielle, liée au champ 'email_user' -->
    <label for="email_user">Votre Adresse E-mail :</label>
    
    <!-- 2. Le vrai champ de saisie -->
    <input type="email" id="email_user" name="email_user" required>
    
    <!-- 3. Le bouton de validation obligatoire -->
    <button type="submit">S'inscrire</button>
</form>
```

!!! tip "Bonus UX (Expérience Utilisateur)"
    Si un visiteur clique ou tapote avec son doigt sur le texte du label "Votre Adresse E-mail", son curseur va instantanément se verrouiller **sur le champ de saisie associé** ! La zone de clic est ainsi décuplée et l'expérience mobile sublimée.

### Le rôle crucial de l'attribut `name`

Dans l'exemple ci-dessus, remarquez l'attribut `name="email_user"`. 
L'`id` sert uniquement au design CSS et au Label. Le `name`, lui, est le **nom de la variable** que votre serveur PHP ou Python va recevoir ! Si vous oubliez d'écrire l'attribut `name`, l'input sera purement ignoré lors de l'envoi du formulaire par le navigateur.

<br />

---

## Les types d'Input magiques du HTML5

Autrefois, tout était du stupide texte. Le HTML5 a apporté des "Types" de champs spécialisés qui déclenchent des interfaces natives selon si l'utilisateur est sur PC, Mac, iOS ou Android !

```html title="Code HTML - Les nouveaux types HTML5"
<!-- Saisie de mot de passe (les caractères se transforment en ••••) -->
<input type="password" name="pwd">

<!-- Saisie téléphonique (Ouvre le énorme clavier 'Chiffres' sur Smartphone) -->
<input type="tel" name="telephone" placeholder="06 12 34 56 78">

<!-- Saisie de Date (Ouvre un vrai Calendrier visuel cliquable) -->
<input type="date" name="naissance" min="1900-01-01" max="2024-12-31">

<!-- Saisie numérique avec limites (Empêche l'humain d'entrer des lettres) -->
<input type="number" name="age" min="18" max="100">

<!-- Ouvre l'explorateur de fichier natif du système pour envoyer une image -->
<input type="file" name="avatar" accept="image/png, image/jpeg">
```

<br />

---

## Les Choix : Cases à cocher et Boutons Radio

Comment faire quand on veut offrir un choix strict ou multiple aux utilisateurs sans qu'ils aient à écrire ?

### Les Checkbox (Choix Multiple)

Utiles quand on peut tout cocher à la fois (Ou ne rien cocher du tout).

```html title="Code HTML - Cases à cocher multiples"
<label>
    <input type="checkbox" name="newsletter" value="yes" checked>
    M'inscrire à votre newsletter mensuelle
</label>

<label>
    <input type="checkbox" name="cgu" value="yes" required>
    J'indique avoir lu les CGU (Obligatoire !)
</label>
```

!!! info "Raccourci de structuration"
    Inverser et placer le `<input>` **à l'intérieur** du `<label>` est une excellente technique pour lier automatiquement l'étiquette au champ sans avoir à utiliser les fameux attributs `id` et `for`. Le navigateur comprend la fusion de lui-même !

### Les Boutons Radio (Choix Exclusif)

Utiles quand on ne peut choisir qu'une **seule** option possible à l'exclusion de toutes les autres. Toute la ruse consiste à leur donner le **même attribut `name`**.

```html title="Code HTML - Choix exclusif avec les radios"
<p>Quelle est votre taille de T-Shirt ?</p>

<!-- Le navigateur comprend que ce groupe s'appelle "taille", 
     cliquer sur "S" décochera "M" automatiquement. -->
<label>
    <input type="radio" name="taille" value="S"> Petit (S)
</label>

<label>
    <input type="radio" name="taille" value="M" checked> Moyen (M)
</label>
```

<br />

---

## Les zones de textes géantes et listes déroulantes

Pour offrir la possibilité d'écrire un énorme paragraphe (Un formulaire de Contact ou un Commentaire de Blog), l'`input` classique n'est pas taillé pour cela. On utilise le monstre `<textarea>`.

### Le Textarea
Contrairement à un input, le `textarea` n'est pas une balise orpheline. L'espace entre son ouverture et sa fermeture constitue sa valeur originelle à l'écran.

```html title="Code HTML - Bloc de texte multi-lignes"
<label for="message">Décrivez votre problème :</label>

<textarea id="message" name="message" rows="5" cols="50">
Ceci est un texte pré-rempli sur 5 lignes par défaut.
</textarea>
```

### La Liste Déroulante (Le `<select>`)
Parfaite pour faire choisir un pays de résidence parmi 200 choix sans exploser la page avec 200 Boutons Radios !

```html title="Code HTML - Liste déroulante avec groupes"
<label for="pays">Votre pays :</label>

<select id="pays" name="pays">
    <!-- Un regroupement de choix logique visuellement sur le menu -->
    <optgroup label="Europe">
        <option value="fr">France</option>
        <option value="be">Belgique</option>
        <option value="ch">Suisse</option>
    </optgroup>
    
    <optgroup label="Amériques">
        <option value="ca">Canada</option>
        <option value="us">États-Unis</option>
    </optgroup>
</select>
```

<br />

---

## Conclusion et Synthèse

Les formulaires propulsent votre page Web du statut de document passif à celui de véritable application interactive. Gardez toujours en mémoire le trio de tête : la balise `<form>` pour encadrer, les balises `<label>` pour l'accessibilité humaine, et l'attribut `name` pour la liaison avec votre serveur.

> Dans le module suivant, nous apprendrons à donner enfin un véritable sens robotique à l'intégralité du code de notre page avec **L'Art du HTML5 Sémantique (`<main>`, `<header>`, etc.)**.

<br />
