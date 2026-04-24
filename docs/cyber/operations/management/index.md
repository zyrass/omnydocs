---
description: "Gestion Opérationnelle SOC — Hub : métriques clés (MTTD, MTTR), SLA/SLO, organisation des astreintes et communication de crise."
tags: ["SOC", "GESTION", "SLA", "MTTD", "MTTR", "ASTREINTE", "KPI"]
---

# Gestion Opérationnelle du SOC

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → Manager"
  data-version="2025"
  data-time="Hub">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Chef d'Orchestre"
    Un orchestre symphonique peut rassembler les meilleurs musiciens du monde — sans chef d'orchestre pour coordonner, le résultat sera du chaos. La **gestion opérationnelle du SOC** est ce rôle de chef d'orchestre : elle s'assure que les processus sont respectés, les métriques mesurées, les équipes organisées et la communication fluide, même en pleine crise.

Un SOC techniquement excellent peut échouer s'il manque de structure opérationnelle : des SLA non définis, des équipes épuisées par les astreintes, une communication de crise désorganisée. Ce module couvre la **dimension humaine et organisationnelle** du SOC.

<br>

---

## Métriques clés d'un SOC

| KPI | Formule | Objectif indicatif |
|---|---|---|
| **MTTD** | Temps détection − Temps début attaque | < 1 heure |
| **MTTR** | Temps remédiation − Temps détection | < 4h (P1) |
| **Volume d'alertes** | Alertes/jour par analyste | < 50 alertes actionables |
| **Taux de faux positifs** | Faux positifs / Total alertes | < 20% |
| **SLA respect** | Incidents traités dans le SLA / Total | > 95% |
| **Mean Dwell Time** | Temps moyen de présence d'un attaquant | < 30 jours (idéal : < 1 jour) |

<br>

---

## Parcours pédagogique

### 1 — SLA / SLO

Définir des objectifs mesurables, créer des SLA pour un SOC managé, exemples concrets.

[:lucide-book-open-check: Cours SLA/SLO →](./sla.md)

### 2 — Astreintes (On-Call)

Organiser les rotations, gérer l'épuisement, outils d'alerte (PagerDuty, OpsGenie, Grafana OnCall).

[:lucide-book-open-check: Cours Astreintes →](./oncall.md)

### 3 — Communication de Crise

Gérer la communication interne et externe lors d'un incident majeur, template de notification RGPD.

[:lucide-book-open-check: Cours Communication de Crise →](./crisis-comm.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La technique sans organisation génère du chaos. L'organisation sans technique génère de l'inaction. Un SOC performant combine les deux : des **outils bien déployés**, des **processus clairement définis** et des **personnes bien organisées**. Les KPI et SLA ne sont pas de la bureaucratie — ce sont les instruments de mesure qui permettent d'améliorer continuellement le SOC.

> Commencez par **[SLA/SLO →](./sla.md)** pour définir les engagements de votre SOC.

<br>
