---
description: "Le troisième pilier de l'exploitation : interconnecter, analyser et protéger les flux de données entre les serveurs."
tags: ["RESEAU", "NETWORK", "INFRASTRUCTURE", "SERVICES", "SECURITE"]
---

# Réseaux & Protocoles (Ops)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="Hub Réseau">
</div>

!!! quote "Les fondations du système nerveux"
    _Comme pour l'administration système, **il est inutile de s'attaquer à la cybersécurité (hacking, pentest) si vous ne maîtrisez pas le réseau**. Avant d'intercepter un paquet réseau pour en extraire un mot de passe (Sniffing), vous devez comprendre ce qu'est le protocole ARP, comment fonctionne le modèle TCP/IP, et comment un administrateur configure un pare-feu périmétrique. C'est l'objectif de ce hub._

## L'approche Opérationnelle (Ops)

Contrairement à la section des fondamentaux théoriques (Modèle OSI, familles de protocoles), ce hub est **100% pratique et opérationnel**. Vous y apprendrez à utiliser les outils quotidiens de l'ingénieur réseau, à déployer les services de base, et à ériger les premières barrières de défense.

<div class="grid cards" markdown>

-   :lucide-search-code:{ .lg .middle } **Outils d'Analyse Réseau**

    ---
    Un ingénieur réseau n'avance pas à l'aveugle. Apprenez à écouter le trafic, résoudre des noms de domaine, lister les ports ouverts et forger des paquets réseau sur mesure.

    [:octicons-arrow-right-24: Maîtriser le diagnostic](./outils/index.md)

-   :lucide-server-cog:{ .lg .middle } **Services Réseau Fondateurs**

    ---
    Déployer et maintenir les services d'infrastructure qui rendent un réseau utilisable : serveurs DNS locaux, transferts de fichiers (FTP/Samba), annuaires (LDAP) et tunnels sécurisés (SSH).

    [:octicons-arrow-right-24: Déployer les services](./services/index.md)

-   :lucide-shield-alert:{ .lg .middle } **Sécurité Périmétrique**

    ---
    Protéger l'infrastructure depuis l'extérieur. Configuration de pare-feux professionnels (pfSense), de proxys inversés de haute disponibilité (HAProxy), et création de tunnels chiffrés (OpenVPN).

    [:octicons-arrow-right-24: Protéger le périmètre](./security/index.md)

</div>

## Le lien avec la Cybersécurité (Rappel)

**La Blue Team (Défense)** passe 80% de son temps à utiliser les outils présentés dans la section *Sécurité Périmétrique* (pfSense, WAF). Pour bloquer une attaque, il faut configurer correctement son pare-feu et son reverse proxy.

**La Red Team (Attaque)** passe 80% de son temps à utiliser (ou détourner) les outils de la section *Outils d'Analyse* (tcpdump, scapy, nmap). Pour attaquer, il faut comprendre l'état des ports et savoir injecter des paquets illégitimes dans le réseau.

Dans tous les cas, **la maîtrise de l'administration réseau est le prérequis**.