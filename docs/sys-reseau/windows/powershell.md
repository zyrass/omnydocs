---
description: "Le Shell moderne de Microsoft : syntaxe Cmdlets, pipeline orienté objet et scripts d'administration."
icon: lucide/book-open-check
tags: ["POWERSHELL", "WINDOWS", "CLI", "SCRIPTING", "AUTOMATISATION"]
---

# L'Automatisation (PowerShell)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.1"
  data-time="45 - 60 minutes">
</div>


!!! quote "Analogie pédagogique"
    _L'Active Directory (AD) sous Windows est comme l'état civil central et le cadastre d'un pays. Au lieu de laisser chaque ville (ordinateur) gérer ses passeports et ses lois, l'AD centralise l'identité de tous les citoyens (utilisateurs) et impose des lois fédérales (GPO) applicables partout instantanément._

!!! quote "Le Shell Orienté Objet"
    _Si Bash sous Linux traite tout comme du **texte** (ce qui oblige à utiliser `grep` ou `awk` pour découper les chaînes), PowerShell traite tout comme des **Objets**. Quand vous listez des processus avec PowerShell, il ne vous renvoie pas une grille de texte, mais des objets ayant des propriétés (Nom, ID, Mémoire, Propriétaire). C'est ce qui rend PowerShell infiniment supérieur pour l'administration système complexe._

<br>

---

## 1. La Syntaxe de Base (Verbe-Nom)

Les commandes natives de PowerShell s'appellent des **Cmdlets** (Command-Applets). Elles suivent une règle de nommage stricte, toujours au singulier, sous la forme `Verbe-Nom`.

