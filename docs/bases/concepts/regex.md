---
description: "Maîtriser les Expressions Régulières (RegEx) pour rechercher, valider et extraire des motifs textuels complexes."
icon: lucide/book-open-check
tags: ["REGEX", "VALIDATION", "CHAÎNES", "PATTERN", "PARSING"]
---

# Les Expressions Régulières (RegEx)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>

!!! quote "Un langage dans le langage"
    _Les **Expressions Régulières** (souvent abrégées RegEx ou RegExp) sont une séquence de caractères formant un motif de recherche. Initialement perçues comme une suite incompréhensible de symboles cryptiques, elles constituent en réalité l'un des outils les plus puissants d'un développeur pour analyser, valider ou extraire de la donnée textuelle complexe en une seule ligne de code._

## À quoi ça sert concrètement ?

Imaginons que vous demandiez à un utilisateur de saisir son numéro de téléphone. Il pourrait l'écrire de dizaines de façons : `0612345678`, `06 12 34 56 78`, `+33 6 12 34 56 78`, `06.12.34.56.78`.

Comment vérifier en PHP ou JavaScript que la chaîne est bien un numéro valide ?
- **Méthode classique (Procédurale)** : Vous feriez des dizaines de `if`, vous retireriez les espaces, vérifieriez la longueur, vérifieriez que chaque caractère est bien un chiffre... C'est lourd et source de bugs.
- **Méthode RegEx** : Vous définissez un "Motif" (Pattern) et vous demandez au moteur : *"Est-ce que cette chaîne correspond à mon motif ?"*

## La Syntaxe Fondamentale

Une expression régulière est généralement encadrée par des délimiteurs, le plus souvent des slashes `/`.

Exemple : `/^[0-9]{10}$/` (Vérifie qu'il y a exactement 10 chiffres).

Voici les blocs de construction pour lire cette "magie noire".

### 1. Les Caractères Littéraux et les Méta-caractères
Si vous cherchez le mot "chat", la regex est simplement `/chat/`. 
Mais certains caractères ont un pouvoir spécial (Méta-caractères) : `. ^ $ * + ? ( ) [ ] { } \ |`

Si vous voulez chercher un vrai point `.`, vous devez "l'échapper" avec un antislash : `\.`.

### 2. Les Classes de Caractères (Les Ensembles)
Les crochets `[]` permettent de définir un ensemble de caractères autorisés à une position donnée.

- `/[aeiouy]/` : Trouve **UNE** voyelle (a, e, i, o, u, ou y).
- `/[a-z]/` : Trouve n'importe quelle lettre minuscule de a à z.
- `/[0-9]/` : Trouve n'importe quel chiffre.
- `/[^0-9]/` : Le `^` à l'intérieur de crochets signifie la **négation**. Trouve tout ce qui n'est PAS un chiffre.

### 3. Les Raccourcis
Parce qu'écrire `[0-9]` ou `[a-zA-Z0-9_]` est long, des raccourcis (classes prédéfinies) existent :

- `\d` : Un chiffre (équivalent à `[0-9]`). (*d pour digit*)
- `\D` : Tout sauf un chiffre.
- `\w` : Un caractère alphanumérique ou un underscore (`[a-zA-Z0-9_]`). (*w pour word character*)
- `\s` : Un espace (espace, tabulation, saut de ligne). (*s pour space*)
- `.` (le point) : N'importe quel caractère (sauf les sauts de ligne).

### 4. Les Quantificateurs (Combien de fois ?)
Ils s'appliquent au caractère (ou au groupe) qui les précède immédiatement.

- `*` : 0 fois ou plus (Optionnel ou infini).
- `+` : 1 fois ou plus (Obligatoire au moins une fois).
- `?` : 0 ou 1 fois (Optionnel).
- `{n}` : Exactement `n` fois. (Ex: `\d{4}` = exactement 4 chiffres).
- `{min,max}` : Entre `min` et `max` fois. (Ex: `\w{3,10}` = un mot de 3 à 10 lettres).

### 5. Les Ancres (Positionnement)
Elles ne matchent pas un caractère, mais une **position** dans la chaîne.

- `^` : Début de la chaîne.
- `$` : Fin de la chaîne.

!!! danger "L'importance des ancres pour la validation"
    Si vous vérifiez un code postal avec `/ \d{5} /`, la chaîne `Mon code est 75000 et bla bla` sera validée car le moteur trouve "75000" à l'intérieur.
    Si vous utilisez `/^\d{5}$/`, la chaîne devra **commencer et se terminer** par 5 chiffres. La chaîne précédente sera donc rejetée. C'est capital pour la sécurité.

---

## Cas Pratiques Fréquents

### L'Adresse Email Simple
`/^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$/`

**Traduction :**
1. `^` : Depuis le début.
2. `[\w\.-]+` : Un ou plusieurs caractères alphanumériques, points ou tirets.
3. `@` : Un "@" littéral.
4. `[\w\.-]+` : Un ou plusieurs caractères alphanumériques, points ou tirets (le nom de domaine).
5. `\.` : Un vrai point (échappé).
6. `[a-zA-Z]{2,}` : Une extension (com, fr, org) composée de lettres uniquement, d'une longueur de 2 minimum.
7. `$` : Jusqu'à la fin.

### Le Numéro de Téléphone Français
`/^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/`

**Traduction :** Accepte `+33 6 12 34 56 78`, `0033612345678`, ou `06.12.34.56.78`. (Il utilise des groupes non-capturants `(?:)` pour gérer les différentes syntaxes du préfixe international).

## Les Groupes de Capture `()`

Les parenthèses ont un double rôle :
1. Elles appliquent un quantificateur à un ensemble entier. Ex: `/(bla)+/` matche "blablabla".
2. Elles **capturent** la valeur trouvée pour pouvoir l'extraire et l'utiliser dans votre code.

**Exemple d'extraction (JavaScript) :**
Imaginons une date formatée en `AAAA-MM-JJ`.
```javascript
const regex = /^(\d{4})-(\d{2})-(\d{2})$/;
const match = "2026-12-25".match(regex);

console.log(match[1]); // "2026" (Groupe 1)
console.log(match[2]); // "12"   (Groupe 2)
console.log(match[3]); // "25"   (Groupe 3)
```

## Les Flags (Drapeaux)

Les flags modifient le comportement global du moteur RegEx. Ils se placent après le slash final : `/pattern/flags`.

- `i` (Insensitive) : Ignore la casse (A = a).
- `g` (Global) : Ne s'arrête pas après la première occurrence trouvée, mais cherche dans tout le texte.
- `m` (Multiline) : Les ancres `^` et `$` correspondent au début et à la fin de chaque *ligne*, plutôt que de la chaîne globale.

## Conclusion

Les Expressions Régulières sont universelles : la même RegEx de validation d'email fonctionnera en PHP, en JavaScript, en Python, et même dans l'outil de recherche de votre IDE. C'est une compétence transversale qui a une durée de vie infinie dans votre carrière de développeur.