---
description: "Maîtriser le format CSV pour le traitement de données tabulaires"
icon: lucide/book-open-check
tags: ["CSV", "DONNÉES", "FORMATS", "PARSING", "DÉVELOPPEMENT"]
---

# CSV - Comma-Separated Values

## Introduction

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="1.1"
  data-time="40-45 minutes">
</div>

!!! quote "Analogie pédagogique"
    _Imaginez un **tableau Excel simplifié** où chaque ligne représente une entrée et chaque colonne une information. Maintenant, enregistrez ce tableau en **texte brut** en séparant les colonnes par des virgules. **CSV fonctionne exactement ainsi** : c'est le format le plus simple pour stocker des données tabulaires, lisible par les humains et facilement manipulable par les machines._

> **CSV (Comma-Separated Values)** est un format de fichier **texte brut** utilisé pour représenter des **données tabulaires** (lignes et colonnes). Chaque ligne du fichier correspond à une **ligne de données**, et les valeurs de chaque colonne sont séparées par un **délimiteur** (généralement une virgule, d'où son nom).

CSV est le format **universel d'échange de données** : exporté par Excel, Google Sheets, bases de données, logs serveurs, et manipulable par tous les langages de programmation. Sa simplicité en fait le choix privilégié pour les **imports/exports**, **migrations de données**, **logs structurés**, et **analyses de données**.

!!! info "Pourquoi c'est important ?"
    CSV permet l'**échange de données** entre systèmes hétérogènes, l'**import/export** massif, le **traitement batch**, l'**analyse de logs**, la **génération de rapports**, et constitue le format standard pour les **outils de data science** (pandas, R).

## Structure CSV

### Format de base

**Fichier CSV simple :**
```csv
nom,prenom,age,ville
Dupont,Alice,28,Paris
Martin,Bob,35,Lyon
Dubois,Charlie,42,Marseille
```

**Structure :**

- **Première ligne** : En-têtes (noms des colonnes)
- **Lignes suivantes** : Données
- **Séparateur** : Virgule `,` (peut être `;`, `\t`, `|`)

### Règles et variations

**Gestion des virgules dans les valeurs :**
```csv
nom,prenom,adresse
Dupont,Alice,"12 rue des Fleurs, Paris"
Martin,Bob,"Appartement 5, 3ème étage, Lyon"
```

**Guillemets doubles échappés :**
```csv
nom,citation
Shakespeare,"To be, or not to be: that is the ""question"""
Einstein,"E=mc²"
```

**Caractères spéciaux et encodage :**
```csv
nom,prenom,commentaire
Müller,François,"Caractères accentués: é à ç"
O'Brien,Seán,"Apostrophes et accents"
```

**Variations de délimiteurs :**
```csv
# Séparateur point-virgule (Excel européen)
nom;prenom;age
Dupont;Alice;28

# Séparateur tabulation (TSV)
nom	prenom	age
Dupont	Alice	28

# Séparateur pipe
nom|prenom|age
Dupont|Alice|28
```

## Cas d'usage en cybersécurité

!!! danger "Attention - prenez ses exemples de contenu avec ce que l'on peut obtenir. Il n'est pas question de l'analyser ici."

### Exemple 1 : Logs de connexion

!!! example "Exemple n°1 - Logs de connexion"

    ```csv
    timestamp,ip_source,username,action,resultat,pays
    2025-11-15 10:23:45,192.168.1.100,alice,login,success,FR
    2025-11-15 10:24:12,203.0.113.50,bob,login,failed,CN
    2025-11-15 10:24:15,203.0.113.50,bob,login,failed,CN
    2025-11-15 10:24:18,203.0.113.50,bob,login,failed,CN
    2025-11-15 10:25:03,10.0.0.50,charlie,sudo,success,FR
    2025-11-15 10:26:30,198.51.100.25,admin,login,failed,RU
    ```

### Exemple 2 : Scan de vulnérabilités

!!! example "Exemple n°2 - Scan de vulnérabilités"

    ```csv
    ip,port,service,version,vulnerabilite,criticite,cve
    192.168.1.10,22,SSH,OpenSSH 7.2,Weak Encryption,MEDIUM,CVE-2016-6210
    192.168.1.10,80,HTTP,Apache 2.4.7,Outdated,LOW,CVE-2017-9798
    192.168.1.15,3306,MySQL,5.5.62,SQL Injection,HIGH,CVE-2019-2614
    192.168.1.20,21,FTP,vsftpd 2.3.4,Backdoor,CRITICAL,CVE-2011-2523
    192.168.1.25,445,SMB,SMBv1,EternalBlue,CRITICAL,CVE-2017-0144
    ```

### Exemple 3 : Audit permissions fichiers

!!! example "Exemple n°3 - Audit permissions fichiers"

    ```csv
    fichier,proprietaire,groupe,permissions,modification,taille
    /etc/passwd,root,root,644,2025-11-15 08:00:00,2048
    /etc/shadow,root,shadow,640,2025-11-15 08:00:00,1024
    /var/www/html/index.php,www-data,www-data,644,2025-11-14 15:30:00,5120
    /home/alice/.ssh/id_rsa,alice,alice,600,2025-11-10 12:00:00,3072
    /tmp/suspicious.sh,nobody,nogroup,777,2025-11-15 09:45:00,512
    ```

## Manipulation CSV par langage

### :fontawesome-brands-python: Python

**Lecture CSV avec module standard :**
```python
import csv

# Lecture basique
with open('users.csv', 'r', encoding='utf-8') as fichier:
    lecteur = csv.reader(fichier)
    
    # Lire les en-têtes
    entetes = next(lecteur)
    print(f"Colonnes : {entetes}")
    
    # Lire les données
    for ligne in lecteur:
        nom, prenom, age, ville = ligne
        print(f"{prenom} {nom} ({age} ans) - {ville}")
```

**Lecture avec DictReader (recommandé) :**
```python
import csv

with open('logs.csv', 'r', encoding='utf-8') as fichier:
    lecteur = csv.DictReader(fichier)
    
    for ligne in lecteur:
        # Accès par nom de colonne
        timestamp = ligne['timestamp']
        ip = ligne['ip_source']
        action = ligne['action']
        
        if ligne['resultat'] == 'failed':
            print(f"❌ Échec connexion : {ligne['username']} depuis {ip}")
```

!!! info "Pourquoi c'est recommandé ?"
    **DictReader** permet d'accéder aux colonnes par **nom** plutôt que par index, rendant le code **plus lisible et maintenable**. Si l'ordre des colonnes change dans le CSV, le code continue de fonctionner sans modification.

**Écriture CSV :**
```python
import csv

# Données à écrire
utilisateurs = [
    {'nom': 'Dupont', 'prenom': 'Alice', 'age': 28, 'role': 'admin'},
    {'nom': 'Martin', 'prenom': 'Bob', 'age': 35, 'role': 'user'},
    {'nom': 'Dubois', 'prenom': 'Charlie', 'age': 42, 'role': 'user'}
]

with open('output.csv', 'w', encoding='utf-8', newline='') as fichier:
    colonnes = ['nom', 'prenom', 'age', 'role']
    writer = csv.DictWriter(fichier, fieldnames=colonnes)
    
    # Écrire en-têtes
    writer.writeheader()
    
    # Écrire données
    writer.writerows(utilisateurs)
```

**Analyse de logs de sécurité :**
```python
import csv
from collections import Counter
from datetime import datetime

def analyser_logs_connexion(fichier_csv):
    """Analyse les tentatives de connexion échouées"""
    
    echecs_par_ip = Counter()
    echecs_par_user = Counter()
    
    with open(fichier_csv, 'r', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        
        for ligne in lecteur:
            if ligne['resultat'] == 'failed':
                echecs_par_ip[ligne['ip_source']] += 1
                echecs_par_user[ligne['username']] += 1
    
    # Détecter attaques brute-force
    print("=== IPs suspectes (>3 échecs) ===")
    for ip, count in echecs_par_ip.items():
        if count > 3:
            print(f"🚨 {ip}: {count} tentatives échouées")
    
    # Comptes ciblés
    print("\n=== Comptes ciblés ===")
    for user, count in echecs_par_user.most_common(5):
        print(f"   {user}: {count} échecs")

# Utilisation
analyser_logs_connexion('logs.csv')
```

**Filtrage et transformation :**
```python
import csv

def filtrer_vulnerabilites_critiques(input_file, output_file):
    """Extrait uniquement les vulnérabilités CRITICAL et HIGH"""
    
    with open(input_file, 'r', encoding='utf-8') as f_in:
        lecteur = csv.DictReader(f_in)
        
        # Filtrer
        vuln_critiques = [
            ligne for ligne in lecteur 
            if ligne['criticite'] in ['CRITICAL', 'HIGH']
        ]
    
    # Écrire résultat
    if vuln_critiques:
        with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
            colonnes = vuln_critiques[0].keys()
            writer = csv.DictWriter(f_out, fieldnames=colonnes)
            writer.writeheader()
            writer.writerows(vuln_critiques)
        
        print(f"✅ {len(vuln_critiques)} vulnérabilités critiques extraites")

# Utilisation
filtrer_vulnerabilites_critiques('scan.csv', 'critiques.csv')
```

**Avec pandas (bibliothèque data science) :**
```python
import pandas as pd

# Lecture ultra-simple
df = pd.read_csv('logs.csv')

# Filtrage élégant
echecs = df[df['resultat'] == 'failed']

# Groupement et comptage
attaques_par_ip = echecs.groupby('ip_source').size()
ips_suspectes = attaques_par_ip[attaques_par_ip > 3]

print("IPs avec >3 tentatives :")
print(ips_suspectes)

# Export résultat
ips_suspectes.to_csv('ips_blacklist.csv', header=['count'])
```

### :fontawesome-brands-js: JavaScript -  (Node.js)

**Lecture avec csv-parser**

```javascript
const fs = require('fs'); // package standard "file-system"
const csv = require('csv-parser');

// Installation : npm install csv-parser

const resultats = [];

fs.createReadStream('users.csv')
    .pipe(csv())
    .on('data', (ligne) => {
        // Chaque ligne est un objet
        console.log(`${ligne.prenom} ${ligne.nom} (${ligne.age} ans)`);
        resultats.push(ligne);
    })
    .on('end', () => {
        console.log(`\n✅ ${resultats.length} lignes lues`);
    })
    .on('error', (err) => {
        console.error('❌ Erreur:', err);
    });
```

**Écriture avec csv-writer**
  
```javascript
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Installation : npm install csv-writer

const csvWriter = createCsvWriter({
    path: 'output.csv',
    header: [
        {id: 'nom', title: 'Nom'},
        {id: 'prenom', title: 'Prénom'},
        {id: 'age', title: 'Âge'},
        {id: 'role', title: 'Rôle'}
    ]
});

const donnees = [
    {nom: 'Dupont', prenom: 'Alice', age: 28, role: 'admin'},
    {nom: 'Martin', prenom: 'Bob', age: 35, role: 'user'},
    {nom: 'Dubois', prenom: 'Charlie', age: 42, role: 'user'}
];

csvWriter.writeRecords(donnees)
    .then(() => {
        console.log('✅ Fichier CSV créé avec succès');
    })
    .catch((err) => {
        console.error('❌ Erreur:', err);
    });
```

**Analyse de logs (async/await)**

```javascript
const fs = require('fs');
const csv = require('csv-parser');

async function analyserLogs(fichierCsv) {
    return new Promise((resolve, reject) => {
        const echecs = [];
        const ipCounter = {};
        
        fs.createReadStream(fichierCsv)
            .pipe(csv())
            .on('data', (ligne) => {
                if (ligne.resultat === 'failed') {
                    echecs.push(ligne);
                    
                    // Compter par IP
                    const ip = ligne.ip_source;
                    ipCounter[ip] = (ipCounter[ip] || 0) + 1;
                }
            })
            .on('end', () => {
                // IPs suspectes (>3 échecs)
                const suspectes = Object.entries(ipCounter)
                    .filter(([ip, count]) => count > 3)
                    .map(([ip, count]) => ({ip, count}));
                
                resolve({
                    totalEchecs: echecs.length,
                    ipsSuspectes: suspectes
                });
            })
            .on('error', reject);
    });
}

// Utilisation
(async () => {
    try {
        const resultats = await analyserLogs('logs.csv');
        
        console.log(`📊 Total échecs: ${resultats.totalEchecs}`);
        console.log('\n🚨 IPs suspectes:');
        
        resultats.ipsSuspectes.forEach(({ip, count}) => {
            console.log(`   ${ip}: ${count} tentatives`);
        });
    } catch (err) {
        console.error('❌ Erreur:', err);
    }
})();
```

!!! quote "IIFE rencontré dans le code ci-dessus"
    L'**IIFE**[^1] `(async () => { ... })()` encapsule le code asynchrone pour pouvoir utiliser `await` au niveau racine. En JavaScript, `await` ne peut être utilisé que dans une fonction `async`, d'où cette syntaxe qui crée et exécute immédiatement une fonction asynchrone anonyme.


**Filtrage et transformation**
  
```javascript
const fs = require('fs');
const csv = require('csv-parser');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

async function filtrerVulnerabilites(inputFile, outputFile) {
    const critiques = [];
    
    // Lecture et filtrage
    await new Promise((resolve, reject) => {
        fs.createReadStream(inputFile)
            .pipe(csv())
            .on('data', (ligne) => {
                if (['CRITICAL', 'HIGH'].includes(ligne.criticite)) {
                    critiques.push(ligne);
                }
            })
            .on('end', resolve)
            .on('error', reject);
    });
    
    // Écriture résultat
    if (critiques.length > 0) {
        const colonnes = Object.keys(critiques[0]);
        
        const writer = createCsvWriter({
            path: outputFile,
            header: colonnes.map(col => ({id: col, title: col}))
        });
        
        await writer.writeRecords(critiques);
        console.log(`✅ ${critiques.length} vulnérabilités critiques extraites`);
    }
}

// Utilisation
filtrerVulnerabilites('scan.csv', 'critiques.csv')
    .catch(err => console.error('❌ Erreur:', err));
```

### :fontawesome-brands-php: PHP
    
**Lecture CSV"**

```php
<?php

// Lecture basique
$fichier = fopen('users.csv', 'r');

// Lire en-têtes
$entetes = fgetcsv($fichier);
echo "Colonnes : " . implode(', ', $entetes) . "\n\n";

// Lire données
while (($ligne = fgetcsv($fichier)) !== false) {
    list($nom, $prenom, $age, $ville) = $ligne;
    echo "$prenom $nom ($age ans) - $ville\n";
}

fclose($fichier);
?>
```

**Lecture avec en-têtes associatifs**
  
```php
<?php

function lireCsvAvecEntetes($fichierCsv) {
    $fichier = fopen($fichierCsv, 'r');
    
    // Lire en-têtes
    $entetes = fgetcsv($fichier);
    
    $donnees = [];
    while (($ligne = fgetcsv($fichier)) !== false) {
        // Combiner en-têtes et valeurs
        $donnees[] = array_combine($entetes, $ligne);
    }
    
    fclose($fichier);
    return $donnees;
}

// Utilisation
$logs = lireCsvAvecEntetes('logs.csv');

foreach ($logs as $log) {
    if ($log['resultat'] === 'failed') {
        echo "❌ Échec: {$log['username']} depuis {$log['ip_source']}\n";
    }
}
?>
```

**Écriture CSV :**

```php
<?php

$utilisateurs = [
    ['nom' => 'Dupont', 'prenom' => 'Alice', 'age' => 28, 'role' => 'admin'],
    ['nom' => 'Martin', 'prenom' => 'Bob', 'age' => 35, 'role' => 'user'],
    ['nom' => 'Dubois', 'prenom' => 'Charlie', 'age' => 42, 'role' => 'user']
];

$fichier = fopen('output.csv', 'w');

// Écrire en-têtes
$colonnes = array_keys($utilisateurs[0]);
fputcsv($fichier, $colonnes);

// Écrire données
foreach ($utilisateurs as $user) {
    fputcsv($fichier, $user);
}

fclose($fichier);
echo "✅ Fichier CSV créé\n";
?>
```

**Analyse de logs de sécurité :**

```php
<?php

function analyserLogsConnexion($fichierCsv) {
    $fichier = fopen($fichierCsv, 'r');
    $entetes = fgetcsv($fichier);
    
    $echecs_par_ip = [];
    $echecs_par_user = [];
    
    while (($ligne = fgetcsv($fichier)) !== false) {
        $log = array_combine($entetes, $ligne);
        
        if ($log['resultat'] === 'failed') {
            // Compter par IP
            $ip = $log['ip_source'];
            $echecs_par_ip[$ip] = ($echecs_par_ip[$ip] ?? 0) + 1;
            
            // Compter par utilisateur
            $user = $log['username'];
            $echecs_par_user[$user] = ($echecs_par_user[$user] ?? 0) + 1;
        }
    }
    
    fclose($fichier);
    
    // Afficher IPs suspectes
    echo "=== IPs suspectes (>3 échecs) ===\n";
    foreach ($echecs_par_ip as $ip => $count) {
        if ($count > 3) {
            echo "🚨 $ip: $count tentatives échouées\n";
        }
    }
    
    // Afficher comptes ciblés
    echo "\n=== Comptes ciblés ===\n";
    arsort($echecs_par_user);
    foreach (array_slice($echecs_par_user, 0, 5, true) as $user => $count) {
        echo "   $user: $count échecs\n";
    }
}

// Utilisation
analyserLogsConnexion('logs.csv');
?>
```

**Filtrage avec délimiteur personnalisé :**

```php
<?php

function filtrerVulnerabilites($inputFile, $outputFile, $delimiter = ',') {
    $input = fopen($inputFile, 'r');
    $entetes = fgetcsv($input, 0, $delimiter);
    
    $critiques = [];
    
    while (($ligne = fgetcsv($input, 0, $delimiter)) !== false) {
        $vuln = array_combine($entetes, $ligne);
        
        if (in_array($vuln['criticite'], ['CRITICAL', 'HIGH'])) {
            $critiques[] = $ligne;
        }
    }
    
    fclose($input);
    
    // Écrire résultat
    if (!empty($critiques)) {
        $output = fopen($outputFile, 'w');
        fputcsv($output, $entetes, $delimiter);
        
        foreach ($critiques as $ligne) {
            fputcsv($output, $ligne, $delimiter);
        }
        
        fclose($output);
        echo "✅ " . count($critiques) . " vulnérabilités critiques extraites\n";
    }
}

// Utilisation
filtrerVulnerabilites('scan.csv', 'critiques.csv');
?>
```

### :fontawesome-brands-golang: Go (Golang)

**Lecture CSV :**

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
)

