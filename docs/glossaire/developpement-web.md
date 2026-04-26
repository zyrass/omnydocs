---
description: "Glossaire — Développement Web : Frontend, backend, APIs, frameworks, sécurité web et performance."
icon: lucide/book-a
tags: ["GLOSSAIRE", "DÉVELOPPEMENT", "WEB", "JAVASCRIPT", "API"]
---

# Développement Web

<div
  class="omny-meta"
  data-level="🟢 Tout niveau"
  data-version="1.0"
  data-time="Consultation">
</div>


!!! quote "Analogie pédagogique"
    _Construire une application web est comme bâtir un restaurant. Le HTML est la structure des murs, le CSS est la décoration et l'éclairage, et le JavaScript est l'ensemble des systèmes interactifs (portes automatiques, caisse enregistreuse). Enfin, le Backend est la cuisine où les commandes (requêtes) sont préparées secrètement avant d'être servies._

## A

### AJAX

!!! note "Définition"
    Technique permettant la communication asynchrone entre navigateur et serveur sans rechargement de page.

Utilisé pour créer des applications web dynamiques et interactives.

- **Acronyme :** Asynchronous JavaScript and XML
- **Technologies :** Fetch API (moderne), `XMLHttpRequest` (historique), JSON

```mermaid
graph TB
    A[AJAX] --> B[Asynchrone]
    A --> C[JavaScript]
    A --> D[Fetch API]
```

_Explication : AJAX est défini comme : technique permettant la communication asynchrone entre navigateur et serveur sans rechargement de page._

<br>

---

### Angular

!!! note "Définition"
    Framework JavaScript développé par Google pour créer des applications web single-page.

Utilisé pour développer des applications web d'entreprise avec architecture stricte.

- **Technologies :** TypeScript (natif), RxJS, Angular CLI
- **Concepts :** composants, services, directives, pipes

```mermaid
graph TB
    A[Angular] --> B[TypeScript]
    A --> C[SPA]
    A --> D[Google]
```

_Explication : Angular est défini comme : framework JavaScript développé par Google pour créer des applications web single-page._

<br>

---

### API Gateway

!!! note "Définition"
    Point d'entrée unifié gérant les requêtes vers des microservices backend.

Utilisé pour centraliser l'authentification, le routage et la gestion des APIs.

- **Fonctionnalités :** rate limiting, transformation, monitoring, cache
- **Services :** AWS API Gateway, Kong, NGINX

```mermaid
graph TB
    A[API Gateway] --> B[Microservices]
    A --> C[Authentification]
    A --> D[Rate limiting]
```

_Explication : API Gateway est défini comme : point d'entrée unifié gérant les requêtes vers des microservices backend._

<br>

---

## B

### Babel

!!! note "Définition"
    Transpileur JavaScript convertissant le code moderne ES6+ en version compatible navigateurs.

Utilisé pour utiliser les dernières fonctionnalités JS tout en gardant la compatibilité.

- **Fonctionnalités :** ES6+ vers ES5, plugins, presets (`env`, `react`, `typescript`)
- **Configuration :** `.babelrc`, `babel.config.js`

```mermaid
graph TB
    A[Babel] --> B[Transpilation]
    A --> C[ES6+]
    A --> D[Compatibilité]
```

_Explication : Babel est défini comme : transpileur JavaScript convertissant le code moderne ES6+ en version compatible navigateurs._

<br>

---

### Bootstrap

!!! note "Définition"
    Framework CSS responsive fournissant des composants et une grille pré-stylés.

Utilisé pour développer rapidement des interfaces web responsive.

- **Composants :** navbar, cards, modals, forms
- **Système :** grille 12 colonnes, breakpoints responsive

```mermaid
graph TB
    A[Bootstrap] --> B[CSS Framework]
    A --> C[Responsive]
    A --> D[Grid System]
```

_Explication : Bootstrap est défini comme : framework CSS responsive fournissant des composants et une grille pré-stylés._

<br>

---

## C

### CDN

!!! note "Définition"
    Réseau de serveurs géographiquement distribués pour la livraison optimisée de contenu.

Utilisé pour améliorer les performances en servant les assets depuis le nœud le plus proche.

