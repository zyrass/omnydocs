---
title: Docker Compose
description: Orchestration locale, réseaux internes natifs, variables d'environnement et syntaxe YAML pour déployer des stacks applicatives.
icon: lucide/book-open-check
tags: ["DOCKER", "COMPOSE", "YAML", "RESEAU", "ORCHESTRATION"]
---

# Docker Compose : L'Orchestration Locale

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2.0"
  data-time="45-60 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Chef d'Orchestre"
    Si la commande `docker run` est un musicien solitaire (un violoniste par exemple), alors une application d'entreprise est un **orchestre symphonique**.
    
    Vous avez besoin d'un violon (le serveur Web), d'un piano (la base de données) et de percussions (un cache Redis). Vous *pourriez* demander à chaque musicien de commencer à jouer séparément, en espérant qu'ils se synchronisent.
    
    **Docker Compose est le chef d'orchestre.** Vous lui donnez une partition unique (le fichier `docker-compose.yml`), et d'un seul mouvement de baguette, il fait entrer chaque musicien dans le bon ordre, en s'assurant qu'ils jouent tous sur le même tempo (le réseau virtuel).

La philosophie du DevSecOps (Infrastructure as Code) interdit formellement de lancer des serveurs avec des commandes manuelles kilométriques. Compose permet de **déclarer** l'architecture souhaitée dans un fichier versionnable.

<br>

---

## De l'Impératif (Bash) au Déclaratif (YAML)

Imaginons le déploiement d'un blog WordPress qui dépend d'une base de données MariaDB.

=== ":simple-gnubash: L'approche Bash (Impérative)"

    Pour déployer cette architecture avec le moteur Docker classique, le SysAdmin doit exécuter ces commandes manuelles :

    ```bash title="Commandes manuelles (Risqué en production)"
    # 1. Créer manuellement un réseau virtuel pour que les conteneurs se parlent
    docker network create wp_network
    
    # 2. Démarrer la BDD en attachant le réseau, un volume, et des variables
    docker run -d --name db \
      --network wp_network \
      -v wp_data:/var/lib/mysql \
      -e MYSQL_ROOT_PASSWORD=secret \
      -e MYSQL_DATABASE=wordpress \
      mariadb:10.6
      
    # 3. Démarrer WordPress en priant pour que la BDD soit prête
    docker run -d --name web \
      --network wp_network \
      -p 8080:80 \
      -e WORDPRESS_DB_HOST=db:3306 \
      -e WORDPRESS_DB_PASSWORD=secret \
      wordpress:latest
    ```

    *Problème : Si le serveur redémarre, qui va retaper ces commandes ? Personne.*

=== ":simple-docker: L'approche Compose (Déclarative)"

    Nous déclarons simplement l'état final souhaité dans un fichier standard. Compose s'occupera de créer le réseau par défaut et de lancer les processus dans le bon ordre.

    ```yaml title="docker-compose.yml"
    version: '3.8' # Version de l'API Compose
    
    services:
      # --- Service 1 : La Base de données ---
      db:
        image: mariadb:10.6
        restart: unless-stopped # Redémarre seul si le conteneur crashe
        volumes:
          - wp_data:/var/lib/mysql
        environment:
          MYSQL_ROOT_PASSWORD: secret
          MYSQL_DATABASE: wordpress
    
      # --- Service 2 : Le Serveur Web ---
      web:
        image: wordpress:latest
        depends_on:
          - db # Compose attendra que 'db' soit lancé avant de lancer 'web'
        ports:
          - "8080:80" # Mapping du port vers l'extérieur (le PC)
        environment:
          WORDPRESS_DB_HOST: db:3306 # Le nom du service devient l'adresse IP !
          WORDPRESS_DB_PASSWORD: secret
    
    # Déclaration globale des volumes virtuels requis
    volumes:
      wp_data:
    ```

<br>

---

## La Magie du Réseau Interne (DNS Résolution)

L'un des plus grands pouvoirs de Docker Compose est sa gestion automatique du réseau (*Bridge Network*).

Lorsque vous lancez `docker compose up`, Compose crée un réseau virtuel fermé (par exemple nommé `projet_default`). Il y place tous vos services.

