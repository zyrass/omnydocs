---
description: "SSH : protocole sécurisé, administration distante, tunneling, authentification, hardening"
icon: lucide/book-open-check
tags: ["SSH", "OPENSSH", "SECURITY", "REMOTE", "TUNNELING", "KEYS", "ADMINISTRATION"]
---

# SSH

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-time="8-10 heures"
  data-version="1.0">
</div>

## Introduction au Secure Shell Protocol

!!! quote "Analogie pédagogique"
    _Imaginez le **système postal sécurisé diplomatique avec valises chiffrées et couriers authentifiés** : SSH fonctionne comme **canal communication chiffré bout-en-bout permettant administration distante serveurs avec authentification cryptographique forte** garantissant confidentialité/intégrité. **Système courrier diplomatique SSH** : enveloppes scellées chiffrement militaire (AES-256), signatures authentiques vérification expéditeur (clés publiques/privées), couriers certifiés identité prouvée (certificats), messages intacts anti-falsification (HMAC), tunnels sécurisés transport confidentiel (port forwarding), point contrôle unique ambassade (bastion host), passeport électronique sans mot passe (SSH keys), audits complets journaux communications (logs). **Sans SSH/sécurité** : administration via Telnet cleartext (mots passe interceptables réseau), FTP non-chiffré transferts fichiers (données sensibles exposées), VNC/RDP vulnérables (exploitation facile), credentials hardcodés scripts (fuites GitHub), accès direct serveurs production (pas audit/contrôle), brute-force passwords réussis (faible entropie), man-in-the-middle attacks succès (pas authentification serveur), compliance impossible (RGPD/PCI-DSS/ISO27001 requis chiffrement). **Avec SSH** : **Chiffrement fort** (AES-256-GCM authenticated encryption), **Authentification robuste** (clés ED25519 4096-bit impossibles bruteforce), **Intégrité garantie** (HMAC détecte altération paquets), **Forward secrecy** (compromission clé pas déchiffrement historique), **Tunneling sécurisé** (VPN-like forwarding TCP), **Audit complet** (logs centralisés SIEM), **Zero-trust** (bastion + 2FA obligatoire), **Automation** (Ansible/Terraform infra as code). **SSH = standard sécurité** : 95%+ serveurs Linux administration SSH, 100% clouds (AWS/Azure/GCP) accès SSH natif, DevOps CI/CD pipelines SSH deployment, compliance mandatory (banques/santé/gouvernement), alternative propriétaire inexistante viable, protocole open-source audité (OpenSSH développement 25+ ans). **Architecture SSH** : Client OpenSSH (ssh, scp, sftp commandes), Server OpenSSH sshd daemon, Protocol SSH-2 (SSH-1 deprecated insecure), Key exchange Diffie-Hellman, Encryption AES/ChaCha20, MAC HMAC-SHA2, Compression optionnel zlib. **Cas usage critiques** : Sysadmin connexion serveurs distants, DevOps deployment automatisé, Developers Git push/pull repositories, Security audits forensique incidents, Backup transferts chiffrés rsync/scp, Tunneling contournement firewalls (port forwarding), Bastion hosts point entrée unique DMZ, Jump hosts multi-hop administration. **Chiffres adoption** : OpenSSH installé 1+ milliard devices, 22 port SSH 2ème plus scanné Internet (après 80/443), 90%+ attaques SSH = brute-force password, 0.001% exploitation vulnérabilités (code mature audité). **SSH révolution administration** : Avant SSH années 90 = Telnet cleartext passwords capturés Wireshark trivial, rsh/rlogin trust-based sans crypto, FTP passwords plaintext logs serveurs, administration impossible hostile networks. Après SSH 1995+ = Tatu Ylönen crée SSH-1 Finland, OpenSSH 1999 OpenBSD (Theo de Raadt), adoption universelle 2000s, standard de facto IETF RFC 4250-4254, évolution continue (ED25519 2014, ChaCha20 2016, FIDO2 U2F 2020). **SSH = infrastructure critique invisible** : chaque `git push` utilise SSH, chaque déploiement cloud SSH, chaque backup distant SSH, chaque tunnel VPN peut être SSH, chaque accès serveur production SSH obligatoire compliance._

**SSH en résumé :**

- ✅ **Protocole sécurisé** = Chiffrement bout-en-bout (AES-256, ChaCha20)
- ✅ **Authentification** = Password, Keys (RSA/ED25519), Certificates, 2FA
- ✅ **Administration** = Shell distant, commandes, scripts automation
- ✅ **Transfert fichiers** = SCP, SFTP, rsync over SSH
- ✅ **Tunneling** = Port forwarding (local/remote/dynamic), SOCKS proxy
- ✅ **Security** = Hardening, fail2ban, bastions, audit
- ✅ **Cross-platform** = Linux, Windows (OpenSSH, PuTTY), macOS
- ✅ **Standard** = RFC 4250-4254, OpenSSH reference implementation

**Guide structure :**

1. Introduction et concepts SSH
2. Installation et configuration basique
3. Authentification (passwords et keys)
4. Configuration avancée SSH client
5. Configuration sécurisée SSH server
6. SSH keys management avancé
7. Tunneling et port forwarding
8. ProxyJump et bastions
9. SCP, SFTP et transferts fichiers
10. Security hardening production
11. Troubleshooting et monitoring
12. Cas pratiques (automation, bastion, compliance)

---

## Section 1 : Introduction et Concepts SSH

### 1.1 Qu'est-ce que SSH ?

**SSH = Secure Shell (Protocole Shell Sécurisé)**

```
Fonction principale :
Connexion sécurisée chiffrée vers serveurs distants

Remplace protocoles insecure :
❌ Telnet (port 23) : Cleartext, passwords visibles
❌ rlogin/rsh : Trust-based, pas crypto
❌ FTP : Passwords plaintext

Historique :
1995 : SSH-1 créé par Tatu Ylönen (Finland) après incident sniffer
1996 : SSH Communications Security founded
1998 : SSH-2 protocol (incompatible SSH-1, plus sécurisé)
1999 : OpenSSH créé par OpenBSD (Theo de Raadt)
2006 : SSH-2 standardisé IETF (RFC 4250-4254)
2024 : OpenSSH 9.6+ (current, ED25519, FIDO2 U2F support)

Port default :
22/tcp (SSH)
```

**Pourquoi SSH est critique ?**

```
Administration serveurs :
✅ Seul moyen sécurisé administration Linux distante
✅ Standard cloud (AWS EC2, Azure VM, GCP instances)
✅ Required compliance (PCI-DSS, HIPAA, ISO27001)

DevOps automation :
✅ Ansible, Terraform, Puppet over SSH
✅ CI/CD pipelines deployment
✅ Git repositories (GitHub, GitLab SSH)

Transferts fichiers sécurisés :
✅ SCP (Secure Copy)
✅ SFTP (SSH File Transfer Protocol)
✅ rsync over SSH

Tunneling :
✅ Port forwarding (VPN-like)
✅ SOCKS proxy
✅ Reverse tunnels (NAT traversal)

Statistics :
- 95%+ Linux servers administrés via SSH
- Port 22 = 2ème plus scanné Internet
- 1+ milliard devices OpenSSH installé
- 90%+ attaques SSH = brute-force passwords
```

### 1.2 Architecture SSH Protocol

**SSH-2 Protocol Stack :**

```
┌─────────────────────────────────────────────┐
│  SSH Connection Protocol (RFC 4254)         │
│  - Interactive shell                        │
│  - Remote command execution                 │
│  - Port forwarding                          │
│  - File transfer (SCP/SFTP)                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  SSH Authentication Protocol (RFC 4252)     │
│  - Password                                 │
│  - Public key                               │
│  - Host-based                               │
│  - Keyboard-interactive (2FA)               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  SSH Transport Layer Protocol (RFC 4253)    │
│  - Key exchange (DH, ECDH)                  │
│  - Encryption (AES, ChaCha20)               │
│  - MAC (HMAC-SHA2)                          │
│  - Compression (zlib)                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  TCP/IP (Port 22)                           │
└─────────────────────────────────────────────┘
```

**SSH Connection Flow :**

```
1. TCP Connection
   Client → Server : SYN (port 22)
   Server → Client : SYN-ACK
   Client → Server : ACK

2. SSH Version Exchange
   Server → Client : SSH-2.0-OpenSSH_9.6
   Client → Server : SSH-2.0-OpenSSH_9.6

3. Key Exchange (Diffie-Hellman)
   Client ↔ Server : Échange clés publiques
   → Session key générée (symétrique)
   
4. Host Key Verification
   Server → Client : Host public key + signature
   Client vérifie fingerprint (~/.ssh/known_hosts)
   
5. Encryption Negotiation
   Algorithmes supportés négociés :
   - Encryption : AES-256-GCM
   - MAC : HMAC-SHA2-256
   - Compression : none/zlib

6. User Authentication
   Options :
   - Password (chiffré)
   - Public key (challenge-response)
   - Keyboard-interactive (2FA)

7. Session Established
   Shell interactif ou commande exécutée
   Données chiffrées AES-256
```

### 1.3 Cryptographie SSH

**Algorithmes cryptographiques :**

```
Key Exchange (échange clés session) :
- diffie-hellman-group-exchange-sha256
- ecdh-sha2-nistp256 (Elliptic Curve DH)
- curve25519-sha256 (moderne, rapide, secure)

Host Key (identité serveur) :
- ssh-rsa (RSA 2048/4096 bits, déprécié SHA-1)
- rsa-sha2-256/512 (RSA avec SHA-2, OK)
- ecdsa-sha2-nistp256 (ECDSA, controversé NSA)
- ssh-ed25519 (EdDSA, recommandé, 256-bit = 3072-bit RSA)

Encryption (chiffrement données) :
- aes128-ctr/aes192-ctr/aes256-ctr (AES Counter mode)
- aes128-gcm@openssh.com/aes256-gcm@openssh.com (Authenticated)
- chacha20-poly1305@openssh.com (moderne, rapide)

MAC (Message Authentication Code) :
- hmac-sha2-256
- hmac-sha2-512
- umac-64@openssh.com
- hmac-sha2-256-etm@openssh.com (Encrypt-then-MAC)

Compression :
- none (default, recommandé)
- zlib@openssh.com
```

**Recommandations cryptographiques 2024 :**

```
✅ MODERNE (recommandé) :
Key exchange : curve25519-sha256
Host key : ssh-ed25519
Encryption : chacha20-poly1305@openssh.com, aes256-gcm@openssh.com
MAC : hmac-sha2-256-etm@openssh.com

⚠️ ACCEPTABLE :
Host key : rsa-sha2-512 (4096-bit)
Encryption : aes256-ctr
MAC : hmac-sha2-512

❌ DÉPRÉCIÉ (éviter) :
Key exchange : diffie-hellman-group1-sha1 (SHA-1 broken)
Host key : ssh-rsa (SHA-1), ssh-dss (DSA deprecated)
Encryption : 3des-cbc, arcfour, blowfish (faibles)
MAC : hmac-md5, hmac-sha1 (MD5/SHA-1 compromis)
```

---

## Section 2 : Installation et Configuration Basique

### 2.1 Installation OpenSSH

