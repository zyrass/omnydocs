---
description: "ClamAV : antivirus open-source complet Linux, scan malware, intégration mail/web, automatisation"
icon: lucide/book-open-check
tags: ["CLAMAV", "ANTIVIRUS", "MALWARE", "SECURITY", "LINUX", "SCANNING"]
---

# ClamAV

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-time="6-8 heures"
  data-version="1.0">
</div>

## Introduction à l'Antivirus Linux

!!! quote "Analogie pédagogique"
    _Imaginez un **système immunitaire ultra-performant avec mémoire collective mondiale** : ClamAV fonctionne comme **défense biologique analysant CHAQUE "organisme" (fichier) entrant corps (serveur)** pour détecter pathogènes (malware). **Système immunitaire biologique** : anticorps (signatures virus) reconnaissent pathogènes spécifiques, mémoire immunitaire (base signatures) mise à jour après nouvelle infection découverte communauté médicale, lymphocytes (scanner) patrouillent organisme détectant menaces, quarantaine (isolation fichiers infectés) empêche propagation. **Sans antivirus** : infections silencieuses (backdoors, ransomware, cryptominers), propagation réseau (worms), vol données (trojans), serveur compromis devient zombie (botnet). **Avec ClamAV** : **Scan proactif** (analyse fichiers uploadés temps réel), **Base signatures** (8+ millions malware connus, mise à jour horaire), **Détection heuristique** (comportements suspects même virus inconnus), **Quarantaine automatique** (isolation fichiers infectés), **Integration transparente** (mail servers, web servers, file shares, cloud storage). **Architecture ClamAV** : 1) **clamd** (daemon ultra-rapide multi-thread scan résidents mémoire), 2) **clamscan** (CLI scan ponctuel filesystem), 3) **freshclam** (updater automatique signatures), 4) **clamdscan** (client daemon, scan rapide via socket), 5) **clamav-milter** (integration Postfix/Sendmail), 6) **clamonacc** (on-access scanning temps réel). **Use cases production** : serveurs mail (scan pièces jointes AVANT delivery), serveurs web (upload fichiers utilisateurs), serveurs fichiers (partages Samba/NFS), hébergeurs mutualisés (isolation tenants), gateways réseau (scan proxy HTTP), instances cloud (conformité sécurité). **Performance** : daemon clamd scan 1GB en ~30 secondes (SSD NVMe), multi-thread scaling linéaire (8 cores = 8x faster), faible overhead CPU (<5% idle), signatures compressées efficacement. **ClamAV = standard industrie antivirus Linux/Unix** : utilisé 90% serveurs mail professionnels, intégré solutions backup (Veeam, Acronis), packages distributions majeures, gratuit GPL sans limitations commerciales._

**ClamAV en résumé :**

- ✅ **Open-source** = GPL, gratuit usage commercial, communauté active
- ✅ **Multi-plateforme** = Linux, BSD, macOS, Windows, Solaris
- ✅ **Base signatures** = 8M+ malware, mise à jour quotidienne (parfois horaire)
- ✅ **Detection avancée** = Signatures + heuristique + machine learning
- ✅ **Performance** = Daemon multi-thread, scan rapide, faible overhead
- ✅ **Intégrations** = Mail (Postfix, Exim), Web (Apache, Nginx), SMB, FTP
- ✅ **Formats supportés** = 100+ formats (archives, documents, exécutables)
- ✅ **On-access scanning** = Scan temps réel (clamonacc, kernel fanotify)
- ✅ **Production-ready** = Utilisé millions serveurs, stable, fiable

**Guide structure :**

1. Introduction et concepts ClamAV
2. Installation (package managers, source, Docker)
3. Configuration clamd daemon
4. Scan manuel (clamscan/clamdscan)
5. Mise à jour signatures (freshclam)
6. On-access scanning temps réel
7. Intégration mail servers (Postfix/Amavis)
8. Intégration web servers (upload scanning)
9. Automatisation et monitoring
10. Performance tuning production
11. Troubleshooting et maintenance
12. Best practices et cas d'usage

---

## Section 1 : Introduction et Concepts

### 1.1 Qu'est-ce que ClamAV ?

**ClamAV = Clam AntiVirus, engine open-source détection malware**

```
ClamAV Architecture :

┌─────────────────────────────────────────────────────────┐
│                    ClamAV Ecosystem                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │   clamscan   │  │  clamdscan   │  │  clamonacc  │  │
│  │  (CLI scan)  │  │ (fast daemon │  │ (on-access) │  │
│  │              │  │   client)    │  │   scanning  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘  │
│         │                  │                  │         │
│         ├──────────────────┴──────────────────┤         │
│         │                                     │         │
│  ┌──────▼──────────────────────────────────────▼──┐    │
│  │              clamd (daemon)                    │    │
│  │  Multi-thread scanning engine                 │    │
│  │  Signatures loaded in memory                  │    │
│  └──────────────────┬─────────────────────────────┘    │
│                     │                                  │
│  ┌──────────────────▼──────────────────────────────┐   │
│  │         libclamav (core engine)                │   │
│  │  - Signature matching                          │   │
│  │  - Heuristic detection                         │   │
│  │  - Archive unpacking (zip, tar, rar...)       │   │
│  │  - Document parsing (PDF, Office, HTML...)    │   │
│  └──────────────────┬──────────────────────────────┘   │
│                     │                                  │
│  ┌──────────────────▼──────────────────────────────┐   │
│  │      Signature Database (~8M+ signatures)      │   │
│  │  /var/lib/clamav/                              │   │
│  │  - main.cvd (main database ~200MB)            │   │
│  │  - daily.cvd (daily updates ~50MB)            │   │
│  │  - bytecode.cvd (bytecode signatures)         │   │
│  └──────────────────▲──────────────────────────────┘   │
│                     │                                  │
│  ┌──────────────────┴──────────────────────────────┐   │
│  │          freshclam (updater)                    │   │
│  │  Auto-update signatures from Cloudflare CDN   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Composants principaux :**

```bash
clamd         # Daemon multi-thread (production)
clamscan      # CLI scanner (scan ponctuel)
clamdscan     # Client daemon (rapide via socket)
freshclam     # Updater signatures automatique
clamonacc     # On-access scanner (temps réel)
clamav-milter # Mail filter (Postfix/Sendmail)
clamconf      # Configuration checker
sigtool       # Signature management tool
clamsubmit    # Submit false positives/negatives
```

### 1.2 Types Détection

**1. Signature-based (hash/pattern matching) :**

```
Signature = Empreinte unique malware connu

Exemples :
- Hash MD5/SHA256 fichier complet
- Pattern bytes spécifiques (hexadecimal)
- Regex contenu fichier

Format signature ClamAV :
MalwareName:TargetType:Offset:HexSignature

Exemple réel :
Win.Trojan.Agent-123456:0:*:6d7a90000300000004000000ffff

Avantages :
+ Détection rapide (lookup hash table)
+ Zéro false positives (signature exacte)
+ Faible overhead CPU

Inconvénients :
- Ne détecte QUE malware connus
- Nouveaux variants échappent (polymorphic)
```

**2. Heuristic detection (comportement suspect) :**

```
Analyse comportement fichier sans signature exacte

Exemples heuristiques :
- Executable avec comportement suspect (auto-copy, registry modification)
- PDF avec JavaScript obfusqué
- Office document avec macros VBA malveillantes
- Archive avec trop de fichiers compressés (zip bomb)
- Entropy anormalement haute (encryption/packing)

Avantages :
+ Détecte nouveaux malware (zero-day)
+ Identifie variants polymorphic

Inconvénients :
- Plus de false positives
- Plus coûteux CPU
```

**3. Bytecode signatures (portable detection) :**

```
Code portable exécuté par ClamAV pour détection complexe

Bytecode = Instructions Python-like compilées
Permet logique détection sophistiquée

Exemple use case :
- Détecter malware avec multiples étapes unpacking
- Analyser fichiers avec encryption custom
- Évaluer macros Office contextuellement
```

### 1.3 Formats Fichiers Supportés

**Archives (unpacking automatique) :**

```
ZIP, RAR, TAR, GZIP, BZIP2, 7ZIP, ARJ, LZH, CAB, CHM
ACE, SIS, NSIS, ISO9660, DMG, HFS+, CPIO, JAR, APK

Récursion archives :
archive.zip
  ├── malware.exe          (scanné)
  ├── nested.zip           (unpacked)
  │   └── trojan.dll       (scanné)
  └── document.pdf         (scanné)

Limite profondeur : 16 niveaux (configurable)
Limite ratio compression : 1:250 (anti zip-bomb)
```

**Documents :**

```
PDF              (JavaScript detection, embedded files)
Microsoft Office (DOC, XLS, PPT - macro detection)
Office Open XML  (DOCX, XLSX, PPTX)
OpenDocument     (ODT, ODS, ODP)
RTF              (Rich Text Format)
HTML/XML         (script injection, iframes malicieux)
```

**Executables :**

```
Windows PE       (EXE, DLL, SCR, SYS)
ELF              (Linux binaries)
Mach-O           (macOS binaries)
Java             (CLASS, JAR)
Android          (APK, DEX)
Python           (PYC bytecode)
```

**Emails :**

```
MBOX, Maildir
MIME multipart
Attachments extraction automatique
Header analysis (phishing detection)
```

### 1.4 Avantages vs Alternatives

| Critère | ClamAV | Sophos | BitDefender | Windows Defender |
|---------|--------|--------|-------------|------------------|
| **Licence** | GPL (gratuit) | Commercial | Commercial | Windows only |
| **Plateforme** | Cross-platform | Cross-platform | Cross-platform | Windows |
| **Detection rate** | 80-85% | 95-98% | 95-99% | 90-95% |
| **Performance** | Léger (daemon) | Moyen | Moyen-lourd | Moyen |
| **Mail integration** | Native (milter) | Via plugin | Via plugin | N/A |
| **On-access scan** | Oui (clamonacc) | Oui | Oui | Oui |
| **Signatures** | 8M+ (public) | Proprietary | Proprietary | Microsoft |
| **False positives** | Faibles | Très faibles | Très faibles | Faibles |
| **Support** | Communauté | Commercial | Commercial | Microsoft |
| **Use case idéal** | Serveurs Linux | Enterprise | Enterprise | Desktop Windows |

**Pourquoi choisir ClamAV :**

```
✅ Serveurs Linux/Unix production
✅ Budget limité (gratuit)
✅ Compliance réglementaire (scan obligatoire)
✅ Mail servers (native integration)
✅ Intégration custom (API/CLI)
✅ Environnements cloud (léger, scriptable)

❌ Ne PAS choisir si :
- Detection rate critique >95% requis (finance, santé)
- Support commercial 24/7 obligatoire
- Windows desktop primary (Defender meilleur)
```

---

## Section 2 : Installation

### 2.1 Installation Package Manager

**Debian/Ubuntu :**

```bash
# Mettre à jour cache
sudo apt update

# Installer ClamAV complet
sudo apt install clamav clamav-daemon clamav-freshclam

# Composants installés :
# - clamav : binaires clamscan, sigtool, etc.
# - clamav-daemon : clamd service
# - clamav-freshclam : freshclam updater

