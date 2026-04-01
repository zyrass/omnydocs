---
description: "Codable Swift : sérialisation et désérialisation JSON, CodingKeys, types imbriqués, dates et gestion des erreurs de décodage."
icon: lucide/book-open-check
tags: ["SWIFT", "CODABLE", "JSON", "DECODABLE", "ENCODABLE", "APIS"]
---

# Codable — Sérialisation JSON

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Traducteur Universel"
    Imaginez que vos structs Swift parlent une langue — le Swift. Les APIs REST parlent une autre langue — le JSON. `Codable` est le traducteur officiel entre ces deux mondes. Vous lui montrez votre struct une seule fois, et il sait automatiquement comment la convertir vers JSON (encodage) et comment reconstruire une struct depuis du JSON (décodage).

    Avant `Codable` (Swift 4, 2017), cette conversion demandait des dizaines de lignes de code manuel error-prone. Aujourd'hui, une seule ligne suffit dans la majorité des cas.

`Codable` est composé de deux protocols : `Decodable` (JSON → Swift) et `Encodable` (Swift → JSON). La majorité du temps, on utilise `Codable = Decodable & Encodable` pour les deux directions à la fois.

!!! note "Prérequis"
    Ce module s'appuie sur les **Protocols** (module 09) et les **Optionals** (module 06). Les types imbriqués et les erreurs `DecodingError` utilisent les **Enums** (module 08).

<br>

---

## Décodage Basique : JSON → Swift

=== ":simple-swift: Swift"

    ```swift title="Swift - Décoder un objet JSON simple"
    import Foundation

    // 1. Définir la struct avec Codable
    // Swift synthétise automatiquement l'implémentation si toutes les propriétés sont Codable
    struct Utilisateur: Codable {
        let id: Int
        let nom: String
        let email: String
    }

    // 2. Données JSON (en pratique, elles viennent d'URLSession)
    let json = """
    {
        "id": 42,
        "nom": "Alice Martin",
        "email": "alice@example.com"
    }
    """.data(using: .utf8)!

    // 3. Décoder avec JSONDecoder
    let décodeur = JSONDecoder()

    do {
        let utilisateur = try décodeur.decode(Utilisateur.self, from: json)
        print(utilisateur.nom)    // "Alice Martin"
        print(utilisateur.email)  // "alice@example.com"
    } catch {
        print("Erreur de décodage : \(error)")
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - JSON.parse (pas de typage fort)"
    const json = '{"id": 42, "nom": "Alice Martin", "email": "alice@example.com"}';

    // JS : JSON.parse retourne any — pas de vérification de types
    const utilisateur = JSON.parse(json);
    console.log(utilisateur.nom);    // "Alice Martin"
    console.log(utilisateur.email);  // "alice@example.com"

    // Aucune garantie que les champs existent ou ont le bon type
    // TypeScript + Zod ou similaire nécessaire pour la validation
    ```

=== ":simple-php: PHP"

    ```php title="PHP - json_decode"
    <?php
    $json = '{"id": 42, "nom": "Alice Martin", "email": "alice@example.com"}';

    // json_decode avec true → tableau associatif
    $utilisateur = json_decode($json, true);
    echo $utilisateur['nom'];    // "Alice Martin"

    // Pas de typage automatique — validation manuelle nécessaire
    ```

=== ":simple-python: Python"

    ```python title="Python - json.loads et dataclasses"
    import json
    from dataclasses import dataclass

    json_str = '{"id": 42, "nom": "Alice Martin", "email": "alice@example.com"}'

    # json.loads : dict Python, pas de typage automatique
    données = json.loads(json_str)
    print(données["nom"])

    # Avec dacite ou pydantic pour la validation typée (équivalent Codable)
    # from pydantic import BaseModel
    # class Utilisateur(BaseModel):
    #     id: int; nom: str; email: str
    # u = Utilisateur(**données)
    ```

<br>

---

## Encodage Basique : Swift → JSON

```swift title="Swift - Encoder une struct vers JSON"
let utilisateur = Utilisateur(id: 1, nom: "Bob", email: "bob@example.com")

let encodeur = JSONEncoder()
encodeur.outputFormatting = .prettyPrinted   // JSON indenté pour la lisibilité

do {
    let données = try encodeur.encode(utilisateur)
    let jsonString = String(data: données, encoding: .utf8)!
    print(jsonString)
    // {
    //   "id" : 1,
    //   "nom" : "Bob",
    //   "email" : "bob@example.com"
    // }
} catch {
    print("Erreur d'encodage : \(error)")
}
```

