---
description: "Projet Pratique : Coder une API RESTful d'authentification complète sans état (Stateless) basée sur les JSON Web Tokens (JWT)."
icon: lucide/shield-check
tags: ["PHP", "PROCÉDURAL", "API", "JWT", "SÉCURITÉ"]
status: stable
---

# Projet 12 : API Auth avec JWT (JSON Web Token)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    Aujourd'hui, de plus en plus d'applications n'ont plus de session PHP classique. Votre serveur PHP sert juste d'**API** et discute avec une App Mobile (React Native) ou un Frontend déporté (Vue.js, Nuxt). 
    Puisque PHP ne garde plus la mémoire de qui est connecté (Stateless), c'est au téléphone du client de stocker un Badge Sécurisé (Le Token JWT) et de le montrer au serveur à chaque requête. Apprenez à forger et valider ces badges.

!!! abstract "Objectifs Pédagogiques"
    1.  **Mécanique Stateless** : Comprendre pourquoi l'API ne stocke aucune session utilisateur sur le serveur (Zéro mémoire CPU).
    2.  **Forging (Génération)** : Fabriquer un Jeton JWT en trois blocs (Header, Payload public, Signature).
    3.  **Cryptographie Symétrique** : Comprendre le rôle fondamental du Secret Serveur avec `hash_hmac` (SHA256).
    4.  **Authorization Bearer** : Récupérer le jeton envoyé par le frontend dans les Headers HTTP de la requête.

## 1. Moteur de Cryptographie JWT

Dans un JWT, la donnée au centre (le "Payload") n'est **pas du tout cryptée**, elle est juste encodée en Base64. Le vrai pouvoir magique réside dans la **Signature**. Sans la clé secrète du serveur (Le sel), impossible de générer ou modifier une signature valide.

> Créez un fichier `JwtEngine.php`.

```php
<?php
declare(strict_types=1);

/**
 * FABRIQUE DE JSON WEB TOKENS
 * Aucun Framework, Pur PHP.
 */
class JwtEngine {
    
    // Le secret du Serveur (Ne jamais versionner sur Github !)
    private string $secretServer = 'Kk3y_sUpeR_53cR3te_iNz@rR_#90L!P';
    
    /**
     * Génère un Jeton d'une durée de vie limitée (ex: 1 Heure)
     */
    public function forger(array $payload, int $dureeSecondes = 3600): string {
        
        // Bloc 1 : Le Header (On annonce la couleur algorithmique)
        $header = [
            'typ' => 'JWT',
            'alg' => 'HS256'
        ];
        
        // Bloc 2 : Le Payload (Les données utiles)
        // 'iat' (Issued At) : Timestamp de création
        // 'exp' (Expiration) : Timestamp de fin de vie
        $payload['iat'] = time();
        $payload['exp'] = time() + $dureeSecondes;
        
        // On encode ces deux tableaux JSON sous format Base64 sécurisé pour les URLs
        $base64UrlHeader = $this->base64UrlEncode(json_encode($header));
        $base64UrlPayload = $this->base64UrlEncode(json_encode($payload));
        
        // Bloc 3 : La Grande Signature ! 🔐
        // On colle le Header et le Payload, et on hache ce bloc avec notre Secret Serveur.
        $signature = hash_hmac(
            'sha256',
            $base64UrlHeader . "." . $base64UrlPayload,
            $this->secretServer,
            true
        );
        $base64UrlSignature = $this->base64UrlEncode($signature);
        
        // On retourne le JWT final, les 3 blocs séparés par des point (".")
        return $base64UrlHeader . "." . $base64UrlPayload . "." . $base64UrlSignature;
    }
    
    /**
     * Vérifie la validité mathématique et temporelle d'un Token
     * Retourne le Tableau $payload si valide, false sinon.
     */
    public function decoderSiValide(string $jwt) {
        // Un JWT possède toujours 3 morceaux (X.Y.Z)
        $morceaux = explode('.', $jwt);
        if (count($morceaux) !== 3) {
            return false;
        }
        
        // Déstructuration
        [$headerVenu, $payloadVenu, $signatureVenue] = $morceaux;
        
        // 1. RE-CALUL DE LA SIGNATURE
        // On prend les données claires reçues, et on refait le calcul que seul notre serveur connait.
        $signatureCalculeeLocal = hash_hmac(
            'sha256',
            $headerVenu . "." . $payloadVenu,
            $this->secretServer,
            true // True = Retour binaire pur
        );
        
        // On compare la signature calculée avec la signature envoyée par le Client.
        // Si Hacker a modifié son Payload ("role": "admin" au lieu de "user"), la signature va s'effondrer !
        if (!hash_equals($signatureCalculeeLocal, $this->base64UrlDecode($signatureVenue))) {
            return false; // Falsification ou Mauvais Secret
        }
        
        // 2. VÉRIFICATION DU TEMPS
        $donneesBrutes = json_decode($this->base64UrlDecode($payloadVenu), true);
        if ($donneesBrutes['exp'] < time()) {
            return false; // Token Trop vieux, le Pass Temporel a expiré.
        }
        
        // Tout est parfait, on retourne les données de l'utilisateur !
        return $donneesBrutes;
    }
    
    // --- Utilitaires Internes ---
    private function base64UrlEncode(string $data): string {
        return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
    }
    private function base64UrlDecode(string $data): string {
        return base64_decode(strtr($data, '-_', '+/'));
    }
}
```

## 2. Le Serveur API (Routeur HTTP Stateless)

C'est ici que votre client Javascript va appeler `/api.php?action=login` en envoyant son mot de passe. Il récupérera un gros block JWT (au lieu d'un simple Cookie de Session).

