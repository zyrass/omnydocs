---
description: "CVSS (Common Vulnerability Scoring System) — Le standard mondial pour évaluer et communiquer la sévérité des vulnérabilités logicielles."
icon: lucide/book-open-check
tags: ["REPORTING", "CVSS", "SCORING", "VULNERABILITE", "RISQUE"]
---

# CVSS — Le Score de la Menace

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-version="v3.1 & v4.0"
  data-time="~45 minutes">
</div>

<img src="../../../assets/images/cyber/cvss.svg" width="100" align="center" style="display: block; margin: 0 auto;">

## Introduction

!!! quote "Analogie pédagogique — L'Échelle de Richter de la Cyber"
    Imaginez un tremblement de terre. On utilise l'échelle de Richter pour dire s'il est grave ou non. Le **CVSS** est l'échelle de Richter pour les failles informatiques. Il permet de dire si une faille est une simple "fissure dans le mur" (Score 2.0) ou si elle risque de faire "s'écrouler tout le bâtiment" (Score 10.0). Sans cet outil, chaque expert aurait son propre avis et il serait impossible pour une entreprise de savoir quel trou reboucher en premier.

Le **Common Vulnerability Scoring System (CVSS)** est une méthode de notation standardisée permettant d'évaluer la sévérité des vulnérabilités. Il produit un score numérique allant de **0.0 à 10.0**.

---

## Les 3 Groupes de Métriques

Le score final est le résultat de trois couches successives de calcul :

### 1. Base Score (Le score intrinsèque)
Les caractéristiques de la faille qui ne changent pas avec le temps ou l'environnement.
CVSS (Common Vulnerability Scoring System) est le standard mondial de l'industrie pour évaluer la sévérité des vulnérabilités logicielles. Il fournit un système de notation numérique (de 0.0 à 10.0) permettant de prioriser les remédiations de manière objective, en se basant sur des critères techniques mesurables.

<br>

---

## Les Trois Groupes de Métriques

Le score CVSS final est calculé en combinant plusieurs facteurs répartis en trois catégories :
- **Base Score (Métriques de base)** : Représente les qualités intrinsèques d'une vulnérabilité (accessibilité, complexité, privilèges requis, impact sur la confidentialité/intégrité/disponibilité).
- **Temporal Score (Métriques temporelles)** : Ajuste le score en fonction de l'état actuel de la vulnérabilité (existence d'un exploit public, disponibilité d'un correctif).
- **Environmental Score (Métriques environnementales)** : Personnalise le score selon l'importance du système affecté dans l'infrastructure spécifique du client.

<br>

---

## Échelle de Sévérité

| Score | Sévérité | Action Requise |
|---|---|---|

!!! danger "Confondre Sévérité et Risque"
    Une vulnérabilité peut avoir une **Sévérité** de 10.0 (critique) mais un **Risque** de 0 si le serveur est éteint ou derrière 4 pare-feux. Votre rapport doit toujours mentionner les deux.

!!! warning "L'abus du 'Privileges Required: None'"
    Vérifiez bien si l'attaquant a besoin d'être authentifié avant de mettre 10.0. Une faille qui nécessite un compte administrateur n'est jamais critique de base.

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le CVSS est le thermomètre de la sécurité. En l'utilisant correctement, vous parlez le même langage que les constructeurs de logiciels (Microsoft, Cisco) et que les responsables sécurité de vos clients. C'est l'outil qui apporte l'objectivité indispensable à tout audit de sécurité.

> Une fois vos vulnérabilités scorées, il est temps de proposer des solutions concrètes dans votre **[Plan de Remédiation →](./remediation.md)**.





