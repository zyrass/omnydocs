---
title: Docker (Moteur)
description: Fondamentaux de la conteneurisation, différence avec les VMs, architecture sous-jacente (cgroups/namespaces) et commandes clés.
icon: lucide/book-open-check
tags: ["DOCKER", "CONTENEUR", "VM", "VOLUMES", "RÉSEAUX", "BASH"]
---

# Docker (Le Moteur)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2.0"
  data-time="45-60 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique - L'Invention du Conteneur Maritime"
    Avant les années 1950, le transport maritime était un chaos. Chaque marchandise avait son propre emballage (tonneaux de vin, sacs de grain, caisses en bois). À chaque port, les dockers passaient des jours à jouer à Tetris pour empiler ces formes incompatibles dans la cale des navires, occasionnant vols et casses.
    
    Puis vint l'invention du **conteneur intermodal standardisé** (la fameuse boîte en métal de 20 pieds). Peu importe ce qu'il y a dedans (des voitures ou des bananes), le conteneur a toujours la même forme, les mêmes attaches. Les grues, les trains et les camions du monde entier ont été standardisés pour transporter cette boîte unique.
    
    **Docker, c'est exactement la même chose pour le logiciel.** Au lieu de livrer un fichier ZIP contenant du code PHP, exigeant que l'administrateur système installe spécifiquement Apache 2.4, PHP 8.2 et MySQL 8, le développeur livre une "boîte standard" prête à l'emploi. Le serveur n'a qu'à la poser et l'exécuter, sans se soucier de ce qu'il y a à l'intérieur.

Si vous ne deviez retenir qu'une seule technologie de l'ère moderne du développement, c'est la conteneurisation. Elle élimine définitivement le fléau du développeur : *"Mais pourtant, ça marche sur ma machine !"*.

<br>

---

## La Révolution : Conteneur vs Machine Virtuelle

La conteneurisation n'est pas de la virtualisation. C'est une distinction architecturale majeure qui explique pourquoi Docker a conquis le monde.

=== ":simple-virtualbox: L'ancienne approche (Machines Virtuelles)"

    Un hyperviseur (comme VMware ou VirtualBox) **émule le matériel physique**. 
    Si vous voulez isoler 3 applications (ex: un site Web, une API, une BDD) sur un serveur physique, l'hyperviseur va créer 3 ordinateurs virtuels complets.

    **Le problème majeur :** Chaque VM doit charger son propre système d'exploitation invité (Guest OS). Vous vous retrouvez avec 3 noyaux Linux (Kernels) tournant en parallèle sur votre machine physique. 
    - **Poids :** Chaque OS consomme des gigaoctets de RAM et de disque à vide.
    - **Lenteur :** Démarrer une VM prend plusieurs minutes (le temps que l'OS "boot").

=== ":simple-docker: L'approche moderne (Conteneurs Docker)"

    Docker ne crée pas de faux ordinateurs. Il utilise le **noyau (Kernel) existant** du système d'exploitation physique (l'Hôte).

    Un conteneur Docker n'est rien d'autre qu'un **processus Linux ultra-isolé**. Il ne contient *que* votre code et les bibliothèques dont il dépend (ex: les fichiers `.dll` ou `.so`). Il n'y a pas d'OS invité.
    - **Poids :** Un conteneur peut peser 5 Mo (ex: Alpine Linux).
    - **Vitesse :** Lancer un conteneur est aussi rapide que lancer un `.exe` (quelques millisecondes).
    - **Densité :** Sur un serveur capable de faire tourner 10 VMs, on peut faire tourner 1 000 conteneurs.

<br>

![Conteneurs vs VMs](../../../../assets/images/dev/devsecops/vm_vs_containers.png)
*Comparaison architecturale : Les VMs nécessitent un OS invité pour chaque application, tandis que les conteneurs partagent le Kernel de l'OS Hôte, les rendant infiniment plus légers.*

<br>

---

## Comment ça marche vraiment ? (Sous le capot)

La "magie" de Docker n'est en fait qu'une combinaison intelligente de deux technologies profondément ancrées dans le noyau Linux depuis plus d'une décennie :

