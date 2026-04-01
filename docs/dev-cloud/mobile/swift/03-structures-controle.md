---
description: "Structures de contrôle Swift : if, guard, switch avec pattern matching, boucles for-in, while et repeat-while."
icon: lucide/book-open-check
tags: ["SWIFT", "CONTRÔLE", "GUARD", "SWITCH", "BOUCLES"]
---

# Structures de Contrôle

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.1"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Poste de Contrôle aux Frontières"
    Une structure de contrôle, c'est comme un agent aux frontières. Il examine chaque situation, la compare à des règles précises, et décide du chemin à prendre : continuer, bifurquer, revenir en arrière, ou recommencer. En Swift, ces décisions sont exprimées par des constructions syntaxiques particulièrement expressives — notamment `guard` qui n'existe pas en PHP ou JavaScript, et un `switch` capable de bien plus que de simples comparaisons d'entiers.

<br>

---

## Conditions : `if` / `else`

=== ":simple-swift: Swift"

    ```swift title="Swift - if / else if / else"
    let age = 17
    let aUneCarteEtudiant = true

    if age >= 18 {
        print("Accès adulte autorisé")
    } else if age >= 16 && aUneCarteEtudiant {
        print("Accès tarif réduit")
    } else {
        print("Accès refusé")
    }

    // Les parenthèses autour de la condition sont FACULTATIVES en Swift
    // La convention communautaire : ne pas les écrire
    if age >= 18 { print("Majeur") }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - if / else if / else"
    const age = 17;
    const aUneCarteEtudiant = true;

    if (age >= 18) {
        console.log("Accès adulte autorisé");
    } else if (age >= 16 && aUneCarteEtudiant) {
        console.log("Accès tarif réduit");
    } else {
        console.log("Accès refusé");
    }
    // Les parenthèses sont OBLIGATOIRES en JavaScript
    ```

=== ":simple-php: PHP"

    ```php title="PHP - if / elseif / else"
    <?php
    $age = 17;
    $aUneCarteEtudiant = true;

    if ($age >= 18) {
        echo "Accès adulte autorisé";
    } elseif ($age >= 16 && $aUneCarteEtudiant) {
        echo "Accès tarif réduit";
    } else {
        echo "Accès refusé";
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - if / elif / else"
    age = 17
    a_une_carte_etudiant = True

    if age >= 18:
        print("Accès adulte autorisé")
    elif age >= 16 and a_une_carte_etudiant:
        print("Accès tarif réduit")
    else:
        print("Accès refusé")
    ```

<br>

---

## `guard` — La Sortie Anticipée Obligatoire

`guard` est l'une des constructions les plus importantes de Swift. Elle n'existe pas en PHP ou JavaScript.

Son principe : vérifier qu'une condition est vraie, et **sortir du contexte courant** si elle est fausse. Le corps du `guard` contient le chemin de l'échec. Le chemin du succès continue normalement après.

