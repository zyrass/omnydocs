---
description: "Fail2ban : protection anti-intrusion, ban automatique IPs malveillantes, intégration firewall, monitoring"
icon: lucide/book-open-check
tags: ["FAIL2BAN", "SECURITY", "IPS", "BRUTE-FORCE", "LINUX", "FIREWALL"]
---

# Fail2ban

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-time="6-8 heures"
  data-version="1.2">
</div>

## Introduction à la Protection d'Intrusion

!!! quote "Analogie pédagogique"
    _Imaginez un **vigile intelligent immeuble avec mémoire photographique et réflexes ultra-rapides** : Fail2ban fonctionne comme **système défense automatisé analysant comportements suspects TEMPS RÉEL et bannissant intrus immédiatement**. **Vigile immeuble classique** : surveille entrées/sorties, note visiteurs louches (tentatives connexion échouées), après X comportements suspects (3 échecs password SSH), appelle sécurité (ban IP firewall), signale dans registre (logs), interdit accès temporairement ou définitivement. **Sans Fail2ban** : attaques brute-force SSH (10,000 tentatives/heure, password faibles crackés), bots scanning vulnérabilités (WordPress login spam), credential stuffing (listes passwords volés testés massivement), DDoS applicatif (flood requêtes), exploitation 0-days (scanning automatisé failles). **Avec Fail2ban** : **Surveillance continue logs** (auth.log, nginx access.log, apache error.log), **Détection patterns suspects** (regex matching failed password, 404 floods, SQL injection attempts), **Ban automatique rapide** (3 échecs → ban IP 10 minutes via iptables/UFW), **Escalade progressive** (récidive → ban permanent), **Notifications admins** (email/Slack alerts attaques détectées), **Whitelist IPs légitimes** (admins jamais bannis). **Architecture Fail2ban** : 1) **Log monitoring** (tail -f tous logs services), 2) **Filters** (regex patterns détection attaques spécifiques), 3) **Jails** (configurations service-specific : sshd, nginx, postfix), 4) **Actions** (commandes ban : iptables -I, ufw insert, sendmail alert), 5) **Database** (SQLite track IPs bannies, tentatives, timestamps). **Fail2ban = IPS (Intrusion Prevention System) léger** : Python pure (pas d'agent lourd), règles firewall dynamiques (ajoute/retire automatiquement), 100+ filtres pré-configurés (SSH, Apache, Nginx, Postfix, Dovecot, WordPress, etc.), extensible facilement (custom filters/actions), production-proven (millions serveurs). **Protection multicouches** : SSH (max 3 tentatives, ban 1h), web servers (404 scans, brute-force admin panels), mail servers (SMTP auth failures), databases (PostgreSQL auth), fail2ban lui-même (trop de commandes fail2ban-client). **Statistiques réelles production** : serveur SSH public sans Fail2ban = 50,000 tentatives brute-force/jour, avec Fail2ban = 98% attaques stoppées après 3 tentatives, bande passante économisée ~80%, charge CPU réduite (bots bannis arrêtent), logs moins pollués._

**Fail2ban en résumé :**

- ✅ **IPS automatisé** = Détection + ban automatique temps réel
- ✅ **Multi-services** = SSH, web, mail, FTP, databases, custom
- ✅ **Firewall agnostic** = iptables, UFW, firewalld, nftables, CSF
- ✅ **Léger** = Python, faible CPU/RAM, daemon efficace
- ✅ **Extensible** = Filtres regex custom, actions personnalisées
- ✅ **Notifications** = Email, Slack, webhooks, syslog
- ✅ **Persistent** = Database SQLite track bans, récidives
- ✅ **Production-ready** = Stable, fiable, millions installations

**Guide structure :**

1. Introduction et concepts IPS
2. Installation et configuration initiale
3. Jails (prisons) configuration
4. Filtres et regex patterns
5. Actions (ban/unban/notifications)
6. Intégration SSH avancée
7. Intégration web servers (Nginx/Apache)
8. Intégration mail servers (Postfix/Dovecot)
9. Monitoring et alertes
10. Whitelist et gestion IPs
11. Performance et tuning
12. Best practices production

---

## Section 1 : Introduction et Concepts

### 1.1 Qu'est-ce que Fail2ban ?

**Fail2ban = IPS (Intrusion Prevention System) monitoring logs + ban automatique**

```
Architecture Fail2ban :

┌─────────────────────────────────────────────────────────┐
│                   Services Logs                         │
│  /var/log/auth.log (SSH)                               │
│  /var/log/nginx/access.log (Web)                       │
│  /var/log/mail.log (Postfix)                           │
└─────────────────┬───────────────────────────────────────┘
                  │ tail -F (monitoring continu)
                  ↓
┌─────────────────────────────────────────────────────────┐
│              Fail2ban Daemon (fail2ban-server)         │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Jail: sshd   │  │ Jail: nginx  │  │ Jail: postfix│ │
│  │ Filter: sshd │  │ Filter: nginx│  │ Filter: smtp │ │
│  │ Action: ban  │  │ Action: ban  │  │ Action: ban  │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                  │                  │         │
│         └──────────────────┴──────────────────┘         │
│                           ↓                             │
│              ┌─────────────────────────┐                │
│              │ SQLite Database         │                │
│              │ /var/lib/fail2ban/*.db  │                │
│              │ Track bans, attempts    │                │
│              └─────────────────────────┘                │
└─────────────────┬───────────────────────────────────────┘
                  │ Execute actions
                  ↓
┌─────────────────────────────────────────────────────────┐
│                    Firewall                             │
│  iptables -I INPUT -s 203.0.113.50 -j DROP             │
│  ufw insert 1 deny from 203.0.113.50                   │
└─────────────────────────────────────────────────────────┘
```

**Composants principaux :**

```
fail2ban-server   # Daemon principal (monitoring logs)
fail2ban-client   # CLI interface (ban/unban/status)
fail2ban-regex    # Test tool (tester regex filters)

/etc/fail2ban/
├── fail2ban.conf      # Config daemon (ne PAS éditer)
├── fail2ban.local     # Overrides daemon config
├── jail.conf          # Jails par défaut (ne PAS éditer)
├── jail.local         # Overrides jails (ÉDITER ICI)
├── filter.d/          # Filtres regex (patterns détection)
│   ├── sshd.conf
│   ├── nginx-*.conf
│   └── ...
├── action.d/          # Actions (ban commands)
│   ├── iptables.conf
│   ├── ufw.conf
│   └── sendmail.conf
└── jail.d/            # Jails additionnels
    └── custom.local

/var/lib/fail2ban/     # Database persistence
/var/log/fail2ban.log  # Logs Fail2ban
```

### 1.2 Concepts Clés

**Jail (Prison) :**

```
Jail = Configuration protection service spécifique

Composants jail :
- Filter  : Quel pattern chercher logs (regex)
- Action  : Quoi faire si match (ban IP)
- Logpath : Où chercher (fichier log)
- Maxretry: Combien d'échecs avant ban (default 5)
- Findtime: Période analyse (default 10 min)
- Bantime : Durée ban (default 10 min)

Exemple jail SSH :
[sshd]
enabled  = true
port     = 22
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3
findtime = 600     # 10 minutes
bantime  = 3600    # 1 heure
```

**Filter (Filtre) :**

```
Filter = Regex pattern détection attaque

Exemple filter SSH (/etc/fail2ban/filter.d/sshd.conf) :

[Definition]
failregex = ^.*Failed password for .* from <HOST>.*$
            ^.*Invalid user .* from <HOST>.*$
            ^.*authentication failure.*rhost=<HOST>.*$

<HOST> = placeholder IP attaquant (remplacé automatiquement)

Log SSH :
Jan 16 14:30:45 server sshd[12345]: Failed password for root from 203.0.113.50 port 54321 ssh2

Regex match → IP 203.0.113.50 détectée
```

**Action :**

```
Action = Commande exécutée lors ban/unban

Exemple action iptables (/etc/fail2ban/action.d/iptables.conf) :

[Definition]
actionstart = iptables -N f2b-<name>
              iptables -I INPUT -j f2b-<name>

actionban   = iptables -I f2b-<name> -s <ip> -j DROP

actionunban = iptables -D f2b-<name> -s <ip> -j DROP

actionstop  = iptables -F f2b-<name>
              iptables -X f2b-<name>

<name> = jail name (ex: sshd)
<ip>   = IP à bannir
```

**Timeline attaque typique :**

```
14:30:00 - Attaquant tente connexion SSH → Failed
14:30:05 - Attaquant tente 2e fois → Failed
14:30:10 - Attaquant tente 3e fois → Failed
14:30:11 - Fail2ban détecte 3 échecs < 10 min
14:30:11 - Fail2ban exécute actionban
14:30:11 - iptables -I INPUT -s 203.0.113.50 -j DROP
14:30:11 - Attaquant BANNI (tous paquets droppés)
15:30:11 - Bantime expiré (1h après)
15:30:11 - Fail2ban exécute actionunban
15:30:11 - iptables -D INPUT -s 203.0.113.50 -j DROP
15:30:11 - IP débannée automatiquement
```

### 1.3 Fail2ban vs Alternatives

| Critère | Fail2ban | DenyHosts | SSHGuard | OSSEC |
|---------|----------|-----------|----------|-------|
| **Type** | IPS multi-services | SSH seulement | SSH/mail | HIDS complet |
| **Complexité** | Moyenne | Basse | Basse | Haute |
| **Extensible** | Très | Non | Peu | Très |
| **Performance** | Légère | Très légère | Légère | Moyenne-lourde |
| **Firewall** | Tous | hosts.deny | pf/iptables | Agents |
| **Active** | Oui (actif) | Non (abandonné) | Oui | Oui |
| **Use case** | Production multi-services | SSH basique | SSH/mail simple | Enterprise SIEM |

**Avantages Fail2ban :**

```
✅ Multi-services (SSH, web, mail, FTP, custom)
✅ Firewall agnostic (iptables, UFW, nftables, CSF)
✅ Extensible facilement (filters/actions custom)
✅ Notifications flexibles (email, Slack, webhooks)
✅ Database persistence (SQLite tracking)
✅ Récidive detection (ban permanent après X fois)
✅ Production-proven (stable, millions serveurs)
✅ Active développement (mises à jour régulières)
```

### 1.4 Use Cases Production

**Scénarios typiques :**

```
1. SSH brute-force protection
   → Ban après 3 échecs en 10 min

2. WordPress admin brute-force
   → Ban après 5 tentatives wp-login.php

3. Nginx 404 scanning
   → Ban après 20 requêtes 404 en 1 min

4. Postfix SMTP auth failures
   → Ban après 3 échecs auth SMTP

5. Apache mod_security triggers
   → Ban après détection SQL injection

6. FTP brute-force
   → Ban après 3 échecs login FTP

7. Dovecot IMAP auth failures
   → Ban après 5 échecs password

8. Custom app API abuse
   → Ban après 100 req/min même endpoint
```

---

## Section 2 : Installation et Configuration Initiale

### 2.1 Installation

**Debian/Ubuntu :**

```bash
# Update repos
sudo apt update

# Installer Fail2ban
sudo apt install fail2ban

# Vérifier version
fail2ban-client version
# Output : Fail2Ban v1.0.2

# Vérifier service
sudo systemctl status fail2ban

# Activer au boot
sudo systemctl enable fail2ban
```

**RHEL/CentOS/Rocky/Alma :**

```bash
# Installer EPEL
sudo yum install epel-release

# Installer Fail2ban
sudo yum install fail2ban fail2ban-systemd

# Start service
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

**Arch Linux :**

```bash
sudo pacman -S fail2ban

sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

### 2.2 Structure Configuration

**Fichiers configuration :**

```bash
# Vérifier structure
tree /etc/fail2ban

# NE JAMAIS éditer directement :
# - fail2ban.conf (config daemon)
# - jail.conf (jails par défaut)
# - filter.d/*.conf (filtres par défaut)
# - action.d/*.conf (actions par défaut)

# TOUJOURS éditer dans .local :
# - fail2ban.local (overrides daemon)
# - jail.local (overrides jails)
# - jail.d/*.local (jails custom)
# - filter.d/*.local (filtres custom)
# - action.d/*.local (actions custom)
```

### 2.3 Configuration Daemon (fail2ban.local)

```bash
# Créer config local (overrides defaults)
sudo nano /etc/fail2ban/fail2ban.local

# Configuration recommandée :

[Definition]
# Niveau logging (CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG)
loglevel = INFO

# Destination logs
logtarget = /var/log/fail2ban.log

# Rotation logs
logrotate = ROTATE

# Socket file (communication client/server)
socket = /var/run/fail2ban/fail2ban.sock

# PID file
pidfile = /var/run/fail2ban/fail2ban.pid

# Database persistence
dbfile = /var/lib/fail2ban/fail2ban.sqlite3
dbpurgeage = 86400  # Purge entrées >24h

# Sauvegarder et restart
sudo systemctl restart fail2ban
```

### 2.4 Configuration Jails Basique

```bash
# Créer jail.local (overrides jail.conf)
sudo nano /etc/fail2ban/jail.local

# Configuration production basique :

[DEFAULT]
# Ban settings globaux (tous jails sauf override)
bantime  = 3600       # Ban 1 heure (3600 secondes)
findtime = 600        # Fenêtre 10 minutes
maxretry = 3          # 3 tentatives max

# Whitelist IPs (jamais bannies)
ignoreip = 127.0.0.1/8 ::1
           192.168.1.0/24   # Réseau local
           203.0.113.10     # Admin IP

# Firewall backend (auto-détecté)
banaction = iptables-multiport
# Alternatives : ufw, firewalld, nftables

# Email notifications (optionnel)
destemail = admin@example.com
sender = fail2ban@example.com
mta = sendmail
action = %(action_mwl)s
# action_mw  : ban + email
# action_mwl : ban + email + logs

# === JAILS ===

# SSH protection
[sshd]
enabled  = true
port     = 22
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3
bantime  = 3600
findtime = 600

# HTTP Auth (Apache/Nginx basic auth)
[nginx-http-auth]
enabled  = true
port     = http,https
filter   = nginx-http-auth
logpath  = /var/log/nginx/error.log
maxretry = 5

# Sauvegarder
# NE PAS restart encore (vérifier config avant)
```

### 2.5 Vérification Configuration

```bash
# Tester configuration syntaxe
sudo fail2ban-client -t

# Output attendu :
# OK: configuration test is successful

# Si erreurs :
# ERROR: Invalid configuration
# Corriger avant restart

# Start/Restart Fail2ban
sudo systemctl restart fail2ban

# Vérifier status
sudo systemctl status fail2ban

# Vérifier jails actives
sudo fail2ban-client status

# Output :
# Status
# |- Number of jail:      2
# `- Jail list:   sshd, nginx-http-auth
```

---

## Section 3 : Jails Configuration Avancée

### 3.1 Anatomie Jail Complète

```bash
# Exemple jail SSH complet avec tous paramètres

[sshd]
# === Activation ===
enabled  = true

# === Network ===
port     = 22                    # Port(s) service (comma-separated)
protocol = tcp                   # tcp, udp, icmp, all
chain    = INPUT                 # iptables chain (INPUT, FORWARD)

# === Logs ===
logpath  = /var/log/auth.log     # Log file(s) à monitorer
backend  = auto                  # auto, pyinotify, gamin, polling, systemd
logencoding = auto               # utf-8, auto

# === Filter ===
filter   = sshd                  # Filter name (/etc/fail2ban/filter.d/sshd.conf)

# === Detection ===
maxretry = 3                     # Nombre max tentatives
findtime = 600                   # Fenêtre temps (secondes)
bantime  = 3600                  # Durée ban (secondes)

# Bantime incrémental (récidive)
bantime.increment = true
bantime.factor = 2               # Multiplicateur
bantime.maxtime = 86400          # Ban max 24h

# === Action ===
action   = iptables-multiport    # Action à exécuter
           sendmail-whois-lines  # Action secondaire (notification)

# === Options avancées ===
ignorecommand =                  # Commande check si ignorer IP
ignoreself = true                # Ne jamais bannir localhost
usedns = warn                    # DNS lookup (yes, warn, no)
```

### 3.2 Paramètres Temps (bantime/findtime)

```bash
# Durées en secondes
# Suffixes supportés : s (sec), m (min), h (hour), d (day), w (week)

# Exemples :
bantime  = 10m          # 10 minutes
bantime  = 1h           # 1 heure
bantime  = 1d           # 1 jour
bantime  = -1           # Ban permanent

findtime = 5m           # Fenêtre 5 minutes
findtime = 1h           # Fenêtre 1 heure

# Bantime incrémental (escalade récidives)
[sshd]
bantime = 1h
bantime.increment = true
bantime.factor = 2
bantime.maxtime = 1w

# Logique :
# 1ère offense : 1h ban
# 2ème offense : 2h ban (1h × 2)
# 3ème offense : 4h ban (2h × 2)
# 4ème offense : 8h ban (4h × 2)
# ...
# Max : 1 week ban
```

### 3.3 Actions Multiple (Ban + Notification)

```bash
# Syntaxe action multiple :
action = %(action_)s          # Ban seulement
         %(action_mw)s        # Ban + email notification
         %(action_mwl)s       # Ban + email + logs
         custom-action        # Action custom

# Exemple complet :
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

# Ban via iptables + notification email + Slack
action = iptables-multiport[name=sshd, port=22, protocol=tcp]
         sendmail-whois-lines[name=sshd, dest=admin@example.com]
         slack-notify[name=sshd]

# Variables disponibles actions :
# <ip>       : IP bannie
# <failures> : Nombre tentatives
# <time>     : Timestamp ban
# <matches>  : Lignes log matchées
```

### 3.4 Jails Conditionnels

```bash
# Activer jail selon condition (ex: service installé)

[nginx-http-auth]
enabled = auto  # Active SI logpath existe
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log

# Jail avec multiple logpaths
[apache-auth]
enabled = true
port = http,https
filter = apache-auth
logpath = /var/log/apache2/error.log
          /var/log/apache2/*error.log
          /var/log/httpd/error_log

# Jail backend spécifique
[sshd-systemd]
enabled = true
port = 22
filter = sshd
backend = systemd  # Utilise journald au lieu fichier log
```

### 3.5 Exemples Jails Services Courants

**SSH avancé :**

```bash
[sshd]
enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3
bantime  = 1h
findtime = 10m
bantime.increment = true
bantime.maxtime = 1w

[sshd-ddos]
enabled  = true
port     = ssh
filter   = sshd-ddos
logpath  = /var/log/auth.log
maxretry = 10
findtime = 1m
bantime  = 10m
```

**Nginx :**

```bash
[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
filter = nginx-noscript
logpath = /var/log/nginx/access.log

[nginx-badbots]
enabled = true
port = http,https
filter = nginx-badbots
logpath = /var/log/nginx/access.log
maxretry = 2

[nginx-noproxy]
enabled = true
port = http,https
filter = nginx-noproxy
logpath = /var/log/nginx/access.log

[nginx-limit-req]
enabled = true
port = http,https
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
```

**Apache :**

```bash
[apache-auth]
enabled = true
port = http,https
filter = apache-auth
logpath = /var/log/apache2/*error.log

[apache-badbots]
enabled = true
port = http,https
filter = apache-badbots
logpath = /var/log/apache2/*access.log
maxretry = 2

[apache-noscript]
enabled = true
port = http,https
filter = apache-noscript
logpath = /var/log/apache2/*error.log

[apache-overflows]
enabled = true
port = http,https
filter = apache-overflows
logpath = /var/log/apache2/*error.log
maxretry = 2

[apache-modsecurity]
enabled = true
port = http,https
filter = apache-modsecurity
logpath = /var/log/apache2/modsec_audit.log
maxretry = 2
```

**Postfix/Dovecot :**

```bash
[postfix]
enabled = true
port = smtp,465,587
filter = postfix
logpath = /var/log/mail.log

[postfix-sasl]
enabled = true
port = smtp,465,587,submission
filter = postfix-sasl
logpath = /var/log/mail.log

[dovecot]
enabled = true
port = pop3,pop3s,imap,imaps
filter = dovecot
logpath = /var/log/mail.log

[postfix-rbl]
enabled = true
port = smtp,465,587,submission
filter = postfix-rbl
logpath = /var/log/mail.log
maxretry = 1
```

---

## Section 4 : Filtres et Regex Patterns

### 4.1 Structure Filter

```bash
# Fichier filter : /etc/fail2ban/filter.d/sshd.conf

[INCLUDES]
# Inclure filtres communs
before = common.conf

[Definition]
# Préfixe standard logs (optionnel)
_daemon = sshd

# Regex failregex (OBLIGATOIRE)
failregex = ^%(__prefix_line)sFailed password for .* from <HOST>.*$
            ^%(__prefix_line)sInvalid user .* from <HOST>.*$
            ^%(__prefix_line)sAuthentication failure.*rhost=<HOST>.*$

# Regex ignoreregex (optionnel, prioritaire sur failregex)
ignoreregex =

# Exemple ligne log matchée :
# Jan 16 14:30:45 server sshd[12345]: Failed password for root from 203.0.113.50 port 54321 ssh2

# Placeholders :
# <HOST>          : IP attaquant (automatique)
# <F-CONTENT>     : Capture content arbitraire
# __prefix_line   : Timestamp + hostname standard
```

### 4.2 Regex Patterns Courants

**Pattern failed password :**

```bash
# SSH failed password
failregex = ^.*Failed password for .* from <HOST>.*$

# Pattern détaillé :
# ^               : Début ligne
# .*              : N'importe quoi (timestamp, etc.)
# Failed password : Texte littéral
# for .*          : Username (n'importe quel)
# from <HOST>     : IP source (capturée)
# .*$             : Reste ligne jusqu'à fin
```

**Pattern invalid user :**

```bash
# SSH invalid user
failregex = ^.*Invalid user .* from <HOST>.*$

# Matche :
# Jan 16 14:30:45 server sshd[12345]: Invalid user admin from 203.0.113.50 port 54321
```

**Pattern Nginx 404 :**

```bash
# Nginx 404 scanning
failregex = ^<HOST> -.*"(GET|POST|HEAD) .* HTTP.*" 404

# Matche :
# 203.0.113.50 - - [16/Jan/2024:14:30:45 +0000] "GET /admin.php HTTP/1.1" 404 162
```

**Pattern WordPress brute-force :**

```bash
# wp-login.php attempts
failregex = ^<HOST> -.*POST.*/wp-login\.php

# Matche :
# 203.0.113.50 - - [16/Jan/2024:14:30:45 +0000] "POST /wp-login.php HTTP/1.1" 200
```

### 4.3 Créer Filter Custom

**Exemple : Filter custom app (Node.js/Express) :**

```bash
# Application logs format :
# [2024-01-16 14:30:45] ERROR: Login failed for user admin from 203.0.113.50

# Créer filter custom
sudo nano /etc/fail2ban/filter.d/myapp.local

[Definition]
failregex = ^\[.*\] ERROR: Login failed .* from <HOST>$
ignoreregex =

# Jail correspondant
sudo nano /etc/fail2ban/jail.local

[myapp]
enabled = true
port = 3000
filter = myapp
logpath = /var/log/myapp/app.log
maxretry = 5
bantime = 1h
```

**Exemple : Filter API rate limiting :**

```bash
# API logs :
# 2024-01-16 14:30:45 | 203.0.113.50 | RATE_LIMIT | /api/search | 429

sudo nano /etc/fail2ban/filter.d/api-ratelimit.local

[Definition]
failregex = ^.* \| <HOST> \| RATE_LIMIT \|
ignoreregex =

# Jail
[api-ratelimit]
enabled = true
port = http,https
filter = api-ratelimit
logpath = /var/log/api/access.log
maxretry = 3
findtime = 60
bantime = 600
```

### 4.4 Tester Filters (fail2ban-regex)

```bash
# Syntaxe : fail2ban-regex <logfile> <filter>

# Test filter SSH
sudo fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf

# Output :
# Running tests
# =============
# 
# Use   failregex filter file : sshd, basedir: /etc/fail2ban
# Use         log file : /var/log/auth.log
# Use         encoding : UTF-8
# 
# Results
# =======
# 
# Failregex: 245 total
# |-  #) [# of hits] regular expression
# |   1) [123] ^.*Failed password for .* from <HOST>.*$
# |   2) [85] ^.*Invalid user .* from <HOST>.*$
# |   3) [37] ^.*authentication failure.*rhost=<HOST>.*$
# 
# Ignoreregex: 0 total
# 
# Date template hits:
# |- [# of hits] date format
# |  [245] {^LN-BEG}ExYear(?P<_sep>[-/.])Month(?P=_sep)Day(?:T|  ?)24hour:Minute:Second
# 
# Lines: 12453 lines, 0 ignored, 245 matched, 12208 missed

# Test filter custom avec ligne log directe
echo "Jan 16 14:30:45 server sshd[12345]: Failed password for root from 203.0.113.50" | \
    fail2ban-regex - /etc/fail2ban/filter.d/sshd.conf

# Test regex inline (sans fichier filter)
echo "203.0.113.50 - - [16/Jan/2024:14:30:45] GET /admin.php 404" | \
    fail2ban-regex - '^<HOST> -.*GET .* 404'

# Debug verbose
fail2ban-regex -v /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf
```

### 4.5 Filters Avancés (Conditions Multiples)

```bash
# Filter avec multiple conditions (mode="aggressive")

[Definition]
# Mode normal : 1 failregex match = +1 tentative
# Mode aggressive : multiple patterns = conditions ET

failregex = ^<HOST> .*POST /login.*
            ^<HOST> .*"status": 401

# Matche seulement SI les 2 lignes présentes pour même IP

# Exemple logs :
# 203.0.113.50 POST /login HTTP/1.1
# 203.0.113.50 Response: {"status": 401, "error": "Invalid credentials"}

# Utilité : Réduire false positives (scan bots vs vrais attaquants)
```

---

## Section 5 : Actions (Ban/Unban/Notifications)

### 5.1 Actions Firewall

**iptables (défaut) :**

```bash
# /etc/fail2ban/action.d/iptables-multiport.conf

[Definition]
# Start : créer chain Fail2ban
actionstart = iptables -N f2b-<name>
              iptables -A f2b-<name> -j RETURN
              iptables -I INPUT -p <protocol> -m multiport --dports <port> -j f2b-<name>

# Ban : ajouter règle drop IP
actionban = iptables -I f2b-<name> 1 -s <ip> -j DROP

# Unban : supprimer règle
actionunban = iptables -D f2b-<name> -s <ip> -j DROP

# Stop : supprimer chain
actionstop = iptables -D INPUT -p <protocol> -m multiport --dports <port> -j f2b-<name>
             iptables -F f2b-<name>
             iptables -X f2b-<name>

# Variables disponibles :
# <name>     : Jail name
# <ip>       : IP à bannir
# <port>     : Port(s)
# <protocol> : tcp, udp, etc.
```

**UFW :**

```bash
# /etc/fail2ban/action.d/ufw.conf

[Definition]
actionstart =
actionstop =
actioncheck =
actionban = ufw insert 1 deny from <ip> to any
actionunban = ufw delete deny from <ip> to any

# Usage dans jail :
[sshd]
enabled = true
banaction = ufw
port = 22
filter = sshd
logpath = /var/log/auth.log
```

**firewalld :**

```bash
# /etc/fail2ban/action.d/firewallcmd-ipset.conf

[Definition]
actionstart = firewall-cmd --direct --add-chain ipv4 filter f2b-<name>
              firewall-cmd --direct --add-rule ipv4 filter INPUT 0 -j f2b-<name>

actionban = firewall-cmd --ipset=f2b-<name> --add-entry=<ip>

actionunban = firewall-cmd --ipset=f2b-<name> --remove-entry=<ip>
```

**nftables :**

```bash
# /etc/fail2ban/action.d/nftables.conf

[Definition]
actionstart = nft add table inet f2b-<name>
              nft add chain inet f2b-<name> input { type filter hook input priority 0 \; }
              nft add set inet f2b-<name> addr-set-<name> { type ipv4_addr \; }
              nft add rule inet f2b-<name> input ip saddr @addr-set-<name> drop

actionban = nft add element inet f2b-<name> addr-set-<name> { <ip> }

actionunban = nft delete element inet f2b-<name> addr-set-<name> { <ip> }
```

### 5.2 Actions Notifications

**Email (sendmail) :**

```bash
# /etc/fail2ban/action.d/sendmail-whois-lines.conf

[Definition]
actionstart =
actionstop =
actioncheck =

actionban = printf "Subject: [Fail2Ban] <name>: banned <ip>
            From: <sender>
            To: <dest>
            
            Hi,
            
            The IP <ip> has just been banned by Fail2Ban after
            <failures> attempts against <name>.
            
            Here are more information about <ip>:
            
            `whois <ip>`
            
            Lines containing IP in logfile:
            `grep '<ip>' <logpath>`
            
            Regards,
            Fail2Ban" | /usr/sbin/sendmail -f <sender> <dest>

actionunban =

# Variables :
# <ip>       : IP bannie
# <failures> : Nombre tentatives
# <name>     : Jail name
# <logpath>  : Log file path
# <sender>   : Email sender
# <dest>     : Email destinataire
```

**Slack webhook :**

```bash
# Créer action Slack
sudo nano /etc/fail2ban/action.d/slack-notify.local

[Definition]
actionstart =
actionstop =
actioncheck =

actionban = curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"⚠️ *Fail2Ban Alert*\n*Jail:* <name>\n*IP:* <ip>\n*Failures:* <failures>\n*Time:* <time>"}' \
    <slack_webhook_url>

