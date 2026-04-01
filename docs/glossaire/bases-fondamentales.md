---
description: "Glossaire — Bases Fondamentales : Algorithmique, programmation, structures de données et architecture des systèmes."
icon: lucide/book-a
tags: ["GLOSSAIRE", "BASES", "ALGORITHMIQUE", "PROGRAMMATION"]
---

# Bases Fondamentales

<div
  class="omny-meta"
  data-level="🟢 Tout niveau"
  data-version="1.0"
  data-time="Consultation">
</div>

## A

!!! note "Algorithme"
    > Séquence d'instructions logiques et ordonnées pour résoudre un problème ou effectuer une tâche spécifique.

    Utilisé en programmation, recherche opérationnelle, intelligence artificielle et optimisation.

    - **Synonymes :** procédure, méthode, processus algorithmique

    ```mermaid
    graph LR
        A[Algorithme] --> B[Structure de données]
        A --> C[Complexité]
        A --> D[Programme]
    ```

<br>

---

!!! note "API"
    > Interface de programmation permettant la communication et l'échange de données entre différents logiciels ou services.

    Essentiel dans l'architecture microservices, développement web et intégration de systèmes.

    - **Acronyme :** Application Programming Interface
    - **Variantes :** REST API, GraphQL API, SOAP API

    ```mermaid
    graph LR
        A[API] --> B[Microservices]
        A --> C[Intégration]
        A --> D[Protocole HTTP]
    ```

<br>

---

!!! note "ASCII"
    > Standard d'encodage de caractères utilisant 7 bits pour représenter 128 caractères différents.

    Utilisé pour la compatibilité entre systèmes, protocoles de communication et encodage de base.

    - **Acronyme :** American Standard Code for Information Interchange
    - **Extension :** ASCII étendu (8 bits, 256 caractères)

    ```mermaid
    graph LR
        A[ASCII] --> B[UTF-8]
        A --> C[Encodage]
        A --> D[Compatibilité]
    ```

<br>

---

## B

!!! note "Big O"
    > Notation mathématique décrivant la complexité algorithmique dans le pire des cas en fonction de la taille des données.

    Utilisé pour analyser et comparer l'efficacité des algorithmes.

    - **Variantes :** Θ (Theta), Ω (Omega), o (petit o)

    ```mermaid
    graph LR
        A[Big O] --> B[Algorithme]
        A --> C[Performance]
        A --> D[Optimisation]
    ```

<br>

---

!!! note "Binaire"
    > Système de numération en base 2 utilisant uniquement les chiffres 0 et 1, langage fondamental des ordinateurs.

    Utilisé dans tous les systèmes informatiques, représentation des données et logique booléenne.

    - **Variantes :** BCD (Binary Coded Decimal), Gray code

    ```mermaid
    graph LR
        A[Binaire] --> B[Bit]
        A --> C[Octet]
        A --> D[Processeur]
    ```

<br>

---

!!! note "Bit"
    > Plus petite unité d'information en informatique, peut valoir 0 ou 1.

    Utilisé pour mesurer la capacité de stockage et la vitesse de transmission.

    - **Variantes :** kb (kilobit), Mb (mégabit), Gb (gigabit)

    ```mermaid
    graph LR
        A[Bit] --> B[Octet]
        A --> C[Binaire]
        A --> D[Données]
    ```

<br>

---

!!! note "Byte"
    > Unité d'information composée de 8 bits, capable de représenter 256 valeurs différentes.

    Utilisé pour mesurer la taille des fichiers et la capacité mémoire.

    - **Synonyme :** Octet
    - **Variantes :** KB (kilobyte), MB (mégabyte), GB (gigabyte)

    ```mermaid
    graph LR
        A[Byte] --> B[Bit]
        A --> C[Mémoire]
        A --> D[Stockage]
    ```

<br>

---

## C

!!! note "Cache"
    > Mémoire rapide stockant temporairement des données fréquemment utilisées pour accélérer les accès.

    Utilisé dans les processeurs, navigateurs web, bases de données et systèmes distribués.

    - **Types :** Cache L1/L2/L3, cache web, cache applicatif

    ```mermaid
    graph LR
        A[Cache] --> B[Mémoire]
        A --> C[Performance]
        A --> D[Processeur]
    ```

<br>

---

!!! note "Compilation"
    > Processus de traduction du code source écrit par un programmeur en code machine exécutable par l'ordinateur.

    Utilisé dans le développement logiciel avec des langages comme C, C++, Rust, Go.

    - **Antonyme :** Interprétation
    - **Types :** AOT (Ahead-of-Time), JIT (Just-in-Time)

    ```mermaid
    graph LR
        A[Compilation] --> B[Code source]
        A --> C[Code machine]
        A --> D[Exécution]
    ```

<br>

---

