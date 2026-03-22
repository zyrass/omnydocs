---
description: "Projet Pratique POO : Forger un Validateur Universel (Formulaires, API) avec un système de règles injectables via Interfaces."
icon: lucide/shield-check
tags: ["PHP", "POO", "INTERFACE", "VALIDATION"]
status: stable
---

# Projet 19 : Système de Validation

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    Valider un formulaire revient souvent à coder des `if(!empty($_POST['...']))`, imbriqués à l'infini.
    Dans un framework professionnel (comme Laravel), la validation se fait par **Règles**. 
    Une `ValidationRule` est une classe qui applique un test unique (Ex: `EmailRule`, `MinLengthRule`).

!!! abstract "Objectifs Pédagogiques"
    1.  **L'Interface Règle** : Créer `ValidationRuleInterface` spécifiant le format obligatoire de toute règle (`validate()` et `getMessage()`).
    2.  **L'Interface Moteur** : Créer l'interface de l'arbitre en chef `ValidatorInterface` qui se chargera de boucler sur toutes les règles.
    3.  **Extensibilité Infinie** : Demain, si vous voulez créer une `IsAdultAgeRule`, vous n'aurez pas à modifier le coeur du validateur. C'est l'essence du principe **Open/Closed** (SOLID).

## 1. Les Contrats du Validateur

Voici les règles juridiques que devront respecter nos objets pour s'emboîter parfaitement.

```php
<?php
declare(strict_types=1);

/**
 * Toute règle spécifique devra posséder ces deux méthodes !
 */
interface ValidationRuleInterface {
    
    // Teste la valeur passée, renvoie vrai ou faux
    public function validate(mixed $value): bool;
    
    // Le message d'erreur à ressortir si False
    public function getMessage(): string;
}

/**
 * Le moteur maître qui regroupe et lance les règles
 */
interface ValidatorInterface {
    
    // Ajouter une règle à la volée sur un "champ" spécifique
    public function addRule(string $field, ValidationRuleInterface $rule): void;
    
    // Parcourir toutes les règles contre un tableau de données massives
    public function validate(array $data): bool;
    
    // Obtenir le tableau des plaintes s'il y en a eu
    public function getErrors(): array;
}
?>
```

## 2. Création de nos "Petites Briques" (Les Règles)

On passe à l'implémentation. On construit les Legos.

```php
<?php
declare(strict_types=1);

require_once 'Interfaces.php';

// --- RÈGLE 1 : CHAMP OBLIGATOIRE ---
class RequiredRule implements ValidationRuleInterface {
    
    public function validate(mixed $value): bool {
        // "0" et int 0 sont valides, même si "empty()" les considère faux.
        return !empty($value) || $value === '0' || $value === 0;
    }
    
    public function getMessage(): string {
        return 'Ce champ est absolument requis.';
    }
}

// --- RÈGLE 2 : FORMAT EMAIL ---
class EmailRule implements ValidationRuleInterface {
    
    public function validate(mixed $value): bool {
        // Un simple filtre natif PHP suffit à résoudre le souci
        return filter_var($value, FILTER_VALIDATE_EMAIL) !== false;
    }
    
    public function getMessage(): string {
        return "Le format de l'e-mail est invalide.";
    }
}

// --- RÈGLE 3 : LONGUEUR MINIMUM (Avec Paramètre !) ---
class MinLengthRule implements ValidationRuleInterface {
    
    private int $minLength;
    
    // On profite du constructeur pour passer la contrainte de longueur
    public function __construct(int $minLength) {
        $this->minLength = $minLength;
    }
    
    public function validate(mixed $value): bool {
        // Le cast (string) évite de planter si "$value" est un tableau 
        return mb_strlen((string)$value) >= $this->minLength;
    }
    
    public function getMessage(): string {
        return "Vous devez entrer au minimum {$this->minLength} caractères.";
    }
}
?>
```

