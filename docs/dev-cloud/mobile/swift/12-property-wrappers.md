---
description: "Property Wrappers Swift : @propertyWrapper, implémentation, wrappedValue, projectedValue et lien avec SwiftUI."
icon: lucide/book-open-check
tags: ["SWIFT", "PROPERTY-WRAPPER", "SWIFTUI", "STATE", "BINDING", "PUBLISHED"]
---

# Property Wrappers

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - L'Emballage Intelligent"
    Imaginez un journal intime avec une serrure. Le contenu du journal, c'est la valeur que vous stockez. La serrure est un comportement supplémentaire qui s'exécute chaque fois que vous ouvrez ou fermez le journal : elle enregistre l'heure d'accès, notifie votre gardien, valide votre empreinte digitale.

    Un **Property Wrapper**, c'est cette serrure. Il enveloppe une propriété et intercept chaque lecture (`get`) et chaque écriture (`set`) pour y ajouter un comportement personnalisé — sans que l'utilisateur de la propriété n'ait besoin de savoir que ce comportement existe.

    Voici pourquoi comprendre `@propertyWrapper` est indispensable avant SwiftUI : **`@State`, `@Binding`, `@Published`, `@ObservedObject`, `@EnvironmentObject` sont tous des Property Wrappers**. Quand vous écrivez `@State var compteur = 0`, vous utilisez un wrapper que Apple a construit avec exactement cette mécanique.

<br>

---

## Le Problème que les Property Wrappers Résolvent

```swift title="Swift - Sans Property Wrapper : répétition de la logique"
// Supposons que vous voulez garantir qu'un prénom n'est jamais vide
// et toujours en majuscule initiale

class FormulaireSansWrapper {
    // Propriété privée de stockage
    private var _prenom: String = ""

    // Propriété publique avec logique
    var prenom: String {
        get { _prenom }
        set {
            let valeur = newValue.trimmingCharacters(in: .whitespaces)
            _prenom = valeur.isEmpty ? "Anonyme" : valeur.capitalized
        }
    }

    private var _nom: String = ""
    var nom: String {
        get { _nom }
        set {
            let valeur = newValue.trimmingCharacters(in: .whitespaces)
            _nom = valeur.isEmpty ? "Anonyme" : valeur.capitalized
        }
    }
    // La même logique répétée pour chaque propriété — pas maintenable
}
```

Avec un Property Wrapper, cette logique s'écrit une seule fois et se réutilise.

<br>

---

## Créer un Property Wrapper

Un Property Wrapper est une struct (ou class) annotée `@propertyWrapper` avec une propriété obligatoire `wrappedValue`.

=== ":simple-swift: Swift"

    ```swift title="Swift - Property Wrapper minimal"
    @propertyWrapper
    struct NomFormaté {
        // wrappedValue : la propriété qui stocke la valeur réelle
        private var valeurStockée: String = "Anonyme"

        var wrappedValue: String {
            get { valeurStockée }
            set {
                let nettoyé = newValue.trimmingCharacters(in: .whitespaces)
                valeurStockée = nettoyé.isEmpty ? "Anonyme" : nettoyé.capitalized
            }
        }

        // Initialiseur : peut accepter des paramètres de configuration
        init(wrappedValue: String) {
            self.wrappedValue = wrappedValue   // Utilise le setter pour valider
        }

        init() {}   // Valeur par défaut "Anonyme"
    }

    // Utilisation avec l'annotation @
    struct Formulaire {
        @NomFormaté var prenom: String
        @NomFormaté var nom: String = "martin"   // Initialisé avec une valeur
    }

    var f = Formulaire(prenom: "  alice  ")
    print(f.prenom)   // "Alice" — espaces supprimés, majuscule
    print(f.nom)      // "Martin" — capitalized

    f.prenom = ""
    print(f.prenom)   // "Anonyme" — valeur par défaut si vide

    // La logique est encapsulée une fois — pas répétée pour chaque propriété
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Décorateurs (proposition TC39, TypeScript)"
    // JavaScript n'a pas de property wrappers natifs
    // TypeScript : décorateurs de propriétés (similaires mais différents)

    // function NomFormaté(target: any, key: string) {
    //     let valeur = target[key];
    //     Object.defineProperty(target, key, {
    //         get: () => valeur,
    //         set: (v: string) => {
    //             const nettoyé = v.trim();
    //             valeur = nettoyé ? nettoyé.charAt(0).toUpperCase() + nettoyé.slice(1) : "Anonyme";
    //         }
    //     });
    // }

    // Ou avec des getters/setters explicites
    class Formulaire {
        #prenom = "Anonyme";
        get prenom() { return this.#prenom; }
        set prenom(v) {
            const nettoyé = v.trim();
            this.#prenom = nettoyé ? nettoyé[0].toUpperCase() + nettoyé.slice(1) : "Anonyme";
        }
    }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Pas d'équivalent natif (magic methods)"
    <?php
    // PHP : __get et __set permettent d'intercepter les accès aux propriétés
    // Pas aussi expressif ou typé que les property wrappers Swift

    class Formulaire {
        private array $données = [];

        public function __set(string $nom, mixed $valeur): void {
            $nettoyé = trim((string) $valeur);
            $this->données[$nom] = $nettoyé === "" ? "Anonyme" : ucfirst($nettoyé);
        }

        public function __get(string $nom): mixed {
            return $this->données[$nom] ?? "Anonyme";
        }
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - Descripteurs (équivalent conceptuel)"
    # Python : descripteurs via __get__/__set__ (proche des property wrappers)

    class NomFormaté:
        def __set_name__(self, owner, name):
            self.name = f"_{name}"

        def __get__(self, obj, type=None):
            return getattr(obj, self.name, "Anonyme")

        def __set__(self, obj, value: str):
            nettoyé = value.strip()
            setattr(obj, self.name, nettoyé.capitalize() if nettoyé else "Anonyme")

    class Formulaire:
        prenom = NomFormaté()
        nom = NomFormaté()

    f = Formulaire()
    f.prenom = "  alice  "
    print(f.prenom)   # "Alice"
    ```

