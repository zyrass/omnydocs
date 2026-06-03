---
description: "Tests automatisés de l'authentification Breeze avec PHPUnit : Feature tests des routes login, register et dashboard."
icon: lucide/book-open-check
tags: ["LARAVEL", "BREEZE", "PROJET GUIDÉ"]
---

# Phase 6 — Tests d'Authentification

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Laravel 11"
  data-time="~1 heure">
</div>

## Objectifs de la Phase 6

!!! info "Ce que vous allez faire"
    - Configurer l'environnement de test (SQLite en mémoire)
    - Écrire des Feature Tests pour l'inscription et la connexion
    - Tester les redirections (accès non authentifié, accès post-connexion)
    - Atteindre une couverture minimale des routes d'authentification

## Configuration du Fichier `phpunit.xml`

```xml title="phpunit.xml — Base de données de test en mémoire"
<php>
    <env name="APP_ENV" value="testing"/>
    <env name="DB_CONNECTION" value="sqlite"/>
    <env name="DB_DATABASE" value=":memory:"/>
</php>
```

## Feature Tests — Authentification

```php title="tests/Feature/Auth/RegistrationTest.php"
<?php

namespace Tests\Feature\Auth;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class RegistrationTest extends TestCase
{
    use RefreshDatabase;

    public function test_registration_screen_can_be_rendered(): void
    {
        $response = $this->get('/register');
        $response->assertStatus(200);
    }

    public function test_new_users_can_register(): void
    {
        $response = $this->post('/register', [
            'name'                  => 'Test User',
            'email'                 => 'test@example.com',
            'password'              => 'password',
            'password_confirmation' => 'password',
        ]);

        $this->assertAuthenticated();
        $response->assertRedirect(route('dashboard', absolute: false));
    }

    public function test_users_cannot_register_with_invalid_email(): void
    {
        $response = $this->post('/register', [
            'name'                  => 'Test User',
            'email'                 => 'not-an-email',
            'password'              => 'password',
            'password_confirmation' => 'password',
        ]);

        $this->assertGuest();
        $response->assertSessionHasErrors('email');
    }
}
```

```bash
# Lancer tous les tests
php artisan test

# Avec couverture de code (xdebug requis)
php artisan test --coverage
```


<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un test d'authentification qui passe est une garantie : chaque refactorisation future du système d'authentification sera couverte. Le pattern `$this->assertAuthenticated()` + `$response->assertRedirect()` vérifie en deux assertions que l'inscription a créé une session ET redirigé vers le bon endroit. Ces tests sont votre assurance qualité contre les régressions.

> [Phase 7 — Déploiement sur VPS →](./phase7.md)
