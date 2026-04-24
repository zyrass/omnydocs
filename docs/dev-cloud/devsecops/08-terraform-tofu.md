---
title: Terraform / OpenTofu
description: L'Infrastructure as Code (IaC) pour provisionner l'architecture cloud avec le langage HCL. L'idempotence des ressources brutes.
icon: lucide/book-open-check
tags: ["IAC", "TERRAFORM", "OPENTOFU", "PROVISIONNEMENT", "HCL", "CLOUD"]
---

# Terraform : Le Provisionnement Cloud

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="40-50 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Constructeur Automobile"
    Rappelez-vous l'analogie de la maison : Terraform est le promoteur immobilier. Il achète le terrain et pose les murs, avant qu'Ansible ne vienne faire la peinture.
    
    Imaginez maintenant que vous êtes un constructeur automobile. L'ancienne méthode (avant le Cloud) consistait à envoyer un e-mail à votre fournisseur de métal : *"Bonjour, je voudrais commander 100 tonnes d'acier, merci de me les livrer dans un mois."*
    
    Aujourd'hui, avec le Cloud Computing (AWS, Azure), vous ne parlez plus à des humains, vous parlez à des **API**. Vous envoyez une requête HTTP à AWS : *"Donne-moi 5 serveurs avec 16 Go de RAM tout de suite"*, et en 30 secondes, les serveurs sont à vous.
    
    **Terraform** est l'outil qui transforme vos requêtes d'infrastructure en code. Au lieu de cliquer sur des boutons dans l'interface Web d'AWS (ce qui est long, propice aux erreurs et non traçable), vous écrivez un fichier texte qui décrit l'architecture souhaitée.

Terraform, créé par HashiCorp, est le leader mondial du **Provisionnement**. *(Note : Suite à un changement de licence de HashiCorp, la communauté open source a créé un "fork" strictement identique appelé **OpenTofu**).*

<br>

---

## Le Langage HCL (HashiCorp Configuration Language)

Contrairement à Ansible ou Docker Compose qui utilisent le YAML, Terraform utilise son propre langage déclaratif : le **HCL**.
Il est conçu pour être à la fois lisible par l'humain et extrêmement strict pour éviter les erreurs d'infrastructure (qui coûtent très cher sur le Cloud).

=== ":simple-terraform: Exemple HCL (Déclaratif)"

    ```hcl title="main.tf (Création d'un serveur AWS)"
    # 1. On déclare le fournisseur (Provider)
    provider "aws" {
      region = "eu-west-3" # Paris
    }

    # 2. On déclare la ressource souhaitée (Un serveur EC2)
    resource "aws_instance" "mon_serveur_web" {
      ami           = "ami-0abcdef1234567890" # Image Ubuntu
      instance_type = "t3.micro"              # Taille du serveur (CPU/RAM)
      
      tags = {
        Name = "Serveur-Production-01"
      }
    }
    ```

Le script ci-dessus est **déclaratif**. Vous ne dites pas à Terraform *comment* contacter AWS, comment s'authentifier, ou quelles requêtes réseau effectuer. Vous lui décrivez simplement le **résultat final souhaité**.

<br>

---

## Le Cœur de Terraform : L'État (The State)

C'est ici que Terraform montre sa véritable puissance par rapport à un simple script Bash.

Terraform conserve une mémoire photographique de ce qu'il a créé. Ce fichier mémoire s'appelle le `terraform.tfstate`.

1. **Jour 1 :** Vous exécutez le code ci-dessus. Terraform lit le fichier `.tf`, regarde l'API d'AWS, voit qu'il n'y a pas de serveur, et **le crée**. Il l'inscrit dans son `.tfstate`.
2. **Jour 2 :** Vous ré-exécutez exactement le même code. Terraform lit le fichier, compare avec son `.tfstate` et avec l'API d'AWS. Il s'aperçoit que le serveur existe déjà. Résultat : **Il ne fait absolument rien.** (Idempotence).
3. **Jour 3 :** Vous changez `instance_type = "t3.micro"` en `"t3.large"` dans le code. Vous exécutez Terraform. Il va comparer l'état actuel et l'état désiré, et en déduire qu'il doit modifier le serveur existant sans en créer un deuxième.

!!! danger "La perte du fichier State"
    Le fichier `terraform.tfstate` est la relique la plus précieuse d'un projet IaC. S'il est détruit, Terraform "oublie" qu'il a créé les serveurs. Au prochain lancement, il essaiera de tous les recréer, ce qui provoquera des conflits massifs ou des factures Cloud astronomiques. De plus, il contient souvent des **secrets en clair** (mots de passe BDD). Il ne doit **jamais** être versionné sur Git, mais stocké dans un coffre-fort distant (ex: un *S3 Bucket* sécurisé).

<br>

---

## Le Flux de Travail Terraform (Le Plan de Bataille)

On ne lance jamais Terraform à l'aveugle. Modifier des serveurs de production est une opération chirurgicale. Le flux de travail standard se compose de 3 commandes :

```bash title="Workflow Terraform"
# 1. INIT : Télécharge les plugins (Providers AWS/GCP) nécessaires.
terraform init

# 2. PLAN : La phase de simulation. (Crucial !)
# Terraform vous dit EXACTEMENT ce qu'il a l'intention de faire, sans le faire.
# "Je vais détruire 1 base de données, modifier 2 réseaux, et créer 5 serveurs."
terraform plan

# 3. APPLY : L'exécution. (Demande confirmation manuelle).
# Applique les changements prévus dans le "plan".
terraform apply
```

L'étape de `terraform plan` est l'une des raisons principales de l'adoption massive de Terraform par les équipes de sécurité et d'opérations (SecOps). Avant de modifier l'infrastructure, l'équipe entière peut lire le "Plan" et le valider lors d'une *Code Review*.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Terraform est le chef d'orchestre du Cloud Computing. Il permet de provisionner des milliers de composants (Réseaux, Serveurs, Bases de données) chez n'importe quel fournisseur (AWS, Azure, GCP) via le langage unifié **HCL**. Son fichier de mémoire (`State`) garantit **l'idempotence** des déploiements. En couplant le provisionnement de Terraform avec la gestion de configuration d'Ansible, vous obtenez une infrastructure 100% "As Code", reproductible en cas de désastre.

> Avec notre infrastructure provisionnée, configurée et conteneurisée, la fondation est solide. Il est temps de nous attaquer à la couche applicative, là où les failles se cachent le plus souvent : **L'AppSec (Application Security)** et l'Authentification via les JWT.

<br>