func main() {
    // Ouvrir fichier
    fichier, err := os.Open("users.csv")
    if err != nil {
        panic(err)
    }
    defer fichier.Close()
    
    // Créer lecteur CSV
    lecteur := csv.NewReader(fichier)
    
    // Lire toutes les lignes
    lignes, err := lecteur.ReadAll()
    if err != nil {
        panic(err)
    }
    
    // En-têtes
    entetes := lignes[0]
    fmt.Printf("Colonnes : %v\n\n", entetes)
    
    // Données
    for _, ligne := range lignes[1:] {
        nom, prenom, age, ville := ligne[0], ligne[1], ligne[2], ligne[3]
        fmt.Printf("%s %s (%s ans) - %s\n", prenom, nom, age, ville)
    }
}
```

**Lecture avec structure typée :**

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
    "strconv"
)

type Utilisateur struct {
    Nom    string
    Prenom string
    Age    int
    Ville  string
}

func lireUtilisateurs(fichierCsv string) ([]Utilisateur, error) {
    fichier, err := os.Open(fichierCsv)
    if err != nil {
        return nil, err
    }
    defer fichier.Close()
    
    lecteur := csv.NewReader(fichier)
    lignes, err := lecteur.ReadAll()
    if err != nil {
        return nil, err
    }
    
    var utilisateurs []Utilisateur
    
    // Ignorer en-têtes (lignes[0])
    for _, ligne := range lignes[1:] {
        age, _ := strconv.Atoi(ligne[2])
        
        utilisateurs = append(utilisateurs, Utilisateur{
            Nom:    ligne[0],
            Prenom: ligne[1],
            Age:    age,
            Ville:  ligne[3],
        })
    }
    
    return utilisateurs, nil
}

func main() {
    users, err := lireUtilisateurs("users.csv")
    if err != nil {
        panic(err)
    }
    
    for _, u := range users {
        fmt.Printf("%s %s (%d ans) - %s\n", u.Prenom, u.Nom, u.Age, u.Ville)
    }
}
```