!!! note "Complexité temporelle"
    > Mesure du temps d'exécution d'un algorithme en fonction de la taille des données d'entrée.

    Utilisé pour l'analyse d'algorithmes et l'optimisation de performance.

    - **Notation :** Big O, Theta, Omega

    ```mermaid
    graph LR
        A[Complexité temporelle] --> B[Big O]
        A --> C[Algorithme]
        A --> D[Performance]
    ```

<br>

---

## D

!!! note "Débogage"
    > Processus d'identification, d'analyse et de correction des erreurs dans un programme informatique.

    Utilisé durant le développement logiciel et la maintenance applicative.

    - **Synonyme :** Debug
    - **Outils :** debugger, breakpoints, logs

    ```mermaid
    graph LR
        A[Débogage] --> B[Bug]
        A --> C[Test]
        A --> D[Qualité logicielle]
    ```

<br>

---

!!! note "DFS"
    > Algorithme de parcours d'arbres ou de graphes explorant aussi profondément que possible avant de revenir en arrière.

    Utilisé en intelligence artificielle, résolution de problèmes et analyse de graphes.

    - **Acronyme :** Depth-First Search
    - **Antonyme :** BFS (Breadth-First Search)

    ```mermaid
    graph LR
        A[DFS] --> B[Graphe]
        A --> C[Arbre]
        A --> D[BFS]
    ```

<br>

---

## E

!!! note "Encodage"
    > Processus de conversion de données dans un format spécifique selon des règles définies.

    Utilisé pour la représentation de caractères, compression et transmission de données.

    - **Types :** UTF-8, ASCII, Base64, URL encoding

    ```mermaid
    graph LR
        A[Encodage] --> B[ASCII]
        A --> C[UTF-8]
        A --> D[Données]
    ```

<br>

---

## F

!!! note "Fonction"
    > Bloc de code réutilisable effectuant une tâche spécifique, pouvant recevoir des paramètres et retourner une valeur.

    Utilisé dans tous les paradigmes de programmation pour la modularité et la réutilisabilité.

    - **Synonymes :** méthode, procédure, routine
    - **Types :** fonction pure, fonction récursive, fonction lambda

    ```mermaid
    graph LR
        A[Fonction] --> B[Paramètre]
        A --> C[Valeur de retour]
        A --> D[Modularité]
    ```

<br>

---

!!! note "Framework"
    > Structure logicielle préconçue fournissant une base et des outils pour développer des applications.

    Utilisé pour accélérer le développement et standardiser l'architecture.

    - **Types :** framework web, framework mobile, framework de test
    - **Exemples :** React, Django, Spring

    ```mermaid
    graph LR
        A[Framework] --> B[Bibliothèque]
        A --> C[Architecture]
        A --> D[Développement]
    ```

<br>

---

## G

!!! note "Garbage Collection"
    > Processus automatique de libération de la mémoire occupée par des objets qui ne sont plus utilisés.

    Utilisé dans les langages managés comme Java, C#, Python pour éviter les fuites mémoire.

    - **Synonyme :** ramasse-miettes
    - **Types :** mark-and-sweep, generational GC, reference counting

    ```mermaid
    graph LR
        A[Garbage Collection] --> B[Gestion mémoire]
        A --> C[Performance]
        A --> D[Langage managé]
    ```

<br>

---

!!! note "Git"
    > Système de contrôle de version distribué permettant de suivre les modifications de fichiers et de collaborer.

    Utilisé dans le développement logiciel pour le versioning et la collaboration.

    - **Commandes principales :** `add`, `commit`, `push`, `pull`, `merge`
    - **Plateformes :** GitHub, GitLab, Bitbucket

    ```mermaid
    graph LR
        A[Git] --> B[Version control]
        A --> C[Collaboration]
        A --> D[Repository]
    ```

<br>

---

## H

!!! note "Hash"
    > Fonction mathématique transformant des données de taille arbitraire en une empreinte de taille fixe.

    Utilisé pour l'intégrité des données, l'indexation et la cryptographie.

    - **Synonymes :** hachage, empreinte
    - **Algorithmes :** MD5, SHA-256, bcrypt

    ```mermaid
    graph LR
        A[Hash] --> B[Cryptographie]
        A --> C[Intégrité]
        A --> D[Table de hachage]
    ```

<br>

---

!!! note "Heap"
    > Structure de données arborescente où chaque nœud parent est ordonné par rapport à ses enfants / Zone mémoire pour allocation dynamique.

    Utilisé dans les algorithmes de tri, files de priorité et gestion mémoire.

    - **Types :** max-heap, min-heap, binary heap
    - **Distinction :** heap (structure de données) vs heap (zone mémoire)

    ```mermaid
    graph LR
        A[Heap] --> B[Arbre binaire]
        A --> C[File de priorité]
        A --> D[Gestion mémoire]
    ```

<br>

---

