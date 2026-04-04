---
description: "TypeScript 01 — Fondamentaux : types de base, interfaces, alias, fonctions typées, classes et enums."
icon: lucide/book-open-check
tags: ["TYPESCRIPT", "TYPES", "INTERFACES", "CLASSES", "ENUMS", "FONCTIONS"]
---

# Module 01 — Fondamentaux TypeScript

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="TypeScript 5.x"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Formulaire Administatif"
    En France, certains formulaires officiels refusent d'être soumis si un champ obligatoire est vide ou mal rempli. TypeScript fonctionne de la même façon avec votre code : il refuse de "compiler" (laisser passer) si une fonction reçoit un `string` là où elle attend un `number`, ou si un objet n'a pas la propriété requise. Vous corrigez les erreurs **avant** de déployer, pas après.

<br>

---

## 1. Configuration Initiale

```bash title="Bash — Initialiser TypeScript dans un projet"
# Installer TypeScript (en dépendance de développement)
npm install --save-dev typescript ts-node @types/node

# Générer le fichier tsconfig.json
npx tsc --init
```

```json title="JSON — tsconfig.json : configuration TypeScript recommandée"
{
  "compilerOptions": {
    "target":            "ES2022",         // Version JS cible
    "module":            "CommonJS",       // Système de modules (NodeJS)
    "lib":               ["ES2022"],       // Bibliothèques typées
    "rootDir":           "./src",          // Dossier source
    "outDir":            "./dist",         // Dossier de sortie (JS compilé)
    "strict":            true,             // Mode strict (OBLIGATOIRE !)
    "noImplicitAny":     true,             // Interdit les 'any' implicites
    "strictNullChecks":  true,             // null/undefined traités séparément
    "esModuleInterop":   true,             // Import modules CommonJS
    "skipLibCheck":      true,             // Ignorer les erreurs dans .d.ts
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

```bash title="Bash — Compiler et exécuter TypeScript"
# Compiler (génère les fichiers .js dans dist/)
npx tsc

# Mode watch (recompile à chaque modification)
npx tsc --watch

# Exécuter directement (sans compilation préalable)
npx ts-node src/index.ts
```

<br>

---

## 2. Types de Base

```typescript title="TypeScript — Types primitifs et annotations"
// ─── Primitifs ────────────────────────────────────────────────────────────────
let name:    string  = "Alice";
let age:     number  = 30;
let isAdmin: boolean = true;
let score:   null    = null;           // Seulement null
let input:   undefined = undefined;   // Seulement undefined

// ─── Inférence de type (TypeScript devine le type) ───────────────────────────
let city    = "Paris";    // TypeScript infère : string
let count   = 42;          // TypeScript infère : number
let active  = false;       // TypeScript infère : boolean
// city = 42; // ❌ Erreur : Type 'number' is not assignable to type 'string'

// ─── Tableaux ─────────────────────────────────────────────────────────────────
let fruits:    string[]       = ["apple", "banana", "orange"];
let scores:    number[]       = [95, 87, 92];
let mixed:     Array<string>  = ["hello", "world"];    // Syntaxe générique (équivalent)

// ─── Tuple (tableau de taille et types fixes) ─────────────────────────────────
let coordinate: [number, number]      = [48.8566, 2.3522];  // [lat, lng]
let person:     [string, number, boolean] = ["Alice", 30, true];

// ─── Union Type (OU) ──────────────────────────────────────────────────────────
let id:     string | number = "ABC-123";
id = 42;           // ✅ number aussi accepté

let status: "active" | "inactive" | "pending" = "active";
// status = "banned"; // ❌ Erreur : littéral non autorisé

// ─── Any (dangereux — à éviter) ───────────────────────────────────────────────
let userInput: any = "Hello";
userInput = 42;    // Accepte tout — désactive la vérification de type

// ─── Unknown (any sécurisé) ───────────────────────────────────────────────────
let mysteryValue: unknown = "maybe a string";
// mysteryValue.toUpperCase(); // ❌ Erreur sans vérification de type

