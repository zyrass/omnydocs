---
description: "Reconnaitre les attaques CSRF, le DDoS ForceBrute et valider le cycle d'apprentissage de sécurité."
icon: lucide/shield-ban
tags: ["LARAVEL", "SECURITY", "CSRF", "RATELIMIT"]
---

# Failles d'injections & Auto-Évaluation

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="1 Heure">
</div>

## 1. Protection CSRF : Falsification par Inter-Sites

### 1.1 Qu'est-ce qu'une attaque CSRF ?

Alice est connectée à `blog-laravel.com`. 
Alice visite un site tiers (sans s'en rendre compte) de phishing sur son mail : `facturation-sante.com`.

Il est courant que les Hackers injectent sur leurs propres sites ce code invisible :
```html
<form id="hack" method="POST" action="https://blog-laravel.com/posts/1/delete"></form>
<script>document.getElementById('hack').submit();</script>
```

Le navigateur trompé enverra la requête de supression du serveur à la place d'Alice car le cookie d'origine lié au blog l'homologue.

### 1.2 La parade incontournable `@csrf`

Le serveur n'exécute aucunes requêtes sensibles si un **Token à Usage Unique** issu du véritable site ne corrobore pas la provenance. Le jeton aléatoire est appaisé et renouvelé pour 1 seule validation POST ou PUT.

Ce dernier s'écrit de la manière suivante dans le Frontend HTML sous Laravel : `<form method="POST">@csrf</form>`.
Tout envoi est automatiquement vérrouillé par `419 Expired`. Vous n'avez strictement aucun dév à administrer. C'est l'essence de Laravel.

Pour l'implémentation de formulaires dynamiques sans actualisation JavaScript :
```html
<meta name="csrf-token" content="{{ csrf_token() }}">

<script>
fetch('/api/posts', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
    }
});
</script>
```

<br>

---

## 2. Le Rate Limiting : Contre-attaquer le Brute Force

En 2024, envoyer 50 requêtes de Login par secondes automatisées permet de faire chuter le serveur ou pire de décrypter un mot de passe par dictionnaire de mots. La restriction du taux est un standard.

```php title="app/Providers/AppServiceProvider.php"
// Dans la fonction de boot de l'Applicatif central
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('login', function (Request $request) {
    // Autoriser 5 tentatives ratées par l'Email ET ce par IP ! Passé le délais de 1 minutes, une nouvelle tentative s'offre a lui.
    return Limit::perMinute(5)->by($request->input('email') . '|' . $request->ip());
});
```

Pour utiliser ce service "LimitRate" natif de Laravel, vous le branchez à une route logique en controller :

```php title="app/Http/Controllers/Auth/AuthController.php"
public function login(Request $request)
{
    // C'est ce bout de code que l'on traque par son hash global ou par sa condition d'echec (Trop souvent)
    $key = $request->input('email') . '|' . $request->ip();
    
    // Check de l'épuisement des tirs
    if (RateLimiter::tooManyAttempts('login:' . $key, 5)) {
        return back()->withErrors(['email' => "Trop de tentatives. Bloqués."]);
    }

    if (!AuthSystemCheckOK) {
        RateLimiter::hit('login:' . $key); // -1 Tir Disponible / +1 Rate Echec.
        return back()->withErrors(['email' => 'Identifiants incorrects.']);
    }

    // Le login est bon ! Reset de ses tirs complet à Zero.
    RateLimiter::clear('login:' . $key);
}
```

<br>

---

## 3. Auto-Évaluation du Module 4

Afin de clore the bloc de sécurité, pouvez vous répondre à ces 4 questions fondamentales du Backend PHP :

1. **Question :** Pourquoi utiliser une fonction de régénération de requête du coeur (`session()->regenerate()`) juste après avoir accepté un compte lors d'un AuthController ou LoginController manuel ?
   <details>
   <summary>Réponse</summary>
   Pour prévenir les attaques de **session fixation**. Renouveler l'ID de connexion est obligatoire, la vielle est annihilée. Le hacker qui la pister depuis 15 minutes tombe alors devant un ID nouveau qu'il ne pouvait anticiper.
   </details>

2. **Question :** Pourquoi les messages d'erreurs en Frontend d'une tentative de Hack ou de Login foiré doivent être masqués ou rester flous (`Login Incorrect`) ? Et non pas ("Cet Email n'existe pas" ou "Le Pwd d'Alain n'a pas 10 lettres" !)
   <details>
   <summary>Réponse</summary>
   Pour éviter l'énumération par ingénérie sociale. Le hacker, si on lui donne les informations de quoi et en quoi la donnée est fausse, se resserrera en entonnoire vers la bonne réponse par déduction.
   </details>

3. **Question :** Qu'est ce qu'un Cookie concrétement sur Laravel ?
   <details>
   <summary>Réponse</summary>
   Une chaîne de caractère encapsulée de force en retour de réponse HTTP par un Server. La chaîne s'installe tel un document TXT caché dans `%AppData%` du système d'éxploitation ou de l'URL cible, avec des propriétés intrinsèques lues uniquement par ce le serveur, empêchant autrui de le deviner ou de le manipuler. C'est l'encapsuleur des sessions PHP.
   </details>

4. **Question :** Un module complet existe t-il sur le framework sous forme de StarterKit ?
   <details>
   <summary>Réponse</summary>
   Parfaitement, ce module est formatif pour revoir le PHP au sens large du concept, mais la façade magique d'Auth `Auth::attempt($credentials)` est implémenté et est géré par les boites prêtes `Laravel Breeze` ou `Jetstream` (Incluant 2FA et Emails Checks).   
   </details>

<br>

---

## Conclusion Générale du Module

!!! quote "Récapitulatif"
    Vous avez reproduit **from scratch**, sans l'aide l'écosystème, toute la mécanique de **session**, la **validation du token CSRF**, la structure du Middlewares Intercepteurs. Breeze effectue le tout de bout en bout automatiquement ce que vous donne un immense avantage dans la compréhension des cas de failles et pour le débuggage si l'usine s'enraye.

L'authentification valide le droit d'être sur une page avec succès.  
Cependant, l'Autorisation est un sujet différent, pouvez-vous être libre de modifier l'article d'Alain en tant qu'auteur sans en être capable administrateur ? Ce droit d'accès logique s'adresse via le **Module 5**.
