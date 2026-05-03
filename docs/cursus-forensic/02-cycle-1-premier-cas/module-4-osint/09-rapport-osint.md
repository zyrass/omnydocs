---
title: 4.9 Production du rapport OSINT structuré
description: Construction d'un rapport OSINT professionnel exploitable - structure type, vocabulaire, traçabilité, captures hashées. Exemple complet appliqué à ARTECH avec annexes et recommandations défensives.
authors:
  - Zyrass
date:
  created: 2026-04-30
tags:
  - Rapport OSINT
  - Documentation
  - Livrable
  - ARTECH
data-level: 🟡
---

# 4.9 Production du rapport OSINT structuré

!!! quote "L'analogie de l'expert qui présente devant un magistrat"

    Un expert technique convoqué par un magistrat dispose de quinze minutes pour exposer ses conclusions. Il a passé trois mois sur l'affaire. Si son rapport est confus, mal structuré ou plein de jargon, son expertise s'évapore en cinq minutes. À l'inverse, un rapport limpide, factuel, documenté étaye chacune de ses conclusions avec une preuve traçable. Le magistrat peut alors statuer en confiance. Votre rapport OSINT joue exactement ce rôle pour la suite des opérations. Que ce soit pour informer un commanditaire, briefer une équipe d'attaque autorisée ou archiver vos travaux, sa qualité conditionne sa valeur. Ce chapitre vous donne la grille pour produire un rapport qui survit à l'épreuve du temps.

## Métadonnées du chapitre

Ce chapitre synthétise tout le travail OSINT en un livrable professionnel. Voici ses caractéristiques.

| Champ | Valeur |
|---|---|
| Durée estimée | 3 heures |
| Niveau | Synthèse |
| Prérequis | 4.1 à 4.8 |
| Livrables | Template rapport OSINT, rapport ARTECH partiel |
| Auto-explication | 12 minutes |

## Objectifs pédagogiques

À l'issue de ce chapitre, vous serez capable de :

- Structurer un rapport OSINT complet
- Appliquer un vocabulaire neutre et factuel
- Garantir la traçabilité de chaque information
- Produire un rapport ARTECH exploitable
- Distinguer faits avérés et hypothèses
- Formuler des recommandations défensives

---

## 1. Vocabulaire et tonalité du rapport

Un rapport OSINT n'est pas un roman. Sa qualité repose largement sur le respect de règles linguistiques strictes.

### 1.1 Principes rédactionnels

Voici les règles fondamentales à appliquer dans tout rapport OSINT.

| Règle | Application |
|---|---|
| Phrases courtes | Maximum 25 mots |
| Voix active privilégiée | "L'analyste a identifié" plutôt que "il a été identifié" |
| Vocabulaire neutre | Pas de termes émotionnels |
| Pas de spéculation | Faits avérés vs hypothèses balisés |
| Citations sourcées | Chaque affirmation référencée |
| Temps : passé composé | Cohérence temporelle |

### 1.2 Vocabulaire à éviter vs à privilégier

Voici la liste des termes à éviter et leur équivalent neutre.

| À éviter | À privilégier |
|---|---|
| "L'attaquant a piraté" | "L'utilisateur identifié a accédé" |
| "Système compromis" | "Système présentant des indicateurs d'accès non autorisé" |
| "Évidemment" | "Sur la base des éléments collectés" |
| "Mot de passe faible" | "PSK susceptible d'être bruteforcé en N heures" |
| "Erreur de l'admin" | "Configuration constatée le YYYY-MM-DD" |
| "C'est sûr" | "Les éléments concordent à 80%" |
| "Cible facile" | "Surface d'attaque étendue" |
| "Hacker" | "Acteur malveillant identifié" |

### 1.3 Échelle de confiance

Pour qualifier vos affirmations, voici l'échelle de confiance à utiliser.

| Niveau | Critère | Formulation type |
|---|---|---|
| Confirmé | 3+ sources indépendantes concordantes | "Il est établi que..." |
| Probable | 2 sources concordantes | "Les éléments suggèrent que..." |
| Hypothétique | 1 source ou inférence | "Il est possible que..." |
| À vérifier | Information non corroborée | "L'information reste à confirmer" |

