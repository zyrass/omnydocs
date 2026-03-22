---
description: "Projet Pratique : Initiation complète à un système de base de données en mémoire (Session). Création d'un CRUD procédural avec recherche dynamique et algorithme de tri."
icon: lucide/contact
tags: ["PHP", "PROCÉDURAL", "CRUD", "SESSION", "RECHERCHE"]
status: stable
---

# Projet 7 : Gestionnaire de Contacts (CRUD)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    Le célèbre système **CRUD** (Create, Read, Update, Delete) est l'essence même d'une application de gestion. Au lieu d'utiliser une base de données MySQL complexe pour l'instant, nous allons tricher intelligemment : nous allons stocker nos contacts dans un tableau PHP géant qui survivra au rafraichissement de la page grâce aux **Sessions**.

!!! abstract "Objectifs Pédagogiques"
    1.  **Démarrage Sécurisé des Sessions** : Apprendre à utiliser `session_start()` pour stocker un "fichier de sauvegarde" propre à chaque utilisateur.
    2.  **Moteur de Recherche Native** : Utiliser la nouvelle fonction PHP 8 `str_contains` couplée au super filtre `array_filter` pour scanner une base de données.
    3.  **Algorithmique de Tri** : Utiliser le Spaceship Operator `<=>` pour trier un tableau multidirectionnel complexe (Ordre alphabétique croissant ou décroissant).
    4.  **Architecture POST asynchrone** : Faire cohabiter 2 actions complètement différentes sur la même page (Ajout et Suppression) en insérant un Input Hidden magique `name="action"`.

## 1. Moteur Logique & Routage

Créez le fichier `contacts.php`. Les sessions doivent toujours être allumées sur la toute première ligne. Le but ici est de confier la lourde tâche (chercher, trier, effacer) à des fonctions propres.

