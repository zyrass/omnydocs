---
title: 7.4 Cas du ransomware en cours d'exécution
description: Réponse à incident forensique face à un poste Windows compromis par ransomware. Reconnaissance des indicateurs en cours, décision critique d'isolation, acquisition mémoire prioritaire, triage rapide, préservation des preuves. Perspective DFIR strictement défensive.
authors:
  - Zyrass
date:
  created: 2026-04-30
tags:
  - DFIR
  - Ransomware
  - Acquisition mémoire
  - Triage
  - Réponse à incident
data-level: 🔴
---

# 7.4 Cas du ransomware en cours d'exécution

!!! quote "L'analogie du pompier qui arrive devant l'incendie en cours"

    Un pompier expérimenté arrivant sur un sinistre n'éteint pas le feu en premier. Il évalue d'abord : combien de personnes sont à l'intérieur, où le feu se propage, quel est le risque d'effondrement, où sont les bouteilles de gaz. Cette évaluation dure 90 secondes mais détermine toute la stratégie. S'il se précipite dans les flammes sans évaluer, il sauve une victime mais en perd trois. L'analyste forensique face à un poste compromis par ransomware en cours d'exécution agit pareillement. Le réflexe naturel serait d'éteindre la machine pour stopper le chiffrement. Mauvaise idée. Avant tout, on évalue, on capture la mémoire qui contient peut-être les clés de déchiffrement, on isole sans interrompre, puis on décide. Ce chapitre vous donne la grille de décision en quatre minutes qui peut sauver les données ou les condamner.

## Métadonnées du chapitre

Ce chapitre est l'un des plus opérationnels du module 7. Voici ses caractéristiques.

| Champ | Valeur |
|---|---|
| Durée estimée | 3 heures |
| Niveau | Pratique critique |
| Prérequis | 7.1 (RFC 3227), 7.2 (décision allumer/éteindre), 7.3 (BitLocker) |
| Livrables | Procédure de réponse ransomware en 4 minutes |
| Auto-explication | 12 minutes |

## Objectifs pédagogiques

À l'issue de ce chapitre, vous serez capable de :

- Reconnaître un ransomware en cours d'exécution dans les premières secondes
- Appliquer la grille de décision isolation et acquisition
- Justifier la priorité de l'acquisition mémoire face au ransomware
- Effectuer un triage rapide des processus et connexions
- Préserver les indices disque malgré le chiffrement en cours
- Documenter chaque décision pour la chaîne de garde

---

## 1. Pourquoi le ransomware est un cas particulier

Le ransomware en cours d'exécution est l'un des scénarios les plus stressants en DFIR. Voici ce qui le rend unique.

### 1.1 Course contre la montre

Voici les facteurs qui imposent une réaction rapide.

| Facteur | Conséquence |
|---|---|
| Chiffrement actif | Chaque seconde, des fichiers sont perdus |
| Propagation latérale | Le ransomware peut atteindre les partages réseau |
| Suppression VSS | Volume Shadow Copies souvent détruites en premier |
| Exfiltration parallèle | Double extorsion : data volée avant chiffrement |
| Persistance multiple | Tâches planifiées, services, registres |

### 1.2 Tension entre objectifs

Plusieurs objectifs s'opposent partiellement. Voici la matrice de tensions.

| Objectif | Action immédiate | Tension avec |
|---|---|---|
| Stopper le chiffrement | Éteindre la machine | Préservation mémoire |
| Préserver les clés en RAM | Maintenir alimentation | Stoppage du chiffrement |
| Limiter la propagation | Isoler du réseau | Communication C2 si forensic en ligne |
| Documenter la scène | Photos, captures | Temps perdu pour la suite |
| Préparer la décrypteuse éventuelle | Ne rien casser | Action défensive immédiate |

### 1.3 Importance des clés en mémoire

Plusieurs familles de ransomware laissent des **clés de chiffrement en mémoire** pendant l'exécution. Si l'acquisition est rapide, ces clés peuvent être extraites par les outils de l'analyste ou par les chercheurs en sécurité.

Voici quelques cas historiques documentés publiquement.