```bash
# === CLIENT SSH ===

# Debian/Ubuntu
sudo apt update
sudo apt install openssh-client

# RHEL/CentOS/Rocky
sudo dnf install openssh-clients

# macOS (pré-installé)
ssh -V
# OpenSSH_9.0p1, LibreSSL 3.3.6

# Windows 10/11 (pré-installé depuis 1809)
# Settings → Apps → Optional Features → OpenSSH Client
# Ou via PowerShell :
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

# Vérifier installation
ssh -V
# OpenSSH_9.6p1, OpenSSL 3.0.13

# === SERVER SSH ===

# Debian/Ubuntu
sudo apt install openssh-server

# RHEL/CentOS/Rocky
sudo dnf install openssh-server

# Démarrer service
sudo systemctl start sshd
sudo systemctl enable sshd

# Vérifier statut
sudo systemctl status sshd

# Vérifier écoute port 22
sudo ss -tlnp | grep :22
# LISTEN 0 128 0.0.0.0:22 0.0.0.0:* users:(("sshd",pid=1234,fd=3))

# Firewall (si actif)
sudo ufw allow 22/tcp
# ou
sudo firewall-cmd --add-service=ssh --permanent
sudo firewall-cmd --reload
```

### 2.2 Première Connexion SSH

```bash
# Connexion basique
ssh user@hostname

# Exemples
ssh john@192.168.1.10
ssh admin@server.example.com
ssh root@203.0.113.50

# Port non-standard
ssh -p 2222 user@hostname

# Verbose (debugging)
ssh -v user@hostname    # Verbose
ssh -vv user@hostname   # More verbose
ssh -vvv user@hostname  # Debug level

# Première connexion : Host key verification
# Output :
The authenticity of host 'server.example.com (192.168.1.10)' can't be established.
ED25519 key fingerprint is SHA256:abc123def456...
Are you sure you want to continue connecting (yes/no/[fingerprint])?

# Taper 'yes' → Ajoute host à ~/.ssh/known_hosts

# Connexions suivantes : pas de prompt (host key validé)

# Commande distante (sans shell interactif)
ssh user@hostname 'ls -la /tmp'
ssh user@hostname 'df -h'
ssh user@hostname 'sudo systemctl status nginx'

# Multiple commandes
ssh user@hostname 'uptime && free -h && df -h'

# Ou avec heredoc
ssh user@hostname << 'EOF'
    uptime
    free -h
    df -h
EOF

# Déconnexion
exit
# ou Ctrl+D
# ou ~ (tilde escape) puis .
```

### 2.3 Configuration Client SSH

```bash
# Fichier config client : ~/.ssh/config

# Créer/éditer config
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/config

# Configuration basique
Host server1
    HostName 192.168.1.10
    User john
    Port 22

# Usage
ssh server1  # Équivalent: ssh -p 22 john@192.168.1.10

# Configuration avancée
Host prod-web
    HostName web.example.com
    User deploy
    Port 2222
    IdentityFile ~/.ssh/id_prod
    ForwardAgent yes

Host *.example.com
    User admin
    Port 22
    IdentityFile ~/.ssh/id_example

# Wildcards et patterns
Host dev-*
    User developer
    Port 22

Host 10.0.*
    User root

# Configuration globale (tous hosts)
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
    Compression yes

# Permissions config file
chmod 600 ~/.ssh/config

# Test config
ssh -G server1  # Affiche config effective
```

### 2.4 Configuration Server SSH Basique

```bash
# Fichier config serveur : /etc/ssh/sshd_config

# Backup original
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.orig

# Configuration minimale sécurisée
# /etc/ssh/sshd_config

# Port et listening
Port 22
#Port 2222  # Changer port (security through obscurity)
AddressFamily inet  # IPv4 seulement (ou 'any' pour IPv4+IPv6)
ListenAddress 0.0.0.0  # Écoute toutes interfaces

# Protocol
Protocol 2  # SSH-2 seulement (SSH-1 deprecated)

# Host keys
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

# Logging
SyslogFacility AUTH
LogLevel INFO  # Ou VERBOSE pour debug

# Authentication
PermitRootLogin no  # IMPORTANT: Désactiver root login
PasswordAuthentication yes  # Temporaire, passer à 'no' après setup keys
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

# Security
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes

# Timeouts
LoginGraceTime 60
ClientAliveInterval 300
ClientAliveCountMax 2

# X11 forwarding
X11Forwarding no  # Désactiver si pas nécessaire

# Subsystems
Subsystem sftp /usr/lib/openssh/sftp-server

# Tester configuration
sudo sshd -t
# Si OK : pas d'output

# Redémarrer sshd
sudo systemctl restart sshd

# Vérifier logs
sudo tail -f /var/log/auth.log  # Debian/Ubuntu
sudo tail -f /var/log/secure    # RHEL/CentOS
```

---

## Section 3 : Authentification (Passwords et Keys)

### 3.1 Authentification Password

```bash
# Connexion avec password (interactif)
ssh user@hostname
# Password:

# Password via variable (INSECURE, éviter)
# N/A - SSH ne supporte pas password en argument

# Changer password utilisateur SSH
# Sur serveur
passwd  # Change password utilisateur actuel
sudo passwd username  # Change password autre user

# Politique mots de passe forts
# /etc/pam.d/common-password (Debian) ou /etc/pam.d/system-auth (RHEL)
password requisite pam_pwquality.so retry=3 minlen=12 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1

# Force user changer password prochaine connexion
sudo chage -d 0 username

# Désactiver password authentication (après setup keys)
# /etc/ssh/sshd_config
PasswordAuthentication no
ChallengeResponseAuthentication no

sudo systemctl restart sshd
```

### 3.2 Générer SSH Keys

```bash
# Générer clé SSH (recommandé ED25519)
ssh-keygen -t ed25519 -C "john@example.com"

# Output :
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/john/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/john/.ssh/id_ed25519
Your public key has been saved in /home/john/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:abc123... john@example.com

# Fichiers générés
~/.ssh/id_ed25519      # Clé privée (SECRET, ne jamais partager)
~/.ssh/id_ed25519.pub  # Clé publique (partageable)

# Générer RSA 4096-bit (si ED25519 pas supporté)
ssh-keygen -t rsa -b 4096 -C "john@example.com"

# Générer avec nom custom
ssh-keygen -t ed25519 -f ~/.ssh/id_prod -C "prod-server"

# Générer sans passphrase (automation, CI/CD)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ci

# Permissions clés (critiques)
chmod 600 ~/.ssh/id_ed25519      # Private key readable owner only
chmod 644 ~/.ssh/id_ed25519.pub  # Public key readable all

# Lister clés
ls -la ~/.ssh/
```

### 3.3 Déployer SSH Keys

```bash
# === MÉTHODE 1 : ssh-copy-id (simple) ===

# Copier clé publique vers serveur
ssh-copy-id user@hostname

# Avec clé spécifique
ssh-copy-id -i ~/.ssh/id_prod.pub user@hostname

# Port non-standard
ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 2222 user@hostname

# ssh-copy-id fait automatiquement :
# 1. Copie ~/.ssh/id_ed25519.pub vers serveur
# 2. Append à ~/.ssh/authorized_keys
# 3. Set permissions correctes (600)

# === MÉTHODE 2 : Manuelle ===

# Sur client : afficher clé publique
cat ~/.ssh/id_ed25519.pub

# Copier output

# Sur serveur : ajouter à authorized_keys
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
# Coller clé publique (1 ligne)

chmod 600 ~/.ssh/authorized_keys

# === MÉTHODE 3 : Via SSH command ===

# One-liner depuis client
cat ~/.ssh/id_ed25519.pub | ssh user@hostname 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'

# === MÉTHODE 4 : Provisioning (Ansible, Terraform) ===

# Ansible
- name: Deploy SSH key
  authorized_key:
    user: john
    key: "{{ lookup('file', '~/.ssh/id_ed25519.pub') }}"
    state: present

# === TESTER CONNEXION KEY ===

# Connexion sans password (si key déployée)
ssh user@hostname
# Pas de prompt password

# Test avec key spécifique
ssh -i ~/.ssh/id_prod user@hostname

# Verbose (voir quelle key utilisée)
ssh -v user@hostname
# debug1: Offering public key: /home/john/.ssh/id_ed25519 ED25519
# debug1: Server accepts key: pkalg ssh-ed25519
# debug1: Authentication succeeded (publickey).
```

### 3.4 SSH Agent (Gestion Passphrases)

```bash
# Problème : Clés avec passphrase = prompt à chaque connexion

# Solution : ssh-agent (cache passphrases en mémoire)

# Démarrer ssh-agent
eval "$(ssh-agent -s)"
# Agent pid 12345

# Ajouter clé à agent
ssh-add ~/.ssh/id_ed25519
# Enter passphrase for /home/john/.ssh/id_ed25519:
# Identity added: /home/john/.ssh/id_ed25519 (john@example.com)

# Ajouter avec lifetime (auto-remove après délai)
ssh-add -t 3600 ~/.ssh/id_ed25519  # 1 heure

# Lister clés en agent
ssh-add -l
# 256 SHA256:abc123... john@example.com (ED25519)

# Supprimer clé d'agent
ssh-add -d ~/.ssh/id_ed25519

# Supprimer toutes clés
ssh-add -D

# Tuer agent
ssh-agent -k

# Auto-start ssh-agent (ajouter à ~/.bashrc ou ~/.zshrc)
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
fi

# macOS : Keychain integration
# ~/.ssh/config
Host *
    UseKeychain yes
    AddKeysToAgent yes

# Ajouter clé à Keychain (stocke passphrase)
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# Windows : Démarrer ssh-agent service
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent

# Ajouter clé Windows
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

---

## Section 4 : Configuration Avancée SSH Client

### 4.1 Config File Avancé

```bash
# ~/.ssh/config complet

# === HOSTS SPÉCIFIQUES ===

Host prod-web
    HostName 203.0.113.50
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_prod_ed25519
    IdentitiesOnly yes  # Utilise seulement clés spécifiées
    ForwardAgent yes    # Forward SSH agent
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host bastion
    HostName bastion.example.com
    User jump
    Port 22
    IdentityFile ~/.ssh/id_bastion

Host private-server
    HostName 10.0.1.50
    User admin
    ProxyJump bastion  # Connexion via bastion
    IdentityFile ~/.ssh/id_private

# === PATTERNS WILDCARDS ===

Host *.example.com
    User admin
    IdentityFile ~/.ssh/id_example
    Port 22

Host dev-*
    User developer
    ForwardAgent no  # Sécurité : pas forward agent dev

Host 10.0.1.*
    User root
    StrictHostKeyChecking no  # Attention: INSECURE

# === TUNNELING ===

Host tunnel-db
    HostName db-server.internal.com
    User dba
    LocalForward 5432 localhost:5432  # Port forward PostgreSQL
    
Host socks-proxy
    HostName proxy.example.com
    User proxyuser
    DynamicForward 1080  # SOCKS proxy

# === OPTIONS GLOBALES ===

Host *
    # Keepalive
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
    
    # Performance
    Compression yes
    
    # Security
    HashKnownHosts yes
    VisualHostKey yes
    StrictHostKeyChecking ask
    
    # Crypto preferences (modern)
    KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
    HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256
    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
    MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
    
    # Logging
    LogLevel INFO

# Permissions
chmod 600 ~/.ssh/config
```

### 4.2 Options Ligne Commande

```bash
# === CONNEXION OPTIONS ===

# Port
ssh -p 2222 user@hostname

# Identity file (clé spécifique)
ssh -i ~/.ssh/id_prod user@hostname

# Login name
ssh -l username hostname
# Équivalent: ssh username@hostname

# IPv4/IPv6 seulement
ssh -4 user@hostname  # Force IPv4
ssh -6 user@hostname  # Force IPv6

# === FORWARDING OPTIONS ===

# Agent forwarding
ssh -A user@hostname

# X11 forwarding
ssh -X user@hostname  # X11 forwarding
ssh -Y user@hostname  # Trusted X11 forwarding

# Port forwarding (détails section 7)
ssh -L 8080:localhost:80 user@hostname    # Local forward
ssh -R 9090:localhost:3000 user@hostname  # Remote forward
ssh -D 1080 user@hostname                 # Dynamic (SOCKS)

# === SECURITY OPTIONS ===