<br>

---

## `CodingKeys` — Mapper les Noms JSON vers Swift

Les APIs REST utilisent souvent `snake_case` (`user_name`, `created_at`) alors que Swift utilise `camelCase` (`userName`, `createdAt`). `CodingKeys` mappe les deux.

=== ":simple-swift: Swift"

    ```swift title="Swift - CodingKeys pour le mapping snake_case ↔ camelCase"
    struct Article: Codable {
        let id: Int
        let titre: String
        let contenu: String
        let datePublication: Date
        let nombreVues: Int

        // CodingKeys : enum qui mappe les noms JSON aux noms Swift
        enum CodingKeys: String, CodingKey {
            case id
            case titre            // Identique dans JSON et Swift
            case contenu          // Identique
            case datePublication  = "date_publication"  // JSON: snake_case
            case nombreVues       = "nombre_vues"       // JSON: snake_case
        }
    }

    // Alternative : demander à JSONDecoder de convertir automatiquement
    let décodeur = JSONDecoder()
    décodeur.keyDecodingStrategy = .convertFromSnakeCase
    // Plus besoin de CodingKeys pour le snake_case standard

    let json = """
    {
        "id": 1,
        "titre": "Introduction à Swift",
        "contenu": "Swift est un langage...",
        "date_publication": 0,
        "nombre_vues": 1250
    }
    """.data(using: .utf8)!
    ```

    ```swift title="Swift - keyDecodingStrategy : la solution automatique"
    struct ArticleAuto: Codable {
        let id: Int
        let titre: String
        let datePublication: Date   // Mappé automatiquement depuis "date_publication"
        let nombreVues: Int         // Mappé depuis "nombre_vues"
    }

    let décodeur = JSONDecoder()
    // Convertit automatiquement snake_case → camelCase
    décodeur.keyDecodingStrategy = .convertFromSnakeCase
    // Interprète les timestamps Unix comme des dates
    décodeur.dateDecodingStrategy = .secondsSince1970
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Mapping manuel ou bibliothèque"
    // JS : mapping manuel ou via une bibliothèque comme class-transformer
    const json = { id: 1, date_publication: 1234567890, nombre_vues: 1250 };

    // Mapping manuel
    const article = {
        id: json.id,
        datePublication: new Date(json.date_publication * 1000),
        nombreVues: json.nombre_vues
    };
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Mapping via classe ou bibliothèque"
    <?php
    $json = ['id' => 1, 'date_publication' => 1234567890, 'nombre_vues' => 1250];

    class Article {
        public function __construct(
            public int $id,
            public \DateTime $datePublication,
            public int $nombreVues
        ) {}

        public static function fromArray(array $data): self {
            return new self(
                id: $data['id'],
                datePublication: new \DateTime("@{$data['date_publication']}"),
                nombreVues: $data['nombre_vues']
            );
        }
    }
    ```

<br>

---

## Types Imbriqués et Tableaux

```swift title="Swift - Décoder des structures JSON complexes"
// JSON imbriqué typique d'une API REST
let jsonComplexe = """
{
    "status": "success",
    "data": {
        "utilisateurs": [
            {"id": 1, "nom": "Alice", "actif": true},
            {"id": 2, "nom": "Bob",   "actif": false}
        ],
        "total": 2
    }
}
""".data(using: .utf8)!

// Modèle Swift qui reflète la structure JSON
struct RéponseAPI: Codable {
    let status: String
    let data: Payload

    struct Payload: Codable {
        let utilisateurs: [UtilisateurSimple]
        let total: Int

        struct UtilisateurSimple: Codable {
            let id: Int
            let nom: String
            let actif: Bool
        }
    }
}

let décodeur = JSONDecoder()
do {
    let réponse = try décodeur.decode(RéponseAPI.self, from: jsonComplexe)
    print(réponse.status)                          // "success"
    print(réponse.data.total)                      // 2
    print(réponse.data.utilisateurs[0].nom)        // "Alice"

    let actifs = réponse.data.utilisateurs.filter { $0.actif }
    print(actifs.count)   // 1
} catch {
    print("Erreur : \(error)")
}
```

<br>

---

## Propriétés Optionnelles dans le JSON

