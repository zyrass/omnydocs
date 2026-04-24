---
title: Ansible
description: Gestion de configuration, principe d'idempotence, agentless, et rédaction de Playbooks YAML.
icon: lucide/book-open-check
tags: ["IAC", "ANSIBLE", "CONFIGURATION", "YAML", "AGENTLESS"]
---

# Ansible : Gestion de Configuration

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.1"
  data-time="45-60 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique - L'Armée des Clones"
    Imaginez que vous êtes le général d'une armée. Vous devez donner un ordre à 10 000 soldats : *"Nettoyez vos armes, équipez vos casques, et tenez la ligne"*.
    
    L'ancienne méthode consistait à aller voir chaque soldat un par un pour lui donner la consigne en personne (connexion SSH manuelle). Cela prend des jours, et vous risquez d'oublier un soldat ou de mal formuler l'ordre.
    
    **Ansible est le Général**. Il possède une liste exacte de tous ses soldats (*L'Inventaire*). Il rédige l'ordre officiel sur un parchemin (*Le Playbook*), et utilise un porte-voix magique (*Le protocole SSH*) pour que les 10 000 soldats reçoivent l'ordre et l'exécutent simultanément en 10 secondes.

Ansible (développé par RedHat) est l'outil phare de la **Gestion de Configuration**. Contrairement à Terraform qui *construit* l'infrastructure (les murs), Ansible la *configure* (installe la peinture, les meubles et l'électricité).

<br>

---

## Les Deux Piliers d'Ansible

La popularité écrasante d'Ansible face à ses concurrents historiques (Puppet, Chef, SaltStack) repose sur deux décisions architecturales de génie :

### 1. Agentless (Sans Agent)

Puppet et Chef nécessitaient d'installer un programme (un *agent*) tournant en permanence sur chaque serveur cible pour écouter les ordres.

Ansible est **Agentless**. Il n'a besoin de rien sur le serveur cible à part une chose qui s'y trouve déjà par défaut sur 100% des distributions Linux : un serveur **SSH** et **Python**.
L'ordinateur qui lance Ansible va se connecter en SSH aux cibles, pousser un script Python temporaire, l'exécuter, et effacer ses traces en repartant. C'est propre, sécurisé, et cela ne consomme aucune RAM en arrière-plan.

### 2. L'Idempotence absolue

L'idempotence est le Saint Graal du DevSecOps. En mathématiques, une opération est idempotente si l'exécuter une fois a le même résultat que l'exécuter 10 000 fois.

=== ":simple-gnubash: Script Bash (Non-Idempotent)"

    ```bash title="Exemple d'un script fragile"
    # Si on lance ce script 2 fois, Nginx sera redémarré 2 fois (coupure de service)
    # Et la ligne "listen 80;" sera ajoutée 2 fois à la fin du fichier (erreur de syntaxe).
    apt-get install nginx
    echo "listen 80;" >> /etc/nginx/nginx.conf
    systemctl restart nginx
    ```

=== ":simple-ansible: Playbook Ansible (Idempotent)"

    ```yaml title="Le paradigme déclaratif"
    # Ansible regarde D'ABORD l'état actuel du serveur.
    # Si Nginx est DÉJÀ installé, il ne fait rien (Statut : "OK").
    # Si Nginx N'EST PAS installé, il l'installe (Statut : "CHANGED").
    - name: "S'assurer que Nginx est présent"
      apt:
        name: nginx
        state: present
    ```

!!! tip "La garantie Ansible"
    Vous pouvez lancer un Playbook Ansible 50 fois par jour sur votre parc en production. S'il n'y a pas de dérive (si personne n'a touché manuellement aux serveurs), Ansible parcourra tout le parc en renvoyant `OK`, **sans rien casser, sans rien redémarrer, sans rien modifier**.

<br>

---

## L'Anatomie d'un Projet Ansible

Un projet Ansible tient dans un dossier contenant (au minimum) deux éléments vitaux : l'**Inventaire** et le **Playbook**.

### L'Inventaire (Qui ?)

L'inventaire est un fichier texte (souvent nommé `hosts.ini` ou `inventory.yml`) qui liste les adresses IP de vos serveurs et les regroupe logiquement.

```ini title="hosts.ini"
# Groupe des serveurs web
[webservers]
192.168.1.10
192.168.1.11

# Groupe des bases de données
[databases]
192.168.1.50

# Un groupe contenant d'autres groupes (Meta-groupe)
[production:children]
webservers
databases
```

### Le Playbook (Quoi ?)

Le Playbook est le script rédigé en YAML. Il définit les **Tâches** (Tasks) à exécuter sur un groupe d'hôtes ciblé.

```yaml title="playbook.yml"
---
- name: "Configuration de la flotte Web"
  hosts: webservers      # Cible le groupe défini dans l'inventaire
  become: true           # Demande les droits Root (sudo)
  
  tasks:
    - name: "Installer Docker Engine"
      apt:
        name: docker-ce
        state: present
        update_cache: yes
        
    - name: "S'assurer que le service Docker est actif"
      service:
        name: docker
        state: started
        enabled: yes
        
    - name: "Ajouter l'utilisateur ubuntu au groupe docker"
      user:
        name: ubuntu
        groups: docker
        append: yes
```

<br>

---

## Les Modules (L'Intelligence d'Ansible)

Dans le code ci-dessus, remarquez l'utilisation des mots-clés `apt`, `service`, `user`. Ce sont des **Modules**.
Ansible possède des milliers de modules natifs. Ils encapsulent la complexité des différents OS.

Par exemple, le module `user` de notre script sait très bien que pour ajouter un groupe sous Ubuntu (Debian), il doit appeler la commande bash `usermod -aG`, mais que sous un autre système l'appel pourrait être différent. **Le module masque la complexité du système d'exploitation.**

### Quelques modules de base :

| Module | Fonction (Idempotente) |
| --- | --- |
| `copy` | Copier un fichier de notre PC vers le serveur distant, uniquement si le fichier a changé (hash MD5). |
| `file` | Créer un dossier, modifier les droits (`chmod 755`), supprimer un fichier. |
| `ufw` | Ouvrir ou fermer un port sur le Pare-feu d'Ubuntu. |
| `git` | Cloner un dépôt GitHub, ou s'assurer que le code est bien sur la branche `main`. |
| `shell` | *(À éviter si possible)*. Exécuter une commande Bash brute. **Attention, le module shell n'est PAS idempotent par défaut**. |

<br>

---

## Variables et Templates (Jinja2)

Configurer Nginx c'est bien, mais que faire si le `webserver` 1 doit écouter sur le port 80, et le `webserver` 2 sur le port 8080 ?
Ansible intègre le moteur de template **Jinja2**.

Vous créez un fichier générique (un "Template") avec des variables :

```nginx title="nginx.conf.j2 (Sur votre PC)"
server {
    # La variable sera remplacée à la volée par Ansible pendant le déploiement
    listen {{ port_ecoute }};
    server_name omnydocs.com;
}
```

Ansible transpilera ce fichier à la volée, enverra le fichier généré sur le serveur cible, et redémarrera Nginx *uniquement* si le fichier final a changé !

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Ansible est le cœur de la gestion de configuration DevSecOps. Son architecture **Agentless** (via SSH) le rend universel et ultra-léger. Son utilisation exclusive du YAML déclaratif force les équipes à écrire des déploiements **idempotents**, garantissant qu'un serveur en production restera exactement dans l'état défini par le code, même si on exécute le script 100 fois par jour.

> Ansible configure l'intérieur de la machine. Mais qui achète cette machine ? Qui la commande à Amazon Web Services ou à OVH ? Qui demande qu'elle ait 16 Go de RAM ? C'est le rôle exclusif du Provisionnement, géré par le second titan de l'IaC : **Terraform**.

<br>