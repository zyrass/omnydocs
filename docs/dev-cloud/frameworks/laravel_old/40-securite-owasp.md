---
description: "Prendre conscience des risques de base avec OWASP Top 10 liés aux APIs et le web."
icon: lucide/book-open-check
tags: ["LARAVEL", "SECURITY", "OWASP", "VULNERABILITIES"]
---

# L'Architecture Sécurité (OWASP)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Vue d'ensemble du Top 10

L’OWASP Top 10 représente le document de sensibilisation standard pour les développeurs sur les risques de sécurité des applications Web. 

Concernant ce dont Laravel vous protège par habitude ou que vous devez faire vous même :

| Catégorie OWASP | Protection Native Laravel / Solution |
|-----------------|--------------------------------------|
| **A01: Broken Access** | Policies, Gates (Ce n'est pas Laravel qui l'écrira pour vous) |
| **A02: Cryptographic Failures** | Facade `Hash::` et `Crypt::` (AES-256) |
| **A03: Injection (SQL)** | **Eloquent** le gère de base ! Si requete brute : bindings `?` |
| **A07: Auth Failures** | Starter Kits (Breeze), RateLimiting natif (Throttle) |
| **CSRF** | Middleware natif automatisé avec la directive `@csrf` |


<br>

---


## 2. A01 Broken Access Control (Contrôle d'accès cassé)

Un utilisateur accède à des ressources qu'il ne devrait pas pouvoir voir/modifier. C'est l'erreur numéro 1 en création de logiciel en solo. 

```php
// VULNÉRABLE : Pas de vérification d'ownership (Quid de l'admin ?)
Route::get('/posts/{post}/edit', function (Post $post) {
    return view('posts.edit', compact('post'));
});
// Résultat : N'importe qui peut éditer n'importe quel post
```

La bonne pratique est d'utiliser le module d'autorisation. Relire si besoin le chapitre Gate & Policies des modules antérieurs.

<br>

---

## 3. A03 Injection SQL

Données utilisateur interprétées comme du code.

**VULNÉRABLE : SQL brut avec concaténation non filtrée**
```php
$email = $request->input('email');
// L'email recut pourrait être par le rigolo du web : "' OR '1'='1"
$user = DB::select("SELECT * FROM users WHERE email = '$email'");
// Il va selectionner tout ! Et péter les plomb.
```

**La Solution Laravel** : SÉCURISÉ et utilisé de base partout ! (Eloquent)
```php
$user = User::where('email', $request->email)->first(); // Auto Echappé des balises SQL.
```


Méfiez vous des champs de texte de type "Formulaires", qui n'ont pas subi le passage par les objets Laravel. Il n'en tiendra qu'à vous de les sécuriser.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La sécurité n'est pas une fonctionnalité que l'on ajoute à la fin — c'est une discipline que l'on intègre à chaque décision d'architecture. Laravel protège contre la majorité de l'OWASP Top 10 par défaut (CSRF, XSS via Blade, injection SQL via Eloquent), mais la responsabilité du développeur reste entière sur la validation des entrées, la gestion des permissions et la protection des données sensibles.

> [Sécurité maîtrisée. Optimisez maintenant les performances avec les queues et jobs asynchrones →](./41-file-attente-et-jobs.md)
