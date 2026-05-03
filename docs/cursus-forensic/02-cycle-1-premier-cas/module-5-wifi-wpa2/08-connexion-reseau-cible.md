---
title: 5.8 Connexion au réseau cible et reconnaissance interne
description: Connexion au réseau ARTECH avec PSK cracké, configuration discrète, reconnaissance ARP, DHCP, mDNS, identification des cibles internes. Première phase de pivoting depuis le LAN.
authors:
  - Zyrass
date:
  created: 2026-04-30
tags:
  - Connexion
  - Reconnaissance
  - LAN
  - ARP
  - mDNS
data-level: 🔴
---

# 5.8 Connexion au réseau cible et reconnaissance interne

!!! quote "L'analogie du visiteur qui entre dans le hall d'accueil"

    Vous venez de pénétrer dans un bâtiment d'entreprise dont vous aviez la clé. Le hall d'accueil est désert. Avant d'aller plus loin, vous prenez le temps d'observer : le plan affiché au mur, les flèches indicatrices, les conversations qui filtrent depuis les bureaux, les noms sur les portes, l'horloge centrale, les patterns du trafic des employés. Cette observation patiente, sans bouger, est la phase de reconnaissance interne. Elle conditionne tout ce qui suit. Si vous foncez tête baissée vers le serveur, vous déclenchez les alertes. Si vous écoutez d'abord, vous comprenez l'organisation et choisissez le bon chemin. Pour ARTECH, vous venez de cracker le PSK Wi-Fi. Vous êtes maintenant dans le hall. Ce chapitre vous apprend à observer avant d'agir.

## Métadonnées du chapitre

Ce chapitre marque le passage de l'attaque externe à l'attaque interne. Voici ses caractéristiques.

| Champ | Valeur |
|---|---|
| Durée estimée | 3 heures |
| Niveau | Pratique |
| Prérequis | 5.6 ou 5.7 (PSK obtenu) |
| Livrables | Cartographie LAN ARTECH avec hôtes identifiés |
| Auto-explication | 12 minutes |

## Objectifs pédagogiques

À l'issue de ce chapitre, vous serez capable de :

- Vous connecter au réseau cible discrètement
- Faire de la reconnaissance ARP passive
- Capturer DHCP et mDNS pour identification
- Distinguer trafic broadcast vs unicast
- Identifier les cibles internes prioritaires
- Préparer le scan nmap (chapitre 5.9)

---

## 1. Préparation à la connexion

### 1.1 Considérations préalables

Avant de vous connecter, il faut anticiper plusieurs éléments. Voici les considérations critiques.

| Considération | Impact |
|---|---|
| Profil discret | Pas de hostname évident |
| MAC randomisée | Évite traçabilité |
| Pas de DHCP automatique | Choix d'IP statique précis |
| Pas de services autodiscovery | Évite émissions involontaires |
| Routing isolé | Pas de fuite vers Internet |

### 1.2 Configuration de la carte

Voici la séquence pour préparer votre carte avant connexion.

```bash
# Ramener la carte en mode managed après le mode monitor
sudo airmon-ng stop wlan1mon

# Sortie typique
# PHY    Interface       Driver          Chipset
# phy1   wlan1mon        rtl88xxau       Realtek RTL8812AU
#                (mac80211 station mode vif enabled on [phy1]wlan1)

# Vérification mode managed
iwconfig wlan1
# Mode:Managed  ESSID:off/any

# MAC randomisation
sudo ip link set wlan1 down
sudo macchanger -A wlan1
sudo ip link set wlan1 up

# Note : MAC random n'est pas obligatoire mais recommandée
```

### 1.3 Désactivation services autodiscovery

Pour rester discret, désactivez les services qui annoncent votre présence.

```bash
# Désactiver mDNS (Avahi sur Linux)
sudo systemctl stop avahi-daemon
sudo systemctl disable avahi-daemon

# Désactiver SSDP (UPnP)
# Pas de service UPnP par défaut sur Kali, vérifier
ss -uln | grep 1900

# Désactiver auto-update et beacons
# Utile en pentest sérieux pour éviter call-home
```

## 2. Configuration WPA supplicant

### 2.1 Création du fichier de config