## 3. Le Moteur Central (L'Orchestrateur)

Le moteur n'est qu'un "chef d'orchestre". Il ne connait PAS le code interne des règles `EmailRule`. Il sait juste qu'une règle a une méthode `validate()` et une méthode `getMessage()`. C'est l'Interface qui le lui garantit !

```php
<?php
declare(strict_types=1);

class FormValidator implements ValidatorInterface {
    
    // Tableau multidimensionnel [ 'email' => [Rule1, Rule2], 'password' => [Rule3] ]
    private array $rules = [];
    
    // Pile des erreurs générées lors de l'exécution
    private array $errors = [];
    
    // =======
    
    public function addRule(string $field, ValidationRuleInterface $rule): void {
        // Si le champ n'existe pas encore dans la matrice des règles, on l'initialise
        if (!isset($this->rules[$field])) {
            $this->rules[$field] = [];
        }
        
        // On pousse l'objet Règle dans la case du Champ choisi
        $this->rules[$field][] = $rule;
    }
    
    public function validate(array $data): bool {
        // On remet les compteurs à zéro (si on réutilise l'objet)
        $this->errors = [];
        
        // On loop sur TOUS les champs prévus (email, password...)
        foreach ($this->rules as $field => $rulesAssignedToThisField) {
            
            // On loop sur toutes les RÈGLES qui attendent ce champ.
            foreach ($rulesAssignedToThisField as $ruleObject) {
                
                // On extrait la valeur si elle existe dans la requête HTTP/Tableau
                $value = $data[$field] ?? null;
                
                // On attaque la valeur de l'utilisateur avec la Muraillle !
                if (!$ruleObject->validate($value)) {
                    // C'est un ÉCHEC, on ajoute la phrase de plainte au rapport d'erreurs
                    $this->errors[$field][] = $ruleObject->getMessage();
                }
            }
        }
        
        // La requête est valide SI la corbeille d'erreurs est VIDE !
        return empty($this->errors);
    }
    
    public function getErrors(): array {
        return $this->errors;
    }
}
?>
```

## 4. Crash Test Terminal

```php
<?php
require_once 'Validator.php'; // Toutes les classes + interfaces jointes

// ---- LE DÉVELOPPEUR PRÉPARE SON TERRAIN ----
$validator = new FormValidator();

// Assemblage du LEGO (Construction du Pare-Feu)
$validator->addRule('prenom', new RequiredRule());
$validator->addRule('prenom', new MinLengthRule(3));

$validator->addRule('email_contact', new RequiredRule());
$validator->addRule('email_contact', new EmailRule());

// ---- LE CLIENT SOUMET SES DATA DEPUIS LE FRONT-END ($_POST) ----
$dataUserFakePost = [
    'prenom' => 'Al', // ERROR: Trop court par rapport à 3 !
    'email_contact' => 'je_suis_un_hacker_ou_un_neuneu' // ERROR: Pas d'arobase
];

// ---- L'ARBITRAGE DU CODE ----
echo ">> LANCEMENT DE L'ANALYSE...\n\n";

if (!$validator->validate($dataUserFakePost)) {
    echo "❌ <b>Validation Échouée !</b> Voici le rapport :\n";
    
    // Affichage natif propre pour le terminal
    print_r($validator->getErrors());
    
} else {
    echo "🟢 Succès ! Bienvenue sur l'application.";
}
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">Il est incroyable de remarquer à nouveau que votre <code>FormValidator</code> est extrêmement résilient. Vous pouvez à présent construire le code suivant à part sans modifier le coeur :</p>
  <ul class="space-y-4 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">1</span>
      <span class="text-gray-700"><code>class IsBannedIPRule implements ValidationRuleInterface</code></span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">2</span>
      <span class="text-gray-700">L'injecter en une ligne <code>$validator->addRule('ip', new IsBannedIPRule());</code></span>
    </li>
  </ul>
</div>