- **Acronyme :** Content Delivery Network
- **Avantages :** latence réduite, cache distribué, résistance DDoS

```mermaid
graph TB
    A[CDN] --> B[Performance]
    A --> C[Cache]
    A --> D[Distribution]
```

_Explication : CDN est défini comme : réseau de serveurs géographiquement distribués pour la livraison optimisée de contenu._

<br>

---

### CORS

!!! note "Définition"
    Mécanisme permettant aux serveurs d'autoriser les requêtes provenant d'autres domaines.

Utilisé pour sécuriser les requêtes cross-origin dans les applications web.

- **Acronyme :** Cross-Origin Resource Sharing
- **En-têtes :** `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`

```mermaid
graph TB
    A[CORS] --> B[Cross-origin]
    A --> C[Sécurité]
    A --> D[API]
```

_Explication : CORS est défini comme : mécanisme permettant aux serveurs d'autoriser les requêtes provenant d'autres domaines._

<br>

---

### CSS

!!! note "Définition"
    Langage de feuilles de style décrivant la présentation des documents HTML.

Utilisé pour styliser et mettre en forme toutes les pages web.

- **Acronyme :** Cascading Style Sheets
- **Fonctionnalités modernes :** CSS Grid, Flexbox, Custom Properties, Animations

```mermaid
graph TB
    A[CSS] --> B[Style]
    A --> C[HTML]
    A --> D[Responsive]
```

_Explication : CSS est défini comme : langage de feuilles de style décrivant la présentation des documents HTML._

<br>

---

### CSRF

!!! note "Définition"
    Attaque forçant un utilisateur authentifié à exécuter des actions non désirées.

Utilisé comme vecteur d'attaque exploitant la confiance du serveur envers le navigateur.

- **Acronyme :** Cross-Site Request Forgery
- **Protection :** tokens CSRF, cookies `SameSite=Strict`, vérification de l'origine

```mermaid
graph TB
    A[CSRF] --> B[Attaque]
    A --> C[Token]
    A --> D[Sécurité web]
```

_Explication : CSRF est défini comme : attaque forçant un utilisateur authentifié à exécuter des actions non désirées._

<br>

---

## D

### Django

!!! note "Définition"
    Framework web Python haut niveau suivant le principe "batteries incluses".

Utilisé pour développer rapidement des applications web robustes et sécurisées.

- **Architecture :** MVT (Model-View-Template)
- **Fonctionnalités :** ORM, admin interface, authentification, migrations

```mermaid
graph TB
    A[Django] --> B[Python]
    A --> C[MVT]
    A --> D[ORM]
```

_Explication : Django est défini comme : framework web Python haut niveau suivant le principe "batteries incluses"._

<br>

---

### DOM

!!! note "Définition"
    Représentation en mémoire de la structure hiérarchique d'un document HTML/XML.

Utilisé par JavaScript pour manipuler dynamiquement le contenu des pages web.

- **Acronyme :** Document Object Model
- **API :** `createElement`, `querySelector`, `addEventListener`

```mermaid
graph TB
    A[DOM] --> B[HTML]
    A --> C[JavaScript]
    A --> D[Manipulation]
```

_Explication : DOM est défini comme : représentation en mémoire de la structure hiérarchique d'un document HTML/XML._

<br>

---

### Docker

!!! note "Définition"
    Plateforme de conteneurisation permettant d'empaqueter applications et dépendances.

Utilisé pour standardiser les environnements de développement et déploiement.

- **Concepts :** images, containers, Dockerfile, volumes, registries
- **Avantages :** portabilité, isolation, reproductibilité

```mermaid
graph TB
    A[Docker] --> B[Container]
    A --> C[Image]
    A --> D[Isolation]
```

_Explication : Docker est défini comme : plateforme de conteneurisation permettant d'empaqueter applications et dépendances._

<br>

---

## E

### Express.js

!!! note "Définition"
    Framework web minimaliste et flexible pour Node.js.

Utilisé pour créer des APIs REST et des applications web côté serveur.

- **Fonctionnalités :** routing HTTP, middleware, template engines
- **Écosystème :** Passport, Morgan, Helmet, nombreux middlewares

```mermaid
graph TB
    A[Express.js] --> B[Node.js]
    A --> C[API REST]
    A --> D[Middleware]
```