# Strict host key checking
ssh -o StrictHostKeyChecking=no user@hostname  # INSECURE
ssh -o StrictHostKeyChecking=yes user@hostname

# Disable password auth (force keys)
ssh -o PasswordAuthentication=no user@hostname

# === DEBUG OPTIONS ===

# Verbose
ssh -v user@hostname     # Niveau 1
ssh -vv user@hostname    # Niveau 2
ssh -vvv user@hostname   # Niveau 3 (max debug)

# === AUTRES OPTIONS ===

# Compression
ssh -C user@hostname

# TTY allocation
ssh -t user@hostname 'sudo command'  # Force pseudo-terminal
ssh -T user@hostname 'command'       # No TTY

# Background (avec port forward)
ssh -f -N -L 8080:localhost:80 user@hostname
# -f : Background
# -N : No command (forward only)

# Connection timeout
ssh -o ConnectTimeout=10 user@hostname

# Multiple options
ssh -o "StrictHostKeyChecking=no" -o "UserKnownHostsFile=/dev/null" user@hostname
```

### 4.3 Known Hosts Management

```bash
# ~/.ssh/known_hosts : Stocke fingerprints serveurs

# Format
hostname ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA...

# Hashed format (privacy)
|1|abc123...= ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA...

# Vérifier fingerprint serveur
ssh-keyscan hostname >> ~/.ssh/known_hosts

# Afficher fingerprint
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
# 256 SHA256:abc123... root@hostname (ED25519)

# Supprimer host de known_hosts
ssh-keygen -R hostname
ssh-keygen -R 192.168.1.10

# Vider known_hosts (ATTENTION)
> ~/.ssh/known_hosts

# Ignorer known_hosts (temporaire, INSECURE)
ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no user@hostname

# Hash all known_hosts entries
ssh-keygen -H -f ~/.ssh/known_hosts
```

---

## Section 5 : Configuration Sécurisée SSH Server

### 5.1 Hardening sshd_config

```bash
# /etc/ssh/sshd_config - Configuration sécurisée production

# === NETWORK ===
Port 22  # Ou port non-standard (2222, 2200, etc.)
AddressFamily inet  # IPv4 only (ou 'any')
ListenAddress 0.0.0.0

# === PROTOCOL ===
Protocol 2

# === HOST KEYS ===
# Désactiver RSA si possible, garder ED25519
HostKey /etc/ssh/ssh_host_ed25519_key
#HostKey /etc/ssh/ssh_host_rsa_key

# === CRYPTO MODERNE ===
# Key exchange
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512

# Host key algorithms
HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256

# Ciphers
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr

# MACs
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256

# === LOGGING ===
SyslogFacility AUTH
LogLevel VERBOSE  # Production: VERBOSE pour audits

# === AUTHENTICATION ===
LoginGraceTime 30  # 30 secondes pour s'authentifier
PermitRootLogin no  # CRITIQUE: Jamais root direct
StrictModes yes
MaxAuthTries 3  # 3 tentatives max
MaxSessions 3   # 3 sessions simultanées max

PubkeyAuthentication yes
PasswordAuthentication no  # DÉSACTIVER après setup keys
PermitEmptyPasswords no
ChallengeResponseAuthentication no

AuthorizedKeysFile .ssh/authorized_keys

# === PAM ===
UsePAM yes

# === TIMEOUTS ===
ClientAliveInterval 300  # 5 minutes
ClientAliveCountMax 2    # 2 x 5min = 10min timeout total

# === FORWARDING ===
AllowAgentForwarding yes
AllowTcpForwarding yes
X11Forwarding no  # Désactiver si pas nécessaire
PermitTunnel no

# === FEATURES ===
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
Compression delayed  # Après auth seulement

# === RESTRICTIONS USERS ===
# Autoriser seulement certains users
AllowUsers deploy admin john
# Ou groups
AllowGroups sshusers

# Deny users
DenyUsers root test guest

# === CHROOT SFTP (optionnel) ===
# Match Group sftponly
#     ChrootDirectory /home/%u
#     ForceCommand internal-sftp
#     AllowTcpForwarding no
#     X11Forwarding no

# === BANNER ===
Banner /etc/ssh/banner.txt

# === SUBSYSTEMS ===
Subsystem sftp /usr/lib/openssh/sftp-server -f AUTHPRIV -l INFO

# Test configuration
sudo sshd -t

# Restart
sudo systemctl restart sshd
```

### 5.2 Restrictions par User/Group

```bash
# === MATCH BLOCKS (conditions) ===

# /etc/ssh/sshd_config

# Restriction par user
Match User deploy
    AllowTcpForwarding no
    X11Forwarding no
    ForceCommand /usr/local/bin/deploy-script.sh

# Restriction par group
Match Group developers
    PasswordAuthentication yes
    MaxSessions 2

# Restriction IP source
Match Address 192.168.1.0/24
    PasswordAuthentication yes
    
Match Address 0.0.0.0/0,!192.168.1.0/24
    PasswordAuthentication no
    PubkeyAuthentication yes

# SFTP-only users (chroot)
Match Group sftponly
    ChrootDirectory /home/%u/sftp
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
    PermitTunnel no

# 2FA pour certains users
Match User admin
    AuthenticationMethods publickey,keyboard-interactive

# Créer group sftponly
sudo groupadd sftponly

# Ajouter user à group
sudo usermod -aG sftponly username

# Créer structure chroot SFTP
sudo mkdir -p /home/username/sftp
sudo chown root:root /home/username/sftp
sudo chmod 755 /home/username/sftp
sudo mkdir /home/username/sftp/upload
sudo chown username:username /home/username/sftp/upload
```

### 5.3 Fail2ban Protection

```bash
# Installer fail2ban
sudo apt install fail2ban  # Debian/Ubuntu
sudo dnf install fail2ban  # RHEL/CentOS

# Configuration
# /etc/fail2ban/jail.local

[DEFAULT]
bantime = 3600  # 1 heure ban
findtime = 600  # 10 minutes window
maxretry = 3    # 3 tentatives

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log  # Debian
#logpath = /var/log/secure   # RHEL
maxretry = 3
bantime = 86400  # 24h pour SSH

# Actions (ban via iptables)
banaction = iptables-multiport
action = %(action_mwl)s  # Mail avec whois + logs

# Email notifications
destemail = admin@example.com
sendername = Fail2Ban
action = %(action_mwl)s

# Démarrer fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Status
sudo fail2ban-client status
sudo fail2ban-client status sshd

# Vérifier bans actifs
sudo fail2ban-client get sshd banned

# Unban IP
sudo fail2ban-client set sshd unbanip 192.0.2.100

# Logs
sudo tail -f /var/log/fail2ban.log

# Test regex filter
sudo fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf
```

---

## Section 6 : SSH Keys Management Avancé

### 6.1 Multiple Keys Management

```bash
# Structure organisation multiple keys

~/.ssh/
├── config
├── id_ed25519          # Personal key
├── id_ed25519.pub
├── id_prod_rsa         # Production key
├── id_prod_rsa.pub
├── id_github_ed25519   # GitHub key
├── id_github_ed25519.pub
├── id_aws_ed25519      # AWS key
├── id_aws_ed25519.pub
└── known_hosts

# ~/.ssh/config pour gérer multiple keys

Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_github_ed25519
    IdentitiesOnly yes

Host prod-*
    HostName %h.example.com
    User deploy
    IdentityFile ~/.ssh/id_prod_rsa
    IdentitiesOnly yes

Host aws-*
    HostName %h
    User ec2-user
    IdentityFile ~/.ssh/id_aws_ed25519
    IdentitiesOnly yes

Host *
    IdentityFile ~/.ssh/id_ed25519
    AddKeysToAgent yes

# Usage
ssh github.com  # Utilise id_github_ed25519
ssh prod-web1   # Utilise id_prod_rsa
ssh aws-server  # Utilise id_aws_ed25519
```

### 6.2 SSH Certificates

```bash
# SSH Certificates = Alternative keys (plus scalable)

# Avantages :
# ✅ Durée vie limitée (expiration automatique)
# ✅ Pas besoin déployer clés publiques sur chaque serveur
# ✅ Révocation centralisée
# ✅ Metadata (principals, extensions)

# === CA (Certificate Authority) Setup ===

# Générer CA key (GARDER SECRET)
ssh-keygen -t ed25519 -f ~/.ssh/ca_user_key -C "User CA"

# Signer user key avec CA
ssh-keygen -s ~/.ssh/ca_user_key \
    -I john_doe \
    -n john,admin \
    -V +52w \
    ~/.ssh/id_ed25519.pub

# Output: ~/.ssh/id_ed25519-cert.pub

# Paramètres :
# -s : CA key
# -I : Key ID (identifier)
# -n : Principals (users autorisés)
# -V : Validity period (+52w = 1 an)

# Vérifier certificat
ssh-keygen -L -f ~/.ssh/id_ed25519-cert.pub

# Output :
id_ed25519-cert.pub:
        Type: ssh-ed25519-cert-v01@openssh.com user certificate
        Public key: ED25519-CERT SHA256:abc123...
        Signing CA: ED25519 SHA256:def456... (using ssh-ed25519)
        Key ID: "john_doe"
        Serial: 0
        Valid: from 2024-01-16T12:00:00 to 2025-01-16T12:00:00
        Principals:
                john
                admin
        Critical Options: (none)
        Extensions:
                permit-agent-forwarding
                permit-port-forwarding
                permit-pty
                permit-user-rc
                permit-X11-forwarding

# === SERVER Configuration ===

# Déployer CA public key sur serveur
scp ~/.ssh/ca_user_key.pub server:/etc/ssh/ca_user_key.pub

# /etc/ssh/sshd_config
TrustedUserCAKeys /etc/ssh/ca_user_key.pub

sudo systemctl restart sshd

# === CLIENT Usage ===

# Connexion avec certificat (automatique si présent)
ssh john@server
# SSH utilise id_ed25519-cert.pub automatiquement

# === HOST Certificates (serveurs) ===

# Générer CA host
ssh-keygen -t ed25519 -f ~/.ssh/ca_host_key -C "Host CA"

# Signer host key
ssh-keygen -s ~/.ssh/ca_host_key \
    -I server.example.com \
    -h \
    -n server.example.com,192.168.1.10 \
    -V +520w \
    /etc/ssh/ssh_host_ed25519_key.pub

# -h : Host certificate (pas user)
# -n : Hostnames/IPs valides

# Server config
# /etc/ssh/sshd_config
HostCertificate /etc/ssh/ssh_host_ed25519_key-cert.pub

# Client config
# ~/.ssh/known_hosts
@cert-authority *.example.com ssh-ed25519 AAAA... (CA host public key)
```

### 6.3 Key Rotation et Revocation

```bash
# === ROTATION CLÉS ===

# Processus rotation zero-downtime :

# 1. Générer nouvelle clé
ssh-keygen -t ed25519 -f ~/.ssh/id_new_ed25519

# 2. Déployer nouvelle clé (ajouter, pas remplacer)
ssh-copy-id -i ~/.ssh/id_new_ed25519.pub user@server

# 3. Tester nouvelle clé
ssh -i ~/.ssh/id_new_ed25519 user@server

# 4. Update config local
# ~/.ssh/config
Host server
    IdentityFile ~/.ssh/id_new_ed25519

# 5. Supprimer ancienne clé serveur (après tests)
ssh user@server
nano ~/.ssh/authorized_keys
# Supprimer ancienne clé

# 6. Backup puis supprimer ancienne clé locale
mv ~/.ssh/id_old_ed25519 ~/.ssh/backup/
mv ~/.ssh/id_old_ed25519.pub ~/.ssh/backup/

# === RÉVOCATION CLÉS ===

# Option 1 : Supprimer de authorized_keys
ssh user@server
sed -i '/old-key-comment/d' ~/.ssh/authorized_keys

