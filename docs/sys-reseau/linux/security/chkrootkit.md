---
description: "Chkrootkit : détection rootkits Linux, scan kernel/binaires, automatisation, monitoring sécurité"
icon: lucide/book-open-check
tags: ["CHKROOTKIT", "ROOTKIT", "SECURITY", "MALWARE", "LINUX", "DETECTION"]
---

# Chkrootkit

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-time="4-6 heures"
  data-version="1.0">
</div>

## Introduction à la Détection de Rootkits

!!! quote "Analogie pédagogique"
    _Imaginez un **détective forensique spécialisé crimes invisibles avec équipement détection ADN traces microscopiques** : Chkrootkit fonctionne comme **expert détection intrusions furtives analysant CHAQUE recoin système cherchant présence camouflée attaquants**. **Détective forensique scène crime** : poudre empreintes digitales (scan binaries modifiés), lumière UV révèle fluides invisibles (détection processus cachés), analyse ADN traces (checksums fichiers système), détection micro-caméras espions (backdoors réseau), recherche passages secrets (rootkits kernel-level), chronologie événements (logs tampering detection). **Sans Chkrootkit** : rootkits invisibles (malware niveau kernel masque processus/fichiers/connexions), backdoors persistants (accès root permanent attaquants), keyloggers silencieux (vol credentials admins), sniffers réseau furtifs (interception trafic non détectée), bootkit firmware (infection avant OS load), compromission totale invisible (serveur zombie contrôlé). **Avec Chkrootkit** : **Scan 70+ rootkits connus** (lrk, t0rn, Ambient's Rootkit, rsh backdoor, Romanian rootkit, RH-Sharpe's rootkit, etc.), **Détection binaires modifiés** (compare checksums ls, ps, netstat, login, sshd vs originaux), **Processus cachés** (compare `ps` output vs `/proc` entries), **Ports cachés** (compare `netstat` vs raw `/proc/net/tcp`), **Fichiers LKM suspects** (Loadable Kernel Modules rootkits), **Strings analysis** (recherche patterns malveillants binaries), **Network sniffers** (détection promiscuous mode interfaces). **Architecture Chkrootkit** : Collection ~20 scripts shell + binaires C compilés (ifpromisc.c, chklastlog.c, chkwtmp.c, check_wtmpx.c, chkproc.c, chkdirs.c, strings.c) = approche multi-vecteurs détection. **Rootkits détectés** : Niveau USER-SPACE (binaries trojaned : ls, ps, netstat, top, find, du), Niveau KERNEL (LKM : adore, knark, kbeast), Niveau FIRMWARE (moins commun, hors scope chkrootkit). **Chkrootkit = outil référence depuis 1997** : créé Nelson Murilo & Klaus Steding-Jessen Pangeia Informatica Brazil, open-source GPL, maintenance active communauté, intégré distributions majeures (Debian/Ubuntu repos officiels), léger (pas daemon, scan ponctuel), safe (read-only, pas modification système). **Limitations importantes** : détecte SEULEMENT rootkits CONNUS (signatures-based, pas heuristique avancée), faux positifs fréquents (virtualisation, containers, kernels custom), peut être trompé si rootkit sophistiqué (si /bin/ls trojaned, chkrootkit utilise /bin/ls pour scanner...), nécessite binaires propres (statically-compiled versions recommandées). **Compléments essentiels** : rkhunter (détection alternative, plus récent), AIDE/Tripwire (file integrity monitoring), lynis (audit sécurité complet), ClamAV (antivirus), osquery (monitoring forensique temps réel)._

**Chkrootkit en résumé :**

- ✅ **Détection rootkits** = 70+ rootkits connus (signatures)
- ✅ **Binaries trojaned** = Compare checksums fichiers système
- ✅ **Processus cachés** = Détection discordances ps vs /proc
- ✅ **Ports cachés** = Compare netstat vs /proc/net/tcp
- ✅ **LKM rootkits** = Scan kernel modules suspects
- ✅ **Léger** = Scripts shell + petits binaires C, pas daemon
- ✅ **Safe** = Read-only, aucune modification système
- ✅ **Gratuit** = GPL, open-source depuis 1997

**Guide structure :**

1. Introduction et concepts rootkits
2. Installation et vérification intégrité
3. Premier scan et interprétation résultats
4. Tests détaillés (50+ checks)
5. Options et modes scan
6. Automatisation (cron, monitoring)
7. Chkrootkit vs Rkhunter vs alternatives
8. Faux positifs et whitelist
9. Intégration SIEM et alertes
10. Cas pratiques détection rootkits
11. Limitations et compléments sécurité
12. Best practices production

---

## Section 1 : Introduction et Concepts

### 1.1 Qu'est-ce qu'un Rootkit ?

**Rootkit = Malware furtif masquant présence attaquant système compromis**

```
Niveaux rootkits (du plus visible au plus furtif) :

┌─────────────────────────────────────────────────────┐
│ Application Rootkits                                │
│ Binaries trojaned (ls, ps, netstat, login, sshd)  │
│ Détection : Facile (compare checksums)             │
│ Persistance : Faible (updates OS écrasent)         │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│ Library Rootkits                                    │
│ Shared libraries modifiées (libc, libdl)          │
│ LD_PRELOAD hijacking                               │
│ Détection : Moyenne (checksums, LD_PRELOAD var)    │
│ Persistance : Moyenne                              │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│ Kernel Rootkits (LKM - Loadable Kernel Modules)   │
│ Modules kernel malveillants                        │
│ Hook syscalls (read, write, getdents, etc.)       │
│ Cache processus, fichiers, connexions             │
│ Détection : Difficile (nécessite kernel analysis) │
│ Persistance : Haute                               │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│ Firmware/Bootkit Rootkits                          │
│ BIOS/UEFI malware                                  │
│ MBR/boot sector infection                         │
│ Détection : Très difficile (hors OS)              │
│ Persistance : Extrême (survit reinstall OS)       │
└─────────────────────────────────────────────────────┘

Chkrootkit détecte principalement :
✅ Application rootkits (binaries trojaned)
✅ Library rootkits (LD_PRELOAD)
✅ Kernel rootkits (LKM basiques)
❌ Firmware rootkits (hors scope)
```

**Exemples rootkits célèbres :**

```
Application-level :
- lrk (Linux Rootkit v5) : ls, ps, netstat trojaned
- t0rn : 20+ binaries modifiés + backdoor
- Romanian rootkit : keylogger + backdoor

Kernel-level (LKM) :
- Adore : Cache processus/fichiers via kernel hooks
- Knark : Full featured LKM rootkit
- Mood-NT : Hides processes, files, network
- Synaptic : Advanced kernel rootkit

Exemples comportements cachés :
- Processus : `ps aux` ne montre PAS backdoor running
- Fichiers : `ls -la /tmp` ne montre PAS rootkit files
- Connexions : `netstat -tunap` ne montre PAS connexions attaquant
- Logs : Connexions effacées de /var/log/auth.log
```

### 1.2 Comment Chkrootkit Détecte ?

**Méthodes détection Chkrootkit :**

```
1. Signature-based Detection
   ─────────────────────────
   Recherche strings spécifiques binaries connus malveillants
   
   Exemple :
   # Recherche signature "t0rn" rootkit
   strings /sbin/init | grep "t0rn"
   
   Si trouvé → INFECTED

2. Checksum Comparison
   ────────────────────
   Compare checksums binaires système vs base données propres
   
   Problème : Chkrootkit n'a PAS base checksums intégrée
   Solution : Créer baseline propre (installation fresh)

3. Behavior-based Detection
   ─────────────────────────
   Compare outputs outils système vs lecture directe /proc
   
   Exemple processus cachés :
   # ps aux liste 50 processus
   # /proc/ contient 55 directories (PIDs)
   # → 5 processus CACHÉS par rootkit
   
4. Known Locations
   ────────────────
   Scan directories typiques rootkits
   
   /dev/.* (fichiers cachés /dev)
   /usr/lib/.* (libraries cachées)
   /tmp/... (backdoors temporaires)

5. Promiscuous Mode Detection
   ───────────────────────────
   Détecte interfaces réseau mode promiscuous (sniffing)
   
   ifpromisc : Test chaque interface
   Si promiscuous → Sniffer potentiel

6. LKM Analysis
   ────────────
   Scan /proc/modules pour modules suspects
   Recherche hooks syscall connus
```

### 1.3 Composants Chkrootkit

```bash
# Structure Chkrootkit
chkrootkit/
├── chkrootkit          # Script shell principal
├── ifpromisc           # Détection promiscuous mode (C compiled)
├── chklastlog          # Vérifie lastlog deletions (C)
├── chkwtmp             # Vérifie wtmp deletions (C)
├── check_wtmpx         # Vérifie wtmpx (Solaris) (C)
├── chkproc             # Détection processus cachés (C)
├── chkdirs             # Détection fichiers cachés (C)
├── strings             # Alternative strings command (C)
└── chkutmp             # Vérifie utmp deletions (C)

# Binaires compilés statiquement (recommandé)
# Pourquoi ? Si libc trojaned, binaires dynamiques compromis
# Compilation statique = standalone, pas dépendances .so
```

**Tests effectués (50+) :**