## 2. Structure d'un rapport OSINT professionnel

### 2.1 Architecture en 9 sections

Voici la structure standard recommandée pour un rapport OSINT.

```text
RAPPORT OSINT - STRUCTURE TYPE
================================

I.    Page de garde
II.   Synthèse exécutive (1 page)
III.  Cadrage et méthodologie
IV.   Résultats par catégorie
V.    Cartographie des relations
VI.   Cibles privilégiées identifiées
VII.  Surface d'attaque
VIII. Recommandations défensives
IX.   Annexes
       - Annexe A : sources et URLs
       - Annexe B : captures hashées
       - Annexe C : journal des actions
       - Annexe D : glossaire
```

### 2.2 Page de garde

La page de garde contient les informations essentielles d'identification.

```text
Exemple de page de garde
==========================

OmnyVia
Audit OSINT défensif - ARTECH SAS
Référence : OmnyVia-OSINT-2026-001

Document confidentiel
Date d'émission : 2026-XX-XX
Auteur : Zyrass / OmnyVia
Destinataire : Hélène Lefebvre, PDG ARTECH SAS
Classification : Confidentiel

Empreinte SHA-256 du document signé :
a1b2c3...
```

### 2.3 Synthèse exécutive

La synthèse exécutive **doit tenir en 1 page** maximum. Elle s'adresse aux décideurs non techniques.

Voici la structure type d'une synthèse exécutive.

```text
SYNTHÈSE EXÉCUTIVE - exemple
================================

CONTEXTE
  ARTECH SAS, distributeur médical Lyon Vaise,
  a mandaté OmnyVia pour évaluer son exposition
  publique à l'OSINT, dans le cadre d'une
  démarche de durcissement de la posture sécurité.

PÉRIODE DE COLLECTE
  Du AAAA-MM-JJ au AAAA-MM-JJ (5 jours).

SOURCES UTILISÉES
  Pappers, BODACC, LinkedIn, theHarvester,
  Hunter.io, Wigle.net, Maltego CE.
  L'ensemble en sources publiques, sans contact
  direct avec ARTECH ni ses employés.

FAITS MARQUANTS
  - 14 employés identifiables publiquement
  - Format d'emails déduit (prenom.nom@artech.fr)
  - 3 cibles privilégiées de phishing identifiées
  - Wi-Fi ARTECH-WIFI cartographié sur Wigle
  - 2 fuites historiques contenant des emails ARTECH

NIVEAU D'EXPOSITION
  Modéré à élevé. ARTECH présente une
  surface d'attaque OSINT typique d'une PME
  française, avec quelques améliorations
  prioritaires identifiées.

RECOMMANDATIONS PRIORITAIRES
  1. Sensibilisation employés au profilage LinkedIn
  2. Renommage du SSID Wi-Fi
  3. Réinitialisation des comptes affectés par fuites
  4. Migration WPA3-SAE
  5. Audit OSINT trimestriel récurrent
```

### 2.4 Cadrage et méthodologie

Cette section précise les conditions de la mission. Voici son contenu type.

```text
CADRAGE ET MÉTHODOLOGIE
==========================

Mandat
  Référence : OmnyVia-OSINT-2026-001
  Signataire : Hélène Lefebvre, PDG ARTECH SAS
  Date signature : YYYY-MM-DD
  Durée : 5 jours ouvrés

Périmètre autorisé
  - Reconnaissance OSINT passive
  - Sources publiques uniquement
  - Pas de scan actif d'infrastructure
  - Pas de sock puppet engageant les employés

Périmètre exclu
  - Tentative de connexion Wi-Fi
  - Phishing actif
  - Vol de credentials
  - Récupération de données via fuites illégales

Base légale RGPD
  Article 6.1.f - Intérêt légitime
  Test de mise en balance : Annexe E

Conservation
  6 mois post-livrable, anonymisation immédiate.
  Destruction garantie au 2026-XX-XX (J + 6 mois).

Méthodologie suivie
  Framework OSINT Bazzell
  Workflow OmnyAcademy en 7 étapes
  Documentation continue (Hunchly + Manifest SHA-256)
```

## 3. Résultats par catégorie

