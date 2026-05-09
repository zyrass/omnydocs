---
title: 7.13 Auto-évaluation et synthèse
description: Bilan complet du module 7 - acquisition mémoire Windows. Récapitulatif des compétences acquises, auto-évaluation globale 30 questions, cas de validation finale, erreurs courantes en mission, préparation du module 7 bis macOS et du module 8 disque.
authors:
  - Zyrass
date:
  created: 2026-04-30
tags:
  - Auto-évaluation
  - Synthèse
  - Module 7
  - Bilan compétences
  - Préparation module suivant
data-level: 🟢
---

# 7.13 Auto-évaluation et synthèse

!!! quote "L'analogie du contrôleur aérien en fin de quart"

    Un contrôleur aérien terminant son quart de huit heures ne quitte pas son poste sans transmission. Il déroule devant son successeur tous les vols en cours, leurs altitudes, leurs caps, les anomalies en surveillance, les communications attendues. Sans cette transmission disciplinée, le successeur démarre aveugle, et un avion peut être oublié dans une fréquence laissée silencieuse. La transition de fin de module joue le même rôle. Vous avez parcouru douze chapitres techniques denses, accumulé des centaines de procédures, manipulé une dizaine d'outils. Sans synthèse explicite, votre cerveau classera certains éléments en "déjà fait, oublié rapidement". Cette consolidation est ce qui transforme la lecture passive en compétence durable. Prenez le temps de cette transmission à vous-même avant d'embarquer sur le module 7 bis.

## Métadonnées du chapitre

Ce chapitre clôt le module 7. Voici ses caractéristiques.

| Champ | Valeur |
|---|---|
| Durée estimée | 3 heures |
| Niveau | Synthèse et validation |
| Prérequis | 7.1 à 7.12 (tous chapitres du module) |
| Livrables | Auto-évaluation complétée, bilan documenté |
| Auto-explication | 10 minutes |

## Objectifs pédagogiques

À l'issue de ce chapitre, vous serez capable de :

- Évaluer votre niveau de maîtrise du module 7
- Identifier vos points faibles à retravailler
- Réaliser un cas de validation complet en autonomie
- Faire le lien avec les modules précédents et suivants
- Préparer votre embarquement sur le module 7 bis macOS
- Présenter votre travail en évaluation tierce

---

## 1. Bilan du module

### 1.1 Volume couvert

Voici le volume couvert par le module 7.

| Indicateur | Valeur |
|---|---|
| Nombre de chapitres | 13 |
| Durée estimée totale | 35 heures |
| Pages de documentation | ~150 |
| Outils manipulés | 6 (Magnet RAM, DumpIt, FTK, Belkasoft, WinPmem, KAPE) |
| Scripts PowerShell développés | 8 |
| Procédures juridiques abordées | 12 |
| Cas pratiques simulés | 4 |

### 1.2 Cartographie des compétences

Voici la cartographie des compétences acquises par chapitre.

| Chapitre | Compétence acquise |
|---|---|
| 7.1 | Théorie volatilité RFC 3227 et hiérarchie de capture |
| 7.2 | Décision allumer/éteindre selon contexte forensique |
| 7.3 | Gestion du chiffrement BitLocker actif |
| 7.4 | Réponse à incident ransomware en cours |
| 7.5 | Préparation et maintenance d'un kit USB DFIR |
| 7.6 | Maîtrise de DumpIt (acquisition simple et rapide) |
| 7.7 | Maîtrise de Magnet RAM Capture (référence 2026) |
| 7.8 | Maîtrise de FTK Imager Lite (polyvalent) |
| 7.9 | Maîtrise de Belkasoft RAM Capturer (backup) |
| 7.10 | Procédure hash SHA-256 et double copie |
| 7.11 | Scellement physique et chaîne de garde |
| 7.12 | Mission complète documentée de bout en bout |
| 7.13 | Synthèse et validation des acquis |

### 1.3 Niveau attendu

Voici le niveau de maîtrise attendu en fin de module.

