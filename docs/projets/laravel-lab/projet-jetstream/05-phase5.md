---
description: "Création du Dashboard de Pentest en Angular : Graphiques Chart.js, formulaires Material, tableaux de vulnérabilités réactifs et gestion des Teams."
icon: lucide/book-open-check
tags: ["ANGULAR", "MATERIAL", "DASHBOARD", "UI", "CHARTJS"]
---

# Phase 5 : Interface Dashboard (Angular Signals)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="5h - 7h">
</div>

## Objectif de la Phase

> C'est ici que l'application prend vie. Le backend fournit les données, le frontend les exploite. Nous allons concevoir une **interface de niveau professionnel** avec Angular Material. Cette interface inclura un Dashboard de statistiques (avec graphiques Chart.js), une gestion fluide des Teams (SaaS), des formulaires réactifs pour le CRUD des missions et des vulnérabilités (Findings), et une intégration avancée des Signals pour garantir une fluidité d'affichage à 60 FPS sans le moindre scintillement.

## Étape 5.1 : Layout Principal et Navigation

Commençons par créer l'ossature de l'application : une barre de navigation latérale (Sidenav) et un entête (Toolbar) pour gérer le changement d'équipe (Teams Switcher).

```bash
ng generate component layout/main-layout
```

```html title="src/app/layout/main-layout/main-layout.component.html"
<mat-sidenav-container class="sidenav-container">
  
  <mat-sidenav #sidenav mode="side" opened class="sidenav">
    <div class="logo-container">
      <h2>ShieldPentest</h2>
    </div>
    
    <mat-nav-list>
      <a mat-list-item routerLink="/dashboard" routerLinkActive="active-link">
        <mat-icon matListItemIcon>dashboard</mat-icon>
        <span matListItemTitle>Dashboard</span>
      </a>
      <a mat-list-item routerLink="/missions" routerLinkActive="active-link">
        <mat-icon matListItemIcon>security</mat-icon>
        <span matListItemTitle>Missions</span>
      </a>
      <a mat-list-item routerLink="/teams" routerLinkActive="active-link">
        <mat-icon matListItemIcon>group</mat-icon>
        <span matListItemTitle>Mon Équipe</span>
      </a>
    </mat-nav-list>
  </mat-sidenav>

  <mat-sidenav-content>
    <mat-toolbar color="primary">
      <button mat-icon-button (click)="sidenav.toggle()">
        <mat-icon>menu</mat-icon>
      </button>
      
      <span class="spacer"></span>
      
      <!-- Affichage de l'équipe actuelle via Signal -->
      <span class="team-badge" *ngIf="authService.currentTeam() as team">
        {{ team.name }}
      </span>

      <!-- Menu Profil -->
      <button mat-button [matMenuTriggerFor]="profileMenu">
        {{ authService.currentUser()?.name }}
        <mat-icon>arrow_drop_down</mat-icon>
      </button>
      
      <mat-menu #profileMenu="matMenu">
        <button mat-menu-item>Mon Profil</button>
        <button mat-menu-item (click)="authService.logout()">Déconnexion</button>
      </mat-menu>
    </mat-toolbar>

    <!-- Zone d'affichage dynamique -->
    <div class="content-padding">
      <router-outlet></router-outlet>
    </div>
  </mat-sidenav-content>
  
</mat-sidenav-container>
```

!!! note "Liaison au AuthService"
    Notez l'appel direct aux signaux : `authService.currentTeam()` et `authService.currentUser()`. L'UI se mettra à jour automatiquement dès que ces valeurs changeront.

## Étape 5.2 : Le Dashboard Analytics (Chart.js)

Un outil de cybersécurité nécessite des statistiques claires pour évaluer le niveau de risque global.

```bash
# Installation de Chart.js et de son wrapper Angular
npm install chart.js ng2-charts
ng generate component features/dashboard/dashboard-home
```

Dans notre composant de dashboard, nous allons générer un graphique de distribution des vulnérabilités par sévérité.

```typescript title="src/app/features/dashboard/dashboard-home.component.ts"
import { Component, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { MissionStateService } from '../../core/services/mission-state.service';
import { ChartConfiguration, ChartData, ChartType } from 'chart.js';

@Component({
  selector: 'app-dashboard-home',
  standalone: true,
  imports: [CommonModule, BaseChartDirective, /* ... modules Material */],
  template: `
    <div class="dashboard-grid">
      <!-- Carte des Statistiques Globales -->
      <mat-card>
        <mat-card-header>
          <mat-card-title>Vulnérabilités Actives</mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div class="chart-container">
            <canvas baseChart
              [data]="pieChartData()"
              [type]="pieChartType"
              [options]="pieChartOptions">
            </canvas>
          </div>
        </mat-card-content>
      </mat-card>
    </div>
  `
})
export class DashboardHomeComponent {
  private missionState = inject(MissionStateService);

  // Dérivation automatique (Computed Signal) des données pour le graphique
  public pieChartData = computed<ChartData<'pie'>>(() => {
    const stats = this.missionState.globalStats(); // ex: { critical: 2, high: 5, medium: 12, low: 3 }
    
    return {
      labels: ['Critique', 'Haute', 'Moyenne', 'Basse'],
      datasets: [
        {
          data: [stats.critical, stats.high, stats.medium, stats.low],
          backgroundColor: ['#d32f2f', '#f57c00', '#fbc02d', '#388e3c'],
        }
      ]
    };
  });

  public pieChartType: ChartType = 'pie';
  public pieChartOptions: ChartConfiguration['options'] = { responsive: true };
}
```

