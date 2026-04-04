# Audit Complet — Section Développement (`docs/dev-cloud`)

> **Date :** Avril 2026 | **Référentiel :** SKILL v2.0.0 (Zensical) | **Version :** 4.0 FINAL

---

## Tableau de synthèse global

| Section | TOML | État réel | Conformité SKILL | Pédagogie | Priorité | Verdict |
|---|---|---|---|---|---|---|
| `lang/html/` | 3.1 | ✅ 7 modules | ✅ | ✅ | — | ✅ |
| `lang/css/` | 3.1 | ✅ 11 modules | ✅ | ✅ | — | ✅ |
| `lang/javascript/` | 3.1 | ✅ 8 modules (3 blocs) | ✅ | ✅ | — | ✅ |
| `lang/php/` | 3.1 | ✅ 16 modules | 🚨 Nommage | ✅ | **P1** | ⚠️ |
| `lang/python/` | 3.1 | 🔇 Gelé (TOML commenté) | — | — | Manuel | 🔇 |
| `frameworks/laravel/` | 3.2 | ✅ 43 leçons | ✅ | ✅ | — | ✅ |
| `frameworks/tailwind/` | ❌ | 🚨 Inexistant | ❌ | ❌ | **P3** | 🚨 |
| `frameworks/alpine/` | 3.2 | ✅ 5 modules | ⚠️ micro-ajust. | ✅ | **P1** | ✅ |
| `frameworks/livewire/` | 3.2 | ✅ 5 modules solides | ⚠️ Index ≠ réalité | ✅ | **P2** | ⚠️ |
| `stacks/tall/` | 3.3 | ✅ 10 fichiers | ⚠️ CDN + `<small>` | ✅ | — | ⚠️ |
| `stacks/index.md` | 3.3 | 🚨 TOML brut (sans page) | ❌ | ❌ | — | 🚨 |
| `mobile/swift/` | 3.4 | ✅ 18 modules | ✅ | ✅ | — | ✅ |
| `mobile/swiftui/` | 3.4 | ✅ 18 modules rédigés | À auditer | À auditer | **P1** | ✅* |
| `mobile/vapor/` | 3.4 | ✅ 12 modules rédigés | À auditer | À auditer | **P1** | ✅* |
| `data/sqlite.md` | 3.5 | ✅ 83 Ko monolithique | ⚠️ | ⚠️ | **P4** | ⚠️ |
| `data/` (4 autres) | 3.5 | 🚨 Stubs ~220 octets | ❌ | ❌ | **P3** | 🚨 |
| `modelisation/uml/` | 3.6 | ✅ 12 diag. + intro | ⚠️ index vide | ✅ | **P1** | ⚠️ |
| `modelisation/merise/` | 3.6 | ✅ 5 modules terminés | ✅ | ✅ | — | ✅ |
| `tests-qualite/index.md` | 3.7 | ⚠️ 30 Ko, bug syntaxe | 🚨 | 🚨 | **P5** | 🚨 |
| `tests-qualite/phpunit/` | 3.7 | ✅ 8 modules | 🚨 Nommage | ⚠️ Lourd | **P2** | ⚠️ |
| `tests-qualite/pest/` | 3.7 | ✅ 8 modules | 🚨 Nommage | ⚠️ Lourd | **P2** | ⚠️ |
| `tests-qualite/tdd.md` | 3.7 | 🚨 Stub | ❌ | ❌ | **P6** | 🚨 |
| `tests-qualite/pyramide` | 3.7 | 🚨 Stub | ❌ | ❌ | **P6** | 🚨 |
| `tests-qualite/coverage` | 3.7 | 🚨 Stub | ❌ | ❌ | **P6** | 🚨 |
| `tests-qualite/vitest/` | 3.7 | 🚨 Stub + rapport | ❌ | ❌ | **P7** | 🚨 |
| `tests-qualite/cypress/` | 3.7 | 🚨 Stub + rapport | ❌ | ❌ | **P7** | 🚨 |
| `tests-qualite/jest/` | 3.7 | 🚨 Rapport seul | ❌ | ❌ | **P7** | 🚨 |
| `devsecops/` | 3.8 | 🚨 Tout vide | ❌ | ❌ | **P8** | 🚨 |
| `cloud/` | — | 🔇 Hors TOML | — | — | Commenté | 🔇 |
| `architecture/` | — | 🔇 Hors TOML | — | — | Commenté | 🔇 |

