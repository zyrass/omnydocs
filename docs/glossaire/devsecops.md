---
description: "Glossaire — DevSecOps : CI/CD, Infrastructure as Code, sécurité intégrée, monitoring et culture DevOps."
icon: lucide/book-a
tags: ["GLOSSAIRE", "DEVSECOPS", "CI/CD", "INFRASTRUCTURE", "AUTOMATISATION"]
---

# DevSecOps

<div
  class="omny-meta"
  data-level="🟢 Tout niveau"
  data-version="1.0"
  data-time="Consultation">
</div>

## A

!!! note "Ansible"
    > Outil d'automatisation IT sans agent (agentless) pour la configuration, le déploiement et l'orchestration de systèmes.

    Ansible est apprécié pour sa simplicité : les tâches sont décrites en YAML lisible, sans agent à installer sur les machines cibles. Il se connecte via SSH et applique des playbooks de manière idempotente.

    - **Langage :** YAML (playbooks, roles, inventories)
    - **Avantages :** agentless, idempotence, courbe d'apprentissage faible
    - **Alternatives :** Chef (Ruby), Puppet, Salt

    ```mermaid
    graph LR
        A[Ansible] --> B[Automatisation]
        A --> C[Configuration management]
        A --> D[Orchestration]
    ```

<br>

---

!!! note "Artifact"
    > Produit livrable généré par un processus de build et stocké dans un dépôt centralisé pour distribution et versioning.

    Un artifact est le résultat concret d'une étape de CI : une JAR, une image Docker, un package npm, un binaire compilé. Il est versionné et promu entre environnements (dev → staging → prod) sans être recompilé.

    - **Types :** binaires, images Docker, packages (npm, pip, Maven), libraries
    - **Dépôts :** Nexus, Artifactory, Harbor, GitHub Packages, ECR

    ```mermaid
    graph LR
        A[Artifact] --> B[Build]
        A --> C[Repository]
        A --> D[Versioning]
    ```

<br>

---

!!! note "Automation"
    > Exécution automatique de tâches répétitives sans intervention humaine pour réduire les erreurs et accélérer les cycles.

    L'automatisation est la colonne vertébrale du DevSecOps — elle couvre le testing, le déploiement, le provisioning d'infrastructure et le monitoring, remplaçant les processus manuels sujets aux erreurs.

    - **Domaines :** testing, deployment, infrastructure provisioning, monitoring, security scanning
    - **Outils :** Jenkins, GitLab CI, GitHub Actions, Ansible, Terraform

    ```mermaid
    graph LR
        A[Automation] --> B[Efficacité]
        A --> C[Réduction erreurs]
        A --> D[Standardisation]
    ```

<br>

---

## B

!!! note "Blue-Green Deployment"
    > Stratégie de déploiement utilisant deux environnements identiques (blue = actif, green = standby) pour les mises à jour sans interruption.

    Le trafic utilisateur bascule instantanément de l'environnement blue vers le green une fois la nouvelle version validée. En cas de problème, le rollback est immédiat — il suffit de rebascule le trafic.

    - **Principe :** bascule instantanée entre les deux environnements
    - **Avantages :** zero downtime, rollback en quelques secondes, test en production contrôlé
    - **Contrainte :** coût doublé (deux environnements complets en parallèle)

    ```mermaid
    graph LR
        A[Blue-Green] --> B[Zero downtime]
        A --> C[Rollback immédiat]
        A --> D[Canary — comparaison]
    ```

<br>

---

## C

!!! note "CI/CD"
    > Pratiques d'intégration et de livraison continues automatisant l'ensemble du cycle de développement logiciel.

    L'intégration continue (CI) déclenche automatiquement build et tests à chaque commit. La livraison continue (CD) étend ce pipeline jusqu'au déploiement automatique en production. Ensemble, ils réduisent drastiquement le risque et la durée des cycles de release.

    - **Acronyme :** Continuous Integration / Continuous Deployment (ou Delivery)
    - **Pipeline type :** source → build → test → security scan → deploy → monitor
    - **Outils :** GitHub Actions, GitLab CI, Jenkins, CircleCI, ArgoCD

    ```mermaid
    graph LR
        A[CI/CD] --> B[Intégration continue]
        A --> C[Déploiement continu]
        A --> D[Pipeline automatisé]
    ```

