---
description: "Types et variables en Swift : let, var, inférence de types, types fondamentaux et conversion explicite."
icon: lucide/book-open-check
tags: ["SWIFT", "TYPES", "VARIABLES", "CONSTANTES", "INFÉRENCE"]
---

# Types et Variables

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Contrat de Location"
    En Swift, déclarer une variable, c'est signer un contrat avec le compilateur. Quand vous écrivez `let age = 28`, vous dites : *"Je crée un emplacement mémoire nommé `age`, de type `Int`, dont la valeur ne changera jamais."* Si plus tard vous essayez de modifier `age`, le compilateur rompra le contrat immédiatement — à la compilation, pas à l'exécution.

    Ce système peut sembler contraignant venant de PHP ou JavaScript où tout est flexible et mutable par défaut. En réalité, c'est l'inverse : cette rigueur vous protège d'une classe entière de bugs que vous ne découvrirez jamais, parce qu'ils ne pourront jamais exister.

Ce module couvre le système de types de Swift — l'une des fonctionnalités qui le distinguent le plus des langages dynamiques.

<br>

---

## `let` et `var` : Constantes et Variables

Swift distingue fondamentalement deux types de liaisons :

- `let` — déclare une **constante** : la valeur ne peut plus être modifiée après initialisation.
- `var` — déclare une **variable** : la valeur peut être réassignée.

=== ":simple-swift: Swift"

    ```swift title="Swift - let et var"
    // CONSTANTE : la valeur est fixée à la déclaration
    // Toute tentative de modification produit une erreur de compilation
    let nomUtilisateur = "alice_dev"
    let dateNaissance = 1995

    // VARIABLE : la valeur peut être modifiée
    var score = 0
    var estConnecte = false

    // Modification d'une variable : valide
    score = 100
    estConnecte = true

    // Modification d'une constante : ERREUR DE COMPILATION
    // nomUtilisateur = "bob"
    // error: cannot assign to value: 'nomUtilisateur' is a 'let' constant
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - const et let (analogie)"
    // JavaScript a un système similaire depuis ES6
    // const ≈ let Swift (mais attention : const en JS n'est pas aussi strict)
    const nomUtilisateur = "alice_dev";
    const dateNaissance = 1995;

    // let en JS ≈ var en Swift
    let score = 0;
    let estConnecte = false;

    score = 100;        // Valide
    estConnecte = true; // Valide

    // DIFFÉRENCE IMPORTANTE : const en JS ne protège pas les contenus d'objets/tableaux
    const tableau = [1, 2, 3];
    tableau.push(4); // Valide en JS — pas en Swift pour les collections de type let
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Variables et constantes"
    <?php
    // PHP n'a pas de const pour les variables locales
    // define() et const créent des constantes globales
    define('NOM_UTILISATEUR', 'alice_dev');
    const DATE_NAISSANCE = 1995;

    // Les variables PHP sont toutes mutables par défaut
    $score = 0;
    $estConnecte = false;

    $score = 100;
    $estConnecte = true;

    // PHP 8.1+ introduit les propriétés readonly (pour les classes uniquement)
    // Il n'y a pas d'équivalent direct à let pour les variables locales
    ```

=== ":simple-python: Python"

    ```python title="Python - Variables (pas de constantes natives)"
    # Python n'a pas de mécanisme natif de constantes
    # La convention est d'utiliser MAJUSCULES pour signaler "ne pas modifier"
    NOM_UTILISATEUR = "alice_dev"  # Convention, pas une restriction
    DATE_NAISSANCE = 1995

    # Toutes les variables Python sont mutables
    score = 0
    est_connecte = False

    score = 100
    est_connecte = True

    # Python 3.8+ : TypedDict avec Final pour signaler l'immutabilité (typing)
    from typing import Final
    MAX_TENTATIVES: Final = 3
    ```

