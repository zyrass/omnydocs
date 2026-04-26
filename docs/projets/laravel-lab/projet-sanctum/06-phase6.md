---
description: "Intégration du GameStateService avec Signals, gestion asynchrone des actions de combat et synchronisation des données serveur/client."
icon: lucide/book-open-check
tags: ["ANGULAR", "SIGNALS", "GAME-STATE", "HTTPCLIENT", "LOGIC"]
---

# Phase 6 : Intégration API ↔ Frontend (Game State)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3h - 4h">
</div>


!!! quote "Analogie pédagogique"
    _Sécuriser une API avec Sanctum s'apparente à donner un jeton d'accès temporaire à un livreur. Au lieu de lui donner les clés de la maison (authentification de session), vous lui donnez un badge qui ne permet d'ouvrir que la porte du garage, et qui peut être révoqué à tout moment._

## Objectif de la Phase

> Nous avons notre API backend qui calcule les règles du jeu en toute sécurité, et notre interface Frontend qui est prête à les afficher. Il manque le chef d'orchestre : le **GameStateService**. Contrairement à une application de gestion (SaaS), un jeu ne fait pas d'"Optimistic Updates" sur un combat (le joueur ne sait pas s'il va faire un coup critique ou rater). Le client doit envoyer l'action, **attendre** la résolution du serveur, puis animer les résultats de manière séquentielle.

## Étape 6.1 : Le GameStateService (Signals)

Ce service centralisera l'état du joueur, du combat en cours, et l'historique des actions (logs).

```bash
ng generate service core/services/game-state
```

```typescript title="src/app/core/services/game-state.service.ts"
import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

// Interfaces simplifiées (à placer dans shared/models/)
export interface Character { id: number; name: string; class: string; level: number; current_hp: number; max_hp: number; /* ... */ }
export interface Battle { id: number; monster_id: number; monster_current_hp: number; status: string; monster: any; }

@Injectable({
  providedIn: 'root'
})
export class GameStateService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private readonly API_URL = 'http://localhost:8000/api';

  // --- SIGNALS DE L'ÉTAT DU JEU ---
  readonly character = signal<Character | null>(null);
  readonly currentBattle = signal<Battle | null>(null);
  readonly combatLogs = signal<string[]>([]);
  readonly isActionPending = signal<boolean>(false); // Bloque le bouton Attaquer pendant le chargement

  /**
   * Charge le profil du joueur au démarrage
   */
  loadCharacterProfile() {
    this.http.get<Character>(`${this.API_URL}/characters/my-character`).subscribe({
      next: (char) => this.character.set(char),
      error: () => this.character.set(null) // Pas de perso = Redirection (géré par Guard)
    });
  }

  /**
   * Lance un combat (Explore Dungeon)
   */
  startBattle() {
    this.isActionPending.set(true);
    this.http.post<{message: string, battle: Battle, character: Character}>(`${this.API_URL}/battles/start`, {})
      .subscribe({
        next: (response) => {
          this.character.set(response.character);
          this.currentBattle.set(response.battle);
          this.combatLogs.set([response.message]); // Initialise le log avec "Un Monstre apparaît !"
          
          this.isActionPending.set(false);
          this.router.navigate(['/battle']); // Navigue vers l'arène
        },
        error: (err) => {
          this.isActionPending.set(false);
          // Gérer l'erreur (ex: Déjà en combat, Mort)
        }
      });
  }

  /**
   * Exécute un tour de combat (Attaque)
   */
  attack() {
    if (!this.currentBattle() || this.isActionPending()) return;
    
    this.isActionPending.set(true);
    
    this.http.post<{status: string, logs: string[], battle?: Battle, character: Character}>(
      `${this.API_URL}/battles/attack`, 
      {}
    ).subscribe({
      next: (response) => {
        // 1. Mise à jour des logs (On ajoute les nouveaux au tableau existant)
        this.combatLogs.update(logs => [...logs, ...response.logs]);
        
        // 2. Mise à jour des stats du perso (HP, XP)
        this.character.set(response.character);
        
        // 3. Mise à jour du combat (HP du monstre, statut)
        if (response.battle) {
          this.currentBattle.set(response.battle);
        } else {
          // Si pas de retour 'battle', on met à jour uniquement le statut (ex: victory/defeat)
          this.currentBattle.update(b => b ? { ...b, status: response.status } : null);
        }

        // 4. Si niveau supérieur détecté (XP), on pourrait déclencher un événement ou modal
        // ...

        this.isActionPending.set(false);
      },
      error: () => {
        this.isActionPending.set(false);
      }
    });
  }

  /**
   * Terminer / Quitter l'arène
   */
  clearBattleState() {
    this.currentBattle.set(null);
    this.combatLogs.set([]);
  }
}
```

## Étape 6.2 : Animations de Dégâts (Delay Artificiel)

Dans un jeu vidéo, la **sensation (Game Feel)** est aussi importante que la logique.
Quand le joueur clique sur "Attaquer", le serveur répond en 50ms. Mettre à jour l'interface instantanément n'est pas agréable (on ne voit pas l'action).

Nous allons ajouter un léger délai dans le composant de Combat pour animer séparément l'attaque du joueur, puis la riposte du monstre.

Modifions la méthode `attack()` du `BattleArenaComponent` :

```typescript title="src/app/features/battle/battle-arena.component.ts"
export class BattleArenaComponent {
  gameState = inject(GameStateService);
  
  isPlayerHit = false;
  isMonsterHit = false;

  attack() {
    // Déclenche l'appel réseau
    this.gameState.attack();
    
    // Animation du monstre qui clignote en rouge
    this.isMonsterHit = true;
    setTimeout(() => this.isMonsterHit = false, 300);

    // Pour l'animation du joueur, on écoute les changements de log (approximatif)
    // Dans une version plus poussée, l'API renverrait les actions séparément.
    setTimeout(() => {
       if (this.gameState.currentBattle()?.status === 'in_progress') {
         this.isPlayerHit = true;
         setTimeout(() => this.isPlayerHit = false, 300);
       }
    }, 600); // 600ms plus tard, le joueur se fait frapper
  }
}
```

## Étape 6.3 : Le système de Level Up (Modal)

Lorsque le joueur passe au niveau supérieur, la requête `attack()` renvoie les nouvelles statistiques (`max_hp`, `strength`, etc.). Il est très satisfaisant d'afficher une fenêtre modale (Dialog) félicitant le joueur.

En utilisant `MatDialog` (Angular Material) :

```typescript
// Dans le subscribe() de attack() :
const oldLevel = this.character()?.level || 1;
const newLevel = response.character.level;

if (newLevel > oldLevel) {
  this.dialog.open(LevelUpModalComponent, {
    data: { oldLevel, newLevel, character: response.character }
  });
}
```

## Étape 6.4 : Le Leaderboard

Afficher le classement des meilleurs joueurs crée de la rétention. 
Dans le contrôleur Laravel (`CharacterController`), vous avez une méthode `leaderboard` :

```php title="app/Http/Controllers/Api/CharacterController.php"
public function leaderboard()
{
    // Récupère le Top 10 basé sur l'XP
    $topCharacters = Character::with('user:id,name') // Optionnel si relation
                        ->orderBy('experience', 'desc')
                        ->limit(10)
                        ->get(['id', 'name', 'class', 'level', 'experience']);

    return response()->json($topCharacters);
}
```

Côté Angular, un simple appel HTTP et un tableau Material complèteront la vue Panthéon.

## Conclusion de la Phase 6

L'âme du jeu est là. L'intégration est terminée :
- ✅ **Synchronisation parfaite** via les Signals de l'état du Joueur et de l'état du Combat.
- ✅ **Game Feel** amélioré grâce aux animations et aux retards intentionnels (Timeouts).
- ✅ **Protection totale** : le client ne fait que demander au serveur le résultat de l'action, l'UI s'adapte en conséquence (Server-Authoritative).

La phase de conception principale est finie. Dans la **Phase 7**, nous verrons comment tester ce système complexe (TDD) et optimiser les performances (Redis Cache) pour supporter des centaines de combats simultanés.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les fonctionnalités avancées (upload de fichiers, exports PDF/CSV, notifications par email) doivent systématiquement passer par des queues en production. Une API qui bloque la réponse HTTP pendant 3 secondes pour générer un PDF expose le serveur aux timeouts et aux doubles clics des utilisateurs. Répondez immédiatement avec un ID de job, notifiez quand le traitement est terminé.

> [Fonctionnalités avancées implementées. Renforcez maintenant avec les tests automatisés →](./07-phase7.md)
