---
description: "Maîtriser les formulaires HTML : input, label, fieldset, datalist, validation native, textarea, select et les types modernes."
icon: lucide/book-open-check
tags: ["HTML", "FORMULAIRES", "INPUT", "INTERACTION", "ACCESSIBILITÉ", "VALIDATION"]
---

# Les Formulaires

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.1"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - La Communication Bidirectionnelle"
    Jusqu'à présent, vos sites Web étaient des monuments statiques : l'utilisateur consomme ce que vous lui donnez, sans jamais pouvoir interagir. Le **Formulaire HTML** casse ce mur. C'est l'outil universel qui permet à votre visiteur de vous **envoyer** de la donnée — un mail de contact, une création de compte, un paiement bancaire.

    La création d'un formulaire exige une rigueur technique précise. Des `<label>` mal configurés rendent le formulaire inutilisable pour les personnes malvoyantes. Le mauvais `type` sur un `<input>` prive les utilisateurs mobiles du bon clavier natif. Une validation absente côté HTML expose votre serveur à des données invalides.

Ce module vous apprend à créer des formulaires professionnels, accessibles, validés et exploitables.

<br>

---

## La balise maîtresse `<form>`

Tout formulaire doit être enveloppé dans la balise `<form>`. Elle définit **comment** et **vers où** les données seront envoyées au serveur.

```html title="HTML - Structure fondamentale d'un formulaire"
<!-- Un formulaire de recherche simple -->
<form action="/recherche" method="GET">
    <!-- Les champs et boutons se placent ici -->
</form>
```

<br>

### GET vs POST : la méthode d'envoi

L'attribut `method` dicte comment les données transitent du navigateur vers le serveur.

| Méthode | Visibilité | Usage correct |
| --- | --- | --- |
| `GET` | Visible dans l'URL (`?q=chaussure`) | Recherche, filtres, navigation — jamais pour des données sensibles. |
| `POST` | Dans le corps de la requête HTTP | Mots de passe, inscriptions, paiements, tout envoi de fichier. |

<br>

### Les attributs essentiels de `<form>`

```html title="HTML - Attributs complets de la balise form"
<!--
    action  : URL de destination des données (chemin absolu ou relatif).
    method  : GET ou POST.
    enctype : Type d'encodage. Obligatoire si le formulaire contient un input type="file".
    novalidate : Désactive la validation native HTML5 (utile quand on gère la
                 validation côté JavaScript ou framework).
    autocomplete : "on" ou "off" — contrôle le remplissage automatique du navigateur.
-->
<form
    action="/profil/modifier"
    method="POST"
    enctype="multipart/form-data"
    autocomplete="off"
>
    <!-- Champs du formulaire -->
</form>
```

!!! warning "L'oubli fatal de `enctype` sur les formulaires avec fichiers"
    Sans `enctype="multipart/form-data"`, les fichiers sélectionnés via `<input type="file">` **ne sont jamais envoyés au serveur**. Le formulaire envoie uniquement le nom du fichier en texte, pas son contenu. C'est l'une des erreurs les plus fréquentes des développeurs débutants.

!!! info "L'attribut `novalidate`"
    Par défaut, le navigateur valide les champs avant soumission (champs `required`, format `email`, etc.). L'attribut `novalidate` sur `<form>` désactive entièrement cette validation native. À utiliser uniquement quand vous prenez en charge la validation vous-même — via JavaScript, Alpine.js, ou Laravel Form Requests.

<br>

---

## Le duo fondamental : `<label>` et `<input>`

Chaque champ de saisie doit avoir une étiquette officielle. Placer un paragraphe avant un champ n'est pas une étiquette — c'est du texte décoratif sans lien sémantique.

<br>

### Lier un label à un input

La liaison s'effectue par correspondance entre l'attribut `for` du label et l'attribut `id` de l'input.

```html title="HTML - Liaison label et input via id et for"
<form action="/contact" method="POST">
    <!-- for="email_user" lie ce label à l'input dont l'id est "email_user" -->
    <label for="email_user">Votre adresse e-mail :</label>

    <!-- id="email_user" reçoit le focus au clic sur le label -->
    <!-- name="email_user" est la variable reçue par le serveur PHP/Python -->
    <input type="email" id="email_user" name="email_user" required>

    <button type="submit">S'inscrire</button>
</form>
```

