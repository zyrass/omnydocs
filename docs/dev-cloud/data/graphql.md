---
description: "GraphQL — Langage de requête pour APIs : schéma typé, queries, mutations, subscriptions, comparaison REST et intégration Laravel."
icon: lucide/network
tags: ["GRAPHQL", "API", "LARAVEL", "SCHEMA", "TYPESCRIPT"]
---

# GraphQL

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2024"
  data-time="15-20 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Pizzeria à la Carte vs le Menu Fixe"
    Une API REST, c'est comme un menu fixe : vous commandez "la planche entrée" et vous recevez tout ce qu'elle contient, que vous en ayez besoin ou non (over-fetching). Ou vous devez commander 3 plats séparément pour composer votre repas (under-fetching, N+1 appels). GraphQL, c'est la pizzeria à la carte : vous listez exactement les ingrédients que vous voulez sur votre pizza, dans un seul appel. Un seul endpoint, une seule requête, exactement les données demandées — ni plus, ni moins.

**GraphQL** est un langage de requête pour APIs créé par Facebook en 2015. Il permet aux clients de demander **exactement les données dont ils ont besoin**, dans un seul appel, via un schéma typé qui sert à la fois de contrat et de documentation.

> GraphQL ne remplace pas REST dans tous les cas — il excelle pour les clients multiples avec besoins différents (web, mobile, partenaires).

<br>

---

## 1. GraphQL vs REST — Comparaison

### Le problème de REST

```bash title="Bash — REST : over-fetching et under-fetching"
# ❌ Over-fetching : trop de données
GET /api/users/1
# Réponse : { id, name, email, avatar, bio, phone, address, preferences, ... }
# → On voulait juste name et email

# ❌ Under-fetching : trop d'appels (N+1)
GET /api/posts            # Liste de posts → 10 posts
GET /api/users/1          # Auteur du post 1
GET /api/users/3          # Auteur du post 2
GET /api/users/7          # Auteur du post 3
# → 11 requêtes HTTP pour afficher une liste simple
```

### La solution GraphQL

```graphql title="GraphQL — Une seule requête, exactement les données voulues"
# ✅ Un seul appel, exactement ce qu'on veut :
query {
  posts {
    title
    createdAt
    author {
      name    # Seulement name et avatar — pas tout le profil utilisateur
      avatar
    }
    tags {
      name
    }
  }
}

# Réponse JSON :
# {
#   "data": {
#     "posts": [
#       { "title": "...", "createdAt": "...", "author": { "name": "Alice", "avatar": "..." }, "tags": [...] },
#       ...
#     ]
#   }
# }
```

| Critère | REST | GraphQL |
|---|---|---|
| **Endpoints** | Un par ressource | Un seul (`/graphql`) |
| **Over-fetching** | Fréquent | Éliminé par conception |
| **Under-fetching** | N+1 appels courant | Résolu dans une requête |
| **Typage** | Manuel / OpenAPI | Schéma typé natif |
| **Documentation** | Externe (Swagger) | Introspection native |
| **Cache HTTP** | Natif (GET) | Complexe (POST par défaut) |
| **Courbe d'apprentissage** | Faible | Moyenne |
| **Idéal pour** | APIs publiques, CRUD simple | Apps multi-clients, dashboards |

<br>

---

## 2. Le Schéma GraphQL

Le schéma est le **contrat** entre le serveur et les clients. Il définit les types, les champs, et les opérations disponibles.