Créez le fichier serveur `api.php`.

```php
<?php
// Désactiver l'affichage d'erreurs HTML car on est une API JSON !
header('Content-Type: application/json');
require_once 'JwtEngine.php';

$jwtWorker = new JwtEngine();

// Fausse Base de Données Utilisateurs V2
$usersFakeDB = [
    'neo@matrix.sys' => ['id' => 1, 'role' => 'admin', 'password_hash' => '$2y$10$wN3nK6K/1t2y8K.G4F1fLuFvS.U8y4Q3qR3c6bL.hS2I2N3v5E5kC'], // = asdfghjk
    'trinity@matrix.sys' => ['id' => 2, 'role' => 'user', 'password_hash' => '$2y$10$wN3nK6K/1t2y8K.G4F1fLuFvS.U8y4Q3qR3c6bL.hS2I2N3v5E5kC'] 
];

// Quel Route on attaque ? (login ou data-privee)
$routeHtp = $_GET['action'] ?? '404';

// ============================================
// ÉTAPE 1 : RÉCUPÉRATION DU JETON (Auth Middleware)
// ============================================

// Les framework Front comme React ou VueJs vont envoyer le Token dans les "Headers" de leur requête Axios
// Sous la forme : "Authorization: Bearer myTokenJWT.xxxxx.yyyyyy"
$headerAuth = getallheaders()['Authorization'] ?? '';
$tokenClient = '';

if (preg_match('/Bearer\s(\S+)/', $headerAuth, $matches)) {
    $tokenClient = $matches[1];
}

// ============================================
// ÉTAPE 2 : LE ROUTAGE JSON REST API
// ============================================

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $routeHtp === 'login') {
    
    // Récupération du JSON Body (Axios.post) -> Pas dans le super $_POST classique mais dans le flux raw !
    $jsonBrut = file_get_contents('php://input');
    $dataPost = json_decode($jsonBrut, true);
    
    $email = $dataPost['email'] ?? '';
    $pass  = $dataPost['password'] ?? '';
    
    // Tentative de Login (Normalement en vrai avec PDO & password_verify)
    if (isset($usersFakeDB[$email]) && password_verify($pass, $usersFakeDB[$email]['password_hash'])) {
        
        $userDB = $usersFakeDB[$email];
        
        // SUCCÈS :  Le Pass est forgé !
        $payloadMaison = [
            'sub' => $userDB['id'], // 'sub' = Subject Identifier (ID user)
            'email' => $email,
            'role' => $userDB['role']
        ];
        
        $nouveauJwt = $jwtWorker->forger($payloadMaison, 30); // Validité = 30 secondes seulement
        
        echo json_encode([
            'status' => 'success',
            'token' => $nouveauJwt,    // Le Front end l'attrappera et le stockera en LocalStorage !
            'expires_in_seconds' => 30
        ]);
        exit();
        
    } else {
        http_response_code(401); // Unauthorized
        echo json_encode(['status' => 'error', 'message' => "Erreur d'Identifiants."]);
        exit();
    }
}

// ==== LA ROUTE PRIVÉE : REQUIERT UN BADGE ! ====
if ($_SERVER['REQUEST_METHOD'] === 'GET' && $routeHtp === 'profil') {
    
    if (empty($tokenClient)) {
         http_response_code(401);
         echo json_encode(['status' => 'error', 'message' => "Token Manquant. Accès Refusé."]);
         exit();
    }
    
    // Je confie le Badge au vigile JWT
    $donneesDechiffres = $jwtWorker->decoderSiValide($tokenClient);
    
    if (!$donneesDechiffres) {
         http_response_code(403); // Forbidden
         echo json_encode(['status' => 'error', 'message' => "Le Token est Falsifié, Purgé ou Expiré."]);
         exit();
    }
    
    // BINGO, ON A ACCÈS AUX DONNÉES SECRÈTES !
    echo json_encode([
        'status' => 'success',
        'secrete_data' => "Le coffre-fort de la Matrice s'ouvre !",
        'votre_id_decode' => $donneesDechiffres['sub'],
        'votre_role_decode' => $donneesDechiffres['role']
    ]);
    exit();
}

// Default 404
http_response_code(404);
echo json_encode(['error' => 'Endpoint introuvable.']);
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">Puisqu'on n'a pas de Front-End, utilisez <strong>Postman</strong>, <strong>Insomnia</strong> ou juste un petit script d'appel <code>fetch</code> console pour comprendre la mécanique :</p>
  <ul class="space-y-4 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">1</span>
      <span class="text-gray-700">Faites un <code>POST /api.php?action=login</code> avec un Body Raw JSON : <code>{"email": "neo@matrix.sys", "password": "asdfghjk"}</code>. Observez la réponse JSON de l'API. Vous venez de chourrer le fameux <code>eyJ0...</code>.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">2</span>
      <span class="text-gray-700">Déchiffrez votre propre JWT (sans connaitre le mot de passe secret du serveur !) en le collant dans le debugger du site officiel <strong><a href="https://jwt.io/" target="_blank">jwt.io</a></strong>. Vous verrez votre ID, votre rôle et votre Email en clair (Payload data) !</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">3</span>
      <span class="text-gray-700">Allez, tentez d'atteindre la route protégée pendant 30 sec : Faites un <code>GET /api.php?action=profil</code> en mettant bien dans votre outil de requête le Header : <code>Authorization: Bearer VotreeeToooKen...</code>. Le coffre-fort va s'ouvrir.</span>
    </li>
  </ul>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
