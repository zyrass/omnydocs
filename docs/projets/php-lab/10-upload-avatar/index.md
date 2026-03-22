---
description: "Projet Pratique : Coder un système d'upload d'image 100% sécurisé (MIME Type, Finfo, Whitelisting, Génération UUID)."
icon: lucide/upload-cloud
tags: ["PHP", "PROCÉDURAL", "UPLOAD", "FICHIER", "SÉCURITÉ"]
status: stable
---

# Projet 10 : Upload d'Avatar Sécurisé

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    Autoriser un utilisateur à envoyer un fichier sur votre propre Serveur Web est l'action **la plus dangereuse** en informatique. Un hacker peut renommer un virus `.exe` ou un script pirate `.php` en `.jpg` pour prendre le contrôle total du serveur.
    Dans ce projet de classe Master, vous allez oublier l'idée de faire confiance à l'extension d'un fichier. Nous allons analyser l'ADN binaire du fichier grâce à l'extension `finfo` de PHP !

!!! abstract "Objectifs Pédagogiques"
    1.  **L'attribut enctype** : Comprendre pourquoi le formulaire HTML exige impérativement `multipart/form-data` pour ne pas envoyer que du texte.
    2.  **Superglobale $_FILES** : Manipuler la variable spéciale PHP qui intercepte les fichiers en transit dans le dossier temporaire du serveur (`/tmp`).
    3.  **L'ADN Binaire (MIME Type)** : Utiliser `finfo_file` pour scanner l'intérieur du fichier et découvrir sa vraie nature, indépendamment de son `.extension`.
    4.  **Nommage Anti-Collision** : Générer un nouveau nom unique indéchiffrable avec `uniqid()` pour que les fichiers ne s'écrasent jamais et qu'un hacker ne puisse pas deviner l'URL d'accès.

## 1. La Classe Uploader

Créez un dossier appelé `uploads` à la racine de votre projet (à côté de vos fichiers PHP). C'est là que les avatars sains seront rangés.
Créez ensuite `uploader.php`.

