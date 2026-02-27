---
description: "PowerShell : shell automation Windows, scripting production, gestion infrastructure, DevOps"
icon: lucide/book-open-check
tags: ["POWERSHELL", "WINDOWS", "SCRIPTING", "AUTOMATION", "DEVOPS", "ADMINISTRATION"]
---

# PowerShell

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-time="10-12 heures"
  data-version="1.0">
</div>

## Introduction aux Fondamentaux de PowerShell

!!! quote "Analogie pédagogique"
    _Imaginez un **chef d'orchestre symphonique dirigeant orchestre moderne avec instruments numériques connectés** : PowerShell fonctionne comme **langage coordination orchestrant infrastructure Windows/Azure/cloud avec objets structurés (pas simple texte)** selon partition précise (scripts). **Chef orchestre concert numérique** : partition avec notations riches (cmdlets verbe-nom), instruments connectés MIDI (objets .NET structurés), communication bidirectionnelle temps réel (pipeline objets pas texte), partition interactive modifiable en direct (console REPL), bibliothèque infinie partitions (modules PowerShell Gallery 10,000+), enregistrement performances (transcripts logs), synchronisation multi-orchestres distants (PowerShell Remoting), automation complète répétitions (scheduled tasks/DSC). **Sans PowerShell Windows** : tâches répétitives manuelles GUI (cliquer 50 fois même action), scripts batch limités (cmd.exe archaïque texte seulement), VBScript obsolète complexe, non-scalable (gérer 1000 serveurs impossible manuellement), erreurs humaines (oubli étape critique backup), non-reproductible (collègue absent = procédure perdue). **Avec PowerShell** : **Automation complète** (gérer Active Directory 10,000 users via script), **Objets structurés** (manipuler propriétés directement pas parsing texte), **Remoting natif** (exécuter commandes 1000 serveurs simultanément), **Modules réutilisables** (PSGallery 10K+ modules communauté), **Pipeline puissant** (filtrer/transformer/exporter objets chaînés), **Cross-platform** (PowerShell Core 7+ = Linux/macOS/Windows), **Integration cloud** (Azure/AWS/GCP modules officiels), **DSC** (Desired State Configuration infrastructure as code), **Error handling robuste** (try/catch/finally comme langages modernes). **PowerShell = standard automation Microsoft** : utilisé Azure automation, Exchange Online, Active Directory, Microsoft 365, System Center, Windows Server, SQL Server, IIS, 95% infrastructure Microsoft mondiale. **Différence fondamentale vs Bash** : Bash = texte/strings (parsing difficile), PowerShell = objets .NET (propriétés directes). Bash pipeline = texte brut, PowerShell pipeline = objets typés. **Puissance PowerShell** : 15+ ans développement (2006 Jeffrey Snover Microsoft), cross-platform depuis 2016 (PowerShell Core open-source), syntaxe moderne C#-like, écosystème mature (10K+ modules), performance native .NET, debugging intégré (ISE/VSCode), communauté massive Microsoft._

**PowerShell en résumé :**

- ✅ **Shell moderne** = Windows, Linux, macOS (PowerShell 7+)
- ✅ **Orienté objets** = Pipeline objets .NET (pas texte)
- ✅ **Cmdlets** = Verbe-Nom (Get-Process, Set-Service, etc.)
- ✅ **Remoting** = Gestion serveurs distants natif (WinRM/SSH)
- ✅ **Modules** = 10,000+ PowerShell Gallery (communauté)
- ✅ **Cloud-ready** = Azure, AWS, GCP modules officiels
- ✅ **DSC** = Infrastructure as Code déclaratif
- ✅ **Production-ready** = Error handling, logging, transcripts

**Guide structure :**

1. Introduction et concepts PowerShell
2. Variables, types et objets .NET
3. Structures de contrôle
4. Fonctions et modules
5. Pipeline et manipulation objets
6. Fichiers, registre et I/O
7. Text processing et regex
8. Paramètres et validation
9. Debugging et error handling
10. Remoting et background jobs
11. Best practices et sécurité
12. Cas pratiques production

---

## Section 1 : Introduction et Concepts

### 1.1 Qu'est-ce que PowerShell ?

**PowerShell = Shell automation et scripting basé objets .NET**

```
Historique PowerShell :

2006 : PowerShell 1.0 (Windows PowerShell, Monad)
2009 : PowerShell 2.0 (Remoting, ISE, modules)
2012 : PowerShell 3.0 (Workflows, CIM)
2013 : PowerShell 4.0 (Desired State Configuration)
2016 : PowerShell 5.1 (Windows PowerShell final version)
2016 : PowerShell Core 6.0 (cross-platform, open-source)
2020 : PowerShell 7.0 (unified, .NET Core 3.1)
2024 : PowerShell 7.4+ (current, .NET 8)

PowerShell vs Windows PowerShell :
- Windows PowerShell 5.1 : Windows-only, .NET Framework, final
- PowerShell 7+ : Cross-platform, .NET Core, future
```

**Différence fondamentale : Objets vs Texte**

```powershell
# Bash : texte (parsing requis)
ps aux | grep nginx | awk '{print $2}'

# PowerShell : objets (propriétés directes)
Get-Process -Name nginx | Select-Object -Property Id

# Bash pipeline = strings
ls -l | grep ".txt" | wc -l

# PowerShell pipeline = objets
Get-ChildItem -Filter *.txt | Measure-Object

# Exemple concret différence :
# Bash
date=$(date +%Y-%m-%d)
echo "Date: $date"

# PowerShell
$date = Get-Date -Format "yyyy-MM-dd"
Write-Output "Date: $date"

# Mais surtout :
# Bash : date est STRING
# PowerShell : Get-Date retourne objet DateTime avec propriétés

$now = Get-Date
$now.Year          # 2024
$now.Month         # 1
$now.DayOfWeek     # Tuesday
$now.AddDays(7)    # Objet DateTime +7 jours
```

### 1.2 Cmdlets et Syntaxe

**Cmdlet = Commande PowerShell format Verbe-Nom**

```powershell
# Format standard : Verbe-Nom
Get-Process
Set-Service
New-Item
Remove-User

# Verbes approuvés (Get-Verb)
Get     # Récupérer données
Set     # Modifier données
New     # Créer ressource
Remove  # Supprimer ressource
Start   # Démarrer service/process
Stop    # Arrêter
Enable  # Activer
Disable # Désactiver
Import  # Importer données
Export  # Exporter données
Test    # Tester condition
Invoke  # Exécuter action

# Paramètres nommés
Get-Process -Name "powershell"
Get-ChildItem -Path C:\Temp -Filter "*.log"

# Paramètres positionnels (ordre important)
Get-Process powershell
Get-ChildItem C:\Temp *.log

# Paramètres switch (boolean)
Get-ChildItem -Recurse      # -Recurse:$true
Get-ChildItem -Recurse:$false

# Aliases (raccourcis)
ls      # Alias de Get-ChildItem
dir     # Alias de Get-ChildItem
gci     # Alias de Get-ChildItem
ps      # Alias de Get-Process
cat     # Alias de Get-Content
cd      # Alias de Set-Location

# Help system
Get-Help Get-Process
Get-Help Get-Process -Full
Get-Help Get-Process -Examples
Get-Help Get-Process -Online

# Update help
Update-Help  # Télécharge aide à jour
```

### 1.3 Console vs Scripts

**Mode interactif (console) :**

```powershell
# Console PowerShell
PS C:\> Get-Date
Tuesday, January 16, 2024 2:30:45 PM

PS C:\> Get-Process | Where-Object {$_.CPU -gt 100}
# Résultats interactifs

# REPL (Read-Eval-Print Loop)
PS C:\> 2 + 2
4

PS C:\> "Hello" * 3
HelloHelloHello
```

**Mode script (.ps1) :**

```powershell
# Script : backup.ps1

# Shebang pas nécessaire PowerShell
# Mais indication utile

<#
.SYNOPSIS
    Automated backup script
.DESCRIPTION
    Backs up specified directory to destination
.PARAMETER Source
    Source directory path
.PARAMETER Destination
    Destination backup path
.EXAMPLE
    .\backup.ps1 -Source C:\Data -Destination D:\Backup
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Source,
    
    [Parameter(Mandatory=$true)]
    [string]$Destination
)

# Script logic
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = Join-Path $Destination "backup_$timestamp"

Write-Host "Creating backup: $Source -> $backupPath"
Copy-Item -Path $Source -Destination $backupPath -Recurse

Write-Host "Backup completed successfully"

# Exécution :
# .\backup.ps1 -Source C:\Data -Destination D:\Backup
```

### 1.4 Execution Policy

**Sécurité scripts PowerShell**

```powershell
# Voir policy actuelle
Get-ExecutionPolicy

# Policies disponibles :
# Restricted    : Aucun script (default Windows client)
# AllSigned     : Seulement scripts signés
# RemoteSigned  : Scripts locaux OK, remote signés requis
# Unrestricted  : Tous scripts (warning remote)
# Bypass        : Aucune restriction

# Changer policy (Admin requis)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Scopes :
# Process       : Session actuelle seulement
# CurrentUser   : Utilisateur actuel
# LocalMachine  : Tous utilisateurs machine

# Bypass temporaire (développement)
powershell.exe -ExecutionPolicy Bypass -File script.ps1

# Unblock fichier téléchargé
Unblock-File -Path .\script.ps1

# Signer script (production)
$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert
Set-AuthenticodeSignature -FilePath script.ps1 -Certificate $cert
```