*Cliquer sur le texte du `<label>` déplace le focus directement sur le champ associé. La zone de clic est ainsi élargie — particulièrement précieux sur mobile.*

!!! tip "Liaison implicite par imbrication"
    Placer le `<input>` **à l'intérieur** du `<label>` crée une liaison automatique sans nécessiter `id` et `for`. C'est une technique valide mais qui rend le ciblage CSS moins précis.

    ```html title="HTML - Liaison implicite par imbrication"
    <label>
        <!-- Le navigateur lie automatiquement ce label à l'input qu'il contient -->
        Accepter les CGU
        <input type="checkbox" name="cgu" value="yes" required>
    </label>
    ```

<br>

### L'attribut `name` : la variable côté serveur

L'attribut `id` ne sert qu'au CSS et au `label`. C'est l'attribut `name` qui détermine le nom de la variable transmise au serveur. **Sans `name`, le champ est ignoré lors de l'envoi.**

```html title="HTML - Distinction id et name"
<!--
    id="prenom"   → utilisé par label for="prenom" et le CSS
    name="prenom" → reçu côté serveur comme $_POST['prenom'] en PHP
                    ou request('prenom') en Laravel
-->
<input type="text" id="prenom" name="prenom">
```

<br>

### Les champs cachés (`<input type="hidden">`)

Les champs cachés transmettent des données au serveur sans les afficher à l'utilisateur. Ils sont fondamentaux en PHP et Laravel — notamment pour les tokens CSRF[^1] et les identifiants d'enregistrements.

```html title="HTML - Champs cachés pour les tokens et identifiants"
<form action="/articles/modifier" method="POST">
    <!-- Transmis au serveur mais invisible à l'écran -->
    <!-- En Laravel, @csrf génère automatiquement ce type de champ -->
    <input type="hidden" name="_token" value="abc123xyz...">

    <!-- L'ID de l'article à modifier, invisible mais transmis -->
    <input type="hidden" name="article_id" value="42">

    <label for="titre">Titre de l'article :</label>
    <input type="text" id="titre" name="titre" required>

    <button type="submit">Enregistrer</button>
</form>
```

*Un champ `type="hidden"` est **visible dans le code source** de la page. Il ne convient pas pour des données réellement confidentielles — uniquement pour des identifiants techniques non sensibles.*

<br>

---

## Les types d'`<input>` HTML5

HTML5 a introduit des types de champs spécialisés qui déclenchent des interfaces natives adaptées à chaque appareil et chaque type de donnée.

<br>

### Tableau complet des types d'input

| Type | Comportement | Usage |
| --- | --- | --- |
| `text` | Texte libre une ligne | Nom, prénom, titre |
| `email` | Clavier avec `@` sur mobile, validation format | Adresse e-mail |
| `password` | Caractères masqués en `••••` | Mots de passe |
| `tel` | Clavier numérique sur mobile | Numéro de téléphone |
| `number` | Flèches d'incrément, valeurs min/max | Âge, quantité |
| `date` | Sélecteur de calendrier natif | Date de naissance, rendez-vous |
| `time` | Sélecteur d'heure natif | Heure de rendez-vous |
| `url` | Valide le format d'URL | Sites web, liens |
| `search` | Champ avec bouton d'effacement natif | Barre de recherche |
| `range` | Curseur glissant entre min et max | Volume, niveau, budget |
| `color` | Sélecteur de couleur natif | Personnalisation |
| `file` | Explorateur de fichiers système | Upload d'image, document |
| `checkbox` | Case à cocher | Options multiples |
| `radio` | Bouton radio | Choix exclusif dans un groupe |
| `hidden` | Invisible à l'écran | Tokens, identifiants techniques |
| `submit` | Bouton de soumission | Valider le formulaire |

<br>

### Exemples des types courants

