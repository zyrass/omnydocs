---
description: "Initialisation du client de jeu Angular 21 avec gestion des tokens en LocalStorage et configuration des interceptors Bearer."
icon: lucide/book-open-check
tags: ["ANGULAR", "SIGNALS", "LOCALSTORAGE", "BEARER", "INTERCEPTOR"]
---

# Phase 4 : Setup Angular 21 + Signals

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="1h30 - 2h">
</div>


!!! quote "Analogie pédagogique"
    _Sécuriser une API avec Sanctum s'apparente à donner un jeton d'accès temporaire à un livreur. Au lieu de lui donner les clés de la maison (authentification de session), vous lui donnez un badge qui ne permet d'ouvrir que la porte du garage, et qui peut être révoqué à tout moment._

## Objectif de la Phase

> L'API backend est fonctionnelle. Nous allons maintenant créer l'interface client de notre jeu avec **Angular 21**. À la différence de Jetstream, l'authentification est ici gérée par des **Personal Access Tokens**. Nous devons donc construire un service capable de stocker ces tokens de manière sécurisée (LocalStorage) et un intercepteur HTTP chargé de les injecter automatiquement dans chaque requête vers le backend sous la forme d'un en-tête `Authorization: Bearer <token>`.

## Étape 4.1 : Création du Projet Angular (Standalone)

Comme pour le projet précédent, nous partons sur une architecture moderne.

```bash
# Générer le projet Angular 21
ng new dungeon-rpg-client --routing --style=scss

cd dungeon-rpg-client
```

Pas de proxy complexe ici : puisque nous envoyons les tokens explicitement, les requêtes CORS cross-origin fonctionneront nativement (si Laravel est bien configuré).

Côté Laravel, vérifiez simplement dans `config/cors.php` :
```php
'paths' => ['api/*', 'sanctum/csrf-cookie'],
'allowed_origins' => ['http://localhost:4200'], // Le port Angular
'supports_credentials' => false, // PAS BESOIN pour les Bearer tokens
```

## Étape 4.2 : Le TokenService (Gestion du LocalStorage)

Il nous faut un service dédié uniquement à la lecture/écriture du token dans le navigateur.

```bash
ng generate service core/services/token
```

```typescript title="src/app/core/services/token.service.ts"
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TokenService {
  private readonly TOKEN_KEY = 'rpg_auth_token';

  saveToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  hasToken(): boolean {
    return !!this.getToken();
  }
}
```

## Étape 4.3 : L'AuthService propulsé par Signals

Créons le service d'authentification principal qui dialoguera avec l'API Laravel en utilisant les tokens.

```bash
ng generate service core/services/auth
```

```typescript title="src/app/core/services/auth.service.ts"
import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';
import { TokenService } from './token.service';
import { User } from '../../shared/models/user.model'; // Modèle TS à créer

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private tokenService = inject(TokenService);
  private router = inject(Router);

  // Le State (Signal)
  readonly currentUser = signal<User | null | undefined>(undefined);
  
  readonly isAuthenticated = computed(() => !!this.currentUser());

  private readonly API_URL = 'http://localhost:8000/api';

  login(credentials: any) {
    return this.http.post<{user: User, token: string}>(`${this.API_URL}/login`, credentials)
      .pipe(
        tap(response => {
          this.tokenService.saveToken(response.token);
          this.currentUser.set(response.user);
          this.router.navigate(['/game']); // Redirection vers le jeu
        })
      );
  }

  register(data: any) {
    return this.http.post<{user: User, token: string}>(`${this.API_URL}/register`, data)
      .pipe(
        tap(response => {
          this.tokenService.saveToken(response.token);
          this.currentUser.set(response.user);
          this.router.navigate(['/character-creation']);
        })
      );
  }

  logout() {
    // Si un token est présent, on dit à l'API de le détruire
    if (this.tokenService.hasToken()) {
      this.http.post(`${this.API_URL}/logout`, {}).subscribe({
        next: () => this.clearSession(),
        error: () => this.clearSession() // Même en cas d'erreur réseau, on purge côté front
      });
    } else {
      this.clearSession();
    }
  }

  private clearSession() {
    this.tokenService.removeToken();
    this.currentUser.set(null);
    this.router.navigate(['/login']);
  }

  // Lancé au démarrage de l'app (app.component.ts)
  restoreSession() {
    if (this.tokenService.hasToken()) {
      this.http.get<User>(`${this.API_URL}/user`).subscribe({
        next: (user) => this.currentUser.set(user),
        error: () => this.clearSession() // Token expiré ou invalide
      });
    } else {
      this.currentUser.set(null);
    }
  }
}
```

