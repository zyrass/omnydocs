---
description: "Méthodologies reconnues pour identifier, évaluer et traiter les risques de sécurité de l'information"
tags: ["RISQUES", "EBIOS RM", "MEHARI", "ISO 27005", "ANALYSE"]
---

# Analyse de Risques

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="1.0"
  data-time="6-8 minutes">
</div>


!!! quote "Analogie pédagogique"
    _L'analyse de risques est comme la souscription d'une assurance. Vous n'allez pas payer un coffre-fort à 10 000€ pour protéger un stylo. C'est l'art de proportionner les mesures de sécurité à la valeur de l'actif défendu._

## Introduction

**L'analyse de risques** constitue le **socle fondamental** de toute démarche de sécurité de l'information. Elle permet d'identifier les menaces pesant sur les actifs critiques, d'évaluer leur probabilité et leur impact, puis de définir les mesures de traitement appropriées selon l'appétit au risque de l'organisation.

> Obligatoire dans le cadre d'un SMSI (ISO 27001) et exigée par les réglementations (RGPD, NIS2, DORA), l'analyse de risques transforme la sécurité en **démarche rationnelle et proportionnée** plutôt qu'en accumulation de mesures techniques.

!!! info "Pourquoi l'analyse de risques est essentielle ?"
    - **Priorisation** : Concentrer les efforts sur les risques les plus critiques
    - **Conformité** : Exigence ISO 27001, RGPD, NIS2, DORA
    - **Justification** : Argumenter les investissements sécurité auprès de la direction
    - **Communication** : Langage commun entre technique et métier
    - **Traçabilité** : Démontrer la démarche de gestion des risques aux auditeurs

## Les trois méthodologies majeures

!!! note "Cette section présente les trois méthodologies majeures qui peuvent toutes se substituer les unes aux autres."

<div class="grid cards" markdown>

-   :lucide-shield-alert:{ .lg .middle } **EBIOS Risk Manager** — _Méthode française ANSSI_

    ---

    Méthode de référence de l'**ANSSI** pour la gestion des risques cyber, axée sur les scénarios de menace et l'approche par risque métier.

    **Type** : Méthodologie française | **Portée** : Cyber-risques

    [:lucide-book-open-check: Voir la fiche complète sur EBIOS RM](./ebios-rm/)

-   :lucide-layers:{ .lg .middle } **MEHARI** — _Méthode Harmonisée d'Analyse de Risques_

    ---

    Méthode développée par le **CLUSIF** offrant une approche complète et outillée de la gestion des risques SI.

    **Type** : Méthodologie française | **Portée** : Risques SI globaux

    [:lucide-book-open-check: Voir la fiche complète sur MEHARI](./mehari/)

</div>

<div class="grid cards" markdown>

-   :lucide-globe:{ .lg .middle } **ISO 27005** — _Norme internationale_

    ---

    Norme internationale fournissant un **cadre générique** de gestion des risques SI, alignée avec ISO 31000.

    **Type** : Norme ISO | **Portée** : Risques SI (approche universelle)

    [:lucide-book-open-check: Voir la fiche complète sur ISO 27005](./iso-27005/)

</div>

## Processus d'analyse de risques

Quelle que soit la méthodologie choisie, l'analyse de risques suit généralement ces étapes :

1. **Établir le contexte** : Périmètre, actifs critiques, parties prenantes
2. **Identifier les risques** : Menaces, vulnérabilités, scénarios d'attaque
3. **Évaluer les risques** : Probabilité × Impact = Niveau de risque
4. **Traiter les risques** : Accepter, réduire, transférer, éviter
5. **Surveiller et réviser** : Suivi continu et mises à jour

## Rôle dans le SMSI

L'analyse de risques constitue **l'étape fondatrice** du SMSI (ISO 27001). Elle alimente directement la **Déclaration d'Applicabilité** (Statement of Applicability) qui justifie le choix des mesures de sécurité à implémenter parmi les 93 contrôles d'ISO 27002.

> Les fiches suivantes détaillent chaque méthodologie avec ses étapes, ses outils et ses livrables attendus.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le choix de la méthodologie d'analyse de risques dépend du contexte : EBIOS RM est la référence pour les OIV/OSE et les projets sensibles en France (préconisé par l'ANSSI), MEHARI est plus adaptée aux démarches outillées en entreprise, et ISO 27005 offre le cadre international le plus portable. Quelle que soit la méthode, la rigueur du processus prime sur l'outil choisi.

> [Complétez votre vision GRC avec la gestion opérationnelle des vulnérabilités →](../../vuln/)
