---
description: "Parcours d'Apprentissage Laravel : 3 projets complets pour maîtriser l'authentification et l'architecture."
tags: ["LARAVEL", "BREEZE", "JETSTREAM", "SANCTUM", "PROJETS"]
---

# Laravel Lab : Parcours d'Apprentissage

<div
  class="omny-meta"
  data-level="🟢 Débutant à 🔴 Avancé"
  data-version="1.0"
  data-time="Projets Pratiques">
</div>

!!! quote "La pratique comme moteur d'apprentissage"
    _La théorie est essentielle, mais c'est par la pratique que l'on forge une véritable expertise. Ce "Laravel Lab" est conçu comme un **parcours progressif en 3 niveaux**. Plutôt que d'apprendre des concepts isolés, vous allez construire trois projets complets, du plus simple (authentification classique) au plus complexe (API REST SaaS et Jeu Vidéo temps réel)._

Ce hub regroupe les trois projets majeurs du parcours Laravel. Chaque projet utilise une technologie d'authentification différente (Breeze, Jetstream, Sanctum) et introduit des concepts d'architecture de plus en plus avancés.

## Les 3 Niveaux du Parcours

<div class="grid cards" markdown>

-   :lucide-wind:{ .lg .middle } **Niveau 1 — Laravel Breeze**

    ---
    **Blog Éditorialiste Professionnel**  
    Découvrez les fondamentaux de Laravel avec une application classique. Gestion CRUD, rôles (Admin/Auteur), machine à états de publication et interface Blade simple. Idéal pour commencer.

    **Niveau** : 🟢 Débutant | **Phases** : 7

    [:lucide-arrow-right: Démarrer le Projet Breeze](./projet-breeze/index.md)

-   :lucide-plane-takeoff:{ .lg .middle } **Niveau 2 — Laravel Jetstream**

    ---
    **Plateforme SaaS Pentest (B2B)**  
    Passez à la vitesse supérieure. Architecture Multi-Tenancy (Teams), Authentification 2FA renforcée, génération de rapports PDF (DOMPDF) et intégration d'un Frontend moderne en Angular 21 + Signals.

    **Niveau** : 🟡 Intermédiaire à 🔴 Avancé | **Phases** : 8

    [:lucide-arrow-right: Démarrer le Projet Jetstream](./projet-jetstream/index.md)

-   :lucide-shield-check:{ .lg .middle } **Niveau 3 — Laravel Sanctum**

    ---
    **Dungeon RPG Temps Réel**  
    Maîtrisez les API REST pures. Authentification par Tokens API (Sanctum), logique de jeu vidéo complexe (Combat tour par tour, Leaderboard) et Frontend riche réactif (Angular Animations + Signals).

    **Niveau** : 🔴 Avancé | **Phases** : 8

    [:lucide-arrow-right: Démarrer le Projet Sanctum](./projet-sanctum/index.md)

</div>

## Architecture de Progression

Le schéma ci-dessous illustre l'évolution de vos compétences à travers les trois projets :

```mermaid
graph TB
    subgraph Niveau 1 : Fondamentaux
        B[Projet Breeze<br/>Blog Éditorial]
        B1(Session Auth)
        B2(Blade UI)
        B3(CRUD & Policies)
        B --> B1 & B2 & B3
    end
    
    subgraph Niveau 2 : Architecture SaaS
        J[Projet Jetstream<br/>Plateforme Pentest]
        J1(Teams & 2FA)
        J2(Angular Signals)
        J3(Multi-Tenancy)
        J --> J1 & J2 & J3
    end
    
    subgraph Niveau 3 : API First
        S[Projet Sanctum<br/>Dungeon RPG]
        S1(Token Auth)
        S2(API REST)
        S3(Logique Jeu Avancée)
        S --> S1 & S2 & S3
    end
    
    B ===> J
    J ===> S
    
    style B fill:#e1f5e1
    style B1 fill:#e1f5e1,stroke-dasharray: 5 5
    style B2 fill:#e1f5e1,stroke-dasharray: 5 5
    style B3 fill:#e1f5e1,stroke-dasharray: 5 5
    
    style J fill:#fff4e1
    style J1 fill:#fff4e1,stroke-dasharray: 5 5
    style J2 fill:#fff4e1,stroke-dasharray: 5 5
    style J3 fill:#fff4e1,stroke-dasharray: 5 5
    
    style S fill:#ffe1e1
    style S1 fill:#ffe1e1,stroke-dasharray: 5 5
    style S2 fill:#ffe1e1,stroke-dasharray: 5 5
    style S3 fill:#ffe1e1,stroke-dasharray: 5 5
```

!!! tip "Recommandation"
    Même si vous avez déjà des bases en Laravel, il est fortement conseillé de suivre les projets **dans l'ordre**. Le projet Jetstream s'appuie sur des concepts vus dans Breeze, et le projet Sanctum pousse la logique API REST encore plus loin.