Cette section est le **cœur du rapport**. Elle organise les résultats par thématique.

### 3.1 Identité organisationnelle

Voici la structure type pour cette sous-section.

```text
IDENTITÉ ORGANISATIONNELLE
============================

Données légales (source : Pappers, BODACC)
  Raison sociale : ARTECH SAS
  SIRET : XXX XXX XXX 00012
  Forme juridique : SAS
  Capital : 100 000 €
  Date création : YYYY-MM
  Effectif : 20 à 49 (tranche INSEE)
  NAF : 4646Z (commerce de gros pharmaceutique)
  Adresse : N rue X, 69009 Lyon

Dirigeants
  Hélène Lefebvre, Présidente
  Date prise de fonction : YYYY

Filiales
  Aucune identifiée

Annonces BODACC notables (5 dernières années)
  YYYY : Création
  YYYY : Modification statutaire
  YYYY : Augmentation capital
```

### 3.2 Empreinte numérique

Cette sous-section détaille la présence en ligne. Voici le contenu type.

```text
EMPREINTE NUMÉRIQUE
=====================

Domaine principal
  artech.fr
  Hébergement : France (Cloudflare CDN devant)
  IP publique : XX.XX.XX.XX
  AS : ASNNN (FR)

Sous-domaines identifiés (par theHarvester + crt.sh)
  www.artech.fr
  mail.artech.fr (MX)
  intranet.artech.fr (résolution interne)
  api.artech.fr
  shop.artech.fr

Versions historiques (Wayback)
  Captures 2018, 2020, 2022, 2024
  Refonte majeure : 2020
  Ajout boutique en ligne : 2022

Présence réseaux sociaux entreprise
  LinkedIn Company : 800+ followers
  Twitter/X : 150 followers, peu actif
  Facebook : 200 likes, peu actif
  YouTube : non présent
```

### 3.3 Empreinte humaine

Cette sous-section détaille les employés identifiés.

```text
EMPREINTE HUMAINE
===================

Effectif identifiable publiquement
  14 sur ~30 estimés (47%)

Format d'emails déduit
  prenom.nom@artech.fr
  Confiance : 92% (Hunter.io)

Liste des employés identifiés (anonymisée pour ce rapport)
  [Liste détaillée dans Annexe F]

Concentration géographique
  90% Lyon métropole
  10% télétravail provincial

Plateformes les plus utilisées
  LinkedIn : 14/14 employés identifiés
  X : 4/14
  GitHub : 2/14 (techniques)
  Strava : 1/14 (visible publique)

Profils actifs
  Posts LinkedIn fréquents : 3 employés
  Engagement public quotidien : 1 employé
```

### 3.4 Empreinte Wi-Fi

Cette sous-section présente les résultats du wardriving.

```text
EMPREINTE WI-FI
=================

Wi-Fi détectés autour du bâtiment ARTECH
  47 AP visibles (zone urbaine dense)

ARTECH-WIFI identifié
  BSSID : 64:70:02:XX:XX:XX
  Constructeur : TP-Link
  Modèle probable : Archer C7
  Sécurité : WPA2-PSK CCMP
  Canal : 6
  RSSI depuis trottoir : -67 dBm
  Position GPS : 45.7682, 4.8014

Référencement public
  Présent dans Wigle.net depuis 2022
  Position trilatéralisée à ~10 m du bâtiment

Voisinage
  3 entreprises voisines identifiables
  Plusieurs Livebox résidentielles
  2 cafés Wi-Fi public à 50 m
```

### 3.5 Fuites de données

Voici comment présenter les résultats de cette catégorie.

```text
FUITES DE DONNÉES (HIBP)
==========================

Recherche : domain audit @artech.fr (HIBP Pro)

Résultats
  Total emails @artech.fr exposés : 5
  
  CRITIQUE
    - PDG (LinkedIn 2021, Adobe 2013)
      Mot de passe vu dans Pwned Passwords
  
  ÉLEVÉ
    - DSI (Dropbox 2012, MyFitnessPal 2018)
  
  MODÉRÉ
    - 3 employés (LinkedIn 2021)

Action recommandée
  Reset immédiat des comptes CRITIQUE
  Activation MFA obligatoire
```