# Option 2 : Utiliser RevokedKeys (sshd)
# /etc/ssh/sshd_config
RevokedKeys /etc/ssh/revoked_keys

# /etc/ssh/revoked_keys
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... # Clé révoquée

sudo systemctl restart sshd

# Option 3 : Certificates revocation (KRL)
# Créer Key Revocation List
ssh-keygen -k -f revoked_keys.krl ~/.ssh/compromised_key.pub

# Server config
# /etc/ssh/sshd_config
RevokedKeys /etc/ssh/revoked_keys.krl

# === AUDIT CLÉS ===

# Lister tous authorized_keys
sudo find /home -name authorized_keys -exec sh -c 'echo "=== {} ==="; cat {}' \;

# Chercher clés dupliquées
sudo find /home -name authorized_keys -exec cat {} \; | sort | uniq -d

# Chercher clés faibles (< 2048 bits RSA)
for key in $(find ~/.ssh -name "*.pub"); do
    echo "Key: $key"
    ssh-keygen -l -f $key
done

# Script audit complet keys
#!/bin/bash
# ssh-keys-audit.sh

find /home -name authorized_keys | while read file; do
    echo "File: $file"
    while read line; do
        if [[ $line =~ ^ssh- ]]; then
            type=$(echo $line | awk '{print $1}')
            key=$(echo $line | awk '{print $2}')
            comment=$(echo $line | awk '{print $3}')
            
            fingerprint=$(echo "$type $key" | ssh-keygen -lf -)
            
            echo "  Type: $type"
            echo "  Comment: $comment"
            echo "  Fingerprint: $fingerprint"
            echo ""
        fi
    done < "$file"
done
```

## Section 7 : Tunneling et Port Forwarding

### 7.1 Local Port Forwarding

**Principe : Forwarder port local vers service distant via SSH**

```bash
# Syntaxe
ssh -L [bind_address:]local_port:remote_host:remote_port user@ssh_server

# Exemple 1 : Accéder base de données distante localement
ssh -L 5432:localhost:5432 user@db-server.example.com

# Explication :
# - Port local 5432 (PostgreSQL)
# - Forward vers db-server.example.com:5432
# - Connexion PostgreSQL chiffrée via SSH

# Usage après tunnel établi :
psql -h localhost -p 5432 -U dbuser mydatabase

# Exemple 2 : Accéder service interne via bastion
ssh -L 8080:internal-web.local:80 user@bastion.example.com

# Access via browser :
# http://localhost:8080

# Exemple 3 : Multiple forwards
ssh -L 5432:db1.internal:5432 \
    -L 3306:db2.internal:3306 \
    -L 6379:redis.internal:6379 \
    user@bastion.example.com

# Exemple 4 : Bind address spécifique
ssh -L 0.0.0.0:8080:internal-web:80 user@bastion
# Accessible depuis réseau local (pas seulement localhost)
# ATTENTION: Security risk si réseau non trusted

# Exemple 5 : Background tunnel
ssh -f -N -L 5432:localhost:5432 user@db-server
# -f : Background
# -N : No command (tunnel only)

# Kill tunnel background
ps aux | grep "ssh.*5432"
kill <PID>

# Ou via autossh (auto-reconnect)
autossh -M 0 -f -N -L 5432:localhost:5432 user@db-server

# Configuration persistante
# ~/.ssh/config
Host db-tunnel
    HostName db-server.example.com
    User dbadmin
    LocalForward 5432 localhost:5432
    
# Usage
ssh -f -N db-tunnel
```

**Use cases Local Forward :**

```bash
# 1. Database access (PostgreSQL, MySQL, MongoDB)
ssh -L 5432:localhost:5432 user@db-server
psql -h localhost -U postgres

# 2. Web admin panels (internal tools)
ssh -L 8080:admin.internal:80 user@bastion
# http://localhost:8080

# 3. Redis/Memcached access
ssh -L 6379:redis.internal:6379 user@bastion
redis-cli -h localhost

# 4. Elasticsearch/Kibana
ssh -L 9200:es.internal:9200 -L 5601:kibana.internal:5601 user@bastion

# 5. RDP via SSH tunnel
ssh -L 3389:windows-server.internal:3389 user@bastion
# xfreerdp /v:localhost:3389

# 6. VNC via SSH
ssh -L 5900:vnc-server.internal:5900 user@bastion
# vncviewer localhost:5900
```

### 7.2 Remote Port Forwarding

**Principe : Exposer service local vers serveur distant**

```bash
# Syntaxe
ssh -R [bind_address:]remote_port:local_host:local_port user@ssh_server

# Exemple 1 : Exposer web server local
ssh -R 8080:localhost:3000 user@public-server.com

# Service local :3000 accessible via public-server.com:8080

# Exemple 2 : Exposer service derrière NAT
# Machine locale (derrière NAT, pas IP publique)
ssh -R 2222:localhost:22 user@public-vps.com

# Depuis VPS, accès machine locale :
ssh -p 2222 localuser@localhost

# Exemple 3 : Webhook callback local dev
ssh -R 8080:localhost:3000 user@public-server.com
# Webhook externe → public-server.com:8080 → localhost:3000

# Exemple 4 : Reverse tunnel persistant
ssh -f -N -R 2222:localhost:22 user@vps.example.com

# Configuration Server (/etc/ssh/sshd_config)
GatewayPorts yes  # Permet bind 0.0.0.0 (pas seulement localhost)
# ATTENTION: Security risk

# Ou
GatewayPorts clientspecified  # Client choisit bind address

# ~/.ssh/config
Host reverse-tunnel
    HostName vps.example.com
    User tunnel
    RemoteForward 8080 localhost:3000
    ServerAliveInterval 60
    ServerAliveCountMax 3
    
# Usage
ssh -f -N reverse-tunnel
```

**Use cases Remote Forward :**

```bash
# 1. Développement local avec webhooks externes
# GitHub webhooks → VPS:8080 → localhost:3000
ssh -R 8080:localhost:3000 user@vps.com

# 2. Accès machine derrière NAT/firewall
ssh -R 2222:localhost:22 user@public-server.com
# Admin peut SSH vers localhost:2222 depuis public-server

# 3. Demo local app à client distant
ssh -R 8080:localhost:5000 user@demo-server.com
# Client accède demo-server.com:8080

# 4. IoT device callback (device derrière NAT)
ssh -R 5000:localhost:5000 user@cloud-server.com

# 5. Continuous reverse tunnel (monitoring)
autossh -M 0 -f -N -R 2222:localhost:22 monitoring@central-server.com
```

### 7.3 Dynamic Port Forwarding (SOCKS Proxy)

**Principe : Créer SOCKS proxy via SSH**

```bash
# Syntaxe
ssh -D [bind_address:]local_port user@ssh_server

# Exemple 1 : SOCKS proxy basique
ssh -D 1080 user@remote-server.com

# Configure browser/app utiliser SOCKS5 localhost:1080
# Tout trafic browser → chiffré via SSH

# Exemple 2 : SOCKS avec bind address
ssh -D 0.0.0.0:1080 user@remote-server.com
# Accessible depuis réseau local

# Exemple 3 : Background SOCKS proxy
ssh -f -N -D 1080 user@remote-server.com

# Configuration Firefox SOCKS proxy :
# Preferences → Network Settings → Manual proxy
# SOCKS Host: localhost
# Port: 1080
# SOCKS v5: Yes
# Proxy DNS: Yes (important)

# Configuration Chrome/Chromium
google-chrome --proxy-server="socks5://localhost:1080"

# Configuration système (Linux)
export ALL_PROXY=socks5://localhost:1080

# Test proxy
curl --proxy socks5://localhost:1080 https://ipinfo.io

# ~/.ssh/config
Host socks-proxy
    HostName proxy-server.example.com
    User proxyuser
    DynamicForward 1080
    
# Usage
ssh -f -N socks-proxy

# proxychains (forcer apps utiliser SOCKS)
sudo apt install proxychains4

# /etc/proxychains4.conf
[ProxyList]
socks5 127.0.0.1 1080

# Usage
proxychains4 curl https://ipinfo.io
proxychains4 nmap target.com
```

**Use cases Dynamic Forward :**

```bash
# 1. Contourner firewall corporate
ssh -D 1080 user@home-server.com
# Browser utilise SOCKS → Tout trafic via home

# 2. Sécuriser navigation WiFi public
ssh -D 1080 user@vps-secure.com
# Tout trafic chiffré via VPS

# 3. Accéder réseau interne distant
ssh -D 1080 user@corporate-vpn.com
# Browser accède resources internes via SOCKS

# 4. Testing geo-restrictions
ssh -D 1080 user@us-server.com
# Apparaît comme IP US

# 5. Pentesting via pivot
ssh -D 1080 user@compromised-server.internal
proxychains4 nmap internal-network
```

### 7.4 Tunneling Avancé

```bash
# === MULTIHOP TUNNELING ===

# Tunnel via multiples serveurs
ssh -L 5432:final-db:5432 -J bastion1,bastion2 user@final-server

# Ou avec ProxyJump
# ~/.ssh/config
Host final-server
    ProxyJump bastion1,bastion2
    LocalForward 5432 localhost:5432

# === REVERSE + LOCAL COMBINED ===

# Machine A (local) veut accéder Machine C via Machine B
# Machine A → B (reverse) → C (local)

# Sur Machine A :
ssh -R 8080:localhost:8080 user@machineB

# Sur Machine B :
ssh -L 8080:localhost:8080 user@machineC

# === TUN/TAP TUNNELING (VPN-like) ===

# Server (/etc/ssh/sshd_config)
PermitTunnel yes

# Client
sudo ssh -w 0:0 user@server

# Configure tun0 interface
sudo ip addr add 10.0.0.1/30 dev tun0
sudo ip link set tun0 up

# Server configure tun0
sudo ip addr add 10.0.0.2/30 dev tun0
sudo ip link set tun0 up

# Route traffic via tunnel
sudo ip route add 192.168.1.0/24 via 10.0.0.2

# === PERSISTENT TUNNELS (systemd) ===

# /etc/systemd/system/ssh-tunnel-db.service
[Unit]
Description=SSH Tunnel to Database
After=network.target

[Service]
Type=simple
User=tunneluser
ExecStart=/usr/bin/ssh -N -L 5432:localhost:5432 user@db-server.com
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

sudo systemctl enable ssh-tunnel-db
sudo systemctl start ssh-tunnel-db

# === AUTOSSH (auto-reconnect) ===

sudo apt install autossh

# autossh avec monitoring
autossh -M 20000 -f -N -L 5432:localhost:5432 user@db-server

# -M : Monitoring port (20000 + 20001)
# Auto-reconnect si connexion perdue

# systemd avec autossh
[Service]
ExecStart=/usr/bin/autossh -M 0 -N -o "ServerAliveInterval 60" -o "ServerAliveCountMax 3" -L 5432:localhost:5432 user@db-server.com
```

---

## Section 8 : ProxyJump et Bastions

### 8.1 ProxyJump (Jump Host)

```bash
# ProxyJump = Connexion via serveur intermédiaire

# Syntaxe
ssh -J jump_host target_host

# Exemple 1 : Single jump
ssh -J bastion.example.com user@internal-server.local

# Exemple 2 : Multiple jumps
ssh -J bastion1.com,bastion2.com user@final-server

# Exemple 3 : Jump avec user différent
ssh -J jump_user@bastion.com target_user@internal-server

# Configuration ~/.ssh/config
Host bastion
    HostName bastion.example.com
    User jump
    IdentityFile ~/.ssh/id_bastion

Host internal-*
    ProxyJump bastion
    User admin
    IdentityFile ~/.ssh/id_internal

Host internal-web
    HostName 10.0.1.50
    
Host internal-db
    HostName 10.0.1.51

