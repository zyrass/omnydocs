---
description: "Application pratique de vos connaissances en Eloquent ORM."
icon: lucide/clipboard-list
tags: ["LARAVEL", "PRATIQUE", "EXERCICE", "BILAN"]
---

# Bilan BDD & Mini-Projet

<div
  class="omny-meta"
  data-level="🔵 Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Exercice pratique : Un système de tickets de SAV

Pour valider vos acquis, vous allez concevoir depuis zéro un CRUD permettant à des utilisateurs d'ouvrir des "Tickets" de demande de maintenance. Un ticket possède plusieurs commentaires qui lui sont assignés.

1. Initier un modèle `Ticket` associé avec son Controller Resources et les Migrations (`-mcr`)
2. Le ticket requiert la clef User qui l'a posé, le `Sujet`, et le Status du Ticket `resolu / non-resolu`.
3. Initier un Modéle enfant (HasMany) via un modèle `Commentaire`
4. Réunir l'ensemble dans une route Controller pour afficher toutes ces informations liées (`with()`) en respectant la boucle anti-N+1 en `EagerLoading`. 
5. Les commenter via interface Blade.

> La correction sans le code pure front-end blade (par déduction) est disponible ci-dessous si les concepts de relations flousses.

### 1.1 Solution Déclarative

```bash
php artisan make:model Ticket -mcr
php artisan make:model Comment -m
```

```php title="database/migrations/..._tickets_table.php"
// Migrations
public function up()
{
    Schema::create('tickets', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->string('subject');
        $table->boolean('resolved')->default(false);
        $table->timestamps();
    });
}
```

### 1.2 Solution Relationnelle (Model)

```php title="app/Models/Ticket.php"
// Modèle Ticket
class Ticket extends Model
{
    protected $fillable = ['subject', 'resolved', 'user_id'];

    public function user() {
        return $this->belongsTo(User::class);
    }
    public function comments() {
        return $this->hasMany(Comment::class);
    }
}
```

```php title="app/Models/Comment.php"
// Modèle Comment
class Comment extends Model
{
    protected $fillable = ['body', 'ticket_id', 'user_id'];

    public function ticket() {
        return $this->belongsTo(Ticket::class);
    }
    public function user() {
        return $this->belongsTo(User::class); // Celui qui poste la reponse
    }
}
```

### 1.3 Solution Transitive (Controller)

```php title="app/Http/Controllers/TicketController.php"
public function show(Ticket $ticket)
{
    // On repaire le ticket Injectée via URL Binding.
    // Et on force la relation sur une variable pour tout remonter coté Blade Front-end !
    $ticket->load('comments.user'); // Eager loading pour le ticket unique via méthode load (Car pas de with possible sur un item Binding injecté)
    return view('tickets.show', compact('ticket'));
}
```

<br>

---

## 2. Quiz d'auto-évaluation 

Avant de quitter le Module 3, validez ces points :

1. **Question :** Quelle est la différence entre `find()` et `findOrFail()` ?
   <details>
   <summary>Réponse</summary>
   `find()` retourne `null` si l'enregistrement n'existe pas. `findOrFail()` lève une exception `ModelNotFoundException` (Erreur 404 automatique géré par l'infrastructure pour l'utilisateur).
   </details>

2. **Question :** Qu'est-ce que le problème de Boucle N+1 ?
   <details>
   <summary>Réponse</summary>
   Exécuter N requêtes supplémentaires base de données à chaque tour de paramètre dans une boucle "Foreach", au lieu de charger toutes les relations en 1 seule requête globale de matrice préparatoire avec `with()`.
   </details>

3. **Question :** Comment protéger les modifications directes via variable `create()`  ?
   <details>
   <summary>Réponse</summary>
   `protected $fillable` définit les colonnes autorisées pour l'assignation de masse au sein du model ciblé, protégeant contre l'injection de colonnes non désirées via requêtes web contrefaites.
   </details>

<br>

---

## Conclusion Générale du Module

!!! quote "Récapitulatif"
    Eloquent ORM transforme la manipulation de base de données d'une **corvée technique** en une **API élégante et expressive**. Vous avez maintenant les outils pour :
    - Structurer proprement votre schéma sans PHPMyAdmin.
    - Interroger la base de données sans écrire de SQL.
    - Modéliser des relations complexes entre entités.
    
    Ces concepts sont **universels** dans le développement POO MVC (Symfony etc).
    

**Prochaine étape :**  
Le **Module 4 - Authentification Custom** va vous apprendre à sécuriser votre application en créant un système d'authentification complet **à la main** (sessions, hashing, middlewares), avant d'utiliser les starter kits semi-automatiques.
