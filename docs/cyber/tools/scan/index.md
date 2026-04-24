---
description: "Outils de scan automatisé de vulnérabilités : infrastructure, services réseau et applications web — de l'open source au standard commercial"
tags: ["SCAN", "VULNÉRABILITÉS", "OPENVAS", "NESSUS", "NUCLEI", "PENTEST", "AUDIT"]
---

# Cyber : Scan de Vulnérabilités

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire & 🔴 Avancé"
  data-version="1.0"
  data-time="5-7 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Radar de Surveillance Automatique"
    Imaginez une sentinelle qui fait le tour d'un bâtiment toutes les heures avec un immense projecteur. Elle ne cherche pas à forcer les serrures, mais elle vérifie si les fenêtres sont bien fermées, si les lumières sont allumées là où elles devraient être, et si le badge de sécurité est périmé. Le **scan de vulnérabilités** est cette sentinelle automatisée : elle analyse chaque service pour y trouver des défauts de construction (CVE) sans jamais franchir le seuil.

**Le scan de vulnérabilités** est la phase qui fait le lien entre la reconnaissance et l'exploitation. Une fois les actifs exposés identifiés, le scanner analyse chaque service détecté pour le comparer à sa base de signatures et identifier les versions vulnérables, les configurations faibles, les certificats expirés et les CVE exploitables.

<br>

---

!!! info "Pourquoi cette section est essentielle ?"
    - **Identification automatisée** : détecter les vulnérabilités connues (CVE) sur des centaines d'hôtes simultanément
    - **Priorisation** : classer les vulnérabilités par score CVSS pour orienter les efforts d'exploitation
    - **Couverture large** : identifier des vecteurs d'attaque que la reconnaissance manuelle aurait manqués
    - **Preuve documentée** : produire des rapports de scan exploitables pour le client et pour orienter le reporting
    - **Scan ciblé** : avec Nuclei, exécuter des templates spécifiques sur des vulnérabilités récentes ou sectorielles

## Les outils de cette section

<div class="grid cards" markdown>

-   **OpenVAS / Greenbone**

    ---

    Scanner de vulnérabilités open source de référence (Greenbone Community Edition). Dispose d'une base de NVT (Network Vulnerability Tests) régulièrement mise à jour, couvrant les services réseau, les applications web et les équipements. Interface web intégrée (GSA).

    [Voir OpenVAS](./openvas.md)

-   **Nessus**

    ---

    Scanner commercial de référence (Tenable). Standard de l'industrie pour les audits de vulnérabilités en environnement entreprise. Couvre infrastructure, cloud, conteneurs et applications web avec une base de plugins supérieure à 180 000. Version Essentials gratuite disponible.

    [Voir Nessus](./nessus.md)

</div>

<div class="grid cards" markdown>

-   **Nuclei**

    ---

    Scanner rapide basé sur des templates YAML (ProjectDiscovery). Permet d'exécuter des vérifications précises et ciblées : CVE spécifiques, misconfigurations cloud, exposition de fichiers sensibles, en-têtes de sécurité manquants. Extensible et intégrable dans des pipelines CI/CD.

    [Voir Nuclei](../web/nuclei.md)

</div>

## Public cible

!!! info "À qui s'adresse cette section ?"
    - **Pentesters** en phase de scanning avant l'exploitation
    - **Auditeurs sécurité** réalisant des audits de conformité et de vulnérabilités
    - **Équipes SOC/Vuln Management** gérant les vulnérabilités sur une base continue (côté défense)
    - **DevSecOps** intégrant des scans dans les pipelines de déploiement (Nuclei en particulier)

## Rôle dans l'écosystème offensif

Le scan de vulnérabilités s'insère entre la **reconnaissance passive** (OSINT) et l'**exploitation**. Il transforme une liste d'actifs exposés en une liste de vecteurs d'attaque priorisés. Les résultats d'un scan Nessus ou Nuclei orientent directement le choix des exploits dans Metasploit et la construction du plan de traitement des risques dans le rapport final.

<br>

---

## Conclusion

!!! quote "L'automatisation au service de l'expertise"
    Le scanner ne remplace pas le pentester, il lui libère du temps. En automatisant la découverte des vulnérabilités triviales, il permet à l'auditeur de se concentrer sur les failles logiques complexes que seule l'intelligence humaine peut déceler.

> Une fois les failles identifiées, passez à l'attaque ciblée sur les services réseau avec le module **[Pentest Réseau](../network/index.md)**.