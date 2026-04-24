---
description: "Initialisation du projet Angular 21, configuration de l'authentification basée sur Signals et mise en place des Interceptors."
icon: lucide/book-open-check
tags: ["ANGULAR", "SIGNALS", "SPA", "FRONTEND", "INTERCEPTOR"]
---

# Phase 4 : Setup Angular 21 + Signals

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1h30 - 2h">
</div>

## Objectif de la Phase

> Notre API Laravel (Backend) est opérationnelle. Il est temps de construire l'interface utilisateur. Pour une plateforme SaaS de Pentest exigeant une grande réactivité et une expérience utilisateur fluide, nous choisissons **Angular 21**. Cette phase couvre la création du projet, la mise en place du routing, l'installation d'Angular Material et l'implémentation de la logique d'authentification en utilisant le nouveau paradigme de gestion d'état : les **Signals**.

## Étape 4.1 : Création du Projet Angular 21

Assurez-vous d'avoir la dernière version du CLI Angular installée globalement :

```bash
# Installer ou mettre à jour Angular CLI
npm install -g @angular/cli@21

# Se placer à la racine (en dehors du dossier Laravel saas-pentest)
# Créer l'application frontend (Standalone components par défaut)
ng new pentest-platform --routing --style=scss

cd pentest-platform
```

Angular utilise désormais les **Standalone Components** par défaut, éliminant le besoin fastidieux de déclarer les composants dans des `NgModules`.

## Étape 4.2 : Configuration du Proxy de Développement

En développement, votre frontend tourne sur `http://localhost:4200` et l'API sur `http://localhost:8000`. Bien que nous ayons configuré CORS côté Laravel, l'utilisation d'un proxy Angular simplifie énormément la gestion des cookies de session Sanctum (évitant de devoir configurer `withCredentials` partout).

Créez un fichier `proxy.conf.json` à la racine de votre projet Angular :

```json title="proxy.conf.json"
{
  "/api": {
    "target": "http://localhost:8000",
    "secure": false,
    "changeOrigin": true
  },
  "/sanctum": {
    "target": "http://localhost:8000",
    "secure": false,
    "changeOrigin": true
  }
}
```

Mettez à jour `angular.json` pour utiliser ce proxy au démarrage :

```json title="angular.json"
"architect": {
  "serve": {
    "builder": "@angular-devkit/build-angular:dev-server",
    "options": {
      "proxyConfig": "proxy.conf.json"
    }
  }
}
```

Désormais, une requête HTTP vers `/api/user` depuis Angular sera redirigée de manière transparente vers `http://localhost:8000/api/user`.

## Étape 4.3 : Installation d'Angular Material

Pour concevoir rapidement un dashboard professionnel, propre et accessible, nous intégrons Angular Material.

```bash
ng add @angular/material
```

Répondez aux questions :
- Choisissez un thème (ex: Indigo/Pink ou Custom).
- Activez la typographie globale.
- Activez les animations.

## Étape 4.4 : Le AuthService propulsé par Signals

Historiquement, l'état d'authentification était géré via des `BehaviorSubject` (RxJS). Angular 21 introduit les **Signals**, offrant une syntaxe beaucoup plus simple, synchrone et exempte de fuites de mémoire.

Créons notre service d'authentification :

```bash
ng generate service core/services/auth
```

```typescript title="src/app/core/services/auth.service.ts"
import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { User } from '../../shared/models/user.model'; // À créer

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);

  // Le State (Signal)
  // undefined = en cours de chargement, null = non authentifié, User = authentifié
  readonly currentUser = signal<User | null | undefined>(undefined);

  // Computed Signals (dérivés automatiquement)
  readonly isAuthenticated = computed(() => this.currentUser() !== null && this.currentUser() !== undefined);
  readonly currentTeam = computed(() => this.currentUser()?.current_team);
  
  // Login via Sanctum (Stateful)
  login(credentials: any) {
    return this.http.get('/sanctum/csrf-cookie').pipe(
      tap(() => {
        return this.http.post('/login', credentials).subscribe(() => {
          this.fetchUser();
        });
      })
    );
  }

  logout() {
    return this.http.post('/logout', {}).subscribe(() => {
      this.currentUser.set(null); // Mise à jour instantanée du signal
    });
  }

  fetchUser() {
    this.http.get<User>('/api/user').subscribe({
      next: (user) => this.currentUser.set(user),
      error: () => this.currentUser.set(null)
    });
  }
}
```

!!! tip "La Magie des Signals"
    Partout dans vos composants où vous lierez `authService.currentUser()`, Angular mettra automatiquement à jour le DOM sans avoir besoin d'utiliser le pipe `async` ni de gérer de souscriptions (RxJS).

## Étape 4.5 : Le Guard d'Authentification

Nous devons protéger les routes internes du Dashboard. Avec Angular moderne, les Guards sont de simples fonctions injectables.

```bash
ng generate guard core/guards/auth --implements CanActivateFn
```

```typescript title="src/app/core/guards/auth.guard.ts"
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  // Les Signals sont synchrones, la vérification est instantanée
  if (authService.isAuthenticated()) {
    return true;
  }

  // Redirection vers le login si non authentifié
  return router.createUrlTree(['/login']);
};
```

## Étape 4.6 : L'Intercepteur HTTP (CORS & Erreurs)

Même si nous utilisons un proxy en dev, il est recommandé de configurer l'envoi des requêtes avec les *credentials* (cookies) explicitement. Nous gérons aussi les erreurs 401 (Session expirée).

Dans Angular 21 (Standalone), les intercepteurs sont définis sous forme de fonctions.

```bash
ng generate interceptor core/interceptors/auth
```

```typescript title="src/app/core/interceptors/auth.interceptor.ts"
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const authService = inject(AuthService);

  // On s'assure que les cookies sont toujours envoyés
  const clonedRequest = req.clone({
    withCredentials: true
  });

  return next(clonedRequest).pipe(
    catchError((error: HttpErrorResponse) => {
      // Si Laravel renvoie 401 ou 419 (CSRF Token mismatch)
      if (error.status === 401 || error.status === 419) {
        authService.currentUser.set(null); // Déconnecte l'utilisateur côté front
        router.navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
};
```

Il faut ensuite enregistrer cet intercepteur dans `app.config.ts` :

```typescript title="src/app/app.config.ts"
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { routes } from './app.routes';
import { authInterceptor } from './core/interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor])) // Enregistrement ici
  ]
};
```

## Étape 4.7 : Structure du Routing (Lazy Loading)

Pour garantir des performances optimales (chargement rapide), nous mettons en place le *Lazy Loading* pour les différentes sections de la plateforme.

```typescript title="src/app/app.routes.ts"
import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadChildren: () => import('./features/dashboard/dashboard.routes').then(m => m.DASHBOARD_ROUTES)
  },
  {
    path: 'missions',
    canActivate: [authGuard],
    loadChildren: () => import('./features/missions/mission.routes').then(m => m.MISSION_ROUTES)
  }
];
```

## Conclusion de la Phase 4

Votre socle Frontend est désormais solidement arrimé :
- ✅ Projet **Angular 21** Standalone créé.
- ✅ **Proxy** configuré pour communiquer avec l'API Laravel sans encombre.
- ✅ Gestion d'état simplifiée et surpuissante grâce aux **Signals** (`AuthService`).
- ✅ **Intercepteurs** et **Guards** opérationnels pour sécuriser l'accès.

Dans la **Phase 5**, nous allons utiliser la puissance de Material Design et des Signals pour construire l'interface de notre Dashboard de Pentest.