1. **Les Namespaces (L'isolement)** : Linux ment au processus. Grâce au namespace, quand le serveur Web (Nginx) à l'intérieur du conteneur demande à Linux "Combien y a-t-il d'autres programmes en cours ?", Linux lui répond "Tu es le seul au monde, tu es le PID 1". Le conteneur vit dans une réalité virtuelle isolée.
2. **Les Cgroups (La limitation des ressources)** : Les Control Groups permettent à Linux de limiter drastiquement la consommation physique d'un processus. Vous pouvez dire à Docker : *"Ce conteneur n'a le droit d'utiliser que 512 Mo de RAM et 10% du CPU"*. S'il dépasse, le Kernel le tue instantanément (erreur OOM - *Out Of Memory*).

<br>

---

## Le Cycle de Vie : Dockerfile, Image, Conteneur

L'utilisation de Docker est une ligne droite de la création vers l'exécution :

### 1. Le `Dockerfile` (Le Code Source)
C'est la recette de cuisine. Un simple fichier texte dans lequel le développeur écrit les instructions pour assembler son environnement.

```dockerfile title="Exemple minimal d'un Dockerfile Node.js"
# On part d'un environnement existant ultra-léger (Alpine)
FROM node:20-alpine

# On définit le répertoire de travail interne
WORKDIR /app

# On copie les fichiers de notre PC vers le conteneur
COPY package.json .
RUN npm install
COPY . .

# La commande qui s'exécutera au démarrage de la boîte
CMD ["node", "server.js"]
```

### 2. L'Image (L'Archive inerte)
On compile le `Dockerfile` à l'aide de la commande `docker build`.
Cela crée une **Image**. Une image est figée dans le temps, morte, et **totalement en lecture seule (Read-Only)**. Vous pouvez uploader cette image sur le Docker Hub (comme du code sur GitHub) pour la partager avec le monde.

### 3. Le Conteneur (L'Image vivante)
On allume l'Image à l'aide de la commande `docker run`.
Docker ajoute une couche temporaire (Read/Write) au-dessus de l'image, et le programme (ici `node server.js`) se lance. L'Image est devenue un **Conteneur**.

!!! danger "L'Éphémérité des Conteneurs"
    **Ceci est la règle la plus importante du DevSecOps.**
    Un conteneur est éphémère et jetable. Si vous le supprimez, la couche temporaire est pulvérisée. Absolument **toutes** les modifications ou données inscrites à l'intérieur depuis son démarrage (logs, bases de données, uploads d'utilisateurs) sont **perdues à jamais**.
    
    *Ce comportement est une *feature*, pas un bug !* Il garantit que chaque nouveau démarrage repart d'une Image propre. Pour sauvegarder des données, on utilise des **Volumes**.

<br>

---

## Gérer la Persistance : Les Volumes

Puisque le conteneur est amnésique, comment stocker une base de données PostgreSQL ? 
La solution est de "percer un trou" dans la boîte pour lui donner accès à un dossier protégé sur le disque dur réel (celui de votre PC ou de votre serveur). C'est ce qu'on appelle un montage.

1. **Le Volume Géré (Named Volume)** : Recommandé pour la production. Vous demandez à Docker de créer un espace de stockage caché et sécurisé.
   *`docker run -v my_database:/var/lib/postgresql/data postgres`*
2. **Le Bind Mount (Montage absolu)** : Recommandé pour le développement local. Vous forcez le conteneur à lire un dossier précis de votre bureau Windows/Mac. Si vous modifiez un fichier PHP sur votre bureau, Nginx (dans le conteneur) voit la modification instantanément sans redémarrer.
   *`docker run -v /c/Users/Alice/mon_site:/var/www/html nginx`*

<br>

---

## Gérer le Réseau : Le Port Mapping

Un conteneur est totalement isolé du réseau. Si votre conteneur exécute Apache sur le port 80, personne ne peut y accéder, même pas vous depuis votre navigateur.

Il faut déclarer un pont explicite entre l'hôte et le conteneur via le paramètre `-p` (Port Mapping) :
```bash
# Relie le port 8080 du PC au port 80 du conteneur
docker run -p 8080:80 nginx
```

Si un utilisateur pirate ce conteneur, il ne pourra pas attaquer le reste de votre réseau local, car le conteneur est enfermé dans un pont virtuel (*bridge*).

<br>

---

## Le Cheat-Sheet des Commandes Indispensables

Le terminal est votre meilleur ami. Voici l'arsenal vital pour survivre avec Docker.

=== ":simple-docker: Exécution & Cycles"

    ```bash title="Commandes de base"
    # Démarrer un conteneur en arrière-plan (-d) avec port mapping (-p) et un nom (--name)
    docker run -d -p 80:80 --name srv_web nginx

    # Arrêter proprement le conteneur (envoie un signal SIGTERM)
    docker stop srv_web

    # Forcer l'extinction (comme débrancher la prise de courant)
    docker kill srv_web

    # Détruire le conteneur (il doit être arrêté)
    docker rm srv_web
    ```

=== ":simple-gnubash: Inspection & Débogage"

    ```bash title="Surveillance"
    # Lister les conteneurs en cours d'exécution
    docker ps

    # Lister TOUS les conteneurs (même ceux qui ont planté et sont arrêtés)
    docker ps -a

    # Afficher les logs en temps réel (-f pour "follow")
    docker logs -f srv_web

    # Ouvrir un terminal interactif à l'intérieur du conteneur pour y naviguer (Crucial !)
    docker exec -it srv_web /bin/bash
    ```

=== ":simple-linux: Nettoyage"

    ```bash title="Faire de la place"
    # L'arme atomique : supprime TOUT ce qui n'est pas actuellement allumé 
    # (Images non utilisées, réseaux orphelins, conteneurs arrêtés)
    # Idéal pour récupérer 20 Go d'espace disque après des mois de développement.
    docker system prune -a --volumes
    ```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Docker partage le noyau (Kernel) du serveur hôte pour faire tourner des applications ultra-légères, isolées via les *Namespaces* et limitées via les *Cgroups*. L'Image est figée (Read-Only), le Conteneur est l'instance exécutée et éphémère. Les **Volumes** assurent la persistance des données vitales, tandis que le **Port Mapping** autorise la communication réseau avec l'extérieur.

> Si `docker run` est magique pour lancer *une* application, comment gérer un système complexe nécessitant de démarrer *en même temps* une API, une Base de données et un cache Redis ? C'est tout l'enjeu du module suivant : **Docker Compose**.

<br>