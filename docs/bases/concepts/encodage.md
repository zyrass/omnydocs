---
description: "Comprendre comment les ordinateurs représentent le texte : ASCII, Unicode, UTF-8 et autres formats (Base64)."
icon: lucide/book-open-check
tags: ["ENCODAGE", "UTF-8", "ASCII", "UNICODE", "BASE64"]
---

# Encodage de Caractères : ASCII & UTF-8

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>


!!! quote "Analogie pédagogique"
    _L'encodage est comme un dictionnaire de traduction entre l'humain et la machine. L'humain lit un 'A', l'ordinateur ne comprend que des '0' et des '1'. L'encodage (comme UTF-8) est la règle stricte qui dit 'cette série de chiffres signifie un A'._

!!! quote "Le langage des machines"
    _Au niveau matériel, un ordinateur ne comprend ni le français, ni le japonais, ni même la lettre "A". Il ne comprend que des variations de tension électrique, représentées logiquement par des **0 et des 1** (Bits). L'encodage est simplement le dictionnaire de traduction qui permet à l'ordinateur de convertir ces suites de zéros et de uns en caractères lisibles par un humain, et vice-versa._

## La genèse : ASCII (American Standard Code for Information Interchange)

Créé dans les années 1960, **l'ASCII** est le grand-père de l'encodage informatique.

À cette époque, la mémoire coûtait extrêmement cher. Il a donc été décidé que chaque caractère tiendrait sur seulement **7 bits** (soit un demi-octet, étendu à 8 bits plus tard).
Avec 7 bits, on peut représenter $2^7$ caractères, soit **128 caractères possibles**.

**Que contient la table ASCII ?**
- L'alphabet latin non accentué (A-Z, a-z).
- Les chiffres (0-9).
- La ponctuation basique (?, !, $, @).
- Des caractères de contrôle invisibles (Retour à la ligne, Fin de fichier).

!!! warning "La limite de l'ASCII"
    Puisque la table ASCII ne contient que 128 "places", elle n'a pas la place pour le "é", le "ç", l'alphabet cyrillique, ou le japonais. Ce format était suffisant pour les pays anglophones, mais totalement inutilisable pour le reste du monde.

## Le chaos de la régionalisation (ISO-8859-x)

Pour contourner la limite de l'ASCII, l'industrie est passée sur 8 bits (256 caractères). Les 128 premiers restaient identiques à l'ASCII, et les 128 restants dépendaient **de votre région**.
- En Europe de l'Ouest, on utilisait la table `ISO-8859-1` (Latin-1) qui ajoutait le "é", "è", "ç".
- En Russie, on utilisait la table `Windows-1251`.

**Le problème :** Si un Français envoyait un fichier texte (encodé en Latin-1) à un Russe, l'ordinateur russe lisait le fichier avec sa propre table. Le "é" français se transformait en un symbole cyrillique incompréhensible (le fameux phénomène du *Mojibake*).

## L'unification : Unicode

Face à ce chaos, le consortium **Unicode** est né dans les années 90 avec une mission titanesque : créer un dictionnaire universel contenant **absolument tous les symboles de l'humanité** (langues mortes, idéogrammes, et même les émojis 🚀).

Unicode n'est pas un encodage, c'est un **Standard**. Il assigne simplement un numéro unique à chaque symbole.
Exemple : Le symbole de l'Euro (€) est le caractère numéro `U+20AC`.

## La révolution : UTF-8

Avoir une grande table Unicode c'est bien, mais comment la stocker en bits ? 
Si on décide que chaque caractère prend 4 octets (32 bits) pour être sûr d'avoir de la place pour tout, un simple texte anglais prendrait 4 fois plus de mémoire que nécessaire !

C'est là qu'intervient **l'UTF-8** (Unicode Transformation Format - 8 bit). C'est un encodage **à taille variable**.

<div class="grid cards" markdown>

-   :lucide-type:{ .lg .middle } **Caractères standards (A-Z)**

    ---
    Ils ne prennent **1 seul octet**. Cerise sur le gâteau, leur code binaire est exactement le même qu'en ASCII. Un fichier purement ASCII est donc un fichier UTF-8 valide. (Rétrocompatibilité totale).

-   :lucide-languages:{ .lg .middle } **Caractères accentués (é, ç)**

    ---
    L'UTF-8 comprend qu'il a besoin de plus de place et utilise **2 octets**.

-   :lucide-smile:{ .lg .middle } **Idéogrammes et Émojis (漢字, 🚀)**

    ---
    L'UTF-8 s'étend automatiquement pour utiliser **3 ou 4 octets**.

</div>

!!! success "La norme du Web"
    Aujourd'hui, **UTF-8 est utilisé sur plus de 98% du Web**. Dans tous vos projets HTML, vous devez toujours avoir la balise `<meta charset="UTF-8">` pour éviter les erreurs d'affichage.

## Les formats annexes (Transport de données)

En développement, vous croiserez le mot "encodage" dans deux autres contextes spécifiques au transport de données.

### L'encodage Base64

Certains protocoles (comme les vieux serveurs d'emails) n'acceptent QUE du texte basique (ASCII) et paniquent s'ils reçoivent un fichier binaire (une image, un PDF).
Le **Base64** résout ce problème. Il prend votre fichier binaire, et le convertit en une longue chaîne de caractères alphanumériques simples (`A-Z`, `a-z`, `0-9`, `+`, `/`).

*Exemple pratique : Envoyer une image en JSON via une API REST (l'image devient une immense chaîne `data:image/png;base64,iVBORw0KGgo...`).*

### L'URL Encoding (Pourcent-encodage)

Dans une URL, certains caractères ont une signification spéciale : `?` sépare l'URL des paramètres, `&` sépare les paramètres, l'espace n'est pas autorisé.
Si vous passez une donnée contenant ces caractères dans une URL, il faut l'encoder.

L'espace devient `%20`. 
Le "é" devient `%C3%A9`.

*C'est pourquoi une URL contenant des espaces ressemble souvent à : `https://site.com/mon%20super%20fichier.pdf`.*

## Différence entre Encodage, Hachage et Chiffrement

Ces trois termes sont souvent confondus par les développeurs juniors :

1. **L'Encodage (UTF-8, Base64)** : Change le format des données pour la machine. **Aucune sécurité**. N'importe qui peut le décoder (car l'algorithme est public et ne nécessite pas de clé).
2. **Le Hachage (SHA-256, Bcrypt)** : Fonction à sens unique. On l'utilise pour les **Mots de passe**. Impossible à décoder (on vérifie juste si les hachages correspondent).
3. **Le Chiffrement / Cryptage (AES, RSA)** : Sécurise les données. Réversible **uniquement** si on possède la clé secrète.

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La maîtrise du concept de encodage est un pilier de l'informatique fondamentale. Au-delà de la syntaxe technique, c'est cette compréhension théorique qui différencie un simple technicien d'un véritable ingénieur capable de concevoir des systèmes robustes et maintenables.