!!! tip "Le Résolveur DNS Interne"
    Vous n'avez **jamais** besoin de gérer ou de connaître les adresses IP (ex: `172.17.0.4`) de vos conteneurs. Docker intègre un DNS interne. 
    **Le nom du service défini dans le YAML devient automatiquement son nom de domaine**.
    
    C'est pour cela que dans l'exemple ci-dessus, WordPress se connecte à la base de données simplement en ciblant l'URL `db` sur le port `3306`.

### Isoler les services par sécurité (AppSec)

Dans un environnement DevSecOps mature, on ne met pas tous les services sur le même réseau. On crée des réseaux distincts pour compartimenter l'architecture (principe du *Moindre Privilège*).

```yaml title="Compartimentation réseau avancée"
services:
  web:
    image: nginx
    networks:
      - frontend   # Connecté à Internet
      - backend    # Peut parler à l'API
      
  api:
    image: node
    networks:
      - backend    # Parle au Web et à la BDD
      - db_net
      
  database:
    image: postgres
    networks:
      - db_net     # Isolée de manière étanche. Le serveur Web ne peut PAS la contacter.

networks:
  frontend:
  backend:
  db_net:
```

<br>

---

## Sécurité : Le problème des variables en clair

Dans notre premier exemple YAML, les mots de passe (`secret`) sont écrits en clair. Si vous "pushez" ce fichier sur GitHub, votre base de données est compromise.

En DevSecOps, on utilise un fichier caché nommé `.env` (qui ne doit **jamais** être versionné sur Git) pour stocker les secrets.

=== ":simple-dotenv: Fichier .env (Ignoré par Git)"

    ```bash title=".env"
    # Fichier stocké uniquement sur le serveur de production
    DB_ROOT_PASS=hQ9!mX2$vL
    APP_PORT=8080
    ```

=== ":simple-yaml: Fichier docker-compose.yml"

    ```yaml title="docker-compose.yml"
    services:
      db:
        image: mariadb:10.6
        environment:
          # Compose ira automatiquement lire le .env et injecter la valeur
          MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASS}
          
      web:
        image: wordpress:latest
        ports:
          - "${APP_PORT}:80"
    ```

<br>

---

## L'Arsenal du Chef d'Orchestre

Placez votre terminal dans le dossier contenant le fichier `docker-compose.yml` (ou `compose.yml` sur les versions très récentes).

```bash title="Commandes quotidiennes"
# Lancer tout l'orchestre en tâche de fond (Detached)
docker compose up -d

# Voir quels musiciens sont en train de jouer
docker compose ps

# Écouter ce que disent tous les services en même temps (les logs fusionnés)
docker compose logs -f

# Mettre l'orchestre en pause (sans détruire les instruments)
docker compose stop

# La commande de nettoyage total :
# Arrête les conteneurs ET détruit le réseau interne. 
# Rassurez-vous, les données stockées dans les Volumes sont conservées.
docker compose down
```

!!! warning "L'évolution de la commande"
    Vous lirez souvent d'anciens tutoriels utilisant `docker-compose` (avec un tiret). C'était un script Python externe. Depuis la version 2 (V2), Compose a été réécrit en Go et intégré nativement au moteur Docker en tant que plugin. **Utilisez toujours la syntaxe moderne sans tiret : `docker compose`**.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Docker Compose est l'outil indispensable pour orchestrer plusieurs conteneurs sur **une seule machine** (ordinateur de développement ou serveur unique). Il transforme des séries de commandes Bash fragiles en un fichier YAML déclaratif, élégant et versionnable. Il crée automatiquement des réseaux isolés et intègre un DNS interne qui transforme le nom de vos services en URL de connexion.

> Si Docker Compose gère l'orchestration sur **une seule machine**, que faire si vous devez déployer votre application sur un cluster de **100 serveurs** interconnectés ? Compose montre ici ses limites. C'est pour cette raison qu'existent des orchestrateurs massifs comme Kubernetes, ou des gestionnaires de configuration comme **Ansible** (que nous aborderons dans la section IaC).

<br>