<br>

---

## La `projectedValue` — Le `$`

Un Property Wrapper peut exposer une **valeur projetée** accessible via le préfixe `$`. C'est exactement ce que vous utilisez dans SwiftUI avec `$nomVariable`.

```swift title="Swift - projectedValue : accéder à des informations sur le wrapper"
@propertyWrapper
struct Validé {
    private var valeur: String = ""
    // La valeur projetée : métadonnée sur l'état du wrapper
    private(set) var projectedValue: Bool = false   // estValide

    var wrappedValue: String {
        get { valeur }
        set {
            valeur = newValue
            // Met à jour la valeur projetée automatiquement
            projectedValue = newValue.count >= 3
        }
    }

    init(wrappedValue: String) {
        self.wrappedValue = wrappedValue
    }
}

struct Formulaire {
    @Validé var prenom: String = ""
}

var f = Formulaire()

f.prenom = "Al"
print(f.prenom)    // "Al"
print(f.$prenom)   // false — moins de 3 caractères, invalide

f.prenom = "Alice"
print(f.prenom)    // "Alice"
print(f.$prenom)   // true — valide

// En SwiftUI :
// @State var compteur = 0
// $compteur → Binding<Int> exposé comme projectedValue
// TextField("Nom", text: $nom)  ← utilise la projectedValue
```

<br>

---

## Les Wrappers Paramétrables

Un wrapper peut accepter des paramètres de configuration.

```swift title="Swift - Wrapper paramétrable"
@propertyWrapper
struct Clampé {
    private var valeur: Double
    let minimum: Double
    let maximum: Double

    var wrappedValue: Double {
        get { valeur }
        set { valeur = max(minimum, min(maximum, newValue)) }
    }

    init(wrappedValue: Double, minimum: Double, maximum: Double) {
        self.minimum = minimum
        self.maximum = maximum
        self.valeur = max(minimum, min(maximum, wrappedValue))
    }
}

struct Paramètres {
    @Clampé(minimum: 0, maximum: 100) var volume: Double = 50
    @Clampé(minimum: 0.5, maximum: 3.0) var vitesseLecture: Double = 1.0
    @Clampé(minimum: 0, maximum: 1) var opacité: Double = 1.0
}

var p = Paramètres()
p.volume = 150   // Impossible de dépasser 100
print(p.volume)  // 100.0

p.volume = -20
print(p.volume)  // 0.0
```

<br>

---

## Comprendre les Wrappers SwiftUI

Maintenant que vous connaissez le mécanisme, voici comment les wrappers SwiftUI fonctionnent conceptuellement.

```swift title="Swift - @State : implémentation conceptuelle simplifiée"
// Ce n'est pas le code exact d'Apple — mais le principe est identique

@propertyWrapper
struct MonState<T> {
    // La valeur est stockée HORS de la struct SwiftUI
    // (dans le graph de rendu de SwiftUI, pas dans la struct elle-même)
    private var valeurInterne: T
    private var notifierChangement: () -> Void = {}

    var wrappedValue: T {
        get { valeurInterne }
        set {
            valeurInterne = newValue
            // Déclenche un nouveau rendu de la vue
            notifierChangement()
        }
    }

    // projectedValue retourne un Binding<T>
    // C'est le $variable que vous passez à un TextField
    var projectedValue: Binding<T> {
        Binding(
            get: { self.wrappedValue },
            set: { self.wrappedValue = $0 }
        )
    }

    init(wrappedValue: T) {
        self.valeurInterne = wrappedValue
    }
}

// En SwiftUI réel :
// struct MaVue: View {
//     @State var compteur = 0
//
//     var body: some View {
//         VStack {
//             Text("\(compteur)")
//             Button("Incrémenter") {
//                 compteur += 1   // Déclenche un re-render via wrappedValue.set
//             }
//             Stepper("Valeur", value: $compteur)  // $compteur = projectedValue (Binding)
//         }
//     }
// }
```

