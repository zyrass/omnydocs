---
description: "Génération de rapports PDF professionnels côté serveur avec Laravel DOMPDF et téléchargement côté client via Angular."
icon: lucide/book-open-check
tags: ["LARAVEL", "DOMPDF", "PDF", "REPORTING", "API"]
---

# Phase 7 : Génération Rapports PDF

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2h - 3h">
</div>

## Objectif de la Phase

> Le livrable final d'une mission de test d'intrusion est le **Rapport de Sécurité**. Il doit être professionnel, brandé aux couleurs du client, et contenir des graphiques exécutifs ainsi que le détail des vulnérabilités. Nous allons utiliser la librairie `barryvdh/laravel-dompdf` côté Laravel pour générer ce PDF à la volée à partir d'une vue Blade, puis l'envoyer de manière sécurisée (Blob) à notre application Angular.

## Étape 7.1 : Installation et Configuration de DOMPDF

DOMPDF est un convertisseur HTML vers PDF en PHP. Il est extrêmement robuste pour les layouts de type document.

```bash
# Installation du wrapper Laravel pour DOMPDF
composer require barryvdh/laravel-dompdf
```

*(L'auto-discovery de Laravel l'enregistre automatiquement).*

## Étape 7.2 : Création de la Vue Blade pour le PDF

Bien que notre projet utilise Angular en frontend, nous utilisons la puissance du moteur de template **Blade** uniquement pour structurer notre rapport PDF côté backend.

Créez un fichier `resources/views/reports/pentest.blade.php`. N'utilisez **pas** de CDN externes pour le CSS (DOMPDF gère mal les requêtes externes), intégrez le CSS directement dans une balise `<style>`.

```html title="resources/views/reports/pentest.blade.php"
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rapport d'Audit - {{ $mission->name }}</title>
    <style>
        body { font-family: 'Helvetica', 'Arial', sans-serif; color: #333; }
        .page-break { page-break-after: always; }
        .cover-page { text-align: center; margin-top: 150px; }
        .logo { width: 200px; margin-bottom: 50px; }
        .title { font-size: 28px; color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; }
        .subtitle { font-size: 18px; color: #666; margin-top: 20px; }
        .date { margin-top: 100px; font-weight: bold; }
        
        .finding { border: 1px solid #ddd; margin-bottom: 20px; }
        .finding-header { padding: 10px; background-color: #f8f9fa; border-bottom: 1px solid #ddd; }
        .finding-title { font-size: 18px; font-weight: bold; margin: 0; }
        
        .badge { padding: 5px 10px; color: white; font-weight: bold; border-radius: 3px; }
        .badge.critical { background-color: #dc2626; }
        .badge.high { background-color: #ea580c; }
        .badge.medium { background-color: #eab308; color: #333; }
        .badge.low { background-color: #16a34a; }
        
        .finding-body { padding: 15px; }
        h3 { font-size: 14px; text-transform: uppercase; color: #666; margin-top: 0; }
    </style>
</head>
<body>

    <!-- Page de Garde -->
    <div class="cover-page page-break">
        <!-- Remplacer par base64 image pour de meilleures performances PDF -->
        <img src="{{ public_path('images/shield-logo.png') }}" class="logo">
        <h1 class="title">Rapport d'Audit de Sécurité</h1>
        <div class="subtitle">Mission : {{ $mission->name }}</div>
        <div class="subtitle">Client : {{ $mission->team->name }}</div>
        <div class="date">{{ \Carbon\Carbon::parse($mission->end_date)->format('d F Y') }}</div>
    </div>

    <!-- Executive Summary -->
    <div class="page-break">
        <h1 class="title">1. Executive Summary</h1>
        <p>Ce rapport détaille les résultats du test d'intrusion ({{ $mission->type }}) réalisé du {{ $mission->start_date }} au {{ $mission->end_date }}.</p>
        
        <p><strong>Statistiques Globales :</strong></p>
        <ul>
            <li>Critiques : {{ $stats['critical'] }}</li>
            <li>Hautes : {{ $stats['high'] }}</li>
            <li>Moyennes : {{ $stats['medium'] }}</li>
            <li>Basses : {{ $stats['low'] }}</li>
        </ul>
        
        <!-- Intégration d'un graphique (passé en Base64 depuis Angular ou généré en PHP via QuickChart) -->
        @if($chartImage)
            <img src="{{ $chartImage }}" style="width: 100%; max-width: 500px; margin-top: 20px;">
        @endif
    </div>

    <!-- Détail des Vulnérabilités -->
    <div>
        <h1 class="title">2. Détail des Vulnérabilités</h1>
        
        @foreach($mission->findings as $finding)
            <div class="finding {{ $loop->iteration % 2 == 0 ? 'page-break' : '' }}">
                <div class="finding-header">
                    <p class="finding-title">
                        {{ $finding->title }} 
                        <span class="badge {{ $finding->severity }}">{{ strtoupper($finding->severity) }} ({{ $finding->cvss_score }})</span>
                    </p>
                </div>
                <div class="finding-body">
                    <h3>Description</h3>
                    <p>{{ $finding->description }}</p>
                    
                    <h3>Impact</h3>
                    <p>{{ $finding->impact }}</p>
                    
                    <h3>Proof of Concept (PoC)</h3>
                    <pre style="background: #eee; padding: 10px;">{{ $finding->poc }}</pre>
                </div>
            </div>
        @endforeach
    </div>

</body>
</html>
```