| Famille | Clés extractibles en RAM | Source |
|---|---|---|
| LockBit Black (3.0) | Oui dans certaines versions | Analyses CERT-FR |
| BlackCat / Alphv | Oui dans Rust binary | Recherches publiques |
| Conti | Oui (clés AES par fichier) | Trickbot/Conti leaks 2022 |
| REvil | Variable selon version | Travaux Bitdefender |
| Babuk | Code source fuité 2021 | Source code public |

L'enseignement opérationnel est clair. **Acquérir la mémoire avant tout autre acte** maximise les chances de récupération ultérieure des données.

## 2. Phase 1 - Premières secondes - reconnaissance

Vous arrivez devant un poste Windows. Comment savoir en moins d'une minute si un ransomware est actif ?

### 2.1 Indicateurs visuels

Voici les indicateurs visibles à l'écran et au système.

| Indicateur | Description | Confiance |
|---|---|---|
| Wallpaper modifié | Ransom note à la place du fond d'écran | Très élevée |
| Fichiers `*.txt` partout | "HOW_TO_DECRYPT.txt" dans chaque dossier | Très élevée |
| Extensions modifiées | `.lockbit`, `.enc`, `.crypt`, `.encrypted` | Très élevée |
| Pop-up ransom | Fenêtre permanente avec compteur | Très élevée |
| Imprimante en boucle | Impression continue de la ransom note | Élevée |
| Activité disque massive | LED stockage allumée en permanence | Élevée |
| Lenteur extrême | OS quasi inutilisable | Modérée |

### 2.2 Indicateurs en ligne de commande rapide

Si vous avez accès au terminal (PowerShell admin), voici les commandes rapides.

```powershell
# Note : commandes à lancer depuis un terminal admin déjà ouvert
# Si rien n'est ouvert, NE PAS s'authentifier (perte d'indices)

# Processus suspects par usage CPU
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Processus avec usage disque élevé (signe de chiffrement actif)
Get-Counter '\Process(*)\IO Write Bytes/sec' -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty CounterSamples |
    Sort-Object -Property CookedValue -Descending |
    Select-Object -First 10

# Connexions réseau actives (potentiel C2)
Get-NetTCPConnection -State Established |
    Select-Object LocalAddress, RemoteAddress, RemotePort, OwningProcess

# Suppression VSS récente (signature très forte de ransomware)
Get-WinEvent -LogName "Microsoft-Windows-VSS/Operational" -MaxEvents 50 -ErrorAction SilentlyContinue |
    Where-Object { $_.Message -match "delete" }
```

### 2.3 Interrogation de l'utilisateur

Si l'utilisateur est présent, voici les questions à poser en moins de 60 secondes.

```text
INTERROGATOIRE EXPRESS UTILISATEUR
=====================================

1. À quelle heure avez-vous remarqué le problème ?
2. Qu'avez-vous fait juste avant ?
   (mail ouvert, lien cliqué, fichier exécuté ?)
3. Avez-vous redémarré, fermé, autre action ?
4. Est-ce votre machine personnelle ou pro ?
5. Êtes-vous connecté à des partages réseau ?
6. Avez-vous des sauvegardes récentes ?
7. Avez-vous remarqué autre chose d'inhabituel
   ces derniers jours ?

DOCUMENTER les réponses verbatim avec horodatage.
```

### 2.4 Signature - LE moment de décision

Si **trois indicateurs** ou plus concordent, vous avez la quasi-certitude qu'un ransomware est actif. Vous passez immédiatement en phase 2.

## 3. Phase 2 - Décision critique en 60 secondes

Cette phase est la plus délicate. Trois questions, trois réponses, dans cet ordre.

### 3.1 Question 1 - Couper le réseau ?

Voici la matrice de décision sur l'isolation réseau.

| Situation | Décision |
|---|---|
| Poste isolé sans partages | Pas urgent |
| Poste sur un domaine AD | Isoler immédiatement |
| Poste avec partages réseau montés | Isoler immédiatement |
| EDR actif gérant l'isolation | Laisser EDR faire |
| Forensic à distance via EDR uniquement | Conserver le réseau le temps du dump |

Voici la procédure d'isolation physique.

