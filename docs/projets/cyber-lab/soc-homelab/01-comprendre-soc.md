---
description: "Module 1 - Définition d'un SOC, gouvernance, SIEM vs EDR, et choix stratégiques (8/5 vs 24/7)."
---

# Module 1 - Comprendre ce qu'est un SOC

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Gouvernance & Stratégie"
  data-time="~1 h">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le corps humain et son système immunitaire"
    Imaginez votre entreprise comme un corps humain. Les pare-feux et antivirus classiques sont comme votre peau : ils bloquent 99% des infections courantes. Mais si une bactérie agressive (hacker) pénètre sous la peau, il vous faut un système immunitaire actif, capable de repérer l'anomalie, de corréler les symptômes (fièvre, toux) et de déclencher une réponse immunitaire ciblée (globules blancs). Le **SOC (Security Operations Center)** est ce système immunitaire : il ne se contente pas de bloquer à l'aveugle, il analyse en profondeur pour survivre aux attaques complexes.

## 1.1 - Objectifs pédagogiques

À la fin de ce module, l'apprenant doit être capable de :

- Définir avec ses propres mots ce qu'est un SOC, un SIEM, un EDR, un IDS et un SOAR, et de citer un outil open-source pour chacun.
- Justifier l'existence d'un SOC à un dirigeant non-technique en moins de cinq minutes.
- Distinguer les trois modèles d'opération d'un SOC (internalisé, mutualisé, externalisé) et leurs implications budgétaires.
- Citer les trois contraintes structurelles qui empêchent une PME de monter un SOC classique.

<br>

---

## 1.2 - Définitions opérationnelles

Le vocabulaire de la cybersécurité est saturé d'acronymes qui se recoupent. Voici les définitions strictement nécessaires pour la suite du cours.

