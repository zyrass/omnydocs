---
description: "Jest — Hub de navigation : fondamentaux, mocking avancé, coverage et intégration CI/CD."
icon: lucide/flask-conical
tags: ["JEST", "JAVASCRIPT", "TESTS", "MOCKING", "COVERAGE", "CICD"]
---

# Jest

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🟡 Intermédiaire"
  data-version="Jest 29.x / Node.js 18+"
  data-time="Hub">
</div>

## Présentation

!!! quote "Analogie pédagogique — Le Filet de Sécurité"
    Jest est le filet de sécurité d'un acrobate : invisible quand tout se passe bien, indispensable quand quelque chose cloche. Chaque `test()` est un maille du filet. Plus le filet est dense (couverture élevée), plus vous pouvez acrobatiser (refactoriser) en confiance. Jest vérifie automatiquement que chaque maille tient — à chaque modification de code.

**Jest** est le framework de test JavaScript le plus populaire, créé par Facebook. Il intègre runner, assertions (`expect`), mocking et coverage dans un seul outil.

| Caractéristique | Valeur |
|---|---|
| **Créé par** | Facebook/Meta (2014) |
| **Cas d'usage** | Tests unitaires JS/TS (Node, React, Vue) |
| **Intégrations** | React Testing Library, Vue Test Utils |
| **Runner** | Intégré (jsdom ou Node) |

<br>

---

## Modules de cette Formation

| Module | Contenu | Niveau |
|---|---|---|
| [01 — Fondamentaux](./01-fondamentaux.md) | Installation, `describe/test/expect`, matchers, setup | 🟢 |
| [02 — Mocking Avancé](./02-mocking-avance.md) | `jest.fn()`, `jest.mock()`, spies, modules, timers | 🟡 |

<br>

---

## Prérequis

- Node.js 18+
- Bases JavaScript (ES6 : modules, async/await)

<br>
