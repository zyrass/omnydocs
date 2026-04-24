---
description: "Découverte de GitLab CI/CD : architecture des runners, définition des pipelines via .gitlab-ci.yml, stages, artifacts et bonnes pratiques pour l'entreprise."
icon: lucide/book-open-check
tags: ["GITLAB", "CICD", "RUNNERS", "YAML", "PIPELINE", "AUTOMATISATION"]
---

# GitLab CI/CD

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="1.0"
  data-time="15 Minutes">
</div>

## Introduction à GitLab CI/CD

!!! quote "Définition : GitLab CI/CD"
    Intégré par défaut à l'écosystème GitLab, **GitLab CI/CD** est un moteur puissant d'automatisation des tests, de la construction et du déploiement d'applications. 

Si GitHub Actions brille par son écosystème communautaire (Marketplace), GitLab CI/CD est historiquement le **chouchou des grandes entreprises** grâce à sa flexibilité extrême, sa gestion fine des environnements (Environments & Deployments) et surtout son architecture basée sur des **GitLab Runners** très faciles à héberger soi-même (On-Premise).

<br>

---

## 1. L'Architecture : GitLab Server vs GitLab Runners

Le paradigme de GitLab CI/CD repose sur une stricte séparation des rôles entre le chef d'orchestre et les ouvriers.

```mermaid
flowchart LR
    Dev([Développeur]) -- "git push" --> GL[Serveur GitLab\n(Gère les dépôts & l'UI)]
    
    subgraph "GitLab Runners (Les Ouvriers)"
        R1[Runner 1\nServeur Linux]
        R2[Runner 2\nConteneur Docker]
        R3[Runner 3\nServeur Windows]
    end

    GL -- "Envoie des Jobs" --> R1
    GL -- "Envoie des Jobs" --> R2
    GL -- "Envoie des Jobs" --> R3
    
    R1 -. "Remonte les Logs & Statuts" .-> GL
    R2 -. "Remonte les Logs & Statuts" .-> GL

    style GL fill:#fc6d26,stroke:#fff,stroke-width:2px,color:#fff
    style R1 fill:#34495e,stroke:#fff,stroke-width:2px,color:#fff
    style R2 fill:#2980b9,stroke:#fff,stroke-width:2px,color:#fff
```

Contrairement à de vieux systèmes, le Serveur GitLab ne compile **jamais** de code. Il se contente de lire votre fichier de configuration et de distribuer les tâches aux **Runners**. 
Vous pouvez enregistrer vos propres serveurs (ou instances EC2) en tant que Runners privés pour exécuter des builds lourds sans payer de frais de minutes cloud à GitLab.

<br>

---

## 2. Anatomie d'un pipeline `.gitlab-ci.yml`

Tout le pipeline est défini dans un fichier à la racine du projet nommé `.gitlab-ci.yml`. GitLab utilise la notion de **Stages** (étapes) pour garantir l'ordre d'exécution. Tous les jobs d'un même stage s'exécutent en parallèle, et le stage suivant ne démarre que si le précédent a réussi.

```yaml title=".gitlab-ci.yml"
# 1. Image Docker par défaut pour tous les jobs
image: node:20-alpine

# 2. Définition de l'ordre d'exécution global
stages:
  - lint
  - test
  - build
  - deploy

# --- STAGE: LINT ---
eslint_check:
  stage: lint
  script:
    - npm ci
    - npm run lint

# --- STAGE: TEST ---
unit_tests:
  stage: test
  script:
    - npm ci
    - npm run test:unit
  # Conserver les résultats (coverage) même si ça échoue
  artifacts:
    when: always
    paths:
      - coverage/

# --- STAGE: BUILD ---
build_app:
  stage: build
  script:
    - npm ci
    - npm run build
  # Conserver le dossier "dist/" pour le prochain stage
  artifacts:
    expire_in: 1 week
    paths:
      - dist/

# --- STAGE: DEPLOY ---
deploy_production:
  stage: deploy
  script:
    - echo "Déploiement en cours sur le serveur..."
    - rsync -avz ./dist/ user@serveur:/var/www/html/
  # Ce job ne s'exécute que si on pousse sur la branche main
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### Concepts cruciaux du YAML GitLab
*   **image** : Presque tous les jobs GitLab s'exécutent dans un conteneur Docker éphémère. Vous choisissez l'image de base (`node`, `php`, `python`).
*   **artifacts** : Contrairement à GitHub Actions où les fichiers passent difficilement d'un job à l'autre, les artefacts GitLab permettent de stocker des fichiers générés (comme un dossier `dist/` compilé) et de les rendre accessibles automatiquement aux jobs des stages suivants.
*   **rules** (anciennement `only/except`) : Permet de conditionner finement quand un job doit tourner (ex: uniquement sur des tags de version, ou uniquement si un fichier spécifique a été modifié).

<br>

---

## 3. Variables CI/CD et Environnements

GitLab gère excellemment le cycle de vie des environnements (Staging, Pre-Prod, Prod).

Dans les paramètres du projet (*Settings > CI/CD > Variables*), vous pouvez stocker vos secrets (clés API, mots de passe). Vous pouvez même "protéger" une variable pour qu'elle ne soit exposée **que** lors d'un déploiement sur la branche `main`, évitant ainsi qu'une branche de test n'utilise la base de données de production.

```yaml title="Exemple d'environnement"
deploy_staging:
  stage: deploy
  script:
    - ./deploy.sh
  environment:
    name: staging
    url: https://staging.monsite.com
```

!!! tip "L'intégration DevSecOps native"
    L'un des gros points forts de la version payante (Ultimate) de GitLab est l'intégration clé en main de scanners de sécurité (SAST, DAST, Container Scanning, Dependency Scanning) qui injectent automatiquement leurs rapports de vulnérabilités directement dans l'interface de Merge Request.