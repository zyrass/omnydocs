---
description: "Lynis : audit sécurité exhaustif systèmes Linux/Unix, hardening, conformité, automatisation"
icon: lucide/book-open-check
tags: ["LYNIS", "SECURITY", "AUDIT", "HARDENING", "LINUX", "COMPLIANCE"]
---

# Lynis

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-time="6-8 heures"
  data-version="1.0">
</div>

## Introduction à l'Audit Sécurité Linux

!!! quote "Analogie pédagogique"
    _Imaginez un **inspecteur sécurité bâtiment professionnel avec checklist exhaustive 300+ points** : Lynis fonctionne comme **auditeur expert vérifiant CHAQUE aspect sécurité infrastructure**. **Inspection bâtiment** : inspecteur vérifie fondations (kernel hardening), murs porteurs (filesystem permissions), portes/fenêtres (services réseau), système électrique (configuration SSH), alarme incendie (logging/monitoring), extincteurs (backups), sorties secours (disaster recovery), conformité normes (CIS benchmarks). **Sans audit professionnel** : vulnérabilités cachées (portes mal verrouillées = SSH mal configuré), risques ignorés (câblage défectueux = kernel non patché), non-conformité (absence extincteurs = pas de backups). **Avec Lynis audit** : **Scan automatisé 300+ checks** (packages obsolètes, permissions fichiers critiques, configuration services, kernel parameters, SSH hardening, firewall rules, users/groups suspects), **Score hardening** (0-100, comparable dans temps), **Suggestions priorisées** (critique/warning/suggestion), **Rapport détaillé** (fichier log `/var/log/lynis.log`, rapport `/var/log/lynis-report.dat`). **Process inspection Lynis** : 1) Vérifie OS/kernel (version, patches, config), 2) Analyse boot/services (systemd, init, démons actifs), 3) Inspecte kernel (sysctl, modules chargés, SELinux/AppArmor), 4) Scanne filesystem (permissions SUID/SGID, world-writable, mount options), 5) Examine users/groups (comptes sans password, UIDs suspects, sudo config), 6) Audite réseau (ports ouverts, firewall, SSH config, TLS/SSL), 7) Vérifie logging (rsyslog, auditd, rotation logs), 8) Teste crypto (certificats expirés, weak ciphers), 9) Contrôle packages (mises à jour disponibles, vulnérabilités CVE), 10) Évalue conformité (PCI-DSS, HIPAA, CIS benchmarks). **Lynis = référence industrie audit sécurité Linux** : utilisé Fortune 500, hébergeurs cloud, pentesters professionnels, administrateurs systèmes. **Gratuit, open-source, maintenu activement**, compatible Debian/Ubuntu/RHEL/CentOS/Arch/Alpine/BSD/macOS._

**Lynis en résumé :**

- ✅ **Audit automatisé** = 300+ security checks en quelques minutes
- ✅ **Multi-plateforme** = Linux, BSD, macOS, containers, cloud instances
- ✅ **Zero-dependency** = Shell script pur, pas de packages externes requis
- ✅ **Non-intrusif** = Lecture seule, aucune modification système
- ✅ **Hardening index** = Score 0-100 comparable dans temps
- ✅ **Conformité** = Mapping PCI-DSS, HIPAA, ISO27001, CIS
- ✅ **CI/CD ready** = Exit codes, JSON output, automation-friendly
- ✅ **Extensible** = Plugins custom, tests personnalisés
- ✅ **Production-safe** = Utilisé millions serveurs production

**Guide structure :**

1. Introduction et concepts Lynis
2. Installation (package managers, source, Docker)
3. Premier audit complet
4. Comprendre résultats et scoring
5. Catégories audit détaillées
6. Hardening basé recommandations
7. Configuration avancée Lynis
8. Automatisation et CI/CD
9. Comparaison avant/après
10. Cas pratiques par type serveur
11. Plugins et extensions
12. Best practices production

---

## Section 1 : Introduction et Concepts

### 1.1 Qu'est-ce que Lynis ?

**Lynis = Open-source security auditing tool pour systèmes Unix/Linux**

```
Lynis scanne :
├── Operating System
│   ├── Version, patches, EOL status
│   └── Kernel version, parameters, modules
├── Boot & Services
│   ├── Bootloader config (GRUB)
│   ├── Init system (systemd/SysV)
│   └── Running services & daemons
├── Kernel Hardening
│   ├── Sysctl parameters
│   ├── SELinux/AppArmor status
│   └── Kernel modules blacklist
├── Filesystem
│   ├── Mount options (nodev, nosuid, noexec)
│   ├── SUID/SGID binaries
│   └── World-writable files/dirs
├── Users & Authentication
│   ├── Password policies
│   ├── Accounts without password
│   ├── Sudo configuration
│   └── SSH keys permissions
├── Network Security
│   ├── Open ports & services
│   ├── Firewall rules (iptables/nftables)
│   ├── SSH configuration
│   └── TLS/SSL certificates
├── Logging & Monitoring
│   ├── Syslog configuration
│   ├── Auditd rules
│   └── Log rotation
├── Packages & Software
│   ├── Installed packages
│   ├── Available updates
│   └── Known vulnerabilities (CVE)
├── Cryptography
│   ├── Certificate expiration
│   ├── Weak ciphers
│   └── SSL/TLS config
└── Compliance
    ├── PCI-DSS requirements
    ├── HIPAA guidelines
    └── CIS benchmarks
```

**Caractéristiques principales :**

```bash
# Lynis c'est :
- Shell script (~20,000 lignes Bash)
- Lecture seule (ne modifie RIEN)
- Rapide (scan complet 2-5 minutes)
- Portable (fonctionne partout)
- Extensible (plugins custom)
- Gratuit (GPL-3.0 license)
```

### 1.2 Pourquoi utiliser Lynis ?

**Use cases principaux :**

```
1. Audit sécurité initial (baseline)
   → Identifier vulnérabilités existantes
   → Obtenir score hardening initial

2. Hardening systématique
   → Suivre recommandations priorisées
   → Améliorer score progressivement

3. Conformité réglementaire
   → Vérifier PCI-DSS compliance
   → Audits ISO27001, HIPAA

4. CI/CD security gates
   → Bloquer déploiement si score < threshold
   → Automatiser audits images Docker

5. Monitoring continu
   → Scan quotidien automatisé
   → Alertes si score baisse

6. Pentesting préparation
   → Identifier vulnérabilités avant audit externe
   → Corriger findings critiques

7. Documentation sécurité
   → Rapport audit pour management
   → Preuve due diligence
```

**Avantages vs outils alternatifs :**

