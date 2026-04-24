---
description: "Découverte de Wazuh : architecture, composants, déploiement et intégration d'un SIEM/XDR open source dans un écosystème DevSecOps."
icon: lucide/book-open-check
tags: ["WAZUH", "SIEM", "XDR", "OBSERVABILITE", "DEVSECOPS"]
---

# Wazuh : SIEM et XDR Open Source

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="1.0"
  data-time="20 Minutes">
</div>

## Introduction à Wazuh

!!! quote "Définition : Wazuh"
    **Wazuh** est une plateforme open source de sécurité unifiée qui combine les capacités d'un **SIEM** (Security Information and Event Management) et d'un **XDR** (Extended Detection and Response). Elle permet de protéger les charges de travail sur site, virtualisées, conteneurisées et basées sur le cloud.

Contrairement aux solutions de surveillance classiques qui se contentent de vérifier si un serveur est "en ligne" (comme Nagios ou Zabbix), Wazuh scrute **ce qui se passe à l'intérieur** du système : les fichiers modifiés, les processus suspects, les failles de configuration et les vulnérabilités logicielles.

<br>

---

## 1. Architecture de la Plateforme

Wazuh repose sur une architecture distribuée et hautement évolutive, séparant la collecte, l'analyse et le stockage des données.

```mermaid
flowchart TD
    subgraph Endpoints ["Vos Serveurs & Cloud"]
        A1[Wazuh Agent\n(Linux)]
        A2[Wazuh Agent\n(Windows)]
        A3[Wazuh Agent\n(Docker/K8s)]
    end

    subgraph Wazuh_Cluster ["Cluster Central Wazuh"]
        M[Wazuh Server\n(Manager / Analyse)]
        I[(Wazuh Indexer\n(Stockage & Recherche))]
        D[Wazuh Dashboard\n(Interface UI)]
    end

    A1 -- "Logs & Events (Chiffré)" --> M
    A2 -- "Logs & Events (Chiffré)" --> M
    A3 -- "Logs & Events (Chiffré)" --> M

    M -- "Indexation" --> I
    D -- "Requêtes API" --> I
    D -. "Gestion" .-> M

    style A1 fill:#252f3e,stroke:#00aae6,stroke-width:2px,color:#fff
    style A2 fill:#252f3e,stroke:#00aae6,stroke-width:2px,color:#fff
    style A3 fill:#252f3e,stroke:#00aae6,stroke-width:2px,color:#fff
    style M fill:#00aae6,stroke:#fff,stroke-width:2px,color:#fff
    style I fill:#00aae6,stroke:#fff,stroke-width:2px,color:#fff
    style D fill:#00aae6,stroke:#fff,stroke-width:2px,color:#fff
```

### Les 4 Piliers de l'architecture

1. **Wazuh Agent** : Un programme léger installé sur les machines cibles (serveurs, postes de travail). Il lit les journaux, surveille l'intégrité des fichiers système, et envoie ces données au serveur.
2. **Wazuh Server (Manager)** : Le cerveau. Il reçoit les données des agents, les décode, et les passe dans un moteur de règles pour détecter les menaces (ex: attaques par force brute, malwares).
3. **Wazuh Indexer** : Le moteur de base de données (basé sur OpenSearch/Elasticsearch). Il stocke les millions d'événements et permet des recherches ultra-rapides.
4. **Wazuh Dashboard** : L'interface web (basée sur Kibana/OpenSearch Dashboards) pour visualiser les alertes, gérer les configurations et créer des rapports.

<br>

---

## 2. Capacités et Fonctionnalités Clés

Wazuh n'est pas qu'un simple collecteur de logs. Il intègre plusieurs modules de sécurité avancés, activés par défaut ou facilement configurables.

### FIM (File Integrity Monitoring)
Le module FIM surveille vos fichiers critiques (ex: `/etc/passwd`, configurations Nginx). Si un fichier est modifié, supprimé ou créé, l'agent calcule son hash (MD5, SHA1) et alerte immédiatement le serveur. C'est essentiel pour détecter l'installation de backdoors ou de ransomwares.

