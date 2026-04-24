---
description: "Présentation détaillée de Laravel Jetstream : L'arsenal avancé pour les applications SaaS."
icon: lucide/book-open-check
tags: ["LARAVEL", "AUTH", "JETSTREAM", "SAAS", "TEAMS", "2FA"]
---

# Laravel Jetstream

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Laravel 11"
  data-time="Théorie">
</div>

!!! quote "Le moteur des professionnels"
    Si *Laravel Breeze* est un vélo léger et maniable, **Laravel Jetstream** est un avion de ligne commercial. Jetstream est un starter kit massif conçu pour équiper immédiatement votre nouvelle application de fonctionnalités "Entreprises" : Authentification à deux facteurs (2FA), gestion d'équipes (Teams), gestion de session de navigateurs et jetons d'API (Tokens). 

<br>

---

## 1. À quoi sert Jetstream ?

Jetstream encapsule la logique métier la plus complexe des applications SaaS modernes afin que vous n'ayez pas à l'inventer de zéro. Il repose en arrière plan sur un puissant package appelé **Laravel Fortify** (le moteur sous le capot). 

### Quand utiliser Jetstream ?
- Pour des **applications SaaS** (Software as a Service) massives qui nécessitent la création de "Groupes" (Gestion de Teams).
- Si votre cahier des charges exige une exigence de sécurité élevée immédiate (2FA, déconnexion des sessions distantes).
- Si vos utilisateurs ont besoin de générer des clés d'API dans leur profil pour connecter des services tiers.

!!! warning "La complexité"
    Contrairement à Breeze où tout le code source est visible dans vos dossiers `app/Http/Controllers`, Jetstream **cache** sa logique au sein du dossier `vendor/` (Moteur Fortify). La personnalisation de la logique (Login, Inscription) ne se fait donc pas en touchant des contrôleurs de base, mais en passant par le fichier `FortifyServiceProvider` et les actions (Dossier `app/Actions`). Le niveau requis est donc très élevé.

### Les choix technologiques front-end
Jetstream est plus restrictif que Breeze concernant le frontal graphique, car il génère des tableaux de bord interactifs complexes.
1. **Livewire** (avec des composants Blade natifs).
2. **Inertia.js avec Vue** (Uniquement Vue, React n'est pas le standard historique ici).

<br>

---

## 2. Diagramme d'architecture Jetstream (Moteur Fortify)

Voici l'architecture technique qui sépare le Frontend généré par Jetstream, du Backend propulsé par Fortify.

```mermaid
graph TD
    User(("Utilisateur")) -->|Interagit| JS[Interface Jetstream]
    
    subgraph Frontend [Vues Publiées (Livewire/Vue)]
        JS --> UI_Profile(Gestion de Profil / 2FA)
        JS --> UI_Teams(Gestion des Équipes & Rôles)
        JS --> UI_API(Gestion des Tokens API)
    end
    
    subgraph Backend [Logique Cachée (Vendor : Fortify)]
        UI_Profile --> F_Auth(Authentification)
        UI_Teams --> F_Reg(Inscription / Teams)
        UI_API --> SL_Sanctum(Création Jetsons)
    end
    
    subgraph Actions [Logique Mutable (Votre Code)]
        F_Reg --> A_CreateTeam(Action: CreateNewUser)
        F_Auth --> A_Update(Action: UpdateProfileInformation)
    end
```

_Le schéma souligne que les interfaces (UI) communiquent d'abord avec le pont `vendor` (Fortify), qui redescend parfois appeler les fichiers générés dans votre dossier `app/Actions` pour vous laisser le contrôle final de la création._

<br>

---

## Conclusion et mise en pratique

!!! quote "Le marteau-piqueur n'est pas là pour enfoncer un clou"
    L'erreur la plus commune des développeurs intermédiaires est d'installer Jetstream pour créer un simple "Blog". Cette sur-ingénierie entraîne l'installation de centaines de fichiers inutiles et d'une dette technique liée à Fortify. **Utilisez Jetstream pour ce pourquoi il a été conçu : propulser une startup Tech qui veut facturer des abonnements en groupe !**

> **Curieux de voir la bête en action ?**  
> Retrouvez la mise en place d'outils massifs sur le terrain directement dans notre [Lab Laravel](../../projets/laravel-lab/).

<br>