---
title: HashiCorp Vault
description: Centralisation des secrets, injection dynamique, et résolution du paradoxe du Secret Zéro pour les architectures cloud.
icon: lucide/book-open-check
tags: ["SECRETS", "VAULT", "HASHICORP", "SECRET-ZERO", "CHIFFREMENT"]
---

# Vault (Gestion des Secrets)

<div
  class="omny-meta"
  data-level="🟠 Avancé"
  data-version="1.0"
  data-time="30-40 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Coffre et la Clé"
    Vous avez acheté le coffre-fort le plus impénétrable du monde pour y cacher le mot de passe de votre base de données. C'est parfait.
    Mais un problème philosophique se pose immédiatement : **où allez-vous cacher la clé qui ouvre le coffre ?**
    Si vous donnez la clé au serveur Web pour qu'il puisse ouvrir le coffre et lire le mot de passe, un pirate qui pirate le serveur Web volera la clé... et pourra vider le coffre.

C'est ce qu'on appelle en cybersécurité le **Paradoxe du Secret Zéro (Secret Zero Problem)**.
L'outil **HashiCorp Vault** a été créé spécifiquement pour résoudre ce paradoxe et empêcher les développeurs de coder en dur (Hardcode) des mots de passe dans leurs fichiers source.

<br>

---

## Le Secret Zéro : Comment Vault authentifie les machines ?

Vault ne "donne" pas de mot de passe à un serveur sans vérifier son identité. Mais comment un serveur informatique (sans cerveau, sans empreinte digitale) prouve-t-il qui il est ?

Vault utilise l'environnement de confiance dans lequel baigne le serveur.

=== ":simple-amazon: AWS IAM (Exemple Cloud)"

    1. Le serveur Web AWS démarre.
    2. Il contacte Vault : *"Je suis le serveur de paiement légitime"*.
    3. Vault ne le croit pas sur parole. Il interroge silencieusement l'API centrale d'AWS (AWS IAM) : *"Ce serveur est-il bien celui qu'il prétend être, et a-t-il été lancé par un administrateur légitime ?"*
    4. AWS confirme. Vault autorise le serveur à lire les secrets.

=== ":simple-kubernetes: Kubernetes (Exemple Orchestrateur)"

    1. Le conteneur (Pod) démarre dans le cluster K8s.
    2. Il envoie à Vault le "Jeton de Service" (ServiceAccount Token) généré et signé par le maître Kubernetes lui-même.
    3. Vault vérifie la signature cryptographique du jeton auprès du cluster K8s.
    4. Vault injecte le secret en mémoire vive du conteneur.

Ainsi, la "clé du coffre" n'est jamais stockée nulle part. Elle est l'identité cryptographique ou matérielle de la machine, garantie par un tiers de confiance (AWS, Azure, Kubernetes).

<br>

---

## Les Secrets Dynamiques (La Révolution Vault)

Stocker un mot de passe dans Vault (Secret statique) est utile, mais Vault propose une mécanique infiniment supérieure : **Les Secrets Dynamiques**.

Dans une architecture classique, la base de données PostgreSQL a un utilisateur `admin_web` avec le mot de passe `T0pS3cret`. Ce mot de passe est valable à vie. S'il fuite, la BDD est compromise.

Voici comment Vault change les règles du jeu :

```mermaid
sequenceDiagram
    participant Srv as Serveur Web
    participant Vlt as HashiCorp Vault
    participant DB as PostgreSQL

    Srv->>Vlt: 1. J'ai besoin d'accéder à la BDD pour traiter une commande.
    activate Vlt
    Vlt->>Vlt: Vérifie l'identité du serveur (Secret Zéro)
    Vlt->>DB: 2. CREATE USER temp_user_87f1 WITH PASSWORD 'xy9$Zq';
    Vlt->>DB: GRANT SELECT, INSERT ON commandes TO temp_user_87f1;
    Vlt-->>Srv: 3. Voici tes identifiants (Valables 10 minutes).
    deactivate Vlt
    
    Srv->>DB: 4. Traite la commande avec les identifiants temporaires.
    
    Note over Vlt, DB: 10 minutes plus tard...
    Vlt->>DB: 5. DROP USER temp_user_87f1; (Identifiant détruit à jamais)
```

### L'avantage de l'Éphémérité
- **Zéro Surface d'Attaque** : Si un pirate arrive à voler les identifiants présents dans la mémoire du serveur Web, ils ne fonctionneront plus dans 10 minutes.
- **Auditabilité Absolue** : Puisque Vault crée un utilisateur unique pour *chaque* session et *chaque* serveur, l'équipe sécurité (SOC) peut tracer l'auteur de chaque requête SQL dans la base de données avec une précision chirurgicale.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Il est formellement interdit de versionner des mots de passe dans Git, ou de les coder en dur dans les fichiers applicatifs. **HashiCorp Vault** centralise la gestion des secrets en résolvant le paradoxe du "Secret Zéro" grâce à la délégation d'identité (AWS IAM, Kubernetes). Sa véritable force réside dans la génération de **Secrets Dynamiques** éphémères (Lease), qui ferment la fenêtre de tir des pirates de quelques années à quelques minutes.

> La gestion des Secrets clôture ce pilier majeur du **DevSecOps**. Mais concevoir et déployer une architecture sécurisée ne sert à rien si vous êtes aveugle à ce qui s'y passe. Il est temps d'ouvrir les yeux sur votre infrastructure dans la dernière section de ce cours : **L'Observabilité (Obs-Sec)**.

<br>