**Écriture CSV :**

```go
package main

import (
    "encoding/csv"
    "os"
)

type Utilisateur struct {
    Nom    string
    Prenom string
    Age    int
    Role   string
}

func main() {
    utilisateurs := []Utilisateur{
        {"Dupont", "Alice", 28, "admin"},
        {"Martin", "Bob", 35, "user"},
        {"Dubois", "Charlie", 42, "user"},
    }
    
    // Créer fichier
    fichier, err := os.Create("output.csv")
    if err != nil {
        panic(err)
    }
    defer fichier.Close()
    
    writer := csv.NewWriter(fichier)
    defer writer.Flush()
    
    // Écrire en-têtes
    entetes := []string{"nom", "prenom", "age", "role"}
    writer.Write(entetes)
    
    // Écrire données
    for _, u := range utilisateurs {
        ligne := []string{
            u.Nom,
            u.Prenom,
            fmt.Sprintf("%d", u.Age),
            u.Role,
        }
        writer.Write(ligne)
    }
    
    fmt.Println("✅ Fichier CSV créé")
}
```

**Analyse de logs :**

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
)

type LogConnexion struct {
    Timestamp string
    IPSource  string
    Username  string
    Action    string
    Resultat  string
    Pays      string
}

func analyserLogs(fichierCsv string) {
    fichier, err := os.Open(fichierCsv)
    if err != nil {
        panic(err)
    }
    defer fichier.Close()
    
    lecteur := csv.NewReader(fichier)
    lignes, _ := lecteur.ReadAll()
    
    echecsParIP := make(map[string]int)
    echecsParUser := make(map[string]int)
    
    // Ignorer en-têtes
    for _, ligne := range lignes[1:] {
        log := LogConnexion{
            Timestamp: ligne[0],
            IPSource:  ligne[1],
            Username:  ligne[2],
            Action:    ligne[3],
            Resultat:  ligne[4],
            Pays:      ligne[5],
        }
        
        if log.Resultat == "failed" {
            echecsParIP[log.IPSource]++
            echecsParUser[log.Username]++
        }
    }
    
    // Afficher IPs suspectes
    fmt.Println("=== IPs suspectes (>3 échecs) ===")
    for ip, count := range echecsParIP {
        if count > 3 {
            fmt.Printf("🚨 %s: %d tentatives échouées\n", ip, count)
        }
    }
    
    // Afficher comptes ciblés
    fmt.Println("\n=== Comptes ciblés ===")
    for user, count := range echecsParUser {
        fmt.Printf("   %s: %d échecs\n", user, count)
    }
}

