---
description: "YARA — Langage de détection de malwares par contenu : syntaxe des règles, strings, conditions, modules et intégration avec les outils SOC."
icon: lucide/book-open-check
tags: ["YARA", "MALWARE", "DÉTECTION", "SIGNATURES", "SOC", "THREAT INTELLIGENCE"]
---

# YARA — Signatures de Détection de Malwares

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="YARA 4.x"
  data-time="~3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Loupe du Botaniste"
    Un botaniste identifie une plante rare non pas par son nom (inconnu) mais par ses **caractéristiques distinctives** : forme des feuilles, couleur des fleurs, disposition des tiges. Même si la plante est légèrement mutée, certains traits restent caractéristiques de son espèce. **YARA** fonctionne identiquement avec les malwares : il cherche les **chaînes de caractères, séquences de bytes ou patterns** qui caractérisent un malware ou une famille entière — même si l'attaquant a modifié des parties du code.

**YARA** est le standard industriel pour écrire des signatures de détection de malwares basées sur le **contenu des fichiers**. Contrairement aux hash (qui changent avec un seul bit modifié), les règles YARA peuvent détecter des **variantes d'une même famille** de malware.

**Utilisations en SOC :**
- Scanner des fichiers suspects remontés par le FIM Wazuh
- Enrichir les alertes avec l'identification du malware
- Threat Hunting sur des archives de fichiers
- Intégration dans les sandboxes d'analyse

<br>

---

## Syntaxe d'une règle YARA

```
rule NomDeLaRegle : tags {
    meta:
        // Métadonnées (non utilisées pour la détection)
    strings:
        // Chaînes, bytes ou regex à chercher
    condition:
        // Logique booléenne de déclenchement
}
```

<br>

---

## Les 3 types de strings

```yara title="yara-strings-examples.yar — Les 3 types de strings YARA"
rule ExempleStrings {
    strings:
        // 1. Chaîne de texte (ASCII par défaut)
        $text1 = "cmd.exe /c whoami"
        $text2 = "powershell -enc" nocase      // insensible à la casse
        $text3 = "malware.exe" wide            // UTF-16 (chaînes Windows)
        $text4 = "evil" ascii wide nocase      // ASCII + UTF-16 + insensible

        // 2. Séquence hexadécimale (pour les shellcodes ou données binaires)
        $hex1 = { 4D 5A 90 00 }               // Magic bytes PE (MZ header)
        $hex2 = { 6A 40 68 00 30 00 00 }      // Shellcode courant
        $hex3 = { FC E8 8? 00 00 00 }         // Wildcard : 8? = 80-8F (shellcode Meterpreter)

        // 3. Expression régulière (regex)
        $regex1 = /https?:\/\/[a-z0-9]{8,}\.(xyz|top|ru|cn)\//  // C2 DGA
        $regex2 = /[A-Za-z0-9+\/]{50,}={0,2}/  // Chaîne Base64 longue (payload encodé)

    condition:
        any of them
}
```

<br>

---

## Règles YARA complètes — Exemples SOC