```graphql title="GraphQL — Définition d'un schéma complet"
# ─── Types scalaires de base ──────────────────────────────────────────────────
# String, Int, Float, Boolean, ID (built-in)
# + types scalaires custom : Date, DateTime, JSON, Upload...

# ─── Types Object ────────────────────────────────────────────────────────────
type User {
  id:        ID!          # ! = Non-nullable (obligatoire)
  name:      String!
  email:     String!
  avatar:    String       # Nullable (optionnel)
  role:      UserRole!    # Enum
  posts:     [Post!]!     # [Type!]! = tableau non-null de valeurs non-nulles
  createdAt: DateTime!
}

type Post {
  id:          ID!
  title:       String!
  content:     String
  published:   Boolean!
  author:      User!
  tags:        [Tag!]!
  comments:    [Comment!]!
  likesCount:  Int!
  createdAt:   DateTime!
}

type Tag {
  id:    ID!
  name:  String!
  posts: [Post!]!
}

type Comment {
  id:        ID!
  content:   String!
  author:    User!
  post:      Post!
  createdAt: DateTime!
}

# ─── Enum ────────────────────────────────────────────────────────────────────
enum UserRole {
  ADMIN
  EDITOR
  VIEWER
}

# ─── Types d'entrée (pour les mutations) ──────────────────────────────────────
input CreatePostInput {
  title:   String!
  content: String
  tagIds:  [ID!]
}

input UpdatePostInput {
  title:   String
  content: String
  tagIds:  [ID!]
}

# ─── Opérations racines ───────────────────────────────────────────────────────
type Query {
  # Récupérer un utilisateur
  user(id: ID!): User
  users(limit: Int = 20, offset: Int = 0): [User!]!
  me: User                               # Utilisateur authentifié

  # Récupérer des posts
  post(id: ID!): Post
  posts(published: Boolean, authorId: ID): [Post!]!
  searchPosts(query: String!): [Post!]!
}

type Mutation {
  # Authentification
  login(email: String!, password: String!): AuthPayload!
  logout: Boolean!

  # Posts
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: UpdatePostInput!): Post!
  deletePost(id: ID!): Boolean!
  publishPost(id: ID!): Post!

  # Commentaires
  addComment(postId: ID!, content: String!): Comment!
}

type Subscription {
  # Événements temps réel
  newComment(postId: ID!): Comment!
  postPublished: Post!
}

type AuthPayload {
  token: String!
  user:  User!
}
```

<br>

---

## 3. Queries — Lire des Données

```graphql title="GraphQL — Queries : lecture de données avec arguments et fragments"
# ─── Query simple ─────────────────────────────────────────────────────────────
query GetUser {
  user(id: "1") {
    name
    email
  }
}

# ─── Query avec variables ─────────────────────────────────────────────────────
query GetUser($id: ID!) {
  user(id: $id) {
    name
    email
    role
    posts {
      title
      published
      createdAt
    }
  }
}
# Variables : { "id": "1" }

# ─── Fragments (réutilisation de champs) ──────────────────────────────────────
fragment PostBasics on Post {
  id
  title
  createdAt
  author { name }
}

query GetPosts {
  posts(published: true) {
    ...PostBasics         # Utilisation du fragment
    tags { name }
  }
}

# ─── Aliases (renommer le champ dans la réponse) ──────────────────────────────
query GetMultipleUsers {
  admin: user(id: "1") { name email }    # "admin" dans la réponse
  editor: user(id: "2") { name email }   # "editor" dans la réponse
}

# ─── Directives conditionnelles ───────────────────────────────────────────────
query GetPost($id: ID!, $withComments: Boolean!) {
  post(id: $id) {
    title
    content
    comments @include(if: $withComments) {  # Inclure si $withComments = true
      content
      author { name }
    }
  }
}

# ─── Introspection (documentation auto) ──────────────────────────────────────
query IntrospectSchema {
  __schema {
    types {
      name
      kind
      fields { name type { name } }
    }
  }
}
```

<br>

---

## 4. Mutations — Modifier des Données

```graphql title="GraphQL — Mutations : créer, modifier, supprimer"
# ─── Créer ────────────────────────────────────────────────────────────────────
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    createdAt
    author { name }
  }
}
# Variables :
# {
#   "input": {
#     "title": "Mon Article GraphQL",
#     "content": "Contenu...",
#     "tagIds": ["1", "3"]
#   }
# }

# ─── Mettre à jour ────────────────────────────────────────────────────────────
mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
  updatePost(id: $id, input: $input) {
    id
    title
    tags { name }
  }
}

# ─── Authentification ─────────────────────────────────────────────────────────
mutation Login {
  login(email: "alice@example.com", password: "secret") {
    token
    user {
      id
      name
      role
    }
  }
}
```

<br>

---

## 5. Subscriptions — Temps Réel

```graphql title="GraphQL — Subscriptions WebSocket"
# ─── S'abonner aux nouveaux commentaires ──────────────────────────────────────
subscription OnNewComment($postId: ID!) {
  newComment(postId: $postId) {
    id
    content
    createdAt
    author {
      name
      avatar
    }
  }
}

# ─── Côté client JavaScript (Apollo Client) ───────────────────────────────────
```

```javascript title="JavaScript — Apollo Client : subscription WebSocket"
import { gql, useSubscription } from '@apollo/client';

const NEW_COMMENT = gql`
  subscription OnNewComment($postId: ID!) {
    newComment(postId: $postId) {
      id
      content
      author { name avatar }
      createdAt
    }
  }
`;

function CommentsSection({ postId }) {
  const { data, loading } = useSubscription(NEW_COMMENT, {
    variables: { postId }
  });

  // data.newComment contient le nouveau commentaire en temps réel
}
```

<br>

---

## 6. Intégration Laravel — Lighthouse

