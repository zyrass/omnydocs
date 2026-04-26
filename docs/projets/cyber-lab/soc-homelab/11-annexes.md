---
description: "Annexes du Cyber-Lab : Audit critique du projet original de 2025, récapitulatif des outils, idées de projets avancés et liens vers les documentations officielles."
---

# Annexes

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Ressources"
  data-time="~15 min">
</div>

## Introduction

!!! quote "Analogie pédagogique — La boîte à outils du mécanicien"
    Les annexes ne se lisent pas de bout en bout comme un roman. C'est votre boîte à outils. Vous y revenez quand vous cherchez un lien précis, une commande oubliée, ou de l'inspiration pour votre prochain défi.

<br>

---

## Annexe A - Audit critique du projet original (R03-SOC 2025)

Ce cours est la transposition pédagogique d'un mémoire de certification réel rendu en février 2025. Voici ce qui a été conservé, et ce qui a été modifié pour des raisons de rigueur technique et pédagogique.

### Ce qui était très bon et a été conservé
- **L'angle "PME"** : La justification des contraintes (finances, effectifs) est extrêmement réaliste et ancrée dans le monde professionnel francophone actuel.
- **La topologie simple** : Le choix d'une cible et d'un attaquant séparés sous Vagrant est parfait pour la simulation.
- **Le Script Discord** : Une excellente preuve de concept d'intégration externe en Python.

### Ce qui posait problème et a été corrigé
- **L'abstraction excessive du réseau** : Le projet utilisait un mélange NAT/Bridge aléatoire. Le cours impose le mode `private_network` (Host-Only) pour garantir un isolement total.
- **La sous-évaluation matérielle** : Allouer 4 Go au SIEM Wazuh 4.x provoque des corruptions de base de données silencieuses. Le cours impose 6 Go minimum.
- **L'absence de rôle "Attaquant / Défenseur"** : L'étudiant jouait les deux en même temps sans distinguer la provenance des logs. L'approche par "Casquettes" (Module 8) a été ajoutée.
- **Le Scripting bash fragile** : Le calcul des KPI se faisait via un pipeline Bash peu robuste. Remplacé par un script Python modulaire (Module 9).

<br>

---

## Annexe B - Récapitulatif de la boîte à outils

Un tableau synthétique des logiciels utilisés, pour vos futurs recrutements ou entretiens.

| Outil | Catégorie | Ce qu'il fait dans le projet | Ce qu'il fait en production (Entreprise) |
|---|---|---|---|
| **Vagrant** | Orchestrateur (IaC) | Crée nos 3 VMs depuis un fichier texte | Déploie des environnements de dev identiques à la prod |
| **VirtualBox** | Hyperviseur de type 2 | Fait tourner les VMs sur Windows/Mac | Remplacé par VMware ESXi ou Proxmox (Type 1) |
| **Ubuntu 24.04** | OS Linux | Héberge nos outils | OS standard des serveurs Web/App mondiaux |
| **Suricata** | NIDS (Network IDS) | Renifle les paquets ICMP et génère des logs | Placé en coupure (Tap) sur le cœur de réseau physique |
| **Wazuh Agent** | HIDS/EDR | Lit le fichier de log Suricata et l'envoie | Surveille la RAM, les processus et les clés USB |
| **Wazuh Server** | SIEM | Reçoit, filtre et déclenche le script Discord | Cerveau central du SOC, ingère des téraoctets par jour |
| **Discord (API)** | Webhook / ChatOps | Affiche l'alerte sur votre téléphone | Remplacé par Slack, Teams, ou Jira (Ticketing) |

<br>

---

## Annexe C - Idées de projets pour aller plus loin

Vous avez terminé le HomeLab ? Voici 4 défis pour monter en compétence (sans changer de VMs).

1. **Le Web Application Firewall (WAF)** :
   - Installez `nginx` sur la cible.
   - Installez ModSecurity.
   - Depuis l'attaquant, lancez une attaque SQL Injection (via `curl`).
   - Objectif : Voir l'alerte SQL Injection remonter dans Wazuh.

2. **La réponse active (Active Response)** :
   - Wazuh permet non seulement de lire, mais d'agir.
   - Configurez Wazuh pour que si une IP échoue 5 fois à se connecter en SSH en moins d'une minute, Wazuh ordonne à l'agent d'ajouter cette IP au pare-feu (`iptables -DROP`) pendant 10 minutes.

3. **Le fichier malveillant (FIM - File Integrity Monitoring)** :
   - Activez le module FIM sur l'agent Wazuh.
   - Surveillez le dossier `/etc/`.
   - Modifiez `/etc/passwd` depuis la cible.
   - Objectif : Recevoir une alerte "Fichier système critique modifié" sur Discord.

4. **Le Bruteforce Windows** :
   - Créez une 4ème VM sous Windows 10 (via Vagrant ou manuellement).
   - Installez l'agent Wazuh Windows.
   - Depuis l'attaquant, lancez un bruteforce RDP (avec l'outil `hydra`).
   - Objectif : Créer une règle Wazuh pour intercepter les EventID Windows d'échec de connexion.

<br>

---

## Annexe D - Ressources et documentations officielles

La cybersécurité évolue tous les mois. Ne vous fiez jamais à un tutoriel vieux de 3 ans (pas même celui-ci). La vérité absolue se trouve dans la documentation de l'éditeur.

- **Wazuh Documentation (4.14)** : [https://documentation.wazuh.com](https://documentation.wazuh.com)
- **Suricata User Guide (7.x)** : [https://suricata.readthedocs.io](https://suricata.readthedocs.io)
- **Vagrant Documentation** : [https://developer.hashicorp.com/vagrant/docs](https://developer.hashicorp.com/vagrant/docs)
- **Matrice MITRE ATT&CK** : [https://attack.mitre.org](https://attack.mitre.org)
- **Discord Developer Portal (Webhooks)** : [https://discord.com/developers/docs/resources/webhook](https://discord.com/developers/docs/resources/webhook)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Vous avez maintenant posé vos mains dans le cambouis. Vous savez que le SOC n'est pas une boîte magique qu'on achète 100 000 euros, mais un assemblage minutieux de logs, de règles, de scripts et de processus humains.

> Retourner à l'accueil du cours : **[Introduction au projet →](./index.md)**
