---
description: "Création de l'interface graphique du jeu en Angular : Création de personnage, Hub central (Village), Scène de Combat et Animations des barres de statut."
icon: lucide/book-open-check
tags: ["ANGULAR", "UI", "HUD", "ANIMATIONS", "GAME-DEV"]
---

# Phase 5 : Interface Jeu (UI & Animations)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="4h - 5h">
</div>


!!! quote "Analogie pédagogique"
    _Sécuriser une API avec Sanctum s'apparente à donner un jeton d'accès temporaire à un livreur. Au lieu de lui donner les clés de la maison (authentification de session), vous lui donnez un badge qui ne permet d'ouvrir que la porte du garage, et qui peut être révoqué à tout moment._

## Objectif de la Phase

> Un jeu nécessite une interface très spécifique (HUD). Fini les tableaux Material de Jetstream, nous allons créer une interface sombre, immersive, inspirée des RPG classiques. Nous aborderons la création de l'écran de sélection de classe, du "Village" (hub central), et surtout de l'écran de "Combat" avec ses barres de Points de Vie (HP/MP) dynamiques et le journal des événements (Combat Logs) en autoscroll.

## Étape 5.1 : Écran de Création de Personnage

C'est le premier écran que voit un nouveau joueur.

```html title="src/app/features/character/creation/creation.component.html"
<div class="creation-container">
  <h1 class="title-fantasy">Forgez votre Destinée</h1>

  <form [formGroup]="charForm" (ngSubmit)="createCharacter()" class="creation-form">
    
    <div class="input-group">
      <label>Nom du Héros</label>
      <input type="text" formControlName="name" placeholder="Ex: Arthas" maxlength="20">
    </div>

    <div class="class-selector">
      <!-- Choix de la classe avec style visuel dynamique -->
      <div class="class-card" 
           [class.selected]="charForm.get('class')?.value === 'warrior'"
           (click)="selectClass('warrior')">
        <img src="assets/icons/sword.png" alt="Guerrier">
        <h3>Guerrier</h3>
        <p>Haute Force & Défense. Faible Agilité.</p>
      </div>

      <div class="class-card" 
           [class.selected]="charForm.get('class')?.value === 'mage'"
           (click)="selectClass('mage')">
        <img src="assets/icons/staff.png" alt="Mage">
        <h3>Mage</h3>
        <p>Haute Intelligence. Faible Défense.</p>
      </div>

      <div class="class-card" 
           [class.selected]="charForm.get('class')?.value === 'rogue'"
           (click)="selectClass('rogue')">
        <img src="assets/icons/dagger.png" alt="Voleur">
        <h3>Voleur</h3>
        <p>Haute Agilité (Esquive). Force Moyenne.</p>
      </div>
    </div>

    <button type="submit" [disabled]="charForm.invalid" class="btn-primary">
      Entrer dans le Donjon
    </button>
  </form>
</div>
```

## Étape 5.2 : Le HUD (Heads Up Display) et Barres de Vie

Nous allons créer un composant réutilisable pour afficher les barres de statut avec une transition CSS fluide.

```bash
ng generate component shared/components/status-bar
```

```html title="src/app/shared/components/status-bar/status-bar.component.html"
<div class="status-bar-container">
  <div class="label">
    <span>{{ label }}</span>
    <span>{{ current }} / {{ max }}</span>
  </div>
  <div class="bar-background">
    <!-- La largeur change dynamiquement, le CSS gère la transition -->
    <div class="bar-fill" 
         [style.width.%]="percentage" 
         [style.background-color]="color">
    </div>
  </div>
</div>
```

```typescript title="src/app/shared/components/status-bar/status-bar.component.ts"
import { Component, Input, computed, signal } from '@angular/core';

@Component({
  selector: 'app-status-bar',
  standalone: true,
  templateUrl: './status-bar.component.html',
  styleUrls: ['./status-bar.component.scss']
})
export class StatusBarComponent {
  @Input() label = 'HP';
  @Input() color = '#e74c3c'; // Rouge par défaut
  @Input() current = 0;
  @Input() max = 100;

  get percentage() {
    return Math.max(0, Math.min(100, (this.current / this.max) * 100));
  }
}
```

## Étape 5.3 : Le Hub Central (Le Village)

Le village est le point de repli. Il affiche les statistiques du joueur et offre la possibilité de lancer une mission (Combat).

```html title="src/app/features/village/village.component.html"
<div class="village-layout">
  
  <!-- Panneau de gauche : Profil du Joueur -->
  <aside class="player-profile" *ngIf="gameState.character() as char">
    <div class="avatar-box">
      <img [src]="'assets/avatars/' + char.class + '.png'" alt="Avatar">
      <h2>{{ char.name }} (Lvl {{ char.level }})</h2>
      <p class="class-label">{{ char.class | titlecase }}</p>
    </div>

    <div class="stats-box">
      <app-status-bar label="HP" color="#e74c3c" [current]="char.current_hp" [max]="char.max_hp"></app-status-bar>
      <app-status-bar label="MP" color="#3498db" [current]="char.current_mp" [max]="char.max_mp"></app-status-bar>
      <app-status-bar label="XP" color="#f1c40f" [current]="char.experience" [max]="char.level * 100 * 1.5"></app-status-bar>
      
      <div class="attributes grid">
        <div>⚔️ Force: {{ char.strength }}</div>
        <div>🛡️ Déf: {{ char.defense }}</div>
        <div>✨ Int: {{ char.intelligence }}</div>
        <div>🏃 Agi: {{ char.agility }}</div>
      </div>
    </div>
  </aside>

  <!-- Panneau de droite : Actions -->
  <main class="village-actions">
    <h1>Le Village</h1>
    <p>Vous êtes en sécurité ici. Préparez-vous avant de repartir.</p>

    <div class="action-buttons">
      <!-- Appel API Start Battle -->
      <button class="btn-danger large" (click)="exploreDungeon()">
        🔥 Explorer le Donjon (Combat)
      </button>
      
      <button class="btn-secondary large">
        🏥 Se reposer (Auberge)
      </button>
      
      <button class="btn-secondary large" routerLink="/leaderboard">
        🏆 Panthéon (Classement)
      </button>
    </div>
  </main>
</div>
```