func main() {
    analyserLogs("logs.csv")
}
```

**Filtrage avec concurrence :**

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
    "sync"
)

type Vulnerabilite struct {
    IP          string
    Port        string
    Service     string
    Version     string
    Vuln        string
    Criticite   string
    CVE         string
}

func filtrerVulnerabilites(inputFile, outputFile string) {
    // Lecture
    input, _ := os.Open(inputFile)
    defer input.Close()
    
    lecteur := csv.NewReader(input)
    lignes, _ := lecteur.ReadAll()
    entetes := lignes[0]
    
    // Filtrage concurrent
    var wg sync.WaitGroup
    critiques := make([][]string, 0)
    mu := sync.Mutex{}
    
    for _, ligne := range lignes[1:] {
        wg.Add(1)
        go func(l []string) {
            defer wg.Done()
            
            criticite := l[5] // Index colonne criticite
            if criticite == "CRITICAL" || criticite == "HIGH" {
                mu.Lock()
                critiques = append(critiques, l)
                mu.Unlock()
            }
        }(ligne)
    }
    
    wg.Wait()
    
    // Écriture
    if len(critiques) > 0 {
        output, _ := os.Create(outputFile)
        defer output.Close()
        
        writer := csv.NewWriter(output)
        defer writer.Flush()
        
        writer.Write(entetes)
        writer.WriteAll(critiques)
        
        fmt.Printf("✅ %d vulnérabilités critiques extraites\n", len(critiques))
    }
}

func main() {
    filtrerVulnerabilites("scan.csv", "critiques.csv")
}
```

