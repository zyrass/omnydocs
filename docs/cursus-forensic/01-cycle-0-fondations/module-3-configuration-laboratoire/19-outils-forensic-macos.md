---
title: 3.19 Outils forensic macOS approfondis
description: Utilisation pratique de mac_apt, AutoMacTC et autres outils sur MacBook M1. Extraction d'artefacts, parsing de logs unifiés, analyse de plists, manipulation TCC.db.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - mac_apt
  - AutoMacTC
  - macOS Forensic
  - Outils
data-level: 🔴
---

# 3.19 Outils forensic macOS approfondis

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 4 heures |
| Niveau | Pratique |
| Prérequis | 3.18 |

## 1. mac_apt - Pratique guidée

### 1.1 Liste des modules

```bash
cd ~/forensic-tools
python3 mac_apt.py --list_plugins
```

Modules principaux à connaître :

| Module | Extrait |
|---|---|
| USERS | Comptes utilisateurs |
| LAUNCHD | Daemons et agents |
| QUARANTINE | Fichiers téléchargés |
| SAFARI | Historique Safari |
| SPOTLIGHT | Cache Spotlight |
| INSTALLHISTORY | Historique installations |
| BASHHIST | Historique bash |
| ZSHHIST | Historique zsh |
| WIFI | Réseaux Wi-Fi connus |
| TCC | Permissions TCC.db |
| AUTOSTART | Tous mécanismes de démarrage |
| TIMEMACHINE | Configuration TM |
| UNIFIEDLOGS | Logs unifiés |

### 1.2 Acquisition logique préalable

Pour utiliser mac_apt sur votre M1 vivant :

```bash
# Soit sur un montage live (déconseillé strict)
sudo python3 mac_apt.py -i / -o ~/forensic-output -m MOUNTED \
    --plugins USERS,LAUNCHD,QUARANTINE,SAFARI

# Soit après création image disque
sudo asr restore --source / --target /Volumes/Backup/macm1.dmg \
    --erase --noverify
```

### 1.3 Analyse rapide

```bash
# Extraction utilisateurs et historiques
python3 mac_apt.py -i / -o output -m MOUNTED \
    --plugins USERS,BASHHIST,ZSHHIST,QUARANTINE

# Voir résultats
ls output/
# Excel et SQLite générés

sqlite3 output/mac_apt.db ".tables"
sqlite3 output/mac_apt.db "SELECT * FROM ZshHistory LIMIT 20;"
```

## 2. AutoMacTC - Triage rapide

### 2.1 Lancement

```bash
cd ~/forensic-tools/automactc

# Triage complet (peut prendre 10-30 min)
sudo python3 automactc.py -m all -o output/

# Modules ciblés rapides
sudo python3 automactc.py \
    -m users,bash,quarantines,wifi,asl,coreanalytics \
    -o output/

# Modules disponibles
python3 automactc.py --list_modules
```

### 2.2 Sortie

| Fichier | Contenu |
|---|---|
| `users.csv` | Comptes |
| `bash.csv` | Historique bash |
| `quarantines.csv` | Téléchargements |
| `wifi.csv` | Réseaux Wi-Fi |
| `asl.csv` | Logs ASL |
| `eventtaps.csv` | Hooks clavier (suspects) |

## 3. Manipulation TCC.db

### 3.1 Lecture

```bash
# TCC niveau utilisateur
sqlite3 ~/Library/Application\ Support/com.apple.TCC/TCC.db "SELECT service, client, auth_value FROM access;"

# TCC niveau système (nécessite Full Disk Access)
sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "SELECT service, client, auth_value FROM access;"
```

### 3.2 Interprétation auth_value

| Valeur | Signification |
|---|---|
| 0 | Refusé |
| 2 | Autorisé |

### 3.3 Services TCC notables

| Service | Permission |
|---|---|
| kTCCServiceMicrophone | Microphone |
| kTCCServiceCamera | Caméra |
| kTCCServiceScreenCapture | Capture écran |
| kTCCServiceAccessibility | Accessibilité (très puissant) |
| kTCCServiceSystemPolicyAllFiles | Full Disk Access |
| kTCCServicePostEvent | Synthétiser événements clavier/souris |

## 4. Logs unifiés - Analyses

### 4.1 Recherches forensic typiques

```bash
# Logons SSH
log show --predicate 'process == "sshd"' --last 30d --info

# Tentatives sudo
log show --predicate 'process == "sudo"' --last 7d

# Modifications launchd
log show --predicate 'subsystem == "com.apple.xpc.launchd"' --last 7d

# Activité réseau processus suspect
log show --predicate 'process == "suspect_app"' --last 1d --info

# Lancements applications
log show --predicate 'subsystem == "com.apple.launchservices" AND eventMessage contains "LAUNCH"' --last 1d
```

