---
title: 3.4 Configuration OpenWrt sur TP-Link Archer C7
description: Installation et configuration complète d'OpenWrt sur le routeur Archer C7. Flashage du firmware, configuration de base, réseau LAN/WAN, Wi-Fi, accès SSH. Étape par étape pour débutant.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - OpenWrt
  - Archer C7
  - Routeur
  - Configuration
data-level: 🔴
---

# 3.4 Configuration OpenWrt sur TP-Link Archer C7

!!! quote "L'analogie du chef qui change ses couteaux"

    Un chef cuisinier garde toujours ses couteaux, mais il les affûte selon ses besoins. Le routeur livré par le fabricant est correct pour un usage standard. Mais pour un laboratoire forensic, il faut l'affûter : OpenWrt remplace le firmware d'origine et donne accès à toutes les fonctions avancées. Wi-Fi configurable finement, journalisation complète, contrôle réseau total. C'est l'outil affûté du forensicien.

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 4 heures |
| Niveau | Pratique avancée |
| Prérequis | Notions réseau, accès Web admin |

## 1. Pourquoi OpenWrt

| Avantage | Précision |
|---|---|
| Open source | Audit possible, transparent |
| Personnalisation | Configuration fine du Wi-Fi |
| Logs détaillés | Forensic complet |
| Communauté active | Support, packages |
| Sécurité maintenue | Mises à jour régulières |
| Forensic-friendly | tcpdump natif, journalisation kernel |

## 2. Vérification compatibilité

### 2.1 Identifier la version exacte

L'Archer C7 a plusieurs versions matérielles. La V5 est la plus courante en 2026.

```text
Vérification :
  Sous le routeur, étiquette : Ver: 5.0
  Site OpenWrt : https://openwrt.org/toh/tp-link/archer_c7
  Vérifier ligne Archer C7 v5
```

### 2.2 Téléchargement firmware

```bash
# Version stable 23.05 ou plus récente en 2026
# Site officiel uniquement
wget https://downloads.openwrt.org/releases/23.05.X/targets/ath79/generic/openwrt-23.05.X-ath79-generic-tplink_archer-c7-v5-squashfs-factory.bin

# Vérifier signature
wget https://downloads.openwrt.org/releases/23.05.X/targets/ath79/generic/sha256sums
sha256sum -c sha256sums --ignore-missing
```

## 3. Procédure de flashage

### 3.1 Préparation

```text
ATTENTION
=========
Le flashage peut "briquer" le routeur si interrompu.
Faire une sauvegarde de la config d'origine si besoin.
Brancher sur onduleur ou sur prise stable.
NE PAS débrancher pendant le flashage.
```

### 3.2 Étapes via interface Web TP-Link

| Étape | Action |
|---|---|
| 1 | Brancher le routeur, attendre démarrage complet |
| 2 | Se connecter par câble (pas Wi-Fi) |
| 3 | Aller sur http://192.168.0.1 |
| 4 | Login admin/admin (par défaut) |
| 5 | System Tools → Firmware Upgrade |
| 6 | Choisir le fichier `.bin` OpenWrt factory |
| 7 | Confirmer, attendre 5-10 minutes |
| 8 | Le routeur redémarre |

### 3.3 Premier accès OpenWrt

Après reboot :

```bash
# OpenWrt par défaut
IP : 192.168.1.1
Login : root
Pas de mot de passe au premier accès

# Connexion
ssh root@192.168.1.1
```

**Première action** : définir un mot de passe.

```bash
# Sur le routeur
passwd
# Entrer mot de passe robuste
```

## 4. Configuration de base

### 4.1 Accès LuCI (interface Web)

http://192.168.1.1 - login root + mot de passe défini.

### 4.2 Configuration réseau

```bash
# Édition fichier réseau
vi /etc/config/network
```

Configuration finale :

```text
# /etc/config/network

config interface 'loopback'
    option device 'lo'
    option proto 'static'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'

config globals 'globals'
    option ula_prefix 'fdXX:XXXX:XXXX::/48'

# LAN - Réseau labo
config interface 'lan'
    option device 'br-lan'
    option proto 'static'
    option ipaddr '192.168.50.1'
    option netmask '255.255.255.0'
    option ip6assign '60'

# WAN - Vers box internet
config interface 'wan'
    option device 'eth0.2'
    option proto 'dhcp'

config interface 'wan6'
    option device 'eth0.2'
    option proto 'dhcpv6'

config device
    option name 'br-lan'
    option type 'bridge'
    list ports 'eth0.1'

config switch
    option name 'switch0'
    option reset '1'
    option enable_vlan '1'

config switch_vlan
    option device 'switch0'
    option vlan '1'
    option ports '0t 1 2 3 4'

config switch_vlan
    option device 'switch0'
    option vlan '2'
    option ports '0t 5'
```

