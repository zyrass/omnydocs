---
description: "Collections Swift : Array, Dictionary, Set — value semantics, mutabilité, itération et opérations fonctionnelles."
icon: lucide/book-open-check
tags: ["SWIFT", "ARRAY", "DICTIONARY", "SET", "COLLECTIONS", "VALUE-SEMANTICS"]
---

# Collections

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Les Trois Contenants de la Cuisine"
    Imaginez trois contenants dans une cuisine. Une **liste de courses** : chaque article a un numéro d'ordre, les doublons sont possibles, et l'ordre compte — c'est l'`Array`. Un **carnet d'adresses** : chaque contact a un nom unique qui permet de le retrouver directement — c'est le `Dictionary`. Un **sac de billes uniques** : chaque bille existe en un seul exemplaire, l'ordre n'a pas d'importance, et vous vérifiez en un instant si une bille est présente — c'est le `Set`.

    Ce qui rend les collections Swift différentes de PHP et JavaScript : ce sont des **value types**. Assigner une collection à une nouvelle variable la **copie** entièrement. Ce comportement surprend systématiquement les développeurs venant de langages où les tableaux sont des références.

<br>

---

## Array — La Liste Ordonnée

=== ":simple-swift: Swift"

    ```swift title="Swift - Array : création et opérations fondamentales"
    // Déclaration avec inférence de type
    let fruits = ["pomme", "banane", "cerise"]   // [String]
    var notes = [15, 18, 12, 9, 16]              // [Int]

    // Déclaration explicite
    var messages: [String] = []       // Tableau vide
    var scores: Array<Int> = []       // Syntaxe alternative (identique)

    // Tableau avec valeur répétée
    let zéros = Array(repeating: 0, count: 5)   // [0, 0, 0, 0, 0]

    // Accès par index (commence à 0)
    print(fruits[0])   // "pomme"
    print(fruits[2])   // "cerise"

    // ATTENTION : accès hors limites = crash à l'exécution
    // print(fruits[10])  // Fatal error: Index out of range

    // Propriétés utiles
    print(fruits.count)      // 3
    print(fruits.isEmpty)    // false
    print(fruits.first)      // Optional("pomme")
    print(fruits.last)       // Optional("cerise")

    // first et last retournent un Optional — on verra pourquoi au module 06
    ```

    ```swift title="Swift - Modification d'un Array (var obligatoire)"
    var courses = ["lait", "pain"]

    // Ajout
    courses.append("beurre")                    // ["lait", "pain", "beurre"]
    courses.append(contentsOf: ["oeufs", "sel"]) // Ajouter plusieurs éléments
    courses.insert("farine", at: 1)             // Insertion à un index

    // Suppression
    courses.remove(at: 0)         // Supprime "lait"
    courses.removeLast()          // Supprime le dernier
    courses.removeAll()           // Vide le tableau

    // Modification
    courses[0] = "fromage"        // Remplace l'élément à l'index 0

    // Recherche
    let contientPain = courses.contains("pain")
    let indexPain = courses.firstIndex(of: "pain")   // Optional<Int>
    ```

    ```swift title="Swift - La value semantics en pratique"
    var original = [1, 2, 3]
    var copie = original   // COPIE du tableau, pas une référence

    copie.append(4)

    print(original)   // [1, 2, 3]  — original non modifié
    print(copie)      // [1, 2, 3, 4]

    // En JavaScript ou PHP : original aurait aussi 4 si c'était un objet/référence
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Array (référence, pas copie)"
    const fruits = ["pomme", "banane", "cerise"];
    let notes = [15, 18, 12, 9, 16];

    console.log(fruits[0]);   // "pomme"
    console.log(fruits.length); // 3

    // Modification
    const courses = ["lait", "pain"];
    courses.push("beurre");              // Ajout en fin
    courses.unshift("farine");           // Ajout en début
    courses.splice(1, 0, "oeufs");       // Insertion à l'index 1
    courses.pop();                       // Supprime le dernier
    courses.shift();                     // Supprime le premier

    // DIFFÉRENCE : Array JavaScript est un objet — pas une copie à l'assignation
    const original = [1, 2, 3];
    const ref = original;   // Référence, pas une copie
    ref.push(4);
    console.log(original);  // [1, 2, 3, 4] — original modifié !

    // Pour copier : spread operator
    const copie = [...original];
    ```

