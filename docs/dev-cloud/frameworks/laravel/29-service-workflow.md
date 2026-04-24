---
description: "Structurer la logique métier et valider son flux de base de donnée."
icon: lucide/book-open-check
tags: ["LARAVEL", "SERVICE", "TRANSACTIONS", "LOGIC"]
---

# Le Service de Workflow

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Cerveau Externe : Modèle de la Class Service

Plutôt que d'inonder nos Controller, et les rendre illisibles avec des vérifications du type "Si ce post est validé à cause de ce Status mais qu'en plus il a un Titre qui n'est pas bon...", il est courant de créer un fournisseur indépendant.

```php title="app/Services/PostWorkflowService.php"
class PostWorkflowService
{
    // Ce code prend en amont l'article demandé ET l'Intervenant qui fait l'action.
    public function approve(Post $post, User $admin, ?string $adminNote = null): Post
    {
        // On effectue Nos REGLES METIERS avant toute choses 
        if (!$post->isSubmitted()) {
            throw new InvalidArgumentException("Seuls posts soumis sont valables");
        }

        // Transactions DB : Soit TOUT se valide et modifie à la seconde près, soit IL ANNULE TOUT !
        return DB::transaction(function () use ($post, $admin, $adminNote) {
            
            // LA BASE MYSQL FAIT LA MODIF !
            $post->update([
                'status' => PostStatus::PUBLISHED,
                'published_at' => now(),
                'admin_note' => $adminNote,
                'reviewed_by' => $admin->id,
            ]);

            // LA TRANSACTION PEUT ENVOYER LE MAIL ICI SANS PEUR QUE CA SE PERDE !
            // event(new PostPublished($post));

            return $post->fresh(); // ON RAFRAICHIT la MEMOIRE et on renvoie le modele à son Controller.
        });
    }
}
```

Et pour cause, l'intêret de procéder par ce Cerveau Externe est sa ré-utilisation. Souvenez-vous pour qu'un Auteur Soumette, qu'un Boss Décide, ou Annule, ou Re-Corrige.

```php title="app/Services/PostWorkflowService.php"
// A METTRE DANS LA MEME CLASSE QU'AU DESSUS !
public function reject(Post $post, User $admin, string $reason): Post
{
    // Ne peut empecher un article d'être publié que s'il est au statut SOUMIS !!
    if (!$post->isSubmitted()) { throw new InvalidArgumentException("Refusé"); }
    
    // Le boss n'a même pas mit de laison a son refus !? 
    if (empty(trim($reason))) { throw new InvalidArgumentException("Raison Obligatoire !!"); }

    return DB::transaction(function () use ($post, $admin, $reason) {
        $post->update([
            'status' => PostStatus::REJECTED,
            'rejected_at' => now(), // C'est lui qui prend le chrono !
            'admin_note' => $reason,
            'reviewed_by' => $admin->id,
        ]);
        return $post->fresh();
    });
}
```

<br>

---

## 2. Controller Exécutif (La Main d'Œuvre)

Ce contrôleur gèrera le coté Modérateur (Admin) depuis son panneau central de l'Application sans avoir à réfléchir aux regles de sécurités qui bloquent en fond du Script de Base de donnée ! 
*(Et pourtant rappelez-vous que tout ça est enrobé de Middlewares sur vos URLs dans web.php afin d'être sur des routes inaccessibles pour rappel !!)*

Il n'y a plus aucune charge mentale sur son script !

```php title="app/Http/Controllers/Admin/PostController.php"
class PostController extends Controller
{
    // Injection du Parametre "Cerveau EXTERNE" !!
    public function __construct(private PostWorkflowService $workflowService) {}

    // 1- L'Admin arrive sur son Panel... On lui ressort les posts des Auteurs (submitted)
    public function pending()
    {
        $this->authorize('admin'); // Policy Global Admin !
        // Le ::submitted() est reconnu car nous avons le Scope Filtré implémenté precedemment !
        $posts = Post::submitted()->latest('submitted_at')->paginate(20);
        return view('admin.posts', compact('posts')); // Vous listez cette vue comme désiré.
    }

    // 2- L'admin CLIQUE sur le Formulaire "ACCEPTER L'ARTICLE" /approve d'un post
    public function approve(Request $request, Post $post)
    {
        $this->authorize('approve', $post); // Policy
        $this->workflowService->approve($post, user(), $request->validate(['admin_note' => 'nullable|string']));
        
        return redirect()->route('admin.posts.pending');
    }

    // 3- L'admin CLIQUE sur le Formulaire "REFUSER L'ARTICLE" /reject d'un post
    public function reject(Request $request, Post $post)
    {
        $this->authorize('reject', $post); // Policy
        $this->workflowService->reject($post, user(), $request->validate(['reason' => 'required|string']));
        return redirect()->route('admin.posts.pending');
    }
}
```

<br>

---

## Conclusion

Ce Service et son Exécutif valident pour de bons les états par de puissantes Transactions Sécurisant la moindre des informations requiertes et temporelles.

Il pourrait être intéressant de pousser un dernier concept de sécurité concernant la mécanique de validation des champs, que vous avez très certainement l'habitude d'écrire en `$request->validate()` avec d'infinies variables dans tous vos Controller métiers pour tout et n'importe quoi...  Nous parlerons de ça avec la composante Fichiers qui sont une menace absolu pour la sécurité d'un site.
