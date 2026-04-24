---
description: "SOAR — Security Orchestration, Automation & Response : réduire le MTTR, automatiser les playbooks et orchestrer les outils du SOC avec Shuffle et Cortex."
tags: ["SOAR", "AUTOMATISATION", "ORCHESTRATION", "SOC", "MTTR", "PLAYBOOK"]
---

# SOAR & Automatisation

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-version="2025"
  data-time="Hub">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Chaîne de Production Automatisée"
    Dans une usine manuelle, chaque pièce passe entre les mains d'un ouvrier différent. L'industrialisation a remplacé les tâches répétitives par des robots, permettant aux humains de se concentrer sur les décisions complexes. Un SOC sans SOAR est une usine manuelle : les analystes passent 80% de leur temps sur des tâches répétitives (vérifier une IP sur VirusTotal, chercher un hash dans MISP, créer un ticket...). Le **SOAR automatise ces tâches** pour que les analystes se concentrent sur la vraie valeur ajoutée.

<br>

---

## Parcours SOAR

### 1 — Comprendre le SOAR

Définition, différence SIEM/SOAR, métriques clés (MTTD, MTTR) et cas d'usage.

[:lucide-book-open-check: Cours SOAR →](./soar.md)

### 2 — Playbooks Automatisés

Concevoir et implémenter des playbooks de réponse automatique : déclencheurs, actions, branchements conditionnels.

[:lucide-book-open-check: Cours Playbooks SOAR →](./playbooks.md)

### 3 — Cortex — Automatisation des Analyses

Le moteur d'analyzers et de responders de TheHive : analyse automatique des IOC et déclenchement d'actions de réponse.

[:lucide-book-open-check: Cours Cortex →](./cortex.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le SOAR ne remplace pas les analystes — il **démultiplie leur efficacité**. Un analyste sans SOAR traite 20 alertes/jour. Le même analyste avec SOAR traite 200 alertes/jour, car les 90% de tâches répétitives sont automatisées. L'objectif : que chaque alerte nécessitant une décision humaine arrive à l'analyste **déjà enrichie, déjà corrélée, et avec les premières actions de containment déjà effectuées**.

> Commencez par **[SOAR →](./soar.md)** pour comprendre les concepts avant de passer aux playbooks pratiques.

<br>
