---
title: Inventaire Matériel
description: Liste exhaustive du hardware nécessaire pour un laboratoire forensic et offensif physique. Budget, avantages et équipement de pointe.
icon: lucide/book-open-check
tags:
  - Hardware
  - Laboratoire
  - Budget
  - Équipement
---

# Inventaire Matériel du Laboratoire

!!! abstract "Physique vs Virtuel : L'importance du matériel réel"
    
    Il est tentant de tout virtualiser (VMware, Proxmox) pour économiser du budget. C'est suffisant pour faire du développement ou de l'analyse basique de malware, mais **totalement insuffisant pour un cursus Forensic complet**.
    L'investigation numérique repose sur des interactions matérielles complexes : l'extraction de RAM physique, le contournement des puces TPM (BitLocker), les ponts réseau matériels, ou l'acquisition de disques natifs. Apprendre uniquement sur des machines virtuelles, c'est comme apprendre à piloter sur simulateur sans jamais toucher un vrai moteur. De plus, une machine virtuelle ne vous préparera jamais aux problématiques de **chaîne de garde** et d'intégrité devant un tribunal.

Ce document liste l'équipement complet pour constituer votre laboratoire hybride (Offensif et Forensic) pour les 24 prochains mois.

<br>

---

## 1. L'équipement Forensic & Intégrité (La Preuve Légale)