!!! tip "La règle d'or Swift : `let` par défaut"
    En Swift, la convention universelle est d'utiliser `let` partout et de ne passer à `var` que quand la valeur doit effectivement changer. Xcode vous avertit si vous déclarez une variable avec `var` dont la valeur ne change jamais — il suggère de la convertir en `let`. Cette discipline rend le code plus prévisible et les intentions plus claires.

<br>

---

## L'Inférence de Types

Swift est statiquement typé : chaque valeur a un type précis connu à la compilation. Mais contrairement à d'autres langages statiquement typés (Java, C#), vous n'avez **presque jamais besoin d'écrire le type explicitement** — le compilateur l'infère depuis la valeur initiale.

=== ":simple-swift: Swift"

    ```swift title="Swift - Inférence de types"
    // Avec inférence (style recommandé)
    let age = 28              // Inféré : Int
    let taille = 1.82         // Inféré : Double
    let prenom = "Alice"      // Inféré : String
    let estActif = true       // Inféré : Bool

    // Avec annotation de type explicite (quand nécessaire)
    let temperature: Double = 36    // Sans annotation : serait inféré comme Int
    let compteur: Int = 0
    let message: String = "Bonjour"

    // Vérifier le type inféré dans Xcode : Option + clic sur le nom de la variable
    // Xcode affiche : "let age: Int"

    // ERREUR : réassigner un type différent — impossible en Swift
    var nombre = 42           // Inféré : Int
    // nombre = "quarante-deux"
    // error: cannot assign value of type 'String' to type 'Int'
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Typage dynamique (pas d'inférence statique)"
    // JavaScript est dynamiquement typé : le type peut changer à l'exécution
    let age = 28;               // number (implicite)
    let taille = 1.82;          // number
    let prenom = "Alice";       // string
    let estActif = true;        // boolean

    // En JS, on peut changer le type d'une variable — ce que Swift refuse
    let nombre = 42;            // number
    nombre = "quarante-deux";   // string — valide en JS, erreur en Swift

    // TypeScript apporte l'inférence statique similaire à Swift
    // let nombre: number = 42;
    // nombre = "quarante-deux"; // Erreur TypeScript
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Typage dynamique avec types optionnels (PHP 8)"
    <?php
    // PHP est dynamiquement typé par défaut
    $age = 28;          // int (implicite)
    $taille = 1.82;     // float
    $prenom = "Alice";  // string
    $estActif = true;   // bool

    // PHP 8 : déclarations de types dans les fonctions et propriétés
    // Mais pas pour les variables locales
    function afficherAge(int $age): string {
        return "Age : $age ans";
    }

    // strict_types=1 force le respect des types dans les appels de fonctions
    declare(strict_types=1);
    ```

=== ":simple-python: Python"

    ```python title="Python - Typage dynamique avec annotations (Python 3.5+)"
    # Python est dynamiquement typé
    age = 28          # int (implicite)
    taille = 1.82     # float
    prenom = "Alice"  # str
    est_actif = True  # bool

    # Les annotations de type (PEP 484) sont optionnelles et non forcées
    age: int = 28
    taille: float = 1.82

    # mypy ou pyright peuvent vérifier les types à l'analyse statique
    # mais Python lui-même ne les fait pas respecter à l'exécution
    age = "vingt-huit"  # Valide en Python, violerait une annotation int
    ```

<br>

---

## Les Types Fondamentaux

Swift dispose de types primitifs qui correspondent à des types bien connus, avec quelques subtilités importantes.

<br>

### Entiers : `Int`

```swift title="Swift - Le type Int et ses variantes"
// Int : entier signé, taille adaptée à la plateforme (64 bits sur iOS/macOS modernes)
let population: Int = 8_000_000_000  // Les underscores améliorent la lisibilité

// Variantes de taille fixe (rarement nécessaires)
let valeur8:  Int8  = 127       // -128 à 127
let valeur16: Int16 = 32_767    // -32 768 à 32 767
let valeur32: Int32 = 2_147_483_647
let valeur64: Int64 = 9_223_372_036_854_775_807

// UInt pour les entiers non signés (uniquement positifs)
let index: UInt = 0

// Limites
print(Int.max)   // 9 223 372 036 854 775 807 sur 64 bits
print(Int.min)   // -9 223 372 036 854 775 808

// Opérations arithmétiques standard
let a = 10
let b = 3
print(a + b)   // 13
print(a - b)   // 7
print(a * b)   // 30
print(a / b)   // 3  — division entière : la partie décimale est tronquée
print(a % b)   // 1  — modulo (reste de la division)
```

