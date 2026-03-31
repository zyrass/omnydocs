---
description: "Les Optionals Swift : nil safety, optional binding, guard let, nil coalescing et optional chaining."
icon: lucide/book-open-check
tags: ["SWIFT", "OPTIONALS", "NIL", "GUARD", "UNWRAPPING", "NIL-SAFETY"]
---

# Optionals

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - La Boîte de Schrödinger"
    Imaginez une boîte fermée sur votre bureau. Elle contient **peut-être** un document important, peut-être rien du tout. En PHP ou JavaScript, on vous permettrait d'ouvrir la boîte et d'utiliser son contenu directement — si elle est vide, le programme plante ou se comporte de façon imprévisible. En Swift, le type `Optional` est une boîte étiquetée : l'étiquette indique explicitement *"cette boîte peut être vide"*. Swift vous **interdit** d'utiliser le contenu sans vérifier d'abord si la boîte contient quelque chose.

    Les Optionals éliminent à la compilation toute une catégorie de bugs — les fameux `TypeError: Cannot read properties of null` de JavaScript et les `Trying to get property of non-object` de PHP.

Les Optionals sont probablement le concept le plus déroutant pour un développeur venant de PHP ou JavaScript. Prenez le temps de les comprendre — tout le reste de Swift (et 100% de SwiftUI) est construit dessus.

<br>

---

## Le Problème que les Optionals Résolvent

Dans les langages sans nil safety, `null`/`nil` peut apparaître partout, à tout moment, de façon silencieuse.

=== ":simple-swift: Swift"

    ```swift title="Swift - Sans Optional, nil est impossible à ignorer"
    // En Swift, une variable de type String NE PEUT PAS être nil
    var prenom: String = "Alice"
    // prenom = nil   // ERREUR DE COMPILATION
    // error: 'nil' cannot be assigned to type 'String'

    // Pour déclarer qu'une valeur PEUT être absente : on ajoute ?
    var prenomOptional: String? = "Alice"   // Type : Optional<String>
    prenomOptional = nil   // Valide — c'est la sémantique attendue

    // La différence visuelle est intentionnelle :
    // String  → toujours une chaîne, garanti par le compilateur
    // String? → peut être une chaîne, peut être nil
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - null peut surgir partout"
    // En JavaScript, null et undefined peuvent apparaître sur n'importe quel type
    let prenom = "Alice";
    prenom = null;       // Valide, aucun avertissement
    prenom = undefined;  // Aussi valide

    // Le bug classique : appeler une méthode sur null
    const utilisateur = null;
    // utilisateur.nom  // TypeError: Cannot read properties of null
    // Aucune protection à la déclaration — l'erreur n'arrive qu'à l'exécution
    ```

=== ":simple-php: PHP"

    ```php title="PHP - null implicite partout"
    <?php
    // PHP : null peut être assigné à n'importe quelle variable
    $prenom = "Alice";
    $prenom = null;   // Valide

    // PHP 8 : types nullables avec ?
    function trouverUtilisateur(int $id): ?array {
        // Peut retourner un tableau ou null
        return null;
    }

    $user = trouverUtilisateur(42);
    // $user["nom"]  // Warning/Error si $user est null
    // PHP 8 : $user?->nom  (nullsafe operator — similaire à optional chaining Swift)
    ```

=== ":simple-python: Python"

    ```python title="Python - None sans protection"
    # Python : None peut être assigné à n'importe quelle variable
    prenom = "Alice"
    prenom = None

    # Le bug classique
    utilisateur = None
    # utilisateur["nom"]  # TypeError: 'NoneType' object is not subscriptable
    # Aucune protection à la déclaration
    ```

<br>

---

## Créer et Inspecter un Optional

