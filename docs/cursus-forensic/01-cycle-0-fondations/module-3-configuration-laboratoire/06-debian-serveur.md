---
title: 3.6 Installation Debian 12 serveur
description: Installation de Debian 12 stable sur le serveur du laboratoire. Préparation USB bootable, partitionnement avec LUKS chiffré, installation minimale, premier boot, sécurisation.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Debian
  - Linux
  - LUKS
  - Installation
data-level: 🟡
---

# 3.6 Installation Debian 12 serveur

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 2 heures |
| Niveau | Pratique |

## 1. Pourquoi Debian 12

| Critère | Réponse |
|---|---|
| Stabilité | LTS, mises à jour sécurité 5 ans |
| Communauté | Documentation excellente |
| Forensic-friendly | Outils nombreux disponibles |
| Sobriété | Système minimal possible |
| Reproductibilité | Configuration prévisible |

Version cible : **Debian 12 Bookworm** (sortie juin 2023, support jusqu'en 2028).

## 2. Préparation

### 2.1 Téléchargement ISO

```bash
# ISO officielle netinst (300 Mo)
wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.X.0-amd64-netinst.iso

# Vérification SHA-256
wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/SHA256SUMS
sha256sum -c SHA256SUMS --ignore-missing
```

### 2.2 Création USB bootable

```bash
# Linux/macOS
sudo dd if=debian-12.X.0-amd64-netinst.iso of=/dev/sdX bs=4M status=progress conv=fdatasync

# Windows : Rufus ou balenaEtcher
```

## 3. Procédure d'installation

| Étape | Choix |
|---|---|
| 1 | Booter sur USB, Graphical Install |
| 2 | Langue : Français |
| 3 | Pays : France |
| 4 | Clavier : Français AZERTY |
| 5 | Hostname : `server-lab` |
| 6 | Domaine : `lab.local` |
| 7 | Mot de passe root robuste |
| 8 | Utilisateur : `zyrass` |
| 9 | Mot de passe utilisateur robuste |
| 10 | Partitionnement : Manuel |

### 3.1 Partitionnement avec LUKS

Schéma recommandé :

```text
PARTITIONNEMENT - DISQUE 256 GO
=================================

/dev/sda1   1 GB    /boot           ext4
/dev/sda2   240 GB  LUKS chiffré
  /dev/mapper/sda2_crypt
    LVM
      vg-system
        lv-root    50 GB  /         ext4
        lv-home    20 GB  /home     ext4
        lv-var     30 GB  /var      ext4
        lv-tmp     10 GB  /tmp      ext4
        lv-swap    8 GB   swap
        lv-data    100 GB /data     ext4
        (libre)    22 GB
```

### 3.2 Pourquoi LUKS

| Bénéfice | Précision |
|---|---|
| Réaliste | Reproduit ce qu'on trouve en entreprise |
| Pédagogique | Exercice forensic chiffrement |
| Pratique | Volume chiffré en cas de vol matériel |

### 3.3 Sélection des paquets

```text
TÂCHES À INSTALLER
==================

[X] Serveur SSH
[X] Utilitaires standard du système
[ ] Environnement de bureau (NON, serveur headless)
[ ] Serveur web
[ ] Serveur d'impression
[ ] Serveur de fichiers SSH (déjà couvert)
```

### 3.4 GRUB et finalisation

| Étape | Choix |
|---|---|
| GRUB | Installer dans le MBR du disque principal |
| Disque GRUB | /dev/sda |

## 4. Premier boot

### 4.1 Démarrage

Mot de passe LUKS demandé en premier au boot, puis login standard.

### 4.2 Vérifications

```bash
# Versions
uname -a
cat /etc/debian_version

# Mises à jour
sudo apt update
sudo apt upgrade -y

# Statut services essentiels
systemctl status ssh
systemctl status networking
```

## 5. Configuration réseau statique

```bash
sudo vi /etc/network/interfaces
```

```text
# /etc/network/interfaces

source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

# Interface principale
auto eth0
iface eth0 inet static
    address 192.168.50.10/24
    gateway 192.168.50.1
    dns-nameservers 192.168.50.1 1.1.1.1
```

```bash
# Application
sudo systemctl restart networking
ip addr show eth0
```

## 6. Configuration hostname et /etc/hosts

```bash
sudo hostnamectl set-hostname server-lab.lab.local

# /etc/hosts
sudo vi /etc/hosts
```

```text
127.0.0.1       localhost
127.0.1.1       server-lab.lab.local server-lab
192.168.50.1    router-lab.lab.local router-lab
192.168.50.10   server-lab.lab.local server-lab
192.168.50.150  win-compta.lab.local win-compta
192.168.50.151  win-stage.lab.local win-stage
192.168.50.170  mac-m1.lab.local mac-m1
```

## 7. Durcissement de base

### 7.1 SSH

```bash
sudo vi /etc/ssh/sshd_config
```

```text
# Configuration SSH durcie
Port 22
Protocol 2
PermitRootLogin no
PasswordAuthentication yes    # Provisoire, sera no après ajout clés
PubkeyAuthentication yes
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
AllowUsers zyrass
LoginGraceTime 30
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
```

```bash
sudo systemctl restart ssh
```

### 7.2 Pare-feu UFW

```bash
sudo apt install ufw -y

# Configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow from 192.168.50.0/24

# Activation
sudo ufw enable
sudo ufw status verbose
```

### 7.3 Fail2ban

```bash
sudo apt install fail2ban -y

sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Vérification
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

## 8. Mise à jour automatique

```bash
sudo apt install unattended-upgrades -y

# Configuration
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 9. Sauvegarde post-installation

```bash
# Snapshot LVM
sudo lvcreate -L 5G -s -n root_snapshot /dev/vg-system/lv-root
sudo lvcreate -L 5G -s -n home_snapshot /dev/vg-system/lv-home

# Liste snapshots
sudo lvs
```

## 10. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Version Debian utilisée ? | 12 Bookworm |
| 2 | Pourquoi LUKS ? | Réaliste, pédagogique, sécurité |
| 3 | Paquets installés ? | SSH + utilitaires standard, pas DE |
| 4 | IP statique fichier ? | `/etc/network/interfaces` |
| 5 | Pare-feu ? | UFW |
| 6 | Anti brute-force ? | fail2ban |

---

**Chapitre suivant** : [3.7 Configuration serveur (SSH, Samba, intranet)](03-7-config-serveur.md)
