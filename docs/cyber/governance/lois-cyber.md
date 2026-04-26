---
description: "Lois Cyber — Le cadre juridique et réglementaire encadrant la cybersécurité, le pentest et la réponse à incident (Loi Godfrain, RGPD, NIS2, DORA)."
icon: lucide/scale
tags: ["GOUVERNANCE", "LOIS", "JURIDIQUE", "PENTEST", "CONFORMITÉ"]
---

# Cadre Légal et Réglementaire

<div
  class="omny-meta"
  data-level="🟢 Fondamental"
  data-version="2026"
  data-time="~30 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/lois.svg" width="250" align="center" alt="Balance Justice Cyber Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Permis de Chasse"
    Un pentester sans contrat, c'est comme un chasseur qui entre sur une propriété privée armé jusqu'aux dents : peu importe que ses intentions soient bonnes, il est en infraction. Les lois sont les frontières du terrain de jeu. Elles protègent à la fois la victime (les données personnelles) et le pentester (qui a le "permis" légal d'attaquer via son contrat).

La cybersécurité n'est pas qu'un défi technique, c'est un domaine extrêmement encadré par le droit. Une action technique (comme un scan de port) peut basculer d'une prestation de service légitime à un acte criminel passible de prison, simplement parce qu'un papier (le contrat) manque. 

Ce module compile les lois fondamentales que tout professionnel (Red Team ou Blue Team) doit connaître.

<br>

---

## 🏛️ 1. Le Droit Pénal (L'Attaque)

En France, le Code Pénal réprime l'ensemble de ce qu'on appelle les atteintes aux STAD (Systèmes de Traitement Automatisé de Données). Historiquement connue sous le nom de **Loi Godfrain (1988)**.

### Les 4 infractions majeures
1. **L'accès et le maintien frauduleux (Art. 323-1)**
   - *Exemple technique* : Scanner un serveur avec Nmap, trouver un port Telnet ouvert sans mot de passe, et s'y connecter.
   - *Peine maximale* : 3 ans d'emprisonnement et 100 000 € d'amende (doublée si le système appartient à l'État).
2. **L'atteinte à l'intégrité (Art. 323-2)**
   - *Exemple technique* : Supprimer un log, modifier une base de données, défigurer un site web (Defacement).
3. **L'atteinte au fonctionnement (Art. 323-2)**
   - *Exemple technique* : Lancer une attaque par déni de service (DDoS) qui ralentit ou rend indisponible le serveur.
4. **La création ou fourniture d'outils (Art. 323-3-1)**
   - *Exemple technique* : Créer un malware, un crypteur ou partager une liste de mots de passe volés *dans le but* de commettre une infraction.

!!! warning "L'Exception du Pentester"
    Pour être dans la légalité, un auditeur doit posséder une autorisation expresse, écrite et préalable du propriétaire du système. Cette autorisation prend la forme d'un contrat incluant une clause de "Rules of Engagement" (RoE).

<br>

---

## 🛡️ 2. La Protection des Données (La Fuite)

Lors d'un test d'intrusion ou d'une réponse à incident, vous allez manipuler des données. 

### Le RGPD (Règlement Général sur la Protection des Données)
- **Objectif** : Protéger les données personnelles des citoyens européens (PII).
- **Obligation en cas de fuite** : Si un incident compromet des données personnelles (ex: base de données clients volée par un ransomware), l'entreprise a **72 heures** pour notifier l'autorité de contrôle (la CNIL en France).
- **Impact Pentest** : Un pentester qui "exfiltre" la base de données de production entière vers son propre serveur AWS sans l'avoir expressément stipulé dans le contrat commet une faille de sécurité lui-même.

<br>

---

## 🏢 3. Les Réglementations Opérationnelles (L'Obligation)

Les entreprises ne font pas de la sécurité uniquement par bonne volonté, mais parce que la loi les y oblige.

### NIS 2 (Network and Information Security Directive)
Directive européenne visant à élever le niveau commun de cybersécurité.
- **Cible** : Les OSE (Opérateurs de Services Essentiels) et des milliers d'entreprises de taille moyenne à grande dans des secteurs critiques (Énergie, Transport, Santé).
- **Impact** : Obligation d'avoir un SMSI, de faire des tests d'intrusion réguliers, et de signaler les incidents majeurs en 24h.

### DORA (Digital Operational Resilience Act)
Le petit frère de NIS2, mais ciblé exclusivement sur le secteur **Financier** (Banques, Assurances).
- **Impact** : Oblige les banques à réaliser des "Threat-Led Penetration Testing" (TLPT) — c'est-à-dire des missions Red Team très poussées qui testent la résilience réelle face à des attaques de type APT.

<br>

---

## 🌐 4. L'Extraterritorialité (Le Droit International)

Internet n'a pas de frontières, les lois si.

- **CLOUD Act (États-Unis)** : Permet aux forces de l'ordre américaines de contraindre un fournisseur cloud américain (AWS, Azure, GCP) à fournir des données stockées sur ses serveurs, même si ces serveurs sont situés en Europe. C'est l'argument principal en faveur du Cloud Souverain (SecNumCloud).
- **Convention de Budapest** : Le premier traité international sur la cybercriminalité, facilitant la coopération entre polices pour enquêter sur les hackers traversant les frontières.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un bon outil vous donne le pouvoir de détruire ou d'investiguer un système, mais la loi dicte quand et comment vous pouvez le faire. Comprendre la Loi Godfrain, le RGPD et NIS2 vous permet de dialoguer avec les directions (COMEX) et de justifier le budget sécurité.

> Avant d'installer un système d'exploitation offensif comme Kali Linux, assurez-vous d'avoir compris ce cadre légal. Passez ensuite au choix de votre OS avec **[Le Comparatif des OS Cyber](../tools/os-cyber.md)**.