<br>

---

!!! note "Canary Deployment"
    > Stratégie de déploiement progressif orientant une faible proportion du trafic réel vers la nouvelle version pour valider en production.

    Le terme vient des canaris utilisés dans les mines pour détecter les gaz toxiques. Les premières requêtes servent de test — si les métriques se dégradent, le déploiement est stoppé automatiquement.

    - **Principe :** déploiement graduel avec monitoring des métriques clés
    - **Métriques surveillées :** taux d'erreur, latence, business KPIs
    - **Comparaison :** Blue-Green = bascule totale, Canary = progression contrôlée

    ```mermaid
    graph LR
        A[Canary Deployment] --> B[Déploiement progressif]
        A --> C[Monitoring métriques]
        A --> D[Blue-Green comparaison]
    ```

<br>

---

!!! note "Chef"
    > Plateforme d'automatisation d'infrastructure utilisant du code Ruby (cookbooks) pour décrire et appliquer la configuration des serveurs.

    Chef fonctionne en mode client-serveur : un chef-server centralise les politiques, les nodes (clients) les téléchargent et les appliquent. L'approche convergente garantit que chaque exécution ramène le système vers l'état désiré.

    - **Concepts :** cookbooks, recipes, nodes, chef-server, chef-client
    - **Approche :** Infrastructure as Code, convergence automatique
    - **Alternatives :** Ansible (agentless), Puppet (déclaratif)

    ```mermaid
    graph LR
        A[Chef] --> B[Configuration management]
        A --> C[Ruby cookbooks]
        A --> D[Infrastructure as Code]
    ```

<br>

---

!!! note "Configuration Drift"
    > Divergence progressive entre la configuration réelle d'un système et son état désiré, causée par des modifications manuelles non contrôlées.

    La dérive de configuration est un problème silencieux mais critique — des modifications manuelles non tracées peuvent créer des incohérences entre serveurs, rendre les déploiements imprévisibles et compromettre la sécurité.

    - **Causes :** modifications manuelles (ssh + vim), mises à jour partielles, erreurs humaines
    - **Solutions :** configuration management (Ansible, Chef), immutable infrastructure, IaC

    ```mermaid
    graph LR
        A[Configuration Drift] --> B[État désiré]
        A --> C[Monitoring conformité]
        A --> D[Immutable infrastructure]
    ```

<br>

---

## D

!!! note "DAST"
    > Tests de sécurité dynamiques analysant une application en cours d'exécution pour détecter les vulnérabilités exploitables depuis l'extérieur.

    Contrairement au SAST (analyse statique du code), le DAST simule un attaquant externe qui interagit avec l'application en fonctionnement. Il détecte les vulnérabilités runtime comme les injections SQL, XSS, ou mauvaises configurations de sécurité.

    - **Acronyme :** Dynamic Application Security Testing
    - **Approche :** black box testing, simulation d'attaques réelles
    - **Outils :** OWASP ZAP, Burp Suite, Veracode, Acunetix

    ```mermaid
    graph LR
        A[DAST] --> B[Application running]
        A --> C[Simulation attaques]
        A --> D[SAST comparaison]
    ```

<br>

---

!!! note "Docker Registry"
    > Service de stockage et de distribution centralisés d'images de conteneurs Docker.

    Le registry est l'équivalent d'un dépôt de packages pour les images Docker. La pipeline CI/CD construit une image, la pousse vers le registry, puis les orchestrateurs (Kubernetes) la tirent pour l'exécuter.

    - **Types :** public (Docker Hub), privé (Harbor, ECR, ACR, GHCR)
    - **Fonctionnalités :** vulnerability scanning, contrôle d'accès, réplication géographique
    - **Bonnes pratiques :** scanner les images à chaque push, activer le signing (Notary/Cosign)

    ```mermaid
    graph LR
        A[Docker Registry] --> B[Images Docker]
        A --> C[Distribution pipeline]
        A --> D[Kubernetes pull]
    ```

<br>

---