```php
<?php
declare(strict_types=1);

/**
 * Uploader d'Images Strict et Sécurisé
 */

class AvatarUploader {
    
    // Configurations stricte de la Classe
    private const TAILLE_MAX = 2 * 1024 * 1024; // 2 MégaOctets (2 MB)
    
    // Liste Blanche des extensions théoriques
    private const EXT_AUTORISEES = ['jpg', 'jpeg', 'png', 'webp', 'gif'];
    
    // L'ADN Binaire Réel accepté (MIME Type Officiel)
    private const MIME_AUTORISES = [
        'image/jpeg', 
        'image/png', 
        'image/webp',
        'image/gif'
    ];
    
    // Dossier d'atterrissage sur le serveur
    private string $dossierCible;
    
    public function __construct(string $dossierObjectif = 'uploads/') {
        // Optionnel : on crée le dossier s'il n'existe pas
        if (!is_dir($dossierObjectif)) {
            mkdir($dossierObjectif, 0755, true); // CHMOD 755 (Lecture/Exécution Publique, Écriture Privée)
        }
        $this->dossierCible = rtrim($dossierObjectif, '/') . '/';
    }
    
    /**
     * Traite un fichier issu de $_FILES['champ_fichier']
     * Retourne un tableau structuré : ['success' => bool, 'message' => string, 'path' => string]
     */
    public function uploaderUnFichier(array $fichier): array {
        
        // 1. DÉTÈCTION DES ERREURS DE TRANSFERT DU PROTOCOLE HTTP
        // UPLOAD_ERR_OK = Code 0 (Tout s'est bien passé jusqu'au dossier temporaire)
        if (!isset($fichier['error']) || is_array($fichier['error'])) {
            return $this->reponse(false, 'Format de transfert HTTP corrompu.');
        }
        
        switch ($fichier['error']) {
            case UPLOAD_ERR_OK:
                break; // Parfait, on continue !
            case UPLOAD_ERR_INI_SIZE:
            case UPLOAD_ERR_FORM_SIZE:
                return $this->reponse(false, 'Le fichier pèse trop de mégaoctets.');
            case UPLOAD_ERR_PARTIAL:
                return $this->reponse(false, 'La connexion internet a sauté, fichier incomplet.');
            case UPLOAD_ERR_NO_FILE:
                return $this->reponse(false, 'Aucun fichier transmis. Avez-vous cliqué sur le bouton Parcourir ?');
            default:
                return $this->reponse(false, 'Erreur serveur inconnue.');
        }
        
        // 2. VÉRIFICATION DE LA TAILLE RÉELLE (En plus de PHP.ini)
        if ($fichier['size'] > self::TAILLE_MAX) {
            return $this->reponse(false, 'Le poids dépasse la limite stricte de 2 MB.');
        }
        
        // 3. VÉRIFICATION MAGIQUE DU MIME TYPE (La Protection Ultime)
        // On demande au serveur de scanner les octets binaires ('magic bytes') du fichier contenu dans le dossier Temp (/tmp/phpA4B2...)
        $finfo = new finfo(FILEINFO_MIME_TYPE);
        $mineTypeReel = $finfo->file($fichier['tmp_name']);
        
        if ($mineTypeReel === false || !in_array($mineTypeReel, self::MIME_AUTORISES, true)) {
            return $this->reponse(false, "Ce fichier n'est pas une image. Falsification détéctée.");
        }
        
        // 4. VÉRIFICATION SECONDAIRE DE L'EXTENSION
        // On découpe la chaine par le point "." et on prend le dernier bout (end).
        $nomOriginal = pathinfo($fichier['name'], PATHINFO_FILENAME);
        // Evite les failles d'attaque Null Byte ou de double extension fichier.php.jpg
        $nomOriginalClean = preg_replace('/[^a-zA-Z0-9-_\.]/', '', $nomOriginal);
        
        $extension = strtolower(pathinfo($fichier['name'], PATHINFO_EXTENSION));
        
        if (!in_array($extension, self::EXT_AUTORISEES, true)) {
             return $this->reponse(false, 'Le format de l\'extension (.' . $extension . ') est inconnu au bataillon.');
        }
        
        // 5. DESTRUCTION DU NOM ORIGINAL ET GÉNÉRATION D'UN UUID UNIQUE
        // Le hacker ne peut jamais écraser un vieux fichier ou appeler index.php car on casse la nomination
        // uniqid renvoie par exemple '64a9b2c3d4e5f' (Timestamp en millisecondes héxadécimales)
        $nouveauNomFichier = sprintf('%s-%s.%s',
            $nomOriginalClean, // On garde une trace de ce qu'il a tenté de taper
            uniqid(more_entropy: true), // + de désordre (Entropy)
            $extension
        );
        
        // 6. TÉLÉPORTATION FINALE !
        // Le chemin absolu d'arrivée : uploads/mon-chat-64a9b2c3d4e5f.jpg
        $cheminFinal = $this->dossierCible . $nouveauNomFichier;
        
        // On déplace le fichier du /tmp du serveur vers notre dossier /uploads
        if (!move_uploaded_file($fichier['tmp_name'], $cheminFinal)) {
            return $this->reponse(false, 'Échec d\'écriture sur le disque dur. Un problème de permission CHMOD ?');
        }
        
        // C'est un succès absolu
        return $this->reponse(true, 'Avatar Propulsé et Sécurisé !', $cheminFinal);
    }
    
    // Petit Formatteur Array natif PHP
    private function reponse(bool $succes, string $msg, string $chemin = null): array {
        return [
            'success' => $succes,
            'message' => $msg,
            'path' => $chemin
        ];
    }
}

// ==========================================
// LE CONTRÔLEUR HTTP (POST INJECTION)
// ==========================================

$feedback = null;
$nouveauCheminImage = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['mon_avatar'])) {
    
    // 1. Initialisation de la Classe
    $gestionnaireUpload = new AvatarUploader();
    
    // 2. On envoie tout le payload $_FILES
    $resultat = $gestionnaireUpload->uploaderUnFichier($_FILES['mon_avatar']);
    
    // 3. Traitement du retour fonctionnel Array
    if ($resultat['success'] === true) {
        $feedback = [ 'ok' => true, 'texte' => $resultat['message'] ];
        $nouveauCheminImage = $resultat['path']; // Contient "uploads/nom-fau-617823.png"
    } else {
        $feedback = [ 'ok' => false, 'texte' => $resultat['message'] ];
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Laboratoire Upload</title>
    <!-- Code CSS Minimaliste, pas de surcharge ! -->
    <style>
        body { font-family: system-ui; text-align: center; margin-top: 50px; background: #e2e8f0; color: #1e293b;}
        .card { background: white; max-width: 450px; margin: auto; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .upload-zone { border: 2px dashed #94a3b8; padding: 30px; border-radius: 8px; margin-bottom: 20px; background: #f8fafc; cursor: pointer; transition: 0.3s;}
        .upload-zone:hover { border-color: #3b82f6; background: #eff6ff;}
        input[type="file"] { margin: 15px 0;}
        button { background: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer;}
        .preview { margin-top: 20px; border-radius: 50%; width: 150px; height: 150px; object-fit: cover; border: 4px solid #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
        .alr { padding: 15px; border-radius: 6px; margin-top: 20px; font-weight: bold; }
        .alr-ok { background: #dcfce7; color: #166534; border: 1px solid #4ade80;}
        .alr-ko { background: #fee2e2; color: #991b1b; border: 1px solid #f87171;}
    </style>
</head>
<body>

<div class="card">
    <h2>📸 Changement d'Avatar</h2>
    <p style="color: #64748b; font-size: 0.9rem;">Formats Acceptés : JPG, WebP, PNG, GIF</p>
    
    <!-- L'encodage multipart/form-data EST OBLIGATOIRE POUR UN FICHIER ! -->
    <form method="POST" enctype="multipart/form-data">
        <label class="upload-zone">
            <div>📂 Sélectionnez une Image sur votre ordinateur</div>
            <!-- accept="..." Guide le navigateur mais ne protège de rien côté serveur ! -->
            <input type="file" name="mon_avatar" required accept="image/png, image/jpeg, image/webp, image/gif">
        </label>
        
        <button type="submit">Propulser sur le Serveur 🚀</button>
    </form>
    
    <?php if ($feedback): ?>
        <div class="alr <?= $feedback['ok'] ? 'alr-ok' : 'alr-ko' ?>">
            <?= htmlspecialchars($feedback['texte']) ?>
        </div>
        
        <?php if ($feedback['ok'] && $nouveauCheminImage): ?>
            <!-- Affichage de la photo qui vient juste de pop dans le dossier "uploads/" -->
            <img class="preview" src="<?= htmlspecialchars($nouveauCheminImage) ?>" alt="Nouvel Avatar">
        <?php endif; ?>
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
      <span class="text-gray-700">Vous avez testé le système et vu apparaître un tout nouveau nom long très laid comme <code>monchien-627a81b29a.jpg</code>. C'est parfait, c'est ce qu'on attend du générateur d'UUID basé sur l'Entropy temporelle. Finies les collisions de noms de fichiers (Deux utilisateurs qui uploadent <code>profil.jpg</code>).</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Vous avez changé volontairement le nom d'un fichier excel <code>compta.xlsx</code> en <code>compta.jpg</code> avant de l'envoyer. L'extension PHP <code>finfo_file</code> a analysé le coeur binaire, détecté un Spreadsheet XML et a levé l'Alerte Rouge : Falsification Détectée. Le Hacker (Vous) est coincé.</span>
    </li>
  </ul>
</div>