---

## Section 2 : Variables, Types et Objets

### 2.1 Variables

```powershell
# Déclaration simple
$name = "John Doe"
$age = 30
$isActive = $true

# Typage explicite (optionnel mais recommandé)
[string]$name = "John"
[int]$age = 30
[bool]$isActive = $true

# Types .NET communs
[string]     # System.String
[int]        # System.Int32
[long]       # System.Int64
[double]     # System.Double
[decimal]    # System.Decimal
[bool]       # System.Boolean
[datetime]   # System.DateTime
[array]      # System.Array
[hashtable]  # System.Collections.Hashtable

# Variables automatiques (built-in)
$PSVersionTable      # Version PowerShell
$Home               # Home directory user
$PWD                # Current directory
$PID                # Process ID PowerShell
$Host               # Host information
$Error              # Array dernières erreurs
$_                  # Current pipeline object
$args               # Array arguments
$true / $false      # Boolean
$null               # Null

# Portée (scope)
$global:var = "global"      # Scope global
$script:var = "script"      # Scope script
$local:var = "local"        # Scope local (default)
$private:var = "private"    # Private scope

# Variables environnement
$env:PATH
$env:COMPUTERNAME
$env:USERNAME
$env:TEMP

# Set environment variable
$env:MY_VAR = "value"

# Permanent (System level - Admin)
[Environment]::SetEnvironmentVariable("MY_VAR", "value", "Machine")

# Permanent (User level)
[Environment]::SetEnvironmentVariable("MY_VAR", "value", "User")

# Constant et readonly
Set-Variable -Name PI -Value 3.14159 -Option Constant
Set-Variable -Name Config -Value "prod" -Option ReadOnly

# Remove variable
Remove-Variable -Name temp
```

### 2.2 Types et Objets .NET

```powershell
# Tout est objet .NET
$number = 42
$number.GetType()
# TypeName: System.Int32

# Propriétés et méthodes
$text = "Hello World"
$text.Length              # 11
$text.ToUpper()           # HELLO WORLD
$text.Replace("World", "PowerShell")  # Hello PowerShell
$text.Split(" ")          # Array: Hello, World

# DateTime objet
$now = Get-Date
$now.Year                 # 2024
$now.Month                # 1
$now.DayOfWeek            # Tuesday
$now.AddDays(7)           # +7 jours
$now.ToString("yyyy-MM-dd")  # 2024-01-16

# Get-Member : explorer objet
$process = Get-Process -Name powershell
$process | Get-Member

# Output :
# TypeName: System.Diagnostics.Process
# Name              MemberType
# ----              ----------
# Kill              Method
# WaitForExit       Method
# CPU               Property
# Id                Property
# Name              Property
# ...

# Cast types
[int]"42"                 # String to int
[string]42                # Int to string
[datetime]"2024-01-16"    # String to datetime

# Test types
$value = 42
$value -is [int]          # True
$value -is [string]       # False
```

### 2.3 Arrays

```powershell
# Array création
$fruits = @("apple", "banana", "cherry")
$numbers = @(1, 2, 3, 4, 5)
$mixed = @(1, "two", 3.0, $true)

# Array vide
$empty = @()

# Access elements
$fruits[0]                # apple
$fruits[1]                # banana
$fruits[-1]               # cherry (last)

# Length
$fruits.Count             # 3
$fruits.Length            # 3

# Ajouter élément (ATTENTION: arrays immutables)
$fruits += "date"         # Crée nouveau array
# Better: utiliser ArrayList

# ArrayList (mutable)
$list = [System.Collections.ArrayList]@()
$list.Add("apple")
$list.Add("banana")
$list.Remove("apple")
$list.Insert(0, "cherry")

# Array range
$range = 1..10            # 1, 2, 3, ..., 10
$range = 10..1            # 10, 9, 8, ..., 1

# Array operations
$combined = $fruits + $numbers        # Concatenation
$fruits -contains "apple"             # True
$fruits -notcontains "grape"          # True

# Iteration
foreach ($fruit in $fruits) {
    Write-Output $fruit
}

# Array methods
$numbers.Sum()            # Somme (PSv5+)
$numbers.Where({$_ -gt 3})   # Filter
$numbers.ForEach({$_ * 2})   # Map
```

### 2.4 Hashtables (Dictionnaires)

```powershell
# Hashtable création
$user = @{
    Name = "John Doe"
    Age = 30
    Email = "john@example.com"
    IsActive = $true
}

# Access values
$user["Name"]             # John Doe
$user.Name                # John Doe (dot notation)

# Add/modify
$user["Department"] = "IT"
$user.Salary = 50000

# Remove key
$user.Remove("Salary")

# Test key exists
$user.ContainsKey("Name")      # True
$user.ContainsKey("Salary")    # False

# Keys et values
$user.Keys
$user.Values

# Iteration
foreach ($key in $user.Keys) {
    Write-Output "$key = $($user[$key])"
}

# Ordered hashtable (maintient ordre insertion)
$ordered = [ordered]@{
    First = 1
    Second = 2
    Third = 3
}

# Nested hashtables
$config = @{
    Database = @{
        Server = "localhost"
        Port = 5432
        Name = "mydb"
    }
    Logging = @{
        Level = "Info"
        Path = "C:\Logs"
    }
}

$config.Database.Server   # localhost
```

---

## Section 3 : Structures de Contrôle

### 3.1 Conditions (if/else)

```powershell
# If basique
if ($age -gt 18) {
    Write-Output "Adult"
}

# If/else
if ($age -ge 18) {
    Write-Output "Adult"
} else {
    Write-Output "Minor"
}

# If/elseif/else
if ($score -ge 90) {
    Write-Output "A"
} elseif ($score -ge 80) {
    Write-Output "B"
} elseif ($score -ge 70) {
    Write-Output "C"
} else {
    Write-Output "F"
}

# Opérateurs comparaison
-eq     # Equal
-ne     # Not equal
-gt     # Greater than
-ge     # Greater or equal
-lt     # Less than
-le     # Less or equal
-like   # Wildcard match
-notlike
-match  # Regex match
-notmatch
-contains
-notcontains
-in     # Value in array
-notin

# Case sensitive versions (ajouter 'c')
-ceq    # Case-sensitive equal
-clike
-cmatch

# Exemples
$name -eq "John"
$name -like "J*"
$name -match "^[A-Z]"
5 -in @(1,2,3,4,5)

# Test fichiers
if (Test-Path "C:\file.txt") {
    Write-Output "File exists"
}

# Opérateurs logiques
-and
-or
-not  # ou !
-xor

# Exemples
if ($age -gt 18 -and $isActive) {
    Write-Output "Active adult"
}

if (-not $isDeleted) {
    Write-Output "Not deleted"
}

if (!$isDeleted) {  # Même chose
    Write-Output "Not deleted"
}

# Ternary operator (PowerShell 7+)
$result = $age -ge 18 ? "Adult" : "Minor"
```

### 3.2 Switch Statement

```powershell
# Switch basique
switch ($color) {
    "red"   { Write-Output "Stop" }
    "yellow" { Write-Output "Caution" }
    "green" { Write-Output "Go" }
    default { Write-Output "Unknown" }
}

# Switch avec multiples valeurs
switch ($fruit) {
    "apple"  { Write-Output "Fruit" }
    "banana" { Write-Output "Fruit" }
    "carrot" { Write-Output "Vegetable" }
}

# Switch regex
switch -Regex ($input) {
    "^[0-9]+$"      { Write-Output "Number" }
    "^[A-Za-z]+$"   { Write-Output "Letters" }
    default         { Write-Output "Mixed" }
}

# Switch wildcard
switch -Wildcard ($filename) {
    "*.txt"  { Write-Output "Text file" }
    "*.log"  { Write-Output "Log file" }
    "*.ps1"  { Write-Output "PowerShell script" }
}

# Switch avec array (teste chaque élément)
$items = @("apple", "banana", "carrot")
switch ($items) {
    "apple"  { Write-Output "Found apple" }
    "banana" { Write-Output "Found banana" }
}

# Switch file content
switch -File "C:\file.txt" {
    "ERROR"   { Write-Output "Error found: $_" }
    "WARNING" { Write-Output "Warning found: $_" }
}
```

### 3.3 Loops

```powershell
# For loop
for ($i = 0; $i -lt 10; $i++) {
    Write-Output "Count: $i"
}

# Foreach loop (array)
$fruits = @("apple", "banana", "cherry")
foreach ($fruit in $fruits) {
    Write-Output $fruit
}

# ForEach-Object (pipeline)
1..10 | ForEach-Object {
    Write-Output "Number: $_"
}

# Alias : foreach, %
1..10 | foreach { $_ * 2 }
1..10 | % { $_ * 2 }

# While loop
$count = 1
while ($count -le 5) {
    Write-Output "Count: $count"
    $count++
}

# Do-While (execute au moins une fois)
$count = 1
do {
    Write-Output "Count: $count"
    $count++
} while ($count -le 5)

# Do-Until
$count = 1
do {
    Write-Output "Count: $count"
    $count++
} until ($count -gt 5)

# Break
for ($i = 0; $i -lt 10; $i++) {
    if ($i -eq 5) { break }
    Write-Output $i
}

# Continue
for ($i = 0; $i -lt 10; $i++) {
    if ($i -eq 5) { continue }
    Write-Output $i
}

# Break avec label
:outer foreach ($i in 1..3) {
    foreach ($j in 1..3) {
        if ($i -eq 2 -and $j -eq 2) {
            break outer
        }
        Write-Output "$i,$j"
    }
}
```