*La lisibilité des grands nombres avec des underscores (`8_000_000_000`) est une fonctionnalité syntaxique de Swift ignorée par le compilateur — le nombre vaut exactement 8000000000.*

<br>

### Nombres décimaux : `Double` et `Float`

=== ":simple-swift: Swift"

    ```swift title="Swift - Double et Float"
    // Double : virgule flottante 64 bits — RECOMMANDÉ
    let pi: Double = 3.14159265358979
    let taux: Double = 0.20

    // Float : virgule flottante 32 bits — moins précis, rarement utilisé
    let coordonnee: Float = 48.8566

    // Quand on écrit un nombre décimal, Swift infère Double par défaut
    let temperature = 37.5   // Inféré : Double

    // Opérations
    let prixHT = 100.0
    let tva = 0.20
    let prixTTC = prixHT * (1 + tva)  // 120.0

    // Formatage pour l'affichage
    print(String(format: "Prix TTC : %.2f €", prixTTC))
    // Affiche : Prix TTC : 120.00 €
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - number (pas de distinction Double/Float)"
    // JavaScript n'a qu'un seul type numérique : number (IEEE 754 double precision)
    const pi = 3.14159265358979;
    const taux = 0.20;

    const prixHT = 100.0;
    const prixTTC = prixHT * (1 + taux);  // 120.00000000000001 (précision flottante)

    // Formatage
    console.log(`Prix TTC : ${prixTTC.toFixed(2)} €`);
    ```

=== ":simple-php: PHP"

    ```php title="PHP - float (équivalent de Double)"
    <?php
    $pi = 3.14159265358979;  // float
    $taux = 0.20;

    $prixHT = 100.0;
    $prixTTC = $prixHT * (1 + $taux);

    // Formatage
    echo sprintf("Prix TTC : %.2f €", $prixTTC) . PHP_EOL;
    echo number_format($prixTTC, 2, ',', ' ') . ' €' . PHP_EOL;
    ```

=== ":simple-python: Python"

    ```python title="Python - float (équivalent de Double)"
    pi = 3.14159265358979  # float (toujours double precision en Python)
    taux = 0.20

    prix_ht = 100.0
    prix_ttc = prix_ht * (1 + taux)

    # Formatage
    print(f"Prix TTC : {prix_ttc:.2f} €")
    ```

<br>

### Chaînes de caractères : `String`

=== ":simple-swift: Swift"

    ```swift title="Swift - String et ses spécificités"
    // String : type valeur en Swift (copié lors de l'assignation)
    let prenom = "Alice"
    let nom = "Martin"

    // Concaténation avec +
    let nomComplet = prenom + " " + nom

    // Interpolation (méthode recommandée)
    let message = "Bonjour \(prenom) \(nom) !"

    // String multilignes (trois guillemets)
    let bio = """
    Développeuse iOS
    Passionnée de Swift
    Basée à Lyon
    """

    // Propriétés et méthodes utiles
    print(prenom.count)                  // 5 (nombre de caractères)
    print(prenom.isEmpty)                // false
    print(prenom.uppercased())           // "ALICE"
    print(prenom.lowercased())           // "alice"
    print(prenom.hasPrefix("Al"))        // true
    print(prenom.hasSuffix("ce"))        // true
    print(prenom.contains("lic"))        // true

    // Caractère unique : type Character
    let initiale: Character = "A"
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - string"
    const prenom = "Alice";
    const nom = "Martin";

    // Concaténation
    const nomComplet = prenom + " " + nom;

    // Template literals
    const message = `Bonjour ${prenom} ${nom} !`;

    // Multilignes
    const bio = `Développeuse iOS
