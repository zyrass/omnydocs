---
description: "L'administration des environnements Microsoft en entreprise, du PowerShell à l'Active Directory."
tags: ["WINDOWS", "SYSTEME", "AD", "GPO", "POWERSHELL"]
---

# Systèmes Windows Server

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="Hub Windows">
</div>

!!! quote "Le pilier de l'entreprise"
    _Si Linux est le roi incontesté de l'hébergement Cloud public et des serveurs web, **Windows Server** règne en maître absolu sur l'infrastructure interne des entreprises de taille moyenne et grande. Gérer un parc de 500 ordinateurs employés, centraliser leurs mots de passe, et déployer des règles de sécurité globables est un cauchemar sous Linux. Sous Windows, grâce à l'Active Directory, c'est natif._

## Organisation de la section

Contrairement au développement logiciel, l'administration d'un parc Windows d'entreprise demande une grande rigueur, une compréhension de la philosophie Microsoft (très orientée "Objet" même dans son Shell) et une maîtrise des politiques de groupe.

<div class="grid cards" markdown>

-   :lucide-terminal-square:{ .lg .middle } **Automatisation (PowerShell)**

    ---
    Oubliez l'invite de commande DOS obsolète (cmd). Découvrez le Shell moderne, surpuissant et orienté objet de Microsoft pour automatiser l'administration.

    [:octicons-arrow-right-24: Maîtriser PowerShell](./powershell.md)

-   :lucide-network:{ .lg .middle } **L'Annuaire (AD & GPO)**

    ---
    Le cœur nucléaire du réseau d'entreprise. Gérer de manière centralisée des milliers d'utilisateurs, d'ordinateurs et appliquer des stratégies globales (GPO).

    [:octicons-arrow-right-24: Explorer l'Active Directory](./ad-gpo.md)

-   :lucide-shield-half:{ .lg .middle } **Sécurisation (Hardening)**

    ---
    Un serveur Windows non durci est la cible favorite des ransomwares. Apprenez les meilleures pratiques pour verrouiller un contrôleur de domaine et limiter la surface d'attaque.

    [:octicons-arrow-right-24: Durcir Windows Server](./hardening.md)

</div>

## Le Changement de Paradigme (CLI vs GUI)

Il est tentant d'administrer Windows Server uniquement à la souris (via le Server Manager). **C'est une très mauvaise habitude.** 

Microsoft pousse depuis plus de 10 ans l'installation de "Windows Server Core" (une version sans aucune interface graphique) pour des raisons de sécurité (surface d'attaque réduite) et de performance. L'administrateur moderne doit être capable de gérer un domaine entier via `PowerShell` ou des outils d'administration à distance (RSAT / Windows Admin Center).