```swift title="Swift - Optional : les deux états possibles"
// Un Optional<String> peut valoir :
// .some("Alice")  → contient une valeur
// .none           → ne contient rien (= nil)

var email: String? = "alice@example.com"
var téléphone: String? = nil

// Afficher un Optional directement (déconseillé en production)
print(email)      // Optional("alice@example.com")
print(téléphone)  // nil

// Vérification simple
if email != nil {
    print("Email présent")
}

// MAUVAISE PRATIQUE : forcer le déballage avec !
// Si la valeur est nil, le programme CRASHE immédiatement
print(email!)     // "alice@example.com" — dangereux
// print(téléphone!)  // Fatal error: Unexpectedly found nil while unwrapping
```

!!! danger "`!` le forced unwrap — à éviter"
    L'opérateur `!` force l'extraction d'un Optional sans vérification. Si la valeur est `nil`, le programme plante avec `Fatal error: Unexpectedly found nil`. Ne l'utilisez que quand vous avez une **certitude absolue** que la valeur n'est jamais nil — ce qui arrive rarement. Dans 95% des cas, il existe une meilleure alternative.

<br>

---

## Optional Binding — `if let`

L'optional binding extrait la valeur d'un Optional **dans un nouveau scope**, seulement si elle existe.

=== ":simple-swift: Swift"

    ```swift title="Swift - if let pour déballer un Optional"
    var prenom: String? = "Alice"

    // if let : crée une constante locale contenant la valeur déballée
    // Le bloc s'exécute uniquement si prenom contient une valeur
    if let nomRéel = prenom {
        // Dans ce bloc, nomRéel est de type String (pas String?)
        print("Bonjour \(nomRéel)")   // "Bonjour Alice"
    } else {
        print("Prénom absent")
    }

    // Swift 5.7+ : shadowing simplifié (même nom pour la constante déballée)
    if let prenom {
        print("Bonjour \(prenom)")   // prenom est String ici, pas String?
    }

    // Déballer plusieurs Optionals simultanément
    var ville: String? = "Lyon"
    var codePostal: String? = "69001"

    if let v = ville, let cp = codePostal {
        // Les deux blocs s'exécutent seulement si les DEUX ont une valeur
        print("\(v) (\(cp))")
    }

    // Combiner optional binding et condition
    if let age = Int("28"), age >= 18 {
        print("Majeur : \(age) ans")
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Vérification manuelle de null/undefined"
    let prenom = "Alice";

    // Equivalent de if let en JS : vérification explicite
    if (prenom !== null && prenom !== undefined) {
        console.log(`Bonjour ${prenom}`);
    }

    // Opérateur nullish (??)
    const affichage = prenom ?? "Inconnu";

    // Optional chaining (?.)
    const utilisateur = null;
    const ville = utilisateur?.adresse?.ville;  // undefined, pas de crash

    // Logical AND court-circuit
    prenom && console.log(`Bonjour ${prenom}`);
    ```

=== ":simple-php: PHP"

    ```php title="PHP - isset et null coalescing"
    <?php
    $prenom = "Alice";

    // isset() : vérifie si la variable existe et n'est pas null
    if (isset($prenom)) {
        echo "Bonjour $prenom";
    }

    // Null coalescing operator ?? (PHP 7+)
    $affichage = $prenom ?? "Inconnu";

    // Nullsafe operator ?-> (PHP 8+)
    $utilisateur = null;
    $ville = $utilisateur?->adresse?->ville;   // null, pas de crash
    ```

=== ":simple-python: Python"

    ```python title="Python - Vérification de None"
    prenom = "Alice"

    # Vérification standard
    if prenom is not None:
        print(f"Bonjour {prenom}")

    # Opérateur or (attention : falsy values)
    affichage = prenom or "Inconnu"

    # Walrus operator := (Python 3.8+) — proche de if let
    import re
    if match := re.search(r'\d+', "texte42"):
        print(match.group())  # "42"
    ```

<br>

---

## `guard let` — La Sortie Anticipée avec Optionals

`guard let` combine le `guard` du module 03 avec l'optional binding. C'est la technique recommandée pour valider des entrées en début de fonction.