actionunban =

[Init]
slack_webhook_url = https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Usage jail :
[sshd]
enabled = true
action = iptables-multiport[name=sshd, port=22]
         slack-notify[name=sshd]
```

**Discord webhook :**

```bash
sudo nano /etc/fail2ban/action.d/discord-notify.local

[Definition]
actionban = curl -X POST -H 'Content-Type: application/json' \
    --data '{"username":"Fail2Ban","avatar_url":"https://example.com/fail2ban.png","embeds":[{"title":"🚨 IP Banned","color":15158332,"fields":[{"name":"Jail","value":"<name>","inline":true},{"name":"IP","value":"<ip>","inline":true},{"name":"Failures","value":"<failures>","inline":true}],"timestamp":"<time>"}]}' \
    <discord_webhook_url>

[Init]
discord_webhook_url = https://discord.com/api/webhooks/YOUR/WEBHOOK
```

**Telegram bot :**

```bash
sudo nano /etc/fail2ban/action.d/telegram-notify.local

[Definition]
actionban = curl -s -X POST "https://api.telegram.org/bot<bot_token>/sendMessage" \
    -d "chat_id=<chat_id>" \
    -d "text=🚨 Fail2Ban Alert%0AJail: <name>%0AIP: <ip>%0AFailures: <failures>"