if (typeof mysteryValue === "string") {
    console.log(mysteryValue.toUpperCase()); // ✅ TypeScript est sûr ici
}

// ─── Never (code inaccessible) ────────────────────────────────────────────────
function throwError(message: string): never {
    throw new Error(message);  // Ne retourne jamais
}
```

<br>

---

## 3. Interfaces & Type Aliases

```typescript title="TypeScript — Interfaces : définir la forme d'un objet"
// ─── Interface ────────────────────────────────────────────────────────────────
interface User {
    readonly id:   number;       // readonly : ne peut pas être modifié après création
    name:          string;
    email:         string;
    age?:          number;        // ? : propriété optionnelle
    role:          "admin" | "user" | "moderator";
}

const alice: User = {
    id:    1,
    name:  "Alice Dupont",
    email: "alice@example.com",
    role:  "admin",
};
// alice.id = 2; // ❌ Erreur : Cannot assign to 'id' because it is a read-only property.

// ─── Extension d'interface ────────────────────────────────────────────────────
interface AdminUser extends User {
    permissions: string[];
    lastLogin:   Date;
}

const admin: AdminUser = {
    id:          1,
    name:        "Bob Admin",
    email:       "bob@example.com",
    role:        "admin",
    permissions: ["read", "write", "delete"],
    lastLogin:   new Date(),
};

// ─── Interfaces avec méthodes ─────────────────────────────────────────────────
interface Repository<T> {
    findById(id: number): Promise<T | null>;
    findAll():            Promise<T[]>;
    create(data: Partial<T>): Promise<T>;
    update(id: number, data: Partial<T>): Promise<T>;
    delete(id: number): Promise<void>;
}
```

```typescript title="TypeScript — Type Aliases : nommer des types complexes"
// ─── Type Alias ───────────────────────────────────────────────────────────────
type ID          = string | number;
type Nullable<T> = T | null;
type Callback    = (error: Error | null, result: string) => void;

// ─── Object type ──────────────────────────────────────────────────────────────
type Point = {
    x: number;
    y: number;
    label?: string;
};

// ─── Interface vs Type ────────────────────────────────────────────────────────
// Règle : interface pour les objets extensibles, type pour les unions/unions complexes

// Interface → extensible avec extends
interface Animal {
    name: string;
}
interface Dog extends Animal {
    breed: string;
}

// Type → union
type StringOrNumber     = string | number;
type HttpMethod         = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
type ApiResponse<T>     = { data: T; status: number; message: string; };
```

<br>

---

## 4. Fonctions Typées

```typescript title="TypeScript — Typer les paramètres, retours et surcharges"
// ─── Fonctions de base ────────────────────────────────────────────────────────
function greet(name: string): string {
    return `Bonjour, ${name} !`;
}

// ─── Paramètres optionnels et par défaut ──────────────────────────────────────
function createUser(
    name:  string,
    role:  "admin" | "user" = "user",   // Valeur par défaut
    email?: string                       // Paramètre optionnel
): User {
    return { id: Date.now(), name, role, email: email ?? `${name}@domain.com` };
}

// ─── Arrow functions ──────────────────────────────────────────────────────────
const add = (a: number, b: number): number => a + b;

const fetchData = async (url: string): Promise<Response> => {
    return await fetch(url);
};

// ─── Rest parameters ──────────────────────────────────────────────────────────
function sumAll(...numbers: number[]): number {
    return numbers.reduce((acc, n) => acc + n, 0);
}
console.log(sumAll(1, 2, 3, 4, 5)); // 15

// ─── Types de fonction ────────────────────────────────────────────────────────
type Comparator<T> = (a: T, b: T) => number;

const compareNumbers: Comparator<number> = (a, b) => a - b;
const compareStrings: Comparator<string> = (a, b) => a.localeCompare(b);

