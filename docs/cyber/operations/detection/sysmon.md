---
description: "Sysmon — Télémétrie Windows haute-fidélité pour la détection SOC : installation, configuration XML, événements critiques et intégration avec Wazuh."
icon: lucide/book-open-check
tags: ["SYSMON", "WINDOWS", "TÉLÉMÉTRIE", "DÉTECTION", "SOC", "WAZUH", "EVENT LOG"]
---

# Sysmon — Télémétrie Windows Haute-Fidélité

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Sysmon 15.x"
  data-time="~3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Boîte Noire de l'Avion"
    Les Event Logs Windows natifs sont comme le journal de bord d'un avion : ils notent les grandes étapes (décollage, atterrissage) mais pas les détails critiques (cap, altitude à chaque seconde, anomalies moteur). **Sysmon** est la **boîte noire** de Windows : il enregistre chaque événement avec tous les détails nécessaires à une investigation — hash du processus, connexion réseau par processus, injection de code détectée. Sans Sysmon, votre SOC vole à l'aveugle sur Windows.

**System Monitor (Sysmon)** est un service Windows de la suite Sysinternals (Microsoft) qui enrichit considérablement les capacités de journalisation du système. Il génère des événements Windows détaillés pour :

- Chaque **création de processus** (avec hash SHA256 et ligne de commande complète)
- Chaque **connexion réseau** (avec le processus source)
- Chaque **modification de fichier** ou **chargement de driver**
- Les **injections de processus** (CreateRemoteThread, ProcessAccess)
- Les **modifications de registre** (clés de persistance)
- Les **requêtes DNS** (avec le processus demandeur)

<br>

---

## Installation

```powershell title="Installation Sysmon sur Windows — PowerShell (Administrateur)"
# Télécharger Sysmon depuis le site officiel Microsoft Sysinternals
Invoke-WebRequest -Uri "https://download.sysinternals.com/files/Sysmon.zip" -OutFile "C:\Temp\Sysmon.zip"
Expand-Archive -Path "C:\Temp\Sysmon.zip" -DestinationPath "C:\Temp\Sysmon"

# Télécharger une configuration Sysmon optimisée pour le SOC (SwiftOnSecurity)
# Cette config est la référence communautaire la plus utilisée
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml" -OutFile "C:\Temp\sysmon-config.xml"

# Installer Sysmon avec la configuration SOC
C:\Temp\Sysmon\Sysmon64.exe -accepteula -i C:\Temp\sysmon-config.xml

# Vérifier que le service est actif
Get-Service Sysmon64

# Voir les événements générés immédiatement
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 10 | Format-List TimeCreated, Id, Message
```

<br>

---

## Les événements critiques pour un SOC

Sysmon génère plus de 30 types d'événements. Voici les **plus importants** pour la détection :

| Event ID | Nom | Ce qu'il détecte | Priorité SOC |
|---|---|---|---|
| **1** | ProcessCreate | Tout nouveau processus (hash, parent, cmdline) | 🔴 Critique |
| **3** | NetworkConnect | Connexions réseau initiées par processus | 🔴 Critique |
| **7** | ImageLoad | DLL chargées (détection DLL hijacking) | 🟠 Élevée |
| **8** | CreateRemoteThread | Injection de thread dans un autre processus | 🔴 Critique |
| **10** | ProcessAccess | Accès mémoire entre processus (credential dumping) | 🔴 Critique |
| **11** | FileCreate | Création de fichiers (payloads droppés) | 🟡 Moyenne |
| **12/13** | RegistryEvent | Modifications registre (persistance) | 🟠 Élevée |
| **15** | FileCreateStreamHash | Fichiers avec Zone.Identifier (téléchargés) | 🟡 Moyenne |
| **17/18** | PipeEvent | Création/connexion de named pipes (C2, latmov) | 🟠 Élevée |
| **22** | DNSQuery | Requêtes DNS par processus (C2, DNS tunneling) | 🔴 Critique |
| **25** | ProcessTampering | Tentative d'effacement d'image processus | 🔴 Critique |

<br>

---

## Configuration XML Sysmon

La puissance de Sysmon vient de sa configuration XML flexible — on peut **inclure ou exclure** n'importe quel événement selon des critères précis pour réduire le bruit.

