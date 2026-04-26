---
description: "Arch-Lab : laboratoire complet multi-OS sous VirtualBox pour l'apprentissage professionnel de Linux, des réseaux et de la cybersécurité. Sept modules progressifs de la théorie à la pratique."
tags: ["LAB", "ARCH", "VIRTUALBOX", "MULTI-OS", "FORMATION", "CYBER", "DEVSECOPS"]
---

# Linux (Arch Lab)

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire & 🔴 Avancé"
  data-version="0.2"
  data-time="3h à 6h par module">
</div>


!!! quote "Analogie pédagogique"
    _Concevoir l'architecture d'un projet de bout en bout, c'est passer du métier de maçon à celui d'architecte urbaniste. Vous ne posez plus seulement des briques (code), vous anticipez les flux de circulation, la résistance aux séismes (pannes de serveurs) et l'ajout de futurs quartiers (scalabilité)._

## Bienvenue dans Arch-Lab

**Arch-Lab** est un laboratoire complet et structuré conçu pour **vous permettre** de maîtriser les systèmes Linux, les réseaux virtuels et l'administration multi-plateformes dans un environnement professionnel simulé.

Ce projet **vous guide** à travers la construction progressive d'un environnement virtualisé composé de :

- **Arch Linux** (serveur minimal et poste desktop)
- **Ubuntu LTS** (écosystème Debian/apt)
- **Rocky Linux** (écosystème Red Hat/dnf, standard entreprise)
- **Windows** (poste utilisateur et administration)
- **Un réseau VirtualBox** segmenté et sécurisé (NAT, Host-Only, Internal)

!!! abstract "Philosophie du projet"
    Arch-Lab ne se limite pas à l'installation de systèmes d'exploitation. Il **vous enseigne** la logique d'architecture, les différences fondamentales entre les familles Linux, la conception réseau et les bonnes pratiques professionnelles utilisées en entreprise, en DevSecOps et en cybersécurité.

<br>

---

## Parcours Pédagogique

Ce laboratoire est organisé en **sept modules progressifs**, chacun construisant sur les connaissances du précédent. Vous êtes libre de suivre ce parcours à votre rythme, mais l'ordre recommandé garantit une progression logique et cohérente.

### Aperçu des Modules

<div class="grid cards" markdown>