```
Binaries Checks :
- ls, ps, netstat, login, sshd, named, du, find, grep
- ifconfig, ssh, syslogd, tcpd, top, cron, sendmail

Rootkit Signatures :
- lrk (v3, v4, v5, v6)
- Ambient's Rootkit (ARK)
- Ramen Worm
- rh-sharpe's rootkit
- Omega Worm
- Showtee
- Lion Worm
- RSHA's rootkit
- Romanian rootkit
- RK17
- Suckit
- Volc rootkit
- T0rn rootkit
- Mithra's rootkit
- LOC rootkit
- ... et 50+ autres

LKM Checks :
- adore, rial, knark, rtkit, mood-nt
- syslog interception
- trojaned kernel modules

Network Checks :
- Promiscuous mode interfaces
- Packet sniffers
- Backdoor ports listening

File Checks :
- Hidden files /dev
- Suspicious files /tmp, /var/tmp
- Modified system files

Log Checks :
- Deleted wtmp entries
- Deleted lastlog entries
- Suspicious log gaps
```

### 1.4 Chkrootkit Limitations

**Limitations critiques :**

```
❌ Peut être trompé par rootkit sophistiqué
   Si /bin/ls trojaned, chkrootkit utilise /bin/ls pour scanner
   
   Solution : Utiliser binaires statically-compiled externes
            ou booter Live CD pour scan offline

❌ Détection signature-based uniquement
   Rootkits nouveaux/custom non détectés
   
   Solution : Compléter avec rkhunter, AIDE, Lynis

❌ Faux positifs fréquents
   Virtualisation (OpenVZ, LXC, Docker)
   Kernels custom, modules légitimes
   
   Solution : Whitelist, ignorer warnings connus

❌ Pas de base checksums intégrée
   Ne peut PAS dire si /bin/ls modifié sans référence
   
   Solution : Créer baseline installation propre
            Utiliser package manager verify (debsums, rpm -V)

❌ Binaires système utilisés pour scan
   Si système compromis, résultats pas fiables
   
   Solution : Scan offline (Live CD/USB)
            Binaires statiques compilation propre

❌ Pas de protection temps réel
   Scan ponctuel, pas daemon monitoring continu
   
   Solution : Compléter avec osquery, OSSEC, Wazuh
```

---

## Section 2 : Installation et Vérification Intégrité

### 2.1 Installation Package Manager

**Debian/Ubuntu :**

```bash
# Installer chkrootkit
sudo apt update
sudo apt install chkrootkit

# Vérifier installation
which chkrootkit
# /usr/sbin/chkrootkit

# Version
chkrootkit -V
# chkrootkit version 0.55

# Localisation binaires
dpkg -L chkrootkit | grep bin
# /usr/sbin/chkrootkit
# /usr/lib/chkrootkit/ifpromisc
# /usr/lib/chkrootkit/chklastlog
# /usr/lib/chkrootkit/chkwtmp
# /usr/lib/chkrootkit/chkproc
# /usr/lib/chkrootkit/chkdirs
# /usr/lib/chkrootkit/strings-static
```

**RHEL/CentOS/Rocky/Alma :**

```bash
# Installer EPEL
sudo yum install epel-release

# Installer chkrootkit
sudo yum install chkrootkit

# Vérifier
chkrootkit -V
```

**Arch Linux :**

```bash
# Installer depuis AUR
yay -S chkrootkit

# Ou depuis source (recommandé)
```

### 2.2 Installation depuis Source (Recommandé Production)

```bash
# Installer dépendances build
sudo apt install build-essential wget

# Télécharger source officiel
cd /tmp
wget ftp://ftp.chkrootkit.org/pub/seg/pac/chkrootkit.tar.gz

# Vérifier signature GPG (IMPORTANT)
wget ftp://ftp.chkrootkit.org/pub/seg/pac/chkrootkit.tar.gz.sig
gpg --verify chkrootkit.tar.gz.sig chkrootkit.tar.gz

# Extraire
tar -xzf chkrootkit.tar.gz
cd chkrootkit-*

# Compiler
make sense

# Vérifier binaires créés
ls -lh
# -rwxr-xr-x 1 user user  15K ifpromisc
# -rwxr-xr-x 1 user user  12K chklastlog
# -rwxr-xr-x 1 user user  13K chkwtmp
# -rwxr-xr-x 1 user user  18K chkproc
# -rwxr-xr-x 1 user user  14K chkdirs
# -rwxr-xr-x 1 user user  25K strings-static

# Installer dans /opt (isolé système)
sudo mkdir -p /opt/chkrootkit
sudo cp -r * /opt/chkrootkit/
sudo chmod +x /opt/chkrootkit/chkrootkit

# Créer symlink
sudo ln -s /opt/chkrootkit/chkrootkit /usr/local/bin/chkrootkit

# Vérifier
chkrootkit -V
```

### 2.3 Compilation Statique (Sécurité Maximale)

```bash
# Binaires statiquement liés (pas dépendances shared libraries)
# Important si libc potentiellement compromise

cd /tmp/chkrootkit-*

# Compiler statiquement
gcc -static -o ifpromisc ifpromisc.c
gcc -static -o chklastlog chklastlog.c
gcc -static -o chkwtmp chkwtmp.c
gcc -static -o chkproc chkproc.c
gcc -static -o chkdirs chkdirs.c
gcc -static -o strings-static strings.c

# Vérifier binaries statiques
file ifpromisc
# ifpromisc: ELF 64-bit LSB executable, statically linked

ldd ifpromisc
# not a dynamic executable

# Installer binaires statiques
sudo mkdir -p /opt/chkrootkit-static
sudo cp * /opt/chkrootkit-static/

# Utiliser pour scans critiques
/opt/chkrootkit-static/chkrootkit
```

### 2.4 Vérification Intégrité Installation

```bash
# Vérifier checksums package (Debian/Ubuntu)
sudo debsums chkrootkit

# Output si OK :
# /usr/sbin/chkrootkit                                      OK
# /usr/lib/chkrootkit/ifpromisc                            OK
# ...

# Vérifier avec package manager (RHEL)
sudo rpm -V chkrootkit

# Vérifier permissions (doit être root-owned)
ls -l /usr/sbin/chkrootkit
# -rwxr-xr-x 1 root root 123456 Jan 16 2024 /usr/sbin/chkrootkit

# Vérifier pas setuid/setgid (risque sécurité)
find /usr/lib/chkrootkit -perm /6000 -ls
# Rien (output vide = bon)

# Créer checksums baseline (installation propre)
sudo md5sum /usr/sbin/chkrootkit > /root/chkrootkit-baseline.md5
sudo md5sum /usr/lib/chkrootkit/* >> /root/chkrootkit-baseline.md5

# Vérifier baseline plus tard
sudo md5sum -c /root/chkrootkit-baseline.md5
```

---

## Section 3 : Premier Scan et Interprétation Résultats

### 3.1 Premier Scan Basique

```bash
# Lancer scan (requiert root)
sudo chkrootkit

# Output typique (système sain) :
# ROOTDIR is `/'
# Checking `amd'...                                           not found
# Checking `basename'...                                      not infected
# Checking `biff'...                                          not found
# Checking `chfn'...                                          not infected
# Checking `chsh'...                                          not infected
# Checking `cron'...                                          not infected
# Checking `crontab'...                                       not infected
# Checking `date'...                                          not infected
# Checking `du'...                                            not infected
# Checking `dirname'...                                       not infected
# Checking `echo'...                                          not infected
# Checking `egrep'...                                         not infected
# Checking `env'...                                           not infected
# Checking `find'...                                          not infected
# Checking `fingerd'...                                       not found
# Checking `gpm'...                                           not infected
# Checking `grep'...                                          not infected
# Checking `hdparm'...                                        not infected
# Checking `su'...                                            not infected
# Checking `ifconfig'...                                      not infected
# Checking `inetd'...                                         not tested
# Checking `inetdconf'...                                     not found
# Checking `identd'...                                        not found
# Checking `init'...                                          not infected
# Checking `killall'...                                       not infected
# Checking `ldsopreload'...                                   not infected
# Checking `login'...                                         not infected
# Checking `ls'...                                            not infected
# Checking `lsof'...                                          not infected
# Checking `mail'...                                          not found
# Checking `mingetty'...                                      not found
# Checking `netstat'...                                       not infected
# Checking `named'...                                         not found
# Checking `passwd'...                                        not infected
# Checking `pidof'...                                         not infected
# Checking `pop2'...                                          not found
# Checking `pop3'...                                          not found
# Checking `ps'...                                            not infected
# Checking `pstree'...                                        not infected
# Checking `rpcinfo'...                                       not found
# Checking `rlogind'...                                       not found
# Checking `rshd'...                                          not found
# Checking `slogin'...                                        not infected
# Checking `sendmail'...                                      not found
# Checking `sshd'...                                          not infected
# Checking `syslogd'...                                       not tested
# Checking `tar'...                                           not infected
# Checking `tcpd'...                                          not infected
# Checking `tcpdump'...                                       not infected
# Checking `top'...                                           not infected
# Checking `telnetd'...                                       not found
# Checking `timed'...                                         not found
# Checking `traceroute'...                                    not found
# Checking `vdir'...                                          not infected
# Checking `w'...                                             not infected
# Checking `write'...                                         not infected

# Scan dure 30 secondes - 2 minutes selon système
```

### 3.2 Statuts Possibles

```bash
# Statuts output chkrootkit :

