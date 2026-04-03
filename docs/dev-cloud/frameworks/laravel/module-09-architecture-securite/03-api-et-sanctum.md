---
description: "Connecter son application Back-End a des systèmes Extérieurs (Mobile Flutter, VueJS...)"
icon: lucide/network
tags: ["LARAVEL", "API", "SANCTUM", "PASSPORT", "JETSTREAM"]
---

# Sanctum & API Tokens

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Créer une API Laravel (Sans Vue Front End)

Imaginez que ReactJS ou Flutter (Mobile), n'ont aucunes informations sur vos bases ni vos dossiers Laravel, puisqu'ils existent à par entière autre part ! Et Ils doivent afficher les POST de la base ! Alors ils attendent qu'une communication en format Brut (Un flux Texte JSON en l’occurrence) soient émit depuis votre serveur.

Ceci n'est que le rôle des **APIs**.

Si votre Route Web Classique retourne : `return view('dashboard', $post);` à une page Mobile... Il verra le code HTML. C'est absurde.
A l'inverse, l'API de Laravel (Géré dans le dossier des routes `/routes/api.php`) ne se servira que de cet élément formateur : `return response()->json(['post' => $post] )`.  Ce qui permet la lecture des variables brutes part le téléphone Mobile !


Mais comment le téléphone Mobile peut-il identifier qu'il est bien un "Utilisateur Existant" pour aller ajouter des Likes ? Laravel Sanctum et les Tokens ! 

<br>

---

## 2. Sanctum l'identificateur

**Sanctum : Qu'est-ce que c'est ?**
Laravel Sanctum fournit un système d'authentification léger pour se souvenir d'une trace d'un "Jeton texte" de la personne !   
(Alternativement à "Passeport" qui lui est destiné a un vrai OAUTH et jetons renouvenables).

1. L'application Flutter Mobile appelle la route de Laravel Api : `/api/login` (et lui transmet l'email et le password).
2. Laravel vérifie la BDD `users` et repond : "Oui tu es Alain ! Voici une chaine de charactère de 60 jetons (ton token personnel) pour cette session Mobile : garde la bien au chaud".
3. Le Flutter enregistre le token dans sa mémoire caché locale.
4. Au clic sur "Like" le post. Le Flutter re-balance une route vers `/api/like` et rajoute dans "Authorization header: Le Token XXXXX".
5. Laravel API vérifie avec **Sanctum** la base des Tokens. Valide sa provenance : Ouvre l'action.

```bash
composer require laravel/sanctum
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
php artisan migrate
```

Son implementation dans le controlleur "Emetteur" est si rapide ! Et il vous permet de l'identifier avec le nom de l'appareil (S'il se fait voler on peut supprimer son jeton, ce qui suppimera l'accès au voleur pour la prochaine requette API !).

```php
// Créer un token avec des capacités (abilities si on veut les limiter aux lecture seules !)
$tokenCreation = clone $user->createToken($request->device_name);
// Pui on renvoie la chaine brute String du token.
$token = $tokenCreation->plainTextToken;

// Renvoyé vers Flutter Mobile.
return response()->json([
    'token_secret' => $token
]);
```

C'est ainsi qu'a l'autre bout du monde le Mobile consommera la variable Json "token_secret" pour enregistrer son pass vers votre base ! 

C'est là tout ce que fera le Paquetage **Laravel Jetstream** de base au lieu de Breeze. Il inclut un panel pour que vos Utilisateurs web gèrent leur propres "jetons d'API (Sanctum)" dans leur paramètres de compte et les révoque... Si tel était le souhait de votre architecture !

Passons au Bilan final de la théorie des serveurs.
