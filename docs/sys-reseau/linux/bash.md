---
description: "Bash : shell scripting fondamentaux, automatisation, scripting production, best practices"
icon: lucide/book-open-check
tags: ["BASH", "SHELL", "SCRIPTING", "LINUX", "AUTOMATION", "DEVOPS"]
---

# Bash

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-time="8-10 heures"
  data-version="1.0">
</div>

## Introduction aux Fondamentaux du Scripting

!!! quote "Analogie pédagogique"
    _Imaginez un **chef orchestre symphonique dirigeant 100+ musiciens instruments différents avec partition complexe synchronisation précise** : Bash fonctionne comme **langage coordination orchestrant TOUS outils système Linux (commandes = musiciens) selon script précis (partition) exécution automatisée**. **Chef orchestre concert** : partition musicale complète (script bash détaillé), baguette direction précise (commandes shell), coordination sections orchestre (pipes entre commandes), tempo synchronisé (boucles/conditions), crescendo/decrescendo dynamique (variables/logique), répétitions mémorisées (fonctions réutilisables), gestion erreurs (si musicien rate note = error handling), improvisation encadrée (paramètres flexibles). **Sans Bash scripting** : tâches répétitives manuelles (backup quotidien = 50 commandes manuelles), erreurs humaines (oubli étape critique), temps perdu (monitoring serveurs = vérifier manuellement chaque jour), non-reproductible (collègue absent = procédure perdue), non-scalable (10 serveurs OK, 100 serveurs impossible manuellement). **Avec Bash scripting** : **Automatisation complète** (cron job exécute backup 3h matin automatiquement), **Reproductibilité garantie** (même script = même résultat toujours), **Error handling robuste** (si backup échoue = email alert + retry + log détaillé), **Scalabilité** (script gère 1000 serveurs aussi facilement que 1), **Documentation vivante** (script = procédure exécutable commentée), **Composition puissante** (combiner 50+ outils Unix via pipes/redirections), **Portabilité** (bash présent TOUS systèmes Unix/Linux). **Bash = langage glue système** : colle ensemble coreutils (ls, cp, grep, awk, sed), network tools (curl, wget, ssh), monitoring (ps, top, netstat), file processing (tar, gzip, find), text manipulation (cut, tr, sort, uniq). **Architecture script production** : Shebang (#!/bin/bash), Variables configuration, Fonctions modulaires, Logging structuré, Error handling (set -euo pipefail), Arguments parsing (getopts), Exit codes standards, Comments documentation. **Use cases production réels** : backup automatisés (databases, files, configurations), monitoring serveurs (CPU/RAM/disk alerts), deployment scripts (CI/CD pipelines), log rotation/analysis (parse millions lignes), user provisioning (création comptes/permissions), security audits (scan configurations), data processing (ETL pipelines), incident response (automated remediation). **Bash = standard DevOps/SRE** : utilisé Google SRE, Amazon AWS CLI backends, Kubernetes operators, Docker entrypoints, Ansible modules, Terraform providers, 99% infrastructure automation mondiale. **Puissance Bash** : 40+ ans développement (depuis 1989 Brian Fox GNU), rétrocompatible sh POSIX, intégré TOUS Linux/Unix/macOS, syntaxe concise expressive, écosystème outils mature, performance native (pas interpréteur lourd), debugging facilité (bash -x), communauté massive._

**Bash en résumé :**

- ✅ **Shell standard** = Présent tous systèmes Linux/Unix/macOS
- ✅ **Automatisation** = Scripts reproductibles, schedules cron
- ✅ **Composition** = Pipes, redirections, command substitution
- ✅ **Variables** = Strings, arrays, associative arrays, environnement
- ✅ **Contrôle flux** = if/else, case, for/while loops
- ✅ **Fonctions** = Code modulaire réutilisable
- ✅ **I/O robuste** = Redirections, here-documents, process substitution
- ✅ **Production-ready** = Error handling, logging, exit codes

**Guide structure :**

1. Introduction et concepts shell
2. Variables et expansion
3. Structures de contrôle
4. Fonctions et modularité
5. Manipulation strings et arrays
6. Redirections et pipes
7. Expressions régulières et text processing
8. Arguments et options (getopts)
9. Debugging et error handling
10. Process management et signals
11. Best practices et sécurité
12. Cas pratiques production

---

## Section 1 : Introduction et Concepts

### 1.1 Qu'est-ce que Bash ?

**Bash = Bourne Again SHell, interpréteur commandes Unix/Linux**

```
Historique shells Unix :

1971 : Thompson shell (sh) - Ken Thompson, Unix V1
1977 : Bourne shell (sh) - Stephen Bourne, Unix V7
1978 : C shell (csh) - Bill Joy, BSD Unix
1983 : Korn shell (ksh) - David Korn, AT&T
1989 : Bash (bash) - Brian Fox, GNU Project ⭐
2001 : Z shell (zsh) - Paul Falstad

Bash = Bourne Again SHell
├─ Rétrocompatible Bourne shell (sh)
├─ Features C shell (csh) et Korn shell (ksh)
├─ Extensions GNU (arrays, arithmetic, etc.)
└─ Standard Linux/Unix moderne

Versions Bash :
- Bash 3.x : macOS (old, license GPL v2)
- Bash 4.x : Linux standard (GPL v3, features avancées)
- Bash 5.x : Latest (2019+, associative arrays, etc.)
```

**Shell vs Script :**

```
Mode interactif (shell) :
$ ls -la
$ cd /var/log
$ grep "error" syslog
→ Commandes tapées manuellement terminal

Mode script (bash script) :
#!/bin/bash
# backup.sh - Automated backup script

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d)

tar -czf "$BACKUP_DIR/backup-$DATE.tar.gz" /var/www
echo "Backup completed: $BACKUP_DIR/backup-$DATE.tar.gz"
→ Commandes dans fichier exécutable automatiquement
```

### 1.2 Anatomie Script Bash

```bash
#!/bin/bash
# ^^^ Shebang : indique interpréteur à utiliser

# Script : example.sh
# Description : Example bash script structure
# Author : SysAdmin Team
# Date : 2024-01-16
# Version : 1.0

# === CONFIGURATION ===
# Variables globales configuration
SCRIPT_NAME=$(basename "$0")
SCRIPT_DIR=$(dirname "$0")
LOG_FILE="/var/log/${SCRIPT_NAME%.sh}.log"

# === FONCTIONS ===
# Fonctions réutilisables

# Log message avec timestamp
log() {
    local level="$1"
    shift
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

# Main logic function
main() {
    log "INFO" "Script started"
    
    # Votre logique ici
    
    log "INFO" "Script completed"
}

# === EXECUTION ===
# Point entrée script

# Vérifier si root (si requis)
if [[ $EUID -ne 0 ]]; then
    log "ERROR" "This script must be run as root"
    exit 1
fi

# Exécuter fonction principale
main "$@"

# Exit code (0 = success)
exit 0
```

**Composants essentiels :**

```
1. Shebang (#!)
   #!/bin/bash          → Utilise bash
   #!/bin/sh            → Utilise sh (POSIX)
   #!/usr/bin/env bash  → Trouve bash dans PATH (portable)

2. Comments (#)
   # Commentaire une ligne
   : '
   Commentaire
   multi-lignes
   '

3. Variables
   NAME="value"         → String
   COUNT=42             → Number (stored as string)
   ARRAY=(a b c)        → Array

4. Structures contrôle
   if/then/else/fi
   case/esac
   for/while/until

5. Fonctions
   function_name() {
       # code
   }

6. Exit codes
   exit 0               → Success
   exit 1               → Error
   $?                   → Last command exit code
```

### 1.3 Premier Script

```bash
#!/bin/bash
# hello.sh - Premier script Bash

# Afficher message
echo "Hello, World!"

# Demander nom utilisateur
read -p "What is your name? " NAME

# Message personnalisé
echo "Hello, $NAME!"

# Informations système
echo ""
echo "System information:"
echo "  Hostname: $(hostname)"
echo "  User: $(whoami)"
echo "  Date: $(date)"
echo "  Uptime: $(uptime -p)"

# Exécution :
# chmod +x hello.sh
# ./hello.sh

# Output :
# Hello, World!
# What is your name? John
# Hello, John!
# 
# System information:
#   Hostname: server01
#   User: admin
#   Date: Tue Jan 16 14:30:45 UTC 2024
#   Uptime: up 5 days, 3 hours, 22 minutes
```

### 1.4 Exécution Scripts

```bash
# Méthode 1 : Executable direct (shebang)
chmod +x script.sh
./script.sh

# Méthode 2 : Interpréteur explicite
bash script.sh
sh script.sh

# Méthode 3 : Source (exécute dans shell actuel)
source script.sh
. script.sh

# Méthode 4 : Inline
bash -c 'echo "Hello"'

# Différence source vs execution :
# Execution (./script.sh) :
# - Crée sub-shell
# - Variables pas disponibles après
# - cd dans script n'affecte pas shell parent

# Source (source script.sh) :
# - Exécute dans shell actuel
# - Variables persistent
# - cd affecte shell actuel
# - Utile pour charger configuration

# Exemple :
# config.sh
export DB_HOST="localhost"
export DB_USER="admin"

# Usage :
source config.sh
echo $DB_HOST  # localhost (disponible)

# vs
./config.sh
echo $DB_HOST  # vide (pas disponible)
```

---

## Section 2 : Variables et Expansion

### 2.1 Déclaration Variables

```bash
# Syntaxe : NAME=value (PAS d'espaces autour =)

# String
NAME="John Doe"
MESSAGE='Single quotes: no expansion'

# Number (stocké comme string)
COUNT=42
PRICE=19.99

# Command substitution
CURRENT_DATE=$(date +%Y-%m-%d)
USER_COUNT=$(wc -l < /etc/passwd)

# Arithmetic
RESULT=$((5 + 3))
((COUNTER++))

# Read-only (constant)
readonly PI=3.14159
declare -r MAX_USERS=100

# Arrays
FRUITS=("apple" "banana" "cherry")
declare -a NUMBERS=(1 2 3 4 5)

# Associative arrays (Bash 4+)
declare -A CONFIG
CONFIG[host]="localhost"
CONFIG[port]=3306

# Environment variables (export = disponible sub-processes)
export PATH="/usr/local/bin:$PATH"
export DATABASE_URL="postgres://localhost/mydb"

# Local variables (fonctions seulement)
function example() {
    local temp="temporary value"
    echo "$temp"
}
```

**Conventions nommage :**

```bash
# UPPER_CASE : Variables environnement/constantes
export MAX_CONNECTIONS=100
readonly DATABASE_NAME="production"

# lower_case : Variables locales scripts
user_input="test"
file_count=5

# Éviter noms conflits avec commandes
# ❌ test="value"  (conflit avec commande test)
# ✅ test_value="value"

# Éviter noms variables shell spéciales
# ❌ PATH="..."    (écrase PATH système)
# ✅ MY_PATH="..."

# Préfixer variables projet
APP_NAME="myapp"
APP_VERSION="1.0"
APP_CONFIG_DIR="/etc/myapp"
```

### 2.2 Expansion Variables

```bash
# Basic expansion
NAME="John"
echo "Hello $NAME"              # Hello John
echo "Hello ${NAME}"            # Hello John (explicite, recommandé)

# Protéger expansion (quotes)
echo "Value: $NAME"             # Value: John
echo 'Value: $NAME'             # Value: $NAME (littéral)

# Expansion avec default value
echo "${UNDEFINED:-default}"    # default (si UNDEFINED vide/unset)
echo "${UNDEFINED:=default}"    # default (et assigne UNDEFINED=default)
echo "${UNDEFINED:?Error msg}"  # Affiche erreur si unset
echo "${DEFINED:+alternate}"    # alternate si DEFINED non-vide

# String manipulation
FILE="/path/to/file.txt"

# Longueur
echo "${#FILE}"                 # 18

# Substring
echo "${FILE:0:5}"              # /path
echo "${FILE:9}"                # file.txt

# Remove prefix/suffix
echo "${FILE#*/}"               # path/to/file.txt (remove shortest /)
echo "${FILE##*/}"              # file.txt (remove longest /)
echo "${FILE%.*}"               # /path/to/file (remove shortest .ext)
echo "${FILE%%.*}"              # /path/to/file (remove longest .ext)

# Replace
echo "${FILE/file/document}"    # /path/to/document.txt (first)
echo "${FILE//o/O}"             # /path/tO/file.txt (all)

# Case modification (Bash 4+)
NAME="john doe"
echo "${NAME^}"                 # John doe (first char upper)
echo "${NAME^^}"                # JOHN DOE (all upper)
echo "${NAME,}"                 # john doe (first char lower)
echo "${NAME,,}"                # john doe (all lower)

# Array expansion
FRUITS=("apple" "banana" "cherry")
echo "${FRUITS[@]}"             # apple banana cherry (all elements)
echo "${FRUITS[0]}"             # apple (first element)
echo "${#FRUITS[@]}"            # 3 (array length)
echo "${FRUITS[@]:1:2}"         # banana cherry (slice)
```

### 2.3 Variables Spéciales

```bash
# Paramètres positionnels
$0      # Nom script
$1-$9   # Arguments 1 à 9
${10}   # Argument 10+ (brackets requis)
$#      # Nombre arguments
$@      # Tous arguments (séparés)
$*      # Tous arguments (string unique)

# Exemple :
# script.sh arg1 arg2 arg3
echo "Script: $0"           # script.sh
echo "First arg: $1"        # arg1
echo "All args: $@"         # arg1 arg2 arg3
echo "Arg count: $#"        # 3

# Process IDs
$$      # PID script actuel
$!      # PID dernier background process
$PPID   # PID parent process

# Exit codes
$?      # Exit code dernière commande

# Exemple :
ls /existing
echo $?                     # 0 (success)

ls /nonexistent
echo $?                     # 2 (error)

# Other special
$-      # Current shell options
$_      # Last argument dernière commande
```

### 2.4 Arrays

```bash
# Indexed arrays (index numérique)
FRUITS=("apple" "banana" "cherry")

# Déclaration explicite
declare -a NUMBERS
NUMBERS=(1 2 3 4 5)

# Assignment individuel
COLORS[0]="red"
COLORS[1]="green"
COLORS[2]="blue"

# Append
FRUITS+=("date")
FRUITS[${#FRUITS[@]}]="elderberry"

# Access
echo "${FRUITS[0]}"         # apple
echo "${FRUITS[@]}"         # tous éléments
echo "${FRUITS[*]}"         # tous (string)
echo "${#FRUITS[@]}"        # length (4)

# Iteration
for fruit in "${FRUITS[@]}"; do
    echo "$fruit"
done

# Indices
echo "${!FRUITS[@]}"        # 0 1 2 3

# Slice
echo "${FRUITS[@]:1:2}"     # banana cherry

# Associative arrays (Bash 4+, comme dict/hash)
declare -A CONFIG
CONFIG["host"]="localhost"
CONFIG["port"]=3306
CONFIG["user"]="admin"

# Access
echo "${CONFIG[host]}"      # localhost

# Keys
echo "${!CONFIG[@]}"        # host port user

# Iteration
for key in "${!CONFIG[@]}"; do
    echo "$key = ${CONFIG[$key]}"
done

# Example: counting words
declare -A word_count
for word in $(cat file.txt); do
    ((word_count[$word]++))
done

for word in "${!word_count[@]}"; do
    echo "$word: ${word_count[$word]}"
done
```

---

## Section 3 : Structures de Contrôle

### 3.1 Conditions (if/else)

```bash
# Syntaxe if
if [[ condition ]]; then
    # commands
elif [[ condition ]]; then
    # commands
else
    # commands
fi

# Tests fichiers
if [[ -f "/etc/passwd" ]]; then
    echo "File exists"
fi

if [[ -d "/var/log" ]]; then
    echo "Directory exists"
fi

if [[ -r "/etc/shadow" ]]; then
    echo "File readable"
fi

# Opérateurs fichiers
-e FILE     # Exists
-f FILE     # Regular file
-d FILE     # Directory
-L FILE     # Symbolic link
-r FILE     # Readable
-w FILE     # Writable
-x FILE     # Executable
-s FILE     # Non-empty (size > 0)
-N FILE     # Modified since last read

# Comparaisons files
FILE1 -nt FILE2    # FILE1 newer than FILE2
FILE1 -ot FILE2    # FILE1 older than FILE2
FILE1 -ef FILE2    # Same file (hard links)

# Tests strings
if [[ -z "$VAR" ]]; then
    echo "String empty"
fi

if [[ -n "$VAR" ]]; then
    echo "String not empty"
fi

if [[ "$VAR1" == "$VAR2" ]]; then
    echo "Strings equal"
fi

if [[ "$VAR" =~ ^[0-9]+$ ]]; then
    echo "String is number"
fi

# Opérateurs strings
-z STRING       # Empty
-n STRING       # Not empty
STR1 == STR2    # Equal
STR1 != STR2    # Not equal
STR1 < STR2     # Less than (lexicographic)
STR1 > STR2     # Greater than
STR =~ REGEX    # Regex match

# Comparaisons numériques
NUM1 -eq NUM2   # Equal
NUM1 -ne NUM2   # Not equal
NUM1 -lt NUM2   # Less than
NUM1 -le NUM2   # Less or equal
NUM1 -gt NUM2   # Greater than
NUM1 -ge NUM2   # Greater or equal

# Exemple :
if [[ $COUNT -gt 10 ]]; then
    echo "Count greater than 10"
fi

# Opérateurs logiques
if [[ -f "file.txt" && -r "file.txt" ]]; then
    echo "File exists and readable"
fi

if [[ "$USER" == "root" || "$EUID" -eq 0 ]]; then
    echo "Running as root"
fi

if [[ ! -f "missing.txt" ]]; then
    echo "File does not exist"
fi

# Exemples pratiques
# Check root
if [[ $EUID -ne 0 ]]; then
    echo "ERROR: Must run as root" >&2
    exit 1
fi

# Check command exists
if ! command -v docker &>/dev/null; then
    echo "ERROR: docker not installed"
    exit 1
fi

# Check argument
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Check file not empty
if [[ ! -s "data.txt" ]]; then
    echo "ERROR: data.txt is empty"
    exit 1
fi

# Ternary-like (avec &&/||)
[[ -f "file.txt" ]] && echo "Found" || echo "Not found"

# Note : [[ ]] vs [ ]
# [[ ]] : Bash keyword (recommended)
#   - Pas de word splitting
#   - Pattern matching
#   - Regex support
# [ ] : POSIX command
#   - Nécessite quotes
#   - Plus compatible mais limité
```

### 3.2 Case Statement

```bash
# Syntaxe case
case "$VARIABLE" in
    pattern1)
        # commands
        ;;
    pattern2|pattern3)
        # commands
        ;;
    *)
        # default
        ;;
esac

# Exemple : menu
read -p "Choose option (a/b/c): " CHOICE

case "$CHOICE" in
    a|A)
        echo "Option A selected"
        ;;
    b|B)
        echo "Option B selected"
        ;;
    c|C)
        echo "Option C selected"
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

# Exemple : file extension
FILE="document.pdf"

case "$FILE" in
    *.txt)
        echo "Text file"
        ;;
    *.pdf)
        echo "PDF file"
        ;;
    *.jpg|*.png|*.gif)
        echo "Image file"
        ;;
    *)
        echo "Unknown file type"
        ;;
esac

# Exemple : command-line options
case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        start_service
        ;;
    status)
        check_status
        ;;
    --help|-h)
        show_help
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

# Patterns avancés
case "$VAR" in
    [0-9])              # Single digit
        ;;
    [0-9][0-9])         # Two digits
        ;;
    [a-zA-Z]*)          # Starts with letter
        ;;
    *[!0-9]*)           # Contains non-digit
        ;;
esac
```

### 3.3 Loops (for/while/until)

```bash
# For loop - list
for item in apple banana cherry; do
    echo "$item"
done

# For loop - range
for i in {1..10}; do
    echo "Number: $i"
done

# For loop - range avec step
for i in {0..100..10}; do
    echo "$i"
done
# Output : 0 10 20 30 ... 100

# For loop - array
FRUITS=("apple" "banana" "cherry")
for fruit in "${FRUITS[@]}"; do
    echo "$fruit"
done

# For loop - command output
for file in $(ls *.txt); do
    echo "Processing: $file"
done

# For loop - C-style
for ((i=0; i<10; i++)); do
    echo "Count: $i"
done

# While loop
COUNT=1
while [[ $COUNT -le 5 ]]; do
    echo "Count: $COUNT"
    ((COUNT++))
done

# While - read file
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt

# While - infinite loop (daemon)
while true; do
    check_status
    sleep 60
done

# Until loop (inverse while)
COUNT=1
until [[ $COUNT -gt 5 ]]; do
    echo "Count: $COUNT"
    ((COUNT++))
done

# Break et continue
for i in {1..10}; do
    if [[ $i -eq 5 ]]; then
        continue  # Skip 5
    fi
    
    if [[ $i -eq 8 ]]; then
        break  # Stop at 8
    fi
    
    echo "$i"
done
# Output : 1 2 3 4 6 7

# Nested loops
for i in {1..3}; do
    for j in {a..c}; do
        echo "$i$j"
    done
done
# Output : 1a 1b 1c 2a 2b 2c 3a 3b 3c

# Loop avec index
ITEMS=("apple" "banana" "cherry")
for i in "${!ITEMS[@]}"; do
    echo "Item $i: ${ITEMS[$i]}"
done
# Output :
# Item 0: apple
# Item 1: banana
# Item 2: cherry
```

---

## Section 4 : Fonctions et Modularité

### 4.1 Déclaration Fonctions

```bash
# Syntaxe 1 (POSIX)
function_name() {
    # commands
}

# Syntaxe 2 (Bash)
function function_name {
    # commands
}

# Syntaxe 3 (Bash, explicite)
function function_name() {
    # commands
}

# Exemple simple
greet() {
    echo "Hello, World!"
}

# Appeler fonction
greet

# Fonction avec arguments
greet_user() {
    local name="$1"
    echo "Hello, $name!"
}

greet_user "John"
# Output : Hello, John!

# Arguments multiples
add() {
    local num1="$1"
    local num2="$2"
    local result=$((num1 + num2))
    echo "$result"
}

result=$(add 5 3)
echo "Result: $result"
# Output : Result: 8

# Return value (exit code seulement)
is_even() {
    local num="$1"
    if [[ $((num % 2)) -eq 0 ]]; then
        return 0  # true
    else
        return 1  # false
    fi
}

if is_even 4; then
    echo "Even"
fi

# Return string (via echo + command substitution)
get_date() {
    echo "$(date +%Y-%m-%d)"
}

current_date=$(get_date)
echo "Date: $current_date"
```

### 4.2 Variables Locales

```bash
# local : variable locale fonction (Bash)
# Sans local : variable globale

global_var="global"

test_scope() {
    local local_var="local"
    global_var="modified"
    
    echo "Inside function:"
    echo "  local_var: $local_var"
    echo "  global_var: $global_var"
}

echo "Before function:"
echo "  global_var: $global_var"
# echo "  local_var: $local_var"  # Undefined

test_scope

echo "After function:"
echo "  global_var: $global_var"  # modified
# echo "  local_var: $local_var"  # Still undefined

# Best practice : TOUJOURS utiliser local dans fonctions
calculate() {
    local input="$1"
    local result=$((input * 2))
    echo "$result"
}
```

### 4.3 Fonctions Avancées

```bash
# Arguments par défaut
greet() {
    local name="${1:-World}"  # Default "World" si $1 vide
    echo "Hello, $name!"
}

greet          # Hello, World!
greet "John"   # Hello, John!

# Arguments variables (comme *args Python)
sum_all() {
    local total=0
    for num in "$@"; do
        ((total += num))
    done
    echo "$total"
}

result=$(sum_all 1 2 3 4 5)
echo "Sum: $result"  # Sum: 15

# Récursion
factorial() {
    local n="$1"
    if [[ $n -le 1 ]]; then
        echo 1
    else
        local prev=$(factorial $((n - 1)))
        echo $((n * prev))
    fi
}

result=$(factorial 5)
echo "5! = $result"  # 5! = 120

# Fonction retourne multiple values (via variables globales)
get_user_info() {
    local username="$1"
    
    # Simulate getting user info
    USER_FULL_NAME="John Doe"
    USER_EMAIL="john@example.com"
    USER_ID=1001
}

get_user_info "john"
echo "Name: $USER_FULL_NAME"
echo "Email: $USER_EMAIL"
echo "ID: $USER_ID"

# Ou via echo multiple lines
get_system_info() {
    echo "$(hostname)"
    echo "$(uname -r)"
    echo "$(uptime -p)"
}

IFS=$'\n' read -r -d '' HOSTNAME KERNEL UPTIME < <(get_system_info && printf '\0')
echo "Host: $HOSTNAME"
echo "Kernel: $KERNEL"
echo "Uptime: $UPTIME"
```

### 4.4 Librairies et Sourcing

```bash
# Créer librairie fonctions réutilisables
# lib/utils.sh

#!/bin/bash
# utils.sh - Utility functions library

# Log with timestamp
log() {
    local level="$1"
    shift
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*"
}

# Check if command exists
command_exists() {
    command -v "$1" &>/dev/null
}

# Check if running as root
require_root() {
    if [[ $EUID -ne 0 ]]; then
        log "ERROR" "This script must be run as root"
        exit 1
    fi
}

# Confirm action
confirm() {
    local message="$1"
    read -p "$message (y/n): " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

# Retry command with exponential backoff
retry() {
    local max_attempts="$1"
    shift
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if "$@"; then
            return 0
        fi
        
        log "WARN" "Attempt $attempt failed, retrying..."
        sleep $((2 ** attempt))
        ((attempt++))
    done
    
    log "ERROR" "All $max_attempts attempts failed"
    return 1
}

# Utiliser librairie
# main-script.sh

#!/bin/bash
# Source library
source "$(dirname "$0")/lib/utils.sh"

# Utiliser fonctions
log "INFO" "Script started"

if ! command_exists docker; then
    log "ERROR" "Docker not installed"
    exit 1
fi

if confirm "Continue with operation?"; then
    log "INFO" "Proceeding..."
else
    log "INFO" "Cancelled"
    exit 0
fi

# Retry operation
if retry 3 curl -sSf https://example.com; then
    log "INFO" "Success"
else
    log "ERROR" "Failed after retries"
fi
```

---

## Section 5 : Manipulation Strings et Arrays

### 5.1 String Operations

```bash
# Concatenation
first="Hello"
last="World"
full="$first $last"         # Hello World
full="${first}, ${last}!"   # Hello, World!

# Length
text="Hello"
echo "${#text}"             # 5

# Substring extraction
text="Hello World"
echo "${text:0:5}"          # Hello
echo "${text:6}"            # World
echo "${text: -5}"          # World (space important)

# Find and replace
text="Hello World"
echo "${text/World/Universe}"       # Hello Universe (first)
echo "${text//o/0}"                 # Hell0 W0rld (all)

# Remove prefix
path="/usr/local/bin/script.sh"
echo "${path#*/}"           # usr/local/bin/script.sh (shortest)
echo "${path##*/}"          # script.sh (longest)

# Remove suffix
filename="document.tar.gz"
echo "${filename%.*}"       # document.tar (shortest)
echo "${filename%%.*}"      # document (longest)

# Case conversion (Bash 4+)
text="Hello World"
echo "${text^}"             # Hello World (first char)
echo "${text^^}"            # HELLO WORLD (all upper)
echo "${text,}"             # hello World (first lower)
echo "${text,,}"            # hello world (all lower)

# Default values
echo "${UNDEFINED:-default}"        # default (si vide/unset)
echo "${UNDEFINED:=assign}"         # assign (et assigne)
echo "${DEFINED:+alternate}"        # alternate (si défini)
echo "${UNDEFINED:?Error message}"  # Exit avec erreur si unset

# Trim whitespace
trim() {
    local var="$1"
    var="${var#"${var%%[![:space:]]*}"}"  # trim leading
    var="${var%"${var##*[![:space:]]}"}"  # trim trailing
    echo "$var"
}

text="   Hello World   "
echo "$(trim "$text")"      # Hello World

# Split string
IFS=',' read -ra PARTS <<< "apple,banana,cherry"
for part in "${PARTS[@]}"; do
    echo "$part"
done
# Output :
# apple
# banana
# cherry

# Join array
ITEMS=("apple" "banana" "cherry")
JOINED=$(IFS=,; echo "${ITEMS[*]}")
echo "$JOINED"              # apple,banana,cherry
```

### 5.2 Array Operations

```bash
# Create array
FRUITS=("apple" "banana" "cherry")

# Access elements
echo "${FRUITS[0]}"         # apple
echo "${FRUITS[1]}"         # banana
echo "${FRUITS[-1]}"        # cherry (last)

# All elements
echo "${FRUITS[@]}"         # apple banana cherry
echo "${FRUITS[*]}"         # apple banana cherry

# Array length
echo "${#FRUITS[@]}"        # 3

# Append
FRUITS+=("date")
FRUITS[${#FRUITS[@]}]="elderberry"

# Prepend
FRUITS=("zero" "${FRUITS[@]}")

# Insert at position
FRUITS=("${FRUITS[@]:0:2}" "new" "${FRUITS[@]:2}")

# Remove element
unset 'FRUITS[1]'           # Remove index 1

# Slice
echo "${FRUITS[@]:1:2}"     # Elements 1-2
echo "${FRUITS[@]:2}"       # From index 2 to end

# Loop with index
for i in "${!FRUITS[@]}"; do
    echo "Index $i: ${FRUITS[$i]}"
done

# Check if element exists
if [[ " ${FRUITS[@]} " =~ " apple " ]]; then
    echo "Found apple"
fi

# Sort array
IFS=$'\n' SORTED=($(sort <<<"${FRUITS[*]}"))
unset IFS

# Reverse array
REVERSE=()
for ((i=${#FRUITS[@]}-1; i>=0; i--)); do
    REVERSE+=("${FRUITS[$i]}")
done

# Remove duplicates
declare -A seen
UNIQUE=()
for item in "${FRUITS[@]}"; do
    if [[ -z ${seen[$item]} ]]; then
        UNIQUE+=("$item")
        seen[$item]=1
    fi
done

# Array from command output
FILES=($(ls *.txt))
LINES=($(cat file.txt))

# Read file into array
mapfile -t LINES < file.txt
# ou
readarray -t LINES < file.txt
```

### 5.3 Associative Arrays

```bash
# Bash 4+ only
declare -A CONFIG

# Assignment
CONFIG["host"]="localhost"
CONFIG["port"]=3306
CONFIG["user"]="admin"
CONFIG["password"]="secret"

# Access
echo "${CONFIG[host]}"      # localhost

# All keys
echo "${!CONFIG[@]}"        # host port user password

# All values
echo "${CONFIG[@]}"         # localhost 3306 admin secret

# Check key exists
if [[ -v CONFIG[host] ]]; then
    echo "Host is set: ${CONFIG[host]}"
fi

# Iterate
for key in "${!CONFIG[@]}"; do
    echo "$key = ${CONFIG[$key]}"
done

# Remove key
unset 'CONFIG[password]'

# Count
echo "${#CONFIG[@]}"        # 3 (after removing password)

# Example: counting words
declare -A word_count

while read -r line; do
    for word in $line; do
        ((word_count[$word]++))
    done
done < file.txt

# Display sorted by count
for word in "${!word_count[@]}"; do
    echo "${word_count[$word]} $word"
done | sort -rn

# Example: configuration parser
declare -A CONFIG

while IFS='=' read -r key value; do
    # Skip comments and empty lines
    [[ $key =~ ^[[:space:]]*# ]] && continue
    [[ -z $key ]] && continue
    
    # Trim whitespace
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)
    
    CONFIG[$key]="$value"
done < config.ini

echo "Database: ${CONFIG[database]}"
echo "Port: ${CONFIG[port]}"
```

---

## Section 6 : Redirections et Pipes

### 6.1 Redirections Standard

```bash
# Standard streams
# 0 : stdin (input)
# 1 : stdout (output)
# 2 : stderr (errors)

# Redirect stdout
echo "Hello" > file.txt         # Écrase fichier
echo "World" >> file.txt        # Append fichier

# Redirect stderr
command 2> errors.log           # Stderr vers fichier
command 2>> errors.log          # Stderr append

# Redirect stdout et stderr
command > output.log 2>&1       # Les deux vers même fichier
command &> output.log           # Même chose (Bash 4+)

# Redirect stderr vers stdout
command 2>&1                    # Stderr → stdout

# Discard output
command > /dev/null             # Ignore stdout
command 2> /dev/null            # Ignore stderr
command &> /dev/null            # Ignore all

# Redirect stdin
command < input.txt             # Lire depuis fichier
command <<< "inline input"      # Here-string

# Tee (write to file AND stdout)
command | tee output.log        # Stdout vers fichier et terminal
command | tee -a output.log     # Append mode

# Examples pratiques
# Log script output
exec > >(tee -a script.log)
exec 2>&1
echo "All output logged"

# Backup stdout/stderr
exec 3>&1 4>&2                  # Save to fd 3,4
exec > output.log 2>&1          # Redirect
echo "Logged"
exec 1>&3 2>&4                  # Restore
echo "Back to terminal"

# Multiple redirections
{
    echo "Line 1"
    echo "Line 2"
    echo "Line 3"
} > output.txt

# Process substitution
diff <(ls dir1) <(ls dir2)
```

### 6.2 Here Documents

```bash
# Here-doc : multi-line input
cat << EOF > file.txt
Line 1
Line 2
Line 3
EOF

# Here-doc with variable expansion
NAME="John"
cat << EOF
Hello $NAME
Current date: $(date)
EOF

# Here-doc sans expansion (quote delimiter)
cat << 'EOF'
$NAME will not expand
$(date) will not execute
EOF

# Here-doc avec indent (<<-)
if true; then
    cat <<- EOF
		This is indented
		Tabs removed
	EOF
fi

# Here-doc vers variable
read -r -d '' SQL_QUERY << EOF
SELECT *
FROM users
WHERE active = 1
  AND created_at > '2024-01-01'
ORDER BY username;
EOF

echo "$SQL_QUERY"

# Here-doc vers commande
mysql -u root -p << EOF
CREATE DATABASE mydb;
USE mydb;
CREATE TABLE users (id INT, name VARCHAR(50));
INSERT INTO users VALUES (1, 'John');
EOF

# Here-doc interactive
psql << EOF
\c database_name
\dt
SELECT COUNT(*) FROM users;
\q
EOF

# Pratique : configuration file generation
cat > /etc/myapp/config.yml << EOF
---
database:
  host: $DB_HOST
  port: $DB_PORT
  user: $DB_USER
  
app:
  debug: false
  workers: $(nproc)
EOF
```

### 6.3 Pipes

```bash
# Pipe basique : stdout → stdin
ls -l | grep ".txt"
cat file.txt | wc -l

# Pipeline multiple
ps aux | grep nginx | grep -v grep | awk '{print $2}'

# Pipe avec redirections
cat input.txt | grep "error" | sort | uniq > errors.txt

# Tee dans pipeline
cat log.txt | grep "ERROR" | tee errors.txt | wc -l

# Pipe stderr (|&)
command 2>&1 | grep "error"
command |& grep "error"        # Même chose (Bash 4+)

# Named pipes (FIFO)
mkfifo mypipe
cat > mypipe &                 # Writer (background)
cat mypipe                     # Reader

# Process substitution
# <(command) : output comme fichier
diff <(sort file1.txt) <(sort file2.txt)

# >(command) : input comme fichier
echo "test" > >(cat > file.txt)

# Examples pratiques

# Monitor log temps réel avec filtres
tail -f /var/log/syslog | grep --line-buffered "error" | while read line; do
    echo "[$(date)] $line"
done

# Parallel processing
cat urls.txt | xargs -P 4 -I {} curl -sS {} | grep "title"

# Complex pipeline
cat access.log |
    grep "GET" |
    awk '{print $7}' |
    sort |
    uniq -c |
    sort -rn |
    head -10

# Pipeline avec error handling
set -o pipefail                # Pipeline fails si une commande fail
cat file.txt | grep "pattern" | sort
if [[ $? -ne 0 ]]; then
    echo "Pipeline failed"
fi
```

## Section 7 : Expressions Régulières et Text Processing

### 7.1 Regex avec Grep

```bash
# Grep basique
grep "pattern" file.txt                 # Search pattern
grep -i "pattern" file.txt              # Case insensitive
grep -v "pattern" file.txt              # Invert match (exclude)
grep -n "pattern" file.txt              # Show line numbers
grep -c "pattern" file.txt              # Count matches

# Grep récursif
grep -r "pattern" /var/log              # Recursive search
grep -r --include="*.log" "error" /var/log

# Grep avec context
grep -A 3 "pattern" file.txt            # 3 lines After
grep -B 3 "pattern" file.txt            # 3 lines Before
grep -C 3 "pattern" file.txt            # 3 lines Context (both)

# Regex patterns
grep "^start" file.txt                  # Start of line
grep "end$" file.txt                    # End of line
grep "^$" file.txt                      # Empty lines
grep "[0-9]" file.txt                   # Digit
grep "[a-zA-Z]" file.txt                # Letter
grep "a.c" file.txt                     # a + any char + c
grep "colou?r" file.txt                 # color or colour
grep "file[0-9]\+" file.txt             # file + 1+ digits

# Extended regex (grep -E ou egrep)
grep -E "error|warning" file.txt        # OR
grep -E "^[0-9]{3}-[0-9]{4}$" file.txt  # Phone format
grep -E "\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b" -i file.txt  # Email

# Perl regex (grep -P)
grep -P "\d{3}-\d{4}" file.txt          # \d = digit
grep -P "(?<=error: ).*" file.txt       # Lookbehind

# Practical examples
# Extract IPs from log
grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" access.log

# Find email addresses
grep -oE "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" file.txt

# Extract URLs
grep -oE "(http|https)://[a-zA-Z0-9./?=_%:-]*" file.txt

# Find errors in logs (last 24h)
find /var/log -name "*.log" -mtime -1 -exec grep -iH "error\|critical\|fatal" {} \;
```

### 7.2 Regex avec Bash [[]]

```bash
# Pattern matching dans conditions
if [[ "$string" =~ ^[0-9]+$ ]]; then
    echo "String is number"
fi

# Extract regex groups
string="User: john@example.com"
if [[ "$string" =~ User:\ ([a-z]+)@([a-z]+\.[a-z]+) ]]; then
    username="${BASH_REMATCH[1]}"      # john
    domain="${BASH_REMATCH[2]}"        # example.com
    echo "Username: $username"
    echo "Domain: $domain"
fi

# Validation patterns
# Email
EMAIL="user@example.com"
if [[ "$EMAIL" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
    echo "Valid email"
fi

# Phone (US format)
PHONE="555-1234"
if [[ "$PHONE" =~ ^[0-9]{3}-[0-9]{4}$ ]]; then
    echo "Valid phone"
fi

# IP address
IP="192.168.1.1"
if [[ "$IP" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
    echo "Valid IP format"
fi

# Date (YYYY-MM-DD)
DATE="2024-01-16"
if [[ "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "Valid date format"
fi

# Extract parts
LOG="[2024-01-16 14:30:45] ERROR: Connection failed"
if [[ "$LOG" =~ \[([^\]]+)\]\ ([A-Z]+):\ (.+) ]]; then
    timestamp="${BASH_REMATCH[1]}"
    level="${BASH_REMATCH[2]}"
    message="${BASH_REMATCH[3]}"
    
    echo "Timestamp: $timestamp"
    echo "Level: $level"
    echo "Message: $message"
fi
```

### 7.3 Text Processing avec Awk

```bash
# Awk basique : print columns
echo "john 25 engineer" | awk '{print $1}'           # john
echo "john 25 engineer" | awk '{print $2, $3}'       # 25 engineer

# Process file
awk '{print $1}' file.txt                            # First column
awk '{print $1, $3}' file.txt                        # Columns 1 and 3

# Field separator
awk -F: '{print $1}' /etc/passwd                     # Username from passwd
awk -F, '{print $2}' data.csv                        # CSV column 2

# Patterns
awk '/error/ {print}' log.txt                        # Lines containing "error"
awk '$3 > 100' data.txt                              # Lines where col3 > 100

# Built-in variables
# NR : Line number
# NF : Number of fields
# FS : Field separator
# OFS : Output field separator

awk '{print NR, $0}' file.txt                        # Line numbers
awk '{print NF}' file.txt                            # Field count per line
awk 'NF > 0' file.txt                                # Non-empty lines

# Conditions
awk '$3 > 50 {print $1, $3}' data.txt
awk '$2 == "active" {print $1}' status.txt

# BEGIN/END blocks
awk 'BEGIN {sum=0} {sum+=$1} END {print sum}' numbers.txt

# Calculations
awk '{sum+=$1; count++} END {print sum/count}' numbers.txt    # Average

# Practical examples
# Sum column
awk '{sum+=$3} END {print sum}' sales.txt

# Count unique values
awk '{count[$1]++} END {for (k in count) print k, count[k]}' data.txt

# Format output
awk '{printf "%-10s %5d\n", $1, $2}' data.txt

# Process CSV
awk -F, 'NR>1 {print $1, $3}' data.csv               # Skip header

# Extract from log
awk '/ERROR/ {print $1, $2, $NF}' app.log

# Top 10 IPs from access log
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# Parse Apache log
awk '{print $1, $7, $9}' access.log                  # IP, URL, Status
```

### 7.4 Text Processing avec Sed

```bash
# Sed basique : substitution
sed 's/old/new/' file.txt                    # Replace first occurrence
sed 's/old/new/g' file.txt                   # Replace all (global)
sed 's/old/new/gi' file.txt                  # Case insensitive

# In-place edit
sed -i 's/old/new/g' file.txt                # Modify file directly
sed -i.bak 's/old/new/g' file.txt            # Create backup

# Delete lines
sed '/pattern/d' file.txt                    # Delete matching lines
sed '1d' file.txt                            # Delete first line
sed '$d' file.txt                            # Delete last line
sed '1,5d' file.txt                          # Delete lines 1-5

# Print specific lines
sed -n '10p' file.txt                        # Print line 10
sed -n '10,20p' file.txt                     # Print lines 10-20
sed -n '/pattern/p' file.txt                 # Print matching lines

# Insert/append
sed '1i\New first line' file.txt             # Insert before line 1
sed '1a\New second line' file.txt            # Append after line 1
sed '$a\New last line' file.txt              # Append at end

# Change line
sed '5c\Replacement line' file.txt           # Replace line 5

# Multiple operations
sed -e 's/old/new/g' -e 's/foo/bar/g' file.txt
sed 's/old/new/g; s/foo/bar/g' file.txt

# Regex grouping
sed 's/\([0-9]\{3\}\)-\([0-9]\{4\}\)/(\1) \2/' file.txt
# 555-1234 → (555) 1234

# Practical examples
# Remove empty lines
sed '/^$/d' file.txt

# Remove comments
sed '/^#/d' file.txt

# Remove trailing whitespace
sed 's/[[:space:]]*$//' file.txt

# Add prefix to lines
sed 's/^/> /' file.txt

# Extract email from HTML
sed -n 's/.*href="\([^"]*\)".*/\1/p' page.html

# Format log timestamps
sed 's/^\([0-9-]* [0-9:]*\).*/[\1]/' log.txt

# Remove ANSI color codes
sed 's/\x1b\[[0-9;]*m//g' colored.txt

# Convert DOS to Unix line endings
sed -i 's/\r$//' file.txt

# Comment out lines
sed 's/^/# /' config.txt

# Uncomment lines
sed 's/^# //' config.txt
```

---

## Section 8 : Arguments et Options

### 8.1 Paramètres Positionnels

```bash
#!/bin/bash
# script.sh arg1 arg2 arg3

# Access arguments
echo "Script name: $0"                # script.sh
echo "First arg: $1"                  # arg1
echo "Second arg: $2"                 # arg2
echo "Third arg: $3"                  # arg3

# All arguments
echo "All args (\$@): $@"             # arg1 arg2 arg3
echo "All args (\$*): $*"             # arg1 arg2 arg3
echo "Arg count: $#"                  # 3

# Difference $@ vs $*
# $@ : Each argument separate
# $* : All arguments as single string

# Example with loop
for arg in "$@"; do
    echo "Argument: $arg"
done

# Shift : remove first argument
echo "Before shift: $1"               # arg1
shift
echo "After shift: $1"                # arg2 (was $2)

# Shift multiple
shift 2                               # Remove 2 arguments

# Check arguments count
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <arg1> <arg2>"
    exit 1
fi

# Default values
ARG1="${1:-default}"                  # Use default if $1 empty
ARG2="${2:-default}"

# Require argument
if [[ -z "$1" ]]; then
    echo "ERROR: Missing required argument"
    exit 1
fi
```

### 8.2 Getopts (Options Courtes)

```bash
#!/bin/bash
# Parse short options (-a -b -c value)

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    -h          Show help
    -v          Verbose mode
    -f FILE     Input file
    -o FILE     Output file
    -n NUM      Number value
EOF
    exit 1
}

# Default values
VERBOSE=false
INPUT_FILE=""
OUTPUT_FILE=""
NUMBER=0

# Parse options
while getopts "hvf:o:n:" opt; do
    case $opt in
        h)
            usage
            ;;
        v)
            VERBOSE=true
            ;;
        f)
            INPUT_FILE="$OPTARG"
            ;;
        o)
            OUTPUT_FILE="$OPTARG"
            ;;
        n)
            NUMBER="$OPTARG"
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            usage
            ;;
        :)
            echo "Option -$OPTARG requires an argument" >&2
            usage
            ;;
    esac
done

# Shift processed options
shift $((OPTIND - 1))

# Remaining arguments
echo "Remaining args: $@"

# Use parsed options
[[ "$VERBOSE" == true ]] && echo "Verbose mode enabled"
[[ -n "$INPUT_FILE" ]] && echo "Input file: $INPUT_FILE"
[[ -n "$OUTPUT_FILE" ]] && echo "Output file: $OUTPUT_FILE"
[[ $NUMBER -gt 0 ]] && echo "Number: $NUMBER"
```

### 8.3 Long Options (Manual Parsing)

```bash
#!/bin/bash
# Parse long options (--help --verbose --file=value)

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    -h, --help              Show help
    -v, --verbose           Verbose mode
    -f, --file FILE         Input file
    -o, --output FILE       Output file
    -n, --number NUM        Number value
    --dry-run               Dry run mode
EOF
    exit 1
}

# Default values
VERBOSE=false
INPUT_FILE=""
OUTPUT_FILE=""
NUMBER=0
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--file)
            INPUT_FILE="$2"
            shift 2
            ;;
        --file=*)
            INPUT_FILE="${1#*=}"
            shift
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --output=*)
            OUTPUT_FILE="${1#*=}"
            shift
            ;;
        -n|--number)
            NUMBER="$2"
            shift 2
            ;;
        --number=*)
            NUMBER="${1#*=}"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "Unknown option: $1" >&2
            usage
            ;;
        *)
            break
            ;;
    esac
done

# Validation
if [[ -z "$INPUT_FILE" ]]; then
    echo "ERROR: --file required" >&2
    exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "ERROR: File not found: $INPUT_FILE" >&2
    exit 1
fi

# Use options
[[ "$VERBOSE" == true ]] && echo "Processing: $INPUT_FILE"
[[ "$DRY_RUN" == true ]] && echo "DRY RUN MODE"
```

### 8.4 Argument Parsing Production

```bash
#!/bin/bash
# production-script.sh - Complete argument parsing

set -euo pipefail

# === CONFIGURATION ===
SCRIPT_NAME=$(basename "$0")
VERSION="1.0.0"

# Defaults
VERBOSE=false
DEBUG=false
DRY_RUN=false
CONFIG_FILE=""
LOG_LEVEL="INFO"

# === FUNCTIONS ===
usage() {
    cat << EOF
$SCRIPT_NAME v$VERSION - Description of script

Usage: $SCRIPT_NAME [OPTIONS] <command> [ARGS]

Commands:
    start           Start service
    stop            Stop service
    restart         Restart service
    status          Check status

Options:
    -h, --help              Show this help
    -v, --verbose           Verbose output
    -d, --debug             Debug mode
    -c, --config FILE       Configuration file
    -l, --log-level LEVEL   Log level (DEBUG|INFO|WARN|ERROR)
    --dry-run               Dry run mode
    --version               Show version

Examples:
    $SCRIPT_NAME start
    $SCRIPT_NAME --verbose --config app.conf restart
    $SCRIPT_NAME --dry-run stop

EOF
    exit 0
}

version() {
    echo "$SCRIPT_NAME version $VERSION"
    exit 0
}

log() {
    local level="$1"
    shift
    
    # Log level filtering
    case "$LOG_LEVEL" in
        DEBUG) levels="DEBUG INFO WARN ERROR" ;;
        INFO)  levels="INFO WARN ERROR" ;;
        WARN)  levels="WARN ERROR" ;;
        ERROR) levels="ERROR" ;;
    esac
    
    if [[ " $levels " =~ " $level " ]]; then
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*" >&2
    fi
}

# === ARGUMENT PARSING ===
COMMAND=""
ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage
            ;;
        --version)
            version
            ;;
        -v|--verbose)
            VERBOSE=true
            LOG_LEVEL="DEBUG"
            shift
            ;;
        -d|--debug)
            DEBUG=true
            set -x
            shift
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --config=*)
            CONFIG_FILE="${1#*=}"
            shift
            ;;
        -l|--log-level)
            LOG_LEVEL="$2"
            shift 2
            ;;
        --log-level=*)
            LOG_LEVEL="${1#*=}"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --)
            shift
            ARGS+=("$@")
            break
            ;;
        -*)
            log "ERROR" "Unknown option: $1"
            usage
            ;;
        *)
            if [[ -z "$COMMAND" ]]; then
                COMMAND="$1"
            else
                ARGS+=("$1")
            fi
            shift
            ;;
    esac
done

# === VALIDATION ===
if [[ -z "$COMMAND" ]]; then
    log "ERROR" "No command specified"
    usage
fi

if [[ -n "$CONFIG_FILE" ]] && [[ ! -f "$CONFIG_FILE" ]]; then
    log "ERROR" "Config file not found: $CONFIG_FILE"
    exit 1
fi

# === MAIN LOGIC ===
case "$COMMAND" in
    start)
        log "INFO" "Starting service..."
        [[ "$DRY_RUN" == true ]] && log "INFO" "[DRY RUN] Would start service"
        ;;
    stop)
        log "INFO" "Stopping service..."
        [[ "$DRY_RUN" == true ]] && log "INFO" "[DRY RUN] Would stop service"
        ;;
    restart)
        log "INFO" "Restarting service..."
        ;;
    status)
        log "INFO" "Checking status..."
        ;;
    *)
        log "ERROR" "Unknown command: $COMMAND"
        usage
        ;;
esac

log "INFO" "Completed successfully"
exit 0
```

---

## Section 9 : Debugging et Error Handling

### 9.1 Set Options

```bash
# Bash options pour robustesse

# Exit on error
set -e
# ou
set -o errexit
# Script arrête si commande retourne code ≠ 0

# Exit on undefined variable
set -u
# ou
set -o nounset
# Script arrête si variable non définie utilisée

# Pipe fail
set -o pipefail
# Pipeline fail si UNE commande fail (pas seulement dernière)

# Combined (best practice production)
set -euo pipefail

# Example impact :
#!/bin/bash
set -euo pipefail

# Sans set -e, continuerait après erreur
command_that_fails
echo "This won't execute if set -e"

# Sans set -u, $UNDEFINED serait vide
echo "Value: $UNDEFINED"  # Error avec set -u

# Sans pipefail, ignore errors sauf dernière commande
cat nonexistent.txt | grep "pattern" | wc -l
# Avec pipefail : fail si cat fail

# Disable temporarily
set +e
risky_command || true
set -e

# Xtrace (debugging)
set -x                    # Print commands before execution
set -o xtrace

# Output example avec set -x :
# + echo 'Hello World'
# Hello World
# + COUNT=5
# + echo 'Count: 5'
# Count: 5

# Disable xtrace
set +x

# Voir toutes options actives
echo "$-"
# Output : himBHs (h=hashall, i=interactive, etc.)

# Custom PS4 (xtrace prompt)
export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
set -x
# Output :
# +(script.sh:15): main(): echo 'Hello'
```

### 9.2 Trap et Cleanup

```bash
# Trap : execute code on signals/errors

# Basic trap
trap 'echo "Script interrupted"' INT
# Ctrl+C will print message

# Cleanup on exit
cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/tempfile
    kill $BACKGROUND_PID 2>/dev/null || true
}

trap cleanup EXIT

# Cleanup on error
error_handler() {
    local line="$1"
    echo "ERROR on line $line" >&2
    cleanup
    exit 1
}

trap 'error_handler $LINENO' ERR

# Multiple signals
trap 'echo "Terminated"; cleanup; exit' INT TERM

# Ignore signal
trap '' INT              # Ignore Ctrl+C

# Reset trap
trap - INT               # Reset to default

# Common signals
# INT  : Interrupt (Ctrl+C)
# TERM : Terminate
# EXIT : Script exit (normal or error)
# ERR  : Error (requires set -E)
# HUP  : Hangup (terminal closed)

# Production example
#!/bin/bash
set -euo pipefail

# Temp file for cleanup
TEMP_FILE=$(mktemp)
LOCK_FILE="/var/lock/$(basename "$0").lock"

cleanup() {
    local exit_code=$?
    
    echo "Cleaning up..."
    
    # Remove temp files
    [[ -f "$TEMP_FILE" ]] && rm -f "$TEMP_FILE"
    
    # Release lock
    [[ -f "$LOCK_FILE" ]] && rm -f "$LOCK_FILE"
    
    # Kill background jobs
    jobs -p | xargs -r kill 2>/dev/null || true
    
    if [[ $exit_code -ne 0 ]]; then
        echo "Script failed with exit code: $exit_code" >&2
    fi
    
    exit $exit_code
}

trap cleanup EXIT INT TERM

# Acquire lock
if [[ -f "$LOCK_FILE" ]]; then
    echo "ERROR: Script already running" >&2
    exit 1
fi
echo $$ > "$LOCK_FILE"

# Script logic...
echo "Processing..." > "$TEMP_FILE"

# Cleanup automatically called on exit
```

### 9.3 Error Handling Patterns

```bash
# Pattern 1: Check command exists
if ! command -v docker &>/dev/null; then
    echo "ERROR: docker not installed" >&2
    exit 1
fi

# Pattern 2: Check exit code explicitly
if ! grep "pattern" file.txt; then
    echo "Pattern not found"
    exit 1
fi

# Pattern 3: Store exit code
grep "pattern" file.txt
exit_code=$?
if [[ $exit_code -ne 0 ]]; then
    echo "Grep failed with code: $exit_code"
fi

# Pattern 4: OR operator (continue on error)
mkdir /tmp/dir 2>/dev/null || true
rm -f file.txt || echo "File not found (ignored)"

# Pattern 5: AND operator (chain success)
cd /tmp && rm -rf old_data && mkdir new_data

# Pattern 6: Subshell (isolate errors)
(
    set -e
    command1
    command2
    command3
) || echo "Subshell failed"

# Pattern 7: Function error handling
safe_command() {
    local result
    result=$(risky_command 2>&1) || {
        echo "ERROR: risky_command failed: $result" >&2
        return 1
    }
    echo "$result"
}

# Pattern 8: Retry logic
retry() {
    local max_attempts=$1
    local delay=$2
    shift 2
    
    local attempt=1
    until "$@"; do
        if [[ $attempt -ge $max_attempts ]]; then
            echo "ERROR: Failed after $max_attempts attempts" >&2
            return 1
        fi
        
        echo "Attempt $attempt failed, retrying in ${delay}s..." >&2
        sleep "$delay"
        ((attempt++))
    done
}

# Usage
retry 5 2 curl -sSf https://example.com

# Pattern 9: Defensive checks
process_file() {
    local file="$1"
    
    # Check argument
    if [[ -z "$file" ]]; then
        echo "ERROR: No file specified" >&2
        return 1
    fi
    
    # Check file exists
    if [[ ! -f "$file" ]]; then
        echo "ERROR: File not found: $file" >&2
        return 1
    fi
    
    # Check readable
    if [[ ! -r "$file" ]]; then
        echo "ERROR: File not readable: $file" >&2
        return 1
    fi
    
    # Process
    cat "$file"
}

# Pattern 10: Exit codes standards
# 0   : Success
# 1   : General error
# 2   : Misuse (wrong arguments)
# 126 : Command can't execute
# 127 : Command not found
# 128+n : Fatal signal n

exit_with_error() {
    local message="$1"
    local code="${2:-1}"
    echo "ERROR: $message" >&2
    exit "$code"
}

[[ $# -eq 0 ]] && exit_with_error "Missing arguments" 2
```

### 9.4 Debugging Techniques

```bash
# Technique 1: Bash debugger (bashdb)
# Install: apt install bashdb
# Usage: bashdb script.sh

# Technique 2: Print debugging
debug() {
    if [[ "${DEBUG:-false}" == true ]]; then
        echo "[DEBUG] $*" >&2
    fi
}

DEBUG=true
debug "Variable value: $VAR"
debug "Function called with: $@"

# Technique 3: Verbose logging
log() {
    local level="$1"
    shift
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $*" >&2
}

log "INFO" "Processing file: $file"
log "WARN" "Disk space low"
log "ERROR" "Operation failed"

# Technique 4: Stack trace on error
print_stack_trace() {
    local frame=0
    echo "Stack trace:" >&2
    while caller $frame >&2; do
        ((frame++))
    done
}

trap 'print_stack_trace' ERR

# Technique 5: Dry run mode
DRY_RUN=true

execute() {
    if [[ "$DRY_RUN" == true ]]; then
        echo "[DRY RUN] Would execute: $*"
    else
        "$@"
    fi
}

execute rm -rf /tmp/data
execute systemctl restart nginx

# Technique 6: Step-by-step execution
read -p "Press enter to continue..."

# Technique 7: Conditional debugging
if [[ "${BASH_SUBSHELL}" -gt 0 ]]; then
    echo "Running in subshell level: $BASH_SUBSHELL"
fi

# Technique 8: Function tracing
set -o functrace
trap 'echo "Function: ${FUNCNAME[0]}"' DEBUG

# Technique 9: Performance profiling
TIMEFORMAT='Execution time: %R seconds'
time {
    # Code to profile
    sleep 2
}

# Technique 10: ShellCheck (static analysis)
# Install: apt install shellcheck
# Usage: shellcheck script.sh
# Catches common errors before execution
```

---

## Section 10 : Process Management et Signals

### 10.1 Background Jobs

```bash
# Run background
command &
sleep 10 &

# Jobs control
jobs                    # List background jobs
jobs -l                 # With PIDs
jobs -r                 # Running jobs
jobs -s                 # Stopped jobs

# Bring to foreground
fg                      # Last job
fg %1                   # Job 1
fg %command             # Job by command name

# Send to background
bg                      # Continue stopped job in background
bg %1

# Wait for jobs
wait                    # Wait all background jobs
wait $PID               # Wait specific PID
wait %1                 # Wait job 1

# Kill jobs
kill %1                 # Kill job 1
kill -9 %1              # Force kill
killall process_name    # Kill by name

# Example: parallel processing
for file in *.txt; do
    process_file "$file" &
done
wait                    # Wait all complete

echo "All files processed"

# Limit concurrent jobs
MAX_JOBS=4
for file in *.txt; do
    # Wait if at limit
    while [[ $(jobs -r | wc -l) -ge $MAX_JOBS ]]; do
        sleep 0.1
    done
    
    process_file "$file" &
done
wait
```

### 10.2 Process Control

```bash
# Get process info
ps aux                          # All processes
ps aux | grep nginx             # Find process
pgrep nginx                     # PIDs by name
pgrep -u user                   # PIDs by user

# Process tree
pstree                          # Tree all processes
pstree -p $$                    # Tree current script

# Process details
top                             # Interactive monitor
htop                            # Better top (if installed)
pidof nginx                     # PID by name

# Start process
nohup command &                 # Ignore hangup signal
nohup command > output.log 2>&1 &

# Disown (detach from shell)
command &
disown                          # Detach last background job
disown %1                       # Detach job 1

# Screen/tmux (persistent sessions)
screen -S session_name          # Start screen
screen -r session_name          # Reattach
# Ctrl+A, D : Detach

tmux new -s session_name        # Start tmux
tmux attach -t session_name     # Reattach

# Daemon creation
#!/bin/bash
# daemon.sh

# Fork to background
{
    # Close file descriptors
    exec 0</dev/null
    exec 1>/var/log/daemon.log
    exec 2>&1
    
    # Change directory
    cd /
    
    # Set umask
    umask 0
    
    # Daemon loop
    while true; do
        # Work
        echo "$(date): Working..."
        sleep 60
    done
} &

# Save PID
echo $! > /var/run/daemon.pid

# Start daemon
./daemon.sh

# Stop daemon
kill $(cat /var/run/daemon.pid)
```

### 10.3 Signals

```bash
# Signal types
# SIGTERM (15) : Graceful termination
# SIGKILL (9)  : Force kill (can't catch)
# SIGINT (2)   : Interrupt (Ctrl+C)
# SIGHUP (1)   : Hangup (reload config)
# SIGSTOP (19) : Pause (can't catch)
# SIGCONT (18) : Continue

# Send signals
kill -TERM $PID                 # Graceful stop
kill -9 $PID                    # Force kill
kill -HUP $PID                  # Reload config
kill -USR1 $PID                 # User signal 1

# Signal names
kill -SIGTERM $PID
kill -15 $PID                   # Same as SIGTERM

# Trap signals in script
#!/bin/bash

running=true

# Graceful shutdown
shutdown() {
    echo "Shutting down gracefully..."
    running=false
}

# Reload configuration
reload() {
    echo "Reloading configuration..."
    source config.sh
}

trap shutdown TERM INT
trap reload HUP

# Main loop
while $running; do
    echo "Working..."
    sleep 5
done

echo "Stopped"

# Usage
./script.sh &
PID=$!

kill -HUP $PID                  # Reload
kill -TERM $PID                 # Graceful stop

# Timeout with signal
timeout 10s command             # Kill after 10s
timeout -s KILL 10s command     # SIGKILL after 10s

# Process group signals
kill -TERM -$$                  # Kill process group
```

### 10.4 IPC (Inter-Process Communication)

```bash
# Named pipes (FIFO)
mkfifo /tmp/mypipe

# Writer (background)
echo "Hello" > /tmp/mypipe &

# Reader
cat /tmp/mypipe                 # Blocks until data

# Cleanup
rm /tmp/mypipe

# Example: bidirectional communication
mkfifo /tmp/pipe1 /tmp/pipe2

# Process 1
{
    while true; do
        read line < /tmp/pipe1
        echo "Process 1 received: $line"
        echo "Response from P1" > /tmp/pipe2
    done
} &

# Process 2
{
    echo "Hello from P2" > /tmp/pipe1
    read response < /tmp/pipe2
    echo "Process 2 received: $response"
} &

# Shared files (simple IPC)
echo "data" > /tmp/shared.txt
data=$(cat /tmp/shared.txt)

# File locking
{
    flock -x 200                # Exclusive lock
    # Critical section
    echo "Locked operation"
    sleep 2
} 200>/tmp/lockfile

# Process substitution
diff <(ls dir1) <(ls dir2)      # Compare outputs

# Coprocess (Bash 4+)
coproc NAME { command; }        # Start coprocess
echo "input" >&"${NAME[1]}"     # Write to coprocess
read output <&"${NAME[0]}"      # Read from coprocess
```

---

## Section 11 : Best Practices et Sécurité

### 11.1 Script Template Production

```bash
#!/usr/bin/env bash
#
# script-name.sh - Brief description
#
# Author: Your Name <email@example.com>
# Created: 2024-01-16
# Version: 1.0.0
#
# Description:
#   Detailed description of what this script does
#
# Usage:
#   script-name.sh [OPTIONS] <command> [ARGS]
#
# Dependencies:
#   - bash >= 4.0
#   - curl
#   - jq
#
# Exit codes:
#   0 - Success
#   1 - General error
#   2 - Invalid arguments

set -euo pipefail
IFS=$'\n\t'

# === CONFIGURATION ===
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
readonly SCRIPT_VERSION="1.0.0"
readonly TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Defaults
VERBOSE=false
DEBUG=false
DRY_RUN=false
LOG_FILE="/var/log/${SCRIPT_NAME%.sh}.log"

# === COLORS ===
if [[ -t 1 ]]; then
    readonly RED='\033[0;31m'
    readonly GREEN='\033[0;32m'
    readonly YELLOW='\033[1;33m'
    readonly NC='\033[0m'
else
    readonly RED=''
    readonly GREEN=''
    readonly YELLOW=''
    readonly NC=''
fi

# === FUNCTIONS ===

# Logging
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE" >&2
}

log_info() {
    log "INFO" "$*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
    log "WARN" "$*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
    log "ERROR" "$*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
    log "INFO" "$*"
}

# Error handling
error_exit() {
    local message="$1"
    local code="${2:-1}"
    log_error "$message"
    exit "$code"
}

# Cleanup
cleanup() {
    local exit_code=$?
    
    log_info "Cleanup started"
    
    # Remove temp files
    [[ -n "${TEMP_DIR:-}" ]] && [[ -d "$TEMP_DIR" ]] && rm -rf "$TEMP_DIR"
    
    # Kill background jobs
    jobs -p | xargs -r kill 2>/dev/null || true
    
    if [[ $exit_code -ne 0 ]]; then
        log_error "Script failed with exit code: $exit_code"
    else
        log_info "Script completed successfully"
    fi
    
    exit $exit_code
}

trap cleanup EXIT INT TERM

# Validation
require_command() {
    local cmd="$1"
    if ! command -v "$cmd" &>/dev/null; then
        error_exit "Required command not found: $cmd" 127
    fi
}

require_root() {
    if [[ $EUID -ne 0 ]]; then
        error_exit "This script must be run as root" 1
    fi
}

# === MAIN ===
main() {
    log_info "Script started: $SCRIPT_NAME v$SCRIPT_VERSION"
    
    # Validate dependencies
    require_command "curl"
    require_command "jq"
    
    # Your logic here
    
    log_success "All operations completed"
}

# Parse arguments and call main
# (argument parsing code from Section 8)

main "$@"
exit 0
```

### 11.2 Security Best Practices

```bash
# 1. Input validation
validate_input() {
    local input="$1"
    
    # Whitelist characters
    if [[ ! "$input" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        error_exit "Invalid input: $input"
    fi
}

# 2. Avoid command injection
# ❌ BAD
eval "ls $USER_INPUT"           # NEVER use eval with user input
command="rm $USER_FILE"
$command                        # Command from variable

# ✅ GOOD
ls "$USER_INPUT"                # Quoted variable
rm -f "$USER_FILE"              # Direct command

# 3. Use arrays for commands with arguments
# ❌ BAD
files="file1.txt file2.txt"
rm $files                       # Word splitting issue

# ✅ GOOD
files=("file1.txt" "file2.txt")
rm "${files[@]}"

# 4. Sanitize file paths
sanitize_path() {
    local path="$1"
    
    # Remove .. (directory traversal)
    path="${path//\.\./}"
    
    # Remove leading slashes (absolute paths)
    path="${path#/}"
    
    echo "$path"
}

# 5. Use mktemp for temporary files
# ❌ BAD
TEMP_FILE="/tmp/myfile_$$"      # Predictable name

# ✅ GOOD
TEMP_FILE=$(mktemp)             # Random secure name
TEMP_DIR=$(mktemp -d)

# 6. Set secure umask
umask 077                       # Files: 600, Dirs: 700

# 7. Avoid sensitive data in ps
# ❌ BAD
mysql -u root -pPASSWORD        # Password visible in ps

# ✅ GOOD
mysql --defaults-file=/secure/mysql.cnf

# 8. Secure password handling
read_password() {
    local password
    read -s -p "Enter password: " password
    echo >&2
    echo "$password"
}

PASSWORD=$(read_password)
# Use $PASSWORD
unset PASSWORD                  # Clear from memory

# 9. Check file permissions before reading secrets
if [[ $(stat -c %a /etc/secret.key) != "600" ]]; then
    error_exit "Insecure permissions on secret.key"
fi

# 10. Use process substitution instead of temp files
diff <(sort file1.txt) <(sort file2.txt)

# 11. Validate URLs before curl
validate_url() {
    local url="$1"
    if [[ ! "$url" =~ ^https?:// ]]; then
        error_exit "Invalid URL: $url"
    fi
}

# 12. Avoid wildcards in sensitive operations
# ❌ DANGEROUS
rm -rf /$DIR/*                  # If $DIR empty = rm -rf /*

# ✅ SAFE
if [[ -n "$DIR" ]] && [[ -d "$DIR" ]]; then
    rm -rf "${DIR:?}/"*
fi
```

### 11.3 Performance Best Practices

```bash
# 1. Avoid subshells when possible
# ❌ SLOW
count=$(cat file.txt | wc -l)

# ✅ FAST
count=$(wc -l < file.txt)

# 2. Use built-ins instead of external commands
# ❌ SLOW
dirname=$(dirname "$path")
basename=$(basename "$path")

# ✅ FAST
dirname="${path%/*}"
basename="${path##*/}"

# 3. Process files line by line efficiently
# ❌ SLOW (cat | while)
cat file.txt | while read line; do
    echo "$line"
done

# ✅ FAST (while < redirection)
while IFS= read -r line; do
    echo "$line"
done < file.txt

# 4. Avoid loops for simple operations
# ❌ SLOW
for file in *.txt; do
    rm "$file"
done

# ✅ FAST
rm *.txt

# 5. Use [[ ]] instead of [ ]
# [[ ]] is bash keyword (faster, more features)
if [[ "$var" == "value" ]]; then
    # ...
fi

# 6. Minimize command substitutions
# ❌ SLOW (multiple calls)
date=$(date)
echo "$date"
echo "$date"

# ✅ FAST (one call)
date=$(date)
echo "$date"
echo "$date"

# 7. Use printf instead of echo for formatting
printf "%-10s %5d\n" "Name" 123

# 8. Parallel processing for independent tasks
# GNU Parallel
parallel process_file ::: *.txt

# Or xargs
find . -name "*.txt" | xargs -P 4 -I {} process {}

# 9. Cache expensive operations
declare -A cache

get_user_info() {
    local username="$1"
    
    if [[ -z "${cache[$username]:-}" ]]; then
        cache[$username]=$(expensive_lookup "$username")
    fi
    
    echo "${cache[$username]}"
}

# 10. Use case instead of multiple if
# ❌ SLOW
if [[ "$var" == "a" ]]; then
    # ...
elif [[ "$var" == "b" ]]; then
    # ...
fi

# ✅ FAST
case "$var" in
    a) # ... ;;
    b) # ... ;;
esac
```

### 11.4 Code Quality Best Practices

```bash
# 1. Use shellcheck
# Install: apt install shellcheck
# Run: shellcheck script.sh

# 2. Consistent naming
GLOBAL_CONSTANT="value"         # UPPER_SNAKE_CASE
local_variable="value"          # lower_snake_case
function_name() { }             # lower_snake_case

# 3. Document functions
#######################################
# Process user data from file
# Arguments:
#   $1 - Input file path
#   $2 - Output directory
# Returns:
#   0 on success, 1 on error
# Globals:
#   VERBOSE
#######################################
process_data() {
    local input_file="$1"
    local output_dir="$2"
    
    # Implementation
}

# 4. Use readonly for constants
readonly PI=3.14159
readonly MAX_CONNECTIONS=100

# 5. Fail fast
[[ $# -eq 0 ]] && error_exit "No arguments provided"
[[ ! -f "$file" ]] && error_exit "File not found: $file"

# 6. One command per line in long chains
result=$(
    cat file.txt |
    grep "pattern" |
    sort |
    uniq -c |
    sort -rn |
    head -10
)

# 7. Use meaningful variable names
# ❌ BAD
x="value"
tmp="temporary"

# ✅ GOOD
user_count="value"
temp_directory="temporary"

# 8. Group related code
# Variables
readonly CONFIG_FILE="/etc/app.conf"
readonly LOG_FILE="/var/log/app.log"

# Functions
setup_environment() { }
validate_config() { }
start_application() { }

# Main
main() {
    setup_environment
    validate_config
    start_application
}

# 9. Avoid deep nesting
# ❌ BAD (deeply nested)
if [[ condition1 ]]; then
    if [[ condition2 ]]; then
        if [[ condition3 ]]; then
            # code
        fi
    fi
fi

# ✅ GOOD (early returns)
[[ ! condition1 ]] && return
[[ ! condition2 ]] && return
[[ ! condition3 ]] && return
# code

# 10. Version control friendly
# - Keep scripts under 500 lines
# - Separate large scripts into modules
# - Use source for shared code
```

---

## Section 12 : Cas Pratiques Production

### 12.1 Backup Script Automatisé

```bash
#!/bin/bash
# backup.sh - Automated backup script

set -euo pipefail

# Configuration
readonly BACKUP_SOURCE="/var/www"
readonly BACKUP_DEST="/backup"
readonly RETENTION_DAYS=30
readonly TIMESTAMP=$(date +%Y%m%d_%H%M%S)
readonly BACKUP_FILE="backup_${TIMESTAMP}.tar.gz"
readonly LOG_FILE="/var/log/backup.log"
readonly ALERT_EMAIL="admin@example.com"

# Functions
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

send_alert() {
    local subject="$1"
    local message="$2"
    
    echo "$message" | mail -s "$subject" "$ALERT_EMAIL"
}

check_disk_space() {
    local required_gb="$1"
    local available_gb=$(df -BG "$BACKUP_DEST" | awk 'NR==2 {print $4}' | sed 's/G//')
    
    if [[ $available_gb -lt $required_gb ]]; then
        log "ERROR: Insufficient disk space"
        send_alert "Backup Failed: Disk Space" "Required: ${required_gb}GB, Available: ${available_gb}GB"
        exit 1
    fi
    
    log "Disk space check passed: ${available_gb}GB available"
}

perform_backup() {
    log "Starting backup: $BACKUP_SOURCE → $BACKUP_DEST/$BACKUP_FILE"
    
    # Create backup with progress
    tar -czf "$BACKUP_DEST/$BACKUP_FILE" \
        --exclude='*.log' \
        --exclude='cache/*' \
        -C "$(dirname "$BACKUP_SOURCE")" \
        "$(basename "$BACKUP_SOURCE")" \
        2>&1 | tee -a "$LOG_FILE"
    
    # Verify
    if [[ -f "$BACKUP_DEST/$BACKUP_FILE" ]]; then
        local size=$(du -h "$BACKUP_DEST/$BACKUP_FILE" | cut -f1)
        log "Backup created successfully: $BACKUP_FILE ($size)"
    else
        log "ERROR: Backup file not created"
        send_alert "Backup Failed" "Backup file was not created"
        exit 1
    fi
}

verify_backup() {
    log "Verifying backup integrity..."
    
    if tar -tzf "$BACKUP_DEST/$BACKUP_FILE" >/dev/null 2>&1; then
        log "Backup verification passed"
    else
        log "ERROR: Backup verification failed"
        send_alert "Backup Failed: Verification" "Backup file is corrupted"
        exit 1
    fi
}

cleanup_old_backups() {
    log "Cleaning up backups older than $RETENTION_DAYS days..."
    
    find "$BACKUP_DEST" -name "backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    local remaining=$(find "$BACKUP_DEST" -name "backup_*.tar.gz" | wc -l)
    log "Cleanup completed. Remaining backups: $remaining"
}

# Main
main() {
    log "=== Backup started ==="
    
    # Pre-flight checks
    [[ $EUID -ne 0 ]] && { log "ERROR: Must run as root"; exit 1; }
    [[ ! -d "$BACKUP_SOURCE" ]] && { log "ERROR: Source not found"; exit 1; }
    [[ ! -d "$BACKUP_DEST" ]] && mkdir -p "$BACKUP_DEST"
    
    # Check disk space (require 10GB)
    check_disk_space 10
    
    # Perform backup
    perform_backup
    
    # Verify
    verify_backup
    
    # Cleanup
    cleanup_old_backups
    
    # Success notification
    send_alert "Backup Successful" "Backup completed: $BACKUP_FILE"
    log "=== Backup completed successfully ==="
}

main "$@"
exit 0

# Cron : Daily 3AM
# 0 3 * * * /usr/local/bin/backup.sh
```

### 12.2 Log Analysis et Monitoring

```bash
#!/bin/bash
# log-analyzer.sh - Analyze and alert on log patterns

set -euo pipefail

# Configuration
readonly LOG_FILE="${1:-/var/log/syslog}"
readonly ALERT_EMAIL="admin@example.com"
readonly ERROR_THRESHOLD=10
readonly WARN_THRESHOLD=50

# Patterns
readonly ERROR_PATTERN="ERROR|CRITICAL|FATAL"
readonly WARN_PATTERN="WARNING|WARN"
readonly ATTACK_PATTERN="failed password|authentication failure|invalid user"

# Analysis functions
analyze_errors() {
    local count=$(grep -ciE "$ERROR_PATTERN" "$LOG_FILE" || true)
    
    echo "Errors found: $count"
    
    if [[ $count -gt $ERROR_THRESHOLD ]]; then
        # Extract top errors
        local top_errors=$(grep -iE "$ERROR_PATTERN" "$LOG_FILE" | \
            cut -d: -f4- | \
            sort | uniq -c | sort -rn | head -10)
        
        # Alert
        mail -s "ALERT: High error count ($count)" "$ALERT_EMAIL" <<EOF
Error threshold exceeded: $count errors (threshold: $ERROR_THRESHOLD)

Top 10 errors:
$top_errors

Review log: $LOG_FILE
EOF
    fi
}

analyze_security() {
    local attacks=$(grep -ciE "$ATTACK_PATTERN" "$LOG_FILE" || true)
    
    if [[ $attacks -gt 0 ]]; then
        # Extract attacking IPs
        local attacking_ips=$(grep -iE "$ATTACK_PATTERN" "$LOG_FILE" | \
            grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" | \
            sort | uniq -c | sort -rn | head -10)
        
        echo "Security events: $attacks"
        echo "Top attacking IPs:"
        echo "$attacking_ips"
        
        # Auto-block top offenders (>20 attempts)
        echo "$attacking_ips" | while read count ip; do
            if [[ $count -gt 20 ]]; then
                echo "Blocking IP: $ip (attempts: $count)"
                ufw deny from "$ip" 2>/dev/null || true
            fi
        done
    fi
}

generate_report() {
    cat <<EOF
=== Log Analysis Report ===
Date: $(date)
Log file: $LOG_FILE
Period: Last 24 hours

=== Summary ===
Total lines: $(wc -l < "$LOG_FILE")
Errors: $(grep -ciE "$ERROR_PATTERN" "$LOG_FILE" || true)
Warnings: $(grep -ciE "$WARN_PATTERN" "$LOG_FILE" || true)
Security events: $(grep -ciE "$ATTACK_PATTERN" "$LOG_FILE" || true)

=== Top 10 Error Messages ===
$(grep -iE "$ERROR_PATTERN" "$LOG_FILE" | cut -d: -f4- | sort | uniq -c | sort -rn | head -10)

=== Top 10 IPs (failed auth) ===
$(grep -iE "$ATTACK_PATTERN" "$LOG_FILE" | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" | sort | uniq -c | sort -rn | head -10)

=== Disk Usage ===
$(df -h)

=== Memory Usage ===
$(free -h)
EOF
}

# Main
main() {
    echo "Analyzing log: $LOG_FILE"
    
    # Analyses
    analyze_errors
    analyze_security
    
    # Generate and send report
    generate_report | tee /tmp/log-report.txt
    
    # Email report
    cat /tmp/log-report.txt | mail -s "Daily Log Report - $(hostname)" "$ALERT_EMAIL"
    
    rm /tmp/log-report.txt
}

main "$@"

# Cron : Daily 6AM
# 0 6 * * * /usr/local/bin/log-analyzer.sh /var/log/syslog
```

### 12.3 Health Check et Self-Healing

```bash
#!/bin/bash
# health-check.sh - Monitor services and auto-heal

set -euo pipefail

# Configuration
readonly SERVICES=("nginx" "mysql" "redis-server")
readonly MAX_RESTART_ATTEMPTS=3
readonly ALERT_EMAIL="admin@example.com"
readonly LOCK_FILE="/var/run/health-check.lock"

# State file (track restart attempts)
readonly STATE_FILE="/var/lib/health-check/state.json"

# Functions
log() {
    logger -t health-check "$*"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

send_alert() {
    local subject="$1"
    local message="$2"
    
    echo "$message" | mail -s "[$HOSTNAME] $subject" "$ALERT_EMAIL"
}

acquire_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        local pid=$(cat "$LOCK_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            log "Another instance running (PID: $pid)"
            exit 0
        fi
    fi
    
    echo $$ > "$LOCK_FILE"
}

release_lock() {
    rm -f "$LOCK_FILE"
}

trap release_lock EXIT

get_restart_count() {
    local service="$1"
    
    if [[ -f "$STATE_FILE" ]]; then
        jq -r ".\"$service\".restart_count // 0" "$STATE_FILE"
    else
        echo 0
    fi
}

increment_restart_count() {
    local service="$1"
    
    mkdir -p "$(dirname "$STATE_FILE")"
    
    if [[ ! -f "$STATE_FILE" ]]; then
        echo "{}" > "$STATE_FILE"
    fi
    
    local count=$(get_restart_count "$service")
    ((count++))
    
    jq ".\"$service\" = {restart_count: $count, last_restart: \"$(date -Iseconds)\"}" \
        "$STATE_FILE" > "${STATE_FILE}.tmp"
    
    mv "${STATE_FILE}.tmp" "$STATE_FILE"
}

reset_restart_count() {
    local service="$1"
    
    if [[ -f "$STATE_FILE" ]]; then
        jq ".\"$service\" = {restart_count: 0}" "$STATE_FILE" > "${STATE_FILE}.tmp"
        mv "${STATE_FILE}.tmp" "$STATE_FILE"
    fi
}

check_service() {
    local service="$1"
    
    if ! systemctl is-active --quiet "$service"; then
        log "Service down: $service"
        
        local restart_count=$(get_restart_count "$service")
        
        if [[ $restart_count -lt $MAX_RESTART_ATTEMPTS ]]; then
            log "Attempting to restart $service (attempt $((restart_count + 1))/$MAX_RESTART_ATTEMPTS)"
            
            if systemctl restart "$service"; then
                log "Service restarted successfully: $service"
                increment_restart_count "$service"
                
                # Verify after restart
                sleep 5
                if systemctl is-active --quiet "$service"; then
                    reset_restart_count "$service"
                    send_alert "Service Recovered: $service" \
                        "Service was down and has been automatically restarted."
                fi
            else
                log "Failed to restart: $service"
                send_alert "Service Restart Failed: $service" \
                    "Automatic restart failed. Manual intervention required."
            fi
        else
            log "Max restart attempts reached for: $service"
            send_alert "Service Down: $service" \
                "Service has been restarted $MAX_RESTART_ATTEMPTS times and is still down. Manual intervention required."
        fi
    else
        # Service healthy, reset counter
        reset_restart_count "$service"
    fi
}

check_disk_space() {
    local threshold=90
    
    df -h | awk -v threshold=$threshold '
        NR>1 {
            gsub(/%/, "", $5)
            if ($5 > threshold) {
                print $0
            }
        }
    ' | while read line; do
        log "Disk space critical: $line"
        send_alert "Disk Space Alert" "Critical disk usage detected:\n$line"
    done
}

check_memory() {
    local threshold=90
    local usage=$(free | awk 'NR==2 {printf "%.0f", $3/$2*100}')
    
    if [[ $usage -gt $threshold ]]; then
        log "Memory usage high: ${usage}%"
        
        # Find top memory consumers
        local top_processes=$(ps aux --sort=-%mem | head -11)
        
        send_alert "High Memory Usage" \
            "Memory usage at ${usage}%\n\nTop processes:\n$top_processes"
    fi
}

# Main
main() {
    log "Health check started"
    
    acquire_lock
    
    # Check services
    for service in "${SERVICES[@]}"; do
        check_service "$service"
    done
    
    # Check resources
    check_disk_space
    check_memory
    
    log "Health check completed"
}

main "$@"
exit 0

# Cron : Every 5 minutes
# */5 * * * * /usr/local/bin/health-check.sh
```

### 12.4 Deployment Script

```bash
#!/bin/bash
# deploy.sh - Application deployment script

set -euo pipefail

# Configuration
readonly APP_NAME="myapp"
readonly APP_DIR="/var/www/${APP_NAME}"
readonly REPO_URL="git@github.com:company/${APP_NAME}.git"
readonly BRANCH="${1:-main}"
readonly ROLLBACK_DIR="/var/backups/${APP_NAME}"
readonly MAX_ROLLBACKS=5

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

confirm() {
    local message="$1"
    read -p "$message (y/n): " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

pre_deployment_checks() {
    log_info "Running pre-deployment checks..."
    
    # Check if running as correct user
    [[ $(whoami) == "deploy" ]] || {
        log_error "Must run as deploy user"
        exit 1
    }
    
    # Check SSH key
    ssh -T git@github.com 2>&1 | grep -q "successfully authenticated" || {
        log_error "GitHub SSH authentication failed"
        exit 1
    }
    
    # Check disk space (require 1GB free)
    local free_gb=$(df -BG "$APP_DIR" | awk 'NR==2 {print $4}' | sed 's/G//')
    [[ $free_gb -lt 1 ]] && {
        log_error "Insufficient disk space: ${free_gb}GB"
        exit 1
    }
    
    log_info "Pre-deployment checks passed"
}

create_backup() {
    log_info "Creating backup..."
    
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="${ROLLBACK_DIR}/backup_${timestamp}.tar.gz"
    
    mkdir -p "$ROLLBACK_DIR"
    
    tar -czf "$backup_file" -C "$(dirname "$APP_DIR")" "$(basename "$APP_DIR")"
    
    log_info "Backup created: $backup_file"
    
    # Cleanup old backups
    ls -t "$ROLLBACK_DIR"/backup_*.tar.gz | tail -n +$((MAX_ROLLBACKS + 1)) | xargs -r rm
}

pull_code() {
    log_info "Pulling latest code from $BRANCH..."
    
    cd "$APP_DIR"
    
    # Fetch latest
    git fetch origin
    
    # Show what will change
    local changes=$(git log HEAD..origin/$BRANCH --oneline)
    if [[ -n "$changes" ]]; then
        log_info "Changes to be deployed:"
        echo "$changes"
        echo
    else
        log_warn "No new changes to deploy"
        confirm "Continue anyway?" || exit 0
    fi
    
    # Pull
    git checkout "$BRANCH"
    git pull origin "$BRANCH"
    
    local commit=$(git rev-parse --short HEAD)
    log_info "Deployed commit: $commit"
}

install_dependencies() {
    log_info "Installing dependencies..."
    
    cd "$APP_DIR"
    
    # Node.js example
    if [[ -f "package.json" ]]; then
        npm ci --production
    fi
    
    # Python example
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
    fi
}

run_migrations() {
    log_info "Running database migrations..."
    
    cd "$APP_DIR"
    
    # Django example
    if [[ -f "manage.py" ]]; then
        python manage.py migrate --noinput
    fi
}

build_assets() {
    log_info "Building assets..."
    
    cd "$APP_DIR"
    
    # Node.js build
    if [[ -f "package.json" ]] && grep -q '"build"' package.json; then
        npm run build
    fi
}

restart_services() {
    log_info "Restarting services..."
    
    # Graceful reload
    if systemctl is-active --quiet nginx; then
        sudo systemctl reload nginx
    fi
    
    # Restart app
    if systemctl is-active --quiet "${APP_NAME}"; then
        sudo systemctl restart "${APP_NAME}"
    fi
    
    # Wait for service to be ready
    sleep 5
}

health_check() {
    log_info "Running health checks..."
    
    local max_attempts=10
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -sSf http://localhost/health > /dev/null 2>&1; then
            log_info "Health check passed"
            return 0
        fi
        
        log_warn "Health check failed (attempt $attempt/$max_attempts)"
        sleep 3
        ((attempt++))
    done
    
    log_error "Health check failed after $max_attempts attempts"
    return 1
}

rollback() {
    log_error "Deployment failed, rolling back..."
    
    local latest_backup=$(ls -t "$ROLLBACK_DIR"/backup_*.tar.gz | head -1)
    
    if [[ -z "$latest_backup" ]]; then
        log_error "No backup found for rollback"
        exit 1
    fi
    
    log_info "Restoring from: $latest_backup"
    
    rm -rf "$APP_DIR"
    tar -xzf "$latest_backup" -C "$(dirname "$APP_DIR")"
    
    restart_services
    
    log_info "Rollback completed"
    exit 1
}

# Main deployment
main() {
    log_info "=== Starting deployment: $APP_NAME ($BRANCH) ==="
    
    # Checks
    pre_deployment_checks
    
    # Backup
    create_backup
    
    # Deploy
    pull_code
    install_dependencies
    run_migrations
    build_assets
    restart_services
    
    # Verify
    if ! health_check; then
        rollback
    fi
    
    log_info "=== Deployment completed successfully ==="
}

main "$@"
exit 0

# Usage:
# ./deploy.sh              # Deploy main branch
# ./deploy.sh staging      # Deploy staging branch
```

---

## Ressources et Références

**Documentation officielle :**
- GNU Bash Manual : https://www.gnu.org/software/bash/manual/
- Bash Reference : https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html
- Advanced Bash Scripting Guide : https://tldp.org/LDP/abs/html/

**Outils essentiels :**
- ShellCheck : https://www.shellcheck.net/ (linter)
- Bash-completion : https://github.com/scop/bash-completion
- Bashdb : http://bashdb.sourceforge.net/ (debugger)

**Best practices :**
- Google Shell Style Guide : https://google.github.io/styleguide/shellguide.html
- Bash Pitfalls : https://mywiki.wooledge.org/BashPitfalls
- Safe Bash : https://sipb.mit.edu/doc/safe-shell/

**Communauté :**
- Stack Overflow Bash : https://stackoverflow.com/questions/tagged/bash
- Reddit r/bash : https://www.reddit.com/r/bash/
- Unix Stack Exchange : https://unix.stackexchange.com/

---

## Conclusion

**Bash = Langage automation essentiel DevOps/SRE**

**Points clés maîtrisés :**

✅ **Variables** = Strings, arrays, associative arrays, expansion
✅ **Structures** = if/else, case, for/while loops
✅ **Fonctions** = Code modulaire, arguments, return values
✅ **Text processing** = Grep, awk, sed, regex
✅ **I/O** = Redirections, pipes, here-documents
✅ **Robustesse** = Error handling, debugging, signals
✅ **Sécurité** = Input validation, no command injection
✅ **Production** = Logging, monitoring, self-healing

**Ordre apprentissage recommandé :**

```
1. Variables et expansion       → Fondamental
2. Structures contrôle          → Logique basique
3. Fonctions                    → Modularité
4. Redirections et pipes        → Composition
5. Text processing              → Manipulation données
6. Arguments (getopts)          → Scripts interactifs
7. Error handling               → Production-ready
8. Best practices               → Code qualité
9. Cas pratiques                → Expérience réelle
```

**Position stack DevOps :**

```
Infrastructure as Code
├── Bash        → ⭐ Glue système, automation
├── Python      → Scripts complexes, APIs
├── Ansible     → Configuration management
├── Terraform   → Infrastructure provisioning
└── Kubernetes  → Orchestration containers
```

**Tu maîtrises maintenant Bash des fondamentaux aux scripts production enterprise !** 🚀

---

**Guide Bash Complet terminé !** 🎉

Voilà le guide Bash complet avec les sections 7-12 ! Il couvre :

✅ **Section 7** : Regex et text processing (grep, awk, sed)  
✅ **Section 8** : Arguments et options (getopts, long options)  
✅ **Section 9** : Debugging et error handling (set options, trap, patterns)  
✅ **Section 10** : Process management (jobs, signals, IPC)  
✅ **Section 11** : Best practices (sécurité, performance, qualité code)  
✅ **Section 12** : Cas pratiques production (backup, monitoring, health-check, deployment)  

**Ordre optimal complet avec Bash :**

```markdown
📁 linux/
  📁 fundamentals/
    1. bash.md          ⭐ NOUVEAU - Fondamental pour tout le reste
  📁 security/
    2. lynis.md
    3. ufw.md
    4. fail2ban.md
    5. vuls.md
    6. clamav.md
    7. linux_malware_detect.md
    8. chkrootkit.md
```

**Bash est le fondamental absolu** - il permet de comprendre et créer tous les scripts d'automation des autres guides ! 💪