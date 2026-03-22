---
description: "Projet Pratique : Apprenez à concevoir un formulaire de contact blindé contre les attaques du Top 10 OWASP (XSS, CSRF, Rate Limiting)."
icon: lucide/mail-warning
tags: ["PHP", "PROCÉDURAL", "SÉCURITÉ", "OWASP", "CSRF", "XSS"]
status: stable
---

# Projet 9 : Formulaire de Contact Blindé

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    Le formulaire de contact, présent sur 99% des sites web, est la 1ère porte d'entrée pour les pirates informatiques. Spam, Déni de Service, Vol de Session (XSS), Soumission Forcée (CSRF).
    Dans ce projet, vous allez monter un formulaire de Classe Militaire. Un script tellement blindé qu'il pourrait être déployé en production demain.

!!! abstract "Objectifs Pédagogiques"
    1.  **Architecture de Défense en Profondeur** : Gérer les Headers de sécurité HTTP en PHP.
    2.  **Jeton CSRF Cryptographique** : Créer un Token unique et indéchiffrable avec `random_bytes` qui valide l'identité du Posteur.
    3.  **Rate Limiting d'Urgence** : Empêcher un bot de soumettre 500 formulaires à la seconde en bloquant temporairement son adresse IP.
    4.  **Assainissement (Sanitization)** : Combiner le type strict PHP, les `filter_var` et le `htmlspecialchars`.

## 1. L'Engine de Sécurité

Nous allons regrouper nos protections dans un fichier unique `formulaire-securise.php`. Mettez-vous dans la peau d'un DevSecOps.