```text
ISOLATION RÉSEAU PHYSIQUE
============================

Méthode 1 - Débrancher le câble Ethernet
  Avantage : immédiat, pas de logon
  Inconvénient : aucun

Méthode 2 - Désactiver le Wi-Fi (touche fonction)
  Avantage : sans déverrouiller
  Inconvénient : Bluetooth peut rester actif

Méthode 3 - PowerShell Disable-NetAdapter
  Avantage : précis
  Inconvénient : nécessite session ouverte

Méthode 4 - Cage de Faraday / pochette anti-ondes
  Avantage : isole tous les protocoles
  Inconvénient : matériel spécifique
```

### 3.2 Question 2 - Acquisition mémoire avant tout

La réponse est presque toujours **OUI**, sauf cas extrêmes. Voici les facteurs.

| Facteur | Acquérir la mémoire ? |
|---|---|
| Ransomware connu pour clés en RAM | OUI absolument |
| Famille inconnue | OUI par défaut |
| Disque chiffré BitLocker actif | OUI (clés de volume en RAM) |
| Volume disque presque saturé I/O | OUI mais en parallèle |
| Suspicion d'exfiltration en cours | OUI (sessions C2 visibles) |

Voici les rares cas où l'on peut envisager d'éteindre avant.

| Situation | Justification |
|---|---|
| Risque immédiat sur vie humaine (équipement médical) | Sauvegarde de la fonction prime |
| Ordre explicite hiérarchique avec décharge | Couvre la décision |
| Aucun outil d'acquisition disponible | Pas le choix |

### 3.3 Question 3 - Que faire des écrans et périphériques ?

Voici les bons réflexes annexes.

| Élément | Action |
|---|---|
| Écran | Photographier l'état actuel (smartphone) |
| Clés USB branchées | Photographier mais NE PAS retirer |
| Disques externes | Idem, ne pas démonter |
| Imprimante en boucle | Couper son alimentation seule |
| Souris / clavier | Conserver, peuvent contenir traces |

## 4. Phase 3 - Acquisition mémoire prioritaire

Vous passez à l'acquisition. Voici la procédure pratique.

### 4.1 Outils recommandés

Voici les outils principaux d'acquisition mémoire Windows en 2026.

| Outil | Type | Vitesse | Note |
|---|---|---|---|
| Magnet RAM Capture | Gratuit | Rapide | Bonne référence |
| FTK Imager Lite | Gratuit | Moyen | Acquisition multi-formats |
| DumpIt (Comae) | Gratuit | Très rapide | Hibernation-style |
| Belkasoft RAM Capturer | Gratuit | Rapide | Léger, portable |
| WinPmem | Gratuit | Rapide | Open source, scriptable |

### 4.2 Préparation du kit USB

L'acquisition se fait depuis un **kit USB d'analyste** préparé à l'avance. Voici son contenu type.

```text
KIT USB DFIR - CONTENU TYPE
==============================

/Tools/
  /MagnetRAMCapture/
    MagnetRAMCapture.exe
  /FTK_Imager/
    Imager_Lite/
  /DumpIt/
    DumpIt.exe
  /WinPmem/
    winpmem_mini_x64_rc2.exe
  /Sysinternals/
    autoruns.exe
    procexp.exe
    pslist.exe
    handle.exe
    tcpview.exe

/Scripts/
  triage-quick.ps1
  hash-immediate.ps1
  log-action.ps1

/Docs/
  procedure-rapide.pdf
  formulaire-scellement.pdf
```

Le kit USB doit être en **lecture seule** physiquement (clé avec switch hardware) pour éviter toute contamination.

### 4.3 Acquisition avec Magnet RAM Capture

Voici la procédure pas à pas avec Magnet RAM Capture.

```powershell
# Branchement du kit USB en lecture seule (E: par exemple)
# Identification de la lettre du disque cible où écrire (F: par exemple, disque externe DFIR dédié)

# Lancement (depuis le kit USB)
E:\Tools\MagnetRAMCapture\MagnetRAMCapture.exe

# Dans l'interface :
#   Output path : F:\acquisitions\poste-XYZ\YYYYMMDD-HHMMSS-memdump.raw
#   Format : Raw (.raw) ou Microsoft Crash Dump (.dmp)
#   Compression : non (à hash après pour intégrité)

# Cliquer "Start"
# Acquisition de 16 Go RAM prend typiquement 3-8 minutes
```

### 4.4 Acquisition en ligne de commande - WinPmem

Pour les contextes scriptables, WinPmem est efficace.

