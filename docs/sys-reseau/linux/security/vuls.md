---
description: "Vuls : scanner vulnérabilités CVE agentless, monitoring packages, reporting, intégration CI/CD"
icon: lucide/book-open-check
tags: ["VULS", "CVE", "VULNERABILITY", "SCANNER", "LINUX", "SECURITY", "PATCHING"]
---

# Vuls

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-time="6-8 heures"
  data-version="1.0">
</div>

## Introduction au Scanner de Vulnérabilités

!!! quote "Analogie pédagogique"
    _Imaginez un **médecin spécialisé maladies infectieuses avec base données mondiale 200,000+ pathogènes catalogués** : Vuls fonctionne comme **scanner médical automatisé analysant CHAQUE logiciel installé comparant versions catalogue vulnérabilités connues CVE**. **Médecin infectiologue consultation préventive** : dossier médical patient complet (inventory packages système), base données maladies connues (CVE database 200K+ vulnérabilités), analyse sang/radiologie (scan versions logiciels), diagnostic précis (CVE-2024-1234 OpenSSL critical RCE), prescription traitement (apt upgrade openssl), suivi évolution patient (monitoring continu), alerte épidémies nouvelles (CVE feed temps réel), dossier électronique centralisé (dashboard VulsRepo). **Sans Vuls** : packages obsolètes exploitables (Apache 2.4.29 = CVE-2021-44790 SSRF critical), kernel non patché (CVE-2022-0847 Dirty Pipe privilege escalation), bibliothèques vulnérables (Log4Shell CVE-2021-44228 RCE), zero-days exploités silencieusement (attaquants scannent Internet vulnérabilités connues), compliance violations (PCI-DSS exige patching <30 jours), responsabilité légale (breach via CVE public documenté). **Avec Vuls** : **Scan agentless** (SSH remote scan, pas agent installer), **200,000+ CVE database** (NVD, JVN, OVAL, Debian Security Tracker, Red Hat Security Data), **Multi-distro** (Ubuntu, Debian, RHEL, CentOS, Amazon Linux, Alpine, etc.), **Scoring CVSS** (priorité v3.1 critical 9.0-10.0), **Reporting avancé** (JSON, text, CSV, HTML, dashboard web VulsRepo), **Integration CI/CD** (scan containers, images Docker avant deploy), **Notifications** (Slack, Email, ChatWork, stride), **Exploit detection** (exploitdb, Metasploit modules disponibles). **Architecture Vuls** : Scanner Go (performant, statically-compiled) + Config TOML (servers list) + Databases locales SQLite (CVE cache) + Optional VulsRepo (dashboard React) + Goval-dictionary (OVAL data) + Gost (Security Tracker) + Go-exploitdb (exploit DB). **Workflow typique** : 1) fetch-nvd (download NVD database), 2) config.toml (define servers SSH), 3) vuls scan (collect package versions), 4) vuls report (match CVE), 5) VulsRepo dashboard (visualize), 6) triage patches (prioritize critical). **Cas usage production** : compliance PCI-DSS (scan mensuel obligatoire), infrastructure 100+ serveurs (centralized scanning), CI/CD pipeline (block deploy vulnerable images), SLA patch management (track remediation 30 jours), audit post-incident (identify exploited CVE), vendor software lifecycle (EOL tracking). **Différence vs Lynis** : Lynis = audit CONFIGURATION (hardening, settings, permissions) vs Vuls = scanner PACKAGES (CVE vulnerabilities versions software). **Complémentarité** : Lynis trouve misconfiguration ("SSH PermitRootLogin yes" = mauvais), Vuls trouve CVE ("OpenSSH 7.4p1 = CVE-2023-38408"). **Vuls = standard industrie** : utilisé Fortune 500, gouvernements, scale 10,000+ servers, active community GitHub 10K+ stars, maintenance continue._

**Vuls en résumé :**

- ✅ **200,000+ CVE** = NVD, JVN, OVAL, Security Trackers
- ✅ **Agentless** = Scan SSH remote, pas agent à déployer
- ✅ **Multi-distro** = Ubuntu, Debian, RHEL, CentOS, Alpine, Amazon Linux
- ✅ **CVSS scoring** = Priorité v3.1 (critical 9.0-10.0)
- ✅ **Dashboard web** = VulsRepo React visualization
- ✅ **CI/CD ready** = Scan containers/images Docker
- ✅ **Gratuit** = GPL, open-source, community active
- ✅ **Performant** = Go binary, scan rapide, faible overhead

**Guide structure :**

1. Introduction et concepts CVE
2. Installation et architecture
3. Configuration databases (NVD, OVAL, Gost)
4. Configuration scans (config.toml)
5. Modes scan (local, remote SSH, container)
6. Reporting et analyse résultats
7. Dashboard VulsRepo
8. Intégration CI/CD (Docker, Kubernetes)
9. Automatisation et monitoring
10. Patch management workflow
11. Cas pratiques (Log4Shell, Dirty Pipe, etc.)
12. Best practices enterprise

---

## Section 1 : Introduction et Concepts

### 1.1 Qu'est-ce que Vuls ?

**Vuls = VULnerability Scanner agentless open-source**

```
Vuls (Vulnerability Scanner) :

Créé       : 2016 par Future Corporation (Japon)
Langage    : Go (performant, statically-compiled)
Objectif   : Détecter CVE packages Linux
Architecture : Agentless (SSH) ou local
Database   : NVD, JVN, OVAL, Security Trackers
Méthode    : Inventory packages → Match CVE database
Licence    : GPL v3

Architecture Vuls :

┌─────────────────────────────────────────────────────┐
│                  Vuls Scanner                       │
│              (vuls scan + report)                   │
└─────────────┬───────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────┐
│              Target Servers                         │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ Server 1     │  │ Server 2     │  SSH (agentless)│
│  │ Ubuntu 22.04 │  │ CentOS 8     │                │
│  └──────────────┘  └──────────────┘                │
└─────────────┬───────────────────────────────────────┘
              │ Package inventory
              ↓
┌─────────────────────────────────────────────────────┐
│              CVE Databases                          │
│  ┌──────────────────────────────────────────────┐  │
│  │ NVD (National Vulnerability Database)        │  │
│  │ 200,000+ CVE entries                         │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │ OVAL (Open Vulnerability Assessment Language)│  │
│  │ Ubuntu, Debian, RHEL, Oracle Linux          │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │ Gost (Security Tracker)                      │  │
│  │ Debian, Ubuntu, RHEL Security Advisories    │  │
│  └──────────────────────────────────────────────┘  │
└─────────────┬───────────────────────────────────────┘
              │ Match CVE
              ↓
┌─────────────────────────────────────────────────────┐
│              Vuls Results                           │
│  - CVE-2024-1234 (OpenSSL 3.0.7) CVSS 9.8 Critical│
│  - CVE-2023-5678 (kernel 5.15.0) CVSS 7.8 High    │
│  - CVE-2022-9012 (nginx 1.18.0) CVSS 5.3 Medium   │
└─────────────┬───────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────┐
│           VulsRepo Dashboard (optional)             │
│  Web UI visualization + trending + filtering       │
└─────────────────────────────────────────────────────┘
```

### 1.2 CVE (Common Vulnerabilities and Exposures)

**CVE = Identifiant unique vulnérabilité sécurité**

```
Format CVE :
CVE-YYYY-NNNNN

Exemples célèbres :
CVE-2021-44228 : Log4Shell (Apache Log4j RCE)
CVE-2022-0847  : Dirty Pipe (Linux kernel privilege escalation)
CVE-2014-0160  : Heartbleed (OpenSSL information disclosure)
CVE-2017-5638  : Apache Struts2 RCE (Equifax breach)
CVE-2014-6271  : Shellshock (Bash RCE)

Anatomie CVE :

CVE-2021-44228 (Log4Shell)
├─ ID : CVE-2021-44228
├─ Published : 2021-12-10
├─ CVSS v3.1 : 10.0 CRITICAL
│   ├─ Attack Vector : Network
│   ├─ Attack Complexity : Low
│   ├─ Privileges Required : None
│   ├─ User Interaction : None
│   └─ Impact : Complete compromise
├─ Affected : Apache Log4j 2.0-beta9 to 2.15.0 (exclusif)
├─ Description : JNDI injection RCE via crafted LDAP request
├─ References : 
│   ├─ https://nvd.nist.gov/vuln/detail/CVE-2021-44228
│   └─ https://www.lunasec.io/docs/blog/log4j-zero-day/
└─ Exploit Available : YES (public PoC, Metasploit module)

CVSS Scoring :

0.0          : None
0.1 - 3.9    : Low
4.0 - 6.9    : Medium
7.0 - 8.9    : High
9.0 - 10.0   : Critical

Priorité patching :
Critical 9.0+ → Immediate (24h)
High 7.0-8.9  → Urgent (7 jours)
Medium 4.0-6.9 → Normal (30 jours)
Low 0.1-3.9   → Planifié (90 jours)
```

### 1.3 Databases CVE

**Sources données Vuls :**

```
1. NVD (National Vulnerability Database)
   ─────────────────────────────────────
   Maintainer : NIST (US Government)
   Coverage : ALL CVE (200,000+)
   Update : Daily
   Format : JSON feeds
   
   vuls fetch-nvd
   # Télécharge JSON feeds NVD
   # ~/.vuls/nvd/ (~2GB)

2. JVN (Japan Vulnerability Notes)
   ────────────────────────────────
   Maintainer : JPCERT/CC (Japan)
   Coverage : CVE Japanese focus
   Update : Daily
   
   vuls fetch-jvn
   
3. OVAL (Open Vulnerability Assessment Language)
   ──────────────────────────────────────────────
   Coverage : Distribution-specific
   Sources :
   - Ubuntu OVAL
   - Debian OVAL
   - RHEL OVAL
   - Oracle Linux OVAL
   - SUSE OVAL
   
   goval-dictionary fetch-ubuntu 22
   goval-dictionary fetch-debian 11
   goval-dictionary fetch-redhat 8
   
4. Gost (Security Tracker)
   ────────────────────────
   Coverage : Distribution security advisories
   Sources :
   - Debian Security Tracker
   - Ubuntu Security Notices
   - RHEL Security Data
   
   gost fetch debian
   gost fetch ubuntu
   gost fetch redhat

5. Go-exploitdb
   ─────────────
   Coverage : Exploit Database
   Sources : Offensive Security Exploit-DB
   
   go-exploitdb fetch exploitdb
   go-exploitdb fetch awesomepoc
```

### 1.4 Vuls vs Alternatives

| Critère | Vuls | OpenVAS | Nessus | Qualys | Lynis |
|---------|------|---------|--------|--------|-------|
| **Type** | CVE scanner | Vuln scanner | Vuln scanner | Cloud SaaS | Config audit |
| **Focus** | Packages CVE | Network + OS | Network + OS | Enterprise | Hardening |
| **Agent** | Agentless (SSH) | Network scan | Agent/Agentless | Agent | Local |
| **Prix** | Gratuit | Gratuit | Payant | Payant | Gratuit |
| **Database** | NVD/OVAL/Gost | NASL/NVT | Plugins | Cloud DB | Built-in |
| **Performance** | Rapide | Lourd | Moyen | Moyen | Rapide |
| **Scale** | 1000+ servers | <100 hosts | Enterprise | Cloud | Single host |
| **Reporting** | JSON/HTML/Slack | Web UI | Web UI | Dashboard | Text/JSON |
| **CI/CD** | Oui | Non | Limité | Non | Oui |

