---
description: "Projet Pratique : Apprenez à architecturer un fichier helper contenant des dizaines de fonctions pures (Échappement, CSRF, Regex, Random password) pour accélérer vos futurs développements."
icon: lucide/library
tags: ["PHP", "PROCÉDURAL", "FONCTIONS", "SÉCURITÉ", "REGEX"]
status: stable
---

# Projet 5 : Bibliothèque Utilitaires

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="8.3"
  data-time="1 Heure">
</div>

!!! quote "Le Pitch"
    A force de réécrire les mêmes blocs de code (Générer un mot de passe, Échapper XSS, Formater une Date française), on perd un temps précieux.
    Dans ce projet, vous allez créer `utilities.php`. Ce sera **votre boîte à outils de Dév PHP**. Vous l'inclurez (`require_once`) en tête de tous vos futurs projets.

!!! abstract "Objectifs Pédagogiques"
    1.  **Architecture Helper** : Grouper les fonctions par thématique (Sécurité, Formatage, Validation) avec des commentaires DocBlock PHP professionnels.
    2.  **Sécurité CSRF & XSS** : Créer l'indispensable fonction de vérification de Jeton (Token) pour protéger les formulaires contre la falsification de session.
    3.  **Expressions Régulières (Regex)** : Valider mathématiquement la solidité d'un mot de passe injecté.
    4.  **Génération Aléatoire** : Exploiter la librairie cryptographique PHP native (`random_bytes`).

## 1. La Boîte à Outils (utilities.php)

Créez le fichier `utilities.php`. Il ne contient AUCUN HTML. Il ne fait qu'exposer des fonctions à d'autres scripts.

```php
<?php
declare(strict_types=1);

/**
 * Bibliothèque de fonctions utilitaires sécurisées
 * 
 * @version 1.0.0
 */

// ============================================
// FONCTIONS SÉCURITÉ
// ============================================

/**
 * Échappe HTML pour prévenir XSS
 */
function e(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

/**
 * Valide une adresse email via le filtre NATIF PHP (Plus performant qu'une Regex)
 */
function validerEmail(string $email): bool {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Génère un token CSRF sécurisé (Cryptographie moderne)
 */
function genererTokenCSRF(): string {
    if (!isset($_SESSION['csrf_token'])) {
        // Crée 32 octets aléatoires et les convertit en format Hexadécimal lisible
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Vérifie le token CSRF lors de la soumission du POST
 */
function verifierTokenCSRF(string $token): bool {
    return isset($_SESSION['csrf_token']) 
        && hash_equals($_SESSION['csrf_token'], $token); // hash_equals prévient les attaques temporelles (Timing Attack)
}

/**
 * Tranche le gras d'une chaîne envoyée par un form
 */
function nettoyer(string $input): string {
    return trim(strip_tags($input));
}

// ============================================
// FONCTIONS VALIDATION & REGEX
// ============================================

/**
 * Valide un mot de passe fort via Regex (Expressions Régulières)
 * 
 * Critères :
 * - Min 8 caractères
 * - Au moins 1 majuscule [A-Z]
 * - Au moins 1 minuscule [a-z]
 * - Au moins 1 chiffre [0-9]
 * - Au moins 1 caractère spécial
 */
function estMotDePasseFort(string $password): bool {
    if (strlen($password) < 8) return false;
    
    $patterns = [
        '/[A-Z]/',      // Majuscule
        '/[a-z]/',      // Minuscule
        '/[0-9]/',      // Chiffre
        '/[^A-Za-z0-9]/' // Spécial
    ];
    
    foreach ($patterns as $pattern) {
        if (!preg_match($pattern, $password)) {
            return false;
        }
    }
    
    return true;
}

// ============================================
// FONCTIONS FORMATAGE
// ============================================

/**
 * Formatage comptable Euro
 */
function formaterPrix(float $montant, int $decimales = 2): string {
    return number_format($montant, $decimales, ',', ' ') . ' €';
}

/**
 * Génère un slug propre pour les URL de vos futurs articles de blog !
 */
function genererSlug(string $texte): string {
    $slug = mb_strtolower($texte);
    $slug = iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $slug); // Fait sauter les accents
    $slug = preg_replace('/[^a-z0-9]+/', '-', $slug); // Remplace les espaces et spéciaux par des tirets
    return trim($slug, '-');
}

// ============================================
// FONCTIONS HELPER SYSTÈME
// ============================================

/**
 * Redirection HTTP brute (Type de retour 'never' car elle tue le script)
 */
function rediriger(string $url): never {
    header("Location: $url");
    exit();
}

/**
 * Générateur de mot de passe aléatoire
 */
function genererMotDePasse(int $longueur = 12): string {
    $caracteres = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()';
    $password = '';
    
    for ($i = 0; $i < $longueur; $i++) {
        // Tire un chiffre aléatoire entre 0 et la taille du dictionnaire (strlen)
        $password .= $caracteres[random_int(0, strlen($caracteres) - 1)];
    }
    
    return $password;
}

/**
 * La Fonction Suprême : Le "Dump and Die" (dd)
 * Affiche proprement le contenu (Array/Objet/String) et tue la page.
 * Utilisée intensivement en Audit et Débug.
 */
function dd(mixed $variable, bool $die = true): void {
    echo '<pre style="background:#0f172a;color:#38bdf8;padding:15px;border-radius:5px;font-size:14px;box-shadow:0 4px 6px rgba(0,0,0,1)">';
    var_dump($variable);
    echo '</pre>';
    
    if ($die) die();
}
?>
```