## Section 4 : Fonctions et Modules

### 4.1 Fonctions Basiques

```powershell
# Fonction simple
function Get-Greeting {
    Write-Output "Hello, World!"
}

# Appeler fonction
Get-Greeting

# Fonction avec paramètres
function Get-UserGreeting {
    param(
        [string]$Name
    )
    Write-Output "Hello, $Name!"
}

Get-UserGreeting -Name "John"

# Fonction avec return
function Get-Square {
    param([int]$Number)
    return $Number * $Number
}

$result = Get-Square -Number 5
Write-Output $result  # 25

# Fonction avec multiple parameters
function New-User {
    param(
        [string]$FirstName,
        [string]$LastName,
        [int]$Age
    )
    
    $fullName = "$FirstName $LastName"
    Write-Output "Created user: $fullName (Age: $Age)"
}

New-User -FirstName "John" -LastName "Doe" -Age 30

# Paramètres positionnels
function Add-Numbers {
    param(
        [Parameter(Position=0)]
        [int]$First,
        
        [Parameter(Position=1)]
        [int]$Second
    )
    return $First + $Second
}

Add-Numbers 5 3        # Positional
Add-Numbers -First 5 -Second 3  # Named
```

### 4.2 Fonctions Avancées

```powershell
# Advanced function (cmdlet-like)
function Get-SystemInfo {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$ComputerName,
        
        [Parameter(Mandatory=$false)]
        [switch]$IncludeDisk
    )
    
    begin {
        Write-Verbose "Starting system info collection"
    }
    
    process {
        $os = Get-CimInstance -ClassName Win32_OperatingSystem -ComputerName $ComputerName
        
        $info = [PSCustomObject]@{
            ComputerName = $ComputerName
            OS = $os.Caption
            Version = $os.Version
            LastBoot = $os.LastBootUpTime
        }
        
        if ($IncludeDisk) {
            $disk = Get-CimInstance -ClassName Win32_LogicalDisk -ComputerName $ComputerName |
                Where-Object {$_.DriveType -eq 3}
            $info | Add-Member -MemberType NoteProperty -Name DiskInfo -Value $disk
        }
        
        return $info
    }
    
    end {
        Write-Verbose "Completed system info collection"
    }
}

# Usage
Get-SystemInfo -ComputerName "localhost" -Verbose
Get-SystemInfo -ComputerName "localhost" -IncludeDisk

# Pipeline support
function Get-ProcessMemory {
    [CmdletBinding()]
    param(
        [Parameter(
            Mandatory=$true,
            ValueFromPipeline=$true,
            ValueFromPipelineByPropertyName=$true
        )]
        [string]$Name
    )
    
    process {
        Get-Process -Name $Name | Select-Object Name, @{
            Name='MemoryMB'
            Expression={[math]::Round($_.WorkingSet64 / 1MB, 2)}
        }
    }
}

# Pipeline usage
"powershell", "chrome" | Get-ProcessMemory
Get-Process | Get-ProcessMemory

# Validation attributes
function Set-UserAge {
    param(
        [Parameter(Mandatory=$true)]
        [ValidateRange(0, 150)]
        [int]$Age,
        
        [Parameter(Mandatory=$true)]
        [ValidateLength(1, 50)]
        [string]$Name,
        
        [Parameter(Mandatory=$true)]
        [ValidatePattern('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')]
        [string]$Email
    )
    
    Write-Output "User: $Name, Age: $Age, Email: $Email"
}

# Default parameter values
function Connect-Database {
    param(
        [string]$Server = "localhost",
        [int]$Port = 5432,
        [string]$Database = "postgres"
    )
    
    Write-Output "Connecting to $Server`:$Port/$Database"
}

Connect-Database  # Uses defaults
Connect-Database -Server "prod-db" -Port 3306
```

### 4.3 Modules

```powershell
# Module = collection de fonctions/cmdlets

# Créer module
# File: MyModule.psm1

function Get-CustomGreeting {
    param([string]$Name)
    "Hello from module, $Name!"
}

function Set-CustomConfig {
    param([string]$Value)
    Write-Output "Config set: $Value"
}

Export-ModuleMember -Function Get-CustomGreeting, Set-CustomConfig

# Importer module
Import-Module .\MyModule.psm1

# Utiliser fonctions module
Get-CustomGreeting -Name "John"

# Voir modules chargés
Get-Module

# Voir modules disponibles
Get-Module -ListAvailable

# Supprimer module
Remove-Module MyModule

# Module avec manifest (.psd1)
# File: MyModule.psd1
@{
    ModuleVersion = '1.0.0'
    GUID = 'a1b2c3d4-...'
    Author = 'Your Name'
    Description = 'Custom module description'
    RootModule = 'MyModule.psm1'
    FunctionsToExport = @('Get-CustomGreeting', 'Set-CustomConfig')
    VariablesToExport = @()
    CmdletsToExport = @()
}

# PowerShell Gallery (repository officiel)
# Rechercher module
Find-Module -Name Az

# Installer module
Install-Module -Name Az -Scope CurrentUser

# Update module
Update-Module -Name Az

# Modules système importants
Import-Module ActiveDirectory    # AD management
Import-Module Az                  # Azure
Import-Module Exchange           # Exchange Online
Import-Module Microsoft.Graph    # Microsoft 365

# Auto-import (PSModulePath)
$env:PSModulePath
# C:\Users\User\Documents\PowerShell\Modules;
# C:\Program Files\PowerShell\Modules;
# ...
```

### 4.4 Dot Sourcing

```powershell
# Dot sourcing = exécute script dans scope actuel

# File: functions.ps1
function Get-CustomDate {
    Get-Date -Format "yyyy-MM-dd"
}

function Get-CustomTime {
    Get-Date -Format "HH:mm:ss"
}

# Sans dot sourcing (sub-scope)
.\functions.ps1
Get-CustomDate  # ERROR: Command not found

# Avec dot sourcing (current scope)
. .\functions.ps1
Get-CustomDate  # OK: 2024-01-16

# Use case: configuration files
# File: config.ps1
$DatabaseServer = "prod-db.example.com"
$DatabasePort = 5432
$LogPath = "C:\Logs"

# Main script
. .\config.ps1
Write-Output "Connecting to $DatabaseServer`:$DatabasePort"
```

---

## Section 5 : Pipeline et Manipulation Objets

### 5.1 Pipeline Basics

```powershell
# Pipeline = passer objets entre cmdlets

# Simple pipeline
Get-Process | Where-Object {$_.CPU -gt 100}

# Multiple stages
Get-Process |
    Where-Object {$_.WorkingSet64 -gt 100MB} |
    Sort-Object -Property CPU -Descending |
    Select-Object -First 10 -Property Name, CPU, WorkingSet64

# $_ = current pipeline object
Get-ChildItem C:\Temp |
    Where-Object {$_.Length -gt 1MB} |
    ForEach-Object {
        Write-Output "$($_.Name) - $([math]::Round($_.Length / 1MB, 2)) MB"
    }

# Out-Null (discard output)
Get-Process | Out-Null

# Tee-Object (output to file AND pipeline)
Get-Process |
    Tee-Object -FilePath processes.txt |
    Where-Object {$_.CPU -gt 50}
```

### 5.2 Where-Object (Filter)

```powershell
# Filter objets dans pipeline

# Simple condition
Get-Service | Where-Object {$_.Status -eq "Running"}

# Multiple conditions
Get-Process | Where-Object {
    $_.CPU -gt 50 -and $_.WorkingSet64 -gt 100MB
}

# Simplified syntax (PowerShell 3+)
Get-Service | Where-Object Status -eq "Running"
Get-Process | Where-Object CPU -gt 50

# Comparison operators
Get-ChildItem | Where-Object Name -like "*.log"
Get-ChildItem | Where-Object Extension -match "\.txt$"
Get-ChildItem | Where-Object LastWriteTime -gt (Get-Date).AddDays(-7)

# Complex filters
Get-EventLog -LogName System -Newest 100 |
    Where-Object {
        $_.EntryType -eq "Error" -and
        $_.TimeGenerated -gt (Get-Date).AddHours(-24)
    }

# .Where() method (PowerShell 4+)
$processes = Get-Process
$processes.Where({$_.CPU -gt 50})
```

### 5.3 Select-Object (Project)

```powershell
# Select properties

# Select specific properties
Get-Process | Select-Object -Property Name, Id, CPU

# First/Last objects
Get-Process | Select-Object -First 10
Get-Process | Select-Object -Last 5

# Unique values
Get-Process | Select-Object -Property ProcessName -Unique

# Calculated properties
Get-Process | Select-Object Name, @{
    Name='MemoryMB'
    Expression={[math]::Round($_.WorkingSet64 / 1MB, 2)}
}

