---
title: 2.5 PowerShell pour analyste forensic
description: PowerShell appliqué au forensic Windows - cmdlets essentiels, modules forensic, scripts d'investigation, automatisation. Outil principal de l'analyste sur poste Windows.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - PowerShell
  - Windows
  - Scripting
  - Forensic
data-level: 🟡
---

# 2.5 PowerShell pour analyste forensic

!!! quote "L'analogie du couteau suisse"

    PowerShell est le couteau suisse de l'analyste Windows. Plus puissant que cmd, plus moderne que VBS, mieux intégré que Python sur Windows. Il accède au registre, aux WMI, aux Event Logs, aux processus, aux services, à .NET. Une bonne maîtrise transforme votre productivité forensic.

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 6 heures |
| Niveau | Standard |
| Prérequis | 2.4 |

## 1. Bases du langage

### 1.1 Cmdlets

PowerShell utilise une convention `Verbe-Nom` :

```powershell
Get-Process       # liste processus
Get-Service       # liste services
Get-WinEvent      # logs événements
Get-ChildItem     # liste fichiers (alias ls, dir)
Stop-Process      # arrête processus
```

### 1.2 Pipeline objet

Contrairement à bash qui pipe du texte, PowerShell pipe **des objets** :

```powershell
# Bash style (texte)
ps aux | grep nginx | awk '{print $2}'

# PowerShell (objets)
Get-Process nginx | Select-Object Id, Name, Path
```

### 1.3 Variables et types

```powershell
$processus = Get-Process
$processus.Count                    # nombre
$processus | Get-Member             # méthodes/propriétés disponibles
$processus[0].Name                  # accès direct

# Types stricts
[int]$age = 30
[string]$nom = "Zyrass"
[datetime]$now = Get-Date
```

### 1.4 Filtres

```powershell
# Where-Object (filtrage)
Get-Process | Where-Object { $_.WorkingSet -gt 100MB }

# Select-Object (projection)
Get-Service | Select-Object Name, Status, StartType

# Sort-Object
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Group-Object
Get-Process | Group-Object Company | Sort-Object Count -Descending
```

## 2. Cmdlets forensic essentiels

### 2.1 Processus

```powershell
# Tous les processus avec chemin
Get-Process | Select-Object Name, Id, Path, Company

# Avec ligne de commande (WMI/CIM)
Get-CimInstance Win32_Process | 
    Select-Object ProcessId, Name, CommandLine, ExecutablePath, ParentProcessId

# Processus suspects (chemin temp/appdata)
Get-Process | Where-Object {
    $_.Path -match "temp|appdata|users\\public" -and $_.Path
} | Select-Object Name, Id, Path

# Arborescence parent-enfant
function Get-ProcessTree {
    Get-CimInstance Win32_Process | 
        Select-Object ProcessId, ParentProcessId, Name, ExecutablePath, CommandLine |
        Sort-Object ParentProcessId
}
```

### 2.2 Services

```powershell
# Services en cours
Get-Service | Where-Object Status -eq Running

# Services au chemin suspect
Get-CimInstance Win32_Service | 
    Where-Object { $_.PathName -match "temp|appdata|users\\public" } |
    Select-Object Name, State, PathName, StartName

# Services modifiés récemment (par registre)
Get-ChildItem "HKLM:\System\CurrentControlSet\Services" |
    Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-30) } |
    Select-Object PSChildName, LastWriteTime
```

### 2.3 Registre

```powershell
# Lecture
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

# Recherche
Get-ChildItem "HKLM:\SOFTWARE" -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "suspicious_keyword" }

# Tâches planifiées via registre
Get-ScheduledTask | Where-Object State -ne Disabled |
    Select-Object TaskName, TaskPath, State, Author
```

### 2.4 Event Logs

