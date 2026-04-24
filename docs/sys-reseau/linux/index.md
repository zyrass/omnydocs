---
description: "Administration avancée, scripting et sécurisation de l'environnement serveur GNU/Linux."
tags: ["LINUX", "SYSTEME", "BASH", "SYSTEMD", "SECURITE"]
---

# Systèmes Linux

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="Hub Linux">
</div>

!!! quote "Le socle de l'Internet mondial"
    _Plus de 90% du cloud public et la quasi-totalité des supercalculateurs tournent sous Linux. Maîtriser l'administration d'un serveur Linux n'est pas une compétence optionnelle, c'est le prérequis fondamental pour tout ingénieur infrastructure, DevOps ou spécialiste en cybersécurité._

## Organisation de la section

Cette section couvre l'utilisation quotidienne d'un serveur Linux (sans interface graphique), sa gestion interne et son durcissement.

<div class="grid cards" markdown>

-   :lucide-terminal:{ .lg .middle } **Shell & Scripting (Bash)**

    ---
    L'automatisation et l'exploitation système par la ligne de commande.

    [:octicons-arrow-right-24: Maîtriser Bash](./bash.md)

-   :lucide-users-cog:{ .lg .middle } **Administration Système**

    ---
    Gestion des utilisateurs, des groupes, des permissions POSIX et des tâches planifiées (cron).

    [:octicons-arrow-right-24: Administrer l'OS](./admin.md)

-   :lucide-cpu:{ .lg .middle } **Services & Daemons (Systemd)**

    ---
    Comprendre le cycle de vie des processus, la journalisation système et la création de services.

    [:octicons-arrow-right-24: Gérer les processus](./services-daemons.md)

-   :lucide-shield-check:{ .lg .middle } **Sécurité & Durcissement (Host)**

    ---
    La protection de l'hôte Linux : Pare-feu (ufw), Anti-Bruteforce (fail2ban), Audit (Lynis) et Anti-malwares (ClamAV, chkrootkit).

    [:octicons-arrow-right-24: Sécuriser Linux](./security/index.md)

</div>