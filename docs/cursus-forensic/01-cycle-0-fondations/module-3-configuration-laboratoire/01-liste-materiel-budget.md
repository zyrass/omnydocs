---
title: 3.1 Liste matériel et budget
description: Liste complète et raisonnée du matériel pour votre laboratoire forensic physique. Trois niveaux de budget (essentiel, recommandé, avancé), avec sources d'achat et critères de choix.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Matériel
  - Budget
  - HomeLab
  - Configuration
data-level: 🟡
---

# 3.1 Liste matériel et budget

!!! quote "L'analogie de l'atelier de menuisier"

    Un menuisier débutant peut commencer avec une scie, un marteau, et quelques clous. Au fil du temps, son atelier s'enrichit : raboteuse, dégauchisseuse, défonceuse, scie radiale. Chaque outil ajouté élargit le périmètre de ses ouvrages possibles. Mais surtout : un mauvais outil rend le travail mauvais quel que soit le talent. Pour votre laboratoire forensic, le principe est identique. Il faut un minimum d'outils dès le départ, et leurs caractéristiques doivent être cohérentes avec votre objectif d'apprendre par l'attaque.

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 2 heures |
| Type | Théorique préparatoire |

## 1. Trois niveaux de budget

| Niveau | Budget | Public |
|---|---|---|
| Essentiel | 600 - 800 € | Démarrage strict, tient le cycle 1 |
| Recommandé | 800 - 1 200 € | Cycle complet OmnyAcademy confortablement |
| Avancé | 1 500 - 2 500 € | Vise une carrière forensic professionnelle |

## 2. Niveau Essentiel - 600 à 800 €

### 2.1 Liste

| Catégorie | Élément | Prix indicatif | Notes |
|---|---|---|---|
| Routeur | TP-Link Archer C7 V5 | 30-50 € | Compatible OpenWrt, recyclé |
| Postes | 2 mini PC i5 8e gen reconditionné | 350-500 € (les 2) | 8 Go RAM, SSD 256 Go |
| Serveur | Raspberry Pi 4 8 Go + carte SD 64 Go | 80-100 € | Ou recyclage PC ancien |
| Switch | Switch 5 ports gigabit non managé | 15-20 € | TP-Link ou Netgear |
| Câbles | Lot 5 câbles RJ45 cat.6 | 15 € | 1 m, 3 m, 5 m |
| Wi-Fi | Carte Alfa AWUS036ACS | 40-50 € | Mode monitor obligatoire |
| Storage | 1 SSD externe 256 Go | 30-40 € | Pour acquisitions |
| Storage | 4 clés USB 32 Go | 25-30 € | Outils, scellés |

**Total Essentiel : ~600-800 €**

### 2.2 Limites

Avec ce budget, vous tenez le cycle 0 et le début du cycle 1. Limitations :

- Pas d'Active Directory (un Pi ne fait pas tourner Windows Server)
- Pas de write-blocker matériel (utilisation logicielle uniquement)
- Acquisitions disque limitées en taille

## 3. Niveau Recommandé - 800 à 1 200 €

### 3.1 Différences avec Essentiel

| Élément | Upgrade | Surcoût |
|---|---|---|
| Postes | 2 portables d'occasion 16 Go | +150 € |
| Serveur | Mini PC Intel N100 16 Go | +100 € |
| Storage | 2 SSD 512 Go | +50 € |
| Write-blocker | USB write-blocker (Tableau ou WiebeTech) | +100 € |
| Faraday | Sacoche faraday | +30 € |

**Total Recommandé : ~1 100-1 200 €**

### 3.2 Bénéfices

- Active Directory possible (Windows Server eval ou Samba AD)
- Acquisitions disques réelles complètes
- Manipulations forensic conformes (write-blocker)

## 4. Niveau Avancé - 1 500 à 2 500 €

### 4.1 Ajouts

| Élément | Prix |
|---|---|
| 2e portable Kali dédié | +400 € |
| 3e portable CAINE dédié | +400 € |
| Hub USB-C alimenté | +50 € |
| Lecteur disques durs internes | +50 € |
| 4 To stockage NAS | +200 € |
| Onduleur petit format | +100 € |

### 4.2 Justification

Le niveau avancé permet :

- Forensic à grande échelle
- Acquisitions parallèles
- Postes dédiés par fonction (pas multi-boot)
- Continuité matérielle (onduleur)