## Étape 5.4 : La Scène de Combat (Battle Arena)

Le cœur du jeu ! Une disposition en écran splitté avec le monstre à droite, le joueur à gauche, et les logs au centre.

```html title="src/app/features/battle/battle-arena.component.html"
<div class="arena-container" *ngIf="gameState.currentBattle() as battle">
  
  <div class="combatants-row">
    
    <!-- Zone du Joueur -->
    <div class="player-zone" *ngIf="gameState.character() as char">
      <div class="sprite-container">
        <!-- Application d'une animation CSS si le joueur subit des dégâts -->
        <img [src]="'assets/avatars/' + char.class + '.png'" 
             [class.shake]="isPlayerHit" 
             class="sprite">
      </div>
      <div class="combat-stats">
        <h3>{{ char.name }} (Lvl {{ char.level }})</h3>
        <app-status-bar color="#e74c3c" [current]="char.current_hp" [max]="char.max_hp"></app-status-bar>
      </div>
    </div>

    <!-- Zone du Monstre -->
    <div class="monster-zone" *ngIf="battle.monster as monster">
      <div class="combat-stats text-right">
        <h3>{{ monster.name }} (Lvl {{ monster.level }})</h3>
        <app-status-bar color="#e74c3c" [current]="battle.monster_current_hp" [max]="monster.max_hp"></app-status-bar>
      </div>
      <div class="sprite-container">
        <!-- Application d'une animation CSS si le monstre subit des dégâts -->
        <img [src]="'assets/monsters/' + monster.type + '.png'" 
             [class.flash-red]="isMonsterHit" 
             class="sprite">
      </div>
    </div>

  </div>

  <!-- Combat Logs (Auto-scroll) -->
  <div class="combat-log-box" #logContainer>
    <p *ngFor="let log of gameState.combatLogs()">
      {{ log }}
    </p>
  </div>

  <!-- Actions Panel -->
  <div class="actions-panel" *ngIf="battle.status === 'in_progress'">
    <button class="btn-attack" (click)="attack()" [disabled]="isAttacking">
      ⚔️ Attaquer
    </button>
    <button class="btn-magic" disabled>
      ✨ Magie (WIP)
    </button>
    <button class="btn-flee" (click)="flee()">
      🏃 Fuir
    </button>
  </div>

  <!-- Écran de Fin (Victoire/Défaite) -->
  <div class="battle-end-overlay" *ngIf="battle.status === 'victory' || battle.status === 'defeat'">
    <div class="end-card">
      <h1 [class.text-victory]="battle.status === 'victory'" 
          [class.text-defeat]="battle.status === 'defeat'">
        {{ battle.status === 'victory' ? 'VICTOIRE !' : 'VOUS ÊTES MORT...' }}
      </h1>
      <button class="btn-primary" (click)="returnToVillage()">Retour au Village</button>
    </div>
  </div>

</div>
```

!!! tip "Autoscroll du Combat Log"
    Pour que le journal des événements reste toujours affiché sur la dernière ligne après une attaque, utilisez le Lifecycle Hook d'Angular :
    ```typescript
    @ViewChild('logContainer') private logContainer!: ElementRef;
    
    scrollToBottom(): void {
      try {
        this.logContainer.nativeElement.scrollTop = this.logContainer.nativeElement.scrollHeight;
      } catch(err) { }
    }
    // Appeler scrollToBottom() juste après avoir ajouté un log.
    ```

## Conclusion de la Phase 5

Le jeu possède désormais une interface digne d'un RPG classique :
- ✅ L'écran de création instancie le bon visuel selon la classe choisie.
- ✅ Le **composant StatusBar** gère les transitions CSS pour des barres de vie animées (fluides).
- ✅ Le **Layout de Combat** est asymétrique, immersif, et gère les états de fin de partie (Overlay).
- ✅ Le journal de combat retranscrit l'action calculée par le backend.

Dans la **Phase 6**, nous lierons l'intelligence de ces interfaces avec la vraie logique de l'API grâce au `GameStateService` basé sur les Signals.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La conception des endpoints REST doit anticiper les besoins du client dès le début : filtrage, pagination, tri, et inclusion conditionnelle de relations (`?include=posts`). Laravel API Resources permettent de versionner ces structures sans casser les clients existants. Un endpoint mal versionnéest la source numéro un de conflits lors des montées de version.

> [API REST structurée. Implementez maintenant les fonctionnalités avancées (upload, exports) →](./06-phase6.md)