# Multiple calculated properties
Get-ChildItem | Select-Object Name,
    @{N='SizeMB'; E={[math]::Round($_.Length / 1MB, 2)}},
    @{N='Age'; E={(New-TimeSpan -Start $_.CreationTime).Days}},
    @{N='Type'; E={if ($_.PSIsContainer) {"Folder"} else {"File"}}}

# Expand nested properties
Get-Process | Select-Object -ExpandProperty Modules

# Skip objects
Get-Process | Select-Object -Skip 5 -First 10
```

### 5.4 Sort-Object et Group-Object

```powershell
# Sort objects

# Sort ascending (default)
Get-Process | Sort-Object -Property CPU

# Sort descending
Get-Process | Sort-Object -Property CPU -Descending

# Sort multiple properties
Get-ChildItem | Sort-Object -Property Extension, Name

# Sort with calculated property
Get-ChildItem | Sort-Object -Property @{
    Expression={$_.Length}
    Descending=$true
}

# Group objects
Get-Service | Group-Object -Property Status

# Output :
# Count Name       Group
# ----- ----       -----
#   120 Running    {AdobeARMservice, Appinfo, ...}
#    85 Stopped    {AppVClient, BcastDVRUserService, ...}

# Group with calculated property
Get-ChildItem | Group-Object -Property Extension

# Access groups
$grouped = Get-Process | Group-Object -Property ProcessName
foreach ($group in $grouped) {
    Write-Output "$($group.Name): $($group.Count) instances"
    # Access group members
    # $group.Group
}
```

### 5.5 Measure-Object et Compare-Object

```powershell
# Measure objects

# Count
Get-ChildItem | Measure-Object

# Sum
Get-ChildItem | Measure-Object -Property Length -Sum

# Statistics
Get-Process | Measure-Object -Property CPU -Average -Sum -Maximum -Minimum

# Output :
# Count    : 245
# Average  : 5.234
# Sum      : 1282.45
# Maximum  : 234.56
# Minimum  : 0.01

# Line/Word/Character count
Get-Content file.txt | Measure-Object -Line -Word -Character

# Compare objects
$old = Get-Content old.txt
$new = Get-Content new.txt

Compare-Object -ReferenceObject $old -DifferenceObject $new

# Output :
# InputObject    SideIndicator
# -----------    -------------
# new line       =>            (in new only)
# old line       <=            (in old only)

# Include equal
Compare-Object $old $new -IncludeEqual

# Compare by property
$oldProcs = Get-Process
Start-Sleep -Seconds 5
$newProcs = Get-Process

Compare-Object $oldProcs $newProcs -Property Name
```

---

## Section 6 : Fichiers, Registre et I/O

### 6.1 File System Operations

```powershell
# Navigation
Get-Location      # pwd
Set-Location C:\  # cd
Push-Location     # Save location stack
Pop-Location      # Restore location

# List files
Get-ChildItem                    # ls, dir
Get-ChildItem -Path C:\Temp
Get-ChildItem -Filter "*.log"
Get-ChildItem -Recurse          # Recursive
Get-ChildItem -Force            # Include hidden
Get-ChildItem -File             # Files only
Get-ChildItem -Directory        # Directories only

# Create
New-Item -Path C:\Temp\test.txt -ItemType File
New-Item -Path C:\Temp\NewFolder -ItemType Directory

# Create with content
New-Item -Path test.txt -ItemType File -Value "Hello World"

# Copy
Copy-Item -Path source.txt -Destination dest.txt
Copy-Item -Path C:\Source -Destination C:\Dest -Recurse

# Move
Move-Item -Path old.txt -Destination new.txt
Move-Item -Path C:\Source\* -Destination C:\Dest

# Remove
Remove-Item -Path file.txt
Remove-Item -Path C:\Folder -Recurse -Force

# Rename
Rename-Item -Path old.txt -NewName new.txt

# Test existence
Test-Path -Path C:\file.txt     # True/False

# Get properties
Get-Item -Path file.txt
Get-ItemProperty -Path file.txt

# Set properties
Set-ItemProperty -Path file.txt -Name IsReadOnly -Value $true
```

### 6.2 File Content

```powershell
# Read file
Get-Content -Path file.txt

# Read specific lines
Get-Content -Path file.txt -TotalCount 10    # First 10
Get-Content -Path file.txt -Tail 10          # Last 10

# Read as single string
Get-Content -Path file.txt -Raw

# Read binary
Get-Content -Path file.bin -Encoding Byte

# Write file (overwrite)
Set-Content -Path file.txt -Value "Hello World"

# Write array (each element = line)
$lines = @("Line 1", "Line 2", "Line 3")
Set-Content -Path file.txt -Value $lines

# Append
Add-Content -Path file.txt -Value "New line"

# Out-File (formatté)
Get-Process | Out-File -FilePath processes.txt
Get-Service | Out-File -FilePath services.txt -Append

# Export formats
Get-Process | Export-Csv -Path processes.csv -NoTypeInformation
Get-Process | Export-Clixml -Path processes.xml
Get-Process | ConvertTo-Json | Out-File processes.json

# Import formats
Import-Csv -Path data.csv
Import-Clixml -Path data.xml
Get-Content data.json | ConvertFrom-Json

# Tail file (monitor)
Get-Content -Path C:\Logs\app.log -Wait -Tail 10
```

### 6.3 Paths

```powershell
# Join paths
Join-Path -Path C:\Temp -ChildPath file.txt
# C:\Temp\file.txt

# Split path
Split-Path -Path C:\Temp\file.txt -Parent      # C:\Temp
Split-Path -Path C:\Temp\file.txt -Leaf        # file.txt
Split-Path -Path C:\Temp\file.txt -Extension   # .txt

# Test path type
Test-Path -Path C:\Temp -PathType Container    # Directory
Test-Path -Path C:\file.txt -PathType Leaf     # File

# Resolve path (expand wildcards)
Resolve-Path -Path C:\Temp\*.txt

# Convert path
Convert-Path -Path .\relative\path
# C:\Full\Path\relative\path

# File info object
$file = Get-Item -Path file.txt
$file.FullName
$file.Name
$file.Extension
$file.Directory
$file.Length
$file.CreationTime
$file.LastWriteTime
```

### 6.4 Registry

```powershell
# Registry providers (comme file system)

# Navigate registry
Set-Location HKCU:\Software

# List keys
Get-ChildItem -Path HKCU:\Software

# Get value
Get-ItemProperty -Path "HKCU:\Software\MyApp" -Name Version

# Set value
New-ItemProperty -Path "HKCU:\Software\MyApp" -Name Version -Value "1.0" -PropertyType String

# Modify value
Set-ItemProperty -Path "HKCU:\Software\MyApp" -Name Version -Value "2.0"

# Remove value
Remove-ItemProperty -Path "HKCU:\Software\MyApp" -Name Version

# Create key
New-Item -Path "HKCU:\Software\MyApp"

# Remove key
Remove-Item -Path "HKCU:\Software\MyApp" -Recurse

# Test key exists
Test-Path -Path "HKCU:\Software\MyApp"

# Registry hives
# HKLM: = HKEY_LOCAL_MACHINE
# HKCU: = HKEY_CURRENT_USER
# HKCR: = HKEY_CLASSES_ROOT
```

---

## Section 7 : Text Processing et Regex

### 7.1 String Manipulation

```powershell
# String methods
$text = "Hello World"

$text.Length              # 11
$text.ToUpper()           # HELLO WORLD
$text.ToLower()           # hello world
$text.Trim()              # Remove whitespace
$text.TrimStart("H")      # ello World
$text.TrimEnd("d")        # Hello Worl

# Substring
$text.Substring(0, 5)     # Hello
$text.Substring(6)        # World

# Replace
$text.Replace("World", "PowerShell")  # Hello PowerShell

# Split
$text.Split(" ")          # Array: Hello, World
"a,b,c".Split(",")        # Array: a, b, c

# Join
$array = @("a", "b", "c")
$array -join ","          # a,b,c
$array -join " - "        # a - b - c

# Contains
$text.Contains("World")   # True
$text.StartsWith("Hello") # True
$text.EndsWith("World")   # True

# IndexOf
$text.IndexOf("W")        # 6
$text.LastIndexOf("l")    # 9

# Padding
"5".PadLeft(3, "0")       # 005
"5".PadRight(3, "0")      # 500

# Format strings
"Hello, {0}! You are {1} years old." -f "John", 30
"Value: {0:N2}" -f 1234.5678    # Value: 1,234.57
"Date: {0:yyyy-MM-dd}" -f (Get-Date)
```

### 7.2 Regular Expressions

```powershell
# Match operator
"Hello123" -match "\d+"   # True
$Matches[0]               # 123

# Extract groups
$text = "Email: john@example.com"
if ($text -match "(\w+)@(\w+\.\w+)") {
    $username = $Matches[1]  # john
    $domain = $Matches[2]    # example.com
}

# Named groups
$text = "2024-01-16"
if ($text -match "(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})") {
    $year = $Matches['year']
    $month = $Matches['month']
    $day = $Matches['day']
}

# Select-String (grep)
Select-String -Path *.log -Pattern "ERROR"
Select-String -Path file.txt -Pattern "error" -CaseSensitive
Select-String -Path *.txt -Pattern "\d{3}-\d{4}" -AllMatches