!!! note "Hexadécimal"
    > Système de numération en base 16 utilisant les chiffres 0-9 et les lettres A-F.

    Utilisé pour représenter les adresses mémoire, codes couleur et données binaires.

    - **Notation :** préfixe `0x` (ex. `0xFF`), préfixe `#` (ex. `#FF0000`)

    ```mermaid
    graph LR
        A[Hexadécimal] --> B[Binaire]
        A --> C[Adresse mémoire]
        A --> D[Code couleur]
    ```

<br>

---

## I

!!! note "IDE"
    > Environnement de développement intégré combinant éditeur de code, débogueur, compilateur et autres outils.

    Utilisé pour augmenter la productivité des développeurs.

    - **Acronyme :** Integrated Development Environment
    - **Exemples :** VS Code, IntelliJ, Eclipse

    ```mermaid
    graph LR
        A[IDE] --> B[Éditeur]
        A --> C[Débogueur]
        A --> D[Productivité]
    ```

<br>

---

!!! note "Interprétation"
    > Exécution directe du code source ligne par ligne sans compilation préalable.

    Utilisé dans les langages de script comme Python, JavaScript, Ruby.

    - **Antonyme :** Compilation
    - **Avantages :** flexibilité, développement rapide

    ```mermaid
    graph LR
        A[Interprétation] --> B[Code source]
        A --> C[Exécution directe]
        A --> D[Compilation]
    ```

<br>

---

## J

!!! note "JIT"
    > Technique de compilation à la volée pendant l'exécution du programme pour optimiser les performances.

    Utilisé dans les machines virtuelles comme JVM, .NET CLR.

    - **Acronyme :** Just-In-Time compilation
    - **Avantage :** optimisations runtime spécifiques à l'environnement d'exécution

    ```mermaid
    graph LR
        A[JIT] --> B[Machine virtuelle]
        A --> C[Optimisation]
        A --> D[Performance]
    ```

<br>

---

## L

!!! note "Langage de programmation"
    > Syntaxe formelle permettant d'écrire des instructions compréhensibles par un ordinateur.

    Utilisé pour créer des logiciels, applications et systèmes.

    - **Types :** compilés, interprétés, hybrides
    - **Paradigmes :** impératif, orienté objet, fonctionnel

    ```mermaid
    graph LR
        A[Langage de programmation] --> B[Paradigme]
        A --> C[Syntaxe]
        A --> D[Programme]
    ```

<br>

---

!!! note "Liste chaînée"
    > Structure de données linéaire où chaque élément contient des données et un pointeur vers l'élément suivant.

    Utilisé pour l'implémentation de structures dynamiques et algorithmes.

    - **Types :** simple, double, circulaire
    - **Avantages :** insertion/suppression efficaces en O(1) si le nœud est connu

    ```mermaid
    graph LR
        A[Liste chaînée] --> B[Pointeur]
        A --> C[Nœud]
        A --> D[Structure dynamique]
    ```

<br>

---

## M

!!! note "Mémoire virtuelle"
    > Technique permettant d'utiliser l'espace disque comme extension de la mémoire physique.

    Utilisé par les systèmes d'exploitation pour gérer la mémoire efficacement.

    - **Mécanismes :** pagination, segmentation, swap
    - **Avantages :** isolation des processus, gestion transparente pour les applications

    ```mermaid
    graph LR
        A[Mémoire virtuelle] --> B[Pagination]
        A --> C[Mémoire physique]
        A --> D[Système d'exploitation]
    ```

<br>

---

## O

!!! note "Objet"
    > Instance d'une classe en programmation orientée objet, combinant données et méthodes.

    Utilisé pour modéliser des entités du monde réel dans le code.

    - **Concepts liés :** encapsulation, héritage, polymorphisme
    - **Langages :** Java, C++, Python, C#

    ```mermaid
    graph LR
        A[Objet] --> B[Classe]
        A --> C[Encapsulation]
        A --> D[POO]
    ```

<br>

---

## P

!!! note "Pile"
    > Structure de données LIFO où les éléments sont ajoutés et retirés par le même bout.

    Utilisé pour la gestion des appels de fonctions, expressions arithmétiques et algorithmes de parcours.

    - **Acronyme :** LIFO (Last In, First Out)
    - **Opérations :** push, pop, top/peek

    ```mermaid
    graph LR
        A[Pile] --> B[LIFO]
        A --> C[Appel de fonction]
        A --> D[File]
    ```

<br>

---

!!! note "Pointeur"
    > Variable contenant l'adresse mémoire d'une autre variable ou structure de données.

    Utilisé dans les langages de bas niveau pour la gestion directe de la mémoire.

    - **Langages :** C, C++, Assembly
    - **Risques :** segmentation fault, memory leak

    ```mermaid
    graph LR
        A[Pointeur] --> B[Adresse mémoire]
        A --> C[Référence]
        A --> D[Gestion mémoire]
    ```