Voici comment créer un fichier WPA supplicant pour ARTECH.

```bash
# Génération avec wpa_passphrase
sudo wpa_passphrase ARTECH-WIFI ArtechMedical2020! \
    | sudo tee /tmp/wpa-artech.conf

# Sortie typique
# network={
#     ssid="ARTECH-WIFI"
#     #psk="ArtechMedical2020!"
#     psk=8e2a4f3b...  (hash PMK)
# }
```

### 2.2 Configuration enrichie

Pour plus de contrôle, créez manuellement avec options avancées.

```bash
# Configuration complète
sudo tee /tmp/wpa-artech.conf << EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="ARTECH-WIFI"
    psk="ArtechMedical2020!"
    key_mgmt=WPA-PSK
    proto=RSN
    pairwise=CCMP
    group=CCMP
    priority=1
    scan_ssid=0
}
EOF
```

### 2.3 Connexion

Voici la commande pour activer la connexion.

```bash
# Tuer NetworkManager si actif (peut interférer)
sudo systemctl stop NetworkManager

# Lancement wpa_supplicant
sudo wpa_supplicant \
    -B \
    -i wlan1 \
    -c /tmp/wpa-artech.conf \
    -D nl80211

# Vérification connexion
iwconfig wlan1
# Doit afficher ESSID:"ARTECH-WIFI" et un débit (Bit Rate)

# Vérification association
sudo wpa_cli -i wlan1 status
# Doit afficher wpa_state=COMPLETED
```

### 2.4 Configuration IP

Une fois connecté en couche 2, il faut une IP en couche 3.

```bash
# Option A - DHCP (visible)
sudo dhclient wlan1

# Option B - IP statique (plus discret)
sudo ip addr add 192.168.50.99/24 dev wlan1
sudo ip route add default via 192.168.50.1

# Choix de l'IP : éviter conflits
# Plage usuelle ARTECH : 192.168.50.0/24
# IPs déjà occupées (lab) : .1 (router), .10 (serveur),
#   .150-151 (Win), .170 (Mac)
# Choisir IP haute peu utilisée : .99 ou .220
```

### 2.5 Validation connexion

Voici les commandes de validation.

```bash
# Test ping vers gateway
ping -c 4 192.168.50.1

# Si DHCP utilisé, voir l'IP attribuée
ip addr show wlan1

# Vérification table de routage
ip route

# Test résolution DNS (peut révéler que vous êtes connecté)
# À éviter dans un premier temps
```

## 3. Reconnaissance ARP passive

L'**ARP** (Address Resolution Protocol) traduit les IPs en MACs au sein du LAN. C'est un protocole bavard.

### 3.1 Principe ARP

Voici comment fonctionne ARP.

```text
ARP - PROTOCOLE BAVARD
========================

ARP REQUEST (broadcast)
  "Qui a 192.168.50.10 ?"
  Source : MAC client + IP client
  Destination : ff:ff:ff:ff:ff:ff (broadcast)

ARP REPLY (unicast)
  "192.168.50.10 est à 02:42:ac:11:00:0a"
  Source : MAC serveur + IP serveur
  Destination : MAC client

CONSÉQUENCE
  Tout le trafic ARP est en CLAIR.
  Tout le monde sur le LAN peut le voir
  (avec la GTK Wi-Fi qui couvre les broadcasts).
```

### 3.2 Capture ARP avec tcpdump

Voici la commande pour capturer le trafic ARP.

```bash
# Capture ARP en temps réel
sudo tcpdump -i wlan1 -n arp

# Sortie typique
# 15:32:14.123 ARP, Request who-has 192.168.50.10 tell 192.168.50.150
# 15:32:14.124 ARP, Reply 192.168.50.10 is-at 64:70:02:aa:bb:cc
# 15:32:15.456 ARP, Request who-has 192.168.50.1 tell 192.168.50.151
```

Chaque ligne révèle qui parle à qui. Sans même envoyer un paquet, vous cartographiez le LAN.

### 3.3 ARP scan actif

Pour accélérer, vous pouvez faire un **ARP scan actif** qui envoie une requête ARP à toutes les IPs.

