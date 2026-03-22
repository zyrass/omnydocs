---
description: "Projet Pratique : Construisez votre première application PHP fonctionnelle. Une calculatrice gérant finement le transtypage, la sécurité XSS, et les structures de contrôle (Switch/Match)."
icon: lucide/calculator
tags: ["PHP", "PROCÉDURAL", "MATH", "FORMULAIRE", "SÉCURITÉ"]
---

# Projet 1 : Calculatrice Sécurisée

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="8.3"
  data-time="1 Heure">
</div>

!!! quote "Le Pitch"
    Avant de coder des algorithmes bancaires complexes, apprenons à faire parler deux nombres. Votre mission est de créer une calculatrice web. L'utilisateur saisit deux chiffres dans un formulaire, sélectionne une opération (+, -, *, /) et le serveur PHP lui renvoie la réponse.
    **Le défi :** Empêcher le piratage (XSS) et la destruction locale (Division par Zéro).

!!! abstract "Objectifs Pédagogiques"
    1.  **Récupération GET/POST** : Capter les données envoyées par un visiteur HTML vers le script distant PHP.
    2.  **Transtypage Strict** : Le web n'est que du Texte (String). Transformez ces chaînes en Nombres Flottants (Floats) de manière ultra-sécurisée avec `filter_input()`.
    3.  **Logique de Branchement** : Utiliser la structure `switch()` ou le moderne `match()` de PHP 8 pour diriger le flux mathématique.
    4.  **Échappement XSS** : Nettoyer purement toute sortie serveur vers le navigateur avec `htmlspecialchars`.

## 1. Algorithme Sécurisé

Voici la solution architecturale du projet. Créez un fichier `calculatrice.php`.

```php
<?php
declare(strict_types=1);

/**
 * Calculatrice simple et sécurisée (Logique d'abord, Rendu ensuite)
 */

// 1. HELPER : Fonction d'échappement HTML pour contrer le XSS
function e(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

// 2. CAPTURE SÉCURISÉE : L'utilisation de filtres natifs plutôt que de lire bêtement $_GET['a']
$a = filter_input(INPUT_GET, 'a', FILTER_VALIDATE_FLOAT);
$b = filter_input(INPUT_GET, 'b', FILTER_VALIDATE_FLOAT);
$operation = $_GET['op'] ?? ''; // Null coalescing pour parer l'omission

// 3. ÉTAT (STATE)
$resultat = null;
$erreur = null;

// 4. MOTEUR MATHÉMATIQUE & VERROUS
if ($a === false || $a === null) {
    $erreur = "Le premier nombre est invalide ou absent.";
} elseif ($b === false || $b === null) {
    $erreur = "Le second nombre est invalide ou absent.";
} else {
    // Structure Switch classique (idéale pour des validations à branchements multiples)
    switch ($operation) {
        case 'addition':
            $resultat = $a + $b;
            break;
            
        case 'soustraction':
            $resultat = $a - $b;
            break;
            
        case 'multiplication':
            $resultat = $a * $b;
            break;
            
        case 'division':
            // Règle d'or absolue en mathématique informatique
            if ($b == 0) {
                $erreur = "Division par Zéro impossible (FailSafe).";
            } else {
                $resultat = $a / $b;
            }
            break;
            
        case 'modulo':
            if ($b == 0) {
                $erreur = "Modulo par Zéro impossible.";
            } else {
                $resultat = $a % $b;
            }
            break;
            
        case 'puissance':
            $resultat = $a ** $b; // Opérateur de puissance moderne
            break;
            
        default:
            $erreur = "Tentative de piratage ou opération inconnue.";
    }
}
?>
```

## 2. Rendu Interface (HTML Injecté)

L'architecture correcte d'un script PHP basique implique de séparer la logique pure (en haut, sans aucun html) du Rendu (en bas). Collez la suite dans le même fichier, sous balise fermante `?>`.

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Calculatrice PHP</title>
    <style>
        body { font-family: system-ui; text-align:center; padding: 20px; background: #f8fafc; }
        .box { background: white; margin: 20px auto; max-width: 400px; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .result { background: #dcfce7; color: #166534; padding: 15px; border-radius: 5px; font-weight: bold;}
        .error { background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 5px; font-weight: bold;}
        input, select, button { padding: 10px; width: 100%; margin: 10px 0; border: 1px solid #cbd5e1; border-radius: 4px; }
        button { background: #3b82f6; color: white; border: none; font-weight: bold; cursor:pointer;}
    </style>
</head>
<body>
    
    <div class="box">
        <h2>Casio 3000</h2>
        
        <!-- INJECTION DES MESSAGES (Toujours passés dans e() !) -->
        <?php if ($erreur): ?>
            <div class="error"><?= e($erreur) ?></div>
        <?php endif; ?>
        
        <?php if ($resultat !== null): ?>
            <div class="result">
                <?= e((string)$a) ?> <?= e($operation) ?> <?= e((string)$b) ?> 
                <br><strong>= <?= e((string)$resultat) ?></strong>
            </div>
        <?php endif; ?>
        
        <!-- LE FORMULAIRE -->
        <form method="GET">
            <input type="number" step="any" name="a" placeholder="Nombre A" value="<?= e($_GET['a'] ?? '') ?>" required>
            
            <select name="op" required>
                <option value="addition" <?= $operation === 'addition' ? 'selected' : '' ?>>+</option>
                <option value="soustraction" <?= $operation === 'soustraction' ? 'selected' : '' ?>>-</option>
                <option value="multiplication" <?= $operation === 'multiplication' ? 'selected' : '' ?>>X</option>
                <option value="division" <?= $operation === 'division' ? 'selected' : '' ?>>/</option>
            </select>
            
            <input type="number" step="any" name="b" placeholder="Nombre B" value="<?= e($_GET['b'] ?? '') ?>" required>
            
            <button type="submit">Calculer</button>
        </form>
    </div>

</body>
</html>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-2 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Je divise par 0 : Le PHP bloque avant de cracher une erreur système moche.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">J'entre des lettres "ABC" dans l'URL ? Le <code>filter_input</code> renvoie une erreur douce "Nombre Invalide".</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">J'essaie du XSS dans l'URL (<code>?a=&lt;script&gt;</code>) : Le navigateur le transforme en texte mort <code>&amp;lt;script&amp;gt;</code>. Sécurité maximale !</span>
    </li>
  </ul>
</div>