```swift title="Swift - Gérer les champs absents ou null avec Optional"
struct Profil: Codable {
    let id: Int
    let nom: String
    let biographie: String?    // Peut être absent du JSON ou null
    let siteWeb: URL?          // Peut être null
    let âge: Int?
}

// JSON avec certains champs absents
let json1 = """{"id": 1, "nom": "Alice"}""".data(using: .utf8)!
let json2 = """{"id": 2, "nom": "Bob", "biographie": null, "age": 28}""".data(using: .utf8)!

let décodeur = JSONDecoder()
// Comportement par défaut :
// - Champ absent du JSON → propriété Optional = nil ✓
// - Champ présent avec valeur null → propriété Optional = nil ✓
// - Champ absent pour une propriété non-Optional → DecodingError.keyNotFound ✗

if let p1 = try? décodeur.decode(Profil.self, from: json1) {
    print(p1.biographie ?? "Aucune bio")   // "Aucune bio"
}
```

<br>

---

## Gestion des Erreurs de Décodage

```swift title="Swift - Diagnostiquer précisément les erreurs Codable"
let jsonMalformé = """
{
    "id": "quarante-deux",
    "nom": "Alice"
}
""".data(using: .utf8)!

struct Test: Codable {
    let id: Int
    let nom: String
}

do {
    let résultat = try JSONDecoder().decode(Test.self, from: jsonMalformé)
    print(résultat)
} catch let DecodingError.typeMismatch(type, context) {
    // Type attendu vs type reçu
    print("Type incorrect : attendu \(type)")
    print("Chemin : \(context.codingPath.map { $0.stringValue })")
    // "Chemin : ["id"]"
} catch let DecodingError.keyNotFound(clé, context) {
    // Clé requise absente du JSON
    print("Clé manquante : \(clé.stringValue)")
} catch let DecodingError.valueNotFound(type, context) {
    // Valeur null pour une propriété non-Optional
    print("Valeur null inattendue pour type \(type)")
} catch let DecodingError.dataCorrupted(context) {
    // JSON invalide syntaxiquement
    print("JSON invalide : \(context.debugDescription)")
} catch {
    print("Erreur inattendue : \(error)")
}
```

<br>

---

## Codable avec URLSession — Le Pattern Complet

Voici le pattern production complet pour consommer une API REST en Swift.

```swift title="Swift - Requête réseau complète avec Codable et async/await"
import Foundation

// 1. Les modèles de données
struct Post: Codable, Identifiable {
    let id: Int
    let userId: Int
    let title: String
    let body: String
}

// 2. La couche réseau
enum ErreurAPI: Error {
    case urlInvalide
    case réponseInvalide(Int)
    case décodageÉchoué(Error)
}

func chargerPosts() async throws -> [Post] {
    // Construction de l'URL
    guard let url = URL(string: "https://jsonplaceholder.typicode.com/posts") else {
        throw ErreurAPI.urlInvalide
    }

    // Requête réseau asynchrone (module 14 — Concurrence)
    let (données, réponse) = try await URLSession.shared.data(from: url)

    // Vérification du status HTTP
    guard let http = réponse as? HTTPURLResponse,
          (200...299).contains(http.statusCode) else {
        let code = (réponse as? HTTPURLResponse)?.statusCode ?? 0
        throw ErreurAPI.réponseInvalide(code)
    }

    // Décodage
    let décodeur = JSONDecoder()
    décodeur.keyDecodingStrategy = .convertFromSnakeCase

    do {
        return try décodeur.decode([Post].self, from: données)
    } catch {
        throw ErreurAPI.décodageÉchoué(error)
    }
}

// 3. Appel depuis un contexte async
Task {
    do {
        let posts = try await chargerPosts()
        print("Chargé \(posts.count) posts")
        print(posts.first?.title ?? "")
    } catch ErreurAPI.urlInvalide {
        print("URL invalide")
    } catch ErreurAPI.réponseInvalide(let code) {
        print("Erreur HTTP \(code)")
    } catch ErreurAPI.décodageÉchoué(let erreur) {
        print("Décodage échoué : \(erreur)")
    }
}
```

<br>

---

## Encodage Personnalisé avec `init(from:)` et `encode(to:)`

Pour les cas complexes où la synthèse automatique ne suffit pas.

