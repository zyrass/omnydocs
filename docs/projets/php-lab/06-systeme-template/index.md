---
description: "Projet Pratique : Initiation à l'architecture MVC avec la création d'un mini-moteur de templating pour séparer le PHP du HTML (Concept ob_start et extract)."
icon: lucide/layout-template
tags: ["PHP", "PROCÉDURAL", "TEMPLATE", "ARCHITECTURE", "BUFFERS"]
status: stable
---

# Projet 6 : Système de Template Simple

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="8.3"
  data-time="1 Heure">
</div>

!!! quote "Le Pitch"
    Vous êtes fatigués d'intercaler vos balises `< ?php echo $variable ? >` en plein milieu de votre HTML. Le code devient un plat de spaghettis illisible.
    Dans ce projet, vous allez créer l'ancêtre du système **Blade (Laravel) ou Twig (Symfony)** : un moteur de templating natif. Le PHP calculera la logique d'un côté, et le HTML se contentera de consommer de la donnée propre.

!!! abstract "Objectifs Pédagogiques"
    1.  **Tampon de Sortie (Output Buffering)** : Maîtriser `ob_start()` et `ob_get_clean()`. Le PHP génèrera du code en mémoire RAM cachée plutôt que de l'envoyer au navigateur, permettant de l'encapsuler dans une variable.
    2.  **Extraction de Variables** : Découvrir la magie d' `extract($data)`, qui transforme le tableau clé-valeur `['nom' => 'Alice']` en une véritable variable `$nom = 'Alice'` accessible pour la vue.
    3.  **Concept de Layout (Master Page)** : Créer un gabarit parent HTML qui encadrera tout votre futur contenu web généré.

## 1. Le Moteur de Templating

Ici on conçoit le fichier central (le routeur/contrôleur) qui inclura la vue à la demande. Créez `templating.php`.

```php
<?php
declare(strict_types=1);

/**
 * Moteur de Template Procédural
 */

// 1. LA MAGIE DE L'OUTPUT BUFFERING
function renderVue(string $nomVue, array $data = []): string {
    
    // Si on passe ['nom' => 'Alice', 'role' => 'Admin']
    // extract() va injecter ces clés dans les portées locales de la fonction 
    // -> $nom = 'Alice';
    // -> $role = 'Admin';
    extract($data);
    
    // On allume le magnétoscope (Tampon de sortie RAM)
    ob_start();
    
    // On inclut le fichier HTML brut. Il va être interprété, mais au lieu
    // de partir vers le navigateur, il est piégé par ob_start() !
    $fichierCible = __DIR__ . "/vues/" . $nomVue . ".php";
    
    if (file_exists($fichierCible)) {
        include $fichierCible;
    } else {
        echo "<h1>Erreur 404 : Vue [$nomVue] introuvable.</h1>";
    }
    
    // On coupe l'enregistrement et on retourne la cassette brute sous forme de String !
    return ob_get_clean();
}

// 2. LE GENERATEUR DE LAYOUT (MASTER PAGE)
// Cette fonction prend le contenu HMTL généré par 'renderVue' et l'entoure
// avec le Squelette de base du site web entier (Header, Footer).
function layout(string $titrePage, string $htmlInterieur): string {
    return renderVue('master-layout', [
        'titre' => $titrePage,
        'contenu' => $htmlInterieur // On passe une string HTML massive complète
    ]);
}

// ============================================
// SIMULATION D'UN CONTROLEUR (Page d'accueil)
// ============================================

// A. Logique pure : Base de Données simulée
$utilisateur = 'Alice Liddel';
$taches = ['Acheter du pain', 'Finir le projet PHP', 'Aller à la salle'];

// B. On confie la donnée au moteur de Rendu, qui va nous renvoyer une string HTML compilée
$htmlDeLaPage = renderVue('accueil', [
    'nom' => $utilisateur,
    'liste' => $taches
]);

// C. On emballe cette string compilée dans le Layout global du site web
echo layout('Mon Super Dashboard', $htmlDeLaPage);

?>
```

## 2. L'Arborescence des Vues

Créez un dossier appelé `vues` au même endroit. Nous y allons placer nos 2 fichiers purement graphiques.

### A. Le Squelette Parent (master-layout.php)

Dans `vues/master-layout.php`. Observez la propreté. 

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title><?= htmlspecialchars($titre) ?></title>
    <style>
        body { font-family: system-ui; margin: 0; background: #f8fafc; color: #334155; }
        header { background: #0f172a; color: white; padding: 20px; text-align: center; }
        footer { background: #e2e8f0; text-align: center; padding: 10px; margin-top: 50px; font-size: 0.8rem; }
        main { max-width: 800px; margin: 30px auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
</head>
<body>

    <header>
        <h1>[LOGO] Mon Application Web</h1>
    </header>

    <main>
        <!-- MAGIE : La Vue 'Accueil' viendra s'injecter exactement ici ! -->
        <?= $contenu ?>
    </main>

    <footer>
        &copy; 2026 OmnyDocs Corporation. Tous droits réservés.
    </footer>

</body>
</html>
```

### B. La Vue Enfant (accueil.php)

Dans `vues/accueil.php`. Le code le plus minimaliste du monde.

```html
<h2>Bienvenue sur ton Dashboard, <?= htmlspecialchars($nom) ?> 👋</h2>

<p>Voici l'état de la base de données :</p>

<?php if (empty($liste)): ?>
    <div style="padding: 15px; background: #dcfce7; color: #166534; border-radius: 5px;">
        Tu n'as aucune tâche aujourd'hui !
    </div>
<?php else: ?>
    <ul>
        <?php foreach ($liste as $item): ?>
            <li style="margin-bottom: 10px;"><?= htmlspecialchars($item) ?></li>
        <?php endforeach; ?>
    </ul>
<?php endif; ?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-2 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Vous maitrisez enfin le concept le plus important du web, la séparation Vue-Contrôleur. Le <code>templating.php</code> ne contient aucun HTML, et la vue <code>accueil.php</code> ne contient qu'es déclencheurs basiques.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">L'utilisation combinée d'<code>ob_start()</code> et <code>extract()</code> est la fondation pure du MVC complet que nous aborderons dans le summum du PHP Produit.</span>
    </li>
  </ul>
</div>
