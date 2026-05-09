---
description: "Configuration des services sur le serveur Debian - SSH avec clés, Samba pour partage Windows/macOS, Apache pour intranet ARTECH simulé, journalisation centralisée pour forensic."
icon: lucide/settings
tags: ["SSH", "SAMBA", "APACHE", "DEBIAN"]
---

# Configuration serveur (SSH, Samba, intranet)

<div
  class="omny-meta"
  data-level="🟡 Standard"
  data-version="Modèle 2026"
  data-time="3 heures">
</div>

!!! note "**Livrables :** _Services de partage de fichiers (Samba) et d'Intranet Web (Apache) opérationnels et vulnérables_"
!!! note "**Auto-explication :** _10 minutes_"

<br>

---

<br>

!!! quote "L'analogie de la vitrine commerciale"

    Un bâtiment vierge ne sert à rien s'il n'accueille pas de clients. De même, un serveur Linux nu ne présente aucun intérêt pour un pirate. Ce qui l'attire, ce sont les services exposés : le partage de fichiers (Samba) qui contient les données comptables, et le site Intranet (Apache) qui sert de porte d'entrée. Dans ce chapitre, nous allons "meubler" notre serveur ARTECH en y installant les services vitaux d'une PME, tout en laissant intentionnellement quelques fenêtres ouvertes.

## Objectifs pédagogiques

!!! tip "À la fin de ce chapitre, vous serez capable de :"

    - Sécuriser l'accès d'administration (SSH) via l'utilisation stricte de clés cryptographiques.
    - Déployer un serveur de fichiers Samba compatible avec l'Active Directory (simulé ou réel).
    - Monter un serveur Web Apache hébergeant une application PHP/SQLite volontairement vulnérable (SQLi).
    - Configurer la journalisation centralisée (rsyslog) pour faciliter la collecte de preuves (Forensic).

<br>

---

<br>

## Verrouillage de l'administration SSH

La première étape consiste à bloquer les attaques par force brute sur notre accès d'administration en interdisant l'utilisation de mots de passe.

### Génération des clés sur le poste de l'analyste

!!! info "L'algorithme moderne de référence est Ed25519 (plus court et plus sécurisé que RSA)."

```bash title="Commandes Terminal (PC Analyste) - Génération de la paire de clés SSH Ed25519"
# Génération de la paire de clés sur votre machine personnelle
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_lab -C "dupond@lab"
# Affichage de la clé PUBLIQUE (À copier dans le presse-papier)
cat ~/.ssh/id_ed25519_lab.pub
```

### Déploiement sur le serveur Debian

!!! quote "Connectez-vous au serveur (`192.168.50.10`) avec le mot de passe, puis injectez la clé."

Voici comment faire :

```bash title="Commandes Linux (Serveur) - Ajout de la clé publique"
# Création du répertoire SSH et gestion stricte des droits
mkdir -p ~/.ssh
chmod 700 ~/.ssh
    
# Collez votre clé publique à l'intérieur des guillemets (Remplacer AAAA...)
echo "ssh-ed25519 AAAA... dupond@lab" >> ~/.ssh/authorized_keys
    
# Sécurisation du fichier d'autorisation
chmod 600 ~/.ssh/authorized_keys
```

### Désactivation définitive du mot de passe

> Il est important de désactiver la connexion par mot de passe pour éviter les attaques par force brute.  

!!! warning "Attention : Si vous n'avez pas configuré la clé SSH, vous serez bloqué hors du serveur ! Vérifiez d'abord votre connexion SSH par clé avant de continuer."

```bash title="Commandes Linux (Serveur) - Configuration sshd_config"
sudo vi /etc/ssh/sshd_config
```
    
```text title="Modifications requises dans sshd_config"
PasswordAuthentication no          # INTERDIT la connexion par mot de passe
PubkeyAuthentication yes           # OBLIGE la connexion par clé
```
    
```bash title="Relance du service"
sudo systemctl restart ssh
```

#### Test de la connexion SSH

Si la connexion SSH réussit sans vous demander de mot de passe, félicitations, vous avez réussi ! Sinon, vérifiez que vous avez bien suivi les étapes précédentes.

```bash title="Commandes Linux (Serveur) - Test de la connexion SSH"
ssh -i ~/.ssh/id_ed25519_lab dupond@192.168.50.10
```

<br>

---

<br>

## Partage de fichiers (Samba)

Le serveur sert principalement de serveur de fichiers et héberge les documents de la société ARTECH.

### Installation et Configuration

