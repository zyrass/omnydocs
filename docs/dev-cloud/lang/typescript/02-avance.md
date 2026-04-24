---
description: "TypeScript 02 — Types avancés : génériques, utility types (Partial, Required, Pick, Omit, Record), type guards et discriminated unions."
icon: lucide/book-open-check
tags: ["TYPESCRIPT", "GENERIQUES", "UTILITY-TYPES", "TYPE-GUARDS", "MAPPED-TYPES"]
---

# Types Avancés TypeScript

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="TypeScript 5.x"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Les Moules à Gaufres"
    Un moule à gaufres donne la même forme à n'importe quelle pâte (chocolat, vanille, nature). Les **génériques TypeScript** sont ces moules : vous définissez la forme (`Array<T>`, `Repository<T>`) et TypeScript adapte le type automatiquement selon ce que vous y versez. `Array<string>` est le même moule qu'`Array<number>`, mais le résultat est typé différemment.

<br>

---

## 1. Génériques (Generics)

```typescript title="TypeScript — Fonctions génériques"
// ─── Sans générique (peu flexible) ───────────────────────────────────────────
function firstItem(arr: number[]): number {
    return arr[0];  // Ne fonctionne qu'avec number[]
}

// ─── Avec générique (flexible et typé) ───────────────────────────────────────
function firstItem<T>(arr: T[]): T | undefined {
    return arr[0];
}

const num    = firstItem([1, 2, 3]);           // T inféré : number
const str    = firstItem(['a', 'b', 'c']);      // T inféré : string
const user   = firstItem<User>([userData]);     // T explicite : User

// ─── Plusieurs paramètres génériques ─────────────────────────────────────────
function pair<A, B>(first: A, second: B): [A, B] {
    return [first, second];
}
const result = pair('hello', 42);  // [string, number]

// ─── Contraintes génériques (extends) ─────────────────────────────────────────
interface HasId { id: number; }

// T doit avoir une propriété 'id'
function findById<T extends HasId>(items: T[], id: number): T | undefined {
    return items.find(item => item.id === id);
}

// ─── Génériques avec valeurs par défaut ──────────────────────────────────────
interface ApiResponse<T = unknown> {
    data:    T;
    status:  number;
    message: string;
}

type UserResponse    = ApiResponse<User>;    // data: User
type ArticleResponse = ApiResponse<Article>; // data: Article
type DefaultResponse = ApiResponse;          // data: unknown
```

```typescript title="TypeScript — Classes et interfaces génériques"
// Interface générique : Repository Pattern
interface Repository<T, ID = number> {
    findById(id: ID):           Promise<T | null>;
    findAll(filters?: Partial<T>): Promise<T[]>;
    create(data: Omit<T, 'id'>): Promise<T>;
    update(id: ID, data: Partial<T>): Promise<T>;
    delete(id: ID): Promise<void>;
}

// Classe générique implémentant l'interface
class InMemoryRepository<T extends { id: number }> implements Repository<T> {
    private items: T[] = [];

    async findById(id: number): Promise<T | null> {
        return this.items.find(item => item.id === id) ?? null;
    }

    async findAll(filters?: Partial<T>): Promise<T[]> {
        if (!filters) return this.items;
        return this.items.filter(item =>
            Object.entries(filters).every(([key, val]) =>
                item[key as keyof T] === val
            )
        );
    }

    async create(data: Omit<T, 'id'>): Promise<T> {
        const item = { ...data, id: Date.now() } as T;
        this.items.push(item);
        return item;
    }

    async update(id: number, data: Partial<T>): Promise<T> {
        const index = this.items.findIndex(i => i.id === id);
        if (index === -1) throw new Error(`Item ${id} not found`);
        this.items[index] = { ...this.items[index], ...data };
        return this.items[index];
    }

    async delete(id: number): Promise<void> {
        this.items = this.items.filter(i => i.id !== id);
    }
}

// Utilisation
const userRepo    = new InMemoryRepository<User>();
const articleRepo = new InMemoryRepository<Article>();
```

<br>

---

## 2. Utility Types