# Get matches
$matches = Select-String -Path file.txt -Pattern "\d+"
foreach ($match in $matches) {
    Write-Output "Line $($match.LineNumber): $($match.Line)"
}

# Replace with regex
$text = "Phone: 555-1234"
$text -replace "\d{3}-\d{4}", "XXX-XXXX"
# Phone: XXX-XXXX

# Regex object
$regex = [regex]"\d+"
$regex.Match("abc123def").Value    # 123
$regex.Matches("a1b2c3").Count     # 3

# Common patterns
$emailPattern = '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
$phonePattern = '^\d{3}-\d{3}-\d{4}$'
$urlPattern = '^https?://[a-zA-Z0-9.-]+\.[a-z]{2,}(/.*)?$'
$ipPattern = '^(\d{1,3}\.){3}\d{1,3}$'

# Validate
$email = "user@example.com"
if ($email -match $emailPattern) {
    Write-Output "Valid email"
}
```

### 7.3 Text Processing Examples

```powershell
# Parse log file
Get-Content app.log | Where-Object {$_ -match "ERROR"} |
    ForEach-Object {
        if ($_ -match "\[(.*?)\].*ERROR: (.*)") {
            [PSCustomObject]@{
                Timestamp = $Matches[1]
                Message = $Matches[2]
            }
        }
    }

# Extract emails from file
$emails = Get-Content contacts.txt |
    Select-String -Pattern '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' -AllMatches |
    ForEach-Object {$_.Matches.Value} |
    Select-Object -Unique

# Parse CSV manually
Get-Content data.csv | ForEach-Object {
    $fields = $_ -split ","
    [PSCustomObject]@{
        Name = $fields[0]
        Age = $fields[1]
        City = $fields[2]
    }
}

# Clean text
$text = Get-Content file.txt -Raw
$text = $text -replace "\r\n", "`n"     # Normalize line endings
$text = $text -replace "\s+", " "       # Multiple spaces to one
$text = $text.Trim()                    # Remove leading/trailing
```

---

## Section 8 : Paramètres et Validation

### 8.1 Parameter Attributes

```powershell
# Mandatory parameter
function Test-Mandatory {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name
    )
    Write-Output "Name: $Name"
}

# Test-Mandatory  # Error: missing Name
Test-Mandatory -Name "John"  # OK

# Position
function Test-Position {
    param(
        [Parameter(Position=0)]
        [string]$First,
        
        [Parameter(Position=1)]
        [string]$Second
    )
    Write-Output "$First $Second"
}

Test-Position "Hello" "World"  # Positional
Test-Position -First "Hello" -Second "World"  # Named

# Pipeline input
function Test-Pipeline {
    param(
        [Parameter(ValueFromPipeline=$true)]
        [string]$InputValue
    )
    
    process {
        Write-Output "Received: $InputValue"
    }
}

"a", "b", "c" | Test-Pipeline

# Pipeline by property name
function Get-ProcessInfo {
    param(
        [Parameter(ValueFromPipelineByPropertyName=$true)]
        [string]$Name
    )
    
    process {
        Get-Process -Name $Name
    }
}

[PSCustomObject]@{Name="powershell"} | Get-ProcessInfo

# HelpMessage
function Test-Help {
    param(
        [Parameter(Mandatory=$true, HelpMessage="Enter user name")]
        [string]$UserName
    )
    Write-Output $UserName
}

# Test-Help  # Prompts with help message
```

### 8.2 Validation Attributes

```powershell
# ValidateRange
function Set-Age {
    param(
        [ValidateRange(0, 150)]
        [int]$Age
    )
    Write-Output "Age set: $Age"
}

Set-Age -Age 30   # OK
# Set-Age -Age 200  # Error: outside range

# ValidateLength
function Set-Name {
    param(
        [ValidateLength(1, 50)]
        [string]$Name
    )
    Write-Output "Name: $Name"
}

# ValidatePattern (regex)
function Set-Email {
    param(
        [ValidatePattern('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')]
        [string]$Email
    )
    Write-Output "Email: $Email"
}

Set-Email -Email "user@example.com"  # OK
# Set-Email -Email "invalid"  # Error: pattern mismatch

# ValidateSet (enum)
function Set-Priority {
    param(
        [ValidateSet("Low", "Medium", "High", "Critical")]
        [string]$Priority
    )
    Write-Output "Priority: $Priority"
}

Set-Priority -Priority "High"  # OK
# Set-Priority -Priority "Urgent"  # Error: not in set

# Tab completion avec ValidateSet
Set-Priority -Priority <TAB>  # Cycles: Low, Medium, High, Critical

# ValidateScript (custom validation)
function Set-FilePath {
    param(
        [ValidateScript({Test-Path $_})]
        [string]$Path
    )
    Write-Output "Valid path: $Path"
}

Set-FilePath -Path "C:\Windows"  # OK
# Set-FilePath -Path "C:\NonExistent"  # Error

# ValidateNotNull / ValidateNotNullOrEmpty
function Set-Value {
    param(
        [ValidateNotNullOrEmpty()]
        [string]$Value
    )
    Write-Output $Value
}

# ValidateCount (array)
function Set-Items {
    param(
        [ValidateCount(1, 5)]
        [string[]]$Items
    )
    Write-Output "Items: $($Items -join ', ')"
}

Set-Items -Items "a", "b", "c"  # OK
# Set-Items -Items @()  # Error: count < 1
```

### 8.3 Parameter Sets

```powershell
# Multiple parameter sets
function Get-Data {
    [CmdletBinding(DefaultParameterSetName='ByName')]
    param(
        [Parameter(ParameterSetName='ByName', Mandatory=$true)]
        [string]$Name,
        
        [Parameter(ParameterSetName='ById', Mandatory=$true)]
        [int]$Id,
        
        [Parameter(ParameterSetName='All')]
        [switch]$All
    )
    
    switch ($PSCmdlet.ParameterSetName) {
        'ByName' {
            Write-Output "Getting data by name: $Name"
        }
        'ById' {
            Write-Output "Getting data by ID: $Id"
        }
        'All' {
            Write-Output "Getting all data"
        }
    }
}

Get-Data -Name "John"    # ByName set
Get-Data -Id 123         # ById set
Get-Data -All            # All set
# Get-Data -Name "John" -Id 123  # Error: incompatible parameters

# Dynamic parameters (advanced)
function Get-DynamicParam {
    [CmdletBinding()]
    param(
        [string]$Type
    )
    
    DynamicParam {
        if ($Type -eq "File") {
            $attribute = New-Object System.Management.Automation.ParameterAttribute
            $attribute.Mandatory = $true
            
            $collection = New-Object System.Collections.ObjectModel.Collection[System.Attribute]
            $collection.Add($attribute)
            
            $param = New-Object System.Management.Automation.RuntimeDefinedParameter(
                'Path', [string], $collection
            )
            
            $dictionary = New-Object System.Management.Automation.RuntimeDefinedParameterDictionary
            $dictionary.Add('Path', $param)
            return $dictionary
        }
    }
    
    process {
        if ($Type -eq "File") {
            Write-Output "File path: $($PSBoundParameters['Path'])"
        }
    }
}
```

---

## Section 9 : Debugging et Error Handling

### 9.1 Error Handling Basics

```powershell
# Try/Catch/Finally
try {
    Get-Item -Path "C:\NonExistent.txt" -ErrorAction Stop
    Write-Output "File found"
}
catch {
    Write-Output "Error: $($_.Exception.Message)"
}
finally {
    Write-Output "Cleanup executed"
}

# Multiple catch blocks
try {
    # Risky operation
}
catch [System.IO.FileNotFoundException] {
    Write-Output "File not found"
}
catch [System.UnauthorizedAccessException] {
    Write-Output "Access denied"
}
catch {
    Write-Output "Unknown error: $_"
}

# Error variable
try {
    Get-Item "C:\NonExistent"
}
catch {
    $errorMessage = $_.Exception.Message
    $errorType = $_.Exception.GetType().FullName
    $errorLine = $_.InvocationInfo.ScriptLineNumber
    
    Write-Output "Error at line $errorLine : $errorMessage"
}

# Throw custom errors
function Divide-Numbers {
    param([int]$a, [int]$b)
    
    if ($b -eq 0) {
        throw "Division by zero not allowed"
    }
    
    return $a / $b
}

try {
    Divide-Numbers -a 10 -b 0
}
catch {
    Write-Output "Caught: $_"
}
```

### 9.2 Error Actions

```powershell
# ErrorAction preference
# Stop        : Throw terminating error
# Continue    : Display error, continue (default)
# SilentlyContinue : Suppress error, continue
# Inquire     : Prompt user

# Per-command ErrorAction
Get-Item "C:\NonExistent" -ErrorAction SilentlyContinue

# Global preference
$ErrorActionPreference = "Stop"  # All errors terminate

# ErrorVariable (capture errors)
Get-ChildItem "C:\NonExistent" -ErrorAction SilentlyContinue -ErrorVariable myErrors

foreach ($error in $myErrors) {
    Write-Output "Error: $($error.Exception.Message)"
}

# $Error automatic variable (last errors)
$Error[0]  # Most recent error
$Error.Count
$Error.Clear()

