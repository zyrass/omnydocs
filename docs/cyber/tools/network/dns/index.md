---
description: "Outils d'interrogation DNS pour la reconnaissance d'infrastructure : résolution de noms, transferts de zone, énumération de sous-domaines"
tags: ["DNS", "RECONNAISSANCE", "RÉSEAU", "OSINT", "DIG", "NSLOOKUP", "HOST"]
---

# Cyber : DNS — Outils d'interrogation

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="5-7 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le GPS de l'Infrastructure"
    Imaginez que vous cherchiez à cartographier une ville fortifiée sans pouvoir y entrer. Le **DNS** est le registre public qui indique quelle rue mène à quel bâtiment, où se trouve la mairie (serveur mail) et quels sont les accès de service. Interroger le DNS, c'est consulter le plan de la ville pour identifier les points d'entrée potentiels avant de s'en approcher.

**Le DNS (Domain Name System)** est l'annuaire d'Internet — et l'une des sources d'information les plus riches pour la reconnaissance d'infrastructure. Interroger correctement les serveurs DNS d'une organisation permet d'en cartographier les actifs exposés : sous-domaines, serveurs de messagerie, enregistrements SPF/DKIM/DMARC, serveurs d'authentification, et parfois des actifs internes exposés involontairement.

<br>

---

!!! info "Pourquoi cette section est essentielle ?"
    - **Cartographie d'infrastructure** : identifier les actifs exposés d'une organisation depuis l'extérieur
    - **Énumération de sous-domaines** : découvrir des services oubliés, des environnements de staging ou des portails d'administration
    - **Transfert de zone** : tenter d'obtenir l'intégralité des enregistrements DNS (AXFR) sur les serveurs mal configurés
    - **Analyse de la messagerie** : lire les enregistrements MX, SPF, DKIM, DMARC pour évaluer la posture anti-phishing
    - **Reconnaissance interne** : depuis une machine compromise, interroger les DNS internes pour cartographier le réseau

## Les outils de cette section

<div class="grid cards" markdown>

-   **dig**

    ---

    Outil DNS de référence, issu de BIND. Flexible, scriptable et disponible sur toutes les plateformes Unix. Permet d'interroger n'importe quel type d'enregistrement (A, AAAA, MX, TXT, NS, SOA, CNAME) sur n'importe quel serveur DNS, avec un contrôle fin des options de requête.

    [Voir dig](./dig.md)

-   **dog**

    ---

    Alternative moderne à dig, écrite en Rust. Sortie colorisée et lisible nativement, support du format JSON pour l'intégration dans des scripts, syntaxe simplifiée. Idéal pour un usage interactif au terminal.

    [Voir dog](./dog.md)

</div>

<div class="grid cards" markdown>

-   **nslookup**

    ---

    Outil DNS historique, multiplateforme (Windows et Linux). Moins flexible que dig mais disponible nativement sur Windows sans installation — ce qui en fait un outil de reconnaissance utile depuis une machine Windows compromise en post-exploitation.

    [Voir nslookup](./nslookup.md)

-   **host**

    ---

    Outil DNS minimaliste pour les résolutions rapides. Syntaxe épurée, idéal pour les scripts shell et les one-liners de reconnaissance. Particulièrement adapté aux lookups A/AAAA/MX/TXT sans surcharge syntaxique.

    [Voir host](./host.md)

</div>

## Public cible

!!! info "À qui s'adresse cette section ?"
    - **Pentesters** en phase de reconnaissance active ou passive
    - **Red Teamers** cartographiant l'infrastructure d'une cible
    - **Administrateurs réseau** diagnostiquant des problèmes de résolution
    - **Analystes OSINT** reconstituant la surface d'attaque externe d'une organisation

## Rôle dans l'écosystème offensif

Les outils DNS s'insèrent dans la **phase de reconnaissance** — la première phase de tout test d'intrusion. Ils sont non intrusifs, légaux à utiliser contre n'importe quel domaine, et fournissent des informations de haute valeur avant tout engagement actif avec la cible. Les données DNS alimentent les phases suivantes : l'énumération OSINT (theHarvester, Amass), le scan de ports (Nmap sur les IPs identifiées) et la cartographie de la surface d'attaque.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Ce module vous dote des outils fondamentaux pour cette catégorie d'attaque ou d'analyse. Gardez à l'esprit qu'un outil ne remplace pas la compréhension du concept : c'est votre capacité à interpréter les résultats qui fait de vous un véritable expert technique en cybersécurité.

!!! quote "La visibilité par le nom"
    Le DNS est souvent le premier domino qui tombe lors d'une reconnaissance. Un enregistrement oublié ou un serveur mal configuré peut révéler des pans entiers de l'infrastructure que l'organisation pensait cachés.

> La reconnaissance DNS terminée, poursuivez la cartographie réseau avec le module **[Pentest Réseau](../index.md)**.