```xml title="sysmon-config-soc.xml — Configuration orientée détection SOC"
<Sysmon schemaversion="4.82">

  <!-- Hashing : SHA256 pour les fichiers, MD5 pour la compatibilité CTI -->
  <HashAlgorithms>sha256,md5</HashAlgorithms>
  <CheckRevocation/>  <!-- Vérifier les signatures de code -->

  <EventFiltering>

    <!-- ================================================================
         Event ID 1 — Création de processus
         Exclure les processus système très bruyants (antivirus, update)
         ================================================================ -->
    <RuleGroup name="ProcessCreate" groupRelation="or">
      <ProcessCreate onmatch="exclude">
        <!-- Exclure les processus légitimes qui créent beaucoup de sous-processus -->
        <Image condition="is">C:\Windows\System32\svchost.exe</Image>
        <Image condition="is">C:\Windows\System32\WerFault.exe</Image>
        <ParentImage condition="is">C:\Program Files\Windows Defender\MsMpEng.exe</ParentImage>
      </ProcessCreate>
    </RuleGroup>

    <!-- ================================================================
         Event ID 3 — Connexions réseau
         Monitorer les processus qui NE devraient PAS faire du réseau
         ================================================================ -->
    <RuleGroup name="NetworkConnect" groupRelation="or">
      <NetworkConnect onmatch="include">
        <!-- Alerter si Word/Excel se connecte à Internet -->
        <Image condition="contains">WINWORD.EXE</Image>
        <Image condition="contains">EXCEL.EXE</Image>
        <!-- Alerter si PowerShell se connecte (hors port 80/443 légitimes) -->
        <Image condition="end with">powershell.exe</Image>
        <!-- Connexions réseau de cmd.exe = très suspect -->
        <Image condition="end with">cmd.exe</Image>
      </NetworkConnect>
    </RuleGroup>

    <!-- ================================================================
         Event ID 10 — Accès mémoire entre processus
         Technique de credential dumping (LSASS)
         ================================================================ -->
    <RuleGroup name="ProcessAccess" groupRelation="or">
      <ProcessAccess onmatch="include">
        <!-- Tout processus qui accède à LSASS = credential dumping potentiel -->
        <TargetImage condition="end with">lsass.exe</TargetImage>
      </ProcessAccess>
    </RuleGroup>

    <!-- ================================================================
         Event ID 22 — Requêtes DNS
         Détecter le DNS tunneling et les domaines C2
         ================================================================ -->
    <RuleGroup name="DnsQuery" groupRelation="or">
      <DnsQuery onmatch="exclude">
        <!-- Exclure les domaines Microsoft légitimes -->
        <QueryName condition="end with">.microsoft.com</QueryName>
        <QueryName condition="end with">.windows.com</QueryName>
        <QueryName condition="end with">.windowsupdate.com</QueryName>
      </DnsQuery>
    </RuleGroup>

  </EventFiltering>
</Sysmon>
```

_Cette configuration utilise une stratégie **include/exclude** : par défaut Sysmon capture tout, vous excluez le bruit connu pour rester focalisé sur les événements suspects._

<br>

---

## Intégration avec Wazuh

Une fois Sysmon installé, l'agent Wazuh sur Windows collecte automatiquement ses événements via le canal **Microsoft-Windows-Sysmon/Operational**.

```xml title="ossec.conf (agent Windows) — Activer la collecte Sysmon"
<ossec_config>

  <!-- Collecter les événements Sysmon via Windows Event Log -->
  <localfile>
    <location>Microsoft-Windows-Sysmon/Operational</location>
    <log_format>eventchannel</log_format>
    <!-- Collecte uniquement les nouveaux événements (depuis l'installation de l'agent) -->
    <only-future-events>yes</only-future-events>
  </localfile>

</ossec_config>
```

### Règles Wazuh dédiées à Sysmon

Wazuh inclut nativement des règles pour les événements Sysmon. Vous pouvez en ajouter :

```xml title="local_rules.xml — Règles Wazuh basées sur les Event IDs Sysmon"
<group name="sysmon,windows,">

  <!-- Event ID 10 : Accès à LSASS = Credential Dumping -->
  <rule id="100050" level="15">
    <if_group>sysmon</if_group>
    <field name="win.system.eventID">10</field>
    <field name="win.eventdata.targetImage" type="pcre2">(?i)lsass\.exe</field>
    <description>CRITIQUE : Accès mémoire à LSASS — possible credential dumping (Mimikatz)</description>
    <mitre>
      <id>T1003.001</id>  <!-- OS Credential Dumping: LSASS Memory -->
    </mitre>
  </rule>

  <!-- Event ID 1 : PowerShell encodé (T1059.001) -->
  <rule id="100051" level="12">
    <if_group>sysmon</if_group>
    <field name="win.system.eventID">1</field>
    <field name="win.eventdata.image" type="pcre2">(?i)powershell\.exe</field>
    <field name="win.eventdata.commandLine" type="pcre2">(?i)(-enc|-encodedcommand|-e\s+[A-Za-z0-9+/=]{20,})</field>
    <description>PowerShell encodé détecté — possible obfuscation malveillante</description>
    <mitre>
      <id>T1059.001</id>  <!-- Command and Scripting: PowerShell -->
      <id>T1027</id>      <!-- Obfuscated Files or Information -->
    </mitre>
  </rule>

</group>
```

<br>

---

## Mettre à jour la configuration

```powershell title="Mettre à jour la config Sysmon sans redémarrage"
# Appliquer une nouvelle configuration à chaud
Sysmon64.exe -c C:\Temp\nouvelle-config.xml

# Vérifier la configuration active
Sysmon64.exe -s

# Désinstaller proprement (si nécessaire)
Sysmon64.exe -u
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Sysmon est **indispensable** dans tout SOC surveillant des endpoints Windows. Sans lui, vous voyez des événements tronqués : un processus créé sans son hash, une connexion réseau sans le processus source. Avec Sysmon, chaque événement devient une **empreinte complète** permettant une investigation précise. La configuration SwiftOnSecurity est un excellent point de départ — peaufinez-la selon votre environnement.

> Continuez avec **[YARA →](./yara.md)** pour apprendre à écrire des signatures de détection de malwares sur les fichiers que Sysmon vous a permis d'identifier.

<br>