=== ":simple-swift: Swift"

    ```swift title="Swift - guard avec conditions booléennes"
    func traiterCommande(quantite: Int, stock: Int, utilisateur: String) {
        // Sans guard : imbrication en pyramide difficile à lire
        // if quantite > 0 {
        //     if stock >= quantite {
        //         if !utilisateur.isEmpty { ... }
        //     }
        // }

        // Avec guard : préconditions exprimées à plat, en début de fonction
        guard quantite > 0 else {
            print("Erreur : quantité invalide")
            return   // Obligatoire — guard doit toujours quitter le scope
        }

        guard stock >= quantite else {
            print("Erreur : stock insuffisant (\(stock) disponibles)")
            return
        }

        guard !utilisateur.isEmpty else {
            print("Erreur : utilisateur non identifié")
            return
        }

        // Ici, toutes les conditions sont garanties valides
        print("Commande de \(quantite) validée pour \(utilisateur)")
    }

    traiterCommande(quantite: 3,  stock: 10, utilisateur: "alice")  // OK
    traiterCommande(quantite: 0,  stock: 10, utilisateur: "alice")  // quantité invalide
    traiterCommande(quantite: 15, stock: 5,  utilisateur: "alice")  // stock insuffisant
    ```

    !!! note "guard et les Optionals"
        `guard` peut aussi déballer des Optionals avec `guard let` — c'est l'une de ses utilisations les plus fréquentes en pratique. Cette syntaxe sera couverte entièrement dans le **module 06 — Optionals** une fois que vous aurez compris ce qu'est un Optional. Pour l'instant, retenez le principe : `guard` vérifie une condition et sort si elle est fausse.

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Early return (équivalent manuel de guard)"
    // JavaScript n'a pas de guard — pattern équivalent : early return
    function traiterCommande(quantite, stock, utilisateur) {
        if (quantite <= 0) {
            console.log("Erreur : quantité invalide");
            return;
        }
        if (stock < quantite) {
            console.log(`Erreur : stock insuffisant (${stock} disponibles)`);
            return;
        }
        if (!utilisateur) {
            console.log("Erreur : utilisateur non identifié");
            return;
        }
        console.log(`Commande de ${quantite} validée pour ${utilisateur}`);
    }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Early return (équivalent de guard)"
    <?php
    function traiterCommande(int $quantite, int $stock, string $utilisateur): void {
        if ($quantite <= 0) {
            echo "Erreur : quantité invalide";
            return;
        }
        if ($stock < $quantite) {
            echo "Erreur : stock insuffisant ($stock disponibles)";
            return;
        }
        if (empty($utilisateur)) {
            echo "Erreur : utilisateur non identifié";
            return;
        }
        echo "Commande de $quantite validée pour $utilisateur";
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - Early return (équivalent de guard)"
    def traiter_commande(quantite: int, stock: int, utilisateur: str) -> None:
        if quantite <= 0:
            print("Erreur : quantité invalide")
            return
        if stock < quantite:
            print(f"Erreur : stock insuffisant ({stock} disponibles)")
            return
        if not utilisateur:
            print("Erreur : utilisateur non identifié")
            return
        print(f"Commande de {quantite} validée pour {utilisateur}")
    ```

!!! tip "guard vs if : quand choisir lequel"
    Utilisez `guard` pour les **préconditions** en début de fonction — conditions qui doivent être vraies pour que la suite ait du sens. Utilisez `if/else` quand vous **branchez la logique** entre deux chemins alternatifs valides.

<br>

---

## `switch` — Le Pattern Matching

Le `switch` Swift va bien au-delà de la simple comparaison de valeurs. C'est un outil de **pattern matching** qui peut correspondre à des intervalles, des conditions et des chaînes multiples.

=== ":simple-swift: Swift"

    ```swift title="Swift - switch avec pattern matching"
    let score = 78

    // Correspondance sur des intervalles
    switch score {
    case 90...100:
        print("Mention Très Bien")
    case 80..<90:
        print("Mention Bien")
    case 70..<80:
        print("Mention Assez Bien")
    case 50..<70:
        print("Passable")
    case 0..<50:
        print("Insuffisant")
    default:
        print("Score invalide")
    }

    // Plusieurs valeurs dans un même case
    let commande = "nord"
    switch commande {
    case "nord", "n":
        print("Direction : Nord")
    case "sud", "s":
        print("Direction : Sud")
    case let direction where direction.hasPrefix("est"):
        // where : condition supplémentaire
        print("Direction : \(direction)")
    default:
        print("Direction inconnue")
    }

    // Pas de fallthrough automatique en Swift — pas besoin de break
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - switch (comparaison stricte uniquement)"
    const score = 78;

    // JS switch n'accepte pas les intervalles : on utilise if/else
    if (score >= 90)      console.log("Mention Très Bien");
    else if (score >= 80) console.log("Mention Bien");
    else if (score >= 70) console.log("Mention Assez Bien");

    // switch JS : break obligatoire pour éviter le fallthrough
    const commande = "nord";
    switch (commande) {
        case "nord": case "n":
            console.log("Direction : Nord"); break;
        case "sud":  case "s":
            console.log("Direction : Sud");  break;
        default:
            console.log("Direction inconnue");
    }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - match() (PHP 8)"
    <?php
    $score = 78;

    $mention = match(true) {
        $score >= 90 => "Très Bien",
        $score >= 80 => "Bien",
        $score >= 70 => "Assez Bien",
        $score >= 50 => "Passable",
        default      => "Insuffisant"
    };
    echo $mention;
    ```

=== ":simple-python: Python"

    ```python title="Python - match/case (Python 3.10+)"
    score = 78

    match score:
        case s if s >= 90: print("Mention Très Bien")
        case s if s >= 80: print("Mention Bien")
        case s if s >= 70: print("Mention Assez Bien")
        case _:            print("Insuffisant")
    ```

<br>

---

## Boucles

<br>

### `for-in` — Itération sur une séquence

=== ":simple-swift: Swift"

    ```swift title="Swift - Boucles for-in"
    let fruits = ["pomme", "banane", "cerise"]
    for fruit in fruits {
        print(fruit)
    }

    // Intervalle fermé : 1 à 5 inclus
    for i in 1...5 {
        print("Étape \(i)")
    }

    // Intervalle semi-ouvert : 0 à 4
    for i in 0..<5 {
        print(i)
    }

    // _ pour ignorer la valeur d'itération
    for _ in 0..<3 {
        print("Répétition")
    }

    // Dictionnaire : déstructuration de la paire clé/valeur
    let capitales = ["France": "Paris", "Espagne": "Madrid"]
    for (pays, capitale) in capitales {
        print("\(pays) → \(capitale)")
    }

    // stride : itération par pas personnalisé
    for n in stride(from: 0, to: 10, by: 2) {
        print(n)   // 0, 2, 4, 6, 8
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - for...of et for...in"
    const fruits = ["pomme", "banane", "cerise"];

    for (const fruit of fruits) { console.log(fruit); }

    for (let i = 1; i <= 5; i++) { console.log(`Étape ${i}`); }

    const capitales = { France: "Paris", Espagne: "Madrid" };
    for (const pays in capitales) {
        console.log(`${pays} → ${capitales[pays]}`);
    }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - for et foreach"
    <?php
    $fruits = ["pomme", "banane", "cerise"];
    foreach ($fruits as $fruit) { echo $fruit . PHP_EOL; }

    for ($i = 1; $i <= 5; $i++) { echo "Étape $i" . PHP_EOL; }

    $capitales = ["France" => "Paris", "Espagne" => "Madrid"];
    foreach ($capitales as $pays => $capitale) {
        echo "$pays → $capitale" . PHP_EOL;
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - for et range"
    fruits = ["pomme", "banane", "cerise"]
    for fruit in fruits: print(fruit)

    for i in range(1, 6): print(f"Étape {i}")

    for i in range(0, 10, 2): print(i)   # stride équivalent

    capitales = {"France": "Paris", "Espagne": "Madrid"}
    for pays, capitale in capitales.items():
        print(f"{pays} → {capitale}")
    ```

<br>

### `while` et `repeat-while`

```swift title="Swift - while, repeat-while et contrôle de boucle"
// while : vérifie la condition AVANT chaque itération
var tentatives = 0
while tentatives < 3 {
    print("Tentative \(tentatives + 1)")
    tentatives += 1
}

// repeat-while : exécute au moins une fois, condition vérifiée APRÈS
var nombre = 10
repeat {
    print(nombre)
    nombre -= 3
} while nombre > 0
// Affiche : 10, 7, 4, 1

// Contrôle de boucle
for i in 1...10 {
    if i == 5 { continue }   // Saute cette itération
    if i == 8 { break }      // Quitte la boucle
    print(i)   // 1, 2, 3, 4, 6, 7
}

// Boucles étiquetées : break/continue sur une boucle externe spécifique
boucleExterne: for i in 1...3 {
    for j in 1...3 {
        if j == 2 { continue boucleExterne }
        print("\(i)-\(j)")
    }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `if/else` fonctionne sans parenthèses obligatoires. `guard` exprime les préconditions et oblige à traiter les erreurs en premier — il doit toujours quitter le scope. Le `switch` effectue du pattern matching sur des intervalles et des conditions sans `break`. `for-in` itère sur n'importe quelle séquence, `stride` contrôle le pas. `repeat-while` est l'équivalent de `do...while`.

> Dans le module suivant, nous couvrirons les **Fonctions et Closures** — la clé pour comprendre comment Swift traite les fonctions comme des valeurs de première classe.

<br>