```powershell
# Commande type WinPmem
# Hash systeme avant (pour vérification ultérieure)
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$output = "F:\acquisitions\poste-XYZ\$timestamp-memdump.raw"

# Lancement
E:\Tools\WinPmem\winpmem_mini_x64_rc2.exe $output

# Sortie attendue
# CR3: 0x...
# Memory size: 16 GB
# Output: F:\acquisitions\...\memdump.raw
# Acquisition complete

# Hash immédiat
Get-FileHash $output -Algorithm SHA256 | Format-List
```

### 4.5 Hash immédiat et double copie

L'acquisition doit être hashée immédiatement et copiée en double exemplaire pour la chaîne de garde.

```powershell
# Hash SHA-256
$hash = (Get-FileHash $output -Algorithm SHA256).Hash
"$hash  $output" | Out-File -Encoding utf8 "$output.sha256"

# Double copie sur un second support
Copy-Item $output "G:\acquisitions-copy\$timestamp-memdump.raw"

# Vérification du hash de la copie
$hash2 = (Get-FileHash "G:\acquisitions-copy\$timestamp-memdump.raw" -Algorithm SHA256).Hash
if ($hash -eq $hash2) {
    Write-Host "[OK] Hash original et copie identiques"
} else {
    Write-Host "[ERREUR] Hashes divergent - copie corrompue"
}
```

## 5. Phase 4 - Triage rapide après acquisition

Une fois la mémoire capturée, vous pouvez observer le système vivant pendant quelques minutes pour le triage. L'objectif est de **collecter des indicateurs volatils** avant l'arrêt.

### 5.1 Triage processus

Voici les commandes de triage processus à enchaîner.

```powershell
# Snapshot processus complet avec command line
Get-WmiObject Win32_Process |
    Select-Object ProcessId, ParentProcessId, Name, ExecutablePath, CommandLine, CreationDate |
    Export-Csv "F:\triage\processus-$timestamp.csv" -NoTypeInformation

# Hash des binaires des processus actifs
Get-Process | ForEach-Object {
    if ($_.Path) {
        $h = Get-FileHash $_.Path -Algorithm SHA256 -ErrorAction SilentlyContinue
        [PSCustomObject]@{
            PID = $_.Id
            Name = $_.Name
            Path = $_.Path
            SHA256 = $h.Hash
        }
    }
} | Export-Csv "F:\triage\processus-hash-$timestamp.csv" -NoTypeInformation

# Process Hacker en mode read-only depuis le kit
E:\Tools\Sysinternals\procexp.exe
# Sauvegarder en .pml pour analyse offline
```

### 5.2 Triage réseau

Voici les commandes de triage réseau.

```powershell
# Connexions TCP établies avec processus
Get-NetTCPConnection -State Established |
    Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort,
                  @{N="Process"; E={(Get-Process -Id $_.OwningProcess).Name}} |
    Export-Csv "F:\triage\netstat-$timestamp.csv" -NoTypeInformation

# Cache DNS récent (révèle domaines C2 contactés)
ipconfig /displaydns > "F:\triage\dns-cache-$timestamp.txt"

# Connexions UDP
Get-NetUDPEndpoint |
    Export-Csv "F:\triage\udp-$timestamp.csv" -NoTypeInformation

# Tables ARP
arp -a > "F:\triage\arp-$timestamp.txt"

# Sessions SMB ouvertes
Get-SmbSession 2>$null |
    Export-Csv "F:\triage\smb-sessions-$timestamp.csv" -NoTypeInformation
```

### 5.3 Triage persistance

Voici les commandes pour identifier la persistance ransomware.

```powershell
# Tâches planifiées récentes
Get-ScheduledTask |
    Where-Object { $_.Date -gt (Get-Date).AddDays(-7) } |
    Export-Csv "F:\triage\tasks-$timestamp.csv" -NoTypeInformation

# Services récemment installés
Get-WmiObject Win32_Service |
    Select-Object Name, DisplayName, PathName, State, StartMode |
    Export-Csv "F:\triage\services-$timestamp.csv" -NoTypeInformation

# Clés Run du registre (autostart)
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" |
    Out-File "F:\triage\hklm-run-$timestamp.txt"
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" |
    Out-File "F:\triage\hkcu-run-$timestamp.txt"

# Autoruns Sysinternals
E:\Tools\Sysinternals\autoruns.exe -accepteula -nobanner -a * -c |
    Out-File "F:\triage\autoruns-$timestamp.csv"
```

