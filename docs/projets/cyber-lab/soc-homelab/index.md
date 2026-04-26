---
description: "Cyber-Lab — Introduction au SOC minimaliste open-source, pré-requis et configuration matérielle."
---

# SOC Homelab

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Wazuh, Suricata, Vagrant"
  data-time="~30 min">
</div>

## Avant-propos - Comment lire ce cours

!!! quote "Analogie pédagogique — L'apprentissage par la pratique"
    Lire un manuel sur la construction d'un SOC, c'est comme lire un livre sur la natation : on comprend le mouvement, mais on coule une fois dans l'eau. Ce cours n'est pas un manuel théorique, c'est un **laboratoire d'entraînement**. Vous n'allez pas lire sur les SOC, vous allez en construire un de toutes pièces, l'attaquer et le défendre.

Ce cours s'adresse à un apprenant qui sait déjà se servir d'une console Linux, qui comprend la pile TCP/IP et qui a déjà touché à la virtualisation. L'objectif n'est pas de redonner les bases mais de **construire un SOC minimaliste de bout en bout** dans un HomeLab Vagrant + VirtualBox, en comprenant chaque décision technique et organisationnelle.

Chaque module respecte la même trame :

1. **Objectifs pédagogiques** - ce qu'il faut savoir et savoir-faire à la fin du module.
2. **Concepts** - le quoi et le pourquoi.
3. **Mise en pratique** - le comment, avec scripts et configurations commentés.
4. **Points de vigilance** - les pièges courants qui font perdre des heures.
5. **Axes d'amélioration** - écarts entre le projet original (février 2025) et l'état de l'art (avril 2026).

Le code, les fichiers de configuration et les scripts sont volontairement annotés ligne par ligne. Si vous lisez ce cours sans tout comprendre, **arrêtez-vous et cherchez** : un SOC se construit sur une compréhension fine des chaînes de causalité.

<br>

---

## 0.1 - Pourquoi ce projet existe

La majorité des PME francophones n'ont **ni équipe sécurité, ni budget SOC**. Quand un dirigeant demande à son responsable IT "est-ce qu'on est protégés ?", la réponse honnête est souvent "je ne sais pas, on n'a aucune visibilité sur ce qui se passe sur nos machines". Construire un SOC minimaliste open-source dans un HomeLab répond à trois besoins distincts :

1. **Pédagogique** - comprendre les briques d'un SOC en les manipulant, pas en lisant des slides.
2. **Démonstratif** - produire un livrable qui montre à une direction ce qu'un SOC apporte concrètement, en chiffres.
3. **Capacitaire** - poser les bases techniques et organisationnelles pour passer ensuite à un SOC en production.

!!! note "Origine du projet"
    Le projet original est issu d'une certification (RNCP 36399 - Expert en sécurité digitale) ; il n'est ni un produit fini, ni un référentiel d'industrie. Ce cours en extrait les enseignements et corrige ses approximations.

<br>

---

## 0.2 - Pré-requis pour suivre ce cours

| Domaine | Niveau attendu | Pourquoi |
|---|---|---|
| Linux ligne de commande | Confortable avec `apt`, `systemd`, édition de fichiers, droits POSIX | Tout se passe en CLI, sur Ubuntu |
| Réseau TCP/IP | Comprendre IP, routage de base, ICMP, NAT, ports | Le scénario porte sur du trafic ICMP entre VMs |
| Virtualisation | Avoir déjà lancé une VM, compris ce qu'est un host-only | VirtualBox + Vagrant |
| XML / YAML / Ruby | Capable de lire et modifier sans tout casser | Configurations Wazuh, Suricata et Vagrantfile |
| Anglais technique | Lire la doc Wazuh sans traducteur | La documentation officielle est en anglais |

<br>

---

## 0.3 - Configuration matérielle nécessaire

Le projet original tourne sur un poste i5-10600KF avec 32 Go de RAM, ce qui est confortable mais pas nécessaire. Le tableau suivant donne les seuils réalistes pour reproduire ce HomeLab.