```text
NIVEAU CIBLE FIN MODULE 7
============================

Connaissance théorique
  RFC 3227 internalisée
  Hiérarchie volatilité réflexe
  Cadre juridique français maîtrisé
  Standards (ISO 27037, NIST SP 800-86) compris

Compétence technique
  Acquisition mémoire en moins de 5 minutes
  Triage live en moins de 10 minutes
  Hash et copie en moins de 15 minutes
  Scellement complet en moins de 20 minutes
  Mission DFIR ARTECH en moins de 4 heures totales

Réflexes professionnels
  Photo systématique avant/après actions
  Documentation horodatée immédiate
  Hash systématique post-acquisition
  Témoin identifié pour scellement
  Chaîne de garde rigoureuse

Posture juridique
  Distinction mandat civil vs judiciaire
  Notifications RGPD respectées
  Articles pénaux mobilisables
  Position recommandée non-paiement
```

## 2. Auto-évaluation globale - 30 questions

### 2.1 Théorie et méthodologie

| # | Question | Réponse type |
|---|---|---|
| 1 | Que signifie l'acronyme RFC 3227 ? | Guidelines for Evidence Collection and Archiving |
| 2 | Premier ordre dans la hiérarchie de volatilité ? | Registres CPU et caches |
| 3 | Pourquoi acquérir la mémoire avant le disque ? | Volatilité supérieure, perte rapide |
| 4 | Standard ISO de référence pour acquisition ? | ISO/IEC 27037:2012 |
| 5 | Différence pull-the-plug vs shutdown ? | Pull = arrêt brutal, conserve disque ; shutdown = altère état |
| 6 | Définition de "immédiat" pour le hash ? | Avant toute manipulation du fichier |

### 2.2 Outils d'acquisition

| # | Question | Réponse type |
|---|---|---|
| 7 | Outil de référence acquisition mémoire 2026 ? | Magnet RAM Capture |
| 8 | Outil le plus léger ? | DumpIt (~500 Ko) |
| 9 | Outil polyvalent mémoire + disque ? | FTK Imager |
| 10 | Outil avec driver kernel léger ? | Belkasoft RAM Capturer |
| 11 | Outil open source recommandé ? | WinPmem |
| 12 | Privilèges requis pour tous ? | Administrateur |

### 2.3 Sécurité et intégrité

| # | Question | Réponse type |
|---|---|---|
| 13 | Algorithme de hash recommandé ? | SHA-256 |
| 14 | Pourquoi pas MD5 ni SHA-1 ? | Cassés cryptographiquement |
| 15 | Combien de copies minimum ? | Original + 1 copie (2 supports) |
| 16 | Format compagnon hash ? | .sha256 compatible sha256sum Linux |
| 17 | Combien d'emplacements pour conservation hash ? | 3 minimum |
| 18 | Validation post-copie ? | Hash copie = hash original strictement |

### 2.4 Procédure juridique

| # | Question | Réponse type |
|---|---|---|
| 19 | Article CPP central pour scellement ? | Article 97 |
| 20 | Article code civil sur preuve électronique ? | Article 1366 |
| 21 | Format identifiant scellé OmnyVia ? | SCL-AAAA-NNN-X |
| 22 | Délai notification CNIL ? | 72 heures (RGPD article 33) |
| 23 | Témoin requis au scellement ? | Oui, identifié avec papiers |
| 24 | Conservation minimum scellé ? | 5 ans recommandés |

### 2.5 Cas pratique

| # | Question | Réponse type |
|---|---|---|
| 25 | Première action arrivée site ransomware ? | Reconnaissance indicateurs (1 minute) |
| 26 | Décision avant acquisition ? | Isolation réseau si propagation possible |
| 27 | Outils premier et second choix ? | Magnet RAM Capture puis DumpIt |
| 28 | Triage live pendant copies ? | Oui, gain de temps |
| 29 | Mode d'arrêt après acquisition ransomware ? | Pull-the-plug |
| 30 | Documentation finale ? | Rapport + scellement + chaîne de garde + photos |

### 2.6 Auto-correction et progression

Voici comment interpréter votre score.

| Score | Niveau | Action |
|---|---|---|
| 28-30 | Maîtrise complète | Passer au module 7 bis |
| 24-27 | Bonne maîtrise | Réviser chapitres faibles avant 7 bis |
| 20-23 | Maîtrise partielle | Refaire les cas pratiques en lab |
| 15-19 | Acquisition fragile | Reprendre intégralement les chapitres faibles |
| Moins de 15 | Module à refaire | Reprendre depuis 7.1 |

## 3. Cas de validation finale

### 3.1 Scénario pratique

Voici le cas pratique de validation finale à réaliser en autonomie.

