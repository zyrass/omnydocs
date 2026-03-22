---
description: "Mise en œuvre, administration, durcissement et supervision des infrastructures informatiques locales et réseaux."
icon: lucide/server
tags: ["SYTEME", "LINUX", "WINDOWS", "RESEAU", "INFRASTRUCTURE"]
---

# Systèmes & Infra

<div
  class="omny-meta"
  data-level="🟢 Débutant à 🔴 Avancé"
  data-version="1.0"
  data-time="10-15 minutes">
</div>

!!! quote "Analogie"
    _Le développeur construit les bâtiments; l'administrateur système et opérations prépare le terrain, pose les fondations, construit les routes de communication (les réseaux), installe les caméras de vidéosurveillance (monitoring) et sécurise les portes (firewalls)._

!!! abstract "Résumé"
    Contrairement aux Fondamentaux IT (conceptuels) et au Développement Web (applicatif), cette vaste partie adopte une approche 100% orientée **exploitation**. Y sont traités l'administration de systèmes **Linux** et **Windows**, le déploiement et maintien des **Réseaux**, et l'ensemble des piliers modernes de l'infrastructure que sont la virtualisation, le stockage et l'observabilité.

!!! info "Prérequis : Fondamentaux IT"
    L'administration de systèmes et réseaux exige une compréhension des modèles conceptuels (OSI, TCP/IP) ou du rôle d'un OS (Kernel vs User-space). Il est très fortement recommandé d'avoir assimilé la section **Bases & IT** avant d'appliquer des configurations dans cette partie.

<br />

---

## Les piliers de l'exploitation

Cette macro-section s'articule autour de six compétences et domaines incontournables pour les ingénieurs infrastructure, administrateurs et SRE (Site Reliability Engineers).

<div class="grid cards" markdown>

-   :simple-linux:{ .lg .middle } **Systèmes Linux**

    ---

    **Périmètre** : Le moteur du web. Automatisation par shell (`Bash`), gestion fine de l'OS (`systemd`, permissions), et son **durcissement profond** (`ufw`, `fail2ban`, `lynis`, auditing).

    [:octicons-arrow-right-24: Entrer dans l'univers Linux](./linux/index.md)

-   :simple-windows:{ .lg .middle } **Systèmes Windows**

    ---

    **Périmètre** : Au cœur des environnements d'entreprise. Administration poussée en ligne de commande via **PowerShell**, structuration de domaines avec l'**Active Directory (AD)** et sécurisation serveur (GPO/Hardening).

    [:octicons-arrow-right-24: Découvrir l'administration Windows](./windows/index.md)

-   :lucide-network:{ .lg .middle } **Services Réseau & Périphéries**

    ---

    **Périmètre** : Les outils d'analyse vitaux (tcpdump, scapy, nslookup), les services DNS, SSH, LDAP... sans oublier les briques de **sécurité périmétrique** indispensables (pfSense, WAF, proxy et VPN).

    [:octicons-arrow-right-24: Analyser et protéger les flux](./network/index.md)

-   :lucide-cpu:{ .lg .middle } **Virtualisation (Hyperviseurs)**

    ---

    **Périmètre** : Comprendre et appliquer les briques permettant l'isolation, du simple l'émulateur (**QEMU**) à l'hyperviseur bare-metal de Type 1 ultra performant en production (**KVM / Proxmox**).

    [:octicons-arrow-right-24: Isoler et virtualiser](./virtualisation/index.md)

-   :lucide-hard-drive:{ .lg .middle } **Stockage & PRA**

    ---

    **Périmètre** : Assurer la continuité d'activité à tout prix et sans erreur. Les systèmes de fichiers, les architectures **RAID**, et les plans de reprise d'activité (**PRA** / Sauvegardes / Amanda).

    [:octicons-arrow-right-24: Sauvegarder et organiser](./storage/index.md)

-   :lucide-activity:{ .lg .middle } **Supervision (Observabilité)**

    ---

    **Périmètre** : Vous ne pouvez pas défendre ou réparer ce que vous ne voyez pas. L'étude des Logs (systèmes & composants) et le monitoring réseau avec `ntop`/`ntopng`.

    [:octicons-arrow-right-24: Garder un œil sur les systèmes](./supervision/index.md)

</div>

<br />

---

## Conclusion

!!! quote "Conclusion"
    _Maintenir une infrastructure va bien au-delà de l'installation du système d'exploitation de base. Il s'agit d'orchestrer sa résilience face aux corruptions (Virtualisation/PRA), de prévenir ou repérer les failles béantes (Supervision/Durcissement) et de distribuer les ressources de manière adéquate via des briques réseaux robustes. Un bon administrateur ne règle pas les problèmes en urgence ; il bâtit des systèmes conçus pour ne jamais s'effondrer._

<br />