### :fontawesome-brands-rust: Rust

**Lecture CSV avec csv crate :**

```rust
use csv::Reader;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    // Créer lecteur
    let mut lecteur = Reader::from_path("users.csv")?;
    
    // Lire en-têtes
    let entetes = lecteur.headers()?;
    println!("Colonnes : {:?}\n", entetes);
    
    // Lire données
    for resultat in lecteur.records() {
        let ligne = resultat?;
        
        let nom = &ligne[0];
        let prenom = &ligne[1];
        let age = &ligne[2];
        let ville = &ligne[3];
        
        println!("{} {} ({} ans) - {}", prenom, nom, age, ville);
    }
    
    Ok(())
}
```

**Lecture avec serde (désérialisation automatique) :**

```rust
use csv::Reader;
use serde::Deserialize;
use std::error::Error;

#[derive(Debug, Deserialize)]
struct Utilisateur {
    nom: String,
    prenom: String,
    age: u32,
    ville: String,
}

fn lire_utilisateurs(fichier_csv: &str) -> Result<Vec<Utilisateur>, Box<dyn Error>> {
    let mut lecteur = Reader::from_path(fichier_csv)?;
    let mut utilisateurs = Vec::new();
    
    for resultat in lecteur.deserialize() {
        let utilisateur: Utilisateur = resultat?;
        utilisateurs.push(utilisateur);
    }
    
    Ok(utilisateurs)
}

fn main() -> Result<(), Box<dyn Error>> {
    let users = lire_utilisateurs("users.csv")?;
    
    for u in users {
        println!("{} {} ({} ans) - {}", u.prenom, u.nom, u.age, u.ville);
    }
    
    Ok(())
}
```