## Étape 5.3 : Liste des Missions (Material Data Table)

Le composant liste affichera les missions sous forme de tableau interactif (tri, pagination) avec Material.

```html title="src/app/features/missions/mission-list/mission-list.component.html"
<div class="header-actions">
  <h1>Missions de l'équipe</h1>
  <button mat-raised-button color="primary" routerLink="new">
    <mat-icon>add</mat-icon> Nouvelle Mission
  </button>
</div>

<mat-table [dataSource]="missionState.missions()" class="mat-elevation-z8">

  <ng-container matColumnDef="name">
    <mat-header-cell *matHeaderCellDef> Nom de la Mission </mat-header-cell>
    <mat-cell *matCellDef="let mission"> {{mission.name}} </mat-cell>
  </ng-container>

  <ng-container matColumnDef="status">
    <mat-header-cell *matHeaderCellDef> Statut </mat-header-cell>
    <mat-cell *matCellDef="let mission">
      <span class="status-badge" [class]="mission.status">
        {{ mission.status | uppercase }}
      </span>
    </mat-cell>
  </ng-container>

  <ng-container matColumnDef="dates">
    <mat-header-cell *matHeaderCellDef> Période </mat-header-cell>
    <mat-cell *matCellDef="let mission"> 
      {{mission.start_date | date}} - {{mission.end_date | date}} 
    </mat-cell>
  </ng-container>

  <ng-container matColumnDef="actions">
    <mat-header-cell *matHeaderCellDef> Actions </mat-header-cell>
    <mat-cell *matCellDef="let mission">
      <button mat-icon-button color="primary" [routerLink]="[mission.id]">
        <mat-icon>visibility</mat-icon>
      </button>
    </mat-cell>
  </ng-container>

  <mat-header-row *matHeaderRowDef="displayedColumns"></mat-header-row>
  <mat-row *matRowDef="let row; columns: displayedColumns;"></mat-row>
</mat-table>

<!-- Indicateur de chargement -->
<mat-progress-bar mode="indeterminate" *ngIf="missionState.loading()"></mat-progress-bar>
```

## Étape 5.4 : Formulaire Réactif (Reactive Forms)

Créons le formulaire d'ajout d'une nouvelle vulnérabilité. Les *Reactive Forms* d'Angular sont parfaits pour gérer les validations complexes.

```typescript title="src/app/features/findings/finding-form/finding-form.component.ts"
import { Component, inject } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { FindingStateService } from '../finding-state.service';

@Component({
  selector: 'app-finding-form',
  standalone: true,
  imports: [ReactiveFormsModule, /* Material Modules */],
  templateUrl: './finding-form.component.html'
})
export class FindingFormComponent {
  private fb = inject(FormBuilder);
  private findingState = inject(FindingStateService);

  findingForm = this.fb.nonNullable.group({
    title: ['', [Validators.required, Validators.maxLength(255)]],
    cvss_score: [0, [Validators.required, Validators.min(0), Validators.max(10)]],
    severity: ['medium', Validators.required],
    description: ['', Validators.required],
    poc: ['', Validators.required],
    impact: ['', Validators.required]
  });

  onSubmit() {
    if (this.findingForm.valid) {
      // Le composant délègue la logique au service via un appel asynchrone
      this.findingState.createFinding(this.findingForm.getRawValue());
      // Redirection ou notification de succès...
    }
  }
}
```

## Étape 5.5 : Le CVSS Calculator Interactif

Une fonctionnalité clé d'un outil de pentest est le calcul de score. Au lieu de saisir manuellement "9.8", nous pouvons créer un composant interactif qui met à jour le formulaire principal.

1. **Input / Output** : Le composant enfant (Calculator) recevra les vecteurs d'attaque.
2. **Calcul Réactif** : À l'aide de signaux dérivés (`computed`), le score numérique changera en temps réel lorsque l'utilisateur modifiera un vecteur (ex: Network -> Local).

*(L'implémentation complète du calculateur CVSS v3.1 implique des dizaines de règles mathématiques, nous laissons cela comme composant modulaire à intégrer).*

## Conclusion de la Phase 5

L'interface de l'application SaaS prend forme :
- ✅ **Layout général** avec navigation latérale et gestion de profil.
- ✅ **Tableau de bord visuel** grâce à l'intégration de Chart.js.
- ✅ **Tableaux de données interactifs** avec Material Design.
- ✅ **Formulaires robustes** pour saisir les données critiques (Findings).

L'interface est belle, mais elle doit maintenant communiquer efficacement et de manière asynchrone avec notre Backend Laravel. Ce sera l'objet de la **Phase 6 : Intégration API ↔ Frontend**.