<br>

---

!!! note "Polymorphisme"
    > Capacité d'un objet à prendre plusieurs formes selon le contexte d'utilisation.

    Utilisé en programmation orientée objet pour la flexibilité et l'extensibilité du code.

    - **Types :** polymorphisme de sous-type, paramétrique, ad-hoc
    - **Mécanismes :** surcharge, redéfinition, interfaces

    ```mermaid
    graph LR
        A[Polymorphisme] --> B[Héritage]
        A --> C[Interface]
        A --> D[POO]
    ```

<br>

---

## R

!!! note "Récursivité"
    > Technique de programmation où une fonction s'appelle elle-même pour résoudre un problème.

    Utilisé pour résoudre des problèmes décomposables en sous-problèmes similaires.

    - **Éléments :** cas de base (condition d'arrêt), cas récursif
    - **Exemples :** factorielle, suite de Fibonacci, parcours d'arbres

    ```mermaid
    graph LR
        A[Récursivité] --> B[Fonction]
        A --> C[Cas de base]
        A --> D[Appel récursif]
    ```

<br>

---

!!! note "Refactoring"
    > Processus de restructuration du code existant sans modifier son comportement externe.

    Utilisé pour améliorer la lisibilité, maintenabilité et performance du code sans régression fonctionnelle.

    - **Techniques :** extraction de méthode, renommage, simplification conditionnelle
    - **Outils :** IDE automatisés, analyseurs de code statique

    ```mermaid
    graph LR
        A[Refactoring] --> B[Code legacy]
        A --> C[Maintenabilité]
        A --> D[Qualité logicielle]
    ```

<br>

---

## S

!!! note "Structure de données"
    > Organisation logique et systématique des données en mémoire pour faciliter leur manipulation.

    Utilisé pour optimiser les opérations et l'utilisation de la mémoire selon les cas d'usage.

    - **Types :** linéaires (tableaux, listes), non-linéaires (arbres, graphes)
    - **Critères de choix :** complexité temporelle/spatiale, opérations fréquentes

    ```mermaid
    graph LR
        A[Structure de données] --> B[Algorithme]
        A --> C[Complexité]
        A --> D[Mémoire]
    ```

<br>

---

## T

!!! note "Table de hachage"
    > Structure de données associant des clés à des valeurs via une fonction de hachage pour un accès rapide.

    Utilisé pour l'implémentation de dictionnaires, caches et index avec une complexité moyenne O(1).

    - **Synonymes :** hash table, hash map, dictionnaire
    - **Gestion des collisions :** chaînage, adressage ouvert

    ```mermaid
    graph LR
        A[Table de hachage] --> B[Fonction de hachage]
        A --> C[Clé-valeur]
        A --> D[Collision]
    ```

<br>

---

!!! note "TDD"
    > Méthodologie de développement où les tests unitaires sont écrits avant le code de production.

    Utilisé pour améliorer la qualité du code et garantir la couverture de tests dès la conception.

    - **Acronyme :** Test-Driven Development
    - **Cycle :** Red → Green → Refactor

    ```mermaid
    graph LR
        A[TDD] --> B[Test unitaire]
        A --> C[Code de production]
        A --> D[Refactoring]
    ```

<br>

---

## U

!!! note "UTF-8"
    > Standard d'encodage Unicode utilisant 1 à 4 octets par caractère, rétro-compatible ASCII.

    Utilisé pour représenter tous les caractères Unicode dans les applications modernes. Standard de fait sur le web.

    - **Acronyme :** Unicode Transformation Format 8-bit
    - **Avantages :** compatibilité ASCII, efficacité pour le latin, universalité

    ```mermaid
    graph LR
        A[UTF-8] --> B[Unicode]
        A --> C[ASCII]
        A --> D[Encodage]
    ```

<br>

---

## V

!!! note "Variable"
    > Espace mémoire nommé capable de stocker une valeur qui peut être modifiée pendant l'exécution.

    Utilisé dans tous les langages de programmation pour manipuler les données.

    - **Types :** locale, globale, statique, dynamique
    - **Propriétés :** type de donnée, portée (scope), durée de vie

    ```mermaid
    graph LR
        A[Variable] --> B[Mémoire]
        A --> C[Type de données]
        A --> D[Portée]
    ```

<br>

---

!!! note "Version control"
    > Système de suivi et de gestion des modifications apportées aux fichiers au fil du temps.

    Utilisé dans le développement logiciel pour la collaboration, l'historique et la gestion des branches.

    - **Synonyme :** contrôle de version, SCM (Source Code Management)
    - **Systèmes :** Git, SVN, Mercurial

    ```mermaid
    graph LR
        A[Version control] --> B[Git]
        A --> C[Collaboration]
        A --> D[Historique]
    ```

<br>