```php
<?php
declare(strict_types=1);

/**
 * MOTEUR DE FORMULAIRE ULTRA-SÉCURISÉ (OWASP Top 10)
 */

session_start();

// ==========================================
// 1. LES HEADERS HTTP DE DÉFENSE NAVIGATEUR
// ==========================================
// Empêche notre site d'être "Aspiré" dans une Iframe sur un site pirate (Clickjacking)
header('X-Frame-Options: DENY');
// Empêche le navigateur d'essayer de "deviner" le contenu d'un fichier (MIME Sniffing)
header('X-Content-Type-Options: nosniff');
// Règle très restrictive : on ne charge que nos propres fichiers CSS et Images
header("Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'");

// ==========================================
// 2. HELPER D'AFFICHAGE : XSS SHIELD
// ==========================================
function e(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

// ==========================================
// 3. CLASSE DE DÉFENSE : CSRF (Cross-Site Request Forgery)
// ==========================================
class BouclierCSRF {
    private const CLE_SESSION = 'jeton_de_securite';
    
    public static function forgerToken(): string {
        // S'il n'y a pas de jeton, on génère une chaîne cryptographique de 32 octets (64 caractères Hex)
        if (!isset($_SESSION[self::CLE_SESSION])) {
            $_SESSION[self::CLE_SESSION] = bin2hex(random_bytes(32));
        }
        return $_SESSION[self::CLE_SESSION];
    }
    
    public static function verifier(string $tokenPropose): bool {
        // On utilise hash_equals au lieu de "===" pour contrer les Timing Attacks (mesure du temps de calcul de CPU)
        return isset($_SESSION[self::CLE_SESSION]) 
            && hash_equals($_SESSION[self::CLE_SESSION], $tokenPropose);
    }
}

// ==========================================
// 4. CLASSE DE DÉFENSE : RATE LIMITING (Anti-Spam / Anti-DDOS basique)
// ==========================================
class GardeArriere {
    private const MAX_TENTATIVES = 3;
    private const PERIODE_ATTENTE = 3600; // 1 heure punition
    
    public static function autoriserPassage(string $adresseIP): bool {
        // Initialisation du tableau d'infractions de cette IP
        if (!isset($_SESSION['infractions'][$adresseIP])) {
            $_SESSION['infractions'][$adresseIP] = [];
        }
        
        $maintenant = time();
        
        // On nettoie l'historique : On retire les infractions datant de plus d'1 heure
        $_SESSION['infractions'][$adresseIP] = array_filter(
            $_SESSION['infractions'][$adresseIP],
            fn($timestamp) => ($maintenant - $timestamp) < self::PERIODE_ATTENTE
        );
        
        // Le pirate a-t-il atteint la limite de son quota d'une heure ?
        if (count($_SESSION['infractions'][$adresseIP]) >= self::MAX_TENTATIVES) {
            return false;
        }
        
        // On enregistre cette nouvelle tentative dans le fichier de police !
        $_SESSION['infractions'][$adresseIP][] = $maintenant;
        return true;
    }
}

// ==========================================
// 5. LE CONTRÔLEUR HTTP STRICT
// ==========================================
$succes = null;
$erreurs = []; // Tableau qui va accumuler les failles de l'utilisateur
$donneesSaines = []; // Tableau d'or : ne contient que de la donnée PURIFIÉE.

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    // ÉTAPE 1 : VÉRIFICATION D'IDENTITÉ (CSRF)
    $tokenFourni = $_POST['csrf_token'] ?? '';
    if (!BouclierCSRF::verifier($tokenFourni)) {
        die("<h1>ALERTE SÉCURITÉ : Tentative de Soumission Falsifiée. Jeton CSRF invalide.</h1>");
    }
    
    // ÉTAPE 2 : VÉRIFICATION SPAMBOT (RATE LIMITING)
    if (!GardeArriere::autoriserPassage($_SERVER['REMOTE_ADDR'])) {
        die("<h1>ALERTE SPAM : Vous avez dépassé la limite autorisée. Revenez dans 1 Heure.</h1>");
    }
    
    // ÉTAPE 3 : VALIDATION DES CHAMPS (Sanitization)
    $nomBrut = trim($_POST['nom'] ?? '');
    if (mb_strlen($nomBrut) < 2) {
        $erreurs['nom'] = "Le nom est trop court, espion !";
    } else {
        $donneesSaines['nom'] = $nomBrut;
    }
    
    $emailBrut = trim($_POST['email'] ?? '');
    if (!filter_var($emailBrut, FILTER_VALIDATE_EMAIL)) {
        $erreurs['email'] = "Format d'adresse e-mail irréalisable.";
    } else {
        $donneesSaines['email'] = $emailBrut;
    }
    
    $msgBrut = trim($_POST['message'] ?? '');
    if (mb_strlen($msgBrut) < 10) {
        $erreurs['message'] = "Votre communication secrète doit faire plus de 10 caractères.";
    } else {
        $donneesSaines['message'] = $msgBrut; // On stocke en brut car on l'échappera lors de l'affichage HTML !
    }
    
    // ÉTAPE 4 : ACTION FINALE
    if (empty($erreurs)) {
        // TODO : Exécuter la requête PDO Insert In Database ici !
        
        $succes = "Votre rapport chiffré a été transmis au QG avec succès.";
        
        // TRÈS IMPORTANT : On détruit le Jeton CSRF pour qu'il ne soit plus jamais réutilisable
        unset($_SESSION['jeton_de_securite']);
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Messagerie Sécurisée</title>
    <style>
        body { font-family: system-ui; background: #0f172a; color: #f8fafc; display:flex; justify-content:center; align-items:center; min-height:100vh; margin:0; }
        .bunker { background: #1e293b; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1); width: 100%; max-width: 500px;}
        h1 { color: #38bdf8; margin-top: 0; text-align: center; font-size: 1.5rem; text-transform: uppercase; letter-spacing: 2px;}
        
        .msg { padding: 15px; border-radius: 6px; margin-bottom: 25px; text-align: center; font-weight: bold; }
        .msg-err { background: rgba(239, 68, 68, 0.1); color: #fca5a5; border: 1px solid #ef4444; }
        .msg-ok { background: rgba(34, 197, 94, 0.1); color: #86efac; border: 1px solid #22c55e;}
        
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #94a3b8; font-size: 0.9rem; text-transform: uppercase;}
        input, textarea { width: 100%; box-sizing: border-box; padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 6px; color: white; transition: all 0.3s;}
        input:focus, textarea:focus { outline: none; border-color: #38bdf8; box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);}
        
        .err-label { color: #fca5a5; font-size: 0.8rem; margin-top: 5px; display: block;}
        
        button { background: #38bdf8; color: #0f172a; border: none; width: 100%; padding: 15px; border-radius: 6px; font-weight: bold; text-transform: uppercase; cursor: pointer; transition: 0.3s;}
        button:hover { background: #0ea5e9; transform: translateY(-2px);}
        
        .audit-info { text-align: center; margin-top: 25px; font-size: 0.75rem; color: #475569; border-top: 1px dashed #334155; padding-top: 15px;}
    </style>
</head>
<body>

<div class="bunker">
    <h1>Transmission Sécurisée</h1>
    
    <?php if ($succes): ?>
        <div class="msg msg-ok">🛡️ <?= e($succes) ?></div>
        <!-- Remise à zéro propre du POST pour ne pas re-remplir le form -->
        <?php $_POST = []; ?>
    <?php endif; ?>

    <!-- Le Formulaire s'envoie sur sa propre adresse web (Method POST obligatoirement pour la sécurité) -->
    <form method="POST">
        
        <!-- 🔥 L'ARME SECRÈTE : LE JETON CSRF MASQUÉ -->
        <input type="hidden" name="csrf_token" value="<?= e(BouclierCSRF::forgerToken()) ?>">
        
        <div class="form-group">
            <label>Nom de Code</label>
            <!-- L'attribut value e(...) fait de la Rémanence (Remet ce qu'il a tapé s'il s'est trompé) -->
            <input type="text" name="nom" value="<?= e($_POST['nom'] ?? '') ?>" required>
            <?php if(isset($erreurs['nom'])): ?> <span class="err-label">⚠️ <?= e($erreurs['nom']) ?></span> <?php endif; ?>
        </div>
        
        <div class="form-group">
            <label>Identifiant Électronique</label>
            <input type="email" name="email" value="<?= e($_POST['email'] ?? '') ?>" required>
            <?php if(isset($erreurs['email'])): ?> <span class="err-label">⚠️ <?= e($erreurs['email']) ?></span> <?php endif; ?>
        </div>
        
        <div class="form-group">
            <label>Communication Chiffrée</label>
            <textarea name="message" rows="5" required><?= e($_POST['message'] ?? '') ?></textarea>
            <?php if(isset($erreurs['message'])): ?> <span class="err-label">⚠️ <?= e($erreurs['message']) ?></span> <?php endif; ?>
        </div>
        
        <button type="submit">Crypter & Transmettre</button>
    </form>
    
    <div class="audit-info">
        🔒 SSL/TLS Requis • Anti-CSRF Actif • Rate Limit: 3/h
    </div>
</div>

</body>
</html>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-2 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Ouvrez les Outils de Développement (F12) dans votre navigateur, onglet <strong>Inspecteur</strong>. Cherchez la balise <code>&lt;form&gt;</code>. Vous verrez un <code>&lt;input type="hidden"&gt;</code> contenant une incroyable chaîne indéchiffrable de 64 caractères. C'est le Token CSRF. Modifiez-la à la main avec F12, déposez un caractère aléatoire et cliquez sur Envoyer. Vous vous faites éjecter par l'Étape 1 et vous recevez l'Alerte de Faux Jeton !.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Spammez le bouton "Transmettre" comme un bot affolée en rafraichissant la page avec F5 pendant 3 secondes. Le Rate Limiter prendra le relais et affichera la page rouge "Alerte Spam".</span>
    </li>
  </ul>
</div>
