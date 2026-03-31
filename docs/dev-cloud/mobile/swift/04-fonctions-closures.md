---
description: "Fonctions et closures Swift : paramètres nommés, valeurs de retour, fonctions de premier ordre et trailing closure syntax."
icon: lucide/book-open-check
tags: ["SWIFT", "FONCTIONS", "CLOSURES", "PARAMÈTRES", "PREMIER-ORDRE"]
---

# Fonctions et Closures

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🟡 Intermédiaire"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Chef Cuisinier et ses Recettes"
    Une fonction, c'est une recette de cuisine : vous lui donnez des ingrédients (les paramètres), elle suit des étapes, et vous récupère un plat (la valeur de retour). Swift va plus loin : une closure, c'est une recette que vous pouvez plier, mettre dans votre poche, et donner à quelqu'un d'autre pour qu'il la prépare plus tard. La recette emporte avec elle tout ce dont elle a besoin — les ingrédients qu'elle avait sous la main au moment où vous l'avez pliée.

    Ce mécanisme de "capture" est au cœur de SwiftUI : chaque `Button`, chaque `onAppear`, chaque animation reçoit une closure qui sera exécutée plus tard, dans un autre contexte.

<br>

---

## Déclaration d'une Fonction

=== ":simple-swift: Swift"

    ```swift title="Swift - Syntaxe de base d'une fonction"
    // func nomFonction(parametre: Type) -> TypeRetour { corps }
    func saluer(prenom: String) -> String {
        return "Bonjour, \(prenom) !"
    }

    let message = saluer(prenom: "Alice")
    print(message)   // "Bonjour, Alice !"

    // Fonction sans paramètre ni retour
    func afficherSeparateur() {
        print(String(repeating: "-", count: 40))
    }

    // Le mot-clé return est facultatif si la fonction est une expression unique
    func carré(de n: Int) -> Int {
        n * n   // return implicite
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Déclaration de fonction"
    function saluer(prenom) {
        return `Bonjour, ${prenom} !`;
    }

    const message = saluer("Alice");

    // Arrow function
    const carré = (n) => n * n;

    // Fonction sans paramètre ni retour
    function afficherSeparateur() {
        console.log("-".repeat(40));
    }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Déclaration de fonction"
    <?php
    function saluer(string $prenom): string {
        return "Bonjour, $prenom !";
    }

    $message = saluer("Alice");

    function carré(int $n): int {
        return $n * $n;
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - Déclaration de fonction"
    def saluer(prenom: str) -> str:
        return f"Bonjour, {prenom} !"

    message = saluer("Alice")

    def carré(n: int) -> int:
        return n * n
    ```

<br>

---

## Les Paramètres Nommés — La Spécificité Swift