=== ":simple-php: PHP"

    ```php title="PHP - array (valeur en PHP, comme Swift)"
    <?php
    $fruits = ["pomme", "banane", "cerise"];
    $notes = [15, 18, 12, 9, 16];

    echo $fruits[0];      // "pomme"
    echo count($fruits);  // 3

    $courses = ["lait", "pain"];
    $courses[] = "beurre";                    // Ajout en fin
    array_push($courses, "oeufs", "sel");
    array_unshift($courses, "farine");        // Ajout en début
    array_splice($courses, 1, 1);             // Suppression à l'index 1

    // PHP : les tableaux sont des valeurs (comme Swift)
    $original = [1, 2, 3];
    $copie = $original;   // Copie réelle
    $copie[] = 4;
    print_r($original);   // [1, 2, 3] — non modifié
    ```

=== ":simple-python: Python"

    ```python title="Python - list (référence comme JavaScript)"
    fruits = ["pomme", "banane", "cerise"]
    notes = [15, 18, 12, 9, 16]

    print(fruits[0])    # "pomme"
    print(len(fruits))  # 3

    courses = ["lait", "pain"]
    courses.append("beurre")
    courses.insert(1, "oeufs")
    courses.pop()
    courses.pop(0)

    # Python : les listes sont des références
    original = [1, 2, 3]
    ref = original      # Référence
    ref.append(4)
    print(original)     # [1, 2, 3, 4] — modifié

    copie = original.copy()   # Copie explicite nécessaire
    ```

<br>

---

## Dictionary — La Table de Correspondance

=== ":simple-swift: Swift"

    ```swift title="Swift - Dictionary : création et accès"
    // Déclaration
    let capitales = ["France": "Paris", "Espagne": "Madrid", "Italie": "Rome"]
    // Type inféré : [String: String]

    var scores: [String: Int] = [:]   // Dictionnaire vide

    // Accès — retourne un Optional (la clé peut ne pas exister)
    let capitale = capitales["France"]   // Optional("Paris")
    let inconnue = capitales["Japon"]    // nil

    // Accès avec valeur par défaut (évite l'Optional)
    let val = capitales["Japon", default: "Inconnue"]   // "Inconnue"

    // Modification (var obligatoire)
    var répertoire = ["Alice": "06 12 34 56 78"]
    répertoire["Bob"] = "07 98 76 54 32"     // Ajout
    répertoire["Alice"] = "06 11 22 33 44"   // Mise à jour
    répertoire["Bob"] = nil                   // Suppression

    // Propriétés
    print(répertoire.count)
    print(répertoire.keys)    // Les clés
    print(répertoire.values)  // Les valeurs

    // Itération
    for (nom, téléphone) in répertoire {
        print("\(nom) : \(téléphone)")
    }

    // Vérifier l'existence d'une clé
    if let tel = répertoire["Alice"] {
        print("Alice : \(tel)")   // Déballage de l'Optional — module 06
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Object et Map"
    // Object (usage courant, clés String uniquement)
    const capitales = { France: "Paris", Espagne: "Madrid" };
    console.log(capitales["France"]);    // "Paris"
    console.log(capitales.France);       // "Paris" — accès par point

    // Map (plus proche du Dictionary Swift : clés de tout type)
    const scores = new Map();
    scores.set("Alice", 95);
    scores.set("Bob", 82);
    console.log(scores.get("Alice"));    // 95
    console.log(scores.has("Charlie"));  // false

    for (const [nom, score] of scores) {
        console.log(`${nom} : ${score}`);
    }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - array associatif"
    <?php
    $capitales = ["France" => "Paris", "Espagne" => "Madrid"];
    echo $capitales["France"];   // "Paris"

    $répertoire = ["Alice" => "06 12 34 56 78"];
    $répertoire["Bob"] = "07 98 76 54 32";
    unset($répertoire["Bob"]);

    foreach ($répertoire as $nom => $tel) {
        echo "$nom : $tel\n";
    }

    // Vérifier l'existence d'une clé
    if (isset($répertoire["Alice"])) {
        echo $répertoire["Alice"];
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - dict"
    capitales = {"France": "Paris", "Espagne": "Madrid"}
    print(capitales["France"])              # "Paris"
    print(capitales.get("Japon", "Inconnu")) # "Inconnu"

    répertoire = {"Alice": "06 12 34 56 78"}
    répertoire["Bob"] = "07 98 76 54 32"
    del répertoire["Bob"]

    for nom, tel in répertoire.items():
        print(f"{nom} : {tel}")

    if "Alice" in répertoire:
        print(répertoire["Alice"])
    ```

