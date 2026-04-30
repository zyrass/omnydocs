---
title: 3.11 Kali Linux portable attaquant
description: Configuration d'un portable Kali Linux dédié au rôle d'attaquant dans le laboratoire. Installation Kali 2026, outils essentiels (aircrack-ng, hashcat, Metasploit), méthodologie offensive éthique.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Kali Linux
  - Attaquant
  - Pentest
  - Offensive
data-level: 🔴
---

# 3.11 Kali Linux portable attaquant

!!! quote "L'analogie de l'épéiste s'entraînant face à un mannequin"

    Un épéiste ne s'entraîne pas en face d'un autre épéiste tout de suite. Il commence avec un mannequin, qui ne riposte pas, ne triche pas, ne change pas de stratégie. Le mannequin permet de répéter mille fois le même geste pour le perfectionner. Votre laboratoire ARTECH est ce mannequin. Kali Linux est votre épée. Ce chapitre vous donne l'arme et vous explique comment la manier dans le respect strict de la loi (votre propre lab).

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 3 heures |
| Niveau | Pratique |

## 1. Pourquoi Kali

| Critère | Réponse |
|---|---|
| Préinstallé | 600+ outils offensifs |
| Mises à jour | Hebdomadaires |
| Documentation | Très complète |
| Communauté | Énorme |
| Support hardware | Drivers Wi-Fi monitor inclus |

Version cible : **Kali Linux 2026.X** (rolling release).

## 2. Téléchargement et installation

### 2.1 Téléchargement

```bash
wget https://kali.download/base-images/current/kali-linux-2026.X-installer-amd64.iso

# Vérification SHA-256
wget https://kali.download/base-images/current/SHA256SUMS
sha256sum -c SHA256SUMS --ignore-missing
```

### 2.2 Installation sur portable dédié ou USB live persistant

#### Option A - Installation complète sur portable

Procédure standard d'installation Linux. Choisir :
- Partitionnement guidé chiffré LVM
- Bureau XFCE (léger) ou GNOME
- Installer outils par défaut

#### Option B - USB live persistant (économique)

```bash
# Créer USB persistant 64 Go
sudo dd if=kali-linux-2026.X-live-amd64.iso of=/dev/sdX bs=4M status=progress

# Ajouter partition persistance
sudo parted /dev/sdX mkpart primary ext4 4096MiB 100%
sudo mkfs.ext4 -L persistence /dev/sdX3
sudo mount /dev/sdX3 /mnt
echo "/ union" | sudo tee /mnt/persistence.conf
sudo umount /mnt
```

Au boot, choisir "Live USB Persistence".

## 3. Configuration post-installation

```bash
# Mise à jour
sudo apt update && sudo apt full-upgrade -y

# Outils complémentaires
sudo apt install -y \
    bettercap \
    seclists \
    rockyou \
    crackmapexec \
    impacket-scripts \
    responder \
    bloodhound

# Test wordlists
ls -la /usr/share/wordlists/
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

## 4. Outils essentiels par catégorie

### 4.1 Reconnaissance

| Outil | Usage |
|---|---|
| nmap | Scan réseau |
| masscan | Scan rapide gros réseaux |
| recon-ng | OSINT framework |
| theHarvester | Mails et noms |
| spiderfoot | OSINT massif |

### 4.2 Wi-Fi

| Outil | Usage |
|---|---|
| aircrack-ng | Suite Wi-Fi |
| wifite | Automation Wi-Fi |
| hashcat | Cassage WPA2 GPU |
| reaver | WPS exploit |
| kismet | Détection passive |

### 4.3 Web

| Outil | Usage |
|---|---|
| Burp Suite Community | Proxy web |
| OWASP ZAP | Scanner web |
| sqlmap | SQL injection auto |
| nikto | Scanner web vulns |
| wpscan | WordPress |

### 4.4 Réseau / pivoting

| Outil | Usage |
|---|---|
| Metasploit | Framework exploit |
| crackmapexec | Pentest AD |
| impacket | Scripts Python AD |
| responder | LLMNR/NBT-NS poisoning |
| bloodhound | Cartographie AD |

### 4.5 Mots de passe

| Outil | Usage |
|---|---|
| hashcat | GPU cracking |
| john | CPU cracking |
| hydra | Brute-force services |
| medusa | Alternative à hydra |

## 5. Configuration réseau

```bash
# Vérifier interfaces
ip a

# Connexion Wi-Fi en client (vers ARTECH-WIFI)
nmcli dev wifi connect ARTECH-WIFI password 'ArtechMedical2020!'

# Ou interface en mode monitor (pour capture/attaque)
sudo airmon-ng start wlan0
```

## 6. Méthodologie offensive éthique

### 6.1 Règle absolue

```text
KALI LINUX - RÈGLE NUMÉRO UN
==============================

JE N'UTILISE KALI QUE :
  - Sur mon propre laboratoire
  - Avec autorisation écrite explicite
  - Dans le cadre d'un mandat de pentest

TOUTE AUTRE UTILISATION = INFRACTION PÉNALE
  Articles 323-1 à 323-7 du Code pénal
  Jusqu'à 7 ans de prison et 300 000 € d'amende
```

### 6.2 Méthodologie OSSTMM/PTES

```mermaid
flowchart LR
    A[1 Engagement<br>Mandat] --> B[2 Reconnaissance]
    B --> C[3 Énumération]
    C --> D[4 Vulnerability<br>Analysis]
    D --> E[5 Exploitation]
    E --> F[6 Post-Exploitation]
    F --> G[7 Reporting]
```

### 6.3 Documentation rigoureuse

Toute opération sur Kali doit être tracée :

```bash
# Démarrer un script qui enregistre tout
script -t ~/labs/$(date +%Y%m%d_%H%M%S)_session.log

# ... vos commandes ...

exit
```

## 7. Outils additionnels OmnyAcademy

```bash
# Pour les exercices spécifiques OmnyAcademy
sudo apt install -y \
    macchanger \
    proxychains \
    tor \
    onionscan
    
# Outils spécifiques cycle 1 ARTECH
sudo apt install -y \
    aircrack-ng \
    hashcat \
    hashcat-utils
```

## 8. Préparation Wi-Fi attack

### 8.1 Vérifier carte Wi-Fi avec mode monitor

```bash
# Liste cartes
iwconfig

# Si carte interne ne supporte pas monitor → utiliser Alfa USB
# Branchement Alfa AWUS036ACS, vérifier
sudo airmon-ng

# Activer mode monitor sur Alfa
sudo airmon-ng start wlan1    # (ou wlanX selon nom)
```

### 8.2 Préparation des dictionnaires

```bash
# rockyou.txt déjà décompressé
ls -la /usr/share/wordlists/rockyou.txt

# Génération wordlist ciblée ARTECH
crunch 8 17 -t 'ArtechMedical@@@@!' >> artech_dict.txt
crunch 8 17 -t 'Artech@@@@@@@@@!'  >> artech_dict.txt
```

## 9. Sauvegarde de l'environnement

```bash
# Sauvegarde config /etc
sudo tar czf ~/kali-config-$(date +%Y%m%d).tar.gz /etc/

# Sauvegarde tools custom
tar czf ~/kali-tools-$(date +%Y%m%d).tar.gz ~/tools/

# Documentation labs
mkdir -p ~/labs
echo "Kali config OmnyAcademy" > ~/labs/README.md
```

---

**Chapitre suivant** : [3.12 CAINE 13 portable analyste](03-12-caine-analyste.md)
