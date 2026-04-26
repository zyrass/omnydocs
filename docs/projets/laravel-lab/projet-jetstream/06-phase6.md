---
description: "Connexion de l'application Angular à l'API Laravel via HttpClient, gestion d'état centralisée avec Signals et mises à jour optimistes."
icon: lucide/book-open-check
tags: ["ANGULAR", "SIGNALS", "HTTPCLIENT", "INTEGRATION", "STATE"]
---

# Phase 6 : Intégration API ↔ Frontend

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3h - 4h">
</div>


!!! quote "Analogie pédagogique"
    _Si Breeze est une serrure de maison individuelle, Jetstream est le système de sécurité d'un immeuble de bureaux complet. Il gère non seulement les badges d'accès (authentification), mais aussi les droits par étage (rôles), les équipes (locataires) et la sécurité renforcée (2FA)._

## Objectif de la Phase

> Avoir une belle interface ne suffit pas. Notre application doit communiquer en temps réel avec notre base de données Laravel. Cette phase est fondamentale : nous allons créer les **Services d'État (State Services)** avec Angular Signals pour synchroniser les données de l'API avec notre interface. Nous implémenterons également des mécanismes d'**Optimistic Updates** pour donner l'illusion d'une application instantanée, ainsi qu'une gestion robuste des erreurs (snackbars).

## Étape 6.1 : Définition des Modèles TypeScript

Pour garantir une Type Safety absolue (le grand avantage de TypeScript face au JavaScript classique), nous dupliquons la structure de nos modèles Laravel en interfaces TS.

```typescript title="src/app/shared/models/mission.model.ts"
export interface Mission {
  id: number;
  team_id: number;
  name: string;
  type: 'web' | 'mobile' | 'infrastructure' | 'social_engineering';
  start_date: string;
  end_date: string | null;
  status: 'planning' | 'active' | 'reporting' | 'completed';
  created_at: string;
  // Les relations incluses par l'API Resource
  findings?: Finding[];
}
```

```typescript title="src/app/shared/models/finding.model.ts"
export interface Finding {
  id: number;
  mission_id: number;
  title: string;
  cvss_score: number | null;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  cwe_id: string | null;
  description: string;
  impact: string;
  poc: string;
  status: 'open' | 'fixed' | 'accepted_risk';
  created_at: string;
}
```

## Étape 6.2 : Le Pattern Service d'État avec Signals

Dans les anciennes applications Angular, la gestion d'état passait par des librairies lourdes comme NgRx ou par des `BehaviorSubject` complexes. Avec Angular 21, nous utilisons un **Service d'État basé sur des Signals**.

Ce service a pour rôle de :
1. Faire les appels HTTP.
2. Mettre à jour les Signals locaux.
3. Fournir l'état actuel aux composants sans qu'ils aient besoin de s'abonner (subscribe).

```typescript title="src/app/core/services/mission-state.service.ts"
import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Mission } from '../../shared/models/mission.model';

@Injectable({
  providedIn: 'root'
})
export class MissionStateService {
  private http = inject(HttpClient);

  // 1. Les Signals de base (Writable Signals)
  readonly missions = signal<Mission[]>([]);
  readonly loading = signal<boolean>(false);
  readonly error = signal<string | null>(null);
  readonly selectedMissionId = signal<number | null>(null);

  // 2. Computed Signals (Dérivés automatiques)
  // Se met à jour seul quand `missions` ou `selectedMissionId` change
  readonly selectedMission = computed(() => {
    const id = this.selectedMissionId();
    if (!id) return null;
    return this.missions().find(m => m.id === id) || null;
  });

  readonly activeMissions = computed(() => 
    this.missions().filter(m => m.status === 'active')
  );

  // 3. Méthodes d'action (Mutation de l'état)
  loadMissions() {
    this.loading.set(true);
    this.error.set(null);

    this.http.get<{data: Mission[]}>('/api/missions').subscribe({
      next: (response) => {
        this.missions.set(response.data);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(err.message || 'Erreur de chargement');
        this.loading.set(false);
      }
    });
  }

  selectMission(id: number) {
    this.selectedMissionId.set(id);
  }
}
```

## Étape 6.3 : Optimistic Updates

Lors de la création d'une vulnérabilité (Finding), plutôt que d'attendre la réponse du serveur (qui prend 100-300ms) pour rafraîchir l'interface, nous allons **modifier le state local instantanément** (Optimistic Update) tout en lançant la requête HTTP en arrière-plan.