!!! note "DORA Metrics"
    > Métriques de performance DevOps définies par le programme DevOps Research and Assessment pour mesurer la maturité des équipes de livraison.

    Les quatre métriques DORA sont le standard de référence pour évaluer la performance d'une équipe de développement/ops : fréquence de déploiement, délai de mise en production, taux d'échec des changements et temps de rétablissement (MTTR).

    - **4 métriques :** Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR
    - **Niveaux :** Low, Medium, High, Elite performers

    ```mermaid
    graph LR
        A[DORA Metrics] --> B[Performance DevOps]
        A --> C[Amélioration continue]
        A --> D[Benchmarking équipes]
    ```

<br>

---

## F

!!! note "Feature Flag"
    > Technique permettant d'activer ou désactiver des fonctionnalités applicatives en production sans redéploiement.

    Les feature flags découplent le déploiement du code de son activation. Une feature peut être déployée en production mais désactivée — elle est activée progressivement pour des segments d'utilisateurs ou des équipes internes pour validation.

    - **Avantages :** rollback instantané, rollout progressif, A/B testing, trunk-based development
    - **Outils :** LaunchDarkly, Flagsmith, Split.io, OpenFeature

    ```mermaid
    graph LR
        A[Feature Flag] --> B[Activation contrôlée]
        A --> C[A/B testing]
        A --> D[Rollback instantané]
    ```

<br>

---

## G

!!! note "GitOps"
    > Pratique utilisant Git comme source de vérité unique pour l'état de l'infrastructure et des applications, avec synchronisation automatique.

    GitOps applique les principes du développement logiciel (pull requests, code review, historique Git) à la gestion de l'infrastructure. Des agents surveillent le dépôt Git et appliquent automatiquement tout changement détecté.

    - **Principe :** état désiré dans Git, synchronisation automatique par agents (réconciliation)
    - **Outils :** ArgoCD, Flux, Jenkins X
    - **Contraste :** push-based (CI/CD traditionnel) vs. pull-based (GitOps)

    ```mermaid
    graph LR
        A[GitOps] --> B[Git source de vérité]
        A --> C[Déclaratif]
        A --> D[Synchronisation auto]
    ```

<br>

---

!!! note "Grafana"
    > Plateforme open-source de visualisation et de monitoring permettant la création de dashboards interactifs multi-sources.

    Grafana est la solution de visualisation de référence dans les stacks de monitoring modernes. Elle se connecte à des dizaines de sources de données (Prometheus, InfluxDB, Elasticsearch, Loki) et offre des dashboards temps-réel avec alerting intégré.

    - **Sources de données :** Prometheus, InfluxDB, Elasticsearch, CloudWatch, Loki
    - **Fonctionnalités :** alerting, annotations, templating, panels partageables
    - **Stack classique :** Prometheus (collecte) + Grafana (visualisation)

    ```mermaid
    graph LR
        A[Grafana] --> B[Visualisation]
        A --> C[Dashboards temps-réel]
        A --> D[Prometheus source]
    ```

<br>

---

## H

!!! note "Helm"
    > Gestionnaire de paquets pour Kubernetes facilitant le déploiement, la configuration et le versioning d'applications complexes.

    Helm pour Kubernetes, c'est ce que `apt` est pour Debian ou `npm` pour Node.js. Un chart Helm est un template d'application paramétrable — on peut déployer un Nginx, une base de données ou une application complète en une seule commande.

    - **Concepts :** charts (templates), values (paramètres), releases (instances déployées)
    - **Avantages :** réutilisabilité, versioning, rollback, composition d'applications
    - **Dépôts :** Artifact Hub, Bitnami, charts officiels des projets CNCF

    ```mermaid
    graph LR
        A[Helm] --> B[Kubernetes packaging]
        A --> C[Charts templates]
        A --> D[Release versioning]
    ```

<br>

---

## I

!!! note "IaC"
    > Approche consistant à gérer et provisionner l'infrastructure via du code versionné et automatisé plutôt que par des interfaces graphiques manuelles.

    L'Infrastructure as Code traite les serveurs, réseaux et services cloud comme du code source — avec les mêmes bénéfices : versioning Git, code review, tests automatisés et reproductibilité totale des environnements.

    - **Acronyme :** Infrastructure as Code
    - **Outils :** Terraform (multi-cloud), CloudFormation (AWS), Pulumi (langages natifs), ARM templates (Azure)
    - **Principes :** idempotence, déclaratif, reproductibilité

    ```mermaid
    graph LR
        A[IaC] --> B[Infrastructure versionnée]
        A --> C[Terraform multi-cloud]
        A --> D[Reproductibilité]
    ```

