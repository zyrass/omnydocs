---
description: "Maîtriser les formulaires HTML : input, label, textarea, select, validation HTML5, accessibilité"
icon: lucide/book-open-check
tags: ["HTML", "FORMULAIRES", "INPUT", "VALIDATION", "ACCESSIBILITÉ", "UX"]
---

# V - Formulaires

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="6-8 heures">
</div>

## Introduction : La Communication avec l'Utilisateur

!!! quote "Analogie pédagogique"
    _Imaginez un **guichet d'administration**. Pour obtenir un document, vous devez remplir un formulaire papier : nom, prénom, date de naissance, adresse. Chaque champ a des règles : "Obligatoire" (astérisque rouge), "Format : JJ/MM/AAAA", "Cochez une case". Si vous oubliez un champ ou écrivez mal, l'employé vous renvoie corriger. Les **formulaires HTML**, c'est pareil : ils permettent à l'utilisateur de communiquer avec votre site (inscription, connexion, contact, commande). Chaque `<input>` est un champ à remplir, chaque `<label>` explique quoi mettre, chaque `required` est un champ obligatoire, chaque `pattern` vérifie le format. Un bon formulaire = UX fluide (labels clairs, validation immédiate, messages d'erreur utiles). Un mauvais formulaire = frustration (champs sans label, erreurs cryptiques, pas de validation). Ce module vous apprend à créer des formulaires professionnels, accessibles et user-friendly._

**Formulaires** = Structures HTML permettant la saisie et l'envoi de données utilisateur.

**Pourquoi maîtriser les formulaires ?**

✅ **Interaction** : Communication bidirectionnelle site ↔ utilisateur
✅ **Conversion** : Inscriptions, achats, leads (objectif business)
✅ **Données** : Collecte d'informations structurées
✅ **Validation** : Contrôle qualité des données avant envoi
✅ **Accessibilité** : Utilisables par tous (clavier, lecteurs d'écran)
✅ **UX** : Expérience utilisateur critique (formulaire = friction)

**Cas d'usage courants :**

- **Connexion** : Email + mot de passe
- **Inscription** : Nom, prénom, email, mot de passe
- **Contact** : Nom, email, message
- **Recherche** : Champ de recherche
- **Commande** : Adresse, paiement, livraison
- **Paramètres** : Préférences utilisateur

**⚠️ Enjeux critiques :**

- **Sécurité** : Validation côté serveur obligatoire (HTML = contournable)
- **Accessibilité** : Labels explicites, navigation clavier
- **Performance** : Validation en temps réel sans bloquer
- **UX** : Messages d'erreur clairs, auto-complétion

**Ce module vous enseigne à créer des formulaires professionnels et accessibles.**

---

## 1. Structure de Base d'un Formulaire

### 1.1 Balise `<form>`

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Formulaire de base</title>
</head>
<body>
    <!-- Formulaire simple -->
    <form action="/submit" method="POST">
        <label for="name">Nom :</label>
        <input type="text" id="name" name="name">
        
        <button type="submit">Envoyer</button>
    </form>
    
    <!-- Formulaire avec tous les attributs -->
    <form 
        action="/process-form" 
        method="POST"
        enctype="multipart/form-data"
        autocomplete="on"
        novalidate
    >
        <!-- Champs du formulaire -->
        <input type="text" name="username">
        <button type="submit">Soumettre</button>
    </form>
</body>
</html>
```

**Anatomie de la balise `<form>` :**

```html
<form action="/submit" method="POST" enctype="multipart/form-data">
      ↑             ↑            ↑                    ↑
      |             |            |                    |
   Balise      URL de      Méthode HTTP      Type d'encodage
              traitement   (GET ou POST)     (pour fichiers)
```

**Attributs essentiels :**

| Attribut | Valeurs | Description | Exemple |
|----------|---------|-------------|---------|
| `action` | URL | URL de traitement du formulaire | `action="/contact"` |
| `method` | GET, POST | Méthode HTTP d'envoi | `method="POST"` |
| `enctype` | Voir tableau | Type d'encodage données | `enctype="multipart/form-data"` |
| `autocomplete` | on, off | Auto-complétion navigateur | `autocomplete="on"` |
| `novalidate` | Booléen | Désactiver validation HTML5 | `novalidate` |
| `name` | Texte | Nom du formulaire (JavaScript) | `name="contact-form"` |
| `target` | _blank, _self | Où ouvrir la réponse | `target="_blank"` |

**Valeurs enctype :**

| Valeur | Usage | Exemple |
|--------|-------|---------|
| `application/x-www-form-urlencoded` | Défaut (texte) | Formulaires simples |
| `multipart/form-data` | **Upload fichiers** | Formulaires avec `<input type="file">` |
| `text/plain` | Texte brut (rarement utilisé) | Debugging |

### 1.2 Method : GET vs POST

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>GET vs POST</title>
</head>
<body>
    <!-- GET : Données dans l'URL (visible) -->
    <form action="/search" method="GET">
        <label for="q">Rechercher :</label>
        <input type="text" id="q" name="q">
        <button type="submit">Rechercher</button>
    </form>
    <!-- Résultat : https://site.com/search?q=javascript -->
    
    <!--
    ✅ Utiliser GET pour :
    - Recherche (bookmarkable)
    - Filtres (partageables)
    - Navigation (historique)
    
    ❌ Ne PAS utiliser GET pour :
    - Données sensibles (mot de passe)
    - Modifications serveur (création, suppression)
    - Gros volumes de données
    -->
    
    <!-- POST : Données dans le corps de la requête (invisible) -->
    <form action="/login" method="POST">
        <label for="email">Email :</label>
        <input type="email" id="email" name="email">
        
        <label for="password">Mot de passe :</label>
        <input type="password" id="password" name="password">
        
        <button type="submit">Se connecter</button>
    </form>
    <!-- Données envoyées dans le corps (pas dans l'URL) -->
    
    <!--
    ✅ Utiliser POST pour :
    - Connexion (sécurité)
    - Inscription (données sensibles)
    - Modification données (création, mise à jour, suppression)
    - Upload fichiers
    - Gros volumes de données
    -->
</body>
</html>
```

**Comparaison GET vs POST :**

| Critère | GET | POST |
|---------|-----|------|
| **Visibilité** | Données dans URL | Données cachées |
| **Sécurité** | ❌ Visible (historique, logs) | ✅ Plus sécurisé |
| **Bookmarkable** | ✅ Oui | ❌ Non |
| **Limite taille** | ~2048 caractères | Illimité (pratiquement) |
| **Cache** | ✅ Caché par navigateur | ❌ Pas caché |
| **Historique** | ✅ Conservé | ❌ Pas conservé |
| **Usage** | Lecture, recherche, filtres | Écriture, modification, upload |

---

## 2. Input et Label

### 2.1 Label : Association Explicite

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Labels et inputs</title>
</head>
<body>
    <!-- ✅ BON : Label avec attribut for -->
    <label for="username">Nom d'utilisateur :</label>
    <input type="text" id="username" name="username">
    <!-- Cliquer sur le label focus l'input -->
    
    <!-- ✅ BON : Label enveloppant (implicite) -->
    <label>
        Email :
        <input type="email" name="email">
    </label>
    <!-- Fonctionne aussi, mais for/id préféré -->
    
    <!-- ❌ MAUVAIS : Sans label -->
    <input type="text" name="firstname">
    <input type="text" name="lastname">
    <!-- Inaccessible ! Lecteur d'écran ne sait pas quoi annoncer -->
    
    <!-- ❌ MAUVAIS : Placeholder au lieu de label -->
    <input type="text" placeholder="Nom d'utilisateur">
    <!-- Placeholder disparaît à la saisie, pas accessible -->
</body>
</html>
```

**Pourquoi les labels sont OBLIGATOIRES ?**

1. **Accessibilité** : Lecteurs d'écran annoncent le label
2. **UX** : Zone cliquable plus grande (cliquer label = focus input)
3. **Clarté** : Utilisateur sait quoi saisir
4. **Validation** : Messages d'erreur référencent le label

**Exemple d'accessibilité :**

```html
<!-- Utilisateur aveugle avec lecteur d'écran -->

<!-- ✅ AVEC label -->
<label for="email">Adresse email :</label>
<input type="email" id="email" name="email">
<!-- Lecteur annonce : "Adresse email, zone de saisie" -->

<!-- ❌ SANS label -->
<input type="email" name="email">
<!-- Lecteur annonce : "Zone de saisie" (inutile !) -->
```

### 2.2 Attribut name (Crucial)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Attribut name</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- ✅ AVEC name : Données envoyées -->
        <label for="firstname">Prénom :</label>
        <input type="text" id="firstname" name="firstname" value="Alice">
        
        <label for="lastname">Nom :</label>
        <input type="text" id="lastname" name="lastname" value="Dupont">
        
        <button type="submit">Envoyer</button>
    </form>
    
    <!-- Données envoyées au serveur :
    firstname=Alice&lastname=Dupont
    -->
    
    <!-- ❌ SANS name : Données NON envoyées -->
    <form action="/submit" method="POST">
        <label for="email">Email :</label>
        <input type="email" id="email" value="alice@example.com">
        <!-- ⚠️ PAS de name → PAS envoyé au serveur ! -->
        
        <button type="submit">Envoyer</button>
    </form>
    
    <!-- Données envoyées au serveur :
    (vide, email manquant !)
    -->
</body>
</html>
```

**Règle d'or : `name` est OBLIGATOIRE pour envoyer les données !**

```html
<!-- id   : Pour JavaScript et label (côté client) -->
<!-- name : Pour envoi serveur (côté serveur) -->

<label for="email">Email :</label>
<input type="email" id="email" name="email">
         ↑                ↑           ↑
         |                |           |
    Pour label      Pour label   Pour serveur
                  (JavaScript)
```

---

## 3. Types d'Input HTML5

### 3.1 Text, Email, Password, Tel, URL

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Types d'input texte</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- TEXT : Texte générique -->
        <label for="username">Nom d'utilisateur :</label>
        <input 
            type="text" 
            id="username" 
            name="username"
            placeholder="Votre nom"
            maxlength="50"
            required
        >
        
        <!-- EMAIL : Validation email -->
        <label for="email">Email :</label>
        <input 
            type="email" 
            id="email" 
            name="email"
            placeholder="nom@exemple.com"
            required
        >
        <!-- Navigateur vérifie format email (@ présent) -->
        <!-- Mobile : Clavier avec @ -->
        
        <!-- PASSWORD : Masqué (••••••) -->
        <label for="password">Mot de passe :</label>
        <input 
            type="password" 
            id="password" 
            name="password"
            minlength="8"
            required
        >
        <!-- Caractères masqués pour sécurité -->
        
        <!-- TEL : Téléphone -->
        <label for="phone">Téléphone :</label>
        <input 
            type="tel" 
            id="phone" 
            name="phone"
            placeholder="06 12 34 56 78"
            pattern="[0-9]{10}"
        >
        <!-- Mobile : Clavier numérique -->
        
        <!-- URL : Adresse web -->
        <label for="website">Site web :</label>
        <input 
            type="url" 
            id="website" 
            name="website"
            placeholder="https://example.com"
        >
        <!-- Navigateur vérifie format URL (protocole http:// ou https://) -->
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Différences clés :**

| Type | Validation | Clavier mobile | Usage |
|------|------------|----------------|-------|
| `text` | Aucune | Standard | Texte générique |
| `email` | Format email | @ et . | Adresses email |
| `password` | Aucune | Standard | Mots de passe (masqué) |
| `tel` | Aucune | Numérique | Téléphones |
| `url` | Format URL | .com / | Sites web |

### 3.2 Number, Range, Date, Time

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Types d'input numériques et dates</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- NUMBER : Nombre avec contrôles +/- -->
        <label for="age">Âge :</label>
        <input 
            type="number" 
            id="age" 
            name="age"
            min="18"
            max="120"
            step="1"
            value="25"
        >
        <!-- Contrôles +/- intégrés, validation min/max -->
        
        <!-- RANGE : Slider (curseur) -->
        <label for="volume">Volume : <span id="volume-value">50</span>%</label>
        <input 
            type="range" 
            id="volume" 
            name="volume"
            min="0"
            max="100"
            step="5"
            value="50"
        >
        <!-- Slider visuel pour sélectionner valeur -->
        
        <!-- DATE : Sélecteur de date -->
        <label for="birthdate">Date de naissance :</label>
        <input 
            type="date" 
            id="birthdate" 
            name="birthdate"
            min="1900-01-01"
            max="2024-12-31"
        >
        <!-- Calendrier intégré navigateur -->
        
        <!-- TIME : Heure -->
        <label for="meeting-time">Heure de rendez-vous :</label>
        <input 
            type="time" 
            id="meeting-time" 
            name="meeting-time"
            min="08:00"
            max="18:00"
            step="900"
        >
        <!-- step="900" = incrément 15 minutes (900 secondes) -->
        
        <!-- DATETIME-LOCAL : Date + Heure locale -->
        <label for="appointment">Date et heure :</label>
        <input 
            type="datetime-local" 
            id="appointment" 
            name="appointment"
        >
        
        <!-- MONTH : Mois et année -->
        <label for="credit-card-expiry">Expiration carte :</label>
        <input 
            type="month" 
            id="credit-card-expiry" 
            name="expiry"
        >
        
        <!-- WEEK : Semaine de l'année -->
        <label for="week">Semaine :</label>
        <input 
            type="week" 
            id="week" 
            name="week"
        >
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Attributs pour types numériques/dates :**

| Attribut | Usage | Exemple |
|----------|-------|---------|
| `min` | Valeur minimale | `min="0"` ou `min="2024-01-01"` |
| `max` | Valeur maximale | `max="100"` ou `max="2024-12-31"` |
| `step` | Incrément | `step="5"` ou `step="900"` (secondes) |
| `value` | Valeur par défaut | `value="50"` ou `value="2024-06-15"` |

### 3.3 Color, File, Search, Hidden

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Types d'input spéciaux</title>
</head>
<body>
    <form action="/submit" method="POST" enctype="multipart/form-data">
        <!-- COLOR : Sélecteur de couleur -->
        <label for="favorite-color">Couleur préférée :</label>
        <input 
            type="color" 
            id="favorite-color" 
            name="color"
            value="#ff0000"
        >
        <!-- Color picker intégré navigateur -->
        
        <!-- FILE : Upload de fichier -->
        <label for="avatar">Photo de profil :</label>
        <input 
            type="file" 
            id="avatar" 
            name="avatar"
            accept="image/png, image/jpeg"
            multiple
        >
        <!-- accept : Types MIME autorisés -->
        <!-- multiple : Plusieurs fichiers -->
        
        <!-- FILE : Fichiers multiples avec taille max -->
        <label for="documents">Documents (PDF, max 5MB) :</label>
        <input 
            type="file" 
            id="documents" 
            name="documents"
            accept=".pdf"
            multiple
        >
        <!-- ⚠️ Limite taille côté serveur obligatoire -->
        
        <!-- SEARCH : Champ de recherche -->
        <label for="site-search">Rechercher :</label>
        <input 
            type="search" 
            id="site-search" 
            name="q"
            placeholder="Rechercher sur le site..."
        >
        <!-- Icône "X" pour effacer (sur certains navigateurs) -->
        
        <!-- HIDDEN : Donnée cachée (pas visible utilisateur) -->
        <input 
            type="hidden" 
            name="user-id" 
            value="12345"
        >
        <input 
            type="hidden" 
            name="csrf-token" 
            value="abc123xyz"
        >
        <!-- Usage : ID utilisateur, token CSRF, données techniques -->
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Type file : Attributs spécifiques :**

| Attribut | Description | Exemple |
|----------|-------------|---------|
| `accept` | Types de fichiers autorisés | `accept="image/*"` ou `accept=".pdf,.docx"` |
| `multiple` | Sélection multiple | `multiple` |
| `capture` | Capture caméra (mobile) | `capture="user"` (selfie) ou `capture="environment"` (arrière) |

**Types MIME courants pour accept :**

```html
<!-- Images -->
<input type="file" accept="image/*">
<input type="file" accept="image/png, image/jpeg, image/gif">

<!-- Documents -->
<input type="file" accept=".pdf">
<input type="file" accept=".pdf, .doc, .docx">
<input type="file" accept="application/pdf, application/msword">

<!-- Audio -->
<input type="file" accept="audio/*">
<input type="file" accept=".mp3, .wav">

<!-- Vidéo -->
<input type="file" accept="video/*">
<input type="file" accept=".mp4, .mov">
```

---

## 4. Checkbox et Radio

### 4.1 Checkbox (Cases à Cocher)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Checkbox</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- Checkbox simple -->
        <label>
            <input type="checkbox" name="newsletter" value="yes">
            S'abonner à la newsletter
        </label>
        
        <!-- Checkbox cochée par défaut -->
        <label>
            <input type="checkbox" name="terms" value="accepted" checked required>
            J'accepte les conditions d'utilisation
        </label>
        
        <!-- Groupe de checkbox (même name avec []) -->
        <fieldset>
            <legend>Centres d'intérêt :</legend>
            
            <label>
                <input type="checkbox" name="interests[]" value="tech">
                Technologie
            </label>
            
            <label>
                <input type="checkbox" name="interests[]" value="sport">
                Sport
            </label>
            
            <label>
                <input type="checkbox" name="interests[]" value="art">
                Art
            </label>
            
            <label>
                <input type="checkbox" name="interests[]" value="travel">
                Voyage
            </label>
        </fieldset>
        
        <!-- Checkbox avec id/for séparés -->
        <input type="checkbox" id="subscribe" name="subscribe" value="1">
        <label for="subscribe">S'abonner aux notifications</label>
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Comportement checkbox :**

```
Checkbox NON cochée : Pas envoyée au serveur
Checkbox cochée : Envoyée avec sa valeur

Exemple :
<input type="checkbox" name="newsletter" value="yes">

Non cochée → Serveur reçoit : (rien)
Cochée     → Serveur reçoit : newsletter=yes

Groupe avec [] :
interests[]=tech&interests[]=art
→ Serveur reçoit tableau : ['tech', 'art']
```

### 4.2 Radio Buttons (Boutons Radio)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Radio buttons</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- Radio buttons : Même name = groupe exclusif -->
        <fieldset>
            <legend>Genre :</legend>
            
            <label>
                <input type="radio" name="gender" value="male" checked>
                Homme
            </label>
            
            <label>
                <input type="radio" name="gender" value="female">
                Femme
            </label>
            
            <label>
                <input type="radio" name="gender" value="other">
                Autre
            </label>
        </fieldset>
        
        <!-- Autre groupe radio (name différent) -->
        <fieldset>
            <legend>Taille :</legend>
            
            <input type="radio" id="size-s" name="size" value="S">
            <label for="size-s">S</label>
            
            <input type="radio" id="size-m" name="size" value="M" checked>
            <label for="size-m">M</label>
            
            <input type="radio" id="size-l" name="size" value="L">
            <label for="size-l">L</label>
            
            <input type="radio" id="size-xl" name="size" value="XL">
            <label for="size-xl">XL</label>
        </fieldset>
        
        <!-- Radio obligatoire -->
        <fieldset>
            <legend>Méthode de livraison : <span style="color: red;">*</span></legend>
            
            <label>
                <input type="radio" name="shipping" value="standard" required>
                Standard (3-5 jours) - Gratuit
            </label>
            
            <label>
                <input type="radio" name="shipping" value="express">
                Express (24h) - 9,99€
            </label>
        </fieldset>
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Différence Checkbox vs Radio :**

| Type | Sélection | name | Usage |
|------|-----------|------|-------|
| **Checkbox** | Multiple | Différent ou `name[]` | Accepter CGV, centres d'intérêt |
| **Radio** | **Une seule** | **Identique** (groupe) | Genre, taille, choix exclusif |

**Comportement radio :**

```
Radio buttons avec même name = Groupe exclusif
Une seule option sélectionnable

<input type="radio" name="color" value="red">
<input type="radio" name="color" value="blue">
<input type="radio" name="color" value="green">

Utilisateur sélectionne "blue"
→ Serveur reçoit : color=blue

Autre groupe (name différent) :
<input type="radio" name="size" value="S">
<input type="radio" name="size" value="M">

Indépendant du groupe "color"
```

---

## 5. Textarea et Select

### 5.1 Textarea (Zone de Texte Multi-lignes)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Textarea</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- Textarea simple -->
        <label for="message">Message :</label>
        <textarea 
            id="message" 
            name="message"
            rows="5"
            cols="50"
        ></textarea>
        
        <!-- Textarea avec placeholder -->
        <label for="bio">Biographie :</label>
        <textarea 
            id="bio" 
            name="bio"
            rows="10"
            cols="50"
            placeholder="Parlez-nous de vous..."
        ></textarea>
        
        <!-- Textarea avec valeur par défaut -->
        <label for="description">Description :</label>
        <textarea 
            id="description" 
            name="description"
            rows="8"
            cols="60"
        >Texte par défaut pré-rempli.
Ce texte sera affiché dans la zone.
Plusieurs lignes possibles.</textarea>
        
        <!-- Textarea avec limites -->
        <label for="comment">Commentaire (max 500 caractères) :</label>
        <textarea 
            id="comment" 
            name="comment"
            rows="5"
            cols="50"
            maxlength="500"
            required
        ></textarea>
        
        <!-- Textarea non redimensionnable (CSS) -->
        <label for="feedback">Feedback :</label>
        <textarea 
            id="feedback" 
            name="feedback"
            rows="4"
            cols="50"
            style="resize: none;"
        ></textarea>
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Attributs textarea :**

| Attribut | Description | Exemple |
|----------|-------------|---------|
| `rows` | Nombre de lignes visibles | `rows="5"` |
| `cols` | Nombre de colonnes (caractères) | `cols="50"` |
| `maxlength` | Limite caractères | `maxlength="500"` |
| `placeholder` | Texte indicatif | `placeholder="Votre message..."` |
| `required` | Champ obligatoire | `required` |
| `readonly` | Lecture seule | `readonly` |
| `disabled` | Désactivé | `disabled` |

**⚠️ Valeur textarea : Entre balises, PAS dans attribut value !**

```html
<!-- ❌ MAUVAIS -->
<textarea value="Texte"></textarea>

<!-- ✅ BON -->
<textarea>Texte ici</textarea>
```

### 5.2 Select (Liste Déroulante)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Select</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- Select simple -->
        <label for="country">Pays :</label>
        <select id="country" name="country">
            <option value="">-- Sélectionner un pays --</option>
            <option value="FR">France</option>
            <option value="BE">Belgique</option>
            <option value="CH">Suisse</option>
            <option value="CA">Canada</option>
        </select>
        
        <!-- Select avec option pré-sélectionnée -->
        <label for="language">Langue :</label>
        <select id="language" name="language">
            <option value="fr" selected>Français</option>
            <option value="en">English</option>
            <option value="es">Español</option>
            <option value="de">Deutsch</option>
        </select>
        
        <!-- Select avec groupes (optgroup) -->
        <label for="car">Voiture :</label>
        <select id="car" name="car">
            <optgroup label="Marques françaises">
                <option value="peugeot">Peugeot</option>
                <option value="renault">Renault</option>
                <option value="citroen">Citroën</option>
            </optgroup>
            <optgroup label="Marques allemandes">
                <option value="volkswagen">Volkswagen</option>
                <option value="bmw">BMW</option>
                <option value="mercedes">Mercedes</option>
            </optgroup>
            <optgroup label="Marques japonaises">
                <option value="toyota">Toyota</option>
                <option value="honda">Honda</option>
            </optgroup>
        </select>
        
        <!-- Select multiple -->
        <label for="skills">Compétences (maintenir Ctrl pour sélection multiple) :</label>
        <select id="skills" name="skills[]" multiple size="5">
            <option value="html">HTML</option>
            <option value="css">CSS</option>
            <option value="js">JavaScript</option>
            <option value="php">PHP</option>
            <option value="python">Python</option>
        </select>
        
        <!-- Select obligatoire -->
        <label for="subscription">Type d'abonnement :</label>
        <select id="subscription" name="subscription" required>
            <option value="">-- Choisir --</option>
            <option value="free">Gratuit</option>
            <option value="pro">Pro - 9,99€/mois</option>
            <option value="enterprise">Enterprise - 49,99€/mois</option>
        </select>
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Structure select :**

```html
<select name="pays">
    <option value="FR">France</option>
    ↑       ↑            ↑
    |       |            |
  Balise  Valeur    Texte affiché
          envoyée   à l'utilisateur
          serveur
</select>
```

**Attributs select et option :**

| Élément | Attribut | Description | Exemple |
|---------|----------|-------------|---------|
| `<select>` | `multiple` | Sélection multiple | `multiple` |
| `<select>` | `size` | Nombre options visibles | `size="5"` |
| `<select>` | `required` | Sélection obligatoire | `required` |
| `<option>` | `value` | Valeur envoyée serveur | `value="FR"` |
| `<option>` | `selected` | Option pré-sélectionnée | `selected` |
| `<option>` | `disabled` | Option non sélectionnable | `disabled` |

---

## 6. Fieldset et Legend

### 6.1 Regrouper des Champs

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Fieldset et Legend</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- Regroupement logique avec fieldset -->
        <fieldset>
            <legend>Informations personnelles</legend>
            
            <label for="firstname">Prénom :</label>
            <input type="text" id="firstname" name="firstname" required>
            
            <label for="lastname">Nom :</label>
            <input type="text" id="lastname" name="lastname" required>
            
            <label for="birthdate">Date de naissance :</label>
            <input type="date" id="birthdate" name="birthdate">
        </fieldset>
        
        <fieldset>
            <legend>Coordonnées</legend>
            
            <label for="email">Email :</label>
            <input type="email" id="email" name="email" required>
            
            <label for="phone">Téléphone :</label>
            <input type="tel" id="phone" name="phone">
            
            <label for="address">Adresse :</label>
            <textarea id="address" name="address" rows="3"></textarea>
        </fieldset>
        
        <fieldset>
            <legend>Préférences</legend>
            
            <label>
                <input type="checkbox" name="newsletter" value="yes">
                Recevoir la newsletter
            </label>
            
            <label>
                <input type="checkbox" name="sms" value="yes">
                Recevoir les SMS promotionnels
            </label>
        </fieldset>
        
        <!-- Fieldset désactivé (tous les champs à l'intérieur) -->
        <fieldset disabled>
            <legend>Section désactivée</legend>
            
            <label for="disabled-input">Ce champ est désactivé :</label>
            <input type="text" id="disabled-input" name="disabled-input">
            
            <label>
                <input type="checkbox" name="disabled-check">
                Cette case aussi
            </label>
        </fieldset>
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Avantages fieldset/legend :**

✅ **Sémantique** : Structure logique du formulaire
✅ **Accessibilité** : Lecteurs d'écran annoncent le groupe
✅ **Style** : Bordure visuelle par défaut (personnalisable CSS)
✅ **Désactivation** : `disabled` sur fieldset désactive tous les champs

**Rendu visuel (navigateur) :**

```
┌─ Informations personnelles ──────┐
│                                   │
│ Prénom : [________]               │
│ Nom :    [________]               │
│                                   │
└───────────────────────────────────┘

┌─ Coordonnées ────────────────────┐
│                                   │
│ Email : [________]                │
│ Phone : [________]                │
│                                   │
└───────────────────────────────────┘
```

---

## 7. Validation HTML5

### 7.1 Attributs de Validation

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Validation HTML5</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- REQUIRED : Champ obligatoire -->
        <label for="username">Nom d'utilisateur <span style="color: red;">*</span></label>
        <input 
            type="text" 
            id="username" 
            name="username"
            required
        >
        <!-- Navigateur bloque soumission si vide -->
        
        <!-- MINLENGTH / MAXLENGTH : Longueur -->
        <label for="password">Mot de passe (8-20 caractères) :</label>
        <input 
            type="password" 
            id="password" 
            name="password"
            minlength="8"
            maxlength="20"
            required
        >
        
        <!-- MIN / MAX : Valeur numérique -->
        <label for="age">Âge (18-120) :</label>
        <input 
            type="number" 
            id="age" 
            name="age"
            min="18"
            max="120"
            required
        >
        
        <!-- PATTERN : Expression régulière -->
        <label for="phone">Téléphone (format : 06 12 34 56 78) :</label>
        <input 
            type="tel" 
            id="phone" 
            name="phone"
            pattern="0[1-9]( [0-9]{2}){4}"
            title="Format : 06 12 34 56 78"
            required
        >
        <!-- title : Message d'aide affiché au survol -->
        
        <!-- Pattern : Code postal français -->
        <label for="zipcode">Code postal :</label>
        <input 
            type="text" 
            id="zipcode" 
            name="zipcode"
            pattern="[0-9]{5}"
            title="5 chiffres"
            placeholder="69000"
            required
        >
        
        <!-- Pattern : Nom d'utilisateur -->
        <label for="username-pattern">Nom d'utilisateur (lettres, chiffres, tirets) :</label>
        <input 
            type="text" 
            id="username-pattern" 
            name="username"
            pattern="[a-zA-Z0-9\-]{3,20}"
            title="3-20 caractères : lettres, chiffres, tirets"
            required
        >
        
        <button type="submit">S'inscrire</button>
    </form>
</body>
</html>
```

**Tableau récapitulatif validation :**

| Attribut | Types | Description | Exemple |
|----------|-------|-------------|---------|
| `required` | Tous | Champ obligatoire | `required` |
| `minlength` | text, textarea | Longueur minimale | `minlength="8"` |
| `maxlength` | text, textarea | Longueur maximale | `maxlength="20"` |
| `min` | number, date | Valeur minimale | `min="18"` ou `min="2024-01-01"` |
| `max` | number, date | Valeur maximale | `max="120"` ou `max="2024-12-31"` |
| `pattern` | text, tel, email, url | Regex validation | `pattern="[0-9]{5}"` |
| `title` | Avec pattern | Message d'aide | `title="5 chiffres"` |
| `step` | number, range | Incrément | `step="5"` ou `step="0.01"` |

### 7.2 Patterns Courants (Regex)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Patterns validation</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- Code postal français (5 chiffres) -->
        <label for="zipcode">Code postal :</label>
        <input 
            type="text" 
            id="zipcode" 
            name="zipcode"
            pattern="[0-9]{5}"
            title="5 chiffres (exemple : 69000)"
            placeholder="69000"
        >
        
        <!-- Téléphone français (10 chiffres) -->
        <label for="phone">Téléphone :</label>
        <input 
            type="tel" 
            id="phone" 
            name="phone"
            pattern="0[1-9][0-9]{8}"
            title="10 chiffres commençant par 0"
            placeholder="0612345678"
        >
        
        <!-- Téléphone avec espaces -->
        <label for="phone-spaces">Téléphone (avec espaces) :</label>
        <input 
            type="tel" 
            id="phone-spaces" 
            name="phone"
            pattern="0[1-9]( [0-9]{2}){4}"
            title="Format : 06 12 34 56 78"
            placeholder="06 12 34 56 78"
        >
        
        <!-- Mot de passe fort (min 8, 1 maj, 1 min, 1 chiffre) -->
        <label for="strong-password">Mot de passe fort :</label>
        <input 
            type="password" 
            id="strong-password" 
            name="password"
            pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}"
            title="Min 8 caractères avec au moins 1 majuscule, 1 minuscule, 1 chiffre"
        >
        
        <!-- Nom d'utilisateur (lettres, chiffres, tirets, underscores) -->
        <label for="username">Nom d'utilisateur :</label>
        <input 
            type="text" 
            id="username" 
            name="username"
            pattern="[a-zA-Z0-9_\-]{3,20}"
            title="3-20 caractères : lettres, chiffres, _ et -"
            placeholder="john_doe"
        >
        
        <!-- URL -->
        <label for="website">Site web :</label>
        <input 
            type="url" 
            id="website" 
            name="website"
            pattern="https?://.+"
            title="URL complète (http:// ou https://)"
            placeholder="https://example.com"
        >
        
        <!-- Hexadécimal couleur -->
        <label for="hex-color">Couleur hexadécimale :</label>
        <input 
            type="text" 
            id="hex-color" 
            name="color"
            pattern="#[0-9A-Fa-f]{6}"
            title="Format : #RRGGBB (exemple : #FF5733)"
            placeholder="#FF5733"
        >
        
        <!-- Carte bancaire (16 chiffres, espaces optionnels) -->
        <label for="credit-card">Numéro de carte :</label>
        <input 
            type="text" 
            id="credit-card" 
            name="card"
            pattern="[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}"
            title="16 chiffres groupés par 4 (exemple : 1234 5678 9012 3456)"
            placeholder="1234 5678 9012 3456"
        >
        
        <button type="submit">Valider</button>
    </form>
</body>
</html>
```

**Patterns regex expliqués :**

```regex
[0-9]{5}               → 5 chiffres (code postal)
0[1-9][0-9]{8}         → 0 suivi de 1-9, puis 8 chiffres (téléphone)
[a-zA-Z0-9_\-]{3,20}   → 3-20 caractères alphanumériques + _ et -
(?=.*[a-z])            → Au moins une minuscule (lookahead)
(?=.*[A-Z])            → Au moins une majuscule
(?=.*[0-9])            → Au moins un chiffre
.{8,}                  → Au moins 8 caractères au total
```

### 7.3 Messages d'Erreur Personnalisés (JavaScript)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Messages personnalisés</title>
</head>
<body>
    <form action="/submit" method="POST" id="custom-form">
        <label for="email">Email :</label>
        <input 
            type="email" 
            id="email" 
            name="email"
            required
        >
        
        <label for="password">Mot de passe :</label>
        <input 
            type="password" 
            id="password" 
            name="password"
            minlength="8"
            required
        >
        
        <button type="submit">Envoyer</button>
    </form>
    
    <script>
        // Personnaliser messages d'erreur
        const form = document.getElementById('custom-form');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        
        emailInput.addEventListener('invalid', function(e) {
            e.preventDefault();
            if (emailInput.validity.valueMissing) {
                emailInput.setCustomValidity('Veuillez saisir votre adresse email');
            } else if (emailInput.validity.typeMismatch) {
                emailInput.setCustomValidity('Veuillez saisir une adresse email valide (exemple@domaine.com)');
            }
        });
        
        emailInput.addEventListener('input', function() {
            emailInput.setCustomValidity('');
        });
        
        passwordInput.addEventListener('invalid', function(e) {
            e.preventDefault();
            if (passwordInput.validity.valueMissing) {
                passwordInput.setCustomValidity('Le mot de passe est obligatoire');
            } else if (passwordInput.validity.tooShort) {
                passwordInput.setCustomValidity('Le mot de passe doit contenir au moins 8 caractères');
            }
        });
        
        passwordInput.addEventListener('input', function() {
            passwordInput.setCustomValidity('');
        });
    </script>
</body>
</html>
```

---

## 8. Attributs Essentiels

### 8.1 Placeholder, Autocomplete, Autofocus

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Attributs essentiels</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- PLACEHOLDER : Texte indicatif -->
        <label for="email">Email :</label>
        <input 
            type="email" 
            id="email" 
            name="email"
            placeholder="nom@exemple.com"
        >
        <!-- ⚠️ Placeholder disparaît à la saisie, ne remplace PAS le label -->
        
        <!-- AUTOCOMPLETE : Auto-complétion navigateur -->
        <label for="firstname">Prénom :</label>
        <input 
            type="text" 
            id="firstname" 
            name="firstname"
            autocomplete="given-name"
        >
        
        <label for="lastname">Nom :</label>
        <input 
            type="text" 
            id="lastname" 
            name="lastname"
            autocomplete="family-name"
        >
        
        <label for="email-auto">Email :</label>
        <input 
            type="email" 
            id="email-auto" 
            name="email"
            autocomplete="email"
        >
        
        <label for="phone">Téléphone :</label>
        <input 
            type="tel" 
            id="phone" 
            name="phone"
            autocomplete="tel"
        >
        
        <label for="address">Adresse :</label>
        <input 
            type="text" 
            id="address" 
            name="address"
            autocomplete="street-address"
        >
        
        <label for="zipcode">Code postal :</label>
        <input 
            type="text" 
            id="zipcode" 
            name="zipcode"
            autocomplete="postal-code"
        >
        
        <label for="city">Ville :</label>
        <input 
            type="text" 
            id="city" 
            name="city"
            autocomplete="address-level2"
        >
        
        <label for="country">Pays :</label>
        <input 
            type="text" 
            id="country" 
            name="country"
            autocomplete="country-name"
        >
        
        <!-- Désactiver autocomplete -->
        <label for="verification-code">Code de vérification :</label>
        <input 
            type="text" 
            id="verification-code" 
            name="code"
            autocomplete="off"
        >
        
        <!-- AUTOFOCUS : Focus automatique au chargement -->
        <label for="search">Recherche :</label>
        <input 
            type="search" 
            id="search" 
            name="q"
            autofocus
        >
        <!-- ⚠️ Un seul autofocus par page -->
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Valeurs autocomplete courantes :**

| Valeur | Usage | Exemple |
|--------|-------|---------|
| `name` | Nom complet | John Doe |
| `given-name` | Prénom | John |
| `family-name` | Nom de famille | Doe |
| `email` | Email | john@example.com |
| `tel` | Téléphone | +33612345678 |
| `street-address` | Adresse complète | 123 Rue Example |
| `postal-code` | Code postal | 75001 |
| `address-level2` | Ville | Paris |
| `country-name` | Pays | France |
| `cc-name` | Nom sur carte bancaire | John Doe |
| `cc-number` | Numéro carte | 1234567890123456 |
| `cc-exp` | Expiration carte | 12/2025 |
| `cc-csc` | CVV | 123 |
| `username` | Nom d'utilisateur | johndoe |
| `new-password` | Nouveau mot de passe | (génération auto) |
| `current-password` | Mot de passe actuel | (sauvegardé) |

### 8.2 Readonly et Disabled

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Readonly vs Disabled</title>
</head>
<body>
    <form action="/submit" method="POST">
        <!-- READONLY : Lecture seule (envoyé au serveur) -->
        <label for="user-id">ID Utilisateur :</label>
        <input 
            type="text" 
            id="user-id" 
            name="user-id"
            value="12345"
            readonly
        >
        <!-- Utilisateur ne peut pas modifier, mais donnée envoyée -->
        
        <label for="email">Email (vérifié) :</label>
        <input 
            type="email" 
            id="email" 
            name="email"
            value="alice@example.com"
            readonly
        >
        
        <!-- DISABLED : Désactivé (PAS envoyé au serveur) -->
        <label for="promo-code">Code promo :</label>
        <input 
            type="text" 
            id="promo-code" 
            name="promo-code"
            value="EXPIRED2023"
            disabled
        >
        <!-- Grisé, non modifiable, NON envoyé au serveur -->
        
        <label>
            <input 
                type="checkbox" 
                name="terms" 
                disabled
            >
            Conditions acceptées (déjà validé)
        </label>
        
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
```

**Différence Readonly vs Disabled :**

| Attribut | Modifiable | Envoyé serveur | Focusable | Apparence |
|----------|------------|----------------|-----------|-----------|
| `readonly` | ❌ Non | ✅ **Oui** | ✅ Oui | Normal |
| `disabled` | ❌ Non | ❌ **Non** | ❌ Non | Grisé |

**Quand utiliser :**

- `readonly` : Donnée calculée, ID, valeur confirmée (envoyée au serveur)
- `disabled` : Champ temporairement indisponible, option non applicable

---

## 9. Exercices Pratiques

### Exercice 1 : Formulaire d'Inscription

**Objectif :** Créer un formulaire d'inscription complet avec validation.

**Consigne :** Créer un formulaire avec :
- Nom d'utilisateur (3-20 caractères, alphanumérique)
- Email (validation email)
- Mot de passe (min 8 caractères)
- Confirmation mot de passe
- Date de naissance (adulte 18+)
- Genre (radio buttons)
- Acceptation CGV (checkbox obligatoire)

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inscription</title>
</head>
<body>
    <h1>Créer un compte</h1>
    
    <form action="/register" method="POST">
        <fieldset>
            <legend>Informations de connexion</legend>
            
            <label for="username">Nom d'utilisateur : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="username" 
                name="username"
                pattern="[a-zA-Z0-9_]{3,20}"
                title="3-20 caractères : lettres, chiffres, underscore"
                placeholder="john_doe"
                required
            >
            
            <label for="email">Email : <span style="color: red;">*</span></label>
            <input 
                type="email" 
                id="email" 
                name="email"
                placeholder="nom@exemple.com"
                autocomplete="email"
                required
            >
            
            <label for="password">Mot de passe : <span style="color: red;">*</span></label>
            <input 
                type="password" 
                id="password" 
                name="password"
                minlength="8"
                pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}"
                title="Min 8 caractères avec au moins 1 majuscule, 1 minuscule, 1 chiffre"
                autocomplete="new-password"
                required
            >
            
            <label for="password-confirm">Confirmer le mot de passe : <span style="color: red;">*</span></label>
            <input 
                type="password" 
                id="password-confirm" 
                name="password-confirm"
                minlength="8"
                autocomplete="new-password"
                required
            >
        </fieldset>
        
        <fieldset>
            <legend>Informations personnelles</legend>
            
            <label for="firstname">Prénom :</label>
            <input 
                type="text" 
                id="firstname" 
                name="firstname"
                autocomplete="given-name"
            >
            
            <label for="lastname">Nom :</label>
            <input 
                type="text" 
                id="lastname" 
                name="lastname"
                autocomplete="family-name"
            >
            
            <label for="birthdate">Date de naissance : <span style="color: red;">*</span></label>
            <input 
                type="date" 
                id="birthdate" 
                name="birthdate"
                max="2006-12-31"
                autocomplete="bday"
                required
            >
            <small>Vous devez avoir au moins 18 ans</small>
            
            <fieldset>
                <legend>Genre :</legend>
                
                <label>
                    <input type="radio" name="gender" value="male">
                    Homme
                </label>
                
                <label>
                    <input type="radio" name="gender" value="female">
                    Femme
                </label>
                
                <label>
                    <input type="radio" name="gender" value="other">
                    Autre
                </label>
                
                <label>
                    <input type="radio" name="gender" value="prefer-not-to-say">
                    Préfère ne pas répondre
                </label>
            </fieldset>
        </fieldset>
        
        <fieldset>
            <legend>Conditions</legend>
            
            <label>
                <input type="checkbox" name="terms" value="accepted" required>
                J'accepte les <a href="/terms" target="_blank">Conditions Générales d'Utilisation</a> <span style="color: red;">*</span>
            </label>
            
            <label>
                <input type="checkbox" name="newsletter" value="yes">
                Je souhaite recevoir la newsletter
            </label>
        </fieldset>
        
        <button type="submit">Créer mon compte</button>
        
        <p><small><span style="color: red;">*</span> Champs obligatoires</small></p>
    </form>
</body>
</html>
```

</details>

### Exercice 2 : Formulaire de Contact

**Objectif :** Créer un formulaire de contact accessible.

**Consigne :** Créer un formulaire avec :
- Nom complet
- Email
- Téléphone (optionnel)
- Sujet (liste déroulante)
- Message (textarea, 500 caractères max)
- Fichier joint (optionnel, images uniquement)

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact</title>
</head>
<body>
    <h1>Nous contacter</h1>
    
    <form action="/contact" method="POST" enctype="multipart/form-data">
        <fieldset>
            <legend>Vos coordonnées</legend>
            
            <label for="fullname">Nom complet : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="fullname" 
                name="fullname"
                autocomplete="name"
                required
            >
            
            <label for="email">Email : <span style="color: red;">*</span></label>
            <input 
                type="email" 
                id="email" 
                name="email"
                placeholder="nom@exemple.com"
                autocomplete="email"
                required
            >
            
            <label for="phone">Téléphone (optionnel) :</label>
            <input 
                type="tel" 
                id="phone" 
                name="phone"
                pattern="0[1-9]( [0-9]{2}){4}"
                title="Format : 06 12 34 56 78"
                placeholder="06 12 34 56 78"
                autocomplete="tel"
            >
        </fieldset>
        
        <fieldset>
            <legend>Votre message</legend>
            
            <label for="subject">Sujet : <span style="color: red;">*</span></label>
            <select id="subject" name="subject" required>
                <option value="">-- Choisir un sujet --</option>
                <option value="info">Demande d'information</option>
                <option value="support">Support technique</option>
                <option value="sales">Question commerciale</option>
                <option value="partnership">Partenariat</option>
                <option value="other">Autre</option>
            </select>
            
            <label for="message">Message (max 500 caractères) : <span style="color: red;">*</span></label>
            <textarea 
                id="message" 
                name="message"
                rows="8"
                maxlength="500"
                placeholder="Décrivez votre demande..."
                required
            ></textarea>
            <small id="char-count">0 / 500 caractères</small>
            
            <label for="attachment">Pièce jointe (optionnelle) :</label>
            <input 
                type="file" 
                id="attachment" 
                name="attachment"
                accept="image/png, image/jpeg, application/pdf"
            >
            <small>Formats acceptés : JPG, PNG, PDF (max 5 Mo)</small>
        </fieldset>
        
        <button type="submit">Envoyer le message</button>
        
        <p><small><span style="color: red;">*</span> Champs obligatoires</small></p>
    </form>
    
    <script>
        // Compteur de caractères
        const messageTextarea = document.getElementById('message');
        const charCount = document.getElementById('char-count');
        
        messageTextarea.addEventListener('input', function() {
            const length = this.value.length;
            charCount.textContent = `${length} / 500 caractères`;
            
            if (length > 450) {
                charCount.style.color = 'red';
            } else {
                charCount.style.color = 'black';
            }
        });
    </script>
</body>
</html>
```

</details>

### Exercice 3 : Formulaire de Commande

**Objectif :** Créer un formulaire de commande e-commerce.

**Consigne :** Créer un formulaire avec :
- Adresse de livraison (fieldset)
- Méthode de livraison (radio)
- Informations paiement (fieldset)
- Validation complète

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commander</title>
</head>
<body>
    <h1>Finaliser la commande</h1>
    
    <form action="/checkout" method="POST">
        <fieldset>
            <legend>Adresse de livraison</legend>
            
            <label for="firstname">Prénom : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="firstname" 
                name="firstname"
                autocomplete="given-name"
                required
            >
            
            <label for="lastname">Nom : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="lastname" 
                name="lastname"
                autocomplete="family-name"
                required
            >
            
            <label for="address">Adresse : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="address" 
                name="address"
                placeholder="Numéro et nom de rue"
                autocomplete="street-address"
                required
            >
            
            <label for="address2">Complément d'adresse (optionnel) :</label>
            <input 
                type="text" 
                id="address2" 
                name="address2"
                placeholder="Appartement, bâtiment..."
                autocomplete="address-line2"
            >
            
            <label for="zipcode">Code postal : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="zipcode" 
                name="zipcode"
                pattern="[0-9]{5}"
                title="5 chiffres"
                placeholder="75001"
                autocomplete="postal-code"
                required
            >
            
            <label for="city">Ville : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="city" 
                name="city"
                autocomplete="address-level2"
                required
            >
            
            <label for="phone">Téléphone : <span style="color: red;">*</span></label>
            <input 
                type="tel" 
                id="phone" 
                name="phone"
                pattern="0[1-9]( [0-9]{2}){4}"
                title="Format : 06 12 34 56 78"
                placeholder="06 12 34 56 78"
                autocomplete="tel"
                required
            >
        </fieldset>
        
        <fieldset>
            <legend>Méthode de livraison : <span style="color: red;">*</span></legend>
            
            <label>
                <input 
                    type="radio" 
                    name="shipping" 
                    value="standard"
                    required
                >
                Standard (3-5 jours ouvrés) - <strong>Gratuit</strong>
            </label>
            
            <label>
                <input 
                    type="radio" 
                    name="shipping" 
                    value="express"
                >
                Express (24-48h) - <strong>9,99 €</strong>
            </label>
            
            <label>
                <input 
                    type="radio" 
                    name="shipping" 
                    value="relay"
                >
                Point relais (2-4 jours) - <strong>4,99 €</strong>
            </label>
        </fieldset>
        
        <fieldset>
            <legend>Informations de paiement</legend>
            
            <label for="card-name">Nom sur la carte : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="card-name" 
                name="card-name"
                autocomplete="cc-name"
                required
            >
            
            <label for="card-number">Numéro de carte : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="card-number" 
                name="card-number"
                pattern="[0-9]{16}"
                title="16 chiffres"
                placeholder="1234567890123456"
                autocomplete="cc-number"
                maxlength="16"
                required
            >
            
            <label for="card-expiry">Date d'expiration : <span style="color: red;">*</span></label>
            <input 
                type="month" 
                id="card-expiry" 
                name="card-expiry"
                min="2024-01"
                autocomplete="cc-exp"
                required
            >
            
            <label for="card-cvv">CVV : <span style="color: red;">*</span></label>
            <input 
                type="text" 
                id="card-cvv" 
                name="card-cvv"
                pattern="[0-9]{3}"
                title="3 chiffres au dos de la carte"
                placeholder="123"
                autocomplete="cc-csc"
                maxlength="3"
                required
            >
        </fieldset>
        
        <fieldset>
            <legend>Options</legend>
            
            <label>
                <input type="checkbox" name="save-info" value="yes">
                Enregistrer mes informations pour les prochaines commandes
            </label>
            
            <label>
                <input type="checkbox" name="gift" value="yes">
                C'est un cadeau (emballage cadeau gratuit)
            </label>
        </fieldset>
        
        <button type="submit">Passer la commande</button>
        
        <p><small><span style="color: red;">*</span> Champs obligatoires</small></p>
    </form>
</body>
</html>
```

</details>

---

## 10. Projet du Module : Formulaire Multi-Étapes

### 10.1 Cahier des Charges

**Créer un formulaire d'inscription multi-étapes complet :**

**Spécifications techniques :**
- ✅ 3 étapes (Compte, Profil, Préférences)
- ✅ Tous types d'input utilisés
- ✅ Validation HTML5 complète
- ✅ Labels explicites pour accessibilité
- ✅ Fieldset et legend pour groupes
- ✅ Autocomplete approprié
- ✅ Messages d'aide (title, placeholder)
- ✅ Code validé W3C

**Fonctionnalités :**
1. Étape 1 : Création compte (username, email, password)
2. Étape 2 : Profil (nom, prénom, date naissance, photo)
3. Étape 3 : Préférences (centres d'intérêt, notifications)

### 10.2 Solution Complète

<details>
<summary>Voir la solution complète du projet</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inscription Multi-Étapes</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        
        .step {
            display: none;
        }
        
        .step.active {
            display: block;
        }
        
        .progress-bar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
        }
        
        .progress-step {
            flex: 1;
            text-align: center;
            padding: 10px;
            background: #e0e0e0;
            position: relative;
        }
        
        .progress-step.active {
            background: #4CAF50;
            color: white;
        }
        
        .progress-step.completed {
            background: #2196F3;
            color: white;
        }
        
        fieldset {
            border: 1px solid #ddd;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        legend {
            font-weight: bold;
            padding: 0 10px;
        }
        
        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
        }
        
        input, select, textarea {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            box-sizing: border-box;
        }
        
        input[type="checkbox"],
        input[type="radio"] {
            width: auto;
            margin-right: 5px;
        }
        
        button {
            padding: 10px 20px;
            margin-top: 20px;
            margin-right: 10px;
            cursor: pointer;
        }
        
        button[type="submit"] {
            background-color: #4CAF50;
            color: white;
            border: none;
        }
        
        .error {
            color: red;
            font-size: 0.9em;
        }
        
        small {
            color: #666;
            font-size: 0.85em;
        }
    </style>
</head>
<body>
    <h1>Inscription</h1>
    
    <!-- Barre de progression -->
    <div class="progress-bar">
        <div class="progress-step active" id="progress-1">Étape 1 : Compte</div>
        <div class="progress-step" id="progress-2">Étape 2 : Profil</div>
        <div class="progress-step" id="progress-3">Étape 3 : Préférences</div>
    </div>
    
    <form action="/register" method="POST" enctype="multipart/form-data" id="registration-form">
        
        <!-- Étape 1 : Création compte -->
        <div class="step active" id="step-1">
            <fieldset>
                <legend>Créer votre compte</legend>
                
                <label for="username">
                    Nom d'utilisateur : <span class="error">*</span>
                </label>
                <input 
                    type="text" 
                    id="username" 
                    name="username"
                    pattern="[a-zA-Z0-9_]{3,20}"
                    title="3-20 caractères : lettres, chiffres, underscore"
                    placeholder="john_doe"
                    autocomplete="username"
                    required
                >
                <small>3-20 caractères : lettres, chiffres, underscore uniquement</small>
                
                <label for="email">
                    Adresse email : <span class="error">*</span>
                </label>
                <input 
                    type="email" 
                    id="email" 
                    name="email"
                    placeholder="nom@exemple.com"
                    autocomplete="email"
                    required
                >
                
                <label for="password">
                    Mot de passe : <span class="error">*</span>
                </label>
                <input 
                    type="password" 
                    id="password" 
                    name="password"
                    minlength="8"
                    pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}"
                    title="Minimum 8 caractères avec au moins 1 majuscule, 1 minuscule et 1 chiffre"
                    autocomplete="new-password"
                    required
                >
                <small>Minimum 8 caractères avec au moins 1 majuscule, 1 minuscule et 1 chiffre</small>
                
                <label for="password-confirm">
                    Confirmer le mot de passe : <span class="error">*</span>
                </label>
                <input 
                    type="password" 
                    id="password-confirm" 
                    name="password-confirm"
                    minlength="8"
                    autocomplete="new-password"
                    required
                >
            </fieldset>
            
            <button type="button" onclick="nextStep(1)">Suivant →</button>
        </div>
        
        <!-- Étape 2 : Profil -->
        <div class="step" id="step-2">
            <fieldset>
                <legend>Votre profil</legend>
                
                <label for="firstname">
                    Prénom : <span class="error">*</span>
                </label>
                <input 
                    type="text" 
                    id="firstname" 
                    name="firstname"
                    autocomplete="given-name"
                    required
                >
                
                <label for="lastname">
                    Nom : <span class="error">*</span>
                </label>
                <input 
                    type="text" 
                    id="lastname" 
                    name="lastname"
                    autocomplete="family-name"
                    required
                >
                
                <label for="birthdate">
                    Date de naissance : <span class="error">*</span>
                </label>
                <input 
                    type="date" 
                    id="birthdate" 
                    name="birthdate"
                    max="2006-12-31"
                    autocomplete="bday"
                    required
                >
                <small>Vous devez avoir au moins 18 ans</small>
                
                <label for="phone">
                    Téléphone :
                </label>
                <input 
                    type="tel" 
                    id="phone" 
                    name="phone"
                    pattern="0[1-9]( [0-9]{2}){4}"
                    title="Format : 06 12 34 56 78"
                    placeholder="06 12 34 56 78"
                    autocomplete="tel"
                >
                
                <label for="avatar">
                    Photo de profil :
                </label>
                <input 
                    type="file" 
                    id="avatar" 
                    name="avatar"
                    accept="image/png, image/jpeg"
                >
                <small>Formats acceptés : JPG, PNG (max 2 Mo)</small>
            </fieldset>
            
            <fieldset>
                <legend>Genre</legend>
                
                <label>
                    <input type="radio" name="gender" value="male">
                    Homme
                </label>
                
                <label>
                    <input type="radio" name="gender" value="female">
                    Femme
                </label>
                
                <label>
                    <input type="radio" name="gender" value="other">
                    Autre
                </label>
                
                <label>
                    <input type="radio" name="gender" value="prefer-not-to-say">
                    Préfère ne pas répondre
                </label>
            </fieldset>
            
            <button type="button" onclick="prevStep(2)">← Précédent</button>
            <button type="button" onclick="nextStep(2)">Suivant →</button>
        </div>
        
        <!-- Étape 3 : Préférences -->
        <div class="step" id="step-3">
            <fieldset>
                <legend>Centres d'intérêt</legend>
                <p><small>Sélectionnez vos domaines d'intérêt</small></p>
                
                <label>
                    <input type="checkbox" name="interests[]" value="tech">
                    Technologie
                </label>
                
                <label>
                    <input type="checkbox" name="interests[]" value="sport">
                    Sport
                </label>
                
                <label>
                    <input type="checkbox" name="interests[]" value="art">
                    Art et Culture
                </label>
                
                <label>
                    <input type="checkbox" name="interests[]" value="travel">
                    Voyage
                </label>
                
                <label>
                    <input type="checkbox" name="interests[]" value="food">
                    Gastronomie
                </label>
                
                <label>
                    <input type="checkbox" name="interests[]" value="music">
                    Musique
                </label>
                
                <label>
                    <input type="checkbox" name="interests[]" value="books">
                    Lecture
                </label>
                
                <label>
                    <input type="checkbox" name="interests[]" value="gaming">
                    Jeux vidéo
                </label>
            </fieldset>
            
            <fieldset>
                <legend>Notifications</legend>
                
                <label>
                    <input type="checkbox" name="notifications[]" value="email">
                    Recevoir des notifications par email
                </label>
                
                <label>
                    <input type="checkbox" name="notifications[]" value="sms">
                    Recevoir des notifications par SMS
                </label>
                
                <label>
                    <input type="checkbox" name="notifications[]" value="push">
                    Recevoir des notifications push
                </label>
            </fieldset>
            
            <fieldset>
                <legend>Fréquence newsletter</legend>
                
                <label for="newsletter-frequency">
                    À quelle fréquence souhaitez-vous recevoir notre newsletter ?
                </label>
                <select id="newsletter-frequency" name="newsletter-frequency">
                    <option value="never">Jamais</option>
                    <option value="daily">Quotidienne</option>
                    <option value="weekly" selected>Hebdomadaire</option>
                    <option value="monthly">Mensuelle</option>
                </select>
            </fieldset>
            
            <fieldset>
                <legend>Biographie (optionnelle)</legend>
                
                <label for="bio">
                    Parlez-nous de vous :
                </label>
                <textarea 
                    id="bio" 
                    name="bio"
                    rows="5"
                    maxlength="500"
                    placeholder="Décrivez vos passions, votre parcours..."
                ></textarea>
                <small id="bio-count">0 / 500 caractères</small>
            </fieldset>
            
            <fieldset>
                <legend>Conditions d'utilisation</legend>
                
                <label>
                    <input type="checkbox" name="terms" value="accepted" required>
                    J'accepte les <a href="/terms" target="_blank">Conditions Générales d'Utilisation</a> <span class="error">*</span>
                </label>
                
                <label>
                    <input type="checkbox" name="privacy" value="accepted" required>
                    J'accepte la <a href="/privacy" target="_blank">Politique de Confidentialité</a> <span class="error">*</span>
                </label>
                
                <label>
                    <input type="checkbox" name="age" value="confirmed" required>
                    Je confirme avoir au moins 18 ans <span class="error">*</span>
                </label>
            </fieldset>
            
            <button type="button" onclick="prevStep(3)">← Précédent</button>
            <button type="submit">Créer mon compte</button>
        </div>
        
        <p><small><span class="error">*</span> Champs obligatoires</small></p>
    </form>
    
    <script>
        // Navigation entre étapes
        function nextStep(currentStep) {
            // Valider l'étape actuelle
            const currentStepDiv = document.getElementById(`step-${currentStep}`);
            const inputs = currentStepDiv.querySelectorAll('input[required], select[required]');
            
            let valid = true;
            inputs.forEach(input => {
                if (!input.checkValidity()) {
                    input.reportValidity();
                    valid = false;
                }
            });
            
            if (!valid) return;
            
            // Vérifier confirmation mot de passe (étape 1)
            if (currentStep === 1) {
                const password = document.getElementById('password').value;
                const confirm = document.getElementById('password-confirm').value;
                
                if (password !== confirm) {
                    alert('Les mots de passe ne correspondent pas');
                    return;
                }
            }
            
            // Masquer étape actuelle
            currentStepDiv.classList.remove('active');
            document.getElementById(`progress-${currentStep}`).classList.add('completed');
            
            // Afficher étape suivante
            const nextStep = currentStep + 1;
            document.getElementById(`step-${nextStep}`).classList.add('active');
            document.getElementById(`progress-${nextStep}`).classList.add('active');
            
            // Scroll en haut
            window.scrollTo(0, 0);
        }
        
        function prevStep(currentStep) {
            // Masquer étape actuelle
            document.getElementById(`step-${currentStep}`).classList.remove('active');
            document.getElementById(`progress-${currentStep}`).classList.remove('active');
            
            // Afficher étape précédente
            const prevStep = currentStep - 1;
            document.getElementById(`step-${prevStep}`).classList.add('active');
            document.getElementById(`progress-${prevStep}`).classList.remove('completed');
            
            // Scroll en haut
            window.scrollTo(0, 0);
        }
        
        // Compteur caractères bio
        const bioTextarea = document.getElementById('bio');
        const bioCount = document.getElementById('bio-count');
        
        bioTextarea.addEventListener('input', function() {
            const length = this.value.length;
            bioCount.textContent = `${length} / 500 caractères`;
            
            if (length > 450) {
                bioCount.style.color = 'red';
            } else {
                bioCount.style.color = '#666';
            }
        });
    </script>
</body>
</html>
```

</details>

### 10.3 Checklist de Validation

Avant de considérer votre projet terminé, vérifiez :

- [ ] 3 étapes fonctionnelles avec navigation
- [ ] Tous types d'input utilisés (text, email, password, date, file, etc.)
- [ ] Labels explicites pour tous les champs
- [ ] Attribut `name` sur tous les inputs
- [ ] Validation HTML5 (required, pattern, min, max, etc.)
- [ ] Fieldset et legend pour regroupements logiques
- [ ] Autocomplete approprié sur champs
- [ ] Placeholder et title pour aide utilisateur
- [ ] Checkbox CGV obligatoire
- [ ] Vérification confirmation mot de passe (JavaScript)
- [ ] Messages d'aide (small) sous champs complexes
- [ ] Code indenté et validé W3C

---

## 11. Best Practices

### 11.1 Accessibilité

```html
<!-- ✅ BON : Accessibilité complète -->

<!-- 1. Labels TOUJOURS associés -->
<label for="email">Email :</label>
<input type="email" id="email" name="email" required>

<!-- 2. Fieldset pour groupes radio/checkbox -->
<fieldset>
    <legend>Genre :</legend>
    <label><input type="radio" name="gender" value="male"> Homme</label>
    <label><input type="radio" name="gender" value="female"> Femme</label>
</fieldset>

<!-- 3. Messages d'erreur clairs -->
<input 
    type="tel"
    pattern="[0-9]{10}"
    title="10 chiffres sans espaces"
>

<!-- 4. Indication champs obligatoires -->
<label>
    Nom : <span style="color: red;" aria-label="obligatoire">*</span>
</label>

<!-- 5. Autocomplete pour faciliter saisie -->
<input type="email" autocomplete="email">
```

### 11.2 Sécurité

```html
<!-- ✅ Validation CÔTÉ SERVEUR obligatoire -->
<!-- HTML5 = contournable côté client -->

<!-- ❌ MAUVAIS : Se fier uniquement à HTML5 -->
<input type="email" required>
<!-- Utilisateur malveillant peut bypasser avec DevTools -->

<!-- ✅ BON : HTML5 + Validation serveur -->
<input type="email" required>
<!-- + validation PHP/Node.js/Python côté serveur -->

<!-- ⚠️ Sécurité formulaires -->
<!-- 1. CSRF Token (protection attaques) -->
<input type="hidden" name="csrf-token" value="abc123xyz">

<!-- 2. Limiter upload fichiers -->
<input type="file" accept="image/*">
<!-- + Vérification type MIME côté serveur -->
<!-- + Limite taille fichier côté serveur -->

<!-- 3. HTTPS obligatoire (surtout pour passwords) -->
<!-- 4. Rate limiting côté serveur (anti-spam) -->
```

### 11.3 UX (Expérience Utilisateur)

```html
<!-- ✅ BON : UX optimale -->

<!-- 1. Placeholder informatif (mais pas à la place du label) -->
<label for="phone">Téléphone :</label>
<input 
    type="tel" 
    id="phone"
    placeholder="06 12 34 56 78"
>

<!-- 2. Autofocus sur premier champ (sauf mobile) -->
<input type="text" name="search" autofocus>

<!-- 3. Autocomplete pour gagner du temps -->
<input type="email" autocomplete="email">

<!-- 4. Messages d'erreur utiles -->
<input 
    type="tel"
    pattern="[0-9]{10}"
    title="Format : 10 chiffres (ex: 0612345678)"
>

<!-- 5. Regrouper logiquement (fieldset) -->
<fieldset>
    <legend>Adresse</legend>
    <!-- Champs adresse groupés -->
</fieldset>

<!-- 6. Bouton submit clair -->
<button type="submit">Créer mon compte</button>
<!-- Pas "Envoyer", "Valider" (vague) -->

<!-- 7. Indication progression (formulaires longs) -->
<p>Étape 2 sur 3</p>
```

---

## 12. Checkpoint de Progression

### À la fin de ce Module 5, vous maîtrisez :

**Structure formulaires :**
- [x] Balise `<form>` (action, method, enctype)
- [x] GET vs POST
- [x] Labels obligatoires (accessibilité)
- [x] Attribut `name` (envoi serveur)

**Types d'input :**
- [x] Texte (text, email, password, tel, url)
- [x] Numériques (number, range)
- [x] Dates (date, time, datetime-local, month, week)
- [x] Spéciaux (color, file, search, hidden)
- [x] Checkbox et radio buttons
- [x] Textarea (multi-lignes)
- [x] Select (listes déroulantes)

**Structure avancée :**
- [x] Fieldset et legend (groupes)
- [x] Optgroup (groupes select)

**Validation HTML5 :**
- [x] Attributs (required, minlength, maxlength, min, max)
- [x] Pattern (regex validation)
- [x] Messages personnalisés (JavaScript)

**Attributs essentiels :**
- [x] Placeholder, autocomplete, autofocus
- [x] Readonly vs disabled
- [x] Title (message d'aide)

**Best practices :**
- [x] Accessibilité (labels, fieldset, scope)
- [x] Sécurité (validation serveur, CSRF)
- [x] UX (messages clairs, auto-complétion)

### Prochaine Étape

**Direction le Module 6** où vous allez :
- Maîtriser la sémantique HTML5 complète
- Utiliser header, nav, main, article, section, aside, footer
- Structurer pages accessibles
- Comprendre outline et hiérarchie
- Implémenter breadcrumbs et navigation
- Créer layouts sémantiques professionnels

[:lucide-arrow-right: Accéder au Module 6 - Sémantique HTML5](./module-06-semantique-html5/)

---

**Module 5 Terminé - Bravo ! 🎉 📝**

**Vous avez appris :**
- ✅ Structure complète formulaires (form, label, input)
- ✅ 15+ types d'input HTML5 maîtrisés
- ✅ Validation HTML5 professionnelle (required, pattern, etc.)
- ✅ Checkbox, radio, select, textarea
- ✅ Fieldset et legend (groupes logiques)
- ✅ Autocomplete et accessibilité
- ✅ Best practices sécurité et UX
- ✅ Formulaire multi-étapes complet

**Statistiques Module 5 :**
- 1 projet complet (Formulaire multi-étapes)
- 3 exercices progressifs avec solutions
- 90+ exemples de code
- Formulaires professionnels maîtrisés

**Prochain objectif : Maîtriser la sémantique HTML5 (Module 6)**

**Félicitations pour cette maîtrise des formulaires HTML ! 🚀📝**