## Étape 7.3 : Le Endpoint Laravel de Génération

Créons la logique dans notre API pour assembler les données, compiler la vue Blade, et retourner le PDF sous forme de flux (Stream).

```php title="app/Http/Controllers/Api/ReportController.php"
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Mission;
use Illuminate\Http\Request;
use Barryvdh\DomPDF\Facade\Pdf;

class ReportController extends Controller
{
    public function generatePdf(Request $request, Mission $mission)
    {
        // 1. Autorisation : l'utilisateur doit avoir accès à la mission
        $this->authorize('view', $mission);

        // 2. Eager Loading des données nécessaires
        $mission->load(['team', 'findings' => function($query) {
            $query->orderBy('cvss_score', 'desc'); // Plus critiques en premier
        }]);

        // 3. Calcul des statistiques
        $stats = [
            'critical' => $mission->findings->where('severity', 'critical')->count(),
            'high'     => $mission->findings->where('severity', 'high')->count(),
            'medium'   => $mission->findings->where('severity', 'medium')->count(),
            'low'      => $mission->findings->where('severity', 'low')->count(),
        ];

        // 4. Graphique (Optionnel : envoyé en base64 depuis le front, ou généré ici)
        $chartImage = $request->input('chart_base64', null);

        // 5. Génération du PDF
        $pdf = Pdf::loadView('reports.pentest', [
            'mission' => $mission,
            'stats' => $stats,
            'chartImage' => $chartImage
        ]);

        // Optionnel : configuration du PDF
        $pdf->setPaper('a4', 'portrait');

        // 6. Retourne le PDF en Stream (Pas de sauvegarde sur disque, direct en mémoire)
        return $pdf->stream("Rapport_Audit_{$mission->id}.pdf", [
            "Attachment" => true // Force le téléchargement côté navigateur
        ]);
    }
}
```

## Étape 7.4 : Téléchargement côté Angular (Blob)

Côté Frontend, télécharger un fichier binaire (PDF) généré par une API sécurisée (Sanctum) nécessite une attention particulière. Un simple `<a href="...">` ne fonctionnera pas car il n'enverra pas l'en-tête `Authorization` ou les cookies XSRF correctement (et on ne peut pas intercepter une navigation href avec l'interceptor Angular).

Nous devons faire la requête via `HttpClient` en demandant une réponse de type `blob` (Binary Large Object), puis forcer le téléchargement avec la librairie `file-saver`.

```bash
npm install file-saver
npm install @types/file-saver --save-dev
```

Dans votre composant Angular (`mission-detail.component.ts`) :

```typescript title="src/app/features/missions/mission-detail.component.ts"
import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as saveAs from 'file-saver'; // Import de file-saver

@Component({
  // ...
})
export class MissionDetailComponent {
  private http = inject(HttpClient);
  private snackBar = inject(MatSnackBar);
  
  isGeneratingPdf = false;

  downloadReport(missionId: number) {
    this.isGeneratingPdf = true;
    this.snackBar.open('Génération du PDF en cours...', '', { duration: 3000 });

    // Optionnel : Récupérer le graphique du Dashboard au format Base64
    // const chartCanvas = document.getElementById('myChart') as HTMLCanvasElement;
    // const chartBase64 = chartCanvas.toDataURL('image/png');

    // Requête HTTP en demandant explicitement un blob
    this.http.post(
      `/api/reports/${missionId}/pdf`, 
      { 
        // chart_base64: chartBase64 
      }, 
      { responseType: 'blob' } // CRITIQUE pour télécharger des fichiers binaires
    ).subscribe({
      next: (blob: Blob) => {
        // file-saver force le navigateur à télécharger le fichier
        saveAs(blob, `Rapport_Audit_Mission_${missionId}.pdf`);
        this.isGeneratingPdf = false;
        this.snackBar.open('Téléchargement terminé.', 'OK', { duration: 2000 });
      },
      error: () => {
        this.isGeneratingPdf = false;
        this.snackBar.open('Erreur lors de la génération du rapport.', 'Fermer');
      }
    });
  }
}
```

!!! tip "Astuce Graphiques dans les PDF"
    La librairie DOMPDF ne gère pas l'exécution de JavaScript (donc pas de rendu Chart.js). L'astuce élégante consiste à générer le graphique en canvas sur l'interface Angular, à convertir ce canvas en image Base64 via `toDataURL()`, et à envoyer cette chaîne Base64 au backend lors de la requête PDF. Le backend l'injecte simplement comme un `<img src="...">`.

## Conclusion de la Phase 7

La fonctionnalité de reporting est en place, complétant le workflow de notre plateforme SaaS :
- ✅ **Laravel DOMPDF** configuré et vue Blade structurée (CSS Inline).
- ✅ **API sécurisée** générant un flux de bytes binaire (Stream).
- ✅ **Frontend Angular** récupérant le flux en tant que `Blob` et forçant le téléchargement avec préservation de la session Sanctum.

La prochaine et dernière étape est la **Phase 8 : Tests et Déploiement**.
