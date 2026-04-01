---
description: "Les Optionals Swift : nil safety, optional binding, guard let, nil coalescing, optional chaining et exercices pratiques."
icon: lucide/book-open-check
tags: ["SWIFT", "OPTIONALS", "NIL", "GUARD", "UNWRAPPING", "NIL-SAFETY"]
---

# Optionals

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.1"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - La Boîte de Schrödinger"
    Imaginez une boîte fermée sur votre bureau. Elle contient **peut-être** un document important, peut-être rien du tout. En PHP ou JavaScript, on vous permettrait d'ouvrir la boîte et d'utiliser son contenu directement — si elle est vide, le programme plante ou se comporte de façon imprévisible. En Swift, le type `Optional` est une boîte étiquetée : l'étiquette indique explicitement *"cette boîte peut être vide"*. Swift vous **interdit** d'utiliser le contenu sans vérifier d'abord si la boîte contient quelque chose.

    Les Optionals éliminent à la compilation toute une catégorie de bugs — les `TypeError: Cannot read properties of null` de JavaScript et les `Trying to get property of non-object` de PHP.

Les Optionals sont le concept le plus déroutant pour un développeur venant de PHP ou JavaScript. Prenez le temps de les comprendre — tout le reste de Swift et 100% de SwiftUI est construit dessus.

<br>

---

## Le Problème que les Optionals Résolvent

=== ":simple-swift: Swift"

    ```swift title="Swift - nil est impossible à ignorer"
    // En Swift, une variable de type String NE PEUT PAS être nil
    var prenom: String = "Alice"
    // prenom = nil   // ERREUR DE COMPILATION
    // error: 'nil' cannot be assigned to type 'String'

    // Pour autoriser nil : on ajoute ? au type
    var prenomOptional: String? = "Alice"
    prenomOptional = nil   // Valide — c'est la sémantique déclarée

    // String  → toujours une chaîne, garanti par le compilateur
    // String? → peut être une chaîne, peut être nil
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - null peut surgir partout"
    let prenom = "Alice";
    prenom = null;       // Valide, aucun avertissement
    prenom = undefined;  // Aussi valide

    const utilisateur = null;
    // utilisateur.nom  // TypeError à l'EXÉCUTION — pas de protection à la déclaration
    ```

=== ":simple-php: PHP"

    ```php title="PHP - null implicite partout"
    <?php
    $prenom = "Alice";
    $prenom = null;

    function trouverUtilisateur(int $id): ?array {
        return null;   // PHP 8 : type nullable avec ?
    }
    // $user["nom"]  // Warning si $user est null
    ```

=== ":simple-python: Python"

    ```python title="Python - None sans protection"
    prenom = "Alice"
    prenom = None

    utilisateur = None
    # utilisateur["nom"]  # TypeError à l'exécution
    ```

<br>

---

## Créer et Inspecter un Optional

```swift title="Swift - Les deux états d'un Optional"
var email: String? = "alice@example.com"
var téléphone: String? = nil

// Afficher un Optional directement
print(email)      // Optional("alice@example.com")
print(téléphone)  // nil

// Vérification simple
if email != nil {
    print("Email présent")
}

// MAUVAISE PRATIQUE : forcer le déballage avec !
print(email!)     // "alice@example.com"
// print(téléphone!)  // Fatal error: Unexpectedly found nil — CRASH
```

!!! danger "`!` le forced unwrap — à éviter"
    L'opérateur `!` force l'extraction sans vérification. Si la valeur est `nil`, le programme crashe avec `Fatal error`. Ne l'utilisez que lorsque vous avez une **certitude absolue** que la valeur n'est jamais nil — ce qui arrive rarement. Dans 95% des cas, il existe une meilleure alternative.

<br>

---

## Optional Binding — `if let`

`if let` extrait la valeur d'un Optional dans un nouveau scope, seulement si elle existe.