# Vérifier installation
clamscan --version
# Output : ClamAV 1.0.3/27074/Tue Jan 16 08:52:23 2024

# Services systemd créés
sudo systemctl status clamav-daemon
sudo systemctl status clamav-freshclam
```

**RHEL/CentOS/Rocky/Alma :**

```bash
# Activer EPEL repository
sudo yum install epel-release

# Installer ClamAV
sudo yum install clamav clamav-update clamd

# Ou via DNF (RHEL 8+)
sudo dnf install clamav clamd clamav-update

# Vérifier
clamscan --version
```

**Arch Linux :**

```bash
# Installer depuis official repos
sudo pacman -S clamav

# Activer services
sudo systemctl enable clamav-daemon
sudo systemctl enable clamav-freshclam
```

**macOS :**

```bash
# Via Homebrew
brew install clamav

# Config files location
/usr/local/etc/clamav/

# Copier samples configs
cd /usr/local/etc/clamav/
cp freshclam.conf.sample freshclam.conf
cp clamd.conf.sample clamd.conf

# Éditer configs (remove 'Example' line)
sed -i '' 's/^Example/#Example/' freshclam.conf
sed -i '' 's/^Example/#Example/' clamd.conf
```

### 2.2 Installation depuis Source

```bash
# Dépendances build (Debian/Ubuntu)
sudo apt install -y \
    build-essential \
    libssl-dev \
    libpcre3-dev \
    libjson-c-dev \
    libcurl4-openssl-dev \
    zlib1g-dev \
    libxml2-dev

# Télécharger source
cd /tmp
wget https://www.clamav.net/downloads/production/clamav-1.0.3.tar.gz
tar -xzf clamav-1.0.3.tar.gz
cd clamav-1.0.3

# Configure
./configure \
    --prefix=/usr/local \
    --sysconfdir=/etc/clamav \
    --with-dbdir=/var/lib/clamav \
    --enable-clamdtop \
    --enable-milter

# Compile (utilise tous CPU cores)
make -j$(nproc)

# Install
sudo make install

# Créer user clamav
sudo groupadd clamav
sudo useradd -g clamav -s /bin/false -c "ClamAV User" clamav

# Créer directories
sudo mkdir -p /var/lib/clamav
sudo mkdir -p /var/log/clamav
sudo mkdir -p /var/run/clamav

# Permissions
sudo chown -R clamav:clamav /var/lib/clamav
sudo chown -R clamav:clamav /var/log/clamav
sudo chown -R clamav:clamav /var/run/clamav

# Vérifier
/usr/local/bin/clamscan --version
```

### 2.3 Installation Docker

```bash
# Pull image officielle
docker pull clamav/clamav:latest

# Run container avec persistence
docker run -d \
  --name clamav \
  -p 3310:3310 \
  -v clamav-signatures:/var/lib/clamav \
  clamav/clamav:latest

# Vérifier logs (freshclam update signatures)
docker logs -f clamav
# Attendre message : "Database updated successfully"

# Scanner fichier via container
docker exec clamav clamscan /path/to/file

# Scanner via socket (depuis host)
echo "SCAN /path/to/file" | nc localhost 3310
```

**Docker Compose complet :**

```yaml
# docker-compose.yml
version: '3'

services:
  clamav:
    image: clamav/clamav:latest
    container_name: clamav
    restart: unless-stopped
    
    ports:
      - "3310:3310"
    
    volumes:
      # Signatures persistence
      - clamav-data:/var/lib/clamav
      # Logs
      - ./logs:/var/log/clamav
      # Scan directory
      - ./scan:/scan:ro
    
    environment:
      # Configuration via env vars
      - CLAMAV_NO_FRESHCLAM=false
      - FRESHCLAM_CHECKS=24
    
    healthcheck:
      test: ["CMD", "/usr/local/bin/clamdcheck.sh"]
      interval: 60s
      timeout: 10s
      retries: 3

volumes:
  clamav-data:
```

```bash
# Start services
docker-compose up -d

# Scanner directory
docker-compose exec clamav clamscan -r /scan
```

### 2.4 Configuration Initiale

**Freshclam configuration (mise à jour signatures) :**

```bash
# Éditer config freshclam
sudo nano /etc/clamav/freshclam.conf

# Configuration recommandée :

# RETIRER ligne Example (obligatoire)
#Example

# Database directory
DatabaseDirectory /var/lib/clamav

# Logs
UpdateLogFile /var/log/clamav/freshclam.log
LogFileMaxSize 10M
LogTime yes
LogVerbose no

# Mirror Cloudflare (défaut, rapide)
DatabaseMirror database.clamav.net

# Fréquence checks (24 fois/jour = toutes les heures)
Checks 24

# User (si installé via package, déjà correct)
DatabaseOwner clamav

# Notifications (optionnel)
#OnUpdateExecute /usr/local/bin/clamav-notify.sh
#OnErrorExecute /usr/local/bin/clamav-error-notify.sh

# Test mode (décommenter pour dry-run)
#TestDatabases yes
```

**Première mise à jour signatures :**

```bash
# Update signatures manuellement (première fois)
sudo freshclam

# Output attendu :
# ClamAV update process started at Tue Jan 16 10:30:00 2024
# Downloading main.cvd [100%]
# main.cvd updated (version: 62, sigs: 6647427, f-level: 90, builder: sigmgr)
# Downloading daily.cvd [100%]
# daily.cvd updated (version: 27074, sigs: 2030118, f-level: 90, builder: raynman)
# Downloading bytecode.cvd [100%]
# bytecode.cvd updated (version: 334, sigs: 91, f-level: 90, builder: anvilleg)
# Database updated successfully

# Vérifier signatures téléchargées
ls -lh /var/lib/clamav/
# main.cvd    (~200MB)
# daily.cvd   (~50MB)
# bytecode.cvd (~1MB)

# Activer freshclam service (updates automatiques)
sudo systemctl enable clamav-freshclam
sudo systemctl start clamav-freshclam

# Vérifier service fonctionne
sudo systemctl status clamav-freshclam
```

**Clamd configuration (daemon scanner) :**

```bash
# Éditer config clamd
sudo nano /etc/clamav/clamd.conf

# Configuration production recommandée :

# RETIRER ligne Example
#Example

# Socket (communication locale rapide)
LocalSocket /var/run/clamav/clamd.sock
LocalSocketMode 666

# TCP socket (si accès réseau requis)
#TCPSocket 3310
#TCPAddr 127.0.0.1

# User/Group
User clamav

# Logs
LogFile /var/log/clamav/clamav.log
LogFileMaxSize 10M
LogTime yes
LogClean no       # Ne pas logger fichiers clean (verbeux)
LogVerbose no

# Database directory
DatabaseDirectory /var/lib/clamav

# Performance tuning
MaxThreads 10              # Threads concurrents (ajuster selon CPU)
MaxConnectionQueueLength 30
MaxQueue 200

# Scan options
ScanPE yes                 # Scan Windows PE files
ScanELF yes                # Scan Linux ELF binaries
ScanOLE2 yes               # Scan MS Office documents
ScanPDF yes                # Scan PDFs
ScanHTML yes               # Scan HTML files
ScanArchive yes            # Scan archives (zip, tar, etc.)

# Archive limits (anti zip-bomb)
MaxScanSize 100M           # Max size fichier à scanner
MaxFileSize 25M            # Max size fichier individuel extrait
MaxRecursion 16            # Max profondeur archives imbriquées
MaxFiles 10000             # Max fichiers dans archive
MaxEmbeddedPE 10M          # Max size embedded PE
MaxHTMLNormalize 10M       # Max size HTML normalisé
MaxHTMLNoTags 2M           # Max size HTML sans tags

# Heuristic detection
HeuristicScanPrecedence yes
PhishingSignatures yes
PhishingScanURLs yes

# Self-check (reload signatures sans restart)
SelfCheck 3600             # Toutes les heures

# Notifications (optionnel)
#VirusEvent /usr/local/bin/virus-notify.sh
```

**Démarrer daemon :**

```bash
# Start clamd
sudo systemctl enable clamav-daemon
sudo systemctl start clamav-daemon

# Vérifier daemon running
sudo systemctl status clamav-daemon

# Tester connexion socket
clamdscan --version
# Output : ClamAV 1.0.3/27074/Tue Jan 16 08:52:23 2024

# Ping daemon
clamdscan --ping
# Output : PONG
```

---

## Section 3 : Configuration Clamd Daemon

### 3.1 Architecture Daemon

**Clamd = Daemon multi-thread resident mémoire**

```
Avantages daemon vs CLI :
┌─────────────────────┬─────────────────────┐
│     clamscan        │      clamd          │
│   (CLI scanner)     │    (daemon)         │
├─────────────────────┼─────────────────────┤
│ Lance nouveau       │ Process permanent   │
│ process chaque scan │ mémoire             │
├─────────────────────┼─────────────────────┤
│ Charge signatures   │ Signatures loaded   │
│ à chaque scan       │ une fois (startup)  │
│ ~10s overhead       │ ~0.1s per scan      │
├─────────────────────┼─────────────────────┤
│ Single-thread       │ Multi-thread        │
│ 1 scan à la fois    │ Scans simultanés    │
├─────────────────────┼─────────────────────┤
│ ~200MB RAM          │ ~400MB RAM base     │
│ par scan            │ + ~50MB/scan actif  │
├─────────────────────┼─────────────────────┤
│ Use case :          │ Use case :          │
│ Scan ponctuel       │ Production continue │
│ Cron jobs           │ Mail/web servers    │
│ Scripts manuels     │ On-access scanning  │
└─────────────────────┴─────────────────────┘

Performance comparison :
clamscan /home (10,000 fichiers) : 15 minutes
clamdscan /home (10,000 fichiers) : 2 minutes
```

### 3.2 Options Socket vs TCP

**LocalSocket (Unix domain socket) - RECOMMANDÉ :**

```bash
# Configuration clamd.conf
LocalSocket /var/run/clamav/clamd.sock
LocalSocketMode 666  # rw-rw-rw- (ou 660 pour plus sécurisé)

