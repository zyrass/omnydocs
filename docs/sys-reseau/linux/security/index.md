---
description: "Les outils et pratiques essentiels pour le durcissement (Hardening) de l'hôte Linux."
tags: ["SECURITE", "LINUX", "HARDENING", "DURCISSEMENT", "FIREWALL"]
---

# Sécurité & Durcissement (Host)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="Sous-Hub Sécurité">
</div>


!!! quote "Analogie pédagogique"
    _Le durcissement d'un système Linux est comme la construction des fortifications d'un château. Le pare-feu (UFW) correspond aux douves extérieures, les permissions POSIX (chmod/chown) sont les clés des différentes pièces, et la supervision (Fail2Ban/Lynis) agit comme les gardes effectuant des rondes régulières._

!!! quote "Réduire la surface d'attaque"
    _Un serveur fraîchement installé est comme une maison dont toutes les portes et fenêtres seraient grandes ouvertes. Le "Durcissement" (Hardening) consiste à configurer le système d'exploitation de manière à réduire au maximum les possibilités d'intrusion, avant même de s'occuper de la sécurité des applications web qui y seront hébergées._

## Les Outils de Défense de l'Hôte

Dans ce sous-hub, nous allons détailler les outils et logiciels spécifiques qui permettent de verrouiller et d'auditer un serveur GNU/Linux de manière autonome.

<div class="grid cards" markdown>

-   :lucide-file-search:{ .lg .middle } **Lynis**

    ---
    L'outil d'audit de sécurité et de conformité le plus célèbre pour Linux. Il scanne le système et donne un score de durcissement.

    [:octicons-arrow-right-24: Auditer avec Lynis](./lynis.md)

-   :lucide-brick-wall:{ .lg .middle } **UFW (Uncomplicated Firewall)**

    ---
    L'interface simplifiée pour configurer le pare-feu du noyau Linux (iptables / nftables). Ne laisser ouvert que l'essentiel.

    [:octicons-arrow-right-24: Configurer UFW](./ufw.md)

-   :lucide-shield-ban:{ .lg .middle } **Fail2Ban**

    ---
    Le gardien de vos logs. Il analyse les journaux en temps réel et bannit automatiquement les adresses IP qui tentent des attaques par force brute (ex: sur SSH).

    [:octicons-arrow-right-24: Bloquer les attaques avec Fail2Ban](./fail2ban.md)

-   :lucide-scan-line:{ .lg .middle } **Vuls**

    ---
    Scanner de vulnérabilités open-source sans agent. Il détecte si vos logiciels installés possèdent des failles connues (CVE).

    [:octicons-arrow-right-24: Détecter les CVE avec Vuls](./vuls.md)

-   :lucide-bug-off:{ .lg .middle } **ClamAV**

    ---
    Le moteur antivirus open-source de référence sous Linux, souvent utilisé sur les serveurs de messagerie ou les passerelles web.

    [:octicons-arrow-right-24: Scanner les virus avec ClamAV](./clamav.md)

-   :lucide-virus:{ .lg .middle } **Linux Malware Detect (LMD)**

    ---
    Outil spécialisé dans la détection de malwares (backdoors, webshells) ciblant spécifiquement les environnements d'hébergement web (LAMP).

    [:octicons-arrow-right-24: Traquer les WebShells avec LMD](./linux_malware_detect.md)

-   :lucide-skull:{ .lg .middle } **Chkrootkit**

    ---
    Outil de sécurité qui recherche localement les signes de présence d'un "Rootkit" (un programme malveillant conçu pour cacher son existence et maintenir un accès administrateur).

    [:octicons-arrow-right-24: Débusquer les Rootkits](./chkrootkit.md)

</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Sécuriser un système Linux exige une approche en couches : du pare-feu avec UFW à la détection d'intrusions avec Fail2Ban, en passant par un durcissement régulier. Aucun outil de sécurité ne remplace une bonne configuration de base.

> [Retourner à l'index Linux →](../index.md)
