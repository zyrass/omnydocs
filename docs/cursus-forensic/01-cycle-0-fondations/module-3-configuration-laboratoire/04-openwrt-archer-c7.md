---
description: "Installation et configuration complète d'OpenWrt sur le routeur Archer C7. Flashage du firmware, configuration de base, réseau LAN/WAN, Wi-Fi, accès SSH. Étape par étape pour débutant."
icon: lucide/router
tags: ["OPENWRT", "ARCHER C7", "ROUTEUR", "CONFIGURATION"]
---

# Configuration OpenWrt sur TP-Link Archer C7

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Modèle 2026"
  data-time="4 heures">
</div>

!!! note "**Livrables :** _Routeur OpenWrt flashé et configuré avec le subnet Labo_"
!!! note "**Prérequis :** _Notions réseau de base, accès Web Admin TP-Link_"

<br>

---

<br>

!!! quote "L'analogie du chef qui change ses couteaux"

    Un chef cuisinier garde toujours ses couteaux, mais il les affûte selon ses besoins. Le routeur livré par le fabricant est correct pour un usage standard, mais ses fonctionnalités sont bridées. Pour un laboratoire Forensic, il faut l'affûter : installer **OpenWrt** remplace le firmware "jouet" d'origine par un véritable Linux embarqué. Wi-Fi configurable finement (pour être piraté), journalisation système profonde, contrôle réseau total... C'est le couteau suisse du forensicien réseau.

## Objectifs pédagogiques

!!! tip "À la fin de ce chapitre, vous serez capable de :"

    - Flasher en toute sécurité un firmware tiers (OpenWrt) sur un équipement commercial.
    - Prendre la main sur un Linux embarqué via SSH.
    - Configurer des interfaces virtuelles LAN/WAN (Switching, VLAN) en ligne de commande.
    - Mettre en place la journalisation système avancée pour capturer le trafic d'attaque.

<br>

---

<br>

## Pourquoi OpenWrt ?

> Le tableau ci-dessous expose les atouts d'OpenWrt par rapport au firmware d'usine :

| Avantage | Précision technique |
|---|---|
| **Open Source** | Code auditable, pas de backdoor constructeur. |
| **Personnalisation** | Permet de forcer des configurations Wi-Fi "faibles" pour les exercices d'attaque. |
| **Logs détaillés** | Accès aux logs Kernel (`dmesg`) et système, indispensable pour le Forensic. |
| **Package Manager** | `opkg` permet d'installer des outils pro directement sur le routeur (ex: `tcpdump`). |
| **Sécurité** | Mises à jour maintenues bien plus longtemps que par TP-Link. |

<br>

---

<br>

## Vérification de la compatibilité

### Identifier la version matérielle exacte

L'Archer C7 possède de multiples révisions matérielles (V1, V2... V5). **La version 5 est notre cible de référence.**

```text title="Procédure de vérification matérielle"
1. Retournez physiquement le routeur.
2. Lisez l'étiquette : Cherchez la mention "Ver: 5.0" ou "V5".
3. Allez sur le site officiel OpenWrt : https://openwrt.org/toh/tp-link/archer_c7
4. Confirmez la prise en charge de la "v5".
```

### Téléchargement du Firmware

!!! danger "Ne téléchargez **jamais** un firmware depuis un autre site que le site officiel."

```bash title="Commandes Bash - Récupération (Téléchargement) et contrôle du Firmware"
# Télécharger la version stable (23.05.X) - Image Factory (Pour le premier flash)
wget https://downloads.openwrt.org/releases/23.05.X/targets/ath79/generic/openwrt-23.05.X-ath79-generic-tplink_archer-c7-v5-squashfs-factory.bin

# Télécharger le fichier de sommes de contrôle
wget https://downloads.openwrt.org/releases/23.05.X/targets/ath79/generic/sha256sums
    
# Vérifier l'intégrité cryptographique du fichier
sha256sum -c sha256sums --ignore-missing
```

<br>

---

<br>

## La procédure de Flashage

!!! danger "Attention - Risque de Brick"
    Flasher un firmware comporte toujours un risque de rendre le matériel inutilisable (Brick). 
    - Ne faites **JAMAIS** l'opération en Wi-Fi. Branchez un câble réseau.
    - Ne débranchez **JAMAIS** l'alimentation pendant le processus.
    - Si possible, branchez le routeur sur un onduleur.

### Étapes via l'interface Web TP-Link d'origine

> Le tableau ci-dessous détaille le processus de premier flashage :