Passionnée de JavaScript
Basée à Lyon`;

    // Méthodes
    console.log(prenom.length);             // 5
    console.log(prenom.toUpperCase());      // "ALICE"
    console.log(prenom.startsWith("Al"));   // true
    console.log(prenom.includes("lic"));    // true
    ```

=== ":simple-php: PHP"

    ```php title="PHP - string"
    <?php
    $prenom = "Alice";
    $nom = "Martin";

    // Concaténation avec .
    $nomComplet = $prenom . " " . $nom;

    // Interpolation dans guillemets doubles
    $message = "Bonjour $prenom $nom !";

    // Multilignes : heredoc
    $bio = <<<EOT
    Développeuse iOS
    Passionnée de PHP
    Basée à Lyon
    EOT;

    // Fonctions
    echo strlen($prenom);               // 5
    echo strtoupper($prenom);           // "ALICE"
    echo str_starts_with($prenom, "Al"); // true (PHP 8+)
    echo str_contains($prenom, "lic");   // true (PHP 8+)
    ```

=== ":simple-python: Python"

    ```python title="Python - str"
    prenom = "Alice"
    nom = "Martin"

    # Concaténation
    nom_complet = prenom + " " + nom

    # f-string
    message = f"Bonjour {prenom} {nom} !"

    # Multilignes
    bio = """Développeuse iOS
Passionnée de Python
Basée à Lyon"""

    # Méthodes
    print(len(prenom))              # 5
    print(prenom.upper())           # "ALICE"
    print(prenom.startswith("Al"))  # True
    print("lic" in prenom)          # True
    ```

<br>

### Booléens : `Bool`

```swift title="Swift - Bool et ses opérateurs"
// Bool ne peut valoir que true ou false — pas de valeur "truthy" implicite
let estConnecte: Bool = true
let aDesPermissions = false

// Opérateurs logiques
let peutAcceder = estConnecte && aDesPermissions  // ET logique
let estVisible = estConnecte || aDesPermissions   // OU logique
let estBloque = !estConnecte                       // NON logique

// DIFFÉRENCE IMPORTANTE avec PHP et JavaScript :
// En Swift, on ne peut pas utiliser un Int ou un String comme booléen
let nombre = 1
// if nombre { }  // ERREUR : 'Int' is not convertible to 'Bool'
// En JS : if (1) { } fonctionne (truthy)
// En PHP : if ($nombre) { } fonctionne aussi

// En Swift, il faut être explicite :
if nombre != 0 { print("Nombre non nul") }
```

*L'absence de valeurs "truthy/falsy" en Swift est intentionnelle. Elle évite les bugs subtils comme `if (array)` en PHP qui est vrai même pour un tableau vide en JavaScript.*

<br>

---

## La Conversion de Types

En Swift, les conversions entre types numériques sont toujours **explicites**. Le compilateur refuse les conversions implicites qui pourraient entraîner une perte de données.