[Init]
bot_token = YOUR_BOT_TOKEN
chat_id = YOUR_CHAT_ID
```

### 5.3 Actions Custom

**Script custom (log vers fichier spécial) :**

```bash
# Créer script ban
sudo nano /usr/local/bin/fail2ban-custom-ban.sh

#!/bin/bash
# Custom ban action

IP=$1
JAIL=$2
FAILURES=$3
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Log vers fichier custom
echo "$TIMESTAMP | BANNED | $JAIL | $IP | Attempts: $FAILURES" >> /var/log/fail2ban-custom.log

# Envoyer vers SIEM (exemple Splunk HEC)
curl -k -X POST https://splunk.example.com:8088/services/collector \
    -H "Authorization: Splunk YOUR_HEC_TOKEN" \
    -d "{\"event\":{\"action\":\"ban\",\"jail\":\"$JAIL\",\"ip\":\"$IP\",\"failures\":$FAILURES}}"

# Rendre exécutable
sudo chmod +x /usr/local/bin/fail2ban-custom-ban.sh

# Créer action Fail2ban
sudo nano /etc/fail2ban/action.d/custom-log.local

[Definition]
actionban = /usr/local/bin/fail2ban-custom-ban.sh <ip> <name> <failures>
actionunban =
```

### 5.4 Actions Combinées

```bash
# Jail avec multiples actions
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