**Lighthouse** est le package Laravel de référence pour GraphQL.

```bash title="Bash — Installer Lighthouse"
composer require nuwave/lighthouse
php artisan vendor:publish --tag=lighthouse-schema
# Publie config/lighthouse.php et graphql/schema.graphql
```

```graphql title="GraphQL — graphql/schema.graphql avec directives Lighthouse"
type Query {
  # @paginate : génère automatiquement la pagination
  users: [User!]! @paginate(defaultCount: 20)

  # @find : récupère par ID auto
  user(id: ID! @eq): User @find

  # @all : retourne tous les enregistrements
  tags: [Tag!]! @all

  # @auth : retourne l'utilisateur authentifié
  me: User @auth
}

type Mutation {
  # @create / @update / @delete : CRUD automatique depuis Eloquent
  createUser(
    name:  String! @rules(apply: ["required", "min:2"])
    email: String! @rules(apply: ["required", "email", "unique:users,email"])
  ): User! @create

  updateUser(
    id:    ID!
    name:  String
    email: String @rules(apply: ["email"])
  ): User! @update

  deleteUser(id: ID!): User! @delete
}

type User {
  id:        ID!
  name:      String!
  email:     String!
  posts:     [Post!]! @hasMany           # Relation Eloquent auto
  createdAt: DateTime! @rename(attribute: "created_at")
}

type Post {
  id:       ID!
  title:    String!
  author:   User! @belongsTo           # Relation Eloquent auto
  tags:     [Tag!]! @belongsToMany     # Relation many-to-many auto
}
```

```php title="PHP — Resolver personnalisé avec Lighthouse"
<?php

namespace App\GraphQL\Queries;

use App\Models\Post;
use Illuminate\Support\Facades\Auth;

readonly class UserPosts
{
    /**
     * Resolver pour : posts(published: Boolean): [Post!]!
     */
    public function __invoke(mixed $root, array $args): \Illuminate\Database\Eloquent\Collection
    {
        $query = Post::where('user_id', Auth::id());

        if (isset($args['published'])) {
            $query->where('published', $args['published']);
        }

        return $query->latest()->get();
    }
}
```

```bash title="Bash — Tester avec GraphQL Playground (Lighthouse)"
# En développement, Lighthouse expose automatiquement :
# http://localhost/graphiql  (interface interactive)

# Ou via curl :
curl -X POST http://localhost/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name email } }"}'
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Concevoir un schéma**

```graphql title="GraphQL — Exercice 1 : schéma pour une application de recettes"
# Modélisez un schéma GraphQL pour une application de recettes :
# - Recipe : title, description, duration, difficulty, ingredients, steps, author, tags
# - Ingredient : name, quantity, unit
# - Step : order, description
# - User : name, email, recipes
# - Tag : name

# Définissez :
# 1. Tous les types Object avec leurs champs
# 2. Les types Input pour les mutations
# 3. Les Queries : recipe(id), recipes(filter), searchRecipes(query)
# 4. Les Mutations : createRecipe, updateRecipe, deleteRecipe, rateRecipe
# 5. Une Subscription : recipeAdded
```

**Exercice 2 — Lighthouse en pratique**

```bash title="Bash — Exercice 2 : API GraphQL complète avec Laravel + Lighthouse"
# 1. Installer Lighthouse dans un projet Laravel existant
# 2. Créer les modèles Recipe, Ingredient, Tag avec leurs relations Eloquent
# 3. Écrire le schéma graphql/schema.graphql avec les directives Lighthouse
# 4. Tester les queries et mutations dans GraphiQL
# 5. Ajouter @guard sur les mutations (authentification requise)
# 6. Ajouter la pagination avec @paginate
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    GraphQL résout l'**over-fetching** (trop de données) et l'**under-fetching** (trop d'appels) de REST en permettant aux clients de demander exactement ce dont ils ont besoin, dans un seul appel. Le **schéma** est le contrat central — typé, auto-documenté, introspectable. Les **Queries** lisent, les **Mutations** écrivent, les **Subscriptions** écoutent en temps réel. Dans l'écosystème Laravel, **Lighthouse** est la référence : ses directives (`@paginate`, `@hasMany`, `@create`) génèrent automatiquement le CRUD Eloquent. GraphQL brille pour les applications avec plusieurs clients (web, mobile, partenaires) aux besoins différents. Il ne remplace pas REST pour les APIs publiques simples ou les cas où le cache HTTP est critique.

> L'écosystème BDD est maintenant complet. Retournez à l'[index Base de données →](./index.md) ou explorez les [Frameworks →](../frameworks/index.md).

<br>