# Usage
ssh internal-web  # Automatiquement via bastion
ssh internal-db

# Équivalent ancien (ProxyCommand)
Host internal-*
    ProxyCommand ssh -W %h:%p bastion

# Multihop config
Host bastion1
    HostName bastion1.example.com
    User jump1

Host bastion2
    HostName bastion2.internal
    ProxyJump bastion1
    User jump2

Host final-server
    HostName server.internal
    ProxyJump bastion1,bastion2
    User admin
```

### 8.2 Bastion Host Architecture

```bash
# Bastion = Point d'entrée unique sécurisé

# Architecture :
#
#  Internet
#      │
#      ↓
#  [Bastion Host]  ← Hardened, monitored
#      │
#      ├─→ [Web Server 1] (private network)
#      ├─→ [Web Server 2]
#      ├─→ [DB Server]
#      └─→ [API Server]

# === BASTION SERVER SETUP ===

# 1. Hardening sshd_config
# /etc/ssh/sshd_config

Port 22
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

# Logging maximal
LogLevel VERBOSE

# Pas de forwarding (bastion ne forward pas)
AllowTcpForwarding no
X11Forwarding no
PermitTunnel no

# Force command (audit)
ForceCommand /usr/local/bin/bastion-audit.sh

# Limite users
AllowUsers jumpadmin jumpuser1 jumpuser2

# 2. Install logging/audit
sudo apt install auditd

# /etc/audit/rules.d/ssh.rules
-w /usr/sbin/sshd -p x -k sshd_exec
-w /etc/ssh/sshd_config -p wa -k sshd_config
-w /home -p wa -k home_access

# 3. Install fail2ban
sudo apt install fail2ban

# /etc/fail2ban/jail.local
[sshd]
enabled = true
maxretry = 3
bantime = 86400
findtime = 600

# 4. Script audit connections
# /usr/local/bin/bastion-audit.sh
#!/bin/bash

# Log connexion
logger -t bastion-ssh "User $USER from $SSH_CLIENT connected"

# Send alert
echo "SSH connexion: $USER from $SSH_CLIENT at $(date)" | \
    mail -s "Bastion Access" security@example.com

# Allow interactive shell
exec /bin/bash

# 5. Session recording (script/asciinema)
# ~/.bashrc sur bastion
if [ -n "$SSH_CONNECTION" ]; then
    script -q -f /var/log/sessions/$(date +%Y%m%d-%H%M%S)-$USER.log
fi

# 6. Monitoring (Prometheus/Grafana)
# node_exporter sur bastion

# 7. MFA/2FA (Google Authenticator)
sudo apt install libpam-google-authenticator

# /etc/pam.d/sshd
auth required pam_google_authenticator.so

# /etc/ssh/sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

### 8.3 Bastion Access Patterns

```bash
# === PATTERN 1 : Direct Jump ===

# ~/.ssh/config (client)
Host bastion
    HostName bastion.example.com
    User jump
    IdentityFile ~/.ssh/id_bastion

Host prod-*
    ProxyJump bastion
    User admin
    IdentityFile ~/.ssh/id_prod

Host prod-web1
    HostName 10.0.1.10
    
Host prod-db1
    HostName 10.0.1.20

# Usage
ssh prod-web1  # Via bastion automatiquement

# === PATTERN 2 : Port Forward via Bastion ===

# Database access
ssh -L 5432:prod-db1.internal:5432 bastion

# Multiple services
ssh -L 5432:db:5432 -L 6379:redis:6379 -L 9200:es:9200 bastion

# === PATTERN 3 : SOCKS Proxy via Bastion ===

ssh -D 1080 bastion
# Configure browser SOCKS → accès tous services internes

# === PATTERN 4 : SCP via Bastion ===

# Upload file
scp -o "ProxyJump bastion" file.txt admin@prod-web1:/tmp/

# Download file
scp -o "ProxyJump bastion" admin@prod-web1:/var/log/app.log .

# === PATTERN 5 : Rsync via Bastion ===

rsync -avz -e "ssh -J bastion" /local/dir/ admin@prod-web1:/remote/dir/

# === PATTERN 6 : Ansible via Bastion ===

# ansible.cfg
[defaults]
ssh_args = -o ProxyCommand="ssh -W %h:%p bastion"

# Ou inventory
[prod_servers]
web1 ansible_host=10.0.1.10 ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p bastion"'
```

### 8.4 Multi-Tier Bastion

```bash
# Architecture multi-niveau

# Internet → Bastion Public → Bastion Private → Production

# ~/.ssh/config
Host bastion-public
    HostName bastion.example.com
    User jump-public
    IdentityFile ~/.ssh/id_bastion_public

Host bastion-private
    HostName bastion.internal
    ProxyJump bastion-public
    User jump-private
    IdentityFile ~/.ssh/id_bastion_private

Host prod-*
    ProxyJump bastion-public,bastion-private
    User admin
    IdentityFile ~/.ssh/id_prod

# Ou cascade config
Host bastion-private
    ProxyJump bastion-public

Host prod-*
    ProxyJump bastion-private

# Usage transparent
ssh prod-web1
# SSH établit : local → bastion-public → bastion-private → prod-web1
```

---

## Section 9 : SCP, SFTP et Transferts Fichiers

### 9.1 SCP (Secure Copy)

```bash
# === SCP BASIQUE ===

# Upload file
scp file.txt user@hostname:/remote/path/

# Upload multiple files
scp file1.txt file2.txt user@hostname:/remote/path/

# Upload directory (recursive)
scp -r /local/directory user@hostname:/remote/path/

# Download file
scp user@hostname:/remote/file.txt /local/path/

# Download directory
scp -r user@hostname:/remote/directory /local/path/

# === OPTIONS SCP ===

# Port non-standard
scp -P 2222 file.txt user@hostname:/path/

# Preserve attributes (timestamps, permissions)
scp -p file.txt user@hostname:/path/

# Verbose
scp -v file.txt user@hostname:/path/

# Compression
scp -C large-file.tar.gz user@hostname:/path/

# Limit bandwidth (KB/s)
scp -l 1000 large-file.iso user@hostname:/path/
# 1000 KB/s = ~1 MB/s

# Identity file
scp -i ~/.ssh/id_prod file.txt user@hostname:/path/

# === SCP VIA BASTION ===

# Via ProxyJump
scp -o "ProxyJump bastion" file.txt admin@internal-server:/tmp/

# Via config
# ~/.ssh/config
Host internal-server
    ProxyJump bastion

# Usage simple
scp file.txt internal-server:/tmp/

# === SCP ENTRE SERVEURS ===

# Copie directe entre 2 serveurs distants
scp user1@server1:/path/file.txt user2@server2:/path/

# Via local machine (si servers pas accès direct)
scp user1@server1:/path/file.txt /tmp/
scp /tmp/file.txt user2@server2:/path/

# === EXAMPLES PRATIQUES ===

# Backup logs
scp user@server:/var/log/app.log ./logs/app-$(date +%Y%m%d).log

# Deploy application
scp -r ./dist/* deploy@prod-server:/var/www/app/

# Multiple servers (loop)
for server in web1 web2 web3; do
    scp config.conf $server:/etc/app/
done

# Avec progress bar (pv)
tar czf - /large/directory | pv | ssh user@server 'tar xzf - -C /destination/'
```

### 9.2 SFTP (SSH File Transfer Protocol)

```bash
# === SFTP INTERACTIF ===

# Connexion
sftp user@hostname

# Commandes SFTP (similaire FTP)
sftp> pwd          # Print working directory (remote)
sftp> lpwd         # Local pwd
sftp> ls           # List remote
sftp> lls          # List local
sftp> cd /path     # Change remote dir
sftp> lcd /path    # Change local dir

# Upload
sftp> put file.txt
sftp> put -r directory/

# Download
sftp> get remote-file.txt
sftp> get -r remote-directory/

# Permissions
sftp> chmod 644 file.txt
sftp> chown user:group file.txt

# Create/remove directory
sftp> mkdir newdir
sftp> rmdir emptydir

# Remove file
sftp> rm file.txt

# Rename
sftp> rename old.txt new.txt

# Help
sftp> help

# Exit
sftp> exit

# === SFTP NON-INTERACTIF ===

# Batch mode
sftp -b commands.txt user@hostname

# commands.txt :
cd /remote/path
put file.txt
get remote-file.txt
exit

# One-liner upload
echo "put file.txt" | sftp user@hostname

# Download with sftp
sftp user@hostname:/remote/file.txt /local/path/

# === SFTP ADVANCED ===

# Resume interrupted transfer
sftp> reget large-file.iso

sftp> reput large-file.iso

# Progress meter
sftp> progress
Progress meter enabled

# Preserve file attributes
sftp> put -p file.txt

# === CHROOT SFTP (secure) ===

# Isolate SFTP users (no shell access)

# /etc/ssh/sshd_config
Match Group sftponly
    ChrootDirectory /home/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no

# Create group
sudo groupadd sftponly

# Add user to group
sudo usermod -aG sftponly sftpuser

# Setup chroot structure
sudo mkdir -p /home/sftpuser/files
sudo chown root:root /home/sftpuser
sudo chmod 755 /home/sftpuser
sudo chown sftpuser:sftpuser /home/sftpuser/files

# Test
sftp sftpuser@localhost
sftp> pwd
/files  # Chrooted, can't see /home/sftpuser
```

### 9.3 Rsync over SSH

```bash
# Rsync = Synchronisation efficace (delta transfer)

# === RSYNC BASIQUE ===

# Sync local → remote
rsync -avz /local/dir/ user@hostname:/remote/dir/

# Options :
# -a : Archive mode (recursive, preserve attributes)
# -v : Verbose
# -z : Compression

# Sync remote → local
rsync -avz user@hostname:/remote/dir/ /local/dir/

# === RSYNC OPTIONS UTILES ===

# Progress
rsync -avz --progress /local/ user@host:/remote/

# Delete files not in source
rsync -avz --delete /local/ user@host:/remote/

# Exclude patterns
rsync -avz --exclude='*.log' --exclude='tmp/*' /local/ user@host:/remote/

# Include only patterns
rsync -avz --include='*.txt' --include='*/' --exclude='*' /local/ user@host:/remote/

# Dry-run (test without changes)
rsync -avzn /local/ user@host:/remote/

# Limit bandwidth
rsync -avz --bwlimit=1000 /local/ user@host:/remote/
# 1000 KB/s

# === RSYNC VIA BASTION ===

rsync -avz -e "ssh -J bastion" /local/ admin@internal:/remote/

# Ou via ProxyCommand
rsync -avz -e "ssh -o ProxyCommand='ssh -W %h:%p bastion'" /local/ admin@internal:/remote/

# === RSYNC INCREMENTAL BACKUP ===

# Backup avec hardlinks (économise espace)
#!/bin/bash
# backup-incremental.sh

DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="/backups"
LATEST="$BACKUP_DIR/latest"
DEST="$BACKUP_DIR/backup-$DATE"

rsync -avz --link-dest="$LATEST" \
    user@server:/data/ \
    "$DEST/"

rm -f "$LATEST"
ln -s "$DEST" "$LATEST"

# === RSYNC AVEC EXCLUSIONS ===

# .rsync-exclude file
*.log
*.tmp
.git/
node_modules/
__pycache__/
*.pyc

# Usage
rsync -avz --exclude-from=.rsync-exclude /local/ user@host:/remote/

# === MONITORING RSYNC ===

# Avec progress détaillé
rsync -avz --info=progress2 /large/dir/ user@host:/remote/

# Dry-run avec itemize changes
rsync -avzn --itemize-changes /local/ user@host:/remote/

# Output :
# >f+++++++++ file.txt    (new file)
# .f..t...... existing.txt (timestamp changed)
# cd+++++++++ newdir/     (new directory)
```

