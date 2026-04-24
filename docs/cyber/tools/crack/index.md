---
description: "Techniques d'attaque contre les mécanismes d'authentification : cracking de hashes, bruteforce réseau, génération de wordlists"
tags: ["PASSWORD", "CRACKING", "BRUTEFORCE", "WORDLIST", "HASHCAT", "HYDRA", "RED TEAM"]
---

# Cyber : Password Attacks

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="1.0"
  data-time="6-8 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Trousseau de Clés Infini"
    Imaginez que vous deviez ouvrir une porte verrouillée, mais qu'au lieu d'un crochet, vous ayez un sac contenant des milliards de clés possibles. Le **cracking** consiste à tester ces clés une par une (force brute) ou à utiliser les clés les plus probables (dictionnaire) pour trouver celle qui correspond à la serrure électronique. C'est un jeu de patience et de puissance de calcul où la stratégie (choix des wordlists) est plus importante que la force brute pure.

**Les attaques sur les mots de passe** constituent l'une des phases les plus critiques d'un test d'intrusion. Elles visent à compromettre les mécanismes d'authentification — que ce soit par cracking de hashes capturés hors ligne, par bruteforce d'un service réseau, ou par génération de listes de mots adaptées à la cible.

> Dans la majorité des compromissions réelles, l'exploitation d'un mot de passe faible, réutilisé ou mal protégé constitue le vecteur initial ou le levier d'escalade de privilèges. La maîtrise des outils de cette section est indispensable pour tout auditeur offensif.

!!! info "Pourquoi cette section est essentielle ?"
    - **Cracking hors ligne** : récupérer des mots de passe depuis des hashes capturés (NTLM, bcrypt, SHA-256)
    - **Bruteforce réseau** : tester des authentifications SSH, FTP, HTTP, SMB, RDP en ligne
    - **Génération de wordlists** : construire des dictionnaires ciblés depuis la surface d'attaque
    - **Attaques par dictionnaire** : exploiter les mots de passe courants et les patterns d'entreprise
    - **Rainbow tables** : utiliser des tables précalculées pour les hashes non salés

## Les outils de cette section

<div class="grid cards" markdown>

-   **John the Ripper**

    ---

    Cracker de mots de passe CPU multi-format. Supporte des centaines de types de hashes (NTLM, bcrypt, SHA-*, ZIP, PDF) avec des modes d'attaque variés : wordlist, incrémental, règles.

    [Voir John the Ripper](./john.md)

-   **Hashcat**

    ---

    Cracker GPU ultra-rapide — référence de l'industrie pour le cracking hors ligne. Exploite la puissance des cartes graphiques pour des vitesses plusieurs ordres de grandeur supérieures au CPU.

    [Voir Hashcat](./hashcat.md)

</div>

<div class="grid cards" markdown>

-   **Hydra**

    ---

    Bruteforce d'authentifications réseau en ligne. Supporte SSH, FTP, HTTP/S, SMB, RDP, MySQL, SMTP et des dizaines d'autres protocoles avec parallélisation agressive.

    [Voir Hydra](./hydra.md)

-   **Medusa**

    ---

    Alternative à Hydra, orientée parallélisme massif. Conçu pour tester des listes d'hôtes et de credentials simultanément, adapté aux audits d'infrastructure à grande échelle.

    [Voir Medusa](./medusa.md)

</div>

<div class="grid cards" markdown>

-   **CeWL**

    ---

    Générateur de wordlists par spidering web. Analyse un site cible pour extraire le vocabulaire spécifique à l'organisation — noms de produits, termes métier, noms propres — et construire un dictionnaire adapté.

    [Voir CeWL](./cewl.md)

</div>

## Public cible

!!! info "À qui s'adresse cette section ?"
    - **Pentesters** en phase d'exploitation ou d'élévation de privilèges
    - **Red Teamers** simulant des attaques sur les identités
    - **Auditeurs** évaluant la robustesse des politiques de mots de passe
    - **Équipes défensives** souhaitant comprendre les vecteurs d'attaque pour mieux se protéger

## Rôle dans l'écosystème offensif

Les attaques sur les mots de passe interviennent à plusieurs phases d'un test d'intrusion : en **post-exploitation** (cracking des hashes NTLM récupérés sur un contrôleur de domaine), en **accès initial** (bruteforce d'un portail VPN ou d'un webmail exposé), ou en **mouvement latéral** (password spraying sur Active Directory).

> La génération de wordlists ciblées via CeWL et la connaissance des règles de transformation (mangling rules) dans Hashcat constituent souvent la différence entre un audit qui réussit à craquer les hashes et un audit qui s'arrête sur un résultat vide.

<br>

---

## Conclusion

!!! quote "Du hash au shell"
    Obtenir un mot de passe en clair est souvent la clé de voûte qui permet de transformer une simple présence réseau en une compromission totale du système cible.

> Une fois les accès obtenus, passez à la phase de consolidation avec le module **[Exploitation & Post-Exploit](../exploit/index.md)**.