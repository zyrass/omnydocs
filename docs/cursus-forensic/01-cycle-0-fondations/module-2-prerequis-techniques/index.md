---
title: Module 2 - Prérequis techniques et théoriques
description: Module fondateur des compétences techniques pour le forensic. Linux, Windows, macOS, réseaux, cryptographie, systèmes de fichiers (NTFS, ext4, APFS), MITRE ATT&CK. 78 heures de mise à niveau et d'approfondissement.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Prérequis
  - Linux
  - Windows
  - macOS
  - Réseaux
  - Cryptographie
  - MITRE
data-level: 🟡
---

# II - Prérequis techniques

!!! quote "L'analogie de l'orchestre symphonique"

    Un chef d'orchestre dirige soixante musiciens. Pour le faire correctement, il doit connaître chaque instrument. Pas nécessairement en virtuose, mais suffisamment pour entendre quand le hautbois est désaccordé, quand la harpe ralentit, quand le timbalier anticipe. Il ne joue lui-même aucun instrument pendant le concert, mais sa connaissance de chacun lui permet de comprendre l'ensemble. L'analyste forensic est dans cette position. Il ne va pas tout reconfigurer, tout coder, tout chiffrer lui-même. Mais quand il analyse un poste compromis, il doit reconnaître les signaux faibles de chaque "instrument" du système : le registre Windows désaccordé, le journal systemd qui ralentit, le hash NTFS modifié. Sans cette connaissance transversale, il manque les indices. Ce module construit cette connaissance.

## Présentation du module

Ce module couvre les **prérequis techniques fondamentaux** indispensables à toute pratique du forensic numérique en environnement physique. Il représente **78 heures** réparties sur 17 chapitres (16 du programme initial + intégration du volet macOS).

### Pourquoi ce module est nécessaire

Trois constats motivent ce module :

| Constat | Réponse du module |
|---|---|
| Le forensic VM ne couvre pas les contraintes physiques | Approfondissement spécifique |
| Les analystes français méconnaissent souvent macOS | Chapitres dédiés Apple Silicon |
| Les systèmes de fichiers sont mal compris | Étude approfondie NTFS, ext4, APFS |

### Objectifs pédagogiques

À l'issue de ce module, vous serez capable de :

- Naviguer aisément en CLI Linux, Windows et macOS
- Comprendre les structures internes de chaque OS pour le forensic
- Maîtriser les concepts cryptographiques appliqués au forensic
- Lire et exploiter les structures NTFS, ext4 et APFS
- Appliquer le référentiel MITRE ATT&CK aux investigations
- Reconstituer une kill chain à partir d'observations

### Prérequis

| Critère | Niveau attendu |
|---|---|
| Connaissances de base Linux | Acquis |
| Connaissances de base Windows | Acquis |
| Notions macOS utilisateur | Bienvenu, pas indispensable |
| Réseaux TCP/IP | Notions de base |
| Cryptographie | Notions de base |

### Plan du module

| # | Chapitre | Durée | Niveau |
|---|---|---|---|
| 2.1 | Auto-évaluation diagnostique 80 questions | 2 h | Diagnostic |
| 2.2 | Linux fondamentaux | 6 h | Standard |
| 2.3 | Linux avancé | 6 h | Standard |
| 2.4 | Windows architecture pour forensic | 8 h | Standard |
| 2.4 bis | macOS architecture pour forensic | 8 h | Standard |
| 2.5 | PowerShell pour analyste | 6 h | Standard |
| 2.5 bis | Bash et zsh pour analyste macOS | 4 h | Standard |
| 2.6 | Réseaux TCP/IP approfondi | 4 h | Standard |
| 2.7 | Cryptographie symétrique et asymétrique | 4 h | Standard |
| 2.8 | Hash, signatures, X.509 | 3 h | Standard |
| 2.9 | NTFS en profondeur | 5 h | Exhaustif |
| 2.10 | ext4 en profondeur | 4 h | Exhaustif |
| 2.10 bis | APFS en profondeur | 6 h | Exhaustif |
| 2.11 | MITRE ATT&CK | 5 h | Standard |
| 2.12 | Cyber Kill Chain | 1 h | Standard |
| 2.13 | Diamond Model et Pyramid of Pain | 2 h | Standard |
| 2.14 | Mise en pratique kill chain ARTECH | 4 h | Pratique |

**Total : 78 heures** réparties sur 7-8 semaines à raison de 10h/semaine.

---

**Démarrage** : commencer par le chapitre 2.1 (Auto-évaluation diagnostique). Aucune manipulation matérielle requise pour les chapitres 2.1 à 2.13. Le matériel labo est nécessaire à partir du chapitre 2.14.
