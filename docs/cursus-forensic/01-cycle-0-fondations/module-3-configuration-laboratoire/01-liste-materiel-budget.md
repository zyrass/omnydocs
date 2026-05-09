---
description: "Liste complète et raisonnée du matériel pour votre laboratoire forensic physique. Trois niveaux de budget (essentiel, recommandé, avancé), avec sources d'achat et critères de choix."
icon: lucide/wallet
tags: ["MATÉRIEL", "BUDGET", "HOMELAB", "CONFIGURATION"]
---

# Liste matériel et budget

<div
  class="omny-meta"
  data-level="🟡 Standard"
  data-version="Modèle 2026"
  data-time="2 heures">
</div>

!!! note "**Livrables :** _Liste des courses pour le laboratoire_"
!!! note "**Auto-explication :** _10 minutes_"

<br>

---

<br>

!!! quote "L'analogie de l'atelier de menuisier"

    Un menuisier débutant peut commencer avec une scie, un marteau, et quelques clous. Au fil du temps, son atelier s'enrichit : raboteuse, dégauchisseuse, défonceuse, scie radiale. Chaque outil ajouté élargit le périmètre de ses ouvrages possibles. Mais surtout : un mauvais outil rend le travail mauvais quel que soit le talent. 
    Pour votre laboratoire forensic, le principe est identique. Il faut un minimum d'outils dès le départ, et leurs caractéristiques doivent être cohérentes avec votre objectif d'apprendre par la pratique.

## Objectifs pédagogiques

!!! tip "À la fin de ce chapitre, vous serez capable de :"

    - Identifier les composants essentiels d'un laboratoire Forensic.
    - Adapter votre laboratoire selon votre budget.
    - Comprendre l'importance cruciale du Write-Blocker matériel.
    - Sélectionner le matériel approprié pour des attaques et analyses spécifiques (ex: Wi-Fi, Mac).

<br>

---

<br>

## Trois niveaux de budget

Votre laboratoire peut évoluer. Nous l'avons divisé en trois niveaux selon vos moyens initiaux.

> Voici la répartition budgétaire cible :

| Niveau | Budget | Public cible |
|---|---|---|
| **Essentiel** | 600 - 800 € | Démarrage strict, tient le cycle 1 |
| **Recommandé** | 800 - 1 200 € | Cycle complet OmnyAcademy confortablement |
| **Avancé** | 1 500 - 2 500 € | Vise une carrière forensic professionnelle autonome |

<br>

---

<br>

## Niveau Essentiel - 600 à 800 €

Ce niveau est le minimum vital pour ne pas être bloqué dans les exercices.

### La liste d'achat

> Le tableau ci-dessous détaille le kit de survie du forensic :

| Catégorie | Élément recommandé | Prix indicatif | Notes |
|---|---|---|---|
| **Routeur** | TP-Link Archer C7 V5 | 30-50 € | Compatible OpenWrt, à trouver d'occasion. |
| **Postes (x2)** | Mini PC i5 8e gen (Reconditionnés) | 350-500 € | 8 Go RAM, SSD 256 Go minimum. |
| **Serveur** | Raspberry Pi 4 (8 Go) + SD 64 Go | 80-100 € | Pour héberger les services d'attaque. |
| **Switch** | Switch 5 ports gigabit (Non managé) | 15-20 € | TP-Link ou Netgear. |
| **Câbles** | Lot de 5 câbles RJ45 (Cat.6) | 15 € | Tailles mixtes (1 m, 3 m, 5 m). |
| **Wi-Fi** | Carte Alfa AWUS036ACS | 40-50 € | Mode monitor obligatoire pour le module 5. |
| **Stockage** | 1 SSD externe 256 Go | 30-40 € | Essentiel pour les acquisitions RAM/Disque. |
| **Stockage** | 4 clés USB 32 Go | 25-30 € | Pour les OS Live (Kali, CAINE) et les scellés. |

!!! danger "Les Limites du niveau Essentiel"
    Avec ce budget, vous couvrez les cycles 0 et 1. Cependant, vous ne pourrez pas monter de véritable **Active Directory** (un Raspberry Pi ne fait pas tourner Windows Server nativement) et vous n'aurez pas de **Write-Blocker matériel**, vous forçant à des manipulations logicielles risquées.

<br>

---

<br>

## Niveau Recommandé - 800 à 1 200 €

C'est le niveau cible pour suivre confortablement l'ensemble de la formation OmnyAcademy.

### Les améliorations (Upgrades)

> Le tableau ci-dessous détaille les ajouts par rapport au niveau essentiel :

| Élément | Upgrade recommandé | Surcoût estimé |
|---|---|---|
| **Postes** | 2 portables d'occasion (16 Go RAM) | +150 € |
| **Serveur** | Mini PC Intel N100 (16 Go RAM) | +100 € |
| **Stockage** | 2 SSD externes de 512 Go | +50 € |
| **Write-Blocker** | USB write-blocker (Tableau ou WiebeTech) | +100 € |
| **Pochette** | Sacoche Faraday (Isolation ondes) | +30 € |

