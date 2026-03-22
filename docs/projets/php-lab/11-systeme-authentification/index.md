---
description: "Projet Pratique : Coder un système d'authentification robuste (Login, Register, Logout) avec hachage sécurisé de mot de passe (Bcrypt / Argon2)."
icon: lucide/shield-alert
tags: ["PHP", "PROCÉDURAL", "AUTH", "LOGIN", "SÉCURITÉ"]
status: stable
---

# Projet 11 : Système d'Authentification

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    L'Authentification (Auth), c'est la pierre angulaire des Applications SaaS, E-Commerce ou Réseaux Sociaux. C'est elle qui distingue le visiteur anonyme de l'utilisateur certifié.
    Dans ce projet, vous allez concevoir un système Inscription/Connexion blindé. Plus de mots de passe en clair dans la base de données. Plus de failles de session.

!!! abstract "Objectifs Pédagogiques"
    1.  **Hachage Irréversible** : Comprendre pourquoi la fonction `password_hash()` avec Bcrypt/Argon2 est vitale pour la confidentialité. MD5 et SHA-1 sont morts.
    2.  **Validation d'Identité** : Vérifier un formulaire de connexion avec la fonction native `password_verify()`.
    3.  **Gestion de Session d'État** : Apprendre à injecter l'ID Utilisateur dans la variable `$_SESSION` pour que l'Auth persiste en naviguant de page en page.
    4.  **Déconnexion Nucléaire** : Coder un script de Logout absolu qui écrase la session et le cookie navigateur.

## 0. Préparation (La fausse Base de Données)

Normalement, nos utilisateurs sont stockés dans MySQL (Module 7). Ici, en guise d'entraînement sur la Session pure, nous utiliserons un fichier JSON en guise de BDD (`users.json`).

> **Créez un fichier vide `users.json` contenant uniquement ceci au départ :** `{}`

## 1. La Classe d'Authentification

Créez `auth.php`. Ce sera notre Contrôleur Logique, il embarquera toutes les méthodes (Register, Login, Logout) qui pilotent les données de session.

```php
<?php
declare(strict_types=1);

session_start();

/**
 * Moteur d'Authentification Sécurisé
 */
class Authenticator {
    
    private string $fichierDB = 'users.json';
    
    /**
     * INSCRIPTION [REGISTER]
     */
    public function inscrire(string $email, string $motDePasseBrut): array {
        
        $email = strtolower(trim($email));
        
        // Validation basique
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            return ['success' => false, 'message' => "Format d'email expériemental non supporté."];
        }
        if (mb_strlen($motDePasseBrut) < 8) {
            return ['success' => false, 'message' => "Mot de passe trop faible (8 char min)."];
        }
        
        // Chargement de la Base de données locale
        $db = json_decode(file_get_contents($this->fichierDB), true) ?? [];
        
        // Vérification de doublon
        if (isset($db[$email])) {
            return ['success' => false, 'message' => "Un pirate (ou cous) a déjà pris cet email."];
        }
        
        // === LA MAGIE DU HACHAGE ===
        // Bcrypt génère un "Sel" aléatoire, le mélange au mot de passe et mouline le tout.
        // Résultat Inversable (Même avec l'ordinateur le plus puissant du monde)
        $hashSecurise = password_hash($motDePasseBrut, PASSWORD_BCRYPT, ['cost' => 12]);
        
        // Sauvegarde de l'Utilisateur
        $db[$email] = [
            'id' => uniqid('usr_'),
            'email' => $email,
            'password_hash' => $hashSecurise,
            'date_creation' => date('Y-m-d H:i:s')
        ];
        
        file_put_contents($this->fichierDB, json_encode($db, JSON_PRETTY_PRINT));
        
        return ['success' => true, 'message' => "Inscription validée, Agent. Bienvenue au QG."];
    }
    
    /**
     * CONNEXION [LOGIN]
     */
    public function connecter(string $email, string $motDePassePropose): array {
        
        $email = strtolower(trim($email));
        $db = json_decode(file_get_contents($this->fichierDB), true) ?? [];
        
        // 1. L'email existe-t-il ?
        if (!isset($db[$email])) {
            // SÉCURITÉ : Ne JAMAIS dire "L'email n'existe pas" (Sinon les hackers savent qui a un compte ou non)
            return ['success' => false, 'message' => "Identifiants invalides."];
        }
        
        $userDB = $db[$email];
        
        // 2. Vérification Mathématique du Mot de Passe
        // password_verify reconnait le "Sel" utilisé par Bcrypt lors de l'inscription !
        if (!password_verify($motDePassePropose, $userDB['password_hash'])) {
            return ['success' => false, 'message' => "Identifiants invalides."];
        }
        
        // 3. SUCCÈS : OUVERTURE DE LA SESSION PERSISTANTE
        // On casse l'ancien ID de Session PHP (Anti-Session Fixation Attack)
        session_regenerate_id(true);
        
        // On injecte les preuves de connexion en Session Serveur
        $_SESSION['auth_user_id'] = $userDB['id'];
        $_SESSION['auth_email'] = $userDB['email'];
        $_SESSION['auth_last_login'] = time();
        
        return ['success' => true, 'message' => "Portes blindées ouvertes."];
    }
    
    /**
     * DÉCONNEXION [LOGOUT]
     */
    public function deconnecter(): void {
        // A. On vide nos variables de session
        $_SESSION = [];
        // B. On détruit la session globale sur le Serveur
        session_destroy();
        // C. On supprime le Cookie "PHPSESSID" du navigateur de l'utilisateur
        if (ini_get("session.use_cookies")) {
            $params = session_get_cookie_params();
            setcookie(session_name(), '', time() - 42000,
                $params["path"], $params["domain"],
                $params["secure"], $params["httponly"]
            );
        }
    }
    
    /**
     * EST-IL CONNECTÉ ? [MIDDLEWARE STATE]
     */
    public function estConnecte(): bool {
        return isset($_SESSION['auth_user_id']);
    }
}
?>
```