```bash
# Avec arp-scan
sudo apt install arp-scan -y

sudo arp-scan -I wlan1 192.168.50.0/24

# Sortie typique
# Interface: wlan1, type: EN10MB, MAC: <votre MAC>, IPv4: 192.168.50.99
# Starting arp-scan...
# 192.168.50.1    64:70:02:XX:XX:XX     TP-LINK TECHNOLOGIES CO.,LTD.
# 192.168.50.10   08:00:27:11:22:33     PCS Systemtechnik GmbH (VirtualBox)
# 192.168.50.150  bc:6e:e2:44:55:66     Microsoft Corporation
# 192.168.50.151  d8:bb:c1:77:88:99     Microsoft Corporation
# 192.168.50.170  1c:1b:0d:aa:bb:cc     Apple, Inc.
# 192.168.50.250  aa:11:22:33:44:55     Realtek (votre Kali)
# 
# 6 packets received by filter, 0 packets dropped
# Ending arp-scan: 256 hosts scanned in 12.345 seconds
```

### 3.4 Identification par OUI

Le préfixe MAC (OUI) révèle le constructeur. Voici la lecture pour ARTECH.

| MAC OUI | Constructeur | Probable rôle |
|---|---|---|
| 64:70:02 | TP-Link | Routeur OpenWrt |
| 08:00:27 | VirtualBox | Serveur Debian VM |
| BC:6E:E2 | Microsoft | PC Windows (compta) |
| D8:BB:C1 | Microsoft | PC Windows (stagiaire) |
| 1C:1B:0D | Apple | MacBook M1 |
| 00:0C:29 | VMware | autre VM |

### 3.5 Discrétion ARP

ARP scan est **détectable**. Voici les considérations.

```text
DISCRÉTION ARP
================

ARP scan envoie des requêtes vers TOUTES les IPs.
Visible par :
  - IDS comme Suricata (rules ARP-anomaly)
  - Firewall avec logging
  - Monitoring switch (si SNMP/sFlow)

Mode plus discret :
  - Capture passive uniquement (tcpdump arp)
  - Lente car dépend du trafic spontané
  - 1-2 heures pour tout voir
```

## 4. DHCP traffic

Le **DHCP** est très bavard et révèle énormément.

### 4.1 Capture DHCP

Voici comment capturer le trafic DHCP.

```bash
# DHCP utilise UDP ports 67/68
sudo tcpdump -i wlan1 -n -v port 67 or port 68

# Sortie typique - DHCP Discover (client → broadcast)
# 15:35:12.789 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request
# Client-Ethernet-Address bc:6e:e2:44:55:66
# Vendor-rfc1048 Extensions
#   DHCP-Message Option: DISCOVER
#   Hostname Option "WIN-COMPTA-01"
#   Vendor-Class Option "MSFT 5.0"
```

### 4.2 Information révélée par DHCP

Le DHCP discover/request expose plusieurs informations.

| Champ | Information |
|---|---|
| Hostname | Nom de la machine ("WIN-COMPTA-01") |
| Vendor-Class | OS type ("MSFT 5.0", "android-dhcp-12") |
| Class-Identifier | Spécifique constructeur |
| Parameter-Request | Ce que le client veut savoir |

### 4.3 Identification des hôtes ARTECH

Voici ce que vous pouvez espérer apprendre via DHCP.

```text
HÔTES ARTECH IDENTIFIÉS PAR DHCP
==================================

WIN-COMPTA-01  : PC comptable Sophie Dupont
WIN-STAGE-01   : PC stagiaire Paul Dubois  
DEBIAN-SRV     : Serveur principal
MACBOOK-PRO    : MacBook PDG Hélène Lefebvre
ARTECH-PRINT   : Imprimante réseau (potentiel pivot)

Information cruciale pour le ciblage :
  - Sophie = comptable = cible CEO fraud
  - Paul = stagiaire = cible naive
  - Hélène = PDG = cible whaling
```

## 5. mDNS et Bonjour

Le **mDNS** (Multicast DNS) sert à la découverte de services. Très bavard sur les réseaux d'entreprise.

### 5.1 Capture mDNS

