---
description: "OS Cyber — Le grand comparatif des systèmes d'exploitation dédiés au pentest, au Red Teaming et à l'analyse Forensic : Kali, Parrot, BlackArch, Commando VM."
icon: lucide/monitor-play
tags: ["KALI", "PARROT", "OS", "PENTEST", "FORENSIC"]
---

# Systèmes d'Exploitation Cyber

<div
  class="omny-meta"
  data-level="🟢 Fondamental"
  data-version="2026"
  data-time="~20 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/os.svg" width="250" align="center" alt="Cyber OS Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — La Caisse à Outils vs Le Camion Atelier"
    Vous pouvez très bien installer les outils de pentest (Nmap, Metasploit) un par un sur votre Ubuntu personnel. C'est comme avoir quelques tournevis dans une caisse à outils. Mais les OS spécialisés comme Kali ou Parrot sont des **camions ateliers** : tout y est préinstallé, configuré, mis à jour et organisé par catégories. Quand vous arrivez sur le chantier (la cible), vous ouvrez le camion et vous êtes instantanément opérationnel.

En cybersécurité offensive (Red Team) comme défensive (DFIR), le système d'exploitation n'est pas qu'une plateforme, c'est l'arme principale. Ce module liste et compare les OS les plus reconnus de l'industrie.

<br>

---

## 🐉 1. Le Standard Historique : Kali Linux

Maintenu par Offensive Security (les créateurs de la certification OSCP), Kali est la référence absolue.

- **Base** : Debian (Testing).
- **Philosophie** : Tout pour l'attaque. L'utilisateur root n'est plus par défaut depuis 2020, mais l'OS reste agressif.
- **Les Plus** :
  - **La plus grande communauté** : 90% des tutoriels sur Internet sont faits pour Kali.
  - **Kali NetHunter** : Version mobile pour Android, permettant des attaques WiFi ou BadUSB depuis un smartphone.
  - **Kali Undercover** : Un script amusant qui transforme l'interface de Kali pour ressembler trait pour trait à Windows 10 (pratique pour l'ingénierie sociale dans un train).
- **Inconvénients** : Parfois lourd, il n'est pas conçu comme un OS de bureau quotidien (bien que cela s'améliore).

<br>

---

## 🦜 2. L'Alternative Lègère : Parrot Security OS

Souvent considéré comme l'outsider qui surpasse le maître pour une utilisation quotidienne.

- **Base** : Debian (Testing).
- **Philosophie** : Léger, orienté anonymat et utilisable au quotidien.
- **Les Plus** :
  - **Sandboxing** : De nombreux outils tournent dans des sandbox pour protéger le pentester si un malware se retourne contre lui.
  - **Anonymisation Native** : Intègre Anonsurf, qui route instantanément tout le trafic système à travers le réseau Tor ou I2P en un clic.
  - **Consommation** : Utilise l'environnement de bureau MATE, qui consomme beaucoup moins de RAM que le XFCE de Kali.
- **Inconvénients** : Communauté légèrement plus restreinte (bien que tout outil Kali fonctionne sur Parrot).

<br>

---

## ⬛ 3. Le Poids Lourd : BlackArch Linux

Réservé aux experts, BlackArch est une extension de la redoutable distribution Arch Linux.

- **Base** : Arch Linux.
- **Philosophie** : Avoir *absolument* tous les outils existants.
- **Les Plus** :
  - **Quantité astronomique** : Plus de 2800 outils packagés. Si un obscur script Python publié sur GitHub la veille fait le buzz, il sera sur BlackArch le lendemain.
  - **Contrôle total** : Fidèle à la philosophie Arch, l'utilisateur a un contrôle total sur la configuration de son système.
- **Inconvénients** : Déconseillé aux débutants. Extrêmement lourd si téléchargé en version intégrale (l'ISO pèse plus de 20 Go).

<br>

---

## 🪟 4. Le Choix Windows : Commando VM & FLARE VM

On oublie souvent que le pentest se fait beaucoup dans des environnements Active Directory, où utiliser un outil Windows natif est le meilleur moyen de passer inaperçu (Living off the Land).

### Commando VM (FireEye/Mandiant)
Ce n'est pas un OS, c'est un script PowerShell massif. Vous l'exécutez sur une installation Windows propre, et il installe des centaines d'outils d'attaque (Impacket, BloodHound, Covenant).

### FLARE VM (FireEye/Mandiant)
L'équivalent pour la **Blue Team** (Reverse Engineering et Malware Analysis). Il transforme un Windows standard en laboratoire d'autopsie de virus (débogueurs, désassembleurs, outils Sysinternals).

<br>

---

## 🔎 5. Les OS Dédiés au Forensic & IR

Les OS précédents sont faits pour attaquer. Pour enquêter (DFIR), on a besoin d'OS qui garantissent qu'on ne va pas altérer les disques de la victime.

- **Tsurugi Linux** : Créé en Italie, c'est l'OS spécialisé dans le Digital Forensics, l'Incident Response et l'OSINT. Contrairement à Kali, il bloque par défaut le montage en écriture des disques pour garantir l'intégrité légale des preuves.
- **SIFT Workstation (SANS)** : La distribution de référence pour l'analyse de disques, gérée par l'institut SANS. Souvent couplée à REMnux pour l'analyse malware.

<br>

---

## Tableau Décisionnel

| Scénario | OS Recommandé |
|---|---|
| Débutant, passe la certif OSCP | **Kali Linux** |
| Ordinateur peu puissant, veut de l'anonymat | **Parrot OS** |
| Expert Linux, veut 2800 outils | **BlackArch** |
| Pentest Active Directory très poussé | **Commando VM (Windows)** |
| Réponse à Incident (Copie légale de disque) | **Tsurugi Linux** |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Choisir le bon système d'exploitation est la première décision stratégique d'un opérateur cyber. Si **Kali Linux** demeure le standard absolu pour les débutants, les professionnels s'orientent souvent vers **Parrot OS** pour sa légèreté ou intègrent **Commando VM** pour les attaques sur Active Directory. Du côté défensif, un OS garantissant l'intégrité des preuves comme **Tsurugi** est indispensable.

> Maintenant que vous avez choisi votre camion d'outils, il vous faut un terrain d'entraînement légal pour tirer vos premières balles virtuelles : lisez **[La plateforme DVWA](../web/dvwa.md)**.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La maîtrise théorique et pratique de ces concepts est indispensable pour consolider votre posture de cybersécurité. L'évolution constante des menaces exige une veille technique régulière et une remise en question permanente des acquis.

> [Retour à l'index →](./index.md)
