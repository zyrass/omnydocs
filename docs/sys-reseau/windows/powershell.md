---
description: "Le Shell moderne de Microsoft : syntaxe Cmdlets, pipeline orienté objet et scripts d'administration."
icon: lucide/book-open-check
tags: ["POWERSHELL", "WINDOWS", "CLI", "SCRIPTING", "AUTOMATISATION"]
---

# L'Automatisation (PowerShell)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>

!!! quote "Le Shell Orienté Objet"
    _Si Bash sous Linux traite tout comme du **texte** (ce qui oblige à utiliser `grep` ou `awk` pour découper les chaînes), PowerShell traite tout comme des **Objets**. Quand vous listez des processus avec PowerShell, il ne vous renvoie pas une grille de texte, mais des objets ayant des propriétés (Nom, ID, Mémoire, Propriétaire). C'est ce qui rend PowerShell infiniment supérieur pour l'administration système complexe._

## La Syntaxe de Base (Verbe-Nom)

Les commandes natives de PowerShell s'appellent des **Cmdlets** (Command-Applets). Elles suivent une règle de nommage stricte, toujours au singulier, sous la forme `Verbe-Nom`.

- `Get-Process` (Lister les processus)
- `Stop-Service` (Arrêter un service)
- `New-Item` (Créer un fichier ou un dossier)
- `Set-ExecutionPolicy` (Modifier la politique d'exécution)

### L'aide intégrée (Le sauveur)
Vous n'avez pas besoin de chercher sur Internet, l'aide est incluse :
```powershell
# Mettre à jour l'aide (à faire une fois connecté à internet)
Update-Help

# Lire l'aide d'une commande (avec des exemples)
Get-Help Get-Process -Examples
```

---

## Le Pipeline PowerShell (`|`)

Comme sous Linux, le pipe `|` permet de passer le résultat de la commande gauche à la commande de droite. Mais puisqu'on passe des **Objets**, la manipulation est magique.

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
```powershell
# Récupérer tous les processus, PUIS filtrer ceux qui consomment plus de 100 Mo de RAM
Get-Process | Where-Object {$_.WorkingSet -gt 100MB}
```
*(Note : `$_` représente l'objet courant traversant le pipe).*

### Sélectionner (Select-Object)
```powershell
# Ne garder que le nom et l'ID du processus
Get-Process | Select-Object Name, Id
```

### Trier (Sort-Object)
```powershell
# Trier les services par statut (Démarré puis Arrêté)
Get-Service | Sort-Object Status -Descending
```

---

## Le Scripting et l'Administration

PowerShell (`.ps1`) est un véritable langage de programmation (.NET).

### Variables et Types
Les variables commencent toujours par un `$`.
```powershell
$ServeurWeb = "SRV-WEB-01"
$Ports = @(80, 443) # Un tableau (Array)
```

### Automatiser l'Active Directory
C'est ici que PowerShell brille. Il existe un module spécifique pour gérer l'annuaire d'entreprise.

```powershell
# Importer le module Active Directory
Import-Module ActiveDirectory

# Créer un nouvel utilisateur en une ligne
New-ADUser -Name "John Doe" -GivenName "John" -Surname "Doe" -SamAccountName "jdoe" -UserPrincipalName "jdoe@omnyvia.local" -Path "OU=Employes,DC=omnyvia,DC=local" -AccountPassword (ConvertTo-SecureString "P@ssw0rd123!" -AsPlainText -Force) -Enabled $true
```

## Sécurité : Execution Policy

Par défaut, Windows bloque l'exécution de tout script `.ps1` par sécurité (pour éviter qu'un double-clic accidentel lance un ransomware). Vous obtiendrez l'erreur "running scripts is disabled on this system".

Pour autoriser l'exécution de scripts créés localement (mais exiger une signature numérique pour les scripts téléchargés d'Internet) :
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Conclusion

PowerShell est tellement puissant et standardisé que Microsoft a poussé **PowerShell Core**, le rendant open-source et multiplateforme (disponible sous Linux et macOS). Un administrateur Windows qui refuse d'apprendre PowerShell se condamne à effectuer des tâches répétitives manuellement et sera très limité pour la gestion de l'infrastructure moderne (Azure, Exchange, Active Directory).