## 4. Cartographie des relations

Cette section présente le **graphe Maltego** ou équivalent. Voici comment l'introduire.

```text
CARTOGRAPHIE DES RELATIONS
============================

L'analyse a permis de construire une cartographie
des relations entre entités identifiées (Annexe B
contient le graphe Maltego complet en PDF).

Pivots clés identifiés
  - Domaine artech.fr lie infrastructure et employés
  - Email format permet inférence systématique
  - Trois employés ont fréquenté la même école
    (potentiel cercle de confiance interne)
  - Strava du DSI révèle parcours quotidien
    domicile-travail

Découvertes notables
  Le profilage croisé révèle que deux employés
  partagent un nom de famille rare. Vérification
  ouverte (lien familial probable).
```

## 5. Cibles privilégiées

Cette section synthétise les cibles identifiées au chapitre 4.5.

```text
CIBLES PRIVILÉGIÉES
=====================

Trois cibles ont été identifiées comme prioritaires
pour une éventuelle attaque de phishing.

CIBLE 1 - Profil "stagiaire commerce"
  Score : 78/90
  Justification synthétique :
    - Profil junior, formation cybersécurité limitée
    - Forte exposition publique
    - Tagué publiquement avec collègues identifiables
  Vecteur recommandé :
    Phishing ciblé "instruction tutrice"
    avec macro Word
  Heure d'envoi optimale :
    Lundi matin 8h-9h

CIBLE 2 - Profil "comptable senior"
  Score : 72/90
  Justification synthétique :
    - Validation factures et virements
    - Procédures établies (vulnérable au CEO fraud)
    - Profil discret en ligne mais position critique
  Vecteur recommandé :
    Phishing facture fournisseur usurpée

CIBLE 3 - Profil "PDG"
  Score : 68/90
  Justification synthétique :
    - Whaling = bénéfice maximum
    - Authority bias chez subordonnés
    - Présence publique conférences
  Vecteur recommandé :
    Usurpation identité pour ordre virement comptable
```

## 6. Surface d'attaque

Cette section synthétise tous les points d'entrée potentiels.

```text
SURFACE D'ATTAQUE - SYNTHÈSE
==============================

VECTEUR PHYSIQUE
  Wi-Fi débordant sur trottoir
  Bâtiment dans zone passante
  Pas de vidéosurveillance extérieure visible

VECTEUR HUMAIN
  3 cibles privilégiées identifiées
  Profilage permettant phishing ciblé crédible
  Mots de passe fragilisés par fuites
  Format d'emails connu

VECTEUR INFRASTRUCTURE
  Domaine ARTECH identifié
  Sous-domaines exposés
  Version logicielle CMS détectée (Wappalyzer)
  Mises à jour mensuelles non visibles côté public

VECTEUR ORGANISATIONNEL
  Pas de mention publique d'EDR ou SIEM
  Pas de mention de DPO
  Trombinoscope visible (cartographie facilitée)
  Annonces récentes BODACC (changements internes)
```

## 7. Recommandations défensives

Cette section transforme les vulnérabilités en actions concrètes.

### 7.1 Hiérarchisation

Voici comment hiérarchiser les recommandations dans le rapport.

| Priorité | Critère |
|---|---|
| Critique | Action immédiate (heures-jours) |
| Haute | Action court terme (semaines) |
| Moyenne | Action moyen terme (1-3 mois) |
| Basse | Amélioration long terme (6 mois+) |

### 7.2 Exemple ARTECH

Voici l'extrait de recommandations type appliqué à ARTECH.