// ─── Surcharge de fonctions (overloads) ───────────────────────────────────────
function format(value: string): string;
function format(value: number): string;
function format(value: string | number): string {
    if (typeof value === "number") {
        return value.toFixed(2);
    }
    return value.trim();
}
```

<br>

---

## 5. Classes TypeScript

```typescript title="TypeScript — Classes avec modificateurs d'accès et generics"
class UserService {
    // Modificateurs d'accès
    public    name:     string;     // Accessible partout (défaut)
    private   password: string;     // Seulement dans la classe
    protected role:     string;     // Classe + enfants
    readonly  createdAt: Date;      // Lecture seule

    // Paramètre constructor shorthand (crée et assigne automatiquement)
    constructor(
        public readonly id: number,
        private email: string,
        name: string
    ) {
        this.name      = name;
        this.password  = "";
        this.role      = "user";
        this.createdAt = new Date();
    }

    // Getters & Setters
    get emailAddress(): string {
        return this.email;
    }

    set emailAddress(value: string) {
        if (!value.includes("@")) throw new Error("Email invalide");
        this.email = value;
    }

    // Méthodes publiques
    setPassword(rawPassword: string): void {
        this.password = this.hash(rawPassword);
    }

    // Méthode privée
    private hash(value: string): string {
        return `hashed_${value}`;  // Simplification
    }

    // Méthode statique (appelée sur la classe, pas l'instance)
    static create(email: string, name: string): UserService {
        return new UserService(Date.now(), email, name);
    }
}

// ─── Héritage ─────────────────────────────────────────────────────────────────
class AdminService extends UserService {
    constructor(id: number, email: string, name: string) {
        super(id, email, name);
        this.role = "admin";   // Accessible car protected
    }

    manageUsers(): void {
        console.log(`Admin ${this.name} gère les utilisateurs`);
    }
}

// ─── Implémenter une interface ────────────────────────────────────────────────
interface Serializable {
    toJSON(): object;
    fromJSON(data: object): void;
}

class ArticleModel implements Serializable {
    constructor(public title: string, public content: string) {}

    toJSON(): object {
        return { title: this.title, content: this.content };
    }
    fromJSON(data: any): void {
        this.title   = data.title;
        this.content = data.content;
    }
}
```

<br>

---

## 6. Enums

```typescript title="TypeScript — Enums : ensembles de constantes nommées"
// ─── Enum numérique (défaut) ──────────────────────────────────────────────────
enum Direction {
    North,   // 0
    South,   // 1
    East,    // 2
    West,    // 3
}
console.log(Direction.North);   // 0
console.log(Direction[0]);      // "North"

// ─── Enum numérique avec valeurs personnalisées ───────────────────────────────
enum HttpStatus {
    OK          = 200,
    Created     = 201,
    BadRequest  = 400,
    Unauthorized = 401,
    NotFound    = 404,
    Internal    = 500,
}

function handleResponse(status: HttpStatus): string {
    if (status === HttpStatus.OK) return "Succès";
    if (status === HttpStatus.NotFound) return "Ressource introuvable";
    return "Erreur";
}

// ─── Enum de chaînes (plus lisible et préféré) ───────────────────────────────
enum UserRole {
    Admin     = "ADMIN",
    User      = "USER",
    Moderator = "MODERATOR",
}

const role: UserRole = UserRole.Admin;
console.log(role);  // "ADMIN"

// ─── Const enum (optimisation — remplacé inline à la compilation) ────────────
const enum LogLevel {
    Debug   = "DEBUG",
    Info    = "INFO",
    Warning = "WARNING",
    Error   = "ERROR",
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    TypeScript détecte les erreurs **au développement**, pas à l'exécution. Activez toujours `"strict": true` dans `tsconfig.json` — sans ça, TypeScript est trop permissif. Préférez les **interfaces** pour les objets extensibles, les **type aliases** pour les unions complexes. Les **classes TypeScript** ajoutent `public/private/protected/readonly` et les **raccourcis constructeur**. Les **enums de chaînes** (`Role = "ADMIN"`) sont plus lisibles que les enums numériques. Évitez `any` — utilisez `unknown` + type guard à la place.

> Module suivant : [Types Avancés →](./02-avance.md) — génériques, `Partial`, `Required`, `Pick`, guards, discriminated unions.

<br>
