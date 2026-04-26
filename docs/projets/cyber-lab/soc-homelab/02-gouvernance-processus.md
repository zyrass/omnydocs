---
description: "Module 2 - Rôles, processus et gouvernance d'un SOC, alignement ISO 27001 et playbooks."
---

# Module 2 - Gouvernance, rôles et processus

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Gouvernance & Stratégie"
  data-time="~1 h">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'orchestre symphonique"
    Même avec les meilleurs instruments (Wazuh, Suricata), si chaque musicien joue sa partition dans son coin, le résultat est une cacophonie. Le **SOC Manager** est le chef d'orchestre, les **processus (playbooks)** sont la partition, et l'**ISO 27001** est le cadre qui s'assure que le concert aura bien lieu dans de bonnes conditions. La gouvernance transforme une collection de logiciels en un bouclier opérationnel coordonné.

## 2.1 - Objectifs pédagogiques

À la fin de ce module, l'apprenant doit être capable de :

- Lister les quatre niveaux d'analyse d'un SOC (N1 à N3 + CTI) et d'expliquer pourquoi une PME les fusionne.
- Lire et justifier une matrice RACI de gestion des incidents de sécurité.
- Relier les opérations d'un SOC au cycle PDCA (Deming) de la norme ISO 27001.
- Expliquer l'utilité d'un playbook (processus standardisé) face au stress d'un incident.

<br>

---

## 2.2 - Rôles et responsabilités (Le pilier "Personnes")

Dans un SOC d'entreprise mature (bancaire, industriel), les rôles sont ultra-spécialisés. Dans une PME, la réalité budgétaire force la polyvalence.

| Rôle cible | Responsabilité principale | Réalité en PME |
|---|---|---|
| **Analyste N1 (Triage)** | Regarde l'écran, valide si l'alerte est un vrai positif ou un faux positif. | Souvent sous-traité, ou géré par l'admin système de garde. |
| **Analyste N2 (Investigation)** | Creuse le vrai positif, identifie la cause racine, propose une remédiation. | Géré par l'ingénieur sécurité ou le Lead Tech. |
| **Analyste N3 (Forensic)** | Rétro-ingénierie de malware, chasse aux menaces (Threat Hunting). | Externalisé à un cabinet spécialisé (CERT). |
| **Ingénieur SIEM / SOC** | Maintient la plateforme (Wazuh), crée les règles, gère la charge CPU/RAM. | L'admin système ou DevOps en interne. |
| **Analyste CTI** | Lit les rapports de menaces et met à jour les listes de blocage. | Inexistant, remplacé par des flux automatiques (AlienVault OTX). |
| **SOC Manager** | Gère les plannings, les KPI, et rapporte au RSSI/DSI. | Souvent le RSSI lui-même, ou le DSI. |

!!! warning "L'erreur de la PME"
    Demander au seul administrateur réseau de "gérer le SOC en plus du reste". Face à une alerte critique un vendredi soir, il n'aura ni les playbooks ni le temps d'investiguer correctement.

<br>

---

## 2.3 - Matrice RACI des incidents

![Répartition des rôles et matrice RACI dans une PME](../../assets/cyber-lab/images/04-repartition-roles-pme.png)
<p><em>Exemple de matrice RACI (Responsible, Accountable, Consulted, Informed) pour un incident de sécurité.</em></p>

La matrice RACI fige qui fait quoi pendant la crise. L'exemple typique d'une infection par Ransomware :

