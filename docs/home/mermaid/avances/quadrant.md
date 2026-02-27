---
icon: lucide/square-library
---

# Quadrant Chart (priorisation)

!!! note "Importance"
    Le quadrant chart sert à prioriser : effort vs impact, risque vs valeur, urgence vs importance. C'est utile pour arbitrer des chantiers et communiquer une logique de décision sans surcharger en texte.

## Cas d'utilisation

| Domaine | Pertinence | Contexte |
|---|:---:|---|
| Cyber gouvernance | 🔴 Critique | Priorisation des risques, arbitrage des plans de remédiation |
| Pilotage produit | 🟠 Élevé | Positionnement des fonctionnalités selon effort et valeur métier |
| Gestion de projet | 🟠 Élevé | Arbitrage des chantiers, communication de la logique de décision |
| DevSecOps | 🟡 Modéré | Priorisation des dettes techniques et des correctifs de sécurité |

## Exemple de diagramme

Les coordonnées de chaque point s'expriment en valeurs normalisées entre 0 et 1 sur les deux axes — `[x, y]`. Les labels des quadrants se déclarent dans l'ordre : haut-droite (`quadrant-1`), haut-gauche (`quadrant-2`), bas-gauche (`quadrant-3`), bas-droite (`quadrant-4`).

```mermaid
quadrantChart
  title Priorisation
  x-axis Faible effort --> Fort effort
  y-axis Faible impact --> Fort impact
  quadrant-1 Quick wins
  quadrant-2 Projets strategiques
  quadrant-3 A eviter
  quadrant-4 Taches de fond
  "Docs Fondamentaux": [0.30, 0.80]
  "Refacto CI/CD": [0.70, 0.70]
  "New UI": [0.80, 0.40]
  "Quick fix": [0.20, 0.60]
```

_Ce schéma positionne quatre initiatives selon leur effort et leur impact pour guider la décision de priorisation._

<br />

---

!!! info "Lien officiel : [https://mermaid.js.org/syntax/quadrantChart.html](https://mermaid.js.org/syntax/quadrantChart.html)"

<br />