```html title="HTML - Types d'input HTML5 essentiels"
<!-- Mot de passe masqué -->
<input type="password" name="password" autocomplete="current-password">

<!-- Téléphone : déclenche le clavier numérique sur mobile -->
<input type="tel" name="telephone" placeholder="06 12 34 56 78">

<!-- Date avec limites min et max -->
<input type="date" name="naissance" min="1900-01-01" max="2009-12-31">

<!-- Nombre avec contraintes -->
<input type="number" name="quantite" min="1" max="99" step="1" value="1">

<!-- Curseur glissant -->
<input type="range" name="budget" min="0" max="10000" step="500" value="2500">

<!-- Sélecteur de couleur natif -->
<input type="color" name="couleur_theme" value="#3b82f6">

<!-- Upload de fichier avec filtre de type MIME -->
<input type="file" name="avatar" accept="image/png, image/jpeg, image/webp">

<!-- Upload multiple -->
<input type="file" name="documents[]" accept=".pdf,.docx" multiple>
```

*L'attribut `autocomplete="current-password"` sur un champ mot de passe est recommandé par l'OWASP[^2] : il permet aux gestionnaires de mots de passe de remplir correctement le champ, ce qui favorise l'utilisation de mots de passe forts et uniques.*

<br>

---

## La Validation Native HTML5

HTML5 offre un système de validation côté client intégré au navigateur, sans aucun JavaScript. Cette validation ne remplace pas la validation côté serveur — elle la complète.

```html title="HTML - Attributs de validation natifs"
<form action="/inscription" method="POST">

    <label for="pseudo">Pseudo (3 à 20 caractères) :</label>
    <!--
        required    : le champ ne peut pas être vide à la soumission.
        minlength   : longueur minimale autorisée.
        maxlength   : longueur maximale autorisée.
        pattern     : expression régulière que la valeur doit respecter.
        title       : message affiché dans la bulle d'aide native du navigateur.
    -->
    <input
        type="text"
        id="pseudo"
        name="pseudo"
        required
        minlength="3"
        maxlength="20"
        pattern="[a-zA-Z0-9_\-]+"
        title="Lettres, chiffres, tirets et underscores uniquement"
    >

    <label for="email">E-mail :</label>
    <!--
        autocomplete="email" : aide les gestionnaires de mots de passe
        et le navigateur à proposer la bonne valeur sauvegardée.
    -->
    <input
        type="email"
        id="email"
        name="email"
        required
        autocomplete="email"
    >

    <label for="password">Mot de passe (8 caractères minimum) :</label>
    <!--
        Le pattern impose : au moins une majuscule, une minuscule, un chiffre.
    -->
    <input
        type="password"
        id="password"
        name="password"
        required
        minlength="8"
        autocomplete="new-password"
    >

    <button type="submit">Créer mon compte</button>
</form>
```

!!! warning "La validation HTML5 ne remplace pas la validation serveur"
    La validation native peut être contournée en quelques secondes par n'importe quel utilisateur (suppression de l'attribut `required` via la console du navigateur, requête HTTP directe). Elle améliore l'expérience utilisateur mais **n'assure aucune sécurité**. Toute donnée reçue côté serveur doit être validée indépendamment — via PHP, Laravel Form Requests, ou tout autre mécanisme serveur.

**Tableau des attributs de validation :**

| Attribut | Champs concernés | Rôle |
| --- | --- | --- |
| `required` | Tous | Empêche la soumission si vide |
| `minlength` | `text`, `password`, `textarea` | Longueur minimale |
| `maxlength` | `text`, `password`, `textarea` | Longueur maximale |
| `min` | `number`, `date`, `range` | Valeur minimale |
| `max` | `number`, `date`, `range` | Valeur maximale |
| `pattern` | `text`, `email`, `tel`, `url` | Expression régulière à respecter |
| `step` | `number`, `range`, `date` | Incrément autorisé |
| `autocomplete` | La plupart | Contrôle le remplissage automatique |

<br>

---

## Grouper et structurer : `<fieldset>` et `<legend>`

La balise `<fieldset>` regroupe des champs liés sémantiquement et visuellement. La balise `<legend>` en est le titre officiel, lu en premier par les lecteurs d'écran.

