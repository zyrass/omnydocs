---
title: 3.18 Préparation MacBook M1 forensic
description: Configuration du MacBook M1 personnel comme cible d'analyse forensic. FileVault, Time Machine, comptes utilisateurs, données fictives, installation outils CLI, validation pré-acquisition.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - MacBook M1
  - macOS
  - Apple Silicon
  - Préparation
data-level: 🔴
---

# 3.18 Préparation MacBook M1 forensic

!!! quote "L'analogie du patient consentant"

    Un médecin légiste ne peut pas autopsier un patient au hasard. Il faut un consentement, ou un cadre légal. Dans votre laboratoire, votre MacBook M1 personnel est ce patient consentant. Vous allez le configurer pour qu'il devienne une cible réaliste d'analyse forensic, avec des données réelles, des configurations réalistes, des artefacts représentatifs. Mais avant, faites-en une sauvegarde complète. Une fois l'analyse pratique commencée, certaines actions seront destructrices.

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 4 heures |
| Niveau | Pratique |
| Prérequis | MacBook M1 (le vôtre), 2.4 bis, 2.10 bis |

## 1. État de référence avant configuration

### 1.1 Sauvegarde Time Machine OBLIGATOIRE

```bash
# Vérifier disque externe Time Machine
diskutil list

# Lancer sauvegarde
sudo tmutil startbackup --block

# Vérifier
tmutil latestbackup
```

### 1.2 Documentation état initial

```bash
# Créer un dossier de documentation
mkdir -p ~/Documents/lab-mac-m1
cd ~/Documents/lab-mac-m1

# État système initial
{
  echo "=== ÉTAT INITIAL MACBOOK M1 ==="
  echo "Date : $(date -u)"
  echo
  echo "=== HARDWARE ==="
  system_profiler SPHardwareDataType
  echo
  echo "=== OS ==="
  sw_vers
  echo
  echo "=== UTILISATEURS ==="
  dscl . -list /Users | grep -v ^_
  echo
  echo "=== APPS ==="
  ls /Applications/
  echo
  echo "=== FILEVAULT ==="
  fdesetup status
  echo
  echo "=== SIP ==="
  csrutil status
  echo
  echo "=== APFS ==="
  diskutil apfs list
} > etat-initial.txt
```

## 2. Installation des outils CLI

### 2.1 Xcode Command Line Tools

```bash
# Installation
xcode-select --install

# Confirmation
xcode-select -p
```

### 2.2 Homebrew

```bash
# Installation Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Configuration shell
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# Vérification
brew doctor
```

### 2.3 Outils essentiels

```bash
# Outils forensic et CLI
brew install \
    coreutils \
    findutils \
    gnu-sed \
    git \
    python@3.11 \
    sqlite \
    jq \
    htop \
    wireshark \
    nmap \
    tcpdump
```

### 2.4 Outils forensic spécifiques

```bash
# mac_apt (via pip)
pip3 install mac_apt

# Préparer dossier outils
mkdir -p ~/forensic-tools
cd ~/forensic-tools

# AutoMacTC
git clone https://github.com/CrowdStrike/automactc.git
cd automactc
pip3 install -r requirements.txt
cd ..

# osxcollector (alternative)
git clone https://github.com/Yelp/osxcollector.git
```

## 3. Configuration utilisateurs réalistes

### 3.1 Conserver utilisateur principal

Votre utilisateur principal sur le Mac reste tel quel.

### 3.2 Créer un utilisateur secondaire

```bash
# Créer utilisateur "amis" simulant un compte invité régulier
sudo dscl . -create /Users/amis
sudo dscl . -create /Users/amis UserShell /bin/zsh
sudo dscl . -create /Users/amis RealName "Compte Amis"
sudo dscl . -create /Users/amis UniqueID 510
sudo dscl . -create /Users/amis PrimaryGroupID 20
sudo dscl . -create /Users/amis NFSHomeDirectory /Users/amis
sudo dscl . -passwd /Users/amis "AmisLab2026"
sudo createhomedir -c -u amis
```

## 4. Données fictives réalistes

### 4.1 Documents

```bash
# Documents typiques d'un utilisateur
DOCS_PATH=~/Documents/CasFictifs
mkdir -p $DOCS_PATH

# Documents personnels fictifs
echo "Données fiscales 2025 - simulation" > $DOCS_PATH/fiscalite_2025.pdf
echo "Mots de passe à mémoriser" > $DOCS_PATH/passwords_a_memoriser.txt  # piège classique
echo "Coordonnées clients ARTECH" > $DOCS_PATH/clients_artech.csv
echo "Présentation projet IT" > $DOCS_PATH/projet_IT_2026.pptx

# Photos fictives
mkdir -p ~/Pictures/CasFictifs
touch ~/Pictures/CasFictifs/IMG_{0001..0020}.jpg
```

### 4.2 Historique navigation

