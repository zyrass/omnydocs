---
title: "EVALUATION-2026 — Audit qualité du contenu pédagogique omnydocs"
description: "Évaluation indépendante, transparente et hiérarchisée de la qualité des cours, et adéquation au but : bâtir un cursus TALL (Tailwind v4 / PHP 8.4+ / Laravel 13 / Livewire 4 / Flux UI) avec compléments Python et mobile Apple."
auteur: "Audit automatisé (agent IA)"
date: "2026-06-27"
statut: "Rapport d'évaluation — aucune suppression de contenu effectuée"
---

# EVALUATION-2026 — Audit qualité du contenu pédagogique

> Transparence préalable : ce rapport est une **évaluation**, pas une modification. Aucun fichier de `docs/` n'a été supprimé, déplacé ou réécrit. Les constats négatifs sont assumés et argumentés. Les éléments que je n'ai pas pu vérifier (faits postérieurs à mai 2025 : dates de release réelles de Laravel 13, détails Tailwind v4) sont signalés explicitement comme **non vérifiés**.

---

## 1. Objectif et contexte

L'objectif déclaré est de transformer ce corpus en un **cursus professionnel structuré** permettant d'enseigner :

1. La stack **TALL** dans ses versions cibles : **Tailwind v4 / PHP 8.4+ / Laravel 13 / Livewire 4 / Flux UI**.
2. De **bonnes connaissances Python**.
3. Une **stack mobile Apple** solide en complément (Swift / SwiftUI / Vapor).

La question posée est double : **(a)** les cours sont-ils de qualité ? **(b)** cette sélection de chemins permet-elle un cursus « digne d'intérêt » ?

### Méthodologie d'évaluation (ce que j'ai réellement fait)

| Niveau d'analyse | Couverture |
|---|---|
| Cartographie exhaustive (arborescence, comptage fichiers, profondeur en mots) | 100 % du périmètre demandé + dossiers connexes (`stacks/tall`, `cyber/governance`) |
| Vérification des versions enseignées (grep ciblé : Tailwind v3/v4, Livewire 3/4, Laravel 11/12/13, PHP 8.x, Flux, Composer) | 100 % des dossiers frameworks et stack |
| Lecture intégrale d'échantillons représentatifs | PHP (sécurité/patterns), Livewire, Tailwind, Cyber GRC, Linux/Fail2Ban, arch-lab, rapports d'auto-audit |
| Lecture de survol (frontmatter, structure, métadonnées) | Reste du corpus |

Limite assumée : je n'ai pas relu **ligne à ligne** les ~300 fichiers. Les scores de qualité reposent sur des échantillons jugés représentatifs + des indicateurs objectifs (profondeur, versions, structure). Là où un échantillon a révélé un défaut, je l'extrapole prudemment.

---

## 2. Synthèse exécutive (verdict)

**Verdict global : corpus de très bonne qualité d'ensemble, mais le cœur de cible — la stack TALL dans ses versions annoncées — est le maillon le plus faible et le plus fragmenté.**

En clair :

- La **base de connaissances générales** (fondamentaux, réseaux, PHP, modélisation, tests Pest, mobile Apple, gouvernance cyber) est **solide à excellente**. Plusieurs sections sont d'un niveau professionnel rare pour de la documentation pédagogique francophone.
- La **stack TALL elle-même**, dans les versions que tu veux enseigner (Tailwind **v4**, Livewire **4**, Laravel **13**, **Flux UI**), n'existe aujourd'hui qu'à l'état d'**annonce et de chapitre d'installation**. Le contenu réellement enseignable est encore en **Laravel 11, Livewire 3, Tailwind v3**.

Donc : **oui, la sélection peut fonder un cursus digne d'intérêt**, mais **non, en l'état elle n'enseigne pas encore la cible TALL revendiquée**. Il y a un écart entre la promesse (versions) et le livré (versions). C'est corrigeable, mais c'est le chantier prioritaire.

### Note globale par grand domaine