=== ":simple-swift: Swift"

    ```swift title="Swift - if let pour déballer un Optional"
    var prenom: String? = "Alice"

    // nomRéel est de type String (pas String?) dans ce bloc
    if let nomRéel = prenom {
        print("Bonjour \(nomRéel)")   // "Bonjour Alice"
    } else {
        print("Prénom absent")
    }

    // Swift 5.7+ : shadowing simplifié
    if let prenom {
        print("Bonjour \(prenom)")   // prenom est String ici
    }

    // Déballer plusieurs Optionals simultanément
    var ville: String? = "Lyon"
    var codePostal: String? = "69001"

    if let v = ville, let cp = codePostal {
        print("\(v) (\(cp))")
    }

    // Combiner optional binding et condition
    if let age = Int("28"), age >= 18 {
        print("Majeur : \(age) ans")
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Vérification manuelle"
    let prenom = "Alice";

    if (prenom !== null && prenom !== undefined) {
        console.log(`Bonjour ${prenom}`);
    }

    // Optional chaining (?.)
    const utilisateur = null;
    const ville = utilisateur?.adresse?.ville;  // undefined, pas de crash
    ```

=== ":simple-php: PHP"

    ```php title="PHP - isset et null coalescing"
    <?php
    $prenom = "Alice";

    if (isset($prenom)) {
        echo "Bonjour $prenom";
    }

    $ville = $utilisateur?->adresse?->ville ?? "Inconnue";
    ```

=== ":simple-python: Python"

    ```python title="Python - Vérification de None"
    prenom = "Alice"

    if prenom is not None:
        print(f"Bonjour {prenom}")

    # Walrus operator (Python 3.8+)
    import re
    if match := re.search(r'\d+', "texte42"):
        print(match.group())   # "42"
    ```

<br>

---

## `guard let` — Sortie Anticipée avec Optionals

`guard let` combine le `guard` du module 03 avec l'optional binding. La variable déballée est disponible dans **tout le reste de la fonction** — contrairement à `if let`.

```swift title="Swift - guard let pour les préconditions avec Optionals"
func envoyerEmail(à destinataire: String?, sujet: String?, corps: String?) {
    guard let email = destinataire else {
        print("Erreur : destinataire manquant")
        return
    }

    guard let titreSujet = sujet else {
        print("Erreur : sujet manquant")
        return
    }

    // email et titreSujet sont des String (pas String?) ici
    // Disponibles jusqu'à la fin de la fonction
    let message = corps ?? ""
    print("Envoi de '\(titreSujet)' à \(email) : \(message)")
}

envoyerEmail(à: "alice@example.com", sujet: "Hello", corps: nil)
// Envoi de 'Hello' à alice@example.com :

envoyerEmail(à: nil, sujet: "Hello", corps: "Bonjour")
// Erreur : destinataire manquant
```

!!! tip "if let vs guard let"
    `if let` → faire quelque chose **dans un sous-bloc** avec la valeur. `guard let` → condition **obligatoire** pour la suite de la fonction, valeur disponible ensuite sans imbrication.

<br>

---

## Nil Coalescing — L'Opérateur `??`

=== ":simple-swift: Swift"

    ```swift title="Swift - ?? pour une valeur par défaut"
    var prenom: String? = nil
    var score: Int? = nil

    let affichage = prenom ?? "Anonyme"   // "Anonyme"
    let points = score ?? 0               // 0

    // Enchaînement
    var a: String? = nil
    var b: String? = nil
    var c: String? = "Trouvé"
    let résultat = a ?? b ?? c ?? "Rien"  // "Trouvé"

    // Cas pratique : valeur dans un dictionnaire ou 0 par défaut
    let scores = ["Alice": 150, "Bob": 90]
    let scoreCharlie = scores["Charlie"] ?? 0   // 0
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - ?? et || (différence importante)"
    // ?? : remplace seulement null et undefined
    const score = 0;
    const a = score ?? 10;   // 0 — score existe
    const b = score || 10;   // 10 — PIÈGE : 0 est falsy pour ||
    ```

=== ":simple-php: PHP"

    ```php title="PHP - ?? opérateur null coalescing"
    <?php
    $prenom = null;
    $affichage = $prenom ?? "Anonyme";

    $config = [];
    $config["timeout"] ??= 30;   // Assigne 30 seulement si null/undefined
    ```