**Écriture CSV :**

```rust
use csv::Writer;
use serde::Serialize;
use std::error::Error;

#[derive(Debug, Serialize)]
struct Utilisateur {
    nom: String,
    prenom: String,
    age: u32,
    role: String,
}

fn main() -> Result<(), Box<dyn Error>> {
    let utilisateurs = vec![
        Utilisateur {
            nom: "Dupont".to_string(),
            prenom: "Alice".to_string(),
            age: 28,
            role: "admin".to_string(),
        },
        Utilisateur {
            nom: "Martin".to_string(),
            prenom: "Bob".to_string(),
            age: 35,
            role: "user".to_string(),
        },
        Utilisateur {
            nom: "Dubois".to_string(),
            prenom: "Charlie".to_string(),
            age: 42,
            role: "user".to_string(),
        },
    ];
    
    // Créer writer
    let mut writer = Writer::from_path("output.csv")?;
    
    // Écrire données (en-têtes automatiques avec serde)
    for utilisateur in utilisateurs {
        writer.serialize(utilisateur)?;
    }
    
    writer.flush()?;
    println!("✅ Fichier CSV créé");
    
    Ok(())
}
```

**Analyse de logs avec HashMap :**

```rust
use csv::Reader;
use serde::Deserialize;
use std::collections::HashMap;
use std::error::Error;

#[derive(Debug, Deserialize)]
struct LogConnexion {
    timestamp: String,
    ip_source: String,
    username: String,
    action: String,
    resultat: String,
    pays: String,
}

fn analyser_logs(fichier_csv: &str) -> Result<(), Box<dyn Error>> {
    let mut lecteur = Reader::from_path(fichier_csv)?;
    
    let mut echecs_par_ip: HashMap<String, u32> = HashMap::new();
    let mut echecs_par_user: HashMap<String, u32> = HashMap::new();
    
    for resultat in lecteur.deserialize() {
        let log: LogConnexion = resultat?;
        
        if log.resultat == "failed" {
            // Compter par IP
            *echecs_par_ip.entry(log.ip_source.clone()).or_insert(0) += 1;
            
            // Compter par utilisateur
            *echecs_par_user.entry(log.username.clone()).or_insert(0) += 1;
        }
    }
    
    // Afficher IPs suspectes
    println!("=== IPs suspectes (>3 échecs) ===");
    for (ip, count) in &echecs_par_ip {
        if *count > 3 {
            println!("🚨 {}: {} tentatives échouées", ip, count);
        }
    }
    
    // Afficher comptes ciblés
    println!("\n=== Comptes ciblés ===");
    let mut vec_users: Vec<_> = echecs_par_user.iter().collect();
    vec_users.sort_by(|a, b| b.1.cmp(a.1));
    
    for (user, count) in vec_users.iter().take(5) {
        println!("   {}: {} échecs", user, count);
    }
    
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    analyser_logs("logs.csv")
}
```

