---
title: 5.10 Documentation de la phase d'intrusion
description: Documentation forensique de la phase d'intrusion offensive - chronologie des actions, mapping MITRE ATT&CK, preservation des preuves, traçabilité, livrable rapport offensif. Synthèse du module 5.
authors:
  - Zyrass
date:
  created: 2026-04-30
tags:
  - Documentation
  - MITRE ATT&CK
  - Rapport offensif
  - Forensic
data-level: 🟡
---

# 5.10 Documentation de la phase d'intrusion

!!! quote "L'analogie du chirurgien qui tient son journal opératoire"

    Un chirurgien expérimenté ne se contente pas de réaliser une opération brillante. Il tient un journal détaillé, minute par minute : heure d'incision, instruments utilisés, observations anatomiques, complications, décisions, fermeture. Ce journal sert ensuite à trois usages. À la responsabilité s'il y a litige. À l'enseignement aux internes qui apprendront. À l'amélioration continue de sa pratique. Pour un pentester éthique, le rapport offensif joue exactement ces trois rôles. Il documente la responsabilité du mandat, il instruit l'équipe défensive, il améliore la pratique professionnelle. Sans rapport, l'attaque même réussie ne sert à rien. Avec un rapport médiocre, son impact se dilue. Avec un rapport excellent, l'attaque devient le levier de transformation de la sécurité d'ARTECH.

## Métadonnées du chapitre

Ce chapitre clôt le module 5 par la synthèse documentaire. Voici ses caractéristiques.

| Champ | Valeur |
|---|---|
| Durée estimée | 4 heures |
| Niveau | Synthèse |
| Prérequis | 5.1 à 5.9 maîtrisés |
| Livrables | Rapport offensif phase WiFi+intrusion |
| Auto-explication | 12 minutes |

## Objectifs pédagogiques

À l'issue de ce chapitre, vous serez capable de :

- Structurer un rapport offensif professionnel
- Mapper les actions sur MITRE ATT&CK
- Construire une chronologie horodatée
- Préserver les preuves forensiquement
- Lier l'offensive aux recommandations défensives
- Préparer le passage au module 6 (phishing)

---

## 1. Pourquoi documenter chaque action

### 1.1 Trois finalités du rapport offensif

Voici les trois usages qui justifient l'effort de documentation.

| Finalité | Bénéficiaire | Contenu type |
|---|---|---|
| Responsabilité juridique | Vous, le client | Périmètre, mandat, traçabilité |
| Transformation défensive | Équipe sécurité client | Recommandations actionnables |
| Amélioration continue | Vous, la profession | Lessons learned |

### 1.2 Conséquences d'une mauvaise documentation

Voici les risques d'une documentation médiocre.

| Risque | Conséquence |
|---|---|
| Pas de mandat documenté | Risque pénal (323-1) |
| Pas d'horodatage | Impossible de prouver chronologie |
| Pas de hash sur preuves | Pas de valeur forensique |
| Recommandations vagues | Client ne peut pas agir |
| Manque de pédagogie | Équipe sécu n'apprend pas |

### 1.3 Standard professionnel

Voici les standards de référence pour la documentation offensive.

| Standard | Source |
|---|---|
| OWASP Testing Guide | OWASP |
| PTES (Penetration Testing Execution Standard) | ptes.org |
| OSSTMM | ISECOM |
| NIST SP 800-115 | NIST |
| Code de conduite OSCP | Offensive Security |

OmnyAcademy s'inspire principalement du **PTES** pour la structure.

## 2. Structure d'un rapport offensif

### 2.1 Architecture en 8 sections

Voici la structure recommandée pour un rapport offensif pentest.

```text
RAPPORT OFFENSIF - STRUCTURE TYPE
====================================

I.    Page de garde
II.   Synthèse exécutive (1-2 pages)
III.  Cadrage et mandat
IV.   Méthodologie
V.    Chronologie des actions
VI.   Résultats par phase
VII.  Recommandations défensives priorisées
VIII. Annexes
       - Annexe A : preuves hashées
       - Annexe B : journal complet horodaté
       - Annexe C : mapping MITRE ATT&CK
       - Annexe D : CVE et références
       - Annexe E : scripts utilisés
```

