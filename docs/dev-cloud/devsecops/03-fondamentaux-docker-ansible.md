---
title: Fondamentaux Docker & IaC
description: Différencier précisément le Provisionnement (Terraform), la Configuration (Ansible) et la Conteneurisation (Docker).
icon: lucide/book-open-check
tags: ["IAC", "DOCKER", "TERRAFORM", "ANSIBLE", "DEVSECOPS"]
---

# Séparer les Responsabilités

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="2.0"
  data-time="20-30 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique - L'Achat Immobilier"
    L'erreur la plus fréquente des débutants en DevSecOps est de vouloir tout faire avec un seul outil.
    *« Pourquoi utiliser Ansible si je peux utiliser Docker ? Pourquoi Terraform si j'ai Ansible ? »*
    
    Imaginez que vous souhaitez ouvrir un nouveau magasin :
    1. **Le Provisionnement (Terraform)** : C'est le promoteur immobilier. Il achète le terrain vierge, tire les lignes électriques haute tension, et construit les murs de l'entrepôt brut.
    2. **La Configuration (Ansible)** : C'est l'architecte d'intérieur. Il entre dans l'entrepôt, peint les murs, installe les étagères, met en place les extincteurs et l'alarme (Sécurité / Firewall).
    3. **La Conteneurisation (Docker)** : Ce sont les produits hermétiques prêts à la vente posés sur les étagères.
    
    Vous ne demanderiez pas au promoteur immobilier de peindre les murs, et vous ne demanderiez pas à votre architecte de fabriquer lui-même vos produits.

Avant de plonger dans le code technique, il est **impératif** de comprendre la ligne de démarcation entre ces trois couches de l'infrastructure moderne.

<br>

---

## Le Paysage de l'Automatisation

Dans une architecture de qualité (Masterclass), le déploiement d'un nouveau projet suit une chaîne logistique très stricte, modélisée ici :

```mermaid
graph TD
    subgraph "Niveau 1 : Provisionnement (Créer le matériel virtuel)"
    A[Terraform / OpenTofu] -->|API Call| B(AWS / Azure / Proxmox)
    B --> |Retourne l'IP du serveur vierge| A
    end
    
    subgraph "Niveau 2 : Configuration (Préparer l'OS)"
    C[Ansible] -->|Connexion SSH| B
    C -.->|Installe : Docker, Fail2Ban, Clés SSH| B
    end
    
    subgraph "Niveau 3 : Conteneurisation (Héberger l'Application)"
    D[Docker Engine] -->|Isole et exécute| E[Conteneurs PHP/Node]
    F[Docker Compose] -->|Orchestre la BDD et le Serveur Web| D
    end
    
    A -.->|Passe le relai (Inventaire)| C
    C -->|Copie le docker-compose.yml| F
    
    style A fill:#7b42bc,stroke:#fff,color:#fff
    style C fill:#1A1918,stroke:#fff,color:#fff
    style D fill:#2496ED,stroke:#fff,color:#fff
    style F fill:#2496ED,stroke:#fff,color:#fff
```

### 1. Le Provisionnement (Terraform / OpenTofu)
- **Le Rôle** : Parler aux API des fournisseurs Cloud (AWS, Azure, OVH) pour acheter ou louer des ressources brutes. Il crée la Machine Virtuelle (VM), alloue une adresse IP publique, et crée le réseau virtuel (VPC).
- **Le Danger** : Ne l'utilisez pas pour installer des logiciels à l'intérieur de la VM. Il est aveugle à ce qui se passe dans le système d'exploitation.

### 2. La Gestion de Configuration (Ansible)
- **Le Rôle** : Se connecter en SSH au serveur vierge que Terraform vient de créer. Il s'assure que le système Linux est à jour, ferme les ports dangereux, installe des agents de monitoring, et surtout, installe le moteur Docker.
- **Le Danger** : Ne l'utilisez pas pour compiler et lancer votre application source. Bien qu'Ansible puisse exécuter des scripts, ce n'est pas un orchestrateur d'applications.

### 3. La Conteneurisation (Docker / Compose)
- **Le Rôle** : Enfermer votre code et vos dépendances dans une boîte portable. Si votre application PHP a besoin d'une version très spécifique d'une bibliothèque, cette bibliothèque est dans le conteneur, elle ne "salit" pas le serveur configuré par Ansible.
- **Le Danger** : Ne mettez pas les mots de passe root de votre base de données en clair dans vos fichiers Docker. Utilisez l'injection de variables (AppSec).

<br>

---

## La Symbiose (Le Flux de Travail Parfait)

Comment ces trois outils interagissent-ils dans le monde réel ?

1. Le Développeur modifie le code de l'application et fait un `git push`.
2. Le système CI/CD prend le code, construit l'**Image Docker**, et l'envoie sur un registre privé (comme GitLab Container Registry).
3. Si un nouveau serveur est nécessaire pour supporter le trafic, le système exécute **Terraform**. Une nouvelle machine virtuelle naît chez AWS.
4. Immédiatement après, **Ansible** prend le relais. Il se connecte à la nouvelle machine, la sécurise, et installe Docker.
5. Toujours via Ansible, on ordonne au serveur de faire un `docker compose up`. 
6. Le serveur télécharge l'Image Docker depuis le registre privé et démarre le **Conteneur**. 

L'application est en ligne, de manière 100% automatisée, sécurisée, et reproductible à l'infini.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    La maturité d'une équipe DevSecOps se mesure à sa capacité à ne pas mélanger les pinceaux. **Terraform** crée l'infrastructure brute (Provisionnement). **Ansible** configure l'intérieur du serveur (Configuration). **Docker** fait tourner l'application dans une bulle isolée (Conteneurisation). 

> Maintenant que vous visualisez cette "chaîne logistique", nous allons étudier en détail chacun de ses maillons, en commençant par le sommet : l'Infrastructure as Code (IaC) et la gestion de configuration avec **Ansible**.

<br>