# Ban + Email + Slack + Custom log
action = iptables-multiport[name=sshd, port=22, protocol=tcp]
         sendmail-whois-lines[name=sshd, dest=admin@example.com, sender=fail2ban@example.com]
         slack-notify[name=sshd]
         custom-log[name=sshd]
```

---

## Section 6 : Intégration SSH Avancée

### 6.1 Configuration SSH Complète

```bash
# /etc/fail2ban/jail.local

[sshd]
enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3
bantime  = 1h
findtime = 10m

# Bantime incrémental récidives
bantime.increment = true
bantime.factor = 2
bantime.maxtime = 1w

# Mode aggressive (plus patterns)
mode = aggressive

# Action avec notification
action = iptables-multiport[name=sshd, port=ssh, protocol=tcp]
         sendmail-whois-lines[name=sshd, dest=admin@example.com]

# SSH DDoS protection (trop connexions rapides)
[sshd-ddos]
enabled  = true
port     = ssh
filter   = sshd-ddos
logpath  = /var/log/auth.log
maxretry = 10
findtime = 1m
bantime  = 10m
```

### 6.2 Filter SSH Mode Aggressive

```bash
# Filter sshd mode aggressive détecte plus patterns

# Vérifier filter sshd
sudo cat /etc/fail2ban/filter.d/sshd.conf

[Definition]
# Mode normal
failregex = ^.*Failed password for .* from <HOST>.*$
            ^.*Invalid user .* from <HOST>.*$

# Mode aggressive (si mode=aggressive dans jail)
failregex = ^.*Failed password for .* from <HOST>.*$
            ^.*Invalid user .* from <HOST>.*$
            ^.*Connection closed by <HOST> \[preauth\]$
            ^.*Received disconnect from <HOST>.*\[preauth\]$
            ^.*maximum authentication attempts exceeded .* from <HOST>.*$
            ^.*User .* from <HOST> not allowed because not listed in AllowUsers$

# Mode aggressive détecte :
# - Failed passwords
# - Invalid users
# - Connexions fermées prématurément (scanning)
# - Disconnect rapides (bots)
# - Trop de tentatives
# - Users non autorisés
```

### 6.3 SSH Port Non-Standard

```bash
# Si SSH sur port custom (ex: 2222)

[sshd]
enabled = true
port = 2222  # Port custom
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

