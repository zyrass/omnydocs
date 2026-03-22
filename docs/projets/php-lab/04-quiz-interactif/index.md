---
description: "Projet Pratique : Apprenez l'interférence PHP en utilisant des arrays multidimensionnelles. Stockez des questions, bouclez-les dans un formulaire dynamique, et validez les réponses."
icon: lucide/clipboard-list
tags: ["PHP", "PROCÉDURAL", "ARRAY", "FORMULAIRE", "BOUCLES"]
status: stable
---

# Projet 4 : Quiz Interactif avec Scoring

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="8.3"
  data-time="1 Heure">
</div>

!!! quote "Le Pitch"
    Fini de traiter des variables simples. Dans la réalité, on traite des lots massifs de données. 
    Vous allez coder un mini-site QCM. Le serveur possède une base de données de questions (sous la forme d'un tableau multidimensionnel PHP). Il le transforme en HTML, attend que le joueur clique, et compare ses réponses POST avec sa base de vérité.

!!! abstract "Objectifs Pédagogiques"
    1.  **Arrays Multidimensionnels** : Comprendre la syntaxe `[ [ 'clé' => 'valeur' ] ]` pour mimer une table de base de données.
    2.  **Rendu Dynamique** : Utiliser un `foreach` PHP au beau milieu d'un code HTML pour générer des dizaines d'Input Radio sans les écrire à la main.
    3.  **Traitement de Lot** : Utiliser un `foreach` côté Métier (POST) pour comparer chaque ligne de réponse utilisateur à l'Array d'origine et incrémenter le `$score`.
    4.  **Retour d'Expérience (UX)** : Créer une jauge analytique dynamique avec son attribution de mentions via `match`.

## 1. La Logique Métier & Base de Données

Créez `quiz.php`. Voici le moteur. En phase de production, l'Array `$questions` viendrait d'un MySQL (via PDO). Aujourd'hui, on les code en dur.

```php
<?php
declare(strict_types=1);

/**
 * Quiz Engine : Moteur de génération de QCM
 */

function e(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

// 1. DATA CENTER : Un Array typique d'une application professionnelle
$questions = [
    [
        'question' => 'Quelle est la capitale de la France ?',
        'reponses' => ['Paris', 'Lyon', 'Marseille', 'Toulouse'],
        'correcte' => 0, // L'Index de la bonne réponse
        'points' => 1
    ],
    [
        'question' => 'Combien font 7 × 8 ?',
        'reponses' => ['54', '56', '64', '72'],
        'correcte' => 1,
        'points' => 2 // Question plus dure
    ],
    [
        'question' => 'Quel langage s\'exécute côté serveur ?',
        'reponses' => ['CSS', 'JavaScript', 'HTML', 'PHP'],
        'correcte' => 3,
        'points' => 1
    ]
];

// 2. ÉTAT INITIAL
$score = null;
$maxScore = 0;
$pourcentage = 0;
$appreciation = null;

// Le système compte automatiquement le total de points disponibles 
// (Pour éviter de hard-coder 4 si on ajoute une question demain)
foreach ($questions as $q) {
    // Équivalent propre de += 
    $maxScore = $maxScore + $q['points'];
}

// 3. MOTEUR DE TRAITEMENT
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $score = 0;
    
    // PHP est fantastique : On peut récupérer un tableau HTML via name="reponses[]"
    $reponsesUser = $_POST['reponses'] ?? [];
    
    // On boucle sur NOTRE base sécurisée, pas celle de l'utilisateur
    foreach ($questions as $index => $q) {
        
        // Si l'utilisateur a envoyé une réponse (Input Radio) à l'index courant
        if (isset($reponsesUser[$index])) {
            
            // On transtype sa réponse String ('0', '1') en int
            $reponseChoisie = (int)$reponsesUser[$index];
            
            if ($reponseChoisie === $q['correcte']) {
                $score += $q['points']; // WIN
            }
            // Sinon : Perdu (Rien ne bouge, pas besoin de else)
        }
    }

    // 4. ANALYTIQUE
    $pourcentage = ($score / $maxScore) * 100;

    $appreciation = match (true) {
        $pourcentage === 100.0 => 'Perfection Absolue ! 🏆',
        $pourcentage >= 80.0 => 'Masterclass en cours ! 🎯',
        $pourcentage >= 50.0 => 'Solide mais perfectible 👍',
        default => 'Oups. Retournez au Module 1... 💀'
    };
}
?>
```

## 2. Le Rendu Interface Moteur (HTML Génératif)

Ici, nous allons mélanger le templating HTML et PHP propre grâce aux balises `< ?php foreach(...) : ?> ... < ?php endforeach; ?>`

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>PHP Master Quiz</title>
    <style>
        body { font-family: system-ui; max-width: 650px; margin: 40px auto; padding: 20px; background: #fafafa; }
        .box { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
        .question-block { margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid #e5e7eb; }
        .question-title { font-weight: 800; font-size: 1.1rem; color: #1e293b; margin-bottom: 10px;}
        .options label { display: block; margin-bottom: 8px; cursor: pointer; padding: 8px; border-radius: 4px; transition: background 0.2s;}
        .options label:hover { background: #f1f5f9; }
        button { background: #6366f1; color: white; width: 100%; padding: 15px; border: none; font-size: 1.1rem; font-weight: bold; border-radius: 8px; cursor: pointer;}
        button:hover { background: #4f46e5; }
        .result-panel { text-align: center; background: #e0e7ff; border: 2px solid #818cf8; padding: 25px; border-radius: 8px; margin-bottom: 30px;}
        .score-big { font-size: 3rem; font-weight: 900; color: #3730a3; margin: 10px 0;}
    </style>
</head>
<body>

    <div class="box">
        <h1 style="text-align: center; margin-top:0;">🧠 Le Grand QCM</h1>

        <!-- RÉSULTAT ANALYTIQUE (S'affiche uniquement en POST) -->
        <?php if ($score !== null): ?>
            <div class="result-panel">
                <h3 style="margin-top:0;">Résultat Officiel</h3>
                <div class="score-big"><?= $score ?> / <?= $maxScore ?></div>
                <div style="font-size: 1.2rem; margin-bottom: 15px;">(<?= number_format($pourcentage, 0) ?>%)</div>
                <strong><?= e($appreciation) ?></strong>
                <br><br>
                <a href="quiz.php" style="color: #4f46e5; font-weight: bold;">Refaire le test</a>
            </div>
        <!-- SI NOUS SOMMES EN GET (Page vierge) ON AFFICHE LE FORM -->
        <?php else: ?>
        
        <form method="POST">
            
            <!-- GÉNÉRATION DYNAMIQUE : LE MOTEUR TOURNE ICI -->
            <?php foreach ($questions as $index => $q): ?>
                
                <div class="question-block">
                    <!-- Titre : Question N°X (1 point) -->
                    <div class="question-title">
                        A.<?= $index + 1 ?> — <?= e($q['question']) ?> 
                        <span style="color:#64748b; font-size: 0.8rem;">(<?= $q['points'] ?> pts)</span>
                    </div>
                    
                    <div class="options">
                        <!-- Sous-génération des 4 choix -->
                        <?php foreach ($q['reponses'] as $repIndex => $repText): ?>
                            <label>
                                <!-- Magie : name="reponses[X]" avec la value="Y" -->
                                <input type="radio" name="reponses[<?= $index ?>]" value="<?= $repIndex ?>" required>
                                <?= e($repText) ?>
                            </label>
                        <?php endforeach; ?>
                    </div>
                </div>

            <?php endforeach; ?>
            
            <button type="submit">Valider mon QCM</button>

        </form>

        <?php endif; ?>
    </div>

</body>
</html>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-2 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Comprendre ABSOLUMENT le <code>name="reponses[&lt;?= $index ?&gt;]"</code> HTML. C'est ce qui permet au PHP <code>$_POST['reponses']</code> de récupérer un Tableau au lieu d'une valeur simple !</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Le Formulaire disparait complétement après soumission (il est <code>else</code> par rapport au panel de Résultat).</span>
    </li>
  </ul>
</div>
