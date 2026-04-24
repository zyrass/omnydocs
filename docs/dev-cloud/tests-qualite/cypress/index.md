---
description: "Cypress — Hub de navigation : fondamentaux E2E, tests avancés, intercept réseau, CI/CD et reporting."
icon: lucide/monitor-check
tags: ["CYPRESS", "E2E", "TESTS", "JAVASCRIPT", "CICD"]
---

# Cypress

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Cypress 13.x"
  data-time="Hub">
</div>

## Présentation

!!! quote "Analogie pédagogique — Le Robot Testeur"
    Imaginez embaucher un robot qui clique sur chaque bouton, remplit chaque formulaire, et vérifie chaque page de votre site — 100 fois par jour, sans jamais se fatiguer. Cypress est ce robot : il ouvre un vrai navigateur (Chromium), exécute vos scénarios utilisateur, et vous signale en temps réel si quelque chose ne répond pas comme prévu. Contrairement aux tests unitaires qui testent des fonctions isolées, Cypress teste **l'application entière** du point de vue de l'utilisateur.

**Cypress** est le leader des tests E2E (End-to-End) frontend. Il s'exécute dans le même processus que le navigateur, éliminant les problèmes de synchronisation asynchrone.

| Caractéristique | Valeur |
|---|---|
| **Créé par** | Cypress.io (2015) |
| **Cas d'usage** | Tests E2E, tests d'intégration frontend |
| **Navigateurs** | Chrome, Firefox, Edge, Electron |
| **Composant testing** | React, Vue, Angular (Component Testing) |

<br>

---

## Modules de cette Formation

| Module | Contenu | Niveau |
|---|---|---|
| [01 — Fondamentaux](./01-fondamentaux.md) | Installation, sélecteurs, commandes, assertions | 🟡 |
| [02 — Tests Avancés](./02-tests-avances.md) | Intercept réseau, fixtures, custom commands, CI/CD | 🟡 |
| [03 — Component Testing](./03-component-testing.md) | Tests isolés React/Vue dans un vrai navigateur | 🟡 |
| [04 — Cloud & Parallélisme](./04-cypress-cloud.md) | Diviser le temps CI avec Cypress Cloud et Sorry Cypress | 🔴 |
| [05 — Accessibilité (a11y)](./05-accessibility-testing.md) | Détection automatique des erreurs RGAA via axe-core | 🔴 |

<br>

---

## Prérequis

- Node.js 18+
- Application web cible accessible (dev server)
- Bases HTML/CSS (sélecteurs)

<br>
