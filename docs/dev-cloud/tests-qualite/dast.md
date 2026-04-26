---
description: "DAST — Tests dynamiques de sécurité : OWASP ZAP, tests des 10 vulnérabilités OWASP les plus courantes sur une application Laravel en cours d'exécution."
icon: lucide/book-open-check
tags: ["DAST", "OWASP", "SECURITE", "ZAP", "TESTING", "LARAVEL"]
---

# DAST — Tests Dynamiques de Sécurité

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="2024"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Inspecteur Sous Couverture"
    Le SAST lit votre plan de construction pour détecter les défauts structurels. Le DAST envoie un inspecteur sous couverture dans **le bâtiment en fonctionnement** : il tente d'ouvrir toutes les portes, force les serrures, essaie d'accéder aux pièces interdites, teste les systèmes de sécurité en condition réelle. Ce que le plan ne peut pas révéler, l'inspecteur en action l'expose.

**DAST (Dynamic Application Security Testing)** analyse une application **pendant son exécution** en simulant les attaques d'un attaquant externe. Contrairement au SAST (analyse statique), le DAST teste le comportement réel de l'application — responses HTTP, sessions, authentification, validations.

<br>

---

## 1. OWASP Top 10 — Les Cibles du DAST

Le DAST cherche principalement les vulnérabilités du [OWASP Top 10](https://owasp.org/www-project-top-ten/) :

| # | Vulnérabilité | Exemple Laravel | Risque |
|---|---|---|---|
| A01 | **Broken Access Control** | Accéder à `/admin` sans rôle | 🔴 Critique |
| A02 | **Cryptographic Failures** | Mot de passe en clair en DB | 🔴 Critique |
| A03 | **Injection** (SQL, XSS) | `$_GET['id']` non filtré | 🔴 Critique |
| A04 | **Insecure Design** | Pas de rate limiting sur login | 🟠 Élevé |
| A05 | **Security Misconfiguration** | `APP_DEBUG=true` en production | 🟠 Élevé |
| A06 | **Vulnerable Components** | Dépendances obsolètes | 🟡 Moyen |
| A07 | **Authentication Failures** | Session non invalidée | 🔴 Critique |
| A08 | **Software Integrity Failures** | Pas de vérification des packages | 🟡 Moyen |
| A09 | **Logging Failures** | Aucun log des tentatives login | 🟡 Moyen |
| A10 | **SSRF** | `Http::get($userInput)` | 🟠 Élevé |

<br>

---

## 2. OWASP ZAP — L'Outil de Référence

**ZAP (Zed Attack Proxy)** est l'outil DAST open-source de référence OWASP. Il intercepte et analyse le trafic HTTP entre le navigateur et l'application.

```bash title="Bash — Installer et lancer ZAP"
# ─── Docker (recommandé en CI) ────────────────────────────────────────────────
docker pull zaproxy/zap-stable

# ─── Scan passif rapide (baseline scan) ──────────────────────────────────────
docker run -t zaproxy/zap-stable zap-baseline.py \
    -t https://staging.monapp.com \
    -r zap-report.html

# ─── Scan actif complet (plus agressif) ──────────────────────────────────────
docker run -t zaproxy/zap-stable zap-full-scan.py \
    -t https://staging.monapp.com \
    -r zap-report.html \
    -J zap-report.json

# ─── Mode headless avec API ───────────────────────────────────────────────────
docker run -d -u zap -p 8080:8080 zaproxy/zap-stable \
    zap.sh -daemon -port 8080 -config api.disablekey=true
```

### Intégration CI/CD

```yaml title="YAML — GitHub Actions : ZAP Baseline Scan"
name: DAST — ZAP Scan

on:
  schedule:
    - cron: '0 2 * * *'    # Scan nightly à 2h du matin
  workflow_dispatch:         # Déclenchement manuel

jobs:
  zap-scan:
    runs-on: ubuntu-latest

    services:
      app:                          # L'application à scanner
        image: your-app-image:latest
        ports:
          - 8000:8000
        env:
          APP_ENV: staging

    steps:
      - uses: actions/checkout@v4

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.10.0
        with:
          target: 'http://localhost:8000'
          rules_file_name: '.zap/rules.tsv'     # Règles custom
          cmd_options: '-a'                       # Inclure les alertes

      - name: Upload rapport ZAP
        uses: actions/upload-artifact@v4
        with:
          name: zap-report
          path: report_html.html
        if: always()
```

<br>

---

## 3. Tests Manuels — Vulnérabilités Laravel Courantes

### A01 — Broken Access Control

```php title="PHP — PHPUnit/Pest : tester le contrôle d'accès"
// ─── Test : Un utilisateur ne peut pas accéder aux ressources des autres ──────
it('prevents user from accessing other users posts', function () {
    $alice = User::factory()->create();
    $bob   = User::factory()->create();
    $post  = Post::factory()->create(['user_id' => $bob->id]);

    $response = $this->actingAs($alice)
        ->putJson("/api/posts/{$post->id}", ['title' => 'Hacked!']);

    $response->assertStatus(403);  // Forbidden
    $this->assertDatabaseMissing('posts', ['title' => 'Hacked!']);
});

// ─── Test : Les routes admin sont protégées ────────────────────────────────────
it('blocks non-admin from admin routes', function () {
    $user = User::factory()->create(['role' => 'user']);

    $this->actingAs($user)
        ->get('/admin/users')
        ->assertStatus(403);

    $this->actingAs($user)
        ->delete('/admin/users/1')
        ->assertStatus(403);
});
```

### A03 — Injection SQL & XSS

```php title="PHP — Tester les injections avec PHPUnit/Pest"
// ─── Test SQL Injection ────────────────────────────────────────────────────────
it('is immune to SQL injection in search', function () {
    User::factory()->create(['name' => 'Alice']);

    $malicious = "'; DROP TABLE users; --";

    $response = $this->getJson("/api/users?search=" . urlencode($malicious));

    $response->assertStatus(200);
    // La table existe encore :
    $this->assertDatabaseCount('users', 1);
});

// ─── Test XSS ─────────────────────────────────────────────────────────────────
it('escapes HTML in user-provided content', function () {
    $user = User::factory()->create();

    $xssPayload = '<script>alert("XSS")</script>';

    $this->actingAs($user)
        ->postJson('/api/comments', ['content' => $xssPayload]);

    $comment = Comment::first();

    // Le payload est échappé, pas exécuté
    expect($comment->content)->not->toContain('<script>');
    // Ou vérifie que l'API retourne du HTML échappé :
    $response = $this->getJson('/api/comments/' . $comment->id);
    $response->assertJsonMissing(['<script>']);
});
```

### A07 — Authentication Failures

```php title="PHP — Tester la résistance aux attaques d'authentification"
// ─── Test : Rate limiting sur le login ────────────────────────────────────────
it('blocks login after too many failed attempts', function () {
    $user = User::factory()->create();

    // 6 tentatives échouées
    foreach (range(1, 6) as $i) {
        $this->postJson('/api/login', [
            'email'    => $user->email,
            'password' => 'wrong-password',
        ]);
    }

    // La 7ème doit être bloquée par le rate limiter
    $response = $this->postJson('/api/login', [
        'email'    => $user->email,
        'password' => 'correct-password',
    ]);

    $response->assertStatus(429);  // Too Many Requests
});

// ─── Test : Session invalidée après déconnexion ────────────────────────────────
it('invalidates session on logout', function () {
    $user = User::factory()->create();
    $token = $user->createToken('test')->plainTextToken;

    // Déconnecter
    $this->withToken($token)
        ->postJson('/api/logout')
        ->assertStatus(200);

    // Le token ne fonctionne plus
    $this->withToken($token)
        ->getJson('/api/user')
        ->assertStatus(401);
});
```

### A05 — Security Misconfiguration

```php title="PHP — Tester la configuration de sécurité"
// ─── Test : APP_DEBUG désactivé en production ──────────────────────────────────
it('does not expose stack traces in production', function () {
    config(['app.debug' => false]);

    $response = $this->getJson('/api/route-that-throws');

    // En production, pas de stack trace dans la réponse
    $response->assertJsonMissing(['file', 'trace', 'line']);
    $response->assertJsonStructure(['message']);
});

// ─── Test : Headers de sécurité HTTP ──────────────────────────────────────────
it('returns security headers', function () {
    $response = $this->get('/');

    $response->assertHeader('X-Frame-Options');
    $response->assertHeader('X-Content-Type-Options', 'nosniff');
    $response->assertHeader('Referrer-Policy');
});
```

<br>

---

## 4. Laravel Security Checklist

```php title="PHP — Checklist sécurité Laravel (vérifiable par tests)"
// ─── CSRF Protection ──────────────────────────────────────────────────────────
// ✅ Automatique via VerifyCsrfToken middleware (routes web)
// Test : POST sans token CSRF → 419

// ─── Mass Assignment Protection ───────────────────────────────────────────────
class User extends Model
{
    protected $fillable = ['name', 'email', 'password'];
    // ✅ 'role' n'est PAS fillable — ne peut pas être mass-assigné
}

// Test :
it('prevents mass assignment of role', function () {
    $response = $this->postJson('/api/register', [
        'name'     => 'Alice',
        'email'    => 'alice@example.com',
        'password' => 'SecurePass123!',
        'role'     => 'admin',    // Tentative de mass assignment
    ]);

    $response->assertStatus(201);
    expect(User::first()->role)->not->toBe('admin');
});

// ─── Validation stricte des entrées ──────────────────────────────────────────
// ✅ Toujours valider avec $request->validate() ou Form Request
// Test : envoyer des données invalides → 422 Unprocessable Entity
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — OWASP Top 10 en tests Feature**

```php title="PHP — Exercice 1 : écrire une suite de tests de sécurité"
// Pour votre projet Laravel, écrivez un test pour chaque scénario :
// 1. Route /admin/* retourne 403 pour un utilisateur non-admin
// 2. POST /api/login avec 10 mauvais mots de passe → 429 au 6ème
// 3. Injection SQL dans /api/search?q=... → la DB reste intacte
// 4. XSS dans un formulaire de commentaire → le script n'est pas rendu
// 5. Token expiré → 401 sur les routes protégées
// 6. Utilisateur A ne peut pas modifier les ressources de l'utilisateur B
```

**Exercice 2 — ZAP Baseline Scan**

```bash title="Bash — Exercice 2 : lancer un scan ZAP sur l'environnement local"
# 1. Démarrer votre application Laravel en local (php artisan serve)
# 2. Lancer le baseline scan :
docker run -t zaproxy/zap-stable zap-baseline.py \
    -t http://host.docker.internal:8000 \
    -r zap-report.html

# 3. Ouvrir zap-report.html et analyser les alertes
# 4. Corriger les alertes de niveau "High" (au moins 2)
# 5. Relancer le scan — les alertes doivent avoir disparu
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le DAST complète le SAST en testant l'application **en conditions réelles** — sessions actives, cookies, headers HTTP, comportement des APIs. **ZAP** est l'outil de référence : en baseline scan, il est non-destructif et peut tourner en CI nightly. Les tests Feature Laravel (PHPUnit/Pest) couvrent les vulnérabilités les plus courantes du Top 10 OWASP de façon automatisée, reproductible et intégrée au pipeline de test existant. Priorité absolue : tester le **contrôle d'accès** (A01) et l'**injection** (A03) qui représentent les 2 vecteurs d'attaque les plus exploités.

> Prochaine étape : [Fuzzing →](./fuzzing.md) — générer des entrées aléatoires pour découvrir les comportements inattendus.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La maîtrise de ces concepts de développement moderne est cruciale pour construire des applications scalables, maintenables et sécurisées.

> [Retour à l'index →](./index.md)