```text
RECOMMANDATIONS - ARTECH
==========================

PRIORITÉ CRITIQUE

R1 - Reset des comptes affectés par fuites
  Concerne : PDG, DSI
  Délai : 48 heures
  Effort : 2 heures
  Impact : élimine vecteur connu

R2 - Activation MFA généralisée
  Concerne : tous comptes professionnels
  Délai : 1 semaine
  Effort : 1 jour
  Impact : neutralise réutilisation credentials

PRIORITÉ HAUTE

R3 - Renommage SSID Wi-Fi
  Action : "ARTECH-WIFI" → "Reseau-Pro-01"
  Délai : 1 semaine
  Effort : 2 heures
  Impact : élimine identification publique

R4 - Sensibilisation phishing
  Action : formation 1h à toute l'équipe
  Délai : 1 mois
  Effort : 1 jour analyste + 1h x 14 employés
  Impact : durcit les 3 cibles privilégiées

PRIORITÉ MOYENNE

R5 - Migration WPA3-SAE
  Action : reconfigurer routeur, recréer PSK
  Délai : 2 mois
  Effort : 1 jour technique
  Impact : robustesse cryptographique accrue

R6 - Audit OSINT trimestriel
  Action : suivi récurrent
  Délai : récurrent
  Effort : 1 jour par trimestre
  Impact : détection précoce nouvelles fuites

PRIORITÉ BASSE

R7 - Politique LinkedIn
  Action : guide employés posts publics
  Délai : 6 mois
  Effort : ½ jour rédaction
  Impact : réduit progressivement la surface
```

## 8. Annexes

Les annexes contiennent tous les éléments factuels permettant de vérifier le rapport.

### 8.1 Annexes recommandées

Voici la liste type des annexes pour un rapport OSINT.

| Annexe | Contenu |
|---|---|
| A - Sources et URLs | Toutes les URLs consultées, datées |
| B - Captures hashées | Tous les screenshots avec hash SHA-256 |
| C - Journal des actions | Log horodaté de toute la mission |
| D - Glossaire | Définitions des termes techniques |
| E - Test de mise en balance RGPD | Document daté |
| F - Liste détaillée des employés | Pseudonymisée |
| G - Graphe Maltego | PDF du graphe complet |
| H - Wardriving | Carte KML et CSV Wigle |

### 8.2 Manifest des annexes

Le manifest agrège tous les hashes pour vérification d'intégrité.

```text
MANIFEST.sha256 - exemple
============================

a1b2c3...  rapport-osint-artech-2026.pdf
d4e5f6...  annexe-A-sources.pdf
g7h8i9...  annexe-B-captures.zip
j0k1l2...  annexe-C-journal.txt
m3n4o5...  annexe-D-glossaire.md
p6q7r8...  annexe-E-mise-en-balance.pdf
s9t0u1...  annexe-F-employes-pseudo.csv
v2w3x4...  annexe-G-maltego-graphe.pdf
y5z6a7...  annexe-H-wardriving.kml
```

## 9. Mise en forme et signature

### 9.1 Format de livrable

Voici les recommandations de format pour le livrable final.

| Aspect | Recommandation |
|---|---|
| Format principal | PDF/A pour archivage |
| Police | Sans serif lisible (Inter, Roboto) |
| Taille | 11pt minimum corps |
| Marges | 2.5 cm minimum |
| Pagination | Pied de page systématique |
| Numérotation | Hiérarchique (1.1.1) |

### 9.2 Signature numérique

Pour les rapports formels, une signature numérique est recommandée.

```bash
# Signature avec OpenSSL (clé privée pré-existante)
openssl dgst -sha256 -sign cle-privee.pem \
    -out rapport-osint-artech.sig \
    rapport-osint-artech.pdf

# Vérification
openssl dgst -sha256 -verify cle-publique.pem \
    -signature rapport-osint-artech.sig \
    rapport-osint-artech.pdf
# Doit afficher : Verified OK
```

### 9.3 Versioning

Pour gérer les versions, voici la convention recommandée.

| Version | Statut |
|---|---|
| 0.1 - 0.9 | Brouillons internes |
| 1.0 | Première version livrée |
| 1.1 - 1.9 | Corrections mineures |
| 2.0 | Évolution majeure |

## 10. Cas pratique - Rédaction ARTECH

### 10.1 Préparation matérielle

Voici la structure de dossier à créer pour le rapport.

