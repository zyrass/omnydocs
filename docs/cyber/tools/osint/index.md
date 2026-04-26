---
description: "Collecte d'informations publiques et reconnaissance passive : cartographie d'infrastructure, énumération de cibles, recherche de fuites de données"
tags: ["OSINT", "RECONNAISSANCE", "THEHARVESTER", "SHODAN", "AMASS", "MALTEGO", "RED TEAM"]
---

# Cyber : OSINT & Reconnaissance

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="1.0"
  data-time="7-9 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Détective et l'Empreinte Numérique"
    Imaginez un détective privé qui doit enquêter sur une cible sans jamais l'approcher. Il fouille les registres publics, analyse les réseaux sociaux, observe les allées et venues depuis le trottoir d'en face, et reconstitue la vie de sa cible pièce par pièce. L'**OSINT** est cette phase de filature numérique : on collecte tout ce qui est déjà public pour dessiner une carte précise de la cible avant même de lancer la moindre attaque.

**L'OSINT (Open Source Intelligence)** et la reconnaissance constituent la **première phase de tout test d'intrusion**. Avant toute interaction intrusive avec la cible, un attaquant — ou un pentester — collecte le maximum d'informations depuis des sources publiques : domaines et sous-domaines exposés, adresses e-mail, technologies utilisées, équipements accessibles sur Internet, fuites de credentials, organigrammes.

<br>

---

!!! info "Pourquoi cette section est essentielle ?"
    - **Cartographie de la surface d'attaque** : identifier tous les actifs exposés sans interagir avec eux
    - **Énumération des cibles humaines** : collecter e-mails, comptes LinkedIn, noms d'utilisateurs pour préparer le phishing ou le password spraying
    - **Découverte de sous-domaines** : trouver des environnements de staging, portails internes exposés, APIs non documentées
    - **Identification des technologies** : détecter les CMS, frameworks et versions pour cibler les CVE applicables
    - **Recherche de fuites** : vérifier si des credentials ou des données sensibles ont été exposés publiquement

## Les outils de cette section

<div class="grid cards" markdown>

-   **theHarvester**

    ---

    Outil de collecte OSINT multi-sources : e-mails, sous-domaines, noms d'hôtes, IPs et URLs associés à un domaine cible. Agrège des résultats depuis Google, Bing, LinkedIn, Hunter.io, Shodan et des dizaines d'autres sources en une seule commande.

    [Voir theHarvester](./theharvester.md)

-   **Maltego**

    ---

    Plateforme d'OSINT graphique (Paterva). Visualise les relations entre entités (domaines, IPs, personnes, organisations, e-mails) sous forme de graphes interactifs. Particulièrement puissant pour les investigations complexes et la cartographie de réseaux d'infrastructures.

    [Voir Maltego](./maltego.md)

</div>

<div class="grid cards" markdown>

-   **SpiderFoot**

    ---

    Plateforme d'automatisation OSINT interrogeant plus de 200 sources simultanément. Collecte et corrèle automatiquement les données sur une cible : domaines, IPs, e-mails, comptes sociaux, fuites de données, certificats TLS, dépôts de code publics.

    [Voir SpiderFoot](./spiderfoot.md)

-   **Amass**

    ---

    Outil OWASP de cartographie de la surface d'attaque externe. Spécialisé dans l'énumération exhaustive de sous-domaines via des techniques passives (DNS, certificats TLS, APIs) et actives (brute-force DNS). Standard de référence pour la découverte d'actifs exposés.

    [Voir Amass](./amass.md)

</div>

<div class="grid cards" markdown>

-   **Shodan / Censys**

    ---

    Moteurs de recherche pour les équipements connectés à Internet. Indexent les bannières de services, les certificats TLS et les réponses HTTP de l'ensemble des IPs publiques. Permettent de retrouver les équipements d'une organisation (routeurs, caméras, serveurs industriels, API exposées) sans aucun scan direct.

    [Voir Shodan & Censys](./shodan-censys.md)

</div>

## Public cible

!!! info "À qui s'adresse cette section ?"
    - **Pentesters** en phase de reconnaissance préalable au premier engagement
    - **Red Teamers** construisant leur profil de cible avant une opération
    - **Analystes threat intelligence** suivant des groupes d'attaquants ou des infrastructures malveillantes
    - **Responsables sécurité** souhaitant connaître leur empreinte numérique publique (Threat Exposure Management)

## Rôle dans l'écosystème offensif

L'OSINT et la reconnaissance constituent la **phase zéro** de toute opération offensive — la seule qui soit légalement réalisable sans autorisation préalable sur n'importe quelle cible. Les informations collectées alimentent directement toutes les phases suivantes : scan de vulnérabilités (sur les IPs identifiées), pentest web (sur les sous-domaines découverts), password attacks (avec les e-mails collectés) et social engineering (avec les noms et fonctions des employés).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Ce module vous dote des outils fondamentaux pour cette catégorie d'attaque ou d'analyse. Gardez à l'esprit qu'un outil ne remplace pas la compréhension du concept : c'est votre capacité à interpréter les résultats qui fait de vous un véritable expert technique en cybersécurité.

!!! quote "Savoir avant d'agir"
    Une reconnaissance OSINT exhaustive est le socle de toute opération Red Team réussie. Elle permet de minimiser le bruit lors des phases actives et d'identifier des vecteurs d'attaque souvent invisibles lors d'un scan classique.

> Une fois la surface d'attaque cartographiée, passez à l'identification active des failles avec le module **[Scan de Vulnérabilités](../scan/index.md)**.