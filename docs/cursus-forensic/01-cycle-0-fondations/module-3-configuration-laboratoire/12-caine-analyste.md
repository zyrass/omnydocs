---
title: 3.12 CAINE 13 portable analyste
description: Configuration d'un environnement CAINE Linux dédié à l'analyse forensic. Distribution forensic-friendly italienne, write-blocker logiciel intégré, outils Sleuth Kit, Autopsy, RegRipper, Volatility.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - CAINE
  - Forensic
  - Analyste
  - Sleuth Kit
data-level: 🔴
---

# 3.12 CAINE 13 portable analyste

!!! quote "L'analogie de la salle d'autopsie"

    Une salle d'autopsie médico-légale n'est pas un bloc opératoire ordinaire. Elle est conçue pour préserver l'intégrité des preuves : surfaces inox, instruments stérilisés, traçabilité de chaque geste. CAINE est l'équivalent numérique. C'est une distribution conçue pour la forensic avec des garanties que peu de Linux offrent : montage automatique en lecture seule, write-blocker logiciel actif, outils préinstallés, traçabilité.

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 3 heures |
| Niveau | Pratique |

## 1. Pourquoi CAINE

CAINE (Computer Aided INvestigative Environment) est une distribution Linux italienne **dédiée à la forensic numérique**. Caractéristiques clés :

| Feature | Description |
|---|---|
| Write-blocker logiciel | Activé par défaut |
| Montage RO automatique | Toute clé/disque branchée |
| Outils préinstallés | Sleuth Kit, Autopsy, Volatility, RegRipper |
| Maintenance | Active depuis 2008 |
| Live et installable | USB live ou disque |

Version cible : **CAINE 13.X** (ou plus récente en 2026).

## 2. Téléchargement et installation

### 2.1 Téléchargement

```bash
# Site officiel
wget https://www.caine-live.net/page5/page5.html  # voir lien direct

# ISO typique (4-5 Go)
# caine13.0.iso ou plus récent

# Vérification SHA-256
sha256sum caine13.0.iso
# Comparer avec hash publié sur le site
```

### 2.2 Création USB live

```bash
# Linux/macOS
sudo dd if=caine13.0.iso of=/dev/sdX bs=4M status=progress conv=fdatasync

# Windows : Rufus en mode DD
```

### 2.3 Boot et test

| Action | Précision |
|---|---|
| Boot USB | Sélectionner CAINE Live |
| Mode | Live (sans installation) ou Install |
| Recommandation OmnyAcademy | Installation sur portable dédié |

## 3. Outils principaux

### 3.1 Acquisition

| Outil | Usage |
|---|---|
| dd, dc3dd | Acquisition disque |
| ewfacquire | Format E01 (recommandé) |
| Guymager | Interface graphique acquisition |
| AVML | Acquisition mémoire Linux |

### 3.2 Analyse système de fichiers

| Outil | Usage |
|---|---|
| Sleuth Kit (TSK) | Suite forensic |
| Autopsy | GUI sur TSK |
| fls, icat, mmls | Sleuth Kit CLI |
| testdisk, photorec | Récupération |
| extundelete, ext4magic | Récupération ext |
| analyzeMFT | NTFS MFT |

### 3.3 Mémoire

| Outil | Usage |
|---|---|
| Volatility 3 | Framework analyse mémoire |
| Volatility plugins | Windows, Linux, macOS |
| memdump, malfind | Plugins courants |

### 3.4 Windows artefacts

| Outil | Usage |
|---|---|
| RegRipper | Analyse registre |
| LECmd | Lien LNK |
| MFTECmd | MFT NTFS |
| AppCompatCacheParser | ShimCache |
| AmcacheParser | Amcache |

### 3.5 macOS artefacts

| Outil | Usage |
|---|---|
| mac_apt | Framework Python |
| AutoMacTC | Triage |
| log2timeline / Plaso | Timeline |

### 3.6 Timeline

| Outil | Usage |
|---|---|
| Plaso (log2timeline) | Timeline universelle |
| mactime | Sleuth Kit timeline |
| Timeline Explorer | GUI Windows |

## 4. Configuration réseau

```bash
# IP statique vers labo
sudo ip addr add 192.168.50.251/24 dev eth0
sudo ip route add default via 192.168.50.1
echo "nameserver 192.168.50.1" | sudo tee /etc/resolv.conf

# Persistance via Network Manager
sudo nmtui
```

## 5. Workflow forensic OmnyAcademy

### 5.1 Acquisition d'un disque

```bash
# Identifier le disque suspect
sudo lsblk

# Acquisition E01 avec hash
sudo ewfacquire /dev/sdX
# Renseigner :
# - Case number, Evidence number
# - Description, Examiner name
# - Notes
# - Format : E01
# - Compression : best
# - Bytes per sector : 512
# - Block size : 64
# - Hash : SHA-256

# Vérification
ewfverify image.E01
```

### 5.2 Analyse rapide

```bash
# Monter en lecture seule
sudo ewfmount image.E01 /mnt/ewf
sudo mmls /mnt/ewf/ewf1
# Identifier la partition d'intérêt et son offset

# Listing des fichiers
sudo fls -r -m / -o [offset] /mnt/ewf/ewf1 > body.txt

# Timeline
mactime -b body.txt -d -y > timeline.csv

# Inspection
head -50 timeline.csv
grep "2026-03-12" timeline.csv
```

### 5.3 Lancement Autopsy GUI

```bash
# Démarrer le service
autopsy

# Ouvrir le navigateur sur l'URL indiquée
# http://localhost:9999/autopsy
```

## 6. Préparation espace de travail

```bash
# Structure répertoire
mkdir -p ~/cas/2026-03-XX-artech/{acquisitions,analyses,rapports,timeline,extracted}

# Documentation
cat > ~/cas/2026-03-XX-artech/README.md <<EOF
CAS FORENSIC - ARTECH 2026-03-XX
==================================

Date d'engagement : 2026-XX-XX
Mandat : copie disponible /mandats/
Examiner : Zyrass (OmnyVia)

ÉQUIPEMENTS À ANALYSER
- Disque Win-Compta : SHA-256 ...
- Disque Win-Stage : SHA-256 ...
- Mac M1 : acquisition logique
- Capture mémoire : ...

JOURNAL DE PROGRESSION
[à compléter]
EOF
```

## 7. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Que signifie CAINE ? | Computer Aided INvestigative Environment |
| 2 | Write-blocker dans CAINE ? | Logiciel par défaut |
| 3 | Format d'image standard ? | E01 (EWF) |
| 4 | Outil acquisition GUI ? | Guymager |
| 5 | Framework mémoire ? | Volatility 3 |
| 6 | Outil registre Windows ? | RegRipper |
| 7 | Timeline universelle ? | Plaso / log2timeline |

---

**Chapitre suivant** : [3.13 Carte Wi-Fi Alfa AWUS036ACS](03-13-alfa-wifi.md)