| Domaine | Note /5 | Commentaire d'une ligne |
|---|---|---|
| Bases (fondamentaux, formats, réseaux, concepts) | 4,0 | Solide, quelques fichiers « concepts » trop courts |
| Langages (HTML, CSS, JS, PHP, Python) | 4,0 | PHP exceptionnel ; JS et Python plus légers |
| Modélisation (Merise + UML) | 4,5 | Très complet, rare en français |
| Données (SQL, NoSQL, SQLite, GraphQL) | 4,0 | Progression SQLite très propre |
| Tests (Pest, Jest, Vitest) | 4,0 | Pest excellent ; Jest/Vitest corrects mais plus minces |
| **Stack TALL (Laravel/Livewire/Alpine/Tailwind/stack)** | **3,0** | **Fragmenté, en retard sur les versions cibles, Flux absent** |
| Mobile Apple (Swift, SwiftUI, Vapor) | 4,5 | Très complet et moderne |
| Homelab / Arch-Lab | 4,5 | Installation manuelle Arch détaillée, formateur |
| Système / Linux | 3,5 | Pédagogie correcte mais fiches courtes |
| Cyber — Gouvernance (GRC) | 4,5 | Couverture réglementaire actuelle et large |

---

## 3. Analyse technique détaillée par section

### 3.1 Bases — `docs/bases`

| Sous-section | Fichiers | Profondeur | Note | Constat |
|---|---|---|---|---|
| `fondamentaux` | 7 | 2 000–4 000 mots | 4,0 | Types primitifs, booléen, conditionnel, itératif, fonctions, heap/stack/références. Bon socle algorithmique transversal. |
| `formats-serialisation` | 5 | 2 400–3 200 mots | 4,0 | JSON, XML, YAML, CSV bien couverts. Pertinent (config, API, IaC). |
| `reseaux` | 6 | 3 000–4 350 mots | 4,5 | OSI, TCP/IP, HTTP (méthodes), DNS, liste de protocoles. Profond et bien dosé. |
| `concepts` | 9 | **très inégal** | 3,5 | `architecture-unix` (6 000 mots) excellent ; mais `solid` (1 168), `paradigmes` (925), `regex` (1 038), `design-patterns` (1 076), `encodage` (962) sont **trop courts** pour des sujets de cette importance. |

**Point de vigilance** : SOLID, paradigmes et design patterns à ~1 000 mots sont des survols, alors que ces notions sont structurantes pour un développeur. Ils sont d'ailleurs traités beaucoup plus en profondeur dans la section PHP (cf. 3.2) — il y a donc un **doublon partiel** et un déséquilibre à arbitrer (renvoyer depuis `concepts` vers PHP, ou inversement).

### 3.2 Langages — `docs/dev-cloud/lang`

| Langage | Fichiers | Note | Constat |
|---|---|---|---|
| **PHP** | 16 modules + index | **5,0** | **Point fort majeur du corpus.** Modules de 4 000 à 7 000 mots, du procédural à la POO, MVC, PDO, sécurité, design patterns, standards de production. Code conforme PHP 8 (`declare(strict_types=1)`, propriétés typées, nullable, constructeurs privés bien expliqués). Pédagogie : analogie + théorie + code testable + mises en garde (YAGNI, over-engineering). Niveau professionnel. |
| **CSS** | 13 | 4,5 | Sélecteurs, unités, box model, positionnement, Flexbox, Grid, responsive, animations, avancé. Complet et progressif. |
| **HTML** | 9 | 4,0 | Sémantique HTML5, formulaires, médias, éléments interactifs natifs (`<details>`, `<dialog>`). Moderne. |
| **JavaScript** | 10 | 3,5 | Découpage socle/moteur/application pertinent, ES6 bien traité (2 715 mots). Mais le **socle est mince** (`hello-console` 507, `bases-algorithmiques` 721, `fonctions-objets` 611). Asynchrone et DOM corrects mais courts. À renforcer si JS doit servir de base à Alpine/Livewire. |
| **Python** | 13 (dont Django 2, Flask 1, Tkinter 1) | 3,0 | `python.md` (1 746) + frameworks en **fondamentaux uniquement**. Suffisant pour « initier », **insuffisant pour de « bonnes connaissances »** revendiquées : pas de section data/scripting/sécurité Python, Django limité à 2 fichiers. À étoffer selon l'ambition réelle. |