## 2. L'Interface de Tests

Créez `test_utilities.php`. Nous allons exiger la boîte à outils (`require_once`) et jouer avec. C'est l'équivalent d'un Unittest humain.

```php
<?php
declare(strict_types=1);

// 1. INJECTION DE LA LIBRAIRIE
require_once 'utilities.php';

// Si le fichier Utilities manque, PHP va Fatal Error ici et couper court.
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Tests Boîte à Outils PHP</title>
    <style>body { font-family: system-ui; padding: 40px; } h2 {color:#2563eb; border-bottom:2px solid #bfdbfe; padding-bottom:10px}</style>
</head>
<body>
    <h1>Tests Bibliothèque Utilitaires</h1>

    <h2>e() - Sécurité XSS</h2>
    <?php 
        $input = '<script>alert("Je suis un hacker")</script>';
        echo "Input Brut : " . e($input) . "<br>"; 
    ?>

    <h2>validerEmail()</h2>
    <?php
        $emails = ['contact@omnyvia.com', 'invalid-email', 'bob@test'];
        foreach ($emails as $email) {
            $valide = validerEmail($email) ? '✅ Correct' : '❌ Rejeté';
            echo "$valide : $email<br>";
        }
    ?>

    <h2>estMotDePasseFort()</h2>
    <?php
        $passwords = ['1234', 'password', 'Pass123!', 'OmegaLul123!@#'];
        foreach ($passwords as $pwd) {
            $fort = estMotDePasseFort($pwd) ? '✅ Fort' : '❌ Faible';
            echo "$fort : $pwd<br>";
        }
    ?>

    <h2>formaterPrix()</h2>
    <?php
        echo "Prix : " . formaterPrix(12543.56) . "<br>";
        echo "Prix Gros : " . formaterPrix(999000.99, 2) . "<br>";
    ?>

    <h2>genererSlug()</h2>
    <?php
        echo "Slugifier : " . genererSlug("Maçonnerie Générale & Rénovation ! ") . "<br>";
    ?>

    <h2>genererMotDePasse()</h2>
    <?php
        for ($i = 0; $i < 3; $i++) {
            echo genererMotDePasse(16) . "<br>";
        }
    ?>
</body>
</html>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-2 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Vous avez appelé <code>genererSlug("Maçonnerie Générale & Rénovation ! ")</code> et le PHP a renvoyé l'URL string parfaite <code>maconnerie-generale-renovation</code>.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Le Mot de passe "Pass123!" est recalé par la Regex car il lui manque 1 caractère pour faire la taille minimale de 8.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Le <code>require_once</code> évite que PHP lève une redéclaration fatale si vous tentez de l'inclure une seconde fois par mégarde dans le même script.</span>
    </li>
  </ul>
</div>
