---
description: "Fiabiliser le stockage des données : File Systems, RAID, Sauvegardes et Plans de Reprise."
tags: ["STOCKAGE", "RAID", "SAUVEGARDE", "PRA", "INFRASTRUCTURE"]
---

# Stockage et PRA

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="Hub Stockage">
</div>

!!! quote "Les données sont l'entreprise"
    _Un serveur qui grille, cela coûte 5 000 euros et se remplace en 24 heures. Les données (Base de données clients, codes sources, comptabilité) perdues dans ce serveur qui grille, cela coûte l'existence même de l'entreprise. L'ingénieur infrastructure a pour mission absolue de garantir l'intégrité, la disponibilité et la pérennité de la donnée._

## Garantir l'immortalité de la donnée

La perte de données a généralement deux causes : la panne matérielle (le disque dur meurt) ou l'erreur humaine/malveillante (un stagiaire fait `rm -rf`, ou un Ransomware chiffre les fichiers). Ce hub traite des défenses contre ces deux scénarios.

<div class="grid cards" markdown>

-   :lucide-hard-drive:{ .lg .middle } **RAID & Systèmes de Fichiers**

    ---
    Comment survivre à la mort physique d'un disque dur (RAID) et comment le système d'exploitation organise mathématiquement les données (EXT4, ZFS, BTRFS).

    [:octicons-arrow-right-24: Fiabiliser le matériel](./raid-fs.md)

-   :lucide-database-backup:{ .lg .middle } **Sauvegarde & PRA**

    ---
    La règle du 3-2-1. La différence fondamentale entre une sauvegarde et de la redondance. La création d'un Plan de Reprise d'Activité (PRA).

    [:octicons-arrow-right-24: Concevoir les sauvegardes](./backup-pra.md)

-   :lucide-archive-restore:{ .lg .middle } **Outil : Amanda**

    ---
    Découverte d'Amanda (Advanced Maryland Automatic Network Disk Archiver), l'outil open-source historique pour gérer les sauvegardes réseau centralisées.

    [:octicons-arrow-right-24: Gérer les backups réseau](./amanda.md)

</div>

## Le lien avec la Cybersécurité (Ransomware)

Le **Ransomware** (Rançongiciel) est aujourd'hui la menace numéro un dans le monde. La seule véritable défense absolue contre un ransomware n'est ni un pare-feu, ni un antivirus, c'est **la Sauvegarde Déconnectée**.
Si le pirate chiffre votre serveur, vous effacez tout, vous restaurez la sauvegarde d'hier, et vous reprenez le travail sans payer la rançon. C'est pourquoi les pirates modernes cherchent en priorité à détruire les serveurs de sauvegarde *avant* de lancer le ransomware. Sécuriser l'architecture de sauvegarde est donc le cœur de la défense Cyber.
