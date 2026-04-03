---
description: "Régler les problématiques de commentaires multiples par Ownership, et conclure par une évaluation des permissions d'une grande application."
icon: lucide/clipboard-check
tags: ["LARAVEL", "EXERCICE", "OWNERSHIP"]
---

# Bilan & Exercice

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Exercice de Synthèse (Modération Double)

**Voici un Cas typique du Web d'aujourd'hui :**
* Tout compte `Users` peut Commenter. 
* Un compte peut supprimer et modifier ses propres commentaires. 
* Un Administrateur peut tout raser. **Jusqu'à là, on a les outils : Facile avec Ownership + Bypass.**

* **Cas Complexe :** L'Auteur du Post à l'autorité pour supprimer les commentaires que les Internautes lui ont adressés, même s'il n'est pas Admin du site ! Il gère sa section commentaires.

Comment procéderiez-vous sur le Modele Commentaire pour bloquer la route `$this->authorize('delete', $comment);` ?

<details>
<summary>Spoiler et Explication de Policy Complexe de suppression</summary>

```php
class CommentPolicy
{
    public function delete(User $user, Comment $comment): bool
    {
        if ($user->isAdmin()) { return true; } // Admin tout permis !
        
        if ($user->id === $comment->user_id) { return true; } // Le créateur du message le regrette et le supprime de sa volonté.
        
        // ET FINALEMENT L'ASTUCE METIER COMPLIQUEE !
        if ($user->id === $comment->post->user_id) { return true; } // (Le post relié à ce com' a un créateur ! Et ce créateur c'est moi : Clic Poubelle ! )

        return false;
    }
}
```
</details>

<br>

---

## 2. Checkpoint Auto-Évaluation du Module 5

Afin de valider correctement le fonctionnement Autorisation / Authentification, pouvez-vous répondre à ces questions :


1. **Question :** On vous demande de coder une "Policy", mais en reprenant nos analogies depuis le précédent module, et en les vulgarisant : Quelle ligne sépare une Authentification à une Autorisation ? Gate à une Policy ?
   <details>
   <summary>Réponse</summary>
   * **Authentification** : "Qui es-tu ?", "Montres ton Badge / Ouvre une Session".
   * **Autorisation / Gate** : L'Intelligentie Artificielle du bâtiment ! "Tu peux aller pisser ? Je te passe en True. Tu veux aller dejeuner à la cantine en étant dans ta période Stagiaire ? "Je te passe en False ou retourne un Fatal 403". C'est **Global**.
   * **Policy** : Le Videur du Box ou tu ranges tes documents privés. "Ces dossiers portent l'ID 1. Ton Badge dit ID 5 ? Je te recale, ce n'est pas ta ressource". C'est **Pointu Modèle et Ownership**.
   </details>

2. **Question :** Le Modele Policy est magique parce qu'on ne l'associe pas d'ordinaire dans les fichiers de services, tout se lit tout seuls par le Framework (Laravel > 11). Comment contourner ses dizaines de conditions en une ligne pour un SUPER_ADMIN dans un modèle ModèlePolicy sans avoir à inscrire dans toutes les fonctions `IF Admin return true;` ?
   <details>
   <summary>Réponse</summary>
   Rappel de la méthode `before(User, actions... )` : Exécutée AVANT toute autre méthode par Laravel pour la Policy du modele de cette ressource particuliere. S'il dit `true`, tout passe (Bypass). 
   </details>

3. **Question :** Le Frontend permet il avec la norme `Gate` de cacher ou griser des boutons sensibles tel qu'une suppression ?
   <details>
   <summary>Réponse</summary>
   OUI ! C'est ce qui le rend performant et transparent. `@can('delete', $post) CODE DU BOUTON @endcan`
   </details>

<br>

---

## Conclusion Générale du Module

!!! quote "Récapitulatif"
    **L'autorisation** est la seule couche de sécurité qui détermine ce que chacun peut faire. Sans elle un utilisateur authentifié de l'extérieur est un roi parmis les loups. Modifier les posts des autres, voler des profils, taper des requêtes POST de destructions administratives sur son navigateur...

Ce système est fondamental mais basique. Nous le faisons à la main par étape successive pour la Masterclass. Dans le monde réél ce profilage porte un nom : **L'Architecture Role-Based Access Control (RBAC)**.
Pour des applications d'entreprise (Rôles multiples, équipes, sous-traitants, abonnés), la plomberie devient infernale à gérer via des `Middlewares Array`. Vous utiliserez des gros paquets (Packages) comme **Spatie Laravel Permission** ou **Bouncer**. Et nous les introduirons aux prochains Modules pour l'Industrialisation de nos codes !

Nous allons basculer ce code de sécurité à une réalité métier avec un Workflow Editorial complexe !