```swift title="Swift - guard let pour les préconditions avec Optionals"
func envoyerEmail(à destinataire: String?, sujet: String?, corps: String?) {
    // guard let déballe l'Optional ET sort si nil
    guard let email = destinataire else {
        print("Erreur : destinataire manquant")
        return
    }

    guard let titreSujet = sujet else {
        print("Erreur : sujet manquant")
        return
    }

    // À partir d'ici : email et titreSujet sont des String (pas String?)
    // Ils restent disponibles APRÈS le guard, contrairement à if let
    let message = corps ?? ""   // corps peut être nil : valeur par défaut ""
    print("Envoi de '\(titreSujet)' à \(email) : \(message)")
}

envoyerEmail(à: "alice@example.com", sujet: "Hello", corps: nil)
// Envoi de 'Hello' à alice@example.com :

envoyerEmail(à: nil, sujet: "Hello", corps: "Bonjour")
// Erreur : destinataire manquant
```

!!! tip "if let vs guard let : la règle de décision"
    Utilisez `if let` quand vous voulez **faire quelque chose avec la valeur** dans un sous-bloc. Utilisez `guard let` quand la valeur est une **précondition de la fonction** et que son absence doit interrompre l'exécution. Après `guard let`, la variable déballée est disponible dans tout le reste de la fonction — ce qui n'est pas le cas avec `if let`.

<br>

---

## Nil Coalescing — L'Opérateur `??`

`??` fournit une valeur par défaut quand un Optional est `nil`. C'est la façon la plus concise de déballer un Optional quand on veut toujours obtenir une valeur.

=== ":simple-swift: Swift"

    ```swift title="Swift - Nil coalescing avec ??"
    var prenom: String? = nil
    var score: Int? = nil

    // ?? retourne la valeur de gauche si elle existe, celle de droite sinon
    let affichage = prenom ?? "Anonyme"   // "Anonyme"
    let points = score ?? 0               // 0

    // Enchaînement de ??
    var a: String? = nil
    var b: String? = nil
    var c: String? = "Valeur trouvée"

    let résultat = a ?? b ?? c ?? "Rien"  // "Valeur trouvée"

    // Cas pratique : score d'un utilisateur ou 0 par défaut
    func afficherScore(pour joueur: String, scores: [String: Int]) {
        let s = scores[joueur] ?? 0   // Dictionary retourne un Optional
        print("\(joueur) : \(s) points")
    }

    afficherScore(pour: "Alice", scores: ["Alice": 150, "Bob": 90])
    afficherScore(pour: "Charlie", scores: ["Alice": 150, "Bob": 90])
    // Alice : 150 points
    // Charlie : 0 points
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - ?? et || (différences importantes)"
    let prenom = null;

    // ?? : nullish coalescing — ne remplace que null et undefined
    const affichage1 = prenom ?? "Anonyme";  // "Anonyme"

    // || : retourne la première valeur truthy — ATTENTION aux pièges
    const score = 0;
    const points1 = score || 10;   // 10 — PIÈGE : 0 est falsy !
    const points2 = score ?? 10;   // 0  — Correct : ?? ne remplace pas 0
    ```

=== ":simple-php: PHP"

    ```php title="PHP - ?? opérateur null coalescing"
    <?php
    $prenom = null;
    $affichage = $prenom ?? "Anonyme";   // "Anonyme"

    // Enchaînement
    $a = null;
    $b = null;
    $c = "Valeur";
    $résultat = $a ?? $b ?? $c ?? "Rien";   // "Valeur"

    // ??= opérateur d'assignation null coalescing (PHP 7.4+)
    $config = [];
    $config["timeout"] ??= 30;   // Assigne 30 seulement si null/undefined
    ```

