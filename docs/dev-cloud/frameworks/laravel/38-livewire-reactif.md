---
description: "Débuter les concepts de requetage dynamique avec le Framework en temps réel Backend"
icon: lucide/book-open-check
tags: ["LARAVEL", "LIVEWIRE", "FRONTEND", "REACTIVE"]
---

# L'Architecture Côté Serveur (Livewire)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. La Révolution Livewire

C'est là que l'Ecosystème Laravel est fascinant. Qu'avez vous retenu de l'architecture traditionnelle MVC pour créer une Feature PHP Dynamique dans ces modules ?
* "Il faut faire un Controller avec ses fonctions",
* "Une page Blade qui affiche le retour des Models",
* "Déclarer la route Manuelle Web de ses 2 Elements avec POST/GET...",
* "Mettre du Javascript pour écouter le clic AJAX Fetch s'il y a un tableau et appeler la route de requete..."

Oubliez, la pile **Livewire (L)** écrase ce concept si nécessaire. C'est un framework qui mix en direct les **composants dynamiques** que gère PHP avec les données, sans écrire de JavaScript et SANS RECHARGEMENT !! (`F5`).

D'un bloc d'action dans le terminal :
```bash
php artisan make:livewire SearchPosts
```

La magie crée et auto-lie la Vue au Compte-Goutte de son propre Class Controller sans faire de route HTTP : `app/Livewire/SearchPosts.php` & `resouces/views/livewire/search-posts.blade.php`.

Son comportement dans la base de Laravel va écouter le navigateur et injecter des petits scripts AJAX Javascript tout seuls pour renvoyer le Controlleur à chaque fois sans refraichir le Nav, et remplacer (Morpher) l'Html du composant sans sourciller au sein de la page Mere. Le SEO Google Index reconnait aussi la page (Ce que des outils lourds comme React rendent opaque car construit 100% sur du coté ordinateur) !

<br>

---

## 2. Le Flow de Requête Moderne sans JS !

Etudions notre propre moteur de recherche asynchrone fait sans Javascript avec ce Livewire.

```php title="app/Livewire/SearchPosts.php"
class SearchPosts extends Component
{
    // Ce paramètre sera mis en 'Bind' Data coté HTML magiquement !!!
    public $searchString = '';

    // Ce qu'il injecte à chaque touche tapé et re-injecte dans le composant de sa vue (render())
    public function render()
    {
        // 1- Requète BDD Normale
        $postsList = Post::query()
            // 2- Si On Tape quelque chose et que the '$searchString' est mis à jour depuis le HTML ??
            ->when($this->searchString, function ($query) {
                // 3 - On envoie la recherche !!
                $query->where('title', 'like', "%{$this->searchString}%");
            })
            ->latest()->take(10)->get();

        return view('livewire.search-posts', ['postsList' => $postsList,]);
    }
}
```

Du coté d'intégration de n'importe quel de nos pages actuels `views/dashboard.blade.php`, on appel `<livewire:search-post />`. En voici son contenant à l'intérieur :

```html title="resources/views/livewire/search-posts.blade.php"
<div>
    <!-- MAGIE LIVEWIRE FRONT: Wire:Model -->
    <!-- .live va recharger en AJAX sous le capot à chaque fois qu'on tape dans l'input (Remplir $searchString avec le temps réel du php) ! -->
    <input type="text" wire:model.live="searchString">

    <div class="mt-4 space-y-2">
        <!-- MAGIE LIVEWIRE PHP : IL RELOAD CE FOREACH a CHAQUE FRAPPE DE LETTRE de maniere asynchrone DB !! -->
        @forelse ($postsList as $post)
            <div class="border p-4 rounded">
                <h3 class="font-bold">{{ $post->title }}</h3>
            </div>
        @empty
            <p>Aucun résultat trouvé pour votre recherche.</p>
        @endforelse
    </div>
</div>
```

Finis les route HTTP et Controller manuels. Finis le Jquery Ajax à maintenir. Bienvenu dans le Backend Reactif que l'on appelle communémant "S.S.R" (Server Side Rendering). 


### Mais Livewire Peut Il Gérer et Capter les Actions Utilisateur comme JS ?

Lui aussi pocède un arsenal de directive. Pas des `x-` comme *AlpineJS*, mais des `Wire:` qui vont recompiler la page asynchrone...

Et on peut ainsi appeler le Controller PHP En direct.. Pas besoin de Formulaires HTML !
`<button wire:click="NomDeMaMethodePhp()"> Sauvegarder dans MYSQL (Il fait un $this->validate() derrière, et c'est valid !) </button>`.

Vous avez les armes pour vos propres requetes. Mais c'est une toute autre mentalité qu'il faudrait pour maitriser la Stack TALL et le composant Livewire qui ferait l'Objet à lui seul d'une Documentation géante. Passons au bilan et conclusion.