**Résumé des wrappers SwiftUI et leur rôle :**

| Wrapper | Type de source | Usage |
| --- | --- | --- |
| `@State` | Valeur locale à la vue | État interne simple (`Bool`, `Int`, `String`) |
| `@Binding` | Référence vers un `@State` parent | Partager l'état avec une sous-vue |
| `@StateObject` | ViewModel de la vue | Objet observable créé et possédé par la vue |
| `@ObservedObject` | ViewModel externe | Objet observable passé depuis l'extérieur |
| `@EnvironmentObject` | Environnement global | Données partagées dans toute la hiérarchie |
| `@Published` | Propriété d'un `ObservableObject` | Déclenche la mise à jour de la vue |

<br>

---

## Créer un Wrapper Utile en Production

```swift title="Swift - @UserDefault : persistance locale avec UserDefaults"
@propertyWrapper
struct UserDefault<T> {
    let clé: String
    let valeurParDéfaut: T
    private let stockage = UserDefaults.standard

    var wrappedValue: T {
        get {
            // Lit depuis UserDefaults, retourne la valeur par défaut si absent
            stockage.value(forKey: clé) as? T ?? valeurParDéfaut
        }
        set {
            stockage.set(newValue, forKey: clé)
        }
    }
}

// Utilisation : paramètres persistants de l'application
struct Préférences {
    @UserDefault(clé: "theme_sombre", valeurParDéfaut: false)
    static var estEnModeSombre: Bool

    @UserDefault(clé: "taille_police", valeurParDéfaut: 16)
    static var taillePolice: Int

    @UserDefault(clé: "langue_préférée", valeurParDéfaut: "fr")
    static var langue: String
}

// La valeur est automatiquement persistée entre les lancements
Préférences.estEnModeSombre = true
// Redémarrage de l'app...
print(Préférences.estEnModeSombre)  // true — persisté dans UserDefaults
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Wrapper de validation simple**

```swift title="Swift - Exercice 1"
// Créez @propertyWrapper struct PositifOuZéro
// wrappedValue : Double
// Garantit que la valeur ne peut jamais être négative (remplace par 0 si négative)

struct Compte {
    @PositifOuZéro var solde: Double = 0
}

var c = Compte()
c.solde = 100.0
print(c.solde)   // 100.0
c.solde = -50.0
print(c.solde)   // 0.0 — impossible d'être négatif
```

**Exercice 2 — Wrapper avec projectedValue**

```swift title="Swift - Exercice 2"
// Créez @propertyWrapper struct Historique<T>
// wrappedValue : T (valeur courante)
// projectedValue : [T] (historique de toutes les valeurs assignées)

struct Temperature {
    @Historique var celsius: Double = 0
}

var t = Temperature()
t.celsius = 20.0
t.celsius = 22.5
t.celsius = 18.0

print(t.celsius)    // 18.0
print(t.$celsius)   // [0.0, 20.0, 22.5, 18.0]
```

**Exercice 3 — Comprendre @State**

```swift title="Swift - Exercice 3 (conceptuel)"
// Sans écrire de SwiftUI, répondez à ces questions dans des commentaires :
//
// 1. Pourquoi @State doit-il stocker la valeur EN DEHORS de la struct SwiftUI ?
//    (Hint : rappelez-vous la value semantics des structs — module 07)
//
// 2. Pourquoi @State prend wrappedValue non-Optional par défaut,
//    alors que @Binding prend une Binding<T> comme projectedValue ?
//
// 3. Quelle est la différence entre passer $compteur et compteur à une sous-vue ?
//    Dans quel cas la sous-vue peut-elle modifier la valeur ?
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Un **Property Wrapper** est un type annoté `@propertyWrapper` qui encapsule le comportement de lecture (`get`) et d'écriture (`set`) d'une propriété. `wrappedValue` est la propriété obligatoire qui contient la valeur réelle. `projectedValue` expose une métadonnée accessible via `$` — c'est le `$variable` omniprésent dans SwiftUI. Les wrappers SwiftUI (`@State`, `@Binding`, `@Published`) sont tous construits sur ce mécanisme. Créer vos propres wrappers élimine la duplication de logique sur les propriétés.

> Dans le module suivant, nous couvrirons la **Gestion des Erreurs** — `throws`, `do/catch`, `try` et le type `Result<T, E>`.

<br>