---
description: "Les outils de diagnostic réseau : résolution DNS, écoute des ports, capture de trafic et forge de paquets."
tags: ["OUTILS", "RESEAU", "DIAGNOSTIC", "ANALYSE", "CLI"]
---

# Outils d'Analyse Réseau

<div
  class="omny-meta"
  data-level="🟢 Débutant à 🔴 Avancé"
  data-version="1.0"
  data-time="Sous-Hub Outils">
</div>


!!! quote "Analogie pédagogique"
    _Utiliser des outils d'analyse réseau (comme tcpdump ou scapy), c'est comme brancher un stéthoscope sur les artères d'une ville. Vous ne regardez plus simplement si les camions arrivent à destination, mais vous examinez le contenu de chaque paquet transporté pour détecter une anomalie ou une maladie (latence, perte, malware)._

!!! quote "Voir l'invisible"
    _Le réseau informatique est par nature invisible. Contrairement à un fichier que l'on peut ouvrir dans un éditeur de texte, un paquet réseau transite dans des câbles ou dans l'air à la vitesse de la lumière. Pour comprendre pourquoi une application "ne se connecte pas", ou pourquoi un flux est lent, l'ingénieur réseau a besoin d'outils d'investigation (des "sniffers" et des analyseurs) pour rendre ce flux visible, lisible et auditable._

## Les Couteaux Suisses de l'Ingénieur

Cette section couvre 4 outils fondamentaux, allant de la simple vérification locale à la manipulation avancée de paquets en Python.

<div class="grid cards" markdown>

-   :lucide-globe:{ .lg .middle } **NSLookup (DNS)**

    ---
    L'outil de base pour interroger les serveurs de noms (DNS). Idéal pour comprendre pourquoi un nom de domaine ne pointe pas vers la bonne adresse IP.

    [:octicons-arrow-right-24: Interroger le DNS](./nslookup.md)

-   :lucide-door-open:{ .lg .middle } **Netstat / SS (Ports)**

    ---
    L'outil indispensable pour lister tous les ports ouverts sur votre propre machine et voir quelles applications (Processus) écoutent le réseau.

    [:octicons-arrow-right-24: Analyser les connexions locales](./netstat.md)

-   :lucide-waves:{ .lg .middle } **Tcpdump (Capture)**

    ---
    Le sniffer par excellence en ligne de commande. Il permet d'intercepter, de filtrer et d'enregistrer l'intégralité du trafic réseau transitant par une carte réseau.

    [:octicons-arrow-right-24: Capturer le trafic en direct](./tcpdump.md)

-   :lucide-hammer:{ .lg .middle } **Scapy (Forge de paquets)**

    ---
    Un outil Python surpuissant (très utilisé en cybersécurité) permettant de créer des paquets réseau personnalisés, de les envoyer, et de manipuler presque tous les protocoles existants.

    [:octicons-arrow-right-24: Forger avec Scapy](./scapy.md)

</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La visibilité réseau est primordiale pour l'analyse d'incidents et le troubleshooting. Maîtriser tcpdump, netstat ou scapy permet de diagnostiquer la majorité des anomalies avant qu'elles ne s'aggravent.

> [Retourner à l'index Réseau →](../index.md)
