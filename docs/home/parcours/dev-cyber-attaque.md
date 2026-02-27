---
description: "Parcours détaillé pour se spécialiser en cybersécurité offensive (Red Team / Pentest) dans OmnyDocs."
icon: lucide/crosshair
tags: ["PARCOURS", "CYBERSECURITE", "RED-TEAM", "PENTEST", "OFFENSIF"]
---

# Parcours — Dev → Cyber Attaque

<div
  class="omny-meta"
  data-level="Intermédiaire à Avancé"
  data-version="1.0"
  data-time="5-10 minutes">
</div>

!!! warning "**Accessibilité : avancée** — _Ce parcours exige une compréhension réelle du code applicatif pour exploiter les vulnérabilités de manière pertinente._"

## Que fait ce parcours

Découvrons via ce diagramme de séquence le parcours orienté Cyber Attaque.

```mermaid
sequenceDiagram
  participant L as Apprenant
  participant F as Fondamentaux IT
  participant D as Développement
  participant R as Cyber Attaque

  L->>F: Acquisition des bases
  note over F: Logique, formats de données,<br/>outils, modélisation, Git
  F->>D: Maîtrise applicative
  note over D: HTML/CSS → JavaScript →<br/>PHP → Laravel → Stack TALL
  D->>R: Spécialisation Red Team
  note over R: OSINT, pentest Web & API,<br/>exploitation, post-exploitation, reporting
  R-->>L: Pentester / Red Teamer opérationnel
```

_Ce parcours privilégie la compréhension du code et des vulnérabilités applicatives. Il prépare efficacement aux **tests d'intrusion Web** et **API**, en partant du principe qu'un attaquant qui comprend le code trouve ce que les autres manquent._

!!! quote "En somme, ce parcours est l'extension naturelle du parcours Développeur web vers la sécurité offensive. La maîtrise du développement applicatif est le prérequis direct du pentest Web — on n'exploite correctement que ce que l'on sait construire."

<br />

---

## Matrice

Les lignes ci-dessous sont extraites de la [Matrice de compétences](../matrice.md).  
Elles indiquent à quel stade chaque niveau de progression est structurant pour ce parcours.

| Domaine | N1 | N2 | N3 | N4 |
|:---|:---:|:---:|:---:|:---:|
| Développement | 🟢 Faible | 🟠 Élevé | 🟠 Élevé | 🟡 Modéré |
| Cyber Attaque (Red / Pentest) | — | 🟡 Modéré | 🟡 Modéré | 🟠 Élevé |

**Lecture :** le domaine Développement doit atteindre le N3 avant que la spécialisation Cyber Attaque ne devienne pleinement structurante. Contrairement à la Cyber Défense, la Red Team monte en puissance progressivement jusqu'au N4 — c'est un domaine qui exige de l'expérience accumulée, pas seulement des connaissances théoriques.

<br />

---

## Heatmap

Les colonnes ci-dessous sont extraites de la [Heatmap de compétences](../heatmap.md).  
Elles indiquent l'intensité attendue sur les compétences transversales mobilisées dans ce parcours, sur les deux domaines concernés.

| Compétence | Développement | Cyber Attaque |
|---|:---:|:---:|
| Logique informatique | 🟠 Élevé | 🟡 Modéré |
| **Programmation** | 🔴 **Critique** | 🟠 Élevé |
| Administration Linux | 🟡 Modéré | 🟠 Élevé |
| **Réseaux** | 🟡 Modéré | 🔴 **Critique** |
| Analyse de logs | 🟡 Modéré | 🟡 Modéré |
| Tests applicatifs | 🟠 Élevé | 🟡 Modéré |
| **Pentest** | 🟡 Modéré | 🔴 **Critique** |
| Détection / règles | 🟡 Modéré | 🟡 Modéré |
| Gestion des risques | 🟢 Faible | 🟢 Faible |
| Conformité | 🟢 Faible | 🟢 Faible |

!!! note
    Ce parcours concentre trois compétences critiques. La **Programmation** est critique en Développement — c'est le prérequis qui différencie un pentester applicatif d'un script kiddie. Les **Réseaux** et le **Pentest** deviennent critiques en Cyber Attaque : comprendre les protocoles réseau est indispensable pour cartographier une cible et exploiter des services exposés. L'Administration Linux monte à 🟠 Élevé en Cyber Attaque — la majorité des environnements cibles fonctionnent sous Linux.

<br />

---

## Radar

!!! quote "Note"
    _Le radar ci-dessous illustre la forme du parcours Dev → Cyber Attaque. Les deux pics symétriques sur Développement et Cyber Attaque reflètent la dépendance directe entre maîtrise applicative et exploitation offensive. Ce profil est le miroir offensif du parcours Sys → Cyber Défense._

```mermaid
radar-beta
title Compétences pour le parcours : Dev -> Cyber Attaque

axis Fondamentaux["Fondamentaux IT"]
axis Dev["Developpement"]
axis Sys["Systemes & Infra"]
axis CyberDef["Cyber Defense"]
axis CyberAttq["Cyber Attaque"]
axis Gouvernance["Gouvernance"]

curve CyberAttq["Dev → Cyber Attaque"]{3,5,1,1,5,1}

max 5
min 0
ticks 5
```

<br />

---

## Orientations possibles

Une fois la spécialisation Red Team consolidée, deux extensions stratégiques sont accessibles.

```mermaid
flowchart TB
  RED[Dev → Cyber Attaque]

  GRC[Gouvernance GRC]
  DOUBLE[Double compétence technique]

  RED -->|Expérience offensive → pilotage stratégique| GRC
  RED -->|Ajout du volet infrastructure| DOUBLE
```

_L'extension vers la **Gouvernance** est pertinente à ce stade : un pentester expérimenté comprend les vecteurs d'attaque réels, ce qui donne une crédibilité terrain précieuse pour piloter la conformité et les analyses de risques. L'extension vers la **Double compétence technique** nécessite de compléter intégralement le volet Systèmes & Infrastructure avant de converger._

!!! warning "**Accessibilité : avancée à difficile** — Ces deux extensions supposent d'avoir atteint le N3 en Cyber Attaque avant de bifurquer."

<br />

---

## Conclusion

Le parcours Dev → Cyber Attaque est l'extension offensive naturelle du parcours Développeur web.  
Il produit un profil pentester Web et API opérationnel, capable de conduire des tests d'intrusion applicatifs en environnement professionnel dans un cadre légal et éthique explicite.

**Point d'entrée recommandé : [Fondamentaux IT](../../bases/index.md) — puis [Développement & Stack TALL](../../dev-cloud/index.md) — puis [Cyber : Attaque](../../cyber/tools/index.md).**

!!! note "Pour comparer ce profil avec les autres parcours disponibles, consultez la page [Compréhension](../comprehension.md)."

<br />