**Complémentarité Lynis + Vuls :**

```
┌──────────────────────────────────────────────────┐
│              Security Audit Stack                │
├──────────────────────────────────────────────────┤
│                                                  │
│  Lynis (Configuration Audit)                    │
│  ├─ SSH config (PermitRootLogin, etc.)         │
│  ├─ File permissions (/etc/passwd, etc.)       │
│  ├─ Kernel parameters (sysctl)                 │
│  ├─ Services running (unnecessary daemons)     │
│  └─ Hardening score (0-100)                    │
│                                                  │
│  Vuls (Vulnerability Scanner)                   │
│  ├─ Package versions (apache2 2.4.29)          │
│  ├─ CVE matching (CVE-2021-44790)              │
│  ├─ CVSS scoring (9.0 Critical)                │
│  ├─ Exploit availability (Metasploit)          │
│  └─ Patch recommendations (upgrade apache2)    │
│                                                  │
└──────────────────────────────────────────────────┘

Exemple concret :

Lynis trouve :
❌ SSH PermitRootLogin yes (misconfiguration)
❌ /tmp not mounted noexec (hardening issue)

Vuls trouve :
❌ OpenSSH 7.4p1 = CVE-2023-38408 (vulnerability)
❌ kernel 5.4.0-42 = CVE-2022-0847 Dirty Pipe

→ Les deux complémentaires, pas redondants
```

---

## Section 2 : Installation et Architecture

### 2.1 Installation Vuls (Binary Release)

```bash
# Méthode 1 : Download binary (recommandé)

# Identifier architecture
uname -m
# x86_64 = amd64

# Télécharger dernière version
cd /tmp
VERSION="0.27.0"  # Vérifier dernière : https://github.com/future-architect/vuls/releases
wget https://github.com/future-architect/vuls/releases/download/v${VERSION}/vuls_${VERSION}_linux_amd64.tar.gz

# Extraire
tar -xzf vuls_${VERSION}_linux_amd64.tar.gz

# Installer
sudo mv vuls /usr/local/bin/
sudo chmod +x /usr/local/bin/vuls

# Vérifier
vuls version
# vuls v0.27.0 (build 2024-01-15T12:00:00Z)
```

**Installation dépendances (databases) :**

```bash
# go-cve-dictionary (NVD)
VERSION="0.10.0"
wget https://github.com/vulsio/go-cve-dictionary/releases/download/v${VERSION}/go-cve-dictionary_${VERSION}_linux_amd64.tar.gz
tar -xzf go-cve-dictionary_${VERSION}_linux_amd64.tar.gz
sudo mv go-cve-dictionary /usr/local/bin/

# goval-dictionary (OVAL)
VERSION="0.4.0"
wget https://github.com/vulsio/goval-dictionary/releases/download/v${VERSION}/goval-dictionary_${VERSION}_linux_amd64.tar.gz
tar -xzf goval-dictionary_${VERSION}_linux_amd64.tar.gz
sudo mv goval-dictionary /usr/local/bin/

# gost (Security Tracker)
VERSION="0.3.0"
wget https://github.com/vulsio/gost/releases/download/v${VERSION}/gost_${VERSION}_linux_amd64.tar.gz
tar -xzf gost_${VERSION}_linux_amd64.tar.gz
sudo mv gost /usr/local/bin/

# go-exploitdb (Exploit DB)
VERSION="0.2.0"
wget https://github.com/vulsio/go-exploitdb/releases/download/v${VERSION}/go-exploitdb_${VERSION}_linux_amd64.tar.gz
tar -xzf go-exploitdb_${VERSION}_linux_amd64.tar.gz
sudo mv go-exploitdb /usr/local/bin/

# Vérifier installations
vuls version
go-cve-dictionary version
goval-dictionary version
gost version
go-exploitdb version
```

### 2.2 Installation Docker (Alternative)

```bash
# Docker compose complet (Vuls + databases + VulsRepo)
mkdir -p ~/vuls
cd ~/vuls

# Télécharger docker-compose
wget https://raw.githubusercontent.com/future-architect/vuls/master/setup/docker/docker-compose.yml

# Éditer docker-compose.yml (ajuster volumes paths)
nano docker-compose.yml

# Start containers
docker-compose up -d

# Vérifier containers running
docker-compose ps

# Services :
# - vuls-server (scanner)
# - vulsrepo (dashboard web)
# - go-cve-dictionary (NVD DB)
# - goval-dictionary (OVAL DB)
# - gost (Security Tracker)
```

### 2.3 Structure Directories

```bash
# Créer structure directories Vuls
sudo mkdir -p /var/lib/vuls/{results,logs,cve,oval,gost,exploitdb}
sudo chown -R $USER:$USER /var/lib/vuls

# Structure :
/var/lib/vuls/
├── results/           # Scan results JSON
├── logs/              # Vuls logs
├── cve/               # NVD/JVN databases (SQLite)
├── oval/              # OVAL databases (SQLite)
├── gost/              # Gost databases (SQLite)
└── exploitdb/         # Exploit DB (SQLite)

# Configuration file
mkdir -p ~/.vuls
```

### 2.4 Téléchargement Databases

```bash
# IMPORTANT : Télécharger databases AVANT premier scan
# Databases volumineuses (~2-5 GB total)

# 1. NVD (National Vulnerability Database)
echo "Fetching NVD database (may take 30-60 minutes)..."
go-cve-dictionary fetch nvd --dbpath /var/lib/vuls/cve/cve.sqlite3

# Output :
# INFO[0001] Fetching... URL: https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2024.json.gz
# INFO[0045] Fetched: 15234 CVEs
# ...

# 2. OVAL (pour votre distribution)
# Ubuntu
goval-dictionary fetch ubuntu 22 --dbpath /var/lib/vuls/oval/oval.sqlite3
goval-dictionary fetch ubuntu 20 --dbpath /var/lib/vuls/oval/oval.sqlite3

# Debian
goval-dictionary fetch debian 11 --dbpath /var/lib/vuls/oval/oval.sqlite3
goval-dictionary fetch debian 12 --dbpath /var/lib/vuls/oval/oval.sqlite3

# RHEL/CentOS
goval-dictionary fetch redhat 8 --dbpath /var/lib/vuls/oval/oval.sqlite3
goval-dictionary fetch redhat 9 --dbpath /var/lib/vuls/oval/oval.sqlite3

# 3. Gost (Security Tracker)
gost fetch debian --dbpath /var/lib/vuls/gost/gost.sqlite3
gost fetch ubuntu --dbpath /var/lib/vuls/gost/gost.sqlite3
gost fetch redhat --dbpath /var/lib/vuls/gost/gost.sqlite3

# 4. Exploit DB (optionnel mais recommandé)
go-exploitdb fetch exploitdb --dbpath /var/lib/vuls/exploitdb/exploitdb.sqlite3
go-exploitdb fetch awesomepoc --dbpath /var/lib/vuls/exploitdb/exploitdb.sqlite3

# Vérifier tailles databases
du -sh /var/lib/vuls/*
# cve/         1.8G
# oval/        450M
# gost/        280M
# exploitdb/   120M
# Total: ~2.6GB
```

---

## Section 3 : Configuration Databases

### 3.1 Stratégie Update Databases

```bash
# Databases doivent être updated régulièrement
# NVD : ~100 nouveaux CVE/jour
# OVAL/Gost : Updates distributions hebdomadaires

# Script update automatique
sudo nano /usr/local/bin/vuls-update-db.sh

#!/bin/bash
# Vuls database update script

LOGFILE="/var/log/vuls/db-update.log"
mkdir -p /var/log/vuls

echo "=== Vuls DB Update - $(date) ===" | tee -a $LOGFILE

# 1. NVD update (incremental)
echo "Updating NVD..." | tee -a $LOGFILE
go-cve-dictionary fetch nvd \
    --dbpath /var/lib/vuls/cve/cve.sqlite3 \
    >> $LOGFILE 2>&1

# 2. OVAL update (current year only = faster)
echo "Updating OVAL Ubuntu 22..." | tee -a $LOGFILE
goval-dictionary fetch ubuntu 22 \
    --dbpath /var/lib/vuls/oval/oval.sqlite3 \
    >> $LOGFILE 2>&1

echo "Updating OVAL Debian 11..." | tee -a $LOGFILE
goval-dictionary fetch debian 11 \
    --dbpath /var/lib/vuls/oval/oval.sqlite3 \
    >> $LOGFILE 2>&1

# 3. Gost update
echo "Updating Gost..." | tee -a $LOGFILE
gost fetch ubuntu \
    --dbpath /var/lib/vuls/gost/gost.sqlite3 \
    >> $LOGFILE 2>&1

gost fetch debian \
    --dbpath /var/lib/vuls/gost/gost.sqlite3 \
    >> $LOGFILE 2>&1

# 4. ExploitDB update
echo "Updating ExploitDB..." | tee -a $LOGFILE
go-exploitdb fetch exploitdb \
    --dbpath /var/lib/vuls/exploitdb/exploitdb.sqlite3 \
    >> $LOGFILE 2>&1

echo "DB update completed" | tee -a $LOGFILE

# Permissions
sudo chmod +x /usr/local/bin/vuls-update-db.sh

# Cron : Daily update 2AM
sudo crontab -e
0 2 * * * /usr/local/bin/vuls-update-db.sh
```

### 3.2 Database Maintenance

```bash
# Optimiser databases SQLite (vacuum)
sudo nano /usr/local/bin/vuls-db-maintenance.sh

#!/bin/bash
# Optimize Vuls SQLite databases

echo "=== Vuls DB Maintenance ==="

# Backup databases avant maintenance
BACKUP_DIR="/var/backups/vuls-db-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR
cp /var/lib/vuls/cve/cve.sqlite3 $BACKUP_DIR/
cp /var/lib/vuls/oval/oval.sqlite3 $BACKUP_DIR/
cp /var/lib/vuls/gost/gost.sqlite3 $BACKUP_DIR/

echo "Databases backed up to $BACKUP_DIR"

# Vacuum databases (reclaim space)
echo "Vacuuming NVD database..."
sqlite3 /var/lib/vuls/cve/cve.sqlite3 "VACUUM;"

echo "Vacuuming OVAL database..."
sqlite3 /var/lib/vuls/oval/oval.sqlite3 "VACUUM;"

echo "Vacuuming Gost database..."
sqlite3 /var/lib/vuls/gost/gost.sqlite3 "VACUUM;"

# Stats
echo "Database sizes:"
du -sh /var/lib/vuls/cve/cve.sqlite3
du -sh /var/lib/vuls/oval/oval.sqlite3
du -sh /var/lib/vuls/gost/gost.sqlite3

echo "Maintenance completed"

# Permissions
sudo chmod +x /usr/local/bin/vuls-db-maintenance.sh

# Cron : Monthly
# 0 4 1 * * /usr/local/bin/vuls-db-maintenance.sh
```

---

## Section 4 : Configuration Scans

### 4.1 Configuration File (config.toml)