### 3.3 Modélisation — `docs/dev-cloud/modelisation`

**Note : 4,5.** Merise complet (intro, MCD, MLD, MPD, MPD→SQL) **et** UML très large : 15 types de diagrammes (cas d'usage, classes, séquence, activité, état, composant, déploiement, objet, package, timing, communication, composite, profile, architecture avancée). Cette double couverture Merise + UML en français est rare et constitue un **atout différenciant** pour un cursus. Quelques fichiers UML courts (communication 761, timing 888) mais c'est cohérent avec l'importance relative de ces diagrammes. Bug mineur : `uml/diagrammes/index.md` ne contient que 3 mots (placeholder).

### 3.4 Données — `docs/dev-cloud/data`

**Note : 4,0.** Le sous-parcours **SQLite** (6 modules : installation → types → CRUD/contraintes → jointures → index/transactions → intégration PHP/Laravel) est une **progression exemplaire**, pertinente pour la TALL. Compléments SQL, NoSQL, PostgreSQL, GraphQL corrects (1 500–1 850 mots) mais davantage « panoramas » que masterclass. Cohérent.

### 3.5 Tests & Qualité — `docs/dev-cloud/tests-qualite`

| Outil | Fichiers | Note | Constat |
|---|---|---|---|
| **Pest** | 8 modules | **5,0** | Excellent : fondations, expectations, datasets/higher-order, testing Laravel, plugins, **TDD**, intégration, **CI/CD production**. 4 000–5 200 mots/module. Aligné stack PHP/Laravel. Vrai atout. |
| **Jest** | 5 | 3,5 | Fondamentaux, mocking, React Testing Library, Vue Test Utils, CI/CD. Corrects mais courts (800–1 150 mots). |
| **Vitest** | 4 | 3,5 | Intro/config, écriture, mocking, coverage/CI. Cohérent avec un front Vite, mais mince. |

Remarque : pour un cursus **TALL**, Pest est l'outil prioritaire et il est excellent. Jest/Vitest sont des compléments front légitimes mais secondaires.

### 3.6 Stack TALL — LE point critique

C'est ici que se joue l'adéquation au but. **Il existe non pas un, mais trois (voire quatre) parcours TALL/Laravel concurrents, avec des versions divergentes.** C'est le problème structurel n°1.

| Parcours | Emplacement | Versions enseignées | État réel | Note |
|---|---|---|---|---|
| Laravel « neuf » | `frameworks/laravel` | **Laravel 13 / Livewire 4 / Flux / Tailwind v4** (annoncés) | **Chapitre 00 uniquement** (installation, 10 leçons + structure/projet). Les 27 chapitres promis ne sont **pas écrits**. | 2,0 (comme cours) / la partie installation est bonne (4,0) |
| Laravel « old » | `frameworks/laravel_old` | **Laravel 11** | **Complet** (48 fichiers) | 4,0 (mais version périmée vs cible) |
| Stack TALL intégrée | `stacks/tall` | **Laravel 12 / Livewire 3 / Alpine 3 / PHP 8.4** ; Tailwind v4 cité dans la roadmap | Fichiers **massifs** (75 Ko, 40–60 Ko) mais `data-version` en **0.0.x** (brouillon) | 3,5 (contenu le plus utile, mais draft) |
| Livewire isolé | `frameworks/livewire` | **Livewire 3.x** | 5 leçons **minces** (~600 mots) | 2,5 |
| Alpine isolé | `frameworks/alpine` | Alpine 3 | 5 leçons **minces** (~550 mots) | 2,5 |
| Tailwind isolé | `frameworks/tailwind` | **Tailwind v3** intégral | 8 chapitres corrects | 3,0 (bon pour v3, **échoue la cible v4**) |

**Constats vérifiés (faits, pas opinions) :**

1. **Tailwind v4 n'est enseigné nulle part.** Le cours Tailwind est 100 % **v3** : `data-version="3.x"`, `tailwind.config.js`, `npx tailwindcss init -p`, directives `@tailwind base/components/utilities`, PostCSS + autoprefixer. Or v4 a changé le modèle de configuration (config CSS-first via `@import "tailwindcss"` et `@theme`, plugin `@tailwindcss/vite`, abandon du `tailwind.config.js` par défaut). Recherche `@import "tailwindcss"` / `@theme` / `@tailwindcss/vite` dans tout le corpus : **0 résultat**. Le cours Tailwind est donc **à réécrire** pour la cible v4.

2. **Flux UI n'a aucun contenu pédagogique.** Flux n'apparaît que dans les pages d'**annonce** du parcours Laravel neuf (présentation, « pourquoi Laravel », index). **Aucune leçon** n'enseigne Flux (composants, installation, free vs Pro). Pour un cursus qui pose Flux comme couche UI cible, c'est une **lacune totale** à combler.

3. **Livewire enseigné = v3, cible = v4.** Le contenu existant (`frameworks/livewire`) est explicitement `Livewire 3.x` et reste mince. Livewire 4 (nouveau moteur, nouvelle approche des composants single-file) n'est pas couvert.

4. **Fragmentation des versions Laravel : 11 (old) / 12 (stack tall) / 13 (neuf).** Trois sources de vérité incompatibles cohabitent. Un apprenant ne sait pas laquelle suivre.

**Conclusion section 3.6** : la matière première est là (la stack `stacks/tall` est volumineuse et bien construite, le PHP et Pest sont excellents), mais **aucun parcours ne livre aujourd'hui la cible TALL annoncée de bout en bout**. C'est le chantier qui conditionne la crédibilité de tout le cursus.

### 3.7 Mobile Apple — `docs/dev-cloud/mobile`

**Note : 4,5. Deuxième point fort du corpus.** 55 fichiers :

- **Swift** (18 modules) : couvre jusqu'aux sujets avancés et **modernes** — optionals, generics, property wrappers, **concurrence (async/await)**, ARC/mémoire, keypaths, result builders, Combine. C'est un vrai parcours langage complet.
- **SwiftUI** (18 modules) : vues, layout, **state/binding, `@Observable`** (API récente, bon signe d'actualité), navigation, MVVM, persistence, accessibilité, tests, App Store. Très complet.
- **Vapor** (12 modules) : backend Swift (routing, middleware, Fluent/migrations, JWT, API REST, queues, tests XCTVapor, déploiement). Cohérent avec l'idée « full-stack Swift ».

Pour le complément Apple demandé, **l'objectif est atteint et même dépassé**. Seule réserve : à maintenir dans le temps (SwiftUI évolue vite à chaque WWDC).

### 3.8 Homelab / Arch-Lab — `docs/projets/arch-lab`

**Note : 4,5.** 8 modules, dont `03-arch-serveur` à **10 000 mots** (installation manuelle Arch en UEFI/GPT + systemd-boot, 28 étapes). Démarche « comprendre chaque rouage » très formatrice, alignée avec un profil DevSecOps/cyber. Statut `beta` / `data-version 0.2` honnêtement déclaré. Réseau VirtualBox et lab multi-OS bien pensés.

### 3.9 Système / Linux — `docs/sys-reseau/linux`

**Note : 3,5.** 12 fichiers. Pédagogie correcte (analogie château-fort pour le durcissement, diagrammes Mermaid des « jails » Fail2Ban). **Mais fiches courtes** (~700–990 mots) : `admin`, `bash`, `services-daemons` et les outils sécurité (UFW, Fail2Ban, ClamAV, chkrootkit, Lynis, rkhunter/LMD, Vuls) sont des **fiches pratiques**, pas des cours approfondis. Utile en référentiel opérationnel ; insuffisant comme module d'apprentissage autonome. À étoffer (scénarios, exercices, journalisation/SIEM) selon l'ambition.

### 3.10 Cyber — Gouvernance (GRC) — `docs/cyber/governance`

**Note : 4,5. Troisième point fort.** Couverture **large et actuelle** :

- **Autorités** : ANSSI, CNIL, CLUSIF.
- **ISO** : 27000, 27001, 27002, 27005, 27017, 27018, + 9001, 14001, 20000, 22301, 31000.
- **Référentiels** : NIST CSF, PCI-DSS, HDS, SecNumCloud.
- **Réglementations UE récentes** : **RGPD, NIS2, DORA, AI Act, CRA, DSA, DMA, Data Act, DGA** + mapping ISO/NIS2.
- **SMSI** : PSSI, SDSI, BIA, gestion des risques (**EBIOS-RM**, ISO 27005, MEHARI).
- **Vulnérabilités** : CVE/CVSS, OWASP Top 10, patch management, scan policy.

L'inclusion de NIS2, DORA, AI Act et CRA montre une **veille réglementaire à jour** (textes 2022–2024). C'est exactement ce qu'on attend d'un volet gouvernance crédible. Réserve usuelle : ces textes évoluent (actes délégués, transpositions) — prévoir une revue annuelle.

---

## 4. Erreurs, incohérences et risques relevés (transparence totale)

Conformément à la demande, voici les défauts **factuels** identifiés, sans complaisance.

| # | Gravité | Localisation | Problème | Recommandation |
|---|---|---|---|---|
| 1 | **Élevée** | `frameworks/tailwind/*` | Cours 100 % Tailwind **v3** alors que la cible est **v4** (modèle de config totalement différent). | Réécrire pour v4 (`@import "tailwindcss"`, `@theme`, `@tailwindcss/vite`). |
| 2 | **Élevée** | Tout le périmètre TALL | **Flux UI** : aucun contenu pédagogique, seulement des annonces. | Créer un module Flux dédié (install, composants, Free/Pro, intégration Livewire 4). |
| 3 | **Élevée** | `frameworks/laravel` | Parcours « Laravel 13 » réduit au **chapitre 00**. Les 27 chapitres sont une promesse non tenue. | Soit écrire la suite, soit retirer l'annonce des 27 chapitres pour ne pas tromper l'apprenant. |
| 4 | **Élevée** | `laravel` vs `laravel_old` vs `stacks/tall` | **Fragmentation des versions** : Laravel 11/12/13, Livewire 3/4 cohabitent sans hiérarchie claire. | Désigner **une** source de vérité par sujet ; archiver explicitement `laravel_old`. |
| 5 | Moyenne | `stacks/tall/01-installation.md`, `03-fondations.md`, `index.md` | Mention **« Composer 3+ »**. Composer 3 **n'existe pas** (Composer 2 est la version courante à ma date de connaissance, mai 2025). Probable erreur. | Vérifier sur getcomposer.org et corriger en « Composer 2 » sauf release v3 confirmée. |
| 6 | Moyenne | `frameworks/laravel/chapitre-00/01` et `02` | Laravel 13 qualifié de **« LTS »** / « branche LTS courante ». Laravel **n'a plus de LTS** depuis la 5.1 ; toutes les versions suivent le même cycle (≈2 ans de correctifs). | Corriger : parler de « cycle de support standard », pas de LTS. |
| 7 | Moyenne | `php/15-securite-avancee.md` | Le fichier **nommé « securite-avancee » contient en réalité « XV - Design Patterns »** (titre + frontmatter), doublonnant `12-design-patterns.md`. | Vérifier : soit renommer, soit remettre le vrai contenu sécurité avancée. |
| 8 | **À vérifier** | `laravel/chapitre-00/*` | Affirmations **postérieures à mai 2025** présentées comme faits : « Laravel 13 publié le 17 mars 2026 », « AI SDK first-party stable », « Breeze plus maintenu », dates EOL 2027/2028. **Je ne peux pas les vérifier** (au-delà de ma date de connaissance). | Sourcer chaque affirmation sur la doc officielle / laravel-news avant publication. Ne pas présenter une roadmap comme un fait acquis. |
| 9 | Faible | `bases/concepts` | SOLID/paradigmes/regex/design-patterns trop courts (~1 000 mots) **et** redondants avec PHP. | Arbitrer : approfondir dans `concepts` (langage-agnostique) et renvoyer depuis PHP, ou l'inverse. |
| 10 | Faible | Global | Usage intensif d'**émojis** dans le contenu (✅ ❌ 🔴 🟡 🟢) — en contradiction avec tes propres standards éditoriaux (« n'utilise jamais d'émojis »). | Décider d'une règle unique et l'appliquer (les émojis de niveau peuvent être remplacés par des libellés). |
| 11 | Faible | `uml/diagrammes/index.md` | Fichier quasi vide (3 mots, placeholder). | Compléter ou supprimer du sommaire. |

---

## 5. Adéquation au but : ce cursus est-il « digne d'intérêt » ?

### 5.1 Pour enseigner la TALL (cible v4 / 8.4 / L13 / Lw4 / Flux)

**Partiellement, pas encore en l'état.**

- Les **fondations** sont excellentes : PHP (5/5), Pest (5/5), SQLite, modélisation, CSS/HTML. Un apprenant arrivant sur Laravel aura un socle solide.
- Mais la **couche TALL terminale** (Laravel 13, Livewire 4, Tailwind v4, Flux) est **incomplète et en retard de version**. Aujourd'hui, on peut enseigner **Laravel 11 + Livewire 3 + Tailwind v3** (réel, complet), pas la cible annoncée.
- **Verdict** : la sélection est une **excellente rampe d'accès** vers la TALL, mais le **palier final reste à construire**. C'est l'effort prioritaire.

### 5.2 Pour de « bonnes connaissances » Python

**Insuffisant pour l'ambition affichée.** Le Python est au stade « initiation » (fondamentaux + frameworks en 1–2 fichiers). Acceptable comme culture générale, à étoffer si « bonnes connaissances » signifie autonomie réelle (data, scripting sécurité, Django complet).

### 5.3 Pour une stack mobile Apple en complément

**Objectif atteint et dépassé.** Swift + SwiftUI + Vapor forment un parcours complet, moderne et cohérent (full-stack Swift). C'est l'un des points forts.

### 5.4 Pour le profil DevSecOps / Cyber

**Très bon.** Gouvernance GRC actuelle et large, arch-lab formateur, fiches Linux de durcissement, et un cursus forensic massif (non demandé ici mais présent : ~5 cycles). Cohérent avec ton orientation.

---

## 6. Recommandations priorisées

### Priorité 1 — Rendre la cible TALL réelle (sinon la promesse est vide)

1. **Trancher la fragmentation** : choisir **une** ligne de version par techno et l'afficher (proposition réaliste : Laravel 12 **ou** 13 selon disponibilité officielle vérifiée, Livewire 3→4 selon stabilité réelle, Tailwind **v4**, PHP 8.4). Archiver `laravel_old` et `frameworks/livewire|alpine|tailwind` isolés, ou les marquer « legacy/v3 ».
2. **Réécrire le module Tailwind en v4** (config CSS-first, `@theme`, plugin Vite).
3. **Créer un module Flux UI** de zéro (il n'existe pas).
4. **Écrire la suite du parcours Laravel** au-delà du chapitre 00, ou aligner l'annonce sur le livré.
5. **Consolider `stacks/tall`** (le plus avancé) comme parcours TALL canonique et sortir son `data-version` du stade 0.0.x.

### Priorité 2 — Fiabilité factuelle

6. Corriger les erreurs #5 (Composer 3), #6 (Laravel « LTS »), #7 (fichier PHP 15 mal nommé).
7. Sourcer toutes les affirmations postérieures à 2025 (#8) sur la doc officielle.

### Priorité 3 — Combler les creux

8. Renforcer le **socle JavaScript** (utile avant Alpine/Livewire).
9. Décider du niveau **Python** visé et étoffer en conséquence.
10. Approfondir **SOLID / design patterns / regex** dans `concepts` (et dédoublonner avec PHP).
11. Étoffer **Linux** (scénarios, exercices, supervision/journalisation).

### Priorité 4 — Cohérence éditoriale

12. Règle unique sur les **émojis**.
13. Uniformiser les **conventions de nommage** (`0X-titre.md` partout, comme le notent déjà tes propres rapports d'auto-audit).
14. Nettoyer les **placeholders** (ex. `uml/diagrammes/index.md`).

---

## 7. Note de transparence et limites

- **Aucune suppression** n'a été effectuée. Ce fichier est purement additif.
- Les scores reposent sur des **échantillons + indicateurs objectifs**, pas sur une relecture exhaustive ligne à ligne des ~300 fichiers. Un défaut isolé peut exister dans un fichier non échantillonné.
- Tout ce qui concerne des **faits postérieurs à mai 2025** (releases Laravel 13/Tailwind v4, dates EOL, état de Livewire 4, existence de Composer 3) est signalé comme **non vérifié de mon côté** et doit être confirmé sur les sources officielles avant toute publication. Je n'ai pas affirmé qu'ils étaient faux — j'ai signalé que ton contenu les présente comme acquis sans que je puisse les valider.
- Le dispositif d'**auto-audit** (`00-rapport-formation-*.md`) présent dans plusieurs sections est une bonne pratique : il documente déjà certaines limites (nommage, longueur des fichiers). À conserver et systématiser.

---

## 8. Annexe — Inventaire de profondeur (périmètre demandé)

Profondeur indicative en nombre de mots par section (hors `index`/`rapport`).

| Section | Fichiers .md | Fourchette (mots) |
|---|---|---|
| bases/fondamentaux | 7 | 784 – 4 084 |
| bases/formats-serialisation | 5 | 758 – 3 156 |
| bases/reseaux | 6 | 344 – 4 348 |
| bases/concepts | 9 | 753 – 6 032 |
| dev-cloud/lang/html | 9 | 290 – 3 210 |
| dev-cloud/lang/css | 13 | 365 – 3 393 |
| dev-cloud/lang/javascript | 10 | 332 – 2 715 |
| dev-cloud/lang/php | 18 | 426 – 6 973 |
| dev-cloud/lang/python | 13 | 189 – 1 746 |
| dev-cloud/modelisation | 27 | 3 – 3 079 |
| dev-cloud/data | 13 | 170 – 2 068 |
| dev-cloud/tests-qualite/pest | 10 | 199 – 5 166 |
| dev-cloud/tests-qualite/jest | 7 | 242 – 1 150 |
| dev-cloud/tests-qualite/vitest | 6 | 152 – 1 437 |
| dev-cloud/frameworks/laravel (neuf, ch.00) | 14 | 618 – 3 535 |
| dev-cloud/frameworks/laravel_old | 48 | (Laravel 11, complet) |
| dev-cloud/frameworks/livewire | 7 | 188 – 715 |
| dev-cloud/frameworks/alpine | 7 | 301 – 664 |
| dev-cloud/frameworks/tailwind (v3) | 10 | 298 – 1 788 |
| dev-cloud/stacks/tall (non listé mais central) | 11 | gros fichiers 40–75 Ko, draft 0.0.x |
| dev-cloud/mobile (swift/swiftui/vapor) | 55 | 756 – 2 848 |
| projets/arch-lab | 8 | 2 563 – 10 045 |
| sys-reseau/linux | 12 | 382 – 991 |
| cyber/governance | 48 | (couverture GRC large et actuelle) |

*Fin du rapport EVALUATION-2026.*