- `Get-Process` (Lister les processus)
- `Stop-Service` (Arrêter un service)
- `New-Item` (Créer un fichier ou un dossier)
- `Set-ExecutionPolicy` (Modifier la politique d'exécution)

### Découverte et Aide Intégrée
PowerShell intègre des outils d'auto-découverte qui permettent de trouver et comprendre n'importe quelle commande sans quitter le terminal.

```powershell title="Console PowerShell — recherche de commandes et mise à jour de l'aide"
# Rechercher toutes les commandes contenant le mot "Service"
Get-Command *Service*

# Mettre à jour l'aide locale depuis Internet
Update-Help

# Afficher l'aide complète d'une commande avec des exemples réels
Get-Help Get-Service -Examples
```
_Ces trois commandes forment le socle de l'apprentissage autonome en ligne de commande PowerShell._

### Correspondance Bash vs PowerShell
Pour faciliter la transition, PowerShell utilise des alias qui font correspondre les commandes classiques d'Unix avec leurs Cmdlets équivalentes.

| Commande Bash | Cmdlet PowerShell équivalente | Rôle |
|---|---|---|
| `ls` ou `ll` | `Get-ChildItem` | Lister les fichiers et dossiers |
| `cd` | `Set-Location` | Naviguer dans les répertoires |
| `cat` | `Get-Content` | Lire le contenu d'un fichier |
| `rm` | `Remove-Item` | Supprimer un objet |
| `mkdir` | `New-Item -ItemType Directory` | Créer un dossier |
| `grep` | `Select-String` | Rechercher un motif de texte |

<br>

---

## 2. Le Paradigme Objet et Réflexion

Puisque PowerShell manipule des objets .NET et non des chaînes de caractères brutes, chaque résultat possède des propriétés (attributs contenant des valeurs) et des méthodes (actions exécutables).

### Inspecter un objet avec Get-Member
Pour connaître la structure exacte d'un objet renvoyé par une commande, on utilise `Get-Member` (ou son alias `gm`).

```powershell title="Console PowerShell — inspection d'un objet service"
# Lister toutes les propriétés et méthodes d'un service Windows
Get-Service -Name "wuauserv" | Get-Member
```
_Cette commande révèle que l'objet possède des propriétés comme 'Status' ou 'DisplayName', et des méthodes comme 'Start()' et 'Stop()'._

### Utiliser les méthodes d'un objet
Il est possible d'appeler directement des actions ou d'interagir avec les types .NET.

```powershell title="Script PowerShell — appel de méthodes et accès aux classes .NET"
# Obtenir la date actuelle et appeler une méthode pour formater l'affichage
(Get-Date).AddDays(7)

# Utiliser une classe .NET statique pour obtenir le nom de la machine
[System.Environment]::MachineName

# Appeler une méthode d'instance sur une chaîne de caractères
$Message = "omnyvia"
$Message.ToUpper()
```
_Le code montre comment manipuler directement les objets et invoquer des comportements de bas niveau de la plateforme .NET._

<br>

---

## 3. Le Pipeline et Manipulation de Flux

Le pipeline (`|`) de PowerShell fait transiter des instances d'objets complètes. Cela évite d'avoir à découper des lignes de texte avec des outils complexes.

```mermaid
graph LR
    subgraph Bash (Flux de Texte)
        B_Cmd1[ls -la] -->|Chaîne de caractères| B_Pipe{Pipe |}
        B_Pipe -->|Chaîne de caractères| B_Cmd2[grep 'conf']
    end
    
    subgraph PowerShell (Flux d'Objets .NET)
        P_Cmd1[Get-Process] -->|Objet avec attributs <br/> Nom, ID, RAM| P_Pipe{Pipe |}
        P_Pipe -->|Objet préservé| P_Cmd2[Where-Object <br/> RAM > 100Mo]
        P_Cmd2 -->|Objet préservé| P_Cmd3[Stop-Process]
    end
    
    style B_Cmd1 fill:#34495e,stroke:#fff,color:#fff
    style B_Cmd2 fill:#34495e,stroke:#fff,color:#fff
    style P_Cmd1 fill:#1f618d,stroke:#fff,color:#fff
    style P_Cmd2 fill:#2980b9,stroke:#fff,color:#fff
    style P_Cmd3 fill:#c0392b,stroke:#fff,color:#fff
```

### Filtrer (Where-Object)
```powershell title="Console PowerShell — filtrage d'objets dans le pipeline"
# Récupérer les processus consommant plus de 150 Mo de mémoire de travail (WorkingSet)
Get-Process | Where-Object { $_.WorkingSet -gt 150MB }
```
_La variable spéciale `$_` (ou `$PSItem`) représente l'objet courant qui traverse le pipeline à un instant T._

### Sélectionner (Select-Object)
```powershell title="Console PowerShell — sélection de propriétés spécifiques"
# Ne conserver que le nom et l'identifiant des processus
Get-Process | Select-Object -Property Name, Id
```
_Cette commande projette un nouvel objet contenant uniquement les attributs spécifiés, réduisant la taille du flux de données._

### Trier (Sort-Object)
```powershell title="Console PowerShell — tri d'un ensemble d'objets"
# Trier les services Windows par leur état actuel de manière décroissante
Get-Service | Sort-Object -Property Status -Descending
```
_Le tri s'opère sur la valeur typée de la propriété sélectionnée et non sur une simple représentation textuelle._

!!! tip "Filtrer tôt (Filter Early) vs Filtrer tard (Filter Late)"
    Dans un pipeline long, la règle d'or pour la performance est de filtrer les données le plus tôt possible. Préférer `Get-Service -Name "wuauserv"` à `Get-Service | Where-Object { $_.Name -eq "wuauserv" }`, car la première commande limite la charge sur le système d'exploitation dès la source.

<br>

---

## 4. Structures et Scripting Fondamentaux

Les scripts PowerShell portent l'extension `.ps1`. Ils permettent de concevoir des architectures d'automatisation complexes et structurées.

### Variables, Tableaux et Tables de Hachage
PowerShell gère nativement les structures de données complexes indispensables au scripting système.

```powershell title="Script PowerShell — déclaration de variables et structures de données"
# Déclaration d'une variable chaîne simple
$ServerName = "SRV-APP-01"

# Déclaration d'un tableau (Array)
$TargetPorts = @(80, 443, 8080)

# Déclaration d'une table de hachage (HashTable - dictionnaire Clé/Valeur)
$ServerConfig = @{
    Name = "SRV-DB-01"
    IP   = "192.168.1.50"
    OS   = "Windows Server 2025"
}
```
_Les variables sont faiblement typées par défaut, mais le typage peut être forcé en préfixant la variable, par exemple `[int]$Port = 80`._

### Structures Conditionnelles (If, Switch)
```powershell title="Script PowerShell — logique conditionnelle"
# Condition classique
if ($ServerConfig.IP -like "192.168.*") {
    Write-Host "Le serveur est situé dans le sous-réseau interne." -ForegroundColor Green
} else {
    Write-Warning "Le serveur est hors du réseau interne !"
}

# Utilisation d'un bloc Switch (très optimisé pour tester de multiples valeurs)
$Status = "Running"
switch ($Status) {
    "Running" { Write-Host "Le service fonctionne." }
    "Stopped" { Write-Host "Le service est arrêté." }
    Default   { Write-Warning "Statut inconnu." }
}
```
_Le code montre comment implémenter des embranchements logiques pour adapter le comportement du script aux conditions réseau._

### Boucles (Foreach, ForEach-Object)
```powershell title="Script PowerShell — itérations sur des collections d'objets"
# Boucle Foreach classique (idéale pour les scripts)
foreach ($Port in $TargetPorts) {
    Write-Host "Vérification de l'accès au port $Port..."
}

# Itération directe dans le pipeline avec ForEach-Object (alias %)
$TargetPorts | ForEach-Object {
    Write-Host "Port en cours de traitement : $_"
}
```
_Ces structures permettent de répéter des opérations d'administration sur une série de serveurs ou de comptes d'utilisateurs._

### Fonctions et Paramètres
```powershell title="Script PowerShell — déclaration d'une fonction avec paramètres typés"
function Test-ConnectionPort {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$ComputerName,

        [Parameter(Mandatory=$false)]
        [int]$Port = 443
    )

    process {
        Write-Verbose "Tentative de connexion vers $ComputerName sur le port $Port"
        # Test de connexion TCP bas niveau
        $TCPClient = New-Object System.Net.Sockets.TcpClient
        try {
            $TCPClient.Connect($ComputerName, $Port)
            return $true
        } catch {
            return $false
        } finally {
            $TCPClient.Dispose()
        }
    }
}
```
_La fonction ci-dessus définit un paramètre obligatoire et un facultatif, et intègre une gestion d'erreurs try/catch/finally robuste._

### Gestion des Erreurs et Préférences
PowerShell sépare les erreurs en deux types : bloquantes (terminating) et non bloquantes (non-terminating).

```powershell title="Script PowerShell — capture d'erreurs et gestion du flux"
# Forcer toutes les erreurs à devenir bloquantes pour les intercepter
$ErrorActionPreference = "Stop"

try {
    # Commande qui échouera si le fichier n'existe pas
    Get-Content -Path "C:\chemin\inexistant.txt"
} catch {
    # Capture et affichage du message de l'exception courante
    Write-Error "Échec de lecture du fichier : $_"
} finally {
    Write-Host "Fin de la transaction."
}
```
_L'utilisation de $ErrorActionPreference = "Stop" est une pratique indispensable en scripting professionnel pour garantir l'arrêt propre d'un déploiement en cas d'erreur._

<br>

---

## 5. Les Lecteurs Virtuels (PSDrives & Providers)

PowerShell unifie l'accès à des structures de stockage variées en les présentant sous la forme de lecteurs de disques virtuels.

```powershell title="Console PowerShell — navigation dans la base de registre et les variables"
# Naviguer dans la base de registre comme s'il s'agissait d'un dossier
cd HKLM:\Software\Microsoft
dir

# Lister toutes les variables d'environnement système
cd Env:\
Get-ChildItem

# Parcourir les certificats de l'utilisateur courant
cd Cert:\CurrentUser\My
Get-ChildItem
```
_Ce mécanisme abstrait appelé PSProvider évite d'utiliser des APIs d'administration distinctes pour lire un fichier, une clé de registre ou un certificat._

<br>

---

## 6. Importation, Exportation et Formats d'Échange

PowerShell facilite la conversion des flux d'objets vers les formats standards de l'industrie, simplifiant l'intégration avec des APIs web ou d'autres outils d'administration.

```powershell title="Script PowerShell — manipulation de formats d'échange"
# Exporter la liste des services Windows actifs au format CSV
Get-Service | Where-Object { $_.Status -eq "Running" } | Export-Csv -Path "C:\temp\services.csv" -NoTypeInformation

# Lire un fichier CSV et le réinjecter sous forme d'objets manipulables
$Users = Import-Csv -Path "C:\temp\utilisateurs.csv"

# Convertir un objet de configuration complexe au format JSON
$Configuration = @{
    Env  = "Production"
    Port = 8080
    SSL  = $true
}
$JsonConfig = $Configuration | ConvertTo-Json
```
_La sérialisation préserve le typage des données, ce qui permet de manipuler les fichiers importés avec les mêmes Cmdlets que les objets natifs._

<br>

---

## 7. Sécurité et Hardening de l'Environnement

PowerShell est un outil privilégié pour l'administration système, mais aussi pour les attaquants (phase de post-exploitation). Sa sécurisation est une priorité absolue.

### Comprendre l'Execution Policy
La politique d'exécution n'est pas une barrière de sécurité matérielle, mais un garde-fou pour empêcher l'exécution involontaire de scripts malveillants.

```powershell title="Console PowerShell — modification de la politique d'exécution"
# Vérifier la politique actuelle
Get-ExecutionPolicy

# Configurer la politique pour exiger des scripts signés
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```
_RemoteSigned exige que tous les scripts téléchargés depuis Internet soient signés par un certificat de confiance avant de pouvoir être lancés._

!!! warning "L'Execution Policy n'est pas une limite de sécurité"
    Un attaquant peut facilement contourner la politique d'exécution locale lors du lancement de sa console. La commande suivante permet d'exécuter un script sans droits administrateur, indépendamment de la politique en place :
    `powershell.exe -ExecutionPolicy Bypass -File script.ps1`

### Mesures de durcissement professionnelles
Pour sécuriser PowerShell en entreprise, les administrateurs déploient trois mécanismes via les stratégies de groupe (GPO) :

1. **Constrained Language Mode (CLM)** : Limite PowerShell à un sous-ensemble sécurisé de commandes, interdisant l'appel d'APIs système complexes de bas niveau (comme Win32 ou la manipulation directe de mémoire).
2. **Transcription Logging** : Enregistre l'intégralité du texte saisi et des sorties de consoles dans un dossier sécurisé partagé (SIEM), fournissant un audit complet des actions menées par les utilisateurs.
3. **Module Logging & Script Block Logging** : Capture les blocs de code exécutés en mémoire, y compris si le script d'origine était obfusqué ou chiffré.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    PowerShell est le moteur d'administration incontournable de l'écosystème Microsoft. Sa nature orientée objet supprime la fragilité des traitements textuels de Bash. Une administration Windows moderne exige une maîtrise des pipelines, des structures de données (dictionnaires, tableaux) et une sécurisation stricte des politiques d'exécution système.

> [Continuer vers l'administration d'Active Directory et GPO →](./ad-gpo.md)