```php
<?php
declare(strict_types=1);

// 1. DÉMARRAGE DE LA PERSISTANCE
session_start();

/**
 * HELPER SÉCURITÉ (XSS)
 */
function e(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

// 2. LA BASE DE DONNÉES (Stockée dans la Session Utilisateur)
if (!isset($_SESSION['contacts'])) {
    // Si c'est sa 1ère visite, on lui offre 3 contacts par défaut
    $_SESSION['contacts'] = [
        ['id' => 1, 'nom' => 'Dupont', 'prenom' => 'Alice', 'email' => 'alice@example.com', 'telephone' => '0612345678'],
        ['id' => 2, 'nom' => 'Martin', 'prenom' => 'Bob', 'email' => 'bob@example.com', 'telephone' => '0623456789'],
        ['id' => 3, 'nom' => 'Durand', 'prenom' => 'Charlie', 'email' => 'charlie@example.com', 'telephone' => '0634567890'],
    ];
    // Compteur d'Auto-Incrémentation (Comme MySQL)
    $_SESSION['next_id'] = 4;
}

// ============================================
// 3. FONCTIONS ARCHITECTURALES (LE "MODEL")
// ============================================

/**
 * [CREATE] Ajouter un contact
 */
function ajouterContact(array $data): bool {
    // A. Validation
    if (empty($data['nom']) || empty($data['prenom']) || empty($data['email'])) {
        return false;
    }
    
    // B. Filtre PHP natif
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        return false;
    }
    
    // C. Hydratation de la base
    $contact = [
        'id' => $_SESSION['next_id']++, // Donne '4' et prépare un '5'
        'nom' => trim($data['nom']),
        'prenom' => trim($data['prenom']),
        'email' => trim($data['email']),
        'telephone' => trim($data['telephone'] ?? '')
    ];
    
    // D. Sauvegarde dans la session
    $_SESSION['contacts'][] = $contact;
    return true;
}

/**
 * [DELETE] Supprimer un contact (Par son ID Unique !)
 */
function supprimerContact(int $id): bool {
    foreach ($_SESSION['contacts'] as $key => $contact) {
        if ($contact['id'] === $id) {
            unset($_SESSION['contacts'][$key]); // Efface la ligne du tableau
            // On réindexe le DB proprement (Sinon on a des arrays troués: [0, 2, 3])
            $_SESSION['contacts'] = array_values($_SESSION['contacts']); 
            return true;
        }
    }
    return false;
}

/**
 * [SEARCH] Moteur de Recherche en Mémoire
 */
function rechercherContacts(string $query): array {
    if (empty($query)) {
        return $_SESSION['contacts']; // Rien tapé ? Alors on renvoie tout
    }
    
    $query = strtolower($query);
    
    // Filtre puissant : array_filter garde les éléments qui renvoient TRUE
    return array_filter($_SESSION['contacts'], function($contact) use ($query) {
        $nom = strtolower($contact['nom']);
        $prenom = strtolower($contact['prenom']);
        $email = strtolower($contact['email']);
        
        // str_contains est apparu dans PHP 8 (Avant on utilisait l'affreux strpos)
        return str_contains($nom, $query)
            || str_contains($prenom, $query)
            || str_contains($email, $query);
    });
}

/**
 * [SORT] Tri intelligent avec le Spaceship Operator ( <=> )
 */
function trierContacts(array $contacts, string $colonne, string $ordre = 'asc'): array {
    usort($contacts, function($a, $b) use ($colonne, $ordre) {
        // Le Spaceship renvoie 1 (A>B), -1 (A<B) ou 0 (Egaux)
        $comparison = $a[$colonne] <=> $b[$colonne];
        
        // Si l'utilisateur clique sur "Décroissant", on inverse mathématiquement le signe !
        return $ordre === 'desc' ? -$comparison : $comparison;
    });
    
    return $contacts;
}

// ============================================
// 4. LE CONTRÔLEUR HTTP (ROUTAGE POST)
// ============================================

$message = null;
$erreur = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    // Comment savoir si l'humain a appuyé sur "Ajouter" ou sur la poubelle rouge ?
    // Grâce au champ caché "action" dans nos formulaires HTML respectifs !
    if (isset($_POST['action'])) {
        switch ($_POST['action']) {
            case 'ajouter':
                if (ajouterContact($_POST)) {
                    $message = "Le Contact a bien été inséré en base temporelle.";
                } else {
                    $erreur = "Rejet : Veillez à remplir tous les champs obligatoires (*)";
                }
                break;
            
            case 'supprimer':
                $id = (int)($_POST['id'] ?? 0);
                if (supprimerContact($id)) {
                    $message = "Contact évaporé avec succès 💨";
                } else {
                    $erreur = "Piratage : Cet ID de contact n'existe pas.";
                }
                break;
        }
    }
}

// ============================================
// 5. LE CONTRÔLEUR HTTP (ROUTAGE GET) : PRÉPARATION DE LA VUE
// ============================================

// A. Que demande le client dans son URL ? (?recherche=bob&tri=nom&ordre=asc)
$recherche = $_GET['recherche'] ?? '';
$tri = $_GET['tri'] ?? 'nom'; // Par défaut, tri sur le nom
$ordre = $_GET['ordre'] ?? 'asc'; // Par défaut : A->Z

// B. On pipeline ses données à nos fonctions Métier
$contactsVisuels = rechercherContacts($recherche); // 1. On filtre
$contactsVisuels = trierContacts($contactsVisuels, $tri, $ordre); // 2. On trie le reste
?>
```

## 2. Le Rendu Interface (HTML Dynamique)