```bash
# mDNS utilise port 5353 (multicast 224.0.0.251)
sudo tcpdump -i wlan1 -n port 5353

# Sortie typique
# 15:38:01.234 IP 192.168.50.170.5353 > 224.0.0.251.5353: 0 Printer-AirPrint._ipp._tcp.local
# 15:38:01.456 IP 192.168.50.10.5353 > 224.0.0.251.5353: 0 ARTECH-PRINT._ipp._tcp.local
```

### 5.2 Outil avahi-browse

Pour explorer les services mDNS :

```bash
# Installation
sudo apt install avahi-utils -y

# Listage des services
avahi-browse -a -t -r

# Sortie typique
# +  wlan1 IPv4 ARTECH-PRINT                          IPP Printer    local
# = wlan1 IPv4 ARTECH-PRINT                          IPP Printer    local
#    hostname = [ARTECH-PRINT.local]
#    address = [192.168.50.180]
#    port = [631]
#    txt = ["product=HP LaserJet" "make=HP" ...]
```

### 5.3 NBNS (NetBIOS Name Service)

Sur Windows, **NBNS** complète mDNS. Port 137 UDP.

```bash
# Capture NBNS
sudo tcpdump -i wlan1 -n port 137

# Outil dédié
sudo nbtscan -r 192.168.50.0/24

# Sortie typique
# 192.168.50.150  ARTECH\WIN-COMPTA-01    SERVICES
# 192.168.50.151  ARTECH\WIN-STAGE-01     SERVICES
```

## 6. LLMNR et autres protocoles bavards

### 6.1 LLMNR (Link-Local Multicast Name Resolution)

```bash
# LLMNR port 5355 UDP
sudo tcpdump -i wlan1 -n port 5355

# Capture utile pour identifier les requêtes hostname
```

### 6.2 SSDP (Simple Service Discovery)

```bash
# SSDP port 1900 UDP
sudo tcpdump -i wlan1 -n port 1900
```

### 6.3 IGMP (multicast group)

```bash
# IGMP révèle les inscriptions multicast
sudo tcpdump -i wlan1 -n igmp
```

## 7. Capture exhaustive avec Wireshark

Pour une analyse approfondie, Wireshark est le mieux.

### 7.1 Capture targeted

```bash
# Capture 30 minutes de tout trafic broadcast/multicast
sudo tcpdump -i wlan1 -w artech-recon.pcap \
    "broadcast or multicast or arp" -G 1800 -W 1

# Le fichier artech-recon.pcap contient toute la
# reconnaissance passive de 30 minutes
```

### 7.2 Analyse offline

```bash
# Ouverture Wireshark
wireshark artech-recon.pcap

# Filtres utiles
# arp                              -> Trafic ARP
# bootp                            -> DHCP
# mdns                             -> mDNS
# nbns                             -> NetBIOS
# llmnr                            -> LLMNR
# tcp.flags.syn == 1               -> Tentatives connexion
# wlan.fc.type_subtype == 0x0008   -> Beacons
```

### 7.3 Statistiques Wireshark

Wireshark fournit des statistiques utiles.

```text
STATISTIQUES UTILES (menu Statistics)
========================================

Endpoints
  Liste tous les hôtes avec leurs MAC/IP/ports
  
Conversations
  Liste les flux entre paires d'hôtes
  
Protocol Hierarchy
  Volumes par protocole

Resolved Addresses
  Mapping IP ↔ hostname collecté
```

## 8. Cartographie LAN ARTECH

À l'issue de la reconnaissance, vous avez une carte du LAN.

### 8.1 Schéma type

Voici le schéma typique attendu pour ARTECH.

```mermaid
flowchart LR
    subgraph LAN_ARTECH["LAN ARTECH 192.168.50.0/24"]
        ROUTER[".1 Router OpenWrt<br>TP-Link Archer C7<br>64:70:02:XX:XX:XX"]
        SERVER[".10 Serveur Debian<br>VirtualBox<br>08:00:27:11:22:33"]
        COMPTA[".150 WIN-COMPTA-01<br>Microsoft<br>BC:6E:E2:44:55:66"]
        STAGE[".151 WIN-STAGE-01<br>Microsoft<br>D8:BB:C1:77:88:99"]
        MAC[".170 MACBOOK-PRO<br>Apple<br>1C:1B:0D:AA:BB:CC"]
        PRINT[".180 ARTECH-PRINT<br>HP LaserJet<br>imprimante"]
    end
    KALI[".99 Kali Attaquant<br>aa:11:22:33:44:55]
    KALI -.->|connecté Wi-Fi| ROUTER
```