# Avantages :
+ Plus rapide (pas d'overhead réseau)
+ Plus sécurisé (filesystem permissions)
+ Pas de port réseau exposé

# Inconvénients :
- Accès local uniquement (même machine)

# Usage :
clamdscan --stream /path/to/file
```

**TCP Socket (réseau) :**

```bash
# Configuration clamd.conf
TCPSocket 3310
TCPAddr 127.0.0.1  # localhost only (sécurisé)
# OU
TCPAddr 0.0.0.0    # écoute toutes interfaces (DANGER si pas firewall)

# Avantages :
+ Accès réseau (remote scanning)
+ Multi-serveurs (distributed scanning)

# Inconvénients :
- Moins sécurisé (doit protéger firewall)
- Overhead réseau

# Usage :
clamdscan --stream --fdpass /path/to/file
# Depuis remote :
nc remote-server 3310 < /path/to/file
```

**Sécuriser TCP socket :**

```bash
# 1. Firewall strict (seulement trusted IPs)
sudo ufw allow from 192.168.1.0/24 to any port 3310

# 2. Ou utiliser stunnel (TLS wrapper)
# Config stunnel : /etc/stunnel/clamav.conf
[clamav]
accept = 3311
connect = 127.0.0.1:3310
cert = /etc/ssl/certs/clamav.pem
key = /etc/ssl/private/clamav.key
```

### 3.3 Performance Tuning

**Threads et concurrence :**

```bash
# /etc/clamav/clamd.conf

# MaxThreads = Threads concurrents pour scans
MaxThreads 10
# Recommandation : 1.5x nombre CPU cores
# Exemple : 8 cores → MaxThreads 12

# MaxConnectionQueueLength = File d'attente connexions
MaxConnectionQueueLength 30

# MaxQueue = Scans en attente
MaxQueue 200

# IdleTimeout = Timeout thread idle (secondes)
IdleTimeout 60

# Monitoring threads
# Vérifier threads actifs :
sudo ss -tulpn | grep clamd
# Ou
ps aux | grep clamd | wc -l
```

**Limites mémoire et fichiers :**

```bash
# Limites scan (anti-DoS, anti zip-bomb)

# Max size fichier total à scanner
MaxScanSize 100M
# Fichier > 100MB skipped (log warning)

# Max size fichier individuel extrait d'archive
MaxFileSize 25M

# Max profondeur récursion archives
MaxRecursion 16
# archive.zip → nested1.zip → nested2.zip → ... (max 16)

# Max fichiers dans archive
MaxFiles 10000
# Archive avec >10000 fichiers considérée zip-bomb

# Max size archive compressée
#MaxEmbeddedPE 10M

# Calculer mémoire nécessaire :
# RAM = (MaxThreads × MaxFileSize) + signatures_size + overhead
# Exemple : (10 × 25MB) + 300MB + 100MB = ~650MB minimum
```

**Optimisation signatures :**

```bash
# Désactiver signatures non pertinentes (économise RAM)

# /etc/clamav/clamd.conf

# Désactiver détection phishing (si pas mail server)
#PhishingSignatures no
#PhishingScanURLs no

# Désactiver bytecode signatures (économise CPU)
#Bytecode no

# Limiter types fichiers scannés
#ScanPE yes        # Windows executables
#ScanELF yes       # Linux binaries
#ScanOLE2 yes      # MS Office
#ScanPDF yes       # PDFs
#ScanHTML yes      # HTML
#ScanArchive yes   # Archives

# Désactiver ceux non requis économise ~20% RAM
```

### 3.4 Monitoring Daemon

**Stats temps réel :**

```bash
# Installer clamdtop (si dispo)
sudo apt install clamav-daemon  # Inclus généralement

# Monitorer daemon temps réel
clamdtop

# Output :
# Clamd Statistics
# Uptime: 2d 14h 35m 12s
# Live threads: 3/10
# Queue: 0
# Mem heap: 425.3M
# Mem pools: 387.2M
# Scanned dirs: 15234
# Scanned files: 245678
# Infected files: 3
```

**Logs monitoring :**

```bash
# Tail logs clamd
sudo tail -f /var/log/clamav/clamav.log

# Tail logs freshclam
sudo tail -f /var/log/clamav/freshclam.log

# Extraire infections détectées
sudo grep "FOUND" /var/log/clamav/clamav.log

# Compter infections par jour
sudo grep "$(date +%Y-%m-%d)" /var/log/clamav/clamav.log | grep -c "FOUND"

# Alertes automatiques (logwatch, fail2ban, custom script)
```

**Healthcheck script :**

```bash
#!/bin/bash
# /usr/local/bin/clamd-healthcheck.sh

# Ping daemon
if ! clamdscan --ping > /dev/null 2>&1; then
    echo "ERROR: clamd not responding"
    systemctl restart clamav-daemon
    exit 1
fi

# Vérifier âge signatures (doit être < 2 jours)
MAIN_AGE=$(stat -c %Y /var/lib/clamav/main.cvd)
NOW=$(date +%s)
AGE_HOURS=$(( (NOW - MAIN_AGE) / 3600 ))

if [ $AGE_HOURS -gt 48 ]; then
    echo "WARNING: Signatures outdated ($AGE_HOURS hours old)"
    freshclam
fi

# Vérifier mémoire daemon
MEM_USAGE=$(ps aux | grep clamd | grep -v grep | awk '{print $6}')
if [ $MEM_USAGE -gt 2000000 ]; then  # >2GB
    echo "WARNING: High memory usage: ${MEM_USAGE}KB"
fi

echo "OK: clamd healthy"
```

---

## Section 4 : Scan Manuel (clamscan/clamdscan)

### 4.1 clamscan (CLI Scanner)

**Syntaxe basique :**

```bash
# Scanner fichier unique
clamscan /path/to/file.pdf

# Scanner directory récursif
clamscan -r /home/user/downloads

# Scanner avec résumé
clamscan -r --bell /var/www
# --bell = beep si infection trouvée

# Output typique :
# /home/user/file.txt: OK
# /home/user/malware.exe: Win.Trojan.Agent-123456 FOUND
# /home/user/archive.zip: OK
# 
# ----------- SCAN SUMMARY -----------
# Known viruses: 8647427
# Engine version: 1.0.3
# Scanned directories: 15
# Scanned files: 235
# Infected files: 1
# Data scanned: 450.23 MB
# Time: 125.456 sec (2 m 5 s)
```

**Options essentielles :**

```bash
# --infected (-i) : afficher SEULEMENT fichiers infectés
clamscan -r -i /var/www

# --remove : supprimer fichiers infectés (DANGEREUX)
clamscan -r --remove /tmp/uploads

# --move=DIR : déplacer infectés vers quarantaine
clamscan -r --move=/var/quarantine /home

# --copy=DIR : copier infectés (garde original)
clamscan -r --copy=/var/quarantine /home

# --log=FILE : sauvegarder résultat
clamscan -r --log=/var/log/scan-$(date +%Y%m%d).log /var/www

# --max-filesize=SIZE : skip fichiers > SIZE
clamscan -r --max-filesize=50M /data

# --max-scansize=SIZE : max data à scanner par fichier
clamscan -r --max-scansize=100M /data

# --exclude=REGEX : exclure patterns
clamscan -r --exclude="\.git" --exclude="node_modules" /home/dev

# --exclude-dir=PATTERN : exclure directories
clamscan -r --exclude-dir="^/proc" --exclude-dir="^/sys" /

# --file-list=FILE : scanner fichiers listés dans file
find /var/www -type f -mtime -1 > /tmp/recent-files.txt
clamscan --file-list=/tmp/recent-files.txt
```

**Scan complet système (avec exclusions) :**

```bash
#!/bin/bash
# scan-full-system.sh

LOGFILE="/var/log/clamav/full-scan-$(date +%Y%m%d).log"
QUARANTINE="/var/quarantine"

# Créer quarantine dir
mkdir -p $QUARANTINE

# Full system scan (exclude système directories)
clamscan -r \
    --infected \
    --move=$QUARANTINE \
    --log=$LOGFILE \
    --exclude-dir="^/sys" \
    --exclude-dir="^/proc" \
    --exclude-dir="^/dev" \
    --exclude-dir="^/run" \
    --max-filesize=100M \
    --max-scansize=250M \
    /

# Résumé par email
if grep -q "Infected files: 0" $LOGFILE; then
    echo "✅ Scan OK - No infections" | mail -s "ClamAV Scan Clean" admin@example.com
else
    INFECTED=$(grep "Infected files:" $LOGFILE)
    echo "⚠️ $INFECTED" | mail -s "ClamAV Scan ALERT" admin@example.com
fi
```

### 4.2 clamdscan (Daemon Client)

**Avantages vs clamscan :**

```bash
# clamdscan = client léger communique avec clamd daemon
# Signatures déjà loaded en mémoire (pas de reload)
# Multi-thread scanning via daemon

# Speed comparison :
time clamscan -r /var/www    # ~15 minutes
time clamdscan -r /var/www   # ~2 minutes

# Syntaxe similaire à clamscan
clamdscan -r /var/www
clamdscan --infected --move=/var/quarantine /uploads
clamdscan --log=/var/log/scan.log /home
```

**Options spécifiques clamdscan :**

```bash
# --stream : stream fichiers via socket (recommandé grandes files)
clamdscan --stream /path/to/large-file.zip

# --fdpass : pass file descriptor (plus rapide, Unix socket uniquement)
clamdscan --fdpass /path/to/file

# --multiscan : scan multi-thread (obsolète, default maintenant)
clamdscan --multiscan -r /var/www

# --ping : vérifier daemon vivant
clamdscan --ping
# Output : PONG

# --reload : recharger signatures daemon
clamdscan --reload

# --config-file : utiliser config custom
clamdscan --config-file=/etc/clamav/custom.conf -r /data
```

**Intégration scripts :**

```bash
#!/bin/bash
# scan-directory.sh - Wrapper clamdscan avec notifications

SCAN_DIR="$1"
QUARANTINE="/var/quarantine"
LOGFILE="/var/log/clamav/scan-$(date +%Y%m%d-%H%M%S).log"

if [ -z "$SCAN_DIR" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Vérifier daemon running
if ! clamdscan --ping > /dev/null 2>&1; then
    echo "ERROR: clamd daemon not running"
    systemctl start clamav-daemon
    sleep 5
fi

# Scan avec logging
echo "Scanning $SCAN_DIR..."
clamdscan -r \
    --infected \
    --move=$QUARANTINE \
    --log=$LOGFILE \
    "$SCAN_DIR"

# Parse résultats
INFECTED=$(grep "Infected files:" $LOGFILE | awk '{print $3}')

if [ "$INFECTED" -gt 0 ]; then
    echo "⚠️ ALERT: $INFECTED infected file(s) found"
    echo "Moved to quarantine: $QUARANTINE"
    
    # Envoyer alerte
    grep "FOUND" $LOGFILE | mail -s "ClamAV Alert: $INFECTED infections" admin@example.com
else
    echo "✅ Scan clean - No infections"
fi

# Cleanup old logs (garder 30 jours)
find /var/log/clamav -name "scan-*.log" -mtime +30 -delete
```

### 4.3 Scan Types Spécialisés

**Scan fichiers uploadés web :**

```bash
# Hook upload (PHP, Python, Node.js)
# Exemple PHP :

<?php
// scan-upload.php

$uploadDir = '/var/www/uploads';
$quarantineDir = '/var/quarantine';

if ($_FILES['file']) {
    $tmpFile = $_FILES['file']['tmp_name'];
    $fileName = basename($_FILES['file']['name']);
    
    // Scan avec clamdscan
    $cmd = "clamdscan --no-summary " . escapeshellarg($tmpFile);
    exec($cmd, $output, $return);
    
    if ($return === 0) {
        // Clean - déplacer vers uploads
        move_uploaded_file($tmpFile, "$uploadDir/$fileName");
        echo "File uploaded successfully";
    } else {
        // Infected - quarantaine
        move_uploaded_file($tmpFile, "$quarantineDir/$fileName");
        error_log("Infected file upload attempt: $fileName");
        http_response_code(403);
        echo "File rejected: malware detected";
    }
}
?>
```

**Scan emails (attachments) :**

```bash
# Extraire attachments email et scanner
# Exemple avec Python :

#!/usr/bin/env python3
import email
import subprocess
import tempfile
import os

def scan_email(email_file):
    with open(email_file, 'rb') as f:
        msg = email.message_from_binary_file(f)
    
    infected = []
    
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        
        filename = part.get_filename()
        if filename:
            # Sauvegarder attachment temporaire
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(part.get_payload(decode=True))
                tmp_path = tmp.name
            
            # Scanner avec clamdscan
            result = subprocess.run(
                ['clamdscan', '--no-summary', tmp_path],
                capture_output=True, text=True
            )
            
            if result.returncode != 0:
                infected.append(filename)
            
            os.unlink(tmp_path)
    
    return infected

# Usage
infected = scan_email('/var/mail/user/message.eml')
if infected:
    print(f"Infected attachments: {infected}")
```

**Scan archives compressées :**

```bash
# ClamAV unpack automatiquement, mais on peut forcer :

# Scanner archive sans extraction
clamdscan archive.zip

# Extraire et scanner (plus verbeux)
unzip -d /tmp/extract archive.zip
clamdscan -r /tmp/extract
rm -rf /tmp/extract

# Scanner archives imbriquées (limite profondeur)
clamdscan --max-recursion=10 deeply-nested.zip

# Détecter zip bombs
# ClamAV détecte automatiquement ratios compression suspects
# MaxScanSize et MaxFiles dans clamd.conf limitent damage
```

---

## Section 5 : Mise à Jour Signatures (freshclam)

### 5.1 Configuration Freshclam

**Configuration production (/etc/clamav/freshclam.conf) :**

```bash
# Commenté = disabled
#Example

# Database directory
DatabaseDirectory /var/lib/clamav

# Logs
UpdateLogFile /var/log/clamav/freshclam.log
LogFileMaxSize 10M
LogTime yes
LogVerbose no
LogSyslog yes  # Aussi logger vers syslog

# Mirror (Cloudflare CDN)
DatabaseMirror database.clamav.net
# Mirrors backup (fallback automatique)
#DatabaseMirror db.local.clamav.net

# Fréquence checks
Checks 24  # 24 fois/jour = toutes les heures

# Notifications
#OnUpdateExecute /usr/local/bin/clamav-updated.sh
#OnErrorExecute /usr/local/bin/clamav-error.sh
#OnOutdatedExecute /usr/local/bin/clamav-outdated.sh

# User
DatabaseOwner clamav

# Compression (économise bande passante)
CompressLocalDatabase yes

# Proxy (si requis)
#HTTPProxyServer proxy.example.com
#HTTPProxyPort 8080
#HTTPProxyUsername username
#HTTPProxyPassword password

# Notifications email (optionnel)
#NotifyClamd /etc/clamav/clamd.conf
```

### 5.2 Update Manuel

```bash
# Update signatures manuellement
sudo freshclam

# Output détaillé :
# ClamAV update process started at Tue Jan 16 14:30:00 2024
# Downloading main.cvd [100%]
# main.cvd updated (version: 62, sigs: 6647427)
# Downloading daily.cvd [100%]
# daily.cvd updated (version: 27074, sigs: 2030118)
# Downloading bytecode.cvd [100%]
# bytecode.cvd updated (version: 334, sigs: 91)
# Database updated successfully

# Forcer re-download complet (si corruption)
sudo freshclam --force

# Dry-run (test sans download)
sudo freshclam --test-databases

# Verbose output (debugging)
sudo freshclam --verbose

# Vérifier version signatures
sigtool --info /var/lib/clamav/main.cvd
sigtool --info /var/lib/clamav/daily.cvd
```

### 5.3 Service Automatique

```bash
# Service systemd freshclam (updates automatiques)
sudo systemctl enable clamav-freshclam
sudo systemctl start clamav-freshclam

# Vérifier status
sudo systemctl status clamav-freshclam

# Logs
sudo journalctl -u clamav-freshclam -f

# Restart service (si problème)
sudo systemctl restart clamav-freshclam

# Configuration systemd override (si nécessaire)
sudo systemctl edit clamav-freshclam

# Exemple override : changer intervalle
[Service]
# Check every 30 minutes instead of default
ExecStart=
ExecStart=/usr/bin/freshclam -d --checks=48
```

### 5.4 Monitoring Updates

**Script monitoring signatures :**

```bash
#!/bin/bash
# /usr/local/bin/check-clamav-signatures.sh

MAIN_DB="/var/lib/clamav/main.cvd"
DAILY_DB="/var/lib/clamav/daily.cvd"
ALERT_EMAIL="admin@example.com"
MAX_AGE_HOURS=48  # Alert si signatures >2 jours

# Fonction check age
check_db_age() {
    DB_FILE=$1
    DB_NAME=$(basename $DB_FILE)
    
    if [ ! -f "$DB_FILE" ]; then
        echo "ERROR: $DB_NAME not found"
        return 1
    fi
    
    TIMESTAMP=$(stat -c %Y "$DB_FILE")
    NOW=$(date +%s)
    AGE_HOURS=$(( (NOW - TIMESTAMP) / 3600 ))
    
    echo "$DB_NAME age: $AGE_HOURS hours"
    
    if [ $AGE_HOURS -gt $MAX_AGE_HOURS ]; then
        echo "WARNING: $DB_NAME outdated ($AGE_HOURS hours old)"
        return 1
    fi
    
    return 0
}

# Check databases
ERRORS=0

check_db_age "$MAIN_DB" || ERRORS=$((ERRORS + 1))
check_db_age "$DAILY_DB" || ERRORS=$((ERRORS + 1))

# Si erreurs, tenter update
if [ $ERRORS -gt 0 ]; then
    echo "Attempting signature update..."
    freshclam
    
    # Vérifier succès
    if [ $? -eq 0 ]; then
        echo "Update successful"
    else
        echo "Update failed - sending alert"
        echo "ClamAV signatures update failed" | \
            mail -s "ClamAV Alert: Outdated Signatures" $ALERT_EMAIL
    fi
fi

# Cron job : toutes les 6 heures
# 0 */6 * * * /usr/local/bin/check-clamav-signatures.sh
```

**Prometheus metrics (monitoring avancé) :**

```bash
# Exporter métriques ClamAV pour Prometheus
# /usr/local/bin/clamav-exporter.sh

#!/bin/bash

METRICS_FILE="/var/lib/node_exporter/clamav.prom"

# Version
VERSION=$(clamscan --version | head -1 | awk '{print $3}' | tr -d '/')

# Age signatures
MAIN_AGE=$(( ($(date +%s) - $(stat -c %Y /var/lib/clamav/main.cvd)) / 3600 ))
DAILY_AGE=$(( ($(date +%s) - $(stat -c %Y /var/lib/clamav/daily.cvd)) / 3600 ))

# Nombre signatures
SIGNATURES=$(sigtool --info /var/lib/clamav/main.cvd | grep "Signatures:" | awk '{print $2}')

# Générer metrics
cat > $METRICS_FILE << EOF
# HELP clamav_signatures_total Total number of virus signatures
# TYPE clamav_signatures_total gauge
clamav_signatures_total $SIGNATURES

# HELP clamav_database_age_hours Age of signature database in hours
# TYPE clamav_database_age_hours gauge
clamav_database_age_hours{database="main"} $MAIN_AGE
clamav_database_age_hours{database="daily"} $DAILY_AGE

# HELP clamav_version ClamAV version
# TYPE clamav_version gauge
clamav_version{version="$VERSION"} 1
EOF

# Cron : */5 * * * * /usr/local/bin/clamav-exporter.sh
```

---

## Section 6 : On-Access Scanning Temps Réel

### 6.1 clamonacc (On-Access Scanner)

**Installation et configuration :**

```bash
# Vérifier clamonacc installé (ClamAV 0.102+)
which clamonacc
# /usr/sbin/clamonacc

# Configuration clamd.conf (requis pour clamonacc)
sudo nano /etc/clamav/clamd.conf

# Activer on-access scanning
ScanOnAccess yes

# Directories à monitorer
OnAccessIncludePath /home
OnAccessIncludePath /var/www
OnAccessIncludePath /tmp

# Exclusions (performances)
OnAccessExcludePath /var/lib/clamav
OnAccessExcludePath /sys
OnAccessExcludePath /proc

# Options on-access
OnAccessMaxFileSize 10M         # Skip fichiers >10MB
OnAccessPrevention yes          # Bloquer accès fichiers infectés
OnAccessExtraScanning yes       # Scan aussi en lecture (pas seulement écriture)
OnAccessDisableDDD yes          # Désactiver détection DDD (économise CPU)

# User clamd (doit avoir permissions)
User clamav

# Restart clamd
sudo systemctl restart clamav-daemon
```

**Démarrer clamonacc :**

```bash
# Démarrer manuellement (foreground)
sudo clamonacc -F

# Background
sudo clamonacc

# Avec logging verbeux (debugging)
sudo clamonacc -F --log=/var/log/clamav/clamonacc.log --verbose

# Options utiles
sudo clamonacc \
    --log=/var/log/clamav/clamonacc.log \
    --move=/var/quarantine \
    --exclude-dir=/sys \
    --exclude-dir=/proc \
    --fdpass  # File descriptor passing (plus rapide)
```

**Service systemd clamonacc :**

```bash
# Créer service systemd
sudo nano /etc/systemd/system/clamonacc.service

[Unit]
Description=ClamAV On-Access Scanner
Requires=clamav-daemon.service
After=clamav-daemon.service

[Service]
Type=simple
User=root
ExecStart=/usr/sbin/clamonacc -F --log=/var/log/clamav/clamonacc.log --move=/var/quarantine --fdpass
Restart=on-failure

[Install]
WantedBy=multi-user.target

# Activer service
sudo systemctl daemon-reload
sudo systemctl enable clamonacc
sudo systemctl start clamonacc

# Vérifier
sudo systemctl status clamonacc
```

### 6.2 Kernel fanotify (Backend)

**fanotify = API kernel Linux pour monitoring filesystem events**

```bash
# Vérifier support kernel
grep FANOTIFY /boot/config-$(uname -r)
# CONFIG_FANOTIFY=y
# CONFIG_FANOTIFY_ACCESS_PERMISSIONS=y

# clamonacc utilise fanotify automatiquement si disponible

# Permissions requises :
# - CAP_SYS_ADMIN capability
# - Généralement run as root

# Limitations :
# - Linux kernel 3.8+ requis
# - Pas de support réseau filesystems (NFS, CIFS)
# - Impact performance si trop de paths monitorés
```

### 6.3 Alternative : inotify + scan

**Pour kernels anciens sans fanotify :**

```bash
#!/bin/bash
# /usr/local/bin/inotify-clamav.sh
# Monitor directory avec inotify + scan auto

WATCH_DIR="/var/www/uploads"
QUARANTINE="/var/quarantine"

# Installer inotify-tools
sudo apt install inotify-tools

# Monitor directory
inotifywait -m -r -e close_write,moved_to "$WATCH_DIR" --format '%w%f' | while read FILE
do
    echo "Scanning new file: $FILE"
    
    # Scanner avec clamdscan
    RESULT=$(clamdscan --no-summary "$FILE")
    
    if echo "$RESULT" | grep -q "FOUND"; then
        VIRUS=$(echo "$RESULT" | grep "FOUND" | awk '{print $2}')
        echo "⚠️ INFECTED: $FILE - $VIRUS"
        
        # Déplacer vers quarantaine
        mv "$FILE" "$QUARANTINE/"
        
        # Logger
        logger -t clamav-inotify "Infected file quarantined: $FILE ($VIRUS)"
        
        # Alerte
        echo "Infected file: $FILE ($VIRUS)" | \
            mail -s "ClamAV Alert" admin@example.com
    else
        echo "✓ Clean: $FILE"
    fi
done

# Run as daemon :
# nohup /usr/local/bin/inotify-clamav.sh > /var/log/inotify-clamav.log 2>&1 &
```

### 6.4 Performance Impact

**Mesurer overhead on-access scanning :**

```bash
# Benchmark sans on-access
systemctl stop clamonacc
time dd if=/dev/zero of=/tmp/test bs=1M count=1000
# ~5 seconds

# Benchmark avec on-access
systemctl start clamonacc
time dd if=/dev/zero of=/tmp/test bs=1M count=1000
# ~7 seconds (+40% overhead)

# Impact typique :
# - Writes : +20-40% latence
# - Reads : +5-10% latence (si OnAccessExtraScanning yes)
# - CPU : +5-15% usage continu

# Optimisations :
# 1. Limiter paths monitorés (seulement uploads, shares)
# 2. OnAccessMaxFileSize (skip large files)
# 3. Exclusions (/sys, /proc, logs, DB files)
# 4. OnAccessExtraScanning no (scan writes seulement)
```

---

## Section 7 : Intégration Mail Servers

### 7.1 Architecture Mail Scanning

```
Mail Flow avec ClamAV :

Internet → MTA (Postfix/Exim) → Amavis → ClamAV → Mailbox
                 ↓                  ↓        ↓
              25/587            10024     clamd
                                          (scan)
                                           ↓
                                    Infected? → Quarantine
                                    Clean? → Deliver
```

### 7.2 Postfix + Amavis + ClamAV

**Installation :**

```bash
# Installer composants
sudo apt install postfix amavisd-new clamav clamav-daemon

# Services
sudo systemctl enable clamav-daemon amavisd-new
sudo systemctl start clamav-daemon amavisd-new
```

**Configuration Amavis (/etc/amavis/conf.d/15-content_filter_mode) :**

```perl
# Activer virus checking
@bypass_virus_checks_maps = (
   \%bypass_virus_checks, \@bypass_virus_checks_acl, \$bypass_virus_checks_re);

# Activer spam checking
@bypass_spam_checks_maps = (
   \%bypass_spam_checks, \@bypass_spam_checks_acl, \$bypass_spam_checks_re);
```

**Configuration Amavis (/etc/amavis/conf.d/50-user) :**

```perl
# Domain name
$mydomain = 'example.com';

# Listen on port 10024 (receive from Postfix)
$inet_socket_port = 10024;

# Forward to Postfix on port 10025
$forward_method = 'smtp:[127.0.0.1]:10025';
$notify_method = $forward_method;

# ClamAV scanner
['ClamAV-clamd',
  \&ask_daemon, ["CONTSCAN {}\n", "/var/run/clamav/clamd.sock"],
  qr/\bOK$/m, qr/\bFOUND$/m,
  qr/^.*?: (?!Infected Archive)(.*) FOUND$/m ],

# Actions
$final_virus_destiny = D_DISCARD;  # Discard (or D_BOUNCE, D_REJECT, D_PASS)
$final_banned_destiny = D_BOUNCE;
$final_spam_destiny = D_PASS;      # Mark spam, deliver anyway

# Quarantine
$QUARANTINEDIR = '/var/lib/amavis/virusmails';

# Notifications
$virus_admin = 'postmaster@example.com';
$mailfrom_notify_admin = 'amavis@example.com';
$mailfrom_notify_recip = 'amavis@example.com';

# Limits
$max_servers = 5;
$max_requests = 10;

# Enable notifications
$warnvirusrecip = 1;
$warnbadhrecip = 1;
```

**Configuration Postfix (/etc/postfix/main.cf) :**

```bash
# Content filter (envoyer vers Amavis)
content_filter = smtp-amavis:[127.0.0.1]:10024

# Receive from Amavis
smtpd_recipient_restrictions = 
    permit_mynetworks,
    permit_sasl_authenticated,
    reject_unauth_destination

# After Amavis processing
receive_override_options = no_address_mappings
```

**Configuration Postfix (/etc/postfix/master.cf) :**

```bash
# Amavis content filter
smtp-amavis unix -      -       n       -       2  smtp
    -o smtp_data_done_timeout=1200
    -o smtp_send_xforward_command=yes
    -o disable_dns_lookups=yes
    -o max_use=20

# Receive back from Amavis
127.0.0.1:10025 inet n  -       n       -       -  smtpd
    -o content_filter=
    -o local_recipient_maps=
    -o relay_recipient_maps=
    -o smtpd_restriction_classes=
    -o smtpd_delay_reject=no
    -o smtpd_client_restrictions=permit_mynetworks,reject
    -o smtpd_helo_restrictions=
    -o smtpd_sender_restrictions=
    -o smtpd_recipient_restrictions=permit_mynetworks,reject
    -o smtpd_data_restrictions=reject_unauth_pipelining
    -o smtpd_end_of_data_restrictions=
    -o mynetworks=127.0.0.0/8
    -o smtpd_error_sleep_time=0
    -o smtpd_soft_error_limit=1001
    -o smtpd_hard_error_limit=1000
    -o smtpd_client_connection_count_limit=0
    -o smtpd_client_connection_rate_limit=0
    -o receive_override_options=no_header_body_checks,no_unknown_recipient_checks
```

**Restart services :**

```bash
sudo systemctl restart clamav-daemon
sudo systemctl restart amavisd-new
sudo systemctl restart postfix

# Vérifier
sudo systemctl status clamav-daemon amavisd-new postfix

# Test mail flow
echo "Test email" | mail -s "Test" user@example.com

# Logs
sudo tail -f /var/log/mail.log
sudo tail -f /var/log/clamav/clamav.log
```

### 7.3 Tester Scanning Mail

**EICAR test file (test virus inoffensif) :**

```bash
# Créer fichier EICAR test
cat > /tmp/eicar.txt << 'EOF'
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
EOF

# Envoyer par email
echo "Test virus" | mail -s "EICAR Test" -a /tmp/eicar.txt user@example.com

# Vérifier logs
sudo tail -f /var/log/mail.log | grep -i virus
# Doit voir : "Blocked INFECTED (Eicar-Test-Signature)"

# Vérifier quarantine
sudo ls -lh /var/lib/amavis/virusmails/
```

**Script test complet :**

```bash
#!/bin/bash
# test-mail-scanning.sh

TEST_EMAIL="postmaster@example.com"

# Test 1 : Email clean
echo "Clean email test" | mail -s "Test Clean" $TEST_EMAIL
echo "✓ Test 1: Clean email sent"

# Test 2 : EICAR attachment
cat > /tmp/eicar.txt << 'EOF'
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
EOF
echo "Virus test" | mail -s "Test EICAR" -a /tmp/eicar.txt $TEST_EMAIL
echo "✓ Test 2: EICAR attachment sent (should be blocked)"

# Test 3 : Archive avec EICAR
cd /tmp
zip eicar.zip eicar.txt
echo "Archived virus test" | mail -s "Test EICAR ZIP" -a eicar.zip $TEST_EMAIL
echo "✓ Test 3: EICAR in ZIP sent (should be blocked)"

# Attendre 10s
sleep 10

# Vérifier logs
echo ""
echo "=== Mail Logs ==="
sudo grep -i "eicar\|virus\|infected" /var/log/mail.log | tail -20

echo ""
echo "=== ClamAV Logs ==="
sudo grep -i "eicar\|found" /var/log/clamav/clamav.log | tail -10

# Cleanup
rm /tmp/eicar.txt /tmp/eicar.zip
```

---

## Section 8 : Intégration Web Servers

### 8.1 PHP File Upload Scanning

**Fonction PHP scan upload :**

```php
<?php
// /var/www/html/includes/clamav-scan.php

class ClamAVScanner {
    private $socket = '/var/run/clamav/clamd.sock';
    private $quarantine = '/var/quarantine';
    
    public function scanFile($filePath) {
        if (!file_exists($filePath)) {
            return ['error' => 'File not found'];
        }
        
        // Connecter socket ClamAV
        $socket = socket_create(AF_UNIX, SOCK_STREAM, 0);
        if (!socket_connect($socket, $this->socket)) {
            return ['error' => 'Cannot connect to ClamAV daemon'];
        }
        
        // Envoyer commande SCAN
        $cmd = "SCAN " . $filePath . "\n";
        socket_write($socket, $cmd, strlen($cmd));
        
        // Lire résultat
        $response = '';
        while ($buf = socket_read($socket, 1024)) {
            $response .= $buf;
        }
        socket_close($socket);
        
        // Parser résultat
        if (strpos($response, 'OK') !== false) {
            return ['status' => 'clean'];
        } elseif (strpos($response, 'FOUND') !== false) {
            preg_match('/: (.+) FOUND/', $response, $matches);
            $virus = $matches[1] ?? 'Unknown';
            return ['status' => 'infected', 'virus' => $virus];
        } else {
            return ['error' => 'Scan failed', 'response' => $response];
        }
    }
    
    public function quarantineFile($filePath, $originalName) {
        $quarantinePath = $this->quarantine . '/' . 
            date('Ymd_His') . '_' . basename($originalName);
        
        if (rename($filePath, $quarantinePath)) {
            chmod($quarantinePath, 0000); // Remove all permissions
            return true;
        }
        return false;
    }
}

// Usage dans upload handler
if ($_FILES['file']) {
    $tmpFile = $_FILES['file']['tmp_name'];
    $fileName = $_FILES['file']['name'];
    
    $scanner = new ClamAVScanner();
    $result = $scanner->scanFile($tmpFile);
    
    if (isset($result['error'])) {
        http_response_code(500);
        echo json_encode(['error' => $result['error']]);
    } elseif ($result['status'] === 'infected') {
        // Quarantine
        $scanner->quarantineFile($tmpFile, $fileName);
        
        // Log
        error_log("Infected upload: $fileName - " . $result['virus']);
        
        http_response_code(403);
        echo json_encode([
            'error' => 'File rejected: malware detected',
            'virus' => $result['virus']
        ]);
    } else {
        // Clean - process upload
        move_uploaded_file($tmpFile, '/var/www/uploads/' . $fileName);
        echo json_encode(['success' => true]);
    }
}
?>
```

### 8.2 Python Flask Integration

```python
# /var/www/app/clamav_scanner.py

import socket
import os
import shutil
from datetime import datetime

class ClamAVScanner:
    def __init__(self, socket_path='/var/run/clamav/clamd.sock'):
        self.socket_path = socket_path
        self.quarantine_dir = '/var/quarantine'
        
    def scan_file(self, file_path):
        """Scan file via ClamAV socket"""
        try:
            # Connect to clamd socket
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.socket_path)
            
            # Send SCAN command
            cmd = f"SCAN {file_path}\n".encode()
            sock.send(cmd)
            
            # Read response
            response = sock.recv(4096).decode()
            sock.close()
            
            # Parse response
            if 'OK' in response:
                return {'status': 'clean'}
            elif 'FOUND' in response:
                virus_name = response.split(': ')[1].split(' FOUND')[0]
                return {'status': 'infected', 'virus': virus_name}
            else:
                return {'error': 'Scan failed', 'response': response}
                
        except Exception as e:
            return {'error': str(e)}
    
    def quarantine_file(self, file_path, original_name):
        """Move infected file to quarantine"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        quarantine_path = os.path.join(
            self.quarantine_dir,
            f"{timestamp}_{os.path.basename(original_name)}"
        )
        
        try:
            shutil.move(file_path, quarantine_path)
            os.chmod(quarantine_path, 0o000)  # Remove all permissions
            return True
        except Exception as e:
            print(f"Quarantine failed: {e}")
            return False

# Flask app integration
from flask import Flask, request, jsonify
import tempfile

app = Flask(__name__)
scanner = ClamAVScanner()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Save to temp location
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        # Scan file
        result = scanner.scan_file(tmp_path)
        
        if 'error' in result:
            return jsonify(result), 500
        
        if result['status'] == 'infected':
            # Quarantine
            scanner.quarantine_file(tmp_path, file.filename)
            
            return jsonify({
                'error': 'File rejected: malware detected',
                'virus': result['virus']
            }), 403
        
        # Clean - move to uploads
        upload_path = f"/var/www/uploads/{file.filename}"
        shutil.move(tmp_path, upload_path)
        
        return jsonify({'success': True, 'file': file.filename})
        
    finally:
        # Cleanup temp file if still exists
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 8.3 Nginx Upload Module + ClamAV

**Nginx avec upload module et script scan :**

```nginx
# /etc/nginx/sites-available/upload

server {
    listen 80;
    server_name upload.example.com;
    
    client_max_body_size 100M;
    
    location /upload {
        # Upload module config
        upload_pass /upload_handler;
        upload_store /tmp/nginx_upload;
        upload_store_access user:rw group:rw all:r;
        
        # Pass metadata to handler
        upload_set_form_field $upload_field_name.name "$upload_file_name";
        upload_set_form_field $upload_field_name.path "$upload_tmp_path";
        
        upload_cleanup 400 404 499 500-505;
    }
    
    location /upload_handler {
        proxy_pass http://127.0.0.1:5000/scan_and_process;
    }
}
```

**Handler script (Python Flask) :**

```python
# /var/www/upload-handler/app.py

from flask import Flask, request, jsonify
import subprocess
import os
import shutil

app = Flask(__name__)

UPLOAD_DIR = '/var/www/uploads'
QUARANTINE_DIR = '/var/quarantine'

@app.route('/scan_and_process', methods=['POST'])
def scan_and_process():
    # Get uploaded file path from Nginx
    file_path = request.form.get('file.path')
    file_name = request.form.get('file.name')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 400
    
    # Scan with clamdscan
    result = subprocess.run(
        ['clamdscan', '--no-summary', file_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        # Clean - move to uploads
        dest = os.path.join(UPLOAD_DIR, file_name)
        shutil.move(file_path, dest)
        return jsonify({'status': 'success', 'file': file_name})
    else:
        # Infected - quarantine
        dest = os.path.join(QUARANTINE_DIR, file_name)
        shutil.move(file_path, dest)
        os.chmod(dest, 0o000)
        
        # Extract virus name
        virus = 'Unknown'
        if 'FOUND' in result.stdout:
            virus = result.stdout.split(': ')[1].split(' FOUND')[0]
        
        return jsonify({
            'status': 'rejected',
            'reason': 'malware detected',
            'virus': virus
        }), 403

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

---

## Section 9 : Automatisation et Monitoring

### 9.1 Cron Jobs Scan Automatique

**Scan quotidien complet :**

```bash
# /etc/cron.d/clamav-daily-scan

# Scan complet système tous les jours 2h du matin
0 2 * * * root /usr/local/bin/clamav-full-scan.sh
```

**Script scan automatique :**

```bash
#!/bin/bash
# /usr/local/bin/clamav-full-scan.sh

DATE=$(date +%Y%m%d)
LOGDIR="/var/log/clamav/scans"
LOGFILE="$LOGDIR/scan-$DATE.log"
QUARANTINE="/var/quarantine"
ALERT_EMAIL="admin@example.com"

# Créer directories
mkdir -p $LOGDIR $QUARANTINE

# Scan avec clamdscan (rapide via daemon)
echo "=== ClamAV Full System Scan - $DATE ===" > $LOGFILE
echo "Started: $(date)" >> $LOGFILE

clamdscan -r \
    --infected \
    --move=$QUARANTINE \
    --exclude-dir="^/sys" \
    --exclude-dir="^/proc" \
    --exclude-dir="^/dev" \
    --exclude-dir="^/run" \
    --max-filesize=100M \
    --max-scansize=250M \
    / >> $LOGFILE 2>&1

echo "Completed: $(date)" >> $LOGFILE

# Parse résultats
INFECTED=$(grep "Infected files:" $LOGFILE | awk '{print $3}')
SCANNED=$(grep "Scanned files:" $LOGFILE | awk '{print $3}')

# Résumé
echo "" >> $LOGFILE
echo "=== Summary ===" >> $LOGFILE
echo "Scanned: $SCANNED files" >> $LOGFILE
echo "Infected: $INFECTED files" >> $LOGFILE

# Envoyer alerte si infections
if [ "$INFECTED" -gt 0 ]; then
    SUBJECT="⚠️ ClamAV Alert: $INFECTED infection(s) detected"
    
    # Email avec détails
    {
        echo "ClamAV detected $INFECTED infected file(s) on $(hostname)"
        echo ""
        echo "=== Infected Files ==="
        grep "FOUND" $LOGFILE
        echo ""
        echo "Files moved to: $QUARANTINE"
        echo ""
        echo "Full log: $LOGFILE"
    } | mail -s "$SUBJECT" $ALERT_EMAIL
else
    # Email succès (optionnel, peut désactiver)
    echo "Scan completed - No infections detected" | \
        mail -s "✅ ClamAV Scan Clean - $(hostname)" $ALERT_EMAIL
fi

# Cleanup old logs (garder 90 jours)
find $LOGDIR -name "scan-*.log" -mtime +90 -delete

# Cleanup old quarantine (garder 180 jours)
find $QUARANTINE -type f -mtime +180 -delete
```

### 9.2 Monitoring Dashboard

**Script métriques ClamAV :**

```bash
#!/bin/bash
# /usr/local/bin/clamav-metrics.sh
# Collecter métriques ClamAV pour monitoring

METRICS_DIR="/var/www/html/metrics"
METRICS_FILE="$METRICS_DIR/clamav.json"

mkdir -p $METRICS_DIR

# Daemon status
if systemctl is-active --quiet clamav-daemon; then
    DAEMON_STATUS="running"
else
    DAEMON_STATUS="stopped"
fi

# Signatures age
MAIN_AGE=$(( ($(date +%s) - $(stat -c %Y /var/lib/clamav/main.cvd)) / 3600 ))
DAILY_AGE=$(( ($(date +%s) - $(stat -c %Y /var/lib/clamav/daily.cvd)) / 3600 ))

# Signatures count
SIGNATURES=$(sigtool --info /var/lib/clamav/main.cvd 2>/dev/null | grep "Signatures:" | awk '{print $2}')
[ -z "$SIGNATURES" ] && SIGNATURES=0

# Version
VERSION=$(clamscan --version | head -1 | awk '{print $3}' | tr -d '/')

# Infections dernières 24h
INFECTIONS_24H=$(sudo grep "$(date +%Y-%m-%d)" /var/log/clamav/clamav.log 2>/dev/null | grep -c "FOUND")

# Dernière update freshclam
LAST_UPDATE=$(stat -c %Y /var/lib/clamav/daily.cvd)
LAST_UPDATE_HUMAN=$(date -d @$LAST_UPDATE)

# Quarantine stats
QUARANTINE_COUNT=$(find /var/quarantine -type f 2>/dev/null | wc -l)
QUARANTINE_SIZE=$(du -sh /var/quarantine 2>/dev/null | awk '{print $1}')

# Générer JSON
cat > $METRICS_FILE << EOF
{
  "timestamp": "$(date -Iseconds)",
  "daemon": {
    "status": "$DAEMON_STATUS",
    "version": "$VERSION"
  },
  "signatures": {
    "count": $SIGNATURES,
    "main_age_hours": $MAIN_AGE,
    "daily_age_hours": $DAILY_AGE,
    "last_update": "$LAST_UPDATE_HUMAN"
  },
  "detections": {
    "last_24h": $INFECTIONS_24H
  },
  "quarantine": {
    "files": $QUARANTINE_COUNT,
    "size": "$QUARANTINE_SIZE"
  }
}
EOF

# HTML dashboard simple
cat > $METRICS_DIR/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>ClamAV Dashboard</title>
    <meta http-equiv="refresh" content="60">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .metric { background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric h3 { margin-top: 0; color: #333; }
        .value { font-size: 24px; font-weight: bold; color: #007bff; }
        .warning { color: #ff9800; }
        .error { color: #f44336; }
        .success { color: #4caf50; }
    </style>
</head>
<body>
    <h1>ClamAV Monitoring Dashboard</h1>
    <div id="dashboard">Loading...</div>
    
    <script>
    async function loadMetrics() {
        const response = await fetch('clamav.json');
        const data = await response.json();
        
        let statusClass = data.daemon.status === 'running' ? 'success' : 'error';
        let signaturesClass = data.signatures.daily_age_hours < 48 ? 'success' : 'warning';
        
        document.getElementById('dashboard').innerHTML = `
            <div class="metric">
                <h3>Daemon Status</h3>
                <div class="value ${statusClass}">${data.daemon.status.toUpperCase()}</div>
                <div>Version: ${data.daemon.version}</div>
            </div>
            
            <div class="metric">
                <h3>Signatures</h3>
                <div class="value">${data.signatures.count.toLocaleString()}</div>
                <div class="${signaturesClass}">Last update: ${data.signatures.daily_age_hours}h ago</div>
                <div>${data.signatures.last_update}</div>
            </div>
            
            <div class="metric">
                <h3>Detections (24h)</h3>
                <div class="value ${data.detections.last_24h > 0 ? 'warning' : 'success'}">
                    ${data.detections.last_24h}
                </div>
            </div>
            
            <div class="metric">
                <h3>Quarantine</h3>
                <div class="value">${data.quarantine.files} files</div>
                <div>Total size: ${data.quarantine.size}</div>
            </div>
            
            <div class="metric">
                <small>Last updated: ${data.timestamp}</small>
            </div>
        `;
    }
    
    loadMetrics();
    setInterval(loadMetrics, 60000);
    </script>
</body>
</html>
EOF

# Permissions
chmod 644 $METRICS_FILE $METRICS_DIR/index.html

# Cron : */5 * * * * /usr/local/bin/clamav-metrics.sh
```

### 9.3 Prometheus Exporter

```python
#!/usr/bin/env python3
# /usr/local/bin/clamav-prometheus-exporter.py

from prometheus_client import start_http_server, Gauge, Counter
import subprocess
import time
import re
import os

# Metrics
daemon_up = Gauge('clamav_daemon_up', 'ClamAV daemon status')
signatures_total = Gauge('clamav_signatures_total', 'Total virus signatures')
signatures_age = Gauge('clamav_signatures_age_seconds', 'Age of signature database', ['database'])
scanned_files = Counter('clamav_scanned_files_total', 'Total files scanned')
infected_files = Counter('clamav_infected_files_total', 'Total infected files detected')

def check_daemon():
    """Check if clamd is running"""
    try:
        result = subprocess.run(['clamdscan', '--ping'], 
                              capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def get_signatures_count():
    """Get total signatures count"""
    try:
        result = subprocess.run(['sigtool', '--info', '/var/lib/clamav/main.cvd'],
                              capture_output=True, text=True)
        match = re.search(r'Signatures: (\d+)', result.stdout)
        return int(match.group(1)) if match else 0
    except:
        return 0

def get_signatures_age(db_path):
    """Get age of signature database in seconds"""
    try:
        stat = os.stat(db_path)
        return int(time.time() - stat.st_mtime)
    except:
        return 0

def parse_logs():
    """Parse ClamAV logs for metrics"""
    try:
        with open('/var/log/clamav/clamav.log', 'r') as f:
            for line in f:
                if 'FOUND' in line:
                    infected_files.inc()
                elif 'OK' in line or 'Empty file' in line:
                    scanned_files.inc()
    except:
        pass

def collect_metrics():
    """Collect all metrics"""
    # Daemon status
    daemon_up.set(1 if check_daemon() else 0)
    
    # Signatures
    signatures_total.set(get_signatures_count())
    signatures_age.labels(database='main').set(
        get_signatures_age('/var/lib/clamav/main.cvd')
    )
    signatures_age.labels(database='daily').set(
        get_signatures_age('/var/lib/clamav/daily.cvd')
    )

if __name__ == '__main__':
    # Start Prometheus HTTP server
    start_http_server(9810)
    print("ClamAV Prometheus exporter started on port 9810")
    
    while True:
        collect_metrics()
        time.sleep(60)
```

**Systemd service exporter :**

```bash
# /etc/systemd/system/clamav-exporter.service

[Unit]
Description=ClamAV Prometheus Exporter
After=network.target clamav-daemon.service

[Service]
Type=simple
User=clamav
ExecStart=/usr/local/bin/clamav-prometheus-exporter.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## Section 10 : Performance Tuning Production

### 10.1 Profiling Performance

**Benchmark scan speeds :**

```bash
#!/bin/bash
# benchmark-clamav.sh

TEST_DIR="/var/www"

echo "=== ClamAV Performance Benchmark ==="

# Test 1 : clamscan (cold start)
echo "1. clamscan (cold start)..."
time clamscan -r --no-summary $TEST_DIR > /dev/null 2>&1

# Test 2 : clamdscan (daemon)
echo "2. clamdscan (daemon, hot signatures)..."
time clamdscan -r --no-summary $TEST_DIR > /dev/null 2>&1

# Test 3 : Single large file
dd if=/dev/urandom of=/tmp/testfile bs=1M count=100
echo "3. Single 100MB file..."
time clamdscan /tmp/testfile > /dev/null 2>&1
rm /tmp/testfile

# Test 4 : Many small files
mkdir -p /tmp/smallfiles
for i in {1..1000}; do
    dd if=/dev/urandom of=/tmp/smallfiles/file$i bs=1K count=1 2>/dev/null
done
echo "4. 1000 small files (1KB each)..."
time clamdscan -r /tmp/smallfiles > /dev/null 2>&1
rm -rf /tmp/smallfiles
```

### 10.2 Optimisation Configuration

**clamd.conf optimisé pour serveur haute performance :**

```bash
# /etc/clamav/clamd.conf - Production optimized

# Socket
LocalSocket /var/run/clamav/clamd.sock
LocalSocketMode 666

# Threads (ajuster selon CPU)
# Formule : 1.5 × CPU cores
MaxThreads 16              # 10-12 cores

# Queue
MaxConnectionQueueLength 50
MaxQueue 300

# Timeouts
CommandReadTimeout 300
SendBufTimeout 500

# Memory & Size Limits
MaxScanSize 150M           # Augmenté (si RAM suffisante)
MaxFileSize 50M            # Augmenté
MaxRecursion 20            # Augmenté
MaxFiles 15000             # Augmenté
MaxEmbeddedPE 15M

# Performance optimizations
ScanArchive yes
ScanPE yes
ScanELF yes
ScanOLE2 yes
ScanPDF yes
ScanHTML yes

# Heuristic (coûteux CPU, ajuster selon besoins)
HeuristicScanPrecedence yes
HeuristicAlerts yes
HeuristicScanPrecedence yes

# Algorithmic detection (coûteux CPU)
AlgorithmicDetection yes

# Phishing detection (mail servers principalement)
PhishingSignatures yes
PhishingScanURLs yes

# Self-check moins fréquent (économise CPU)
SelfCheck 7200             # 2 heures au lieu 1 heure

# Logging (production)
LogFile /var/log/clamav/clamav.log
LogTime yes
LogFileMaxSize 50M
LogClean no                # Ne pas logger fichiers clean (économise I/O)
LogVerbose no

# Stats (optionnel)
#StatsEnabled yes
#StatsPEDisabled no
#StatsHostID auto
#StatsTimeout 10
```

### 10.3 Tuning Système OS

**Sysctl optimizations :**

```bash
# /etc/sysctl.d/99-clamav.conf

# Increase file descriptors
fs.file-max = 2097152
fs.nr_open = 2097152

# Network tuning (si TCP socket)
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 8192

# Memory
vm.swappiness = 10              # Limiter swap
vm.overcommit_memory = 1        # Allow memory overcommit

# Apply
sudo sysctl -p /etc/sysctl.d/99-clamav.conf
```

**Systemd service limits :**

```bash
# /etc/systemd/system/clamav-daemon.service.d/override.conf

[Service]
# Increase file descriptors
LimitNOFILE=65536

# Increase memory limit
MemoryLimit=2G

# CPU priority (nice level)
Nice=-5

# IO priority (best-effort, high)
IOSchedulingClass=best-effort
IOSchedulingPriority=2

# Reload systemd
sudo systemctl daemon-reload
sudo systemctl restart clamav-daemon
```

### 10.4 RAM vs Performance Trade-offs

**Calcul mémoire nécessaire :**

```
RAM minimum = Signatures + (MaxThreads × MaxFileSize) + Overhead

Exemple configuration :
- Signatures : ~400MB (main + daily + bytecode)
- MaxThreads : 10
- MaxFileSize : 25MB
- Overhead : ~200MB (system, buffers)

Total : 400 + (10 × 25) + 200 = 850MB minimum

Recommandation production :
- Small server (1-2GB RAM) : MaxThreads=4, MaxFileSize=10M
- Medium server (4-8GB RAM) : MaxThreads=10, MaxFileSize=25M
- Large server (16GB+ RAM) : MaxThreads=20, MaxFileSize=50M
```

**Monitoring mémoire :**

```bash
# Vérifier mémoire clamd
ps aux | grep clamd | grep -v grep
# OU
systemctl status clamav-daemon | grep Memory

# Monitoring continu
watch -n 5 'ps aux | grep clamd | grep -v grep | awk "{print \$6/1024\" MB\"}"'

# Si swap utilisé (mauvais signe)
free -h
# Swap used > 0 → augmenter RAM ou réduire MaxThreads/MaxFileSize
```

---

## Section 11 : Troubleshooting et Maintenance

### 11.1 Problèmes Courants

**Daemon ne démarre pas :**

```bash
# Vérifier logs
sudo journalctl -u clamav-daemon -n 50

# Erreurs communes :

# 1. Signatures manquantes
# ERROR: Can't open file or directory /var/lib/clamav/main.cvd
# Solution :
sudo freshclam

# 2. Permissions incorrectes
# ERROR: Can't create temporary directory /var/lib/clamav/tmp
# Solution :
sudo chown -R clamav:clamav /var/lib/clamav
sudo chmod 755 /var/lib/clamav

# 3. Port/socket déjà utilisé
# ERROR: Socket file /var/run/clamav/clamd.sock exists
# Solution :
sudo rm /var/run/clamav/clamd.sock
sudo systemctl restart clamav-daemon

# 4. Mémoire insuffisante
# ERROR: Memory allocation failed
# Solution : réduire MaxThreads, MaxFileSize dans clamd.conf
```

**Freshclam échecs :**

```bash
# Vérifier logs
sudo tail -f /var/log/clamav/freshclam.log

# Erreurs communes :

# 1. Mirror inaccessible
# WARNING: Can't download daily.cvd from database.clamav.net
# Solution : vérifier réseau, DNS, firewall

# Tester connectivité
ping database.clamav.net
curl -I http://database.clamav.net

# 2. Database outdated
# WARNING: Your ClamAV installation is OUTDATED!
# Solution : update ClamAV version
sudo apt update && sudo apt upgrade clamav

# 3. Disk space full
# ERROR: Can't create temporary file
# Solution :
df -h /var/lib/clamav
# Nettoyer espace ou augmenter partition

# 4. Proxy issues
# ERROR: Connection failed
# Solution : configurer proxy dans freshclam.conf
HTTPProxyServer proxy.example.com
HTTPProxyPort 8080
```

**Performance lente :**

```bash
# Diagnostic

# 1. Vérifier charge CPU
top
# clamd consomme >80% CPU constamment ?

# 2. Vérifier threads actifs
sudo ss -tulpn | grep clamd | wc -l
# Compare avec MaxThreads config

# 3. Vérifier I/O disk
iostat -x 5
# %util proche 100% ?

# 4. Vérifier swap
free -h
# Swap used > 0 ? (très mauvais pour performance)

# Solutions :
# - Réduire MaxThreads
# - Augmenter RAM
# - Exclure directories volumineux non critiques
# - Utiliser SSD au lieu HDD
# - Split scans en batches plus petits
```

### 11.2 Debugging Avancé

**Mode debug clamd :**

```bash
# Arrêter daemon
sudo systemctl stop clamav-daemon

# Lancer en foreground avec debug
sudo clamd -c /etc/clamav/clamd.conf --debug

# Ou éditer clamd.conf temporairement
LogVerbose yes
Debug yes

# Restart
sudo systemctl start clamav-daemon

# Logs ultra-verbeux
sudo tail -f /var/log/clamav/clamav.log
```

**Tester signatures :**

```bash
# Créer EICAR test file
cat > /tmp/eicar.txt << 'EOF'
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
EOF

# Scanner
clamscan /tmp/eicar.txt
# Doit retourner : Eicar-Test-Signature FOUND

# Si pas détecté → signatures corrompues
sudo freshclam --force
```

**Vérifier intégrité signatures :**

```bash
# Test databases
sigtool --info /var/lib/clamav/main.cvd
sigtool --info /var/lib/clamav/daily.cvd

# MD5 checksums
md5sum /var/lib/clamav/*.cvd

# Si corruption suspectée, forcer re-download
sudo rm /var/lib/clamav/*.cvd
sudo freshclam
```

### 11.3 Maintenance Régulière

**Checklist maintenance mensuelle :**

```bash
#!/bin/bash
# clamav-maintenance.sh

echo "=== ClamAV Maintenance - $(date) ==="

# 1. Vérifier version ClamAV
CURRENT_VERSION=$(clamscan --version | awk '{print $3}' | tr -d '/')
echo "Current version: $CURRENT_VERSION"

# 2. Vérifier signatures à jour
MAIN_AGE=$(( ($(date +%s) - $(stat -c %Y /var/lib/clamav/main.cvd)) / 86400 ))
DAILY_AGE=$(( ($(date +%s) - $(stat -c %Y /var/lib/clamav/daily.cvd)) / 86400 ))
echo "Signatures age: main=$MAIN_AGE days, daily=$DAILY_AGE days"

if [ $DAILY_AGE -gt 2 ]; then
    echo "WARNING: Signatures outdated, updating..."
    freshclam
fi

# 3. Vérifier espace disque
DISK_USAGE=$(df -h /var/lib/clamav | tail -1 | awk '{print $5}' | tr -d '%')
echo "Disk usage: $DISK_USAGE%"

if [ $DISK_USAGE -gt 80 ]; then
    echo "WARNING: Low disk space"
fi

# 4. Nettoyer logs anciens (>90 jours)
find /var/log/clamav -name "*.log" -mtime +90 -delete
find /var/log/clamav/scans -name "*.log" -mtime +90 -delete
echo "Old logs cleaned"

# 5. Nettoyer quarantine ancienne (>180 jours)
find /var/quarantine -type f -mtime +180 -delete
echo "Old quarantine files cleaned"

# 6. Vérifier services
for service in clamav-daemon clamav-freshclam; do
    if systemctl is-active --quiet $service; then
        echo "✓ $service running"
    else
        echo "✗ $service NOT running - attempting restart"
        systemctl restart $service
    fi
done

# 7. Test scan
echo "Running test scan..."
echo "test" > /tmp/clamav-test.txt
RESULT=$(clamdscan /tmp/clamav-test.txt 2>&1)
if echo "$RESULT" | grep -q "OK"; then
    echo "✓ Test scan passed"
else
    echo "✗ Test scan failed"
fi
rm /tmp/clamav-test.txt

echo "=== Maintenance completed ==="

# Cron : 0 3 1 * * /usr/local/bin/clamav-maintenance.sh
```

---

## Section 12 : Best Practices et Cas d'Usage

### 12.1 Best Practices Sécurité

```markdown
## Configuration Sécurisée

### Daemon
- [ ] Utiliser LocalSocket plutôt que TCP (si possible)
- [ ] Si TCP requis : bind 127.0.0.1 seulement
- [ ] Firewall strict si TCP accessible réseau
- [ ] Run as user clamav (jamais root)
- [ ] Permissions socket 660 ou 666 selon besoins

### Signatures
- [ ] Freshclam automated updates (24 checks/jour)
- [ ] Monitoring signatures age (<48h)
- [ ] Backup signatures avant updates (optionnel)
- [ ] Multiple mirror fallback configuré

### Scanning
- [ ] Limits configurés (MaxFileSize, MaxRecursion)
- [ ] Exclude système directories (/sys, /proc, /dev)
- [ ] Quarantine directory isolée (permissions 700)
- [ ] Logs rotation automatique
- [ ] Alertes email infections

### Intégrations
- [ ] Mail : Amavis + ClamAV (discard infected)
- [ ] Web : Scan uploads AVANT processing
- [ ] Quarantine automatique fichiers infectés
- [ ] Notifications administrateur
- [ ] Logs audit trail complet
```

### 12.2 Cas d'Usage Production

**Hébergeur Web Mutualisé :**

```yaml
Configuration :
  - clamd daemon : MaxThreads=20
  - on-access scanning : /home/*/public_html
  - cron scan quotidien : tous users
  - quarantine : /var/quarantine/{username}/
  - notifications : email user + admin

Workflow upload :
  1. User upload fichier via FTP/SFTP/Web
  2. inotify trigger → clamdscan file
  3. Si infected → move quarantine + block access
  4. Si clean → allow access
  5. Email notification si infected
```

**Mail Server (1000+ users) :**

```yaml
Stack :
  - Postfix (MTA)
  - Amavis (content filter)
  - ClamAV (virus scanning)
  - SpamAssassin (spam filtering)

Configuration :
  - clamd : MaxThreads=16, TCP socket
  - amavis : 5 child processes
  - action infected : D_DISCARD (pas bounce)
  - quarantine : 90 jours retention
  - monitoring : Prometheus + Grafana

Performance :
  - 10,000 emails/jour
  - Scan moyen : 50ms/email
  - RAM usage : 1.2GB clamd + 800MB amavis
```

**File Server (Samba/NFS) :**

```yaml
Setup :
  - Samba shares : /srv/shares/*
  - on-access : clamonacc monitoring shares
  - scheduled : full scan weekly
  - quarantine : admin-only access

Integration :
  - Samba VFS module : vfs_clamav (optionnel)
  - Ou clamonacc on-access (recommandé)
  - Block infected files immediately
  - Email alert administrator

Exclusions :
  - User home temp directories
  - System shares (netlogon, sysvol)
  - Read-only archives
```

**Cloud Storage Gateway :**

```yaml
Architecture :
  - S3 compatible storage (MinIO/AWS S3)
  - Upload → Lambda/Function → ClamAV scan
  - Infected → reject + log
  - Clean → store in S3

Scaling :
  - Container : Docker ClamAV
  - Orchestration : Kubernetes
  - Auto-scaling : based on queue depth
  - Shared signatures : EFS/persistent volume

Performance :
  - Container : 2 CPU, 4GB RAM
  - Concurrent scans : 10 per container
  - Horizontal scaling : 1-50 pods
```

### 12.3 Checklist Production

```markdown
## Pre-Production Checklist

### Installation
- [ ] ClamAV installé dernière version stable
- [ ] clamd daemon configuré
- [ ] freshclam automated updates
- [ ] Signatures initialement téléchargées
- [ ] Services systemd enabled

### Configuration
- [ ] clamd.conf optimisé (threads, limits)
- [ ] freshclam.conf configuré (mirrors, checks)
- [ ] Socket/TCP configuration sécurisée
- [ ] Logs directories créés avec permissions
- [ ] Quarantine directory créé

### Intégrations
- [ ] Mail server integration testée (si requis)
- [ ] Web upload scanning implémenté (si requis)
- [ ] On-access scanning configuré (si requis)
- [ ] Scripts automatisation déployés

### Monitoring
- [ ] Healthchecks configurés
- [ ] Alertes email configurées
- [ ] Logs rotation configurée
- [ ] Metrics exportés (Prometheus/dashboard)
- [ ] Documentation procédures

### Testing
- [ ] EICAR test file détecté
- [ ] Scan performance acceptable
- [ ] Alerts fonctionnels
- [ ] Quarantine workflow validé
- [ ] Restore procedure testée

### Maintenance
- [ ] Cron jobs scans automatiques
- [ ] Backup strategy définie
- [ ] Update procedure documentée
- [ ] Incident response plan
- [ ] Team formée
```

---

## Ressources et Références

**Documentation officielle :**
- Site web : https://www.clamav.net/
- Documentation : https://docs.clamav.net/
- GitHub : https://github.com/Cisco-Talos/clamav
- FAQ : https://docs.clamav.net/faq/

**Signatures et updates :**
- Cloudflare CDN : database.clamav.net
- Status page : https://www.clamav.net/downloads
- Third-party signatures : https://sanesecurity.com/

**Communauté :**
- Mailing lists : https://www.clamav.net/contact
- Discord : https://discord.gg/ClamAV
- Bug tracker : https://github.com/Cisco-Talos/clamav/issues

**Outils complémentaires :**
- ClamTk (GUI) : https://gitlab.com/dave_m/clamtk
- Amavis : https://www.ijs.si/software/amavisd/
- Sanesecurity : https://sanesecurity.com/

---

## Conclusion

**ClamAV = Antivirus open-source référence Linux/Unix**

**Points clés :**

✅ **Gratuit et open-source** = GPL, usage commercial libre
✅ **Production-ready** = Millions serveurs, stable, fiable
✅ **Performance** = Daemon multi-thread, scan rapide
✅ **Intégrations** = Mail, web, file servers, cloud
✅ **Maintenance simple** = Updates automatiques, monitoring facile

**Workflow recommandé :**

```bash
# 1. Installation
sudo apt install clamav clamav-daemon clamav-freshclam

# 2. Configuration production
# - clamd.conf : MaxThreads selon CPU, limits adaptés
# - freshclam.conf : updates automatiques 24x/jour
# - Socket/TCP sécurisé

# 3. Première mise à jour signatures
sudo freshclam

# 4. Start services
sudo systemctl enable --now clamav-daemon clamav-freshclam

# 5. Intégrations selon use case
# - Mail : Amavis + ClamAV
# - Web : Upload scanning hooks
# - Files : On-access ou cron scans

# 6. Monitoring
# - Healthchecks automatiques
# - Alertes infections
# - Métriques Prometheus

# 7. Maintenance
# - Cron scans quotidiens/hebdomadaires
# - Cleanup logs/quarantine
# - Updates ClamAV version
```

**Limitations à connaître :**

- ❌ Detection rate : 80-85% (vs 95%+ commercial)
- ❌ Pas de support EDR/XDR avancé
- ❌ Heuristique basique (vs ML avancé)
- ❌ Support communauté (pas 24/7 SLA)

✅ Mais :

- Gratuit et suffisant 90% use cases
- Intégration native services Linux
- Lightweight et performant
- Compliance réglementaire (scan requis)


**Tu maîtrises maintenant ClamAV de l'installation au déploiement production multi-serveurs !** 🛡️

---

**Guide ClamAV Complet terminé !** 🎉

Voilà le guide complet ClamAV ! Il couvre exhaustivement :

✅ **12 sections complètes** avec analogie pédagogique  
✅ Installation (packages, source, Docker)  
✅ Configuration daemon clamd optimale  
✅ Scan manuel et automatique (clamscan/clamdscan)   
✅ Mise à jour signatures (freshclam)  
✅ On-access scanning temps réel (clamonacc)  
✅ Intégration mail servers (Postfix + Amavis)  
✅ Intégration web servers (PHP, Python, Nginx)  
✅ Automatisation complète (cron, monitoring, alertes)  
✅ Performance tuning production  
✅ Troubleshooting et debugging  
✅ Best practices et cas d'usage réels  
✅ Scripts production-ready commentés  

**Même rigueur que tes autres guides avec focus antivirus production !** 🔒