=== ":simple-swift: Swift"

    ```swift title="Swift - Conversion de types explicite"
    let entier: Int = 42
    let decimal: Double = 3.14

    // ERREUR : Swift refuse la conversion implicite
    // let resultat = entier + decimal
    // error: binary operator '+' cannot be applied to 'Int' and 'Double'

    // CORRECT : conversion explicite via les initialiseurs de type
    let entierVersDouble = Double(entier)        // 42.0
    let decimalVersEntier = Int(decimal)         // 3  (troncature, pas arrondi)
    let resultat = Double(entier) + decimal      // 45.14

    // Conversion String ↔ Int
    let texte = "42"
    let nombreDepuisTexte = Int(texte)          // Optional<Int> : peut échouer (module 06)
    let texteDepuisNombre = String(entier)      // "42" : toujours valide

    // Conversion String ↔ Double
    let texteDecimal = "3.14"
    let nombreDecimal = Double(texteDecimal)    // Optional<Double>

    print(Int("abc"))     // nil — la conversion a échoué (pas de crash)
    print(Int("42"))      // Optional(42)
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Conversion implicite et explicite"
    // JavaScript effectue des conversions implicites (type coercion)
    const entier = 42;
    const decimal = 3.14;

    // Conversion implicite : JavaScript la fait automatiquement
    const resultat = entier + decimal;  // 45.14 — fonctionne sans conversion

    // Problème de la coercion implicite en JS
    console.log("5" + 3);    // "53" (concaténation, pas addition !)
    console.log("5" - 3);    // 2   (conversion implicite vers number)

    // Conversions explicites
    const texteVersNombre = Number("42");     // 42
    const nombreVersTexte = String(42);       // "42"
    const parseInt_ = parseInt("42px");       // 42 (ignore le "px")
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Casting explicite et implicite"
    <?php
    $entier = 42;
    $decimal = 3.14;

    // PHP fait des conversions implicites dans la plupart des contextes
    $resultat = $entier + $decimal;  // 45.14 — float automatiquement

    // Casting explicite
    $entierVersFloat = (float) $entier;    // 42.0
    $floatVersEntier = (int) $decimal;     // 3 (troncature)
    $texteVersEntier = (int) "42abc";      // 42

    // intval(), floatval(), strval()
    $depuis_texte = intval("42");          // 42
    $vers_texte = strval(42);              // "42"
    ```

=== ":simple-python: Python"

    ```python title="Python - Conversion explicite"
    entier = 42
    decimal = 3.14

    # Python refuse aussi les conversions implicites entre types incompatibles
    # resultat = entier + "texte"  # TypeError: unsupported operand type(s) for +: 'int' and 'str'

    # Mais autorise int + float implicitement
    resultat = entier + decimal  # 45.14

    # Conversions explicites
    entier_vers_float = float(entier)    # 42.0
    float_vers_entier = int(decimal)     # 3 (troncature)
    texte_vers_entier = int("42")        # 42
    entier_vers_texte = str(entier)      # "42"

    # Conversion qui peut échouer
    try:
        nombre = int("abc")
    except ValueError:
        print("Conversion impossible")
    ```

<br>

---

## Les Alias de Types

Swift permet de créer des noms alternatifs pour des types existants, ce qui améliore la lisibilité du code.

```swift title="Swift - typealias pour la lisibilité"
// Créer un alias pour un type existant
typealias Identifiant = Int
typealias NomUtilisateur = String
typealias Celsius = Double

// Utilisation : le code devient auto-documenté
let userId: Identifiant = 42
let login: NomUtilisateur = "alice_dev"
let corpTemp: Celsius = 36.6

// typealias est particulièrement utile pour les types complexes
typealias CompletionHandler = (Bool, String?) -> Void
typealias DictionnaireDeStrings = [String: String]
```

<br>

---

## Tableau Récapitulatif des Types

| Type Swift | Équivalent JS | Équivalent PHP | Équivalent Python | Description |
| --- | --- | --- | --- | --- |
| `Int` | `number` (entier) | `int` | `int` | Entier signé |
| `Double` | `number` (décimal) | `float` | `float` | Virgule flottante 64 bits |
| `Float` | `number` | `float` | — | Virgule flottante 32 bits |
| `String` | `string` | `string` | `str` | Chaîne de caractères |
| `Character` | — | — | — | Caractère unique |
| `Bool` | `boolean` | `bool` | `bool` | Vrai / Faux |
| `UInt` | — | — | — | Entier non signé |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `let` crée une constante — préférez-le par défaut. `var` crée une variable modifiable. L'inférence de types évite de répéter les annotations, mais le type est toujours connu et fixé à la compilation. Une fois déclarée, une variable Swift ne peut pas changer de type. Les conversions entre types numériques sont toujours explicites — le compilateur refuse les conversions implicites qui pourraient perdre des données. `String`, `Int`, `Double`, `Bool` sont les quatre types quotidiens.

> Dans le module suivant, nous aborderons les **Structures de Contrôle** de Swift : `if`, le puissant `guard`, et le `switch` avec pattern matching — une version bien plus expressive que dans les autres langages.

<br>