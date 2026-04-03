---
description: "Série de projets d'apprentissage progressifs avec Alpine.js"
icon: lucide/mountain-snow
tags: ["PROJET", "ALPINE", "LAB", "INDEX"]
---

# Alpine Lab

<div
  class="omny-meta"
  data-level="🟢 Progressif"
  data-version="Alpine 3.x"
  data-time="18 Heures">
</div>

!!! quote "De la théorie à la pratique"
    Bienvenue dans le **Laboratoire Alpine.js**. Vous avez acquis la [Théorie Allégée du Framework](../../dev-cloud/frameworks/alpine/index.md), il est temps de retrousser vos manches. L'objectif de ces 3 projets est de transformer vos connaissances abstraites en outils professionnels réellement utilisables.

<br>

---

## 1. Structure du Programme

La philosophie de ces projets est graduelle. Nous partirons d'une interface simple et locale pour terminer par une Dashboard CyberSécurité intégrant l'export, le calcul mathématique avancé, et la persistance sur disque.

### 🟢 Projet 1 : [Password Generator](./01-password-generator.md)
Un générateur de mots de passe interactif.
* **Objectif :** Maîtriser le Two-Way Data Binding (`x-model`), manipuler les curseurs temporels HTML5 et injecter un état réactif via `x-text`.
* **Points Clés :** `x-data`, `x-model`, `@click`.

### 🟡 Projet 2 : [Currency Converter](./02-currency-converter.md)
Une application connectée de conversion monétaire.
* **Objectif :** Implémenter l'asynchrone. Demander à une API cloud de lui fournir des données réseau au moment où l'application "Mount", gérer un Spinner de chargement conditionnel et réagir organiquement à n'importe quel changement de l'utilisateur.
* **Points Clés :** `x-init`, `$watch`, `x-show`, `x-for`.

### 🔴 Projet 3 : [Pentest Reporting Tool](./03-pentest-tool.md)
Un outil métier complexe de recension des vulnérabilités cyber.
* **Objectif :** Créer une application complète pour enregistrer et filtrer des failles, calculer les codes CVSS v3.1 interactifs de chaque alerte, et sauvegarder pour toujours les avancées dans le Root Local System pour ne jamais perdre le travail de l'auditeur.
* **Points Clés :** `$persist`, `Alpine.store()`, Compositing de variables locales.

<br>

---

L'ensemble du code peut être exécuté dans un simple ficher index.html vierge et ne nécessite aucun outil de "Build" (Node, Webpack, Vite). 
> Préparez votre bloc-notes web et démarrez immédiatement le [Projet 1](./01-password-generator.md).