```typescript title="src/app/core/services/finding-state.service.ts"
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Finding } from '../../shared/models/finding.model';
import { MissionStateService } from './mission-state.service';

@Injectable({
  providedIn: 'root'
})
export class FindingStateService {
  private http = inject(HttpClient);
  private missionState = inject(MissionStateService);
  private snackBar = inject(MatSnackBar);

  createFinding(missionId: number, payload: Partial<Finding>) {
    // 1. Création d'un "Faux" Finding temporaire avec un ID négatif
    const tempFinding: Finding = {
      ...payload,
      id: -Math.floor(Math.random() * 10000), // ID temporaire
      mission_id: missionId,
      created_at: new Date().toISOString()
    } as Finding;

    // 2. Optimistic Update : On ajoute le finding au state IMMÉDIATEMENT
    this.missionState.missions.update(missions => 
      missions.map(mission => {
        if (mission.id === missionId) {
          return {
            ...mission,
            findings: [tempFinding, ...(mission.findings || [])]
          };
        }
        return mission;
      })
    );

    // Notification visuelle de rapidité
    this.snackBar.open('Vulnérabilité enregistrée.', 'OK', { duration: 2000 });

    // 3. Appel HTTP en arrière-plan
    this.http.post<{data: Finding}>(`/api/missions/${missionId}/findings`, payload)
      .subscribe({
        next: (response) => {
          // 4. Succès : On remplace le faux finding par le vrai (avec le bon ID de BDD)
          this.missionState.missions.update(missions => 
            missions.map(mission => {
              if (mission.id === missionId) {
                return {
                  ...mission,
                  findings: (mission.findings || []).map(f => f.id === tempFinding.id ? response.data : f)
                };
              }
              return mission;
            })
          );
        },
        error: (err) => {
          // 5. Erreur : Rollback (On retire le faux finding du state)
          this.missionState.missions.update(missions => 
            missions.map(mission => {
              if (mission.id === missionId) {
                return {
                  ...mission,
                  findings: (mission.findings || []).filter(f => f.id !== tempFinding.id)
                };
              }
              return mission;
            })
          );
          
          this.snackBar.open('Erreur lors de l\'enregistrement. Annulation.', 'Erreur', { duration: 5000 });
        }
      });
  }
}
```

!!! success "Le résultat de l'Optimistic Update"
    Du point de vue de l'utilisateur, l'application réagit en `0ms`. La nouvelle ligne apparaît instantanément dans le tableau, même si le serveur met une seconde à répondre. C'est la marque de fabrique des **applications de classe mondiale (SaaS)**.

## Étape 6.4 : Computed Signals Avancés (Statistiques Auto)

Maintenant que nos Findings sont synchronisés avec l'API, nous pouvons créer des Computed Signals puissants qui recalculeront automatiquement les statistiques du Dashboard dès qu'un Finding est ajouté, modifié ou supprimé.

Ajoutez ceci dans `MissionStateService` :

```typescript
  // Calcule la moyenne CVSS globale de l'équipe
  readonly averageCvssScore = computed(() => {
    let totalScore = 0;
    let count = 0;

    for (const mission of this.missions()) {
      for (const finding of mission.findings || []) {
        if (finding.cvss_score) {
          totalScore += finding.cvss_score;
          count++;
        }
      }
    }

    return count === 0 ? 0 : Number((totalScore / count).toFixed(1));
  });

  // Distribution des sévérités pour Chart.js (Le graphique se mettra à jour en temps réel)
  readonly globalStats = computed(() => {
    const stats = { critical: 0, high: 0, medium: 0, low: 0, info: 0 };

    for (const mission of this.missions()) {
      for (const finding of mission.findings || []) {
        if (stats[finding.severity] !== undefined) {
          stats[finding.severity]++;
        }
      }
    }

    return stats;
  });
```

## Conclusion de la Phase 6

La boucle est bouclée, notre frontend et backend parlent la même langue :
- ✅ **État centralisé** avec les Signals (`signal()`, `computed()`).
- ✅ **Expérience utilisateur instantanée** via les Optimistic Updates.
- ✅ **Type Safety** rigoureuse via les interfaces TypeScript correspondant aux Modèles Laravel.
- ✅ **Graphiques dynamiques** recalculés automatiquement grâce aux Computed Signals.

Dans la **Phase 7**, nous verrons comment exporter tout le travail du Pentester sous forme d'un **rapport PDF professionnel** généré côté serveur.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les notifications temps réel (WebSockets via Pusher ou Laravel Reverb) transforment une application CRUD statique en plateforme collaborative vivante. Le choix architectural critique : broadcast depuis une Queue pour ne jamais bloquer la réponse HTTP, et écouter côté client uniquement sur les canaux auxquels l'utilisateur a accès.

> [Temps réel maîtrisé. Affinez les performances avec les requêtes optimisées et la mise en cache →](./07-phase7.md)
