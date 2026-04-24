---
description: "Flask — Hub de navigation : fondamentaux, routes, templates, ORM SQLAlchemy, authentification et déploiement."
tags: ["FLASK", "PYTHON", "WEB", "MICROFRAMEWORK", "SQLALCHEMY"]
---

# Flask

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Flask 3.x"
  data-time="Hub">
</div>

## Présentation

!!! quote "Analogie pédagogique — La Plaque Chauffante du Chef"
    Flask est une plaque chauffante professionnelle : petite, puissante, portable. Django vous donne le restaurant complet ; Flask vous donne juste la source de chaleur. C'est à vous d'apporter la casserole (SQLAlchemy), les ustensiles (Jinja2), l'assiette (Bootstrap). Cette flexibilité totale est une force pour les APIs légères et les microservices — et un risque si vous manquez de structure.

**Flask** est un microframework Python : il impose le minimum (routing + templates Jinja2) et vous laisse choisir chaque brique (ORM, auth, validation). C'est le choix naturel pour les APIs REST et les microservices.

| Caractéristique | Valeur |
|---|---|
| **Créé par** | Armin Ronacher (2010) |
| **Philosophie** | Minimalism, simplicité, flexibilité |
| **ORM** | SQLAlchemy (séparé) |
| **Templates** | Jinja2 (intégré) |
| **Cas d'usage** | API REST, microservices, prototypes |

<br>

---

## Modules de cette Formation

| Module | Contenu | Niveau |
|---|---|---|
| [01 — Fondamentaux](./01-fondamentaux.md) | Installation, routes, Jinja2, SQLAlchemy, blueprints | 🟡 |

<br>

---

## Prérequis

- Python 3.11+ et `venv`
- Bases HTTP (GET/POST, status codes, headers)
- Bases SQL (SELECT, INSERT, JOIN)

<br>