### 9.4 Transferts Optimisés Production

```bash
# === PARALLEL TRANSFERS ===

# GNU parallel avec SCP
find /data -type f | parallel -j 4 scp {} user@server:/backup/

# Parallel avec rsync
parallel -j 4 rsync -avz {} user@server:/backup/ ::: dir1 dir2 dir3 dir4

# === COMPRESSION À LA VOLÉE ===

# Tar + SSH
tar czf - /large/directory | ssh user@server 'tar xzf - -C /destination/'

# Avec pv (progress)
tar czf - /large/directory | pv | ssh user@server 'tar xzf - -C /destination/'

# === TRANSFERT LARGE FILES ===

# Split large file
split -b 1G large-file.iso part-

# Transfer parts
for part in part-*; do
    scp $part user@server:/tmp/
done

# Reassemble remote
ssh user@server 'cat /tmp/part-* > /destination/large-file.iso'

# === RESUMABLE TRANSFERS ===

# rsync (automatic resume)
rsync -avz --partial --progress /large/ user@server:/remote/

# SCP-like avec resume (via rsync)
rsync -avz --partial --progress file.iso user@server:/path/file.iso

# === BANDWIDTH MANAGEMENT ===

# Multiple transfers avec trickle
trickle -d 1000 -u 500 rsync -avz /data/ user@server:/backup/
# Download: 1000 KB/s, Upload: 500 KB/s

# === VERIFICATION INTEGRITY ===

# Transfer avec checksum
rsync -avz --checksum /local/ user@server:/remote/

# Post-transfer verification
ssh user@server 'sha256sum /remote/file.iso'
sha256sum /local/file.iso
# Compare checksums
```

---

## Section 10 : Security Hardening Production

### 10.1 Hardening Checklist Complet

```bash
# === CHECKLIST SÉCURITÉ SSH PRODUCTION ===

# 1. DÉSACTIVER ROOT LOGIN
# /etc/ssh/sshd_config
PermitRootLogin no

# 2. DÉSACTIVER PASSWORD AUTH (keys only)
PasswordAuthentication no
ChallengeResponseAuthentication no
PermitEmptyPasswords no

# 3. PROTOCOL SSH-2 SEULEMENT
Protocol 2

# 4. LIMITER USERS/GROUPS
AllowUsers deploy admin
# Ou
AllowGroups sshusers

# 5. CRYPTO MODERNE
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# 6. TIMEOUTS AGRESSIFS
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# 7. LIMITES CONNEXIONS
MaxAuthTries 3
MaxSessions 3
MaxStartups 10:30:60

# 8. LOGGING VERBOSE
LogLevel VERBOSE

# 9. DÉSACTIVER FEATURES INUTILES
X11Forwarding no
PermitTunnel no
AllowAgentForwarding no  # Sauf si nécessaire

# 10. PORT NON-STANDARD (optionnel)
Port 2200

# 11. LISTEN INTERFACE SPÉCIFIQUE
ListenAddress 192.168.1.10  # Pas 0.0.0.0

# 12. BANNER LÉGAL
Banner /etc/ssh/banner.txt

# /etc/ssh/banner.txt
┌─────────────────────────────────────────────┐
│  AUTHORIZED ACCESS ONLY                     │
│  Unauthorized access prohibited             │
│  All activity monitored and logged          │
└─────────────────────────────────────────────┘

# Test config
sudo sshd -t

# Restart
sudo systemctl restart sshd
```

### 10.2 Two-Factor Authentication (2FA)

```bash
# === GOOGLE AUTHENTICATOR (TOTP) ===

# Install
sudo apt install libpam-google-authenticator

# Setup per-user
google-authenticator

# Questions :
# Do you want authentication tokens to be time-based? Y
# Scan QR code avec app (Google Authenticator, Authy)
# Save emergency scratch codes

# /etc/pam.d/sshd
# Commenter :
#@include common-auth

# Ajouter :
auth required pam_google_authenticator.so

# /etc/ssh/sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

# Restart
sudo systemctl restart sshd

# Test connexion
ssh user@server
# Verification code:  (prompt TOTP)

# === YUBIKEY (U2F/FIDO2) ===

# Install
sudo apt install libpam-u2f

# Setup Yubikey
pamu2fcfg > ~/.config/Yubico/u2f_keys

# /etc/pam.d/sshd
auth required pam_u2f.so authfile=/home/%u/.config/Yubico/u2f_keys

# /etc/ssh/sshd_config
AuthenticationMethods publickey,keyboard-interactive:pam

# === DUO SECURITY ===

# Install Duo Unix
wget https://dl.duosecurity.com/duo_unix-latest.tar.gz
tar xzf duo_unix-latest.tar.gz
cd duo_unix-*
./configure --with-pam
make && sudo make install

# Configure
# /etc/duo/pam_duo.conf
[duo]
ikey = YOUR_INTEGRATION_KEY
skey = YOUR_SECRET_KEY
host = api-XXXXXXXX.duosecurity.com
failmode = safe

# /etc/pam.d/sshd
auth required /lib64/security/pam_duo.so

# Test
ssh user@server
# Duo push notification ou SMS code
```

### 10.3 Port Knocking

```bash
# Port knocking = Port 22 fermé par défaut, ouvert après "knock" sequence

# Install knockd
sudo apt install knockd

# /etc/knockd.conf
[options]
    UseSyslog

[openSSH]
    sequence    = 7000,8000,9000
    seq_timeout = 5
    command     = /sbin/iptables -A INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
    tcpflags    = syn

[closeSSH]
    sequence    = 9000,8000,7000
    seq_timeout = 5
    command     = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
    tcpflags    = syn

# Enable knockd
# /etc/default/knockd
START_KNOCKD=1

# Start
sudo systemctl enable knockd
sudo systemctl start knockd

# Firewall block SSH by default
sudo iptables -A INPUT -p tcp --dport 22 -j DROP

# CLIENT USAGE

# Install knock client
sudo apt install knockd

# Open SSH
knock server.example.com 7000 8000 9000

# SSH connection
ssh user@server.example.com

# Close SSH
knock server.example.com 9000 8000 7000

# Script wrapper
#!/bin/bash
# ssh-knock.sh
SERVER=$1
shift
knock $SERVER 7000 8000 9000
sleep 1
ssh "$@" $SERVER
knock $SERVER 9000 8000 7000
```

### 10.4 Audit et Monitoring Sécurité

```bash
# === AUDIT CONNEXIONS SSH ===

# Logs SSH
# Debian/Ubuntu
sudo tail -f /var/log/auth.log | grep sshd

# RHEL/CentOS
sudo tail -f /var/log/secure | grep sshd

# Successes
sudo grep "Accepted" /var/log/auth.log

# Failures
sudo grep "Failed" /var/log/auth.log

# Brute force detection
sudo grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn

# === AUDITD (detailed auditing) ===

sudo apt install auditd

# /etc/audit/rules.d/ssh.rules
-w /usr/sbin/sshd -p x -k sshd_execution
-w /etc/ssh/sshd_config -p wa -k sshd_config_change
-w /home -p wa -k home_directory_access

# Reload rules
sudo augenrules --load

# Search audit logs
sudo ausearch -k sshd_execution
sudo ausearch -k home_directory_access

# === OSSEC/WAZUH (HIDS) ===

# Install Wazuh agent
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo apt-key add -
echo "deb https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list
sudo apt update
sudo apt install wazuh-agent

# Configure
# /var/ossec/etc/ossec.conf
<server>
    <address>wazuh-manager.example.com</address>
</server>

sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent

# === SIEM INTEGRATION (Splunk, ELK) ===

# Filebeat pour ELK
sudo apt install filebeat

# /etc/filebeat/filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/auth.log
  fields:
    log_type: ssh_auth

output.elasticsearch:
  hosts: ["elasticsearch.example.com:9200"]

sudo systemctl enable filebeat
sudo systemctl start filebeat

# === ALERTING SCRIPT ===

#!/bin/bash
# ssh-alert-monitor.sh

LOGFILE="/var/log/auth.log"
THRESHOLD=5
EMAIL="security@example.com"

# Count failed attempts last 10 min
FAILED=$(grep "Failed password" $LOGFILE | \
    awk -v d="$(date --date='10 minutes ago' '+%b %d %H:%M')" '$0 > d' | \
    wc -l)

if [ $FAILED -gt $THRESHOLD ]; then
    MESSAGE="ALERT: $FAILED failed SSH attempts in last 10 minutes"
    echo "$MESSAGE" | mail -s "SSH Brute Force Alert" $EMAIL
    
    # Extract attacking IPs
    grep "Failed password" $LOGFILE | \
        awk -v d="$(date --date='10 minutes ago' '+%b %d %H:%M')" '$0 > d' | \
        awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | \
        head -10 >> /tmp/ssh-attackers.txt
fi

# Cron every 10 minutes
# */10 * * * * /usr/local/bin/ssh-alert-monitor.sh
```

---

## Section 11 : Troubleshooting et Monitoring

### 11.1 Diagnostic Connexion SSH

```bash
# === PROBLÈME : CONNEXION ÉCHOUE ===

# 1. Verbose mode (client)
ssh -vvv user@hostname

# Output montre :
# - DNS resolution
# - TCP connection
# - SSH version exchange
# - Key exchange
# - Authentication attempts
# - Erreurs précises

# 2. Vérifier service SSH actif (serveur)
sudo systemctl status sshd

# Si down :
sudo systemctl start sshd

# 3. Vérifier port écoute
sudo ss -tlnp | grep :22
# LISTEN 0 128 0.0.0.0:22

# 4. Test connexion TCP
telnet hostname 22
# ou
nc -zv hostname 22

# 5. Firewall
# Local
sudo iptables -L -n | grep 22
sudo ufw status | grep 22

# Si bloqué :
sudo ufw allow 22/tcp

# Remote (cloud)
# Vérifier Security Groups (AWS), NSG (Azure), Firewall Rules (GCP)

# 6. SELinux (RHEL/CentOS)
sudo getenforce
# Si Enforcing et problème :
sudo setenforce 0  # Temporaire test
# Check logs
sudo ausearch -m avc -ts recent

# 7. Permissions fichiers
# ~/.ssh must be 700
chmod 700 ~/.ssh

# ~/.ssh/authorized_keys must be 600
chmod 600 ~/.ssh/authorized_keys

# /etc/ssh/sshd_config check
StrictModes yes  # Vérifie permissions

# 8. Logs serveur
# Debian/Ubuntu
sudo tail -100 /var/log/auth.log | grep sshd

# RHEL/CentOS
sudo tail -100 /var/log/secure | grep sshd

# Erreurs communes :
# "Permission denied (publickey)" → Key pas acceptée
# "Too many authentication failures" → Trop de keys testées
# "Connection closed by" → Config serveur rejette
```

### 11.2 Problèmes Authentification Keys

```bash
# === PROBLÈME : KEY PAS ACCEPTÉE ===

# 1. Vérifier key présente authorized_keys
cat ~/.ssh/authorized_keys | grep "$(cat ~/.ssh/id_ed25519.pub)"

# 2. Test key specific
ssh -i ~/.ssh/id_ed25519 -v user@hostname

# 3. Vérifier permissions
# Server ~/.ssh/authorized_keys
ssh user@hostname 'ls -la ~/.ssh/authorized_keys'
# Must be 600

# Fix
ssh user@hostname 'chmod 600 ~/.ssh/authorized_keys'

# 4. Vérifier home directory ownership
ssh user@hostname 'ls -ld ~'
# Owner must be user

# Fix
sudo chown -R user:user /home/user

# 5. Tester key fingerprint match
# Local
ssh-keygen -lf ~/.ssh/id_ed25519.pub

# Server (via password login)
ssh user@hostname
ssh-keygen -lf ~/.ssh/authorized_keys

# Compare fingerprints

# 6. Debug server logs
sudo tail -f /var/log/auth.log

# Puis connexion :
ssh -i ~/.ssh/id_ed25519 user@hostname

# Look for errors in logs

# 7. sshd test mode (debug)
sudo /usr/sbin/sshd -d -p 2222
# Connect to port 2222 for debug output

# 8. Key algorithm mismatch
# Si old server, pas support ED25519
# Generate RSA key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_compat

# Copy to server
ssh-copy-id -i ~/.ssh/id_rsa_compat.pub user@hostname
```