# Terminating vs Non-terminating errors
# Non-terminating: cmdlet continues (can be caught with -ErrorAction Stop)
# Terminating: cmdlet stops (caught by try/catch)

# Make non-terminating error catchable
try {
    Get-Item "C:\NonExistent" -ErrorAction Stop
}
catch {
    Write-Output "Caught non-terminating error"
}
```

### 9.3 Debugging

```powershell
# Write debugging output
Write-Debug "Debug message"
Write-Verbose "Verbose message"
Write-Warning "Warning message"
Write-Error "Error message"
Write-Host "Console message" -ForegroundColor Green

# Enable debug/verbose
$DebugPreference = "Continue"
$VerbosePreference = "Continue"

# Function with debug support
function Test-Debug {
    [CmdletBinding()]
    param([string]$Name)
    
    Write-Debug "Debug: Processing $Name"
    Write-Verbose "Verbose: Processing $Name"
    Write-Output "Output: $Name"
}

Test-Debug -Name "John" -Debug -Verbose

# Set-PSBreakpoint (breakpoints)
Set-PSBreakpoint -Script .\script.ps1 -Line 10
Set-PSBreakpoint -Script .\script.ps1 -Variable myVar
Set-PSBreakpoint -Script .\script.ps1 -Command Get-Process

# Remove breakpoints
Get-PSBreakpoint
Remove-PSBreakpoint -Id 1

# Step debugging
# s : Step Into
# v : Step Over
# o : Step Out
# c : Continue
# q : Quit

# Transcript (log all output)
Start-Transcript -Path "C:\Logs\session.log"
# ... commands ...
Stop-Transcript

# Measure execution time
Measure-Command {
    Get-Process
}

# Profiling
$sw = [System.Diagnostics.Stopwatch]::StartNew()
# Code to profile
$sw.Stop()
Write-Output "Elapsed: $($sw.Elapsed.TotalSeconds) seconds"
```

### 9.4 Error Handling Production

```powershell
# Robust function template
function Invoke-RobustOperation {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Path,
        
        [int]$RetryCount = 3,
        [int]$RetryDelay = 2
    )
    
    begin {
        $attempt = 0
        $success = $false
    }
    
    process {
        while (-not $success -and $attempt -lt $RetryCount) {
            $attempt++
            
            try {
                Write-Verbose "Attempt $attempt of $RetryCount"
                
                # Operation
                $result = Get-Content -Path $Path -ErrorAction Stop
                
                $success = $true
                Write-Verbose "Operation succeeded"
                return $result
            }
            catch {
                Write-Warning "Attempt $attempt failed: $($_.Exception.Message)"
                
                if ($attempt -lt $RetryCount) {
                    Write-Verbose "Retrying in $RetryDelay seconds..."
                    Start-Sleep -Seconds $RetryDelay
                }
                else {
                    Write-Error "Operation failed after $RetryCount attempts"
                    throw
                }
            }
        }
    }
}

# Logging framework
function Write-Log {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [ValidateSet('INFO', 'WARN', 'ERROR', 'DEBUG')]
        [string]$Level = 'INFO',
        
        [string]$LogPath = "C:\Logs\app.log"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    Add-Content -Path $LogPath -Value $logMessage
    
    switch ($Level) {
        'ERROR' { Write-Error $Message }
        'WARN'  { Write-Warning $Message }
        'DEBUG' { Write-Debug $Message }
        default { Write-Verbose $Message }
    }
}
```

---

## Section 10 : Remoting et Background Jobs

### 10.1 PowerShell Remoting (PSRemoting)

```powershell
# Enable remoting (admin)
Enable-PSRemoting -Force

# Test remoting
Test-WSMan -ComputerName Server01

# Enter remote session (interactive)
Enter-PSSession -ComputerName Server01

# Exit remote session
Exit-PSSession

# Execute command remote
Invoke-Command -ComputerName Server01 -ScriptBlock {
    Get-Service
}

# Execute on multiple computers
Invoke-Command -ComputerName Server01, Server02, Server03 -ScriptBlock {
    Get-Process | Where-Object {$_.CPU -gt 100}
}

# Pass arguments
Invoke-Command -ComputerName Server01 -ScriptBlock {
    param($ServiceName)
    Get-Service -Name $ServiceName
} -ArgumentList "wuauserv"

# Using variables (automatic)
$services = "wuauserv", "spooler"
Invoke-Command -ComputerName Server01 -ScriptBlock {
    Get-Service -Name $using:services
}

# Execute script file remote
Invoke-Command -ComputerName Server01 -FilePath .\script.ps1

# Persistent session
$session = New-PSSession -ComputerName Server01

# Use session
Invoke-Command -Session $session -ScriptBlock {
    Get-Date
}

# Import module from remote
Import-PSSession -Session $session -Module ActiveDirectory

# Disconnect session
Disconnect-PSSession -Session $session

# Reconnect
$session = Get-PSSession -ComputerName Server01
Connect-PSSession -Session $session

# Remove session
Remove-PSSession -Session $session

# Credentials
$cred = Get-Credential
Invoke-Command -ComputerName Server01 -Credential $cred -ScriptBlock {
    Get-Process
}
```

### 10.2 Background Jobs

```powershell
# Start job
$job = Start-Job -ScriptBlock {
    Get-Process | Where-Object {$_.CPU -gt 50}
}

# Get jobs
Get-Job

# Wait for job
Wait-Job -Job $job

# Get job results
Receive-Job -Job $job

# Keep results (receive multiple times)
Receive-Job -Job $job -Keep

# Remove job
Remove-Job -Job $job

# Job state
$job.State  # Running, Completed, Failed

# Stop job
Stop-Job -Job $job

# Multiple jobs
$jobs = @()
$jobs += Start-Job -ScriptBlock { Get-Process }
$jobs += Start-Job -ScriptBlock { Get-Service }

# Wait all
$jobs | Wait-Job

# Get all results
$jobs | Receive-Job

# Remote job
$job = Invoke-Command -ComputerName Server01 -ScriptBlock {
    Get-EventLog -LogName System -Newest 100
} -AsJob

# Job with parameters
$job = Start-Job -ScriptBlock {
    param($Path)
    Get-ChildItem -Path $Path
} -ArgumentList "C:\Temp"

# Scheduled job (Task Scheduler)
$trigger = New-JobTrigger -Daily -At 3am
Register-ScheduledJob -Name "DailyBackup" -ScriptBlock {
    # Backup logic
} -Trigger $trigger

# Thread job (PowerShell 7+, faster)
$job = Start-ThreadJob -ScriptBlock {
    Get-Process
}
```

---

## Section 11 : Best Practices et Sécurité

### 11.1 Script Template Production

```powershell
<#
.SYNOPSIS
    Brief description of script
.DESCRIPTION
    Detailed description of what this script does
.PARAMETER ComputerName
    Target computer name
.PARAMETER Credential
    Credentials for remote access
.EXAMPLE
    .\Script.ps1 -ComputerName Server01
.NOTES
    Author: Your Name
    Created: 2024-01-16
    Version: 1.0.0
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string]$ComputerName,
    
    [Parameter(Mandatory=$false)]
    [System.Management.Automation.PSCredential]$Credential,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('INFO', 'WARN', 'ERROR', 'DEBUG')]
    [string]$LogLevel = 'INFO'
)

# === CONFIGURATION ===
$ErrorActionPreference = "Stop"
$VerbosePreference = if ($PSBoundParameters['Verbose']) { "Continue" } else { "SilentlyContinue" }

$ScriptName = $MyInvocation.MyCommand.Name
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogPath = Join-Path $env:TEMP "$ScriptName.log"

# === FUNCTIONS ===
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = 'INFO'
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    Add-Content -Path $LogPath -Value $logMessage
    
    switch ($Level) {
        'ERROR' { Write-Error $Message }
        'WARN'  { Write-Warning $Message }
        'DEBUG' { Write-Debug $Message }
        default { Write-Verbose $Message }
    }
}

function Test-Prerequisites {
    Write-Log "Checking prerequisites"
    
    # Test remoting
    if (-not (Test-WSMan -ComputerName $ComputerName -ErrorAction SilentlyContinue)) {
        throw "Cannot connect to $ComputerName via WinRM"
    }
    
    Write-Log "Prerequisites check passed"
}

# === MAIN ===
try {
    Write-Log "Script started: $ScriptName"
    
    # Prerequisites
    Test-Prerequisites
    
    # Main logic
    $result = Invoke-Command -ComputerName $ComputerName -Credential $Credential -ScriptBlock {
        # Your logic here
        Get-ComputerInfo
    }
    
    # Output
    $result
    
    Write-Log "Script completed successfully"
}
catch {
    Write-Log "Script failed: $($_.Exception.Message)" -Level ERROR
    throw
}
finally {
    Write-Log "Script finished"
}

# Exit codes
exit 0
```

### 11.2 Security Best Practices

```powershell
# 1. Credentials (NEVER hardcode)
# ❌ BAD
$password = "MyPassword123"
$username = "admin"

# ✅ GOOD
$cred = Get-Credential

# ✅ BETTER (secure string)
$securePassword = ConvertTo-SecureString "Password" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("username", $securePassword)