> **✅\*** : SwiftUI (18 mod.) et Vapor (12 mod.) sont rédigés mais n'ont pas encore été audités SKILL en détail.

---

## Analyse détaillée

<br>

---

### 1. `lang/` — Langages & Standards (3.1)

#### ✅ HTML — Conforme

7 modules (`01-introduction.md` → `07-elements-interactifs-natifs.md`), rapport de formation, index. Aucune action requise.

#### ✅ CSS — Conforme (11 modules)

Refonte complète confirmée par le TOML : `01-introduction-css.md` → `11-responsive-design.md`. Sélecteurs, unités, box model, animations, positionnement, Flexbox, Grid, responsive. Formation solide. Aucune action requise.

#### ✅ JavaScript — Terminé et conforme (audit intégré)

**Formation complète :** 8 modules en 3 blocs, tous nommés de manière explicite et numérotée.

| Bloc | Modules | Taille | Conformité SKILL |
|---|---|---|---|
| `socle/` | 01-hello-et-console, 02-bases-algorithmiques, 03-fonctions-et-objets | 3.6 – 5 Ko | ✅ |
| `moteur/` | 04-environnement-modules, 05-syntaxe-moderne-es6 | 7.6 – 19 Ko | ✅ |
| `application/` | 06-dom-manipulation, 07-persistance-locale, 08-logique-asynchrone | 7 – 10.5 Ko | ✅ |

Rapport de formation interne : **✅ Terminé & Conforme**. Frontmatter, `omny-meta`, admonitions, code commenté avec titres, conclusions avec transition — tout est en ordre.

**Point de vigilance :** `05-syntaxe-moderne-es6.md` à 19 Ko est le module le plus lourd. Il reste sous le seuil critique (pas de problème actuel), mais à surveiller si le contenu grossit.

**Recommandation du rapport interne :** Envisager un projet final dans `application/` combinant Fetch API, DOM et ES6. Non urgent.

#### 🚨 PHP — Nommage (Priorité 1)

16 modules rédigés, contenu solide. Seul problème : nommage `module1.md` → `module16.md` — illisible en maintenance.

**Plan de renommage (exemple) :**

| Actuel | Proposé |
|---|---|
| `module1.md` | `01-syntaxe-et-variables.md` |
| `module7.md` | `07-gestion-erreurs.md` |
| `module8.md` | `08-classes-et-objets.md` |
| `module16.md` | `16-solid-et-design-patterns.md` |

Le renommage implique une **mise à jour du TOML** (`03-nav-dev-cloud.toml`, lignes 120-138).

#### 🔇 Python — Gelé

Django, Flask, Tinker commentés dans le TOML. Reprise lors de la filière Cyber. Aucune action — l'utilisateur gère le TOML manuellement.

---

### 2. `frameworks/` — Frameworks & Bibliothèques (3.2)

#### ✅ Laravel Masterclass — Modèle de référence absolu

43 leçons numérotées et nommées, 9 blocs thématiques documentés dans le TOML, sous-section `auth/`, rapport de formation ✅ SKILL v2.0. Aucune action requise.

Les modules 36-39 traitent de TALL (Tailwind) sans qu'un cours Tailwind existe — résolu par la création P3.

#### 🚨 Tailwind CSS — Inexistant (Priorité 3)

Le T de TALL n'a aucun cours. **Emplacement :** `frameworks/tailwind/`, **en première position dans le bloc Frameworks du TOML** (avant Laravel).

**Périmètre validé — 8 modules :**