# Vérifier iptables rules générées
sudo iptables -L f2b-sshd -n -v
# Doit montrer port 2222, pas 22
```

### 6.4 Whitelist Admin IPs

```bash
# Dans [DEFAULT] section jail.local
[DEFAULT]
ignoreip = 127.0.0.1/8 ::1
           192.168.1.0/24        # LAN
           203.0.113.10          # Admin office
           198.51.100.0/24       # VPN subnet

# IPs ignorées JAMAIS bannies (même si tentatives échouées)

# Vérifier whitelist active
sudo fail2ban-client get sshd ignoreip
```

### 6.5 Monitoring SSH Bans

```bash
# Status jail SSH
sudo fail2ban-client status sshd

# Output :
# Status for the jail: sshd
# |- Filter
# |  |- Currently failed: 0
# |  |- Total failed:     245
# |  `- File list:        /var/log/auth.log
# `- Actions
#    |- Currently banned: 12
#    |- Total banned:     48
#    `- Banned IP list:   203.0.113.50 203.0.113.51 ...

# Liste IPs bannies
sudo fail2ban-client get sshd banip

# Statistiques
sudo fail2ban-client get sshd stats

# Unbanner IP manuellement
sudo fail2ban-client set sshd unbanip 203.0.113.50
```

---

## Section 7 : Intégration Web Servers

### 7.1 Nginx Jails Complets

```bash
# /etc/fail2ban/jail.local