not found       # Binary pas installé (normal)
not infected    # Binary testé, propre ✅
not tested      # Test skipped (dépendances manquantes)
Vulnerable      # Vulnérabilité détectée ⚠️
INFECTED        # Rootkit détecté ❌
Warning         # Suspect mais pas certain ⚠️

# Exemples :

Checking `ls'...                                            not infected
# ✅ /bin/ls est propre

Checking `lkm'...                                           You have     3 process hidden for readdir command
# ❌ SUSPECT : 3 processus cachés détectés

Checking `sniffer'...                                       eth0: PACKET SNIFFER(/sbin/dhclient[12345])
# ⚠️ WARNING : Interface promiscuous mode (peut être légitime)

Checking `w55808'...                                        INFECTED
# ❌ DANGER : Rootkit w55808 détecté
```

### 3.3 Interprétation Sections Output

**Section Binaries :**

```bash
# Checking binaires système communs
Checking `ls'...                                            not infected
Checking `ps'...                                            not infected
Checking `netstat'...                                       not infected
Checking `login'...                                         not infected
Checking `sshd'...                                          not infected

# Si INFECTED :
Checking `ls'...                                            INFECTED
# → Binary /bin/ls modifié (trojaned)
# → Système compromis
# → Nécessite investigation forensique
```

**Section LKM (Loadable Kernel Modules) :**

```bash
Checking `lkm'...                                           chkproc: nothing deleted
# ✅ Pas de processus cachés

# Ou :
Checking `lkm'...                                           You have     5 process hidden for readdir command
# ❌ 5 processus non visibles via `ps` mais présents /proc
# → Rootkit kernel-level probable
```

**Section Sniffer :**

```bash
Checking `sniffer'...                                       lo: not promisc and no packet sniffer sockets
# ✅ Pas de sniffer détecté

# Ou :
Checking `sniffer'...                                       eth0: PACKET SNIFFER(/usr/sbin/tcpdump[1234])
# ⚠️ tcpdump running (légitime si admin utilise)

# Ou :
Checking `sniffer'...                                       eth0: PACKET SNIFFER(/tmp/.hidden/sniff[5678])
# ❌ Sniffer suspect location /tmp/.hidden
```

**Section Rootkits signatures :**

```bash
Searching for Romanian rootkit...                          Nothing found
Searching for Ambient's rootkit (ark)...                   Nothing found
Searching for suspicious files and dirs...                 Nothing found
Searching for LKM rootkits...                              Nothing detected
Searching for Linux/Ebury - Operation Windigo ssh...       Not infected

# Si détection :
Searching for t0rn rootkit...                              INFECTED
Searching for t0rn rootkit default files...               /usr/info/.t0rn found
# ❌ t0rn rootkit files détectés
```

### 3.4 Sauvegarder Résultats Scan

```bash
# Scan avec sauvegarde output
sudo chkrootkit > /var/log/chkrootkit-scan-$(date +%Y%m%d).log 2>&1

# Ou avec timestamp détaillé
sudo chkrootkit | tee /var/log/chkrootkit/scan-$(date +%Y%m%d-%H%M%S).log

# Extraire seulement problèmes
sudo chkrootkit | grep -E "INFECTED|Vulnerable|Warning" > /var/log/chkrootkit-issues.log

# Comparer scans (avant/après)
diff /var/log/chkrootkit-scan-20240115.log /var/log/chkrootkit-scan-20240116.log
```

---

## Section 4 : Tests Détaillés

### 4.1 Tests Binaires Système

**Binaries testés :**

```bash
# Chkrootkit teste ~50 binaries système

# Méthode test (exemple ls) :
strings /bin/ls | grep "known_rootkit_signature"

# Liste complète binaries testés :
basename, biff, chfn, chsh, cron, crontab, date
dirname, du, echo, env, egrep, find, fingerd
gpm, grep, hdparm, su, ifconfig, inetd, init
killall, login, ls, lsof, mail, mingetty
netstat, named, passwd, pidof, pop2, pop3
ps, pstree, rpcinfo, rlogind, rshd, slogin
sendmail, sshd, syslogd, tar, tcpd, tcpdump
top, telnetd, timed, traceroute, vdir, w, write

# Exemple test sshd :
Checking `sshd'...
# 1. Vérifie process running
# 2. Vérifie binary /usr/sbin/sshd
# 3. Recherche strings suspects
# 4. Compare comportement attendu
```

### 4.2 Tests Rootkits Signatures

**70+ rootkits signatures :**

```bash
# Tests effectués :

# 1. lrk (Linux Rootkit)
Searching for lrk3 rootkit...
Searching for lrk4 rootkit...
Searching for lrk5 rootkit...
Searching for lrk6 rootkit...
# Recherche : /dev/.kork, /usr/src/.puta, /dev/ptyr

# 2. Ramen Worm
Searching for Ramen Worm...
# Recherche : /usr/lib/ldlibps.so, /usr/lib/ldliblogin.so

# 3. Maniac rootkit
Searching for Maniac files...
# Recherche : /usr/bin/sourcemask, /usr/bin/enim

# 4. RH-Sharpe's rootkit
Searching for RH-Sharpe's rootkit...
# Recherche : /bin/bkd, /dev/ptyzx, /dev/ptyzy

# 5. Romanian rootkit
Searching for Romanian rootkit...
# Recherche : /usr/include/file.h, /usr/include/proc.h

# 6. Ambient's rootkit (ARK)
Searching for Ambient's rootkit (ark)...
# Recherche : /dev/ptyxx, /usr/lib/lib.so, /usr/man/.ark

# 7. Suckit rootkit
Searching for Suckit rootkit...
# Recherche : /sbin/init infected, /dev/.pizda, /dev/.pula

# 8. Volc rootkit
Searching for Volc rootkit...
# Recherche : /usr/bin/.volc, /usr/bin/volc

# 9. T0rn rootkit
Searching for T0rn rootkit...
Searching for T0rn rootkit default files...
# Recherche : /usr/src/.puta, /usr/info/.t0rn

# 10. LOC rootkit
Searching for LOC rootkit...
# Recherche : /tmp/xp, /tmp/kidd0.c