### 5.4 Triage chiffrement en cours

Voici comment évaluer l'avancement du chiffrement.

```powershell
# Scan rapide d'extensions suspectes dans dossiers utilisateurs
$suspExtensions = @(".lockbit", ".enc", ".encrypted", ".crypt", ".locked", ".[a-z0-9]{6,8}$")
$userPaths = @("C:\Users", "D:\")

foreach ($path in $userPaths) {
    if (Test-Path $path) {
        Get-ChildItem $path -Recurse -File -ErrorAction SilentlyContinue |
            Where-Object {
                $ext = $_.Extension
                $suspExtensions | Where-Object { $ext -match $_ }
            } |
            Select-Object FullName, Length, LastWriteTime |
            Export-Csv "F:\triage\suspect-files-$timestamp.csv" -Append -NoTypeInformation
    }
}

# Recherche de la ransom note (fichiers texte typiques)
$ransomNoteNames = @(
    "HOW_TO_DECRYPT*.txt",
    "READ_ME*.txt",
    "DECRYPT_INSTRUCT*.txt",
    "*RECOVERY*.txt"
)

foreach ($pattern in $ransomNoteNames) {
    Get-ChildItem "C:\" -Recurse -File -Filter $pattern -ErrorAction SilentlyContinue |
        Select-Object FullName, LastWriteTime |
        Export-Csv "F:\triage\ransom-notes-$timestamp.csv" -Append -NoTypeInformation
}
```

## 6. Phase 5 - Préservation des indices disque

Une fois le triage en mémoire effectué, vous préparez l'arrêt et l'acquisition disque (chapitre suivant).

### 6.1 Récupération de la ransom note

La ransom note est un indicateur très précieux pour identifier la famille.

```powershell
# Copie d'une ransom note représentative pour analyse
$note = Get-ChildItem "C:\Users\Public\Desktop\HOW_TO_DECRYPT.txt" -ErrorAction SilentlyContinue
if ($note) {
    Copy-Item $note.FullName "F:\triage\ransom-note-sample.txt"
    Get-FileHash $note.FullName -Algorithm SHA256
}

# La ransom note contient typiquement :
#   - Identifiant de la victime (UUID)
#   - URL Tor du portail de paiement
#   - Email de contact
#   - Famille / branding du ransomware
```

### 6.2 Identification de famille

Voici comment identifier la famille de ransomware à partir des indices.

| Indice | Méthode |
|---|---|
| Extension fichiers | Recherche dans bases publiques (ID Ransomware) |
| Texte de la ransom note | Recherche signatures connues |
| Hash binaire principal | VirusTotal après acquisition |
| URL onion contact | Recherche dans threat intel |
| Pattern de chiffrement | Analyse offline ultérieure |

L'outil **ID Ransomware** (id-ransomware.malwarehunterteam.com) accepte une ransom note ou un fichier chiffré et identifie la famille avec confiance.

### 6.3 Décision d'arrêt après triage

Une fois le triage terminé, vous avez deux options pour l'arrêt.

| Option | Avantages | Inconvénients |
|---|---|---|
| Pull-the-plug (alimentation coupée) | Stoppe immédiatement le chiffrement, préserve l'état disque | Corruption fichiers en écriture |
| Shutdown propre (`shutdown /s`) | État disque cohérent | Continue le chiffrement pendant le shutdown |
| Hibernation forcée | Capture finale en hiberfil.sys | Ressuscite si on redémarre |

Pour la majorité des cas ransomware, le **pull-the-plug est recommandé** une fois la mémoire acquise. La corruption potentielle de fichiers en écriture est marginale par rapport au chiffrement continu.

### 6.4 Documentation horodatée

Chaque étape doit être documentée. Voici le template type.

