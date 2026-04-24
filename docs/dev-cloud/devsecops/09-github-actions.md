---
description: "Découverte de GitHub Actions : automatisation des workflows, CI/CD natif, concepts fondamentaux (Events, Jobs, Runners) et création d'un premier pipeline YAML."
icon: lucide/book-open-check
tags: ["GITHUB", "ACTIONS", "CICD", "WORKFLOW", "YAML", "AUTOMATISATION"]
---

# GitHub Actions

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="1.0"
  data-time="15 Minutes">
</div>

## Introduction à GitHub Actions

!!! quote "Définition : GitHub Actions"
    **GitHub Actions** est la plateforme d'intégration continue et de livraison continue (CI/CD) intégrée nativement à GitHub. Elle permet d'automatiser vos flux de travail logiciels directement depuis votre dépôt de code.

Finis les serveurs Jenkins lourds à maintenir : avec GitHub Actions, l'automatisation se déclare sous forme de fichiers de configuration `YAML` et s'exécute sur des serveurs éphémères (les **Runners**) fournis par GitHub ou hébergés par vos soins.

<br>

---

## 1. Concepts Fondamentaux

Pour maîtriser GitHub Actions, il faut comprendre l'anatomie d'une exécution. L'approche est purement événementielle.

```mermaid
flowchart TD
    E[Event\n(Ex: push sur la branche main)] --> W{Workflow\n(Fichier .yml)}
    W --> J1(Job 1 : Tests\nS'exécute sur Ubuntu)
    W --> J2(Job 2 : Build\nS'exécute sur Windows)
    
    J1 -. "Succès" .-> J3(Job 3 : Déploiement\nS'exécute si J1 est OK)
    
    subgraph Job 1 [Détail d'un Job]
        S1[Step 1 : Cloner le code] --> S2[Step 2 : Installer Node.js]
        S2 --> S3[Step 3 : npm run test]
    end
    
    style E fill:#f39c12,stroke:#fff,stroke-width:2px,color:#fff
    style W fill:#34495e,stroke:#fff,stroke-width:2px,color:#fff
    style J1 fill:#2980b9,stroke:#fff,stroke-width:2px,color:#fff
    style J3 fill:#27ae60,stroke:#fff,stroke-width:2px,color:#fff
```

### Le vocabulaire de base
*   **Workflow** : Une procédure automatisée configurable (ex: "Déployer en Prod"). Défini par un fichier YAML dans le dossier `.github/workflows/`.
*   **Events** : Ce qui déclenche le workflow (un `push`, la création d'une `pull_request`, une tâche planifiée `schedule`, ou un clic manuel `workflow_dispatch`).
*   **Jobs** : Un ensemble d'étapes (steps) exécutées sur un même serveur (Runner). Les jobs s'exécutent en parallèle par défaut, sauf si on définit des dépendances (`needs`).
*   **Steps** : Une tâche individuelle au sein d'un job. Ça peut être une simple commande shell (ex: `npm install`) ou une **Action** réutilisable.
*   **Runners** : Le serveur (Linux, Windows, macOS) qui exécute vos workflows.

<br>

---

## 2. Anatomie d'un Workflow YAML

Voici l'exemple classique d'un pipeline d'Intégration Continue (CI) pour une application Node.js. Le but : vérifier que le code compile et que les tests passent à chaque fois qu'un développeur pousse son code.

```yaml title=".github/workflows/ci.yml"
name: Intégration Continue (Node.js)

# 1. Événements déclencheurs
on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main" ]

# 2. Les tâches à exécuter
jobs:
  test-and-build:
    name: Tester et Compiler
    runs-on: ubuntu-latest # Le Runner

    # 3. Les étapes
    steps:
      # Action officielle GitHub pour cloner le code
      - name: 📥 Cloner le dépôt
        uses: actions/checkout@v4

      # Action officielle pour installer Node.js
      - name: ⚙️ Configurer Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm' # Accélère les futures exécutions

      - name: 📦 Installer les dépendances
        run: npm ci

      - name: 🧪 Exécuter les tests (Lint & Unit)
        run: |
          npm run lint
          npm run test

      - name: 🏗️ Compiler le projet
        run: npm run build
```

!!! tip "Les Actions du Marketplace"
    L'un des plus grands atouts de GitHub Actions est son **Marketplace**. Au lieu de réinventer la roue, vous pouvez utiliser des actions créées par la communauté (via la directive `uses:`), par exemple pour configurer SSH, envoyer un message sur Slack, ou déployer sur AWS.

<br>

---

## 3. Gestion des Secrets (DevSecOps)

Il est **strictement interdit** de coder en dur des mots de passe ou des clés API dans vos fichiers YAML. 

GitHub propose un coffre-fort chiffré intégré : les **GitHub Secrets**.
1. Allez dans *Settings > Secrets and variables > Actions* de votre dépôt.
2. Ajoutez un secret, par exemple `DOCKERHUB_TOKEN`.
3. Utilisez-le dans votre workflow via la syntaxe `${{ secrets.DOCKERHUB_TOKEN }}`.

```yaml title="Exemple : Déploiement sécurisé"
      - name: 🐳 Connexion à DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

Les secrets ne seront jamais affichés en clair dans les logs d'exécution (ils sont masqués par des étoiles `***`).

!!! note "Variables vs Secrets"
    Si la valeur n'est pas confidentielle (ex: l'URL d'un environnement de staging `API_URL=staging.monsite.com`), utilisez les **Variables d'environnement** de GitHub Actions au lieu des Secrets. Cela rend vos logs plus lisibles et facilite le débogage.