---
description: "Cadres méthodologiques des opérations offensives : phases de pentest, MITRE ATT&CK, OpSec, C2 et techniques d'évasion"
tags: ["RED TEAM", "MÉTHODOLOGIE", "MITRE ATTACK", "PENTEST", "C2", "OPSEC", "KILL CHAIN"]
---

# Cyber : Méthodologies Red Team

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="7-9 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Partition du Chef d'Orchestre"
    Imaginez un orchestre où chaque musicien jouerait ce qu'il veut sans suivre de partition. Le résultat serait un chaos inaudible. En Red Team, la **méthodologie** est la partition : elle définit qui fait quoi, à quel moment, et comment chaque instrument (outil) doit s'accorder avec les autres pour produire une symphonie (opération) cohérente, furtive et efficace. C'est ce qui transforme une attaque désordonnée en une opération militaire de haute précision.

**Les méthodologies Red Team** constituent le cadre intellectuel et opérationnel qui structure les opérations offensives. Un Red Teamer ne se contente pas d'enchaîner des outils — il suit un plan d'opération cohérent, maintient une discipline OpSec rigoureuse, documente ses actions en les alignant sur les cadres de référence reconnus, et produit un rapport exploitable par la défense.

<br>

---

!!! info "Pourquoi cette section est essentielle ?"
    - **Structurer les phases** : découper une opération offensive en étapes claires et reproductibles
    - **Aligner sur MITRE ATT&CK** : documenter les techniques utilisées avec un langage universel
    - **Maintenir l'OpSec** : opérer sans se faire détecter par les équipes défensives
    - **Piloter les C2** : gérer les agents déployés depuis une infrastructure de commande maîtrisée
    - **Démontrer l'impact** : prouver qu'un adversaire réel aurait pu atteindre ses objectifs

## Les sujets de cette section

<div class="grid cards" markdown>

-   **Phases d'un Pentest**

    ---

    Méthodologie complète d'un test d'intrusion : Reconnaissance, Scanning, Exploitation, Post-Exploitation, Reporting. Chaque phase, ses objectifs, ses livrables et sa place dans le cycle d'audit.

    [Voir les phases d'un pentest](./pentest-phases.md)

-   **EBIOS RM — Vue Red Team**

    ---

    Utilisation d'EBIOS Risk Manager comme cadre de planification d'une opération Red Team. Identification des sources de risque, construction des scénarios d'attaque et mapping aux événements redoutés de l'organisation cible.

    [Voir EBIOS RM vue Red Team](./ebios-redteam.md)

</div>

<div class="grid cards" markdown>

-   **MITRE ATT&CK**

    ---

    Base de connaissances des tactiques, techniques et procédures (TTP) des adversaires réels. Framework de référence pour documenter les opérations offensives, mesurer la couverture défensive et construire des scénarios d'attaque réalistes.

    [Voir MITRE ATT&CK](./mitre-attack.md)

-   **OpSec & Anonymisation**

    ---

    Operational Security : techniques pour opérer sans laisser de traces identifiables. Chaînes de proxies, Tor, VPN enchaînés, effacement de logs, infrastructure éphémère, timestomping. L'OpSec distingue un Red Teamer d'un script kiddie.

    [Voir OpSec & Anonymisation](./opsec.md)

</div>

<div class="grid cards" markdown>

-   **Stéganographie**

    ---

    Dissimulation de données dans des fichiers apparemment anodins (images, audio, vidéo, documents). Technique utilisée pour l'exfiltration furtive de données et le stockage de payloads dans des canaux non surveillés.

    [Voir Stéganographie](./steganographie.md)

-   **C2 — Command & Control**

    ---

    Frameworks de commande et contrôle : Cobalt Strike, Sliver, Havoc, Mythic. Architecture d'une infrastructure C2, gestion des agents (beacons), techniques d'évasion des EDR, canaux de communication alternatifs.

    [Voir C2 Frameworks](./c2-frameworks.md)

</div>

## Public cible

!!! info "À qui s'adresse cette section ?"
    - **Red Teamers** planifiant et exécutant des opérations adverses simulées
    - **Pentesters** souhaitant structurer leurs audits avec des méthodologies reconnues
    - **Responsables sécurité** commanditant des exercices Red Team et souhaitant en comprendre le déroulement
    - **Blue Teamers** souhaitant comprendre les méthodes adverses pour améliorer leur détection et leur réponse

## Rôle dans l'écosystème offensif

Les méthodologies Red Team constituent la **colonne vertébrale de toute opération offensive sérieuse**. Sans cadre méthodologique, un test d'intrusion risque d'être chaotique, non reproductible et difficilement interprétable par le client. MITRE ATT&CK fournit le vocabulaire commun entre les équipes offensives et défensives. L'OpSec garantit que l'exercice teste réellement les capacités de détection de l'organisation.

<br>

---

## Conclusion

!!! quote "L'excellence opérationnelle par la rigueur"
    La méthodologie est ce qui sépare le hacker amateur du professionnel de la sécurité. C'est elle qui garantit que l'audit apporte une valeur ajoutée réelle au client en identifiant non seulement les failles, mais aussi les lacunes organisationnelles et de détection.

> Maintenant que vous avez le cadre, passez à la pratique avec les outils de **[Reconnaissance & OSINT](../osint/index.md)**.