> L'utilisation d'un serveur de fichiers est essentielle pour permettre le partage de fichiers entre différents utilisateurs. Dans ce cas, nous utilisons Samba pour permettre le partage de fichiers entre différents utilisateurs.  
> N'oubliez pas d'adapter les chemins et les noms de fichiers à votre configuration personnelle.

```bash title="Commandes Linux - Installation des paquets Samba"
sudo apt install samba samba-common-bin -y
```
    
```bash title="Commandes Linux - Édition du fichier smb.conf"
sudo vi /etc/samba/smb.conf
```

> Voici à quoi devrait ressembler votre fichier smb.conf :
    
```text title="Fichier /etc/samba/smb.conf - Partages ARTECH"
[global]
    workgroup = ARTECH
    server string = Server ARTECH
    server role = standalone server
    log file = /var/log/samba/log.%m
    max log size = 1000
    logging = file
    
    # PARAMÈTRES VOLONTAIREMENT VULNÉRABLES (Pour Pédagogie)
    # On autorise l'authentification NTLMv1, cible privilégiée des attaquants
    ntlm auth = yes
    lanman auth = no
    client lanman auth = no
    client plaintext auth = no
    
    # Logs extrêmement détaillés pour nos futures analyses Forensic
    log level = 3
    syslog = 0
    map to guest = never

# ---- PARTAGE COMPTA ----
[compta]
    path = /data/compta
    browseable = yes
    read only = no
    guest ok = no
    valid users = compta, direction
    create mask = 0660
    directory mask = 0770

# ---- PARTAGE DIRECTION ----
[direction]
    path = /data/direction
    browseable = yes
    read only = no
    guest ok = no
    valid users = direction
    create mask = 0640
    directory mask = 0750

# ---- PARTAGE PUBLIC ----
[public]
    path = /data/public
    browseable = yes
    read only = no
    guest ok = yes
    create mask = 0664
    directory mask = 0775
```

### Création des utilisateurs et des données fictives

Nous devons simuler la vie de l'entreprise avec des faux comptes (Mots de passe faibles inclus).

#### Peuplement du serveur de fichiers

> L'objectif étant de se rapprocher au maximum de la réalité. Ainsi, nous allons créer des utilisateurs et des dossiers pour simuler la vie de l'entreprise.

```bash title="Commandes Linux - Création des comptes et dossiers"
# Création des utilisateurs système Linux
sudo useradd -m compta
sudo useradd -m direction
sudo useradd -m stagiaire

# Création des accès Samba (Mots de passe contextuels faibles)
sudo smbpasswd -a compta      # Entrer : Compta2026
sudo smbpasswd -a direction   # Entrer : Direction2026!
sudo smbpasswd -a stagiaire   # Entrer : Stage2026

# Création des arborescences de données
sudo mkdir -p /data/{compta,direction,public}

# Attribution des droits propriétaires Linux
sudo chown compta:compta /data/compta
sudo chown direction:direction /data/direction
sudo chown nobody:nogroup /data/public

# Définition stricte des permissions octales
sudo chmod 770 /data/{compta,direction}
sudo chmod 775 /data/public

# Génération de "fausses" données pour donner du réalisme
sudo cp /usr/share/man/man1/ls.1.gz /data/compta/factures_2026.gz
sudo cp /usr/share/man/man1/ls.1.gz /data/direction/strategie_secrete.docx
sudo cp /usr/share/man/man1/ls.1.gz /data/public/note_service.txt
```

#### Vérification

> Permet de s'assurer que les partages sont accessibles.

```bash title="Commandes Linux - Vérification des partages"
sudo smbstatus
```

#### Activation

> Permet de démarrer et d'activer les services Samba.

```bash title="Commandes Linux - Démarrage Samba"
sudo systemctl enable smbd nmbd
sudo systemctl start smbd nmbd

# Afficher l'état du service
sudo smbstatus
```

<br>

---

<br>

## Le portail Intranet (Apache & PHP)

La PME possède un portail interne avec une base de données de connexion. Ce portail a été codé "sur un coin de table" et présente une faille classique : l'Injection SQL.

### Installation et structure du site

> Nous allons installer Apache et PHP pour héberger le site intranet. Ce site est volontairement vulnérable pour les besoins de l'exercice.

#### Déploiement du serveur Web

```bash title="Commandes Linux - Installation Apache/PHP"
# Installation des paquets
sudo apt install apache2 php libapache2-mod-php sqlite3 -y

# Création du conteneur virtuel (VirtualHost)
sudo vi /etc/apache2/sites-available/intranet.conf
```
    
