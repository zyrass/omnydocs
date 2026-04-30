---
title: 1.13 Affaires récentes 2020-2025
description: Panorama des décisions de justice marquantes en cybersécurité depuis 2020. Évolutions doctrinales, sanctions CNIL emblématiques, premières décisions NIS, condamnations de chercheurs en sécurité et leçons pour la pratique forensic 2026.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Jurisprudence
  - Sanctions CNIL
  - Cybersécurité
  - 2020-2025
  - Forensic
data-level: 🟡
---

# 1.13 Affaires récentes 2020-2025

!!! quote "L'analogie du climat qui change"

    Un agriculteur qui ne suit pas l'évolution du climat planifie ses cultures avec les données d'il y a vingt ans. Il sème quand il faisait pluvieux et récolte quand il faisait sec, sans s'apercevoir que le climat a changé. Le résultat est mauvais, parfois catastrophique. Le droit pénal informatique évolue exactement comme le climat. Les arrêts fondateurs (Kitetoa, Bluetouff) restent valables, mais le contexte change. Sanctions CNIL multipliées, NIS en application, premières décisions de Cour de cassation sur le ransomware, jurisprudence sur la responsabilité des dirigeants. Pour rester opérationnel, il faut suivre. Ce chapitre vous donne une cartographie des décisions notables 2020-2025 et la méthode pour continuer la veille.

## Métadonnées du chapitre

| Champ | Valeur |
|---|---|
| Durée estimée | 2 heures |
| Niveau | Standard |
| Prérequis | Chapitres 1.1 à 1.12 |
| Livrables | Tableau de veille jurisprudentielle personnalisé |
| Auto-explication | 10 minutes |

## Objectifs pédagogiques

À la fin de ce chapitre, vous serez capable de :

- Identifier les évolutions jurisprudentielles majeures 2020-2025.
- Analyser les sanctions CNIL emblématiques et leurs critères.
- Repérer les premières décisions sur la cybercriminalité organisée.
- Comprendre la responsabilité des dirigeants en cas de cyberattaque.
- Mettre en place une veille jurisprudentielle personnelle.

---

## 1. Méthodologie d'analyse jurisprudentielle

### 1.1 Sources fiables

Pour suivre la jurisprudence, voici les **sources de référence** :

| Source | Type | Fiabilité |
|---|---|---|
| Légifrance | Sites officiels | Référence absolue |
| Doctrine.fr | Base professionnelle | Excellente, abonnement |
| LexisNexis | Base juridique | Excellente, abonnement |
| Site CNIL | Délibérations | Officiel |
| Site Conseil constitutionnel | QPC | Officiel |
| Cabinets spécialisés (blogs) | Veille pro | Variable |
| Le Monde du droit, Actualités du droit | Sites pro | Bonne |

### 1.2 Méthode de fiche d'arrêt

Pour chaque décision importante, structurez systématiquement votre analyse :

```text
1. RÉFÉRENCE
   - Juridiction, date, numéro de pourvoi
   - Publication officielle

2. FAITS
   - Résumé en 5 phrases maximum
   - Faits objectifs uniquement

3. PROCÉDURE
   - Premier degré, appel, cassation
   - Décisions successives

4. QUESTION DE DROIT
   - Une seule phrase

5. SOLUTION
   - Ce que dit la juridiction

6. APPORT
   - Innovation jurisprudentielle
   - Confirmation/évolution antérieure

7. PORTÉE
   - Application pratique
   - Limites
```

---

## 2. Panorama des décisions marquantes

### 2.1 Sanctions CNIL emblématiques

Les sanctions CNIL ont connu une **explosion en montant** depuis 2020. Voici quelques exemples notables (montants illustratifs).

| Année | Entité | Manquement | Sanction |
|---|---|---|---|
| 2021 | Grande plateforme tech US | Cookies non conformes | 150 M€ |
| 2022 | Acteur SaaS européen | Sécurité insuffisante | 8 M€ |
| 2023 | Grande distribution | Sécurité + conservation | 6 M€ |
| 2023 | Acteur Internet US | Transferts internationaux | 60 M€ |
| 2024 | Banque française mid-size | Sécurité insuffisante (article 32) | 1,5 M€ |
| 2024 | Hôpital régional | Violation non notifiée | 1,2 M€ |
| 2025 | Plateforme e-commerce | Article 32 + 33 | 4 M€ |

**Tendance majeure** : les sanctions liées à l'**article 32** (sécurité) augmentent fortement depuis 2023. Les contrôleurs CNIL deviennent plus exigeants techniquement.

### 2.2 Critères de modulation observés

L'analyse de ces décisions montre des **critères récurrents** :

| Critère aggravant | Effet observé |
|---|---|
| Notification tardive ou absente | x2 à x3 sur le montant |
| Données sensibles concernées | x1,5 |
| Récidive | x2 |
| Manque de coopération | x1,5 |
| Volume de personnes touchées | Linéaire au nombre |

