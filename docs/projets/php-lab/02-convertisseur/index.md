---
description: "Projet Pratique : Architecture d'un convertisseur d'unités (Température, Distance, Poids) utilisant des fonctions pures et la gestion des chaînes concaténées."
icon: lucide/arrow-left-right
tags: ["PHP", "PROCÉDURAL", "FONCTIONS", "MATH", "SWITCH"]
status: stable
---

# Projet 2 : Convertisseur d'Unités

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    Votre entreprise internationale a besoin d'un outil interne pour convertir des miles en kilomètres, des kilos en livres, et des Celsius en Fahrenheit. Ce projet vous apprend à structurer des **Fonctions Pures** (qui font une seule chose) et à concaténer dynamiquement des chaînes de caractères pour déclencher l'action adéquate.

!!! abstract "Objectifs Pédagogiques"
    1.  **Fonctions Mathématiques Pures** : Créer des fonctions typées (`float $valeur) : float`) qui retournent toujours un résultat prévisible sans effet de bord.
    2.  **String Concaténation Dynamique** : Reconstruire une clé de switch dynamiquement (Ex: `$from . '_to_' . $to` donne `celsius_to_fahrenheit`).
    3.  **Filtrage Front-End Réactif** : Garder l'historique de la valeur entrée dans le formulaire HTML après le rechargement.

## 1. La Logique Métier (Le Cerveau)

Ce projet demande beaucoup plus de logique "isolée". Nous allons écrire 6 fonctions de calcul dédiées qui pourraient être réutilisables dans n'importe quel autre script. Créez `convertisseur.php`.

```php
<?php
declare(strict_types=1);

/**
 * Projet Convertisseur d'Unités Multiples
 */

// 1. HELPER SECURE
function e(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

// 2. FONCTIONS DE CONVERSIONS PURES
// TEMPÉRATURE
function celsiusToFahrenheit(float $celsius): float {
    return ($celsius * 9/5) + 32;
}
function fahrenheitToCelsius(float $fahrenheit): float {
    return ($fahrenheit - 32) * 5/9;
}

// DISTANCE
function kmToMiles(float $km): float {
    return $km * 0.621371;
}
function milesToKm(float $miles): float {
    return $miles / 0.621371;
}

// POIDS
function kgToLbs(float $kg): float {
    return $kg * 2.20462;
}
function lbsToKg(float $lbs): float {
    return $lbs / 2.20462;
}

// 3. CAPTURE SÉCURISÉE DES DONNÉES UTILISATEURS
$value = filter_input(INPUT_GET, 'value', FILTER_VALIDATE_FLOAT);
$from = $_GET['from'] ?? '';
$to = $_GET['to'] ?? '';

// 4. ETAT
$result = null;
$error = null;

// 5. MOTEUR DE DÉCISION
// Si la valeur est bien un nombre...
if ($value !== false && $value !== null) {
    
    // Astuce Prod : On crée une Clé String unique à partir des 2 requêtes
    $conversionType = $from . '_to_' . $to;
    
    switch ($conversionType) {
        // Températures
        case 'celsius_to_fahrenheit':
            $result = celsiusToFahrenheit($value);
            break;
        case 'fahrenheit_to_celsius':
            $result = fahrenheitToCelsius($value);
            break;
            
        // Distances
        case 'km_to_miles':
            $result = kmToMiles($value);
            break;
        case 'miles_to_km':
            $result = milesToKm($value);
            break;
            
        // Poids
        case 'kg_to_lbs':
            $result = kgToLbs($value);
            break;
        case 'lbs_to_kg':
            $result = lbsToKg($value);
            break;
            
        // Gestion des erreurs Utilisateur (Same to Same)
        case 'celsius_to_celsius':
        case 'km_to_km':
        case 'kg_to_kg':
            $result = $value; // Pas de conversion nécessaire
            break;
            
        default:
            $error = "Conversion de [{$from}] vers [{$to}] non supportée ou incohérente.";
    }
} elseif (isset($_GET['value'])) {
    // S'il a cliqué sur 'Convertir' mais que le champ était vide ou contient du texte
    $error = "Veuillez entrer une valeur numérique valide.";
}
?>
```

## 2. Rendu Interface (HTML Dynamique)