-   :lucide-book-open:{ .lg .middle } **Module 1 : Vision Globale du Projet**

    ---

    **Durée estimée :** 30-40 minutes  
    **Niveau :** 🟢 Débutant

    Découvrez les objectifs pédagogiques d'Arch-Lab, l'architecture d'ensemble, le rôle de chaque distribution et la logique de construction du laboratoire.

    Ce module **vous donne** les clés pour comprendre pourquoi chaque système a été choisi et comment ils s'articulent dans un environnement professionnel.

    [:lucide-arrow-right: Accéder au Module 1](#module-1-vision-globale)

-   :lucide-layers:{ .lg .middle } **Module 2 : Panorama des Familles Linux**

    ---

    **Durée estimée :** 50-70 minutes  
    **Niveau :** 🟢 Débutant & 🟡 Intermédiaire

    Comprenez les différences fondamentales entre Debian/Ubuntu (apt), Red Hat/Rocky (dnf/yum) et Arch (pacman).

    Ce module **vous permet** d'identifier les philosophies, les cycles de vie, les formats de paquets et les cas d'usage de chaque famille.

    [:lucide-arrow-right: Accéder au Module 2](#module-2-panorama-linux)

-   :lucide-server:{ .lg .middle } **Module 3 : Installation Arch Linux Serveur**

    ---

    **Durée estimée :** 90-120 minutes  
    **Niveau :** 🟡 Intermédiaire

    Installez un serveur Arch Linux minimal sous VirtualBox avec UEFI, GPT, systemd-boot et NetworkManager.

    Ce module **vous enseigne** l'installation manuelle complète d'Arch, pierre angulaire de votre compréhension système.

    [:lucide-arrow-right: Accéder au Module 3](#module-3-arch-serveur)

-   :lucide-monitor:{ .lg .middle } **Module 4 : Installation Arch Linux Desktop**

    ---

    **Durée estimée :** 75-90 minutes  
    **Niveau :** 🟡 Intermédiaire

    Transformez votre serveur Arch en poste desktop avec KDE Plasma ou GNOME, Display Manager et outils essentiels.

    Ce module **vous apprend** à construire un environnement graphique moderne et optimisé pour VirtualBox.

    [:lucide-arrow-right: Accéder au Module 4](#module-4-arch-desktop)

-   :lucide-network:{ .lg .middle } **Module 5 : Réseau VirtualBox Professionnel**

    ---

    **Durée estimée :** 90-110 minutes  
    **Niveau :** 🟡 Intermédiaire & 🔴 Avancé

    Concevez une topologie réseau réaliste avec NAT, Host-Only et Internal Network.

    Ce module **vous forme** à la segmentation réseau, l'adressage IP et l'isolation des machines comme en environnement d'entreprise.

    [:lucide-arrow-right: Accéder au Module 5](#module-5-reseau-virtualbox)

-   :lucide-package:{ .lg .middle } **Module 6 : Déploiement Multi-OS**

    ---

    **Durée estimée :** 120-180 minutes  
    **Niveau :** 🟡 Intermédiaire & 🔴 Avancé

    Déployez Ubuntu LTS, Rocky Linux et Windows dans votre laboratoire et intégrez-les au réseau.

    Ce module **vous permet** de construire un environnement complet simulant un petit datacenter d'entreprise.

    [:lucide-arrow-right: Accéder au Module 6](#module-6-lab-multi-os)

-   :lucide-wrench:{ .lg .middle } **Module 7 : Automatisation et Maintenance**

    ---

    **Durée estimée :** 40-60 minutes  
    **Niveau :** 🟡 Intermédiaire

    Maîtrisez les snapshots, les scripts d'automatisation VirtualBox et les bonnes pratiques de maintenance.

    Ce module **vous donne** les outils pour industrialiser votre laboratoire et le rendre reproductible.

    [:lucide-arrow-right: Accéder au Module 7](#module-7-annexes)

</div>

---

## Objectifs Pédagogiques d'Arch-Lab

À l'issue de ce parcours complet, **vous serez capable de** :

<div class="grid cards" markdown>

-   :fontawesome-solid-graduation-cap:{ .lg .middle } **Maîtriser les Familles Linux**

    ---

    Comprendre les différences entre Debian/Ubuntu (apt), Red Hat/Rocky (dnf) et Arch (pacman).
    
    Identifier la famille adaptée selon le contexte : développement, production, formation, cybersécurité.
    
    Naviguer efficacement dans les trois écosystèmes de gestion de paquets.

-   :fontawesome-solid-server:{ .lg .middle } **Construire des Systèmes de Zéro**

    ---

    Installer manuellement Arch Linux en mode UEFI/GPT avec systemd-boot.
    
    Comprendre l'architecture interne d'un système Linux moderne (boot, init, réseau, utilisateurs).
    
    Transformer un serveur minimal en poste desktop complet avec environnement graphique.

-   :fontawesome-solid-diagram-project:{ .lg .middle } **Concevoir un Réseau Virtuel Professionnel**

    ---

    Créer une topologie réseau réaliste avec VirtualBox (NAT, Host-Only, Internal Network).
    
    Segmenter et isoler les machines selon leurs rôles (serveurs, postes utilisateurs, administration).
    
    Maîtriser l'adressage IP statique et les tests de connectivité inter-systèmes.

-   :fontawesome-solid-shield-halved:{ .lg .middle } **Orchestrer un Laboratoire Multi-OS**

    ---

    Déployer et intégrer Ubuntu, Rocky Linux, Arch et Windows dans un environnement cohérent.
    
    Reproduire un mini-datacenter d'entreprise virtualisé pour des scénarios réalistes.
    
    Maintenir et automatiser votre laboratoire avec snapshots, clonage et scripts.

</div>

---

## Prérequis Techniques

Avant de commencer Arch-Lab, **assurez-vous de disposer de** :

### Matériel

- **CPU** : processeur 64 bits avec support de virtualisation (Intel VT-x ou AMD-V activé dans le BIOS)
- **RAM** : 16 Go minimum (48 Go recommandé pour faire tourner toutes les VMs simultanément)
- **Stockage** : 150 Go d'espace disque disponible (SSD fortement recommandé)
- **Système hôte** : Windows 10/11, Linux ou macOS

### Logiciels

- **VirtualBox** : version 7.0 ou supérieure ([télécharger](https://www.virtualbox.org/))
- **Extension Pack VirtualBox** : pour les fonctionnalités avancées (USB 3.0, PXE boot)
- **ISO Arch Linux** : dernière version ([télécharger](https://archlinux.org/download/))
- **ISO Ubuntu LTS** : version 24.04 recommandée ([télécharger](https://ubuntu.com/download/desktop))
- **ISO Rocky Linux** : version 9.x ([télécharger](https://rockylinux.org/download))
- **ISO Windows** : Windows 10 ou 11 (avec licence valide)

### Connaissances

- **Utilisation basique** d'un terminal Linux (commandes `cd`, `ls`, `sudo`)
- **Notions de réseau** (adresse IP, masque de sous-réseau, gateway)
- **Compréhension du concept** de machine virtuelle

!!! tip "Si vous êtes débutant"
    Ne vous inquiétez pas si certains concepts vous semblent flous. Chaque module **vous explique** en détail chaque étape, chaque commande et chaque option utilisée.

---

## Organisation du Travail

### Durée Totale Estimée

| Profil | Durée estimée |
|--------|---------------|
| **Débutant** (suit chaque étape attentivement) | 12 à 15 heures |
| **Intermédiaire** (connaissances Linux de base) | 8 à 10 heures |
| **Avancé** (expérience système et réseau) | 6 à 8 heures |

### Rythme Recommandé

1. **Jour 1** : Modules 1 et 2 (fondations théoriques)
2. **Jour 2** : Module 3 (installation Arch Serveur)
3. **Jour 3** : Module 4 (installation Arch Desktop)
4. **Jour 4** : Module 5 (réseau VirtualBox)
5. **Jour 5** : Module 6 (déploiement multi-OS)
6. **Jour 6** : Module 7 (automatisation et consolidation)

!!! warning "Important"
    Prenez le temps de **faire des pauses régulières**. L'installation manuelle d'Arch Linux (Module 3) est techniquement exigeante et nécessite concentration et attention.

---

## Structure des Modules

Chaque module suit une structure pédagogique cohérente :

1. **Introduction** : contexte et objectifs du module
2. **Objectifs d'apprentissage** : ce que vous saurez faire à la fin
3. **Prérequis** : vérifications avant de commencer
4. **Schémas et diagrammes** : représentations visuelles des concepts
5. **Procédures détaillées** : étapes pas à pas avec commandes commentées
6. **Vérifications** : tests pour valider chaque étape
7. **Dépannage** : solutions aux problèmes courants
8. **Le mot de la fin** : récapitulatif et préparation du module suivant
9. **Ressources complémentaires** : liens vers documentation officielle

---

## Conventions Utilisées

### Blocs de Code

```bash
# Les commentaires précèdent toujours les commandes
# Ils expliquent le pourquoi et le comment
commande --option argument
```

### Notes Importantes

!!! info "Information"
    Points d'information complémentaires pour approfondir votre compréhension.

!!! tip "Astuce"
    Conseils pratiques pour gagner du temps ou éviter des erreurs courantes.

!!! warning "Attention"
    Points de vigilance importants pour éviter des problèmes.

!!! danger "Critique"
    Avertissements sur des actions potentiellement destructrices.

### Footnotes

Les termes techniques sont systématiquement expliqués en bas de page[^1].

[^1]: **Footnote** : note explicative en bas de page pour clarifier un concept sans alourdir le texte principal.

---

## Philosophie Pédagogique

Arch-Lab repose sur trois piliers :

### 1. Apprentissage par la Pratique

Vous n'apprendrez pas en lisant passivement. Chaque module **vous demande** de manipuler, d'installer, de configurer. C'est en faisant que vous comprendrez réellement.

### 2. Compréhension Profonde

Nous ne nous contentons pas de copier-coller des commandes. Chaque commande est **expliquée**, chaque option est **détaillée**, chaque choix est **justifié**.

### 3. Approche Professionnelle

Ce laboratoire reproduit des pratiques d'entreprise réelles : segmentation réseau, snapshots, documentation, scripts d'automatisation. Vous construisez des compétences directement transférables en contexte professionnel.

---

## Communauté et Support

### Ressources Officielles

- **Arch Wiki** : [wiki.archlinux.org](https://wiki.archlinux.org) - documentation de référence
- **VirtualBox Manual** : [virtualbox.org/manual](https://www.virtualbox.org/manual/) - manuel officiel
- **Rocky Linux Docs** : [docs.rockylinux.org](https://docs.rockylinux.org) - documentation Rocky
- **Ubuntu Documentation** : [help.ubuntu.com](https://help.ubuntu.com) - aide Ubuntu

### Forums et Communautés

- **Arch Linux Forums** : [bbs.archlinux.org](https://bbs.archlinux.org)
- **Reddit /r/archlinux** : communauté active et bienveillante
- **Stack Overflow** : pour les questions techniques précises

---

## Licence et Utilisation

Ce projet est conçu à des fins **pédagogiques et éducatives**. Vous êtes libre de :

- Suivre ce parcours à votre rythme
- Adapter les configurations à vos besoins
- Réutiliser les scripts et configurations fournis
- Partager ce projet avec d'autres apprenants

!!! note "Attribution"
    Si vous réutilisez ou adaptez ce contenu, merci de mentionner Arch-Lab comme source.

---

## Prêt à Commencer ?

Vous avez maintenant toutes les informations nécessaires pour démarrer votre aventure Arch-Lab.

**Commencez par le Module 1** pour découvrir la vision globale du projet, comprendre l'architecture d'ensemble et saisir comment les sept modules s'articulent.

[:lucide-rocket: Commencer le Module 1](./01-introduction.md){ .md-button .md-button--primary }

---

## Changelog

| Version | Date | Modifications |
|---------|------|---------------|
| 1.0 | 2025-01-XX | Version initiale complète des 7 modules |

---

**Bonne formation, et n'oubliez pas : l'apprentissage système demande patience, rigueur et curiosité. Prenez votre temps, expérimentez, cassez, réparez. C'est ainsi que l'on devient expert.**

<!-- 

---
description: "Arch-Lab : laboratoire complet multi-OS sous VirtualBox (Arch, Ubuntu, Rocky, Windows) pour l’apprentissage de Linux, des réseaux et de la cybersécurité."
icon: lucide/briefcase-business
tags: ["LAB", "ARCH", "VIRTUALBOX", "MULTI-OS", "FORMATION", "CYBER", "DEVSECOPS"]
---

# Arch-Lab — Laboratoire Multi-OS sous VirtualBox

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire & 🔴 Avancé"
  data-version="1.0"
  data-time="3h à 6h (par modules)">
</div>

## Présentation générale

**Arch-Lab** est un laboratoire complet, conçu pour reproduire un environnement professionnel multi-systèmes sous VirtualBox :

- Arch Linux (serveur minimal + poste desktop)  
- Ubuntu LTS (famille apt)  
- Rocky Linux (famille dnf/yum, univers RHEL)  
- Windows (poste utilisateur / administration)  
- un réseau structuré (NAT, Host-Only, Internal)  
- des scénarios compatibles administration, Dev, DevSecOps et cybersécurité.

L’objectif est de fournir un socle pédagogique permettant de :

- comprendre les différences entre les principales familles GNU/Linux ;  
- apprendre à construire et administrer des OS de manière structurée ;  
- modéliser un réseau interne réaliste, comparable à un petit SI d’entreprise ;  
- disposer d’un environnement stable pour les futurs labs (SOC, pentest, SIEM, etc.).

:::info
Les pages de ce projet sont fortement inter-dépendantes :  
il est recommandé de suivre les modules **dans l’ordre** pour conserver une cohérence technique et pédagogique.
:::

---

## Parcours recommandé

Le projet Arch-Lab est découpé en **sept modules**, chacun formalisé dans un fichier Zensical dédié.

Chaque carte ci-dessous affiche :

- un **rôle** du module dans le projet,  
- les **prérequis** attendus,  
- un lien direct vers le fichier associé,  
- un identifiant d’icône (`lucide-*` ou `fontawesome-brands-*`) exploitable par vos templates.

---

<div class="grid cards" markdown>

-   <div class="card-icon" data-icon="lucide/layers" data-fa="fontawesome-brands-x"></div>

    ### 01. Introduction — Vision & Architecture Globale  
    **Fichier :** `01-introduction.md`  

    Ce module présente l’architecture générale d’Arch-Lab :  
    objectifs pédagogiques, positionnement des distributions, rôle de VirtualBox et vue d’ensemble du réseau (NAT / Host-Only / Internal).

    Il sert de **porte d’entrée** au projet, en expliquant comment les sept fichiers s’articulent et en quoi ce lab peut être utilisé en développement, administration, DevSecOps et cybersécurité.

    [:lucide-arrow-right Accéder au module](./01-introduction.md)

-   <div class="card-icon" data-icon="lucide/boxes" data-fa="fontawesome-brands-linux"></div>

    ### 02. Panorama des Familles GNU/Linux (apt / dnf-yum / pacman)  
    **Fichier :** `02-panorama-linux.md`  

    Ce module analyse les trois grandes familles :

    - Debian / Ubuntu (apt)  
    - Red Hat / Rocky / Fedora (dnf/yum)  
    - Arch Linux (pacman)

    Il décrit leurs philosophies, leurs formats de paquets, leurs usages typiques et leur rôle dans un laboratoire multi-OS.

    [:lucide-arrow-right Accéder au module](./02-panorama-linux.md)

-   <div class="card-icon" data-icon="lucide/server" data-fa="fontawesome-brands-x"></div>

    ### 03. Arch Serveur Minimal — Base du Lab  
    **Fichier :** `03-arch-serveur.md`  

    Installation complète d’un **serveur Arch Linux minimal** sous VirtualBox (UEFI, GPT, pacstrap, systemd-boot, NetworkManager, compte administrateur, Guest Additions).

    Ce serveur constitue la **fondation technique** du lab, réutilisable comme template pour d’autres rôles (web, DNS, bastion, etc.).

    [:lucide-arrow-right Accéder au module](./03-arch-serveur.md)

-   <div class="card-icon" data-icon="lucide/monitor" data-fa="fontawesome-brands-desktop"></div>

    ### 04. Arch Desktop — Poste Utilisateur KDE / GNOME  
    **Fichier :** `04-arch-desktop.md`  

    Transformation d’une base Arch en **poste Desktop** complet :

    - installation de Xorg,  
    - KDE Plasma ou GNOME,  
    - Display Manager (SDDM/GDM),  
    - polices, outils essentiels, intégration VirtualBox.

    Ce poste est le **point d’observation principal** du lab pour les scénarios utilisateurs.

    [:lucide-arrow-right Accéder au module](./04-arch-desktop.md)

-   <div class="card-icon" data-icon="lucide/network" data-fa="fontawesome-brands-sitemap"></div>

    ### 05. Réseau VirtualBox — NAT, Host-Only, Internal  
    **Fichier :** `05-virtualbox-reseau.md`  

    Conception et mise en place d’une **topologie réseau professionnelle** sous VirtualBox :

    - NAT pour l’accès Internet,  
    - Host-Only pour l’administration depuis l’hôte,  
    - Internal Network pour le LAN isolé du lab.

    Le module inclut des schémas Mermaid, un plan d’adressage standard et des bonnes pratiques de cloisonnement.

    [:lucide-arrow-right Accéder au module](./05-virtualbox-reseau.md)

-   <div class="card-icon" data-icon="lucide/terminal" data-fa="fontawesome-brands-microsoft"></div>

    ### 06. Lab Multi-OS — Arch, Ubuntu, Rocky, Windows  
    **Fichier :** `06-lab-multi-os.md`  

    Assemblage complet du lab :

    - intégration d’Ubuntu LTS (apt),  
    - intégration de Rocky Linux (dnf/yum, univers RHEL),  
    - intégration d’une machine Windows,  
    - cohérence réseau et scénarios pédagogiques.

    Ce module transforme Arch-Lab en **mini-SI d’entreprise** virtualisé.

    [:lucide-arrow-right Accéder au module](./06-lab-multi-os.md)

-   <div class="card-icon" data-icon="lucide/wrench" data-fa="fontawesome-brands-git-alt"></div>

    ### 07. Annexes, Snapshots & Automatisation  
    **Fichier :** `07-annexes.md`  

    Ensemble des **outils de maintenance et d’industrialisation** :

    - méthodologie de snapshots,  
    - scripts `VBoxManage` pour démarrer/arrêter/exporter les VMs,  
    - standardisation des hostnames et interfaces,  
    - organisation de l’arborescence de travail,  
    - export global du lab.

    Ce module permet d’inscrire Arch-Lab dans une démarche professionnelle, reproductible, versionnable.

    [:lucide-arrow-right Accéder au module](./07-annexes.md)

</div> -->

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La compréhension des principes d'architecture est la vraie barrière entre le simple codeur et l'ingénieur logiciel. Ce lab pose les bases méthodologiques qui vous suivront tout au long de votre carrière, peu importe le langage que vous utiliserez.

!!! quote "Arch-Lab — votre mini-datacenter privé"
    En sept modules progressifs, vous allez passer de zéro à un **laboratoire multi-OS professionnel** : cinq systèmes interconnectés, trois familles Linux maîtrisées, et une infrastructure réseau segmentée identique à celle des entreprises. C'est votre terrain d'entraînement pour Linux, la cybersecurité et le DevSecOps.

**Commencez par le Module 1 pour découvrir l'architecture globale du projet.**

[:lucide-arrow-right: Démarrer le Module 1](./01-introduction.md){ .md-button .md-button--primary }