```typescript title="TypeScript — Utility Types : transformer des types existants"
interface Article {
    id:         number;
    title:      string;
    content:    string;
    status:     "draft" | "published";
    author:     string;
    created_at: Date;
}

// ─── Partial<T> : toutes les propriétés deviennent optionnelles ───────────────
type UpdateArticle = Partial<Article>;
// { id?: number; title?: string; content?: string; status?: ... }

const patch: UpdateArticle = { title: "Nouveau titre" };  // ✅ Partiel valide

// ─── Required<T> : toutes les propriétés deviennent obligatoires ─────────────
interface DraftArticle {
    title:    string;
    content?: string;   // optionnel
}
type FullArticle = Required<DraftArticle>;
// { title: string; content: string; }  ← content maintenant obligatoire

// ─── Pick<T, Keys> : sélectionner certaines propriétés ───────────────────────
type ArticlePreview = Pick<Article, 'id' | 'title' | 'status'>;
// { id: number; title: string; status: "draft" | "published"; }

// ─── Omit<T, Keys> : exclure certaines propriétés ────────────────────────────
type CreateArticle = Omit<Article, 'id' | 'created_at'>;
// { title: string; content: string; status: ...; author: string; }

// ─── Record<Keys, Value> : dictionnaire typé ─────────────────────────────────
type StatusLabels = Record<Article["status"], string>;
const labels: StatusLabels = {
    draft:     "Brouillon",
    published: "Publié",
};

type RouteHandlers = Record<string, (req: Request) => Response>;

// ─── Readonly<T> : toutes les propriétés en lecture seule ────────────────────
type ImmutableArticle = Readonly<Article>;
// const a: ImmutableArticle = {...}; a.title = ""; // ❌ Erreur

// ─── ReturnType<T> : extraire le type de retour d'une fonction ────────────────
function getUser() { return { id: 1, name: "Alice", email: "alice@example.com" }; }
type GetUserReturn = ReturnType<typeof getUser>;
// { id: number; name: string; email: string; }

// ─── Parameters<T> : extraire les paramètres d'une fonction ──────────────────
function createArticle(title: string, content: string, status: "draft" | "published") {}
type CreateParams = Parameters<typeof createArticle>;
// [title: string, content: string, status: "draft" | "published"]

// ─── NonNullable<T> : exclure null et undefined ───────────────────────────────
type MaybeUser = User | null | undefined;
type GuaranteedUser = NonNullable<MaybeUser>;  // User (sans null ni undefined)
```

<br>

---

## 3. Type Guards

```typescript title="TypeScript — Narrowing : réduire le type à l'exécution"
type StringOrNumber = string | number;

function processValue(value: StringOrNumber): string {
    // ─── typeof guard ────────────────────────────────────────────────────────
    if (typeof value === "string") {
        return value.toUpperCase();  // TypeScript sait : string ici
    }
    return value.toFixed(2);         // TypeScript sait : number ici
}

// ─── instanceof guard ─────────────────────────────────────────────────────────
function handleError(error: unknown): string {
    if (error instanceof Error) {
        return error.message;   // TypeScript sait : Error ici
    }
    if (typeof error === "string") {
        return error;
    }
    return "Erreur inconnue";
}

// ─── in guard (propriété dans l'objet) ────────────────────────────────────────
interface Dog  { bark():  void; }
interface Cat  { meow():  void; }
type Pet = Dog | Cat;

function makeSound(pet: Pet): void {
    if ("bark" in pet) {
        pet.bark();  // TypeScript sait : Dog ici
    } else {
        pet.meow();  // TypeScript sait : Cat ici
    }
}

// ─── User-defined type guard (prédicat de type) ────────────────────────────────
interface Admin { role: "admin"; permissions: string[]; }
interface User  { role: "user"; }
type AnyUser = Admin | User;

// La signature "value is Admin" dit à TypeScript :
// si cette fonction retourne true → value est Admin dans le bloc if
function isAdmin(value: AnyUser): value is Admin {
    return value.role === "admin";
}

function showPermissions(user: AnyUser): void {
    if (isAdmin(user)) {
        console.log(user.permissions);  // ✅ TypeScript sait : Admin ici
    } else {
        console.log("Utilisateur standard");
    }
}
```