=== ":simple-python: Python"

    ```python title="Python - or comme nil coalescing (attention aux pièges)"
    prenom = None

    # Python n'a pas d'opérateur ?? natif
    affichage = prenom if prenom is not None else "Anonyme"

    # or : attention, remplace toutes les valeurs falsy (0, "", [])
    score = 0
    points = score or 10   # 10 — PIÈGE : 0 est falsy
    points_correct = score if score is not None else 10  # 0 — Correct
    ```

<br>

---

## Optional Chaining — L'Opérateur `?.`

Optional chaining permet d'appeler des propriétés ou méthodes en chaîne sur un Optional. Si l'un des maillons est `nil`, toute la chaîne retourne `nil` sans crash.

```swift title="Swift - Optional chaining avec ?."
struct Adresse {
    var ville: String
    var codePostal: String
}

struct Utilisateur {
    var nom: String
    var adresse: Adresse?   // L'adresse peut être absente
}

var utilisateur: Utilisateur? = Utilisateur(nom: "Alice", adresse: Adresse(ville: "Lyon", codePostal: "69001"))
var utilisateurSansAdresse: Utilisateur? = Utilisateur(nom: "Bob", adresse: nil)
var utilisateurNil: Utilisateur? = nil

// ?. : accès optionnel à chaque niveau de la chaîne
// Si un maillon est nil, la chaîne retourne nil immédiatement
let ville1 = utilisateur?.adresse?.ville           // Optional("Lyon")
let ville2 = utilisateurSansAdresse?.adresse?.ville // nil
let ville3 = utilisateurNil?.adresse?.ville         // nil

// Combiner ?. et ?? pour obtenir une valeur finale non-optionnelle
let affichage1 = utilisateur?.adresse?.ville ?? "Ville inconnue"   // "Lyon"
let affichage2 = utilisateurNil?.adresse?.ville ?? "Ville inconnue" // "Ville inconnue"

// Optional chaining sur des méthodes
let villes = ["Lyon", "Paris", "Marseille"]
let premièreVille: String? = villes.first
print(premièreVille?.uppercased() ?? "Aucune")   // "LYON"
```

<br>

---

## `while let` et `for case let`

```swift title="Swift - Patterns avancés avec les Optionals"
// while let : traiter des valeurs jusqu'au premier nil
var itérateur = [1, 2, 3, nil, 5].makeIterator()
while let valeur = itérateur.next() {
    print(valeur)   // 1, 2, 3  — s'arrête au nil
}

// for case let : filtrer les nils dans une boucle
let valeursMixtes: [Int?] = [1, nil, 3, nil, 5, 6]
for case let valeur? in valeursMixtes {
    print(valeur)   // 1, 3, 5, 6 — les nils sont ignorés
}

// Équivalent avec compactMap (plus idiomatique)
let valeursNonNulles = valeursMixtes.compactMap { $0 }   // [1, 3, 5, 6]
```

<br>

---

## Tableau Récapitulatif des Techniques

| Technique | Quand l'utiliser |
| --- | --- |
| `if let` | Faire quelque chose avec la valeur dans un sous-bloc |
| `guard let` | Précondition de fonction — valeur requise pour continuer |
| `??` | Fournir une valeur par défaut quand nil |
| `?.` | Accès en chaîne sans crash si un maillon est nil |
| `!` | Certitude **absolue** que la valeur n'est jamais nil (rare) |
| `compactMap` | Filtrer les nils dans une collection |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Un Optional est un type qui contient soit une valeur, soit `nil` — et Swift vous oblige à choisir explicitement comment gérer les deux cas. `if let` et `guard let` déballent un Optional dans une variable non-optionnelle. `??` fournit une valeur par défaut. `?.` enchaîne des accès sans crash. Le `!` force le déballage et crashe si nil — à éviter. Ce système garantit à la compilation qu'aucune variable ne sera `nil` par surprise.

> Dans le module suivant, nous aborderons **Structs et Classes** — la distinction fondamentale entre value types et reference types, qui explique pourquoi les Optionals, les Arrays et tout SwiftUI fonctionnent comme ils fonctionnent.

<br>