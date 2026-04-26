---
description: "Projet Pratique : Architecture d'un système de notation éducatif en PHP. Utilisation intensive du parsing de chaînes, de la logique de branchement, et de l'architecture POST."
icon: lucide/graduation-cap
tags: ["PHP", "PROCÉDURAL", "POST", "TABLEAUX", "MATH"]
status: stable
---

# Projet 3 : Système de Notes avec Conditions

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    Le rectorat a besoin de votre aide pour concevoir un panel prof. Vous devez écrire un script PHP capable d'ingérer une liste de nombres bruts tapée par un professeur, de la nettoyer, d'en calculer la moyenne exacte, et d'attribuer automatiquement une Mention scolaire en utilisant la syntaxe moderne `match()` de PHP 8.

!!! abstract "Objectifs Pédagogiques"
    1.  **Formulaire POST** : Gérer un formulaire par la méthode sécurisée `POST` plutôt que `GET`.
    2.  **Manipulation de Chaînes & Tableaux** : Convertir un champ texte brut (12, 14.5, 9) en un véritable tableau indexé PHP (`explode()`, `trim()`).
    3.  **Boucles et Fonctions Mathématiques** : Écrire un `foreach` robuste pour rejeter les notes absurdes (lettres, > 20, < 0).
    4.  **Expressions Match** : Remplacer l'antique `switch` par une assignation directe et élégante avec `match()`.

## 1. La Logique Métier

Créez le fichier `notes.php`.

```php
<?php
declare(strict_types=1);

/**
 * Système de gestion de notes (Moyenne et Mentions)
 */

// 1. HELPER SÉCURITÉ
function e(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

// 2. FONCTIONS DE TRAITEMENT (Isolées)
function calculerMoyenne(array $notes): float {
    if (empty($notes)) return 0.0;
    // Les fonctions natives de PHP pour les maths de tableaux
    return array_sum($notes) / count($notes);
}

function determinerMention(float $moyenne): string {
    // La puissance de l'instruction Match (Nouveauté PHP 8)
    return match (true) {
        $moyenne >= 16 => 'Très bien 🏆',
        $moyenne >= 14 => 'Bien 🎖️',
        $moyenne >= 12 => 'Assez bien 👍',
        $moyenne >= 10 => 'Passable 😐',
        default => 'Insuffisant ❌' // Si aucune n'est vraie
    };
}

function validerNote(float $note): bool {
    return $note >= 0 && $note <= 20;
}

// 3. ÉTAT (STATE)
$notesValidesArray = [];
$moyenne = null;
$mention = null;
$erreur = null;

// 4. MOTEUR - Détection Exclusive d'un Submit POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    // Le prof tape "14, 15, 12.5"
    $notesInput = $_POST['notesBrutes'] ?? '';
    
    // Transforme la chaîne en un Array de Strings [ "14", " 15", " 12.5"]
    $tableauDecoupe = explode(',', $notesInput);
    
    $ToutesLesNotesSontValides = true;
    
    // Parcours et nettoyage (Sanitization)
    foreach ($tableauDecoupe as $texteBranche) {
        $chainePropre = trim($texteBranche); // Enlève les espaces autour
        
        if ($chainePropre === '') continue; // Ignore les cases vides (ex: "14,,15")
        
        // Anti-Crash : Est-ce qu'on a bien un nombre ?
        if (!is_numeric($chainePropre)) {
            $erreur = "Le système a crashé à cause de '$chainePropre'. Uniquement des nombres !";
            $ToutesLesNotesSontValides = false;
            break; // Stoppe la boucle immédiatement
        }
        
        $note = (float)$chainePropre;
        
        // Anti-Fail : Entre 0 et 20 ?
        if (!validerNote($note)) {
            $erreur = "Triche détectée : '$note' n'est pas comprise entre 0 et 20.";
            $ToutesLesNotesSontValides = false;
            break;
        }
        
        // Tout va bien, on sauvegarde dans le tableau officiel
        $notesValidesArray[] = $note;
    }
    
    // Si la boucle est allée jusqu'au bout sans casser le drapeau "ToutesLesNotesSontValides"
    if ($ToutesLesNotesSontValides && !empty($notesValidesArray)) {
        $moyenne = calculerMoyenne($notesValidesArray);
        $mention = determinerMention($moyenne);
    } elseif (empty($notesValidesArray) && !$erreur) {
        $erreur = "Veuillez saisir au moins une note.";
    }
}
?>
```