| Configuration | RAM hôte | CPU | Disque libre | Verdict |
|---|---|---|---|---|
| Minimale fonctionnelle | 16 Go | 4 cœurs physiques | 60 Go | Limite : Wazuh-Indexer souffre |
| Confortable | 24 Go | 6 cœurs | 80 Go | Bon compromis |
| Recommandée | 32 Go ou + | 8 cœurs | 100 Go SSD | Aucune friction |

!!! warning "Attention aux ressources RAM"
    Sur un Windows 11 hôte qui consomme déjà 8 Go pour le système et les outils habituels, partir de 16 Go totaux est jouable **uniquement** si l'on baisse la mémoire allouée à VM1 (SIEM) à 6 Go. En dessous, Wazuh-Indexer plante au démarrage.

```text title="Allocation mémoire de référence (16 Go hôte, Windows 11)"
Hôte Windows 11 + outils    : 8 Go
VM1 - SIEM (Wazuh complet)  : 6 Go  (au lieu de 8 Go)
VM2 - Attaquant             : 1 Go
VM3 - Cible                 : 1 Go
Réserve système             : 0 Go  (tendu, fermer Chrome avant)
```

_Répartition idéale de la mémoire pour garantir un fonctionnement sans crash du SIEM tout en gardant l'hôte stable._

<br>

---

## 0.4 - Outils logiciels - versions ciblées en 2026

Le projet d'origine utilise Wazuh 4.10.1 et Ubuntu 22.04. Ces versions sont fonctionnelles mais ne sont plus celles qu'un projet neuf utiliserait aujourd'hui. Le tableau suivant fixe les versions de référence pour ce cours.

| Composant | Version projet 2025 | Version cours 2026 | Justification du changement |
|---|---|---|---|
| OS invité | Ubuntu 22.04 LTS (Jammy) | Ubuntu 24.04 LTS (Noble) | LTS plus récente, support jusqu'en 2029 |
| Box Vagrant | `bento/ubuntu-22.04` | `bento/ubuntu-24.04` | Image officielle Bento à jour |
| Wazuh | 4.10.1 | 4.14.5 (stable) | Correctifs de sécurité, SCA Windows 2025, support Ubuntu 24.04 |
| Suricata | 6.0.x | 7.0.x LTS | Suricata 6 EOL, 7 est la branche LTS active |
| VirtualBox | 7.0 | 7.1 ou 7.2 | Compatibilité Ubuntu 24.04 et Windows 11 |
| Vagrant | 2.3 | 2.4+ | Support stable des boxes récentes |

!!! caution "À propos de Wazuh 5.0"
    Pour Wazuh, la version 5.0 est en bêta (avril 2026). **Ne pas l'utiliser pour ce cours** : le protocole de communication entre agents et serveur a été réécrit, la documentation est encore mouvante, et les intégrations communautaires (scripts d'alerte) ne sont pas portées.

<br>

---

## 0.5 - Conventions de notation utilisées dans ce cours

```bash title="Code Bash - Exemple de formatage de commande"
# Les blocs de commandes shell sont préfixés par un commentaire
# expliquant ce que fait la ligne, jamais ce qu'elle est.
sudo apt update -y                # Met à jour les index de paquets
sudo apt full-upgrade -y          # Applique les montées de version disponibles
```

_Chaque commande critique sera accompagnée d'un commentaire inline pour expliquer son comportement._

Les chemins absolus sont écrits en `/var/ossec/etc/` ; les variables ou portions à remplacer sont notées `<comme_ceci>`. Les avertissements importants sont introduits via des boîtes d'alerte. Aucun pictogramme ni émoji n'est utilisé en dehors des règles strictes du style Zensical.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Ce projet est une approche "Hands-on" (pratique) : vous allez rencontrer des erreurs, devoir débugger, et lire des logs. La maîtrise de la cybersécurité passe par ces étapes d'essais et erreurs, en comprenant chaque brique que l'on empile.

> Vous avez la configuration matérielle et vous comprenez les objectifs de ce projet. Découvrons ensemble ce qu'est véritablement un SOC dans le **[Module 1 : Comprendre le SOC →](./01-comprendre-soc.md)**
