---
description: "Projet Pratique POO : Développer un connecteur HTTP distant (API Rest) et anticiper les coupures réseaux avec un système de relance automatique (Retry) basé sur les Exceptions (Try/Catch)."
icon: lucide/network
tags: ["PHP", "POO", "EXCEPTIONS", "API", "RÉSEAU"]
status: stable
---

# Projet 23 : Client API Bouncer (Retry Logic)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    Le réseau est instable par nature. Quand votre Backend PHP demande d'encaisser un paiement chez Stripe, il arrive que leur API ne réponde pas assez vite (Timeout) ou que vous ayez cliqué 200 fois (Rate Limite : Erreur 429).
    Un bon ingénieur Backend de niveau Masterclass encapsulera toujours sa requête réseau dans un *Retry Bouncer* : Une boucle de `Try-Catch` qui relance intelligemment la requête avant de déclarer Forfait.

!!! abstract "Objectifs Pédagogiques"
    1.  **Typage d'erreurs HTTP** : Générer une famille stricte d'exceptions HTTP (`ApiTimeoutException`, `ApiRateLimitException`).
    2.  **La Boucle Infernale controlée** : Lancer un `while` loop bridé au nombre d'essais (ex: `maxRetries = 3`).
    3.  **L'Escalade Temporelle (Backoff)** : Intercepter le coup (Catch) pour ordonner au code d'attendre 2 secondes (`sleep(2)` et `continue;`), puis de retenter sa chance. 

## 1. Création des Objets Erreurs API

De la même manière que HTTP dispose des Codes 4xx et 5xx, developpons l'équivalent Orienté Objet en PHP.

```php
<?php
declare(strict_types=1);

// L'Apex : Si on veut tout intercepter d'un bloc sans réfléchir
class ApiException extends Exception {}

// Les Classes Enfants
class ApiTimeoutException extends ApiException {}
class ApiRateLimitException extends ApiException {}
class ApiAuthenticationException extends ApiException {}
class ApiNotFoundException extends ApiException {}
?>
```

## 2. Le Client API "Blindé"

Cette Classe effectue une vraie requête HTTP grâce à `file_get_contents` orienté *Stream*. Si le serveur craque, elle "amortit" l'Exception et lance automatiquement un `sleep()` pour relancer la machine sans même perturber la fonction principale de votre application métier en aval !