## 2. Rendu Interface (HTML Injecté)

Collez ce bloc sous le précédent pour gérer l'affichage. L'historique du textarea est gardé intelligemment !

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Panel Professeur - Notes</title>
    <style>
        body { font-family: system-ui; max-width: 600px; margin: 50px auto; padding: 20px; background: #f1f5f9; }
        .box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        textarea { width: 100%; box-sizing: border-box; padding: 15px; border: 1px solid #cbd5e1; border-radius: 5px; font-size: 16px; margin-bottom: 5px;}
        button { width: 100%; padding: 15px; background: #0f172a; color: white; font-weight: bold; border: none; border-radius: 5px; cursor: pointer; }
        .error { background: #fee2e2; padding: 15px; border-radius: 5px; color: #991b1b; margin-bottom: 20px; border-left: 4px solid #ef4444; font-weight: bold;}
        .result { background: #eff6ff; padding: 20px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #3b82f6; }
        .tag { background: #334155; color: white; padding: 4px 8px; border-radius: 4px; margin: 2px; display: inline-block; font-size: 0.9rem;}
        .mention { font-size: 2rem; font-weight: 900; color: #0f172a; margin-top: 15px; text-align: center;}
    </style>
</head>
<body>
    <div class="box">
        <h1 style="text-align: center; margin-top:0;">📊 Panel de Notation</h1>
        
        <?php if ($erreur): ?>
            <div class="error">⚠️ <?= e($erreur) ?></div>
        <?php endif; ?>
        
        <?php if ($moyenne !== null && $mention !== null): ?>
            <div class="result">
                <h3>Bulletin Officiel</h3>
                <div>
                    <strong>Notes Validées :</strong><br>
                    <div style="margin: 10px 0;">
                        <?php foreach ($notesValidesArray as $n): ?>
                            <span class="tag"><?= e((string)$n) ?> / 20</span>
                        <?php endforeach; ?>
                    </div>
                </div>
                <hr style="border:0; border-top:1px solid #cbd5e1; margin:15px 0;">
                <p><strong>Moyenne Globale :</strong> <?= number_format($moyenne, 2) ?> / 20</p>
                <div class="mention"><?= e($mention) ?></div>
            </div>
        <?php endif; ?>
        
        <!-- FORMULAIRE METHOD POST ! -->
        <form method="POST">
            <label style="font-weight:bold; display:block; margin-bottom:10px;">Saisir les notes (séparées par des virgules)</label>
            <textarea 
                name="notesBrutes" 
                rows="4" 
                placeholder="Exemple : 15, 12.5, 9, 14"
                required
            ><?= e($_POST['notesBrutes'] ?? '') ?></textarea>
            
            <p style="font-size:0.8rem; color:#64748b; margin-top:0;">Les décimales s'écrivent avec le point, pas la virgule (ex: 15.5).</p>
            
            <button type="submit">Générer le Bulletin</button>
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
      <span class="text-gray-700">Vous tapez "15, 12, ABC". L'algorithme repère "ABC", bloque l'exécution et affiche l'Alerte "Le système a crashé".</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Le textarea conserve EXACTEMENT ce que l'utilisateur avait tapé après soumission. (Le code <code>$_POST['notesBrutes']</code> sécurisé).</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">L'instruction Match (PHP 8) renvoie instantanément "Mention très bien 🏆" pour une moyenne de 17.5. Code 0% Legacy !</span>
    </li>
  </ul>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