### 4.2 Format JSON pour traitement

```bash
log show --last 1h --style json > logs.json

# Extraction avec jq
jq '.[] | select(.process == "sshd")' logs.json
```

## 5. Plists - Analyse

```bash
# Convertir tous plists binaires en XML
find ~/Library -name "*.plist" -exec plutil -convert xml1 -o - {} \;

# Cibler launchd
ls ~/Library/LaunchAgents/ /Library/LaunchAgents/ /Library/LaunchDaemons/ 2>/dev/null

for f in ~/Library/LaunchAgents/*.plist; do
    echo "=== $f ==="
    plutil -p "$f"
done
```

## 6. Spotlight - Source précieuse

```bash
# Recherche fichiers récents
mdfind -onlyin ~ "kMDItemFSCreationDate >= \$time.today(-30)" | head -30

# Métadonnées d'un fichier
mdls ~/Documents/CasFictifs/fiscalite_2025.pdf

# Retrouver d'où vient un fichier
mdfind kMDItemWhereFroms

# Apps utilisées récemment
mdfind "kMDItemContentType == 'com.apple.application-bundle'" \
    -attr kMDItemLastUsedDate
```

## 7. Quarantine et signatures

### 7.1 Vérifier signatures applications

```bash
# Toutes apps
for app in /Applications/*.app; do
    if codesign -dvv "$app" 2>&1 | grep -q "Authority"; then
        echo "[SIGNED] $app"
    else
        echo "[UNSIGNED] $app"
    fi
done
```

### 7.2 Quarantine database

```bash
# Lire DB quarantine (appartient au user)
sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2 \
    "SELECT datetime(LSQuarantineTimeStamp+978307200,'unixepoch'),
            LSQuarantineAgentName,
            LSQuarantineDataURLString
     FROM LSQuarantineEvent
     ORDER BY LSQuarantineTimeStamp DESC LIMIT 50;"
```

## 8. Script triage complet

```bash
cat > ~/forensic-tools/triage-mac.sh <<'EOF'
#!/bin/bash
# Triage rapide Mac - 5 minutes

OUT="/tmp/triage-$(hostname)-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"

echo "Triage en cours dans $OUT"

# Système
sw_vers > "$OUT/sw_vers.txt"
system_profiler SPHardwareDataType > "$OUT/hardware.txt"
csrutil status > "$OUT/csrutil.txt"
fdesetup status > "$OUT/filevault.txt"

# Utilisateurs
dscl . -list /Users > "$OUT/users.txt"
dscl . -read /Groups/admin GroupMembership > "$OUT/admins.txt"

# Persistance
ls -la /Library/LaunchDaemons/ > "$OUT/launch_daemons.txt" 2>/dev/null
ls -la /Library/LaunchAgents/ > "$OUT/launch_agents_system.txt" 2>/dev/null
ls -la ~/Library/LaunchAgents/ > "$OUT/launch_agents_user.txt" 2>/dev/null

# Login items
osascript -e 'tell application "System Events" to get name of every login item' > "$OUT/login_items.txt" 2>/dev/null

# Processus
ps auxf > "$OUT/processes.txt"
launchctl list > "$OUT/launchctl.txt"

# Réseau
lsof -i -P -n > "$OUT/connections.txt" 2>/dev/null
netstat -an > "$OUT/netstat.txt"

# Histories
cp ~/.zsh_history "$OUT/zsh_history.txt" 2>/dev/null
cp ~/.bash_history "$OUT/bash_history.txt" 2>/dev/null

# Quarantine
sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2 \
    "SELECT datetime(LSQuarantineTimeStamp+978307200,'unixepoch'), 
     LSQuarantineAgentName, LSQuarantineDataURLString 
     FROM LSQuarantineEvent ORDER BY LSQuarantineTimeStamp DESC LIMIT 100;" \
    > "$OUT/quarantine.txt" 2>/dev/null

# Hash global
cd "$OUT"
shasum -a 256 * > MANIFEST.sha256
cd -

echo "Triage terminé : $OUT"
echo "Hash MANIFEST: $(shasum -a 256 $OUT/MANIFEST.sha256)"
EOF

chmod +x ~/forensic-tools/triage-mac.sh
```

---

**Chapitre suivant** : [3.20 Mode Recovery et DFU Apple Silicon](03-20-recovery-dfu-apple-silicon.md)