```text
SCÉNARIO DE VALIDATION
========================

Contexte
  Vous êtes consultant DFIR. Un client (PME industrielle
  fictive) constate une compromission active sur le poste
  de son responsable comptable. Wallpaper ransom note,
  fichiers chiffrés .lock partout, demande 100k USD en BTC.

Configuration cible (à reproduire en lab)
  VM Windows 11 22H2 avec 8 Go RAM
  Hostname : POSTE-COMPTA-LAB
  Utilisateur connecté : compta_lab
  Connexion réseau active vers serveur partage
  Quelques fichiers de test chiffrés (simulation)
  Ransom note sur bureau (simulation)
  
  Note : utiliser la simulation pédagogique du chapitre 7.4
  pour reproduire l'environnement sans danger.

Mission
  1. Documenter votre arrivée sur site (heure UTC)
  2. Effectuer la reconnaissance rapide
  3. Prendre les décisions d'isolation et acquisition
  4. Effectuer l'acquisition mémoire avec hash
  5. Effectuer le triage live
  6. Effectuer la double copie validée
  7. Éteindre proprement la machine
  8. Sceller le disque externe contenant l'acquisition
  9. Remplir formulaire scellement et chaîne de garde
  10. Rédiger un rapport d'acquisition synthétique

Contrainte temps
  4 heures maximum (bonus si réussi en 3h)

Livrables attendus
  - Acquisition raw + log + hash + copies validées
  - Triage CSV (processus, réseau, persistance)
  - Photos horodatées (au minimum 10)
  - Formulaire scellement signé
  - Document chaîne de garde initial
  - Rapport d'acquisition (5 pages minimum)
```

### 3.2 Grille d'évaluation

Voici la grille d'évaluation à utiliser.

| Critère | Poids | Score 0-5 |
|---|---|---|
| Reconnaissance rapide effectuée | 5% | _ |
| Décisions critiques cohérentes | 10% | _ |
| Acquisition mémoire complète | 15% | _ |
| Hash SHA-256 cohérent | 10% | _ |
| Double copie validée | 10% | _ |
| Triage live complet | 10% | _ |
| Photos horodatées suffisantes | 5% | _ |
| Formulaire scellement complet | 10% | _ |
| Chaîne de garde sans rupture | 10% | _ |
| Rapport d'acquisition rigoureux | 15% | _ |
| **Total pondéré** | **100%** | _ |

Score à atteindre : 75/100 minimum pour validation.

### 3.3 Auto-correction

Voici les points fréquents à corriger après le cas pratique.

| Point faible fréquent | Action corrective |
|---|---|
| Hash oublié post-acquisition | Procédure systématique à automatiser |
| Photos sans EXIF horodaté | Vérifier date/heure smartphone |
| Témoin non identifié | Toujours noter identité avec papiers |
| Documentation a posteriori | Carnet horodatage continu |
| Triage incomplet | Checklist détaillée du chapitre 7.4 |
| Format E01 non choisi pour disque | Privilégier formats forensiques |
| Pull-the-plug inapproprié | Distinguer cas selon situation |
| Notification CNIL oubliée | Calendrier 72h dans rapport |

## 4. Erreurs courantes en mission

### 4.1 Erreurs critiques

Voici les erreurs critiques à absolument éviter.

| Erreur | Conséquence | Évitement |
|---|---|---|
| Manipulation du fichier original | Altération preuve | Travail uniquement sur copies |
| Pas de hash de référence | Intégrité non démontrable | Hash systématique post-acquisition |
| Étiquette mal posée | Possibilité contournement | Strict sur jointure |
| Pas de témoin scellement | Preuve contestable | Témoin identifié toujours |
| Documentation en retard | Reconstruction suspecte | Carnet horodatage continu |
| Connexion compte utilisateur | Modification timeline | Travail depuis kit externe |

### 4.2 Erreurs fréquentes mineures

Voici les erreurs fréquentes mais mineures à connaître.

| Erreur | Conséquence | Évitement |
|---|---|---|
| Photo sans échelle | Difficulté évaluation taille | Règle ou pièce de monnaie |
| Disque destination presque plein | Acquisition tronquée | Espace libre vérifié 110% RAM |
| Antivirus quarantaine outil | Acquisition échoue | Whitelist préalable kit |
| Mauvais binaire 32/64 | Échec silencieux | Détection auto architecture |
| Hash sans algorithme spécifié | Confusion | Toujours préciser SHA-256 |
| Format compagnon non standard | Pas vérifiable Linux | sha256sum compatible |

