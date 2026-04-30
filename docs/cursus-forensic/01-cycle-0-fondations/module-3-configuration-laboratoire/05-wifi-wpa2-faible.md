---
title: 3.5 Wi-Fi WPA2-PSK volontairement faible
description: Configuration du Wi-Fi WPA2 avec passphrase volontairement faible pour exercices de capture de handshake et cassage offline avec hashcat. Réalisme pédagogique.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Wi-Fi
  - WPA2
  - Pentest
  - hashcat
data-level: 🔴
---

# 3.5 Wi-Fi WPA2-PSK volontairement faible

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 1 heure |
| Niveau | Pratique |

## 1. Pourquoi un Wi-Fi délibérément faible

L'apprentissage par l'attaque exige des cibles **réalistes**. De nombreuses PME utilisent encore en 2026 :

- WPA2-PSK (pas WPA3)
- Passphrases de 8-16 caractères
- Mots de passe basés sur le nom de l'entreprise + année

C'est ce que vous allez reproduire pour vous entraîner à le casser.

## 2. Configuration OpenWrt

```bash
vi /etc/config/wireless
```

```text
# /etc/config/wireless - Wi-Fi 2.4 GHz uniquement

config wifi-device 'radio0'
    option type 'mac80211'
    option path 'pci0000:00/0000:00:00.0'
    option channel '6'
    option band '2g'
    option htmode 'HT20'
    option country 'FR'
    option txpower '20'
    option disabled '0'

config wifi-iface 'default_radio0'
    option device 'radio0'
    option network 'lan'
    option mode 'ap'
    option ssid 'ARTECH-WIFI'
    option encryption 'psk2'
    option key 'ArtechMedical2020!'
    option ieee80211w '0'
```

```bash
# Application
wifi reload

# Vérification
iw dev wlan0 info
```

## 3. Caractéristiques du mot de passe

`ArtechMedical2020!` :

- 17 caractères
- Lettres maj+min
- Chiffres
- 1 caractère spécial
- **Mais** : structure prévisible (entreprise + année + !)

C'est exactement ce que des dictionnaires modernes (`rockyou.txt` enrichi) détectent.

## 4. Test de validation

Vérifier que le SSID est visible :

```bash
# Depuis votre poste
iwlist wlan0 scan | grep -A 3 ARTECH
nmcli dev wifi list | grep ARTECH
```

Connexion :

```bash
nmcli dev wifi connect ARTECH-WIFI password 'ArtechMedical2020!'
```

---

**Chapitre suivant** : [3.6 Installation Debian 12 serveur](03-6-debian-serveur.md)
