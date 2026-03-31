---
description: "Gestion des erreurs Swift : throws, do/catch, try, try?, try! et le type Result<T, E>."
icon: lucide/book-open-check
tags: ["SWIFT", "ERREURS", "THROWS", "DO-CATCH", "RESULT", "TRY"]
---

# Gestion des Erreurs

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Contrat de Livraison"
    Quand vous commandez un colis, le livreur peut soit réussir la livraison, soit échouer pour une raison précise : adresse introuvable, destinataire absent, colis endommagé. Un bon système de livraison ne fait pas comme si les échecs n'existaient pas — il les documente, les communique, et permet au destinataire de réagir de façon appropriée à chaque cas.

    Swift adopte cette philosophie : une fonction qui peut échouer l'annonce explicitement avec `throws`. L'appelant est **obligé** de traiter les cas d'erreur — il ne peut pas les ignorer comme en JavaScript avec une Promise non gérée.

<br>

---

## Définir des Erreurs

En Swift, les erreurs sont des types qui se conforment au protocol `Error`. Les enums sont la structure idéale.

=== ":simple-swift: Swift"

    ```swift title="Swift - Définir des types d'erreur avec enum"
    // Une erreur Swift : un type conforme au protocol Error
    enum ErreurFichier: Error {
        case fichierIntrouvable(chemin: String)
        case permissionsInsuffisantes
        case fichierCorrompu(détail: String)
        case disquePlein(espaceDisponible: Int)
    }

    enum ErreurRéseau: Error {
        case timeout(durée: TimeInterval)
        case httpErreur(code: Int, message: String)
        case décodageImpossible
        case pasDInternet
    }

    // Les erreurs peuvent implémenter LocalizedError pour des messages lisibles
    extension ErreurRéseau: LocalizedError {
        var errorDescription: String? {
            switch self {
            case .timeout(let d):       return "Timeout après \(d) secondes"
            case .httpErreur(let c, let m): return "HTTP \(c) : \(m)"
            case .décodageImpossible:   return "Impossible de décoder la réponse"
            case .pasDInternet:         return "Pas de connexion Internet"
            }
        }
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Gestion des erreurs avec throw et try/catch"
    // JavaScript : Error est une classe, pas un enum
    class ErreurFichier extends Error {
        constructor(message, chemin) {
            super(message);
            this.name = "ErreurFichier";
            this.chemin = chemin;
        }
    }

    class ErreurHTTP extends Error {
        constructor(code, message) {
            super(message);
            this.name = "ErreurHTTP";
            this.code = code;
        }
    }

    // Pas d'exhaustivité vérifiée par le compilateur
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Exceptions héritant de Exception"
    <?php
    class ErreurFichier extends RuntimeException {
        public function __construct(
            string $message,
            private string $chemin,
            int $code = 0
        ) {
            parent::__construct($message, $code);
        }

        public function getChemin(): string { return $this->chemin; }
    }

    class ErreurHTTP extends RuntimeException {
        public function __construct(
            private int $statusCode,
            string $message
        ) {
            parent::__construct($message);
        }
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - Exceptions personnalisées"
    class ErreurFichier(Exception):
        def __init__(self, message: str, chemin: str):
            super().__init__(message)
            self.chemin = chemin

    class ErreurHTTP(Exception):
        def __init__(self, code: int, message: str):
            super().__init__(message)
            self.code = code
    ```

<br>

---

## Fonctions qui Lancent des Erreurs : `throws`

```swift title="Swift - Déclarer une fonction faillible avec throws"
import Foundation

// throws : annonce que cette fonction peut lancer une erreur
func lireFichier(à chemin: String) throws -> String {
    // guard + throw : valider et lever une erreur si la condition échoue
    guard !chemin.isEmpty else {
        throw ErreurFichier.fichierIntrouvable(chemin: chemin)
    }

    // Simulation — en production : FileManager
    guard chemin.hasSuffix(".txt") else {
        throw ErreurFichier.fichierCorrompu(détail: "Format non supporté")
    }

    return "Contenu du fichier \(chemin)"
}

func chargerDonnéesAPI(url: String) throws -> Data {
    guard !url.isEmpty else {
        throw ErreurRéseau.httpErreur(code: 400, message: "URL vide")
    }

    // Simulation d'une erreur réseau
    throw ErreurRéseau.timeout(durée: 30)
}
```