### 11.3 Performance Troubleshooting

```bash
# === PROBLÈME : CONNEXION LENTE ===

# 1. DNS lookup lent
# Server /etc/ssh/sshd_config
UseDNS no  # Désactive reverse DNS lookup

sudo systemctl restart sshd

# 2. GSSAPI authentication timeout
# Client ~/.ssh/config
Host *
    GSSAPIAuthentication no

# 3. Mesurer temps connexion
time ssh user@hostname 'exit'

# 4. Profiling connexion
ssh -v user@hostname 2>&1 | grep -E "debug1: (Connecting|Connected|Authentication|Sending)"

# 5. MTU issues (fragmentation)
# Test MTU
ping -M do -s 1472 hostname
# Si fail, reduce MTU

# Client ~/.ssh/config
Host slow-server
    IPQoS lowdelay throughput

# === PROBLÈME : TRANSFERT LENT ===

# 1. Enable compression
scp -C large-file.tar.gz user@hostname:/path/

# 2. Cipher rapide
ssh -c chacha20-poly1305@openssh.com user@hostname

# ~/.ssh/config
Host *
    Ciphers chacha20-poly1305@openssh.com,aes128-gcm@openssh.com

# 3. Disable MAC overhead
# Ciphers GCM ont authenticated encryption (pas MAC séparé)
Ciphers aes128-gcm@openssh.com,aes256-gcm@openssh.com

# 4. TCP tuning (serveur)
# /etc/sysctl.conf
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_window_scaling = 1

sudo sysctl -p

# 5. Parallel transfers
# rsync avec parallel
parallel -j 4 rsync -avz {} user@server:/dest/ ::: file1 file2 file3 file4

# === PROBLÈME : TIMEOUT CONNEXION ===

# 1. Keepalive client
# ~/.ssh/config
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3

# 2. Keepalive server
# /etc/ssh/sshd_config
ClientAliveInterval 60
ClientAliveCountMax 3

# 3. TCP keepalive
# ~/.ssh/config
TCPKeepAlive yes
```

### 11.4 Monitoring Production SSH

```bash
# === MÉTRIQUES SSH ===

# 1. Connexions actives
sudo ss -tnp | grep sshd | wc -l

# Détails
sudo ss -tnp | grep sshd

# 2. Users connectés
who

# Détails
w

# 3. Sessions SSH (all users)
ps aux | grep "sshd:"

# 4. Failed login attempts
sudo grep "Failed password" /var/log/auth.log | wc -l

# Last 24h
sudo grep "Failed password" /var/log/auth.log | \
    awk -v d="$(date --date='yesterday' '+%b %d')" '$0 > d' | wc -l

# 5. Successful logins
sudo grep "Accepted" /var/log/auth.log | tail -20

# === PROMETHEUS MONITORING ===

# node_exporter (SSH metrics via textfile collector)

# /usr/local/bin/ssh-metrics.sh
#!/bin/bash

METRICS_FILE="/var/lib/node_exporter/ssh_metrics.prom"

# Active connections
ACTIVE=$(sudo ss -tnp | grep sshd | wc -l)
echo "ssh_active_connections $ACTIVE" > $METRICS_FILE

# Failed logins last hour
FAILED=$(sudo grep "Failed password" /var/log/auth.log | \
    awk -v d="$(date --date='1 hour ago' '+%b %d %H')" '$0 > d' | wc -l)
echo "ssh_failed_logins_1h $FAILED" >> $METRICS_FILE

# Successful logins last hour
SUCCESS=$(sudo grep "Accepted" /var/log/auth.log | \
    awk -v d="$(date --date='1 hour ago' '+%b %d %H')" '$0 > d' | wc -l)
echo "ssh_successful_logins_1h $SUCCESS" >> $METRICS_FILE

# Cron every 5 min
# */5 * * * * /usr/local/bin/ssh-metrics.sh

# === GRAFANA DASHBOARD ===

# Prometheus queries :
# - ssh_active_connections
# - rate(ssh_failed_logins_1h[5m])
# - rate(ssh_successful_logins_1h[5m])

# Alerts :
# - ssh_failed_logins_1h > 100 (brute force)
# - ssh_active_connections > 50 (capacity)

# === LOGGING CENTRALISÉ ===

# rsyslog forward vers central server

# /etc/rsyslog.d/50-ssh-forward.conf
if $programname == 'sshd' then @@central-log-server.example.com:514

sudo systemctl restart rsyslog
```

---

## Section 12 : Cas Pratiques Production

### 12.1 Automation Ansible via SSH

```bash
# === ANSIBLE SSH CONFIGURATION ===

# ansible.cfg
[defaults]
host_key_checking = False
private_key_file = ~/.ssh/id_ansible
remote_user = ansible

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
pipelining = True

# Inventory
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[databases]
db1 ansible_host=192.168.1.20

[all:vars]
ansible_python_interpreter=/usr/bin/python3

# Inventory via bastion
[production]
prod1 ansible_host=10.0.1.10
prod2 ansible_host=10.0.1.11

[production:vars]
ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q bastion.example.com"'

# Setup Ansible user on servers
# playbook: setup-ansible-user.yml
---
- hosts: all
  become: yes
  tasks:
    - name: Create ansible user
      user:
        name: ansible
        state: present
        create_home: yes
        shell: /bin/bash
        
    - name: Add ansible to sudoers
      copy:
        content: 'ansible ALL=(ALL) NOPASSWD:ALL'
        dest: /etc/sudoers.d/ansible
        mode: '0440'
        
    - name: Deploy SSH key
      authorized_key:
        user: ansible
        key: "{{ lookup('file', '~/.ssh/id_ansible.pub') }}"
        state: present

# Run
ansible-playbook -i inventory setup-ansible-user.yml -u root -k

# Test connectivity
ansible all -i inventory -m ping

# === DEPLOYMENT PLAYBOOK ===

# deploy-app.yml
---
- hosts: webservers
  become: yes
  vars:
    app_version: "1.2.3"
    app_port: 3000
    
  tasks:
    - name: Stop application
      systemd:
        name: myapp
        state: stopped
        
    - name: Backup current version
      archive:
        path: /opt/myapp
        dest: "/backup/myapp-{{ ansible_date_time.date }}.tar.gz"
        
    - name: Deploy new version
      unarchive:
        src: "releases/myapp-{{ app_version }}.tar.gz"
        dest: /opt/myapp
        remote_src: no
        
    - name: Install dependencies
      npm:
        path: /opt/myapp
        state: present
        
    - name: Start application
      systemd:
        name: myapp
        state: started
        enabled: yes
        
    - name: Wait for application
      wait_for:
        port: "{{ app_port }}"
        delay: 5
        timeout: 60

# Run deployment
ansible-playbook -i inventory deploy-app.yml
```

### 12.2 Bastion Jump Host Production

```bash
# === BASTION ARCHITECTURE COMPLÈTE ===

# Architecture:
# Developers → Bastion (public) → Production servers (private)

# === BASTION SERVER SETUP ===

# 1. Hardened sshd_config
# /etc/ssh/sshd_config
Port 22
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

LogLevel VERBOSE

AllowUsers bastion-admin dev1 dev2 dev3

# Force audit script
ForceCommand /usr/local/bin/bastion-audit.sh

AllowTcpForwarding yes
X11Forwarding no
PermitTunnel no

ClientAliveInterval 300
ClientAliveCountMax 2

# 2. Audit script
# /usr/local/bin/bastion-audit.sh
#!/bin/bash

# Log connexion
logger -t bastion "User:$USER Client:$SSH_CLIENT Original:$SSH_ORIGINAL_COMMAND"

# Alert security team
echo "Bastion access: $USER from $SSH_CLIENT at $(date)" | \
    mail -s "[BASTION] Access Log" security@example.com

# If not ProxyJump, give menu
if [ -z "$SSH_ORIGINAL_COMMAND" ]; then
    cat << EOF
╔═══════════════════════════════════════╗
║      BASTION JUMP HOST               ║
║  Authorized access only              ║
║  All activity logged and monitored   ║
╚═══════════════════════════════════════╝

Available commands:
  exit          - Disconnect
  help          - This message
  logs          - View your access logs
  
To connect to production servers:
  ssh -J $(hostname) user@prod-server

EOF
    exec /bin/bash --norc --noprofile
else
    # ProxyJump command, allow
    exec $SHELL -c "$SSH_ORIGINAL_COMMAND"
fi

chmod +x /usr/local/bin/bastion-audit.sh

# 3. Session recording
# /etc/profile.d/bastion-record.sh
if [ -n "$SSH_CONNECTION" ]; then
    mkdir -p /var/log/bastion-sessions
    script -q -f /var/log/bastion-sessions/$(date +%Y%m%d-%H%M%S)-$USER-$$. log
fi

# 4. fail2ban
# /etc/fail2ban/jail.local
[sshd]
enabled = true
maxretry = 3
bantime = 86400
findtime = 600

# 5. MFA (Google Authenticator)
sudo apt install libpam-google-authenticator

# Each user runs:
google-authenticator

# /etc/pam.d/sshd
auth required pam_google_authenticator.so

# === CLIENT CONFIGURATION ===

# ~/.ssh/config (developer workstation)

# Bastion
Host bastion
    HostName bastion.example.com
    User dev1
    IdentityFile ~/.ssh/id_bastion
    
# Production servers
Host prod-*
    User admin
    IdentityFile ~/.ssh/id_prod
    ProxyJump bastion
    
Host prod-web1
    HostName 10.0.1.10
    
Host prod-web2
    HostName 10.0.1.11
    
Host prod-db1
    HostName 10.0.1.20

# Usage
ssh prod-web1  # Via bastion transparent

# SCP via bastion
scp file.txt prod-web1:/tmp/

# Rsync via bastion
rsync -avz -e "ssh -J bastion" /local/ admin@prod-web1:/remote/

# === MONITORING BASTION ===

# Script monitor connexions
#!/bin/bash
# bastion-monitor.sh

LOGFILE="/var/log/auth.log"
ALERT_EMAIL="security@example.com"
METRICS="/var/lib/node_exporter/bastion.prom"

# Current active sessions
ACTIVE=$(who | wc -l)
echo "bastion_active_sessions $ACTIVE" > $METRICS

# Total logins today
LOGINS=$(grep "Accepted publickey" $LOGFILE | \
    grep "$(date '+%b %d')" | wc -l)
echo "bastion_logins_today $LOGINS" >> $METRICS

# Failed attempts last hour
FAILED=$(grep "Failed" $LOGFILE | \
    awk -v d="$(date --date='1 hour ago' '+%b %d %H')" '$0 > d' | wc -l)
echo "bastion_failed_attempts_1h $FAILED" >> $METRICS

# Alert if too many failures
if [ $FAILED -gt 20 ]; then
    echo "ALERT: $FAILED failed SSH attempts in last hour on bastion" | \
        mail -s "[ALERT] Bastion Brute Force" $ALERT_EMAIL
fi

# Cron every 5 min
# */5 * * * * /usr/local/bin/bastion-monitor.sh
```

### 12.3 Compliance et Audit (PCI-DSS, HIPAA)