```yara title="soc-detection.yar — Règles pratiques pour un SOC"
// ===========================================================================
// Règle 1 : Détection de Mimikatz (credential dumping)
// Cherche les chaînes caractéristiques de Mimikatz même si renommé
// ===========================================================================
rule Mimikatz_Generic {
    meta:
        author      = "SOC Team"
        description = "Détection générique de Mimikatz par ses chaînes internes"
        threat_level = 10
        mitre       = "T1003.001"

    strings:
        // Chaînes présentes dans tous les builds Mimikatz
        $s1 = "mimikatz" nocase wide ascii
        $s2 = "sekurlsa::logonpasswords" nocase
        $s3 = "lsadump::sam" nocase
        $s4 = "kerberos::golden" nocase
        // Fonctions exports de mimikatz.dll
        $s5 = "SekurLSAInject" nocase

    condition:
        // 2 chaînes suffisent (tolérance aux variantes)
        2 of ($s*)
}

// ===========================================================================
// Règle 2 : Fichier PE téléchargé via PowerShell (Dropper)
// ===========================================================================
rule Dropper_PowerShell_PE {
    meta:
        description = "Exécutable Windows (PE) potentiellement droppé par PowerShell"
        mitre       = "T1059.001,T1204.002"

    strings:
        // MZ header (signature de tout exécutable Windows)
        $mz = { 4D 5A }
        // Traces PowerShell dans le fichier
        $ps1 = "System.Net.WebClient" nocase
        $ps2 = "DownloadFile" nocase
        $ps3 = "IEX(" nocase  // Invoke-Expression (exécution en mémoire)

    condition:
        // Fichier PE qui contient des traces PowerShell = dropper suspect
        $mz at 0 and any of ($ps*)
}

// ===========================================================================
// Règle 3 : Ransomware générique (chiffrement de masse)
// ===========================================================================
rule Ransomware_Generic_Behavior {
    meta:
        description = "Comportement générique de ransomware (note de rançon + chiffrement)"
        mitre       = "T1486"

    strings:
        // Notes de rançon courantes
        $ransom1 = "YOUR FILES ARE ENCRYPTED" nocase
        $ransom2 = "Send Bitcoin" nocase
        $ransom3 = "decrypt your files" nocase
        $ransom4 = "README_DECRYPT" nocase
        // API Windows utilisées pour le chiffrement massif
        $api1 = "CryptEncrypt" nocase
        $api2 = "CryptGenKey" nocase
        // Suppression des sauvegardes (technique courante)
        $vss1 = "vssadmin delete shadows" nocase
        $vss2 = "wbadmin delete" nocase

    condition:
        (1 of ($ransom*)) or (2 of ($api*)) or (1 of ($vss*))
}

<br>

---

## Expertise : Modules et Analyse Avancée

YARA permet d'importer des modules pour analyser la structure interne des fichiers (PE, ELF, .NET) ou calculer des métriques mathématiques.

### 1 — Le module PE (Portable Executable)
Indispensable pour limiter les faux positifs en ciblant des caractéristiques spécifiques des fichiers Windows.

```yara title="yara-pe-module.yar — Utilisation du module PE"
import "pe"

rule Suspicious_PE_Structure {
    condition:
        // Cible uniquement les fichiers Windows (MZ header)
        uint16(0) == 0x5A4D and 
        
        // Fichier sans table de symboles et avec peu de fonctions importées
        pe.number_of_signatures == 0 and
        pe.number_of_imports < 5 and
        
        // Section de code avec un nom inhabituel (ex: UPX, .aspack)
        for any section in pe.sections : (
            section.name == ".upx" or section.name == ".reloc"
        )
}
```

### 2 — Le module Math : Détection de l'Obfuscation
Les malwares sont souvent packés ou chiffrés pour échapper à l'analyse statique. Cela génère une **entropie élevée** (désordre statistique).

```yara title="yara-entropy.yar — Détection par entropie"
import "math"

rule High_Entropy_Section {
    meta:
        description = "Détection de sections compressées ou chiffrées"
    condition:
        for any section in pe.sections : (
            // Une entropie > 7.0 indique presque à coup sûr du code chiffré/packé
            math.entropy(section.raw_data_offset, section.raw_data_size) > 7.0
        )
}
```

---

## Optimisation des performances SOC

Dans un environnement de production (SOC), scanner des milliers de fichiers avec des centaines de règles peut saturer le CPU.

!!! danger "L'erreur classique de performance"
    Évitez les regex trop permissives comme `/.*/` ou les conditions qui obligent YARA à scanner l'intégralité du fichier si une signature simple en début de fichier (comme le MZ header) pourrait l'exclure immédiatement.

| Pratique | Pourquoi ? |
|---|---|
| **`uint16(0) == 0x5A4D`** | Exclut 90% des fichiers non-exécutables en 1 nanoseconde. |
| **Limiter la taille** | `filesize < 5MB` évite de scanner des fichiers ISO ou logs géants. |
| **Positionnement** | `$str at 0` ou `$str in (0..1024)` limite la zone de recherche. |
| **Éviter `nocase`** | Si vous connaissez la casse exacte, ne pas utiliser `nocase` divise le temps de recherche par 2. |
```