## 5. Détail des choix critiques

### 5.1 Pourquoi le TP-Link Archer C7

| Critère | Réponse |
|---|---|
| Prix | 30-50 € reconditionné |
| Disponibilité | Très répandu, faciles à trouver |
| OpenWrt | Compatible officiellement V5 |
| Wi-Fi | Dual band, suffisant pour labo |
| CPU | 720 MHz, OK pour OpenWrt |
| RAM | 128 Mo suffisants |
| Documentation | Très bien documenté |

**Alternative** : Linksys WRT3200ACM si budget plus large (60-80 €).

### 5.2 Pourquoi Apple Silicon en cible

Vous avez déjà un MacBook M1 8 Go, qui devient **votre cible Mac** pour le forensic. Avantages :

- Apple Silicon authentique
- FileVault et Secure Enclave réels
- APFS et SSV en conditions réelles

Limites : 8 Go = pas pour analyser de gros dumps. C'est une **cible**, pas un poste analyste.

### 5.3 Pourquoi Alfa AWUS036ACS spécifiquement

| Critère | Réponse |
|---|---|
| Mode monitor | Oui (Realtek RTL8812AU) |
| Injection | Oui |
| Linux drivers | Stables (aircrack-ng) |
| Bandes | 2.4 + 5 GHz |
| Antenne | Externe haute portée |
| Prix | 40-50 € |
| Référence | Standard pentest |

**Important** : éviter les cartes Wi-Fi internes des PC/portables, le mode monitor n'est presque jamais possible.

### 5.4 Write-blocker - Critique forensic

Un **write-blocker** matériel est l'outil qui distingue un forensic amateur d'un forensic professionnel. Il garantit qu'aucune écriture n'est faite sur le disque suspect.

| Type | Prix | Usage |
|---|---|---|
| Logiciel (mode kernel) | 0 € | Apprentissage uniquement |
| USB write-blocker | 80-150 € | Recommandé minimum |
| FireWire/Thunderbolt | 200-400 € | Plus rapide |
| Stations forensic complètes | 1500+ € | Pro |

**Pour OmnyAcademy** : USB write-blocker suffit.

## 6. Sources d'achat reconditionné

### 6.1 Sites recommandés

| Site | Spécialité |
|---|---|
| Backmarket | Postes et téléphones reconditionnés |
| Recommerce | Matériel pro |
| Retron | PCs reconditionnés |
| ITEK | Serveurs et matériel pro |
| Le Bon Coin | Particuliers (vigilance) |
| eBay | International, vigilance contrefaçon |
| Amazon Renewed | Garanties |
| AliExpress | Cartes Wi-Fi spécialisées |

### 6.2 Critères de vérification

| Critère | Vérification |
|---|---|
| Garantie | Minimum 6 mois |
| État | Grade A ou B (cosmétique acceptable) |
| Specs | Vérifier RAM/SSD vs annonce |
| Origine | Privilégier France/UE pour garantie |
| Avis vendeur | >95% satisfaction |
| Effacement | Vérifier secure erase fait |

### 6.3 Précautions

| Risque | Mitigation |
|---|---|
| Hardware faible | Demander photo Bench |
| Espionnage matériel | Réinstallation OS systématique |
| Pas de garantie | Refuser si pas de garantie écrite |
| BIOS verrouillé | Vérifier accès BIOS au déballage |

## 7. Synthèse budgétaire

```text
LABORATOIRE OMNYACADEMY - BUDGET

NIVEAU ESSENTIEL    600-800 €
NIVEAU RECOMMANDÉ   800-1200 €
NIVEAU AVANCÉ       1500-2500 €

PRIORITÉS d'investissement (si budget limité) :
  1. Routeur OpenWrt              25-50 €
  2. Carte Wi-Fi Alfa             40-50 €
  3. 2 postes Windows              350-500 €
  4. Serveur Linux                 80-150 €
  5. Stockage SSD externe          30-50 €
  6. Write-blocker (différable)    100-150 €

À utiliser depuis votre matériel existant :
  - PC Windows 48 Go (poste analyste principal)
  - MacBook M1 8 Go (cible analyse Mac)

Sources : reconditionné > occasion > neuf
```

---

**Chapitre suivant** : [3.2 Achats reconditionnés - sources et précautions](03-2-achats-reconditionne.md)
