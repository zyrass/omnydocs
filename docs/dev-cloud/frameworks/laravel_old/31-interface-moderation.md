---
description: "Mettre en pratique les éléments destructeurs et conclure par l'Auto Évaluation du module."
icon: lucide/book-open-check
tags: ["LARAVEL", "WORKFLOW", "SUMMARY"]
---

# Confirmations & Bilan

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="1 Heure">
</div>

## 1. Exercice de Synthèse

Il ne reste plus que l'aspect de Destructions et des soumissions d'États de cet énorme morceau en guise d'Exercice final ! 

Toute validation ou toute destruction de status dans un projet s'accompagne à **100% de modal de confirmation en JS**, à défaut de vous casser les dents dans le Controlleur si le Javascript Front n'est pas votre force, voici comment créer la route manuelle d'une validation d'États pour votre Utilisateur via Controller !

1. Faire une Vue spéciale de confirmation de soumission de post de Brouillon : La case doit être obligatoire Front et Back ! (Indice: Un Helper et Model est nécéssaire pour tracker en un éclair qu'il ne se mangera plus cette vue s'il a déjà validé une fois le boucan... Il n'est pas stupide).
2. Ce même Controlleur doit posséder la fonction qui envoie définitivement en attente la page.

<details>
<summary>Solution</summary>

```html title="resources/views/posts/confirm-submit.blade.php"
@error('confirm_first_submission')
    <p style="color: red;">{{ $message }}</p>
@enderror

<form method="POST" action="{{ route('posts.submit', $post) }}">
    @csrf
    <input type="checkbox" name="confirm_first_submission" required>
    <button type="submit">Confirmer la soumission</button>
</form>
```

```php title="app/Http/Controllers/PostController.php"
// Route vers : posts/confirm  = confirm()
public function confirm(Post $post)
{
    // Ce mec a posté plus de d'un article à son actif. Pas bésoin de le harceler avec l'aide d'interface.
    if (user()->has_submitted_post) { return null; }
    
    return view('posts.confirm-submit', ['post' => $post]);
}

// Route POST vers : posts/submit = submit()
// Il recevra donc la methode POST de notre VIEW plus haut.
public function submit(Request $request, Post $post)
{
    $this->authorize('submit', $post); // Toujours..
    
    // Si c'est un ptit nouveau.
    if (!user()->has_submitted_post) {
        $request->validate(['confirm_first_submission' => ['required', 'accepted']]);
        
        user()->update(['has_submitted_post' => true]); // Devient un Ancien via model Track BDD !
    }
    
    // Le Service Cerveau de la page précedente fait l'Etat Soumis de Base de donnees !
    $this->workflowService->submit($post, user()); 
    return redirect()->route('posts.show', $post);
}
```

</details>


<br>

---

## 2. Checkpoint Auto-Évaluation du Module 6

Afin de valider correctement ce gros module conceptuel et de terminer la logique métier brute, veuillez vous exercer une dernière fois sur les concepts avancés d'architecture de PHP :


1. **Question :** Pourquoi déporter des règles métiers de controller dans un fichier FormRequest unique et personnalisé ?
   <details>
   <summary>Réponse</summary>
   A mesure que votre produit grandit, sémantiquement les conditions ne peuvent pas se balader partout dans tous les contrôlleurs métiers, elles doivent être classées proprement. Créer un StoreFileRequest, un LoginAdminRequest vous assure une séparation des contraintes et un Code "DRY" sur tous les processus qui le requiert.
   </details>

2. **Question :** Pouvez-vous expliquer le but des DB transanctions lors des écritures ?
   <details>
   <summary>Réponse</summary>
   Les DB Transactions sont le garant de l'atomicité des fichiers : Ou soit tout se passe sans encombres durant les longues secondes d'écritures de la fonction Service, ou soit le script échoue sans laisser la moindre trace corrompue et revient à un état sécurisé. 
   </details>

3. **Question :** Une méthode de Controller peut-elle envoyer le Mail d'aussitôt et comment un Controller doit interragir avec les validations d'un Modèle ?
   <details>
   <summary>Réponse</summary>
   Si l'application est complexe (Soumission sur plusieurs tables, etats et validations), non. C'est l'essence de l'Exercice du "Service". Le Service fait les calculs du cerveaux, le Controller ne fait qu'indiquer la porte (`Approve()`).
   </details>

<br>

---

## Conclusion Générale du Module

!!! quote "Récapitulatif"
    Ce module d'Architecture représente la finalité et les plafonds que vous atteindrez systématiquement dans vos métiers. Transformer l'Information pour éviter un CRUD basique. La refonte via un **système de publication professionnel** avec workflow de validation, règles métier complexes, et gestion d'images est la fondation finale.


Ce pattern est universel dans les applications d'entreprise : Pensez-le comme un gestionnaire de commandes e-commerce, un système de support tickets clients...

Vos fondations sont posées... Mais une chose vous turlupine... Écrire un système de validation de Login ou de Register ou vous devrez tester des mot-de phrases par regex, lier des tables de profils manuellement... Il doit ben exister un Starter-Kit et un "Boilerplate" ? 

Oui. Les Automatisations existent sur ce Framework pour effacer de votre esprit les Modules de l'Auth vu précédemment et de le refondre avec aisance grace au package : **Laravel Breeze**.