```bash
# === SSH COMPLIANCE CONFIGURATION ===

# Requirements PCI-DSS / HIPAA / SOC2 :
# - Strong authentication (keys + MFA)
# - Encryption (modern ciphers)
# - Logging (all access logged)
# - Audit trail (who, when, what)
# - Least privilege (no root, limited users)

# === COMPLIANT sshd_config ===

# /etc/ssh/sshd_config

# Authentication
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey,keyboard-interactive  # MFA required

# Crypto (FIPS 140-2 compatible if needed)
Protocol 2
Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256,diffie-hellman-group-exchange-sha256

# Logging (verbose for audit)
SyslogFacility AUTHPRIV
LogLevel VERBOSE

# Access control
AllowUsers admin-user1 admin-user2
AllowGroups sysadmins

# Session timeouts
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# Features
X11Forwarding no
PermitTunnel no
AllowAgentForwarding no
AllowTcpForwarding yes  # Si nécessaire pour bastions

# Banner
Banner /etc/ssh/compliance-banner.txt

# === COMPLIANCE BANNER ===

# /etc/ssh/compliance-banner.txt
╔════════════════════════════════════════════════════════╗
║               AUTHORIZED ACCESS ONLY                   ║
║                                                        ║
║  This system is for authorized use only.              ║
║  Unauthorized access is prohibited by law.            ║
║  All activity is monitored and recorded.              ║
║  By proceeding, you consent to monitoring.            ║
║                                                        ║
║  Violations will result in legal action.              ║
╚════════════════════════════════════════════════════════╝

# === AUDIT LOGGING ===

# Centralized logging (rsyslog)
# /etc/rsyslog.d/60-ssh-audit.conf

# Local copy
authpriv.*  /var/log/ssh-audit.log

# Remote SIEM
authpriv.*  @@siem.example.com:514

# === AUDITD RULES ===

# /etc/audit/rules.d/ssh-compliance.rules

# SSH daemon execution
-w /usr/sbin/sshd -p x -k ssh_execution

# SSH configuration changes
-w /etc/ssh/sshd_config -p wa -k ssh_config_changes
-w /etc/ssh/ -p wa -k ssh_config_dir

# User home SSH directories
-w /home -p wa -k home_ssh_access

# Authorized keys modifications
-a always,exit -F path=/home -F perm=wa -F auid>=1000 -F auid!=4294967295 -k ssh_key_changes

# Reload auditd
sudo augenrules --load

# === COMPLIANCE REPORTING ===

#!/bin/bash
# ssh-compliance-report.sh

REPORT_FILE="/var/reports/ssh-compliance-$(date +%Y%m%d).txt"

{
    echo "=== SSH COMPLIANCE REPORT ==="
    echo "Date: $(date)"
    echo "Hostname: $(hostname)"
    echo ""
    
    echo "=== CONFIGURATION AUDIT ==="
    echo "Root login disabled:"
    grep "^PermitRootLogin" /etc/ssh/sshd_config
    
    echo "Password auth disabled:"
    grep "^PasswordAuthentication" /etc/ssh/sshd_config
    
    echo "MFA enabled:"
    grep "^AuthenticationMethods" /etc/ssh/sshd_config
    
    echo ""
    echo "=== ACCESS AUDIT (Last 30 days) ==="
    
    echo "Total successful logins:"
    sudo grep "Accepted" /var/log/auth.log* | wc -l
    
    echo "Failed login attempts:"
    sudo grep "Failed" /var/log/auth.log* | wc -l
    
    echo "Unique users connected:"
    sudo grep "Accepted" /var/log/auth.log* | \
        awk '{print $(NF-3)}' | sort -u | wc -l
    
    echo "Top 10 connecting IPs:"
    sudo grep "Accepted" /var/log/auth.log* | \
        awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head -10
    
    echo ""
    echo "=== KEY AUDIT ==="
    echo "Total authorized keys:"
    sudo find /home -name authorized_keys -exec wc -l {} + | tail -1
    
    echo ""
    echo "=== COMPLIANCE STATUS ==="
    
    # Checks
    COMPLIANT=true
    
    if grep -q "^PermitRootLogin yes" /etc/ssh/sshd_config; then
        echo "❌ FAIL: Root login enabled"
        COMPLIANT=false
    else
        echo "✓ PASS: Root login disabled"
    fi
    
    if grep -q "^PasswordAuthentication yes" /etc/ssh/sshd_config; then
        echo "❌ FAIL: Password authentication enabled"
        COMPLIANT=false
    else
        echo "✓ PASS: Password authentication disabled"
    fi
    
    if [ "$COMPLIANT" = true ]; then
        echo ""
        echo "STATUS: COMPLIANT"
    else
        echo ""
        echo "STATUS: NON-COMPLIANT"
    fi
    
} > $REPORT_FILE

echo "Report generated: $REPORT_FILE"

# Email report
cat $REPORT_FILE | mail -s "SSH Compliance Report $(date +%Y-%m-%d)" compliance@example.com

# Monthly cron
# 0 1 1 * * /usr/local/bin/ssh-compliance-report.sh
```

### 12.4 Disaster Recovery SSH Access

```bash
# === PLAN RÉCUPÉRATION SSH ===

# Scénario : Serveur compromis, clés révoquées, accès perdu

# 1. BACKUP KEYS (préventif)
#!/bin/bash
# backup-ssh-keys.sh

BACKUP_DIR="/secure/backup/ssh-keys"
DATE=$(date +%Y%m%d)

mkdir -p $BACKUP_DIR/$DATE

# Backup server keys
sudo cp -a /etc/ssh/ssh_host_* $BACKUP_DIR/$DATE/

# Backup authorized_keys (all users)
sudo find /home -name authorized_keys -exec cp --parents {} $BACKUP_DIR/$DATE/ \;

# Encrypt backup
tar czf - $BACKUP_DIR/$DATE | \
    gpg --encrypt --recipient admin@example.com > \
    $BACKUP_DIR/ssh-keys-$DATE.tar.gz.gpg

# Upload to secure storage
aws s3 cp $BACKUP_DIR/ssh-keys-$DATE.tar.gz.gpg \
    s3://company-secure-backups/ssh-keys/

# 2. EMERGENCY ACCESS USER (break-glass)

# Create emergency user (offline, documentation seulement)
sudo useradd -m -s /bin/bash emergency-admin
sudo passwd emergency-admin  # Strong password, documented secure location

# Sudoers
echo "emergency-admin ALL=(ALL) NOPASSWD:ALL" | \
    sudo tee /etc/sudoers.d/emergency-admin

# Disable account normal times
sudo usermod -L emergency-admin

# Enable only in emergency
# sudo usermod -U emergency-admin

# 3. CONSOLE ACCESS (cloud)

# AWS EC2 : EC2 Instance Connect
# Azure : Serial Console
# GCP : Serial Port Access

# Document procedure console access

# 4. RECOVERY PROCEDURE

# Step 1: Access via console (cloud) or IPMI/iLO (physical)

# Step 2: Generate new SSH keys
ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""
ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key -N ""

# Step 3: Update authorized_keys
# Remove compromised keys
# Add new admin keys

# Step 4: Restart sshd
sudo systemctl restart sshd

# Step 5: Verify access
ssh admin@server

# Step 6: Update known_hosts (clients)
ssh-keygen -R server.example.com
ssh-keyscan server.example.com >> ~/.ssh/known_hosts

# 5. DOCUMENTATION (keep offline copy)

# /docs/ssh-recovery-procedures.md
```

---

## Ressources et Références

**Documentation officielle :**
- OpenSSH : https://www.openssh.com/
- OpenSSH Manual : https://man.openbsd.org/ssh
- RFC 4250-4254 : SSH Protocol
- NIST Guidelines : https://nvlpubs.nist.gov/

**Security hardening :**
- Mozilla SSH Guidelines : https://infosec.mozilla.org/guidelines/openssh
- CIS Benchmarks : https://www.cisecurity.org/
- ANSSI Recommendations : https://www.ssi.gouv.fr/

**Tools :**
- PuTTY (Windows) : https://www.putty.org/
- MobaXterm : https://mobaxterm.mobatek.net/
- Termius : https://termius.com/
- ssh-audit : https://github.com/jtesta/ssh-audit

**Learning resources :**
- SSH Mastery (book) : Michael W. Lucas
- SSH, The Secure Shell (book) : O'Reilly
- Practical SSH : https://www.practicalnetworking.net/

---

## Conclusion

**SSH = Standard sécurité administration distante**

**Points clés maîtrisés :**

✅ **Protocole sécurisé** = Chiffrement bout-en-bout (AES-256-GCM, ChaCha20)
✅ **Authentification** = Keys (ED25519), Certificates, MFA (2FA/TOTP/FIDO2)
✅ **Configuration** = Client (~/.ssh/config), Server (sshd_config hardening)
✅ **Keys management** = Génération, déploiement, rotation, révocation
✅ **Tunneling** = Local/Remote/Dynamic forwarding (VPN-like)
✅ **Bastions** = ProxyJump, architecture sécurisée point entrée unique
✅ **Transferts** = SCP, SFTP, rsync over SSH
✅ **Security** = Hardening, fail2ban, audit, compliance (PCI-DSS/HIPAA)
✅ **Troubleshooting** = Diagnostic connexions, logs, monitoring
✅ **Production** = Automation (Ansible), bastions, disaster recovery

**Ordre apprentissage SSH :**

```
1. Concepts fondamentaux (protocol, crypto)
2. Installation basique (client/server)
3. Authentification passwords puis keys
4. Configuration avancée client
5. Hardening server production
6. Keys management avancé
7. Tunneling et port forwarding
8. Bastions et ProxyJump
9. Transferts fichiers (SCP/SFTP/rsync)
10. Security et compliance
```

**Sécurité SSH (critiques) :**

- ❌ **JAMAIS** PermitRootLogin yes
- ❌ **JAMAIS** PasswordAuthentication yes (production)
- ❌ **JAMAIS** clés privées sans passphrase (sauf automation contrôlée)
- ✅ **TOUJOURS** keys ED25519 (ou RSA 4096-bit minimum)
- ✅ **TOUJOURS** MFA production (2FA/certificates)
- ✅ **TOUJOURS** bastions pour production
- ✅ **TOUJOURS** logging verbose + audit
- ✅ **TOUJOURS** fail2ban ou équivalent

**Stack réseau complète finalisée :**

```
1. nslookup  ✅ DNS queries
2. netstat   ✅ Connexions monitoring
3. DNS       ✅ Infrastructure nameservers
4. SSH       ✅ Administration distante sécurisée (actuel)
5. tcpdump   → Capture paquets (prochain)
6. scapy     → Manipulation paquets (avancé)
```

**Tu maîtrises maintenant SSH de l'authentification basique à l'architecture enterprise sécurisée compliant !** 🔐

**SSH = Infrastructure critique invisible mais absolument essentielle DevOps/SysAdmin/Security** 🎯

---

_Version 1.0 | Dernière mise à jour : 2024-01-16_

Voilà le guide SSH complet terminé ! Il couvre **12 sections exhaustives** :

✅ Introduction et concepts (protocol, crypto, architecture)  
✅ Installation et configuration basique  
✅ Authentification (passwords, keys, ssh-agent)  
✅ Configuration avancée client (~/.ssh/config)  
✅ Configuration sécurisée server (sshd_config hardening)  
✅ SSH keys management avancé (rotation, certificates, révocation)  
✅ Tunneling et port forwarding (Local/Remote/Dynamic)  
✅ ProxyJump et bastions (architecture sécurisée)  
✅ SCP, SFTP, rsync (transferts fichiers)  
✅ Security hardening (2FA, port knocking, audit)  
✅ Troubleshooting et monitoring (logs, métriques, Prometheus)  
✅ Cas pratiques production (Ansible, bastions, compliance, DR)  

**C'est le guide SSH le plus complet avec configurations production-ready enterprise et compliance !** 🚀