[![Netlify Status](https://api.netlify.com/api/v1/badges/7d23ede9-b221-4615-a001-f8704bbc523f/deploy-status)](https://app.netlify.com/projects/omnydocs/deploys)

# OmnyDocs

OmnyDocs est un espace de documentation centralisé conçu pour explorer et transmettre les concepts fondamentaux de l'informatique. Il couvre un large spectre allant du développement web à la cybersécurité. Ce projet s'appuie sur le générateur de site statique **Zensical** pour compiler et servir ses pages.

Tout comme un artisan organise son atelier en disposant des boîtes à outils étiquetées et isolées pour chaque type de travail afin d'éviter de mélanger les outils de plomberie et d'électricité, OmnyDocs utilise Python et un environnement virtuel pour séparer ses dépendances du reste du système d'exploitation. Cette isolation garantit un espace de travail propre, stable et reproductible.

<br>

---

## 💻 Configuration pour Windows 11

Pour travailler sur cette documentation en local sous Windows 11, vous devez configurer votre environnement de développement. Exécutez les étapes ci-dessous dans votre terminal (PowerShell ou Invite de commandes).

### 🏷️ [Label : Initialisation] Création de l'environnement virtuel

```bash title="Création de l'environnement virtuel Python"
# Crée un environnement virtuel isolé nommé ".venv" dans le dossier du projet
py -m venv .venv
```

_Cette commande utilise l'exécuteur Python universel de Windows (`py`) pour initialiser un sous-dossier étanche nommé `.venv`. Ce dossier contiendra son propre interpréteur et ses propres paquets indépendamment du système global._

### 🏷️ [Label : Activation] Activation de l'environnement virtuel

```powershell title="Activation de l'environnement sous Windows 11"
# Active l'environnement virtuel dans la session PowerShell actuelle
.\.venv\Scripts\activate
```

_L'activation redirige temporairement les variables d'environnement de votre terminal actuel vers le dossier `.venv`. Ainsi, toutes les commandes Python et les paquets installés s'exécuteront dans ce contexte isolé._

### 🏷️ [Label : Mise à jour] Mise à jour du gestionnaire de paquets (pip)

```bash title="Mise à jour de pip dans l'environnement virtuel"
# Met à jour pip vers sa dernière version stable au sein de l'environnement virtuel
py -m pip install --upgrade pip
```

_Mettre à jour le gestionnaire de paquets `pip` permet d'obtenir les derniers correctifs de sécurité et garantit une installation sans erreur des dépendances de Zensical._

### 🏷️ [Label : Installation] Déploiement de Zensical

```bash title="Installation de la bibliothèque Zensical"
# Installe Zensical et ses dépendances logicielles au sein de l'environnement virtuel
pip install zensical
```

_Cette commande télécharge le moteur de rendu Zensical depuis les serveurs officiels et l'installe au sein de l'environnement virtuel activé pour permettre la compilation locale du projet._

<br>

---

## 🛠️ Génération et Utilisation locale

Une fois votre environnement configuré, vous pouvez assembler les fichiers de configuration et démarrer le serveur de prévisualisation local.

### ⚙️ Génération de la configuration globale

Le projet assemble sa navigation et sa configuration depuis plusieurs sous-fichiers TOML. Générez le fichier de configuration principal `zensical.toml` avant de démarrer le serveur :

```bash title="Génération de la configuration via Python"
# Lance le script python d'assemblage des fragments TOML
python scripts/generate-zensical.py
```

_Ce script python parcourt les fragments de configuration dans `config/toml/` et les fusionne pour générer le fichier `zensical.toml` requis à la racine._

Si vous préférez utiliser PowerShell nativement :

```powershell title="Génération de la configuration via PowerShell"
# Lance le script PowerShell pour assembler le fichier zensical.toml
.\scripts\generate-zensical.ps1
```

_Ce script PowerShell réalise le même assemblage de fichiers en s'assurant d'utiliser un encodage UTF-8 sans signature (BOM) compatible avec le compilateur._

### 🚀 Lancement du serveur local

```bash title="Lancement du serveur de développement local"
# Démarre le serveur web local avec rechargement à chaud automatique
zensical serve
```

_Zensical démarre alors un serveur Web de test local. Vous pouvez visualiser le rendu en temps réel en ouvrant l'adresse indiquée (généralement `http://127.0.0.1:8000`) dans votre navigateur._

### 🔄 Maintenance et Mise à jour de Zensical

Pour vérifier votre version ou forcer une réinstallation propre :

```bash title="Vérification et réinstallation de Zensical"
# Connaître la version de Zensical actuellement installée
pip show zensical

# Forcer la réinstallation et la mise à jour complète de Zensical
pip install --upgrade --force-reinstall zensical
```

_Ces commandes permettent de diagnostiquer la version active et de résoudre rapidement les anomalies de dépendances en réinstallant proprement le moteur._

<br>

---

## Conclusion

!!! quote "Résumé de la configuration"
    La configuration d'un environnement isolé sous Windows 11 est une étape essentielle et rapide pour exécuter OmnyDocs. L'utilisation de Zensical offre un confort moderne de rédaction technique avec une prévisualisation instantanée.

> Consultez la section [Environnements virtuels (VENV)](file:///j:/www/Omnyvia/omnydocs/docs/bases/outils/environnement-virtuel/venv.md) pour en savoir plus sur l'isolation des projets.