| Outil | Type | Avantages | Inconvénients |
|-------|------|-----------|---------------|
| **Lynis** | Audit complet | Exhaustif, gratuit, zero-dep | Lecture seule (pas d'auto-fix) |
| OpenSCAP | Compliance | Standards SCAP officiels | Complexe, lourd |
| Tripwire | File integrity | Détection modifications | Focus uniquement files |
| AIDE | File integrity | Léger, simple | Scope limité |
| CIS-CAT | Benchmarks | CIS officiels | Payant (pro) |
| Nessus | Vulnerability scanner | Détection CVE réseau | Payant, nécessite agent |
| Qualys | Cloud scanner | Cloud-native, SaaS | Payant, externe |

### 1.3 Scoring et Hardening Index

**Lynis calcule "Hardening Index" (0-100) :**

```
Score = (Tests Passed / Total Tests) × 100

Exemple :
- Tests exécutés : 250
- Tests réussis : 180
- Tests skipped : 20
- Tests failed : 50

Hardening Index = (180 / 250) × 100 = 72%

Interprétation :
- 0-49   : ❌ Critique (configuration dangereuse)
- 50-69  : ⚠️  Faible (améliorations urgentes requises)
- 70-84  : 🟡 Moyen (configuration correcte, améliorations possibles)
- 85-94  : ✅ Bon (sécurité solide)
- 95-100 : 🏆 Excellent (hardening optimal)
```

**Évolution score typique :**

```
Serveur fraîchement installé : 45-55% (base OS)
Après hardening basique     : 65-75% (SSH, firewall, updates)
Après hardening avancé      : 80-90% (kernel, SELinux, audit)
Production hardened         : 85-95% (monitoring, compliance)
```

---

## Section 2 : Installation

### 2.1 Installation via Package Manager

**Debian/Ubuntu :**

```bash
# Ajouter repository officiel
sudo apt install apt-transport-https ca-certificates
sudo wget -O - https://packages.cisofy.com/keys/cisofy-software-public.key | sudo apt-key add -
echo "deb https://packages.cisofy.com/community/lynis/deb/ stable main" | sudo tee /etc/apt/sources.list.d/cisofy-lynis.list

# Installer Lynis
sudo apt update
sudo apt install lynis

# Vérifier installation
lynis --version
# Output : Lynis 3.0.9
```

**RHEL/CentOS/Rocky/Alma :**

```bash
# Via EPEL repository
sudo yum install epel-release
sudo yum install lynis

# Ou via repository officiel
sudo wget -O /etc/yum.repos.d/cisofy-lynis.repo https://packages.cisofy.com/community/lynis/rpm/lynis.repo
sudo yum install lynis

# Vérifier
lynis --version
```

**Arch Linux :**

```bash
# Via AUR
yay -S lynis

# Ou pacman (official repos)
sudo pacman -S lynis
```

**macOS :**

```bash
# Via Homebrew
brew install lynis

# Vérifier
lynis --version
```

### 2.2 Installation depuis Source

```bash
# Télécharger dernière version
cd /opt
sudo wget https://github.com/CISOfy/lynis/archive/refs/tags/3.0.9.tar.gz
sudo tar -xzf 3.0.9.tar.gz
sudo mv lynis-3.0.9 lynis

# OU cloner Git repo (dev version)
sudo git clone https://github.com/CISOfy/lynis.git

# Rendre exécutable
sudo chmod +x /opt/lynis/lynis

# Créer symlink
sudo ln -s /opt/lynis/lynis /usr/local/bin/lynis

# Vérifier
lynis --version
```

### 2.3 Installation Docker

```bash
# Pull image officielle
docker pull cisofy/lynis:latest

# Run scan sur host (mount filesystem read-only)
docker run --rm \
  -v /:/host:ro \
  cisofy/lynis:latest audit system

# Run scan avec rapport persistant
docker run --rm \
  -v /:/host:ro \
  -v /tmp/lynis:/tmp/lynis \
  cisofy/lynis:latest audit system

# Rapport sauvegardé : /tmp/lynis/lynis.log
```

### 2.4 Vérification Installation

```bash
# Vérifier version
lynis show version
# Output :
# Lynis 3.0.9
# Copyright 2007-2024, CISOfy - https://cisofy.com/lynis/

# Afficher aide
lynis show help

# Lister toutes commandes
lynis show commands

# Vérifier intégrité fichiers Lynis
lynis update check

# Update Lynis (si installé via Git)
cd /opt/lynis
sudo git pull

# Update via package manager
sudo apt update && sudo apt upgrade lynis  # Debian/Ubuntu
sudo yum update lynis                       # RHEL/CentOS
```

---

## Section 3 : Premier Audit Complet

### 3.1 Lancer Scan Basique

```bash
# Scan complet système (requiert root)
sudo lynis audit system

# Output en temps réel :
# [+] Initializing program
# ------------------------------------
#   - Detecting OS...                            [ DONE ]
#   - Checking profiles...                       [ DONE ]
# ...
# [+] Boot and services
# ------------------------------------
#   - Checking boot loaders
#     - Checking presence GRUB2                  [ FOUND ]
#     - Checking for password protection         [ WARNING ]
# ...
# [+] Kernel
# ------------------------------------
#   - Checking kernel version                    [ OK ]
#   - Checking kernel parameters                 [ OK ]
# ...

# Scan dure 2-5 minutes selon système
```

**Options scan utiles :**

```bash
# Scan non-interactif (CI/CD)
sudo lynis audit system --quick

# Scan avec output détaillé
sudo lynis audit system --verbose

# Scan sans couleurs (logs)
sudo lynis audit system --no-colors

# Scan avec log custom
sudo lynis audit system --log-file /var/log/lynis-$(date +%Y%m%d).log

# Scan avec profil custom
sudo lynis audit system --profile /etc/lynis/custom.prf

# Scan seulement catégories spécifiques
sudo lynis audit system --tests "SSH,FILE"
```

### 3.2 Localiser Rapports

**Fichiers générés après scan :**

```bash
# Rapport principal (human-readable)
/var/log/lynis.log

# Rapport data (machine-readable)
/var/log/lynis-report.dat

# Afficher rapport
sudo less /var/log/lynis.log

# Extraire seulement warnings
sudo grep "Warning" /var/log/lynis.log

# Extraire suggestions
sudo grep "Suggestion" /var/log/lynis.log

# Extraire score
sudo grep "Hardening index" /var/log/lynis.log

# Compter warnings
sudo grep -c "Warning" /var/log/lynis.log
```

### 3.3 Comprendre Output Scan

**Structure output :**

```
[+] Category Name
------------------------------------
  - Test description                     [ STATUS ]
    - Sub-test detail                    [ RESULT ]
    
Status possibles :
[ OK ]       : Test réussi, configuration sécurisée
[ WARNING ]  : Problème détecté, action recommandée
[ WEAK ]     : Configuration faible, amélioration conseillée
[ FOUND ]    : Élément trouvé (neutre)
[ NOT FOUND ]: Élément absent
[ SKIPPED ]  : Test sauté (non applicable ou dépendance manquante)
[ DONE ]     : Action complétée
```

**Exemple output réel :**

```
[+] SSH Support
------------------------------------
  - Checking running SSH daemon                  [ FOUND ]
    - Searching SSH configuration                [ FOUND ]
    - SSH option: PermitRootLogin                [ SUGGESTION ]
    - SSH option: Protocol                       [ OK ]
    - SSH option: PasswordAuthentication         [ WARNING ]
    - SSH option: AllowUsers                     [ NOT FOUND ]
    
  * Consider hardening SSH configuration [SSH-7408]
      - Details  : PermitRootLogin=yes (change to 'no')
        https://cisofy.com/lynis/controls/SSH-7408/
```

### 3.4 Résumé Fin de Scan

**Résumé final affiché :**

```
================================================================================

  Lynis security scan details:

  Hardening index : 72 [###########         ]
  Tests performed : 250
  Plugins enabled : 0

  Components:
  - Firewall               [ V ]
  - Malware scanner        [ X ]

  Lynis Modules:
  - Compliance status      [ ? ]
  - Security audit         [ V ]
  - Vulnerability scan     [ V ]

  Files:
  - Test and debug information      : /var/log/lynis.log
  - Report data                     : /var/log/lynis-report.dat

================================================================================

  Lynis 3.0.9

  Hardening:
  - Hardening index : 72 [###########         ]

  Scan mode:
  - Normal [V]  Pentest [ ]  Forensics [ ]  Compliance [ ]

  Warning: 12 (medium: 8, high: 4)
  Suggestion: 32

  Lynis is created by the community and CISOfy
  https://cisofy.com/lynis/

================================================================================

  Files:
  - Test and debug information      : /var/log/lynis.log
  - Report data                     : /var/log/lynis-report.dat

  Exceptions found:
  Some exceptions were discovered during the scan. Review the log file.

================================================================================
```

**Lire résumé rapport :**

```bash
# Afficher résumé
sudo lynis show report

# Afficher seulement warnings
sudo lynis show warnings

# Afficher suggestions
sudo lynis show suggestions

# Afficher details test spécifique
sudo lynis show details SSH-7408
```

---

## Section 4 : Comprendre Résultats et Scoring

### 4.1 Anatomie Rapport lynis.log

**Structure fichier log :**

```bash
# Visualiser structure
sudo less /var/log/lynis.log

# Sections principales :
# 1. Header (metadata scan)
# 2. System Information (OS, kernel, hardware)
# 3. Test Results par catégorie
# 4. Warnings détaillés
# 5. Suggestions détaillées
# 6. Hardening index final
```

**Extraire informations spécifiques :**

```bash
# Score hardening
sudo grep "Hardening index" /var/log/lynis.log
# Output : Hardening index : 72 [###########         ]

# Liste warnings
sudo grep "Warning:" /var/log/lynis.log

# Liste suggestions
sudo grep "Suggestion:" /var/log/lynis.log

# Tests failed
sudo grep "\[ WARNING \]" /var/log/lynis.log

# Tests réussis
sudo grep "\[ OK \]" /var/log/lynis.log | wc -l
```

### 4.2 Parsing lynis-report.dat

**Format rapport data (key=value) :**

```bash
# Afficher rapport data
sudo cat /var/log/lynis-report.dat

# Exemples entrées :
# os=Linux
# os_name=Ubuntu
# os_version=22.04
# hardening_index=72
# warning[]=SSH-7408|PermitRootLogin enabled
# suggestion[]=FILE-6310|Configure file auditing
```

**Extraire données spécifiques :**

```bash
# Hardening index
grep "hardening_index=" /var/log/lynis-report.dat | cut -d= -f2
# Output : 72

# Liste warnings
grep "^warning\[\]=" /var/log/lynis-report.dat | cut -d= -f2

# Liste suggestions
grep "^suggestion\[\]=" /var/log/lynis-report.dat | cut -d= -f2

# OS détecté
grep "^os=" /var/log/lynis-report.dat | cut -d= -f2
```

### 4.3 Priorités Actions

**Classification warnings et suggestions :**

```
Priorité CRITIQUE (corriger immédiatement) :
├── SSH PermitRootLogin=yes
├── Firewall désactivé
├── SELinux/AppArmor disabled
├── Kernel non patché (vulnérabilités connues)
├── Services inutiles exposés réseau
└── Permissions SUID root sur binaries suspects

Priorité HAUTE (corriger sous 7 jours) :
├── Password authentication SSH activée
├── Weak SSH ciphers
├── Logs non rotationnés
├── Auditd non configuré
├── Packages obsolètes avec CVE
└── TLS certificates expirés

Priorité MOYENNE (corriger sous 30 jours) :
├── Mount options manquantes (nodev, nosuid)
├── Compiler installé (gcc, make)
├── USB storage non désactivé
├── Core dumps activés
├── Banner login manquant
└── File integrity monitoring absent

Priorité BASSE (amélioration continue) :
├── Duplicate UIDs/GIDs
├── Empty passwords fields
├── Inactive user accounts
├── Home directories permissions
└── Documentation sécurité
```

### 4.4 Mapping Conformité

**Lynis map tests vers standards :**

```bash
# Tests mappés PCI-DSS
sudo grep "PCI-DSS" /var/log/lynis.log

# Tests mappés ISO27001
sudo grep "ISO27001" /var/log/lynis.log

# Tests mappés CIS
sudo grep "CIS" /var/log/lynis.log

# Rapport conformité custom (exemple)
sudo lynis audit system --tests "AUTHENTICATION" --compliance PCI-DSS
```

**Exemples mapping :**

```
Test Lynis            Standard          Requirement
─────────────────────────────────────────────────────────────
SSH-7408 (PermitRoot) PCI-DSS 2.2.4     Disable root login
FILE-6310 (auditd)    PCI-DSS 10.2      Log security events
KRNL-6000 (sysctl)    CIS 3.2.1         Network hardening
AUTH-9262 (password)  ISO27001 A.9.4.3  Password policy
FIRE-4512 (firewall)  CIS 3.5.1         Firewall enabled
```

---

## Section 5 : Catégories Audit Détaillées

### 5.1 Boot and Services

**Tests effectués :**

```bash
# Bootloader (GRUB)
- GRUB password protection        # Empêche boot single-user non autorisé
- GRUB configuration permissions  # /boot/grub/grub.cfg should be 0600

# Init system
- Systemd vs SysVinit detected
- Service manager configuration
- Failed services detection

# Running services
- Liste services actifs
- Services inutiles détectés
- Services exposés réseau
```

**Hardening recommandé :**

```bash
# 1. Protéger GRUB par password
sudo grub-mkpasswd-pbkdf2
# Enter password: ********
# Output : grub.pbkdf2.sha512.10000.HASH...

# Éditer /etc/grub.d/40_custom
sudo nano /etc/grub.d/40_custom
# Ajouter :
set superusers="admin"
password_pbkdf2 admin grub.pbkdf2.sha512.10000.HASH...

# Regénérer config
sudo update-grub

# 2. Permissions GRUB config
sudo chmod 0600 /boot/grub/grub.cfg

# 3. Désactiver services inutiles
sudo systemctl disable avahi-daemon
sudo systemctl disable cups
sudo systemctl disable bluetooth
sudo systemctl stop avahi-daemon cups bluetooth

# 4. Lister services actifs
systemctl list-units --type=service --state=running

# Analyser chaque service :
# - Est-il nécessaire ?
# - Écoute-t-il réseau ? (netstat -tulpn)
# - Fonctionne-t-il root ? (ps aux | grep service)
```

### 5.2 Kernel Hardening

**Tests sysctl parameters :**

```bash
# Lynis vérifie >50 paramètres kernel
# Fichier référence : /etc/sysctl.conf

# IPv4 forwarding (doit être 0 si pas routeur)
net.ipv4.ip_forward = 0

# Protection SYN flood
net.ipv4.tcp_syncookies = 1

# Désactiver ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0

# Désactiver source routing
net.ipv4.conf.all.accept_source_route = 0

# Log martian packets
net.ipv4.conf.all.log_martians = 1

# Ignore ICMP broadcast
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Protection contre bad error messages
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Reverse path filtering
net.ipv4.conf.all.rp_filter = 1

# TCP/IP stack tuning
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_max_syn_backlog = 2048

# IPv6 (désactiver si non utilisé)
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1

# Kernel security
kernel.dmesg_restrict = 1                 # Restreindre dmesg non-root
kernel.kptr_restrict = 2                  # Masquer kernel pointers
kernel.yama.ptrace_scope = 1              # Restreindre ptrace
kernel.exec-shield = 1                    # ExecShield protection
kernel.randomize_va_space = 2             # ASLR complet

# Filesystem hardening
fs.suid_dumpable = 0                      # Pas de core dumps SUID
fs.protected_hardlinks = 1                # Protection hardlinks
fs.protected_symlinks = 1                 # Protection symlinks
```

**Appliquer hardening kernel :**

```bash
# Créer fichier sysctl custom
sudo nano /etc/sysctl.d/99-lynis-hardening.conf

# Copier tous paramètres ci-dessus
# Ou utiliser profil CIS :
curl -o /etc/sysctl.d/99-cis.conf https://raw.githubusercontent.com/konstruktoid/hardening/master/misc/sysctl.conf

# Appliquer immédiatement
sudo sysctl -p /etc/sysctl.d/99-lynis-hardening.conf

# Vérifier valeurs appliquées
sudo sysctl -a | grep net.ipv4.ip_forward
sudo sysctl -a | grep kernel.dmesg_restrict

# Reboot pour garantir persistence
sudo reboot
```

**Tests modules kernel :**

```bash
# Lynis vérifie modules chargés
lsmod

# Blacklist modules inutiles/dangereux
sudo nano /etc/modprobe.d/blacklist-lynis.conf

# Exemples modules à blacklister :
# Filesystems rares
install cramfs /bin/true
install freevxfs /bin/true
install jffs2 /bin/true
install hfs /bin/true
install hfsplus /bin/true
install udf /bin/true

# Protocols réseau obsolètes
install dccp /bin/true       # Datagram Congestion Control Protocol
install sctp /bin/true       # Stream Control Transmission Protocol
install rds /bin/true        # Reliable Datagram Sockets
install tipc /bin/true       # Transparent Inter Process Communication

# USB storage (serveurs)
install usb-storage /bin/true

# Firewire (DMA attacks)
install firewire-core /bin/true

# Mise à jour initramfs
sudo update-initramfs -u
```

### 5.3 Filesystem Security

**Tests permissions fichiers :**

```bash
# Lynis scan :
# - World-writable files
# - SUID/SGID binaries
# - Sticky bit directories
# - Mount options sécurisées

# Trouver world-writable files
sudo find / -xdev -type f -perm -0002 -ls 2>/dev/null

# Trouver SUID binaries
sudo find / -xdev -type f -perm -4000 -ls 2>/dev/null

# Trouver SGID binaries
sudo find / -xdev -type f -perm -2000 -ls 2>/dev/null

# Trouver directories sans sticky bit
sudo find / -xdev -type d -perm -0002 ! -perm -1000 -ls 2>/dev/null
```

**Hardening permissions :**

```bash
# 1. Permissions fichiers système critiques
sudo chmod 600 /etc/ssh/sshd_config          # SSH config
sudo chmod 644 /etc/passwd                   # Users list
sudo chmod 600 /etc/shadow                   # Passwords hash
sudo chmod 600 /etc/gshadow                  # Groups passwords
sudo chmod 644 /etc/group                    # Groups list
sudo chmod 600 /boot/grub/grub.cfg           # GRUB config
sudo chmod 600 /etc/crontab                  # Cron config
sudo chmod 700 /root                         # Root home
sudo chmod 700 /home/*                       # Users homes

# 2. Retirer SUID si non nécessaire (exemples)
sudo chmod u-s /usr/bin/at                   # At jobs
sudo chmod u-s /usr/bin/wall                 # Broadcast messages
# ATTENTION : NE PAS retirer SUID de sudo, su, passwd, ping

# 3. Mount options sécurisées (/etc/fstab)
sudo nano /etc/fstab

# Exemples :
# /tmp avec nodev, nosuid, noexec
tmpfs /tmp tmpfs defaults,nodev,nosuid,noexec 0 0

# /var/tmp similaire
tmpfs /var/tmp tmpfs defaults,nodev,nosuid,noexec 0 0

# /dev/shm limité
tmpfs /dev/shm tmpfs defaults,nodev,nosuid,noexec 0 0

# Partitions séparées avec restrictions
/dev/sda1 /home ext4 defaults,nodev,nosuid 0 2
/dev/sda2 /var ext4 defaults,nodev 0 2

# Appliquer sans reboot
sudo mount -o remount /tmp
sudo mount -o remount /var/tmp
sudo mount -o remount /dev/shm
```

### 5.4 Users and Authentication

**Tests comptes utilisateurs :**

```bash
# Lynis vérifie :
# - Comptes sans password
# - UIDs/GIDs duplicates
# - Comptes inactifs
# - Password policies
# - Sudo configuration

# 1. Trouver comptes sans password
sudo awk -F: '($2 == "") {print $1}' /etc/shadow

# 2. Trouver UIDs duplicates
sudo awk -F: '{print $3}' /etc/passwd | sort | uniq -d

# 3. Trouver GIDs duplicates
sudo awk -F: '{print $3}' /etc/group | sort | uniq -d

# 4. Lister users avec shell login
sudo awk -F: '$7 !~ /nologin|false/ {print $1}' /etc/passwd

# 5. Vérifier password policy
sudo cat /etc/login.defs | grep -E "PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_WARN_AGE"
```

**Hardening authentication :**

```bash
# 1. Password policy (/etc/login.defs)
sudo nano /etc/login.defs

# Recommandations :
PASS_MAX_DAYS   90      # Expiration password 90 jours
PASS_MIN_DAYS   7       # Minimum 7 jours avant changement
PASS_MIN_LEN    14      # Longueur minimum 14 caractères
PASS_WARN_AGE   14      # Avertir 14 jours avant expiration
UMASK           077     # Permissions par défaut restrictives

# 2. Password complexity (libpam-pwquality)
sudo apt install libpam-pwquality  # Debian/Ubuntu
sudo yum install libpwquality      # RHEL/CentOS

sudo nano /etc/security/pwquality.conf
# Configuration :
minlen = 14               # Longueur minimum
dcredit = -1              # Au moins 1 chiffre
ucredit = -1              # Au moins 1 majuscule
lcredit = -1              # Au moins 1 minuscule
ocredit = -1              # Au moins 1 caractère spécial
difok = 3                 # 3 caractères différents ancien password
maxrepeat = 2             # Max 2 caractères identiques consécutifs
usercheck = 1             # Pas de username dans password
enforcing = 1             # Enforcer policy

# 3. Account lockout après échecs login
sudo nano /etc/pam.d/common-auth  # Debian/Ubuntu
# OU
sudo nano /etc/pam.d/system-auth  # RHEL/CentOS

# Ajouter (avant pam_unix.so) :
auth required pam_faillock.so preauth silent audit deny=5 unlock_time=1800
auth required pam_faillock.so authfail audit deny=5 unlock_time=1800
# 5 tentatives, lock 30 minutes

# 4. Sudo hardening (/etc/sudoers)
sudo visudo

# Recommandations :
Defaults    timestamp_timeout=5        # Timeout sudo 5 min
Defaults    use_pty                    # Force PTY (prevent injection)
Defaults    logfile="/var/log/sudo.log"  # Log sudo commands
Defaults    log_input, log_output      # Log full I/O
Defaults    requiretty                 # Require TTY (prevent cron abuse)
Defaults    passwd_tries=3             # Max 3 password attempts

# 5. Désactiver comptes inutiles
sudo usermod -L -e 1970-01-02 <username>  # Lock + expire
sudo passwd -l <username>                 # Lock seulement

# 6. Retirer shells login comptes système
sudo usermod -s /sbin/nologin <username>
```

### 5.5 SSH Hardening

**Tests SSH Lynis :**

```bash
# Lynis vérifie /etc/ssh/sshd_config :
# - PermitRootLogin (doit être 'no')
# - PasswordAuthentication (préférer 'no', key-only)
# - Protocol (doit être 2 uniquement)
# - AllowUsers/DenyUsers (whitelist)
# - Ciphers (pas de weak ciphers)
# - MACs (secure MACs seulement)
# - LogLevel (VERBOSE pour audit)
```

**Configuration SSH sécurisée :**

```bash
# Backup config originale
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Éditer config
sudo nano /etc/ssh/sshd_config

# Configuration hardened complète :

# === Protocole et écoute ===
Protocol 2                              # SSH2 seulement (SSH1 obsolète)
Port 22                                 # Ou port custom (ex: 2222)
AddressFamily inet                      # IPv4 seulement (ou inet6 si IPv6)
ListenAddress 0.0.0.0                   # Ou IP spécifique

# === Authentication ===
PermitRootLogin no                      # JAMAIS root direct
PasswordAuthentication no               # Keys seulement (après setup)
PubkeyAuthentication yes                # Autoriser SSH keys
PermitEmptyPasswords no                 # Pas de passwords vides
ChallengeResponseAuthentication no      # Désactiver challenge-response
UsePAM yes                              # Utiliser PAM (password policy)

# === Login restrictions ===
AllowUsers deployer admin               # Whitelist users (ou AllowGroups)
DenyUsers root guest                    # Blacklist users
MaxAuthTries 3                          # Max 3 tentatives
MaxSessions 2                           # Max 2 sessions simultanées
LoginGraceTime 30                       # 30s pour s'authentifier

# === Cryptography ===
# Ciphers modernes seulement
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr

# MACs sécurisés
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256

# Key exchange algorithms
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512

# === Features ===
X11Forwarding no                        # Désactiver X11
AllowTcpForwarding no                   # Désactiver port forwarding (ou 'local')
AllowAgentForwarding no                 # Désactiver agent forwarding
PermitTunnel no                         # Désactiver tunneling
GatewayPorts no                         # Pas de gateway ports
PrintMotd no                            # Pas de MOTD (géré PAM)
PrintLastLog yes                        # Afficher last login
TCPKeepAlive yes                        # Keepalive connections
Compression no                          # Désactiver compression (CVE-2016-10012)

# === Logging ===
SyslogFacility AUTH                     # Log vers AUTH facility
LogLevel VERBOSE                        # Logs détaillés (audit)

# === Timeouts ===
ClientAliveInterval 300                 # Ping client every 5 min
ClientAliveCountMax 2                   # Disconnect après 2 pings ratés (10 min idle)

# === Misc ===
UseDNS no                               # Pas de reverse DNS lookup (plus rapide)
StrictModes yes                         # Vérifier permissions files
HostbasedAuthentication no              # Pas d'auth basée host
IgnoreRhosts yes                        # Ignorer .rhosts
Banner /etc/ssh/banner.txt              # Banner login

# Valider config et recharger
sudo sshd -t                            # Test config syntax
sudo systemctl restart sshd             # Appliquer changements
```

**Setup SSH keys (remplacer passwords) :**

```bash
# Sur client :
ssh-keygen -t ed25519 -C "user@hostname"
# Ou RSA 4096 bits :
ssh-keygen -t rsa -b 4096 -C "user@hostname"

# Copier clé publique vers serveur
ssh-copy-id user@server
# Ou manuellement :
cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Sur serveur, vérifier permissions
sudo chmod 700 ~/.ssh
sudo chmod 600 ~/.ssh/authorized_keys

# Tester connexion key
ssh user@server

# Une fois confirmé fonctionnel, désactiver passwords
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no
sudo systemctl restart sshd
```

### 5.6 Network Security

**Tests réseau Lynis :**

```bash
# Ports ouverts
sudo netstat -tulpn
sudo ss -tulpn

# Firewall status
sudo iptables -L -n -v
sudo ufw status verbose
sudo firewall-cmd --list-all

# Network interfaces
ip addr show
ip link show
```

**Hardening firewall (UFW - Ubuntu) :**

```bash
# Installer UFW
sudo apt install ufw

# Configuration default (deny all, allow SSH)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'SSH'

# Ou port SSH custom
sudo ufw allow 2222/tcp comment 'SSH custom port'

# Services autorisés (exemples)
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'
sudo ufw allow from 192.168.1.0/24 to any port 3306 comment 'MySQL LAN only'

# Rate limiting SSH (protection brute-force)
sudo ufw limit 22/tcp

# Activer firewall
sudo ufw enable

# Vérifier rules
sudo ufw status numbered

# Logs
sudo ufw logging on
sudo tail -f /var/log/ufw.log
```

**Hardening firewall (firewalld - RHEL/CentOS) :**

```bash
# Installer firewalld
sudo yum install firewalld
sudo systemctl enable firewalld
sudo systemctl start firewalld

# Configuration zones
sudo firewall-cmd --set-default-zone=public
sudo firewall-cmd --zone=public --list-all

# Services autorisés
sudo firewall-cmd --zone=public --add-service=ssh --permanent
sudo firewall-cmd --zone=public --add-service=http --permanent
sudo firewall-cmd --zone=public --add-service=https --permanent

# Ports custom
sudo firewall-cmd --zone=public --add-port=8080/tcp --permanent

# Rich rules (advanced)
sudo firewall-cmd --permanent --zone=public --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port protocol="tcp" port="3306" accept'

# Rate limiting SSH
sudo firewall-cmd --permanent --add-rich-rule='rule service name="ssh" limit value="3/m" accept'

# Reload config
sudo firewall-cmd --reload

# Vérifier
sudo firewall-cmd --list-all
```

---

## Section 6 : Hardening Basé Recommandations

### 6.1 Workflow Hardening Systématique

```bash
# 1. Baseline audit initial
sudo lynis audit system > /tmp/lynis-baseline.log
SCORE_INITIAL=$(sudo grep "Hardening index" /var/log/lynis.log | grep -oP '\d+')
echo "Score initial : $SCORE_INITIAL"

# 2. Extraire warnings priorité haute
sudo grep "Warning:" /var/log/lynis.log | grep -E "SSH|FIRE|KRNL" > /tmp/warnings-priority.txt

# 3. Extraire suggestions
sudo grep "Suggestion:" /var/log/lynis.log > /tmp/suggestions.txt

# 4. Créer plan action (prioriser)
# - Critique : SSH, Firewall, Kernel
# - Haute : Updates, Auditd, SELinux
# - Moyenne : Permissions, Services
# - Basse : Cosmétique, Documentation

# 5. Appliquer corrections une par une
# ... (voir sections précédentes)

# 6. Re-scan après chaque changement majeur
sudo lynis audit system

# 7. Comparer scores
SCORE_FINAL=$(sudo grep "Hardening index" /var/log/lynis.log | grep -oP '\d+')
echo "Score initial : $SCORE_INITIAL"
echo "Score final   : $SCORE_FINAL"
echo "Amélioration  : $((SCORE_FINAL - SCORE_INITIAL)) points"
```

### 6.2 Script Hardening Automatique

```bash
#!/bin/bash
# lynis-autofix.sh - Automatiser corrections basiques

set -e

echo "🔒 Lynis Auto-Hardening Script"
echo "================================"

# Check root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Ce script doit être exécuté en root"
   exit 1
fi

# Backup configs
echo "📦 Backup configurations..."
mkdir -p /root/lynis-backup-$(date +%Y%m%d)
cp /etc/ssh/sshd_config /root/lynis-backup-$(date +%Y%m%d)/
cp /etc/sysctl.conf /root/lynis-backup-$(date +%Y%m%d)/

# 1. SSH Hardening
echo "🔐 Hardening SSH..."
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#*X11Forwarding.*/X11Forwarding no/' /etc/ssh/sshd_config
sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 3/' /etc/ssh/sshd_config

# Valider et recharger SSH
sshd -t && systemctl reload sshd
echo "✅ SSH hardened"

# 2. Kernel Hardening (sysctl)
echo "⚙️  Hardening kernel parameters..."
cat > /etc/sysctl.d/99-lynis.conf << 'EOF'
# Network security
net.ipv4.ip_forward = 0
net.ipv4.tcp_syncookies = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.all.log_martians = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1
net.ipv4.conf.all.rp_filter = 1

# Kernel hardening
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 2
kernel.yama.ptrace_scope = 1
kernel.randomize_va_space = 2

# Filesystem
fs.suid_dumpable = 0
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
EOF

sysctl -p /etc/sysctl.d/99-lynis.conf
echo "✅ Kernel hardened"

# 3. Firewall
echo "🛡️  Enabling firewall..."
if command -v ufw &> /dev/null; then
    ufw --force enable
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow 22/tcp
    ufw limit 22/tcp
    echo "✅ UFW firewall enabled"
elif command -v firewall-cmd &> /dev/null; then
    systemctl enable --now firewalld
    firewall-cmd --set-default-zone=public
    firewall-cmd --zone=public --add-service=ssh --permanent
    firewall-cmd --reload
    echo "✅ Firewalld enabled"
else
    echo "⚠️  No firewall found (ufw/firewalld)"
fi

# 4. Permissions fichiers critiques
echo "🔒 Fixing file permissions..."
chmod 600 /etc/ssh/sshd_config
chmod 644 /etc/passwd
chmod 600 /etc/shadow
chmod 600 /etc/gshadow
chmod 644 /etc/group
chmod 700 /root

echo "✅ Permissions fixed"

# 5. Désactiver services inutiles
echo "🚫 Disabling unnecessary services..."
SERVICES_TO_DISABLE="avahi-daemon cups bluetooth"
for service in $SERVICES_TO_DISABLE; do
    if systemctl is-active --quiet $service 2>/dev/null; then
        systemctl stop $service
        systemctl disable $service
        echo "  - Disabled: $service"
    fi
done

# 6. Updates
echo "📦 Checking for updates..."
if command -v apt &> /dev/null; then
    apt update
    apt upgrade -y
elif command -v yum &> /dev/null; then
    yum update -y
fi

echo ""
echo "✅ Auto-hardening completed!"
echo "🔄 Reboot recommended to apply all changes"
echo "📊 Run 'lynis audit system' to verify improvements"
```

### 6.3 Hardening Par Type Serveur

**Web Server (Nginx/Apache) :**

```bash
# 1. Désactiver services non-web
sudo systemctl disable bluetooth avahi-daemon cups

# 2. Firewall strict (80, 443, 22 seulement)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable

# 3. SELinux/AppArmor enforcing
sudo aa-enforce /etc/apparmor.d/usr.sbin.nginx  # Ubuntu/Debian
sudo setenforce 1                                # RHEL/CentOS

# 4. Permissions web root
sudo chown -R www-data:www-data /var/www
sudo find /var/www -type d -exec chmod 755 {} \;
sudo find /var/www -type f -exec chmod 644 {} \;

# 5. Nginx hardening
sudo nano /etc/nginx/nginx.conf
# Ajouter :
server_tokens off;                    # Masquer version
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000" always;

# 6. Fail2ban (protection brute-force)
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

**Database Server (MySQL/PostgreSQL) :**

```bash
# 1. Firewall restrictif (DB port seulement depuis app servers)
sudo ufw allow from 192.168.1.0/24 to any port 3306  # MySQL
sudo ufw allow from 192.168.1.0/24 to any port 5432  # PostgreSQL

# 2. Bind localhost seulement (si app locale)
# MySQL :
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
bind-address = 127.0.0.1

# PostgreSQL :
sudo nano /etc/postgresql/*/main/postgresql.conf
listen_addresses = 'localhost'

# 3. Désactiver remote root
mysql -u root -p
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
FLUSH PRIVILEGES;

# 4. Permissions data directory
sudo chmod 700 /var/lib/mysql
sudo chown -R mysql:mysql /var/lib/mysql
```

**Container Host (Docker) :**

```bash
# 1. Docker daemon hardening
sudo nano /etc/docker/daemon.json
{
  "icc": false,                          # Disable inter-container communication
  "userns-remap": "default",             # User namespace isolation
  "live-restore": true,                  # Keep containers running on daemon crash
  "no-new-privileges": true,             # Disable privilege escalation
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}

# 2. AppArmor/SELinux pour containers
sudo aa-enforce /etc/apparmor.d/docker

# 3. Scan images vulnérabilités
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image nginx:latest

# 4. Lynis scan Docker host
sudo lynis audit system --tests CONTAINERS
```

---

## Section 7 : Configuration Avancée Lynis

### 7.1 Profils Custom

**Créer profil personnalisé :**

```bash
# Copier profil default
sudo cp /etc/lynis/default.prf /etc/lynis/custom.prf

# Éditer profil
sudo nano /etc/lynis/custom.prf

# Exemples customisations :

# Skip tests non pertinents
skip-test=FILE-6310    # Skip auditd (si non requis)
skip-test=KRNL-5830    # Skip kernel update check (managed externally)

# Custom paths
config:ssh_daemon_config:/etc/ssh/sshd_config

# Custom thresholds
config:minimum_password_length:14
config:password_max_days:90

# Logging
config:log_tests_incorrect_os:1
config:show_warnings_only:0

# Plugins
plugin:compliance
plugin:software

# Compliance frameworks
compliance:pci-dss
compliance:iso27001

# Scanner sa propre machine uniquement (pas remote)
config:allow_remote_scanning:0
```

**Utiliser profil custom :**

```bash
# Scan avec profil custom
sudo lynis audit system --profile /etc/lynis/custom.prf

# Définir profil par défaut
sudo ln -sf /etc/lynis/custom.prf /etc/lynis/default.prf
```

### 7.2 Tests Custom

**Créer tests personnalisés :**

```bash
# Créer fichier test custom
sudo nano /etc/lynis/include.d/custom-tests

# Exemple test : vérifier Nginx installé
#
# Test ID : CUST-0001
# Description : Check if Nginx is installed
#
Register --test-no CUST-0001 --weight L --network NO --description "Check for Nginx installation"
if [ ${SKIPTEST} -eq 0 ]; then
    if [ -f /usr/sbin/nginx ]; then
        LogText "Result: Nginx is installed"
        Display --indent 2 --text "- Checking Nginx installation" --result "FOUND" --color GREEN
    else
        LogText "Result: Nginx is not installed"
        Display --indent 2 --text "- Checking Nginx installation" --result "NOT FOUND" --color RED
        ReportWarning ${TEST_NO} "Nginx is not installed"
        ReportSuggestion ${TEST_NO} "Install Nginx web server"
    fi
fi

# Exemple test : vérifier backup cron
#
# Test ID : CUST-0002
# Description : Check if backup cron job exists
#
Register --test-no CUST-0002 --weight L --network NO --description "Check backup cron job"
if [ ${SKIPTEST} -eq 0 ]; then
    if crontab -l | grep -q "backup.sh"; then
        LogText "Result: Backup cron job found"
        Display --indent 2 --text "- Checking backup cron job" --result "FOUND" --color GREEN
    else
        LogText "Result: Backup cron job not found"
        Display --indent 2 --text "- Checking backup cron job" --result "NOT FOUND" --color YELLOW
        ReportSuggestion ${TEST_NO} "Configure automated backups with cron"
    fi
fi
```

**Activer tests custom :**

```bash
# Inclure dans profil
sudo nano /etc/lynis/custom.prf

# Ajouter :
include=/etc/lynis/include.d/custom-tests

# Run scan
sudo lynis audit system --profile /etc/lynis/custom.prf
```

### 7.3 Output Formats

**JSON Output (CI/CD) :**

```bash
# Générer rapport JSON
sudo lynis audit system --report-file /tmp/lynis-report.json

# Parser JSON avec jq
sudo jq '.hardening_index' /tmp/lynis-report.json
sudo jq '.warnings[]' /tmp/lynis-report.json
sudo jq '.suggestions[]' /tmp/lynis-report.json
```

**CSV Export :**

```bash
# Extraire data report vers CSV
sudo awk -F'=' '/^warning\[\]=/ {print $2}' /var/log/lynis-report.dat > /tmp/warnings.csv

# Format CSV custom
sudo cat > /tmp/lynis-export.sh << 'EOF'
#!/bin/bash
REPORT=/var/log/lynis-report.dat
OUTPUT=/tmp/lynis-report.csv

echo "Test ID,Status,Description" > $OUTPUT

grep "^warning\[\]=" $REPORT | cut -d= -f2 | while read line; do
    TEST_ID=$(echo $line | cut -d'|' -f1)
    DESC=$(echo $line | cut -d'|' -f2)
    echo "$TEST_ID,WARNING,$DESC" >> $OUTPUT
done

grep "^suggestion\[\]=" $REPORT | cut -d= -f2 | while read line; do
    TEST_ID=$(echo $line | cut -d'|' -f1)
    DESC=$(echo $line | cut -d'|' -f2)
    echo "$TEST_ID,SUGGESTION,$DESC" >> $OUTPUT
done

echo "CSV exported to $OUTPUT"
EOF

chmod +x /tmp/lynis-export.sh
sudo /tmp/lynis-export.sh
```

---

## Section 8 : Automatisation et CI/CD

### 8.1 Cron Job Automatique

```bash
# Créer script scan quotidien
sudo nano /usr/local/bin/lynis-daily.sh

#!/bin/bash
# Lynis daily scan

DATE=$(date +%Y%m%d)
LOGDIR=/var/log/lynis
REPORT_FILE=$LOGDIR/lynis-report-$DATE.log
SCORE_FILE=$LOGDIR/lynis-scores.csv

# Créer directory logs
mkdir -p $LOGDIR

# Run scan
lynis audit system --quick --no-colors > $REPORT_FILE 2>&1

# Extraire score
SCORE=$(grep "Hardening index" $REPORT_FILE | grep -oP '\d+')

# Sauvegarder score avec date
echo "$DATE,$SCORE" >> $SCORE_FILE

# Envoyer alerte si score baisse
YESTERDAY_SCORE=$(tail -2 $SCORE_FILE | head -1 | cut -d',' -f2)
if [ $SCORE -lt $YESTERDAY_SCORE ]; then
    echo "⚠️ Lynis score decreased: $YESTERDAY_SCORE → $SCORE" | \
        mail -s "Lynis Score Alert" admin@example.com
fi

# Cleanup old logs (garder 30 jours)
find $LOGDIR -name "lynis-report-*.log" -mtime +30 -delete

# Permissions exécution
sudo chmod +x /usr/local/bin/lynis-daily.sh

# Ajouter cron job (tous les jours 2h du matin)
sudo crontab -e
0 2 * * * /usr/local/bin/lynis-daily.sh
```

### 8.2 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/lynis-security-audit.yml

name: Lynis Security Audit

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  security-audit:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Install Lynis
        run: |
          sudo apt-get update
          sudo apt-get install -y lynis
      
      - name: Run Lynis audit
        run: |
          sudo lynis audit system --quick --no-colors > lynis-report.log
        continue-on-error: true
      
      - name: Extract hardening index
        id: score
        run: |
          SCORE=$(grep "Hardening index" lynis-report.log | grep -oP '\d+')
          echo "score=$SCORE" >> $GITHUB_OUTPUT
          echo "Hardening Index: $SCORE"
      
      - name: Check score threshold
        run: |
          THRESHOLD=70
          SCORE=${{ steps.score.outputs.score }}
          if [ $SCORE -lt $THRESHOLD ]; then
            echo "❌ Security score $SCORE is below threshold $THRESHOLD"
            exit 1
          else
            echo "✅ Security score $SCORE meets threshold"
          fi
      
      - name: Upload Lynis report
        uses: actions/upload-artifact@v3
        with:
          name: lynis-report
          path: |
            lynis-report.log
            /var/log/lynis.log
            /var/log/lynis-report.dat
      
      - name: Comment PR with score
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const score = '${{ steps.score.outputs.score }}';
            const body = `## 🔒 Lynis Security Audit
            
            **Hardening Index:** ${score}/100
            
            ${score >= 85 ? '✅ Excellent' : score >= 70 ? '🟡 Good' : '⚠️ Needs improvement'}
            
            [View full report in artifacts](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }})`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

### 8.3 Docker Image Scanning

```dockerfile
# Dockerfile.lynis-scanner
FROM debian:12-slim

RUN apt-get update && \
    apt-get install -y \
    lynis \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

```bash
# entrypoint.sh
#!/bin/bash

# Run Lynis audit
lynis audit system --quick --no-colors

# Extract score
SCORE=$(grep "Hardening index" /var/log/lynis.log | grep -oP '\d+')
echo "Hardening Index: $SCORE"

# Exit with code based on score
if [ $SCORE -lt 70 ]; then
    exit 1  # Fail CI
else
    exit 0  # Pass CI
fi
```

**Build et usage :**

```bash
# Build image
docker build -t lynis-scanner -f Dockerfile.lynis-scanner .

# Scan container
docker run --rm \
  -v /:/host:ro \
  lynis-scanner

# Intégrer dans pipeline
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  lynis-scanner
```

### 8.4 Ansible Playbook

```yaml
# lynis-audit.yml
---
- name: Lynis Security Audit
  hosts: all
  become: yes
  
  tasks:
    - name: Install Lynis
      apt:
        name: lynis
        state: present
        update_cache: yes
      when: ansible_os_family == "Debian"
    
    - name: Install Lynis (RHEL)
      yum:
        name: lynis
        state: present
      when: ansible_os_family == "RedHat"
    
    - name: Run Lynis audit
      command: lynis audit system --quick --no-colors
      register: lynis_output
      changed_when: false
    
    - name: Extract hardening index
      shell: "grep 'Hardening index' /var/log/lynis.log | grep -oP '\\d+'"
      register: hardening_score
      changed_when: false
    
    - name: Display score
      debug:
        msg: "Hardening Index: {{ hardening_score.stdout }}"
    
    - name: Fetch Lynis reports
      fetch:
        src: /var/log/lynis.log
        dest: "./reports/{{ inventory_hostname }}-lynis.log"
        flat: yes
    
    - name: Fail if score below threshold
      fail:
        msg: "Security score {{ hardening_score.stdout }} is below threshold 70"
      when: hardening_score.stdout|int < 70
```

**Exécuter playbook :**

```bash
# Single host
ansible-playbook -i inventory.ini lynis-audit.yml

# All hosts
ansible-playbook -i inventory.ini lynis-audit.yml --limit all

# Avec variables
ansible-playbook lynis-audit.yml -e "threshold=75"
```

---

## Section 9 : Comparaison Avant/Après

### 9.1 Tracking Score Evolution

```bash
# Script tracking historique scores
sudo nano /usr/local/bin/lynis-score-tracker.sh

#!/bin/bash
# Track Lynis scores over time

SCORE_FILE=/var/log/lynis-scores.csv
GRAPH_FILE=/var/www/html/lynis-score-graph.html

# Initialiser CSV si absent
if [ ! -f $SCORE_FILE ]; then
    echo "Date,Score" > $SCORE_FILE
fi

# Run scan et extraire score
lynis audit system --quick > /dev/null 2>&1
SCORE=$(grep "Hardening index" /var/log/lynis.log | grep -oP '\d+')
DATE=$(date +%Y-%m-%d)

# Ajouter au CSV
echo "$DATE,$SCORE" >> $SCORE_FILE

# Générer graph HTML (Chart.js)
cat > $GRAPH_FILE << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Lynis Score Evolution</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Lynis Hardening Index Evolution</h1>
    <canvas id="scoreChart" width="800" height="400"></canvas>
    <script>
        // Load CSV data
        fetch('/lynis-scores.csv')
            .then(response => response.text())
            .then(data => {
                const lines = data.split('\n').slice(1);
                const dates = [];
                const scores = [];
                
                lines.forEach(line => {
                    const [date, score] = line.split(',');
                    if (date && score) {
                        dates.push(date);
                        scores.push(parseInt(score));
                    }
                });
                
                const ctx = document.getElementById('scoreChart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: dates,
                        datasets: [{
                            label: 'Hardening Index',
                            data: scores,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: false,
                                min: 0,
                                max: 100
                            }
                        }
                    }
                });
            });
    </script>
</body>
</html>
EOF

echo "Score tracked: $SCORE on $DATE"
```

### 9.2 Diff Reports

```bash
# Comparer deux rapports Lynis
sudo nano /usr/local/bin/lynis-diff.sh

#!/bin/bash
# Compare two Lynis reports

REPORT1=$1
REPORT2=$2

if [ ! -f "$REPORT1" ] || [ ! -f "$REPORT2" ]; then
    echo "Usage: $0 <report1> <report2>"
    exit 1
fi

echo "=== Lynis Reports Comparison ==="
echo ""

# Scores
SCORE1=$(grep "Hardening index" $REPORT1 | grep -oP '\d+')
SCORE2=$(grep "Hardening index" $REPORT2 | grep -oP '\d+')
DIFF=$((SCORE2 - SCORE1))

echo "Score Evolution:"
echo "  Before: $SCORE1"
echo "  After:  $SCORE2"
echo "  Diff:   $DIFF ($( [ $DIFF -gt 0 ] && echo '+' )$DIFF points)"
echo ""

# Warnings comparison
WARNINGS1=$(grep -c "Warning" $REPORT1)
WARNINGS2=$(grep -c "Warning" $REPORT2)
WARNINGS_DIFF=$((WARNINGS2 - WARNINGS1))

echo "Warnings:"
echo "  Before: $WARNINGS1"
echo "  After:  $WARNINGS2"
echo "  Diff:   $WARNINGS_DIFF"
echo ""

# New warnings
echo "=== New Warnings ==="
comm -13 <(grep "Warning:" $REPORT1 | sort) <(grep "Warning:" $REPORT2 | sort)
echo ""

# Resolved warnings
echo "=== Resolved Warnings ==="
comm -23 <(grep "Warning:" $REPORT1 | sort) <(grep "Warning:" $REPORT2 | sort)
```

**Usage :**

```bash
# Sauvegarder baseline
sudo lynis audit system > /tmp/lynis-baseline.log

# Appliquer hardening...
# (voir sections précédentes)

# Nouveau scan
sudo lynis audit system > /tmp/lynis-after.log

# Comparer
sudo /usr/local/bin/lynis-diff.sh /tmp/lynis-baseline.log /tmp/lynis-after.log
```

---

## Section 10 : Cas Pratiques par Type Serveur

### 10.1 Web Server LAMP Stack

**Checklist hardening LAMP :**

```bash
# 1. Base OS hardening
sudo lynis audit system --tests BOOT,KERNEL,AUTH,FIRE

# 2. Apache hardening
# Masquer version
sudo nano /etc/apache2/conf-available/security.conf
ServerTokens Prod
ServerSignature Off

# Activer modules sécurité
sudo a2enmod headers
sudo a2enmod ssl

# Headers sécurité
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"

# 3. PHP hardening
sudo nano /etc/php/8.1/apache2/php.ini
expose_php = Off
display_errors = Off
log_errors = On
allow_url_fopen = Off
allow_url_include = Off
disable_functions = exec,passthru,shell_exec,system,proc_open,popen

# 4. MySQL hardening
sudo mysql_secure_installation
# - Remove anonymous users
# - Disallow root login remotely
# - Remove test database

# 5. Mod_security (WAF)
sudo apt install libapache2-mod-security2
sudo a2enmod security2
sudo systemctl restart apache2

# 6. Fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban

# 7. Re-scan
sudo lynis audit system
```

### 10.2 Database Server Dédié

```bash
# 1. Network isolation
sudo ufw default deny incoming
sudo ufw allow from 192.168.1.0/24 to any port 3306  # MySQL
sudo ufw allow from 192.168.1.0/24 to any port 22    # SSH
sudo ufw enable

# 2. MySQL bind address
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
bind-address = 192.168.1.10  # IP interne

# 3. Désactiver services non-DB
sudo systemctl disable apache2 nginx
sudo apt remove --purge apache2 nginx

# 4. Audit logging MySQL
log_error = /var/log/mysql/error.log
log_slow_queries = /var/log/mysql/slow.log
long_query_time = 2

# 5. Automated backups
sudo nano /usr/local/bin/mysql-backup.sh
#!/bin/bash
mysqldump --all-databases --single-transaction | \
    gzip > /backup/mysql-$(date +\%Y\%m\%d).sql.gz
find /backup -name "mysql-*.sql.gz" -mtime +30 -delete

sudo chmod +x /usr/local/bin/mysql-backup.sh
sudo crontab -e
0 2 * * * /usr/local/bin/mysql-backup.sh

# 6. Lynis scan
sudo lynis audit system --tests DATABASES
```

### 10.3 Container Host Kubernetes

```bash
# 1. CIS Kubernetes Benchmark
sudo lynis audit system --tests CONTAINERS

# 2. Kernel hardening containers
sudo nano /etc/sysctl.d/99-kubernetes.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
kernel.panic = 10
kernel.panic_on_oops = 1
vm.overcommit_memory = 1
vm.panic_on_oom = 0

# 3. AppArmor profiles
sudo aa-enforce /etc/apparmor.d/docker
sudo aa-enforce /etc/apparmor.d/containerd

# 4. Audit logging
sudo apt install auditd
sudo systemctl enable auditd

# Rules audit Docker/K8s
sudo nano /etc/audit/rules.d/docker.rules
-w /usr/bin/docker -k docker
-w /var/lib/docker -k docker
-w /etc/docker -k docker
-w /usr/bin/containerd -k containerd
-w /usr/bin/runc -k runc

sudo systemctl restart auditd

# 5. Scan images
trivy image nginx:latest

# 6. Network policies K8s
kubectl apply -f network-policy-deny-all.yaml
```

---

## Section 11 : Plugins et Extensions

### 11.1 Plugins Officiels

```bash
# Lister plugins disponibles
lynis show plugins

# Activer plugin compliance
sudo nano /etc/lynis/custom.prf
plugin:compliance

# Activer plugin software
plugin:software

# Plugin container_security (Docker/K8s)
plugin:container_security
```

### 11.2 Plugin Custom Exemple

```bash
# Créer plugin custom
sudo nano /etc/lynis/plugins/plugin_custom_audit

#!/bin/bash
#
# Plugin : Custom Security Audit
# Description : Vérifie configurations custom entreprise
#

# Function appelée par Lynis
plugin_custom_audit_init() {
    PLUGIN_NAME="Custom Audit"
    PLUGIN_VERSION="1.0"
    PLUGIN_AUTHOR="Security Team"
    PLUGIN_DESCRIPTION="Custom security checks"
}

plugin_custom_audit_tests() {
    
    # Test 1 : Vérifier backup script existe
    if [ -f /usr/local/bin/backup.sh ]; then
        LogText "OK: Backup script found"
        AddHP 2 2
    else
        LogText "WARNING: Backup script not found"
        ReportWarning "CUST-BACKUP-001" "Backup script missing"
        AddHP 0 2
    fi
    
    # Test 2 : Vérifier monitoring agent
    if systemctl is-active --quiet prometheus-node-exporter; then
        LogText "OK: Monitoring agent running"
        AddHP 2 2
    else
        LogText "WARNING: Monitoring agent not running"
        ReportWarning "CUST-MONITOR-001" "Install monitoring agent"
        AddHP 0 2
    fi
    
    # Test 3 : Vérifier compliance banner
    if [ -f /etc/motd ] && grep -q "Authorized access only" /etc/motd; then
        LogText "OK: Compliance banner present"
        AddHP 1 1
    else
        LogText "SUGGESTION: Add compliance banner"
        ReportSuggestion "CUST-BANNER-001" "Add compliance banner to /etc/motd"
        AddHP 0 1
    fi
}

# Rendre exécutable
sudo chmod +x /etc/lynis/plugins/plugin_custom_audit

# Activer dans profil
sudo nano /etc/lynis/custom.prf
plugin:custom_audit

# Run scan
sudo lynis audit system --profile /etc/lynis/custom.prf
```

---

## Section 12 : Best Practices Production

### 12.1 Routine Maintenance

```bash
# Quotidien :
- Scan Lynis automatique (cron 2AM)
- Review warnings critiques
- Update packages

# Hebdomadaire :
- Analyse tendance scores
- Review logs audit
- Backup vérification

# Mensuel :
- Full audit manuel
- Update Lynis version
- Review conformité compliance

# Trimestriel :
- Pentest externe
- Review policies sécurité
- Formation équipe
```

### 12.2 Documentation

```bash
# Documenter baseline sécurité
sudo lynis audit system > /docs/security-baseline-$(date +%Y%m%d).log

# Créer runbook hardening
cat > /docs/hardening-runbook.md << 'EOF'
# Security Hardening Runbook

## Baseline Configuration

- OS: Ubuntu 22.04 LTS
- Kernel: 5.15.x
- Initial Score: 58/100
- Target Score: 85/100

## Applied Hardenings

1. SSH (Score: +8)
   - PermitRootLogin no
   - PasswordAuthentication no
   - Key-only authentication

2. Firewall (Score: +5)
   - UFW enabled
   - Default deny incoming
   - Whitelist ports: 22,80,443

3. Kernel (Score: +10)
   - Sysctl hardening applied
   - Modules blacklisted
   - SELinux enforcing

## Compliance Mapping

- PCI-DSS: 95% compliant
- ISO27001: 90% compliant
- CIS Benchmark: Level 1 achieved

## Monitoring

- Lynis daily scans: Enabled
- Alerts threshold: Score < 80
- Log retention: 90 days
EOF
```

### 12.3 Checklist Complète Production

```markdown
## Pre-Production Checklist

### Base OS
- [ ] OS version supportée (pas EOL)
- [ ] Kernel patches à jour
- [ ] Packages système à jour
- [ ] SELinux/AppArmor enabled
- [ ] Firewall activé et configuré

### Authentication
- [ ] Root login SSH désactivé
- [ ] Password authentication SSH désactivée
- [ ] Key-only authentication configurée
- [ ] Sudo logging activé
- [ ] Password policy configurée (14+ chars, complexity)
- [ ] Account lockout configuré (5 tentatives)

### Network
- [ ] Ports inutiles fermés
- [ ] Services non-essentiels désactivés
- [ ] Kernel network hardening (sysctl)
- [ ] Firewall rules validées
- [ ] Rate limiting configuré
- [ ] Fail2ban installé

### Filesystem
- [ ] Mount options sécurisées (nodev,nosuid,noexec)
- [ ] Permissions fichiers critiques vérifiées
- [ ] SUID/SGID binaries reviewed
- [ ] World-writable files corrigés
- [ ] Partitions séparées (/tmp, /var, /home)

### Logging & Monitoring
- [ ] Rsyslog configuré
- [ ] Auditd enabled
- [ ] Log rotation configurée
- [ ] Remote logging configuré
- [ ] Monitoring agent installé
- [ ] Alerting configuré

### Backup & Recovery
- [ ] Automated backups configurés
- [ ] Backup testing réalisé
- [ ] Recovery procedure documentée
- [ ] Backup retention policy définie

### Compliance
- [ ] Security banner présent
- [ ] Audit trail enabled
- [ ] Compliance frameworks mappés
- [ ] Documentation sécurité complète

### Lynis Audit
- [ ] Lynis scan passé (score ≥ 85)
- [ ] Warnings critiques corrigés
- [ ] Automated scanning configuré
- [ ] Baseline documenté

### Final Validation
- [ ] Pentest interne réalisé
- [ ] Vulnerability scan passé
- [ ] Documentation approuvée
- [ ] Équipe formée
```

---

## Ressources et Références

**Documentation officielle :**
- Site web : https://cisofy.com/lynis/
- GitHub : https://github.com/CISOfy/lynis
- Documentation : https://cisofy.com/lynis/documentation/
- Controls : https://cisofy.com/lynis/controls/

**Standards sécurité :**
- CIS Benchmarks : https://www.cisecurity.org/cis-benchmarks/
- PCI-DSS : https://www.pcisecuritystandards.org/
- ISO27001 : https://www.iso.org/isoiec-27001-information-security.html
- NIST : https://www.nist.gov/cyberframework

**Communauté :**
- Forum : https://github.com/CISOfy/lynis/discussions
- Issues : https://github.com/CISOfy/lynis/issues
- Twitter : @CISOfy

---

## Conclusion

**Lynis = Outil ESSENTIEL hardening Linux production**

**Points clés :**

✅ **Audit automatisé** = 300+ checks en quelques minutes
✅ **Non-intrusif** = Lecture seule, safe production
✅ **Actionable** = Recommandations concrètes priorisées
✅ **Mesurable** = Score 0-100 comparable
✅ **Gratuit** = Open-source, aucune restriction

**Workflow recommandé :**

```bash
# 1. Baseline initial
sudo lynis audit system > /tmp/baseline.log
SCORE_INITIAL=$(grep "Hardening index" /var/log/lynis.log | grep -oP '\d+')

# 2. Appliquer hardening prioritaire
# - SSH (PermitRootLogin, key-only)
# - Firewall (UFW/firewalld)
# - Kernel (sysctl hardening)
# - Updates (packages à jour)

# 3. Re-scan et mesurer progrès
sudo lynis audit system
SCORE_FINAL=$(grep "Hardening index" /var/log/lynis.log | grep -oP '\d+')
echo "Amélioration : $((SCORE_FINAL - SCORE_INITIAL)) points"

# 4. Automatiser (cron daily)
sudo crontab -e
0 2 * * * /usr/local/bin/lynis-daily.sh

# 5. Monitoring continu
# - Alertes si score baisse
# - Review mensuelle recommendations
# - Update Lynis régulièrement
```

**Objectifs réalistes par environnement :**

```
Development   : 65-75% (hardening basique)
Staging       : 75-85% (production-like)
Production    : 85-95% (hardening complet)
PCI-DSS/HIPAA : 90-95% (compliance stricte)
```

**Tu maîtrises maintenant Lynis de l'audit initial au hardening production !** 🔒

---

**Guide Lynis Complet terminé !** 🎉

Voilà le guide complet Lynis ! Il couvre exhaustivement :

✅ **12 sections complètes** avec analogie pédagogique  
✅ Installation (packages, source, Docker)  
✅ Premier audit et interprétation résultats  
✅ Catégories audit détaillées (boot, kernel, filesystem, users, SSH, network)  
✅ Hardening systématique basé recommandations  
✅ Configuration avancée (profils, tests custom)  
✅ Automatisation CI/CD (GitHub Actions, Ansible, Docker)  
✅ Comparaison avant/après  
✅ Cas pratiques par type serveur (web, DB, containers)  
✅ Plugins et extensions  
✅ Best practices production avec checklist complète  
✅ Scripts commentés et prêts à l'emploi  

**Même rigueur que tes guides Livewire avec focus sécurité infrastructure Linux !** 🛡️