# Nginx HTTP Auth (basic auth)
[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 5

# Nginx 404 Not Found (scanning)
[nginx-noscript]
enabled = true
port = http,https
filter = nginx-noscript
logpath = /var/log/nginx/access.log
maxretry = 6
findtime = 5m

# Nginx Bad Bots
[nginx-badbots]
enabled = true
port = http,https
filter = nginx-badbots
logpath = /var/log/nginx/access.log
maxretry = 2

# Nginx Proxy (open proxy attempts)
[nginx-noproxy]
enabled = true
port = http,https
filter = nginx-noproxy
logpath = /var/log/nginx/access.log
maxretry = 2

# Nginx Limit Req (rate limiting)
[nginx-limit-req]
enabled = true
port = http,https
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
maxretry = 10
findtime = 1m

# Nginx Botsearch (search for exploits)
[nginx-botsearch]
enabled = true
port = http,https
filter = nginx-botsearch
logpath = /var/log/nginx/access.log
maxretry = 2
```

### 7.2 Filters Nginx Custom

**Filter 404 scanning :**

```bash
# /etc/fail2ban/filter.d/nginx-noscript.conf

[Definition]
failregex = ^<HOST> -.*GET.*(\.php|\.asp|\.exe|\.pl|\.cgi|\.scgi)
ignoreregex =

# Matche :
# 203.0.113.50 - - [16/Jan/2024:14:30:45] "GET /admin.php HTTP/1.1" 404
```

**Filter brute-force wp-login :**

```bash
# Créer filter custom WordPress
sudo nano /etc/fail2ban/filter.d/wordpress-auth.local

[Definition]
failregex = ^<HOST> -.*POST.*/wp-login\.php
            ^<HOST> -.*POST.*/xmlrpc\.php

ignoreregex =

# Jail correspondant
[wordpress-auth]
enabled = true
port = http,https
filter = wordpress-auth
logpath = /var/log/nginx/access.log
maxretry = 5
findtime = 5m
bantime = 1h
```

**Filter rate limiting (nginx limit_req) :**

```bash
# Nginx config avec limit_req :
# limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
# limit_req zone=one burst=20 nodelay;

# Logs error.log :
# 2024/01/16 14:30:45 [error] 12345#12345: *67890 limiting requests, excess: 20.123 by zone "one", client: 203.0.113.50

# Filter : /etc/fail2ban/filter.d/nginx-limit-req.conf
[Definition]
failregex = limiting requests, .* client: <HOST>
ignoreregex =
```

### 7.3 Apache Jails

```bash
# Apache HTTP Auth
[apache-auth]
enabled = true
port = http,https
filter = apache-auth
logpath = /var/log/apache2/*error.log
maxretry = 5

# Apache Bad Bots
[apache-badbots]
enabled = true
port = http,https
filter = apache-badbots
logpath = /var/log/apache2/*access.log
maxretry = 2

# Apache No Script
[apache-noscript]
enabled = true
port = http,https
filter = apache-noscript
logpath = /var/log/apache2/*error.log
maxretry = 6

# Apache Overflows (buffer overflow attempts)
[apache-overflows]
enabled = true
port = http,https
filter = apache-overflows
logpath = /var/log/apache2/*error.log
maxretry = 2

# Apache ModSecurity
[apache-modsecurity]
enabled = true
port = http,https
filter = apache-modsecurity
logpath = /var/log/apache2/modsec_audit.log
maxretry = 2
bantime = 12h

# Apache Pass (password protected directories)
[apache-pass]
enabled = true
port = http,https
filter = apache-pass
logpath = /var/log/apache2/*error.log
maxretry = 3
```

### 7.4 WordPress Hardening

```bash
# WordPress multi-jails
sudo nano /etc/fail2ban/jail.d/wordpress.local

[wordpress-hard]
enabled = true
port = http,https
filter = wordpress-hard
logpath = /var/log/nginx/access.log
          /var/log/apache2/access.log
maxretry = 3
findtime = 10m
bantime = 12h

# Filter correspondant
sudo nano /etc/fail2ban/filter.d/wordpress-hard.local

[Definition]
failregex = ^<HOST> -.*POST.*/wp-login\.php
            ^<HOST> -.*POST.*/xmlrpc\.php
            ^<HOST> -.*GET.*/wp-admin.*
            ^<HOST> -.*POST.*/wp-comments-post\.php
            ^<HOST> -.*GET.*/wp-content/plugins/.*\.php
            ^<HOST> -.*GET.*/wp-includes/.*\.php

ignoreregex =

# Patterns détectés :
# - wp-login.php brute-force
# - xmlrpc.php abuse
# - wp-admin direct access (sans cookie auth)
# - Comment spam
# - Direct plugin file access
# - Direct includes file access
```

---

## Section 8 : Intégration Mail Servers

### 8.1 Postfix Jails

```bash
# Postfix SMTP Auth Failures
[postfix-sasl]
enabled = true
port = smtp,465,587,submission
filter = postfix-sasl
logpath = /var/log/mail.log
maxretry = 3
bantime = 1h

# Postfix general (multiple patterns)
[postfix]
enabled = true
port = smtp,465,587
filter = postfix
logpath = /var/log/mail.log
maxretry = 5

# Postfix RBL (Realtime Blackhole List rejections)
[postfix-rbl]
enabled = true
port = smtp,465,587,submission
filter = postfix-rbl
logpath = /var/log/mail.log
maxretry = 1
bantime = 12h
```

### 8.2 Dovecot (IMAP/POP3) Jails

```bash
# Dovecot Auth Failures
[dovecot]
enabled = true
port = pop3,pop3s,imap,imaps,submission,465,sieve
filter = dovecot
logpath = /var/log/mail.log
maxretry = 5
findtime = 10m
bantime = 1h

# Filter dovecot
# /etc/fail2ban/filter.d/dovecot.conf détecte :
# - Invalid password attempts
# - Unknown user attempts
# - Aborted login attempts
```

### 8.3 Exim Jails

```bash
# Exim SMTP Auth
[exim]
enabled = true
port = smtp,465,587
filter = exim
logpath = /var/log/exim4/mainlog

[exim-spam]
enabled = true
port = smtp,465,587
filter = exim-spam
logpath = /var/log/exim4/mainlog
```

### 8.4 Mail Server Complet

```bash
# Configuration complète mail server
sudo nano /etc/fail2ban/jail.d/mailserver.local

# Postfix
[postfix-sasl]
enabled = true
port = smtp,465,587,submission
filter = postfix-sasl
logpath = /var/log/mail.log
maxretry = 3
bantime = 1h
findtime = 10m

[postfix-rbl]
enabled = true
port = smtp,465,587
filter = postfix-rbl
logpath = /var/log/mail.log
maxretry = 1
bantime = 12h

# Dovecot
[dovecot]
enabled = true
port = pop3,pop3s,imap,imaps,submission,465,sieve
filter = dovecot
logpath = /var/log/mail.log
maxretry = 5
bantime = 1h

# Roundcube webmail
[roundcube-auth]
enabled = true
port = http,https
filter = roundcube-auth
logpath = /var/log/roundcube/errors.log
maxretry = 5

# Filter Roundcube custom
sudo nano /etc/fail2ban/filter.d/roundcube-auth.local

[Definition]
failregex = ^.*IMAP Error: Login failed for .* from <HOST>.*$
            ^.*Failed login for .* from <HOST>.*$
ignoreregex =
```

---

## Section 9 : Monitoring et Alertes

### 9.1 Fail2ban-client Commands

```bash
# Status global
sudo fail2ban-client status

# Status jail spécifique
sudo fail2ban-client status sshd

# Liste jails actives
sudo fail2ban-client status | grep "Jail list"

# Statistiques jail
sudo fail2ban-client get sshd stats

# Get configuration jail
sudo fail2ban-client get sshd bantime
sudo fail2ban-client get sshd maxretry
sudo fail2ban-client get sshd findtime

# Get IPs bannies
sudo fail2ban-client get sshd banip

# Get IPs actuellement en "findtime" window
sudo fail2ban-client get sshd failticket

# Bannir IP manuellement
sudo fail2ban-client set sshd banip 203.0.113.50

# Unbannir IP
sudo fail2ban-client set sshd unbanip 203.0.113.50

# Recharger jail sans restart
sudo fail2ban-client reload sshd

# Recharger toutes jails
sudo fail2ban-client reload
```

### 9.2 Logs Monitoring

```bash
# Logs Fail2ban principal
sudo tail -f /var/log/fail2ban.log

# Grep bans
sudo grep "Ban" /var/log/fail2ban.log

# Grep unbans
sudo grep "Unban" /var/log/fail2ban.log

# Statistiques bans par jail
sudo grep "Ban" /var/log/fail2ban.log | awk '{print $6}' | sort | uniq -c | sort -rn

# Top 10 IPs bannies
sudo grep "Ban" /var/log/fail2ban.log | grep -oP '\d+\.\d+\.\d+\.\d+' | sort | uniq -c | sort -rn | head -10

# Bans dernières 24h
sudo grep "$(date --date='1 day ago' +'%Y-%m-%d')" /var/log/fail2ban.log | grep "Ban"
```

### 9.3 Dashboard Script

```bash
#!/bin/bash
# /usr/local/bin/fail2ban-dashboard.sh

echo "=== Fail2ban Dashboard ==="
echo "Generated: $(date)"
echo ""

# Global status
echo "=== Global Status ==="
sudo fail2ban-client status
echo ""

# Jails actives
JAILS=$(sudo fail2ban-client status | grep "Jail list" | cut -d: -f2 | sed 's/,//g')

for JAIL in $JAILS; do
    echo "=== Jail: $JAIL ==="
    
    # Status jail
    sudo fail2ban-client status $JAIL | grep -E "Currently banned|Total banned"
    
    # Top 5 IPs banned
    echo "Top 5 Banned IPs:"
    sudo fail2ban-client get $JAIL banip | head -5
    
    echo ""
done

# Statistiques globales logs
echo "=== Ban Statistics (last 24h) ==="
sudo grep "$(date +'%Y-%m-%d')" /var/log/fail2ban.log | grep "Ban" | wc -l | xargs echo "Total bans today:"

echo ""
echo "=== Top 10 Banned IPs (all time) ==="
sudo grep "Ban" /var/log/fail2ban.log | grep -oP '\d+\.\d+\.\d+\.\d+' | sort | uniq -c | sort -rn | head -10

# Cron : */5 * * * * /usr/local/bin/fail2ban-dashboard.sh > /var/www/html/fail2ban-status.txt
```

### 9.4 Prometheus Exporter

```python
#!/usr/bin/env python3
# /usr/local/bin/fail2ban-prometheus-exporter.py

from prometheus_client import start_http_server, Gauge, Counter
import subprocess
import re
import time

# Metrics
jail_banned_ips = Gauge('fail2ban_jail_banned_ips', 'Currently banned IPs', ['jail'])
jail_total_banned = Counter('fail2ban_jail_total_banned', 'Total banned IPs', ['jail'])
jail_failed_current = Gauge('fail2ban_jail_failed_current', 'Currently failed', ['jail'])
jail_total_failed = Counter('fail2ban_jail_total_failed', 'Total failed', ['jail'])

def get_jails():
    """Get list of active jails"""
    result = subprocess.run(['fail2ban-client', 'status'], 
                          capture_output=True, text=True)
    match = re.search(r'Jail list:\s+(.+)', result.stdout)
    if match:
        return [j.strip() for j in match.group(1).split(',')]
    return []

def get_jail_stats(jail):
    """Get statistics for specific jail"""
    result = subprocess.run(['fail2ban-client', 'status', jail],
                          capture_output=True, text=True)
    
    stats = {}
    for line in result.stdout.split('\n'):
        if 'Currently banned:' in line:
            stats['banned'] = int(line.split(':')[1].strip())
        elif 'Total banned:' in line:
            stats['total_banned'] = int(line.split(':')[1].strip())
        elif 'Currently failed:' in line:
            stats['failed'] = int(line.split(':')[1].strip())
        elif 'Total failed:' in line:
            stats['total_failed'] = int(line.split(':')[1].strip())
    
    return stats

def collect_metrics():
    """Collect metrics from all jails"""
    jails = get_jails()
    
    for jail in jails:
        stats = get_jail_stats(jail)
        
        jail_banned_ips.labels(jail=jail).set(stats.get('banned', 0))
        jail_total_banned.labels(jail=jail).inc(stats.get('total_banned', 0))
        jail_failed_current.labels(jail=jail).set(stats.get('failed', 0))
        jail_total_failed.labels(jail=jail).inc(stats.get('total_failed', 0))

if __name__ == '__main__':
    # Start HTTP server
    start_http_server(9191)
    print("Fail2ban Prometheus exporter started on port 9191")
    
    while True:
        collect_metrics()
        time.sleep(60)
```

**Systemd service exporter :**

```bash
# /etc/systemd/system/fail2ban-exporter.service

[Unit]
Description=Fail2ban Prometheus Exporter
After=network.target fail2ban.service

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/fail2ban-prometheus-exporter.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 9.5 Alertes Email Advanced

```bash
# Configuration email détaillée
sudo nano /etc/fail2ban/action.d/sendmail-custom.local

[Definition]
actionstart =
actionstop =

actionban = printf "Subject: [Fail2Ban] <name>: <ip> BANNED
            From: <sender>
            To: <dest>
            MIME-Version: 1.0
            Content-Type: text/html; charset=utf-8
            
            <html>
            <body style='font-family: Arial; padding: 20px;'>
            <h2 style='color: #c00;'>⛔ IP Banned by Fail2Ban</h2>
            <table style='border-collapse: collapse; width: 100%%;'>
            <tr><td style='padding: 8px; background: #f5f5f5;'><b>Jail</b></td><td style='padding: 8px;'><name></td></tr>
            <tr><td style='padding: 8px; background: #f5f5f5;'><b>IP</b></td><td style='padding: 8px;'><ip></td></tr>
            <tr><td style='padding: 8px; background: #f5f5f5;'><b>Failures</b></td><td style='padding: 8px;'><failures></td></tr>
            <tr><td style='padding: 8px; background: #f5f5f5;'><b>Time</b></td><td style='padding: 8px;'><time></td></tr>
            <tr><td style='padding: 8px; background: #f5f5f5;'><b>Server</b></td><td style='padding: 8px;'>$(hostname)</td></tr>
            </table>
            
            <h3>WHOIS Information:</h3>
            <pre style='background: #f9f9f9; padding: 10px; overflow: auto;'>$(whois <ip> 2>/dev/null || echo 'WHOIS lookup failed')</pre>
            
            <h3>Log Matches:</h3>
            <pre style='background: #f9f9f9; padding: 10px; overflow: auto;'>$(grep '<ip>' <logpath> | tail -20)</pre>
            
            <p style='color: #666; font-size: 12px;'>This is an automated message from Fail2Ban on $(hostname)</p>
            </body>
            </html>" | /usr/sbin/sendmail -t

actionunban = printf "Subject: [Fail2Ban] <name>: <ip> UNBANNED
              From: <sender>
              To: <dest>
              
              The IP <ip> has been unbanned from <name> jail." | /usr/sbin/sendmail -t

[Init]
sender = fail2ban@example.com
dest = admin@example.com
```

---

## Section 10 : Whitelist et Gestion IPs

### 10.1 Ignoreip (Whitelist Permanente)

```bash
# Global whitelist (tous jails)
sudo nano /etc/fail2ban/jail.local

[DEFAULT]
ignoreip = 127.0.0.1/8 ::1
           192.168.0.0/16        # LAN privé
           10.0.0.0/8            # LAN privé
           172.16.0.0/12         # LAN privé
           203.0.113.10          # Admin office
           198.51.100.0/24       # VPN subnet
           monitoring.example.com # Hostname (résolu DNS)

# Whitelist jail spécifique (override global)
[sshd]
enabled = true
ignoreip = 192.168.1.100  # Admin IP spécial SSH
```

### 10.2 Ignorecommand (Whitelist Dynamique)

```bash
# Whitelist basée sur commande externe

sudo nano /etc/fail2ban/jail.local

[DEFAULT]
ignorecommand = /usr/local/bin/fail2ban-whitelist-check.sh <ip>

# Script whitelist check
sudo nano /usr/local/bin/fail2ban-whitelist-check.sh

#!/bin/bash
IP=$1

# Check si IP dans whitelist dynamique
if grep -q "^$IP$" /etc/fail2ban/whitelist-dynamic.txt; then
    exit 0  # Whitelisted
fi

# Check si IP reverse DNS match domaine safe
HOSTNAME=$(dig +short -x $IP | sed 's/\.$//')
if [[ $HOSTNAME =~ \.googlebot\.com$ ]] || [[ $HOSTNAME =~ \.crawl\.baidu\.com$ ]]; then
    exit 0  # Whitelisted (legit bot)
fi

exit 1  # Not whitelisted

# Rendre exécutable
sudo chmod +x /usr/local/bin/fail2ban-whitelist-check.sh
```

### 10.3 Unban Automatique IPs Légitimes

```bash
# Script unban automatique après vérification

sudo nano /usr/local/bin/fail2ban-auto-unban.sh

#!/bin/bash
# Auto unban légitimate IPs

LOGFILE="/var/log/fail2ban.log"
JAILS=$(fail2ban-client status | grep "Jail list" | cut -d: -f2 | sed 's/,//g')

for JAIL in $JAILS; do
    BANNED_IPS=$(fail2ban-client get $JAIL banip)
    
    for IP in $BANNED_IPS; do
        # Check reverse DNS
        HOSTNAME=$(dig +short -x $IP 2>/dev/null | sed 's/\.$//')
        
        # Unban legit bots
        if [[ $HOSTNAME =~ \.googlebot\.com$ ]]; then
            echo "Unbanning legitimate Googlebot: $IP ($HOSTNAME)"
            fail2ban-client set $JAIL unbanip $IP
            logger -t fail2ban-auto-unban "Unbanned Googlebot $IP from $JAIL"
        fi
        
        if [[ $HOSTNAME =~ \.crawl\.baidu\.com$ ]]; then
            echo "Unbanning legitimate Baiduspider: $IP ($HOSTNAME)"
            fail2ban-client set $JAIL unbanip $IP
        fi
    done
done

# Cron : */10 * * * * /usr/local/bin/fail2ban-auto-unban.sh
```

### 10.4 Gestion Database Bans

```bash
# Database SQLite persistence
DBFILE="/var/lib/fail2ban/fail2ban.sqlite3"

# Vérifier database existe
ls -lh $DBFILE

# Query database (liste bans actifs)
sudo sqlite3 $DBFILE "SELECT * FROM bans WHERE timeofban + bantime > strftime('%s', 'now');"

# Liste tous bans historiques
sudo sqlite3 $DBFILE "SELECT ip, jail, timeofban, datetime(timeofban, 'unixepoch', 'localtime') as ban_time FROM bans ORDER BY timeofban DESC LIMIT 50;"

# Statistiques par jail
sudo sqlite3 $DBFILE "SELECT jail, COUNT(*) as total_bans FROM bans GROUP BY jail ORDER BY total_bans DESC;"

# Top 20 IPs most banned
sudo sqlite3 $DBFILE "SELECT ip, COUNT(*) as ban_count FROM bans GROUP BY ip ORDER BY ban_count DESC LIMIT 20;"

# Purge old entries (>30 jours)
sudo sqlite3 $DBFILE "DELETE FROM bans WHERE timeofban < strftime('%s', 'now', '-30 days');"

# Backup database
sudo cp $DBFILE ${DBFILE}.backup-$(date +%Y%m%d)
```

### 10.5 Récidive (Bantime Incrémental)

```bash
# Configuration récidive (ban permanent après X fois)

[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
findtime = 10m
bantime = 1h

# Bantime incrémental
bantime.increment = true
bantime.rndtime = 5m          # Randomisation +/- 5min (anti-pattern)
bantime.maxtime = 1w          # Ban maximum 1 semaine
bantime.factor = 2            # Multiplicateur ×2 chaque fois
bantime.formula = ban.Time * (1<<(ban.Count if ban.Count<20 else 20)) * banFactor
bantime.multipliers = 1 2 4 8 16 32 64

# Récidive : après 3 bans dans periode_observation
bantime.overalljails = true   # Count bans across all jails

# Résultat :
# 1ère offense : 1h
# 2ème offense : 2h
# 3ème offense : 4h
# 4ème offense : 8h
# 5ème offense : 16h
# 6ème offense : 32h
# 7ème offense : 64h
# 8ème offense : 128h
# 9ème offense : 168h (1w max)
```

---

## Section 11 : Performance et Tuning

### 11.1 Optimisation Backend

```bash
# Backend log monitoring (choisir plus performant)

# Vérifier backend disponibles
python3 -c "import fail2ban.server.filtersystemd; print('systemd available')"
python3 -c "import pyinotify; print('pyinotify available')"

# Configuration jail.local
[DEFAULT]
backend = auto  # Auto-detect (recommandé)
# Alternatives :
# backend = systemd    # Si systemd-journald (plus rapide logs systemd)
# backend = pyinotify  # inotify kernel API (très rapide)
# backend = gamin      # File alteration monitor
# backend = polling    # Polling basique (lent, compatible)

# Performance comparison :
# systemd  : Très rapide si logs dans journald
# pyinotify: Très rapide, low CPU
# gamin    : Rapide
# polling  : Lent, high CPU, compatible
```

### 11.2 Tuning Database

```bash
# Database performance tuning
sudo nano /etc/fail2ban/fail2ban.local

[Definition]
dbfile = /var/lib/fail2ban/fail2ban.sqlite3
dbpurgeage = 86400      # Purge entries > 24h (défaut)
# Réduire si DB grows trop :
# dbpurgeage = 3600     # 1 heure

# Purge manuelle
sudo fail2ban-client set dbpurgeage 3600
sudo fail2ban-client reload

# Compacter database
sudo sqlite3 /var/lib/fail2ban/fail2ban.sqlite3 "VACUUM;"
```

### 11.3 Optimisation Regex Filters

```bash
# Regex performantes (éviter backtracking excessif)

# ❌ Regex lente (catastrophic backtracking)
failregex = ^.*Failed.*from.*<HOST>.*$

# ✅ Regex optimisée (plus spécifique)
failregex = ^%(__prefix_line)sFailed password for .* from <HOST> port \d+ ssh2$

# Bonnes pratiques regex :
# 1. Utiliser ^...$ (anchors début/fin)
# 2. Éviter .* au début (utiliser __prefix_line)
# 3. Spécifier patterns précis (.* → \S+ pour username)
# 4. Utiliser \d+ au lieu \d* pour nombres
# 5. Compiler patterns complexes (datepattern)

# Tester performance regex
time fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf
```

### 11.4 Limiter Jails Actives

```bash
# Désactiver jails non nécessaires (économise CPU/RAM)

# Désactiver dans jail.local
[nginx-badbots]
enabled = false  # Désactivé

[apache-auth]
enabled = false  # Pas Apache sur serveur

# Ou commenter section complète

# Vérifier jails actives
sudo fail2ban-client status

# Reload après modifications
sudo fail2ban-client reload
```

### 11.5 Monitoring Performance

```bash
# CPU/RAM usage Fail2ban
ps aux | grep fail2ban-server
# USER  PID  %CPU %MEM    VSZ   RSS TTY STAT START   TIME COMMAND

# Memory détaillée
pmap -x $(pidof fail2ban-server) | tail -1

# Nombre threads
ps -eLf | grep fail2ban-server | wc -l

# Logs verbosité (réduire si trop CPU I/O)
sudo nano /etc/fail2ban/fail2ban.local
loglevel = WARNING  # Au lieu INFO ou DEBUG

# Systemd resources limits
sudo systemctl edit fail2ban

[Service]
MemoryMax=256M
CPUQuota=50%

# Reload
sudo systemctl daemon-reload
sudo systemctl restart fail2ban
```

---

## Section 12 : Best Practices Production

### 12.1 Configuration Production Type

```bash
#!/bin/bash
# setup-fail2ban-production.sh

# Configuration Fail2ban production optimale

# 1. Installer Fail2ban
sudo apt update
sudo apt install fail2ban

# 2. Backup config par défaut
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.conf.bak

# 3. Créer jail.local
sudo tee /etc/fail2ban/jail.local > /dev/null << 'EOF'
[DEFAULT]
# Ban settings
bantime  = 1h
findtime = 10m
maxretry = 3

# Bantime incrémental
bantime.increment = true
bantime.factor = 2
bantime.maxtime = 1w

# Whitelist
ignoreip = 127.0.0.1/8 ::1
           192.168.0.0/16
           YOUR_ADMIN_IP

# Backend
backend = auto
banaction = iptables-multiport

# Notifications
destemail = admin@example.com
sender = fail2ban@$(hostname)
mta = sendmail
action = %(action_mwl)s

# === JAILS ===

# SSH
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
mode = aggressive

# Nginx
[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
filter = nginx-noscript
logpath = /var/log/nginx/access.log
maxretry = 6

[nginx-badbots]
enabled = true
port = http,https
filter = nginx-badbots
logpath = /var/log/nginx/access.log
maxretry = 2

[nginx-limit-req]
enabled = true
port = http,https
filter = nginx-limit-req
logpath = /var/log/nginx/error.log

# WordPress (si applicable)
[wordpress-hard]
enabled = false
port = http,https
filter = wordpress-hard
logpath = /var/log/nginx/access.log
maxretry = 3
bantime = 12h
EOF

# 4. Tester config
sudo fail2ban-client -t

# 5. Enable et start
sudo systemctl enable fail2ban
sudo systemctl restart fail2ban

# 6. Vérifier status
sudo fail2ban-client status

echo "✅ Fail2ban configured for production"
```

### 12.2 Checklist Production

```markdown
## Fail2ban Production Checklist

### Installation
- [ ] Fail2ban installé dernière version stable
- [ ] Service systemd enabled
- [ ] Logs directory writable (/var/log/fail2ban.log)
- [ ] Database directory writable (/var/lib/fail2ban/)

### Configuration
- [ ] jail.local créé (pas éditer jail.conf)
- [ ] Whitelist admin IPs configurée (ignoreip)
- [ ] Bantime/findtime/maxretry ajustés selon risque
- [ ] Bantime incrémental activé (récidives)
- [ ] Backend optimal sélectionné (auto/systemd/pyinotify)

### Jails
- [ ] SSH jail activé et testé
- [ ] Web server jails activés (nginx/apache)
- [ ] Mail server jails activés (si applicable)
- [ ] Jails non nécessaires désactivés
- [ ] Filters testés (fail2ban-regex)

### Actions
- [ ] Firewall integration fonctionnelle (iptables/UFW)
- [ ] Notifications email configurées
- [ ] Actions custom créées (si requis)
- [ ] Tests ban/unban manuel

### Monitoring
- [ ] Logs monitoring configuré (tail -f)
- [ ] Dashboard/status script déployé
- [ ] Prometheus exporter installé (optionnel)
- [ ] Alertes critiques configurées

### Security
- [ ] Ignorecommand testé (whitelist dynamique)
- [ ] Récidive detection activée
- [ ] Database backup configurée
- [ ] Logs rotation configurée

### Testing
- [ ] Tentatives failed password testées
- [ ] Ban automatique vérifié (3 tentatives)
- [ ] Unban automatique vérifié (après bantime)
- [ ] Whitelist IPs testées (pas bannies)
- [ ] Notifications reçues (email/Slack)

### Documentation
- [ ] Procédures unban documentées
- [ ] Whitelist IPs documentée (why)
- [ ] Custom filters/actions documentés
- [ ] Contacts on-call définis

### Maintenance
- [ ] Database purge automatique configurée
- [ ] Logs rotation configurée
- [ ] Backup configuration schedulé
- [ ] Updates Fail2ban trackées
```

### 12.3 Scénarios Par Type Serveur

**Web Server (Nginx/Apache) :**

```bash
# Jails recommandés
[sshd]                   # SSH protection
[nginx-http-auth]        # Basic auth brute-force
[nginx-noscript]         # PHP/scripts scanning
[nginx-badbots]          # Bad bots
[nginx-limit-req]        # Rate limiting violations
[wordpress-hard]         # WordPress brute-force (si WP)
```

**Database Server :**

```bash
# Jails recommandés
[sshd]                   # SSH protection (accès admin)
[mysql-auth]             # MySQL auth failures (si exposé)
[postgresql]             # PostgreSQL auth failures (si exposé)
```

**Mail Server :**

```bash
# Jails recommandés
[sshd]                   # SSH protection
[postfix-sasl]           # SMTP auth failures
[postfix-rbl]            # RBL rejections
[dovecot]                # IMAP/POP3 auth failures
[roundcube-auth]         # Webmail brute-force
```

**VPS Multi-tenant :**

```bash
# Jails recommandés (aggressifs)
[sshd]                   # SSH protection
[sshd-ddos]              # SSH flood protection
[nginx-http-auth]        # Web auth
[nginx-noscript]         # Scanning
[nginx-badbots]          # Bots
[nginx-limit-req]        # Rate limiting
[recidive]               # Récidives multi-jails
```

### 12.4 Troubleshooting Guide

```bash
# Fail2ban ne démarre pas
sudo systemctl status fail2ban
sudo journalctl -u fail2ban -n 50

# Erreur config
sudo fail2ban-client -t
# Corriger erreurs indiquées

# Jail n'active pas
sudo fail2ban-client status
# Vérifier enabled=true dans jail.local

# Logs non monitorés
sudo fail2ban-client get <jail> logpath
# Vérifier fichier existe et readable

# IPs pas bannies
sudo fail2ban-client status <jail>
# Vérifier failticket (tentatives détectées)

# Filter ne matche pas
fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf -v

# Action ban n'exécute pas
sudo iptables -L f2b-<jail> -n -v
# Vérifier chain existe et rules ajoutées

# Performance lente
ps aux | grep fail2ban-server
# Vérifier CPU/RAM usage
# Réduire jails actives
# Optimiser regex filters
```

---

## Ressources et Références

**Documentation officielle :**
- Site : https://www.fail2ban.org/
- Wiki : https://github.com/fail2ban/fail2ban/wiki
- Manuel : `man fail2ban`, `man fail2ban-client`, `man jail.conf`

**GitHub :**
- Repository : https://github.com/fail2ban/fail2ban
- Issues : https://github.com/fail2ban/fail2ban/issues

**Communauté :**
- Mailing list : https://www.fail2ban.org/wiki/index.php/Support
- Stack Overflow : [fail2ban] tag

**Outils complémentaires :**
- fail2ban-web : Interface web monitoring
- fail2web : Dashboard PHP
- PyFail2ban : Python client library

---

## Conclusion

**Fail2ban = Protection essentielle serveurs exposés Internet**

**Points clés :**

✅ **IPS automatisé** = Détection + ban temps réel
✅ **Multi-services** = SSH, web, mail, custom
✅ **Léger** = Python, faible overhead
✅ **Extensible** = Filters/actions custom illimités
✅ **Production-ready** = Millions installations, stable

**Workflow recommandé :**

```bash
# 1. Installation
sudo apt install fail2ban

# 2. Configuration basique
sudo nano /etc/fail2ban/jail.local
# [DEFAULT] bantime/findtime/maxretry
# [sshd] enabled=true

# 3. Whitelist admin IPs
ignoreip = YOUR_ADMIN_IP

# 4. Test config
sudo fail2ban-client -t

# 5. Start
sudo systemctl enable --now fail2ban

# 6. Monitoring
sudo fail2ban-client status

# 7. Maintenance
# - Review logs hebdomadaire
# - Update filters si nouveaux patterns
# - Ajuster bantime selon attaques
# - Backup database mensuel
```

**Erreurs à éviter :**

- ❌ Ne PAS éditer jail.conf (éditer jail.local)
- ❌ Ne PAS oublier whitelist admin IPs (lockout)
- ❌ Ne PAS mettre maxretry=1 (false positives)
- ❌ Ne PAS ignorer logs Fail2ban (monitoring)
- ❌ Ne PAS tester en production (tester regex avant)
- ❌ Ne PAS bannir sans notification (alertes email)
- ❌ Ne PAS négliger database purge (grows forever)

**Tu maîtrises maintenant Fail2ban de la configuration basique à l'intégration production avancée !** 🛡️

---

**Guide Fail2ban Complet terminé !** 🎉

Voilà le guide complet Fail2ban exhaustif ! Il couvre :

✅ **12 sections complètes** avec analogie pédagogique  
✅ Introduction IPS et concepts (jails, filters, actions)  
✅ Installation et configuration initiale sécurisée  
✅ Jails configuration avancée (tous paramètres)  
✅ Filtres regex détaillés et création custom  
✅ Actions multiples (ban, notifications, custom)  
✅ Intégration SSH avancée (mode aggressive, récidive)  
✅ Intégration web (Nginx, Apache, WordPress)  
✅ Intégration mail (Postfix, Dovecot, Exim)  
✅ Monitoring complet (dashboard, Prometheus, alertes)  
✅ Whitelist et gestion IPs (ignoreip, database)  
✅ Performance tuning production  
✅ Best practices par scénario avec scripts prêts  
✅ Troubleshooting complet  

**Même rigueur exhaustive que tes guides précédents !** 🔒