### 2.2 Différences avec rapport OSINT

Voici les différences avec le rapport OSINT du module 4.

| Aspect | Rapport OSINT | Rapport offensif |
|---|---|---|
| Périmètre | Reconnaissance externe | Intrusion active |
| Risque juridique | Faible (sources publiques) | Élevé (323-1) |
| Mandat requis | Recommandé | Indispensable |
| Cibles humaines | Profilage | Évité, focus systèmes |
| Conservation | 6 mois | 6 mois min, contractuel |
| Livrable type | PDF + annexes | PDF + annexes + scripts |

## 3. Chronologie horodatée

La chronologie est le **squelette** du rapport. Sans elle, rien ne tient.

### 3.1 Format ISO 8601 UTC

Tous les horodatages doivent être en **UTC ISO 8601** pour éviter les ambiguïtés.

```text
FORMAT REQUIS
================

YYYY-MM-DDTHH:MM:SSZ

Exemple : 2026-04-30T14:32:15Z

Le Z final indique UTC.
Pas de timezone locale (CEST, CET) qui change.
```

### 3.2 Timeline ARTECH type

Voici une timeline type pour les modules 4 et 5.

```text
TIMELINE OFFENSIVE - ARTECH 2026
====================================

PHASE 1 - OSINT (Module 4)
2026-04-25T08:00:00Z  Cadrage juridique
2026-04-25T09:30:00Z  Pappers + BODACC
2026-04-25T14:00:00Z  theHarvester énumération
2026-04-26T09:00:00Z  Profilage 3 cibles LinkedIn
2026-04-26T15:00:00Z  Maltego cartographie
2026-04-27T10:00:00Z  Wardriving Kismet
2026-04-27T15:30:00Z  Audit fuites HIBP
2026-04-29T09:00:00Z  Rédaction rapport OSINT
2026-04-29T16:00:00Z  Livraison rapport OSINT

PHASE 2 - WI-FI (Module 5)
2026-04-30T09:15:23Z  Préparation Alfa AWUS036ACS
2026-04-30T09:30:45Z  airodump-ng scan général
2026-04-30T09:45:12Z  Identification ARTECH-WIFI BSSID 64:70:02:XX:XX:XX canal 6
2026-04-30T10:00:00Z  Capture ciblée airodump-ng démarrée
2026-04-30T10:15:34Z  Identification client connecté MAC AA:BB:CC:DD:EE:FF
2026-04-30T10:16:08Z  aireplay-ng deauth 5 paquets ciblée
2026-04-30T10:16:55Z  4-way handshake capturé (47 secondes)
2026-04-30T10:18:12Z  Validation aircrack-ng OK
2026-04-30T10:19:33Z  Conversion 22000 hcxpcapngtool
2026-04-30T10:25:00Z  Construction dictionnaire ARTECH
2026-04-30T10:45:30Z  Lancement hashcat mode 22000
2026-04-30T10:46:18Z  PSK CRACKÉ : ArtechMedical2020!
2026-04-30T11:00:00Z  Connexion ARTECH-WIFI IP 192.168.50.99
2026-04-30T11:05:00Z  Reconnaissance ARP passive
2026-04-30T11:30:00Z  arp-scan complet
2026-04-30T11:45:00Z  Cartographie LAN identifiée
2026-04-30T12:00:00Z  Scan nmap phase 1-2-3
2026-04-30T13:00:00Z  Scripts NSE ciblés
2026-04-30T14:30:00Z  Synthèse résultats
```

### 3.3 Outils d'horodatage automatisé

Pour automatiser, plusieurs approches.

```bash
# Création d'un alias bash pour journalisation
alias logp='echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - " >> ~/pentest/artech-2026/journal.md'

# Usage
logp "Préparation Alfa AWUS036ACS"
# Ajoute : 2026-04-30T14:32:15Z - Préparation Alfa AWUS036ACS

# Script shell complet
cat >> ~/.bashrc << 'EOF'
function logp() {
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - $*" >> $LOG_FILE
}
export LOG_FILE=~/pentest/journal.md
EOF
```