<br>

---

## 4. Discriminated Unions

```typescript title="TypeScript — Discriminated Unions : union discriminée par une propriété commune"
// ─── Sans discriminated union (difficile à gérer) ─────────────────────────────
type Shape = {
    kind:   string;
    radius?: number;    // Seulement pour Circle
    side?:   number;    // Seulement pour Square
    width?:  number;    // Seulement pour Rectangle
    height?: number;    // Seulement pour Rectangle
};
// Problème : toutes les propriétés sont optionnelles → TypeScript ne peut pas valider

// ─── Avec discriminated union (clair et sûr) ──────────────────────────────────
type Circle    = { kind: "circle";    radius: number; };
type Square    = { kind: "square";    side: number; };
type Rectangle = { kind: "rectangle"; width: number; height: number; };
type Shape     = Circle | Square | Rectangle;   // ← Discriminated Union

function area(shape: Shape): number {
    switch (shape.kind) {        // "kind" est le discriminant
        case "circle":
            return Math.PI * shape.radius ** 2;  // TypeScript sait : Circle
        case "square":
            return shape.side ** 2;               // TypeScript sait : Square
        case "rectangle":
            return shape.width * shape.height;    // TypeScript sait : Rectangle
        default:
            // TypeScript vérifie que tous les cas sont couverts (exhaustivité)
            const _exhaustive: never = shape;
            throw new Error(`Forme non gérée : ${_exhaustive}`);
    }
}

// ─── Exemple réel : réponses API ──────────────────────────────────────────────
type ApiLoading = { status: "loading"; };
type ApiSuccess<T> = { status: "success"; data: T; };
type ApiError   = { status: "error";   error: string; };
type ApiState<T>  = ApiLoading | ApiSuccess<T> | ApiError;

function renderState<T>(state: ApiState<T>): string {
    switch (state.status) {
        case "loading": return "Chargement...";
        case "success": return `Données : ${JSON.stringify(state.data)}`;
        case "error":   return `Erreur : ${state.error}`;
    }
}
```

<br>

---

## 5. Types Conditionnels et Mapped Types

```typescript title="TypeScript — Types conditionnels et mapped types"
// ─── Types conditionnels ──────────────────────────────────────────────────────
type IsString<T> = T extends string ? "oui" : "non";
type A = IsString<string>;  // "oui"
type B = IsString<number>;  // "non"

// Extraire le type des éléments d'un tableau
type ElementType<T> = T extends Array<infer U> ? U : never;
type StrElem = ElementType<string[]>;   // string
type NumElem = ElementType<number[]>;   // number

// ─── Mapped Types : transformer les clés d'un type ───────────────────────────
// Recréer Partial<T> manuellement
type MyPartial<T> = {
    [K in keyof T]?: T[K];
};

// Rendre toutes les valeurs nullable
type Nullable<T> = {
    [K in keyof T]: T[K] | null;
};

// Préfixer toutes les clés
type Prefixed<T, Prefix extends string> = {
    [K in keyof T as `${Prefix}${Capitalize<string & K>}`]: T[K];
};

type PrefixedUser = Prefixed<{ name: string; email: string }, "user">;
// { userName: string; userEmail: string; }
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les **génériques** permettent d'écrire du code réutilisable et typé — `function fn<T>(x: T): T` préserve le type à travers la transformation. Les **Utility Types** (`Partial`, `Required`, `Pick`, `Omit`, `Record`, `Readonly`) transforment des types existants sans redéfinir. Les **Type Guards** (`typeof`, `instanceof`, `in`, prédicats `value is T`) affinent le type dans un bloc conditionnel. Les **Discriminated Unions** avec une propriété discriminante (`kind`, `type`, `status`) permettent une gestion exhaustive et sûre des états. TypeScript strict + génériques + utility types = code aussi expressif que dynamique, mais **entièrement typé**.

> **Formation TypeScript complète.** Retour à l'[index Langages →](../index.md).

<br>
