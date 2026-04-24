---
description: "Centralisation et analyse des journaux systèmes avec rsyslog et les stacks Elastic/Splunk."
icon: lucide/book-open-check
tags: ["LOGS", "SYSLOG", "ELK", "SIEM", "SUPERVISION"]
---

# Les Logs et leur Centralisation

<div
  class="omny-meta"
  data-level="🟢 Débutant à 🔴 Avancé"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>

!!! quote "Les boîtes noires du serveur"
    _Un "Log" (Journal système) est un simple fichier texte dans lequel un logiciel enregistre tout ce qu'il fait. L'application Web note l'IP de tous ses visiteurs, le pare-feu note toutes les IPs qu'il a bloquées, et le système Linux note toutes les connexions SSH réussies ou échouées. Sans logs, le diagnostic d'une panne ou l'enquête suite à un piratage est mathématiquement impossible._

## 1. Comprendre Syslog (Local)

Historiquement sous Unix/Linux, les logs sont générés par un service de base appelé **Syslog** (ou aujourd'hui `rsyslog` / `journald`).
Ces fichiers se trouvent dans le répertoire sacré : `/var/log`.

- `/var/log/syslog` ou `/var/log/messages` : Les événements globaux du système.
- `/var/log/auth.log` : Toutes les tentatives de connexion (Mots de passe corrects, erreurs, utilisations de `sudo`). *C'est le fichier préféré des auditeurs.*
- `/var/log/nginx/access.log` : Chaque page web visitée par chaque internaute.

### La lecture continue
La commande d'administration la plus tapée au monde pour lire un log en direct (dès qu'une nouvelle ligne est écrite) est :
```bash
# Lire les 10 dernières lignes du fichier d'authentification et suivre les mises à jour en direct
sudo tail -f /var/log/auth.log
```

---

## 2. Le problème de sécurité (Effacement des traces)

Garder les logs en local sur le serveur présente deux défauts majeurs :
1. **La perte mécanique** : Si le serveur web prend feu, le disque dur brûle. Les logs (qui expliqueraient peut-être l'origine de la surcharge ayant causé le feu) brûlent avec.
2. **Le piratage** : Si un pirate s'infiltre sur votre serveur et obtient les droits d'administrateur (Root), **sa toute première action sera de taper `rm -rf /var/log/*`**. Il vient d'effacer ses propres traces. L'enquête est morte.

### La Centralisation (Rsyslog réseau)
La solution est le serveur de centralisation de logs. Dès qu'une connexion ssh échoue sur le Serveur Web (Client), la ligne de log n'est pas seulement écrite localement, elle est immédiatement envoyée par le réseau à un énorme Serveur Central ultra-sécurisé (le "Log Server").
Si le pirate supprime les fichiers locaux du Serveur Web 2 minutes plus tard, il est trop tard : la trace de son IP a déjà été copiée sur le Serveur Central qu'il ne contrôle pas.

```mermaid
graph LR
    subgraph DMZ (Exposé Internet)
        ServeurWeb[Serveur Web]
        ServeurMail[Serveur Mail]
    end
    
    subgraph Réseau Ultra-Sécurisé
        LogServer[(Serveur Central de Logs\nLecture Seule)]
    end
    
    ServeurWeb -->|Envoi UDP/TCP temps réel| LogServer
    ServeurMail -->|Envoi UDP/TCP temps réel| LogServer
    
    style LogServer fill:#27ae60,stroke:#fff,stroke-width:2px,color:#fff
```

---

## 3. L'évolution : ELK et le SIEM

Avoir 500 millions de lignes de texte brut dans un serveur central, c'est bien pour la sécurité, mais inexploitable pour un humain (Faire un `grep` sur 4 Terabytes de texte prend des heures).

L'industrie est donc passée à l'étape supérieure : **L'Indexation et la Visualisation**.
La solution Open Source leader est la stack **ELK (Elasticsearch, Logstash, Kibana)**.

1. **Logstash** (Le trieur) : Reçoit la ligne de texte "User root failed password from 192.168.1.10", la découpe et la catégorise : `User=root`, `Action=fail`, `IP=192.168.1.10`.
2. **Elasticsearch** (La base de données) : Stocke ces variables sous forme indexée (Comme un moteur de recherche hyper rapide).
3. **Kibana** (L'écran) : L'interface web qui permet de faire de superbes graphiques (Camemberts, Courbes d'évolution).

### La naissance du SIEM
Lorsque vous prenez une stack ELK et que vous y ajoutez de "l'intelligence" (Des règles mathématiques du type : *"Alerte-moi immédiatement si un utilisateur rate son mot de passe 50 fois en 1 minute sur 3 serveurs différents"*), le serveur de logs devient un **SIEM (Security Information and Event Management)**, l'outil de travail exclusif du centre de cyberdéfense (SOC).