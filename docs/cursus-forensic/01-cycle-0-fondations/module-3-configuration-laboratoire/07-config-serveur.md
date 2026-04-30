---
title: 3.7 Configuration serveur (SSH, Samba, intranet)
description: Configuration des services sur le serveur Debian - SSH avec clés, Samba pour partage Windows/macOS, Apache pour intranet ARTECH simulé, journalisation centralisée pour forensic.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - SSH
  - Samba
  - Apache
  - Debian
data-level: 🟡
---

# 3.7 Configuration serveur (SSH, Samba, intranet)

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 3 heures |
| Niveau | Pratique |

## 1. SSH avec authentification par clés

### 1.1 Génération clés sur poste analyste

```bash
# Sur votre PC Windows ou autre poste
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_lab -C "zyrass@lab"

# Copier la clé publique
cat ~/.ssh/id_ed25519_lab.pub
```

### 1.2 Installation côté serveur

```bash
# Sur le serveur Debian
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-ed25519 AAAA... zyrass@lab" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 1.3 Désactiver mot de passe

```bash
sudo vi /etc/ssh/sshd_config
```

```text
PasswordAuthentication no
PubkeyAuthentication yes
```

```bash
sudo systemctl restart ssh
```

## 2. Samba - Partage de fichiers

### 2.1 Installation

```bash
sudo apt install samba samba-common-bin -y
```

### 2.2 Configuration

```bash
sudo vi /etc/samba/smb.conf
```

```text
# /etc/samba/smb.conf - ARTECH simulé

[global]
    workgroup = ARTECH
    server string = Server ARTECH
    server role = standalone server
    log file = /var/log/samba/log.%m
    max log size = 1000
    logging = file
    panic action = /usr/share/samba/panic-action %d
    
    server signing = auto
    smb encrypt = desired
    
    # Sécurité - mais volontairement avec NTLMv1 pour pédagogie
    ntlm auth = yes
    lanman auth = no
    client lanman auth = no
    client plaintext auth = no
    
    # Logs détaillés pour forensic
    log level = 3
    syslog = 0
    
    map to guest = never

# Partage Compta
[compta]
    path = /data/compta
    browseable = yes
    read only = no
    guest ok = no
    valid users = compta, direction, @admins
    create mask = 0660
    directory mask = 0770

# Partage Direction
[direction]
    path = /data/direction
    browseable = yes
    read only = no
    guest ok = no
    valid users = direction, @admins
    create mask = 0640
    directory mask = 0750

# Partage public ARTECH
[public]
    path = /data/public
    browseable = yes
    read only = no
    guest ok = yes
    create mask = 0664
    directory mask = 0775
```

### 2.3 Création utilisateurs et répertoires

```bash
# Création utilisateurs Linux
sudo useradd -m compta
sudo useradd -m direction
sudo useradd -m stagiaire

# Mot de passe Linux (pas Samba)
sudo passwd compta       # mdp faible pour pédagogie : Compta2026
sudo passwd direction    # Direction2026!
sudo passwd stagiaire    # Stage2026

# Création utilisateurs Samba
sudo smbpasswd -a compta
sudo smbpasswd -a direction
sudo smbpasswd -a stagiaire

# Création répertoires
sudo mkdir -p /data/{compta,direction,public}
sudo chown compta:compta /data/compta
sudo chown direction:direction /data/direction
sudo chown nobody:nogroup /data/public
sudo chmod 770 /data/{compta,direction}
sudo chmod 775 /data/public

# Données fictives
sudo cp /usr/share/man/man1/ls.1.gz /data/compta/factures_2026.gz
sudo cp /usr/share/man/man1/ls.1.gz /data/direction/strategie_secrete.docx
sudo cp /usr/share/man/man1/ls.1.gz /data/public/note_service.txt
```

### 2.4 Démarrage et test

```bash
sudo systemctl enable smbd nmbd
sudo systemctl start smbd nmbd

# Vérification
sudo smbstatus

# Test depuis le serveur
smbclient -L //localhost -U compta
```

## 3. Apache - Intranet ARTECH

### 3.1 Installation

```bash
sudo apt install apache2 php libapache2-mod-php -y
```

### 3.2 Configuration site intranet

```bash
sudo vi /etc/apache2/sites-available/intranet.conf
```

```text
<VirtualHost *:80>
    ServerName intranet.artech.local
    ServerAdmin admin@artech.local
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

### 3.3 Site PHP minimaliste vulnérable (volontairement)

```bash
sudo mkdir /var/www/intranet
sudo vi /var/www/intranet/index.php
```

```php
<?php
// /var/www/intranet/index.php
// Intranet ARTECH - VOLONTAIREMENT VULNÉRABLE pour pédagogie

session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $user = $_POST['user'] ?? '';
    $pass = $_POST['pass'] ?? '';
    
    // Connexion à la "BDD"
    $db = new SQLite3('/var/www/intranet/users.db');
    
    // VULNÉRABILITÉ INTENTIONNELLE : SQL injection
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
    <h1>Intranet ARTECH</h1>
    <?php if (isset($error)) echo "<p style='color:red'>$error</p>"; ?>
    <form method="POST">
        <input type="text" name="user" placeholder="Identifiant"><br>
        <input type="password" name="pass" placeholder="Mot de passe"><br>
        <button type="submit">Connexion</button>
    </form>
</body>
</html>
```

### 3.4 Base SQLite avec utilisateurs

```bash
sudo apt install sqlite3 -y

cd /var/www/intranet
sudo sqlite3 users.db <<EOF
CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT);
INSERT INTO users VALUES (1, 'admin', 'admin2026', 'admin');
INSERT INTO users VALUES (2, 'compta', 'Compta2026', 'comptable');
INSERT INTO users VALUES (3, 'direction', 'Direction2026!', 'direction');
INSERT INTO users VALUES (4, 'stagiaire', 'Stage2026', 'stagiaire');
EOF

sudo chown www-data:www-data users.db
```

### 3.5 Activation

```bash
sudo a2ensite intranet
sudo a2dissite 000-default
sudo systemctl reload apache2
```

## 4. Journalisation centralisée

```bash
# rsyslog déjà installé
# Configuration pour forensic
sudo vi /etc/rsyslog.d/forensic.conf
```

```text
# Capture verbose pour forensic
auth,authpriv.*    /var/log/auth.log
*.*;auth,authpriv.none    /var/log/syslog
daemon.*    /var/log/daemon.log
mail.*      /var/log/mail.log
```

```bash
sudo systemctl restart rsyslog
```

## 5. Tests de validation

```bash
# Test SSH par clé
ssh -i ~/.ssh/id_ed25519_lab zyrass@192.168.50.10

# Test Samba
smbclient -L //192.168.50.10 -U compta

# Test intranet
curl http://192.168.50.10/

# Voir logs
sudo tail -f /var/log/auth.log
sudo tail -f /var/log/samba/log.smbd
sudo tail -f /var/log/apache2/intranet_access.log
```

---

**Chapitre suivant** : [3.8 Installation Windows 11 Pro - Poste 1 (Compta)](03-8-windows11-poste-compta.md)