### 3.4 Hunchly pour traçabilité web

Comme vu en module 4, **Hunchly** capture automatiquement chaque page consultée. Étendez son usage à la phase offensive.

## 4. Mapping MITRE ATT&CK

Le **MITRE ATT&CK** est le framework de référence pour catégoriser les techniques d'attaque.

### 4.1 Présentation MITRE ATT&CK

Voici les caractéristiques du framework.

| Caractéristique | Valeur |
|---|---|
| Source | MITRE Corporation |
| URL | attack.mitre.org |
| Tactiques | 14 (Reconnaissance → Impact) |
| Techniques | 200+ |
| Sub-techniques | 400+ |
| Mise à jour | Trimestrielle |

### 4.2 Tactiques principales

Voici les 14 tactiques de la matrice Enterprise.

| Tactique | Code | Phase |
|---|---|---|
| Reconnaissance | TA0043 | Pré-attaque |
| Resource Development | TA0042 | Pré-attaque |
| Initial Access | TA0001 | Entrée |
| Execution | TA0002 | Exécution |
| Persistence | TA0003 | Maintien |
| Privilege Escalation | TA0004 | Élévation |
| Defense Evasion | TA0005 | Évasion |
| Credential Access | TA0006 | Vol creds |
| Discovery | TA0007 | Reconnaissance interne |
| Lateral Movement | TA0008 | Latéral |
| Collection | TA0009 | Collecte data |
| Command and Control | TA0011 | C2 |
| Exfiltration | TA0010 | Sortie data |
| Impact | TA0040 | Effet final |

### 4.3 Mapping des actions module 4 et 5

Voici comment mapper vos actions sur MITRE ATT&CK.

| Action | Tactique | Technique |
|---|---|---|
| Pappers/BODACC | Reconnaissance | T1589.002 (Email Address) |
| theHarvester | Reconnaissance | T1589 (Gather Victim Identity) |
| Profilage LinkedIn | Reconnaissance | T1589.003 (Employee Names) |
| Wardriving Kismet | Reconnaissance | T1592.002 (Network Information) |
| Wigle search | Reconnaissance | T1593 (Search Open Tech DB) |
| Capture handshake WPA2 | Credential Access | T1040 (Network Sniffing) |
| Cracking hashcat | Credential Access | T1110.002 (Password Cracking) |
| Connexion réseau cracké | Initial Access | T1078 (Valid Accounts) |
| arp-scan | Discovery | T1018 (Remote System Discovery) |
| nmap services | Discovery | T1046 (Network Service Scanning) |
| Scripts NSE | Discovery | T1083 (File and Directory Discovery) |
| OS detection | Discovery | T1082 (System Information Discovery) |

### 4.4 Tableau MITRE complet ARTECH

Voici la synthèse formatée pour le rapport.

```text
MAPPING MITRE ATT&CK - PHASE WIFI+INTRUSION
===============================================

| Phase | Action | Tactique | Technique ID |
|-------|--------|----------|--------------|
| OSINT | Recensement entreprise | TA0043 Reconnaissance | T1589.002 |
| OSINT | Énumération emails | TA0043 Reconnaissance | T1589 |
| OSINT | Profilage LinkedIn | TA0043 Reconnaissance | T1589.003 |
| OSINT | Wardriving Wi-Fi | TA0043 Reconnaissance | T1592.002 |
| WiFi  | Capture handshake | TA0006 Credential Access | T1040 |
| WiFi  | Cracking offline | TA0006 Credential Access | T1110.002 |
| LAN   | Connexion Wi-Fi | TA0001 Initial Access | T1078 |
| LAN   | ARP scan | TA0007 Discovery | T1018 |
| LAN   | Port scan | TA0007 Discovery | T1046 |
| LAN   | Service enum | TA0007 Discovery | T1046 |
| LAN   | OS fingerprint | TA0007 Discovery | T1082 |
```

## 5. Préservation des preuves

### 5.1 Hashes des artefacts

