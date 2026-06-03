---
description: "Laravel Sanctum — Projet guidé API pure. Authentification stateless par Personal Access Tokens, API RESTful complète, déploiement production sur VPS. 8 phases progressives."
icon: lucide/book-open-check
tags: ["LARAVEL", "SANCTUM", "API", "TOKENS", "REST", "PROJET GUIDÉ"]
---

# Projet Sanctum — API RESTful Pure & Stateless

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="Laravel 11"
  data-time="~10 Heures">
</div>

## Introduction

!!! quote "Qu'est-ce que ce projet ?"
    **Laravel Sanctum** en mode API Pure est le pattern d'architecture pour les applications qui séparent complètement le backend (Laravel API) du frontend (Angular, React, application mobile). Contrairement au mode SPA (cookies de session), ce mode utilise des **Personal Access Tokens** — chaque requête doit transporter son token dans le header `Authorization: Bearer`.

Ce projet guidé construit une **API de gestion de ressources** consommable par n'importe quel client : une application Angular, une app mobile Swift, ou un outil CLI.

<br>

---

## Architecture du Projet

```mermaid
flowchart LR
    classDef phase fill:#d1e7dd,stroke:#198754,color:#000
    classDef client fill:#cce5ff,stroke:#0d6efd,color:#000

    subgraph Backend["Backend Laravel (ce projet)"]
        P1["Phase 1\nInstall API"] --> P2["Phase 2\nBDD"]
        P2 --> P3["Phase 3\nMétier"]
        P3 --> P4["Phase 4\nSanctum Auth"]
        P4 --> P5["Phase 5\nEndpoints REST"]
        P5 --> P6["Phase 6\nFonctionnalités+"]
        P6 --> P7["Phase 7\nTests API"]
        P7 --> P8["Phase 8\nDéploiement"]
    end

    subgraph Clients["Clients consommateurs"]
        C1["Angular SPA"]
        C2["App Swift iOS"]
        C3["Client CLI"]
    end

    Backend -->|"JWT Token"| Clients

    class P1,P2,P3,P4,P5,P6,P7,P8 phase
    class C1,C2,C3 client
```

<br>

---

## Prérequis

!!! info "Prérequis recommandés"
    - ✅ Maîtriser les Relations Eloquent (module 16)
    - ✅ Avoir lu le module API et Sanctum (module 42)
    - ✅ Connaître les Form Requests (module 12)
    - ✅ Notions de base en Queues (module 41)
    - ✅ Un client HTTP installé (Postman, Hoppscotch, Bruno)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Ce projet vous enseigne la compétence la plus demandée du marché Laravel : **concevoir et livrer une API REST professionnelle**. Au terme de ces 8 phases, vous serez capable de construire un backend que n'importe quel frontend peut consommer — Angular, React, Vue, Swift, ou Flutter. C'est l'architecture qui alimente tous les projets modernes découplant le front du back.

> [Commencer : Phase 1 — Installation API Laravel + Sanctum →](./01-phase1.md)
