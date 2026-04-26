---
description: "Tests d'intrusion sur les réseaux sans fil : capture de handshakes, cracking WPA/WPA2, attaques PMKID, Evil Twin, WPS et audit des protocoles d'entreprise 802.1X"
tags: ["WIFI", "SANS FIL", "AIRCRACK", "WPA2", "PMKID", "EVIL TWIN", "WPS", "RED TEAM"]
---

# Cyber : WiFi & Réseaux Sans Fil

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="1.0"
  data-time="7-9 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Les Ondes Invisibles"
    Imaginez un bâtiment sécurisé avec des portes blindées et des badges. Mais imaginez aussi que les conversations et les données qui circulent à l'intérieur s'échappent par les fenêtres sous forme de fumée invisible que l'on peut capturer depuis le trottoir d'en face. Le **pentest WiFi** consiste à attraper cette "fumée numérique" (les ondes) pour en extraire les secrets de connexion et entrer dans le bâtiment sans jamais toucher à une seule porte physique.

**Le pentest WiFi** évalue la sécurité des réseaux sans fil d'une organisation. C'est un vecteur d'accès initial physiquement accessible depuis le parking ou la rue.

<br>

---

!!! info "Pourquoi cette section est essentielle ?"
    - **Accès initial physique** : compromettre un réseau WiFi place l'attaquant sur le LAN interne
    - **Vecteur sous-estimé** : les réseaux WiFi sont souvent moins surveillés que le périmètre filaire
    - **Attaques PMKID** : capturer des hashes WPA2 sans attendre qu'un client se connecte
    - **Evil Twin** : intercepter les authentifications 802.1X et capturer des credentials de domaine
    - **WPS** : exploiter les équipements vulnérables au bruteforce PIN (Pixie Dust)

## Les outils de cette section

<div class="grid cards" markdown>

-   **Aircrack-ng**

    ---

    Suite de référence pour l'audit des réseaux WiFi. Regroupe `airmon-ng`, `airodump-ng`, `aireplay-ng` et `aircrack-ng`. Standard de l'industrie pour la capture et le cracking.

    [Voir Aircrack-ng](./aircrack-ng.md)

-   **Kismet**

    ---

    Détecteur de réseaux sans fil et sniffer passif. Capture le trafic sans émettre, idéal pour la phase de reconnaissance WiFi discrète.

    [Voir Kismet](./kismet.md)

</div>

<div class="grid cards" markdown>

-   **Wifite**

    ---

    Outil d'audit WiFi automatisé. Orchestre l'ensemble des attaques courantes (handshake, PMKID, WPS) en une seule commande.

    [Voir Wifite](./wifite.md)

-   **hcxtools / hcxdumptool**

    ---

    Suite d'outils pour les attaques PMKID. Permet de capturer des hashes WPA2/WPA3 sans attendre qu'un client se connecte.

    [Voir hcxtools](./hcxtools.md)

</div>

<div class="grid cards" markdown>

-   **Reaver / Bully**

    ---

    Outils d'attaque WPS. Exploitent la vulnérabilité du protocole WPS permettant de récupérer la clé via bruteforce du PIN ou attaque Pixie Dust.

    [Voir Reaver / Bully](./reaver-bully.md)

-   **hostapd-wpe**

    ---

    Framework d'attaque Evil Twin ciblant les authentifications 802.1X d'entreprise (EAP-PEAP). Capture les credentials de domaine.

    [Voir hostapd-wpe](./hostapd-wpe.md)

</div>

## Public cible

!!! info "À qui s'adresse cette section ?"
    - **Pentesters** incluant un volet WiFi dans leurs audits physiques
    - **Red Teamers** exploitant les vecteurs d'accès initiaux physiques
    - **Administrateurs réseau** souhaitant renforcer leur configuration WiFi
    - **Auditeurs** évaluant la conformité (WPA3, 802.1X, isolation VLAN)

## Rôle dans l'écosystème offensif

Le pentest WiFi intervient **après la reconnaissance OSINT** et **avant le pentest réseau interne**. Un réseau WiFi compromis est un point d'entrée direct sur le LAN.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Ce module vous dote des outils fondamentaux pour cette catégorie d'attaque ou d'analyse. Gardez à l'esprit qu'un outil ne remplace pas la compréhension du concept : c'est votre capacité à interpréter les résultats qui fait de vous un véritable expert technique en cybersécurité.

!!! quote "La sécurité par-delà les murs"
    Le périmètre de sécurité d'une entreprise s'arrête là où s'arrêtent ses ondes. Maîtriser le pentest sans fil, c'est savoir transformer une vulnérabilité invisible en un accès total à l'infrastructure.

> Une fois l'accès réseau obtenu via le WiFi, poursuivez l'exploration interne avec le module **[Pentest Réseau](../network/index.md)**.