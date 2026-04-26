---
description: "Tests d'intrusion applicatifs Web et API : injection SQL, XSS, CSRF, SSRF, OWASP Top 10, fuzzing de paramètres et énumération de contenus"
tags: ["PENTEST WEB", "API", "OWASP", "BURP SUITE", "FUZZING", "XSS", "INJECTION", "RED TEAM"]
---

# Cyber : Pentest Web & API

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="1.0"
  data-time="7-9 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Inspection de la Façade"
    Imaginez un bâtiment avec de nombreuses fenêtres et portes vitrées (Interfaces Web). Certaines sont blindées, d'autres sont mal fermées, et certaines ne sont que du carton peint en trompe-l'œil. Le **pentest web** consiste à tester chaque vitre pour voir si elle casse, à essayer chaque poignée de porte, et à regarder à travers les fissures pour voir ce qui se passe à l'intérieur. C'est l'art de trouver le défaut dans la vitrine de l'entreprise.

**Le pentest web et API** couvre l'évaluation de sécurité des applications exposées sur Internet ou en réseau interne. Les applications web constituent la surface d'attaque la plus large dans la majorité des organisations.

<br>

---

!!! info "Pourquoi cette section est essentielle ?"
    - **Surface d'attaque dominante** : les applications web sont le vecteur d'accès initial le plus fréquent
    - **Diversité des vulnérabilités** : injection SQL, XSS, CSRF, SSRF, IDOR, XXE, BOLA (APIs)
    - **Fuzzing de paramètres** : découvrir des endpoints cachés et des paramètres non documentés
    - **Analyse de logique métier** : identifier les failles que les scanners automatiques ne détectent pas
    - **APIs REST/GraphQL** : tester les authentifications JWT et les autorisations spécifiques

## Les outils de cette section

<div class="grid cards" markdown>

-   **Burp Suite**

    ---

    Proxy d'interception et plateforme de pentest applicatif (PortSwigger). Standard de l'industrie pour l'audit de sécurité web. Intercepte, modifie et rejoue les requêtes HTTP/S.

    [Voir Burp Suite](./burp.md)

-   **OWASP ZAP**

    ---

    Proxy d'interception et scanner web open source (OWASP). Alternative libre à Burp Suite, orientée automatisation et intégration CI/CD.

    [Voir OWASP ZAP](./zap.md)

</div>

<div class="grid cards" markdown>

-   **Nikto**

    ---

    Scanner de vulnérabilités web orienté configurations et fichiers sensibles. Détecte les en-têtes de sécurité manquants et les fichiers exposés (.git, .env).

    [Voir Nikto](./nikto.md)

-   **ffuf**

    ---

    Fuzzer HTTP rapide et flexible. Découverte de répertoires, de fichiers, de vhosts et de paramètres par substitution de mots depuis une wordlist.

    [Voir ffuf](./ffuf.md)

</div>

<div class="grid cards" markdown>

-   **Gobuster**

    ---

    Outil de brute-force de répertoires, fichiers, DNS et vhosts (Go). Performant et parallélisé, idéal pour l'énumération de contenus.

    [Voir Gobuster](./gobuster.md)

-   **Fuzzing applicatif**

    ---

    Méthodologies et techniques de fuzzing applicatif : mutation de requêtes API et génération de payloads basée sur des grammaires.

    [Voir Fuzzing applicatif](./fuzzing.md)

</div>

## Public cible

!!! info "À qui s'adresse cette section ?"
    - **Pentesters** spécialisés en sécurité applicative web
    - **Développeurs** souhaitant sécuriser leur code (SecDevOps)
    - **Auditeurs** réalisant des revues de sécurité applicative
    - **Bug Bounty Hunters** cherchant des vulnérabilités sur des programmes publics

## Rôle dans l'écosystème offensif

Le pentest web et API s'inscrit dans la phase d'**accès initial**. Une vulnérabilité applicative exploitée peut ouvrir l'accès à l'infrastructure backend, aux bases de données et aux secrets d'infrastructure.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Ce module vous dote des outils fondamentaux pour cette catégorie d'attaque ou d'analyse. Gardez à l'esprit qu'un outil ne remplace pas la compréhension du concept : c'est votre capacité à interpréter les résultats qui fait de vous un véritable expert technique en cybersécurité.

!!! quote "La porte d'entrée numérique"
    Dans un monde où tout est exposé via HTTP, maîtriser le pentest web n'est plus une option, c'est une nécessité. C'est souvent là que se joue le destin de la sécurité d'une entreprise.

> Une fois l'accès web obtenu, pivotez vers l'infrastructure interne avec le module **[Pentest Réseau](../network/index.md)**.