## Étape 4.4 : L'Intercepteur HTTP (Injection du Bearer)

C'est la pièce maîtresse du système Stateless. Angular doit intercepter TOUTES les requêtes sortantes pour y ajouter l'en-tête d'autorisation si le token existe.

```bash
ng generate interceptor core/interceptors/token
```

```typescript title="src/app/core/interceptors/token.interceptor.ts"
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { TokenService } from '../services/token.service';
import { AuthService } from '../services/auth.service';

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  const tokenService = inject(TokenService);
  const authService = inject(AuthService);

  // 1. Clonage de la requête initiale
  let authReq = req;

  // 2. Injection de l'en-tête si le token est présent
  const token = tokenService.getToken();
  if (token != null) {
    authReq = req.clone({
      headers: req.headers.set('Authorization', 'Bearer ' + token)
    });
  }

  // 3. Gestion des erreurs globales (ex: Token Révogué)
  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      // Si l'API renvoie 401 Unauthorized
      if (error.status === 401) {
        authService.logout(); // Purge locale
      }
      return throwError(() => error);
    })
  );
};
```

N'oubliez pas d'enregistrer l'intercepteur dans `app.config.ts` :

```typescript title="src/app/app.config.ts"
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([tokenInterceptor])) // Activer l'intercepteur
  ]
};
```

## Étape 4.5 : Les Guards de Jeu (Routing de sécurité)

Dans un RPG, un utilisateur authentifié ne peut pas jouer tant qu'il n'a pas créé d'avatar. Il nous faut deux guards :
1. `AuthGuard` : Vérifie la présence du token.
2. `HasCharacterGuard` : Vérifie si le joueur possède un personnage actif (redirige vers `/creation` sinon).

```bash
ng generate guard core/guards/has-character --implements CanActivateFn
```

```typescript title="src/app/core/guards/has-character.guard.ts"
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { GameStateService } from '../services/game-state.service'; // À créer en phase 6

export const hasCharacterGuard: CanActivateFn = () => {
  const gameState = inject(GameStateService);
  const router = inject(Router);

  // Si le signal du personnage est peuplé, on passe
  if (gameState.character()) {
    return true;
  }

  // Sinon redirection vers l'écran de création
  return router.createUrlTree(['/character-creation']);
};
```

## Conclusion de la Phase 4

L'architecture client Stateless est prête :
- ✅ **Gestion sécurisée des Tokens** via le LocalStorage.
- ✅ **Intercepteur HTTP** configuré pour attacher automatiquement le `Bearer token`.
- ✅ **Guards conditionnels** prêts à protéger les écrans de jeu.

Dans la **Phase 5**, nous allons concevoir l'interface graphique de notre jeu : la création de personnage, l'affichage du joueur (HUD, HP/MP), et l'écran de combat !

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un token Sanctum n'est pas infaillible : il peut être volé, exposé dans les logs ou partagé. Les bonnes pratiques de sécurité incluent une expiration courte (`tokenExpiresIn`), la révocation à la déconnexion, et la limitation des permissions par token (`can('read-posts')`). Un token root non expirant exposé accidentellement est une catastrophe.

> [Sécurité des tokens maîtrisée. Construisez maintenant les endpoints REST de l'application →](./05-phase5.md)