# ... et 60+ autres
```

### 4.3 Tests LKM (Kernel Modules)

```bash
# Test LKM rootkits
Checking `lkm'...

# Outils utilisés :
chkproc    # Compare ps output vs /proc PIDs
chkdirs    # Compare ls output vs readdir() syscall

# Test processus cachés :
# 1. Liste PIDs via `ps aux`
# 2. Liste PIDs via `/proc/*/` directories
# 3. Compare : discordances = processus cachés

# Exemple output :
You have     3 process hidden for readdir command
# → 3 processus dans /proc mais pas visible via `ls`
# → Indication rootkit kernel-level

# Test fichiers cachés :
You have     8 hidden files for readdir command
# → 8 fichiers présents mais cachés via getdents() hook

# Modules kernel suspects :
Searching for Linux/Ebury - Operation Windigo ssh...
# SSH backdoor sophistiqué (Ebury/Windigo)
# Teste /usr/sbin/sshd pour signatures

# Adore LKM :
Searching for Adore Worm...
# Rootkit LKM cache processus/fichiers/connexions
# Recherche : /dev/adore, /usr/lib/lib*.so.*
```

### 4.4 Tests Network Sniffer

```bash
# Détection packet sniffers
Checking `sniffer'...

# Binaire utilisé : ifpromisc
# Test chaque interface réseau

# Méthode :
# 1. Vérifie promiscuous mode (PROMISC flag)
# 2. Vérifie packet sockets ouverts
# 3. Corrélation processus

# Output normal :
eth0: not promisc and no packet sniffer sockets
lo: not promisc and no packet sniffer sockets

# Output suspect :
eth0: PACKET SNIFFER(/usr/sbin/tcpdump[12345])
# → tcpdump running (peut être légitime)

eth0: PACKET SNIFFER(/tmp/.hax0r/sniff[5678])
# → Sniffer suspect (location /tmp/.hax0r)

# Vérifier manuellement :
ip link show
# eth0: <BROADCAST,MULTICAST,PROMISC,UP> ...
#                           ^^^^^^^ PROMISC = promiscuous mode

# Lister packet sockets :
netstat -i
# Kernel Interface table
# Iface   MTU   RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
# eth0   1500 1234567      0      0 0       8901234      0      0      0 BMPRU
#                                                                        ^^^^^
# P = PROMISC
```

### 4.5 Tests Logs Integrity

```bash
# Tests intégrité logs

# chklastlog : Vérifie /var/log/lastlog
Checking `chklastlog'...
# Détecte deletions entries lastlog
# Compare taille attendue vs réelle

# chkwtmp : Vérifie /var/log/wtmp
Checking `chkwtmp'...
# Détecte deletions entries wtmp (login records)
# Compare timestamps, gaps suspects

# chkutmp : Vérifie /var/run/utmp
Checking `chkutmp'...
# Détecte manipulation utmp (current logins)

# Output normal :
chklastlog: nothing deleted
chkwtmp: nothing deleted

# Output suspect :
chklastlog: deleted entry detected
The tty of the following users don't match `w': user1
# → Entry utilisateur supprimée logs (cover tracks)
```

---

## Section 5 : Options et Modes Scan

### 5.1 Options Command-Line

```bash
# Aide
chkrootkit -h

# Version
chkrootkit -V
# chkrootkit version 0.55

# Liste tests disponibles
chkrootkit -l
# ifpromisc chklastlog chkwtmp check_wtmpx chkproc chkdirs ...

# Exécuter test spécifique
sudo chkrootkit ifpromisc
# Teste seulement promiscuous mode

sudo chkrootkit chkproc
# Teste seulement processus cachés

sudo chkrootkit lkm
# Teste seulement LKM rootkits

# Mode debug (verbeux)
sudo chkrootkit -d
# Affiche commandes exécutées

# Mode quiet (seulement problèmes)
sudo chkrootkit -q
# N'affiche que INFECTED/Warning/Vulnerable

# Spécifier répertoire root custom
sudo chkrootkit -r /mnt/suspect-disk
# Scanne système monté ailleurs (forensique)

# Pas de couleurs (logs)
sudo chkrootkit -n

# Spécifier chemin binaires système
sudo chkrootkit -p /mnt/clean-system/bin
# Utilise binaries propres externes
```

### 5.2 Scan Spécifiques

```bash
# Test sniffer seulement
sudo chkrootkit ifpromisc

# Output :
# lo: not promisc and no packet sniffer sockets
# eth0: not promisc and no packet sniffer sockets

# Test processus cachés seulement
sudo chkrootkit chkproc

# Output :
# chkproc: nothing deleted

# Test fichiers cachés
sudo chkrootkit chkdirs

# Test logs manipulation
sudo chkrootkit chklastlog
sudo chkrootkit chkwtmp

# Test strings dans binaries
sudo chkrootkit strings-static /bin/ls | grep -i rootkit
```

### 5.3 Scan Système Monté (Forensique)

```bash
# Scénario : Disque suspect monté /mnt/suspect

# Monter partition suspecte (read-only)
sudo mount -o ro /dev/sdb1 /mnt/suspect

# Scanner avec chkrootkit
sudo chkrootkit -r /mnt/suspect

# Chkrootkit scannera :
# /mnt/suspect/bin/ls
# /mnt/suspect/usr/sbin/sshd
# /mnt/suspect/etc/
# ...

# Utiliser binaries propres (CRITIQUE)
# Créer directory binaries safe
mkdir /tmp/clean-bins
cp /bin/ls /tmp/clean-bins/
cp /bin/ps /tmp/clean-bins/
cp /bin/netstat /tmp/clean-bins/

# Scanner avec binaries propres
sudo chkrootkit -r /mnt/suspect -p /tmp/clean-bins
```

### 5.4 Scan Offline (Live CD)

```bash
# Méthode la plus sûre : Scanner depuis Live CD/USB

# 1. Booter sur Ubuntu Live USB
# 2. Installer chkrootkit dans Live session
sudo apt update
sudo apt install chkrootkit

# 3. Monter disque suspect (read-only)
sudo mkdir /mnt/system
sudo mount -o ro /dev/sda1 /mnt/system

# 4. Scanner
sudo chkrootkit -r /mnt/system

# 5. Sauvegarder résultats USB externe
sudo chkrootkit -r /mnt/system > /media/usb/scan-results.txt

# Avantages scan offline :
# ✅ Rootkit ne peut PAS interférer (pas running)
# ✅ Binaries Live CD garantis propres
# ✅ Filesystem read-only (pas de tampering)
# ✅ Résultats fiables à 100%
```

---

## Section 6 : Automatisation et Monitoring

### 6.1 Cron Job Quotidien

```bash
# Script scan automatique
sudo nano /usr/local/bin/chkrootkit-scan.sh

#!/bin/bash
# Chkrootkit automated scan

DATE=$(date +%Y%m%d)
LOGDIR="/var/log/chkrootkit"
LOGFILE="$LOGDIR/scan-$DATE.log"
ALERT_EMAIL="admin@example.com"

# Créer directory logs
mkdir -p $LOGDIR

# Run scan
echo "=== Chkrootkit Scan - $DATE ===" > $LOGFILE
echo "Started: $(date)" >> $LOGFILE
echo "" >> $LOGFILE

chkrootkit >> $LOGFILE 2>&1

echo "" >> $LOGFILE
echo "Completed: $(date)" >> $LOGFILE

# Vérifier infections
if grep -qE "INFECTED|Vulnerable" $LOGFILE; then
    # Alerte email
    INFECTED_COUNT=$(grep -c "INFECTED" $LOGFILE)
    VULNERABLE_COUNT=$(grep -c "Vulnerable" $LOGFILE)
    
    {
        echo "⚠️ Chkrootkit Alert - $(hostname)"
        echo ""
        echo "Infected: $INFECTED_COUNT"
        echo "Vulnerable: $VULNERABLE_COUNT"
        echo ""
        echo "=== Details ==="
        grep -E "INFECTED|Vulnerable" $LOGFILE
        echo ""
        echo "Full log: $LOGFILE"
    } | mail -s "ALERT: Chkrootkit detected issues on $(hostname)" $ALERT_EMAIL
fi

# Cleanup old logs (garder 90 jours)
find $LOGDIR -name "scan-*.log" -mtime +90 -delete

# Permissions
chmod +x /usr/local/bin/chkrootkit-scan.sh

# Cron job (tous les jours 3h du matin)
sudo crontab -e
0 3 * * * /usr/local/bin/chkrootkit-scan.sh
```

### 6.2 Monitoring Différentiel

```bash
# Script compare scans (détecte changements)
sudo nano /usr/local/bin/chkrootkit-diff.sh

#!/bin/bash
# Compare chkrootkit scans pour changements

LOGDIR="/var/log/chkrootkit"
TODAY=$(date +%Y%m%d)
YESTERDAY=$(date -d "yesterday" +%Y%m%d)

LOG_TODAY="$LOGDIR/scan-$TODAY.log"
LOG_YESTERDAY="$LOGDIR/scan-$YESTERDAY.log"

if [ ! -f "$LOG_YESTERDAY" ]; then
    echo "No previous scan found for comparison"
    exit 0
fi

# Comparer scans
DIFF=$(diff $LOG_YESTERDAY $LOG_TODAY)

if [ -n "$DIFF" ]; then
    echo "⚠️ Changes detected in chkrootkit scan"
    echo ""
    echo "=== Differences ==="
    echo "$DIFF"
    
    # Email si changements
    echo "$DIFF" | mail -s "Chkrootkit: Changes detected on $(hostname)" admin@example.com
else
    echo "✓ No changes since last scan"
fi

# Cron : après scan quotidien
# 30 3 * * * /usr/local/bin/chkrootkit-diff.sh
```

### 6.3 Integration Nagios/Icinga

```bash
# Plugin Nagios chkrootkit
sudo nano /usr/lib/nagios/plugins/check_chkrootkit

#!/bin/bash
# Nagios plugin chkrootkit

OUTPUT=$(chkrootkit 2>&1)

# Check infections
INFECTED=$(echo "$OUTPUT" | grep -c "INFECTED")
VULNERABLE=$(echo "$OUTPUT" | grep -c "Vulnerable")
WARNING=$(echo "$OUTPUT" | grep -c "Warning")

if [ $INFECTED -gt 0 ]; then
    echo "CRITICAL - $INFECTED rootkit(s) detected | infected=$INFECTED vulnerable=$VULNERABLE"
    exit 2
elif [ $VULNERABLE -gt 0 ]; then
    echo "WARNING - $VULNERABLE vulnerability detected | vulnerable=$VULNERABLE warning=$WARNING"
    exit 1
elif [ $WARNING -gt 0 ]; then
    echo "WARNING - $WARNING warning(s) | warning=$WARNING"
    exit 1
else
    echo "OK - No rootkits detected | clean=1"
    exit 0
fi

# Permissions
chmod +x /usr/lib/nagios/plugins/check_chkrootkit

# Configuration Nagios
# /etc/nagios/objects/commands.cfg
define command {
    command_name    check_chkrootkit
    command_line    $USER1$/check_chkrootkit
}

# /etc/nagios/objects/localhost.cfg
define service {
    use                     local-service
    host_name               localhost
    service_description     Chkrootkit
    check_command           check_chkrootkit
    check_interval          1440  # 1x par jour
}
```

### 6.4 Prometheus Exporter

```python
#!/usr/bin/env python3
# /usr/local/bin/chkrootkit-prometheus-exporter.py

from prometheus_client import start_http_server, Gauge
import subprocess
import re
import time

# Metrics
chkrootkit_infected = Gauge('chkrootkit_infected_count', 'Number of infections detected')
chkrootkit_vulnerable = Gauge('chkrootkit_vulnerable_count', 'Number of vulnerabilities')
chkrootkit_warnings = Gauge('chkrootkit_warning_count', 'Number of warnings')
chkrootkit_scan_duration = Gauge('chkrootkit_scan_duration_seconds', 'Scan duration')
chkrootkit_last_scan = Gauge('chkrootkit_last_scan_timestamp', 'Timestamp last scan')

def run_chkrootkit():
    """Run chkrootkit and parse results"""
    start_time = time.time()
    
    try:
        result = subprocess.run(['chkrootkit'], 
                              capture_output=True, 
                              text=True, 
                              timeout=300)
        
        output = result.stdout + result.stderr
        
        # Count issues
        infected = output.count('INFECTED')
        vulnerable = output.count('Vulnerable')
        warnings = output.count('Warning')
        
        # Update metrics
        chkrootkit_infected.set(infected)
        chkrootkit_vulnerable.set(vulnerable)
        chkrootkit_warnings.set(warnings)
        
        duration = time.time() - start_time
        chkrootkit_scan_duration.set(duration)
        chkrootkit_last_scan.set(time.time())
        
        print(f"Scan completed: infected={infected}, vulnerable={vulnerable}, warnings={warnings}")
        
    except Exception as e:
        print(f"Error running chkrootkit: {e}")

if __name__ == '__main__':
    # Start HTTP server
    start_http_server(9192)
    print("Chkrootkit Prometheus exporter started on port 9192")
    
    # Run scan every 24 hours
    while True:
        run_chkrootkit()
        time.sleep(86400)  # 24h
```

---

## Section 7 : Chkrootkit vs Alternatives

### 7.1 Comparaison Outils

| Critère | Chkrootkit | Rkhunter | AIDE | Lynis | OSSEC |
|---------|------------|----------|------|-------|-------|
| **Type** | Rootkit scanner | Rootkit scanner | FIM | Audit complet | HIDS |
| **Détection** | Signatures 70+ | Signatures 400+ | Checksums | Config audit | Temps réel |
| **Faux positifs** | Élevés | Moyens | Faibles | Faibles | Faibles |
| **Complexité** | Basse | Moyenne | Moyenne | Moyenne | Haute |
| **Maintenance** | Active | Active | Active | Active | Active |
| **Database** | Non | Oui | Oui | Non | Oui |
| **Updates** | Manuels | Auto | Manuel | Auto | Auto |
| **Performance** | Rapide | Rapide | Lent (init) | Moyen | Léger |
| **Use case** | Quick scan | Production | Compliance | Audit | Enterprise |

### 7.2 Chkrootkit vs Rkhunter

```bash
# Chkrootkit
# Avantages :
✅ Plus ancien (1997), très testé
✅ Plus rapide (scripts shell simples)
✅ Pas de config requise (works out of box)
✅ Binaires C compilés statiquement disponibles

# Inconvénients :
❌ Moins de signatures (70 vs 400+)
❌ Pas de database checksums intégrée
❌ Pas d'updates automatiques
❌ Plus de faux positifs

# Rkhunter
# Avantages :
✅ Plus de signatures rootkits (400+)
✅ Database checksums intégrée
✅ Updates automatiques (rkhunter --update)
✅ Moins faux positifs
✅ Whitelist sophistiquée

# Inconvénients :
❌ Plus complexe configuration
❌ Nécessite database init/update
❌ Plus lent

# Recommandation : Utiliser LES DEUX
# Complémentaires, pas redondants
sudo chkrootkit && sudo rkhunter --check --skip-keypress
```

### 7.3 Complémentarité AIDE

```bash
# AIDE (Advanced Intrusion Detection Environment)
# = File Integrity Monitoring (FIM)

# Différence chkrootkit :
# Chkrootkit : Détecte rootkits connus (signatures)
# AIDE : Détecte TOUTE modification fichiers (checksums)

# Workflow complémentaire :

# 1. Installation système propre
sudo apt install aide

# 2. Initialiser database AIDE (baseline)
sudo aideinit
# Crée /var/lib/aide/aide.db.new

# 3. Activer database
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# 4. Scan quotidien AIDE (détecte modifications)
sudo aide --check

# 5. Scan quotidien chkrootkit (détecte rootkits)
sudo chkrootkit

# AIDE détecte :
# - /bin/ls modifié (size, checksum changed)
# - Nouveaux fichiers /dev/.hidden/
# - Permissions modifiées /etc/passwd

# Chkrootkit détecte :
# - Signatures rootkits connus
# - Processus cachés
# - Network sniffers

# Ensemble = protection robuste
```

### 7.4 Integration OSSEC

```bash
# OSSEC = Host-based Intrusion Detection System (HIDS)
# Monitoring temps réel + alertes

# Integration chkrootkit dans OSSEC
# /var/ossec/etc/ossec.conf

<ossec_config>
  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/chkrootkit/scan.log</location>
  </localfile>

  <command>
    <name>chkrootkit</name>
    <executable>chkrootkit.sh</executable>
    <timeout_allowed>yes</timeout_allowed>
  </command>

  <active-response>
    <disabled>no</disabled>
    <command>chkrootkit</command>
    <location>local</location>
    <rules_id>510</rules_id>
  </active-response>
</ossec_config>

# OSSEC déclenche chkrootkit scan selon events
# Résultats centralisés dashboard OSSEC
```

---

## Section 8 : Faux Positifs et Whitelist

### 8.1 Faux Positifs Courants

**Virtualisation / Containers :**

```bash
# Output suspect (faux positif) :
Checking `lkm'...                                           You have     10 process hidden for readdir command

# Cause : OpenVZ/LXC/Docker containers
# Processus containers pas visibles host ou inverse

# Vérifier si virtualisation :
systemd-detect-virt
# Output : openvz, lxc, docker, kvm, etc.

# Solution : Ignorer warning si virtualisation confirmée

# Autre faux positif containers :
Searching for suspicious files and dirs...
Warning: /dev/.lxc found
Warning: /dev/.udev found

# → .lxc, .udev sont légitimes containers/systemd
```

**Kernel Custom / Modules Légitimes :**

```bash
# Faux positif :
Searching for Linux/Ebury - Operation Windigo ssh...       Warning: Possible Linux/Ebury - Operation Windigo installed

# Cause : Kernel custom ou module légitime similar signature
# Vérifier manuellement :
strings /usr/sbin/sshd | grep -i ebury
# Si output vide = faux positif

# Modules kernel légitimes peuvent trigger :
Searching for suspicious files and dirs...
Warning: /lib/modules/5.15.0-91-generic/kernel/drivers/video/.vga found

# → .vga directory légitime kernel modules
```

**DHCP Client / Network Tools :**

```bash
# Faux positif sniffer :
Checking `sniffer'...                                       eth0: PACKET SNIFFER(/sbin/dhclient[1234])

# Cause : dhclient utilise packet sockets (normal DHCP)
# Vérifier process :
ps aux | grep 1234
# root  1234  dhclient -v eth0

# → Légitime, pas rootkit
```

### 8.2 Configuration Suppressions

```bash
# Créer fichier whitelist custom
sudo nano /usr/local/etc/chkrootkit-whitelist.conf

# Processus whitelist (ignore sniffer warnings)
WHITELIST_PROCS="dhclient tcpdump wireshark"

# Fichiers whitelist (ignore suspicious files)
WHITELIST_FILES="/dev/.lxc /dev/.udev /dev/.blkid"

# Modules whitelist
WHITELIST_MODULES="vga"

# Wrapper script chkrootkit avec filtering
sudo nano /usr/local/bin/chkrootkit-filtered.sh

#!/bin/bash
# Chkrootkit avec filtering faux positifs

# Run chkrootkit
OUTPUT=$(chkrootkit 2>&1)

# Filter false positives
echo "$OUTPUT" | \
    grep -v "dhclient" | \
    grep -v "/dev/.lxc" | \
    grep -v "/dev/.udev" | \
    grep -v "OpenVZ" | \
    grep -v "LXC container"

# Permissions
chmod +x /usr/local/bin/chkrootkit-filtered.sh
```

### 8.3 Patch Chkrootkit (Suppressions)

```bash
# Méthode avancée : Patcher chkrootkit script

# Backup original
sudo cp /usr/sbin/chkrootkit /usr/sbin/chkrootkit.original

# Éditer script
sudo nano /usr/sbin/chkrootkit

# Chercher section sniffer test (ligne ~2000)
# Ajouter exceptions :

# Avant :
if [ "$PACKET_SNIFFER" != "0" ]; then
    echo "PACKET SNIFFER($PACKET_SNIFFER)"
fi

# Après (avec filtering) :
if [ "$PACKET_SNIFFER" != "0" ]; then
    # Ignore dhclient (légitime)
    if echo "$PACKET_SNIFFER" | grep -q "dhclient"; then
        : # Ignore
    else
        echo "PACKET SNIFFER($PACKET_SNIFFER)"
    fi
fi

# Sauvegarder
# Note : Patch perdu si update chkrootkit via package manager
```

### 8.4 Documentation Faux Positifs

```bash
# Créer documentation false positives
sudo nano /root/chkrootkit-false-positives.md

# Chkrootkit False Positives Documentation

## Server: web-prod-01

### Virtualisation
- Type: OpenVZ container
- False positive: "10 process hidden for readdir command"
- Reason: Container processes not visible to host
- Action: IGNORE

### Network
- False positive: "PACKET SNIFFER(/sbin/dhclient[1234])"
- Reason: DHCP client legitimate packet socket
- Action: IGNORE

### Suspicious Files
- False positive: "Warning: /dev/.lxc found"
- Reason: LXC container legitimate directory
- Action: IGNORE

## Last reviewed: 2024-01-16
## Reviewed by: Admin Team
```

---

## Section 9 : Intégration SIEM et Alertes

### 9.1 Syslog Integration

```bash
# Logger résultats vers syslog
sudo nano /usr/local/bin/chkrootkit-syslog.sh

#!/bin/bash
# Chkrootkit avec logging syslog

OUTPUT=$(chkrootkit 2>&1)

# Parse résultats
INFECTED=$(echo "$OUTPUT" | grep -c "INFECTED")
VULNERABLE=$(echo "$OUTPUT" | grep -c "Vulnerable")
WARNING=$(echo "$OUTPUT" | grep -c "Warning")

# Log via logger
if [ $INFECTED -gt 0 ]; then
    logger -t chkrootkit -p security.crit "CRITICAL: $INFECTED infection(s) detected"
    echo "$OUTPUT" | grep "INFECTED" | while read line; do
        logger -t chkrootkit -p security.crit "$line"
    done
fi

if [ $VULNERABLE -gt 0 ]; then
    logger -t chkrootkit -p security.warning "WARNING: $VULNERABLE vulnerability detected"
fi

if [ $WARNING -gt 0 ]; then
    logger -t chkrootkit -p security.notice "NOTICE: $WARNING warning(s)"
fi

if [ $INFECTED -eq 0 ] && [ $VULNERABLE -eq 0 ] && [ $WARNING -eq 0 ]; then
    logger -t chkrootkit -p security.info "Scan completed - No issues detected"
fi

# Logs visibles dans /var/log/syslog :
# Jan 16 03:00:01 server chkrootkit[12345]: Scan completed - No issues detected
```

### 9.2 Splunk Integration

```bash
# Envoyer logs Splunk HEC (HTTP Event Collector)
sudo nano /usr/local/bin/chkrootkit-splunk.sh

#!/bin/bash
# Chkrootkit → Splunk

SPLUNK_HEC_URL="https://splunk.example.com:8088/services/collector"
SPLUNK_TOKEN="YOUR_HEC_TOKEN"

# Run scan
OUTPUT=$(chkrootkit 2>&1)

# Parse et envoyer Splunk
TIMESTAMP=$(date +%s)
HOSTNAME=$(hostname)

# Event JSON
JSON_EVENT=$(cat <<EOF
{
  "time": $TIMESTAMP,
  "host": "$HOSTNAME",
  "sourcetype": "chkrootkit",
  "event": {
    "scan_output": $(echo "$OUTPUT" | jq -Rs .),
    "infected": $(echo "$OUTPUT" | grep -c "INFECTED"),
    "vulnerable": $(echo "$OUTPUT" | grep -c "Vulnerable"),
    "warnings": $(echo "$OUTPUT" | grep -c "Warning")
  }
}
EOF
)

# Envoyer Splunk
curl -k -X POST "$SPLUNK_HEC_URL" \
    -H "Authorization: Splunk $SPLUNK_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$JSON_EVENT"
```

### 9.3 Slack Webhook

```bash
# Alertes Slack
sudo nano /usr/local/bin/chkrootkit-slack.sh

#!/bin/bash
# Chkrootkit alertes Slack

SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

OUTPUT=$(chkrootkit 2>&1)

# Vérifier infections
if echo "$OUTPUT" | grep -qE "INFECTED|Vulnerable"; then
    INFECTED=$(echo "$OUTPUT" | grep -c "INFECTED")
    VULNERABLE=$(echo "$OUTPUT" | grep -c "Vulnerable")
    
    # Issues détaillées
    ISSUES=$(echo "$OUTPUT" | grep -E "INFECTED|Vulnerable" | head -10)
    
    # Message Slack
    PAYLOAD=$(cat <<EOF
{
  "text": "🚨 *Chkrootkit Alert*",
  "attachments": [
    {
      "color": "danger",
      "fields": [
        {
          "title": "Server",
          "value": "$(hostname)",
          "short": true
        },
        {
          "title": "Infected",
          "value": "$INFECTED",
          "short": true
        },
        {
          "title": "Vulnerable",
          "value": "$VULNERABLE",
          "short": true
        },
        {
          "title": "Issues",
          "value": "\`\`\`$ISSUES\`\`\`",
          "short": false
        }
      ],
      "footer": "Chkrootkit",
      "ts": $(date +%s)
    }
  ]
}
EOF
)
    
    # Envoyer Slack
    curl -X POST -H 'Content-type: application/json' \
        --data "$PAYLOAD" \
        "$SLACK_WEBHOOK"
fi
```

### 9.4 PagerDuty Integration

```bash
# Alertes PagerDuty (incidents critiques)
sudo nano /usr/local/bin/chkrootkit-pagerduty.sh

#!/bin/bash
# Chkrootkit → PagerDuty

PAGERDUTY_API_KEY="YOUR_API_KEY"
PAGERDUTY_SERVICE_KEY="YOUR_SERVICE_KEY"

OUTPUT=$(chkrootkit 2>&1)

# Trigger incident si INFECTED
if echo "$OUTPUT" | grep -q "INFECTED"; then
    INFECTED_DETAILS=$(echo "$OUTPUT" | grep "INFECTED")
    
    # Créer incident PagerDuty
    curl -X POST "https://api.pagerduty.com/incidents" \
        -H "Accept: application/vnd.pagerduty+json;version=2" \
        -H "Authorization: Token token=$PAGERDUTY_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
          \"incident\": {
            \"type\": \"incident\",
            \"title\": \"Rootkit detected on $(hostname)\",
            \"service\": {
              \"id\": \"$PAGERDUTY_SERVICE_KEY\",
              \"type\": \"service_reference\"
            },
            \"urgency\": \"high\",
            \"body\": {
              \"type\": \"incident_body\",
              \"details\": \"$INFECTED_DETAILS\"
            }
          }
        }"
fi
```

---

## Section 10 : Cas Pratiques Détection

### 10.1 Détection Binary Trojan (ls)

**Scénario : /bin/ls trojaned**

```bash
# Symptômes :
# - Fichiers cachés pas visibles avec `ls`
# - `ls -la /tmp` ne montre pas backdoor files

# Test chkrootkit :
sudo chkrootkit

# Output :
Checking `ls'...                                            INFECTED

# Vérification manuelle :

# 1. Comparer avec binary propre
# Télécharger package coreutils (contient ls)
apt download coreutils
dpkg -x coreutils_*.deb /tmp/clean-bins
/tmp/clean-bins/bin/ls -la /tmp

# Compare avec /bin/ls output :
/bin/ls -la /tmp

# Si différences = INFECTED

# 2. Vérifier checksum
debsums coreutils | grep "/bin/ls"
# Output : /bin/ls                FAILED
# = Checksum mismatch = modifié

# 3. Strings analysis
strings /bin/ls | grep -i "backdoor\|rootkit\|hack"
# Si match = INFECTED

# Remediation :
# 1. Booter Live CD
# 2. Réinstaller package
sudo apt install --reinstall coreutils

# 3. Vérifier
sudo chkrootkit
# Checking `ls'...                                            not infected
```

### 10.2 Détection Processus Caché (LKM)

**Scénario : Rootkit kernel cache processus backdoor**

```bash
# Symptômes :
# - Connexion réseau suspecte (netstat vide)
# - Charge CPU élevée (ps ne montre rien)

# Test chkrootkit :
sudo chkrootkit

# Output :
Checking `lkm'...                                           You have     3 process hidden for readdir command

# Vérification manuelle :

# 1. Comparer ps vs /proc
ps aux | wc -l
# Output : 52 processus

ls /proc | grep "^[0-9]" | wc -l
# Output : 55 PIDs
# → 3 processus cachés !

# 2. Identifier PIDs cachés
comm -23 \
    <(ls /proc | grep "^[0-9]" | sort) \
    <(ps aux | awk '{print $2}' | sort)
# Output : 1234, 5678, 9012

# 3. Examiner processus caché
sudo cat /proc/1234/cmdline
# Output : /tmp/.hax0r/backdoor
# = Backdoor !

# 4. Identifier LKM malveillant
lsmod | grep -v "^Module"
# Chercher modules suspects

# Remediation :
# 1. Arrêter processus (peut résister kill)
sudo kill -9 1234 5678 9012

# 2. Supprimer LKM
sudo rmmod <module_suspect>

# 3. Investigation complète forensique
# → Rebuild complet système recommandé
```

### 10.3 Détection Network Sniffer

**Scénario : Sniffer packet installé attaquant**

```bash
# Test chkrootkit :
sudo chkrootkit ifpromisc

# Output :
eth0: PACKET SNIFFER(/tmp/.sniff/capture[4567])

# Vérification manuelle :

# 1. Vérifier promiscuous mode
ip link show eth0
# eth0: <BROADCAST,MULTICAST,PROMISC,UP> ...
#                           ^^^^^^^ SUSPECT

# 2. Identifier process
ps aux | grep 4567
# Output : root  4567  /tmp/.sniff/capture -i eth0 -w /tmp/.dump

# 3. Vérifier fichiers dump
ls -la /tmp/.dump
# -rw------- 1 root root 500M Jan 16 14:30 traffic.pcap
# → 500MB trafic capturé !

# 4. Analyser dump (vérifier credentials volées)
tcpdump -r /tmp/.dump -A | grep -i "password"

# Remediation :
# 1. Kill process
sudo kill -9 4567

# 2. Désactiver promiscuous mode
sudo ip link set eth0 promisc off

# 3. Supprimer sniffer
sudo rm -rf /tmp/.sniff /tmp/.dump

# 4. Changer passwords compromis
# 5. Investigation forensique complète
```

### 10.4 Détection Logs Tampering

**Scénario : Attaquant efface logs connexions**

```bash
# Test chkrootkit :
sudo chkrootkit chklastlog
sudo chkrootkit chkwtmp

# Output :
The tty of the following users don't match `w': admin
chkwtmp: nothing deleted (but suspicious gaps detected)

# Vérification manuelle :

# 1. Comparer w vs lastlog
w
# admin   pts/0    192.168.1.100   15:30   0:00  bash

lastlog | grep admin
# admin           **Never logged in**
# → SUSPECT : admin connecté mais lastlog dit jamais !

# 2. Vérifier wtmp
last -f /var/log/wtmp | grep admin
# Gaps suspects dans timeline

# 3. Vérifier utmp
who
# admin   pts/0    2024-01-16 15:30 (192.168.1.100)

# Remediation :
# Logs tampering = compromission sévère
# → Investigation forensique complète
# → Rebuild système recommandé
# → Impossible restaurer logs effacés
```

---

## Section 11 : Limitations et Compléments

### 11.1 Limitations Chkrootkit

```markdown
## Limitations Techniques

1. **Dépendance binaires système**
   - Chkrootkit utilise /bin/ls, /bin/ps, etc.
   - Si ces binaries trojaned → résultats non fiables
   
   Solution : Binaires statiques compilation propre
             Scan offline depuis Live CD

2. **Détection signature-based**
   - Détecte SEULEMENT rootkits connus
   - Rootkits custom/nouveaux passent inaperçus
   
   Solution : Compléter avec FIM (AIDE), heuristique

3. **Faux positifs élevés**
   - Virtualisation trigger warnings
   - Kernels custom suspect
   - Applications légitimes (tcpdump)
   
   Solution : Whitelist, documentation false positives

4. **Pas de checksums database**
   - Ne peut dire si binary modifié sans référence
   
   Solution : debsums (Debian), rpm -V (RHEL)
             AIDE database baseline

5. **Scan ponctuel (pas temps réel)**
   - Rootkit peut s'installer entre 2 scans
   
   Solution : HIDS temps réel (OSSEC, Wazuh, osquery)

6. **Rootkits sophistiqués échappent**
   - Rootkits firmware (BIOS/UEFI)
   - Rootkits hypervisor-level
   - Rootkits anti-forensics avancés
   
   Solution : Détection nécessite outils spécialisés
```

### 11.2 Stack Sécurité Complète

```bash
# Stack défense en profondeur

1. Prevention (avant infection)
   ├── Hardening système (Lynis)
   ├── Firewall (UFW, iptables)
   ├── IPS (Fail2ban)
   ├── Updates automatiques
   └── Principle least privilege

2. Detection (pendant/après)
   ├── Rootkit scanners (Chkrootkit, Rkhunter)
   ├── File integrity (AIDE, Tripwire)
   ├── Antivirus (ClamAV)
   ├── Log monitoring (OSSEC, Wazuh)
   └── Network IDS (Snort, Suricata)

3. Response (après détection)
   ├── Alertes automatiques
   ├── Investigation forensique
   ├── Isolation système compromis
   ├── Rebuild depuis backup
   └── Post-incident review

# Configuration complète :

# Prevention
sudo apt install lynis ufw fail2ban unattended-upgrades
sudo lynis audit system
sudo ufw enable
sudo systemctl enable fail2ban

# Detection
sudo apt install chkrootkit rkhunter aide clamav
sudo aideinit
sudo freshclam

# Monitoring
sudo apt install ossec-hids
# Configurer centralisation logs

# Scans quotidiens automatisés
0 3 * * * /usr/local/bin/chkrootkit-scan.sh
0 4 * * * /usr/bin/rkhunter --check --skip-keypress
0 5 * * * /usr/bin/aide --check
0 6 * * * /usr/bin/clamscan -r /home /var/www
```

### 11.3 Outils Complémentaires

**Osquery (Monitoring Forensique) :**

```bash
# Osquery = SQL interface système monitoring

# Installation
wget https://pkg.osquery.io/deb/osquery_5.11.0-1.linux_amd64.deb
sudo dpkg -i osquery_*.deb

# Query processus cachés (similaire chkrootkit)
osqueryi

SELECT * FROM processes 
WHERE pid NOT IN (SELECT pid FROM process_open_sockets);

# Detect promiscuous mode
SELECT * FROM interface_details WHERE flags LIKE '%PROMISC%';

# Detect suspicious modules
SELECT * FROM kernel_modules WHERE name LIKE '%rootkit%';

# Detect hidden files
SELECT * FROM file WHERE path LIKE '/dev/.%';
```

**Unhide (Processus/Ports Cachés) :**

```bash
# Unhide = Détection processus/ports cachés

# Installation
sudo apt install unhide

# Scan processus cachés
sudo unhide proc

# Scan TCP ports cachés
sudo unhide tcp

# Scan rapide
sudo unhide-tcp quick
```

**OSSEC (HIDS Production) :**

```bash
# OSSEC = Host-based IDS temps réel

# Installation server
wget https://github.com/ossec/ossec-hids/archive/3.7.0.tar.gz
tar -xzf 3.7.0.tar.gz
cd ossec-hids-*
sudo ./install.sh

# Configuration rootkit detection
# /var/ossec/etc/ossec.conf
<rootcheck>
  <disabled>no</disabled>
  <check_files>yes</check_files>
  <check_trojans>yes</check_trojans>
  <check_dev>yes</check_dev>
  <check_sys>yes</check_sys>
  <check_pids>yes</check_pids>
  <check_ports>yes</check_ports>
  <check_if>yes</check_if>
  <frequency>36000</frequency> <!-- 10 heures -->
</rootcheck>

# OSSEC combine :
# - File integrity monitoring
# - Rootkit detection
# - Log analysis
# - Active response
```

---

## Section 12 : Best Practices Production

### 12.1 Configuration Production

```bash
#!/bin/bash
# setup-chkrootkit-production.sh

echo "=== Chkrootkit Production Setup ==="

# 1. Installer chkrootkit
sudo apt update
sudo apt install chkrootkit

# 2. Créer directories
sudo mkdir -p /var/log/chkrootkit
sudo mkdir -p /opt/chkrootkit-baseline

# 3. Baseline checksums (système propre)
echo "Creating baseline checksums..."
sudo debsums coreutils > /opt/chkrootkit-baseline/coreutils.debsums
sudo debsums procps > /opt/chkrootkit-baseline/procps.debsums
sudo debsums net-tools > /opt/chkrootkit-baseline/net-tools.debsums

# 4. Script scan automatique
sudo tee /usr/local/bin/chkrootkit-production.sh > /dev/null << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d-%H%M%S)
LOGFILE="/var/log/chkrootkit/scan-$DATE.log"
ALERT_EMAIL="security@example.com"

# Scan
echo "=== Chkrootkit Scan $DATE ===" > $LOGFILE
chkrootkit >> $LOGFILE 2>&1

# Vérifier checksums
echo "" >> $LOGFILE
echo "=== Package Integrity Check ===" >> $LOGFILE
debsums -c coreutils procps net-tools >> $LOGFILE 2>&1

# Alertes
if grep -qE "INFECTED|Vulnerable|FAILED" $LOGFILE; then
    SUMMARY=$(grep -E "INFECTED|Vulnerable|FAILED" $LOGFILE)
    echo "🚨 Security Alert - $(hostname)" | \
        mail -s "ALERT: Rootkit/Integrity Check Failed" \
        -a $LOGFILE $ALERT_EMAIL
fi

# Cleanup (garder 180 jours)
find /var/log/chkrootkit -name "scan-*.log" -mtime +180 -delete
EOF

sudo chmod +x /usr/local/bin/chkrootkit-production.sh

# 5. Cron job
echo "0 3 * * * /usr/local/bin/chkrootkit-production.sh" | sudo crontab -

# 6. Installer compléments
sudo apt install rkhunter aide

# 7. Tests
echo "Running initial scan..."
sudo /usr/local/bin/chkrootkit-production.sh

echo "✅ Chkrootkit production setup completed"
```

### 12.2 Checklist Production

```markdown
## Chkrootkit Production Checklist

### Installation
- [ ] Chkrootkit installé (version latest stable)
- [ ] Vérification intégrité package (debsums/rpm -V)
- [ ] Binaires statiques compilés (backup)
- [ ] Permissions correctes (root-owned)

### Baseline
- [ ] Baseline checksums créée (système propre)
- [ ] Documentation binaries légitimes
- [ ] Whitelist faux positifs documentée
- [ ] Backup baseline sécurisée (offline)

### Automatisation
- [ ] Script scan quotidien créé
- [ ] Cron job configuré (3h matin)
- [ ] Logs directory créé (/var/log/chkrootkit)
- [ ] Rotation logs configurée (180 jours)

### Alertes
- [ ] Email alertes configurées
- [ ] Slack/PagerDuty integration (si critique)
- [ ] Syslog/SIEM integration
- [ ] Escalade procédure documentée

### Compléments
- [ ] Rkhunter installé (détection alternative)
- [ ] AIDE installé (file integrity)
- [ ] Debsums configuré (package verification)
- [ ] OSSEC/Wazuh (si HIDS requis)

### Testing
- [ ] Scan initial exécuté (baseline)
- [ ] Faux positifs identifiés
- [ ] Alertes testées (email fonctionnel)
- [ ] Procédure response testée

### Documentation
- [ ] Runbook incident response
- [ ] False positives documentés
- [ ] Contacts on-call définis
- [ ] Procédure rebuild documentée

### Maintenance
- [ ] Review logs hebdomadaire
- [ ] Update chkrootkit mensuel
- [ ] Baseline refresh annuel
- [ ] Training équipe régulier
```

### 12.3 Incident Response Workflow

```bash
# Workflow si chkrootkit détecte infection

1. ISOLER SYSTÈME
   ─────────────
   # Déconnecter réseau
   sudo ip link set eth0 down
   
   # Bloquer tout trafic
   sudo iptables -P INPUT DROP
   sudo iptables -P OUTPUT DROP
   sudo iptables -P FORWARD DROP

2. PRÉSERVER EVIDENCE
   ──────────────────
   # Snapshot RAM (si VM)
   # Dump mémoire
   sudo dd if=/dev/mem of=/mnt/usb/memory.dump bs=1M
   
   # Copier logs
   sudo tar -czf /mnt/usb/logs-$(date +%Y%m%d).tar.gz /var/log
   
   # Chkrootkit output
   sudo chkrootkit > /mnt/usb/chkrootkit-forensic.log

3. INVESTIGATION FORENSIQUE
   ────────────────────────
   # Booter Live CD (forensique)
   # Scanner offline
   # Analyse binaries suspects
   # Timeline reconstruction

4. CONTAINMENT
   ───────────
   # Arrêter services compromis
   # Changer passwords (depuis autre machine)
   # Révoquer clés SSH
   # Update firewall rules autres serveurs

5. ERADICATION
   ───────────
   # Rebuild système from scratch
   # Restaurer depuis backup propre (avant infection)
   # Ne PAS tenter "nettoyer" rootkit kernel-level

6. RECOVERY
   ────────
   # Rebuild complet
   # Restaurer data depuis backup vérifiée
   # Hardening renforcé
   # Monitoring accru

7. POST-INCIDENT
   ─────────────
   # Root cause analysis
   # Documentation incident
   # Amélioration procédures
   # Training équipe
```

### 12.4 Script Complet Production

```bash
#!/bin/bash
# /usr/local/bin/chkrootkit-enterprise.sh
# Production-grade chkrootkit scanning

set -euo pipefail

# Configuration
LOGDIR="/var/log/chkrootkit"
DATE=$(date +%Y%m%d-%H%M%S)
LOGFILE="$LOGDIR/scan-$DATE.log"
BASELINE_DIR="/opt/chkrootkit-baseline"
ALERT_EMAIL="security-team@example.com"
SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK"

# Fonctions
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOGFILE"
}

alert_email() {
    local subject="$1"
    local body="$2"
    echo "$body" | mail -s "$subject" -a "$LOGFILE" "$ALERT_EMAIL"
}

alert_slack() {
    local message="$1"
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"$message\"}" \
        "$SLACK_WEBHOOK" 2>/dev/null || true
}

# Main
mkdir -p "$LOGDIR"

log "=== Chkrootkit Enterprise Scan Started ==="
log "Hostname: $(hostname)"
log "Kernel: $(uname -r)"

# 1. Chkrootkit scan
log "Running chkrootkit..."
chkrootkit 2>&1 | tee -a "$LOGFILE"

# 2. Package integrity
log ""
log "=== Package Integrity Verification ==="
debsums -c 2>&1 | tee -a "$LOGFILE" || true

# 3. Baseline comparison
if [ -f "$BASELINE_DIR/system-baseline.txt" ]; then
    log ""
    log "=== Baseline Comparison ==="
    CURRENT_HASH=$(find /bin /sbin /usr/bin /usr/sbin -type f -exec md5sum {} \; 2>/dev/null | sort | md5sum)
    BASELINE_HASH=$(cat "$BASELINE_DIR/system-baseline.txt")
    
    if [ "$CURRENT_HASH" != "$BASELINE_HASH" ]; then
        log "WARNING: System binaries changed since baseline!"
    else
        log "OK: System binaries match baseline"
    fi
fi

# 4. Process analysis
log ""
log "=== Process Analysis ==="
PS_COUNT=$(ps aux | wc -l)
PROC_COUNT=$(ls /proc | grep -E '^[0-9]+$' | wc -l)
DIFF=$((PROC_COUNT - PS_COUNT))

log "Processes (ps): $PS_COUNT"
log "Processes (/proc): $PROC_COUNT"
log "Hidden processes: $DIFF"

if [ $DIFF -gt 5 ]; then
    log "WARNING: Significant process hiding detected!"
fi

# 5. Network analysis
log ""
log "=== Network Analysis ==="
for iface in $(ip link show | grep -oP '^\d+: \K[^:]+' | grep -v lo); do
    if ip link show "$iface" | grep -q PROMISC; then
        log "WARNING: Interface $iface in promiscuous mode"
    fi
done

# 6. Parse results
log ""
log "=== Results Summary ==="
INFECTED=$(grep -c "INFECTED" "$LOGFILE" || true)
VULNERABLE=$(grep -c "Vulnerable" "$LOGFILE" || true)
WARNINGS=$(grep -c "Warning" "$LOGFILE" || true)

log "Infected: $INFECTED"
log "Vulnerable: $VULNERABLE"
log "Warnings: $WARNINGS"

# 7. Alertes
if [ $INFECTED -gt 0 ]; then
    SEVERITY="CRITICAL"
    alert_email "🚨 CRITICAL: Rootkit detected on $(hostname)" \
        "Chkrootkit detected $INFECTED infection(s). Immediate action required."
    alert_slack "🚨 *CRITICAL*: Rootkit detected on $(hostname) - $INFECTED infection(s)"
elif [ $VULNERABLE -gt 0 ]; then
    SEVERITY="WARNING"
    alert_email "⚠️ WARNING: Vulnerabilities on $(hostname)" \
        "Chkrootkit detected $VULNERABLE vulnerability. Review required."
    alert_slack "⚠️ *WARNING*: Vulnerabilities on $(hostname) - $VULNERABLE found"
elif [ $WARNINGS -gt 0 ]; then
    SEVERITY="NOTICE"
    log "Notice: $WARNINGS warnings (review recommended)"
else
    SEVERITY="OK"
    log "All checks passed - No issues detected"
fi

log "Scan completed - Severity: $SEVERITY"

# 8. Cleanup
find "$LOGDIR" -name "scan-*.log" -mtime +180 -delete

exit 0
```

---

## Ressources et Références

**Site officiel :**
- Homepage : http://www.chkrootkit.org/
- FTP download : ftp://ftp.chkrootkit.org/pub/seg/pac/
- Documentation : http://www.chkrootkit.org/README

**Alternatives :**
- Rkhunter : https://rkhunter.sourceforge.net/
- AIDE : https://aide.github.io/
- OSSEC : https://www.ossec.net/
- Wazuh : https://wazuh.com/

**Rootkits database :**
- Rootkit Hunter DB : https://rkhunter.sourceforge.net/rootkits.html
- SANS Rootkits : https://www.sans.org/reading-room/whitepapers/malicious/rootkits-101-281

**Communauté :**
- Mailing list : http://www.chkrootkit.org/
- Security focus : https://securityfocus.com/

---

## Conclusion

**Chkrootkit = Outil essentiel détection rootkits Linux**

**Points clés :**

✅ **Détection 70+ rootkits** = Signatures connus depuis 1997
✅ **Multi-vecteurs** = Binaries, LKM, sniffers, logs
✅ **Léger** = Scripts shell + binaires C, pas daemon
✅ **Safe** = Read-only, aucune modification système
✅ **Gratuit** = GPL, open-source, maintenu activement

**Workflow recommandé :**

```bash
# 1. Installation
sudo apt install chkrootkit

# 2. Baseline (système propre)
sudo debsums > /root/baseline-checksums.txt

# 3. Scan initial
sudo chkrootkit > /var/log/chkrootkit-baseline.log

# 4. Automatisation
sudo crontab -e
0 3 * * * /usr/local/bin/chkrootkit-scan.sh

# 5. Alertes
# Configuration email/Slack dans script

# 6. Compléments
sudo apt install rkhunter aide
sudo aideinit

# 7. Monitoring
# Review logs hebdomadaire
# Investigation anomalies
# Update baseline annuel
```

**Limitations critiques :**

- ❌ Peut être trompé (si binaries système compromis)
- ❌ Signatures-based (rootkits custom passent)
- ❌ Faux positifs (virtualisation, containers)
- ❌ Scan ponctuel (pas temps réel)

**Solutions :**

- ✅ Scanner depuis Live CD (offline)
- ✅ Compléter avec rkhunter, AIDE, OSSEC
- ✅ Whitelist faux positifs documentée
- ✅ Stack sécurité multicouches


**Tu maîtrises maintenant chkrootkit de l'installation aux investigations forensiques production !** 🔍

---

**Guide Chkrootkit Complet terminé !** 🎉


Voilà le guide complet Chkrootkit exhaustif ! Il couvre :

✅ **12 sections complètes** avec analogie pédagogique  
✅ Introduction rootkits et concepts (4 niveaux)  
✅ Installation sécurisée (packages, source, statique)  
✅ Premier scan et interprétation résultats  
✅ Tests détaillés (50+ checks binaries, LKM, sniffers)  
✅ Options et modes scan (forensique, offline)  
✅ Automatisation complète (cron, monitoring, SIEM)  
✅ Comparaison vs alternatives (rkhunter, AIDE, OSSEC)  
✅ Faux positifs et whitelist  
✅ Intégration Splunk/Slack/PagerDuty  
✅ Cas pratiques détection (binaries trojaned, LKM, sniffers)  
✅ Limitations et stack sécurité complète  
✅ Best practices production avec scripts prêts  
✅ Incident response workflow complet  

**Même exhaustivité rigoureuse que tes guides précédents !** 🛡️