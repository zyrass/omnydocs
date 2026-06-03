Oui — voici une version **complète, ordonnée et cohérente** du plan, mise à jour avec ce que tu viens d’ajouter pour le **chapitre 0**, ainsi que l’**annexe OWASP à jour**. Laravel Sail est bien présenté par Laravel comme l’interface légère du stack Docker de développement local, compatible avec macOS, Windows via WSL2 et Linux, et un serveur Laravel local peut aussi être exposé sur le réseau via `php artisan serve --host=...`. [laravel](https://laravel.com/docs/13.x/sail)

Le kit Livewire officiel de Laravel 13 est bien annoncé comme basé sur **Livewire 4**, **Tailwind** et **Flux UI**, ce qui reste cohérent avec l’ouverture vers une future stack TALL. [laravel](https://laravel.com/docs/13.x/starter-kits)

## Structure générale

Le cursus conserve une structure simple : **27 chapitres (0 à 26)** et **27 parties fil rouge (0/26 à 26/26)**, avec un parallélisme strict entre théorie et application. La durée réaliste reste **90 à 110 heures** pour aller d’un profil débutant à une application Laravel 13 réellement diffusable. [laravel](https://laravel.com/docs/13.x/sail)

| Élément | Détail |
|---|---|
| Total chapitres | 27, de 0 à 26 |
| Total parties fil rouge | 27, de 0/26 à 26/26 |
| Projet fil rouge | SaaS de gestion de rendez-vous et clients |
| Niveau visé | Débutant vers production |
| Référentiels | Laravel 13, Livewire 4, Cashier Stripe, OWASP Top 10:2025 |
| Durée estimée | 90 à 110 heures |

## Plan complet

### Chapitre 0 — Vision du projet, environnement local, Docker, Sail et Git
1. **Présentation du parcours : ce que nous allons réaliser ensemble de A à Z.**
2. **C’est quoi Laravel ?**
3. **Pourquoi Laravel pour un projet professionnel moderne ?**
4. Développer avec Laravel **sans Docker ni Sail** : avantages, limites et cas d’usage.
5. Développer avec **Docker + Sail** : pourquoi standardiser l’environnement.
6. Installation sur **macOS**.
7. Installation sur **Linux**.
8. Installation sur **Windows / WSL2**.
9. Lancer un serveur local accessible depuis plusieurs ordinateurs avec `php artisan serve --host`.
10. Initialiser Git, structurer `.gitignore` et adopter Conventional Commits.  
Laravel Sail est bien conçu comme une interface CLI légère pour l’environnement Docker de développement Laravel, et ce workflow est documenté comme compatible avec macOS, Linux et Windows via WSL2.  Laravel peut aussi être exposé sur le réseau local en liant le serveur de développement à l’IP LAN de la machine avec `php artisan serve --host=<ip>`. [github](https://github.com/laravel/sail)

**Projet fil rouge — Partie 0/26**  
Présenter le SaaS final visé, préparer la machine, choisir le mode de développement local, initialiser le projet et le dépôt Git.

### Chapitre 1 — Découvrir Laravel 13
1. Présentation de Laravel 13.
2. Cas d’usage du framework.
3. Écosystème officiel.
4. Nouveautés Laravel 13.
5. PHP 8.3+ et prérequis.
6. Structure d’un projet neuf.
7. Cycle requête/réponse.
8. Première route.
9. Première vue.
10. Bonnes pratiques de départ.  
Laravel 13 met en avant les starter kits officiels, l’écosystème moderne autour de Livewire, et une documentation recentrée sur une expérience développeur intégrée. [laravel](https://laravel.com/docs/13.x/starter-kits)

**Projet fil rouge — Partie 1/26**  
Créer la page d’accueil et la structure initiale du SaaS.

### Chapitre 2 — Préparer l’environnement de développement
1. Configurer `.env`.
2. Brancher la base de données.
3. Utiliser Artisan.
4. Utiliser Tinker.
5. Organiser la configuration locale.
6. Préparer VS Code ou PHPStorm.
7. Gérer les erreurs locales.
8. Installer Telescope.
9. Installer Debugbar ou Clockwork.
10. Utiliser Xdebug ou Ray.

**Projet fil rouge — Partie 2/26**  
Configurer totalement l’environnement local du projet.

### Chapitre 3 — Architecture d’une application Laravel
1. Comprendre `app`, `routes`, `resources`, `config`, `database`.
2. Comprendre MVC.
3. Comprendre le container.
4. Comprendre les providers.
5. Organiser les contrôleurs.
6. Organiser les services.
7. Organiser les actions.
8. Nommer correctement les classes.
9. Structurer un projet maintenable.
10. Documenter le projet.

**Projet fil rouge — Partie 3/26**  
Créer la première ressource métier du SaaS et son architecture.

### Chapitre 4 — Base de données et migrations
1. Concevoir le schéma.
2. Créer des migrations.
3. Choisir les types de colonnes.
4. Utiliser les index.
5. Poser les contraintes.
6. Gérer les clés étrangères.
7. Lancer et rollbacker les migrations.
8. Créer des seeders.
9. Créer des factories.
10. Préparer les données de test.

**Projet fil rouge — Partie 4/26**  
Créer la base du domaine client et peupler les données.

### Chapitre 5 — Eloquent ORM
1. Créer des modèles.
2. CRUD avec Eloquent.
3. `fillable` et `guarded`.
4. Mass assignment.
5. Accessors.
6. Mutators.
7. Casts et encrypted casts.
8. Sérialisation.
9. Requêtes lisibles.
10. Optimisation de base.

**Projet fil rouge — Partie 5/26**  
Implémenter le CRUD Client complet.

### Chapitre 6 — Premiers tests avec Pest
1. Pourquoi tester tôt.
2. Installer Pest.
3. Structurer les tests Laravel.
4. Tester une route.
5. Tester une création.
6. Tester la validation.
7. Tester un modèle.
8. Utiliser les factories.
9. Lancer `php artisan test`.
10. Intégrer le test dans le flux quotidien.

**Projet fil rouge — Partie 6/26**  
Écrire les premiers tests du CRUD client.  
Critère de validation : `php artisan test` passe sur les scénarios CRUD fondamentaux.

### Chapitre 7 — Relations entre modèles
1. One to one.
2. One to many.
3. Many to many.
4. Tables pivot.
5. Relations polymorphes.
6. Eager loading.
7. Éviter le N+1.
8. Filtrer par relation.
9. Structurer les relations métier.
10. Relations avancées.

**Projet fil rouge — Partie 7/26**  
Relier clients, sociétés et rendez-vous.

### Chapitre 8 — Gestion des créneaux et conflits de réservation
1. Modéliser les créneaux.
2. Gérer les disponibilités.
3. Détecter les conflits.
4. Stocker en UTC.
5. Afficher selon le fuseau utilisateur.
6. Gérer les récurrences.
7. Écrire les règles métier de réservation.
8. Valider les créneaux.
9. Gérer les cas limites.
10. Tester la logique horaire.

**Projet fil rouge — Partie 8/26**  
Ajouter le cœur métier de réservation au SaaS.

### Chapitre 9 — Routes et contrôleurs
1. Routes web.
2. Routes API.
3. Paramètres de route.
4. Routes nommées.
5. Groupes.
6. Middlewares.
7. Contrôleurs simples.
8. Contrôleurs resource.
9. Organisation des endpoints.
10. Tests simples de routes.

**Projet fil rouge — Partie 9/26**  
Mettre en place toutes les routes métier du projet.  
Critère de validation : les routes critiques répondent avec les codes attendus.

### Chapitre 10 — Blade et interface serveur
1. Syntaxe Blade.
2. Conditions et boucles.
3. Layouts.
4. Sections.
5. Composants Blade.
6. Sous-vues.
7. Messages d’erreur.
8. Réutilisation du code UI.
9. Structuration du layout global.
10. Interface serveur propre.

**Projet fil rouge — Partie 10/26**  
Construire les vues principales du SaaS.

### Chapitre 11 — Formulaires et validation
1. Construire un formulaire.
2. CSRF.
3. Validation serveur.
4. Règles simples.
5. Règles conditionnelles.
6. Messages d’erreur.
7. Anciennes valeurs.
8. FormRequest.
9. Validation de fichiers.
10. Expérience utilisateur.

**Projet fil rouge — Partie 11/26**  
Créer les formulaires métier et leurs validations.

### Chapitre 12 — Authentification moderne et starter kits
1. Auth moderne : sessions, tokens, Fortify.
2. Panorama des 4 kits officiels.
3. Kit Livewire : installation et démarrage.
4. Kit React : installation et démarrage.
5. Kit Vue : installation et démarrage.
6. Kit Svelte : installation et démarrage.
7. Inscription, connexion, déconnexion.
8. Vérification d’email et reset password.
9. 2FA et teams.
10. Sanctum pour SPA et API.  
Laravel 13 fournit quatre starter kits officiels, et son kit Livewire officiel est annoncé comme construit avec **Livewire 4**, **Tailwind** et **Flux UI**. [laravel](https://laravel.com/starter-kits)

**Projet fil rouge — Partie 12/26**  
Installer le starter kit Livewire et sécuriser l’accès au SaaS.

### Chapitre 13 — Facturation SaaS avec Laravel Cashier et Stripe
1. Pourquoi la facturation est un bloc métier à part.
2. Présenter Cashier.
3. Configurer Stripe.
4. Créer les produits et plans.
5. Souscrire à un abonnement.
6. Changer de plan.
7. Annuler ou reprendre un abonnement.
8. Gérer la période d’essai.
9. Gérer les webhooks Stripe.
10. Limiter les fonctionnalités selon le plan.
11. Gérer la cohérence d’état côté applicatif.
12. Tester la facturation en mode sandbox.  
Laravel Cashier fournit une interface officielle et fluide vers les services d’abonnement Stripe. [github](https://github.com/laravel/cashier-stripe)

**Projet fil rouge — Partie 13/26**  
Ajouter les abonnements Stripe et les limites de plan au SaaS.  
Critère de validation : un abonnement de test est créé, modifié et synchronisé via webhook.

### Chapitre 14 — Autorisation, rôles et policies
1. Authentification vs autorisation.
2. Gates.
3. Policies.
4. Autoriser par ressource.
5. Gérer les rôles.
6. Gérer les permissions.
7. Intégrer la notion d’équipe.
8. Tester les policies.
9. Journaliser les actions critiques.
10. Évaluer Spatie Permission.

**Projet fil rouge — Partie 14/26**  
Protéger les ressources du SaaS avec policies et rôles.  
Critère de validation : une policy refuse correctement un accès hors périmètre.

### Chapitre 15 — Sécurité applicative et OWASP Top 10:2025
1. Vue d’ensemble OWASP Top 10:2025.
2. A01 Broken Access Control.
3. A02 Security Misconfiguration.
4. A03 Software Supply Chain Failures.
5. A04 Cryptographic Failures.
6. A05 Injection.
7. A06 Insecure Design.
8. A07 Authentication Failures.
9. A08 Software or Data Integrity Failures.
10. A09 Security Logging and Alerting Failures.
11. A10 Mishandling of Exceptional Conditions.
12. CSRF hors Top 10 mais essentiel.
13. Mass assignment.
14. Audit sécurité complet.  
La liste officielle OWASP Top 10:2025 suit bien cet ordre de A01 à A10. [owasp](https://owasp.org/Top10/2025/)

**Projet fil rouge — Partie 15/26**  
Durcir le SaaS selon un audit OWASP 2025.  
Critère de validation : chaque catégorie prioritaire est reliée à une contre-mesure dans le projet.

### Chapitre 16 — Fichiers, images et stockage
1. Disques de stockage.
2. Uploads.
3. Validation de fichiers.
4. Gestion d’images.
5. Suppression propre.
6. Téléchargement sécurisé.
7. Stockage local.
8. Stockage distant.
9. Organisation des médias utilisateur.
10. Préparation au cloud.

**Projet fil rouge — Partie 16/26**  
Ajouter avatars, documents et gestion des médias.

### Chapitre 17 — Logique métier avancée
1. Services métier.
2. Classes d’action.
3. Events.
4. Listeners.
5. Notifications.
6. Mailables.
7. Jobs.
8. Queues.
9. Organisation de la logique métier.
10. Découper proprement le code applicatif.

**Projet fil rouge — Partie 17/26**  
Refactoriser le SaaS avec services, actions, événements et jobs.

### Chapitre 18 — Scheduler, rappels et temps réel
1. Comprendre le scheduler Laravel.
2. `schedule:run` et le cron système.
3. Tâches planifiées métiers.
4. Rappels automatiques de rendez-vous.
5. Envoi différé de notifications.
6. Horizon et supervision des queues.
7. Reverb et temps réel.
8. Diffuser des événements en direct.
9. Gérer les erreurs de tâches planifiées.
10. Tester le flux complet rappels + temps réel.

**Projet fil rouge — Partie 18/26**  
Mettre en place les rappels automatiques et les notifications temps réel.  
Critère de validation : une tâche planifiée se déclenche correctement et un rappel est observable.

### Chapitre 19 — API REST et documentation
1. Routes API.
2. Contrôleurs API.
3. API Resources.
4. Pagination.
5. Gestion des erreurs.
6. Sanctum côté API.
7. Versionnement.
8. Bonnes pratiques REST.
9. Préparer un front séparé.
10. Documenter avec OpenAPI ou Scribe.

**Projet fil rouge — Partie 19/26**  
Construire l’API REST du SaaS.

### Chapitre 20 — Interfaces dynamiques avec Livewire
1. Créer un composant.
2. État réactif.
3. Validation temps réel.
4. Actions sans reload complet.
5. Tableaux interactifs.
6. Formulaires dynamiques.
7. Composants réutilisables.
8. Cas d’usage métier.
9. Intégration avec le starter kit Livewire.
10. Limites et bonnes pratiques.  
Le kit Livewire officiel de Laravel met explicitement en avant **Livewire 4** et **Flux UI** comme base d’interface. [fluxui](https://fluxui.dev)

**Projet fil rouge — Partie 20/26**  
Rendre le SaaS plus interactif avec Livewire.

### Chapitre 21 — Tests automatisés avec PHPUnit, Pest et E2E
1. Stratégie de test globale.
2. Tests unitaires.
3. Tests fonctionnels.
4. Tests de contrôleurs.
5. Tests de modèles.
6. Tests de validation.
7. Pest avancé.
8. Scénarios métier.
9. Introduction aux tests E2E.
10. Préparer la CI autour des tests.

**Projet fil rouge — Partie 21/26**  
Compléter la couverture de tests de l’application.  
Critère de validation : les parcours métier principaux disposent d’au moins un test automatisé.

### Chapitre 22 — Tests E2E avec Nightwatch
1. Pourquoi un test E2E.
2. Installer Nightwatch.
3. Préparer l’environnement de test.
4. Écrire un scénario de connexion.
5. Écrire un scénario de CRUD.
6. Écrire un scénario de réservation.
7. Écrire un scénario d’abonnement.
8. Capturer les erreurs.
9. Intégrer à la CI.
10. Stabiliser les tests fragiles.

**Projet fil rouge — Partie 22/26**  
Valider les parcours critiques du SaaS en bout en bout.

### Chapitre 23 — Laravel AI SDK
1. Présenter l’AI SDK.
2. Configurer un provider.
3. Générer du texte.
4. Utiliser le tool calling.
5. Générer des embeddings.
6. Recherche vectorielle.
7. Ajouter un assistant métier.
8. Encadrer l’usage IA.
9. Intégrer dans un service Laravel.
10. Mesurer la valeur métier.  
Laravel 13 met en avant un AI SDK first-party dans sa documentation. [raw.githubusercontent](https://raw.githubusercontent.com/driade/laravel-book/master/laravel-docs-13.x.pdf)

**Projet fil rouge — Partie 23/26**  
Ajouter une fonctionnalité IA utile au SaaS.

### Chapitre 24 — Performance, Octane et cache
1. Enjeux de performance.
2. Présenter Octane.
3. FrankenPHP, Swoole, RoadRunner.
4. Installer Octane.
5. Mettre en cache les données métier.
6. Utiliser Redis et tags.
7. Optimiser les requêtes.
8. Utiliser Pulse et Clockwork.
9. Comprendre Blackfire et son coût.
10. Mesurer avant/après.

**Projet fil rouge — Partie 24/26**  
Optimiser le SaaS pour la production.

### Chapitre 25 — CI/CD avec GitLab et GitHub Actions
1. Pourquoi la CI/CD.
2. Pipeline GitLab CI/CD.
3. Pipeline GitHub Actions.
4. Lancer les tests automatiquement.
5. Lancer `composer audit`.
6. Lancer les linters.
7. Préparer staging et production.
8. Sécuriser les secrets.
9. Déployer automatiquement.
10. Surveiller les pipelines.

**Projet fil rouge — Partie 25/26**  
Automatiser tests, audit et déploiement.

### Chapitre 26 — Déploiement, production et ouverture vers la stack TALL
1. Déployer avec Forge.
2. Déployer avec Vapor.
3. Déployer en IaaS sur RockyLinux sécurisé + OVH.
4. Gérer Nginx, PHP-FPM, Redis, Supervisor.
5. Configurer HTTPS, firewall, fail2ban, sauvegardes.
6. Vérifier la checklist production.
7. Comparer Forge, Vapor et IaaS.
8. Positionner Laravel + Livewire dans un vrai projet produit.
9. Conclusion : pourquoi apprendre Alpine.js et Tailwind CSS ensuite.
10. Préparer la future formation TALL : fusionner Tailwind CSS, Alpine.js, Laravel 13 et Livewire 4.  
Les starter kits frontend Laravel reposent sur Tailwind CSS, ce qui rend l’ouverture vers la stack TALL cohérente dans la continuité du kit Livewire. [laravel](https://laravel.com/docs/13.x/frontend)

**Projet fil rouge — Partie 26/26**  
Déployer le SaaS en production et préparer son évolution vers une future stack TALL.

## Annexe OWASP

L’annexe reste un support avancé du chapitre 15. Elle conserve le format **vulnérable / sûr / lien fil rouge**, qui est très adapté à une pédagogie par l’attaque. OWASP 2025 reste bien le référentiel de base. [owasp](https://owasp.org/www-project-top-ten/)

### A01:2025 Broken Access Control

**Vulnérable**
```php
public function show($id)
{
    return Client::findOrFail($id);
}
```

**Sûr**
```php
public function show(Client $client)
{
    $this->authorize('view', $client);
    return view('clients.show', compact('client'));
}
```

**Policy**
```php
public function view(User $user, Client $client)
{
    return $user->team_id === $client->team_id;
}
```

**Lien fil rouge** : Partie 14/26.

### A02:2025 Security Misconfiguration

**Vulnérable**
```env
APP_DEBUG=true
APP_ENV=local
```

**Sûr**
```env
APP_DEBUG=false
APP_ENV=production
```

**Durcissement**
```php
'X-Frame-Options' => 'DENY',
'X-Content-Type-Options' => 'nosniff',
'Referrer-Policy' => 'strict-origin-when-cross-origin',
'Content-Security-Policy' => "default-src 'self'",
```

**Lien fil rouge** : Partie 15/26.

### A03:2025 Software Supply Chain Failures

**Vulnérable**
```bash
composer install
npm install
```

**Sûr**
```bash
composer audit
npm audit
```

**Renforcement**
- verrouiller `composer.lock`,
- vérifier les checksums,
- générer un SBOM,
- contrôler les dépendances en CI.

**Lien fil rouge** : Partie 15/26.

### A04:2025 Cryptographic Failures

**Vulnérable**
```php
$user->api_token = $token;
```

**Sûr**
```php
protected $casts = [
    'password' => 'hashed',
    'api_token' => 'encrypted',
];
```

**Lien fil rouge** : Partie 15/26.

### A05:2025 Injection

**Vulnérable**
```php
Client::whereRaw("email = '$input'")->first();
```

```blade
{!! $userInput !!}
```

**Sûr**
```php
Client::where('email', $input)->first();
```

```blade
{{ $userInput }}
```

**Lien fil rouge** : Partie 15/26.

### A06:2025 Insecure Design

**Vulnérable**
```php
if ($user->subscription->plan === 'basic') {
    //
}
```

**Sûr**
```php
class CheckSubscriptionLimit
{
    public function handle(Request $request, Closure $next)
    {
        $user = $request->user();

        $estPro = $user->subscribedToPrice(config('billing.prices.pro'), 'default');

        if (! $estPro && $user->rendezVous()->count() >= 10) {
            abort(403, 'Limite du plan gratuit atteinte.');
        }

        return $next($request);
    }
}
```

**Lien fil rouge** : Partie 13/26 et Partie 17/26.

### A07:2025 Authentication Failures

**Vulnérable**
```php
RateLimiter::for('login', function (Request $request) {
    return Limit::perMinute(5)->by($request->ip());
});
```

**Sûr**
```php
RateLimiter::for('login', function (Request $request) {
    return Limit::perMinute(5)->by($request->input('email').'|'.$request->ip());
});
```

**Lien fil rouge** : Partie 12/26.

### A08:2025 Software or Data Integrity Failures

**Vulnérable**
```php
$url = Storage::disk('public')->temporaryUrl($path, now()->addMinutes(5));
```

**Sûr**
```php
'documents' => [
    'driver' => 'local',
    'root' => storage_path('app/private'),
    'serve' => true,
],

$url = Storage::disk('documents')->temporaryUrl($path, now()->addMinutes(5));
```

**Encore mieux pour A08**
```php
if (! $request->hasValidSignature()) {
    abort(403);
}
```

**Lien fil rouge** : Partie 16/26 et Partie 13/26.

### A09:2025 Security Logging and Alerting Failures

**Vulnérable**
```php
Log::info('login_failed');
```

**Sûr**
```php
Log::channel('audit')->info('login_failed', [
    'user_id' => $userId,
    'ip' => request()->ip(),
]);
```

**Renforcement**
- déclencher une alerte après N échecs,
- envoyer une notification,
- centraliser les logs.

**Lien fil rouge** : Partie 15/26.

### A10:2025 Mishandling of Exceptional Conditions

**Vulnérable**
```php
try {
    //
} catch (\Exception $e) {
    return true;
}
```

**Sûr**
```php
try {
    //
} catch (\Exception $e) {
    Log::error($e);
    abort(500);
}
```

**Lien fil rouge** : Partie 15/26.

### Hors Top 10 mais essentiels

**CSRF** : protection native Laravel sur les formulaires et flux d’écriture.  
**Mass assignment** : contrôle strict via `$fillable` ou `$guarded`.  
Ces deux points restent essentiels pédagogiquement même hors catégorie autonome OWASP 2025. [owasp](https://owasp.org/Top10/2025/)

## État final

Le plan est maintenant plus clair dès le chapitre 0, avec la vision produit, l’explication de Laravel, le choix entre environnement natif et Docker/Sail, l’installation multi-OS et l’exposition du serveur local sur le réseau. L’annexe OWASP reste alignée avec la pédagogie par l’attaque et techniquement cohérente. [arunas](https://arunas.dev/testing-laravel-websites-over-local-network/)