Sous la balise `?>`. C'est un gros bloc, mais c'est du templating hyper classique. On y retrouve notre fameux `name="action"` caché !

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>SaaS Contacts</title>
    <style>
        body { font-family: system-ui; max-width: 1000px; margin: 30px auto; padding: 20px; background: #e2e8f0; }
        .box { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .msg-ok { background: #dcfce7; color: #166534; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #22c55e;}
        .msg-err { background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #ef4444;}
        
        /* Table V2 */
        table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.95rem; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #cbd5e1; }
        th { background: #0f172a; color: white; cursor: pointer;}
        th a { color: #38bdf8; text-decoration: none; display: flex; align-items: center; justify-content: space-between;}
        tr:hover { background: #f8fafc; }
        
        .search-form { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"], input[type="email"], input[type="tel"] { flex:1; padding: 12px; border: 1px solid #cbd5e1; border-radius: 6px;}
        .btn-search { background: #3b82f6; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
        .btn-del { background: #ef4444; color: white; padding: 8px 12px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
        .btn-create { background: #10b981; width: 100%; margin-top: 10px; color: white; padding: 15px; border: none; border-radius: 6px; font-weight: bold; font-size: 1.1rem; cursor: pointer; }
    </style>
</head>
<body>

<div class="box">
    <h1 style="margin-top: 0">📇 CRM OmnyContacts</h1>

    <?php if ($message): ?> <div class="msg-ok">✅ <?= e($message) ?></div> <?php endif; ?>
    <?php if ($erreur): ?> <div class="msg-err">❌ <?= e($erreur) ?></div> <?php endif; ?>

    <!-- MOTEUR DE RECHERCHE (Transmission en GET pour pouvoir partager l'URL) -->
    <form class="search-form" method="GET">
        <input type="text" name="recherche" placeholder="Rechercher Bob, email..." value="<?= e($recherche) ?>">
        <button type="submit" class="btn-search">Filtrer DB</button>
        <?php if($recherche): ?><a href="contacts.php" style="align-self:center; color: #64748b">✖ Reset</a><?php endif; ?>
    </form>

    <!-- Rendu de la base de données $contactsVisuels -->
    <table>
        <thead>
            <tr>
                <!-- La génération magique de l'Ascenseur de Tri -->
                <th>
                    <a href="?recherche=<?= urlencode($recherche) ?>&tri=nom&ordre=<?= $tri === 'nom' && $ordre === 'asc' ? 'desc' : 'asc' ?>">
                        Nom de famille <span><?= $tri === 'nom' ? ($ordre === 'asc' ? '▲' : '▼') : '↕' ?></span>
                    </a>
                </th>
                <th>Prénom</th>
                <th>E-Mail Pro</th>
                <th>Téléphone</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            <?php if(empty($contactsVisuels)): ?>
                <tr><td colspan="5" style="text-align:center; padding: 30px; font-style:italic">Aucune correspondance.</td></tr>
            <?php else: ?>
                <?php foreach ($contactsVisuels as $c): ?>
                    <tr>
                        <td style="font-weight: bold"><?= e($c['nom']) ?></td>
                        <td><?= e($c['prenom']) ?></td>
                        <td><?= e($c['email']) ?></td>
                        <td><span style="background: #e2e8f0; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;"><?= e($c['telephone']) ?></span></td>
                        <td>
                            <!-- BOUTON DELETE PIÉGÉ D'UN POST (Sécurité : Ne jamais faire une suppression en GET) -->
                            <form method="POST">
                                <input type="hidden" name="action" value="supprimer">
                                <input type="hidden" name="id" value="<?= $c['id'] ?>"> <!-- Pièce Jointe Secrète -->
                                <button type="submit" class="btn-del" onclick="return confirm('Détruire ce dossier ?')">Bannir</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php endif; ?>
        </tbody>
    </table>

    <hr style="border: 0; border-top: 1px dashed #cbd5e1; margin: 40px 0;">

    <h3 style="margin-top: 0">➕ Injecter un nouveau Profil</h3>
    <!-- BOUTON CREATE PIÉGÉ D'UN POST -->
    <form method="POST">
        <input type="hidden" name="action" value="ajouter"> <!-- L'Architecture POST commence ici -->
        
        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
            <input type="text" name="nom" required placeholder="Nom *">
            <input type="text" name="prenom" required placeholder="Prénom *">
        </div>
        <div style="display: flex; gap: 10px;">
            <input type="email" name="email" required placeholder="Email Administratif *">
            <input type="tel" name="telephone" placeholder="Optionnel (06...)">
        </div>

        <button type="submit" class="btn-create">Inscrire en Session</button>
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
      <span class="text-gray-700">Vous avez tapé "bob" dans la barre de recherche. L'URL est devenue <code>?recherche=bob</code> (Méthode GET), ce qui a transmis le mot au contrôleur, qui l'a passé à la fonction <code>rechercherContacts()</code>.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Vous avez cliqué sur "Bannir". Cela a déclenché le Formulaire de suppression en mode POST. Le Contrôleur a détecté <code>$_POST['action'] === 'supprimer'</code> et exécuté l'ordre.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">La persistance : Vous pouvez recharger la page autant de fois que vous le souhaitez, vos nouveaux contacts ajoutés via le Formulaire restent, car le tableau géant réside dans <code>$_SESSION</code> tant que le navigateur n'est pas tué.</span>
    </li>
  </ul>
</div>