| Module | Thème | Niveau |
|---|---|---|
| `01-philosophie-utility-first.md` | De CSS classique à Tailwind — le pourquoi | 🟢 |
| `02-installation-configuration.md` | CLI, Vite, `tailwind.config.js`, purge CSS | 🟢 |
| `03-classes-fondamentales.md` | Spacing, Typography, Colors, Borders, Sizing | 🟢 |
| `04-flexbox-grid-tailwind.md` | Layout avec utilitaires (flex, grid, gap) | 🟢→🟡 |
| `05-responsive-dark-mode.md` | Breakpoints `sm:` `md:` `lg:`, variantes `dark:` | 🟡 |
| `06-etats-interactions.md` | `hover:`, `focus:`, `group-hover:`, `peer:`, transitions | 🟡 |
| `07-composants-et-extraction.md` | `@apply`, conventions de nommage, Blade components | 🟡→🔴 |
| `08-plugins-et-theming-avance.md` | Thème custom, plugins officiels, intégration DaisyUI | 🔴 |

**Objectif :** sortie utilisateur avancé — largement au-delà du junior, accessible depuis le débutant.

#### ✅ Alpine.js — Micro-ajustements (Priorité 1)

5 modules théoriques solides, rapport de formation, approche lab documentée. La formation est qualitative — uniquement des harmonisations de forme à appliquer rapidement.

**Checklist (3 points, sans réécriture) :**

| Point | Règle SKILL | Action |
|---|---|---|
| `!!! quote` d'ouverture (analogie) | §3 obligatoire | Vérifier modules 01-05 |
| `## Conclusion` + `!!! quote` final | §9 obligatoire | Vérifier modules 01-05 |
| Séparateurs `<br>\n\n---` entre sections | §7 | Uniformiser |

#### ⚠️ Livewire — Index à refaire (Priorité 2)

**Les 5 modules existants sont pédagogiquement excellents :**

| Module | Thème | Qualité |
|---|---|---|
| `01-fondations-cycle-de-vie.md` | Rôle, composant, lifecycle | ✅ Analogie forte, code commenté |
| `02-proprietes-actions.md` | wire:model, wire:click, wire:loading | ✅ Exemples concrets |
| `03-formulaires-validation.md` | Validation, wire:submit | ✅ (à confirmer) |
| `04-evenements-communication.md` | $dispatch, listeners | ✅ (à confirmer) |
| `05-avance-production.md` | Uploads, wire:poll, production | ✅ Analogies réelles, cas pro |

**Problème unique :** L'`index.md` (12 Ko) promet 16 modules / 4 parties / 6 ateliers / 60-80h. Le TOML référence 5 fichiers. L'index doit être **réécrit pour correspondre aux 5 modules réels**, présentés comme une formation "Fondations Livewire" solide, avec un chemin vers les ateliers dans `projets/livewire-lab/`.

---

### 3. `stacks/` — Stacks Applicatives (3.3)

#### ✅ `stacks/tall/` — Contenu riche, forme à ajuster

10 fichiers substantiels (40-74 Ko), progression logique (installation → fondations → livewire-pur → alpine-pur → hybride → production → auth).

**Points de forme à corriger :**
- Images `cdn.devdojo.com` → migrer vers `docs/assets/stacks/tall/auteurs/`
- Balises `<small>*Légende*</small>` → `<p><em>Légende</em></p>` (SKILL §5)

#### 🚨 `stacks/index.md` — TOML brut sans page lisible

L'`index.md` contient du code TOML de navigation brut. **À créer** : une vraie page Markdown d'accueil présentant la section Stacks, en s'appuyant sur le contenu TOML section 3.3.

#### 🚨 `stacks/mean.md` et `stacks/mern.md`

Stubs de 215 octets non référencés dans le TOML. Décision à prendre : rédiger ou supprimer.

---

### 4. `mobile/` — Développement Mobile (3.4)

#### ✅ Swift — Exemplaire (18 modules, nommage parfait)

Aucune action requise. C'est le second modèle de référence avec Laravel.

#### ✅ SwiftUI — Rédigé (18 modules, audit P1)

18 modules présents sur disque (10 à 19 Ko chacun) + index (10 Ko) + rapport de formation.

**Action P1 :** Audit conformité SKILL (vérifier analogies, conclusions, séparateurs, `omny-meta`) + retirer la mention "*Section en préparation*" dans `mobile/index.md`.