Sous la balise `?>`, nous intégrons l'Interface permettant à l'humain d'activer notre moteur. Remarquez la logique de l'attribut `selected` pour garder un formulaire persistant !

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Convertisseur Universel</title>
    <style>
        body { font-family: system-ui; text-align:center; padding: 20px; background: #e2e8f0; }
        .box { background: white; margin: 20px auto; max-width: 500px; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .result { background: #dcfce7; color: #166534; padding: 15px; border-radius: 5px; font-weight: bold; font-size: 1.2rem; }
        .error { background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 5px; font-weight: bold;}
        input, select { padding: 10px; width: 45%; margin: 10px 2%; border: 1px solid #cbd5e1; border-radius: 4px; }
        button { background: #3b82f6; color: white; border: none; font-weight: bold; cursor:pointer; width: 95%; padding: 12px; margin-top: 20px; border-radius: 5px;}
        .flex-row { display: flex; justify-content: space-between; align-items: center;}
    </style>
</head>
<body>
    
    <div class="box">
        <h2>🛠️ Convertisseur Universel</h2>
        
        <!-- MESSAGERIE -->
        <?php if ($error): ?>
            <div class="error"><?= e($error) ?></div>
        <?php endif; ?>
        
        <?php if ($result !== null): ?>
            <div class="result">
                <?= e((string)$value) ?> <?= e($from) ?> 
                <br> ⏬ <br>
                <?= e(number_format($result, 2)) ?> <?= e($to) ?>
            </div>
        <?php endif; ?>
        
        <!-- LE FORMULAIRE RE-POPULÉ -->
        <form method="GET">
            <h4 style="text-align: left; padding-left: 10px;">Entrez la Valeur</h4>
            <input type="number" step="any" name="value" style="width: 95%" value="<?= e($_GET['value'] ?? '') ?>" required>
            
            <div class="flex-row">
                <!-- Select DEPART -->
                <select name="from" required>
                    <optgroup label="Température">
                        <option value="celsius" <?= $from === 'celsius' ? 'selected' : '' ?>>Celsius (°C)</option>
                        <option value="fahrenheit" <?= $from === 'fahrenheit' ? 'selected' : '' ?>>Fahrenheit (°F)</option>
                    </optgroup>
                    <optgroup label="Distance">
                        <option value="km" <?= $from === 'km' ? 'selected' : '' ?>>Kilomètres (km)</option>
                        <option value="miles" <?= $from === 'miles' ? 'selected' : '' ?>>Miles (mi)</option>
                    </optgroup>
                    <optgroup label="Poids">
                        <option value="kg" <?= $from === 'kg' ? 'selected' : '' ?>>Kilogrammes (kg)</option>
                        <option value="lbs" <?= $from === 'lbs' ? 'selected' : '' ?>>Livres (lbs)</option>
                    </optgroup>
                </select>

                <span>VERS</span>

                <!-- Select ARRIVÉE -->
                <select name="to" required>
                    <optgroup label="Température">
                        <option value="celsius" <?= $to === 'celsius' ? 'selected' : '' ?>>Celsius (°C)</option>
                        <option value="fahrenheit" <?= $to === 'fahrenheit' ? 'selected' : '' ?>>Fahrenheit (°F)</option>
                    </optgroup>
                    <optgroup label="Distance">
                        <option value="km" <?= $to === 'km' ? 'selected' : '' ?>>Kilomètres (km)</option>
                        <option value="miles" <?= $to === 'miles' ? 'selected' : '' ?>>Miles (mi)</option>
                    </optgroup>
                    <optgroup label="Poids">
                        <option value="kg" <?= $to === 'kg' ? 'selected' : '' ?>>Kilogrammes (kg)</option>
                        <option value="lbs" <?= $to === 'lbs' ? 'selected' : '' ?>>Livres (lbs)</option>
                    </optgroup>
                </select>
            </div>
            
            <button type="submit">Lancer la Conversion</button>
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
      <span class="text-gray-700">Je demande à convertir des Kilomètres en Fahrenheit. Le backend capte 'km_to_fahrenheit', ne la trouve pas dans le Switch, et bloque avec l'erreur personnalisée.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Les fonctions mathématiques font exactement ce pour quoi elles ont été créées, sans interagir avec la superglobale $_GET (Architecture propre).</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Je convertis "60" Miles en Km : le résultat s'affiche, limitant l'arrondi mathématique à 2 chiffres après la virgule via <code>number_format()</code>.</span>
    </li>
  </ul>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