_Explication : Express.js est défini comme : framework web minimaliste et flexible pour Node.js._

<br>

---

## F

### Fetch API

!!! note "Définition"
    Interface moderne native pour effectuer des requêtes HTTP en JavaScript.

Utilisé pour remplacer `XMLHttpRequest` avec une syntaxe Promises plus lisible.

- **Fonctionnalités :** Promises, streaming, objets `Request`/`Response`
- **Support :** tous les navigateurs modernes et Node.js 18+

```mermaid
graph TB
    A[Fetch API] --> B[HTTP]
    A --> C[Promises]
    A --> D[XMLHttpRequest]
```

_Explication : Fetch API est défini comme : interface moderne native pour effectuer des requêtes HTTP en JavaScript._

<br>

---

### Flask

!!! note "Définition"
    Micro-framework web Python léger et extensible.

Utilisé pour créer des applications web simples et des APIs avec un maximum de liberté.

- **Philosophie :** noyau minimal + extensions au choix
- **Extensions :** Flask-SQLAlchemy, Flask-Login, Flask-RESTful

```mermaid
graph TB
    A[Flask] --> B[Python]
    A --> C[Micro-framework]
    A --> D[Extensions]
```

_Explication : Flask est défini comme : micro-framework web Python léger et extensible._

<br>

---

## G

### GraphQL

!!! note "Définition"
    Langage de requête et runtime pour APIs offrant une alternative flexible à REST.

Utilisé pour récupérer exactement les données nécessaires en une seule requête.

- **Avantages :** typage fort, introspection, single endpoint, requêtes imbriquées
- **Concepts :** schema, resolvers, mutations, subscriptions

```mermaid
graph TB
    A[GraphQL] --> B[Query Language]
    A --> C[Schema]
    A --> D[REST]
```

_Explication : GraphQL est défini comme : langage de requête et runtime pour APIs offrant une alternative flexible à REST._

<br>

---

## H

### HTML

!!! note "Définition"
    Langage de balisage standard pour créer des pages web structurées.

Utilisé comme fondation de toutes les pages web pour définir le contenu et la structure.

- **Acronyme :** HyperText Markup Language
- **HTML5 :** nouvelles API et éléments sémantiques (`<nav>`, `<article>`, `<section>`)

```mermaid
graph TB
    A[HTML] --> B[Structure]
    A --> C[Sémantique]
    A --> D[CSS]
```

_Explication : HTML est défini comme : langage de balisage standard pour créer des pages web structurées._

<br>

---

### HTTP/HTTPS

!!! note "Définition"
    Protocoles de transfert de données entre clients web et serveurs.

Utilisé pour toutes les communications web, HTTPS ajoutant la sécurité TLS.

- **Acronyme :** HyperText Transfer Protocol (Secure)
- **Méthodes :** `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`

```mermaid
graph TB
    A[HTTP/HTTPS] --> B[Client-Serveur]
    A --> C[TLS]
    A --> D[REST]
```

_Explication : HTTP/HTTPS est défini comme : protocoles de transfert de données entre clients web et serveurs._

<br>

---

## J

### JavaScript

!!! note "Définition"
    Langage de programmation dynamique pour le développement web côté client et serveur.

Utilisé pour l'interactivité des pages web et le backend avec Node.js.

- **Standards :** ECMAScript (ES6+), TC39
- **Concepts :** closures, prototypes, async/await, modules ESM

```mermaid
graph TB
    A[JavaScript] --> B[DOM]
    A --> C[Node.js]
    A --> D[ECMAScript]
```

_Explication : JavaScript est défini comme : langage de programmation dynamique pour le développement web côté client et serveur._

<br>

---

### JSON

!!! note "Définition"
    Format léger d'échange de données structurées lisible par les humains et les machines.

Utilisé pour la communication entre APIs, configuration et stockage de données.

- **Acronyme :** JavaScript Object Notation
- **Types :** string, number, boolean, null, array, object

```mermaid
graph TB
    A[JSON] --> B[API]
    A --> C[Configuration]
    A --> D[Échange de données]
```

_Explication : JSON est défini comme : format léger d'échange de données structurées lisible par les humains et les machines._