<br>

---

!!! note "Immutable Infrastructure"
    > Architecture où les serveurs et conteneurs ne sont jamais modifiés après déploiement — ils sont remplacés par de nouvelles instances.

    Le principe "replace, don't repair" élimine la dérive de configuration : au lieu de patcher un serveur en production, on génère une nouvelle image avec les correctifs et on remplace les instances existantes. Les conteneurs Docker sont l'incarnation moderne de ce principe.

    - **Principe :** replace, don't repair — nouvelles instances remplacent les anciennes
    - **Bénéfices :** consistency totale, rollback simple, prévisibilité
    - **Lien avec :** Configuration Drift (éliminé), IaC (provisionne les nouvelles instances)

    ```mermaid
    graph LR
        A[Immutable Infrastructure] --> B[Replace not repair]
        A --> C[Consistency totale]
        A --> D[Configuration Drift éliminé]
    ```

<br>

---

## J

!!! note "Jenkins"
    > Serveur d'automatisation open-source pour CI/CD avec une architecture extensible via un écosystème riche de plugins.

    Jenkins est l'un des serveurs CI/CD les plus répandus. Son architecture master/agents lui permet de distribuer les builds sur plusieurs machines. Les pipelines sont définis en code (Jenkinsfile) pour être versionnés avec le projet.

    - **Architecture :** controller (master) + agents (workers)
    - **Concepts :** jobs, pipelines déclaratifs, Jenkinsfile, plugins (>1800 disponibles)
    - **Alternative moderne :** GitHub Actions, GitLab CI (intégration native à la forge)

    ```mermaid
    graph LR
        A[Jenkins] --> B[CI/CD]
        A --> C[Pipelines Jenkinsfile]
        A --> D[Plugins ecosystem]
    ```

<br>

---

## M

!!! note "MTTR"
    > Temps moyen nécessaire pour restaurer un service après une panne ou un incident de production.

    Le MTTR est une métrique DORA fondamentale : une équipe elite résout ses incidents en moins d'une heure. Il se réduit par le monitoring proactif, l'automatisation des runbooks et la pratique des post-mortems.

    - **Acronyme :** Mean Time To Recovery / Restore
    - **Amélioration :** monitoring précis, automation, runbooks, post-mortems sans blâme
    - **Lien avec :** DORA Metrics (l'une des 4 métriques clés)

    ```mermaid
    graph LR
        A[MTTR] --> B[Incident response]
        A --> C[Disponibilité service]
        A --> D[DORA Metrics]
    ```

<br>

---

!!! note "Monitoring"
    > Surveillance continue des systèmes, applications et infrastructure pour détecter et résoudre les problèmes proactivement.

    Le monitoring est le système nerveux de toute infrastructure en production. Il couvre trois dimensions : les métriques d'infrastructure (CPU, mémoire, disque), les métriques applicatives (latence, taux d'erreur) et les métriques métier (commandes, conversions).

    - **Types :** infrastructure, application (APM), business metrics, logs, traces
    - **Stack :** collecte → stockage → visualisation → alerting
    - **Évolution :** monitoring → observabilité (logs + métriques + traces)

    ```mermaid
    graph LR
        A[Monitoring] --> B[Métriques]
        A --> C[Alerting]
        A --> D[Observabilité]
    ```

<br>

---

## P