```html title="HTML - Fieldset et legend pour structurer un formulaire complexe"
<form action="/inscription" method="POST">

    <!-- Groupe 1 : informations personnelles -->
    <fieldset>
        <legend>Informations personnelles</legend>

        <label for="prenom">Prénom :</label>
        <input type="text" id="prenom" name="prenom" required autocomplete="given-name">

        <label for="nom">Nom :</label>
        <input type="text" id="nom" name="nom" required autocomplete="family-name">

        <label for="naissance">Date de naissance :</label>
        <input type="date" id="naissance" name="naissance" required>
    </fieldset>

    <!-- Groupe 2 : informations de connexion -->
    <fieldset>
        <legend>Identifiants de connexion</legend>

        <label for="email_reg">E-mail :</label>
        <input type="email" id="email_reg" name="email" required autocomplete="email">

        <label for="password_reg">Mot de passe :</label>
        <input type="password" id="password_reg" name="password" required minlength="8" autocomplete="new-password">
    </fieldset>

    <!-- Groupe 3 : préférences (fieldset peut être désactivé globalement) -->
    <fieldset disabled>
        <legend>Options premium (abonnement requis)</legend>

        <label for="theme">Thème favori :</label>
        <input type="color" id="theme" name="theme" value="#3b82f6">
    </fieldset>

    <button type="submit">Créer mon compte</button>
</form>
```

*L'attribut `disabled` sur `<fieldset>` désactive **tous** les champs qu'il contient en une seule instruction. Le `<legend>` est annoncé par les lecteurs d'écran avant la lecture de chaque champ du groupe : "Identifiants de connexion — E-mail".*

<br>

---

## Autocomplétion avancée : `<datalist>`

La balise `<datalist>` propose des suggestions à l'utilisateur pendant sa saisie, tout en lui laissant la liberté de taper une valeur non listée. C'est un hybride entre `<input>` et `<select>`.

```html title="HTML - Datalist pour les suggestions de saisie"
<label for="technologie">Technologie principale :</label>

<!--
    L'attribut list sur l'input fait le lien avec l'id du datalist.
    L'utilisateur peut choisir une suggestion OU taper autre chose.
-->
<input
    type="text"
    id="technologie"
    name="technologie"
    list="suggestions-technos"
    placeholder="Commencez à taper..."
    autocomplete="off"
>

<!-- Les options sont les suggestions, pas des choix obligatoires -->
<datalist id="suggestions-technos">
    <option value="Laravel">
    <option value="Alpine.js">
    <option value="Livewire">
    <option value="Tailwind CSS">
    <option value="Go / Gin">
    <option value="Flutter / Dart">
    <option value="Python">
</datalist>
```

*Contrairement à `<select>`, `<datalist>` ne contraint pas l'utilisateur. Si la valeur saisie ne correspond à aucune suggestion, elle est envoyée telle quelle. La validation doit donc être gérée côté serveur.*

!!! note "Différence fondamentale entre datalist et select"
    `<select>` impose un choix parmi une liste fermée. `<datalist>` propose des suggestions mais accepte n'importe quelle valeur libre. Pour une liste de choix obligatoire, utilisez toujours `<select>`.

<br>

---

## Indicateurs d'état : `<meter>` et `<progress>`

Ces deux balises affichent des valeurs numériques sous forme visuelle native, sans CSS ni JavaScript.

<br>

### `<meter>` : une mesure dans une plage connue

`<meter>` représente une valeur scalaire dans une plage définie — un niveau de remplissage, un score, une jauge.

```html title="HTML - Meter pour les jauges et mesures"
<!--
    value  : valeur actuelle.
    min    : valeur minimale de la plage (défaut : 0).
    max    : valeur maximale de la plage (défaut : 1).
    low    : seuil en dessous duquel la valeur est considérée basse.
    high   : seuil au-dessus duquel la valeur est considérée haute.
    optimum : valeur idéale (influence la couleur affichée par le navigateur).
-->
<p>
    Espace disque utilisé :
    <meter
        value="75"
        min="0"
        max="100"
        low="50"
        high="80"
        optimum="20"
        title="75 Go utilisés sur 100 Go"
    >75 Go sur 100 Go</meter>
    <span>75 %</span>
</p>

<p>
    Score de sécurité du mot de passe :
    <meter value="3" min="0" max="5" low="2" high="4" optimum="5">3/5</meter>
</p>
```