### 8.2 Tableau de synthèse

Voici la synthèse à compléter.

| IP | Hostname | MAC | OUI | Rôle probable |
|---|---|---|---|---|
| .1 | OpenWrt | 64:70:02... | TP-Link | Routeur Wi-Fi |
| .10 | DEBIAN-SRV | 08:00:27... | VirtualBox | Serveur principal |
| .150 | WIN-COMPTA-01 | BC:6E:E2... | Microsoft | PC compta Sophie |
| .151 | WIN-STAGE-01 | D8:BB:C1... | Microsoft | PC stagiaire Paul |
| .170 | MACBOOK-PRO | 1C:1B:0D... | Apple | Mac PDG Hélène |
| .180 | ARTECH-PRINT | XX:XX:XX... | HP | Imprimante |

### 8.3 Cibles prioritaires

En croisant avec l'OSINT du module 4, vous priorisez les cibles.

| Cible | Score | Justification |
|---|---|---|
| Serveur Debian (.10) | Critique | Données clients, AD/Samba |
| WIN-COMPTA-01 (.150) | Élevé | CEO fraud, factures |
| WIN-STAGE-01 (.151) | Modéré | Pivot facile, non sensibilisé |
| MACBOOK-PRO (.170) | Élevé | Données stratégiques PDG |
| Imprimante (.180) | Modéré | Pivot SNMP, jobs print sensibles |

## 9. Considérations de discrétion

### 9.1 Trafic généré par votre Kali

Sans précaution, votre Kali émet du trafic révélateur.

```text
TRAFIC PAR DÉFAUT À CONTRÔLER
================================

DHCP discover (si DHCP)
  Hostname "kali"
  → IP statique recommandée

mDNS announces (avahi)
  Hostname.local
  → systemctl stop avahi

NTP sync
  Vers pool.ntp.org
  → désactiver chronyd/timesyncd

Auto-update
  apt-daily.timer
  → systemctl disable

VPN/proxy fuite
  Vers serveur externe
  → désactiver VPN
```

### 9.2 Hostname et persona

Voici les bonnes pratiques pour adopter un profil discret.

```bash
# Changer le hostname pour quelque chose de banal
sudo hostnamectl set-hostname laptop-007

# Désactiver les services bavards
sudo systemctl stop avahi-daemon
sudo systemctl stop cups
sudo systemctl stop samba
```

### 9.3 Que faire si détecté

Si un IDS lève une alerte, vous êtes peut-être détecté.

```text
SCENARIOS DE DÉTECTION
========================

Indicateurs côté défense :
  - Nouvelle MAC association Wi-Fi
  - Nouveau DHCP request avec hostname inhabituel
  - ARP scan (volume anormal)
  - Tentatives de connexion sur services inhabituels

Si suspicion détection :
  - Stopper toute activité
  - Déconnecter de l'AP
  - Documenter ce qui a déclenché
  - Reprendre avec MAC différente, plus discret
```

## 10. Cas pratique - Connexion ARTECH

### 10.1 Scénario

Vous avez le PSK ArtechMedical2020!. Vous vous connectez au lab et cartographiez le LAN.

### 10.2 Workflow

Voici la séquence complète.