!!! note "Pipeline"
    > Séquence automatisée d'étapes transformant le code source en livrable déployé et vérifié en production.

    Le pipeline CI/CD est le cœur du DevSecOps — chaque commit déclenche automatiquement une chaîne de vérifications (build, tests unitaires, scans de sécurité, tests d'intégration, déploiement) sans intervention humaine.

    - **Étapes types :** checkout → build → test → security scan → containerize → deploy → verify
    - **Types :** CI pipeline (validation), CD pipeline (livraison), deployment pipeline (production)
    - **Concept :** "fail fast" — détecter les problèmes le plus tôt possible dans la chaîne

    ```mermaid
    graph LR
        A[Pipeline] --> B[Automatisation]
        A --> C[Étapes sequentielles]
        A --> D[Livraison continue]
    ```

<br>

---

!!! note "Prometheus"
    > Système de monitoring et d'alerting open-source collectant et stockant des métriques en base de données temporelle (time-series).

    Prometheus est devenu le standard de facto du monitoring cloud-native. Son modèle pull-based — il va chercher les métriques chez les applications — et son langage de requête PromQL permettent des analyses précises et flexibles.

    - **Architecture :** pull-based, service discovery automatique, scrape intervals configurables
    - **Langage de requête :** PromQL (Prometheus Query Language)
    - **Écosystème :** Grafana (visualisation), Alertmanager (alerting), exporters (node, blackbox, etc.)

    ```mermaid
    graph LR
        A[Prometheus] --> B[Time-series DB]
        A --> C[PromQL requêtes]
        A --> D[Grafana visualisation]
    ```

<br>

---

## R

!!! note "Rolling Deployment"
    > Stratégie de mise à jour progressive remplaçant les instances de l'ancienne version une par une tout en maintenant le service disponible.

    Kubernetes implémente nativement le rolling deployment : les pods sont remplacés un par un (ou par groupe), et des health checks valident chaque nouvelle instance avant de passer à la suivante. Si un pod échoue, le déploiement s'arrête.

    - **Principe :** remplacement graduel avec health checks à chaque étape
    - **Avantages :** zero downtime, rollback partiel possible, utilisation des ressources optimisée
    - **Comparaison :** Blue-Green (bascule totale) vs. Rolling (progressif)

    ```mermaid
    graph LR
        A[Rolling Deployment] --> B[Mise à jour progressive]
        A --> C[Zero downtime]
        A --> D[Health checks]
    ```

<br>

---

!!! note "Runbook"
    > Documentation procédurale détaillée guidant les équipes ops lors des opérations courantes et de la résolution d'incidents.

    Un runbook transforme l'expertise tacite des ingénieurs en procédures documentées et reproductibles. Pour chaque type d'incident courant, il décrit les symptômes, les étapes de diagnostic, les actions correctives et les voies d'escalade.

    - **Contenu :** symptômes, étapes de diagnostic, actions correctives, escalade, contacts
    - **Format :** markdown/wiki, automation scripts, playbooks SOAR
    - **Bonne pratique :** tester et mettre à jour les runbooks après chaque incident

    ```mermaid
    graph LR
        A[Runbook] --> B[Procédures incidents]
        A --> C[Diagnostic guidé]
        A --> D[Automation SOAR]
    ```

<br>

---

## S

!!! note "SAST"
    > Tests de sécurité statiques analysant le code source sans l'exécuter pour détecter les vulnérabilités dès le développement.

    Le SAST est le "shift left" de la sécurité : en analysant le code avant son exécution, il détecte les injections SQL, les XSS, les secrets hardcodés ou les mauvaises pratiques cryptographiques dès la phase de développement, là où le coût de correction est le plus faible.

    - **Acronyme :** Static Application Security Testing
    - **Approche :** white box testing, analyse AST, détection de patterns dangereux
    - **Outils :** SonarQube, Checkmarx, Semgrep, Veracode, CodeQL

    ```mermaid
    graph LR
        A[SAST] --> B[Analyse code source]
        A --> C[Shift left sécurité]
        A --> D[DAST comparaison]
    ```

<br>

---

!!! note "SCA"
    > Analyse des composants et dépendances tierces utilisées dans un projet pour identifier les vulnérabilités et les licences problématiques.

    La quasi-totalité du code applicatif moderne dépend de centaines de bibliothèques open source. Le SCA les inventorie et les confronte aux bases CVE pour signaler les dépendances vulnérables.

    - **Acronyme :** Software Composition Analysis
    - **Périmètre :** bibliothèques open source, licences, CVE connues, transitive dependencies
    - **Outils :** Snyk, WhiteSource (Mend), Black Duck, Dependabot (GitHub)

    ```mermaid
    graph LR
        A[SCA] --> B[Dépendances tierces]
        A --> C[CVE vulnerabilités]
        A --> D[Open source licences]
    ```

<br>

---

!!! note "Secret Management"
    > Gestion sécurisée et centralisée des informations sensibles telles que mots de passe, clés API, certificats et tokens.

    Hardcoder un secret dans le code source est l'une des erreurs de sécurité les plus fréquentes — et les plus dangereuses. Un secret management robuste stocke les credentials de manière chiffrée, avec audit trail, rotation automatique et accès au moindre privilège.

    - **Bonnes pratiques :** rotation automatique, accès minimal (moindre privilège), audit trail complet
    - **Outils :** HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Kubernetes Secrets (+ SOPS/Sealed Secrets)

    ```mermaid
    graph LR
        A[Secret Management] --> B[Credentials chiffrés]
        A --> C[Rotation automatique]
        A --> D[Audit trail]
    ```

<br>

---

!!! note "SRE"
    > Discipline appliquant les principes et méthodes de l'ingénierie logicielle aux opérations pour améliorer la fiabilité des systèmes.

    Inventé par Google en 2003, le Site Reliability Engineering traite la fiabilité comme une feature logicielle. Les SRE défendent des SLO (objectifs de niveau de service) et gèrent un "error budget" — si le budget d'erreurs est épuisé, plus aucun déploiement risqué n'est autorisé.

    - **Acronyme :** Site Reliability Engineering
    - **Concepts :** SLI (indicateurs), SLO (objectifs), error budgets, toil (travail répétitif à automatiser)
    - **Origine :** Google (Ben Treynor Sloss, 2003)

    ```mermaid
    graph LR
        A[SRE] --> B[Fiabilité système]
        A --> C[SLO error budgets]
        A --> D[Automatisation toil]
    ```

<br>

---

## T

!!! note "Terraform"
    > Outil d'Infrastructure as Code permettant de provisionner et gérer des ressources sur n'importe quel cloud de manière déclarative.

    Terraform décrit l'état désiré de l'infrastructure en HCL (HashiCorp Configuration Language), puis calcule et applique les modifications nécessaires pour atteindre cet état. Il maintient un fichier d'état (state) qui représente la réalité de l'infrastructure provisionnée.

    - **Concepts :** providers (AWS/Azure/GCP/...), resources, data sources, modules, state
    - **Workflow :** `terraform plan` (simulation) → `terraform apply` (application) → `terraform destroy`
    - **Alternative :** OpenTofu (fork open source), Pulumi (langages natifs)

    ```mermaid
    graph LR
        A[Terraform] --> B[Infrastructure as Code]
        A --> C[Multi-cloud providers]
        A --> D[State management]
    ```

<br>

---

## V

!!! note "Vault"
    > Gestionnaire de secrets centralisé d'HashiCorp pour stocker, accéder et gérer les informations sensibles de manière sécurisée.

    Vault va au-delà du simple stockage de secrets : il génère des credentials dynamiques à durée de vie limitée (ex. des identifiants PostgreSQL temporaires valables 1 heure), garantissant que même une fuite de secret expire rapidement.

    - **Fonctionnalités :** chiffrement transit/repos, dynamic secrets, PKI as a service, audit logging
    - **Secrets engines :** AWS, database, PKI, SSH, KV, Transit
    - **Intégrations :** Kubernetes (sidecar injection), CI/CD pipelines, cloud providers

    ```mermaid
    graph LR
        A[Vault] --> B[Secrets chiffrés]
        A --> C[Dynamic secrets TTL]
        A --> D[Audit logging]
    ```

<br>

---

## Conclusion

!!! quote "Résumé — DevSecOps"
    DevSecOps, c'est l'alliance de trois cultures : la vélocité du développement (CI/CD, Pipeline, Feature Flags), la rigueur des opérations (IaC, Monitoring, SRE, Runbooks) et la sécurité intégrée dès la conception (SAST, DAST, SCA, Secret Management). Ces termes forment le vocabulaire de l'ingénieur moderne qui livre vite, fréquemment et en toute confiance.

> Continuez avec le [Glossaire Développement Mobile](./developpement-mobile.md) pour explorer les concepts Swift, iOS et les frameworks Apple.