<br>

---

## Set — L'Ensemble Sans Doublons

```swift title="Swift - Set : unicité et opérations ensemblistes"
// Déclaration (le type doit être Hashable)
var langages: Set<String> = ["Swift", "Python", "Go"]
var compétences: Set = ["Swift", "iOS", "Xcode"]   // Type inféré

// Ajout / Suppression
langages.insert("Rust")
langages.remove("Go")

// Recherche — O(1) : bien plus rapide que Array.contains pour de grandes collections
print(langages.contains("Swift"))   // true

// Pas de doublons : l'insertion d'un doublon est silencieusement ignorée
langages.insert("Swift")
langages.insert("Swift")
print(langages.count)   // Toujours 1 occurrence de "Swift"

// Opérations ensemblistes — la vraie valeur ajoutée de Set
let backend: Set = ["Go", "Rust", "Python", "PHP"]
let frontend: Set = ["Swift", "JavaScript", "TypeScript", "Python"]

let fullstack = backend.union(frontend)           // Tous les éléments
let commun = backend.intersection(frontend)       // ["Python"]
let backendUnique = backend.subtracting(frontend) // Éléments uniquement dans backend
let exclusifs = backend.symmetricDifference(frontend) // Éléments dans l'un OU l'autre mais pas les deux
```

!!! tip "Quand utiliser Set plutôt qu'Array"
    Utilisez `Set` quand l'unicité est importante (IDs, tags, permissions) et quand vous avez besoin de tester la présence fréquemment. `Set.contains` est en O(1) — `Array.contains` est en O(n). Sur 10 000 éléments, la différence de performance est significative.

<br>

---

## Opérations Fonctionnelles sur les Collections

Ces opérations s'appliquent identiquement sur `Array`, `Dictionary` et `Set`.

```swift title="Swift - map, filter, reduce, compactMap, flatMap"
let notes = [14, 18, 7, 15, 11, 19, 8]

// map : transformer chaque élément
let notesSur20 = notes.map { "Note : \($0)/20" }

// filter : garder selon un critère
let reçus = notes.filter { $0 >= 10 }   // [14, 18, 15, 11, 19]

// sorted : trier
let classées = notes.sorted()                    // Croissant
let classéesDéc = notes.sorted(by: >)            // Décroissant

// reduce : réduire à une valeur
let total = notes.reduce(0, +)                   // 92
let moyenne = Double(total) / Double(notes.count) // 13.14...

// compactMap : transformer et supprimer les nils simultanément
let textes = ["14", "excellent", "18", "absent", "7"]
let notesValides = textes.compactMap { Int($0) }  // [14, 18, 7]

// flatMap : aplatir les tableaux imbriqués
let matières = [["Maths", "Physique"], ["Histoire", "Géo"], ["Swift", "Go"]]
let toutesMatières = matières.flatMap { $0 }
// ["Maths", "Physique", "Histoire", "Géo", "Swift", "Go"]

// Chaînage d'opérations
let résultat = notes
    .filter { $0 >= 10 }    // Garder les reçus
    .map { Double($0) }     // Convertir en Double
    .reduce(0, +) / Double(reçus.count)  // Moyenne des reçus
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `Array` est une liste ordonnée qui accepte les doublons — ses éléments s'accèdent par index. `Dictionary` est une table clé/valeur — ses accès retournent un `Optional` car la clé peut être absente. `Set` est un ensemble sans doublons avec des opérations ensemblistes en O(1). Les trois sont des **value types** : une assignation crée une copie, contrairement aux tableaux JavaScript et Python qui sont des références. `let` rend une collection immuable — toute modification requiert `var`.

> Dans le module suivant, nous aborderons le concept le plus déroutant et le plus important de Swift : les **Optionals** — le mécanisme qui élimine les erreurs `null` à la compilation.

<br>