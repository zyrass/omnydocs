---
description: "Déploiement et sécurisation avancée du serveur OpenSSH pour l'administration distante sécurisée."
icon: lucide/book-open-check
tags: ["SSH", "OPENSSH", "RESEAU", "SECURITE", "CRYPTOGRAPHIE"]
---

# Administration Sécurisée (SSH)

<div
  class="omny-meta"
  data-level="🟢 Débutant à 🔴 Avancé"
  data-version="1.0"
  data-time="25 - 35 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Les services réseaux (DNS, FTP, SSH) sont comme les différents guichets spécialisés d'une grande entreprise. Le DNS est l'accueil qui indique où se trouve chaque bureau, SSH est l'entrée de service hyper-sécurisée pour la maintenance, et FTP est le quai de chargement des marchandises. Chaque guichet mal surveillé est une opportunité d'intrusion._

!!! quote "La ligne de vie de l'Ops"
    _Avant SSH (Secure Shell), les administrateurs utilisaient `Telnet` pour se connecter à distance à leurs serveurs. Le problème ? Telnet envoyait les mots de passe "en clair" sur le réseau. Si vous étiez sur le même Wi-Fi, vous pouviez intercepter le mot de passe root avec `tcpdump`. **SSH** (Port 22) a révolutionné cela en chiffrant l'intégralité de la communication de bout en bout._

## 1. Utilisation de base du client

SSH est installé par défaut sur presque tous les systèmes (y compris Windows 10/11 aujourd'hui).

```bash
# Se connecter avec l'utilisateur 'admin' sur le serveur 192.168.1.50
ssh admin@192.168.1.50

# Spécifier un port différent (si le serveur n'est pas sur le 22)
ssh -p 2222 admin@192.168.1.50
```

---

## 2. Le vrai pouvoir : L'authentification par clés

L'authentification par mot de passe est obsolète. Elle est sensible au *bruteforce* et au dictionnaire. La seule méthode professionnelle est la **Cryptographie Asymétrique** (Biclés).

### Le principe
Vous générez sur votre ordinateur une **Clé Privée** (Que vous gardez secrète, c'est votre passe-partout) et une **Clé Publique** (Que vous copiez sur tous les serveurs du monde).
Quand vous tentez de vous connecter, le serveur vous lance un défi mathématique basé sur votre clé publique. Seule votre clé privée peut résoudre le problème.

```mermaid
graph TD
    subgraph PC Administrateur
        Priv[🔑 Clé Privée <br/> id_ed25519]
    end
    
    subgraph Serveur Linux (sshd)
        Pub[🔒 Clé Publique <br/> authorized_keys]
    end
    
    Admin[Client SSH] -->|1. Je veux me connecter| Serveur[Processus sshd]
    Serveur -->|2. Relève ce défi chiffré avec la Clé Publique| Admin
    Priv -.->|3. Résolution mathématique (Déchiffrement)| Admin
    Admin -->|4. Renvoi de la preuve| Serveur
    Serveur -->|5. Preuve Validée ✓ | Shell[Accès Terminal]
    
    style Priv fill:#c0392b,stroke:#fff,color:#fff
    style Pub fill:#27ae60,stroke:#fff,color:#fff
    style Serveur fill:#2980b9,stroke:#fff,color:#fff
```

### Générer et copier les clés
```bash
# Générer une paire de clés très sécurisée (Algorithme Ed25519) sur VOTRE PC
ssh-keygen -t ed25519

# Copier automatiquement la clé publique vers le serveur
ssh-copy-id admin@192.168.1.50
```
Désormais, `ssh admin@192.168.1.50` ne vous demandera plus de mot de passe, mais vous identifiera cryptographiquement.

---

## 3. Sécuriser et Durcir le Serveur (sshd_config)

C'est ici qu'intervient l'Administrateur Système (Blue Team). Le fichier de configuration du serveur est `/etc/ssh/sshd_config`. **Il faut toujours modifier ces paramètres par défaut !**

```text title="/etc/ssh/sshd_config"
# 1. Changer le port par défaut (Évite 99% des robots basiques sur Internet)
Port 2222

# 2. INTERDIRE la connexion directe du super-utilisateur (Root)
# Oblige le pirate à trouver un compte utilisateur ET à deviner son mot de passe sudo.
PermitRootLogin no

# 3. INTERDIRE l'utilisation de mots de passe
# Rend le Bruteforce mathématiquement impossible (Il faut posséder une clé privée)
PasswordAuthentication no

# 4. Autoriser uniquement certains utilisateurs
AllowUsers admin john
```

Après modification, toujours redémarrer le service :
```bash
sudo systemctl restart sshd
```

---

## 4. Les fonctionnalités avancées de SSH

SSH n'est pas juste un terminal distant. C'est un couteau suisse capable de créer des "tunnels" (Port Forwarding).

### Le Transfert de Port Local (Local Forwarding)
Imaginons que la base de données de production n'est accessible *que* depuis le réseau interne (Port 3306 fermé par le pare-feu externe).
Vous pouvez créer un tunnel via SSH pour ramener ce port sur votre propre PC.
```bash
# Tout ce que j'envoie sur MON port local 3306, transfère-le au port 3306 du serveur en passant par le tunnel SSH
ssh -L 3306:127.0.0.1:3306 admin@serveur-prod
```
Vous pouvez maintenant utiliser votre client SQL local sur `localhost:3306`, et vous travaillerez magiquement sur la production.

### Le Transfert de Fichiers Sécurisé (SFTP / SCP)
SSH inclut nativement des outils de transfert de fichiers chiffrés, rendant les vieux serveurs FTP obsolètes.
```bash
# Copier un fichier local vers le serveur
scp document.pdf admin@192.168.1.50:/home/admin/

# S'ouvrir une session FTP interactive mais sécurisée via SSH
sftp admin@192.168.1.50
```

## Conclusion

L'outil SSH est probablement l'outil le plus critique de l'Internet moderne. S'il est mal configuré (mot de passe faible, accès root autorisé, faille non patchée), il offre au pirate la récompense absolue : un accès administrateur distant en ligne de commande. Le durcissement de `sshd_config` est la règle numéro 1 de tout déploiement en production.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Chaque service exposé est un vecteur d'attaque potentiel. La configuration sécurisée des services fondamentaux (DNS, SSH, Samba) est la première et souvent la plus critique ligne de défense de l'infrastructure.

> [Retourner à l'index Réseau →](../index.md)
