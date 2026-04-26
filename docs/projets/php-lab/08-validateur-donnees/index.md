---
description: "Projet Pratique : Coder un système avancé de validation d'entrées utilisateur et s'initier aux Regex (Expressions Régulières) pour sécuriser des formulaires."
icon: lucide/shield-check
tags: ["PHP", "PROCÉDURAL", "REGEX", "VALIDATION", "DATE"]
status: stable
---

# Projet 8 : Validateur de Données Multiformats

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    Sur le Web, le principe fondamental est de **NE JAMAIS FAIRE CONFIANCE À L'UTILISATEUR**. Qu'il soit malveillant ou maladroit, il va entrer des données corrompues.
    Vous allez coder une "Classe" (Approche moderne Orientée Objet pour regrouper des outils) contenant toutes les Regex et fonctions natives de `filter_var()` pour inspecter de A à Z : un email, un numéro de téléphone, une Date et même un Code Postal FR.

!!! abstract "Objectifs Pédagogiques"
    1.  **Filtres Natifs (L'approche élégante)** : Apprendre à utiliser `FILTER_VALIDATE_EMAIL` et `FILTER_VALIDATE_URL` pour les standards normés.
    2.  **Regex (L'approche sur-mesure)** : Utiliser `preg_match` pour forcer des structures complexes, comme le Numéro de Téléphone Français de 10 chiffres commençant par 0.
    3.  **Nettoyage Préventif (Sanitization)** : Utiliser `preg_replace` pour tolérer un utilisateur qui met des espaces ou des tirets dans son téléphone et les retirer avant la validation.
    4.  **Tests Unitaires (Visuels)** : Déboguer nos outils dans un banc d'essai HTML.

## 1. La Classe Validateur

Dans ce projet, nous regroupons nos fonctions utiles dans un bloc fermé : une `Class`. L'usage se fera de manière orientée objet (`$validateur = new Validateur();`). Créez `validateur.php`.

```php
<?php
declare(strict_types=1);

/**
 * Validateur Universel de Données Sensibles
 */

class Validateur 
{
    /**
     * 1. L'EMAIL : Inutile de réécrire une Regex complexe. PHP connait la RFC officielle.
     */
    public function validerEmail(string $email): bool {
        // filter_var renvoie la chaîne OU false. Le !== false permet de retourner un boolean fort
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }
    
    /**
     * 2. LE TÉLÉPHONE: Il y a 100 manières de l'écrire. On nettoie, puis on vérifie
     */
    public function validerTelephoneFr(string $tel): bool {
        // A. Nettoyage Anti-bruit : On enlève les Espaces, Tirets ou Points.
        // L'utilisateur tape '06 12-34.56', la machine voit '06123456'
        $telPropre = preg_replace('/[\s\-\.]/', '', $tel);
        
        // B. Expression Régulière stricte :
        // ^   : Au début
        // 0   : Commence impérativement par un zéro
        // [1-9] : Suivi d'un chiffre de 1 à 9
        // \d{8} : Suivi d'exactement 8 chiffres
        // $   : Et la chaîne s'arrête là (Interdit "0612345678ABCD")
        return preg_match('/^0[1-9]\d{8}$/', $telPropre) === 1;
    }
    
    /**
     * 3. DATE : Vérifier le Format DD/MM/YYYY ET la Réalité du Calendrier (Février a-t-il 29 jours ?)
     */
    public function validerDate(string $date): bool {
        // Regex de vérification de base (Capte Groupes \d{2} et \d{4} séparés par des Slash)
        if (!preg_match('/^(\d{2})\/(\d{2})\/(\d{4})$/', $date, $matches)) {
            return false;
        }
        
        // La Regex a découpé la donnée dans l'Array $matches
        // $matches[1] = DD, $matches[2] = MM, $matches[3] = YYYY
        // checkdate(mois, jour, annee) est une fonction native PHP qui vérifie le calendrier
        return checkdate((int)$matches[2], (int)$matches[1], (int)$matches[3]);
    }
    
    /**
     * 4. URL : Rapide et efficace avec le standard PHP
     */
    public function validerUrl(string $url): bool {
        return filter_var($url, FILTER_VALIDATE_URL) !== false;
    }
    
    /**
     * 5. CODE POSTAL FRANÇAIS (5 Chiffres dont les 2 premiers ne sont pas "00")
     */
    public function validerCodePostal(string $cp): bool {
        // (?:0[1-9]|[1-8]\d|9[0-5]) : C'est toute la subtilité des départements de 01 à 95.
        // \d{3} : Accompagnés de 3 chiffres quelconques
        return preg_match('/^(?:0[1-9]|[1-8]\d|9[0-5]|9[7-8])\d{3}$/', $cp) === 1;
    }
}
?>
```

## 2. L'Interface de Banc d'Essai (Test Suite HTML)

Collé juste en dessous, ce code va utiliser notre classe PHP et auditer des données prédéfinies pour valider si le code Regex fonctionne.

```html
<?php
// On Instancie "L'Outil" Validateur
$validateur = new Validateur();

// Scénarios de Test
$testEmails = ['alain@gmail.com', 'alain@.com', 'contact@omnyvia.fr', 'bob@laposte'];
$testTelephones = ['0612345678', '09 87 65 43 21', '06-11-22-33-44', '+33612345678', '0000000000'];
$testDates = ['14/07/2026', '31/02/2020', '32/01/2000', '15-05-2023'];
$testCP = ['75000', '00123', '95000', '98xyz'];

// Fonction Helper d'Affichage
function badgeResultat(bool $resultat): string {
    return $resultat ? '<span style="color: green; font-weight: bold;">[VALIDE]</span>' : '<span style="color: red; font-weight: bold;">[INVALIDE]</span>';
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Interface de Validation</title>
    <style>
        body { font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 20px; background: #e2e8f0;}
        .board { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: grid; grid-template-columns: 1fr 1fr; gap: 20px;}
        .card { background: #f8fafc; padding: 15px; border: 1px solid #cbd5e1; border-radius: 6px;}
        h3 { margin-top: 0; color: #0f172a; border-bottom: 2px solid #38bdf8; padding-bottom: 5px; }
        ul { list-style: none; padding: 0; }
        li { margin-bottom: 8px; padding: 5px; background: white; border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    </style>
</head>
<body>

    <h1 style="text-align: center;">🛡️ Laboratoire de Validation Regex</h1>

    <div class="board">

        <!-- TEST EMAILS -->
        <div class="card">
            <h3>Emails</h3>
            <ul>
                <?php foreach($testEmails as $email): ?>
                    <li><?= badgeResultat($validateur->validerEmail($email)) ?> : <?= htmlspecialchars($email) ?></li>
                <?php endforeach; ?>
            </ul>
        </div>

        <!-- TEST TÉLÉPHONES -->
        <div class="card">
            <h3>Téléphones France (Sanitized)</h3>
            <ul>
                <?php foreach($testTelephones as $tel): ?>
                    <li><?= badgeResultat($validateur->validerTelephoneFr($tel)) ?> : <?= htmlspecialchars($tel) ?></li>
                <?php endforeach; ?>
            </ul>
        </div>

        <!-- TEST DATES -->
        <div class="card">
            <h3>Dates (DD/MM/YYYY)</h3>
            <ul>
                <?php foreach($testDates as $date): ?>
                    <li><?= badgeResultat($validateur->validerDate($date)) ?> : <?= htmlspecialchars($date) ?></li>
                <?php endforeach; ?>
            </ul>
        </div>

        <!-- TEST CODES POSTAUX -->
        <div class="card">
            <h3>Codes Postaux</h3>
            <ul>
                <?php foreach($testCP as $cp): ?>
                    <li><?= badgeResultat($validateur->validerCodePostal($cp)) ?> : <?= htmlspecialchars($cp) ?></li>
                <?php endforeach; ?>
            </ul>
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
      <span class="text-gray-700">Vous observez que <strong>09 87 65 43 21</strong> a bien été jugé VALIDE. Le mécanisme silencieux <code>preg_replace</code> l'a nettoyé en <code>0987654321</code> avant de l'envoyer à la vraie Regex. C'est le secret d'une UX incroyable.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Vous constatez sur l'écran que <strong>31/02/2020</strong> est INVALIDE. Même si la structure en Regex <code>DD/MM/YYYY</code> est parfaite, la fonction native PHP <code>checkdate()</code> l'a rejeté car la date n'existe pas d'un point de vue calendrier Grégorien.</span>
    </li>
  </ul>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
