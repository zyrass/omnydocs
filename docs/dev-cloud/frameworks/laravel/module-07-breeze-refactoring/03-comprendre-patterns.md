---
description: "Analyser les patterns implémentés et fournis par rapport à nos codes manuels..."
icon: lucide/scan-eye
tags: ["LARAVEL", "BREEZE", "CODE", "ANALYSIS"]
---

# Architecture Générée

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. La Navigation et les Composants Tailwind HTML

La première chose si vous parcourez le dossier des `Views` que vous constaterez sera l'apparition de multitudes de petits dossiers. Des Layouts et des Components (Composants).

### Le Layout Global (Menu)
Precieusement encodé pour afficher le Menu Dynamique pour les Modèles Connectés si session Active, il inclu par default `<html><head>...` et toutes les polices. Tout l'espace disponible au rendu se trouve par la variable `{{ $slot }}` en dessous de son appel `@include('layouts.navigation')`.

Son intégration ce fait comme ceci en enveloppe sur n'importe quel de vos fichiers :
```html
<x-app-layout>
    Taper le contenu texte du Body ici
</x-app-layout>
```

### Les Composants Atomiques
Une liste ahurissante de petit composants de Vue Tailwindcss pour éviter la duplication des `Buttons Bleu, Button Vert, etc`. Et cela s'écrit comme un framework Javascript comme VueJS sur votre espace (Grace aux tags `<x-fichier>`). 

- `<x-input-label for="title" :value="__('Hello')" />`
- `<x-primary-button> Bouton Principal Bleu </x-primary-button>`

<br>

---

## 2. Le Registre Professionnel Breeze

Regardons comment ils configurent leur logique pour que cela fonctionne. Les différences sont assez minimes pour la validation de Mot de Passe, en revanche ils utilisent en une force frappe une **Boucle D'Evènement** via `Events\Registered` qui peut propulser l'email de Confirmation dans les Abymes des Files d'Attentes des mails si activées ! Puis lance de lui même la connexion au tableau de bord.

```php title="app/Http/Controllers/Auth/RegisteredUserController.php"
class RegisteredUserController extends Controller
{
    public function store(Request $request): RedirectResponse
    {
        // 1. Validation Poussée Native ! 
        $request->validate([
            'email' => ['required', 'lowercase', 'email', 'unique:'.User::class],
            'password' => ['required', 'confirmed', Rules\Password::defaults()],
        ]);
        
        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password), // Toujours le faire ou le mettre dans un Mutateur ! (Module 3)
        ]);

        // Evènements asynchrones d'Envois d'Emails !
        event(new Registered($user));

        Auth::login($user);

        return redirect(route('dashboard', absolute: false));
    }
}
```

<br>

---

## 3. Le Login Professionnel FormRequest Breeze

Ils créaient une classe Externe FormRequest qui gèrera à la fois le Rate-Limiting d'IP qui spamme votre serveur de mots-de-passes, et le formulaire. 

```php title="app/Http/Requests/Auth/LoginRequest.php"
class LoginRequest extends FormRequest
{
    // ...
    public function authenticate(): void
    {
        // Rate Limiter d'Attaques de Force Brute natif (ThrottleKey sur IP/Date) ! 
        $this->ensureIsNotRateLimited(); 
        
        if (! Auth::attempt($this->only('email', 'password'), $this->boolean('remember'))) {
            // Echec... On incrémente le cache des frappes méchants Limiter++
            RateLimiter::hit($this->throttleKey());
            // Lever d'erreur 4XX
            throw ValidationException::withMessages(['email' => trans('auth.failed'),]);
        }

        // On reset le cache et on le laisse passer.
        RateLimiter::clear($this->throttleKey());
    }
}
```

Mener un site à bien avec des architectures solides est possible si on laisse se reposer certains bloc sur la structure globale et les paquetages pré-existants (Starter-kits). Il existe d'autres "Kits" officiels que *Breeze* comme *Jetstream* et *Fortify* plus orienté pour l'immense API ou les Équipes d'Entreprises "Teams". Mais Laravel Breeze est le meilleur compromis de refonte possible pour apprendre et avancer en pro.