Pour qu'une preuve soit recevable devant un juge, vous devez garantir que **rien n'a été altéré** lors de son acquisition. Une simple copie sous Windows modifiera les métadonnées (dates d'accès).

### Le Bloqueur d'écriture matériel (Write-Blocker)
C'est la pièce maîtresse du forensicien physique. Il se place entre le disque suspect et votre ordinateur d'analyse, et bloque matériellement toute commande d'écriture.

- **Modèle de référence** : Tableau T8u (USB 3.0) ou WiebeTech UltraBlock.  
- **Budget** : 300 € à 600 € (selon les adaptateurs SATA/NVMe).  
- **Avantages** : L'outil est certifié. Devant un tribunal, l'utilisation d'un bloqueur matériel coupe court à tout débat sur la modification accidentelle des preuves par l'enquêteur.  
- **Inconvénients** : Coût élevé pour un particulier, nécessite plusieurs adaptateurs selon les formats de disques rencontrés.  

### La Tablette de collecte et documentation
Lors d'une saisie physique (Search & Seizure), la documentation visuelle est critique.

- **Modèle** : Tablette iPad ou Android avec un bon capteur photo et une application de prise de notes structurée.  
- **Budget** : 300 € à 500 €.  
- **Avantages** : Permet de photographier l'état des écrans, les connexions de câbles avant démontage, et de remplir les formulaires de chaîne de garde (Chain of Custody) en mobilité. Autonomie excellente sur le terrain.

<br>

---

## 2. L'arsenal Offensif (La Red Team)

Pour comprendre comment enquêter, il faut savoir attaquer avec les bons outils.

### Le PC Portable d'Attaque (Station Hacker)
Une machine dédiée exclusivement aux opérations offensives.

- **OS Recommandé** : Kali Linux, Parrot OS, ou une distribution **Arch Linux** montée de toutes pièces (ce qui fera l'objet d'un projet fil rouge dans ce cursus).  
- **Budget** : 500 € à 800 € (ThinkPad reconditionné type T480/T490 est idéal).  
- **Avantages** : Isolation totale de vos données personnelles. Vous pouvez le connecter à des réseaux compromis sans risque. L'utilisation d'Arch Linux vous forcera à comprendre chaque couche de votre OS.  
- **Inconvénients** : Demande de l'entretien (mises à jour rolling-release sur Arch), batterie parfois capricieuse sous Linux.  

### La Clé Wi-Fi Monitor Mode & Injection
Indispensable pour l'audit sans-fil (WPA2/WPA3, Evil Twin, deauth attacks). Les cartes Wi-Fi internes des PC portables ne supportent presque jamais l'injection de paquets.

- **Modèle de référence** : Alfa Network (ex: AWUS036ACH ou AWUS036NHA).  
- **Budget** : 50 € à 80 €.  
- **Avantages** : Support natif du mode Monitor (écoute passive de tout le trafic aérien) et capacité d'injection de paquets. Antennes à haut gain pour une portée massive.  
- **Inconvénients** : Encombrant physiquement, l'installation des drivers sous certains kernels récents peut être fastidieuse.  

<br>

---

## 3. Le cœur du laboratoire (Les cibles et serveurs)

C'est ici que les attaques sont menées et que les traces sont générées.

### 2x PC Windows Physiques
Deux machines pour simuler un véritable réseau d'entreprise (ex: un poste utilisateur et un contrôleur de domaine / serveur de fichiers).

- **Modèles** : Mini-PC (type Dell OptiPlex Micro ou Lenovo Tiny) reconditionnés.  
- **Budget** : ~200 € l'unité (soit 400 €).  
- **Avantages** : Permet de tester les vraies protections Microsoft (BitLocker lié au vrai composant TPM de la carte mère, Secure Boot, Credential Guard). Permet aussi de pratiquer l'extraction de mémoire vive (RAM) avec des clés USB.  
- **Inconvénients** : Consommation électrique, encombrement de l'espace de travail.  

### Le MacBook Neo (Architecture ARM / M-Series)
L'écosystème Apple est incontournable aujourd'hui, et son forensic est radicalement différent de Windows/Linux.

- **Modèle** : MacBook Air M1 (minimum) ou Mac Mini M1/M2.  
- **Budget** : 600 € à 800 € (reconditionné).  
- **Avantages** : Accès à l'architecture Apple Silicon, au système APFS natif, et à l'interaction avec la Secure Enclave et FileVault. Sans lui, impossible de se former au forensic macOS moderne.  
- **Inconvénients** : Écosystème fermé, évolutivité matérielle nulle (RAM soudée).  

### Le Mini Serveur Linux (L'infrastructure)
Pour héberger vos outils de détection, vos proxys, et simuler l'infrastructure réseau.

- **Modèle** : Intel NUC, Raspberry Pi 5 (avec SSD), ou Mini-PC générique.  
- **Budget** : 150 € à 300 €.  
- **Avantages** : Consommation électrique minime (Always-On). Parfait pour faire tourner un SIEM (Wazuh), un pare-feu (pfSense/OPNsense) ou héberger les payloads et C2 de vos malwares en local.  
- **Inconvénients** : Puissance de calcul parfois limitée si plusieurs machines virtuelles doivent y tourner simultanément.  

<br>

---

## 4. Synthèse du Budget (Objectif 24 mois)

Voici une projection budgétaire. **Rappel : cet équipement doit être acquis progressivement au fil de votre montée en compétence, et non en une seule fois.**

| Équipement | Rôle principal | Budget estimé | Priorité d'achat |
|---|---|---|---|
| Clé Wi-Fi Alfa Network | Attaques réseaux | ~60 € | Haute (Cycle 1) |
| Mini Serveur Linux | Déploiement du labo / SIEM | ~200 € | Haute (Cycle 1) |
| 2x PC Windows Physiques | Cibles réalistes & extraction RAM | ~400 € | Haute (Cycle 1) |
| PC Portable Attaque (Arch/Kali) | Isolation offensive | ~600 € | Moyenne (Cycle 2) |
| Tablette de collecte | Documentation de scène | ~400 € | Moyenne (Cycle 2) |
| MacBook M1 | Forensic écosystème Apple | ~700 € | Basse (Cycle 2/3) |
| Write-Blocker Matériel | Acquisition certifiée | ~400 € | Basse (Cycle 3) |
| **TOTAL ESTIMÉ** | | **~2 760 €** | *(Sur 24 mois)* |

<br>

---

## Conclusion

!!! quote "Le prix de l'excellence"
    
    > Un budget d'environ 2500 € à 3000 € étalé sur deux ans représente le prix d'un seul module dans une formation d'ingénieur en sécurité. Posséder ce matériel vous permettra de manipuler la réalité du terrain et de vous présenter devant un recruteur ou un juge avec une crédibilité absolue.