### 4.3 Erreurs juridiques

Voici les erreurs juridiques à éviter.

| Erreur | Risque | Évitement |
|---|---|---|
| Action hors mandat | Acte illégal | Vérifier étendue mandat |
| Notification CNIL tardive | Sanction RGPD | Calendrier 72h actif |
| Divulgation hors cadre | Article 226-13 | Secret pro respecté |
| Pas de plainte si suspicion | Preuve périssable | Conseiller plainte au client |
| Conservation insuffisante | Indisponibilité au procès | 5 ans minimum |

## 5. Connexions inter-modules

### 5.1 Liens avec les modules précédents

Voici comment le module 7 s'appuie sur les précédents.

| Module précédent | Apport au module 7 |
|---|---|
| Module 1 (Législation) | Cadre juridique RGPD, CPP, code civil |
| Module 2 (Prérequis techniques) | Bases Windows, PowerShell, réseau |
| Module 3 (Configuration laboratoire) | Lab ARTECH simulé pour exercices |
| Module 4 (OSINT) | Reconnaissance préalable contexte ARTECH |
| Module 5 (WiFi WPA2) | Vecteur d'entrée potentiel |
| Module 6 (Phishing) | Vecteur d'entrée principal observé |

### 5.2 Liens avec les modules suivants

Voici comment le module 7 prépare les modules suivants.

| Module suivant | Apport du module 7 |
|---|---|
| Module 7 bis (macOS) | Méthodologie applicable, outils différents |
| Module 8 (Disque) | Hash et chaîne de garde identiques |
| Module 9 (Volatility) | Acquisition mémoire = matière première analyse |
| Module 10 (Rapport) | Rapport d'acquisition = base du rapport final |

### 5.3 Position dans la certification RNCP 36399

Voici comment le module 7 contribue à la certification RNCP 36399.

| Bloc de compétences | Apport du module 7 |
|---|---|
| BC01 - Veille et stratégie | Connaissance outils et menaces actuelles |
| BC02 - Conception sécurité | Pas direct mais cadre méthodologique |
| BC03 - Forensic et incident | CŒUR du module - preuve numérique |
| BC04 - Audit et conseil | Méthodologie applicable |

## 6. Préparation modules suivants

### 6.1 Préparation module 7 bis macOS

Le module 7 bis traite de l'acquisition mémoire macOS. Voici la transition.

```text
TRANSITION VERS MODULE 7 BIS MACOS
=====================================

Différences principales à anticiper
  - Architecture Apple Silicon vs x86
  - System Integrity Protection (SIP)
  - FileVault chiffrement disque
  - APFS filesystem
  - Outils différents (OSXPmem, Volexity Surge, AVML)

Continuités méthodologiques
  - RFC 3227 toujours applicable
  - Hash SHA-256 toujours requis
  - Double copie toujours obligatoire
  - Scellement et chaîne de garde identiques
  - Cadre juridique français inchangé

Prérequis techniques
  - Disposer d'un Mac de test (Apple Silicon recommandé)
  - Installer outils macOS forensique
  - Comprendre architecture XNU/Darwin
```

### 6.2 Préparation module 8 acquisition disque

Le module 8 abordera l'acquisition de disque (suite logique).

```text
TRANSITION VERS MODULE 8 DISQUE
==================================

Différences à anticiper
  - Volume bien plus important (To vs Go)
  - Durées d'acquisition longues (heures)
  - Write-blocker hardware nécessaire
  - Formats E01/EWF dominants
  - SSD avec TRIM problématique
  - RAID éventuel

Continuités méthodologiques
  - Tous les principes du module 7 s'appliquent
  - Outil FTK Imager Lite déjà connu
  - Hash SHA-256 et double copie identiques
  - Scellement et chaîne de garde identiques

Prérequis matériels
  - Write-blocker hardware (USB, SATA)
  - Disques destination très volumineux
  - Adaptateurs (SATA-USB, NVMe-USB)
  - Boîtiers protections
```

### 6.3 Préparation module 9 Volatility

Le module 9 sera l'analyse approfondie de la mémoire acquise.

