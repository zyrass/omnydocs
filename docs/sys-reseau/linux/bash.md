---
description: "Maîtriser le shell Bash : navigation, manipulation de texte, redirections et scripting automatisé."
icon: lucide/book-open-check
tags: ["BASH", "SHELL", "LINUX", "SCRIPTING", "CLI"]
---

# Shell & Scripting (Bash)

<div
  class="omny-meta"
  data-level="🟢 Débutant à 🟡 Intermédiaire"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Bash est le volant et les pédales de votre serveur Linux. Là où une interface graphique vous limite aux boutons prévus par le constructeur, maîtriser la ligne de commande vous permet de manipuler les rouages internes de la machine avec une précision chirurgicale._

!!! quote "L'interface absolue"
    _Une interface graphique (GUI) vous limite aux actions que son créateur a prévues. L'interface en ligne de commande (CLI), via un shell comme **Bash**, vous donne un accès illimité et programmable à chaque atome du système d'exploitation. C'est l'outil universel de l'administrateur système._

## Qu'est-ce que Bash ?

**Bash** (Bourne-Again shell) est l'interpréteur de commandes par défaut sur la très grande majorité des distributions GNU/Linux (Ubuntu, Debian, RHEL). Il joue deux rôles majeurs :
1. **Un interpréteur interactif** : Il écoute ce que vous tapez au clavier et l'exécute immédiatement.
2. **Un langage de programmation** : Il permet de regrouper ces commandes dans des fichiers (`.sh`) pour automatiser des tâches complexes (Scripting).

---

## 1. L'Art des Redirections (Flux Standard)

Le concept fondamental d'Unix est que "Tout est fichier". Un programme qui s'exécute ne "parle" pas directement à l'écran, il écrit dans des flux de données abstraits.

```mermaid
graph LR
    Entree[Clavier / Fichier] -->|stdin 0| Programme[Programme Exécutable]
    Programme -->|stdout 1| Sortie[Écran / Fichier]
    Programme -->|stderr 2| Erreur[Écran / Fichier d'Erreur]
    
    style Programme fill:#1a5276,stroke:#fff,stroke-width:2px,color:#fff
    style Entree fill:#2c3e50,stroke:#fff,color:#fff
    style Sortie fill:#27ae60,stroke:#fff,color:#fff
    style Erreur fill:#c0392b,stroke:#fff,color:#fff
```

En Linux, tout programme possède trois flux standards :
- `stdin` (0) : L'entrée standard (le clavier par défaut).
- `stdout` (1) : La sortie standard (l'écran).
- `stderr` (2) : La sortie d'erreur (l'écran aussi).

Bash permet de manipuler ces flux avec une puissance redoutable.

### Redirection de Sortie (`>` et `>>`)
Plutôt que d'afficher le résultat d'une commande à l'écran, on l'écrit dans un fichier.
```bash
# Écrase le fichier s'il existe
echo "Ceci est un test" > fichier.txt

# Ajoute à la fin du fichier (Append)
echo "Une autre ligne" >> fichier.txt
```

### La Tuyauterie : Le Pipe (`|`)
C'est le concept le plus puissant d'Unix. Il prend la sortie standard de la commande de gauche, et l'injecte dans l'entrée standard de la commande de droite.
```bash
# Liste tous les fichiers, et filtre (grep) uniquement ceux contenant "conf"
ls -la /etc | grep "conf"
```

!!! tip "Le trou noir (/dev/null)"
    Si une commande génère des erreurs que vous voulez ignorer, redirigez `stderr` (le flux 2) vers `/dev/null` (un fichier spécial qui détruit tout ce qu'on y envoie).
    `find / -name "secret.txt" 2> /dev/null`

---

## 2. Manipulation de Texte (Les Couteaux Suisses)

Un administrateur passe son temps à chercher des informations dans des fichiers de logs immenses. Ces trois commandes sont indispensables.

<div class="grid cards" markdown>

-   :lucide-search:{ .lg .middle } **`grep` (Recherche)**

    ---
    Cherche une chaîne (ou une expression régulière) dans un fichier.
    ```bash
    # Cherche "Failed password" dans les logs
    grep "Failed password" /var/log/auth.log
    ```

-   :lucide-scissors:{ .lg .middle } **`awk` (Extraction de colonnes)**

    ---
    Excellent pour traiter des fichiers tabulaires.
    ```bash
    # Affiche uniquement la première colonne (l'IP) du log
    awk '{print $1}' /var/log/apache2/access.log
    ```

-   :lucide-replace:{ .lg .middle } **`sed` (Remplacement)**

    ---
    L'éditeur de flux par excellence.
    ```bash
    # Remplace "Port 22" par "Port 2222"
    sed -i 's/Port 22/Port 2222/g' /etc/ssh/sshd_config
    ```

</div>

---

## 3. Le Scripting Bash

Un script bash commence toujours par un **Shebang** (`#!/bin/bash`), qui indique au système quel interpréteur utiliser. Il doit être rendu exécutable (`chmod +x script.sh`).

### Variables et Arguments
```bash
#!/bin/bash

# Variable (Pas d'espace autour du =)
BACKUP_DIR="/tmp/backup"

# Utilisation des arguments passés au script ($1, $2...)
echo "Bonjour $1, début de la sauvegarde vers $BACKUP_DIR"
```

### Conditions (If / Else)
Attention à la syntaxe stricte (espaces autour des crochets).
```bash
#!/bin/bash

if [ -d "/var/www/html" ]; then
    echo "Le répertoire web existe."
else
    echo "Répertoire introuvable !"
    exit 1
fi
```
*(Opérateurs courants : `-d` pour répertoire, `-f` pour fichier, `-z` pour chaîne vide).*

### Boucles (For / While)
Utile pour traiter plusieurs fichiers ou lignes.
```bash
#!/bin/bash

# Renommer tous les fichiers .txt en .bak
for file in *.txt; do
    mv "$file" "${file%.txt}.bak"
    echo "Fichier $file renommé."
done
```

## Conclusion

Maîtriser Bash, c'est comme apprendre à taper au clavier : c'est un investissement initial qui vous fera gagner des milliers d'heures tout au long de votre carrière. Avant d'installer des usines à gaz comme Ansible ou Chef pour configurer un serveur, demandez-vous toujours : *"Un script Bash de 10 lignes ne suffirait-il pas ?"*

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    L'administration Linux repose sur la maîtrise de la ligne de commande et la compréhension de la philosophie Unix (tout est fichier). L'automatisation via des scripts Bash est la clé de la scalabilité pour gérer des parcs de serveurs.

> [Retourner à l'index Linux →](./index.md)