| Étape | Action requise |
|---|---|
| **1** | Brancher le routeur et attendre son démarrage complet (Témoins allumés). |
| **2** | Connecter votre PC via un câble réseau sur un port LAN (Pas le port WAN bleu). |
| **3** | Naviguer vers `http://192.168.0.1` (IP par défaut TP-Link). |
| **4** | S'authentifier (Souvent `admin` / `admin`). |
| **5** | Menu : *System Tools* → *Firmware Upgrade*. |
| **6** | Parcourir et uploader le fichier `.bin` OpenWrt (`...factory.bin`). |
| **7** | Confirmer et **ne plus toucher à rien** pendant 5 à 10 minutes. |
| **8** | Le routeur va redémarrer automatiquement avec la nouvelle interface. |

<br>

### Premier contact avec OpenWrt

Après le redémarrage, la donne a changé. L'IP d'usine TP-Link n'existe plus.


```bash title="Commandes Bash - Connexion initiale (Première connexion SSH)"
# Nouvelles données par défaut OpenWrt :
# IP    : 192.168.1.1
# Login : root
# Mot de passe : (Vide au premier accès)

# Connexion SSH
ssh root@192.168.1.1

# DÉFINIR IMMÉDIATEMENT UN MOT DE PASSE (OBLIGATOIRE)
passwd
# > Entrer un mot de passe robuste (Il sera utilisé pour le SSH et l'interface Web LuCI)
```

<br>

---

<br>

## Configuration réseau en ligne de commande (CLI)

Vous pouvez utiliser l'interface Web (LuCI) via `http://192.168.1.1`, mais pour bien comprendre l'architecture interne, nous allons éditer directement les fichiers de configuration via `vi`.

### Paramétrage des interfaces (LAN / WAN)

Voici la configuration des interfaces système :

```bash title="Fichier /etc/config/network - Configuration LAN et VLAN"
# Ouvrir le fichier de configuration réseau
vi /etc/config/network
```

```text title="Contenu attendu pour /etc/config/network"
config interface 'loopback'
    option device 'lo'
    option proto 'static'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'

# --- RÉSEAU LABO (LAN) ---
config interface 'lan'
    option device 'br-lan'
    option proto 'static'
    option ipaddr '192.168.50.1'       # Nouvelle IP passerelle du laboratoire
    option netmask '255.255.255.0'     # Masque en /24
    option ip6assign '60'

# --- CONNEXION EXTÉRIEURE (WAN) ---
config interface 'wan'
    option device 'eth0.2'
    option proto 'dhcp'                # Récupère l'IP depuis votre Box Internet

config interface 'wan6'
    option device 'eth0.2'
    option proto 'dhcpv6'

# --- CONFIGURATION DU SWITCH MATÉRIEL ---
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
    option ports '0t 1 2 3 4'          # Ports LAN physiques attribués au VLAN 1

config switch_vlan
    option device 'switch0'
    option vlan '2'
    option ports '0t 5'                # Port WAN physique attribué au VLAN 2
```

### Paramétrage du DHCP et Réservations IP (Baux statiques)

Nous devons nous assurer que nos serveurs et machines d'analyse gardent toujours la même adresse IP, conformément à notre topologie.

```bash title="Fichier /etc/config/dhcp - Configuration DHCP (Dnsmasq)"
vi /etc/config/dhcp
```

```text title="Contenu attendu pour les baux DHCP"
# Configuration principale LAN
config dhcp 'lan'
    option interface 'lan'
    option start '200'                 # Début plage DHCP dynamique (192.168.50.200)
    option limit '50'                  # Nombre d'adresses (Jusqu'à .249)
    option leasetime '12h'
    option dhcpv4 'server'

# --- RÉSERVATIONS DHCP STATIQUES (Exemples) ---
config host
    option name 'server-debian'
    option mac 'XX:XX:XX:XX:XX:XX'     # À remplacer par l'adresse MAC réelle
    option ip '192.168.50.10'

config host
    option name 'win-compta'
    option mac 'YY:YY:YY:YY:YY:YY'
    option ip '192.168.50.150'
    
config host
    option name 'win-stage'
    option mac 'ZZ:ZZ:ZZ:ZZ:ZZ:ZZ'
    option ip '192.168.50.151'

config host
    option name 'mac-m1'
    option mac 'AA:AA:AA:AA:AA:AA'
    option ip '192.168.50.170'
```

### Application des modifications

!!! warning "Changement d'IP imminent"
    En appliquant cette configuration, l'adresse du routeur va passer de `192.168.1.1` à `192.168.50.1`. Votre session SSH sera coupée. Vous devrez renouveler le bail DHCP de votre PC (débrancher/rebrancher le câble) pour obtenir une adresse dans la nouvelle plage, puis vous reconnecter.

```bash title="Commandes Linux - Application de la configuration ( redémarrage des services )"
# Recharger la configuration réseau (Coupure de session attendue)
/etc/init.d/network restart

# Recharger le service DHCP/DNS
/etc/init.d/dnsmasq restart
```