### SCA (Security Configuration Assessment)
Wazuh vérifie automatiquement si vos systèmes respectent les bonnes pratiques de sécurité (CIS Benchmarks). Il va scanner vos configurations et vous dire, par exemple : *"Le login root en SSH est autorisé sur le Serveur B, c'est une vulnérabilité critique"*.

### Détection de Vulnérabilités (VulnDetector)
En se basant sur le catalogue CVE (Common Vulnerabilities and Exposures), l'agent croise les logiciels installés sur vos machines (via `dpkg` ou `rpm`) avec les bases de données de vulnérabilités (NVD, RedHat, Debian). Il liste ainsi les paquets qu'il est urgent de mettre à jour.

!!! note "Audits réglementaires"
    Wazuh est extrêmement utilisé dans le monde professionnel car il inclut des tableaux de bord préconfigurés pour prouver la conformité aux normes **PCI DSS**, **GDPR/RGPD**, **HIPAA**, et **NIST**.

<br>

---

## 3. Wazuh dans l'écosystème DevSecOps

Dans un pipeline DevSecOps moderne, la sécurité n'est plus gérée manuellement à la fin du processus. Wazuh s'intègre parfaitement dans vos chaînes CI/CD et vos outils de déploiement (Infrastructure as Code).

### Déploiement automatisé avec Ansible
Vous ne devez jamais installer l'agent Wazuh manuellement sur 50 serveurs. En DevSecOps, on utilise **Ansible** pour déployer l'agent en masse.

```yaml title="Extrait d'un Playbook Ansible pour Wazuh Agent"
- name: Installer l'agent Wazuh
  hosts: production_servers
  tasks:
    - name: Ajouter le dépôt Wazuh
      apt_repository:
        repo: "deb https://packages.wazuh.com/4.x/apt/ stable main"
        state: present

    - name: Installer le paquet wazuh-agent
      apt:
        name: wazuh-agent
        state: present
      environment:
        WAZUH_MANAGER: "192.168.1.100" # IP du serveur Manager
        WAZUH_AGENT_GROUP: "webservers"
```

### Active Response (Réponse Active)
Wazuh peut réagir **automatiquement** à une menace sans intervention humaine (concept de SOAR - Security Orchestration, Automation, and Response).

**Exemple d'un pipeline défensif :**
1. **Détection** : L'agent repère 10 échecs de connexion SSH en 5 secondes depuis l'IP `203.0.113.5`.
2. **Analyse** : Le Manager valide l'alerte de niveau 10 (Force brute).
3. **Réponse** : Le Manager envoie un ordre "Active Response" à l'agent.
4. **Exécution** : L'agent exécute un script local qui ajoute l'IP `203.0.113.5` dans la liste noire d'`iptables` pour la bloquer temporairement.

<br>

---

## 4. Intégration Cloud & Conteneurs

Wazuh excelle dans l'observabilité des environnements modernes (Docker, Kubernetes, AWS, GCP).

*   **AWS CloudTrail / GuardDuty** : Le serveur Wazuh peut se connecter directement aux API AWS pour lire les logs cloud et détecter, par exemple, la création de règles de pare-feu non autorisées sur un Security Group.
*   **Docker** : Wazuh surveille le démon Docker et détecte les activités suspectes, comme un conteneur lancé avec le flag privilégié (`--privileged`), ce qui représente une faille de sécurité majeure.
*   **Intégration Webhooks** : Lorsqu'une alerte critique est déclenchée, Wazuh peut envoyer un payload JSON via Webhook vers Slack, Discord, ou un outil de ticketing (Jira, TheHive) pour alerter les équipes SOC (Security Operations Center).

!!! tip "Conclusion"
    Wazuh est la brique centrale de l'**Observabilité Sécuritaire (Obs-Sec)**. Il unifie les logs, détecte les anomalies via son moteur de règles, et prouve la conformité de l'infrastructure, le tout en Open Source.