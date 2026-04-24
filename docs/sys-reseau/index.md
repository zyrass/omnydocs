---
description: "Le prérequis absolu à la cybersécurité : concevoir, administrer, durcir et superviser des infrastructures (Linux, Windows, Réseaux, Virtualisation)."
tags: ["SYSTEME", "LINUX", "WINDOWS", "RESEAU", "INFRASTRUCTURE", "DURCISSEMENT"]
---

# Systèmes & Infrastructure (Sys-Réseau)

<div
  class="omny-meta"
  data-level="🟢 Débutant à 🔴 Avancé"
  data-version="2.0"
  data-time="Hub Principal">
</div>

!!! quote "Vous ne pouvez pas défendre ce que vous ne comprenez pas"
    _Il est tentant de vouloir faire de la "Cyber" (Hacking, Pentest, SOC) directement. **C'est une erreur fondamentale.** L'administration système et réseau est le prérequis absolu à la cybersécurité. Avant d'apprendre à exploiter une faille dans un service ou à configurer un pare-feu de nouvelle génération, vous devez savoir comment construire le serveur, configurer les permissions, gérer les routes réseau et lire les journaux de bord. La vraie cybersécurité, c'est avant tout de l'administration système d'excellence._

!!! abstract "Périmètre de la section"
    Cette vaste section adopte une approche 100% orientée **Opérations (Ops) / Blue Team (Défense & Construction)**. Y sont traités l'administration quotidienne et le **durcissement (Hardening)** des systèmes **Linux** et **Windows**, le déploiement des **Réseaux**, et l'ensemble des piliers de l'infrastructure moderne (Virtualisation, Stockage, Observabilité).

## Les Piliers de l'Exploitation

Ce Hub s'articule autour de six domaines incontournables pour les ingénieurs infrastructure, les administrateurs et les futurs experts en cybersécurité.

<div class="grid cards" markdown>

-   :simple-linux:{ .lg .middle } **Systèmes Linux**

    ---

    **Périmètre** : Le moteur du web. Automatisation par shell (`Bash`), gestion fine de l'OS (`systemd`, permissions), et surtout son **durcissement profond** (`ufw`, `fail2ban`, `lynis`, auditing).

    [:octicons-arrow-right-24: Entrer dans l'univers Linux](./linux/index.md)

-   :simple-windows:{ .lg .middle } **Systèmes Windows**

    ---

    **Périmètre** : Au cœur des environnements d'entreprise. Administration poussée en ligne de commande via **PowerShell**, structuration de domaines avec l'**Active Directory (AD)** et sécurisation serveur (GPO/Hardening).

    [:octicons-arrow-right-24: Découvrir l'administration Windows](./windows/index.md)

-   :lucide-network:{ .lg .middle } **Réseaux & Protocoles**

    ---

    **Périmètre** : Les outils d'analyse vitaux (`tcpdump`, `scapy`), les services fondateurs (DNS, SSH, LDAP) et les briques de **sécurité périmétrique** indispensables (pfSense, WAF, proxy et VPN).

    [:octicons-arrow-right-24: Analyser et protéger les flux](./network/index.md)

-   :lucide-cpu:{ .lg .middle } **Virtualisation (Hyperviseurs)**

    ---

    **Périmètre** : Comprendre et appliquer les technologies d'isolation, de l'émulateur basique (**QEMU**) à l'hyperviseur bare-metal ultra performant en production (**KVM / Proxmox**).

    [:octicons-arrow-right-24: Isoler et virtualiser](./virtualisation/index.md)

-   :lucide-hard-drive:{ .lg .middle } **Stockage & Sauvegarde (PRA)**

    ---

    **Périmètre** : Assurer la continuité d'activité (Disaster Recovery). L'architecture matérielle (**RAID**), les systèmes de fichiers, et les Plans de Reprise d'Activité avec des outils comme **Amanda**.

    [:octicons-arrow-right-24: Sauvegarder et organiser](./storage/index.md)

-   :lucide-activity:{ .lg .middle } **Supervision (Observabilité)**

    ---

    **Périmètre** : La vue de l'aigle. L'étude centralisée des Logs (journaux systèmes) et le monitoring temps réel du réseau (`ntop`/`ntopng`) pour repérer instantanément les anomalies.

    [:octicons-arrow-right-24: Garder un œil sur les systèmes](./supervision/index.md)

</div>

## La Frontière avec la "Cyber"

Gardez à l'esprit la limite pédagogique de ce hub :
- Ici, nous apprenons à **construire, faire tourner, et verrouiller (Durcissement/Hardening)** la porte d'un serveur. (Ex: *Configurer `fail2ban` pour bloquer le bruteforce SSH*).
- Les hubs ultérieurs de **Cybersécurité (Gouvernance, Outils, Opérations)** vous apprendront comment tester la solidité de cette porte (Red Team), comment l'auditer selon des normes légales (Gouvernance), ou comment traquer un adversaire qui aurait réussi à l'ouvrir (Threat Hunting).

**Une fois ces 6 piliers maîtrisés, vous serez prêt à plonger dans les tréfonds de la sécurité informatique.**