Chaque artefact (capture, dump, screenshot) doit être **hashé** pour intégrité.

```bash
# Génération hash SHA-256
sha256sum *.cap *.pcap *.txt *.png > MANIFEST.sha256

# Format type
# a1b2c3d4...  artech-handshake-01.cap
# e5f6g7h8...  artech-pmkid.pcapng
# ...

# Validation ultérieure
sha256sum -c MANIFEST.sha256
```

### 5.2 Signature numérique du manifest

Pour l'intégrité légale, signez le manifest.

```bash
# Avec GPG (clé pré-existante)
gpg --output MANIFEST.sha256.sig --detach-sign MANIFEST.sha256

# Vérification
gpg --verify MANIFEST.sha256.sig MANIFEST.sha256
```

### 5.3 Conservation type

Voici la politique recommandée pour la conservation.

| Élément | Durée | Action fin |
|---|---|---|
| Captures PCAP | 6 mois | Suppression sécurisée |
| PSK cracké | Mission active | Effacement immédiat post-rapport |
| Logs nmap | 6 mois | Suppression |
| Screenshots | 6 mois | Anonymisation |
| Rapport final | 5 ans | Archivage chiffré |

### 5.4 Chiffrement des artefacts

Pendant la mission, chiffrez votre dossier de travail.

```bash
# Création conteneur chiffré
mkdir -p ~/pentest-encrypted
cryptsetup luksFormat ~/pentest-encrypted.img
cryptsetup open ~/pentest-encrypted.img pentest

# Mount
sudo mkfs.ext4 /dev/mapper/pentest
sudo mount /dev/mapper/pentest /mnt/pentest

# Travail dans /mnt/pentest
# À la fin :
sudo umount /mnt/pentest
cryptsetup close pentest
```

## 6. Rédaction des recommandations

Pour chaque vulnérabilité exploitée, formulez une recommandation **actionnable**.

### 6.1 Format CIA + actions

Voici la structure type d'une recommandation.

```text
RECOMMANDATION TYPE
=====================

TITRE : Migration WPA2-PSK vers WPA3-SAE

PRIORITÉ : Haute

VULNÉRABILITÉ EXPLOITÉE
  Description courte de la faille technique.
  Référence dans le rapport (section X.Y).
  CVE applicable si pertinent.

IMPACT CIA
  Confidentialité : élevé (PSK cracké)
  Intégrité : moyen (modification trafic possible)
  Disponibilité : faible

CHAMPIONS
  DSI ARTECH : décision technique
  Fournisseur réseau : implémentation

ACTIONS CONCRÈTES
  1. Vérifier compatibilité tous devices avec WPA3
  2. Migration progressive sur 1 mois
  3. Tester WPA3-SAE en mixed mode 1 semaine
  4. Bascule full WPA3 après validation
  5. Désactivation WPA2 legacy

DÉLAI : 2 mois
EFFORT : 2 jours technique + accompagnement
COÛT : Néant si routeur compatible WPA3

VALIDATION DE L'EFFICACITÉ
  Test : tentative cracking handshake post-migration
  Critère : impossibilité de cracking offline
  Méthode : reproduire la procédure du rapport

RISQUE RÉSIDUEL
  Vulnérabilité Dragonblood (2019) sur WPA3 ancien
  Mitigation : firmware à jour
```

### 6.2 Hiérarchisation pour ARTECH

Voici la hiérarchisation recommandée pour ARTECH après modules 4 et 5.

| Priorité | Recommandation | Effort |
|---|---|---|
| Critique | Reset PSK Wi-Fi avec 20+ caractères aléatoires | 1 heure |
| Haute | Migration WPA3-SAE | 2 jours |
| Haute | Activation 802.11w (PMF) en mode required | 1 heure |
| Moyenne | Réduction puissance émission Wi-Fi | 30 min |
| Moyenne | Renommage SSID neutre | 30 min |
| Moyenne | IDS Wi-Fi (Suricata règles deauth) | 1 jour |
| Basse | Audit Wigle trimestriel | Récurrent |
| Basse | Sensibilisation équipe | 1 jour formation |

