---
description: "Cypress — Cloud et Parallélisme : Optimiser le temps d'exécution des tests E2E via la parallélisation et Cypress Cloud."
icon: lucide/book-open-check
tags: ["CYPRESS", "CLOUD", "PARALLELISME", "OPTIMISATION", "CICD"]
---

# 04 — Cypress Cloud & Parallélisme

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Cypress 13.x"
  data-time="~2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    Imaginons que vous ayez 100 gâteaux à préparer (vos tests) et un seul four (votre machine CI). Cela prendra 5 heures. Le parallélisme, c'est brancher 5 fours en même temps : vous aurez fini en 1 heure. Mais pour que cela fonctionne, il faut un "chef" (Cypress Cloud) qui distribue intelligemment les gâteaux entre les fours pour que tous terminent en même temps.

Le principal défaut des tests E2E est leur lenteur. Une suite de 200 tests Cypress peut facilement prendre 30 minutes sur un pipeline CI (GitHub Actions, GitLab CI). Cela ralentit considérablement la boucle de feedback des développeurs.

La solution : **exécuter les tests en parallèle sur plusieurs machines virtuelles (containers) dans votre CI**.

---

## 1. Pourquoi utiliser Cypress Cloud ?

Cypress open-source (le runner gratuit) ne peut exécuter les tests que sur une seule machine.
Pour exécuter les tests sur plusieurs machines (parallélisme), il faut un outil de coordination central qui :

1. Connaît tous les tests à exécuter.
2. Évalue le temps historique de chaque test.
3. Distribue les fichiers de tests aux différentes machines CI de façon optimisée (Load Balancing).

Cet outil de coordination est **Cypress Cloud** (anciennement Cypress Dashboard), un service SaaS payant (avec un tier gratuit).

### Les fonctionnalités de Cypress Cloud

- **Parallélisation intelligente** : Équilibrage de charge basé sur l'historique d'exécution.
- **Flaky Test Management** : Détection automatique des tests instables (flaky) qui réussissent et échouent sans changement de code.
- **Analytics** : Temps d'exécution, évolution de la suite de tests, erreurs fréquentes.
- **Enregistrements vidéo & Screenshots** : Stockage centralisé pour analyser pourquoi un test a échoué en CI.

---

## 2. Configuration du Parallélisme

### 2.1 Connecter son projet à Cypress Cloud

1. Créez un compte sur [cloud.cypress.io](https://cloud.cypress.io).
2. Créez un nouveau projet.
3. Cypress Cloud vous donnera un `projectId` (à mettre dans `cypress.config.js`) et un `Record Key` (un token secret).

```javascript title="cypress.config.js"
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  projectId: "abcd12", // ID public du projet
  e2e: {
    // ...
  }
})
```

### 2.2 Exécution en ligne de commande

Pour envoyer les résultats à Cypress Cloud, ajoutez l'argument `--record` et la clé secrète :

```bash
npx cypress run --record --key abcdef-12345-67890-abcdef
```

Pour activer la parallélisation, ajoutez l'argument `--parallel` :

```bash
npx cypress run --record --key abcdef-12345-67890 --parallel --ci-build-id $CI_PIPELINE_ID
```
*(Le `ci-build-id` indique à Cypress que ces machines travaillent ensemble sur le même job CI).*

---

## 3. Implémentation GitHub Actions

Voici comment configurer un pipeline GitHub Actions pour exécuter Cypress en parallèle sur **3 machines** virtuelles (`containers: [1, 2, 3]`).

```yaml title=".github/workflows/cypress-parallel.yml"
name: Cypress E2E Tests (Parallèle)

on: [push]

jobs:
  cypress-run:
    runs-on: ubuntu-latest
    
    # Stratégie de matrice : on lance le job 3 fois en même temps
    strategy:
      fail-fast: false
      matrix:
        containers: [1, 2, 3] # 3 machines virtuelles

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Start Application Background
        run: npm start &
        
      # Action officielle Cypress
      - name: Cypress Run
        uses: cypress-io/github-action@v6
        with:
          record: true
          parallel: true
        env:
          # Clé secrète stockée dans les secrets GitHub
          CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
          # Token GitHub automatique pour la CI
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Comment ça marche sous le capot ?

1. GitHub lance 3 machines (containers 1, 2, 3).
2. Chaque machine clone le code, installe Node, lance l'app, et contacte Cypress Cloud : *"Bonjour, je suis la machine 1, donne-moi du travail"*.
3. Cypress Cloud répond : *"Machine 1, exécute login.cy.js et checkout.cy.js"*.
4. Au fil de l'eau, Cypress Cloud distribue les fichiers restants jusqu'à ce que tout soit exécuté.
5. Les résultats (vidéos, erreurs) sont renvoyés à Cypress Cloud et regroupés sous un même rapport.

---

## 4. Alternatives Open-Source (Sorry Cypress / Currents)

Si vous ne pouvez pas utiliser Cypress Cloud (coût, rgpd, réseau fermé), il existe une alternative open-source : **Sorry Cypress** (ou sa version managée *Currents.dev*).

Il s'agit d'un serveur que vous hébergez vous-même et qui simule l'API de Cypress Cloud.

1. Déployez le serveur Sorry Cypress via Docker.
2. Modifiez l'URL de l'API Cypress dans votre projet (via un package comme `cypress-cloud`).
3. Vos tests CI s'exécuteront en parallèle, coordonnés par votre propre serveur gratuit.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Dès que l'exécution de vos tests E2E dépasse 10-15 minutes, l'équipe de développement commence à perdre du temps et à repousser l'écriture des tests. La **parallélisation** est la seule solution technique viable à long terme. Avec Cypress Cloud et un fournisseur CI (GitHub, GitLab, CircleCI), vous pouvez diviser un pipeline de 40 minutes en 5 minutes en ajoutant 8 machines en parallèle, gardant ainsi une boucle de feedback ultra-rapide.

<br>
