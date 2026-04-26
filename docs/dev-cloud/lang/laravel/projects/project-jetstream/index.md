---
description: "Laravel Jetstream — Projet guidé avancé. Authentification multi-teams, 2FA, profil complet, API Sanctum et interface Livewire ou Inertia. 8 phases pour une plateforme SaaS."
icon: lucide/book-open-check
tags: ["LARAVEL", "JETSTREAM", "TEAMS", "2FA", "SANCTUM", "PROJET GUIDÉ"]
---

# Projet Jetstream — Plateforme SaaS Multi-Teams

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="Laravel 11"
  data-time="~12 Heures">
</div>

## Introduction

!!! quote "Qu'est-ce que ce projet ?"
    **Laravel Jetstream** est le kit d'authentification avancé de Laravel. Il va bien au-delà de Breeze en incluant nativement : **Teams** (multi-tenant), **2FA** (authentification à deux facteurs), **API tokens (Sanctum)**, **gestion de profil complète**, et le choix entre Livewire ou Inertia.js pour le frontend.

Ce projet guidé simule la construction d'une **plateforme de gestion de missions Pentest** en mode SaaS multi-équipes — un cas d'usage réel et représentatif des applications Jetstream en production.

<br>

---

## Architecture du Projet

```mermaid
flowchart LR
    classDef phase fill:#fff3cd,stroke:#ffc107,color:#000

    P1["Phase 1\nInstallation + Teams"] --> P2["Phase 2\nModèles + Migrations"]
    P2 --> P3["Phase 3\nLogique Métier"]
    P3 --> P4["Phase 4\nAuth + Policies"]
    P4 --> P5["Phase 5\nAPI REST"]
    P5 --> P6["Phase 6\nTemps Réel"]
    P6 --> P7["Phase 7\nOptimisation"]
    P7 --> P8["Phase 8\nTests + Déploiement"]

    class P1,P2,P3,P4,P5,P6,P7,P8 phase
```

<br>

---

## Prérequis

!!! warning "Ce projet est avancé"
    - ✅ Maîtriser les projets Breeze (Phases 1-7)
    - ✅ Connaître les Policies et le RBAC (modules 24-26)
    - ✅ Avoir lu les modules Services et State Machine (28-29)
    - ✅ Connaître les bases des Queues (41)
    - ✅ Node.js + Redis installés

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Jetstream est la référence pour les applications Laravel en production avec des besoins d'authentification avancés. La complexité de sa configuration initiale est compensée par la richesse des fonctionnalités livrées clé en main. Ce projet vous confrontera aux défis réels d'un SaaS : isolation des données par tenant, gestion des droits multi-niveaux, et scalabilité. C'est le projet le plus proche d'une application professionnelle réelle.

> [Commencer : Phase 1 — Installation Jetstream + Teams →](./01-phase1.md)
