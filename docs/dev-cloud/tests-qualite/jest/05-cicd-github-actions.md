---
description: "Jest — CI/CD & GitHub Actions : Automatiser l'exécution de vos tests unitaires et garantir un niveau de qualité constant sur votre projet Node.js."
icon: lucide/book-open-check
tags: ["JEST", "CICD", "GITHUB ACTIONS", "AUTOMATISATION", "QUALITÉ"]
---

# 05 — CI/CD & GitHub Actions avec Jest

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Jest 29.x / GitHub Actions"
  data-time="~2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    Écrire des tests sur votre machine sans les automatiser, c'est comme avoir un détecteur de fumée que vous devez allumer manuellement de temps en temps. S'il n'est pas automatique 24/7, il ne vous protégera pas le jour de l'incendie. L'Intégration Continue (CI) allume le détecteur à **chaque modification de code**.

L'intégration continue (CI) est le point culminant d'une stratégie de testing. Si les tests ne sont exécutés que manuellement par les développeurs en local, ils seront oubliés.

En configurant **GitHub Actions** pour exécuter Jest, vous garantissez que la branche principale (`main` / `master`) n'accepte aucun code cassé. Si une Pull Request (PR) échoue aux tests, le bouton de fusion (Merge) devient rouge et se bloque.

---

## 1. Préparation du projet (package.json)

Avant d'aller dans la CI, assurez-vous que vos scripts locaux sont prêts. Dans GitHub Actions, nous voulons que Jest échoue si un test plante, et nous voulons générer un rapport de "Coverage" (Couverture de code) sans ouvrir d'interface interactive.

```json title="package.json"
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:ci": "jest --ci --coverage --passWithNoTests"
  }
}
```

*Explications :*
- `--ci` : Dit à Jest qu'il s'exécute sur un serveur sans interface humaine (optimise le formatage de la console).
- `--coverage` : Génère le rapport de pourcentage de code testé.
- `--passWithNoTests` : Évite que la CI ne plante si le projet est tout nouveau et ne contient aucun fichier de test.

---

## 2. Le Workflow GitHub Actions

Créez le fichier YAML suivant à la racine exacte de votre dépôt : `.github/workflows/jest-ci.yml`.

Ce workflow s'exécutera à chaque `push` sur la branche principale, et à chaque `pull_request`.

```yaml title=".github/workflows/jest-ci.yml"
name: Node.js CI (Jest)

on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main", "develop" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    # Optionnel: Tester sur plusieurs versions de Node pour une librairie Open Source
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
    # 1. Télécharger le code source sur la machine virtuelle
    - name: Checkout repository
      uses: actions/checkout@v4

    # 2. Installer et configurer Node.js
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm' # Active le cache ultra-rapide pour npm install

    # 3. Installer les dépendances exactement comme dans package-lock.json
    - name: Install dependencies (ci)
      run: npm ci

    # 4. Lancer Jest en mode CI
    - name: Run Jest Unit Tests
      run: npm run test:ci
```

---

## 3. Définir des seuils de couverture (Coverage Thresholds)

Exécuter les tests c'est bien, s'assurer que les développeurs continuent d'écrire de nouveaux tests pour les nouvelles fonctionnalités, c'est mieux.

Jest permet de faire **échouer la CI** si la couverture de code tombe sous un certain pourcentage. C'est le moyen le plus efficace d'imposer une norme de qualité à toute l'équipe.

```javascript title="jest.config.js"
module.exports = {
  // ...
  coverageThreshold: {
    global: {
      branches: 80,   // 80% des if/else/switch testés
      functions: 80,  // 80% des fonctions testées
      lines: 80,      // 80% des lignes de code testées
      statements: 80
    },
    // On peut exiger 100% sur un dossier critique (ex: algorithme de paiement)
    "./src/services/billing/": {
      branches: 100,
      functions: 100,
      lines: 100
    }
  }
}
```

Si un développeur ajoute 50 lignes de code métier sans écrire de tests, la couverture globale descendra à 79%, Jest renverra une erreur, et la Pull Request sera bloquée.

---

## 4. Afficher le Coverage sur GitHub (Reporter)

Lire un long terminal noir pour trouver l'erreur Jest est pénible en CI. Vous pouvez utiliser des "Reporters" GitHub qui commentent directement sur la Pull Request pour dire : *"Cette PR fait passer la couverture de 80% à 82% !"*.

Pour cela, on utilise généralement des actions tierces (comme `jest-coverage-report-action`) ou on lie le projet à un service cloud spécialisé gratuit pour l'open source comme **Codecov** ou **SonarCloud**.

Exemple d'ajout d'une étape Codecov dans le `jest-ci.yml` :

```yaml
    # ... (après l'étape 'Run Jest')
    
    # Envoie le dossier 'coverage/' généré par Jest vers le dashboard Codecov
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        fail_ci_if_error: true
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un workflow CI basique sur GitHub Actions prend moins de 5 minutes à mettre en place (un fichier YAML) et offre une tranquillité d'esprit immense. C'est le "garde du corps" de votre base de code. En bloquant les fusions de code qui cassent les tests (`npm run test:ci`) et en imposant des seuils de couverture stricts (`coverageThreshold`), vous garantissez qu'une application initialement saine le restera mois après mois.

<br>
