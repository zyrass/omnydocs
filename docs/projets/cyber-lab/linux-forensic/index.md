---
description: "Cours complet d'introduction au forensic Linux - acquisition mémoire avec Volatility 3, récupération de fichiers avec PhotoRec et chaîne de garde judiciaire."
---

# Investigation Forensic

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Volatility 3, PhotoRec"
  data-time="~10 h">
</div>

## Présentation du cours

!!! quote "L'analogie du détective"
    Une scène de crime informatique ressemble à une scène de crime physique. Le suspect a effacé ses traces, mais l'environnement conserve des empreintes invisibles à l'œil nu : poussière, fibres, ADN. En forensic numérique, ce sont la mémoire vive, les blocs disques non réécrits, les journaux système et les métadonnées qui jouent ce rôle. L'analyste forensic est ce détective qui sait où regarder, avec quels outils et selon quelles procédures pour que ses découvertes soient recevables devant un juge.

Ce cours s'appuie sur un cas réel d'investigation numérique : la suppression intentionnelle d'un fichier comptable par un dirigeant d'entreprise face à un contrôle fiscal imminent. 

À travers ce scénario, vous apprendrez à construire un laboratoire forensic, à acquérir des preuves selon une chaîne de garde rigoureuse, à analyser la mémoire vive avec **Volatility 3** et à récupérer des fichiers supprimés avec **PhotoRec**.

<br>

---

## Objectifs pédagogiques

À l'issue de ce cours, vous serez en mesure de :

- Mettre en place un laboratoire d'investigation numérique reproductible.
- Acquérir un dump mémoire d'une machine virtuelle sans altérer le système original.
- Maintenir la chaîne de garde via les empreintes cryptographiques.
- Identifier le noyau Linux d'une cible et téléverser les symboles correspondants.
- Exploiter les plugins Volatility pour reconstruire l'historique des commandes.
- Récupérer un fichier supprimé sur un système de fichiers ext4.
- Rédiger un rapport forensic exploitable en contexte judiciaire.

<br>

---

## Prérequis et Public cible

| Domaine | Niveau attendu |
|---|---|
| Ligne de commande Linux | Intermédiaire (cd, ls, dd, hash, redirection) |
| Virtualisation | Connaître VirtualBox (création VM, snapshots) |
| Système de fichiers | Comprendre ext4, inode, métadonnées |
| Cryptographie | Notion de hachage SHA-256 |
| Cadre juridique | Principes de la perquisition numérique en France |

Ce cours s'adresse aux **analystes SOC**, **consultants en cybersécurité**, **étudiants en cybersécurité (Bac+3 à Bac+5)** et **DPO** souhaitant comprendre la mécanique d'une investigation numérique de bout en bout. Il est compatible avec la préparation au bloc **RNCP 36399 BC03 - Investigation Numérique**.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    L'investigation numérique demande une rigueur absolue. Une preuve altérée est une preuve rejetée par le juge.

> Commençons par poser le cadre théorique et juridique dans le **[Module 1 : Fondamentaux de l'investigation numérique →](./01-fondamentaux.md)**