*Le contenu entre les balises `<meter>` est le texte de repli pour les navigateurs ne supportant pas la balise. `optimum` et `high`/`low` influencent la couleur rendue par le navigateur : vert si la valeur est proche de `optimum`, orange ou rouge si elle dépasse `high` ou passe sous `low`.*

<br>

### `<progress>` : une tâche en cours

`<progress>` représente l'avancement d'une tâche en cours — un upload, une installation, une progression dans un formulaire multi-étapes.

```html title="HTML - Progress pour les barres de progression"
<!--
    Sans value : affiche une barre d'animation "indéterminée" (chargement infini).
    Avec value et max : affiche le pourcentage d'avancement.
-->

<!-- Progression déterminée : étape 2 sur 4 -->
<label for="etape">Progression :</label>
<progress id="etape" value="2" max="4">Étape 2 sur 4</progress>

<!-- Progression indéterminée : chargement en cours, durée inconnue -->
<progress>Chargement en cours...</progress>
```

!!! note "Différence entre `<meter>` et `<progress>`"
    `<meter>` représente une **mesure statique** dans une plage connue (un niveau, une jauge). `<progress>` représente **l'avancement d'une tâche** vers un objectif. Si la valeur peut baisser (comme un niveau de batterie), utilisez `<meter>`. Si elle ne peut qu'augmenter vers un objectif, utilisez `<progress>`.

<br>

---

## Les Choix : Cases à cocher et Boutons Radio

<br>

### Les Cases à cocher (`checkbox`) — Choix multiple

Utilisées quand l'utilisateur peut sélectionner plusieurs options simultanément ou n'en cocher aucune.

```html title="HTML - Cases à cocher avec fieldset et legend"
<fieldset>
    <legend>Centres d'intérêt</legend>

    <label>
        <input type="checkbox" name="interets[]" value="securite" checked>
        Cybersécurité
    </label>

    <label>
        <input type="checkbox" name="interets[]" value="dev_web">
        Développement Web
    </label>

    <label>
        <input type="checkbox" name="interets[]" value="devsecops">
        DevSecOps
    </label>
</fieldset>
```

*Notez `name="interets[]"` avec des crochets : cette convention indique au serveur PHP que plusieurs valeurs peuvent être envoyées sous le même nom, sous forme de tableau.*

<br>

### Les Boutons Radio — Choix exclusif

Utilisés quand une seule option est possible parmi plusieurs. Le même `name` sur tous les radio du groupe garantit l'exclusivité.

```html title="HTML - Boutons radio groupés avec fieldset"
<fieldset>
    <legend>Niveau d'expérience</legend>

    <label>
        <input type="radio" name="niveau" value="debutant">
        Débutant
    </label>

    <label>
        <input type="radio" name="niveau" value="intermediaire" checked>
        Intermédiaire
    </label>

    <label>
        <input type="radio" name="niveau" value="avance">
        Avancé
    </label>
</fieldset>
```

<br>

---

## Les Zones de Texte et Listes Déroulantes

<br>

### Le `<textarea>` — Zone de texte multiligne

Contrairement à `<input>`, `<textarea>` est une balise avec fermeture. Son contenu initial est le texte entre les balises d'ouverture et de fermeture.

```html title="HTML - Textarea multiligne avec dimensions et contraintes"
<label for="message">Décrivez votre problème :</label>

<!--
    rows    : nombre de lignes visibles (hauteur initiale).
    cols    : nombre de colonnes visibles (largeur initiale).
    minlength / maxlength : validation native du nombre de caractères.
    placeholder : texte indicatif affiché quand le champ est vide.
-->
<textarea
    id="message"
    name="message"
    rows="6"
    cols="60"
    minlength="20"
    maxlength="2000"
    placeholder="Décrivez votre situation en quelques lignes..."
    required
></textarea>
```

*La balise de fermeture `</textarea>` doit être immédiatement après l'ouverture si vous ne voulez pas de texte pré-rempli. Tout espace ou retour à la ligne entre les balises apparaît dans le champ.*

<br>

### Le `<select>` — Liste déroulante

Idéal pour les listes fermées de nombreux choix.

