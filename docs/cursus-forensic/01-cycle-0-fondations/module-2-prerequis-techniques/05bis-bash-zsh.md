---
title: 2.5 bis Bash et zsh pour analyste macOS
description: Maîtrise du shell sur macOS - zsh par défaut, bash legacy, scripting forensic, alias et fonctions, history, rc files. Outils CLI macOS pour l'investigation rapide.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - bash
  - zsh
  - macOS
  - Shell
  - Forensic
data-level: 🟡
---

# 2.5 bis Bash et zsh pour analyste macOS

!!! quote "L'analogie du dictionnaire vivant"

    Le shell est un dictionnaire vivant qui apprend de vous. Aliases, fonctions, history, configuration. Le shell d'un utilisateur expérimenté ressemble à son écriture manuscrite : unique, reconnaissable, optimisé. L'analyste forensic lit le shell d'un utilisateur compromis comme on lit son journal intime. Chaque alias custom, chaque fonction, chaque entrée d'history révèle qui était cet utilisateur et ce qu'il a fait.

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 4 heures |
| Niveau | Standard |
| Prérequis | 2.4 bis |

## 1. zsh - Shell par défaut depuis Catalina

Apple a remplacé bash par **zsh** comme shell par défaut depuis macOS Catalina (2019).

| Aspect | bash | zsh |
|---|---|---|
| Présence macOS | Présent (legacy 3.2) | Par défaut |
| Configuration | `.bashrc`, `.bash_profile` | `.zshrc`, `.zprofile` |
| History | `.bash_history` | `.zsh_history` |
| Auto-complétion | Basique | Avancée |
| Globbing étendu | Non par défaut | Oui |
| Plugins | Limité | Oh My Zsh, Prezto |

### 1.1 Vérifier le shell

```bash
echo $SHELL
echo $0           # le shell courant
which zsh
which bash
```

### 1.2 Fichiers de configuration

```text
zsh :
  /etc/zshenv         système global, toujours
  ~/.zshenv           user, toujours
  /etc/zprofile       système, login shell
  ~/.zprofile         user, login shell
  /etc/zshrc          système, interactif
  ~/.zshrc            user, interactif (le plus utilisé)
  /etc/zlogin         système, login shell après zshrc
  ~/.zlogin           user, login shell après zshrc

bash :
  /etc/profile
  ~/.bash_profile     login shell
  ~/.bashrc           interactif non-login
  ~/.profile          fallback
```

### 1.3 Ordre de chargement

```mermaid
flowchart LR
    A[Login Shell] --> B[/etc/zprofile]
    B --> C[~/.zprofile]
    C --> D[/etc/zshrc]
    D --> E[~/.zshrc]
    E --> F[/etc/zlogin]
    F --> G[~/.zlogin]
```

## 2. History - Trésor forensic

### 2.1 zsh history

```bash
# Localisation
~/.zsh_history

# Format binaire/timestamp
fc -li 1                    # avec date

# Affichage
history
history -i                  # avec timestamp

# Configuration history
echo $HISTSIZE              # taille mémoire
echo $SAVEHIST              # taille fichier
echo $HISTFILE              # chemin
```

### 2.2 Investigation forensic du history

```bash
# Toutes les commandes du dernier mois
fc -li 1 | awk -v cutoff="$(date -v-1m +%s)" '$1 > cutoff'

# Recherche commande spécifique
grep -i "ssh\|curl\|wget" ~/.zsh_history

# Commandes contenant URL
grep -E "https?://" ~/.zsh_history

# Top des commandes
cat ~/.zsh_history | sed 's/^.*;//' | awk '{print $1}' | sort | uniq -c | sort -rn | head -20
```

### 2.3 Indices forensic

| Indice | Suspicion |
|---|---|
| Commandes curl/wget vers URLs étranges | Très haute |
| Modifications `/Library/LaunchDaemons/` | Très haute |
| Édition de TCC.db | Très haute |
| `chmod 777` ou `chmod +s` | Modérée |
| `unset HISTFILE` ou `history -c` | Très haute (effacement traces) |

## 3. Outils CLI macOS spécifiques

### 3.1 Inspection système

```bash
# Modèle, puce, RAM
system_profiler SPHardwareDataType

# Version macOS détaillée
sw_vers

# Stockage
diskutil list
diskutil info disk1s1

# Réseau
ifconfig
networksetup -listallhardwareports
networksetup -getairportnetwork en0     # Wi-Fi connecté
```

### 3.2 Processus et services

```bash
# Processus
ps auxf

# launchd
launchctl list

# Login items (apps qui démarrent au login)
osascript -e 'tell application "System Events" to get name of every login item'

# Daemons et agents personnalisés
ls -la /Library/LaunchDaemons/
ls -la /Library/LaunchAgents/
ls -la ~/Library/LaunchAgents/
```

### 3.3 Logs

```bash
# Logs unifiés - tail en temps réel
log stream

# Logs récents
log show --last 1h

# Filtrer
log show --predicate 'process == "sshd"' --last 1d

# Logs anciens type syslog
cat /private/var/log/system.log
```