#### ✅ Vapor — Rédigé (12 modules, audit P1)

12 modules présents sur disque (13 à 20 Ko chacun) + index (6.5 Ko) + rapport de formation. Note : le TOML prévoyait 11 modules — un module bonus `12-deploiement.md` est présent.

**Action P1 :** Même audit SKILL que SwiftUI + mise à jour du TOML pour référencer `12-deploiement.md`.

---

### 5. `data/` — Bases de Données (3.5)

#### ⚠️ SQLite — À découper (Priorité 4)

83 Ko dans un seul fichier. Excellent contenu, problème de lisibilité en navigation web.

**Découpage recommandé — 6 modules sans perte de contenu :**
`01-introduction-sqlite.md` | `02-types-et-contraintes.md` | `03-crud-fondamentaux.md` | `04-jointures-et-relations.md` | `05-transactions-et-index.md` | `06-integration-php-laravel.md`

#### 🚨 MariaDB, PostgreSQL, NoSQL, GraphQL — Stubs (Priorité 3)

4 fichiers de ~220 octets. À rédiger après la création du cours Tailwind.

---

### 6. `modelisation/` — Modélisation & Conception (3.6)

**Positionnement :** Les fichiers vivent dans `bases/modelisation/` (cohérent — méthodes transversales) mais sont référencés dans le TOML dev-cloud (cohérent — point d'injection pédagogique). **Statu quo idéal.** Les fichiers seront déplacés manuellement par l'utilisateur si besoin.

#### ✅ Merise — Terminé et conforme

5 modules bien découpés Intro→MCD→MLD→MPD→MPD→SQL (14 à 25 Ko). Rapport validé. Aucune action requise.

#### ⚠️ UML — Contenu présent, index vide (Priorité 1)

12 diagrammes rédigés (5 à 18 Ko chacun) + `uml-intro.md` (8.5 Ko) + rapport de formation.

**Seul problème :** `uml/index.md` est vide (5 octets). **À créer rapidement** selon le modèle des autres index (mobile, Laravel) — présentation de la section, progression recommandée UseCase → Classes → Séquences → Activités → États, carte de navigation vers les 12 diagrammes.

---

### 7. `tests-qualite/` — Tests & Qualité (3.7)

#### ✅ PHPUnit et Pest — Nommage à corriger (Priorité 2)

8 modules chacun, contenu abondant. Problème identique à PHP : `module1.md` à `module8.md`.

| PHPUnit — Renommage proposé | Pest — Renommage proposé |
|---|---|
| `01-installation-configuration.md` | `01-philosophie-et-installation.md` |
| `02-assertions-fondamentales.md` | `02-expectations-api.md` |
| `03-tests-feature-laravel.md` | `03-feature-tests-laravel.md` |
| `04-database-testing.md` | `04-datasets-parametrises.md` |
| `05-mocking-et-doubles.md` | `05-plugins-pest.md` |
| `06-tdd-workflow.md` | `06-tdd-avec-pest.md` |
| `07-integration-complete.md` | `07-migration-phpunit.md` |
| `08-cicd-pipeline.md` | `08-parallel-et-ci.md` |

Le TOML devra être mis à jour en conséquence.

#### 🚨 `tests-qualite/index.md` — Refactorisation (Priorité 5)

- **30 Ko / 985 lignes** — doit être une carte de navigation, pas une formation.
- **Bug Markdown :** bloc de code non fermé (lignes 958-963).
- **Méta-texte visible** (lignes 965-985) — contenu de chantier apprenant-visible.
- Sections **Go Testing, Pytest, Jasmine** à retirer (hors stack actuelle).
- Contenu légitime (TDD, pyramide, coverage) à extraire dans les fichiers dédiés.

#### 🚨 Stubs thématiques — Extraction (Priorité 6)

`tdd.md`, `pyramide-tests.md`, `coverage.md`, `sast.md`, `dast.md`, `fuzzing.md` — stubs de ~220 octets. Le contenu théorique existe dans l'index (29 Ko) et doit en être extrait.

#### 🚨 Vitest, Cypress, Jest — Fondamentaux complets (Priorité 7)

**Vitest — 4 modules :**
`01-installation-configuration.md` | `02-tests-unitaires-fondamentaux.md` | `03-mocking-et-espions.md` | `04-couverture-et-ci.md`

**Cypress — 5 modules :**
`01-installation-premier-test-e2e.md` | `02-selecteurs-et-interactions.md` | `03-assertions-et-attentes.md` | `04-interception-reseau.md` | `05-ci-cd-et-rapports.md`

**Jest — 5 modules :**
`01-installation-et-philosophie.md` | `02-matchers-et-assertions.md` | `03-mocking-modules-api.md` | `04-tests-asynchrones.md` | `05-snapshot-et-coverage.md`

---

### 8. `devsecops/` — DevSecOps (3.8) — Priorité 8

Structure TOML complète (CI/CD, Docker, Secrets, IAC, Culture). Aucun contenu rédigé. Non urgent.

**Ordre logique quand le moment viendra :**
1. Docker (déploiement Laravel)
2. GitHub Actions (CI des projets)
3. Secrets (`.env`, production)

---

### 9. `cloud/` et `architecture/` — Commentés

Hors TOML. Aucune action. Seront intégrés à terme.

---

## Plan d'action — 8 niveaux de priorité (version finale)

### P1 — Consolider les sections rédigées + corrections rapides

| # | Action | Nature | Effort |
|---|---|---|---|
| 1.1 | **Audit SKILL SwiftUI** (18 modules) | Vérif. analogies, conclusions, séparateurs | Moyen |
| 1.2 | **Audit SKILL Vapor** (12 modules) | Idem + référencer `12-deploiement.md` dans TOML | Moyen |
| 1.3 | **MAJ `mobile/index.md`** | Retirer "*en préparation*", activer liens SwiftUI/Vapor | Rapide |
| 1.4 | **Renommer PHP** (`module1.md` → `01-syntaxe.md`) | 16 renommages + TOML | Moyen |
| 1.5 | **Micro-ajustements Alpine** | `!!! quote`, conclusions, séparateurs sur 5 modules | Rapide |
| 1.6 | **Créer `uml/index.md`** | Page de navigation des 12 diagrammes UML | Rapide |

### P2 — Corriger les sections en décalage

| # | Action | Nature | Effort |
|---|---|---|---|
| 2.1 | **Refaire l'index Livewire** | Aligner sur 5 modules existants, ôter les 16 modules fantômes | Moyen |
| 2.2 | **Renommer PHPUnit** (`module1.md` → descriptif) | 8 renommages + TOML | Moyen |
| 2.3 | **Renommer Pest** (`module1.md` → descriptif) | 8 renommages + TOML | Moyen |

### P3 — Créations manquantes critiques

| # | Action | Nature | Effort |
|---|---|---|---|
| 3.1 | **Créer `frameworks/tailwind/`** | 8 modules progressifs, TOML en tête du bloc | Lourd |
| 3.2 | **Rédiger `sql.md`, `postgresql.md`, `nosql.md`, `graphql.md`** | 4 modules BDD | Lourd |

### P4 — Refactorisation monolithique

| # | Action | Nature | Effort |
|---|---|---|---|
| 4.1 | **Découper `sqlite.md`** (83 Ko → 6 modules) | Sans perte de contenu | Moyen |

### P5 — Refactorisation index Tests

| # | Action | Nature | Effort |
|---|---|---|---|
| 5.1 | **Refactoriser `tests-qualite/index.md`** | Supprimer Go/Pytest/Jasmine, fermer bug, nettoyer méta-texte, transformer en hub | Moyen |

### P6 — Rédiger les stubs thématiques Tests

| # | Action | Nature | Effort |
|---|---|---|---|
| 6.1 | **`tdd.md`** | Extraction depuis index | Rapide |
| 6.2 | **`pyramide-tests.md`** | Extraction depuis index | Rapide |
| 6.3 | **`coverage.md`** | Extraction depuis index | Rapide |

### P7 — Créer les formations tests frontend

| # | Action | Nature | Effort |
|---|---|---|---|
| 7.1 | **Vitest** — 4 modules fondamentaux | Création from scratch | Moyen |
| 7.2 | **Cypress** — 5 modules fondamentaux E2E | Création from scratch | Lourd |
| 7.3 | **Jest** — 5 modules fondamentaux | Création from scratch | Lourd |

### P8 — DevSecOps (non urgent)

| # | Action | Nature | Effort |
|---|---|---|---|
| 8.1 | **Docker** — moteur + Compose | Création from scratch | Lourd |
| 8.2 | **GitHub Actions** — pipeline CI | Création from scratch | Moyen |
| 8.3 | **Secrets** — `.env`, entropie, Vault | Création from scratch | Moyen |

---

## Score global — Version finale

| Section | Score /10 | Statut |
|---|---|---|
| `frameworks/laravel/` | **9/10** | ✅ Modèle de référence n°1 |
| `lang/html/` | **8/10** | ✅ Complet et structuré |
| `lang/css/` | **8/10** | ✅ Complet (refonte confirmée TOML) |
| `lang/javascript/` | **8/10** | ✅ Terminé, conforme SKILL, rapport validé |
| `mobile/swift/` | **9/10** | ✅ Modèle de référence n°2 |
| `mobile/swiftui/` | **8/10** | ✅ Rédigé — audit SKILL P1 |
| `mobile/vapor/` | **8/10** | ✅ Rédigé — audit SKILL P1 |
| `modelisation/merise/` | **8/10** | ✅ Terminé et conforme |
| `mobile/index.md` | **8/10** | ✅ Excellent — à mettre à jour P1 |
| `frameworks/alpine/` | **7/10** | ✅ Micro-harmonisation P1 |
| `modelisation/uml/` | **7/10** | ⚠️ Contenu fort, index vide P1 |
| `stacks/tall/` | **6/10** | ⚠️ Riche mais CDN + `<small>` |
| `lang/php/` | **6/10** | ⚠️ Nommage P1 |
| `frameworks/livewire/` | **6/10** | ⚠️ Modules bons, index à refaire P2 |
| `tests-qualite/phpunit/` | **5/10** | ⚠️ Contenu ok, nommage P2 |
| `tests-qualite/pest/` | **5/10** | ⚠️ Contenu ok, nommage P2 |
| `data/sqlite.md` | **4/10** | ⚠️ Complet mais monolithique P4 |
| `tests-qualite/index.md` | **2/10** | 🚨 Bug + méta-texte + trop lourd P5 |
| `stacks/index.md` | **1/10** | 🚨 TOML brut, pas de page lisible |
| `frameworks/tailwind/` | **0/10** | 🚨 Le T de TALL — inexistant P3 |
| `data/` (4 BDD) | **0/10** | 🚨 Stubs P3 |
| `tests-qualite/tdd` etc. | **0/10** | 🚨 Stubs P6 |
| `tests-qualite/vitest/` | **0/10** | 🚨 P7 |
| `tests-qualite/cypress/` | **0/10** | 🚨 P7 |
| `tests-qualite/jest/` | **0/10** | 🚨 P7 |
| `devsecops/` | **0/10** | 🚨 P8 — non urgent |
| `cloud/`, `architecture/` | — | 🔇 À terme |

---

## Conclusion

> [!IMPORTANT]
> **Ce qui est solide :** Laravel (9/10), Swift (9/10), HTML/CSS/JS (8/10), SwiftUI/Vapor (rédigés), Merise (terminée). La section mobile est une **surprise positive** — les trois formations Swift, SwiftUI et Vapor sont toutes rédigées.

> [!WARNING]
> **Les deux manques prioritaires :** (1) Tailwind CSS (P3) — le T de TALL est introuvable dans le cursus. (2) L'index Livewire (P2) qui décrit 16 modules fantômes alors que 5 modules solides existent déjà.

> [!NOTE]
> **Sur la Modélisation (UML/Merise) :** Statu quo parfait — `bases/modelisation/` pour les fichiers, TOML `dev-cloud` pour l'injection pédagogique. Merise terminée, UML solide avec uniquement l'index vide à créer (P1, rapide).