<br>

---

### JWT

!!! note "Définition"
    Standard de token compact et auto-signé pour l'authentification et l'échange d'informations.

Utilisé pour l'authentification stateless dans les APIs REST et applications distribuées.

- **Acronyme :** JSON Web Token
- **Structure :** `<header>.<payload>.<signature>` (Base64url)

```mermaid
graph TB
    A[JWT] --> B[Authentification]
    A --> C[Stateless]
    A --> D[API]
```

_Explication : JWT est défini comme : standard de token compact et auto-signé pour l'authentification et l'échange d'informations._

<br>

---

## N

### Node.js

!!! note "Définition"
    Runtime JavaScript côté serveur basé sur le moteur V8 de Chrome.

Utilisé pour développer des applications backend, APIs et outils avec JavaScript.

- **Caractéristiques :** event-driven, non-blocking I/O, event loop
- **Écosystème :** npm, Express, Fastify, NestJS

```mermaid
graph TB
    A[Node.js] --> B[V8]
    A --> C[Backend]
    A --> D[npm]
```

_Explication : Node.js est défini comme : runtime JavaScript côté serveur basé sur le moteur V8 de Chrome._

<br>

---

### npm

!!! note "Définition"
    Gestionnaire de paquets par défaut pour l'écosystème Node.js.

Utilisé pour installer, gérer et partager des modules JavaScript dans les projets.

- **Acronyme :** Node Package Manager
- **Fichiers :** `package.json`, `package-lock.json`

```mermaid
graph TB
    A[npm] --> B[Node.js]
    A --> C[Packages]
    A --> D[Dépendances]
```

_Explication : npm est défini comme : gestionnaire de paquets par défaut pour l'écosystème Node.js._

<br>

---

## O

### OAuth

!!! note "Définition"
    Framework d'autorisation permettant l'accès sécurisé aux ressources sans partager les mots de passe.

Utilisé pour l'authentification déléguée via des fournisseurs tiers (Google, GitHub).

- **Flux :** authorization code (web), client credentials (M2M)
- **Versions :** OAuth 2.0, OIDC (identité + OAuth 2.0)

```mermaid
graph TB
    A[OAuth] --> B[Autorisation]
    A --> C[Third-party]
    A --> D[API]
```

_Explication : OAuth est défini comme : framework d'autorisation permettant l'accès sécurisé aux ressources sans partager les mots de passe._

<br>

---

### ORM

!!! note "Définition"
    Technique de programmation mappant les objets du code aux tables de base de données.

Utilisé pour simplifier les interactions avec les bases de données relationnelles.

- **Acronyme :** Object-Relational Mapping
- **Exemples :** Sequelize / Prisma (Node.js), SQLAlchemy (Python), Eloquent (Laravel)

```mermaid
graph TB
    A[ORM] --> B[Base de données]
    A --> C[Objets]
    A --> D[SQL]
```

_Explication : ORM est défini comme : technique de programmation mappant les objets du code aux tables de base de données._

<br>

---

## P

### PWA

!!! note "Définition"
    Application web offrant une expérience proche des applications natives mobiles.

Utilisé pour créer des apps web installables avec fonctionnalités hors ligne.

- **Acronyme :** Progressive Web App
- **Technologies :** Service Workers, Web App Manifest, HTTPS

```mermaid
graph TB
    A[PWA] --> B[Service Worker]
    A --> C[Offline]
    A --> D[Installable]
```

_Explication : PWA est défini comme : application web offrant une expérience proche des applications natives mobiles._

<br>

---

### PHP

!!! note "Définition"
    Langage de script côté serveur spécialement conçu pour le développement web.

Utilisé pour créer des sites web dynamiques et des applications backend.

- **Acronyme :** PHP: Hypertext Preprocessor (récursif)
- **Frameworks :** Laravel, Symfony, CodeIgniter

```mermaid
graph TB
    A[PHP] --> B[Server-side]
    A --> C[Web dynamique]
    A --> D[Laravel]
```

_Explication : PHP est défini comme : langage de script côté serveur spécialement conçu pour le développement web._

<br>

---

## R

### React

!!! note "Définition"
    Bibliothèque JavaScript développée par Meta pour construire des interfaces utilisateur.