## 2. Le Portail (Vues & Routing)

Créez `passerelle.php`. C'est l'interface visuelle. Elle va réagir selon l'état de l'utilisateur évalué par le `Moteur Authenticator`.

```php
<?php
// On inclut notre moteur
require_once 'auth.php';

$auth = new Authenticator();
$messageSysteme = null;

// ============================================
// LOGIQUE DE ROUTAGE (POST)
// ============================================
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    // ACTION : DÉCONNEXION
    if (isset($_POST['action']) && $_POST['action'] === 'logout') {
        $auth->deconnecter();
        header("Location: passerelle.php"); // Redirection propre vers la page d'accueil (Login)
        exit();
    }
    
    // ACTION : INSCRIPTION
    if (isset($_POST['action']) && $_POST['action'] === 'register') {
        $resultat = $auth->inscrire($_POST['email'] ?? '', $_POST['password'] ?? '');
        $messageSysteme = $resultat; // Array avec 'success' et 'message'
    }
    
    // ACTION : CONNEXION
    if (isset($_POST['action']) && $_POST['action'] === 'login') {
        $resultat = $auth->connecter($_POST['email'] ?? '', $_POST['password'] ?? '');
        $messageSysteme = $resultat;
        
        // Si ça a marché, on recharge la page pour tomber direct sur le Dashboard protégé
        if ($resultat['success']) {
            header("Location: passerelle.php");
            exit();
        }
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>QG Central</title>
    <!-- Tailwind par CDN pour faire une UI très propre rapidement -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-200 min-h-screen flex items-center justify-center p-4">

    <!-- L'UTILISATEUR EST-IL CONNECTÉ ? (Vérification par la Session PHP) -->
    
    <?php if ($auth->estConnecte()): ?>
    
        <!-- ============================================== -->
        <!-- VUE A : LE DASHBOARD PROTÉGÉ (Privé) -->
        <!-- ============================================== -->
        <div class="bg-slate-800 p-8 rounded-xl shadow-2xl w-full max-w-2xl border border-slate-700">
            <h1 class="text-3xl font-bold text-emerald-400 mb-2">Centre de Commandement</h1>
            <p class="text-slate-400 mb-8 border-b border-slate-700 pb-4">Accès Niveau Accrédité</p>
            
            <div class="grid grid-cols-2 gap-4 mb-8">
                <div class="bg-slate-900 p-4 rounded-lg">
                    <span class="block text-xs text-slate-500 uppercase">Agent Actif</span>
                    <span class="text-lg font-bold text-white"><?= htmlspecialchars($_SESSION['auth_email']) ?></span>
                </div>
                <div class="bg-slate-900 p-4 rounded-lg">
                    <span class="block text-xs text-slate-500 uppercase">Matricule Interne</span>
                    <span class="text-lg font-mono text-cyan-400"><?= htmlspecialchars($_SESSION['auth_user_id']) ?></span>
                </div>
            </div>
            
            <form method="POST">
                <input type="hidden" name="action" value="logout">
                <button type="submit" class="w-full bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 px-4 rounded transition">
                    Verrouiller la session (Logout)
                </button>
            </form>
        </div>
        
    <?php else: ?>
    
        <!-- ============================================== -->
        <!-- VUE B : PORTES DU BUNKER (Formulaires) -->
        <!-- ============================================== -->
        <div class="w-full max-w-md">
            
            <!-- Affichage des Alertes -->
            <?php if ($messageSysteme): ?>
                <div class="p-4 mb-6 rounded border <?= $messageSysteme['success'] ? 'bg-emerald-900/50 border-emerald-500 text-emerald-300' : 'bg-rose-900/50 border-rose-500 text-rose-300' ?>">
                    <?= htmlspecialchars($messageSysteme['message']) ?>
                </div>
            <?php endif; ?>
            
            <div class="bg-slate-800 p-8 rounded-t-xl border-b-2 border-slate-900">
                <h2 class="text-2xl font-bold text-white mb-6">S'identifier (Login)</h2>
                <form method="POST" class="space-y-4">
                    <input type="hidden" name="action" value="login">
                    <div>
                        <label class="block text-sm text-slate-400 mb-1">Dossier (Email)</label>
                        <input type="email" name="email" class="w-full bg-slate-900 border border-slate-700 rounded p-3 text-white focus:border-cyan-500 outline-none" required>
                    </div>
                    <div>
                        <label class="block text-sm text-slate-400 mb-1">Sésame (Password)</label>
                        <input type="password" name="password" class="w-full bg-slate-900 border border-slate-700 rounded p-3 text-white focus:border-cyan-500 outline-none" required>
                    </div>
                    <button type="submit" class="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 rounded transition">Connexion</button>
                </form>
            </div>
            
            <div class="bg-slate-800/50 p-6 rounded-b-xl border-t border-slate-700/50 mt-1">
                <h3 class="text-lg font-bold text-slate-300 mb-4">Nouvelle Recrue ?</h3>
                <form method="POST" class="flex gap-2">
                    <input type="hidden" name="action" value="register">
                    <input type="email" name="email" placeholder="Email" class="flex-1 bg-slate-900 border border-slate-700 rounded px-3 text-sm text-white" required>
                    <input type="password" name="password" placeholder="Pass (8 min)" class="w-32 bg-slate-900 border border-slate-700 rounded px-3 text-sm text-white" required minlength="8">
                    <button type="submit" class="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded text-sm font-bold text-white">S'enrôler</button>
                </form>
            </div>
            
        </div>
        
    <?php endif; ?>

</body>
</html>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-2 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Inscrivez-vous via le second formulaire. Ouvrez votre fichier <code>users.json</code> généré. Vous verrez que votre mot de passe "admin123" n'est plus lisible, il a été transformé par Bcrypt en <code>$2y$12$D2M...</code>. Si la BDD fûite, les Hackers n'auront rien.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Connectez-vous avec ce même mot de passe. Le système va utiliser <code>password_verify</code> pour valider mathématiquement votre frappe contre le Hash. La page se rafraichit et bim ! Vous êtes sur le <strong>Dashboard Protégé</strong>.</span>
    </li>
  </ul>
</div>