```text
TRANSITION VERS MODULE 9 VOLATILITY
======================================

Ce que le module 9 fera
  Exploiter les dumps mémoire acquis au module 7
  
  Plugins essentiels
    windows.info     : informations système
    windows.pslist   : liste processus
    windows.cmdline  : lignes de commande
    windows.netscan  : connexions réseau
    windows.malfind  : détection injection
    windows.hashdump : extraction hashes mots de passe
    windows.cmdscan  : historique cmd
    windows.filescan : fichiers en mémoire

Préparation
  - Avoir Volatility 3 installé sur poste analyste
  - Disposer de dumps de test (issus du module 7)
  - Comprendre concepts basiques (PID, PPID, etc.)
```

## 7. Ressources et références

### 7.1 Sources officielles

Voici les sources officielles à consulter régulièrement.

| Source | URL | Type |
|---|---|---|
| ANSSI guides DFIR | ssi.gouv.fr | Officiel France |
| CERT-FR | cert.ssi.gouv.fr | Alertes France |
| NIST SP 800-86 | nist.gov | Standard international |
| ENISA | enisa.europa.eu | Standard européen |
| ISO 27037 | iso.org | Standard ISO (payant) |
| RFC 3227 | ietf.org/rfc/rfc3227 | Standard libre |

### 7.2 Communautés et formations

Voici les communautés et formations utiles.

| Ressource | Type |
|---|---|
| SANS DFIR | Formations payantes haut niveau |
| GIAC GCFE/GCFA | Certifications forensiques |
| HackingBox podcast | Communauté FR |
| Twitter/X #DFIR | Veille communautaire |
| CFI France | Communauté forensique |
| Volatility user group | Liste mailing |

### 7.3 Outils complémentaires

Voici les outils complémentaires à connaître au-delà du module.

| Outil | Usage |
|---|---|
| Autopsy | Analyse forensique disque |
| KAPE | Triage automatisé |
| Velociraptor | DFIR distribué |
| Eric Zimmerman tools | Suite forensique gratuite |
| Plaso | Timeline analysis |
| MISP | Threat intelligence |

### 7.4 Bibliographie OmnyAcademy

Pour approfondir, voici la bibliographie de référence.

```text
BIBLIOGRAPHIE OmnyAcademy MODULE 7
======================================

Ouvrages fondamentaux
  - "The Art of Memory Forensics" - Hale Ligh, Case, Levy, Walters
  - "Practical Memory Forensics" - Svetlana Ostrovskaya, Oleg Skulkin
  - "Windows Internals" 7th edition - Russinovich, Solomon, Ionescu

Articles et papers
  - Volatility Framework documentation
  - Magnet Forensics white papers
  - SANS DFIR posters et cheat sheets
  - ANSSI guides DFIR (français)

Vidéos formation
  - SANS DFIR YouTube channel
  - 13Cubed (memory forensics)
  - DFIR.training portal

Pour la dimension juridique française
  - "Cybersécurité et droit" - Aldo Schiavone
  - Code de procédure pénale (édition Dalloz)
  - Guide CNIL pour les notifications de violations
```

## 8. Checklist personnelle

### 8.1 Compétences à valider

Voici la checklist personnelle des compétences à valider en fin de module.

```text
CHECKLIST FIN MODULE 7
========================

Théorie
  [ ] RFC 3227 expliquée à un tiers
  [ ] Hiérarchie volatilité réflexe
  [ ] Cadre juridique français maîtrisé
  [ ] Standards ISO 27037 / NIST SP 800-86 compris

Pratique
  [ ] Acquisition Magnet RAM Capture en moins 5 min
  [ ] Acquisition DumpIt en moins 3 min
  [ ] Acquisition FTK Imager mémoire + pagefile OK
  [ ] Acquisition Belkasoft fonctionnelle
  [ ] Hash SHA-256 systématique
  [ ] Double copie validée
  [ ] Triage live en moins 10 min
  [ ] Mission complète ARTECH en moins 4h

Procédure
  [ ] Photographies pré et post systématiques
  [ ] Formulaire scellement complété sans erreur
  [ ] Chaîne de garde rigoureuse
  [ ] Hash conservés trois emplacements
  [ ] Témoin identifié au scellement

Connaissance kit
  [ ] Kit USB préparé et testé
  [ ] MANIFEST.sha256 cohérent
  [ ] Procédures plastifiées disponibles
  [ ] Formulaires vierges en stock
  [ ] Test mensuel programmé

Conformité
  [ ] CPP article 97 cité de mémoire
  [ ] RGPD article 33 (72h) intégré
  [ ] Articles pénaux 323-1+ connus
  [ ] Position non-paiement comprise
```