Utilisé pour créer des applications web interactives basées sur des composants réutilisables.

- **Concepts :** Virtual DOM, JSX, Hooks (`useState`, `useEffect`)
- **Écosystème :** Redux, React Router, Next.js

```mermaid
graph TB
    A[React] --> B[Virtual DOM]
    A --> C[Composants]
    A --> D[JSX]
```

_Explication : React est défini comme : bibliothèque JavaScript développée par Meta pour construire des interfaces utilisateur._

<br>

---

### REST

!!! note "Définition"
    Style architectural pour concevoir des services web utilisant les méthodes HTTP standard.

Utilisé pour créer des APIs simples, scalables et interopérables.

- **Acronyme :** Representational State Transfer
- **Contraintes :** stateless, cacheable, interface uniforme, architecture en couches

```mermaid
graph TB
    A[REST] --> B[HTTP]
    A --> C[Stateless]
    A --> D[API]
```

_Explication : REST est défini comme : style architectural pour concevoir des services web utilisant les méthodes HTTP standard._

<br>

---

### Redux

!!! note "Définition"
    Gestionnaire d'état prévisible et centralisé pour applications JavaScript.

Utilisé pour gérer l'état global des applications React complexes.

- **Concepts :** store (état global), actions (intentions), reducers (pure functions)
- **Principes :** single source of truth, state en lecture seule

```mermaid
graph TB
    A[Redux] --> B[State management]
    A --> C[Store]
    A --> D[React]
```

_Explication : Redux est défini comme : gestionnaire d'état prévisible et centralisé pour applications JavaScript._

<br>

---

## S

### SPA

!!! note "Définition"
    Application web fonctionnant sur une seule page HTML avec navigation dynamique côté client.

Utilisé pour créer des expériences utilisateur fluides sans rechargements complets.

- **Acronyme :** Single Page Application
- **Technologies :** React, Angular, Vue.js avec routing client-side

```mermaid
graph TB
    A[SPA] --> B[Routing client]
    A --> C[UX fluide]
    A --> D[AJAX]
```

_Explication : SPA est défini comme : application web fonctionnant sur une seule page HTML avec navigation dynamique côté client._

<br>

---

### SQL Injection

!!! note "Définition"
    Technique d'attaque injectant du code SQL malveillant dans les requêtes d'une application.

Utilisé pour accéder, modifier ou supprimer des données sans autorisation.

- **Protection :** requêtes préparées, validation des entrées, ORM, WAF
- **Impact :** vol de données, contournement d'authentification, escalade de privilèges

```mermaid
graph TB
    A[SQL Injection] --> B[Attaque]
    A --> C[Base de données]
    A --> D[Sécurité web]
```

_Explication : SQL Injection est défini comme : technique d'attaque injectant du code SQL malveillant dans les requêtes d'une application._

<br>

---

### SSL/TLS

!!! note "Définition"
    Protocoles cryptographiques sécurisant les communications web.

Utilisé pour chiffrer les données échangées — SSL déprécié, TLS est le standard actuel.

- **Acronyme :** Secure Sockets Layer / Transport Layer Security
- **Certificats :** DV (domaine), OV (organisation), EV (extended validation)

```mermaid
graph TB
    A[SSL/TLS] --> B[Chiffrement]
    A --> C[HTTPS]
    A --> D[Certificat]
```

_Explication : SSL/TLS est défini comme : protocoles cryptographiques sécurisant les communications web._

<br>

---

## T

### TypeScript

!!! note "Définition"
    Sur-ensemble typé de JavaScript ajoutant un système de types statique.

Utilisé pour développer des applications JavaScript plus robustes et maintenables.

- **Fonctionnalités :** typage statique, interfaces, generics, enums
- **Adoption :** natif dans Angular, standard dans les gros projets Node.js

```mermaid
graph TB
    A[TypeScript] --> B[JavaScript]
    A --> C[Types]
    A --> D[Compilation]
```

_Explication : TypeScript est défini comme : sur-ensemble typé de JavaScript ajoutant un système de types statique._

<br>

---

## V

### Vue.js

!!! note "Définition"
    Framework JavaScript progressif pour construire des interfaces utilisateur réactives.

