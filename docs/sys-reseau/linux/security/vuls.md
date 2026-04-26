---
description: "Détecter les failles de sécurité connues (CVE) dans les logiciels installés sur vos serveurs avec Vuls."
icon: lucide/book-open-check
tags: ["VULS", "CVE", "VULNERABILITE", "SECURITE", "SCANNER"]
---

# Scanner de Vulnérabilités (Vuls)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Le durcissement d'un système Linux est comme la construction des fortifications d'un château. Le pare-feu (UFW) correspond aux douves extérieures, les permissions POSIX (chmod/chown) sont les clés des différentes pièces, et la supervision (Fail2Ban/Lynis) agit comme les gardes effectuant des rondes régulières._

!!! quote "Garder une longueur d'avance"
    _Une fois votre pare-feu fermé et vos accès sécurisés, la principale menace vient des logiciels que vous utilisez légitimement (Apache, Nginx, OpenSSL, PHP). Chaque jour, de nouvelles failles (CVE - Common Vulnerabilities and Exposures) sont découvertes dans ces composants. Comment savoir si votre serveur est concerné sans lire la presse spécialisée H24 ? C'est le rôle de **Vuls**._

## Qu'est-ce que Vuls ?

**Vuls** (pour VULnerability Scanner) est un outil open-source écrit en Go, conçu pour les environnements Linux/FreeBSD. Contrairement à des scanners commerciaux très lourds (comme Nessus ou Qualys), Vuls est "Agentless" (sans agent).

```mermaid
graph LR
    subgraph Cerveau (Scanner Central)
        Vuls[Vuls Scanner]
        DB[(Bases de Vulnérabilités<br/>NVD, OVAL)]
    end
    
    subgraph Serveurs Cibles
        S1[Serveur Web<br/>Debian]
        S2[Serveur BDD<br/>Ubuntu]
    end
    
    DB -.->|Mise à jour (Fetch)| Vuls
    Vuls -->|Connexion SSH (Pas d'agent)| S1
    Vuls -->|Connexion SSH (Pas d'agent)| S2
    S1 -.->|Liste les paquets installés| Vuls
    
    style Vuls fill:#c0392b,stroke:#fff,stroke-width:2px,color:#fff
    style DB fill:#e67e22,stroke:#fff,color:#fff
    style S1 fill:#2980b9,stroke:#fff,color:#fff
    style S2 fill:#2980b9,stroke:#fff,color:#fff
```

Cela signifie qu'il n'est pas nécessaire d'installer un logiciel lourd sur chaque serveur à surveiller. Vuls s'installe sur un seul serveur "Maître", et se connecte via **SSH** à tous vos autres serveurs pour vérifier les versions des paquets installés, puis croise ces informations avec de multiples bases de données de vulnérabilités (NVD, OVAL).

---

## Le Processus de Fonctionnement

Vuls opère en trois étapes distinctes :

### 1. La collecte des bases de données (Fetch)
Vuls ne sait pas "deviner" les failles. Il doit télécharger les dictionnaires de menaces depuis Internet et les stocker localement.
```bash
# Exemple de commandes pour télécharger la base OVAL pour Debian/Ubuntu
go-oval-dictionary fetch ubuntu 22
gost fetch debian
```

### 2. Le Scan des cibles (Scan)
Vuls se connecte via SSH (en utilisant une clé publique) au serveur cible, liste tous les paquets logiciels installés (via `dpkg` ou `rpm`) et récupère leur version exacte.
```bash
# Scanner le serveur défini dans le config.toml
vuls scan
```

### 3. Le Rapport (Report)
Vuls compare la liste des logiciels trouvés avec les bases de données locales de vulnérabilités, et génère un rapport lisible (dans le terminal, en JSON, ou même par email/Slack).
```bash
vuls report -format-short-text
```

## Exemple de Rapport

Un rapport Vuls est extrêmement précieux car il ne se contente pas de dire "Vous êtes vulnérable". Il vous donne la note de gravité (Score CVSS) et souvent le lien vers la correction.

```text
debian11 (debian 11.6)
======================
Total: 3 (High:1 Medium:2 Low:0 ?:0)
1/3 Fixed, 1/3 Exploit PoC

+------------------+---------+----------+---------+-------------------+
| CVE              | Score   | Package  | FixedIn | Exploit           |
+------------------+---------+----------+---------+-------------------+
| CVE-2021-44228   | 10.0    | log4j    | 2.15.0  | Yes (Log4Shell)   |
| CVE-2022-22720   | 5.3     | apache2  |         |                   |
+------------------+---------+----------+---------+-------------------+
```
*Ici, Vuls a détecté la tristement célèbre faille Log4Shell (Score de 10.0, criticité maximale).*

## Intégration dans l'entreprise

L'utilisation de Vuls est une brique fondamentale du **Patch Management** (Gestion des correctifs). Dans une infrastructure mature :
1. Vuls est exécuté toutes les nuits via une tâche Cron.
2. S'il détecte une faille de niveau "High" ou "Critical", il envoie une alerte sur le canal Slack/Teams de l'équipe système.
3. L'administrateur peut alors planifier une mise à jour d'urgence (`apt upgrade`) du paquet concerné.

## Conclusion

L'audit système de configuration (via Lynis) et l'audit de vulnérabilités des logiciels (via Vuls) sont complémentaires. L'un vérifie que vous avez bien mis un cadenas à votre porte, l'autre vérifie que la marque de votre cadenas n'a pas été piratée récemment. Ces deux outils garantissent que l'administrateur reste proactif plutôt que réactif.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Sécuriser un système Linux exige une approche en couches : du pare-feu avec UFW à la détection d'intrusions avec Fail2Ban, en passant par un durcissement régulier. Aucun outil de sécurité ne remplace une bonne configuration de base.

> [Retourner à l'index Linux →](../index.md)
