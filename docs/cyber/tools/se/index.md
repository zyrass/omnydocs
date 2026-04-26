---
description: "Ingénierie sociale offensive : phishing, spear-phishing, pretexting et simulation de campagnes de manipulation pour évaluer la résistance humaine"
tags: ["SOCIAL ENGINEERING", "PHISHING", "SET", "GOPHISH", "RED TEAM", "SENSIBILISATION"]
---

# Cyber : Social Engineering

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="1.0"
  data-time="5-7 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Cheval de Troie Moderne"
    Imaginez un château imprenable avec des murs de 10 mètres de haut (Firewalls, EDR). Au lieu de l'attaquer de front, vous envoyez un coursier déguisé porter un cadeau au roi. Le garde ouvre la porte parce qu'il a confiance. L'**ingénierie sociale** est ce cadeau piégé : elle utilise la confiance, la peur ou l'urgence pour inciter un humain à ouvrir la porte de l'intérieur, rendant les défenses techniques inutiles.

**L'ingénierie sociale** exploite la psychologie humaine plutôt que les vulnérabilités techniques. Elle représente le vecteur d'attaque le plus efficace dans la réalité opérationnelle : plus de 90% des compromissions débutent par une interaction humaine.

<br>

---

!!! info "Pourquoi cette section est essentielle ?"
    - **Vecteur d'accès initial dominant** : le phishing est la technique d'entrée la plus utilisée dans les attaques réelles
    - **Évaluation de la sensibilisation** : mesurer objectivement le taux de clic et de signalement
    - **Spear-phishing ciblé** : construire des campagnes personnalisées depuis les données OSINT
    - **Pretexting** : simuler des scénarios d'usurpation d'identité crédibles
    - **Démonstration d'impact** : prouver qu'une compromission via le facteur humain est réaliste

## Les outils de cette section

<div class="grid cards" markdown>

-   **SET — Social-Engineer Toolkit**

    ---

    Framework complet d'attaques d'ingénierie sociale (TrustedSec). Automatise la création de campagnes de phishing, le clonage de sites web pour la capture de credentials, la génération de payloads pour les attaques par pièces jointes et les vecteurs d'attaque SMS/voix.

    [Voir SET](./set.md)

-   **GoPhish**

    ---

    Plateforme open source de simulation de phishing. Interface web complète pour créer des campagnes, gérer des listes de cibles, personnaliser les e-mails et les pages d'atterrissage, et suivre en temps réel les métriques.

    [Voir GoPhish](./gophish.md)

</div>

## Public cible

!!! info "À qui s'adresse cette section ?"
    - **Pentesters** intégrant un volet ingénierie sociale dans leurs audits
    - **Red Teamers** simulant des opérations adverses réalistes
    - **Responsables sécurité** pilotant des campagnes de sensibilisation
    - **RSSI** souhaitant démontrer le risque réel que représente le facteur humain

## Rôle dans l'écosystème offensif

L'ingénierie sociale est souvent la **phase de moindre résistance**. Un pare-feu correctement configuré n'offre aucune protection si un employé divulgue ses credentials à un attaquant qui se fait passer pour le support IT.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Ce module vous dote des outils fondamentaux pour cette catégorie d'attaque ou d'analyse. Gardez à l'esprit qu'un outil ne remplace pas la compréhension du concept : c'est votre capacité à interpréter les résultats qui fait de vous un véritable expert technique en cybersécurité.

!!! quote "L'humain, maillon fort ou faible ?"
    La technologie peut être patchée, mais l'humain doit être éduqué. Les outils de cette section ne servent pas qu'à pirater, ils servent à identifier où l'organisation doit investir dans sa culture de sécurité.

> Après avoir testé le facteur humain, documentez vos résultats dans le module **[Reporting](../reporting/index.md)**.