# ✅ BEST (Windows Credential Manager)
$cred = Get-StoredCredential -Target "MyApp"

# 2. Secrets management
# Use Azure Key Vault
$secret = Get-AzKeyVaultSecret -VaultName "MyVault" -Name "DatabasePassword"

# 3. Input validation (always)
function Set-UserData {
    param(
        [ValidatePattern('^[a-zA-Z0-9]+$')]
        [string]$Username,
        
        [ValidateRange(0, 150)]
        [int]$Age
    )
    # Safe to use
}

# 4. Avoid Invoke-Expression
# ❌ DANGEROUS
$command = Read-Host "Enter command"
Invoke-Expression $command  # Code injection risk

# ✅ SAFE
# Use parameters, not dynamic code

# 5. Constrained Language Mode (security)
$ExecutionContext.SessionState.LanguageMode
# FullLanguage      : All features
# ConstrainedLanguage : Restricted (AppLocker)

# 6. Script signing (production)
# Create certificate
$cert = New-SelfSignedCertificate -Subject "CN=PowerShell Code Signing" -Type CodeSigningCert -CertStoreLocation Cert:\CurrentUser\My

# Sign script
Set-AuthenticodeSignature -FilePath .\script.ps1 -Certificate $cert

# Verify signature
Get-AuthenticodeSignature -FilePath .\script.ps1

# 7. Execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 8. Transcript logging (audit)
Start-Transcript -Path "C:\Logs\transcript_$(Get-Date -Format yyyyMMdd).log"
# ... operations ...
Stop-Transcript
```

### 11.3 Performance Best Practices

```powershell
# 1. Avoid pipeline when possible
# ❌ SLOW
$results = @()
1..10000 | ForEach-Object {
    $results += $_  # Array += slow (creates new array)
}

# ✅ FAST
$results = [System.Collections.ArrayList]::new()
1..10000 | ForEach-Object {
    $results.Add($_) | Out-Null
}

# ✅ FASTER
$results = 1..10000  # Direct range

# 2. Filter early in pipeline
# ❌ SLOW
Get-Process | Select-Object Name, CPU | Where-Object {$_.CPU -gt 50}

# ✅ FAST
Get-Process | Where-Object {$_.CPU -gt 50} | Select-Object Name, CPU

# 3. Use .NET methods when faster
# ❌ SLOWER
$text = "hello"
$text.ToUpper()

# ✅ FASTER (for many operations)
[string]::ToUpper($text)

# 4. Avoid Get-WmiObject (deprecated)
# ❌ OLD
Get-WmiObject -Class Win32_OperatingSystem

# ✅ NEW (faster)
Get-CimInstance -ClassName Win32_OperatingSystem

# 5. Use -Filter instead of Where-Object
# ❌ SLOW (client-side filtering)
Get-ChildItem C:\Windows | Where-Object {$_.Extension -eq ".log"}

# ✅ FAST (server-side filtering)
Get-ChildItem C:\Windows -Filter "*.log"

# 6. StringBuilder for many concatenations
$sb = [System.Text.StringBuilder]::new()
1..10000 | ForEach-Object {
    $sb.AppendLine("Line $_") | Out-Null
}
$result = $sb.ToString()

# 7. Parallel processing (PowerShell 7+)
1..10 | ForEach-Object -Parallel {
    Start-Sleep -Seconds 1
    "Task $_ completed"
} -ThrottleLimit 5

# 8. Runspaces (advanced parallel)
# For CPU-intensive tasks
```

### 11.4 Code Quality

```powershell
# 1. Use approved verbs
Get-Verb  # List approved verbs

# ✅ GOOD
function Get-UserData { }
function Set-Configuration { }
function New-Report { }

# ❌ BAD
function Retrieve-UserData { }  # Use Get
function Modify-Config { }      # Use Set

# 2. Consistent naming
# PascalCase : Functions, Parameters
# camelCase : Variables (optionnel, mais cohérent)

# 3. Comment-based help
function Get-Data {
    <#
    .SYNOPSIS
        Gets data from source
    .DESCRIPTION
        Detailed description
    .PARAMETER Source
        Data source
    .EXAMPLE
        Get-Data -Source "DB"
    #>
    param([string]$Source)
}

# 4. Error handling
# Always use try/catch for risky operations

# 5. Verbose output
function Do-Something {
    [CmdletBinding()]
    param()
    
    Write-Verbose "Starting operation"
    # Operation
    Write-Verbose "Operation completed"
}

# 6. PSScriptAnalyzer (linter)
Install-Module PSScriptAnalyzer
Invoke-ScriptAnalyzer -Path .\script.ps1

# 7. Pester (testing)
Describe "Get-Data" {
    It "Returns data" {
        $result = Get-Data -Source "Test"
        $result | Should -Not -BeNullOrEmpty
    }
}
```

---

## Section 12 : Cas Pratiques Production

### 12.1 User Management (Active Directory)

```powershell
# Créer utilisateur AD
function New-ADUserAccount {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$FirstName,
        
        [Parameter(Mandatory=$true)]
        [string]$LastName,
        
        [Parameter(Mandatory=$true)]
        [string]$Department,
        
        [string]$OU = "OU=Users,DC=company,DC=com"
    )
    
    try {
        $username = "$($FirstName.Substring(0,1))$LastName".ToLower()
        $email = "$username@company.com"
        
        # Generate secure password
        Add-Type -AssemblyName System.Web
        $password = [System.Web.Security.Membership]::GeneratePassword(12, 2)
        $securePassword = ConvertTo-SecureString $password -AsPlainText -Force
        
        # Create user
        New-ADUser -Name "$FirstName $LastName" `
            -GivenName $FirstName `
            -Surname $LastName `
            -SamAccountName $username `
            -UserPrincipalName $email `
            -EmailAddress $email `
            -Department $Department `
            -Path $OU `
            -AccountPassword $securePassword `
            -Enabled $true `
            -ChangePasswordAtLogon $true
        
        Write-Output "User created: $username"
        Write-Output "Temporary password: $password"
        
        # Add to department group
        Add-ADGroupMember -Identity $Department -Members $username
        
        # Send email with credentials
        Send-MailMessage -To $email `
            -From "noreply@company.com" `
            -Subject "Welcome - Account Created" `
            -Body "Username: $username`nPassword: $password" `
            -SmtpServer "smtp.company.com"
    }
    catch {
        Write-Error "Failed to create user: $_"
        throw
    }
}

# Bulk user creation from CSV
$users = Import-Csv -Path users.csv
foreach ($user in $users) {
    New-ADUserAccount -FirstName $user.FirstName `
        -LastName $user.LastName `
        -Department $user.Department
}
```

### 12.2 Server Monitoring

```powershell
# Health check script
function Test-ServerHealth {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string[]]$ComputerName,
        
        [int]$CPUThreshold = 80,
        [int]$MemoryThreshold = 90,
        [int]$DiskThreshold = 85
    )
    
    $results = @()
    
    foreach ($computer in $ComputerName) {
        try {
            Write-Verbose "Checking $computer"
            
            $os = Get-CimInstance -ClassName Win32_OperatingSystem -ComputerName $computer
            $cpu = Get-CimInstance -ClassName Win32_Processor -ComputerName $computer
            
            # Memory usage
            $memoryUsed = [math]::Round((($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / $os.TotalVisibleMemorySize) * 100, 2)
            
            # Disk usage
            $disks = Get-CimInstance -ClassName Win32_LogicalDisk -ComputerName $computer -Filter "DriveType=3"
            $diskCritical = $disks | Where-Object {
                ($_.Size - $_.FreeSpace) / $_.Size * 100 -gt $DiskThreshold
            }
            
            # CPU (5 second average)
            $cpuUsage = (Get-Counter "\Processor(_Total)\% Processor Time" -ComputerName $computer).CounterSamples.CookedValue
            
            # Status
            $status = "Healthy"
            $issues = @()
            
            if ($cpuUsage -gt $CPUThreshold) {
                $status = "Warning"
                $issues += "High CPU: $([math]::Round($cpuUsage, 2))%"
            }
            
            if ($memoryUsed -gt $MemoryThreshold) {
                $status = "Warning"
                $issues += "High Memory: $memoryUsed%"
            }
            
            if ($diskCritical) {
                $status = "Critical"
                $issues += "Disk space critical"
            }
            
            $results += [PSCustomObject]@{
                ComputerName = $computer
                Status = $status
                CPUUsage = [math]::Round($cpuUsage, 2)
                MemoryUsage = $memoryUsed
                Issues = $issues -join "; "
                CheckTime = Get-Date
            }
        }
        catch {
            $results += [PSCustomObject]@{
                ComputerName = $computer
                Status = "Unreachable"
                CPUUsage = 0
                MemoryUsage = 0
                Issues = $_.Exception.Message
                CheckTime = Get-Date
            }
        }
    }
    
    return $results
}

# Run health check
$servers = @("Server01", "Server02", "Server03")
$health = Test-ServerHealth -ComputerName $servers -Verbose

# Export results
$health | Export-Csv -Path "health_check_$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation

# Send alert if issues
$critical = $health | Where-Object {$_.Status -eq "Critical"}
if ($critical) {
    Send-MailMessage -To "admin@company.com" `
        -From "monitoring@company.com" `
        -Subject "CRITICAL: Server Health Alert" `
        -Body ($critical | Format-Table | Out-String) `
        -SmtpServer "smtp.company.com"
}
```

### 12.3 Backup Automation

```powershell
# Backup script avec rotation
function Start-Backup {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$SourcePath,
        
        [Parameter(Mandatory=$true)]
        [string]$DestinationPath,
        
        [int]$RetentionDays = 30,
        
        [switch]$Compress
    )
    
    try {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupName = "backup_$timestamp"
        
        # Check disk space
        $requiredSpace = (Get-ChildItem $SourcePath -Recurse | Measure-Object -Property Length -Sum).Sum
        $availableSpace = (Get-PSDrive -Name ($DestinationPath.Substring(0,1))).Free
        
        if ($availableSpace -lt ($requiredSpace * 1.2)) {
            throw "Insufficient disk space. Required: $([math]::Round($requiredSpace/1GB, 2))GB, Available: $([math]::Round($availableSpace/1GB, 2))GB"
        }
        
        Write-Verbose "Starting backup: $SourcePath -> $DestinationPath\$backupName"
        
        if ($Compress) {
            # Compressed backup
            $archivePath = Join-Path $DestinationPath "$backupName.zip"
            Compress-Archive -Path $SourcePath -DestinationPath $archivePath -CompressionLevel Optimal
            
            Write-Output "Compressed backup created: $archivePath"
        }
        else {
            # Mirror backup
            $backupPath = Join-Path $DestinationPath $backupName
            
            robocopy $SourcePath $backupPath /MIR /R:3 /W:5 /MT:8 /LOG+:"$DestinationPath\backup.log"
            
            if ($LASTEXITCODE -le 7) {  # Robocopy success codes
                Write-Output "Backup completed: $backupPath"
            }
            else {
                throw "Robocopy failed with exit code: $LASTEXITCODE"
            }
        }
        
        # Cleanup old backups
        Write-Verbose "Cleaning up backups older than $RetentionDays days"
        
        $cutoffDate = (Get-Date).AddDays(-$RetentionDays)
        Get-ChildItem -Path $DestinationPath -Directory |
            Where-Object {$_.CreationTime -lt $cutoffDate -and $_.Name -like "backup_*"} |
            Remove-Item -Recurse -Force
        
        Get-ChildItem -Path $DestinationPath -Filter "backup_*.zip" |
            Where-Object {$_.CreationTime -lt $cutoffDate} |
            Remove-Item -Force
        
        # Send notification
        Send-MailMessage -To "admin@company.com" `
            -From "backup@company.com" `
            -Subject "Backup Successful: $SourcePath" `
            -Body "Backup completed at $(Get-Date)" `
            -SmtpServer "smtp.company.com"
    }
    catch {
        Write-Error "Backup failed: $_"
        
        # Send alert
        Send-MailMessage -To "admin@company.com" `
            -From "backup@company.com" `
            -Subject "FAILED: Backup $SourcePath" `
            -Body "Error: $($_.Exception.Message)" `
            -SmtpServer "smtp.company.com"
        
        throw
    }
}

# Scheduled task
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File C:\Scripts\backup.ps1"

$trigger = New-ScheduledTaskTrigger -Daily -At 3am

Register-ScheduledTask -TaskName "DailyBackup" `
    -Action $action `
    -Trigger $trigger `
    -User "SYSTEM" `
    -RunLevel Highest
```

### 12.4 Log Analysis

```powershell
# Parse and analyze Windows Event Logs
function Get-SecurityEvents {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [string[]]$ComputerName = $env:COMPUTERNAME,
        
        [Parameter(Mandatory=$false)]
        [int]$Hours = 24,
        
        [Parameter(Mandatory=$false)]
        [int[]]$EventId = @(4624, 4625, 4720, 4726)  # Logon, Failed logon, User created, User deleted
    )
    
    $startTime = (Get-Date).AddHours(-$Hours)
    $results = @()
    
    foreach ($computer in $ComputerName) {
        Write-Verbose "Analyzing $computer"
        
        try {
            $events = Get-WinEvent -ComputerName $computer -FilterHashtable @{
                LogName = 'Security'
                StartTime = $startTime
                ID = $EventId
            } -ErrorAction Stop
            
            foreach ($event in $events) {
                $results += [PSCustomObject]@{
                    ComputerName = $computer
                    TimeCreated = $event.TimeCreated
                    EventId = $event.Id
                    Message = $event.Message.Split("`n")[0]
                    User = $event.Properties[5].Value
                    SourceIP = if ($event.Properties.Count -gt 18) { $event.Properties[18].Value } else { "N/A" }
                }
            }
        }
        catch {
            Write-Warning "Failed to query $computer : $_"
        }
    }
    
    return $results
}

# Analyze failed logons
$failedLogons = Get-SecurityEvents -Hours 24 -EventId 4625

# Group by source IP
$topAttackers = $failedLogons |
    Where-Object {$_.SourceIP -ne "N/A"} |
    Group-Object -Property SourceIP |
    Sort-Object -Property Count -Descending |
    Select-Object -First 10 -Property Count, Name

Write-Output "Top 10 Failed Logon Sources:"
$topAttackers | Format-Table

# Export report
$failedLogons | Export-Csv -Path "security_events_$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation
```

---

## Ressources et Références

**Documentation officielle :**
- Microsoft Docs : https://docs.microsoft.com/powershell/
- PowerShell Gallery : https://www.powershellgallery.com/
- GitHub PowerShell : https://github.com/PowerShell/PowerShell

**Learning resources :**
- Microsoft Learn : https://learn.microsoft.com/powershell/
- PowerShell.org : https://powershell.org/
- Reddit r/PowerShell : https://reddit.com/r/PowerShell/

**Tools :**
- Visual Studio Code + PowerShell Extension
- Windows PowerShell ISE (built-in)
- PSScriptAnalyzer : https://github.com/PowerShell/PSScriptAnalyzer
- Pester (testing) : https://pester.dev/

**Modules essentiels :**
- Az (Azure) : https://github.com/Azure/azure-powershell
- Microsoft.Graph (Microsoft 365) : https://github.com/microsoftgraph/msgraph-sdk-powershell
- ActiveDirectory
- Exchange Online Management

---

## Conclusion

**PowerShell = Automation standard Windows/Cloud moderne**

**Points clés maîtrisés :**

✅ **Objets .NET** = Pipeline objets (pas texte comme Bash)
✅ **Cmdlets** = Verbe-Nom standard (Get-Process, Set-Service)
✅ **Variables** = Types .NET, hashtables, arrays
✅ **Structures** = if/else, switch, for/foreach/while
✅ **Fonctions** = Advanced functions, modules, pipeline support
✅ **Pipeline** = Where-Object, Select-Object, Sort-Object
✅ **I/O** = Files, registry, CSV, JSON, XML
✅ **Regex** = Pattern matching, Select-String
✅ **Validation** = Parameter attributes robustes
✅ **Error handling** = Try/catch/finally production-ready
✅ **Remoting** = PSRemoting natif, background jobs
✅ **Security** = Credentials, signing, constrained mode

**Différences clés vs Bash :**

| Aspect | Bash | PowerShell |
|--------|------|------------|
| **Pipeline** | Texte (strings) | Objets .NET |
| **Parsing** | Nécessaire (awk/sed) | Propriétés directes |
| **Syntaxe** | POSIX shell | C#-like |
| **Platform** | Unix/Linux/macOS | Windows/Linux/macOS |
| **Remoting** | SSH | WinRM/SSH natif |
| **Modules** | Scripts | .NET assemblies |

**Use cases PowerShell :**

1. **Administration Windows** : AD, Exchange, IIS, SQL Server
2. **Cloud** : Azure, AWS, GCP (modules officiels)
3. **DevOps** : CI/CD, deployment, configuration
4. **Automation** : Scheduled tasks, monitoring, backups
5. **Security** : Compliance, auditing, forensics

**Tu maîtrises maintenant PowerShell des fondamentaux aux scripts production enterprise !** 🚀

---

**Guide PowerShell Complet terminé !** 🎉

Voilà le guide PowerShell complet (sections 4-12) ! Cela couvre :

✅ **Section 4** : Fonctions et modules (basic, advanced, pipeline, modules)  
✅ **Section 5** : Pipeline objets (Where, Select, Sort, Group, Measure)  
✅ **Section 6** : Fichiers et registre (I/O complet, paths, registry)  
✅ **Section 7** : Text processing et regex (strings, patterns, Select-String)  
✅ **Section 8** : Paramètres et validation (attributes, parameter sets)  
✅ **Section 9** : Debugging et error handling (try/catch, logging, breakpoints)  
✅ **Section 10** : Remoting et jobs (PSRemoting, background jobs, parallel)  
✅ **Section 11** : Best practices (sécurité, performance, qualité code)  
✅ **Section 12** : Cas pratiques production (AD, monitoring, backup, logs)  

**Différence majeure vs Bash** : PowerShell manipule des **objets .NET** (propriétés/méthodes), pas du texte brut. C'est pourquoi `Get-Process | Where-Object {$_.CPU -gt 50}` accède directement à la propriété `.CPU` sans parsing !

**C'est production-ready et cross-platform (PowerShell 7+) !** 💪