```bash
# Préparation
mkdir -p ~/osint/artech-2026/rapport/{annexes,figures,sources}
cd ~/osint/artech-2026/rapport/

# Initialisation
touch rapport.md
touch CHANGELOG.md
touch MANIFEST.sha256

# Structure markdown
cat > rapport.md << 'EOF'
---
title: Audit OSINT défensif - ARTECH SAS
subtitle: Référence OmnyVia-OSINT-2026-001
author: Zyrass / OmnyVia
date: 2026-XX-XX
classification: Confidentiel
---

# I. Synthèse exécutive
[à rédiger]

# II. Cadrage et méthodologie
[à rédiger]

# III. Résultats par catégorie
[à rédiger]

# IV. Cartographie des relations
[à rédiger]

# V. Cibles privilégiées
[à rédiger]

# VI. Surface d'attaque
[à rédiger]

# VII. Recommandations défensives
[à rédiger]

# VIII. Annexes
[à rédiger]
EOF
```

### 10.2 Conversion PDF

Pour convertir le markdown en PDF professionnel, voici la commande type.

```bash
# Avec pandoc
pandoc rapport.md \
    -o rapport-osint-artech-v1.0.pdf \
    --pdf-engine=xelatex \
    --template=eisvogel \
    -V titlepage \
    -V titlepage-color="003366" \
    -V titlepage-text-color="FFFFFF" \
    -V toc=true \
    -V toc-depth=3 \
    -V geometry:margin=2.5cm \
    -V mainfont="Inter" \
    -V monofont="JetBrains Mono"

# Hash final
sha256sum rapport-osint-artech-v1.0.pdf | tee MANIFEST.sha256
```

## 11. Pièges et bonnes pratiques

### 11.1 Pièges fréquents

Voici les erreurs courantes en rédaction de rapport OSINT.

| Piège | Évitement |
|---|---|
| Vocabulaire trop technique | Glossaire systématique |
| Trop d'annexes mêlées au corps | Séparation stricte |
| Absence d'horodatages | Hunchly ou journal manuel |
| Hypothèses non balisées | Échelle de confiance |
| Recommandations vagues | Délai + effort + impact |

### 11.2 Bonnes pratiques

À l'inverse, voici les pratiques qui distinguent un rapport pro.

| Pratique | Bénéfice |
|---|---|
| Synthèse exécutive 1 page | Décideur saisit l'essentiel |
| Hiérarchie visuelle claire | Navigation facile |
| Graphes plutôt que listes | Relations visibles |
| Citations sourcées partout | Vérifiabilité |
| Signature numérique | Intégrité prouvée |

## 12. Auto-évaluation

Vérifiez votre maîtrise par les questions suivantes.

| # | Question | Réponse |
|---|---|---|
| 1 | Longueur max synthèse exécutive ? | 1 page |
| 2 | Échelle de confiance niveaux ? | Confirmé / Probable / Hypothétique / À vérifier |
| 3 | Format archivage recommandé ? | PDF/A |
| 4 | Annexe pour fichiers et hashes ? | Annexe B |
| 5 | Voix grammaticale privilégiée ? | Active |
| 6 | Outil de conversion MD → PDF ? | pandoc + xelatex |
| 7 | Comment garantir l'intégrité ? | Signature numérique + manifest |
| 8 | Hiérarchisation recommandations ? | Critique / Haute / Moyenne / Basse |

## 13. Synthèse

Voici les points clés à retenir.

```text
RAPPORT OSINT STRUCTURÉ

VOCABULAIRE
  Phrases courtes
  Voix active
  Termes neutres
  Confiance balisée

STRUCTURE 9 SECTIONS
  Page de garde
  Synthèse exécutive (1 page)
  Cadrage
  Résultats par catégorie
  Cartographie
  Cibles privilégiées
  Surface d'attaque
  Recommandations
  Annexes

ÉCHELLE DE CONFIANCE
  Confirmé (3+ sources)
  Probable (2 sources)
  Hypothétique (1 source)
  À vérifier

RECOMMANDATIONS
  Critique / Haute / Moyenne / Basse
  Délai + effort + impact

LIVRABLE
  PDF/A pour archivage
  Signature numérique
  Manifest SHA-256
  Versioning sémantique

OUTILS
  Markdown + pandoc
  xelatex + template eisvogel
  OpenSSL pour signature
  Hunchly pour traçabilité
```

---

**Chapitre précédent** : [4.8 Wardriving passif sur le terrain](4-8-wardriving-passif.md)

**Chapitre suivant** : [4.10 Cas pratique ARTECH profilage complet](4-10-cas-pratique-artech.md)