## 7. Synthèse exécutive

La synthèse exécutive est le **document le plus lu** de votre rapport.

### 7.1 Cibles de la synthèse

Voici à qui s'adresse la synthèse exécutive.

| Audience | Attente |
|---|---|
| PDG / DG | Coût et risque global |
| DSI | Chemin d'attaque général |
| RSSI | Vulnérabilités à traiter |
| Comité direction | Vision stratégique |

### 7.2 Structure type

La synthèse exécutive doit tenir en **1 à 2 pages maximum**. Voici sa structure.

```text
SYNTHÈSE EXÉCUTIVE - ARTECH 2026
====================================

CONTEXTE
  Mandat OmnyVia-PENTEST-2026-001 du AAAA-MM-JJ
  Périmètre : Wi-Fi et LAN ARTECH
  Durée d'audit : 5 jours ouvrés

CHEMIN D'ATTAQUE RÉALISÉ
  1. OSINT a identifié 3 cibles humaines et le SSID Wi-Fi
  2. Capture du 4-way handshake WPA2 en 47 secondes
  3. Cracking offline du PSK en moins d'une minute
  4. Connexion au LAN ARTECH avec PSK obtenu
  5. Cartographie complète du LAN en 30 minutes
  6. Identification des cibles internes prioritaires

CONCLUSION GLOBALE
  La sécurité Wi-Fi d'ARTECH présente une faille
  exploitable en moins de 2 heures par un attaquant
  modérément équipé. Une fois sur le LAN, l'absence
  de segmentation et de monitoring permet une
  reconnaissance complète sans détection.

NIVEAU DE RISQUE
  CRITIQUE pour le périmètre Wi-Fi
  ÉLEVÉ pour le périmètre LAN

5 RECOMMANDATIONS PRIORITAIRES
  1. Reset immédiat du PSK Wi-Fi (1 heure)
  2. Migration WPA3-SAE (2 jours)
  3. Segmentation LAN par VLAN (1 semaine)
  4. Déploiement IDS Wi-Fi (1 semaine)
  5. Audit trimestriel récurrent

INVESTISSEMENT GLOBAL ESTIMÉ
  Effort interne : ~10 jours
  Budget équipement : 2 000 €
  Bénéfice : élimination du chemin d'attaque exploré
```

### 7.3 Tonalité

La synthèse exécutive doit être :

| Critère | Application |
|---|---|
| Factuelle | Pas de superlatifs |
| Neutre | Pas de termes accusatoires |
| Actionnable | Recommandations chiffrées |
| Compréhensible | Pas de jargon technique excessif |
| Honnête | Pas de minimisation, pas d'alarmisme |

## 8. Reproduction et validation

Le rapport doit permettre la **reproduction** de chaque vulnérabilité par l'équipe défensive.

### 8.1 Procédure de reproduction

Pour chaque vulnérabilité, fournissez la procédure exacte.

```text
PROCÉDURE DE REPRODUCTION - PSK CRACKING
==========================================

PRÉREQUIS
  - Carte Wi-Fi compatible mode monitor
  - aircrack-ng suite installée
  - hashcat ou aircrack-ng
  - Un dictionnaire de test

ÉTAPES

1. Mettre la carte en mode monitor
   sudo airmon-ng start wlan1

2. Lancer la capture sur ARTECH-WIFI canal 6
   sudo airodump-ng --bssid <BSSID> --channel 6 -w test wlan1mon

3. Identifier un client connecté
   (visible dans la zone STATION de airodump)

4. Forcer la déauth pour capture handshake
   sudo aireplay-ng --deauth 5 -a <BSSID> -c <CLIENT> wlan1mon

5. Vérifier la mention "WPA handshake" dans airodump

6. Tester le cracking
   hashcat -m 22000 test-01.cap dico.txt

7. Si PSK trouvé : la vulnérabilité existe
   Si pas trouvé : durcissement déjà appliqué

CRITÈRE DE PASSAGE
  PSK révélé = vulnérabilité non corrigée
  PSK non révélé après dictionnaires standards
    + 100M candidats = vulnérabilité corrigée
```