```bash
# Créer configuration scan
nano ~/.vuls/config.toml

# Configuration production :

[cveDict]
type = "sqlite3"
SQLite3Path = "/var/lib/vuls/cve/cve.sqlite3"

[ovalDict]
type = "sqlite3"
SQLite3Path = "/var/lib/vuls/oval/oval.sqlite3"

[gost]
type = "sqlite3"
SQLite3Path = "/var/lib/vuls/gost/gost.sqlite3"

[exploit]
type = "sqlite3"
SQLite3Path = "/var/lib/vuls/exploitdb/exploitdb.sqlite3"

[slack]
hookURL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
channel = "#security-alerts"
iconEmoji = ":ghost:"
authUser = "vuls"

[email]
smtpAddr = "smtp.example.com"
smtpPort = "587"
user = "vuls@example.com"
password = "password"
from = "vuls@example.com"
to = ["security@example.com"]
subjectPrefix = "[Vuls Alert]"

[default]
port = "22"
user = "vulsuser"
keyPath = "/home/vulsuser/.ssh/id_rsa"

# === SERVERS ===

# Local scan
[servers.localhost]
host = "127.0.0.1"
port = "local"

# Remote server SSH
[servers.web-prod-01]
host = "192.168.1.10"
port = "22"
user = "vulsuser"
keyPath = "/home/vulsuser/.ssh/id_rsa"

[servers.db-prod-01]
host = "192.168.1.20"
port = "22"
user = "vulsuser"

# Container scan
[servers.docker-app]
host = "192.168.1.30"
port = "22"
containers = ["nginx:latest", "mysql:8.0"]
```

### 4.2 SSH Key Setup (Agentless)

```bash
# Créer user vuls sur scanner host
sudo useradd -m -s /bin/bash vulsuser
sudo su - vulsuser

# Générer SSH key
ssh-keygen -t ed25519 -C "vuls-scanner" -f ~/.ssh/id_rsa
# Pas de passphrase (automated scanning)

# Copier clé vers target servers
ssh-copy-id -i ~/.ssh/id_rsa.pub user@192.168.1.10
ssh-copy-id -i ~/.ssh/id_rsa.pub user@192.168.1.20

# Test connexion
ssh -i ~/.ssh/id_rsa user@192.168.1.10 'uname -a'

# Permissions target servers (sudo sans password pour scan)
# Sur chaque target server :
sudo visudo

# Ajouter (permet scan packages sans password) :
vulsuser ALL=(ALL) NOPASSWD: /usr/bin/apt-cache, /usr/bin/dpkg, /usr/bin/rpm, /usr/bin/yum, /bin/cat /etc/redhat-release, /bin/cat /etc/os-release

# Ou full sudo (moins sécurisé mais plus simple) :
vulsuser ALL=(ALL) NOPASSWD: ALL
```

### 4.3 Configuration Avancée (Multi-Environment)

```bash
# Séparer configs par environnement
mkdir -p ~/.vuls/{prod,staging,dev}

# config-prod.toml
nano ~/.vuls/prod/config.toml

[servers.web-prod-01]
host = "10.0.1.10"
# ...

[servers.db-prod-01]
host = "10.0.1.20"
# ...

# config-staging.toml
nano ~/.vuls/staging/config.toml

[servers.web-staging-01]
host = "10.0.2.10"
# ...

# Scan environnement spécifique
vuls scan -config ~/.vuls/prod/config.toml
vuls scan -config ~/.vuls/staging/config.toml
```

---

## Section 5 : Modes Scan

### 5.1 Scan Local

```bash
# Scan serveur local (où Vuls installé)

# config.toml
[servers.localhost]
host = "127.0.0.1"
port = "local"

# Scanner
vuls scan localhost

# Output :
# INFO[0000] Start scanning
# INFO[0000] Scanning... localhost
# INFO[0005] Scanning... Finished
# INFO[0005] Reporting...
# localhost (ubuntu22.04)
# ========================
# Total: 45 (High:12 Medium:25 Low:8), 15/45 Fixed

# Report détaillé
vuls report -format-full-text

# Output exemple :
# localhost (ubuntu22.04)
# ========================
# Total: 45 (High:12 Medium:25 Low:8), 15/45 Fixed
# 
# CVE-2023-12345 (CVSS 9.8)
# Package : openssl
# Installed : 3.0.2-0ubuntu1.10
# Fixed : 3.0.2-0ubuntu1.12
# https://ubuntu.com/security/CVE-2023-12345
# 
# CVE-2022-67890 (CVSS 7.5)
# Package : nginx
# ...
```

### 5.2 Scan Remote SSH

```bash
# Scanner serveurs distants via SSH

# config.toml
[servers.web-prod-01]
host = "192.168.1.10"
port = "22"
user = "vulsuser"

[servers.db-prod-01]
host = "192.168.1.20"

# Scanner tous serveurs
vuls scan

# Scanner serveur spécifique
vuls scan web-prod-01

# Scanner multiple servers parallèle
vuls scan web-prod-01 db-prod-01

# Options scan
vuls scan \
    --config=~/.vuls/config.toml \
    --results-dir=/var/lib/vuls/results \
    --log-dir=/var/lib/vuls/logs \
    --debug

# Mode fast-scan (skip changelog)
vuls scan --fast

# Mode deep-scan (full package info)
vuls scan --deep
```

### 5.3 Scan Containers

```bash
# Scanner containers Docker

# config.toml
[servers.docker-host]
host = "192.168.1.30"
port = "22"
containers = ["nginx:latest", "mysql:8.0", "redis:7"]

# OU containers running (auto-detect)
containers = ["running"]

# OU all containers
containers = ["all"]

# Scanner
vuls scan docker-host

# Output :
# INFO Scanning... docker-host
# INFO Scanning container: nginx:latest
# INFO Scanning container: mysql:8.0
# 
# docker-host (ubuntu22.04)
# Container: nginx:latest (debian11)
#   Total: 23 (High:5 Medium:15 Low:3)
#   CVE-2023-... (nginx 1.21.0)
# 
# Container: mysql:8.0 (debian11)
#   Total: 18 (High:3 Medium:12 Low:3)
#   CVE-2022-... (mysql-server 8.0.28)
```

### 5.4 Scan Images Docker

```bash
# Scanner images Docker avant deploy (CI/CD)

# Option 1 : Scan image locale
vuls scan \
    --containers-only \
    myapp:latest

# Option 2 : config.toml
[servers.ci-scanner]
host = "localhost"
port = "local"
containers = ["myapp:latest", "myapp:1.2.3"]

# CI/CD Pipeline (GitLab CI exemple)
.gitlab-ci.yml :

security-scan:
  stage: test
  script:
    - docker build -t myapp:${CI_COMMIT_SHA} .
    - vuls scan --containers-only myapp:${CI_COMMIT_SHA}
    - vuls report -format-json -to-localfile
    - |
      HIGH_COUNT=$(jq '.[] | select(.ScannedCves[].CveDetail.Cvss3Score >= 7.0) | .ScannedCves | length' results/current/*.json | paste -sd+ | bc)
      if [ "$HIGH_COUNT" -gt 0 ]; then
        echo "High severity vulnerabilities found: $HIGH_COUNT"
        exit 1
      fi
```

---

## Section 6 : Reporting et Analyse

### 6.1 Formats Report

```bash
# Format text (human-readable)
vuls report -format-full-text

# Format JSON (machine-readable)
vuls report -format-json -to-localfile

# Output : results/YYYY-MM-DD_HH-MM-SS/*.json

# Format CSV
vuls report -format-csv

# Format one-line-text (CI/CD)
vuls report -format-one-line-text

# Output exemple :
# web-prod-01 Total: 45 (High:12 Medium:25 Low:8) 15/45 Fixed

# Format short-text (summary)
vuls report -format-short-text
```

### 6.2 Filtres Report

```bash
# Filter par sévérité CVSS
vuls report \
    -cvss-over=7.0 \
    -format-full-text

# Seulement CVE critiques (9.0+)
vuls report -cvss-over=9.0

# Filter par confidence
vuls report -confidence-over=80

# Ignorer unfixed CVE (pas de patch disponible)
vuls report -ignore-unfixed

# Ignorer unscored CVE (pas de CVSS)
vuls report -ignore-unscored

# Filter par package
vuls report -cvedb-path /var/lib/vuls/cve/cve.sqlite3 | grep "openssl"

# Report differential (nouveaux CVE seulement)
vuls report \
    -diff \
    -diff-minus=results/2024-01-15_03-00-00 \
    -diff-plus=results/2024-01-16_03-00-00
```

### 6.3 Parser Résultats JSON

```bash
# Analyse JSON avec jq

# Extraire tous CVE critiques
jq '.[] | select(.ScannedCves[].CveDetail.Cvss3Score >= 9.0) | {
  server: .ServerName,
  cve: .ScannedCves[].CveDetail.CveID,
  score: .ScannedCves[].CveDetail.Cvss3Score,
  package: .ScannedCves[].AffectedPackages[].Name
}' results/current/localhost.json

# Count CVE par sévérité
jq '.[] | .ScannedCves[] | 
  if .CveDetail.Cvss3Score >= 9.0 then "Critical"
  elif .CveDetail.Cvss3Score >= 7.0 then "High"
  elif .CveDetail.Cvss3Score >= 4.0 then "Medium"
  else "Low" end' results/current/*.json | \
  sort | uniq -c

# Output :
#  5 Critical
# 12 High
# 25 Medium
#  8 Low

# Liste packages avec CVE
jq -r '.[] | .ScannedCves[] | 
  "\(.CveDetail.CveID) | \(.AffectedPackages[].Name) | \(.CveDetail.Cvss3Score)"' \
  results/current/*.json | \
  sort -t'|' -k3 -rn | \
  head -20
```

### 6.4 Script Report Custom

```bash
#!/bin/bash
# vuls-custom-report.sh

JSON_FILE="$1"

echo "=== Vuls Custom Report ==="
echo "Date: $(date)"
echo ""

# Server info
SERVER=$(jq -r '.[].ServerName' $JSON_FILE)
FAMILY=$(jq -r '.[].Family' $JSON_FILE)
RELEASE=$(jq -r '.[].Release' $JSON_FILE)

echo "Server: $SERVER"
echo "OS: $FAMILY $RELEASE"
echo ""

# CVE statistics
TOTAL=$(jq '[.[].ScannedCves[]] | length' $JSON_FILE)
CRITICAL=$(jq '[.[].ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0)] | length' $JSON_FILE)
HIGH=$(jq '[.[].ScannedCves[] | select(.CveDetail.Cvss3Score >= 7.0 and .CveDetail.Cvss3Score < 9.0)] | length' $JSON_FILE)
MEDIUM=$(jq '[.[].ScannedCves[] | select(.CveDetail.Cvss3Score >= 4.0 and .CveDetail.Cvss3Score < 7.0)] | length' $JSON_FILE)
LOW=$(jq '[.[].ScannedCves[] | select(.CveDetail.Cvss3Score < 4.0)] | length' $JSON_FILE)

echo "=== CVE Summary ==="
echo "Total CVE: $TOTAL"
echo "Critical (9.0+): $CRITICAL"
echo "High (7.0-8.9): $HIGH"
echo "Medium (4.0-6.9): $MEDIUM"
echo "Low (0.0-3.9): $LOW"
echo ""

# Top 10 critical
echo "=== Top 10 Critical CVE ==="
jq -r '.[].ScannedCves[] | 
  select(.CveDetail.Cvss3Score >= 9.0) | 
  "\(.CveDetail.CveID) | \(.CveDetail.Cvss3Score) | \(.AffectedPackages[].Name)"' \
  $JSON_FILE | \
  head -10 | \
  column -t -s'|'

echo ""

# Packages affected
echo "=== Most Affected Packages ==="
jq -r '.[].ScannedCves[].AffectedPackages[].Name' $JSON_FILE | \
  sort | uniq -c | sort -rn | head -10

# Usage
# ./vuls-custom-report.sh results/current/localhost.json
```