<br>

---

## Utilisation en ligne de commande

```bash title="Commandes YARA — Scanner des fichiers et répertoires"
# Installer YARA
apt-get install -y yara    # Ubuntu/Debian
brew install yara           # macOS

# Scanner un fichier unique
yara -r soc-detection.yar /chemin/vers/fichier.exe

# Scanner un répertoire entier récursivement
yara -r soc-detection.yar /var/uploads/

# Scanner avec tous les détails (quelles strings ont matché)
yara -s soc-detection.yar fichier_suspect.exe

# Utiliser un répertoire de règles
yara -r /etc/yara/rules/ /home/ 2>/dev/null

# Intégration avec un fichier PCAP (avec yara-python)
python3 -c "
import yara, dpkt
rules = yara.compile('/etc/yara/rules/soc-detection.yar')
# Scanner les payloads des paquets réseau...
"
```

<br>

---

## Intégration avec Wazuh (Active Response)

Wazuh peut déclencher automatiquement un scan YARA sur tout fichier créé détecté par le FIM :

```xml title="ossec.conf — Déclencher YARA sur les nouveaux fichiers (FIM)"
<ossec_config>
  <!-- Active Response : lancer YARA quand FIM détecte un nouveau fichier -->
  <active-response>
    <command>yara_scan</command>
    <!-- Déclencher sur les alertes FIM (ajout de fichier) -->
    <rules_id>554</rules_id>
    <timeout>60</timeout>
  </active-response>
</ossec_config>
```

```bash title="/var/ossec/active-response/bin/yara_scan — Script de scan automatique"
#!/bin/bash
# Script déclenché par Wazuh Active Response
# $1 = chemin du fichier à scanner

YARA_RULES="/etc/yara/rules/"
FILE_PATH=$(echo $1 | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('parameters', {}).get('alert', {}).get('syscheck', {}).get('path', ''))")

if [ -f "$FILE_PATH" ]; then
    RESULT=$(yara -r "$YARA_RULES" "$FILE_PATH" 2>/dev/null)
    if [ -n "$RESULT" ]; then
        logger -t "yara_scan" "MATCH: $RESULT"
        echo "YARA ALERT: $RESULT" >> /var/ossec/logs/yara_alerts.log
    fi
fi
```

<br>

---

## Sources de règles YARA gratuites

| Source | URL | Contenu |
|---|---|---|
| **Awesome YARA** | github.com/InQuest/awesome-yara | Méta-liste de repos |
| **YARA-Rules** | github.com/Yara-Rules/rules | Règles communautaires |
| **Elastic** | github.com/elastic/protections-artifacts | Règles Elastic Security |
| **Signature-Base** | github.com/Neo23x0/signature-base | Florian Roth (expert reconnu) |
| **MalwareBazaar** | bazaar.abuse.ch | Règles liées aux malwares uploadés |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    YARA est l'outil qui transforme une analyse de malware en **connaissance réutilisable**. Chaque malware analysé devient une règle qui protège contre toutes ses futures variantes. La clé d'une bonne règle YARA est l'**équilibre** : assez spécifique pour ne pas matcher des fichiers légitimes, assez générique pour attraper les variantes de la même famille. Les modules YARA (`pe`, `elf`, `math`) permettent d'aller encore plus loin dans la précision.

> Passez au cours **[Sigma →](./sigma.md)** pour apprendre l'équivalent de YARA, mais pour les événements de logs — le format universel qui unifie la détection dans tous les SIEM.