- **R (Responsible)** : L'Analyste (ou l'Admin Système) qui isole la machine et coupe le réseau. C'est lui qui agit.
- **A (Accountable)** : Le RSSI (ou SOC Manager). Si l'isolation rate, c'est lui qui rend des comptes à la direction.
- **C (Consulted)** : Le Directeur Juridique ou le DPO (pour savoir s'il faut notifier la CNIL).
- **I (Informed)** : La Direction Générale et le service communication.

<br>

---

## 2.4 - Processus standardisés : Les Playbooks (Le pilier "Processus")

![Exemple de processus standardisé (Playbook) pour un SOC](../../assets/cyber-lab/images/05-processus-standardises.png)
<p><em>Workflow typique d'un playbook de remédiation face à une alerte critique.</em></p>

Un **Playbook** est une procédure écrite à l'avance, validée par la direction, qui dicte les actions à prendre face à une alerte spécifique.

Pourquoi est-ce vital ?
À 3h du matin, réveillé par une alerte P1 (Ransomware), un technicien n'a pas la lucidité de réfléchir aux conséquences juridiques ou métier d'une action. Si le playbook dit "Isole le port réseau du serveur de base de données immédiatement", il le fait, car la direction a déjà assumé (via la validation du playbook) que l'interruption de service coûterait moins cher que l'exfiltration des données. Sans playbook, le technicien hésitera, attendra l'avis de son chef, et l'attaque se propagera.

<br>

---

## 2.5 - Intégration à l'ISO 27001 (La roue de Deming)

![Le cycle ISO 27001 appliqué au SOC](../../assets/cyber-lab/images/06-cycle-iso27001-soc.png)
<p><em>Le cycle d'amélioration continue PDCA appliqué aux opérations de sécurité.</em></p>

Le fonctionnement du SOC s'intègre parfaitement dans le cycle PDCA de l'ISO 27001 :

1. **Plan (Planifier)** : La direction approuve le budget SOC, définit la politique de log (quoi surveiller) et rédige les playbooks.
2. **Do (Faire)** : Déploiement de Wazuh, collecte des logs, et traitement des alertes par les analystes.
3. **Check (Vérifier)** : Revue hebdomadaire des indicateurs (KPI). Combien de faux positifs ? Le délai de réaction (MTTR) est-il respecté ?
4. **Act (Agir)** : Affinement des règles Suricata pour réduire les faux positifs, mise à jour des playbooks si l'un d'eux a échoué.

!!! note "Audits et certification"
    Lors d'un audit ISO 27001, l'auditeur ne regardera pas vos règles Wazuh. Il regardera vos playbooks, et vérifiera si un ticket d'incident récent a bien suivi le playbook validé.

<br>

---

## 2.6 - Points de vigilance

- Mettre un technicien junior seul face à une console SIEM, sans playbook clair ni possibilité d'escalader au niveau supérieur, génère du stress et un taux de rotation élevé.
- Ignorer l'étape "Plan" (Planifier) de la roue de Deming. Beaucoup d'équipes foncent sur le "Do" (installer Wazuh) et se retrouvent noyées sous des milliers de logs qu'elles ne savent pas trier, car personne n'a défini ce qui était critique pour le métier.
- L'absence de tests réguliers des playbooks. Un processus jamais testé est présumé non-fonctionnel lors d'une véritable crise.

<br>

---

## 2.7 - Axes d'amélioration vs projet original

| Constat dans le projet 2025 | Amélioration recommandée |
|---|---|
| Le projet mentionne le rôle de l'analyste N1, N2, mais l'apprenant joue tous les rôles simultanément lors du TP sans différencier ses casquettes. | Lors de la partie "Scénario d'attaque", découper explicitement les actions selon le rôle (Ex: "Casquette N1 : je vois l'alerte, je qualifie / Casquette N2 : j'investigue la payload"). |
| Les notions ISO 27001 et PDCA sont survolées, sans lien avec les configurations techniques. | Lors du chapitre "Suricata" (Module 6), faire explicitement le lien avec l'étape "Act" (ajustement pour réduire le bruit) de la roue de Deming. |
| Aucune notion de "Burnout de l'analyste" (Alert Fatigue) n'est abordée. | Ajouter une section spécifique sur la fatigue des alertes lors de la conception des règles de détection (tuning). |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Avoir le meilleur outil du monde (Wazuh, Elastic, Splunk) est inutile sans les humains pour lire les alertes, et sans les processus (Playbooks) pour dicter les actions en situation de stress. L'organisation ISO 27001 permet d'auditer et d'améliorer continuellement ce triptyque.

> La théorie et la gouvernance étant désormais posées, il est temps de passer à la technique pure. Le prochain module va détailler l'infrastructure Vagrant qui va héberger notre projet dans le **[Module 3 : Architecture et topologie du HomeLab →](./03-architecture-homelab.md)**