```html title="HTML - Select avec optgroup et option sélectionnée par défaut"
<label for="pays">Votre pays :</label>

<select id="pays" name="pays" required>
    <!-- Option vide initiale pour forcer un choix conscient -->
    <option value="" disabled selected>-- Choisissez votre pays --</option>

    <optgroup label="Europe">
        <option value="fr">France</option>
        <option value="be">Belgique</option>
        <option value="ch">Suisse</option>
        <option value="lu">Luxembourg</option>
    </optgroup>

    <optgroup label="Amériques">
        <option value="ca">Canada</option>
        <option value="us">États-Unis</option>
    </optgroup>
</select>
```

*L'option `disabled selected` en tête de liste avec une valeur vide est une bonne pratique pour forcer l'utilisateur à faire un choix explicite. Sans elle, le premier pays serait sélectionné par défaut.*

**`<select>` avec sélection multiple :**

```html title="HTML - Select multiple avec taille visible"
<!--
    multiple : permet de sélectionner plusieurs options (Ctrl+clic ou Cmd+clic).
    size     : nombre d'options visibles simultanément sans scroll.
    name[]   : notation tableau pour recevoir plusieurs valeurs côté serveur.
-->
<label for="competences">Compétences (plusieurs choix possibles) :</label>
<select id="competences" name="competences[]" multiple size="5">
    <option value="html">HTML</option>
    <option value="css">CSS</option>
    <option value="js">JavaScript</option>
    <option value="php">PHP</option>
    <option value="go">Go</option>
</select>
```

<br>

---

## Les boutons (`<button>`)

La balise `<button>` a trois comportements distincts selon son attribut `type`.

```html title="HTML - Les trois types de boutons"
<!--
    type="submit"  : (défaut) soumet le formulaire.
    type="reset"   : réinitialise tous les champs à leur valeur initiale.
    type="button"  : ne fait rien nativement — utilisé pour les actions JavaScript.
-->

<!-- Soumet le formulaire vers action/method de la balise form parente -->
<button type="submit">Envoyer le formulaire</button>

<!-- Remet tous les champs à leur valeur initiale -->
<button type="reset">Effacer tout</button>

<!-- Déclenche une action JavaScript sans soumettre le formulaire -->
<button type="button" onclick="verifierDisponibilite()">
    Vérifier la disponibilité
</button>
```

!!! warning "Le piège du `type` par défaut"
    Un `<button>` sans attribut `type` a le comportement `type="submit"` par défaut. Tout bouton placé à l'intérieur d'un `<form>`, même pour une action secondaire (afficher un aperçu, valider un champ), **soumettra le formulaire** si vous oubliez `type="button"`. C'est une source d'erreurs fréquente dans les formulaires Laravel avec des actions multiples.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Un formulaire professionnel repose sur plusieurs couches complémentaires. La balise `<form>` définit la destination et la méthode d'envoi — `enctype="multipart/form-data"` est obligatoire dès qu'un fichier est attendu. Chaque champ doit avoir un `<label>` lié et un `name` explicite. `<fieldset>` + `<legend>` structurent les groupes de champs et améliorent l'accessibilité. La validation native HTML5 (`required`, `pattern`, `minlength`, `autocomplete`) améliore l'expérience utilisateur mais ne remplace jamais la validation côté serveur. `<datalist>` propose des suggestions non contraignantes. `<meter>` et `<progress>` affichent des données scalaires et d'avancement nativement.

> Dans le module suivant, nous donnerons enfin un sens sémantique profond à l'architecture complète de la page avec **HTML5 Sémantique** — les balises `<header>`, `<main>`, `<nav>`, `<article>`, `<section>` et `<footer>`.

<br>

[^1]: **CSRF (Cross-Site Request Forgery)** : attaque par laquelle un site malveillant trompe le navigateur d'un utilisateur authentifié pour lui faire envoyer une requête non souhaitée vers un autre site. Les tokens CSRF, régénérés à chaque formulaire, permettent au serveur de vérifier que la requête provient bien d'un formulaire qu'il a lui-même généré.

[^2]: **OWASP (Open Web Application Security Project)** : organisation internationale à but non lucratif qui publie des référentiels, outils et bonnes pratiques pour la sécurité des applications web. L'OWASP Top 10 liste les dix risques de sécurité les plus critiques des applications web.