```text title="Fichier /etc/apache2/sites-available/intranet.conf"
<VirtualHost *:80>
    ServerName intranet.artech.local
    DocumentRoot /var/www/intranet

    <Directory /var/www/intranet>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/intranet_error.log
    CustomLog ${APACHE_LOG_DIR}/intranet_access.log combined
</VirtualHost>
```

#### Activation du site

```bash title="Commandes Linux - Activation du site"
# Activation du site
sudo a2ensite intranet.conf

# Rechargement de la configuration Apache
sudo systemctl reload apache2

# Afficher l'état du service
sudo apache2ctl status
```

### Le code applicatif vulnérable

!!! danger "Vulnérabilité Intentionnelle"
    Le code ci-dessous ne gère aucune échappement des entrées utilisateurs. Il est trivialement vulnérable aux attaques par Injection SQL (SQLi). C'est le but recherché.

#### Application PHP Intranet

```bash title="Commandes Linux - Création de la page"
# Création du répertoire du site
sudo mkdir -p /var/www/intranet
# Création de la page d'accueil
sudo vi /var/www/intranet/index.php
```
    
```php title="Fichier /var/www/intranet/index.php"
<?php
// Intranet ARTECH - VOLONTAIREMENT VULNÉRABLE pour la pédagogie

session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $user = $_POST['user'] ?? '';
    $pass = $_POST['pass'] ?? '';
    
    // Connexion à la base de données locale
    $db = new SQLite3('/var/www/intranet/users.db');
    
    // /!\ INJECTION SQL POSSIBLE ICI /!\
    $query = "SELECT * FROM users WHERE username='$user' AND password='$pass'";
    $result = $db->query($query);
    
    if ($result && $result->fetchArray()) {
        $_SESSION['user'] = $user;
        header('Location: dashboard.php');
        exit;
    } else {
        $error = "Identifiants incorrects";
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>Intranet ARTECH</title></head>
<body>
    <h1>Connexion Intranet ARTECH</h1>
    <?php if (isset($error)) echo "<p style='color:red'>$error</p>"; ?>
    <form method="POST">
        <input type="text" name="user" placeholder="Identifiant"><br>
        <input type="password" name="pass" placeholder="Mot de passe"><br>
        <button type="submit">Connexion</button>
    </form>
</body>
</html>
```

### La base de données SQLite

> Permet de s'assurer que les partages sont accessibles.

```bash title="Commandes Linux - Création de la BDD via Heredoc"
cd /var/www/intranet

sudo sqlite3 users.db <<EOF
CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT);
INSERT INTO users VALUES (1, 'admin', 'admin2026', 'admin');
INSERT INTO users VALUES (2, 'compta', 'Compta2026', 'comptable');
INSERT INTO users VALUES (3, 'direction', 'Direction2026!', 'direction');
INSERT INTO users VALUES (4, 'stagiaire', 'Stage2026', 'stagiaire');
EOF

# L'utilisateur web (www-data) doit avoir les droits de lecture/écriture
sudo chown www-data:www-data users.db
sudo chmod 660 users.db
```

### Activation finale du site Web

> Permet de s'assurer que le site Web est accessible sur le serveur apache sur le port 80 et que les autres services sont bien démarrés.

```bash title="Commandes Linux - Basculement du VirtualHost"
sudo a2ensite intranet
sudo a2dissite 000-default
sudo systemctl reload apache2
```

<br>

---

<br>

## Tests de validation depuis le poste Analyste

Avant de quitter, assurez-vous que tous les services répondent.

### Commandes de vérification globale

```bash title="Commandes Linux - Tests de connexion"
# 1. Test SSH par clé (Le mot de passe ne doit PAS vous être demandé)
ssh -i ~/.ssh/id_ed25519_lab dupond@192.168.50.10
    
# 2. Test Samba (Devrait lister les partages 'compta', 'direction', 'public')
smbclient -L //192.168.50.10 -U compta
    
# 3. Test intranet (Devrait renvoyer le code HTML de la page de connexion)
curl http://192.168.50.10/
```

<br>

---

<br>

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le serveur Debian est désormais le cœur vivant de l'entreprise ARTECH. Il héberge les fichiers sensibles via Samba (protégés par des mots de passe humains, donc faillibles), et présente un Intranet truffé de failles applicatives (SQLi). Il est prêt à subir le courroux de nos futurs exercices d'attaque pour, par la suite, générer les traces Forensic (fichiers log) que nous devrons analyser.

> [Chapitre suivant : 3.8 Installation Windows 11 Pro - Poste 1 (Compta) →](08-windows11-poste-compta.md)
>
> [Retour à l'index →](./index.md)

<br>