<br>

---

## Appeler une Fonction Faillible : `do/catch`

=== ":simple-swift: Swift"

    ```swift title="Swift - do/catch pour capturer les erreurs"
    // try DOIT précéder tout appel à une fonction throws
    // do/catch englobe le code qui peut lancer une erreur

    do {
        let contenu = try lireFichier(à: "rapport.txt")
        print("Contenu : \(contenu)")
        // Si lireFichier lance une erreur, on saute directement au catch
    } catch ErreurFichier.fichierIntrouvable(let chemin) {
        print("Fichier introuvable : \(chemin)")
    } catch ErreurFichier.fichierCorrompu(let détail) {
        print("Fichier corrompu : \(détail)")
    } catch ErreurFichier.permissionsInsuffisantes {
        print("Permissions insuffisantes")
    } catch {
        // catch sans pattern : capture toutes les erreurs restantes
        // error est automatiquement disponible comme constante
        print("Erreur inattendue : \(error.localizedDescription)")
    }

    // Capturer plusieurs types d'erreur
    do {
        let contenu = try lireFichier(à: "config.txt")
        let données = try chargerDonnéesAPI(url: "https://api.example.com")
        print("Tout chargé : \(contenu)")
    } catch let e as ErreurFichier {
        print("Problème fichier : \(e)")
    } catch let e as ErreurRéseau {
        print("Problème réseau : \(e.localizedDescription)")
    } catch {
        print("Erreur : \(error)")
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - try/catch (synchrone)"
    function lireFichier(chemin) {
        if (!chemin) throw new ErreurFichier("Fichier introuvable", chemin);
        return `Contenu de ${chemin}`;
    }

    try {
        const contenu = lireFichier("rapport.txt");
        console.log(contenu);
    } catch (error) {
        // JavaScript : un seul catch, on teste le type manuellement
        if (error instanceof ErreurFichier) {
            console.log(`Fichier : ${error.message}`);
        } else if (error instanceof ErreurHTTP) {
            console.log(`HTTP ${error.code}`);
        } else {
            console.log(`Erreur : ${error.message}`);
        }
    } finally {
        // Toujours exécuté — Swift a defer (différent mais similaire)
        console.log("Nettoyage");
    }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - try/catch/finally"
    <?php
    function lireFichier(string $chemin): string {
        if (empty($chemin)) {
            throw new ErreurFichier("Fichier introuvable", $chemin);
        }
        return "Contenu de $chemin";
    }

    try {
        $contenu = lireFichier("rapport.txt");
        echo $contenu;
    } catch (ErreurFichier $e) {
        echo "Fichier : " . $e->getMessage();
    } catch (RuntimeException $e) {
        echo "Runtime : " . $e->getMessage();
    } catch (Throwable $e) {
        echo "Erreur : " . $e->getMessage();
    } finally {
        echo "Nettoyage";
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - try/except/finally"
    def lire_fichier(chemin: str) -> str:
        if not chemin:
            raise ErreurFichier("Fichier introuvable", chemin)
        return f"Contenu de {chemin}"

    try:
        contenu = lire_fichier("rapport.txt")
        print(contenu)
    except ErreurFichier as e:
        print(f"Fichier : {e}")
    except ErreurHTTP as e:
        print(f"HTTP {e.code}")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        print("Nettoyage")
    ```

<br>

---

## `try?` et `try!`

