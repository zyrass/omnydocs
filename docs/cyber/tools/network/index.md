---
description: "Tests d'intrusion réseau et services : découverte d'hôtes, énumération de services, exploitation de protocoles Windows, attaques Active Directory et Man-in-the-Middle"
tags: ["PENTEST RÉSEAU", "ACTIVE DIRECTORY", "NMAP", "IMPACKET", "BLOODHOUND", "RESPONDER", "RED TEAM"]
---

# Cyber : Pentest Réseau & Services

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="1.0"
  data-time="8-10 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Système Nerveux du Bâtiment"
    Imaginez un immense bâtiment intelligent. Les tuyaux et les câbles qui passent dans les murs sont le **réseau**. Si vous contrôlez ces conduits, vous pouvez écouter ce qui se dit dans les pièces (Man-in-the-Middle), couper le courant (Déni de service) ou même vous faire passer pour le concierge pour ouvrir toutes les portes (Active Directory). Le **pentest réseau** consiste à explorer ces conduits cachés pour trouver les failles de communication entre les machines.

**Le pentest réseau et services** couvre l'évaluation de sécurité des infrastructures réseau, des services exposés et des environnements Active Directory. C'est l'une des phases les plus riches d'un test d'intrusion interne : une fois un premier accès réseau obtenu — physiquement, via VPN, ou depuis une machine compromise — l'auditeur cartographie les services accessibles, exploite les protocoles mal configurés et cherche des chemins d'escalade jusqu'aux actifs les plus critiques.

<br>

---

!!! info "Pourquoi cette section est essentielle ?"
    - **Découverte réseau** : cartographier les hôtes actifs, les services exposés et les versions vulnérables
    - **Énumération Active Directory** : lister les utilisateurs, groupes, GPO, ACL et relations de confiance
    - **Attaques sur les protocoles** : exploiter LLMNR/NBT-NS, SMB, Kerberos, LDAP et MSSQL
    - **Chemins d'escalade** : identifier les chemins de compromission vers Domain Admin via BloodHound
    - **Pivoting** : atteindre des segments réseau isolés depuis une machine compromise

## Les outils de cette section

<div class="grid cards" markdown>

-   **Nmap (NSE)**

    ---

    Scanner de ports et d'énumération de services — outil fondamental de toute phase de reconnaissance active. Les scripts NSE (Nmap Scripting Engine) étendent ses capacités : détection de vulnérabilités, énumération SMB/LDAP/DNS, brute-force de services, détection de configurations faibles.

    [Voir Nmap](./nmap.md)

-   **DNS Tools**

    ---

    Suite d'outils pour interroger les serveurs DNS et cartographier l'infrastructure réseau : `dig`, `dog`, `nslookup`, `host`. Utilisés en reconnaissance passive et active, y compris depuis une machine compromise pour cartographier les DNS internes.

    [Voir DNS Tools](./dns/index.md)

</div>

<div class="grid cards" markdown>

-   **ping**

    ---

    Test de connectivité ICMP. Utilisé pour vérifier l'accessibilité d'hôtes, mesurer la latence réseau et effectuer une découverte d'hôtes rapide sur un sous-réseau. Simple mais indispensable en phase de découverte initiale.

    [Voir ping](./ping.md)

-   **Scapy**

    ---

    Bibliothèque Python de manipulation de paquets réseau. Permet de forger, envoyer, capturer et analyser des paquets réseau arbitraires à tous les niveaux du modèle OSI. Utilisé pour les tests de protocoles, les attaques réseau sur mesure et le développement d'outils offensifs personnalisés.

    [Voir Scapy](./scapy.md)

</div>

<div class="grid cards" markdown>

-   **Impacket**

    ---

    Suite d'outils Python pour les protocoles réseau Windows (SMB, LDAP, Kerberos, MSSQL, WMI, DCE/RPC). Référence pour les attaques AD : Pass-the-Hash, Pass-the-Ticket, DCSync, secretsdump, Kerberoasting, AS-REP Roasting, relay attacks.

    [Voir Impacket](./impacket.md)

-   **CrackMapExec**

    ---

    Framework d'exploitation et d'énumération multi-protocoles (SMB, WinRM, LDAP, MSSQL, SSH). Permet de tester des credentials sur un parc de machines, d'exécuter des commandes à distance, d'énumérer les partages et les utilisateurs, et de chaîner des attaques AD en masse.

    [Voir CrackMapExec](./cme.md)

</div>

<div class="grid cards" markdown>

-   **Responder**

    ---

    Outil de poisoning LLMNR/NBT-NS/mDNS pour la capture de hashes NTLMv1/v2. Répond aux requêtes de résolution de noms sur le réseau local pour intercepter les authentifications et capturer des hashes crackables offline avec Hashcat ou relayables via NTLM relay attacks.

    [Voir Responder](./responder.md)

-   **BloodHound**

    ---

    Outil de cartographie et d'exploitation Active Directory. Collecte les données AD via SharpHound/BloodHound.py et les visualise sous forme de graphes orientés pour identifier les chemins d'escalade de privilèges vers Domain Admin, les ACL abusables et les délégations mal configurées.

    [Voir BloodHound](./bloodhound.md)

</div>

## Public cible

!!! info "À qui s'adresse cette section ?"
    - **Pentesters** réalisant des audits d'infrastructure interne
    - **Red Teamers** simulant des opérations adverses sur des environnements Active Directory
    - **Administrateurs système** souhaitant comprendre les vecteurs d'attaque pour renforcer leur configuration AD
    - **Équipes Blue Team** cherchant à améliorer la détection des attaques réseau et AD (Pass-the-Hash, DCSync, Kerberoasting)

## Rôle dans l'écosystème offensif

Le pentest réseau et services intervient après la reconnaissance (OSINT, DNS) et constitue le **pivot central d'un test d'intrusion interne**. La chaîne d'exploitation typique dans un environnement Windows d'entreprise suit ce chemin : découverte réseau via Nmap → capture de hashes NTLMv2 via Responder → cracking offline ou relay → accès SMB via CrackMapExec → énumération AD via Impacket → cartographie des chemins d'escalade via BloodHound → compromission du Domain Controller.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Ce module vous dote des outils fondamentaux pour cette catégorie d'attaque ou d'analyse. Gardez à l'esprit qu'un outil ne remplace pas la compréhension du concept : c'est votre capacité à interpréter les résultats qui fait de vous un véritable expert technique en cybersécurité.

!!! quote "Le cœur de l'infrastructure"
    La maîtrise du réseau et de l'Active Directory est ce qui différencie un audit de surface d'une véritable compromission de l'infrastructure cible. Chaque protocole mal configuré est une opportunité pour l'auditeur.

> Une fois l'infrastructure comprise, concentrez-vous sur les points d'entrée applicatifs avec le module **[Pentest Web & API](../web/index.md)**.