---

## Section 7 : Dashboard VulsRepo

### 7.1 Installation VulsRepo

```bash
# VulsRepo = Dashboard web React pour visualisation

# Méthode 1 : Docker (recommandé)
cd ~/vuls
git clone https://github.com/ishiDACo/vulsrepo.git
cd vulsrepo

# Build Docker image
docker build -t vulsrepo .

# Run container
docker run -d \
    -p 5111:5111 \
    -v /var/lib/vuls/results:/vuls/results:ro \
    --name vulsrepo \
    vulsrepo

# Accès web
# http://localhost:5111

# Méthode 2 : Standalone
git clone https://github.com/ishiDACo/vulsrepo.git
cd vulsrepo

# Configuration
nano vulsrepo-config.toml

[Server]
rootPath = "/var/lib/vuls/results"
resultsPath = "/var/lib/vuls/results"
serverPort = "5111"

# Start server
./vulsrepo-server

# Accès web
# http://localhost:5111
```

### 7.2 Configuration VulsRepo

```bash
# Configuration avancée
nano vulsrepo-config.toml

[Server]
rootPath = "/var/lib/vuls"
resultsPath = "/var/lib/vuls/results"
serverPort = "5111"
serverIP = "0.0.0.0"  # Listen all interfaces

[Auth]
authFilePath = "./vulsrepo-auth.toml"

# Authentication (optionnel)
nano vulsrepo-auth.toml

[Users]
[[Users.user]]
username = "admin"
password = "$2a$10$..." # bcrypt hash
permissions = ["admin"]

[[Users.user]]
username = "viewer"
password = "$2a$10$..."
permissions = ["read"]

# Générer bcrypt hash
htpasswd -bnBC 10 "" password | tr -d ':\n'
```

### 7.3 Utilisation Dashboard

```bash
# Features VulsRepo dashboard :

1. Server List
   ├─ Vue ensemble tous serveurs scannés
   ├─ CVE count par server
   ├─ Trending (augmentation/diminution)
   └─ Last scan date

2. Server Detail
   ├─ Liste CVE avec CVSS score
   ├─ Filter par sévérité
   ├─ Search CVE ID
   └─ Export CSV/JSON

3. CVE Detail
   ├─ CVE description complète
   ├─ CVSS vector string
   ├─ Affected packages
   ├─ References (NVD, vendor advisories)
   ├─ Exploits disponibles (ExploitDB)
   └─ Fix available (version patched)

4. Timeline View
   ├─ Évolution CVE dans temps
   ├─ Nouveaux CVE détectés
   ├─ CVE fixed (patched)
   └─ Comparaison scans

5. Statistics
   ├─ Distribution CVSS scores
   ├─ Top affected packages
   ├─ CVE by year
   └─ Fix rate (% patched)

# Screenshot workflow :
# 1. Login → http://localhost:5111
# 2. Select server → web-prod-01
# 3. Filter → Critical (9.0+)
# 4. Click CVE → CVE-2023-12345
# 5. View exploit → ExploitDB #12345
# 6. Export report → CSV download
```

### 7.4 Nginx Reverse Proxy (Production)

```bash
# Exposer VulsRepo via Nginx avec HTTPS

# /etc/nginx/sites-available/vulsrepo
server {
    listen 443 ssl http2;
    server_name vuls.example.com;

    ssl_certificate /etc/letsencrypt/live/vuls.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vuls.example.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Basic auth (additional security)
    auth_basic "Vuls Dashboard";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://127.0.0.1:5111;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Activer site
sudo ln -s /etc/nginx/sites-available/vulsrepo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Créer htpasswd
sudo htpasswd -c /etc/nginx/.htpasswd admin

# Accès : https://vuls.example.com
```

---

## Section 8 : Intégration CI/CD

### 8.1 GitLab CI Pipeline

```yaml
# .gitlab-ci.yml

stages:
  - build
  - security
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

vuls-scan:
  stage: security
  image: vuls/vuls:latest
  script:
    # Update databases
    - go-cve-dictionary fetch nvd --dbpath /tmp/cve.sqlite3
    - goval-dictionary fetch ubuntu 22 --dbpath /tmp/oval.sqlite3
    
    # Pull image to scan
    - docker pull $DOCKER_IMAGE
    
    # Create config
    - |
      cat > config.toml <<EOF
      [cveDict]
      type = "sqlite3"
      SQLite3Path = "/tmp/cve.sqlite3"
      
      [ovalDict]
      type = "sqlite3"
      SQLite3Path = "/tmp/oval.sqlite3"
      
      [servers.docker-image]
      host = "localhost"
      port = "local"
      containers = ["$DOCKER_IMAGE"]
      EOF
    
    # Scan
    - vuls scan -config config.toml
    - vuls report -format-json -to-localfile
    
    # Parse results
    - |
      CRITICAL=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0)] | length' results/current/*.json)
      HIGH=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 7.0 and .CveDetail.Cvss3Score < 9.0)] | length' results/current/*.json)
      
      echo "Critical CVE: $CRITICAL"
      echo "High CVE: $HIGH"
      
      # Fail si critical CVE
      if [ "$CRITICAL" -gt 0 ]; then
        echo "❌ CRITICAL vulnerabilities found - blocking deploy"
        exit 1
      fi
      
      # Warning si high CVE
      if [ "$HIGH" -gt 5 ]; then
        echo "⚠️ WARNING: $HIGH high severity vulnerabilities"
      fi
  
  artifacts:
    paths:
      - results/
    expire_in: 30 days
  
  allow_failure: false

deploy:
  stage: deploy
  needs: ["vuls-scan"]
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE
  only:
    - main
```

### 8.2 GitHub Actions

```yaml
# .github/workflows/security-scan.yml

name: Vuls Security Scan

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily 2AM

jobs:
  vuls-scan:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
      
      - name: Setup Vuls
        run: |
          # Download Vuls
          wget https://github.com/future-architect/vuls/releases/download/v0.27.0/vuls_0.27.0_linux_amd64.tar.gz
          tar -xzf vuls_0.27.0_linux_amd64.tar.gz
          sudo mv vuls /usr/local/bin/
          
          # Download databases tools
          wget https://github.com/vulsio/go-cve-dictionary/releases/download/v0.10.0/go-cve-dictionary_0.10.0_linux_amd64.tar.gz
          tar -xzf go-cve-dictionary_0.10.0_linux_amd64.tar.gz
          sudo mv go-cve-dictionary /usr/local/bin/
      
      - name: Update databases
        run: |
          go-cve-dictionary fetch nvd --dbpath /tmp/cve.sqlite3
      
      - name: Create config
        run: |
          cat > config.toml <<EOF
          [cveDict]
          type = "sqlite3"
          SQLite3Path = "/tmp/cve.sqlite3"
          
          [servers.docker-image]
          host = "localhost"
          port = "local"
          containers = ["myapp:${{ github.sha }}"]
          EOF
      
      - name: Run Vuls scan
        run: |
          vuls scan -config config.toml
          vuls report -format-json -to-localfile
      
      - name: Parse results
        run: |
          CRITICAL=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0)] | length' results/current/*.json)
          HIGH=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 7.0 and .CveDetail.Cvss3Score < 9.0)] | length' results/current/*.json)
          
          echo "::set-output name=critical::$CRITICAL"
          echo "::set-output name=high::$HIGH"
          
          if [ "$CRITICAL" -gt 0 ]; then
            echo "::error::Critical vulnerabilities found"
            exit 1
          fi
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: vuls-results
          path: results/
      
      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('results/current/docker-image.json'));
            const critical = results[0].ScannedCves.filter(c => c.CveDetail.Cvss3Score >= 9.0).length;
            const high = results[0].ScannedCves.filter(c => c.CveDetail.Cvss3Score >= 7.0 && c.CveDetail.Cvss3Score < 9.0).length;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🔒 Vuls Security Scan Results\n\n**Critical:** ${critical}\n**High:** ${high}\n\nFull report available in artifacts.`
            });
```

### 8.3 Jenkins Pipeline

```groovy
// Jenkinsfile

pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "myapp:${env.BUILD_ID}"
        VULS_CONFIG = "config.toml"
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    docker.build(env.DOCKER_IMAGE)
                }
            }
        }
        
        stage('Vuls Scan') {
            agent {
                docker {
                    image 'vuls/vuls:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh '''
                    # Update databases
                    go-cve-dictionary fetch nvd --dbpath /tmp/cve.sqlite3
                    
                    # Create config
                    cat > ${VULS_CONFIG} <<EOF
[cveDict]
type = "sqlite3"
SQLite3Path = "/tmp/cve.sqlite3"

[servers.docker-image]
host = "localhost"
port = "local"
containers = ["${DOCKER_IMAGE}"]
EOF
                    
                    # Scan
                    vuls scan -config ${VULS_CONFIG}
                    vuls report -format-json -to-localfile
                    
                    # Parse
                    CRITICAL=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0)] | length' results/current/*.json)
                    
                    if [ "$CRITICAL" -gt 0 ]; then
                        echo "Critical vulnerabilities found"
                        exit 1
                    fi
                '''
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'kubectl set image deployment/app app=${DOCKER_IMAGE}'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'results/**/*.json', fingerprint: true
        }
        failure {
            emailext (
                subject: "Vuls Scan Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Critical vulnerabilities detected. Check artifacts.",
                to: "security@example.com"
            )
        }
    }
}
```

## Section 9 : Automatisation et Monitoring

### 9.1 Scan Automatique Quotidien

```bash
#!/bin/bash
# /usr/local/bin/vuls-daily-scan.sh
# Production automated scanning

set -euo pipefail

# Configuration
CONFIG="/home/vulsuser/.vuls/config.toml"
RESULTS_DIR="/var/lib/vuls/results"
LOG_DIR="/var/lib/vuls/logs"
ALERT_EMAIL="security@example.com"
SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
LOGFILE="$LOG_DIR/scan-$DATE.log"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOGFILE"
}

log "=== Vuls Daily Scan Started ==="

# 1. Update databases
log "Updating CVE databases..."
go-cve-dictionary fetch nvd --dbpath /var/lib/vuls/cve/cve.sqlite3 >> "$LOGFILE" 2>&1
goval-dictionary fetch ubuntu 22 --dbpath /var/lib/vuls/oval/oval.sqlite3 >> "$LOGFILE" 2>&1
gost fetch ubuntu --dbpath /var/lib/vuls/gost/gost.sqlite3 >> "$LOGFILE" 2>&1

# 2. Run scan
log "Starting vulnerability scan..."
vuls scan \
    -config="$CONFIG" \
    -results-dir="$RESULTS_DIR" \
    -log-dir="$LOG_DIR" \
    >> "$LOGFILE" 2>&1

# 3. Generate reports
log "Generating reports..."
vuls report \
    -config="$CONFIG" \
    -results-dir="$RESULTS_DIR" \
    -format-json \
    -to-localfile \
    >> "$LOGFILE" 2>&1

# 4. Parse results
LATEST_RESULT=$(find "$RESULTS_DIR" -name "*.json" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)

TOTAL_CVE=$(jq '[.[] | .ScannedCves[]] | length' "$LATEST_RESULT")
CRITICAL=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0)] | length' "$LATEST_RESULT")
HIGH=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 7.0 and .CveDetail.Cvss3Score < 9.0)] | length' "$LATEST_RESULT")
MEDIUM=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 4.0 and .CveDetail.Cvss3Score < 7.0)] | length' "$LATEST_RESULT")
LOW=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score < 4.0)] | length' "$LATEST_RESULT")

log "Scan completed - Total: $TOTAL_CVE (Critical: $CRITICAL, High: $HIGH, Medium: $MEDIUM, Low: $LOW)"

# 5. Alertes si critical/high
if [ "$CRITICAL" -gt 0 ] || [ "$HIGH" -gt 10 ]; then
    SEVERITY="CRITICAL"
    
    # Email alert
    {
        echo "Subject: 🚨 Vuls Alert - $SEVERITY Vulnerabilities Detected"
        echo ""
        echo "Scan Date: $DATE"
        echo ""
        echo "=== Summary ==="
        echo "Total CVE: $TOTAL_CVE"
        echo "Critical (9.0+): $CRITICAL"
        echo "High (7.0-8.9): $HIGH"
        echo "Medium (4.0-6.9): $MEDIUM"
        echo "Low (0.0-3.9): $LOW"
        echo ""
        echo "=== Top 10 Critical CVE ==="
        jq -r '.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0) | "\(.CveDetail.CveID) | \(.CveDetail.Cvss3Score) | \(.AffectedPackages[].Name)"' "$LATEST_RESULT" | head -10
        echo ""
        echo "Full report: https://vuls.example.com"
    } | sendmail "$ALERT_EMAIL"
    
    # Slack notification
    SLACK_MESSAGE=$(cat <<EOF
{
  "text": "🚨 *Vuls Alert - Critical Vulnerabilities*",
  "attachments": [
    {
      "color": "danger",
      "fields": [
        {"title": "Critical", "value": "$CRITICAL", "short": true},
        {"title": "High", "value": "$HIGH", "short": true},
        {"title": "Medium", "value": "$MEDIUM", "short": true},
        {"title": "Low", "value": "$LOW", "short": true}
      ],
      "footer": "Vuls Scanner",
      "ts": $(date +%s)
    }
  ]
}
EOF
)
    
    curl -X POST -H 'Content-type: application/json' \
        --data "$SLACK_MESSAGE" \
        "$SLACK_WEBHOOK" 2>/dev/null
fi

# 6. Cleanup old results (>90 days)
log "Cleaning old results..."
find "$RESULTS_DIR" -name "*.json" -mtime +90 -delete
find "$LOG_DIR" -name "scan-*.log" -mtime +90 -delete

log "=== Vuls Daily Scan Completed ==="

# Permissions
chmod +x /usr/local/bin/vuls-daily-scan.sh

# Cron : Daily 3AM
crontab -e
0 3 * * * /usr/local/bin/vuls-daily-scan.sh
```

### 9.2 Monitoring Prometheus

```bash
# Vuls Prometheus exporter
# /usr/local/bin/vuls-prometheus-exporter.sh

#!/bin/bash
# Export Vuls metrics to Prometheus

RESULTS_DIR="/var/lib/vuls/results"
METRICS_FILE="/var/lib/prometheus/node-exporter/vuls.prom"

# Get latest results
LATEST=$(find "$RESULTS_DIR" -name "*.json" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)

if [ -z "$LATEST" ]; then
    exit 0
fi

# Parse metrics
TOTAL=$(jq '[.[] | .ScannedCves[]] | length' "$LATEST")
CRITICAL=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0)] | length' "$LATEST")
HIGH=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 7.0 and .CveDetail.Cvss3Score < 9.0)] | length' "$LATEST")
MEDIUM=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 4.0 and .CveDetail.Cvss3Score < 7.0)] | length' "$LATEST")
LOW=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score < 4.0)] | length' "$LATEST")
LAST_SCAN=$(jq -r '.[].ScannedAt' "$LATEST" | head -1)
TIMESTAMP=$(date -d "$LAST_SCAN" +%s)

# Generate Prometheus metrics
cat > "$METRICS_FILE" <<EOF
# HELP vuls_vulnerabilities_total Total number of vulnerabilities detected
# TYPE vuls_vulnerabilities_total gauge
vuls_vulnerabilities_total $TOTAL

# HELP vuls_vulnerabilities_by_severity Number of vulnerabilities by severity
# TYPE vuls_vulnerabilities_by_severity gauge
vuls_vulnerabilities_by_severity{severity="critical"} $CRITICAL
vuls_vulnerabilities_by_severity{severity="high"} $HIGH
vuls_vulnerabilities_by_severity{severity="medium"} $MEDIUM
vuls_vulnerabilities_by_severity{severity="low"} $LOW

# HELP vuls_last_scan_timestamp Timestamp of last scan
# TYPE vuls_last_scan_timestamp gauge
vuls_last_scan_timestamp $TIMESTAMP
EOF

# Cron : Every 5 minutes
# */5 * * * * /usr/local/bin/vuls-prometheus-exporter.sh

# Prometheus alerting rules
# /etc/prometheus/rules/vuls.yml
groups:
  - name: vuls
    interval: 5m
    rules:
      - alert: VulsCriticalVulnerabilities
        expr: vuls_vulnerabilities_by_severity{severity="critical"} > 0
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Critical vulnerabilities detected"
          description: "{{ $value }} critical CVE found on {{ $labels.instance }}"
      
      - alert: VulsHighVulnerabilities
        expr: vuls_vulnerabilities_by_severity{severity="high"} > 10
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "High vulnerabilities threshold exceeded"
          description: "{{ $value }} high severity CVE found"
```

### 9.3 Differential Scanning

```bash
#!/bin/bash
# vuls-diff-scan.sh
# Detect NEW vulnerabilities since last scan

RESULTS_DIR="/var/lib/vuls/results"

# Get last 2 scans
SCANS=($(find "$RESULTS_DIR" -name "*.json" -type f -printf '%T@ %p\n' | sort -rn | head -2 | cut -d' ' -f2-))

if [ ${#SCANS[@]} -lt 2 ]; then
    echo "Not enough scans for comparison"
    exit 0
fi

LATEST="${SCANS[0]}"
PREVIOUS="${SCANS[1]}"

echo "=== Vuls Differential Report ==="
echo "Comparing:"
echo "  Previous: $(basename $PREVIOUS)"
echo "  Latest:   $(basename $LATEST)"
echo ""

# Extract CVE IDs
PREVIOUS_CVES=$(jq -r '.[] | .ScannedCves[].CveDetail.CveID' "$PREVIOUS" | sort -u)
LATEST_CVES=$(jq -r '.[] | .ScannedCves[].CveDetail.CveID' "$LATEST" | sort -u)

# New CVE (in latest but not in previous)
NEW_CVES=$(comm -13 <(echo "$PREVIOUS_CVES") <(echo "$LATEST_CVES"))
NEW_COUNT=$(echo "$NEW_CVES" | grep -c '^')

# Fixed CVE (in previous but not in latest)
FIXED_CVES=$(comm -23 <(echo "$PREVIOUS_CVES") <(echo "$LATEST_CVES"))
FIXED_COUNT=$(echo "$FIXED_CVES" | grep -c '^')

echo "=== Summary ==="
echo "New vulnerabilities: $NEW_COUNT"
echo "Fixed vulnerabilities: $FIXED_COUNT"
echo ""

if [ $NEW_COUNT -gt 0 ]; then
    echo "=== New CVE Detected ==="
    for CVE in $NEW_CVES; do
        SCORE=$(jq -r ".[] | .ScannedCves[] | select(.CveDetail.CveID == \"$CVE\") | .CveDetail.Cvss3Score" "$LATEST" | head -1)
        PACKAGE=$(jq -r ".[] | .ScannedCves[] | select(.CveDetail.CveID == \"$CVE\") | .AffectedPackages[].Name" "$LATEST" | head -1)
        echo "$CVE | CVSS $SCORE | $PACKAGE"
    done
    echo ""
fi

if [ $FIXED_COUNT -gt 0 ]; then
    echo "=== Fixed CVE ==="
    echo "$FIXED_CVES"
    echo ""
fi

# Alert si nouveaux critiques
NEW_CRITICAL=$(echo "$NEW_CVES" | while read CVE; do
    jq -r ".[] | .ScannedCves[] | select(.CveDetail.CveID == \"$CVE\" and .CveDetail.Cvss3Score >= 9.0) | .CveDetail.CveID" "$LATEST"
done | grep -c '^' || true)

if [ $NEW_CRITICAL -gt 0 ]; then
    echo "⚠️ WARNING: $NEW_CRITICAL new CRITICAL vulnerabilities detected!"
    # Send alert
fi
```

### 9.4 Trending Analysis

```bash
#!/bin/bash
# vuls-trending.sh
# Analyze vulnerability trends over time

RESULTS_DIR="/var/lib/vuls/results"
OUTPUT_FILE="/var/www/html/vuls-trending.csv"

echo "Date,Total,Critical,High,Medium,Low" > "$OUTPUT_FILE"

# Parse all historical scans (last 30 days)
find "$RESULTS_DIR" -name "*.json" -mtime -30 -type f | sort | while read RESULT; do
    DATE=$(jq -r '.[].ScannedAt' "$RESULT" | head -1 | cut -d'T' -f1)
    TOTAL=$(jq '[.[] | .ScannedCves[]] | length' "$RESULT")
    CRITICAL=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0)] | length' "$RESULT")
    HIGH=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 7.0 and .CveDetail.Cvss3Score < 9.0)] | length' "$RESULT")
    MEDIUM=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 4.0 and .CveDetail.Cvss3Score < 7.0)] | length' "$RESULT")
    LOW=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score < 4.0)] | length' "$RESULT")
    
    echo "$DATE,$TOTAL,$CRITICAL,$HIGH,$MEDIUM,$LOW" >> "$OUTPUT_FILE"
done

# Generate HTML chart
cat > /var/www/html/vuls-trending.html <<'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Vuls Vulnerability Trending</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Vulnerability Trends (Last 30 Days)</h1>
    <canvas id="trendChart" width="800" height="400"></canvas>
    
    <script>
    fetch('vuls-trending.csv')
        .then(response => response.text())
        .then(data => {
            const rows = data.split('\n').slice(1).filter(r => r);
            const labels = rows.map(r => r.split(',')[0]);
            const critical = rows.map(r => parseInt(r.split(',')[2]));
            const high = rows.map(r => parseInt(r.split(',')[3]));
            const medium = rows.map(r => parseInt(r.split(',')[4]));
            const low = rows.map(r => parseInt(r.split(',')[5]));
            
            new Chart(document.getElementById('trendChart'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Critical',
                            data: critical,
                            borderColor: 'rgb(220, 53, 69)',
                            backgroundColor: 'rgba(220, 53, 69, 0.1)'
                        },
                        {
                            label: 'High',
                            data: high,
                            borderColor: 'rgb(255, 193, 7)',
                            backgroundColor: 'rgba(255, 193, 7, 0.1)'
                        },
                        {
                            label: 'Medium',
                            data: medium,
                            borderColor: 'rgb(0, 123, 255)',
                            backgroundColor: 'rgba(0, 123, 255, 0.1)'
                        },
                        {
                            label: 'Low',
                            data: low,
                            borderColor: 'rgb(40, 167, 69)',
                            backgroundColor: 'rgba(40, 167, 69, 0.1)'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
    </script>
</body>
</html>
EOF

echo "Trending report: http://your-server/vuls-trending.html"
```

---

## Section 10 : Patch Management Workflow

### 10.1 Prioritization Matrix

```bash
# Matrice priorisation patches

┌─────────────────────────────────────────────────────┐
│            Patch Priority Matrix                    │
├──────────────┬──────────────────────────────────────┤
│ CVSS 9.0-10.0│ CRITICAL - Patch Immediately (24h)  │
│ + Exploit    │ - Stop services if needed            │
│              │ - Emergency change window            │
├──────────────┼──────────────────────────────────────┤
│ CVSS 7.0-8.9 │ HIGH - Urgent (7 days)               │
│ + Public     │ - Schedule maintenance window        │
│              │ - Test patch staging first           │
├──────────────┼──────────────────────────────────────┤
│ CVSS 4.0-6.9 │ MEDIUM - Normal (30 days)            │
│              │ - Include in monthly patching        │
│              │ - Full testing cycle                 │
├──────────────┼──────────────────────────────────────┤
│ CVSS 0.1-3.9 │ LOW - Planned (90 days)              │
│              │ - Quarterly patching cycle           │
│              │ - May defer if mitigated             │
└──────────────┴──────────────────────────────────────┘

Facteurs supplémentaires priorité :
✓ Exploit public disponible (+2 priority)
✓ Service exposé Internet (+1 priority)
✓ Données sensibles traitées (+1 priority)
✓ Compliance requirement (PCI-DSS) (+1 priority)
✗ Service interne seulement (-1 priority)
✗ Mitigation disponible (firewall rule) (-1 priority)
```

### 10.2 Script Triage Automatique

```bash
#!/bin/bash
# vuls-patch-triage.sh
# Automatic patch prioritization

RESULTS_DIR="/var/lib/vuls/results"
OUTPUT="/tmp/patch-priorities.txt"

LATEST=$(find "$RESULTS_DIR" -name "*.json" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)

echo "=== Patch Management Triage Report ===" > "$OUTPUT"
echo "Date: $(date)" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Priority 1: Critical + Exploit
echo "=== PRIORITY 1 - CRITICAL + EXPLOIT (Patch Immediately) ===" >> "$OUTPUT"
jq -r '.[] | .ScannedCves[] | 
    select(.CveDetail.Cvss3Score >= 9.0 and .Exploits != null and (.Exploits | length > 0)) |
    "\(.CveDetail.CveID) | CVSS \(.CveDetail.Cvss3Score) | \(.AffectedPackages[].Name) | \(.AffectedPackages[].NewVersion // "No fix") | Exploit: YES"' \
    "$LATEST" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Priority 2: Critical (no exploit yet)
echo "=== PRIORITY 2 - CRITICAL (Patch within 24-48h) ===" >> "$OUTPUT"
jq -r '.[] | .ScannedCves[] | 
    select(.CveDetail.Cvss3Score >= 9.0 and (.Exploits == null or (.Exploits | length == 0))) |
    "\(.CveDetail.CveID) | CVSS \(.CveDetail.Cvss3Score) | \(.AffectedPackages[].Name) | \(.AffectedPackages[].NewVersion // "No fix")"' \
    "$LATEST" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Priority 3: High + Public
echo "=== PRIORITY 3 - HIGH SEVERITY (Patch within 7 days) ===" >> "$OUTPUT"
jq -r '.[] | .ScannedCves[] | 
    select(.CveDetail.Cvss3Score >= 7.0 and .CveDetail.Cvss3Score < 9.0) |
    "\(.CveDetail.CveID) | CVSS \(.CveDetail.Cvss3Score) | \(.AffectedPackages[].Name) | \(.AffectedPackages[].NewVersion // "No fix")"' \
    "$LATEST" | head -20 >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Generate patching commands
echo "=== Suggested Patching Commands ===" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Ubuntu/Debian
echo "# Ubuntu/Debian:" >> "$OUTPUT"
jq -r '.[] | .ScannedCves[] | 
    select(.CveDetail.Cvss3Score >= 7.0 and .AffectedPackages[].NewVersion != null) |
    .AffectedPackages[].Name' "$LATEST" | \
    sort -u | \
    awk '{print "sudo apt install --only-upgrade " $1}' >> "$OUTPUT"
echo "" >> "$OUTPUT"

# RHEL/CentOS
echo "# RHEL/CentOS:" >> "$OUTPUT"
jq -r '.[] | .ScannedCves[] | 
    select(.CveDetail.Cvss3Score >= 7.0 and .AffectedPackages[].NewVersion != null) |
    .AffectedPackages[].Name' "$LATEST" | \
    sort -u | \
    awk '{print "sudo yum update " $1}' >> "$OUTPUT"

# Display report
cat "$OUTPUT"

# Email to security team
mail -s "Vuls Patch Triage Report - $(date +%Y-%m-%d)" security@example.com < "$OUTPUT"
```

### 10.3 Patch Workflow Complet

```bash
#!/bin/bash
# patch-workflow.sh
# Complete patching workflow with rollback

PACKAGE="$1"
ENVIRONMENT="${2:-production}"  # production, staging, dev

if [ -z "$PACKAGE" ]; then
    echo "Usage: $0 <package> [environment]"
    exit 1
fi

echo "=== Patch Workflow - $PACKAGE ==="
echo "Environment: $ENVIRONMENT"
echo ""

# 1. Pre-patch snapshot
echo "1. Creating pre-patch snapshot..."
if command -v lvcreate &> /dev/null; then
    sudo lvcreate -L 10G -s -n prepatch-$(date +%Y%m%d) /dev/vg0/root
    echo "LVM snapshot created"
elif command -v btrfs &> /dev/null; then
    sudo btrfs subvolume snapshot / /snapshots/prepatch-$(date +%Y%m%d)
    echo "BTRFS snapshot created"
else
    echo "WARNING: No snapshot capability - manual backup recommended"
fi

# 2. Check current version
echo ""
echo "2. Current version:"
dpkg -l | grep "^ii  $PACKAGE " || rpm -q "$PACKAGE"

# 3. Test patch staging (if production)
if [ "$ENVIRONMENT" = "production" ]; then
    echo ""
    echo "3. Testing patch on staging server..."
    ssh staging-server "sudo apt update && sudo apt install --only-upgrade $PACKAGE -y"
    
    echo "Waiting 5 minutes for smoke tests..."
    sleep 300
    
    # Health check staging
    STAGING_HEALTH=$(curl -s -o /dev/null -w '%{http_code}' http://staging-server/health)
    if [ "$STAGING_HEALTH" != "200" ]; then
        echo "❌ Staging health check failed - ABORTING"
        exit 1
    fi
    echo "✓ Staging tests passed"
fi

# 4. Apply patch
echo ""
echo "4. Applying patch..."
if command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install --only-upgrade "$PACKAGE" -y
elif command -v yum &> /dev/null; then
    sudo yum update "$PACKAGE" -y
fi

# 5. Verify new version
echo ""
echo "5. New version:"
dpkg -l | grep "^ii  $PACKAGE " || rpm -q "$PACKAGE"

# 6. Service restart
echo ""
echo "6. Restarting services..."
case "$PACKAGE" in
    nginx|apache2)
        sudo systemctl restart nginx || sudo systemctl restart apache2
        ;;
    mysql*|mariadb*)
        sudo systemctl restart mysql || sudo systemctl restart mariadb
        ;;
    php*)
        sudo systemctl restart php*-fpm
        ;;
esac

# 7. Health check
echo ""
echo "7. Health check..."
sleep 10

if command -v curl &> /dev/null; then
    HEALTH_CODE=$(curl -s -o /dev/null -w '%{http_code}' http://localhost/health || echo "000")
    if [ "$HEALTH_CODE" = "200" ]; then
        echo "✓ Health check passed"
    else
        echo "❌ Health check failed (HTTP $HEALTH_CODE)"
        echo ""
        echo "ROLLBACK? (yes/no)"
        read ROLLBACK
        if [ "$ROLLBACK" = "yes" ]; then
            echo "Rolling back..."
            sudo apt install "$PACKAGE=PREVIOUS_VERSION" -y --allow-downgrades
            sudo systemctl restart nginx apache2 mysql php*-fpm 2>/dev/null
            exit 1
        fi
    fi
fi

# 8. Re-scan Vuls
echo ""
echo "8. Re-scanning vulnerabilities..."
vuls scan localhost
vuls report -format-one-line-text

echo ""
echo "=== Patch completed successfully ==="
```

### 10.4 Patch Compliance Tracking

```bash
#!/bin/bash
# patch-compliance.sh
# Track patch compliance SLA

RESULTS_DIR="/var/lib/vuls/results"
COMPLIANCE_LOG="/var/log/vuls/compliance.log"
SLA_CRITICAL=1    # 1 day
SLA_HIGH=7        # 7 days
SLA_MEDIUM=30     # 30 days

LATEST=$(find "$RESULTS_DIR" -name "*.json" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)

echo "=== Patch Compliance Report - $(date) ===" | tee -a "$COMPLIANCE_LOG"
echo "" | tee -a "$COMPLIANCE_LOG"

# Critical CVE compliance
echo "Critical CVE (SLA: $SLA_CRITICAL day):" | tee -a "$COMPLIANCE_LOG"
jq -r '.[] | .ScannedCves[] | 
    select(.CveDetail.Cvss3Score >= 9.0) |
    {cve: .CveDetail.CveID, published: .CveDetail.PublishedDate, package: .AffectedPackages[].Name}' \
    "$LATEST" | \
while read -r LINE; do
    CVE=$(echo "$LINE" | jq -r '.cve')
    PUBLISHED=$(echo "$LINE" | jq -r '.published' | cut -d'T' -f1)
    PACKAGE=$(echo "$LINE" | jq -r '.package')
    
    # Calculate age
    AGE_DAYS=$(( ($(date +%s) - $(date -d "$PUBLISHED" +%s)) / 86400 ))
    
    if [ $AGE_DAYS -gt $SLA_CRITICAL ]; then
        STATUS="❌ OVERDUE"
        OVERDUE=$((AGE_DAYS - SLA_CRITICAL))
        echo "$STATUS | $CVE | $PACKAGE | Age: ${AGE_DAYS}d | Overdue: ${OVERDUE}d" | tee -a "$COMPLIANCE_LOG"
    else
        echo "✓ Within SLA | $CVE | $PACKAGE | Age: ${AGE_DAYS}d" | tee -a "$COMPLIANCE_LOG"
    fi
done

echo "" | tee -a "$COMPLIANCE_LOG"

# Generate compliance metrics
TOTAL_CRITICAL=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0)] | length' "$LATEST")
OVERDUE_CRITICAL=$(jq -r '.[] | .ScannedCves[] | 
    select(.CveDetail.Cvss3Score >= 9.0) |
    .CveDetail.PublishedDate' "$LATEST" | \
    while read DATE; do
        AGE=$(( ($(date +%s) - $(date -d "$DATE" +%s)) / 86400 ))
        [ $AGE -gt $SLA_CRITICAL ] && echo 1
    done | wc -l)

COMPLIANCE_RATE=$(echo "scale=2; (($TOTAL_CRITICAL - $OVERDUE_CRITICAL) / $TOTAL_CRITICAL) * 100" | bc)

echo "Compliance Rate: $COMPLIANCE_RATE%" | tee -a "$COMPLIANCE_LOG"
echo "Total Critical: $TOTAL_CRITICAL" | tee -a "$COMPLIANCE_LOG"
echo "Overdue: $OVERDUE_CRITICAL" | tee -a "$COMPLIANCE_LOG"
```

---

## Section 11 : Cas Pratiques

### 11.1 Détection Log4Shell (CVE-2021-44228)

```bash
# Scénario : Détecter Log4Shell vulnérabilité critique 2021

# 1. Scan système
vuls scan localhost

# 2. Rechercher spécifiquement Log4Shell
vuls report -format-json -to-localfile

jq '.[] | .ScannedCves[] | select(.CveDetail.CveID == "CVE-2021-44228")' \
    results/current/localhost.json

# Output exemple :
{
  "CveDetail": {
    "CveID": "CVE-2021-44228",
    "Cvss3Score": 10.0,
    "Cvss3Severity": "CRITICAL",
    "Summary": "Apache Log4j2 JNDI features do not protect against attacker controlled LDAP...",
    "PublishedDate": "2021-12-10T10:15:09Z"
  },
  "AffectedPackages": [
    {
      "Name": "log4j-core",
      "Version": "2.14.1",
      "NewVersion": "2.17.1",
      "Repository": "maven"
    }
  ],
  "Exploits": [
    {
      "ExploitType": "exploitdb",
      "ID": "50592",
      "URL": "https://www.exploit-db.com/exploits/50592"
    }
  ]
}

# 3. Vérifier présence Log4j système
find / -name "log4j-core*.jar" 2>/dev/null

# 4. Identifier applications Java utilisant Log4j
lsof | grep log4j

# 5. Patch urgent
# Maven projects
mvn versions:use-latest-versions -DallowSnapshots=false

# Ou manual
wget https://archive.apache.org/dist/logging/log4j/2.17.1/apache-log4j-2.17.1-bin.tar.gz
# Replace JAR files

# 6. Mitigation temporaire (si patch impossible immédiatement)
# Désactiver JNDI lookups
export LOG4J_FORMAT_MSG_NO_LOOKUPS=true

# JVM option
-Dlog4j2.formatMsgNoLookups=true

# 7. Re-scan vérification
vuls scan localhost
vuls report | grep CVE-2021-44228
# Should be empty if patched
```

### 11.2 Dirty Pipe (CVE-2022-0847)

```bash
# Scénario : Kernel privilege escalation

# 1. Détecter vulnérabilité kernel
vuls scan localhost

jq '.[] | .ScannedCves[] | select(.CveDetail.CveID == "CVE-2022-0847")' \
    results/current/localhost.json

# Output :
{
  "CveDetail": {
    "CveID": "CVE-2022-0847",
    "Cvss3Score": 7.8,
    "Cvss3Severity": "HIGH",
    "Summary": "A flaw was found in the way the 'flags' member of the new pipe buffer..."
  },
  "AffectedPackages": [
    {
      "Name": "linux-image-generic",
      "Version": "5.13.0-28-generic",
      "NewVersion": "5.13.0-39-generic"
    }
  ]
}

# 2. Vérifier version kernel actuelle
uname -r
# 5.13.0-28-generic (vulnerable)

# 3. Check exploit disponible
searchsploit dirty pipe
# Linux Kernel 5.8 < 5.16.11 - 'Dirty Pipe' (CVE-2022-0847)

# 4. Patch kernel
sudo apt update
sudo apt install linux-image-generic

# 5. REBOOT requis
sudo reboot

# 6. Après reboot, vérifier
uname -r
# 5.13.0-39-generic (patched)

# 7. Re-scan
vuls scan localhost
vuls report | grep CVE-2022-0847
# Should show as fixed
```

### 11.3 Heartbleed (CVE-2014-0160)

```bash
# Scénario historique : OpenSSL information disclosure

# Détection
vuls scan localhost

jq '.[] | .ScannedCves[] | select(.CveDetail.CveID == "CVE-2014-0160")' \
    results/current/localhost.json

# Vérifier OpenSSL version
openssl version
# OpenSSL 1.0.1e (VULNERABLE)

# Test Heartbleed (script externe)
git clone https://github.com/sensepost/heartbleed-poc.git
cd heartbleed-poc
python heartbleed-poc.py localhost

# Patch
sudo apt update
sudo apt install --only-upgrade openssl libssl1.0.0

# Post-patch CRITIQUE :
# 1. Révoquer certificats SSL
# 2. Générer nouvelles clés privées
# 3. Réinstaller certificats
# 4. Changer passwords/secrets potentiellement exposés

openssl version
# OpenSSL 1.0.1g (patched)
```

### 11.4 Container Vulnerable Image

```bash
# Scénario : Scanner image Docker avant deploy

# config.toml
[servers.docker-scan]
host = "localhost"
port = "local"
containers = ["myapp:1.2.3"]

# Scan
vuls scan docker-scan
vuls report -format-json -to-localfile

# Parse critical
CRITICAL=$(jq '[.[] | .ScannedCves[] | select(.CveDetail.Cvss3Score >= 9.0)] | length' \
    results/current/docker-scan.json)

echo "Critical vulnerabilities: $CRITICAL"

if [ "$CRITICAL" -gt 0 ]; then
    echo "❌ Image contains critical vulnerabilities"
    echo ""
    echo "Details:"
    jq -r '.[] | .ScannedCves[] | 
        select(.CveDetail.Cvss3Score >= 9.0) |
        "\(.CveDetail.CveID) | \(.CveDetail.Cvss3Score) | \(.AffectedPackages[].Name)"' \
        results/current/docker-scan.json
    
    echo ""
    echo "Recommended actions:"
    echo "1. Update base image (FROM ubuntu:22.04 → ubuntu:24.04)"
    echo "2. Update packages in Dockerfile (apt update && apt upgrade)"
    echo "3. Remove unnecessary packages"
    echo "4. Use distroless images if possible"
    
    exit 1
fi

echo "✓ Image scan passed - no critical vulnerabilities"
```

---

## Section 12 : Best Practices Enterprise

### 12.1 Multi-Environment Setup

```bash
# Structure enterprise (dev/staging/prod)

/etc/vuls/
├── prod/
│   ├── config.toml
│   ├── servers.txt
│   └── alerts.toml
├── staging/
│   ├── config.toml
│   └── servers.txt
├── dev/
│   └── config.toml
└── shared/
    └── databases/
        ├── cve.sqlite3
        ├── oval.sqlite3
        └── gost.sqlite3

# Production config
# /etc/vuls/prod/config.toml

[cveDict]
type = "sqlite3"
SQLite3Path = "/etc/vuls/shared/databases/cve.sqlite3"

[slack]
hookURL = "https://hooks.slack.com/services/PROD/WEBHOOK"
channel = "#security-prod"

[email]
to = ["security-team@example.com", "soc@example.com"]
subjectPrefix = "[PROD Vuls]"

[default]
port = "22"
user = "vulsuser"
keyPath = "/home/vulsuser/.ssh/id_rsa_prod"

# Include servers from file
# servers.txt format: hostname,ip,description
# web-prod-01,10.0.1.10,Production web server
# db-prod-01,10.0.1.20,Production database

# Script generate config from inventory
#!/bin/bash
while IFS=, read -r NAME IP DESC; do
    cat >> /etc/vuls/prod/config.toml <<EOF

[servers.$NAME]
host = "$IP"
# $DESC
EOF
done < /etc/vuls/prod/servers.txt

# Scan per environment
vuls scan -config /etc/vuls/prod/config.toml
vuls scan -config /etc/vuls/staging/config.toml
```

### 12.2 Compliance Reporting (PCI-DSS)

```bash
#!/bin/bash
# vuls-pci-compliance.sh
# PCI-DSS Requirement 6.2 compliance

RESULTS_DIR="/var/lib/vuls/results"
COMPLIANCE_DIR="/var/reports/pci-dss"
DATE=$(date +%Y-%m-%d)

mkdir -p "$COMPLIANCE_DIR"

LATEST=$(find "$RESULTS_DIR" -name "*.json" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)

# PCI-DSS 6.2: Critical patches within 30 days
cat > "$COMPLIANCE_DIR/pci-dss-6.2-$DATE.html" <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>PCI-DSS 6.2 Compliance Report</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        .compliant { color: green; font-weight: bold; }
        .non-compliant { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>PCI-DSS Requirement 6.2 - Vulnerability Management</h1>
    <p>Report Date: $DATE</p>
    
    <h2>Requirement: All system components must be protected from known vulnerabilities 
    by installing applicable vendor-supplied security patches. Install critical security 
    patches within one month of release.</h2>
    
    <h3>Critical Vulnerabilities (CVSS 9.0+)</h3>
    <table>
        <tr>
            <th>CVE ID</th>
            <th>CVSS Score</th>
            <th>Package</th>
            <th>Published Date</th>
            <th>Age (days)</th>
            <th>Status</th>
        </tr>
EOF

# Parse critical CVE
jq -r '.[] | .ScannedCves[] | 
    select(.CveDetail.Cvss3Score >= 9.0) |
    {cve: .CveDetail.CveID, score: .CveDetail.Cvss3Score, 
     package: .AffectedPackages[].Name, published: .CveDetail.PublishedDate}' \
    "$LATEST" | \
while read -r LINE; do
    CVE=$(echo "$LINE" | jq -r '.cve')
    SCORE=$(echo "$LINE" | jq -r '.score')
    PACKAGE=$(echo "$LINE" | jq -r '.package')
    PUBLISHED=$(echo "$LINE" | jq -r '.published' | cut -d'T' -f1)
    
    AGE_DAYS=$(( ($(date +%s) - $(date -d "$PUBLISHED" +%s)) / 86400 ))
    
    if [ $AGE_DAYS -le 30 ]; then
        STATUS="<span class='compliant'>COMPLIANT</span>"
    else
        STATUS="<span class='non-compliant'>NON-COMPLIANT</span>"
    fi
    
    cat >> "$COMPLIANCE_DIR/pci-dss-6.2-$DATE.html" <<EOF
        <tr>
            <td>$CVE</td>
            <td>$SCORE</td>
            <td>$PACKAGE</td>
            <td>$PUBLISHED</td>
            <td>$AGE_DAYS</td>
            <td>$STATUS</td>
        </tr>
EOF
done

cat >> "$COMPLIANCE_DIR/pci-dss-6.2-$DATE.html" <<EOF
    </table>
    
    <h3>Summary</h3>
    <p>This report demonstrates compliance with PCI-DSS Requirement 6.2 
    regarding timely patching of critical security vulnerabilities.</p>
</body>
</html>
EOF

echo "PCI-DSS compliance report: $COMPLIANCE_DIR/pci-dss-6.2-$DATE.html"
```

### 12.3 Checklist Production

```markdown
## Vuls Production Deployment Checklist

### Installation
- [ ] Vuls binary installed (/usr/local/bin/vuls)
- [ ] Database tools installed (go-cve-dictionary, goval-dictionary, gost)
- [ ] Databases downloaded and updated
- [ ] VulsRepo dashboard installed (optional)

### Configuration
- [ ] config.toml créé et testé
- [ ] SSH keys configurées (agentless scanning)
- [ ] Sudo permissions configurées target servers
- [ ] Email/Slack notifications configurées
- [ ] Environments séparés (dev/staging/prod)

### Databases
- [ ] NVD database downloaded (2GB)
- [ ] OVAL databases pour distributions utilisées
- [ ] Gost security trackers updated
- [ ] ExploitDB database downloaded
- [ ] Cron update databases quotidien configuré

### Scanning
- [ ] Scan initial exécuté tous environnements
- [ ] Baseline results archivés
- [ ] Scan quotidien automatisé (cron)
- [ ] Scan post-patch workflow testé
- [ ] Container scanning testé (si applicable)

### Reporting
- [ ] VulsRepo dashboard accessible
- [ ] Reports JSON générés automatiquement
- [ ] Trending analysis configuré
- [ ] Differential scanning testé
- [ ] Compliance reports (PCI-DSS) générés

### Alerting
- [ ] Critical CVE alerts fonctionnelles (email)
- [ ] Slack/Teams integration testée
- [ ] PagerDuty integration (si critique)
- [ ] Prometheus metrics exportées
- [ ] Alert thresholds configurés

### Integration
- [ ] CI/CD pipeline integration testée
- [ ] Docker image scanning automated
- [ ] Kubernetes admission controller (optional)
- [ ] SIEM integration (Splunk/ELK)

### Documentation
- [ ] Runbook scan procedures
- [ ] Patch management workflow documenté
- [ ] Escalation procedures définies
- [ ] SLA patching documentés
- [ ] Training équipe complété

### Security
- [ ] Vuls server hardened (firewall, SSH)
- [ ] Database files permissions correctes
- [ ] SSH keys secured (password-protected)
- [ ] VulsRepo authentication enabled
- [ ] Audit logs enabled

### Maintenance
- [ ] Database backup automated
- [ ] Results retention policy (90 days)
- [ ] Log rotation configured
- [ ] Disk space monitoring
- [ ] Performance metrics tracked

### Testing
- [ ] Scan accuracy validated (known CVE)
- [ ] False positives documented
- [ ] Patch workflow tested staging
- [ ] Rollback procedure tested
- [ ] Disaster recovery tested
```

### 12.4 Script Setup Complet Enterprise

```bash
#!/bin/bash
# vuls-enterprise-setup.sh
# Complete enterprise deployment

set -euo pipefail

echo "=== Vuls Enterprise Setup ==="

# 1. Install binaries
echo "1. Installing Vuls and dependencies..."
cd /tmp

VULS_VERSION="0.27.0"
wget https://github.com/future-architect/vuls/releases/download/v${VULS_VERSION}/vuls_${VULS_VERSION}_linux_amd64.tar.gz
tar -xzf vuls_${VULS_VERSION}_linux_amd64.tar.gz
sudo mv vuls /usr/local/bin/

# Database tools
CVE_VERSION="0.10.0"
wget https://github.com/vulsio/go-cve-dictionary/releases/download/v${CVE_VERSION}/go-cve-dictionary_${CVE_VERSION}_linux_amd64.tar.gz
tar -xzf go-cve-dictionary_${CVE_VERSION}_linux_amd64.tar.gz
sudo mv go-cve-dictionary /usr/local/bin/

OVAL_VERSION="0.4.0"
wget https://github.com/vulsio/goval-dictionary/releases/download/v${OVAL_VERSION}/goval-dictionary_${OVAL_VERSION}_linux_amd64.tar.gz
tar -xzf goval-dictionary_${OVAL_VERSION}_linux_amd64.tar.gz
sudo mv goval-dictionary /usr/local/bin/

GOST_VERSION="0.3.0"
wget https://github.com/vulsio/gost/releases/download/v${GOST_VERSION}/gost_${GOST_VERSION}_linux_amd64.tar.gz
tar -xzf gost_${GOST_VERSION}_linux_amd64.tar.gz
sudo mv gost /usr/local/bin/

# 2. Create structure
echo "2. Creating directory structure..."
sudo mkdir -p /var/lib/vuls/{results,logs,cve,oval,gost,exploitdb}
sudo mkdir -p /etc/vuls/{prod,staging,dev,shared/databases}
sudo mkdir -p /var/reports/{vuls,compliance}

# 3. Download databases (LONG - 30-60 min)
echo "3. Downloading vulnerability databases..."
go-cve-dictionary fetch nvd --dbpath /etc/vuls/shared/databases/cve.sqlite3
goval-dictionary fetch ubuntu 22 --dbpath /etc/vuls/shared/databases/oval.sqlite3
goval-dictionary fetch ubuntu 20 --dbpath /etc/vuls/shared/databases/oval.sqlite3
gost fetch ubuntu --dbpath /etc/vuls/shared/databases/gost.sqlite3

# 4. Create config
echo "4. Creating configuration..."
cat > /etc/vuls/prod/config.toml <<'EOF'
[cveDict]
type = "sqlite3"
SQLite3Path = "/etc/vuls/shared/databases/cve.sqlite3"

[ovalDict]
type = "sqlite3"
SQLite3Path = "/etc/vuls/shared/databases/oval.sqlite3"

[gost]
type = "sqlite3"
SQLite3Path = "/etc/vuls/shared/databases/gost.sqlite3"

[slack]
hookURL = "${SLACK_WEBHOOK}"
channel = "#security-prod"

[email]
to = ["security@example.com"]
subjectPrefix = "[Vuls PROD]"

[default]
port = "22"
user = "vulsuser"

[servers.localhost]
host = "127.0.0.1"
port = "local"
EOF

# 5. Setup cron jobs
echo "5. Configuring automated scanning..."
cat > /etc/cron.d/vuls <<'EOF'
# Update databases daily 2AM
0 2 * * * root /usr/local/bin/vuls-update-db.sh

# Scan daily 3AM
0 3 * * * root /usr/local/bin/vuls-daily-scan.sh

# Compliance report monthly
0 4 1 * * root /usr/local/bin/vuls-pci-compliance.sh
EOF

# 6. Create automation scripts (see previous sections)
cp vuls-update-db.sh /usr/local/bin/
cp vuls-daily-scan.sh /usr/local/bin/
cp vuls-pci-compliance.sh /usr/local/bin/
chmod +x /usr/local/bin/vuls-*.sh

# 7. Initial scan
echo "6. Running initial scan..."
vuls scan -config /etc/vuls/prod/config.toml
vuls report -format-json -to-localfile

echo ""
echo "=== Setup Complete ==="
echo "Configuration: /etc/vuls/prod/config.toml"
echo "Results: /var/lib/vuls/results"
echo "Logs: /var/lib/vuls/logs"
echo ""
echo "Next steps:"
echo "1. Configure target servers in config.toml"
echo "2. Setup SSH keys (vulsuser)"
echo "3. Install VulsRepo dashboard (optional)"
echo "4. Configure Slack/email notifications"
echo "5. Test scanning: vuls scan -config /etc/vuls/prod/config.toml"
```

---

## Ressources et Références

**Documentation officielle :**
- GitHub : https://github.com/future-architect/vuls
- Documentation : https://vuls.io/docs/
- VulsRepo : https://github.com/ishiDACo/vulsrepo

**Databases CVE :**
- NVD : https://nvd.nist.gov/
- JVN : https://jvndb.jvn.jp/en/
- OVAL : https://oval.mitre.org/

**Communauté :**
- Slack : https://vuls-slackin.herokuapp.com/
- Issues : https://github.com/future-architect/vuls/issues

**Complémentaires :**
- Lynis : https://cisofy.com/lynis/
- OpenVAS : https://www.openvas.org/
- Trivy : https://github.com/aquasecurity/trivy

---

## Conclusion

**Vuls = Scanner vulnérabilités CVE essentiel infrastructure**

**Points clés :**

✅ **200,000+ CVE database** = NVD, OVAL, Gost, Security Trackers
✅ **Agentless** = Scan SSH remote, pas agent déployer
✅ **Multi-distro** = Ubuntu, Debian, RHEL, CentOS, Alpine
✅ **CI/CD ready** = Scan containers, block deploy vulnerable
✅ **Dashboard VulsRepo** = Visualisation web React
✅ **Enterprise-ready** = Scale 1000+ servers, compliance PCI-DSS

**Workflow recommandé :**

```bash
# 1. Installation
cd /tmp
wget https://github.com/future-architect/vuls/releases/download/v0.27.0/vuls_0.27.0_linux_amd64.tar.gz
tar -xzf vuls_0.27.0_linux_amd64.tar.gz
sudo mv vuls /usr/local/bin/

# 2. Download databases
go-cve-dictionary fetch nvd --dbpath /var/lib/vuls/cve.sqlite3
goval-dictionary fetch ubuntu 22 --dbpath /var/lib/vuls/oval.sqlite3

# 3. Configuration
nano ~/.vuls/config.toml
# Définir servers

# 4. Scan initial
vuls scan
vuls report -format-full-text

# 5. Automatisation
# Cron daily scan + alerts

# 6. Patch management
# Triage → Test staging → Patch prod → Re-scan

# 7. Compliance
# Monthly PCI-DSS reports
```

**Position dans Stack Sécurité :**

```
1. Lynis       → Audit configuration
2. UFW         → Firewall
3. Fail2ban    → IPS
4. Vuls        → ⭐ Scanner CVE packages
5. ClamAV      → Antivirus
6. LMD         → Malware web
7. Chkrootkit  → Rootkits
```

**Vuls complète parfaitement Lynis : configuration vs vulnérabilités !** 

**Tu maîtrises maintenant Vuls du scan basique à l'enterprise deployment !** 🔍

---

**Guide Vuls Complet terminé !** 🎉

Voilà le guide complet Vuls ! Sections 9-12 couvrent :

✅ **Section 9** : Automatisation complète (scan quotidien, Prometheus, trending)
✅ **Section 10** : Patch management workflow (triage, prioritization, compliance SLA)
✅ **Section 11** : Cas pratiques réels (Log4Shell, Dirty Pipe, Heartbleed, containers)
✅ **Section 12** : Best practices enterprise (multi-env, PCI-DSS, checklist, setup complet)

**Ordre optimal mis à jour avec Vuls :**

```markdown
1. lynis.md                  # Audit configuration
2. ufw.md                    # Firewall
3. fail2ban.md               # IPS
4. vuls.md                   # ⭐ Scanner CVE (NOUVEAU - avant antivirus)
5. clamav.md                 # Antivirus général
6. linux_malware_detect.md   # Malware web
7. chkrootkit.md             # Rootkits
```

**Vuls s'insère logiquement entre Fail2ban et ClamAV** car il scanne les **packages système** (vulnérabilités connues), ce qui est une étape de détection différente de l'antivirus (malware) mais complémentaire.

Besoin d'autre chose pour compléter la stack sécurité ? 🛡️