### 8.2 Test de validation post-correction

L'équipe défensive doit pouvoir **tester** que la correction est efficace.

```text
TEST POST-CORRECTION
======================

POUR PSK ROBUSTE
  Reproduire la procédure ci-dessus
  Avec rockyou + dive.rule (~ 100M candidats)
  Si non trouvé en 24h : OK

POUR WPA3-SAE
  Tenter le même chemin d'attaque
  Vérifier que :
    - Pas de 4-way handshake observé
    - Capture PMKID non utilisable
    - SAE échange visible

POUR PMF ACTIF
  Tenter aireplay-ng --deauth
  Vérifier que les clients ne se déconnectent pas
  Confirmer dans airodump-ng les paquets ne sont pas acceptés
```

## 9. Cas pratique - Rapport ARTECH module 5

### 9.1 Création du rapport

Voici la structure de fichier à créer.

```bash
# Préparation
mkdir -p ~/pentest/artech-2026/rapport-offensif/{annexes,figures,scripts}
cd ~/pentest/artech-2026/rapport-offensif/

# Initialisation rapport
cat > rapport.md << 'EOF'
---
title: Rapport Offensif - ARTECH Wi-Fi et LAN
subtitle: Référence OmnyVia-PENTEST-2026-001
author: Zyrass / OmnyVia
date: 2026-XX-XX
classification: Confidentiel
---

# I. Synthèse exécutive

[Contenu chapitre 5.10 section 7]

# II. Cadrage et mandat

[Référence mandat, périmètre, dates]

# III. Méthodologie

Cette mission a suivi la méthodologie OmnyAcademy
inspirée du PTES (Penetration Testing Execution
Standard).

# IV. Chronologie horodatée

[Timeline ARTECH section 3.2]

# V. Résultats par phase

## V.1 OSINT (résumé du rapport module 4)
## V.2 Capture handshake Wi-Fi
## V.3 Cracking PSK
## V.4 Connexion LAN
## V.5 Reconnaissance interne

# VI. Recommandations défensives

## VI.1 Critique
## VI.2 Haute
## VI.3 Moyenne
## VI.4 Basse

# VII. Tableau MITRE ATT&CK

[Tableau section 4.4]

# VIII. Annexes
EOF
```

### 9.2 Annexes type

Voici les annexes à inclure.

| Annexe | Contenu | Format |
|---|---|---|
| A | Manifest hashes SHA-256 | TXT signé |
| B | Journal horodaté complet | MD + PDF |
| C | Mapping MITRE ATT&CK | CSV |
| D | Captures PCAP | Archive chiffrée |
| E | Scripts utilisés | Archive |
| F | Synthèse OSINT (extrait module 4) | PDF |
| G | Cartographie LAN | PNG/SVG |
| H | Rapport nmap (XML) | XML |

### 9.3 Conversion PDF

```bash
# Conversion avec pandoc
pandoc rapport.md \
    -o rapport-offensif-artech-v1.0.pdf \
    --pdf-engine=xelatex \
    --template=eisvogel \
    -V titlepage \
    -V titlepage-color="800000" \
    -V titlepage-text-color="FFFFFF" \
    -V toc=true \
    -V toc-depth=3

# Signature
gpg --output rapport-offensif-artech-v1.0.pdf.sig \
    --detach-sign rapport-offensif-artech-v1.0.pdf

# Manifest final
sha256sum rapport-offensif-artech-v1.0.pdf > MANIFEST-FINAL.sha256
```

## 10. Considérations RGPD du rapport offensif

### 10.1 Données personnelles dans le rapport

Le rapport peut contenir des données personnelles (employés cibles).

| Donnée | Traitement |
|---|---|
| Noms des cibles | Pseudonymisation dans rapport public |
| Emails | Anonymisation dans annexe diffusable |
| Photos extraites | À supprimer du livrable |
| Captures forensiques | Chiffrement du conteneur |

### 10.2 Test de mise en balance

Pour le rapport offensif, refaites le **test de mise en balance** RGPD vu en module 4.

