---
description: "Glossaire — Cloud Computing : Plateformes cloud, conteneurisation, Infrastructure as Code et architectures natives."
icon: lucide/book-a
tags: ["GLOSSAIRE", "CLOUD", "KUBERNETES", "SERVERLESS", "INFRASTRUCTURE"]
---

# Cloud Computing

<div
  class="omny-meta"
  data-level="🟢 Tout niveau"
  data-version="1.0"
  data-time="Consultation">
</div>

## A

!!! note "Auto Scaling"
    > Ajustement automatique des ressources cloud en fonction de la demande en temps réel.

    Utilisé pour optimiser les coûts et maintenir la performance lors de pics de charge.

    - **Métriques déclencheurs :** CPU, mémoire, requêtes par seconde, métriques custom
    - **Types :** horizontal (ajout d'instances — scale out), vertical (augmentation ressources — scale up)

    ```mermaid
    graph LR
        A[Auto Scaling] --> B[Elasticité]
        A --> C[Coût-optimisation]
        A --> D[Performance]
    ```

<br>

---

!!! note "AWS"
    > Plateforme de services cloud Amazon offrant infrastructure, plateforme et logiciels à la demande.

    Utilisé pour héberger, développer et déployer des applications dans le cloud public.

    - **Acronyme :** Amazon Web Services
    - **Services phares :** EC2, S3, RDS, Lambda, VPC, IAM, CloudFront

    ```mermaid
    graph LR
        A[AWS] --> B[EC2]
        A --> C[S3]
        A --> D[Lambda]
    ```

<br>

---

!!! note "Azure"
    > Plateforme cloud Microsoft fournissant services IaaS, PaaS et SaaS.

    Utilisé pour l'intégration avec l'écosystème Microsoft et les applications d'entreprise.

    - **Services :** Virtual Machines, Storage, App Service, Azure Functions
    - **Intégrations :** Active Directory, Office 365, Windows Server

    ```mermaid
    graph LR
        A[Azure] --> B[Microsoft]
        A --> C[Enterprise]
        A --> D[Active Directory]
    ```

<br>

---

## C

!!! note "Container"
    > Unité de déploiement légère incluant application et toutes ses dépendances dans un environnement isolé.

    Utilisé pour standardiser les environnements et simplifier le déploiement entre développement et production.

    - **Avantages :** portabilité, isolation légère, efficacité des ressources vs machines virtuelles
    - **Technologies :** Docker, containerd, CRI-O

    ```mermaid
    graph LR
        A[Container] --> B[Docker]
        A --> C[Isolation]
        A --> D[Portabilité]
    ```

<br>

---

!!! note "CloudFormation"
    > Service AWS d'infrastructure as code utilisant des templates JSON/YAML déclaratifs.

    Utilisé pour provisionner et gérer l'infrastructure AWS de manière reproductible et versionnable.

    - **Concepts :** stacks, templates, resources, parameters, outputs
    - **Avantages :** reproducibilité, versioning Git, rollback automatique

    ```mermaid
    graph LR
        A[CloudFormation] --> B[Infrastructure as Code]
        A --> C[Templates]
        A --> D[AWS]
    ```

<br>

---

## D

!!! note "Docker"
    > Plateforme de conteneurisation permettant d'empaqueter applications et dépendances en images portables.

    Utilisé pour créer des environnements cohérents du développement à la production.

    - **Composants :** Docker Engine, images (template), containers (instance), registries
    - **Commandes :** `docker build`, `docker run`, `docker push`, `docker pull`

    ```mermaid
    graph LR
        A[Docker] --> B[Container]
        A --> C[Image]
        A --> D[Registry]
    ```

<br>

---

!!! note "Dockerfile"
    > Script contenant les instructions séquentielles pour construire une image Docker.

    Utilisé pour automatiser la création d'images reproductibles et documentées.

    - **Instructions :** `FROM`, `RUN`, `COPY`, `EXPOSE`, `CMD`, `ENV`
    - **Bonnes pratiques :** multi-stage builds, minimiser les layers, images de base minimales

    ```mermaid
    graph LR
        A[Dockerfile] --> B[Image]
        A --> C[Build]
        A --> D[Automatisation]
    ```

<br>

---

## E

!!! note "EC2"
    > Service de machines virtuelles cloud d'Amazon Web Services.

    Utilisé pour exécuter des applications dans des instances virtuelles redimensionnables.

    - **Acronyme :** Elastic Compute Cloud
    - **Types d'instances :** general purpose, compute optimized, memory optimized, storage optimized, GPU

    ```mermaid
    graph LR
        A[EC2] --> B[Machine virtuelle]
        A --> C[AWS]
        A --> D[Elastique]
    ```

<br>

---

!!! note "ECS"
    > Service de conteneurs managé d'AWS pour déployer et gérer des applications conteneurisées.

    Utilisé pour orchestrer des containers Docker sans gérer l'infrastructure sous-jacente.

    - **Acronyme :** Elastic Container Service
    - **Modes :** EC2 (gestion des instances vous-même), Fargate (fully serverless managed)

    ```mermaid
    graph LR
        A[ECS] --> B[Container]
        A --> C[AWS]
        A --> D[Fargate]
    ```

<br>

---

!!! note "EKS"
    > Service Kubernetes managé d'AWS simplifiant le déploiement et la gestion des clusters.

    Utilisé pour exécuter Kubernetes en production sans gérer la complexité du control plane.

    - **Acronyme :** Elastic Kubernetes Service
    - **Intégrations :** IAM, VPC, ELB, CloudWatch, ECR

    ```mermaid
    graph LR
        A[EKS] --> B[Kubernetes]
        A --> C[AWS]
        A --> D[Managé]
    ```

<br>

---

## F

!!! note "FaaS"
    > Modèle d'exécution cloud où le code s'exécute en réponse à des événements sans gérer de serveurs.

    Utilisé pour créer des applications event-driven avec une facturation à l'exécution.

    - **Acronyme :** Function as a Service
    - **Exemples :** AWS Lambda, Azure Functions, Google Cloud Functions

    ```mermaid
    graph LR
        A[FaaS] --> B[Serverless]
        A --> C[Event-driven]
        A --> D[Lambda]
    ```

<br>

---

!!! note "Fault tolerance"
    > Capacité d'un système à continuer de fonctionner correctement malgré les pannes de composants.

    Utilisé pour assurer la haute disponibilité des applications et services critiques.

    - **Techniques :** redondance, failover automatique, circuit breakers
    - **Design patterns :** multi-AZ, multi-region, active-passive, active-active

    ```mermaid
    graph LR
        A[Fault tolerance] --> B[Haute disponibilité]
        A --> C[Redondance]
        A --> D[Failover]
    ```

<br>

---

## G

!!! note "GCP"
    > Plateforme de services cloud de Google axée sur l'analytique, l'IA et la data.

    Utilisé pour les applications nécessitant machine learning, big data ou l'infrastructure Google.

    - **Acronyme :** Google Cloud Platform
    - **Services :** Compute Engine, BigQuery, AI Platform, GKE (Kubernetes Engine)

    ```mermaid
    graph LR
        A[GCP] --> B[Google]
        A --> C[Big Data]
        A --> D[AI/ML]
    ```

<br>

---

## H

!!! note "Helm"
    > Gestionnaire de paquets pour Kubernetes facilitant le déploiement d'applications complexes.

    Utilisé pour packager, configurer et déployer des applications Kubernetes avec versioning.

    - **Concepts :** charts (packages), releases (instances déployées), values, templates
    - **Avantages :** réutilisabilité, versioning, rollback, templating puissant

    ```mermaid
    graph LR
        A[Helm] --> B[Kubernetes]
        A --> C[Charts]
        A --> D[Package manager]
    ```

<br>

---

!!! note "Horizontal scaling"
    > Ajout de ressources en parallèle (instances supplémentaires) pour gérer l'augmentation de charge.

    Utilisé pour distribuer la charge sur plusieurs instances identiques derrière un load balancer.

    - **Synonyme :** scale out
    - **Avantages :** élasticité, tolérance aux pannes, coût-efficacité par rapport au scale up

    ```mermaid
    graph LR
        A[Horizontal scaling] --> B[Load balancing]
        A --> C[Elasticité]
        A --> D[Vertical scaling]
    ```

<br>

---

## I

!!! note "IaaS"
    > Modèle cloud fournissant une infrastructure virtualisée (compute, storage, network) à la demande.

    Utilisé pour migrer des workloads existants vers le cloud avec un contrôle maximal.

    - **Acronyme :** Infrastructure as a Service
    - **Composants :** compute (VMs), stockage (blocs/objets), réseau (VPC), virtualisation

    ```mermaid
    graph LR
        A[IaaS] --> B[Infrastructure]
        A --> C[Virtualisation]
        A --> D[PaaS]
    ```

<br>

---

!!! note "IAM"
    > Système de gestion des identités et des accès aux ressources cloud.

    Utilisé pour contrôler finement qui peut accéder à quoi dans l'environnement cloud.

    - **Acronyme :** Identity and Access Management
    - **Concepts :** users, groups, roles, policies (JSON), permissions, least privilege

    ```mermaid
    graph LR
        A[IAM] --> B[Identités]
        A --> C[Accès]
        A --> D[Sécurité]
    ```

<br>

---

## K

!!! note "Kubernetes"
    > Plateforme d'orchestration de conteneurs automatisant le déploiement, la mise à l'échelle et la gestion.

    Utilisé pour gérer des applications conteneurisées à grande échelle en production.

    - **Composants :** control plane (master), worker nodes, pods, services, ingress
    - **Concepts :** deployments, configmaps, secrets, persistent volumes, namespaces

    ```mermaid
    graph LR
        A[Kubernetes] --> B[Orchestration]
        A --> C[Pods]
        A --> D[Services]
    ```

<br>

---

!!! note "kubectl"
    > Outil en ligne de commande pour interagir avec les clusters Kubernetes.

    Utilisé pour déployer, inspecter et gérer les ressources Kubernetes depuis le terminal.

    - **Commandes :** `get`, `create`, `apply`, `delete`, `describe`, `logs`, `exec`
    - **Configuration :** kubeconfig, contexts, namespaces

    ```mermaid
    graph LR
        A[kubectl] --> B[Kubernetes]
        A --> C[CLI]
        A --> D[Cluster]
    ```

<br>

---

## L

!!! note "Lambda"
    > Service de calcul serverless d'AWS exécutant du code en réponse à des événements.

    Utilisé pour créer des applications event-driven sans provisionner ni gérer de serveurs.

    - **Déclencheurs :** API Gateway, S3, DynamoDB, CloudWatch Events, SQS
    - **Langages :** Python, Node.js, Java, C#, Go, Ruby

    ```mermaid
    graph LR
        A[Lambda] --> B[Serverless]
        A --> C[Events]
        A --> D[AWS]
    ```

<br>

---

!!! note "Load Balancer"
    > Service distribuant le trafic entrant sur plusieurs instances pour optimiser disponibilité et performances.

    Utilisé pour améliorer la résilience et répartir équitablement la charge de travail.

    - **Types :** Application (L7 — HTTP/HTTPS), Network (L4 — TCP/UDP), Classic
    - **Algorithmes :** round robin, least connections, weighted, IP hash

    ```mermaid
    graph LR
        A[Load Balancer] --> B[Distribution]
        A --> C[Haute disponibilité]
        A --> D[Performance]
    ```

<br>

---

## M

!!! note "Microservices"
    > Architecture décomposant une application en services indépendants, déployables séparément.

    Utilisé pour améliorer la scalabilité, la maintenabilité et permettre des déploiements indépendants.

    - **Avantages :** diversité technologique, autonomie des équipes, isolation des pannes
    - **Challenges :** complexité des systèmes distribués, latence réseau, cohérence des données

    ```mermaid
    graph LR
        A[Microservices] --> B[Indépendance]
        A --> C[Scalabilité]
        A --> D[API Gateway]
    ```

<br>

---

!!! note "Multi-cloud"
    > Stratégie utilisant plusieurs fournisseurs cloud pour éviter le vendor lock-in.

    Utilisé pour diversifier les risques, optimiser les coûts et utiliser le meilleur service de chaque provider.

    - **Avantages :** négociation de prix, best-of-breed, redondance inter-cloud
    - **Challenges :** complexité de gestion, compétences requises, intégration inter-cloud

    ```mermaid
    graph LR
        A[Multi-cloud] --> B[Diversification]
        A --> C[Vendor lock-in]
        A --> D[Optimisation]
    ```

<br>

---

## P

!!! note "PaaS"
    > Plateforme cloud fournissant un environnement de développement et déploiement complet et managé.

    Utilisé pour développer et déployer des applications sans gérer l'infrastructure sous-jacente.

    - **Acronyme :** Platform as a Service
    - **Exemples :** Heroku, Google App Engine, Azure App Service, Railway

    ```mermaid
    graph LR
        A[PaaS] --> B[Développement]
        A --> C[Déploiement]
        A --> D[IaaS]
    ```

<br>

---

!!! note "Pod"
    > Plus petite unité déployable dans Kubernetes contenant un ou plusieurs conteneurs colocalisés.

    Utilisé comme wrapper pour les conteneurs partageant le même réseau et les mêmes volumes.

    - **Caractéristiques :** éphémère, IP unique dans le cluster, volumes partagés entre containers
    - **Patterns :** sidecar (assistant), ambassador (proxy), adapter (transformation)

    ```mermaid
    graph LR
        A[Pod] --> B[Container]
        A --> C[Kubernetes]
        A --> D[Éphémère]
    ```

<br>

---

## S

!!! note "S3"
    > Service de stockage objet d'AWS offrant durabilité quasi-infinie et scalabilité automatique.

    Utilisé pour stocker et récupérer n'importe quelle quantité de données depuis n'importe où.

    - **Acronyme :** Simple Storage Service
    - **Classes de stockage :** Standard, Infrequent Access (IA), Glacier, Deep Archive

    ```mermaid
    graph LR
        A[S3] --> B[Stockage objet]
        A --> C[Durabilité]
        A --> D[AWS]
    ```

<br>

---

!!! note "SaaS"
    > Modèle cloud où le logiciel est accessible via Internet en tant que service abonné.

    Utilisé pour consommer des applications sans installation, maintenance ni gestion d'infrastructure.

    - **Acronyme :** Software as a Service
    - **Exemples :** Salesforce, Office 365, Google Workspace, Slack, Notion

    ```mermaid
    graph LR
        A[SaaS] --> B[Application]
        A --> C[Internet]
        A --> D[Abonnement]
    ```

<br>

---

!!! note "Serverless"
    > Modèle d'exécution où l'infrastructure est entièrement gérée par le fournisseur cloud.

    Utilisé pour se concentrer sur le code métier avec une scalabilité automatique et une facturation à l'usage.

    - **Avantages :** scalabilité automatique, pay-per-use, zero serveur à gérer
    - **Services :** FaaS (Lambda), API Gateway, bases de données managées, queues

    ```mermaid
    graph LR
        A[Serverless] --> B[FaaS]
        A --> C[Managed services]
        A --> D[Pay-per-use]
    ```

<br>

---

## T

!!! note "Terraform"
    > Outil d'infrastructure as code permettant de provisionner des ressources cloud de manière déclarative.

    Utilisé pour gérer l'infrastructure de manière reproductible, versionnable et multi-cloud.

    - **Concepts :** providers (AWS/Azure/GCP), resources, variables, outputs, state
    - **Workflow :** `terraform init` → `plan` (aperçu) → `apply` (déploiement)

    ```mermaid
    graph LR
        A[Terraform] --> B[Infrastructure as Code]
        A --> C[Multi-cloud]
        A --> D[State]
    ```

<br>

---

## V

!!! note "VPC"
    > Réseau virtuel privé isolé dans le cloud pour vos ressources.

    Utilisé pour créer un environnement réseau sécurisé avec contrôle total du routage et des accès.

    - **Acronyme :** Virtual Private Cloud
    - **Composants :** subnets (publics/privés), route tables, security groups, NACLs, Internet Gateway

    ```mermaid
    graph LR
        A[VPC] --> B[Réseau privé]
        A --> C[Isolation]
        A --> D[Sécurité]
    ```

<br>

---

!!! note "Vertical scaling"
    > Augmentation des ressources (CPU, RAM) d'une machine existante pour gérer plus de charge.

    Utilisé quand l'application ne peut pas être distribuée horizontalement ou en complément.

    - **Synonyme :** scale up
    - **Limitations :** plafond matériel/cloud, single point of failure, coût croissant

    ```mermaid
    graph LR
        A[Vertical scaling] --> B[Ressources]
        A --> C[Scale up]
        A --> D[Horizontal scaling]
    ```

<br>