### 8.2 Validation par les pairs

Voici une grille pour validation par un pair.

```text
VALIDATION PAR PAIR DFIR
===========================

Évaluateur
  Nom : ___________________
  Fonction : ___________________
  Date : ___________________

Critères évalués
  Maîtrise théorique
    [ ] Excellent / Bon / À améliorer
  
  Maîtrise pratique outils
    [ ] Excellent / Bon / À améliorer
  
  Rigueur méthodologique
    [ ] Excellent / Bon / À améliorer
  
  Documentation produite
    [ ] Excellent / Bon / À améliorer
  
  Posture juridique
    [ ] Excellent / Bon / À améliorer

Recommandations
  ____________________________________
  ____________________________________

Signature évaluateur : ___________________
```

## 9. Synthèse finale du module 7

### 9.1 Ce que vous savez maintenant faire

Voici la synthèse de ce que vous maîtrisez en fin de module.

```text
COMPÉTENCES OPÉRATIONNELLES MODULE 7
========================================

Phase 1 - Préparation
  Construire un kit USB DFIR complet
  Maintenir le kit à jour
  Tester régulièrement les outils
  Documenter les versions

Phase 2 - Réponse à incident
  Identifier en 1 minute un ransomware actif
  Décider isolation et acquisition prioritaire
  Photographier la scène systématiquement

Phase 3 - Acquisition
  Choisir l'outil approprié au contexte
  Acquérir la mémoire en moins de 5 minutes
  Effectuer le triage live en parallèle
  Calculer le hash de référence immédiatement

Phase 4 - Préservation
  Effectuer la double copie validée
  Sceller physiquement avec témoin
  Documenter la chaîne de garde
  Stocker en lieu sécurisé

Phase 5 - Documentation
  Rédiger un rapport d'acquisition rigoureux
  Préparer notification CNIL si nécessaire
  Conseiller le client sur suite à donner
  Préparer la transmission éventuelle au juge
```

### 9.2 Position d'OmnyAcademy

Voici la position pédagogique d'OmnyAcademy à la fin du module 7.

```text
POSITION OmnyAcademy POST-MODULE 7
======================================

Vous êtes désormais opérationnel pour
  - Mener une mission DFIR sur poste Windows
  - Produire de la preuve numérique recevable
  - Documenter selon standards internationaux
  - Conseiller un client en posture juridique

Vous pouvez vous présenter comme
  - Capable de répondre à un incident ransomware
  - Maîtrisant les outils standard du marché
  - Rigoureux sur la chaîne de garde
  - À jour sur les standards 2026

Vous n'êtes PAS encore
  - Expert en analyse Volatility approfondie (module 9)
  - Spécialiste acquisition disque massif (module 8)
  - Pratiquant macOS DFIR (module 7 bis)
  - Maître du rapport judiciaire complet (module 10)

Suite recommandée
  Module 7 bis : étendre aux écosystèmes Apple
  Module 8 : maîtriser l'acquisition disque
  Module 9 : exploiter les dumps mémoire
  Module 10 : rédaction rapport finalisé
```

### 9.3 Mot de la fin

Le module 7 est l'un des plus denses du parcours OmnyAcademy. Il représente la fondation pratique de toute la formation DFIR. Sans maîtrise rigoureuse des principes posés dans ces 13 chapitres, les modules suivants seront fragiles. Avec cette maîtrise, vous disposez d'une base solide pour approfondir indéfiniment.

La forensique numérique est un métier exigeant. La rigueur n'est pas optionnelle. La documentation n'est pas un détail. La chaîne de garde n'est pas une formalité. Chaque manquement à ces principes peut transformer une preuve solide en simple élément contestable. Votre client compte sur vous pour faire les choses dans les règles, depuis la première minute jusqu'à la dernière.

Quand vous terminerez votre première vraie mission DFIR, vous comprendrez pourquoi nous avons consacré 35 heures à ce seul module. Bonne suite avec le module 7 bis macOS.

---

**Chapitre précédent** : [7.12 Documentation acquisition cas réel](7-12-documentation-cas-reel.md)

**Module suivant** : [Module 7 bis - Acquisition mémoire macOS](../module-7bis-acquisition-memoire-macos/README.md)