```swift title="Swift - try? et try! pour les cas simples"
// try? : convertit l'erreur en nil — retourne un Optional
// La fonction throws devient une fonction qui retourne Optional<T>
let contenu = try? lireFichier(à: "rapport.txt")
// Si succès : Optional("Contenu...")
// Si erreur : nil (l'erreur est silencieusement ignorée)

if let texte = contenu {
    print(texte)
} else {
    print("Chargement échoué")
}

// Utile avec ?? pour une valeur par défaut
let texte = (try? lireFichier(à: "config.txt")) ?? "Configuration par défaut"

// try! : force le succès — crash si l'erreur est lancée
// Comme le ! des Optionals : à utiliser UNIQUEMENT si vous êtes certain
let contenuObligatoire = try! lireFichier(à: "ressource_critique.txt")
// Si lireFichier lance une erreur : Fatal error — crash immédiat
```

<br>

---

## Le Type `Result<Success, Failure>`

`Result` est une alternative aux fonctions `throws` — utile pour les APIs asynchrones et pour passer des résultats comme valeurs.

```swift title="Swift - Result<Success, Failure> en pratique"
// Result<T, E> : soit .success(T), soit .failure(E)
// Rappel du module 08 : c'est un enum avec associated values

func validerEmail(_ email: String) -> Result<String, ErreurValidation> {
    guard !email.isEmpty else {
        return .failure(.champManquant("email"))
    }
    guard email.contains("@") else {
        return .failure(.formatInvalide("email", valeur: email))
    }
    return .success(email.lowercased())
}

// Traitement du Result
let résultat = validerEmail("Alice@Example.COM")
switch résultat {
case .success(let emailValidé):
    print("Email validé : \(emailValidé)")   // "alice@example.com"
case .failure(let erreur):
    print("Erreur : \(erreur)")
}

// Transformer un Result avec map et flatMap
let emailMajuscules = résultat.map { $0.uppercased() }
// .success("ALICE@EXAMPLE.COM")

// get() : extrait la valeur ou lance l'erreur (convertit Result → throws)
do {
    let email = try résultat.get()
    print(email)
} catch {
    print(error)
}
```

<br>

---

## `defer` — Nettoyage Garanti

`defer` exécute un bloc de code à la **sortie du scope courant**, quelle que soit la raison de cette sortie — succès, erreur, ou `return` anticipé.

```swift title="Swift - defer pour le nettoyage garanti des ressources"
func traiterFichier(chemin: String) throws {
    print("Ouverture du fichier")
    // defer s'exécute TOUJOURS à la sortie de la fonction
    // Même si une erreur est lancée, même si on fait return
    defer {
        print("Fermeture du fichier (toujours exécuté)")
    }

    let contenu = try lireFichier(à: chemin)
    print("Traitement : \(contenu)")
    // La fermeture se fait ici, après le return implicite
}

// Plusieurs defer s'exécutent dans l'ordre inverse (LIFO)
func exemple() {
    defer { print("3 - Dernier defer") }
    defer { print("2 - Deuxième defer") }
    defer { print("1 - Premier defer") }
    print("Corps de la fonction")
}
// Affiche :
// Corps de la fonction
// 1 - Premier defer
// 2 - Deuxième defer
// 3 - Dernier defer
```

*`defer` est l'équivalent Swift du `finally` de PHP, JavaScript et Python — mais plus flexible car il peut être placé n'importe où dans la fonction.*

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `throws` dans la signature d'une fonction annonce qu'elle peut échouer. `try` est obligatoire devant chaque appel à une fonction `throws`. `do/catch` traite les erreurs avec une granularité précise par type. `try?` transforme l'erreur en `nil` — pratique quand l'échec est acceptable. `try!` force le succès et crashe en cas d'erreur — à utiliser avec une certitude absolue. `Result<T, E>` modélise explicitement le succès ou l'échec comme une valeur. `defer` garantit l'exécution du nettoyage quelle que soit la sortie du scope.

> Dans le module suivant, nous aborderons la **Concurrence Moderne** — `async/await`, `Task` et `Actor` — la façon dont Swift gère les opérations asynchrones sans callbacks imbriqués.

<br>