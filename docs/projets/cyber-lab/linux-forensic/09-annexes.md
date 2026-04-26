---
description: "Module 9 - Annexes de l'investigation numérique : glossaire, récapitulatif des outils utilisés et certifications reconnues."
---

# Module 9 - Annexes

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Ressources"
  data-time="~10 min">
</div>

## Introduction

!!! quote "Analogie pédagogique — La boîte à outils du détective"
    Les annexes ne se lisent pas de bout en bout comme un roman. C'est votre boîte à outils. Vous y revenez quand vous cherchez une définition précise pour un rapport, un outil de remplacement, ou de l'inspiration pour passer une certification de spécialité.

## 9.1 - Glossaire Forensic

| Terme | Définition technique simplifiée |
|---|---|
| **Artefact** | Trace numérique laissée par une activité système ou utilisateur. |
| **Carving** | Technique de récupération de fichiers supprimés basée sur leur signature binaire (Magic Numbers), indépendamment de l'index du système de fichiers. |
| **Chaîne de garde** | *Chain of Custody*. Procédure documentaire stricte (hashs, dates, signatures) prouvant qu'une preuve numérique n'a jamais été altérée depuis sa saisie. |
| **Dump** | Copie brute et non structurée du contenu d'une mémoire (RAM) ou d'un support de stockage. |
| **Hash / Empreinte** | Signature cryptographique (ex: SHA-256) garantissant l'intégrité absolue d'un fichier. Si 1 bit change, le hash entier change. |
| **Inode** | Structure de données sous Linux (ext4) décrivant un fichier (ses permissions, ses dates de modification, et l'adresse physique de ses blocs sur le disque). |
| **Symboles Noyau** | Fichier dictionnaire décrivant l'organisation exacte de la RAM pour une version précise de Linux. Indispensable pour Volatility. |
| **Volatilité** | Caractère éphémère d'une donnée. La RAM est hautement volatile (disparaît à l'arrêt), le disque dur est persistant. |

<br>

---

## 9.2 - Récapitulatif des outils de l'analyste

La distribution **Kali Linux** contient par défaut 95% de ces outils.

| Outil | Rôle dans l'investigation | Site officiel / Dépôt |
|---|---|---|
| **dc3dd** | Clonage forensique bit à bit avec calcul de hash simultané. | `sourceforge.net/projects/dc3dd` |
| **Volatility 3** | Framework d'analyse et de traduction de la mémoire vive (RAM). | `volatilityfoundation.org` |
| **PhotoRec** | Outil puissant de *File Carving* en ligne de commande. | `cgsecurity.org` |
| **Sleuth Kit** | Suite d'analyse complète de systèmes de fichiers (inodes, partitions). | `sleuthkit.org` |
| **Autopsy** | Interface graphique web simplifiant l'utilisation de Sleuth Kit. | `sleuthkit.org/autopsy` |
| **Foremost** | Alternative historique à PhotoRec pour le carving de base. | `foremost.sourceforge.net` |

<br>

---

## 9.3 - Pour aller plus loin (Certifications et Labs)

L'investigation numérique est un domaine de spécialité très recherché sur le marché de la cybersécurité. Voici comment officialiser vos compétences.

### Les certifications internationales

| Certification | Émetteur | Niveau | Coût indicatif |
|---|---|---|---|
| **GCFA** (GIAC Certified Forensic Analyst) | SANS Institute | Avancé | ~7 500 € |
| **GCFE** (GIAC Certified Forensic Examiner) | SANS Institute | Intermédiaire | ~7 500 € |
| **EnCE** (EnCase Certified Examiner) | OpenText | Spécialiste | ~3 500 € |
| **CCE** (Certified Computer Examiner) | ISFCE | Intermédiaire | ~1 500 € |

### Entraînement en laboratoire gratuit

Ne testez pas vos outils sur vos machines personnelles, utilisez les environnements en ligne conçus pour cela :

- **Cyberdefenders.org** : Propose des challenges et des "Blue Team Labs" dédiés au forensic, avec des dumps mémoire à analyser (gratuit).
- **DFIR.training** : Immense annuaire de ressources, d'outils et de challenges Digital Forensics & Incident Response.
- **HackTheBox - Forensics** : Des scénarios variés allant de la récupération de logs serveur à l'analyse de malwares.
- **TryHackMe - Chemin DFIR** : Un parcours guidé pas à pas pour les grands débutants.

<br>

---

## Conclusion générale du cours

!!! quote "Le mot de la fin"
    L'investigation numérique est un **métier de méthode** avant d'être un métier d'outils. Les outils changent (Volatility 2 est devenu Volatility 3, les disques durs deviennent des SSD), mais la méthodologie juridique reste. Concentrez-vous sur la rigueur procédurale, l'horodatage systématique et la traçabilité de chaque action : c'est l'unique barrière qui distingue un rapport recevable d'un rapport rejeté au tribunal.

> Revenir à la page d'accueil de la section : **[Lab — Cybersécurité →](../index.md)**