```bash
# Lancer Safari plusieurs fois sur des sites différents
open -a Safari "https://www.google.com"
sleep 5
open -a Safari "https://www.lemonde.fr"
sleep 5
open -a Safari "https://github.com"

# Ces visites seront en historique - artefact forensic réaliste
```

### 4.3 Téléchargements

```bash
# Quelques fichiers téléchargés (avec quarantine flag)
cd ~/Downloads
curl -O https://www.gnu.org/licenses/gpl-3.0.txt
curl -O https://www.kernel.org/doc/html/latest/_sources/index.rst.txt

# Vérifier quarantine attribué
xattr -l ~/Downloads/gpl-3.0.txt
```

## 5. Activer FileVault

```bash
# Si pas déjà actif
sudo fdesetup enable

# Sauvegarder la recovery key !
# La noter sur papier OU dans KeePass dédié
```

## 6. Quelques modifications pour artefacts forensic

### 6.1 LaunchAgent personnel (légitime)

```bash
# Créer un LaunchAgent qui lance un script à la connexion
mkdir -p ~/Library/LaunchAgents
cat > ~/Library/LaunchAgents/com.zyrass.welcome.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.zyrass.welcome</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>echo "Welcome \$(whoami) on \$(hostname)" >> /tmp/welcome.log</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.zyrass.welcome.plist
```

### 6.2 Utilisation Spotlight

```bash
# Forcer Spotlight à indexer (artefacts)
sudo mdutil -E /
sudo mdutil -i on /
```

## 7. Test de validation

```bash
# Script test rapide
cat > ~/forensic-tools/test-prep.sh <<'EOF'
#!/bin/bash
echo "=== TEST PRÉPARATION MAC M1 ==="

# Vérifier outils installés
for tool in brew git python3 nmap sqlite3 jq; do
    if command -v $tool &> /dev/null; then
        echo "[OK] $tool"
    else
        echo "[FAIL] $tool"
    fi
done

# Vérifier mac_apt
python3 -c "import mac_apt" 2>/dev/null && echo "[OK] mac_apt" || echo "[FAIL] mac_apt"

# Vérifier FileVault
fdesetup status | grep "is On" && echo "[OK] FileVault" || echo "[WARN] FileVault"

# Vérifier données fictives
ls ~/Documents/CasFictifs/*.pdf > /dev/null 2>&1 && echo "[OK] Documents fictifs"
ls ~/Pictures/CasFictifs/*.jpg > /dev/null 2>&1 && echo "[OK] Photos fictives"

# Vérifier LaunchAgent
test -f ~/Library/LaunchAgents/com.zyrass.welcome.plist && echo "[OK] LaunchAgent test"

echo "=== FIN TEST ==="
EOF

chmod +x ~/forensic-tools/test-prep.sh
~/forensic-tools/test-prep.sh
```

## 8. Documenter l'état préparé

```bash
{
  echo "=== ÉTAT PRÉPARÉ MACBOOK M1 ==="
  echo "Date : $(date -u)"
  echo "Préparation forensic OmnyAcademy"
  echo
  echo "Modifications apportées :"
  echo "- Compte 'amis' créé (UID 510)"
  echo "- Documents fictifs dans ~/Documents/CasFictifs"
  echo "- Photos fictives dans ~/Pictures/CasFictifs"
  echo "- LaunchAgent com.zyrass.welcome (légitime)"
  echo "- FileVault activé"
  echo "- Outils brew installés"
  echo "- mac_apt installé"
  echo "- AutoMacTC installé"
  echo
  echo "Sauvegarde Time Machine OK avant modifications"
  echo "Recovery FileVault sauvegardée hors machine"
} > ~/Documents/lab-mac-m1/etat-prepare.txt
```

## 9. Sécurité et précautions

```text
RAPPELS
========

1. Sauvegarde Time Machine COMPLÈTE faite avant cette
   préparation. En cas de problème, restauration possible.

2. Recovery key FileVault notée sur papier ET dans KeePass.
   La perte de cette clé = perte définitive des données.

3. Le compte "amis" est un compte simulé. Le supprimer
   après les exercices forensic si non souhaité :
   sudo dscl . -delete /Users/amis
   sudo rm -rf /Users/amis

4. Les modifications réalisées ici sont RÉVERSIBLES
   en restaurant Time Machine.

5. NE PAS pratiquer de vraie attaque sur ce Mac, c'est
   votre poste personnel. Les attaques se font sur les
   postes Windows du labo dédié.
```

## 10. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Sauvegarde avant ? | Time Machine complète |
| 2 | Outil de gestion paquets ? | Homebrew |
| 3 | Outil forensic Python ? | mac_apt, AutoMacTC |
| 4 | Activation FileVault ? | `sudo fdesetup enable` |
| 5 | Voir attribut quarantine ? | `xattr -l fichier` |
| 6 | LaunchAgent location ? | `~/Library/LaunchAgents/` |

---

**Chapitre suivant** : [3.19 Outils forensic macOS approfondis](03-19-outils-forensic-macos.md)