```text
TEST MISE EN BALANCE - PHASE OFFENSIVE
=========================================

Purpose Test
  Audit défensif mandaté par PDG ARTECH.
  Légitime.

Necessity Test
  Le scan offensif est nécessaire pour valider
  la posture sécurité, ce qui ne peut être fait
  par audit documentaire seul.

Balancing Test
  Droits affectés des employés :
    - Vie privée (capture handshake leur device)
    - Confidentialité communications (capture trafic)
  
  Mesures compensatoires :
    - Mandat écrit explicite
    - Période courte
    - Aucune exfiltration de données
    - Capture limitée handshake (pas trafic data)
    - Anonymisation rapport
    - Conservation 6 mois max

  Conclusion : intérêt légitime prévaut, sous
  réserve des mesures compensatoires.

Document signé Zyrass, daté du AAAA-MM-JJ.
```

## 11. Auto-évaluation

Vérifiez votre maîtrise par les questions suivantes.

| # | Question | Réponse |
|---|---|---|
| 1 | Standard de référence pentest ? | PTES |
| 2 | Format horodatage requis ? | ISO 8601 UTC |
| 3 | Framework de mapping techniques ? | MITRE ATT&CK |
| 4 | Tactique pour cracking de PSK ? | Credential Access (TA0006) |
| 5 | Tactique pour scan nmap ? | Discovery (TA0007) |
| 6 | Algorithme de hash recommandé ? | SHA-256 |
| 7 | Outil de signature numérique ? | GPG |
| 8 | Longueur synthèse exécutive ? | 1 à 2 pages |

## 12. Synthèse du module 5

Au terme du module 5, voici ce que vous avez acquis.

```text
MODULE 5 - SYNTHÈSE GLOBALE

ACQUIS THÉORIQUES
  Cryptographie WPA2 (PMK, PTK, GTK, PBKDF2)
  4-way handshake détaillé
  Vulnérabilité capture passive + cracking offline
  PMKID attack
  Différences WPA2 vs WPA3-SAE

ACQUIS PRATIQUES
  Mode monitor et injection (airmon-ng)
  Capture handshake (airodump-ng)
  Deauth ciblée (aireplay-ng)
  Conversion 22000 (hcxpcapngtool)
  Construction dictionnaires français
  Cracking GPU (hashcat)
  Cracking CPU (aircrack-ng)
  Connexion réseau (wpa_supplicant)
  Reconnaissance ARP/DHCP/mDNS
  Scan nmap et scripts NSE

OUTILS MAÎTRISÉS
  aircrack-ng suite (airmon, airodump, aireplay, aircrack)
  hcxtools (hcxpcapngtool, hcxdumptool)
  hashcat (mode 22000, règles)
  crunch, cupp (génération wordlists)
  wpa_supplicant (connexion)
  arp-scan, nbtscan, avahi-browse
  nmap (scan, NSE)
  Wireshark (analyse PCAP)

LIVRABLES PRODUITS
  Capture handshake validée
  PSK ARTECH cracké en lab
  Dictionnaire personnalisé
  Cartographie LAN ARTECH
  Rapport offensif structuré
  Mapping MITRE ATT&CK

PRÉPARATION MODULE 6
  Connexion LAN établie
  Cibles internes identifiées (.150 Sophie, .151 Paul)
  Vecteur phishing depuis LAN possible
  Sliver C2 préparation à venir

CADRE LÉGAL INTÉGRÉ
  Articles 226-15, 323-1 connus
  Mandat documenté requis
  Lab ARTECH dédié
  Documentation forensique systématique

DÉFENSES RECOMMANDÉES POUR ARTECH
  PSK 20+ caractères aléatoires
  Migration WPA3-SAE
  PMF (802.11w) required
  Réduction puissance émission
  IDS Wi-Fi (Suricata)
  Segmentation LAN VLAN
  Monitoring DHCP/ARP anomalies
  Audit trimestriel
```

---

**Chapitre précédent** : [5.9 nmap silencieux et énumération](5-9-nmap-silencieux.md)

**Module suivant** : [Module 6 - Phishing basique](../module-6-phishing-basique/README.md)
