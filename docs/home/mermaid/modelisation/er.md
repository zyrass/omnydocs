---
icon: lucide/square-library
---

# ER Diagram (modèle de données)

!!! note "Importance"
    L'ER diagram formalise un modèle relationnel : tables, relations et cardinalités. Il permet de vérifier la cohérence du schéma, d'anticiper l'intégrité référentielle, et d'aligner équipe dev, DBA et sécurité sur une même représentation.

## Cas d'utilisation

| Domaine | Pertinence | Contexte |
|---|:---:|---|
| Développement | 🔴 Critique | Documentation du schéma de base de données, migrations, contraintes |
| Base de données | 🔴 Critique | Référence principale pour la conception et la revue de schéma relationnel |
| Architecture SI | 🟠 Élevé | Cartographie des flux de données entre composants d'un système |
| Cyber technique | 🟡 Modéré | Analyse d'impact sur les données, forensic, identification des tables sensibles |

## Exemple de diagramme

La notation Mermaid pour les ER diagrams utilise des symboles de cardinalité crow's foot : `||--o{` signifie "un et un seul vers zéro ou plusieurs". Les attributs déclarés dans chaque entité permettent de documenter le type de données directement dans le schéma.

```mermaid
erDiagram
  USERS ||--o{ SESSIONS : has
  USERS ||--o{ POSTS : writes
  POSTS ||--o{ COMMENTS : receives

  USERS {
    string id
    string email
  }

  POSTS {
    string id
    string user_id
    string title
  }

  COMMENTS {
    string id
    string post_id
    string body
  }
```

_Ce schéma modélise un **SI**[^1] minimal : utilisateurs, contenus et commentaires avec leurs relations._

<br />

---

!!! info "Lien officiel : [https://mermaid.js.org/syntax/entityRelationshipDiagram.html](https://mermaid.js.org/syntax/entityRelationshipDiagram.html)"

<br />

[^1]: **SI** — Système d'Information. Désigne l'ensemble des ressources (humaines, techniques, organisationnelles) permettant de collecter, stocker, traiter et diffuser l'information au sein d'une organisation.