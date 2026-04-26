---
description: "Lab — Cybersécurité : L'espace d'entraînement pour les attaques, les défenses et les audits de sécurité."
tags: ["CYBER", "PROJECTS", "LAB", "SOC", "FORENSIC", "MALWARE"]
---

# Lab — Cybersécurité

<div
  class="omny-meta"
  data-level="🟠 Intermédiaire"
  data-version="Multi-projets"
  data-time="~20 h">
</div>

!!! quote "Analogie pédagogique — Le terrain de manœuvre"
    On n'apprend pas la stratégie militaire uniquement dans les livres, il faut un terrain de manœuvre où l'on tire à blanc. Le laboratoire de cybersécurité est ce terrain. Vous allez y construire des architectures, les attaquer pour en comprendre les failles, et les défendre pour en maîtriser la supervision.

!!! quote "Le Pitch"
    Ce répertoire regroupe des **projets pratiques majeurs** couvrant l'ensemble du spectre de la cybersécurité moderne (Blue Team, Red Team, Forensique, etc.). Mettez en pratique vos connaissances théoriques dans des environnements isolés et contrôlés.

!!! abstract "Organisation des Projets"
    - **Blue Team (Défense)** : Construction d'architectures sécurisées et détection d'intrusions (SIEM, IDS).
    - **Red/Purple Team (Attaque & Défense)** : Compromission de cibles, ingénierie sociale et analyse du trafic.
    - **Digital Forensics (Investigation)** : Récupération de preuves numériques et analyse post-mortem.

## 🛡️ Projets Disponibles

<div class="grid cards" markdown>

-   :lucide-shield-check:{ .lg .middle } **Projet 1 — SOC Minimaliste (Blue Team)**

    ---
    **Security Operations Center en HomeLab**  
    Création d'un SIEM (Wazuh) et d'un IDS (Suricata) en environnement isolé via Vagrant avec notifications temps réel sur Discord. Construisez votre première ligne de défense.

    **Niveau** : 🟢 Débutant | **Technos** : Wazuh, Suricata, Vagrant

    [:lucide-arrow-right: Démarrer le projet SOC HomeLab](./soc-homelab/index.md)

-   :lucide-bug:{ .lg .middle } **Projet 2 — Malware & Phishing**

    ---
    **Laboratoire Purple Team (R05)**  
    Ingénierie sociale, génération de *Reverse Shell* (msfvenom), exploitation (C2), puis analyse post-infection (Wireshark) et création de règles de détection YARA.

    **Niveau** : 🟡 Intermédiaire | **Technos** : Metasploit, Wireshark, YARA

    [:lucide-arrow-right: Démarrer le projet Malware & Phishing](./malware-analysis/index.md)

-   :lucide-hard-drive:{ .lg .middle } **Projet 3 — Investigation Forensic**

    ---
    **Digital Forensics and Incident Response (DFIR)**  
    Cas réel d'investigation Linux. Acquisition de preuves, chaîne de garde judiciaire, dump et analyse de la mémoire vive (Volatility 3), et récupération de fichiers (PhotoRec).

    **Niveau** : 🔴 Avancé | **Technos** : Volatility 3, PhotoRec, Linux

    [:lucide-arrow-right: Démarrer le projet Investigation Forensic](./linux-forensic/index.md)

</div>

## 🚧 Projets en Cours de Rédaction

<div class="grid cards" markdown>

-   :lucide-cloud-cog:{ .lg .middle } **Projet 4 — Sécurisation Cloud & Conteneurs**

    ---
    Mise en place et sécurisation d'infrastructure Docker/Kubernetes. Gestion des secrets (HashiCorp Vault) et durcissement des clusters.
    *(En cours de rédaction)*

-   :lucide-app-window:{ .lg .middle } **Projet 5 — Web Application Security**

    ---
    Exploitation et remédiation du Top 10 OWASP sur une application web vulnérable (DVWA/Juice Shop).
    *(En cours de rédaction)*

</div>

<br>

---

## Conclusion

!!! quote "L'état d'esprit"
    La cybersécurité est un domaine où la curiosité et la persévérance priment. Ne sautez pas les étapes, construisez méthodiquement.

> Le premier projet indispensable pour comprendre comment une entreprise se défend est le **[Projet 1 : SOC Minimaliste Open-Source →](./soc-homelab/index.md)**