| Sigle | Signification | Définition opérationnelle | Outil de référence open-source |
|---|---|---|---|
| **SOC** | Security Operations Center | Cellule humaine et technique qui surveille en continu, détecte, qualifie et répond aux incidents de sécurité | (l'ensemble des outils ci-dessous) |
| **SIEM** | Security Information and Event Management | Plateforme qui collecte, normalise, stocke et corrèle les journaux de sécurité pour générer des alertes | Wazuh, Graylog, OpenSearch + Elastic Stack |
| **IDS** | Intrusion Detection System | Sonde qui analyse le trafic réseau ou un flux de logs et émet des alertes en cas de motif suspect | Suricata, Zeek, Snort |
| **EDR** | Endpoint Detection and Response | Agent installé sur un poste, capable de détecter et de réagir localement (isolement, kill process) | Wazuh agent (capacités EDR limitées), Velociraptor pour le forensique |
| **SOAR** | Security Orchestration, Automation and Response | Couche d'orchestration qui automatise les playbooks de réponse entre les outils du SOC | TheHive + Cortex, Shuffle |
| **CTI** | Cyber Threat Intelligence | Renseignement sur les menaces (acteurs, IoC, TTP), nourrit les règles de détection | OpenCTI, MISP |

!!! warning "Le point critique à retenir"
    Un SIEM seul n'est pas un SOC. Un SOC, c'est trois piliers - **Personnes, Processus, Technologie**. Le HomeLab ne couvre que la Technologie ; les deux autres piliers se travaillent en parallèle, avec le RSSI ou son équivalent.

<br>

---

## 1.3 - Pourquoi une PME en a besoin (et pourquoi elle bloque)

![Les trois contraintes structurelles d'une jeune entreprise face au SOC](../../assets/cyber-lab/images/01-contraintes-jeune-entreprise.png)
<p><em>Illustration des freins majeurs empêchant l'adoption d'un SOC dans une PME.</em></p>

Trois contraintes structurelles bloquent l'adoption d'un SOC classique dans une jeune entreprise :

- **Absence de financement** : Les solutions commerciales (Splunk, QRadar, Sentinel) sont au-dessus de 50 000 euros par an pour le minimum syndical, sans compter les licences agents.
- **Cadre normatif incomplet** : Sans politique de sécurité formalisée, on ne sait pas ce qu'on doit surveiller, ni avec quel niveau d'exigence.
- **Effectifs limités** : Un SOC 24/7 demande au minimum cinq personnes (couverture nuit + week-end + congés). Un SOC 8/5 demande deux personnes minimum.

Le HomeLab résout temporairement la première contrainte (zéro coût logiciel), met partiellement en lumière la deuxième (en obligeant à formaliser des règles), et **n'aborde pas du tout** la troisième - qui reste le vrai mur quand l'entreprise grandit.

<br>

---

## 1.4 - Les piliers de la gouvernance d'un SOC

![Les piliers fondamentaux d'un SOC](../../assets/cyber-lab/images/02-piliers-gouvernance-soc.png)
<p><em>Cartographie de la gouvernance et de l'alignement stratégique d'un SOC.</em></p>

Cinq piliers structurent la gouvernance d'un SOC, quel que soit son périmètre :

| Pilier | Question à laquelle il répond |
|---|---|
| Alignement stratégique | Le SOC sert-il les objectifs métier de l'entreprise ? |
| Gestion des risques | Surveille-t-on ce qui est critique, ou ce qui est facile à surveiller ? |
| Optimisation des ressources | Le rapport coût / bénéfice est-il défendable ? |
| Sensibilisation et maturité | Les utilisateurs comprennent-ils leur rôle dans la chaîne de défense ? |
| Anticipation des coûts | Sait-on combien coûtera la version "production" du SOC dans 18 mois ? |

Dans un mémoire de certification ou une présentation à la direction, ces cinq piliers servent de plan-type pour défendre un projet SOC.

<br>

---

## 1.5 - SOC à faible coût - matrice de positionnement

![Matrice coût - efficacité des approches SOC](../../assets/cyber-lab/images/03-matrice-cout-efficacite.png)
<p><em>Analyse comparative entre coût et efficacité des solutions de sécurité.</em></p>

Cette matrice classe quatre approches sur deux axes (coût et efficacité) :

- **HomeLab pour simulation** (faible coût, haute efficacité pédagogique) - notre cas.
- **Mise en œuvre complète du SOC** (haut coût, haute efficacité) - cible à 18-24 mois.
- **Outils open-source de base, sans gouvernance** (faible coût, faible efficacité) - le piège classique.
- **Solutions commerciales coûteuses mais inefficaces** (haut coût, faible efficacité) - existe quand l'outil est imposé sans projet derrière.

!!! note "Le HomeLab comme étape"
    Le HomeLab est une étape, pas une destination. Le confondre avec un SOC opérationnel en production est l'erreur la plus fréquente.

<br>

---

## 1.6 - Priorisation stratégique des défis

![Matrice de priorisation des défis pour la mise en place d'un SOC](../../assets/cyber-lab/images/07-matrice-priorisation-defis.png)
<p><em>Priorisation des actions de sécurité selon leur impact et leur complexité de préparation.</em></p>

Cette matrice positionne quatre actions sur deux axes (impact et préparation requise). Lecture :

- **Démonstration HomeLab** (fort impact, faible préparation) - le présent cours.
- **Sensibilisation à la cybersécurité** (fort impact, haute préparation) - démarche RH/communication.
- **Outils distanciels** (faible impact, faible préparation) - prérequis basiques (VPN, MFA).
- **Infrastructure prête à l'emploi** (faible impact, haute préparation) - le piège de la solution clé en main mal calibrée.

Concrètement, on commence par le quadrant haut-gauche (Démonstration HomeLab) qui maximise le retour sur effort, puis on monte vers le haut-droit (Sensibilisation) qui demande plus d'investissement mais protège plus largement.

<br>

---

## 1.7 - Choix stratégique - 8/5 ou 24/7

![Comparaison des stratégies de surveillance 8/5 et 24/7](../../assets/cyber-lab/images/08-strategie-8-5-vs-24-7.png)
<p><em>Le débat du temps de couverture : coût humain vs vulnérabilité nocturne.</em></p>

Question à poser à la direction, en une phrase : **"Acceptez-vous qu'une attaque lancée le vendredi soir à 23h ne soit détectée que le lundi matin à 8h, soit 57 heures de présence libre de l'attaquant sur nos systèmes ?"**

Si la réponse est non, le 24/7 est obligatoire et il faut budgéter cinq personnes minimum. Si la réponse est oui (parce que l'entreprise estime que ses données ne valent pas le coût humain global), le 8/5 reste un choix défendable, à condition de l'écrire noir sur blanc dans la politique de sécurité et de le documenter dans le registre des risques. 

Refuser de trancher revient à choisir le 8/5 par défaut, sans en assumer les conséquences.

<br>

---

## 1.8 - Points de vigilance

- Confondre "avoir installé un SIEM" avec "avoir un SOC". Un SIEM sans personnel pour traiter les alertes produit du bruit qui finit par être ignoré.
- Acheter une solution commerciale avant d'avoir formalisé la politique de sécurité. Vous achetez un outil sans savoir ce qu'il doit surveiller.
- Croire que le 8/5 protège pendant la nuit "parce que les attaques se produisent rarement". Statistiquement, c'est l'inverse : les attaques exploitent volontairement les heures non ouvrées.

<br>

---

## 1.9 - Axes d'amélioration vs projet original

| Constat dans le projet 2025 | Amélioration recommandée |
|---|---|
| Le rapport mélange gouvernance et technique, ce qui rend la lecture confuse pour un dirigeant | Séparer en deux livrables distincts : note de cadrage 4 pages pour la direction, rapport technique pour l'équipe IT |
| Aucun KPI gouvernance défini en amont (MTTD, MTTR, taux de couverture) | Définir 3 à 5 KPI dès le module 2, et alimenter chacun avec les données réelles du HomeLab |
| Pas de cartographie des risques préalable à la sélection des règles de détection | Ajouter une phase d'identification des risques (méthode EBIOS RM allégée) avant de configurer Wazuh |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un SOC n'est pas un outil que l'on installe et que l'on oublie. C'est une synergie vivante entre la technologie, les processus et l'humain. Le choix d'une couverture 8/5 ou 24/7 démontre immédiatement si le budget suit les ambitions sécuritaires de l'entreprise.

> Maintenant que la définition et la stratégie sont claires, passons à l'organisation humaine et normative dans le **[Module 2 : Gouvernance, rôles et processus du SOC →](./02-gouvernance-processus.md)**