### 4.3 Configuration DHCP

```bash
vi /etc/config/dhcp
```

```text
# /etc/config/dhcp

config dnsmasq
    option domainneeded '1'
    option boguspriv '1'
    option filterwin2k '0'
    option localise_queries '1'
    option rebind_protection '1'
    option rebind_localhost '1'
    option local '/lab/'
    option domain 'lab'
    option expandhosts '1'
    option authoritative '1'
    option readethers '1'
    option leasefile '/tmp/dhcp.leases'
    option resolvfile '/tmp/resolv.conf.d/resolv.conf.auto'
    option nonwildcard '1'
    option localservice '1'

config dhcp 'lan'
    option interface 'lan'
    option start '200'
    option limit '50'
    option leasetime '12h'
    option dhcpv4 'server'

# Réservations DHCP
config host
    option name 'server-debian'
    option mac 'XX:XX:XX:XX:XX:XX'
    option ip '192.168.50.10'

config host
    option name 'win-compta'
    option mac 'XX:XX:XX:XX:XX:XX'
    option ip '192.168.50.150'

config host
    option name 'win-stage'
    option mac 'XX:XX:XX:XX:XX:XX'
    option ip '192.168.50.151'

config host
    option name 'mac-m1'
    option mac 'XX:XX:XX:XX:XX:XX'
    option ip '192.168.50.170'
```

### 4.4 Application et redémarrage

```bash
# Recharger configuration
/etc/init.d/network restart
/etc/init.d/dnsmasq restart

# Vérifier
ip addr
brctl show
```

### 4.5 Test connectivité depuis poste

Reconnexion à `192.168.50.1` (nouvelle IP), authentification.

## 5. Configuration Wi-Fi (chapitre 3.5 détaillé)

Aperçu rapide :

```bash
vi /etc/config/wireless
```

Désactivation Wi-Fi 5 GHz, activation 2.4 GHz uniquement avec WPA2.

## 6. Logs et journalisation forensic

### 6.1 Activer logs persistants

```bash
# Logs dans fichier au lieu de seulement memoire
uci set system.@system[0].log_file='/etc/log/messages'
uci set system.@system[0].log_size='1024'
uci commit system

# Activer logs DNS
uci set dhcp.@dnsmasq[0].logqueries='1'
uci commit dhcp
/etc/init.d/dnsmasq restart
```

### 6.2 Capture de trafic

```bash
# Installer tcpdump
opkg update
opkg install tcpdump

# Capture sur LAN
tcpdump -i br-lan -w /tmp/capture.pcap

# Plus tard, télécharger sur poste analyste pour Wireshark
scp root@192.168.50.1:/tmp/capture.pcap ./
```

## 7. Durcissement de base

| Mesure | Commande |
|---|---|
| Désactiver SSH WAN | `uci set dropbear.@dropbear[0].Interface='lan'` |
| Désactiver pings WAN | iptables ou firewall LuCI |
| Mot de passe robuste | passwd |
| Mises à jour | sysupgrade |

## 8. Sauvegarde configuration

```bash
# Sur le routeur
sysupgrade -b /tmp/backup.tar.gz

# Récupérer
scp root@192.168.50.1:/tmp/backup.tar.gz ./openwrt-backup-$(date +%Y%m%d).tar.gz

# Vérifier
sha256sum openwrt-backup-*.tar.gz > backups.sha256
```

## 9. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Vérifier version Archer C7 ? | Étiquette sous routeur (V5 typique) |
| 2 | IP par défaut OpenWrt ? | 192.168.1.1 |
| 3 | Login par défaut ? | root sans mdp |
| 4 | Fichier config réseau ? | `/etc/config/network` |
| 5 | Application config ? | `/etc/init.d/network restart` |
| 6 | Backup config ? | `sysupgrade -b /tmp/backup.tar.gz` |

---

**Chapitre suivant** : [3.5 Wi-Fi WPA2-PSK volontairement faible](03-5-wifi-wpa2-faible.md)