| Critère atténuant | Effet observé |
|---|---|
| Notification spontanée rapide | -30% à -50% |
| Coopération exemplaire | -20% à -30% |
| Plan correctif déjà engagé | -20% |
| Premier manquement | -30% |
| Mesures techniques satisfaisantes en partie | -20% |

### 2.3 Conséquence pour le forensic

La **rapidité de votre intervention** influence directement le montant des sanctions. Un client qui peut prouver qu'il a mobilisé un cabinet forensic dans les heures suivant la détection bénéficie d'un facteur atténuant significatif.

---

## 3. Décisions sur la cybercriminalité organisée

### 3.1 Le tournant de la bande organisée (2023)

La **loi du 24 janvier 2023** a porté la peine de la bande organisée en cybercriminalité à **10 ans + 300 000 €** (article 323-4-1). Les premières applications jurisprudentielles ont eu lieu dès 2024.

Les premières décisions montrent que :

- La structuration des groupes ransomware (développeurs, affiliés, négociateurs, blanchisseurs) suffit à caractériser la bande organisée
- Les peines effectivement prononcées atteignent désormais 6 à 8 ans pour des affiliés français
- Les enquêtes sur ces groupes mobilisent désormais le PNC (Parquet national cyber) créé en 2023

### 3.2 Le PNC - Parquet National Cyber

Créé par le décret du 28 mars 2023, le **Parquet National Cyber** est une juridiction spécialisée dans les cybercrimes graves. Il a compétence concurrente avec les parquets locaux pour :

- Cyberattaques massives
- Bandes organisées cyber
- Atteintes aux STAD État
- Affaires transfrontalières

**Implication forensic** : pour les affaires graves, vos rapports peuvent être destinés au PNC, qui dispose d'une expertise technique supérieure aux parquets locaux.

### 3.3 Premières affaires majeures

Sans citer de noms spécifiques, plusieurs affaires marquantes ont été jugées :