```text
JOURNAL DE RÉPONSE - INCIDENT RANSOMWARE
============================================

Référence : INC-2026-XXX
Analyste : Zyrass / OmnyVia
Site : ARTECH SAS, Lyon Vaise

CHRONOLOGIE

2026-MM-DDTHH:MM:SSZ  Arrivée sur site
2026-MM-DDTHH:MM:SSZ  Constatation visuelle ransom note
2026-MM-DDTHH:MM:SSZ  Photo écran (smartphone)
2026-MM-DDTHH:MM:SSZ  Décision : isolation réseau
2026-MM-DDTHH:MM:SSZ  Câble Ethernet débranché
2026-MM-DDTHH:MM:SSZ  Décision : acquisition mémoire prioritaire
2026-MM-DDTHH:MM:SSZ  Branchement kit USB read-only
2026-MM-DDTHH:MM:SSZ  Lancement Magnet RAM Capture
2026-MM-DDTHH:MM:SSZ  Acquisition terminée (16 Go, 4m32s)
2026-MM-DDTHH:MM:SSZ  Hash SHA-256 : a1b2c3...
2026-MM-DDTHH:MM:SSZ  Double copie sur disque G:
2026-MM-DDTHH:MM:SSZ  Triage processus / réseau / persistance
2026-MM-DDTHH:MM:SSZ  Récupération ransom note
2026-MM-DDTHH:MM:SSZ  Identification famille : LockBit 3.0
2026-MM-DDTHH:MM:SSZ  Pull-the-plug
2026-MM-DDTHH:MM:SSZ  Disque externe scellé pour acquisition

DÉCISIONS PRISES
  ...

OUTILS UTILISÉS
  ...

SIGNATURES
  Analyste : ___________
  Témoin : ___________
```

## 7. Cadre légal et obligations

### 7.1 Notifications obligatoires

Plusieurs obligations légales s'appliquent en cas de ransomware.

| Obligation | Délai | Référence |
|---|---|---|
| Notification CNIL si données personnelles | 72 heures | RGPD article 33 |
| Information personnes concernées si risque élevé | Sans délai injustifié | RGPD article 34 |
| Plainte auprès du procureur | À l'initiative victime | Code procédure pénale |
| Signalement ANSSI si OIV/OSE | Sans délai | LPM, NIS2 |
| Information assureur | Variable selon contrat | Contrat assurance cyber |

### 7.2 Articles pénaux applicables aux attaquants

Les attaquants sont passibles de plusieurs articles. Connaître ceux-ci est utile pour la rédaction du dépôt de plainte.

| Article | Infraction | Peine |
|---|---|---|
| 323-1 | Accès frauduleux STAD | 3 ans / 100 000 € |
| 323-2 | Entrave / altération STAD | 5 ans / 150 000 € |
| 323-3 | Modification frauduleuse données | 5 ans / 150 000 € |
| 323-3-1 | Détention outils | 5 ans / 75 000 € |
| 312-1 | Extorsion | 7 ans / 100 000 € |
| 226-22 | Atteinte STAD avec données perso | 5 ans / 300 000 € |

### 7.3 Position recommandée sur le paiement

L'ANSSI, le FBI et la majorité des CERT recommandent de **ne pas payer**. Voici les raisons.

| Raison | Justification |
|---|---|
| Pas de garantie de déchiffrement | 30 % des paiements ne donnent rien |
| Financement de l'écosystème criminel | Encourage les futures attaques |
| Risque double extorsion | Données déjà exfiltrées peuvent être publiées |
| Risque sanction OFAC | Si le groupe est sanctionné |
| Obligation déclaration TRACFIN | Transactions crypto suspectes |

## 8. Spécificités par famille de ransomware

Connaître la famille permet d'adapter la réponse.

### 8.1 Tableau synthétique

Voici les caractéristiques de quelques familles majeures actives en 2024-2026.

| Famille | Particularités | Recommandation acquisition |
|---|---|---|
| LockBit 3.0/Black | Très rapide, supprime VSS, exfiltre | Mémoire urgente, clés possibles |
| BlackCat / Alphv | Rust, multi-plateforme, configurable | Mémoire urgente |
| Royal | Partial encryption (rapide), targets gros | Mémoire et triage |
| Akira | Linux + Windows, jeune (2023) | Mémoire, observation |
| BlackBasta | Branding Conti-like, Qbot loader | Persistence multiple |
| Play | Intermittent encryption | Mémoire pendant phase active |
| Phobos / 8base | Petites entreprises, ciblage RDP | Acquisition standard |

### 8.2 Sources de threat intelligence

Pour identifier rapidement et obtenir des IOC, voici les sources de référence.