Utilisé pour créer des applications web avec une courbe d'apprentissage douce.

- **Caractéristiques :** template syntax HTML, réactivité déclarative, composants
- **Écosystème :** Vue Router, Pinia, Nuxt.js (SSR)

```mermaid
graph TB
    A[Vue.js] --> B[Framework progressif]
    A --> C[Templates]
    A --> D[Réactivité]
```

_Explication : Vue.js est défini comme : framework JavaScript progressif pour construire des interfaces utilisateur réactives._

<br>

---

### Virtual DOM

!!! note "Définition"
    Représentation virtuelle légère du DOM réel pour optimiser les performances de rendu.

Utilisé par React pour minimiser les opérations DOM coûteuses via la réconciliation.

- **Principe :** diff algorithm → mise à jour minimale du DOM réel
- **Avantages :** performance, prédictabilité, testabilité sans navigateur

```mermaid
graph TB
    A[Virtual DOM] --> B[DOM réel]
    A --> C[Performance]
    A --> D[React]
```

_Explication : Virtual DOM est défini comme : représentation virtuelle légère du DOM réel pour optimiser les performances de rendu._

<br>

---

## W

### Webpack

!!! note "Définition"
    Bundler de modules construisant des bundles optimisés pour les applications web.

Utilisé pour empaqueter, transformer et optimiser tous les assets d'une application.

- **Concepts :** entry points, loaders, plugins, code splitting
- **Fonctionnalités :** hot module replacement (HMR), tree shaking, lazy loading

```mermaid
graph TB
    A[Webpack] --> B[Bundling]
    A --> C[Modules]
    A --> D[Optimisation]
```

_Explication : Webpack est défini comme : bundler de modules construisant des bundles optimisés pour les applications web._

<br>

---

### WebSocket

!!! note "Définition"
    Protocole de communication bidirectionnelle full-duplex persistante entre client et serveur.

Utilisé pour les applications temps réel nécessitant des échanges fréquents et à faible latence.

- **Applications :** chat, gaming, trading, notifications live, collaboration
- **Avantages :** connexion persistante, faible latence, full-duplex

```mermaid
graph TB
    A[WebSocket] --> B[Temps réel]
    A --> C[Bidirectionnel]
    A --> D[Full-duplex]
```

_Explication : WebSocket est défini comme : protocole de communication bidirectionnelle full-duplex persistante entre client et serveur._

<br>

---

### WYSIWYG

!!! note "Définition"
    Éditeur permettant de visualiser le résultat final pendant la saisie du contenu.

Utilisé dans les CMS pour simplifier la création de contenu sans connaissance HTML.

- **Acronyme :** What You See Is What You Get
- **Exemples :** TinyMCE, CKEditor, Quill

```mermaid
graph TB
    A[WYSIWYG] --> B[Éditeur]
    A --> C[CMS]
    A --> D[Contenu]
```

_Explication : WYSIWYG est défini comme : éditeur permettant de visualiser le résultat final pendant la saisie du contenu._

<br>

---

## X

### XSS

!!! note "Définition"
    Attaque injectant des scripts malveillants dans des pages web légitimes.

Utilisé pour voler des sessions, données utilisateur ou rediriger vers des sites malveillants.

- **Acronyme :** Cross-Site Scripting
- **Types :** reflected (URL), stored (base de données), DOM-based
- **Protection :** encodage des sorties, Content Security Policy (CSP)

```mermaid
graph TB
    A[XSS] --> B[Attaque]
    A --> C[Script injection]
    A --> D[Sécurité web]
```

_Explication : XSS est défini comme : attaque injectant des scripts malveillants dans des pages web légitimes._

<br>

---

### XML

!!! note "Définition"
    Langage de balisage extensible pour structurer et échanger des données hiérarchiques.

Utilisé pour la configuration, les échanges inter-systèmes et les formats de documents.

- **Acronyme :** eXtensible Markup Language
- **Applications :** SOAP, RSS, configs, formats Office (docx, xlsx)

```mermaid
graph TB
    A[XML] --> B[Balisage]
    A --> C[Structure]
    A --> D[SOAP]
```

_Explication : XML est défini comme : langage de balisage extensible pour structurer et échanger des données hiérarchiques._

<br>