**Filtrage avec traitement parallèle (rayon) :**

```rust
use csv::{Reader, Writer};
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::error::Error;

#[derive(Debug, Deserialize, Serialize, Clone)]
struct Vulnerabilite {
    ip: String,
    port: String,
    service: String,
    version: String,
    vulnerabilite: String,
    criticite: String,
    cve: String,
}

fn filtrer_vulnerabilites(
    input_file: &str,
    output_file: &str
) -> Result<(), Box<dyn Error>> {
    // Lecture
    let mut lecteur = Reader::from_path(input_file)?;
    let vulnerabilites: Vec<Vulnerabilite> = lecteur
        .deserialize()
        .collect::<Result<Vec<_>, _>>()?;
    
    // Filtrage parallèle avec rayon
    let critiques: Vec<Vulnerabilite> = vulnerabilites
        .par_iter()
        .filter(|v| v.criticite == "CRITICAL" || v.criticite == "HIGH")
        .cloned()
        .collect();
    
    // Écriture
    if !critiques.is_empty() {
        let mut writer = Writer::from_path(output_file)?;
        
        for vuln in &critiques {
            writer.serialize(vuln)?;
        }
        
        writer.flush()?;
        println!("✅ {} vulnérabilités critiques extraites", critiques.len());
    }
    
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    filtrer_vulnerabilites("scan.csv", "critiques.csv")
}
```

## Le mot de la fin

!!! quote
    **CSV est le format universel de l'échange de données** - simple, lisible, et supporté par tous les langages et outils. Sa simplicité apparente cache une puissance réelle pour le traitement de données tabulaires à grande échelle.
    
    Chaque langage offre ses propres abstractions : 
    
    - **Python avec pandas** pour l'analyse de données
    - **JavaScript avec streams** pour le traitement asynchrone
    - **PHP avec ses fonctions natives** pour l'intégration web
    - **Go avec sa concurrence** pour la performance
    - **Rust avec serde** pour la sécurité de types.
    
    Maîtriser CSV c'est comprendre ses **limites** (pas de types, pas de hiérarchie) et ses **forces** (_universalité, performance, simplicité_). Pour des données simples et tabulaires, CSV reste imbattable.

---

[^1]: En développement JavaScript, **une IIFE** est une fonction immédiatement invoquée qui s’exécute dès sa définition afin d’isoler des variables et éviter toute pollution de l’espace global.