| Source | URL | Type |
|---|---|---|
| ANSSI CERT-FR | cert.ssi.gouv.fr | Alertes France officielles |
| Ransomware.live | ransomware.live | Tracker temps réel |
| MISP communauté FR | misp-project.org | IOC partagés |
| ID Ransomware | id-ransomware.malwarehunterteam.com | Identification rapide |
| No More Ransom | nomoreransom.org | Decryptors gratuits |
| Bleeping Computer | bleepingcomputer.com | Analyses publiques |

### 8.3 Decryptors gratuits

Avant tout paiement, vérifiez si un **decryptor gratuit** existe sur **No More Ransom** ou les sites des éditeurs (Kaspersky, Avast, Emsisoft, Bitdefender).

Quelques familles avec decryptors publics au moment de la rédaction du chapitre.

| Famille | Decryptor disponible |
|---|---|
| LockBit (anciennes versions) | Partiel |
| Babuk | Source code public, decrypt possible |
| HermeticRansom | Avast |
| AstraLocker | Emsisoft |
| Diavol | FBI |

## 9. Cas pratique - Réponse à incident lab

### 9.1 Mise en situation

Vous simulez en lab la réponse à un poste Windows infecté. Vous utilisez **un sample inerte** ou **une simulation pédagogique** (extension renamer + fake ransom note) pour ne pas reproduire un vrai chiffrement.

### 9.2 Protocole de simulation

Voici comment construire une simulation pédagogique sans risque.

```powershell
# ATTENTION : Simulation pédagogique uniquement
# Ce script renomme des fichiers de test et place une fausse note
# Il ne chiffre rien et est réversible

# Création environnement de test isolé
$testRoot = "C:\Lab-Test-Simulation"
New-Item -Path $testRoot -ItemType Directory -Force

# Copie de fichiers de test depuis un répertoire dédié
1..50 | ForEach-Object {
    "Contenu test $_" | Out-File "$testRoot\fichier-$_.txt"
}

# Simulation extension change (réversible)
Get-ChildItem $testRoot -Filter "*.txt" |
    Rename-Item -NewName { $_.Name + ".lab-sim" }

# Fausse ransom note pédagogique
@"
==========================================
SIMULATION PEDAGOGIQUE - LAB ARTECH
==========================================
Ceci est un fichier de simulation utilisé
pour la formation DFIR OmnyAcademy.
Aucun chiffrement reel n'a eu lieu.

Pour reverser :
  Get-ChildItem -Path 'C:\Lab-Test-Simulation' -Filter '*.lab-sim' |
    Rename-Item -NewName { `$_.Name -replace '.lab-sim','' }
==========================================
"@ | Out-File "$testRoot\HOW_TO_DECRYPT-SIMULATION.txt"
```

### 9.3 Exécution du protocole DFIR

Sur le poste de lab "infecté" par cette simulation, vous appliquez la procédure complète des sections 2 à 6.

```text
DÉROULÉ DE L'EXERCICE
=======================

