---
description: "Référentiel des diagrammes Mermaid supportés par Zensical — exemples, cas d'usage et statuts de rendu."
tags: ["MERMAID", "REFERENCE", "DIAGRAMMES", "ZENSICAL"]
---

# Référentiel Mermaid

<div
  class="omny-meta"
  data-level="Tous niveaux"
  data-version="2.1"
  data-time="15-20 minutes">
</div>

!!! quote "Analogie"
    _Un diagramme bien choisi remplace un paragraphe entier. Encore faut-il savoir lequel choisir, et savoir s'il sera correctement rendu par l'outil. Ce référentiel répond aux deux questions._

## Objectif

La maîtrise des diagrammes Mermaid est un atout significatif pour produire une documentation technique claire, structurée et maintenable. Dans OmnyDocs, **la visualisation des flux**, **architectures** et **processus** est **un pilier central de compréhension** : elle réduit l'ambiguïté, accélère la lecture et améliore la capacité de relecture et de maintenance.

Ce référentiel remplit deux rôles distincts :

- valider de manière factuelle ce que le renderer Zensical supporte réellement
- fournir aux lecteurs une vue d'ensemble des types de diagrammes disponibles dans la documentation, avec des exemples concrets et des cas d'usage associés

<br />

---

## Diagrammes essentiels

Les diagrammes essentiels couvrent les besoins les plus fréquents : flux décisionnels, échanges entre composants, architecture en zones. Ils constituent la base visuelle de la documentation.

<div class="grid cards" markdown>

- ### :lucide-square-library: Flowchart
    ---
    Flux décisionnels, workflows, procédures. Le diagramme le plus utilisé en documentation technique.

    [Consulter](./essentiels/flowchart.md)

- ### :lucide-square-library: Flowchart — Subgraph
    ---
    Zones fonctionnelles (client/serveur, LAN/DMZ, équipes). Séparation de responsabilités et frontières d'architecture.

    [Consulter](./essentiels/flowchart_subgraph.md)

- ### :lucide-square-library: Flowchart — Styles & Classes
    ---
    Signalétique normalisée : états OK/Warning/Erreur, composants critiques, chemins à risque. Utile pour les runbooks.

    [Consulter](./essentiels/flowchart_styles_classes.md)

- ### :lucide-square-library: Séquence
    ---
    Chronologie des échanges entre acteurs et composants. Authentification, appels API, traitement asynchrone, incidents.

    [Consulter](./essentiels/sequence.md)

- ### :lucide-square-library: Séquence — Alt / Else
    ---
    Scénarios conditionnels : succès/échec, autorisé/refusé, timeout/réessai. Essentiel pour documenter les contrôles de sécurité.

    [Consulter](./essentiels/sequence_alt_else.md)

</div>


<br />

---

## Modélisation

Les diagrammes de modélisation servent à représenter la structure statique d'un système : entités, relations, états, classes. Incontournables pour le développement et la documentation d'architecture.

<div class="grid cards" markdown>

- ### :lucide-square-library: Class UML
    ---
    Structure des classes, héritage, associations. Référence pour la modélisation orientée objet et la documentation de code.

    [Consulter](./modelisation/class_uml.md)

- ### :lucide-square-library: Diagramme ER
    ---
    Entités et relations d'une base de données. Indispensable pour documenter un schéma de données ou un modèle relationnel.

    [Consulter](./modelisation/er.md)

- ### :lucide-square-library: State Diagram
    ---
    États et transitions d'un système ou d'un objet. Authentification, cycle de vie d'une session, automates finis.

    [Consulter](./modelisation/state.md)

</div>


<br />

---

## Pilotage

Les diagrammes de pilotage représentent la dimension temporelle et l'historique d'un projet ou d'un dépôt. Utiles pour la planification et la documentation de processus DevSecOps.

<div class="grid cards" markdown>

- ### :lucide-square-library: Gantt
    ---
    Planification de projet, jalons, dépendances entre tâches. Référence pour la gestion de projet technique.

    [Consulter](./pilotage/gantt.md)

- ### :lucide-square-library: GitGraph
    ---
    Visualisation des branches et commits Git. Utile pour documenter une stratégie de branching ou un workflow CI/CD.

    [Consulter](./pilotage/gitgraph.md)

</div>

<br />

---

## Synthèse

Les diagrammes de synthèse offrent une lecture agrégée d'un jeu de données ou d'une expérience utilisateur. Complémentaires aux diagrammes techniques pour les sections pédagogiques et les bilans.

<div class="grid cards" markdown>

- ### :lucide-square-library: Journey
    ---
    Parcours utilisateur, expérience étape par étape. Utile pour documenter un onboarding ou un flux d'interaction.

    [Consulter](./synthese/journey.md)

- ### :lucide-square-library: Pie Chart
    ---
    Répartition proportionnelle de données. Lecture rapide d'une distribution (vulnérabilités, couverture, répartition budgétaire).

    [Consulter](./synthese/piechart.md)

</div>

<br />

---

## Avancés

Les diagrammes avancés exploitent des syntaxes récentes ou en version bêta. Leur support par Zensical est à valider — ce référentiel est précisément là pour trancher.

<div class="grid cards" markdown>

- ### :lucide-square-library: Architecture
    ---
    Représentation de composants d'infrastructure. Syntaxe récente à valider sous Zensical.

    [Consulter](./avances/architecture.md)

- ### :lucide-square-library: Block Diagram
    ---
    Blocs fonctionnels et dépendances. Alternative au flowchart pour les vues d'ensemble architecturales.

    [Consulter](./avances/block.md)

- ### :lucide-square-library: Mindmap
    ---
    Arborescence de concepts. Utile pour des vues pédagogiques ou des cartographies de domaines.

    [Consulter](./avances/mindmap.md)

- ### :lucide-square-library: Quadrant
    ---
    Matrice 2×2 à axes libres. Priorisation, positionnement stratégique, cartographie de risques.

    [Consulter](./avances/quadrant.md)

- ### :lucide-square-library: Radar
    ---
    Comparaison multi-axes. Utilisé dans OmnyDocs pour les diagrammes de compétences par parcours.

    [Consulter](./avances/radar.md)

- ### :lucide-square-library: Timeline
    ---
    Chronologie d'événements. Historique de versions, jalons projet, séquence d'incidents.

    [Consulter](./avances/timeline.md)

- ### :lucide-square-library: XY Chart
    ---
    Graphique cartésien (barres, lignes). Données quantitatives, métriques, évolutions.

    [Consulter](./avances/xychart.md)

- ### :lucide-square-library: ZenUML
    ---
    Syntaxe alternative pour les diagrammes de séquence. Support Zensical à confirmer.

    [Consulter](./avances/zenuml.md)

</div>

<br />

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Si les diagrammes essentiels et de modélisation sont correctement rendus, OmnyDocs dispose d'une base visuelle solide pour documenter avec clarté le code, les systèmes et la cybersécurité. Les diagrammes avancés renforcent la qualité pédagogique à condition d'être supportés par Zensical — chaque page de la section Avancés indique le statut de rendu constaté.

> [Commencer par les diagrammes essentiels →](./essentiels/flowchart.md)