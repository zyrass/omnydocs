---
description: "Anticiper les pannes et surveiller l'état de santé du matériel et des services (Zabbix, Prometheus, Grafana)."
icon: lucide/book-open-check
tags: ["MONITORING", "ZABBIX", "PROMETHEUS", "GRAFANA", "SUPERVISION"]
---

# Le Monitoring Matériel et Applicatif

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>


!!! quote "Analogie pédagogique"
    _La supervision (monitoring, logs) est l'équivalent du tableau de bord d'un avion de ligne. Sans ces cadrans et ces alertes, le pilote (l'administrateur) navigue à l'aveugle et ne s'apercevra d'une baisse de pression moteur que lorsque l'avion commencera à perdre de l'altitude._

!!! quote "Réagir avant les utilisateurs"
    _La pire situation pour un administrateur système, c'est de recevoir un appel téléphonique du Directeur lui disant "Le site web de l'entreprise est tombé !". Un bon administrateur ne doit jamais l'apprendre par ses utilisateurs. Il doit l'apprendre par son propre téléphone, qui lui envoie un SMS automatique ("Alerte : Le disque dur est plein à 98%") 10 minutes **avant** que le serveur ne crashe, lui laissant le temps d'intervenir._

## 1. La différence fondamentale (Push vs Pull)

Contrairement aux *Logs* (qui sont des phrases textuelles : "Jean s'est connecté"), le Monitoring récolte des **Métriques** (des chiffres : Le CPU est à 45%, la RAM à 80%, le disque a 10 Go libres).

Pour récolter ces chiffres sur 500 serveurs, l'industrie s'affronte sur deux philosophies :

### Modèle Push (Historique / SNMP)
Le Serveur Central reste passif. Chaque serveur de l'entreprise (Les Agents) est programmé pour envoyer lui-même ses chiffres (Push) au serveur central toutes les 5 minutes.
- **Protocole historique** : SNMP (Simple Network Management Protocol).
- **Avantage** : Facile à configurer pour le pare-feu du serveur central (il ne fait qu'écouter).

### Modèle Pull (Moderne / Prometheus)
Le Serveur Central est actif. Il possède la liste des 500 serveurs de l'entreprise. C'est lui qui contacte chaque serveur toutes les 5 secondes et "tire" (Pull) les données en interrogeant une page web invisible.
- **L'outil star** : **Prometheus** (Inventé par SoundCloud, adopté par la Cloud Native Computing Foundation).
- **Avantage** : Si le serveur 42 ne répond pas, le Serveur Central le sait *immédiatement* (puisqu'il vient d'essayer de le contacter et a échoué). Dans le modèle Push, il aurait fallu attendre de s'apercevoir que le serveur 42 "n'envoie plus rien".

```mermaid
graph TD
    subgraph Philosophie PUSH
        Agent1[Serveur A] -->|Envoie métrique (Push)| Centre1[Serveur de Monitoring]
        Agent2[Serveur B] -->|Envoie métrique (Push)| Centre1
    end
    
    subgraph Philosophie PULL (Prometheus)
        Centre2[Serveur de Monitoring] -->|Interroge (Scrape)| Agent3[Serveur C]
        Centre2 -->|Interroge (Scrape)| Agent4[Serveur D]
    end
    
    style Centre1 fill:#e67e22,stroke:#fff,stroke-width:2px,color:#fff
    style Centre2 fill:#27ae60,stroke:#fff,stroke-width:2px,color:#fff
```

---

## 2. Le couteau suisse de l'entreprise : Zabbix

Si Prometheus est roi dans les environnements "Cloud" (Kubernetes), les entreprises plus traditionnelles "On-Premise" utilisent massivement des logiciels monolithiques comme **Zabbix** ou **Centreon** (qui a historiquement remplacé Nagios).

Zabbix est surpuissant car il "sait tout faire" dans une seule interface Web :
1. **Auto-Découverte** : Il scanne le réseau et ajoute automatiquement le nouveau routeur fraîchement branché.
2. **Templates** : Si vous lui ajoutez un serveur "Linux Debian", il sait automatiquement qu'il doit surveiller la RAM, le SWAP, le CPU et la partition `/var`.
3. **Triggers (Déclencheurs)** : La logique d'alerte. *"SI (CPU > 90% PENDANT 5 minutes) ALORS -> Déclencher l'état d'Alerte"*.
4. **Actions** : *"SI (État d'Alerte est VRAI) ALORS -> Envoyer un email à l'équipe d'astreinte ET Lancer un script de redémarrage du service."*

---

## 3. L'art visuel : Grafana

Personne n'aime regarder des tableaux de chiffres bruts dans Prometheus.
Aujourd'hui, l'architecture classique est le découplage : 
- **Prometheus** fait le travail sale (la récolte et le stockage temporel des chiffres).
- **Grafana** fait le travail visuel. 

Grafana est une application web qui se connecte à Prometheus (ou Zabbix, ou Elasticsearch) et qui "dessine" les tableaux de bord (Dashboards) magnifiques, dynamiques, en mode sombre, que l'on voit souvent sur les grands écrans de télévision accrochés au mur dans les départements IT (Les NOC - Network Operations Centers).

## Conclusion (Surcharge Cognitive)

L'erreur la plus fréquente en supervision est le **Sur-Monitoring** (ou "Alerte Fatigue").
Si un administrateur configure son Zabbix pour recevoir un email à chaque fois qu'un disque dépasse 70% de remplissage, il va recevoir 50 emails par jour. Au bout d'une semaine, son cerveau ignorera totalement les emails de supervision (en créant une règle Outlook qui les met à la corbeille). Le jour où un vrai crash interviendra, l'alerte sera perdue dans la masse.

La supervision doit être silencieuse 99% du temps, et ne crier que pour les événements véritablement critiques.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Une supervision efficace transforme le bruit en alertes exploitables. La centralisation des logs et la création de dashboards pertinents réduisent drastiquement le MTTR (Mean Time To Respond) lors d'un incident.

> [Retourner à l'index →](../index.md)