T+0:00  Découverte ransom note simulée
T+0:30  Photo écran et premiers indicateurs
T+1:00  Décision isolation réseau
T+1:30  Branchement kit USB lab
T+2:00  Lancement acquisition mémoire
T+6:00  Acquisition terminée et hashée
T+6:30  Triage processus / réseau / persistance
T+10:00 Récupération note simulée
T+11:00 Identification "famille" (simulation)
T+12:00 Pull-the-plug
T+13:00 Disque externe préparé
T+15:00 Documentation finalisée
```

### 9.4 Évaluation de l'exercice

Voici la grille d'auto-évaluation post-exercice.

| Critère | Score 1-5 |
|---|---|
| Reconnaissance des indicateurs en moins d'une minute | _ |
| Décision isolation appropriée | _ |
| Acquisition mémoire avant arrêt | _ |
| Hash et double copie immédiats | _ |
| Triage processus complet | _ |
| Triage réseau complet | _ |
| Documentation horodatée continue | _ |
| Respect chaîne de garde | _ |
| Identification correcte de la famille | _ |
| Décision d'arrêt justifiée | _ |

Score total maximum : 50. Au-delà de 35, vous validez le scénario.

## 10. Pièges fréquents

Plusieurs pièges classiques sont à anticiper.

### 10.1 Pièges méthodologiques

Voici les erreurs courantes à éviter.

| Piège | Conséquence | Évitement |
|---|---|---|
| Éteindre par réflexe | Perte des clés en RAM | Acquisition mémoire d'abord |
| Se connecter au compte | Modification timeline | Travailler depuis kit USB |
| Lancer un antivirus immédiatement | Suppression d'indices | Acquisition d'abord |
| Redémarrer pour "voir" | Perte état mémoire | Pull-the-plug après acquisition |
| Oublier les partages réseau | Propagation continue | Isoler le poste rapidement |

### 10.2 Pièges techniques

Voici les erreurs techniques fréquentes.

| Piège | Conséquence | Évitement |
|---|---|---|
| Écrire sur le disque source | Contamination preuve | Cible d'écriture externe distincte |
| Pas de hash immédiat | Pas de valeur forensique | Hash systématique post-acquisition |
| Outils non testés | Échec d'acquisition | Tester le kit USB régulièrement |
| Disque cible saturé | Acquisition tronquée | Vérifier espace avant lancement |
| Antivirus bloque l'outil | Acquisition échoue | Whitelist préalable de l'outil |

## 11. Auto-évaluation

Vérifiez votre maîtrise par les questions suivantes.

| # | Question | Réponse |
|---|---|---|
| 1 | Pourquoi acquérir la mémoire avant tout ? | Clés de chiffrement potentiellement en RAM |
| 2 | Trois indicateurs visuels de ransomware actif ? | Wallpaper modifié, fichiers .txt partout, extensions changées |
| 3 | Quand isoler le poste du réseau ? | Avant l'acquisition si propagation possible |
| 4 | Outil rapide d'acquisition mémoire ? | Magnet RAM Capture / DumpIt |
| 5 | Algorithme de hash recommandé ? | SHA-256 |
| 6 | Délai notification CNIL ? | 72 heures (RGPD article 33) |
| 7 | Outil pour identifier la famille ? | ID Ransomware |
| 8 | Position recommandée sur le paiement ? | Ne pas payer (ANSSI, CERT) |
| 9 | Mode de coupure d'alimentation recommandé ? | Pull-the-plug après acquisition |
| 10 | Recours au préalable du paiement ? | Vérifier No More Ransom |

## 12. Synthèse

Voici les points clés à retenir.

```text
RANSOMWARE EN COURS - RÉPONSE DFIR

PHASE 1 - RECONNAISSANCE (< 1 min)
  Indicateurs visuels : wallpaper, ransom notes, extensions
  Indicateurs CMD : I/O élevé, processus suspect, VSS deleted
  Interrogatoire utilisateur 60 secondes

PHASE 2 - DÉCISION (< 1 min)
  Isolation réseau ? OUI si partages / domaine
  Acquisition mémoire ? OUI presque toujours
  Photos et préservation périphériques

PHASE 3 - ACQUISITION MÉMOIRE
  Kit USB lecture seule
  Magnet RAM Capture, FTK Imager, DumpIt, WinPmem
  Hash SHA-256 immédiat
  Double copie sur support distinct

PHASE 4 - TRIAGE VOLATIL
  Processus + command line + hash
  Connexions réseau + DNS cache
  Persistance : tâches, services, registres
  Évaluation chiffrement en cours

PHASE 5 - PRÉSERVATION
  Récupération ransom note
  Identification famille (ID Ransomware)
  Pull-the-plug post-acquisition
  Documentation horodatée continue

OUTILS DE RÉFÉRENCE
  Magnet RAM Capture : acquisition rapide
  WinPmem : acquisition scriptable
  Sysinternals : Procexp, Autoruns, TCPView
  PowerShell : triage natif

CADRE LÉGAL
  RGPD article 33 : notification CNIL 72h
  RGPD article 34 : information personnes concernées
  Article 323-1 et suivants : poursuites attaquants
  ANSSI : signalement OIV/OSE

RECOMMANDATION FINALE
  Ne pas payer
  Vérifier No More Ransom
  Conserver mémoire pour décrypteurs futurs
  Plainte au procureur
  Notification CNIL si données personnelles
```

---

**Chapitre précédent** : [7.3 Cas du chiffrement BitLocker actif](7-3-bitlocker-actif.md)

**Chapitre suivant** : [7.5 Préparation kit USB acquisition Windows](7-5-kit-usb-acquisition.md)