```php
<?php
declare(strict_types=1);

require_once 'ApiExceptions.php';

class ResilientApiClient {
    
    // --- Configuration Interne de la Mécanique
    private string $baseUrl;
    private string $apiKey;
    
    private int $requestTimeoutMs = 10; // On lâche l'affaire si ça met plus de 10s à répondre
    private int $maxAttempts = 3;       // L'obstination
    
    public function __construct(string $baseUrl, string $apiKey) {
        $this->baseUrl = rtrim($baseUrl, '/');
        $this->apiKey = $apiKey;
    }
    
    // ============================================
    // LE MOTEUR CATCH/RETRY (BOUNCER LOGIC)
    // ============================================
    
    public function queryGet(string $endpoint): array {
        
        $attempt = 0;
        $lastExceptionMemory = null; // On va retenir le dernier coup reçu.
        
        while ($attempt < $this->maxAttempts) {
            
            $attempt++;
            
            try {
                // Si ça marche direct (Coup de chance), ça "return" et stoppe NET la boucle while en renvoyant le tableau JSON !
                return $this->executeLowLevelRequest('GET', $endpoint);
                
            } catch (ApiTimeoutException $e) {
                // Oh non... Le serveur API est lent et a mis plus de 10sec.
                $lastExceptionMemory = $e;
                
                if ($attempt < $this->maxAttempts) {
                    echo "⚠️ [Timeout] Essai $attempt/$this->maxAttempts... On patiente ". ($attempt) ." seconde(s)...\n";
                    // Backoff : Plus on échoue, plus on attend entre deux tentatives (1s.. puis 2s..)
                    sleep($attempt);
                    continue; // ROULE LA BOUCLE !
                }
                
            } catch (ApiRateLimitException $e) {
                $lastExceptionMemory = $e;
                
                // Le serveur nous dit "STOP" (HTTP 429). On va attendre 5 fois plus longtemps !
                if ($attempt < $this->maxAttempts) {
                    echo "🛑 [RateLimit] On va trop vite sur l'API ! Pénalité de " . ($attempt * 5) . " Secondes !\n";
                    sleep($attempt * 5);
                    continue;
                }
            } catch (ApiAuthenticationException $e) {
                // Pas la peine de relancer la boucle pour un mauvais mot de passe ! On sort violemment.
                throw clone $e; 
            }
        }
        
        // --- FIN DE LA BOUCLE ---
        // L'ordinateur vient de rater 3 fois de suite, il jette définitivement l'éponge et informe l'App (Le Contrôleur)
        throw new ApiException(
            "💥 Échec critique et sanglant après {$this->maxAttempts} tentatives. L'API Client rend les armes.",
            0,
            $lastExceptionMemory
        );
    }
    
    // ============================================
    // LA REQUÊTE NATIVE
    // ============================================
    
    private function executeLowLevelRequest(string $method, string $endpoint): array {
        
        $url = $this->baseUrl . '/' . ltrim($endpoint, '/');
        
        $options = [
            'http' => [
                'method' => $method,
                'header' => "Authorization: Bearer {$this->apiKey}\r\n" . "Content-Type: application/json\r\n",
                'timeout' => $this->requestTimeoutMs
            ]
        ];
        
        // On forge la requête HTTP native PHP
        $context = stream_context_create($options);
        
        // Le "@" tait le Warning du moteur Zend PHP si erreur 4xx 5xx car on veut juste traiter avec des Exceptions POO Stylisées
        $responsePayload = @file_get_contents($url, false, $context);
        
        if ($responsePayload === false) {
            
            // ANALYSE FORENSIQUE : Pourquoi $responsePayload est faux ?
            $errorInfo = error_get_last();
            
            if (str_contains($errorInfo['message'] ?? '', 'timeout')) {
                throw new ApiTimeoutException("Délais dépassé vers la cible extraterrestre : $url");
            }
            if (str_contains($errorInfo['message'] ?? '', '429')) {
                throw new ApiRateLimitException("Calmez-vous. HTTP 429.");
            }
            if (str_contains($errorInfo['message'] ?? '', '401')) {
                throw new ApiAuthenticationException("Ceinture Noire Interdite : Clé API incorrecte.");
            }
            
            // Exception par défaut si l'analyse échoue (Erreur Réseau 500, ou pas de Wifi)
            throw new ApiException("Erreur Bas Niveau inconnue vers : $url");
        }
        
        // ==================================
        // ON ARRIVE ICI SEULEMENT EN CAS DE VICTOIRE (200 OK)
        // ==================================
        try {
            // Transforme le Str en Array Associatif. Si le JSON est corrompu, ça THROW la native JsonException direct !
            return json_decode($responsePayload, true, 512, JSON_THROW_ON_ERROR);
        } catch (JsonException $e) {
            // On transforme l'erreur native native en Erreur Domain API
            throw new ApiException("La réponse JSON reçue est incohérente pour nos services.", 0, $e);
        }
    }
}
?>
```

## 3. Le Contrôleur (Au bout de la Chaîne)

Notre module API est magnifique. Regardons qui va devoir s'en servir : Le développeur qui fait la Page Web :

```php
<?php
require_once 'ResilientApiClient.php';

// On branche l'URL d'une API Publique "Lente" qui renvoie du Fake JSON.
$clientStripe = new ResilientApiClient('https://jsonplaceholder.typicode.com', 'api_secret_7777xxx');

echo "<h2>💳 Transaction en cours...</h2>\n";

try {
    
    // Le dévelopeur web ignore totalement que derrière ça va faire des BOUCLES, des sleep() ou planter 2 fois !
    // Si la ligne d'en dessous aboutit, c'est que la 3ème tentative a payé en sous marin.
    $listeDesUtilisateurs = $clientStripe->queryGet('/users');
    
    echo "🟢 Succès Intersidéral !\n";
    echo "Nombre Client Récupérés : " . count($listeDesUtilisateurs) . ".\n";
    echo "Le Premier s'appelle : {$listeDesUtilisateurs[0]['name']} !";
    
} catch (ApiAuthenticationException $e) {
    echo "🔴 Grosse Erreur fatale : Ton passeport n'est pas le bon !";
    
} catch (ApiException $e) {
    // Si on arrive ici, le Bouncer ("Videur de Boite de Nuit") a perdu le combat après ses 3 tentatives Retry et son Backoff.
    // L'outil jette l'éponge et relaye l'échec au développeur final.
    echo "<div style='color:red;'>🚨 CATASTROPHE GLOBALE NETWORK : " . $e->getMessage() . "</div>";
}
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">Vous maitrisez maintenant les blocs <code>Try/Catch</code> pour amortir un choc dans une boucle. Vous êtes à présent capable de dialoguer avec toutes les API du monde sans perturber votre Front-End Angular/React qui attend la donnée.</p>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