```swift title="Swift - Implémentation personnalisée de Codable"
// JSON reçu :
// { "type": "cercle", "valeur": 5.0 }
// { "type": "rectangle", "largeur": 4.0, "hauteur": 6.0 }

enum Forme: Codable {
    case cercle(rayon: Double)
    case rectangle(largeur: Double, hauteur: Double)

    enum CodingKeys: String, CodingKey {
        case type, valeur, largeur, hauteur
    }

    init(from décodeur: Decoder) throws {
        let conteneur = try décodeur.container(keyedBy: CodingKeys.self)
        let type = try conteneur.decode(String.self, forKey: .type)

        switch type {
        case "cercle":
            let rayon = try conteneur.decode(Double.self, forKey: .valeur)
            self = .cercle(rayon: rayon)
        case "rectangle":
            let l = try conteneur.decode(Double.self, forKey: .largeur)
            let h = try conteneur.decode(Double.self, forKey: .hauteur)
            self = .rectangle(largeur: l, hauteur: h)
        default:
            throw DecodingError.dataCorruptedError(
                forKey: .type,
                in: conteneur,
                debugDescription: "Type '\(type)' inconnu"
            )
        }
    }

    func encode(to encodeur: Encoder) throws {
        var conteneur = encodeur.container(keyedBy: CodingKeys.self)

        switch self {
        case .cercle(let rayon):
            try conteneur.encode("cercle", forKey: .type)
            try conteneur.encode(rayon, forKey: .valeur)
        case .rectangle(let l, let h):
            try conteneur.encode("rectangle", forKey: .type)
            try conteneur.encode(l, forKey: .largeur)
            try conteneur.encode(h, forKey: .hauteur)
        }
    }
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"
    Utilisez l'API publique [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com) pour les exercices réseau.

**Exercice 1 — Décoder un objet simple**

```swift title="Swift - Exercice 1"
// Décodez ce JSON dans une struct Swift appropriée
let json = """
{
    "userId": 1,
    "id": 1,
    "title": "Learning Swift",
    "completed": false
}
""".data(using: .utf8)!

// 1. Créez la struct Todo: Codable avec les bons types
// 2. Décodez le JSON avec JSONDecoder
// 3. Affichez le titre
// 4. Que se passe-t-il si vous changez "completed" en Int dans la struct ?
```

**Exercice 2 — CodingKeys**

```swift title="Swift - Exercice 2"
// Cette API retourne du snake_case. Décodez sans keyDecodingStrategy
// (utilisez CodingKeys manuellement)

let json = """
{
    "first_name": "Alice",
    "last_name": "Martin",
    "birth_year": 1995,
    "is_active": true
}
""".data(using: .utf8)!

// Créez struct Personne: Codable avec :
// firstName, lastName, birthYear, isActive (camelCase Swift)
// + CodingKeys qui mappe snake_case → camelCase
```

**Exercice 3 — Tableau imbriqué**

```swift title="Swift - Exercice 3"
// Décodez cette réponse d'API complète
let json = """
{
    "page": 1,
    "per_page": 6,
    "total": 12,
    "data": [
        {"id": 1, "email": "george.bluth@reqres.in", "first_name": "George"},
        {"id": 2, "email": "janet.weaver@reqres.in", "first_name": "Janet"}
    ]
}
""".data(using: .utf8)!

// Créez les structs nécessaires
// Affichez le nombre total d'utilisateurs et le premier email
```

**Exercice 4 — Valeurs optionnelles**

```swift title="Swift - Exercice 4"
// Décodez les deux JSON suivants avec la MÊME struct
// La struct doit gérer gracieusement les champs absents

let json1 = """{"id": 1, "name": "Alice", "company": "OmnyVia"}""".data(using: .utf8)!
let json2 = """{"id": 2, "name": "Bob"}""".data(using: .utf8)!

// struct Utilisateur: Codable { ... }
// Les deux doivent décoder sans erreur
// Pour json2 : company doit valoir nil
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `Codable` = `Decodable & Encodable`. Swift synthétise l'implémentation automatiquement si toutes les propriétés sont Codable. `JSONDecoder` avec `keyDecodingStrategy = .convertFromSnakeCase` gère le mapping snake_case automatiquement. `CodingKeys` permet un mapping explicite et personnalisé. Les propriétés `Optional` gèrent les champs absents ou null dans le JSON. `DecodingError` fournit des messages d'erreur précis avec le chemin de la propriété problématique. Le pattern complet en production combine `URLSession`, `async/await` et `JSONDecoder`.

> Dans le module suivant, nous aborderons les **Generics** — le mécanisme qui permet d'écrire du code paramétrique fonctionnant avec n'importe quel type tout en restant statiquement typé.

<br>