### 3.4 Fichiers et permissions

```bash
# Listage avec extended attributes (xattr)
ls -la@

# Voir attributs étendus (quarantine, etc.)
xattr -l fichier

# Hash
shasum -a 256 fichier
md5 fichier

# Recherche fichiers récents
find ~ -mtime -1 -type f 2>/dev/null

# Recherche par extension
find / -name "*.plist" -mtime -7 2>/dev/null
```

### 3.5 Quarantine flag

macOS marque les fichiers téléchargés avec un attribut `com.apple.quarantine` :

```bash
# Voir si fichier vient d'Internet
xattr -p com.apple.quarantine /Applications/SuspectApp.app

# Liste tous fichiers quarantaine récents
mdfind kMDItemWhereFroms

# Détails Quarantine database
sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2 \
  "SELECT datetime(LSQuarantineTimeStamp+978307200,'unixepoch') as date, \
   LSQuarantineAgentName, LSQuarantineDataURLString FROM LSQuarantineEvent \
   ORDER BY date DESC LIMIT 20;"
```

## 4. Spotlight - Recherche puissante

```bash
# Recherche fichiers
mdfind "ransomware"

# Avec contraintes
mdfind -onlyin ~ "kind:document"
mdfind "kMDItemContentType == 'public.plain-text'"

# Métadonnées d'un fichier
mdls fichier

# Recherche par date de création
mdfind "kMDItemFSCreationDate >= \$time.today(-7)"
```

## 5. Investigation rapide d'un Mac

```bash
#!/bin/bash
# Inventaire forensic rapide macOS

OUT="/tmp/macos_forensic_$(date +%Y%m%d_%H%M%S).txt"

{
echo "=== INVENTAIRE FORENSIC MACOS ==="
echo "Date: $(date -u)"
echo "Host: $(hostname)"
echo

echo "=== HARDWARE ==="
system_profiler SPHardwareDataType | grep -E "Model|Chip|Memory|Serial"

echo
echo "=== OS ==="
sw_vers

echo
echo "=== UTILISATEURS ==="
dscl . -list /Users | grep -v ^_

echo
echo "=== ADMINS ==="
dscl . -read /Groups/admin GroupMembership

echo
echo "=== DAEMONS CUSTOM ==="
ls -la /Library/LaunchDaemons/ | grep -v "^total\|^d"

echo
echo "=== AGENTS CUSTOM SYSTÈME ==="
ls -la /Library/LaunchAgents/ | grep -v "^total\|^d"

echo
echo "=== AGENTS CUSTOM USER ==="
ls -la ~/Library/LaunchAgents/ 2>/dev/null | grep -v "^total\|^d"

echo
echo "=== LOGIN ITEMS ==="
osascript -e 'tell application "System Events" to get name of every login item' 2>/dev/null

echo
echo "=== HISTORY ZSHELL (50 dernières) ==="
tail -50 ~/.zsh_history 2>/dev/null

echo
echo "=== QUARANTINE RÉCENTS ==="
sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2 \
  "SELECT datetime(LSQuarantineTimeStamp+978307200,'unixepoch'), \
   LSQuarantineAgentName, LSQuarantineDataURLString FROM LSQuarantineEvent \
   ORDER BY LSQuarantineTimeStamp DESC LIMIT 30;" 2>/dev/null

echo
echo "=== PROCESSUS ==="
ps auxf

echo
echo "=== CONNEXIONS ==="
lsof -i -P -n 2>/dev/null | head -30

echo
echo "=== FILEVAULT ==="
fdesetup status

echo
echo "=== SIP STATUS ==="
csrutil status

} > "$OUT"

echo "Rapport: $OUT"
shasum -a 256 "$OUT"
```

## 6. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Shell par défaut macOS depuis Catalina ? | zsh |
| 2 | Fichier config principal zsh ? | `~/.zshrc` |
| 3 | History zsh ? | `~/.zsh_history` |
| 4 | Outil pour logs unifiés ? | `log show` |
| 5 | Attribut fichiers téléchargés ? | `com.apple.quarantine` |
| 6 | Outil de recherche Spotlight ? | `mdfind` |
| 7 | Statut FileVault ? | `fdesetup status` |
| 8 | Statut SIP ? | `csrutil status` |

## 7. Synthèse

```text
SHELL MACOS

zsh par défaut :
  ~/.zshrc       config interactive
  ~/.zsh_history history

Outils macOS :
  system_profiler  hardware
  sw_vers          OS
  log show         logs unifiés
  mdfind           Spotlight
  xattr            attributs étendus
  fdesetup         FileVault
  csrutil          SIP

Quarantine :
  ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2

Persistance possible :
  /Library/LaunchDaemons/
  /Library/LaunchAgents/
  ~/Library/LaunchAgents/
  Login Items
```

---

**Chapitre suivant** : [2.6 Réseaux TCP/IP approfondi](02-6-reseaux.md)