```bash
# Préparation
mkdir -p ~/pentest/artech-2026/recon-interne
cd ~/pentest/artech-2026/recon-interne/

# 1. Sortir du mode monitor
sudo airmon-ng stop wlan1mon

# 2. Configuration carte
sudo ip link set wlan1 down
sudo macchanger -A wlan1
sudo ip link set wlan1 up

# 3. Désactiver services bavards
sudo systemctl stop avahi-daemon

# 4. Création config WPA
sudo wpa_passphrase ARTECH-WIFI ArtechMedical2020! \
    | sudo tee /tmp/wpa-artech.conf

# 5. Connexion
sudo wpa_supplicant -B -i wlan1 -c /tmp/wpa-artech.conf

# 6. IP statique (plus discret)
sudo ip addr add 192.168.50.99/24 dev wlan1
sudo ip route add default via 192.168.50.1

# 7. Validation
ping -c 2 192.168.50.1

# 8. Capture passive 5 minutes
sudo tcpdump -i wlan1 -w passive-recon.pcap \
    "broadcast or multicast or arp" \
    -G 300 -W 1

# 9. ARP scan actif
sudo arp-scan -I wlan1 192.168.50.0/24 \
    > arp-scan.txt

# 10. Capture DHCP/mDNS si pas dans passive
sudo tcpdump -i wlan1 -w dhcp-mdns.pcap \
    "port 67 or port 68 or port 5353" \
    -G 600 -W 1 &

# 11. NetBIOS scan
sudo nbtscan -r 192.168.50.0/24 > nbns.txt

# 12. Analyse Wireshark
wireshark passive-recon.pcap

# 13. Synthèse
cat > cartographie-lan.md << 'EOF'
# Cartographie LAN ARTECH

| IP | Hostname | MAC | Constructeur | Rôle |
|---|---|---|---|---|
| .1 | OpenWrt | 64:70:02... | TP-Link | Routeur |
| .10 | DEBIAN-SRV | 08:00:27... | VBox | Serveur |
| .150 | WIN-COMPTA-01 | BC:6E:E2... | Microsoft | PC Sophie |
| .151 | WIN-STAGE-01 | D8:BB:C1... | Microsoft | PC Paul |
| .170 | MACBOOK-PRO | 1C:1B:0D... | Apple | MacBook Hélène |
| .180 | ARTECH-PRINT | XX:XX... | HP | Imprimante |
EOF

# 14. Hash forensic
sha256sum *.pcap *.txt > MANIFEST.sha256

# 15. Documentation
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - Connexion ARTECH et reconnaissance LAN" \
    >> ~/pentest/artech-2026/journal.md
```

## 11. Auto-évaluation

Vérifiez votre maîtrise par les questions suivantes.

| # | Question | Réponse |
|---|---|---|
| 1 | Comment générer config WPA ? | wpa_passphrase |
| 2 | Daemon de connexion ? | wpa_supplicant |
| 3 | Outil ARP scan ? | arp-scan |
| 4 | Port DHCP ? | 67/68 UDP |
| 5 | Port mDNS ? | 5353 UDP |
| 6 | Port NBNS ? | 137 UDP |
| 7 | Information révélée par DHCP ? | Hostname, OS |
| 8 | Service mDNS Linux à arrêter ? | avahi-daemon |

## 12. Synthèse

Voici les points clés à retenir.

```text
CONNEXION ET RECONNAISSANCE INTERNE

PRÉPARATION
  airmon-ng stop wlan1mon
  macchanger -A wlan1
  systemctl stop avahi
  
CONNEXION
  wpa_passphrase SSID PSK > config
  wpa_supplicant -B -i wlan1 -c config
  ip addr add IP/24 dev wlan1
  ip route add default via gateway

RECONNAISSANCE PASSIVE
  tcpdump arp        : ARP requests/replies
  tcpdump port 67-68 : DHCP
  tcpdump port 5353  : mDNS
  tcpdump port 137   : NBNS

OUTILS ACTIFS
  arp-scan : scan ARP rapide
  nbtscan  : NetBIOS hostnames
  avahi-browse : services mDNS

INFORMATION OBTENUE
  IPs actives
  MAC + constructeur (OUI)
  Hostnames
  OS approximatif
  Services exposés

CARTOGRAPHIE ARTECH
  .1   Router OpenWrt
  .10  Serveur Debian
  .150 WIN-COMPTA-01 (Sophie)
  .151 WIN-STAGE-01 (Paul)
  .170 MACBOOK-PRO (Hélène)

DISCRÉTION
  IP statique (pas DHCP)
  Hostname banal
  Services autodiscovery off
  MAC randomisée

NEXT : nmap (5.9)
```

---

**Chapitre précédent** : [5.7 aircrack-ng en mode CPU](5-7-aircrack-ng-cpu.md)

**Chapitre suivant** : [5.9 nmap silencieux et énumération](5-9-nmap-silencieux.md)
