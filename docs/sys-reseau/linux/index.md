---
description: "Linux : administration système, gestion des services et sécurité hôte — un socle opérationnel pour exploiter et sécuriser un système en production"
tags: ["LINUX", "ADMIN", "SYSTEMD", "SERVICES", "SECURITY", "HARDENING"]
---

# Linux

<div
  class="omny-meta"
  data-level="🟢 Débutant à 🔴 Avancé"
  data-version="1.0"
  data-time="30-60 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    _Linux, c’est comme piloter un atelier. L’administration, c’est la gestion des clés et des accès. Les services & daemons, c’est la chaîne de production. La sécurité hôte, c’est la prévention des incidents, la détection, et la capacité à réagir quand quelque chose déraille._

Cette section “Linux” est construite comme un socle complet et pragmatique. L’objectif n’est pas de “connaître des commandes”, mais de comprendre comment un système fonctionne au quotidien : qui a le droit de faire quoi, quels services tournent, comment ils démarrent, où ils loggent, et comment on protège l’hôte contre les menaces courantes.


## Architecture du parcours

```mermaid
graph LR
    A[Administration]
    S[Services & Daemons]
    H["Sécurité (host)"]

    A --> S --> H
    A --> H
    S --> H
```

L’ordre n’est pas strict, mais en pratique : on administre, on comprend les services, puis on durcit la machine.

---

## Vue d’ensemble

<div class="grid cards" markdown>

* :lucide-user-cog:{ .lg .middle } **Administration**

    ---

    Gestion des utilisateurs et groupes, permissions, sudo, tâches planifiées (cron), hygiène système et opérations courantes.

    **Objectif** : administrer proprement un Linux “comme en prod”.

    [:lucide-book-open-check: Accéder](./admin.md)

* :lucide-server:{ .lg .middle } **Services & Daemons**

    ---

    systemd, unités, démarrage/arrêt, dépendances, journaux, logs, supervision de base, diagnostic.

    **Objectif** : maîtriser ce qui tourne et comment le contrôler.

    [:lucide-book-open-check: Accéder](./services-daemons.md)

</div>

<div class="grid cards" markdown>

* :lucide-shield:{ .lg .middle } **Sécurité (host)**

    ---

    Pare-feu, anti-bruteforce, audit de durcissement, détection malware/rootkit. Approche en couches : réduire l’exposition, contrôler l’accès, surveiller, auditer.

    **Objectif** : sécuriser un hôte Linux de manière mesurable et maintenable.

    [:lucide-book-open-check: Accéder](./security/index.md)

</div>

---

## Synthèse “logique métier” (ce que tu dois retenir)

Tu peux voir Linux comme un triangle opérationnel :

* Administration : identité, droits, hygiène.
* Services : disponibilité, fonctionnement, logs.
* Sécurité : réduction du risque + détection + réaction.

Si une seule brique est faible, le système entier devient fragile. La progression du guide suit donc une logique “production”.

<br />