```powershell
# Failed logons (4625) derniers 7 jours
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    ID=4625
    StartTime=(Get-Date).AddDays(-7)
} -MaxEvents 100 | Select-Object TimeCreated, Message

# PowerShell ScriptBlock logging (4104)
Get-WinEvent -FilterHashtable @{
    LogName='Microsoft-Windows-PowerShell/Operational'
    ID=4104
} -MaxEvents 50 | Select-Object TimeCreated, Message

# Services nouvellement installés (7045)
Get-WinEvent -FilterHashtable @{
    LogName='System'
    ID=7045
} | Select-Object TimeCreated, Message

# Audit cleared (1102) - critique !
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=1102}
```

### 2.5 Réseau

```powershell
# Connexions TCP établies
Get-NetTCPConnection | Where-Object State -eq Established

# Avec PID
Get-NetTCPConnection | Where-Object State -eq Established |
    Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess

# Croiser avec processus
$conn = Get-NetTCPConnection | Where-Object State -eq Established
$conn | ForEach-Object {
    $proc = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
    [PSCustomObject]@{
        LocalAddr = "$($_.LocalAddress):$($_.LocalPort)"
        RemoteAddr = "$($_.RemoteAddress):$($_.RemotePort)"
        Process = $proc.Name
        Path = $proc.Path
    }
}
```

## 3. Modules forensic communautaires

| Module | Usage |
|---|---|
| Kansa | Triage IR à grande échelle |
| PowerForensics | Forensic disque NTFS |
| PSReflect | Manipulations bas niveau |
| InvokeATT&CK | Tests MITRE |
| AtomicTestHarnesses | Tests Atomic Red Team |

## 4. Script d'audit forensic complet

```powershell
function Invoke-ForensicAudit {
    param(
        [string]$OutputPath = "$env:TEMP\forensic_audit.json"
    )

    $report = @{
        Timestamp = Get-Date -Format o
        Hostname = $env:COMPUTERNAME
        Users = Get-LocalUser | Select-Object Name, Enabled, LastLogon, PasswordLastSet
        Admins = Get-LocalGroupMember -Group Administrators | Select-Object Name, ObjectClass
        AutoRunHKLM = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue
        AutoRunHKCU = Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue
        SuspiciousServices = Get-CimInstance Win32_Service | 
            Where-Object { $_.PathName -match "temp|appdata|users\\public" } |
            Select-Object Name, State, PathName
        ScheduledTasks = Get-ScheduledTask | Where-Object State -ne Disabled |
            Select-Object TaskName, TaskPath, State
        TopMemoryProcesses = Get-Process | Sort-Object WorkingSet -Descending |
            Select-Object -First 20 Name, Id, Path
        EstablishedConnections = Get-NetTCPConnection | 
            Where-Object State -eq Established |
            Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess
    }

    $report | ConvertTo-Json -Depth 5 | Out-File $OutputPath
    Write-Host "Rapport: $OutputPath"
    Get-FileHash $OutputPath -Algorithm SHA256
}

Invoke-ForensicAudit
```

## 5. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Convention de nommage cmdlets ? | Verbe-Nom |
| 2 | Différence avec bash ? | Pipeline objet vs texte |
| 3 | Cmdlet pour Event Logs ? | Get-WinEvent |
| 4 | Cmdlet pour processus avec ligne de commande ? | Get-CimInstance Win32_Process |
| 5 | Comment filtrer ? | Where-Object |

## 6. Synthèse

```text
POWERSHELL FORENSIC

Cmdlets clés :
  Get-Process / Get-CimInstance Win32_Process
  Get-Service / Win32_Service
  Get-WinEvent
  Get-NetTCPConnection
  Get-ScheduledTask
  Get-ItemProperty (registre)

Filtres :
  Where-Object
  Select-Object
  Sort-Object
  Group-Object

Modules utiles :
  Kansa, PowerForensics, InvokeATT&CK
```

---

**Chapitre suivant** : [2.5 bis Bash et zsh pour analyste macOS](02-5bis-bash-zsh.md)
