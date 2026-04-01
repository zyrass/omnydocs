---
description: "Fonctions et closures Swift : paramètres nommés, valeurs de retour, @escaping, fonctions de premier ordre et trailing closure syntax."
icon: lucide/book-open-check
tags: ["SWIFT", "FONCTIONS", "CLOSURES", "ESCAPING", "PARAMÈTRES", "PREMIER-ORDRE"]
---

# Fonctions et Closures

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🟡 Intermédiaire"
  data-version="1.1"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Chef Cuisinier et ses Recettes"
    Une fonction, c'est une recette de cuisine : vous lui donnez des ingrédients (les paramètres), elle suit des étapes, et vous récupère un plat (la valeur de retour). Swift va plus loin : une closure, c'est une recette que vous pouvez plier, mettre dans votre poche, et donner à quelqu'un d'autre pour qu'il la prépare plus tard. La recette emporte avec elle tout ce dont elle a besoin — les ingrédients qu'elle avait sous la main au moment où vous l'avez pliée.

    Ce mécanisme de "capture" est au cœur de SwiftUI : chaque `Button`, chaque `onAppear`, chaque animation reçoit une closure qui sera exécutée plus tard.

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

    // return implicite pour une expression unique
    func carré(de n: Int) -> Int {
        n * n
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Déclaration de fonction"
    function saluer(prenom) {
        return `Bonjour, ${prenom} !`;
    }

    const carré = (n) => n * n;
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Déclaration de fonction"
    <?php
    function saluer(string $prenom): string {
        return "Bonjour, $prenom !";
    }

    function carré(int $n): int {
        return $n * $n;
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - Déclaration de fonction"
    def saluer(prenom: str) -> str:
        return f"Bonjour, {prenom} !"

    def carré(n: int) -> int:
        return n * n
    ```

<br>

---

## Les Paramètres Nommés — La Spécificité Swift

Chaque paramètre a potentiellement **deux noms** : un label externe (pour l'appelant) et un nom interne (dans le corps).

=== ":simple-swift: Swift"

    ```swift title="Swift - Labels externes et noms internes"
    // func nom(labelExterne nomInterne: Type)
    func déplacer(de origine: Int, vers destination: Int) -> Int {
        return destination - origine
    }

    // Appel : labels externes obligatoires — lecture naturelle
    let distance = déplacer(de: 0, vers: 100)

    // _ : supprime le label externe
    func multiplier(_ a: Int, _ b: Int) -> Int { a * b }
    let résultat = multiplier(4, 5)   // Pas de label

    // Valeur par défaut
    func créerMessage(pour prenom: String, tonalité: String = "formelle") -> String {
        switch tonalité {
        case "informelle": return "Salut \(prenom) !"
        default:           return "Bonjour \(prenom)."
        }
    }

    créerMessage(pour: "Alice")                         // "Bonjour Alice."
    créerMessage(pour: "Bob", tonalité: "informelle")   // "Salut Bob !"
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Pas de labels (déstructuration en remplacement)"
    // Simuler les labels : passer un objet
    function créerMessage({ prenom, tonalite = "formelle" } = {}) {
        return tonalite === "informelle" ? `Salut ${prenom} !` : `Bonjour ${prenom}.`;
    }

    créerMessage({ prenom: "Alice" });
    créerMessage({ prenom: "Bob", tonalite: "informelle" });
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Arguments nommés (PHP 8+)"
    <?php
    function créerMessage(string $prenom, string $tonalite = "formelle"): string {
        return $tonalite === "informelle" ? "Salut $prenom !" : "Bonjour $prenom.";
    }

    créerMessage(prenom: "Alice");
    créerMessage(prenom: "Bob", tonalite: "informelle");
    ```

=== ":simple-python: Python"

    ```python title="Python - Arguments nommés (keyword arguments)"
    def créer_message(prenom: str, tonalite: str = "formelle") -> str:
        return f"Salut {prenom} !" if tonalite == "informelle" else f"Bonjour {prenom}."

    créer_message(prenom="Alice")
    créer_message(prenom="Bob", tonalite="informelle")
    ```

<br>

---

## Valeurs de Retour Multiples avec les Tuples

```swift title="Swift - Retourner plusieurs valeurs"
func statistiques(de tableau: [Int]) -> (min: Int, max: Int, moyenne: Double) {
    let min = tableau.min() ?? 0
    let max = tableau.max() ?? 0
    let moyenne = Double(tableau.reduce(0, +)) / Double(tableau.count)
    return (min, max, moyenne)
}

let résultats = statistiques(de: [4, 8, 2, 15, 6])
print(résultats.min)      // 2
print(résultats.max)      // 15
print(résultats.moyenne)  // 7.0

// Décomposition du tuple
let (valMin, valMax, moy) = statistiques(de: [4, 8, 2, 15, 6])
```

<br>

---

## Closures

Une closure est une **fonction anonyme** qui peut capturer les variables de son contexte.

=== ":simple-swift: Swift"

    ```swift title="Swift - Syntaxe des closures et simplifications"
    // Forme complète
    let multiplierParDeux: (Int) -> Int = { (nombre: Int) -> Int in
        return nombre * 2
    }

    // Inférence du type (Swift déduit depuis la déclaration)
    let multiplierParDeux2: (Int) -> Int = { nombre in
        return nombre * 2
    }

    // return implicite pour une expression unique
    let multiplierParDeux3: (Int) -> Int = { nombre in nombre * 2 }

    // Shorthand argument names : $0, $1...
    let multiplierParDeux4: (Int) -> Int = { $0 * 2 }

    print(multiplierParDeux(5))    // 10
    print(multiplierParDeux4(5))   // 10
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Arrow functions"
    const multiplierParDeux = (nombre) => nombre * 2;
    const multiplierParDeux2 = (nombre) => { return nombre * 2; };
    console.log(multiplierParDeux(5));   // 10
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Arrow functions"
    <?php
    $multiplierParDeux = fn(int $nombre): int => $nombre * 2;
    echo $multiplierParDeux(5);   // 10
    ```

=== ":simple-python: Python"

    ```python title="Python - Lambda"
    multiplier_par_deux = lambda nombre: nombre * 2
    print(multiplier_par_deux(5))   # 10
    ```

<br>

### Trailing Closure Syntax

Quand le dernier paramètre est une closure, Swift autorise une syntaxe spéciale. C'est la syntaxe dominante dans SwiftUI.

```swift title="Swift - Trailing closure syntax"
func effectuerApresDelai(secondes: Double, action: () -> Void) {
    action()
}

// Syntaxe classique
effectuerApresDelai(secondes: 2.0, action: { print("Exécuté") })

// Trailing closure : la closure sort des parenthèses
effectuerApresDelai(secondes: 2.0) {
    print("Exécuté")
}

// Si la closure est le SEUL paramètre : parenthèses entièrement omises
func exécuter(action: () -> Void) { action() }
exécuter { print("Action directe") }

// En SwiftUI, on écrit :
// Button("Valider") {
//     validerFormulaire()
// }
// List(articles) { article in
//     Text(article.titre)
// }
```

<br>

### Capture de Variables

```swift title="Swift - Les closures capturent leur environnement"
func créerCompteur() -> () -> Int {
    var compte = 0

    // La closure capture compte — elle le maintient en vie après la fin de créerCompteur
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
print(compteur2())   // 1 — son propre compte
```

<br>

---

## `@escaping` — Les Closures qui Survivent à la Fonction

C'est l'un des concepts les plus importants pour écrire du code iOS réel. Il apparaît dans toutes les APIs réseau.

Par défaut, une closure passée en paramètre est **non-escaping** : elle s'exécute pendant l'appel de la fonction, puis est libérée. Le compilateur peut optimiser ce cas.

Une closure **`@escaping`** survit à la fonction qui la reçoit — elle est stockée et appelée plus tard, après que la fonction a retourné.

=== ":simple-swift: Swift"

    ```swift title="Swift - @escaping : closure appelée après retour de la fonction"
    // SANS @escaping : la closure s'exécute pendant la fonction
    func exécuterImmédiatement(action: () -> Void) {
        action()   // Appelée ici, pendant l'appel de exécuterImmédiatement
    }   // La closure est libérée ici

    // AVEC @escaping : la closure est stockée et appelée PLUS TARD
    // Le compilateur OBLIGE à marquer @escaping dans ce cas
    class GestionnaireRéseau {
        var completionEnAttente: (() -> Void)?

        func charger(url: String, completion: @escaping () -> Void) {
            // On STOCKE la closure — elle doit survivre à la fin de charger()
            self.completionEnAttente = completion

            // Simulation : la closure sera appelée 2 secondes plus tard
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                self.completionEnAttente?()
            }
        }   // La fonction retourne ICI — mais completion vivra encore 2s
    }

    let gestionnaire = GestionnaireRéseau()
    gestionnaire.charger(url: "https://api.example.com") {
        print("Données reçues — la fonction charger() a déjà retourné !")
    }
    ```

    ```swift title="Swift - @escaping avec Result : pattern réseau courant"
    // Pattern standard dans toutes les APIs iOS avant async/await
    func chargerUtilisateur(id: Int, completion: @escaping (Result<String, Error>) -> Void) {
        // La requête URLSession est asynchrone — completion sera appelée
        // APRÈS que chargerUtilisateur() a retourné
        URLSession.shared.dataTask(with: URL(string: "https://api.example.com/users/\(id)")!) { data, _, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            let nom = String(data: data ?? Data(), encoding: .utf8) ?? ""
            completion(.success(nom))
        }.resume()
    }

    // Utilisation
    chargerUtilisateur(id: 42) { résultat in
        switch résultat {
        case .success(let nom): print("Utilisateur : \(nom)")
        case .failure(let erreur): print("Erreur : \(erreur)")
        }
    }
    ```

    ```swift title="Swift - @escaping et self : le piège de la capture forte"
    class VueArticle {
        var titre = "Mon article"

        func charger() {
            // @escaping + capture de self : risque de cycle de rétention
            // Solution : [weak self] dans la capture list (module 15 — ARC)
            chargerUtilisateur(id: 1) { [weak self] résultat in
                guard let self = self else { return }
                // Si VueArticle a été libérée avant la réponse : on ne fait rien
                print("Réponse pour : \(self.titre)")
            }
        }
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Callbacks asynchrones (toujours @escaping par nature)"
    // En JavaScript, toutes les callbacks asynchrones sont "escaping" par nature
    // Il n'existe pas de distinction non-escaping / escaping

    function chargerUtilisateur(id, completion) {
        fetch(`https://api.example.com/users/${id}`)
            .then(res => res.json())
            .then(data => completion(null, data))
            .catch(err => completion(err, null));
        // La fonction retourne ICI, completion sera appelée plus tard
    }

    chargerUtilisateur(42, (erreur, données) => {
        if (erreur) { console.error(erreur); return; }
        console.log(données);
    });
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Callbacks (pas d'équivalent direct)"
    <?php
    // PHP est synchrone par défaut — les callbacks s'exécutent pendant l'appel
    // Pas d'équivalent natif à @escaping
    // Pour l'asynchrone : ReactPHP, Swoole, ou fibers (PHP 8.1+)

    function exécuterAvecCallback(callable $action): void {
        $action();   // Appelée pendant l'exécution de la fonction
    }

    exécuterAvecCallback(fn() => print("Exécuté"));
    ```

=== ":simple-python: Python"

    ```python title="Python - Callbacks (synchrone par défaut)"
    # Python synchrone : pas de distinction escaping / non-escaping
    # Pour l'asynchrone : asyncio avec async/await

    def exécuter_avec_callback(action):
        action()   # Appelée immédiatement

    import asyncio

    async def charger_utilisateur(id: int, completion):
        # Simulation async
        await asyncio.sleep(1)
        await completion({"nom": "Alice"})
    ```

!!! warning "Quand `@escaping` est obligatoire"
    Le compilateur exige `@escaping` dès qu'une closure est stockée dans une propriété, passée à une autre fonction asynchrone, ou capturée pour être appelée plus tard. Si vous oubliez `@escaping`, le compilateur produit une erreur claire : *"Passing non-escaping parameter 'completion' to function expecting an @escaping closure."*

!!! tip "@escaping et async/await"
    En Swift moderne avec `async/await` (module 14), les callbacks `@escaping` disparaissent dans la plupart des cas — remplacées par des fonctions `async throws`. Vous rencontrerez encore `@escaping` dans les APIs tierces et les SDKs anciens.

<br>

---

## Fonctions comme Valeurs de Premier Ordre

```swift title="Swift - Fonctions comme types"
func doubler(_ n: Int) -> Int { n * 2 }
func tripler(_ n: Int) -> Int { n * 3 }

// Assigner une fonction à une variable
var operation: (Int) -> Int = doubler
print(operation(5))   // 10

operation = tripler
print(operation(5))   // 15

// Passer une fonction comme paramètre
func appliquer(_ valeur: Int, avec transformation: (Int) -> Int) -> Int {
    transformation(valeur)
}

appliquer(4, avec: doubler)   // 8
appliquer(4, avec: tripler)   // 12
```

<br>

---

## `map`, `filter`, `reduce`

```swift title="Swift - Fonctions d'ordre supérieur sur les collections"
let nombres = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

let doublés = nombres.map { $0 * 2 }
let pairs   = nombres.filter { $0 % 2 == 0 }
let somme   = nombres.reduce(0, +)   // 55

// Chaînage
let résultat = nombres
    .filter { $0 % 2 == 0 }
    .map { $0 * $0 }
    .reduce(0, +)   // 4+16+36+64+100 = 220

// compactMap : transforme et supprime les nils
let textes = ["1", "deux", "3", "quatre", "5"]
let entiers = textes.compactMap { Int($0) }   // [1, 3, 5]
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les labels externes rendent les appels lisibles comme de la prose. `_` supprime un label. Les closures sont des fonctions anonymes qui capturent leur environnement. La trailing closure syntax place la closure après les parenthèses — c'est la syntaxe universelle de SwiftUI. `@escaping` est obligatoire quand une closure est stockée ou appelée après le retour de la fonction — pattern indispensable pour les APIs réseau. `map`, `filter` et `reduce` remplacent les boucles sur les collections.

> Dans le module suivant, nous couvrirons les **Collections** — `Array`, `Dictionary`, `Set` — avec leur comportement de value type fondamental en Swift.

<br>