=== ":simple-python: Python"

    ```python title="Python - or (attention aux pièges)"
    prenom = None
    # Python n'a pas d'opérateur ??
    affichage = prenom if prenom is not None else "Anonyme"
    # Attention : or remplace toutes les falsy values (0, "", [])
    ```

<br>

---

## Optional Chaining — L'Opérateur `?.`

`?.` permet d'accéder en chaîne sur un Optional. Si un maillon est nil, toute la chaîne retourne nil sans crash.

```swift title="Swift - Optional chaining avec ?."
struct Adresse {
    var ville: String
}

struct Utilisateur {
    var nom: String
    var adresse: Adresse?
}

var utilisateur: Utilisateur? = Utilisateur(nom: "Alice", adresse: Adresse(ville: "Lyon"))
var utilisateurNil: Utilisateur? = nil

let ville1 = utilisateur?.adresse?.ville   // Optional("Lyon")
let ville2 = utilisateurNil?.adresse?.ville // nil — pas de crash

// Combiner ?. et ??
let affichage = utilisateur?.adresse?.ville ?? "Ville inconnue"   // "Lyon"
let affichage2 = utilisateurNil?.adresse?.ville ?? "Ville inconnue" // "Ville inconnue"
```

<br>

---

## Tableau Récapitulatif

| Technique | Quand l'utiliser |
| --- | --- |
| `if let` | Faire quelque chose avec la valeur dans un sous-bloc |
| `guard let` | Précondition — valeur requise pour la suite de la fonction |
| `??` | Valeur par défaut quand nil |
| `?.` | Accès en chaîne sans crash si un maillon est nil |
| `!` | Certitude absolue que la valeur n'est jamais nil (rare) |
| `compactMap` | Filtrer les nils dans une collection |

<br>

---

## Exercices

!!! note "À vous de jouer"
    Ouvrez un Swift Playground et résolvez les exercices suivants. Les solutions sont volontairement absentes — le compilateur vous guidera.

**Exercice 1 — Déballer un prénom**

```swift title="Swift - Exercice 1"
// Déclarez une variable prenomOptional de type String?
// Assignez-lui "Swift"
// Affichez "Bonjour Swift" si la valeur existe, "Inconnu" sinon
// Puis passez prenomOptional à nil et observez le comportement
var prenomOptional: String? = ???
```

**Exercice 2 — Validation de formulaire**

```swift title="Swift - Exercice 2"
// Complétez la fonction suivante en utilisant guard let
// La fonction doit retourner nil si email est vide ou sans "@"
// Sinon, retourner l'email en minuscules

func validerEmail(_ email: String?) -> String? {
    // Votre code ici
}

print(validerEmail(nil))            // nil
print(validerEmail(""))             // nil
print(validerEmail("Alice@Ex.COM")) // Optional("alice@ex.com")
```

**Exercice 3 — Chaînage d'Optionals**

```swift title="Swift - Exercice 3"
struct Commande {
    var client: Client?
}

struct Client {
    var adresse: Adresse?
}

struct Adresse {
    var codePostal: String
}

var commande: Commande? = Commande(client: Client(adresse: Adresse(codePostal: "69001")))

// Sans optional chaining : écrivez le code avec if let imbriqués
// Avec optional chaining : récupérez le code postal en une ligne
// Résultat attendu : "69001" ou "Non renseigné"
```

**Exercice 4 — Conversion sécurisée**

```swift title="Swift - Exercice 4"
// Écrivez une fonction qui convertit une [String] en [Int]
// en ignorant les valeurs non convertibles
// Hint : compactMap

let entrées = ["12", "cinq", "7", "42", "trente", "100"]
// Résultat attendu : [12, 7, 42, 100]
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Un Optional contient soit une valeur, soit `nil` — Swift vous oblige à choisir comment gérer les deux cas. `if let` et `guard let` déballent un Optional dans une variable non-optionnelle. `??` fournit une valeur par défaut. `?.` enchaîne des accès sans crash. Le `!` force le déballage et crashe si nil. Ce système garantit qu'aucune variable ne sera `nil` par surprise.

> Dans le module suivant, nous aborderons **Structs et Classes** — la distinction fondamentale entre value types et reference types.

<br>