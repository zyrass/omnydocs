---
description: "Observer, alerter et analyser : Logs centralisés, monitoring SNMP et métriques réseau."
tags: ["SUPERVISION", "OBSERVABILITE", "LOGS", "MONITORING", "INFRASTRUCTURE"]
---

# Supervision & Observabilité

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="Hub Supervision">
</div>

!!! quote "Piloter avec les yeux ouverts"
    _Si un pare-feu bloque une attaque, mais que personne ne regarde l'écran, le pare-feu a-t-il vraiment servi à quelque chose ? L'infrastructure (Réseaux, Serveurs, Stockage) génère des millions de messages par heure. La Supervision (ou l'Observabilité) est l'art de capter ce bruit de fond, de le trier, et de le transformer en un tableau de bord lisible ou en une alerte SMS à 3h du matin si la base de données s'effondre._

## Rendre l'infrastructure visible

Ce hub clôture l'apprentissage de l'Administration Système (Ops) et constitue la porte d'entrée parfaite vers la Cybersécurité défensive (Blue Team / SOC). Un analyste en sécurité passe en effet ses journées dans les outils présentés ici pour "chasser" les comportements anormaux.

<div class="grid cards" markdown>

-   :lucide-scroll-text:{ .lg .middle } **Gestion des Logs (Syslog & ELK)**

    ---
    Les journaux systèmes (Logs) sont la seule vérité absolue en informatique. Comment les lire, les centraliser pour éviter qu'un pirate ne les efface, et les rechercher.

    [:octicons-arrow-right-24: Exploiter les journaux](./logs.md)

-   :lucide-activity:{ .lg .middle } **Le Monitoring (Zabbix/Prometheus)**

    ---
    Savoir *avant* les utilisateurs que le serveur va tomber en panne. Surveillance du CPU, de la RAM, et création d'alertes automatisées.

    [:octicons-arrow-right-24: Surveiller la santé](./monitoring.md)

-   :lucide-radar:{ .lg .middle } **L'Observabilité Réseau (Ntop)**

    ---
    L'inspection visuelle du trafic réseau en temps réel. Qui consomme la bande passante ? Quel protocole est le plus utilisé ?

    [:octicons-arrow-right-24: Visualiser les flux](./ntop.md)

</div>

## La Frontière avec le SOC (Security Operations Center)

Les outils de supervision (Ops) et les outils du SOC (Cyber) sont extrêmement similaires, mais n'ont pas la même finalité.

- **L'ingénieur Ops** regarde Grafana et dit : "Le processeur est à 100%, le site web va crasher, il faut ajouter de la RAM."
- **L'analyste SOC** regarde le même écran Grafana et dit : "Le processeur est à 100% à 3h du matin alors qu'il n'y a aucun client sur le site. C'est le signe qu'un mineur de cryptomonnaie (Malware) vient d'infecter le serveur."

La supervision est le socle de l'investigation.
