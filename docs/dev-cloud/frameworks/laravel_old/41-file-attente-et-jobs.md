---
description: "Gérer l'impact asynchrone des tâches lentes de votre serveur PHP avec les Jobs."
icon: lucide/book-open-check
tags: ["LARAVEL", "QUEUES", "JOBS", "ASYNC"]
---

# File d'Attentes & Tâches (Queues)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>


## 1. La Problématique du Bloquant

Les opérations lentes bloquent l'utilisateur et l'expérience en devient un véritable chargement perpétuel. L'image de chargement qui ne part pas à cause d'un Mail à envoyer en validant le formulaire...

```php
// VULNÉRABLE : Utilisateur attend longtemps avant le "Redirect()" de fin ! 
public function store(Request $request) {
    $post = Post::create($request->validated());
    
    Mail::to($post->user)->send(new PostCreated($post)); // LENT : Envoyer un mail : 2s d'API.
    $this->generateThumbnail($post); // TRES LENT : Générer la photo de profil : 3s 
    
    // REDIRECTION SEuLEMENT APRES 5 secondes ! L'USER a fermé votre page il croyait ca Buggé.
    return redirect()->route('posts.show', $post); 
}
```

La solution des **Queues** en asynchrone pour les workers vous sauvera la vie. C'est l'équivalement d'avoir un sous traitant magique qui prendra son temps, après avoir répondu à votre client Web !

```php
// RAPIDE : Utilisateur redirigé immédiatement
public function store(Request $request) {
    $post = Post::create($request->validated());
    
    // Dispatch jobs en arrière-plan à notre Esclave local serveur.
    ProcessNewPost::dispatch($post);
    
    return redirect()->route('posts.show', $post); // Instantané !
}
```

<br>

---

## 2. Le Job et le Background Processing

L'Action en question de "ProcessNewPost" est à configurer de votre coté dans un bloc PHP qu'on appelle "Job" via les commandes artisanales de Laravel.  (`artisan make:job`). 

```php
class ProcessNewPost implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;
    
    public function __construct(public Post $post) {}
    
    public function handle(): void
    {
        // Ces opérations s'exécutent en arrière-plan LENTEMENT et TRanQUILLEMENT.
        Mail::to($this->post->user)->send(new PostCreated($this->post));
        $this->generateThumbnail();
    }
}
```

Pour que ce job soit géré, le Serveur lui devra lancer un deamon d'écoute (Un programme infini tournant sur votre Linux VPS Cloud), `php artisan queue:work` afin qu'il dépile la base de donnée "jobs" dans laquelle votre Front envoi des informations. Cela demande souvent des configurations comme Supervisor ou Redis, que nous aborderons dans les cours d'Infrastructure ! 

Il existe un paquet pour voir toutes les executions en temps réel du terminal, sur un très joli dashboard en noir : **Laravel Horizon** (`composer require laravel/horizon`). A tester absolument en développement Local ou Production.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les queues sont le levier de performance le plus impactant d'une application Laravel en production. Chaque opération qui n'a pas besoin d'un résultat immédiat pour l'utilisateur — envoi d'email, traitement d'image, génération de PDF, appel d'API externe — doit être déportée en file d'attente. C'est la différence entre une application qui répond en 200ms et une qui fait attendre l'utilisateur 3 secondes.

> [Queues maîtrisées. Exposez maintenant votre application via une API Sanctum →](./42-api-et-sanctum.md)