!!! success "Bénéfices du niveau Recommandé"
    Ce budget permet de déployer un vrai domaine **Active Directory** sur le mini PC Intel, de réaliser des acquisitions disques de grande taille sans saturer vos espaces, et surtout, d'apprendre la manipulation légale avec un vrai **Write-Blocker**.

<br>

---

<br>

## Niveau Avancé - 1 500 à 2 500 €

Pour ceux qui visent l'installation d'un laboratoire professionnel permanent.

### L'équipement pro

> Le tableau ci-dessous liste l'équipement d'un analyste confirmé :

| Élément | Surcoût estimé | Objectif |
|---|---|---|
| **Portable Attaquant** | +400 € | PC dédié uniquement à Kali Linux (Pas de VM). |
| **Portable Analyste** | +400 € | PC dédié uniquement à CAINE/SIFT. |
| **Connectique** | +50 € | Hub USB-C alimenté pour supporter plusieurs acquisitions. |
| **Extracteur** | +50 € | Lecteur/Dock pour disques durs internes (SATA/NVMe). |
| **Stockage Froid** | +200 € | NAS de 4 To pour l'archivage des preuves. |
| **Énergie** | +100 € | Onduleur (UPS) pour protéger les acquisitions en cours. |

<br>

---

<br>

## Détail des choix critiques

### Pourquoi le TP-Link Archer C7 ?

!!! abstract "Le choix du Routeur"
    - **Prix :** 30-50 € en reconditionné.
    - **OpenWrt :** La version V5 est officiellement et parfaitement supportée.
    - **Performances :** Dual band, CPU à 720 MHz et 128 Mo de RAM. Largement suffisant pour isoler notre labo.
    - *Alternative :* Linksys WRT3200ACM si le budget le permet (60-80 €).

### Pourquoi l'Alfa AWUS036ACS ?

!!! abstract "Le choix de la carte Wi-Fi"
    - **Le chipset :** Realtek RTL8812AU. Il gère nativement le **Mode Monitor** et l'**Injection de paquets**.
    - **Compatibilité :** Les drivers Linux (`aircrack-ng`) sont extrêmement stables.
    - **Le piège :** N'essayez jamais d'utiliser la carte Wi-Fi interne de votre PC portable pour le pentest, le mode monitor est quasiment toujours verrouillé par les fabricants.

### Le Write-Blocker : L'outil ultime

!!! warning "L'importance du bloqueur en écriture"
    Un **write-blocker** matériel est l'outil qui distingue un bidouilleur d'un expert Forensic. Il se place entre le disque suspect et votre PC d'analyse, et coupe physiquement les broches d'écriture. Il garantit au juge qu'absolument rien n'a pu être altéré sur la preuve. Pour commencer, un modèle USB (WiebeTech ou Tableau) à 100€ est parfait.

### Cible macOS : Votre MacBook M1

!!! info "Le cas Apple Silicon"
    Si vous possédez déjà un MacBook M1 (8 Go), il devient votre **cible Mac** par défaut. C'est idéal : vous ferez face au véritable *Secure Enclave*, au *FileVault* matériel et aux restrictions SIP d'Apple. Cependant, ses 8 Go de RAM en font une mauvaise machine d'analyse pour traiter de gros dumps.

<br>

---

<br>

## Synthèse budgétaire

!!! quote "Mémo d'investissement"
    
    ```text
    PRIORITÉS D'ACHAT (En cas de budget serré) :
    
    1. Routeur OpenWrt              (25-50 €)
    2. Carte Wi-Fi Alfa             (40-50 €)
    3. 2 postes Windows             (350-500 €)
    4. Serveur Linux                (80-150 €)
    5. Stockage SSD externe         (30-50 €)
    6. Write-blocker (différable)   (100-150 €)
    
    MATÉRIEL DÉJÀ ACQUIS (À intégrer) :
    - PC Windows 48 Go (Poste analyste principal)
    - MacBook M1 8 Go (Cible analyse Mac)
    
    RÈGLE D'OR : Privilégier le Reconditionné > Occasion > Neuf.
    ```

<br>

---

<br>

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Votre laboratoire n'a pas besoin d'être parfait dès le premier jour. Investissez dans l'infrastructure réseau (Routeur OpenWrt) et l'équipement d'acquisition de base (SSD, Carte Wi-Fi monitor). Le reste (Write-blocker matériel, NAS, onduleur) viendra avec la professionnalisation de votre pratique. 

> [Chapitre suivant : 3.2 Achats reconditionnés - sources et précautions →](02-achats-reconditionne.md)
>
> [Retour à l'index →](./index.md)

<br>
