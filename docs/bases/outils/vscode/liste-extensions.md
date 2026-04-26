---
description: "Extensions VS Code — La sélection d'extensions indispensables par domaine : PHP/Laravel, Python, JavaScript, Git, et outils de productivité universels."
icon: lucide/book-open-check
tags: ["VSCODE", "EXTENSIONS", "PHP", "LARAVEL", "PYTHON", "PRODUCTIVITÉ"]
---

# Extensions VS Code — La Sélection Pro

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="2024.x"
  data-time="~10 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Boîte à Outils du Menuisier"
    Un menuisier débutant achète une boîte à outils générique avec 200 outils dont il n'utilisera jamais 150. Un menuisier expert possède 30 outils soigneusement choisis, parfaitement entretenus, parfaitement adaptés à son travail.

    Les **extensions VS Code** fonctionnent de la même façon. Installer 50 extensions au hasard ralentit l'éditeur et crée des conflits. Cette liste est la **sélection raisonnée** : un outil par besoin, choisi pour sa qualité et sa maintenance active.

<br>

---

## Extensions Universelles (Tout Développeur)

```bash title="Installation en une ligne (terminal VS Code)"
code --install-extension eamodio.gitlens \
     --install-extension usernamehw.errorlens \
     --install-extension streetsidesoftware.code-spell-checker \
     --install-extension pkief.material-icon-theme \
     --install-extension oderwat.indent-rainbow \
     --install-extension mechatroner.rainbow-csv \
     --install-extension ms-vsliveshare.vsliveshare
```

| Extension | ID | Utilité |
|---|---|---|
| **GitLens** | `eamodio.gitlens` | Blame Git inline, historique, comparaisons de branches |
| **Error Lens** | `usernamehw.errorlens` | Affiche les erreurs directement sur la ligne concernée |
| **Code Spell Checker** | `streetsidesoftware.code-spell-checker` | Correction orthographique dans le code et les commentaires |
| **Material Icon Theme** | `pkief.material-icon-theme` | Icônes par type de fichier dans l'explorateur |
| **Indent Rainbow** | `oderwat.indent-rainbow` | Colorisation des niveaux d'indentation |
| **Rainbow CSV** | `mechatroner.rainbow-csv` | Coloration et requêtes SQL sur les fichiers CSV |
| **Live Share** | `ms-vsliveshare.vsliveshare` | Collaboration en temps réel avec un collègue |

<br>

---

## PHP / Laravel

```bash
code --install-extension bmewburn.vscode-intelephense-client \
     --install-extension amiralizadeh9480.laravel-extra-intellisense \
     --install-extension onecentlin.laravel-blade \
     --install-extension shufo.vscode-blade-formatter
```

| Extension | ID | Utilité |
|---|---|---|
| **PHP Intelephense** | `bmewburn.vscode-intelephense-client` | Autocomplétion, navigation, refactoring PHP (payant pour certaines features avancées) |
| **Laravel Extra Intellisense** | `amiralizadeh9480.laravel-extra-intellisense` | Autocomplétion des routes, vues, configs, modèles Laravel |
| **Laravel Blade Syntax** | `onecentlin.laravel-blade` | Coloration syntaxique des templates Blade |
| **Blade Formatter** | `shufo.vscode-blade-formatter` | Formatage automatique des fichiers `.blade.php` |

<br>

---

## Python

```bash
code --install-extension ms-python.python \
     --install-extension ms-python.black-formatter \
     --install-extension ms-python.pylint \
     --install-extension ms-toolsai.jupyter
```

| Extension | ID | Utilité |
|---|---|---|
| **Python** | `ms-python.python` | Extension officielle Microsoft (IntelliSense, debug, tests) |
| **Black Formatter** | `ms-python.black-formatter` | Formatage PEP 8 automatique avec Black |
| **Pylint** | `ms-python.pylint` | Analyse statique du code Python |
| **Jupyter** | `ms-toolsai.jupyter` | Notebooks Jupyter directement dans VS Code |

<br>

---

## JavaScript / TypeScript / Web

```bash
code --install-extension esbenp.prettier-vscode \
     --install-extension dbaeumer.vscode-eslint \
     --install-extension bradlc.vscode-tailwindcss \
     --install-extension vue.volar
```

| Extension | ID | Utilité |
|---|---|---|
| **Prettier** | `esbenp.prettier-vscode` | Formatage JS/TS/CSS/HTML/JSON |
| **ESLint** | `dbaeumer.vscode-eslint` | Linting JavaScript/TypeScript |
| **Tailwind CSS IntelliSense** | `bradlc.vscode-tailwindcss` | Autocomplétion des classes Tailwind |
| **Vue - Official** | `vue.volar` | Support complet Vue 3 / Nuxt 3 |

<br>

---

## Infrastructure & Devops

```bash
code --install-extension ms-azuretools.vscode-docker \
     --install-extension hashicorp.terraform \
     --install-extension redhat.vscode-yaml \
     --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
```

| Extension | ID | Utilité |
|---|---|---|
| **Docker** | `ms-azuretools.vscode-docker` | Gestion des conteneurs, images et Compose depuis VS Code |
| **HashiCorp Terraform** | `hashicorp.terraform` | Coloration, validation et IntelliSense Terraform |
| **YAML** | `redhat.vscode-yaml` | Validation YAML avec schémas (Kubernetes, GitHub Actions) |
| **Kubernetes** | `ms-kubernetes-tools.vscode-kubernetes-tools` | Exploration et déploiement sur clusters K8s |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La règle d'or des extensions VS Code : **une extension = un besoin précis**. Résistez à l'envie d'installer toutes les extensions bien notées. Chaque extension inutilisée alourdit l'éditeur et consomme des ressources. Commencez avec les universelles + les extensions de votre stack principale, et ajoutez au fur et à mesure des besoins réels.

> [Les Snippets VS Code — Automatiser les patterns répétitifs →](./snippet.md)
