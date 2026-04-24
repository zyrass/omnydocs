---
description: "Création des routes API, des contrôleurs, de la validation des requêtes et de la sérialisation JSON via API Resources."
icon: lucide/book-open-check
tags: ["JETSTREAM", "API", "REST", "JSON", "RESOURCES"]
---

# Phase 3 : Endpoints API REST

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3h - 4h">
</div>

## Objectif de la Phase

> Notre base de données et notre logique métier sont prêtes. Il est temps de les exposer au monde extérieur (notamment à notre future Single Page Application Angular) via une **API RESTful**. Nous allons construire des endpoints standardisés, implémenter une validation stricte des données entrantes, et utiliser les **API Resources** de Laravel pour formater les réponses JSON de manière sécurisée et uniforme.

## Étape 3.1 : Définition des Routes API

Contrairement aux applications classiques qui utilisent `routes/web.php`, nous allons définir nos endpoints dans `routes/api.php`. Les routes définies ici bénéficient automatiquement du préfixe `/api/`.

Ouvrez `routes/api.php` et définissez vos groupes de routes protégés par le middleware Sanctum :

```php title="routes/api.php"
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\MissionController;
use App\Http\Controllers\Api\FindingController;

// Toutes les routes à l'intérieur nécessitent d'être authentifié via Sanctum
Route::middleware('auth:sanctum')->group(function () {
    
    // Obtenir l'utilisateur connecté et son équipe actuelle
    Route::get('/user', function (Request $request) {
        return $request->user()->load('currentTeam');
    });

    // CRUD Missions
    Route::apiResource('missions', MissionController::class);
    
    // Findings relatifs à une mission
    Route::get('/missions/{mission}/findings', [FindingController::class, 'index']);
    Route::post('/missions/{mission}/findings', [FindingController::class, 'store']);
    Route::put('/findings/{finding}', [FindingController::class, 'update']);
    Route::delete('/findings/{finding}', [FindingController::class, 'destroy']);
    
    // Upload d'évidences (images/fichiers)
    Route::post('/findings/{finding}/evidences', [FindingController::class, 'uploadEvidence']);
    
    // Génération du rapport PDF
    Route::get('/reports/{mission}/pdf', [ReportController::class, 'generatePdf']);
});
```

!!! info "Route::apiResource"
    L'utilisation de `Route::apiResource` crée automatiquement les routes pour `index`, `store`, `show`, `update`, et `destroy`, sans créer les routes `create` et `edit` (qui servent uniquement à afficher des formulaires HTML, inutiles dans une API).

## Étape 3.2 : Validation avec les Form Requests

Règle d'or en sécurité : **ne jamais faire confiance aux données envoyées par l'utilisateur**. Nous externalisons la logique de validation dans des Form Requests.

```bash
php artisan make:request StoreFindingRequest
```

```php title="app/Http/Requests/StoreFindingRequest.php"
namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StoreFindingRequest extends FormRequest
{
    public function authorize(): bool
    {
        // La Policy est vérifiée au niveau du contrôleur,
        // donc on peut renvoyer true ici.
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'cvss_score' => ['nullable', 'numeric', 'min:0', 'max:10'],
            'severity' => ['required', Rule::in(['critical', 'high', 'medium', 'low', 'info'])],
            'cwe_id' => ['nullable', 'string', 'regex:/^CWE-\d+$/'],
            'description' => ['required', 'string'],
            'impact' => ['required', 'string'],
            'poc' => ['required', 'string'],
        ];
    }
}
```

## Étape 3.3 : Formatage JSON avec les API Resources

Les API Resources agissent comme une couche de transformation entre vos modèles Eloquent et la réponse JSON finale. Elles permettent de masquer les champs sensibles, de formater les dates, et d'inclure les relations proprement.

```bash
php artisan make:resource FindingResource
```

```php title="app/Http/Resources/FindingResource.php"
namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class FindingResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'mission_id' => $this->mission_id,
            'title' => $this->title,
            'cvss_score' => $this->cvss_score,
            'severity' => $this->severity,
            'cwe_id' => $this->cwe_id,
            'description' => $this->description,
            'impact' => $this->impact,
            'poc' => $this->poc,
            'status' => $this->status,
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),
            // Inclure les relations uniquement si elles sont chargées
            'evidences' => EvidenceResource::collection($this->whenLoaded('evidences')),
        ];
    }
}
```

## Étape 3.4 : Implémentation du Contrôleur

Créons le contrôleur qui assemble la validation, la logique métier et la sérialisation.

```bash
php artisan make:controller Api/FindingController
```

```php title="app/Http/Controllers/Api/FindingController.php"
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Mission;
use App\Models\Finding;
use App\Http\Requests\StoreFindingRequest;
use App\Http\Resources\FindingResource;
use Illuminate\Http\JsonResponse;

class FindingController extends Controller
{
    public function index(Mission $mission)
    {
        // Autorisation (Vérifie si le user appartient à l'équipe de la mission)
        $this->authorize('view', $mission);

        // Récupération des findings avec les évidences préchargées
        $findings = $mission->findings()->with('evidences')->latest()->get();

        return FindingResource::collection($findings);
    }

    public function store(StoreFindingRequest $request, Mission $mission)
    {
        $this->authorize('update', $mission); // Seuls les membres autorisés peuvent ajouter

        $finding = $mission->findings()->create($request->validated());

        return response()->json([
            'message' => 'Vulnérabilité ajoutée avec succès.',
            'data' => new FindingResource($finding),
        ], 201); // 201 Created
    }
}
```

## Étape 3.5 : Upload Sécurisé sur AWS S3 (Évidences)

Les évidences d'un test d'intrusion (captures d'écran, logs) sont hautement confidentielles. Nous allons les stocker sur un bucket privé (S3).

```bash
# Installer le driver S3 pour Flysystem
composer require league/flysystem-aws-s3-v3
```

Dans le contrôleur, ajoutez la méthode d'upload :

```php
public function uploadEvidence(Request $request, Finding $finding)
{
    $this->authorize('update', $finding->mission);

    $request->validate([
        'file' => ['required', 'file', 'mimes:jpg,png,pdf,txt', 'max:10240'], // 10MB max
    ]);

    $file = $request->file('file');
    // Stockage privé dans un bucket (non accessible publiquement via URL)
    $path = $file->storeAs(
        "evidences/{$finding->mission_id}/{$finding->id}", 
        $file->hashName(), 
        's3'
    );

    $evidence = $finding->evidences()->create([
        'file_path' => $path,
        'original_name' => $file->getClientOriginalName(),
        'mime_type' => $file->getMimeType(),
    ]);

    return response()->json($evidence, 201);
}
```

## Conclusion de la Phase 3

L'API REST est désormais opérationnelle :
- ✅ **Endpoints standardisés** mis en place dans `routes/api.php`.
- ✅ **Sécurité assurée** par les Form Requests et les Policies.
- ✅ **Format JSON unifié** et contrôlé grâce aux API Resources.
- ✅ **Upload de fichiers sensibles** sur S3 géré.

Dans la **Phase 4**, nous allons basculer côté Frontend pour initialiser notre projet **Angular 21** et mettre en place la gestion d'état moderne basée sur les **Signals**.