Les paramètres nommés sont l'une des fonctionnalités les plus distinctives de Swift, inspirées d'Objective-C. Chaque paramètre a potentiellement **deux noms** : un label externe (pour l'appelant) et un nom interne (dans le corps de la fonction).

=== ":simple-swift: Swift"

    ```swift title="Swift - Labels externes et noms internes"
    // Syntaxe : func nom(labelExterne nomInterne: Type)
    // labelExterne : utilisé lors de l'appel
    // nomInterne   : utilisé dans le corps de la fonction

    func déplacer(de origine: Int, vers destination: Int) -> Int {
        // Dans le corps : on utilise les noms internes
        return destination - origine
    }

    // À l'appel : on utilise les labels externes
    // La lecture est proche de l'anglais naturel : "move from 0 to 100"
    let distance = déplacer(de: 0, vers: 100)

    // _ : supprime le label externe (l'appelant n'écrit pas le nom)
    func multiplier(_ a: Int, _ b: Int) -> Int {
        return a * b
    }

    let résultat = multiplier(4, 5)   // Pas de label : multiplier(4, 5) et non multiplier(a: 4, b: 5)

    // Valeur par défaut
    func créerMessage(pour prenom: String, tonalité: String = "formelle") -> String {
        switch tonalité {
        case "informelle": return "Salut \(prenom) !"
        default:           return "Bonjour \(prenom)."
        }
    }

    print(créerMessage(pour: "Alice"))                         // "Bonjour Alice."
    print(créerMessage(pour: "Bob", tonalité: "informelle"))   // "Salut Bob !"
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Pas de labels (déstructuration en remplacement)"
    // JavaScript n'a pas de labels de paramètres
    // L'ordre est la seule convention

    function déplacer(origine, destination) {
        return destination - origine;
    }

    const distance = déplacer(0, 100);   // L'ordre est implicite

    // Pour simuler les labels : passer un objet
    function créerMessage({ prenom, tonalite = "formelle" } = {}) {
        return tonalite === "informelle" ? `Salut ${prenom} !` : `Bonjour ${prenom}.`;
    }

    créerMessage({ prenom: "Alice" });
    créerMessage({ prenom: "Bob", tonalite: "informelle" });
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Arguments nommés (PHP 8+)"
    <?php
    function déplacer(int $origine, int $destination): int {
        return $destination - $origine;
    }

    // PHP 8 : arguments nommés (similaire aux labels Swift)
    $distance = déplacer(origine: 0, destination: 100);

    function créerMessage(string $prenom, string $tonalite = "formelle"): string {
        return $tonalite === "informelle" ? "Salut $prenom !" : "Bonjour $prenom.";
    }

    créerMessage(prenom: "Alice");
    créerMessage(prenom: "Bob", tonalite: "informelle");
    ```

=== ":simple-python: Python"

    ```python title="Python - Arguments nommés (keyword arguments)"
    def déplacer(origine: int, destination: int) -> int:
        return destination - origine

    # Python supporte les arguments nommés nativement
    distance = déplacer(origine=0, destination=100)

    def créer_message(prenom: str, tonalite: str = "formelle") -> str:
        return f"Salut {prenom} !" if tonalite == "informelle" else f"Bonjour {prenom}."

    créer_message(prenom="Alice")
    créer_message(prenom="Bob", tonalite="informelle")
    ```

<br>

---

## Valeurs de Retour Multiples

Swift peut retourner plusieurs valeurs simultanément grâce aux tuples.

```swift title="Swift - Retour de plusieurs valeurs avec un tuple"
// Un tuple regroupe plusieurs valeurs sans créer un type dédié
func statistiques(de tableau: [Int]) -> (min: Int, max: Int, moyenne: Double) {
    let min = tableau.min() ?? 0
    let max = tableau.max() ?? 0
    let moyenne = Double(tableau.reduce(0, +)) / Double(tableau.count)
    return (min, max, moyenne)
}

let résultats = statistiques(de: [4, 8, 2, 15, 6])

// Accès par nom du label du tuple
print(résultats.min)      // 2
print(résultats.max)      // 15
print(résultats.moyenne)  // 7.0

// Décomposition du tuple en variables séparées
let (valMin, valMax, moy) = statistiques(de: [4, 8, 2, 15, 6])
print(valMin, valMax, moy)

// _ pour ignorer une valeur du tuple
let (_, maximum, _) = statistiques(de: [4, 8, 2, 15, 6])
```

<br>

---

## Fonctions comme Valeurs de Premier Ordre

En Swift, une fonction est une valeur comme une autre — elle peut être assignée à une variable, passée en paramètre, et retournée par une autre fonction.

=== ":simple-swift: Swift"

    ```swift title="Swift - Fonctions comme types"
    // Type d'une fonction : (TypeParam1, TypeParam2) -> TypeRetour
    func doubler(_ n: Int) -> Int { n * 2 }
    func tripler(_ n: Int) -> Int { n * 3 }

    // Assigner une fonction à une variable
    var operation: (Int) -> Int = doubler
    print(operation(5))   // 10

    operation = tripler
    print(operation(5))   // 15

    // Passer une fonction comme paramètre
    func appliquer(_ valeur: Int, avec transformation: (Int) -> Int) -> Int {
        return transformation(valeur)
    }

    let résultat = appliquer(4, avec: doubler)    // 8
    let résultat2 = appliquer(4, avec: tripler)   // 12

    // Retourner une fonction depuis une fonction (higher-order function)
    func multipliateurPar(_ facteur: Int) -> (Int) -> Int {
        // Retourne une fonction qui multiplie son argument par facteur
        return { nombre in nombre * facteur }
    }

    let tripleur = multipliateurPar(3)
    print(tripleur(7))    // 21
    print(tripleur(10))   // 30
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Fonctions de premier ordre (natif)"
    // JavaScript traite les fonctions comme des valeurs par défaut
    const doubler = (n) => n * 2;
    const tripler = (n) => n * 3;

    let operation = doubler;
    console.log(operation(5));   // 10

    // Higher-order functions
    function appliquer(valeur, transformation) {
        return transformation(valeur);
    }

    appliquer(4, doubler);   // 8

    // Retourner une fonction
    function multipliateurPar(facteur) {
        return (nombre) => nombre * facteur;
    }

    const tripleur = multipliateurPar(3);
    console.log(tripleur(7));   // 21
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Fonctions de premier ordre (callable)"
    <?php
    $doubler = fn(int $n): int => $n * 2;
    $tripler = fn(int $n): int => $n * 3;

    $operation = $doubler;
    echo $operation(5);   // 10

    function appliquer(int $valeur, callable $transformation): int {
        return $transformation($valeur);
    }

    appliquer(4, $doubler);   // 8

    function multipliateurPar(int $facteur): callable {
        return fn(int $nombre): int => $nombre * $facteur;
    }

    $tripleur = multipliateurPar(3);
    echo $tripleur(7);   // 21
    ```

=== ":simple-python: Python"

    ```python title="Python - Fonctions de premier ordre (natif)"
    def doubler(n: int) -> int: return n * 2
    def tripler(n: int) -> int: return n * 3

    operation = doubler
    print(operation(5))   # 10

    def appliquer(valeur: int, transformation) -> int:
        return transformation(valeur)

    appliquer(4, doubler)   # 8

    def multipliateur_par(facteur: int):
        return lambda nombre: nombre * facteur

    tripleur = multipliateur_par(3)
    print(tripleur(7))   # 21
    ```

<br>

---

## Closures

Une closure est une **fonction anonyme** qui peut capturer les variables de son contexte d'origine. C'est l'outil le plus utilisé dans les APIs Apple.

=== ":simple-swift: Swift"

    ```swift title="Swift - Syntaxe des closures"
    // Forme complète d'une closure
    let multiplierParDeux: (Int) -> Int = { (nombre: Int) -> Int in
        return nombre * 2
    }

    // Simplifications progressives permises par Swift

    // 1. Inférence du type (Swift déduit les types depuis la déclaration)
    let multiplierParDeux2: (Int) -> Int = { nombre in
        return nombre * 2
    }

    // 2. return implicite pour une expression unique
    let multiplierParDeux3: (Int) -> Int = { nombre in nombre * 2 }

    // 3. Arguments $0, $1... (shorthand argument names)
    let multiplierParDeux4: (Int) -> Int = { $0 * 2 }

    // Les quatre formes produisent le même résultat
    print(multiplierParDeux(5))    // 10
    print(multiplierParDeux4(5))   // 10
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Arrow functions (équivalent des closures)"
    // Arrow functions capturent aussi leur contexte (this)
    const multiplierParDeux = (nombre) => nombre * 2;

    // Forme complète
    const multiplierParDeux2 = (nombre) => {
        return nombre * 2;
    };

    console.log(multiplierParDeux(5));   // 10
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Closures et arrow functions"
    <?php
    // Closure PHP avec use() pour capturer les variables
    $facteur = 2;
    $multiplier = function(int $nombre) use ($facteur): int {
        return $nombre * $facteur;
    };

    // Arrow function PHP (capture automatique du contexte)
    $multiplierParDeux = fn(int $nombre): int => $nombre * $facteur;

    echo $multiplierParDeux(5);   // 10
    ```

=== ":simple-python: Python"

    ```python title="Python - Lambda et closures"
    # Lambda : expression anonyme simple (une seule expression)
    multiplier_par_deux = lambda nombre: nombre * 2

    # Pour des closures complexes : fonction imbriquée
    def créer_multiplieur(facteur: int):
        def multiplier(nombre: int) -> int:
            return nombre * facteur   # Capture facteur du scope parent
        return multiplier

    multiplier_par_deux2 = créer_multiplieur(2)
    print(multiplier_par_deux2(5))   # 10
    ```

<br>

### Trailing Closure Syntax

Quand le dernier paramètre d'une fonction est une closure, Swift autorise une syntaxe spéciale qui déplace la closure en dehors des parenthèses. C'est la syntaxe dominante dans SwiftUI.

```swift title="Swift - Trailing closure syntax"
// Fonction qui prend une closure en dernier paramètre
func effectuerApresDelai(secondes: Double, action: () -> Void) {
    // En pratique : DispatchQueue.main.asyncAfter(...)
    action()
}

// Syntaxe classique (closure dans les parenthèses)
effectuerApresDelai(secondes: 2.0, action: {
    print("Exécuté après délai")
})

// Trailing closure syntax (closure après les parenthèses)
effectuerApresDelai(secondes: 2.0) {
    print("Exécuté après délai")
}

// Si la closure est le SEUL paramètre : on peut même omettre les parenthèses
func exécuter(action: () -> Void) { action() }

exécuter {
    print("Action directe")
}

// En pratique, dans SwiftUI :
// Button("Valider") {         ← Trailing closure
//     validerFormulaire()
// }
// List(articles) { article in  ← Trailing closure avec paramètre
//     Text(article.titre)
// }
```

<br>

### Capture de Variables

```swift title="Swift - Les closures capturent leur environnement"
func créerCompteur() -> () -> Int {
    var compte = 0   // Variable locale à créerCompteur

    // Cette closure CAPTURE la variable compte
    // Elle maintient une référence vers compte après la fin de créerCompteur
    let incrémenter = {
        compte += 1
        return compte
    }

    return incrémenter
}

let compteur1 = créerCompteur()
let compteur2 = créerCompteur()   // Instance indépendante

print(compteur1())   // 1
print(compteur1())   // 2
print(compteur1())   // 3
print(compteur2())   // 1  — compteur2 a son propre compte
```

*Chaque appel à `créerCompteur()` crée une nouvelle closure avec son propre état capturé. Ce mécanisme est au cœur des `@State` de SwiftUI.*

<br>

---

## `map`, `filter`, `reduce` — Fonctions d'Ordre Supérieur

Ces trois fonctions acceptent des closures et opèrent sur des collections. Elles remplaceront avantageusement les boucles dans de nombreux cas.

=== ":simple-swift: Swift"

    ```swift title="Swift - map, filter, reduce"
    let nombres = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    // map : transforme chaque élément
    let doublés = nombres.map { $0 * 2 }
    // [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    // filter : garde les éléments correspondant au prédicat
    let pairs = nombres.filter { $0 % 2 == 0 }
    // [2, 4, 6, 8, 10]

    // reduce : accumule les éléments en une seule valeur
    let somme = nombres.reduce(0) { accumulateur, élément in
        accumulateur + élément
    }
    // Forme courte : nombres.reduce(0, +)
    // 55

    // Chaînage
    let résultat = nombres
        .filter { $0 % 2 == 0 }     // Garder les pairs
        .map { $0 * $0 }             // Élever au carré
        .reduce(0, +)                // Sommer
    // 4 + 16 + 36 + 64 + 100 = 220

    // compactMap : map + suppression des nils
    let textes = ["1", "deux", "3", "quatre", "5"]
    let entiers = textes.compactMap { Int($0) }   // [1, 3, 5]

    // sorted : trier avec un critère personnalisé
    let mots = ["banane", "cerise", "abricot", "datte"]
    let triés = mots.sorted { $0 < $1 }   // Ou simplement : mots.sorted()
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - map, filter, reduce (natifs)"
    const nombres = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    const doublés = nombres.map(n => n * 2);
    const pairs = nombres.filter(n => n % 2 === 0);
    const somme = nombres.reduce((acc, n) => acc + n, 0);

    const résultat = nombres
        .filter(n => n % 2 === 0)
        .map(n => n * n)
        .reduce((acc, n) => acc + n, 0);   // 220
    ```

=== ":simple-php: PHP"

    ```php title="PHP - array_map, array_filter, array_reduce"
    <?php
    $nombres = range(1, 10);

    $doublés = array_map(fn($n) => $n * 2, $nombres);
    $pairs = array_filter($nombres, fn($n) => $n % 2 === 0);
    $somme = array_reduce($nombres, fn($acc, $n) => $acc + $n, 0);
    ```

=== ":simple-python: Python"

    ```python title="Python - map, filter, reduce"
    from functools import reduce

    nombres = list(range(1, 11))

    doublés = list(map(lambda n: n * 2, nombres))
    pairs = list(filter(lambda n: n % 2 == 0, nombres))
    somme = reduce(lambda acc, n: acc + n, nombres, 0)

    # Compréhensions de liste (style Python recommandé)
    doublés_comp = [n * 2 for n in nombres]
    pairs_comp = [n for n in nombres if n % 2 == 0]
    ```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les fonctions Swift ont des labels externes qui rendent les appels lisibles comme de la prose. `_` supprime un label quand l'appelant n'a pas besoin de le nommer. Les closures sont des fonctions anonymes qui capturent leur environnement — la syntaxe se simplifie progressivement jusqu'aux shorthand arguments `$0`, `$1`. La trailing closure syntax place la closure après les parenthèses — c'est la syntaxe universelle de SwiftUI. `map`, `filter` et `reduce` remplacent les boucles sur les collections.

> Dans le module suivant, nous couvrirons les **Collections** — `Array`, `Dictionary`, `Set` — avec leur particularité fondamentale en Swift : ce sont des **value types** copiés lors de l'assignation.

<br>