<br>

---

<br>

## Outillage Forensic : Captures de paquets et Logs

Le gros avantage d'OpenWrt est de pouvoir sniffer le trafic directement depuis le routeur central.

### Rendre les journaux système persistants

Par défaut, OpenWrt stocke ses logs en RAM pour économiser la mémoire flash. Au redémarrage, tout est perdu. Ce n'est pas acceptable pour une analyse Forensic post-incident.

```bash title="Commandes UCI - Persistance et logs DNS ( Configuration du démon syslog et dnsmasq )"
# Configurer le démon syslog pour écrire dans un fichier disque
uci set system.@system[0].log_file='/etc/log/messages'
uci set system.@system[0].log_size='1024'
uci commit system

# Forcer dnsmasq à journaliser toutes les requêtes DNS (Idéal pour traquer les malwares)
uci set dhcp.@dnsmasq[0].logqueries='1'
uci commit dhcp

# Redémarrer dnsmasq
/etc/init.d/dnsmasq restart
```

### Installer et utiliser tcpdump

```bash title="Commandes Linux - Installation et Capture réseau (PCAP) depuis le routeur"
# Mettre à jour les dépôts de paquets OpenWrt
opkg update

# Installer tcpdump
opkg install tcpdump

# Lancer une capture brute de tout le trafic transitant sur le LAN (bridge)
# Appuyer sur Ctrl+C pour stopper la capture
tcpdump -i br-lan -w /tmp/capture.pcap
```

```bash title="Commandes depuis votre PC Analyste"
# Récupérer la capture sur votre machine pour l'ouvrir dans Wireshark
scp root@192.168.50.1:/tmp/capture.pcap ./mon_analyse.pcap
```

<br>

---

<br>

## Durcissement final (Hardening) et Sauvegarde

> Le tableau ci-dessous résume les actions de sécurisation vitales du routeur :

| Mesure de sécurité | Commande ou Action correspondante |
|---|---|
| **Désactiver le SSH depuis l'extérieur (WAN)** | `uci set dropbear.@dropbear[0].Interface='lan'` |
| **Désactiver la réponse au Ping sur le WAN** | À configurer via le Firewall dans l'interface LuCI. |
| **Mot de passe robuste** | La commande `passwd` doit avoir été exécutée. |
| **Mises à jour firmware régulières** | Commande `sysupgrade` (Attention, efface les paquets additionnels). |

### Sauvegarde cryptographique complète

L'infrastructure étant configurée, il faut "prendre une photo" de son état final (Baseline).

```bash title="Commandes Linux - Backup via sysupgrade - (Sauvegarde des configurations)"
# Créer une archive de sauvegarde sur le routeur
sysupgrade -b /tmp/router-backup.tar.gz
```

```bash title="Commandes depuis votre PC Analyste"
# Rapatrier l'archive sur le PC
scp root@192.168.50.1:/tmp/router-backup.tar.gz ./openwrt-artech-backup-$(date +%Y%m%d).tar.gz

# Empreinte cryptographique pour certifier la sauvegarde
sha256sum openwrt-artech-backup-*.tar.gz > router-backup.sha256
```

<br>

---

<br>

## Auto-évaluation

Testez vos connaissances sur l'administration OpenWrt :

> Questions rapides de contrôle :

| # | Question | Réponse attendue |
|---|---|---|
| **1** | Où vérifier la révision matérielle de l'Archer C7 ? | Sur l'étiquette collée sous le châssis physique. |
| **2** | Quelle est l'adresse IP par défaut après un flashage OpenWrt ? | `192.168.1.1` (Puis `192.168.50.1` après notre config). |
| **3** | Quel est le mot de passe root par défaut sur OpenWrt ? | Il n'y en a pas (vide). Il faut utiliser `passwd` immédiatement. |
| **4** | Dans quel fichier modifie-t-on l'architecture réseau (VLAN, Subnet) ? | `/etc/config/network`. |
| **5** | Quelle commande recharge le service réseau de manière abrupte ? | `/etc/init.d/network restart`. |
| **6** | Comment prendre un snapshot de sauvegarde global de la configuration ? | Via la commande `sysupgrade -b`. |

<br>

---

<br>

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Flasher un routeur avec OpenWrt transforme une vulgaire box domestique en équipement réseau d'entreprise. Vous contrôlez désormais le plan d'adressage de la PME ARTECH et disposez de la capacité redoutable de capturer silencieusement les paquets réseau à la source. L'infrastructure cœur est prête.

> [Chapitre suivant : 3.5 Wi-Fi WPA2-PSK volontairement faible →](05-wifi-wpa2-faible.md)
>
> [Retour à l'index →](./index.md)

<br>
