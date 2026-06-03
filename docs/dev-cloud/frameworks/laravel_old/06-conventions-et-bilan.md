---
description: "Les conventions strices imposées par le Framework et l'auto-évaluation."
icon: lucide/book-open-check
tags: ["LARAVEL", "CONVENTIONS", "BILAN"]
---

# Conventions & Bilan

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Conventions de nommage Laravel

Laravel impose des **conventions strictes** pour bénéficier de la magie de l'auto-découverte (Le Framework peut en déduire certaines actions sans nécessiter de long paramétrage).

| Élément | Convention | Exemple |
|---------|-----------|---------|
| **Controller** | PascalCase + "Controller" | `PostController`, `UserController` |
| **Modèle** | Singulier PascalCase | `Post`, `User`, `Comment` |
| **Table DB** | Pluriel snake_case | `posts`, `users`, `comments` |
| **Migration** | `create_xxx_table` | `2024_01_15_create_posts_table.php` |
| **Route nommée**| snake_case avec point | `posts.index`, `users.show` |
| **Méthode** | camelCase | `index()`, `showProfile()` |

### 1.1 Principe de responsabilité unique (Le S de SOLID)

**Un controller ne doit pas :**
- Contenir de logique métier complexe (à déplacer vers des Classes).
- Exécuter des requêtes SQL directes `DB::raw` (utiliser Eloquent `Post::find`).
- Gérer l'upload direct d'une Image.

**Un controller doit simplement être "L'Aiguilleur de la Route" :**
- Accepter et valider ce qu'il a reçu (la requête entrante).
- Engager le(les) Modèle(s) concerné(s).
- Rendre la page.

<br>

---

## 2. Quiz d'auto-évaluation des Fondations

Avant d'affronter la complexité du Module 2, validez les points suivants :

1. **Question :** Quel fichier sert de point d'entrée pour toutes les requêtes HTTP dans une installation par défaut ?
   <details>
   <summary>Réponse</summary>
   Le Front Controller `public/index.php`
   </details>

2. **Question :** Quelle commande Artisan va me créer en un coup le Modèle post, la Migration post, le Controller post, et la test Factory post ?
   <details>
   <summary>Réponse</summary>
   `php artisan make:model Post -mcrf`
   </details>

3. **Question :** Que fait la directive magique du moteur Blade `{{ $variable }}` ?
   <details>
   <summary>Réponse</summary>
   Elle affiche une variable tout en empêchant dynamiquement l'injection de code malveillant grâce au filtre anti-XSS natif.
   </details>

4. **Question :** Le projet "plante", je dois vérifier ma structure. Où regarder pour ajuster l'identifiant pour la communication avec ma Base de donnée ?
   <details>
   <summary>Réponse</summary>
   La réponse réside toujours dans le fichier caché `.env`
   </details>

<br>

---

## Conclusion Générale

!!! quote "Récapitulatif"
    Vous avez maintenant les **fondations solides** pour travailler avec Laravel. Vous comprenez comment le framework répartit spatialement son code métier (Le patron de conception Modèle/Vue/Contrôleur) et connaissez son cycle de vie. De plus le puissant CLI `php artisan` répond désormais à vos premiers ordres.
    
    Le meilleur moyen d'apprendre Laravel, c'est de **casser des choses**. Modifiez une route, supprimez une balise html vitale, et observez les messages écarlates de Laravel (Whoops/Ignition/Flare). Ses messages d'erreur sont **extrêmement performants** pour vous souligner votre erreur directement.

**Prochaine étape :**  
Dans le **Module 2**, nous explorerons comment des données dynamiques insérées par l'utilisateur transitent des pages web grâce au Route Model Binding et le cœur atomique des Controllers.