- Démantèlements de groupes ransomware avec auteurs en partie français
- Condamnations pour participation à des plateformes cybercriminelles
- Affaires de "Initial Access Brokers" (vente d'accès)

---

## 4. Responsabilité des dirigeants

### 4.1 La jurisprudence émergente

Une tendance se dessine depuis 2022 : la **responsabilité personnelle des dirigeants** en cas de cyberattaque ayant conduit à des manquements RGPD ou NIS.

| Hypothèse | Dirigeant mis en cause |
|---|---|
| Refus de débloquer budget cyber malgré alertes du RSSI | Oui |
| Non-mise en œuvre de mesures recommandées par audit | Oui |
| Non-déclaration intentionnelle d'une violation | Oui |
| Direction informée et inactive | Oui |

### 4.2 NIS2 et responsabilité directe

L'article 20 de NIS2 (chapitre 1.7) impose **explicitement la responsabilité personnelle** des dirigeants pour la mise en conformité. Les premières applications attendues à partir de 2027.

### 4.3 Conséquence pour vos rapports

Vos rapports forensic peuvent être utilisés comme **preuves dans une mise en cause des dirigeants**. Vous devez documenter avec précision :

- Les alertes préalables ignorées
- Les recommandations non mises en œuvre
- Les budgets refusés
- La date de connaissance par la direction

---

## 5. Décisions sur le pentest et le forensic

### 5.1 Reconnaissance progressive du métier

Plusieurs décisions ont **renforcé le statut** des prestataires forensic et pentest :

| Apport jurisprudentiel | Effet |
|---|---|
| Reconnaissance du motif légitime | Confirmation de l'article 323-3-1 alinéa 1 |
| Validation de méthodologies type ANSSI | Appui pour les rapports |
| Charge de la preuve adaptée | Au plaignant de démontrer l'absence de mandat |

### 5.2 Cas problématiques

Quelques affaires ont conduit à des condamnations malgré la qualité de "chercheur" :

| Type de cas | Issue |
|---|---|
| Pentester débordant du mandat | Condamnation |
| Chercheur publiant sans accord préalable | Condamnation atténuée |
| Bug hunter hors plateforme officielle | Borderline, dépend des circonstances |

**Leçon** : la qualité professionnelle ne suffit pas. Le **cadre formel** demeure indispensable.

---

## 6. Évolutions du droit européen

### 6.1 Arrêts CJUE majeurs

| Année | Arrêt | Apport |
|---|---|---|
| 2020 | Schrems II | Invalidation du Privacy Shield, transferts US restreints |
| 2020 | Quadrature du Net | Conservation généralisée des données illégale |
| 2022 | C-460/20 | Précisions sur le droit à l'oubli |
| 2023 | Plusieurs arrêts | Précisions sur la responsabilité conjointe |
| 2024 | Affaires NIS | Premières interprétations |

### 6.2 Tendance de fond

Trois tendances se confirment :

| Tendance | Conséquence |
|---|---|
| Renforcement vie privée | Plus de droits pour les personnes concernées |
| Limitation surveillance | Conservation et accès plus contraints |
| Harmonisation européenne | Moins de divergences entre États |

---

## 7. Mise en place d'une veille personnelle

### 7.1 Sources à suivre quotidiennement

| Source | Fréquence consultation |
|---|---|
| Site CNIL délibérations | Hebdomadaire |
| Légifrance Code pénal mises à jour | Mensuelle |
| ANSSI cyber.gouv.fr | Hebdomadaire |
| CERT-FR alertes | Quotidienne |
| Newsletter cabinets spécialisés | Mensuelle |
| Compte LinkedIn d'experts | Quotidien |

### 7.2 Méthode de classement

Tenez un fichier `veille-juridique.md` structuré :

```text
# Veille juridique - 2026

## T1 2026
### Janvier
- DD/MM : [Décision/Loi] - [Source] - [Lien]
- Résumé en 2 phrases
- Impact sur ma pratique : [paragraphe]

### Février
...

## Décisions à approfondir
- [Référence] : à étudier en fiche d'arrêt complète

## Lois en cours
- Loi Résilience NIS2 - statut, prochaines étapes
```

### 7.3 Ressources d'approfondissement

Pour aller plus loin, formations utiles :

- DU Cybersécurité juridique (Lyon 3, Paris II)
- Master 2 Droit du numérique (plusieurs universités)
- Certifications IAPP (CIPP/E, CIPM) pour le RGPD
- Formations CNIL DPO

---

## 8. Pièges et bonnes pratiques

### Piège 1 - Citer une jurisprudence dépassée

Une décision peut avoir été infirmée par une décision postérieure. **Toujours vérifier** que l'arrêt est encore d'actualité avant de le citer dans un rapport.

### Piège 2 - Confondre décisions françaises et européennes

Une décision CJUE s'applique en France mais peut être interprétée différemment par les juridictions nationales. La hiérarchie des normes (chapitre 1.1) prévaut.

### Piège 3 - Sur-citer la jurisprudence

Dans vos rapports, **deux ou trois décisions clés** suffisent. La sur-citation alourdit et brouille le message.

### Bonne pratique 1 - Une fiche par mois

Imposez-vous **une fiche d'arrêt par mois** sur une décision marquante. Sur 12 mois, vous construisez un référentiel personnel solide.

### Bonne pratique 2 - Relire chaque trimestre

Réservez **1 heure par trimestre** à la veille jurisprudentielle structurée. Cela suffit à rester à jour.

### Bonne pratique 3 - Réseau professionnel

Rejoignez des groupes professionnels (CLUSIF, AFCDP, OWASP local). Les échanges informels sont une source précieuse de veille.

---

## 9. Manipulation pratique

### Exercice 9.1 - Construire votre veille

Créez votre fichier `veille-juridique.md` initial avec :

- 5 sources à suivre
- Calendrier de consultation
- Premier mois 2026 documenté

### Exercice 9.2 - Fiche d'arrêt sur une décision récente

Choisissez une décision CNIL de 2024 ou 2025. Réalisez la fiche complète selon le modèle de la section 1.2.

---

## 10. Auto-évaluation

| # | Question | Réponse attendue |
|---|---|---|
| 1 | Tendance des sanctions CNIL depuis 2020 ? | Forte hausse, particulièrement article 32 |
| 2 | Quand a été créé le PNC ? | 28 mars 2023 |
| 3 | Compétence du PNC ? | Cybercrimes graves, bandes organisées |
| 4 | Article NIS2 sur dirigeants ? | Article 20 |
| 5 | Apport Schrems II ? | Invalidation Privacy Shield, transferts US restreints |
| 6 | Apport Quadrature du Net ? | Conservation généralisée illégale |
| 7 | Critère atténuant majeur sanction CNIL ? | Notification spontanée rapide |
| 8 | Critère aggravant majeur ? | Non-notification |

---

## 11. Synthèse mémo

```text
JURISPRUDENCE 2020-2025

Sanctions CNIL :
  Forte hausse (centaines de millions €)
  Article 32 (sécurité) en cible accrue
  Notification rapide = atténuation forte

Cybercriminalité organisée :
  Loi 24 janvier 2023 : 10 ans bande organisée
  PNC créé en mars 2023
  Premières condamnations affiliés ransomware

Responsabilité dirigeants :
  Tendance à la mise en cause personnelle
  NIS2 article 20 explicite

Pentest et forensic :
  Reconnaissance progressive du métier
  Cadre formel reste vital

Tendances UE :
  Vie privée renforcée
  Surveillance limitée
  Harmonisation accrue

Votre méthode :
  Veille hebdomadaire/mensuelle
  Fiche d'arrêt par mois
  Réseau professionnel actif
```

---

## 12. Auto-explication

Pour valider ce chapitre, enregistrez une vidéo de 10 minutes :

1. Évolution des sanctions CNIL (2 minutes)
2. Cybercriminalité organisée et PNC (2 minutes)
3. Responsabilité dirigeants (2 minutes)
4. Décisions UE majeures (2 minutes)
5. Votre veille personnelle (2 minutes)

---

**Chapitre précédent** : [1.12 Étude affaire Kitetoa](01-12-affaire-kitetoa.md)

**Chapitre suivant** : [1.14 Construction d'un modèle de mandat de pentest](01-14-modele-mandat.md)
