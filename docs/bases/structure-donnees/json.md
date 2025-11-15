---
description: "Maîtriser le format JSON pour l'échange de données structurées"
icon: lucide/book-open-check
tags: ["JSON", "DONNÉES", "FORMATS", "API", "DÉVELOPPEMENT"]
---

# JSON - JavaScript Object Notation

## Introduction

**Niveau :** Débutant & Intermédiaire

!!! quote "Analogie pédagogique"
    _Imaginez un **carnet d'adresses organisé** où chaque personne possède non seulement un nom et un numéro, mais aussi une adresse complète (rue, ville, code postal), plusieurs téléphones (mobile, fixe, bureau), et même des contacts d'urgence qui ont eux-mêmes la même structure. **JSON fonctionne exactement ainsi** : c'est un format qui permet de représenter des données **hiérarchiques et complexes** de manière lisible par les humains tout en restant facile à parser pour les machines._

> **JSON (JavaScript Object Notation)** est un format de **données textuelles** léger et structuré, utilisé pour représenter des **objets, tableaux et valeurs primitives**. Bien qu'initialement dérivé de JavaScript, JSON est devenu un **standard universel** pour l'échange de données entre applications, indépendamment du langage de programmation utilisé.

JSON a **supplanté XML** comme format privilégié pour les **APIs REST**, les **fichiers de configuration**, les **bases de données NoSQL**, et la **communication client-serveur**. Sa syntaxe simple et sa capacité à représenter des structures complexes en font le choix standard pour tout échange de données moderne.

!!! info "Pourquoi c'est important ?"
    JSON est omniprésent : **APIs REST**, **configuration d'applications** (package.json, composer.json), **stockage NoSQL** (MongoDB, CouchDB), **logs structurés**, **webhooks**, **réponses serveur**, et constitue le format standard de communication web moderne.

## Structure JSON

### Types de données

JSON supporte **six types de données** :

**1. String (chaîne de caractères)**
```json
{
  "nom": "Alice Dupont",
  "description": "Administrateur système"
}
```

**2. Number (nombre)**
```json
{
  "age": 28,
  "score": 95.5,
  "temperature": -15.3,
  "scientifique": 1.5e+10
}
```

!!! info "JSON ne distingue pas entiers et décimaux"
    Contrairement à d'autres langages, JSON a un seul type **Number** qui englobe entiers, décimaux, et notation scientifique.

**3. Boolean (booléen)**
```json
{
  "actif": true,
  "admin": false
}
```

**4. Null (valeur nulle)**
```json
{
  "middle_name": null,
  "deleted_at": null
}
```

**5. Array (tableau)**
```json
{
  "roles": ["admin", "user", "moderator"],
  "scores": [98, 87, 92, 100],
  "mixte": [1, "texte", true, null]
}
```

**6. Object (objet/dictionnaire)**
```json
{
  "utilisateur": {
    "nom": "Dupont",
    "prenom": "Alice",
    "contact": {
      "email": "alice@example.com",
      "telephone": "+33612345678"
    }
  }
}
```

!!! example "Exemple complet combinant tous les types"

    ```json
    {
      "nom": "Alice",
      "age": 28,
      "actif": true,
      "middle_name": null,
      "roles": ["admin", "user"],
      "contact": {
        "email": "alice@example.com"
      }
    }
    ```

**Règles syntaxiques strictes :**

- ✅ **Guillemets doubles** obligatoires pour les clés et chaînes : `"nom": "Alice"`
- ❌ **Pas de guillemets simples** : `'nom': 'Alice'` est invalide
- ❌ **Pas de virgule finale** : `{"a": 1, "b": 2,}` est invalide
- ✅ **Encodage UTF-8** pour les caractères spéciaux
- ❌ **Pas de commentaires** dans JSON pur (contrairement à JavaScript)

### Structures de base

**Objet JSON (dictionnaire/map) :**
```json
{
  "nom": "Dupont",
  "prenom": "Alice",
  "age": 28,
  "actif": true,
  "roles": ["admin", "user"]
}
```

**Tableau JSON (liste/array) :**
```json
[
  {
    "id": 1,
    "nom": "Alice"
  },
  {
    "id": 2,
    "nom": "Bob"
  },
  {
    "id": 3,
    "nom": "Charlie"
  }
]
```

**Imbrication complexe :**
```json
{
  "utilisateur": {
    "id": 1234,
    "identite": {
      "nom": "Dupont",
      "prenom": "Alice",
      "date_naissance": "1997-03-15"
    },
    "contact": {
      "email": "alice@example.com",
      "telephones": [
        {
          "type": "mobile",
          "numero": "+33612345678"
        },
        {
          "type": "fixe",
          "numero": "+33145678901"
        }
      ]
    },
    "permissions": {
      "lecture": true,
      "ecriture": true,
      "admin": false
    }
  }
}
```

## Cas d'usage en cybersécurité

!!! danger "Attention - prenez ces exemples de contenu avec ce que l'on peut obtenir. Il n'est pas question de l'analyser ici."

### Exemple 1 : Résultat de scan de vulnérabilités

!!! example "Exemple n°1 - Rapport de scan Nessus/OpenVAS"

    ```json
    {
      "scan_id": "scan_20251115_103045",
      "timestamp": "2025-11-15T10:30:45Z",
      "target": "192.168.1.0/24",
      "vulnerabilities": [
        {
          "host": "192.168.1.10",
          "port": 22,
          "service": "SSH",
          "vulnerability": {
            "name": "Weak SSH Encryption Algorithms",
            "severity": "MEDIUM",
            "cvss_score": 5.3,
            "cve": ["CVE-2016-6210"],
            "description": "Server supports weak encryption algorithms",
            "recommendation": "Disable weak ciphers in sshd_config"
          }
        },
        {
          "host": "192.168.1.15",
          "port": 3306,
          "service": "MySQL",
          "vulnerability": {
            "name": "SQL Injection",
            "severity": "HIGH",
            "cvss_score": 8.1,
            "cve": ["CVE-2019-2614"],
            "description": "MySQL version vulnerable to SQL injection",
            "recommendation": "Upgrade to MySQL 5.7.26 or later"
          }
        },
        {
          "host": "192.168.1.20",
          "port": 445,
          "service": "SMB",
          "vulnerability": {
            "name": "EternalBlue",
            "severity": "CRITICAL",
            "cvss_score": 9.8,
            "cve": ["CVE-2017-0144"],
            "description": "SMBv1 vulnerable to remote code execution",
            "recommendation": "Disable SMBv1 immediately and patch system"
          }
        }
      ],
      "statistics": {
        "total_hosts": 256,
        "hosts_scanned": 45,
        "vulnerabilities_found": 3,
        "severity_breakdown": {
          "critical": 1,
          "high": 1,
          "medium": 1,
          "low": 0
        }
      }
    }
    ```

### Exemple 2 : Logs de firewall structurés

!!! example "Exemple n°2 - Événements firewall JSON"

    ```json
    {
      "events": [
        {
          "timestamp": "2025-11-15T10:23:45.123Z",
          "event_id": "fw_001",
          "action": "BLOCK",
          "source": {
            "ip": "203.0.113.50",
            "port": 54321,
            "country": "CN",
            "asn": "AS4134"
          },
          "destination": {
            "ip": "192.168.1.100",
            "port": 22,
            "service": "SSH"
          },
          "protocol": "TCP",
          "reason": "Blacklisted IP",
          "rule_id": "blacklist_001"
        },
        {
          "timestamp": "2025-11-15T10:24:12.456Z",
          "event_id": "fw_002",
          "action": "ALLOW",
          "source": {
            "ip": "192.168.1.50",
            "port": 45678,
            "country": "FR",
            "asn": "AS3215"
          },
          "destination": {
            "ip": "8.8.8.8",
            "port": 53,
            "service": "DNS"
          },
          "protocol": "UDP",
          "reason": "Legitimate DNS query",
          "rule_id": "allow_dns"
        }
      ]
    }
    ```

### Exemple 3 : Configuration de règles SIEM

!!! example "Exemple n°3 - Règles de détection SIEM"

    ```json
    {
      "rules": [
        {
          "id": "rule_001",
          "name": "Brute Force SSH Detection",
          "enabled": true,
          "severity": "HIGH",
          "conditions": {
            "event_type": "authentication",
            "service": "ssh",
            "result": "failed",
            "threshold": {
              "count": 5,
              "timeframe": "5m",
              "group_by": "source_ip"
            }
          },
          "actions": [
            {
              "type": "alert",
              "channels": ["email", "slack"]
            },
            {
              "type": "block",
              "duration": "1h",
              "target": "source_ip"
            }
          ]
        },
        {
          "id": "rule_002",
          "name": "Privilege Escalation Attempt",
          "enabled": true,
          "severity": "CRITICAL",
          "conditions": {
            "event_type": "command_execution",
            "command_contains": ["sudo", "su", "chmod 777"],
            "user_not_in_group": "admins"
          },
          "actions": [
            {
              "type": "alert",
              "priority": "P1",
              "channels": ["pagerduty", "email"]
            },
            {
              "type": "log",
              "retention": "90d"
            }
          ]
        }
      ]
    }
    ```

### Exemple 4 : Réponse API de threat intelligence

!!! example "Exemple n°4 - Enrichissement IP via API"

    ```json
    {
      "query": {
        "ip": "203.0.113.50",
        "timestamp": "2025-11-15T10:30:00Z"
      },
      "result": {
        "threat_score": 85,
        "classification": "malicious",
        "categories": [
          "botnet",
          "brute_force",
          "port_scanner"
        ],
        "geolocation": {
          "country": "CN",
          "city": "Beijing",
          "latitude": 39.9042,
          "longitude": 116.4074,
          "timezone": "Asia/Shanghai"
        },
        "network": {
          "asn": 4134,
          "organization": "Chinanet",
          "isp": "China Telecom"
        },
        "reputation": {
          "blacklists": [
            {
              "name": "Spamhaus",
              "listed": true,
              "listing_date": "2025-11-10"
            },
            {
              "name": "AbuseIPDB",
              "listed": true,
              "abuse_confidence": 92
            }
          ]
        },
        "recent_activity": [
          {
            "date": "2025-11-14",
            "type": "port_scan",
            "targets": 1247
          },
          {
            "date": "2025-11-13",
            "type": "ssh_bruteforce",
            "attempts": 5632
          }
        ]
      }
    }
    ```

## Manipulation JSON par langage

### :fontawesome-brands-python: Python

**Lecture JSON depuis fichier :**

```python
import json

# Lecture d'un fichier JSON
with open('config.json', 'r', encoding='utf-8') as fichier:
    donnees = json.load(fichier)

# Accès aux données
print(f"Nom: {donnees['nom']}")
print(f"Âge: {donnees['age']}")

# Navigation dans structures imbriquées
if 'adresse' in donnees:
    print(f"Ville: {donnees['adresse']['ville']}")
```

**Lecture JSON depuis string :**

```python
import json

# Parser une chaîne JSON
json_string = '{"nom": "Alice", "age": 28, "actif": true}'
donnees = json.loads(json_string)

print(donnees['nom'])  # Alice
print(type(donnees))   # <class 'dict'>
```

**Écriture JSON vers fichier :**

```python
import json

utilisateur = {
    "id": 1234,
    "nom": "Dupont",
    "prenom": "Alice",
    "roles": ["admin", "user"],
    "actif": True,
    "metadata": {
        "created_at": "2025-11-15T10:00:00Z",
        "last_login": "2025-11-15T15:30:00Z"
    }
}

# Écrire avec indentation (lisible)
with open('utilisateur.json', 'w', encoding='utf-8') as fichier:
    json.dump(utilisateur, fichier, indent=2, ensure_ascii=False)

# Convertir en string JSON
json_string = json.dumps(utilisateur, indent=2, ensure_ascii=False)
print(json_string)
```

**Options de formatage :**

```python
import json

donnees = {"nom": "Alice", "âge": 28, "ville": "Paris"}

# Compact (sans espaces)
compact = json.dumps(donnees, separators=(',', ':'))
# {"nom":"Alice","âge":28,"ville":"Paris"}

# Indenté et trié par clé
lisible = json.dumps(donnees, indent=2, sort_keys=True, ensure_ascii=False)
# {
#   "nom": "Alice",
#   "ville": "Paris",
#   "âge": 28
# }

# Encoder les caractères non-ASCII
ascii_only = json.dumps(donnees, ensure_ascii=True)
# {"nom": "Alice", "\u00e2ge": 28, "ville": "Paris"}
```

**Analyse de logs de sécurité :**

```python
import json
from collections import defaultdict
from datetime import datetime

def analyser_logs_firewall(fichier_json):
    """Analyse les événements firewall JSON"""
    
    with open(fichier_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Compteurs
    actions = defaultdict(int)
    ips_bloquees = defaultdict(int)
    pays_sources = defaultdict(int)
    
    for event in data['events']:
        # Compter par action
        actions[event['action']] += 1
        
        # IPs bloquées
        if event['action'] == 'BLOCK':
            ip = event['source']['ip']
            ips_bloquees[ip] += 1
            pays_sources[event['source']['country']] += 1
    
    # Rapport
    print("=== Statistiques Firewall ===")
    print(f"\nTotal événements: {len(data['events'])}")
    
    print("\n📊 Actions:")
    for action, count in actions.items():
        print(f"  {action}: {count}")
    
    print("\n🚨 Top 5 IPs bloquées:")
    for ip, count in sorted(ips_bloquees.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {ip}: {count} blocages")
    
    print("\n🌍 Pays sources:")
    for pays, count in sorted(pays_sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pays}: {count}")

# Utilisation
analyser_logs_firewall('firewall_logs.json')
```

**Filtrage de vulnérabilités critiques :**

```python
import json

def extraire_vulns_critiques(input_file, output_file):
    """Extrait les vulnérabilités CRITICAL et HIGH"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        scan = json.load(f)
    
    # Filtrer
    critiques = [
        vuln for vuln in scan['vulnerabilities']
        if vuln['vulnerability']['severity'] in ['CRITICAL', 'HIGH']
    ]
    
    # Créer rapport
    rapport = {
        "scan_id": scan['scan_id'],
        "timestamp": scan['timestamp'],
        "vulnerabilities_critiques": critiques,
        "count": len(critiques)
    }
    
    # Sauvegarder
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(critiques)} vulnérabilités critiques extraites")

# Utilisation
extraire_vulns_critiques('scan.json', 'critiques.json')
```

**Requête API avec requests :**

```python
import json
import requests

def interroger_threat_intel(ip_address):
    """Interroge une API de threat intelligence"""
    
    api_url = f"https://api.threatintel.example/v1/ip/{ip_address}"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"🔍 Analyse de {ip_address}")
        print(f"Score de menace: {data['result']['threat_score']}/100")
        print(f"Classification: {data['result']['classification']}")
        print(f"Catégories: {', '.join(data['result']['categories'])}")
        
        # Vérifier blacklists
        for bl in data['result']['reputation']['blacklists']:
            if bl['listed']:
                print(f"⚠️  Listée sur {bl['name']}")
    else:
        print(f"❌ Erreur API: {response.status_code}")

# Utilisation
interroger_threat_intel("203.0.113.50")
```

### :fontawesome-brands-js: JavaScript (Node.js)

**Lecture JSON depuis fichier :**

```javascript
const fs = require('fs');

// Méthode synchrone
const donnees = JSON.parse(fs.readFileSync('config.json', 'utf8'));
console.log(`Nom: ${donnees.nom}`);

// Méthode asynchrone (recommandée)
fs.readFile('config.json', 'utf8', (err, data) => {
    if (err) {
        console.error('❌ Erreur:', err);
        return;
    }
    
    const donnees = JSON.parse(data);
    console.log(`Nom: ${donnees.nom}`);
});

// Avec Promises (moderne)
const fs_promises = require('fs').promises;

async function lireConfig() {
    try {
        const data = await fs_promises.readFile('config.json', 'utf8');
        const donnees = JSON.parse(data);
        return donnees;
    } catch (err) {
        console.error('❌ Erreur:', err);
        throw err;
    }
}
```

**Lecture JSON depuis string :**

```javascript
// Parser une chaîne JSON
const jsonString = '{"nom": "Alice", "age": 28, "actif": true}';
const donnees = JSON.parse(jsonString);

console.log(donnees.nom);      // Alice
console.log(typeof donnees);   // object
```

**Écriture JSON vers fichier :**

```javascript
const fs = require('fs').promises;

const utilisateur = {
    id: 1234,
    nom: 'Dupont',
    prenom: 'Alice',
    roles: ['admin', 'user'],
    actif: true,
    metadata: {
        created_at: '2025-11-15T10:00:00Z',
        last_login: '2025-11-15T15:30:00Z'
    }
};

// Async/await
async function sauvegarder() {
    try {
        // Convertir en JSON avec indentation
        const jsonString = JSON.stringify(utilisateur, null, 2);
        
        await fs.writeFile('utilisateur.json', jsonString, 'utf8');
        console.log('✅ Fichier sauvegardé');
    } catch (err) {
        console.error('❌ Erreur:', err);
    }
}

sauvegarder();
```

**Options de formatage :**

```javascript
const donnees = {nom: 'Alice', âge: 28, ville: 'Paris'};

// Compact (sans espaces)
const compact = JSON.stringify(donnees);
// {"nom":"Alice","âge":28,"ville":"Paris"}

// Indenté (lisible)
const lisible = JSON.stringify(donnees, null, 2);
// {
//   "nom": "Alice",
//   "âge": 28,
//   "ville": "Paris"
// }

// Filtrer certaines propriétés
const filtre = JSON.stringify(donnees, ['nom', 'ville'], 2);
// {
//   "nom": "Alice",
//   "ville": "Paris"
// }

// Transformer avec fonction
const transforme = JSON.stringify(donnees, (key, value) => {
    if (typeof value === 'number') {
        return value.toString();
    }
    return value;
}, 2);
```

**Analyse de logs firewall :**

```javascript
const fs = require('fs').promises;

async function analyserLogsFirewall(fichierJson) {
    try {
        const data = JSON.parse(await fs.readFile(fichierJson, 'utf8'));
        
        // Compteurs
        const actions = {};
        const ipsBloqueesCount = {};
        const paysCount = {};
        
        data.events.forEach(event => {
            // Compter actions
            actions[event.action] = (actions[event.action] || 0) + 1;
            
            // IPs bloquées
            if (event.action === 'BLOCK') {
                const ip = event.source.ip;
                ipsBloqueesCount[ip] = (ipsBloqueesCount[ip] || 0) + 1;
                
                const pays = event.source.country;
                paysCount[pays] = (paysCount[pays] || 0) + 1;
            }
        });
        
        // Affichage
        console.log('=== Statistiques Firewall ===');
        console.log(`\nTotal événements: ${data.events.length}`);
        
        console.log('\n📊 Actions:');
        Object.entries(actions).forEach(([action, count]) => {
            console.log(`  ${action}: ${count}`);
        });
        
        console.log('\n🚨 Top 5 IPs bloquées:');
        Object.entries(ipsBloqueesCount)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .forEach(([ip, count]) => {
                console.log(`  ${ip}: ${count} blocages`);
            });
        
        console.log('\n🌍 Pays sources:');
        Object.entries(paysCount)
            .sort((a, b) => b[1] - a[1])
            .forEach(([pays, count]) => {
                console.log(`  ${pays}: ${count}`);
            });
            
    } catch (err) {
        console.error('❌ Erreur:', err);
    }
}

// Utilisation
analyserLogsFirewall('firewall_logs.json');
```

**Filtrage de vulnérabilités :**

```javascript
const fs = require('fs').promises;

async function extraireVulnsCritiques(inputFile, outputFile) {
    try {
        const scan = JSON.parse(await fs.readFile(inputFile, 'utf8'));
        
        // Filtrer
        const critiques = scan.vulnerabilities.filter(vuln => 
            ['CRITICAL', 'HIGH'].includes(vuln.vulnerability.severity)
        );
        
        // Créer rapport
        const rapport = {
            scan_id: scan.scan_id,
            timestamp: scan.timestamp,
            vulnerabilities_critiques: critiques,
            count: critiques.length
        };
        
        // Sauvegarder
        await fs.writeFile(
            outputFile, 
            JSON.stringify(rapport, null, 2),
            'utf8'
        );
        
        console.log(`✅ ${critiques.length} vulnérabilités critiques extraites`);
        
    } catch (err) {
        console.error('❌ Erreur:', err);
    }
}

// Utilisation
extraireVulnsCritiques('scan.json', 'critiques.json');
```

**Requête API avec fetch :**

```javascript
async function interrogerThreatIntel(ipAddress) {
    const apiUrl = `https://api.threatintel.example/v1/ip/${ipAddress}`;
    
    try {
        const response = await fetch(apiUrl, {
            headers: {
                'Authorization': 'Bearer YOUR_API_KEY',
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        console.log(`🔍 Analyse de ${ipAddress}`);
        console.log(`Score de menace: ${data.result.threat_score}/100`);
        console.log(`Classification: ${data.result.classification}`);
        console.log(`Catégories: ${data.result.categories.join(', ')}`);
        
        // Vérifier blacklists
        data.result.reputation.blacklists.forEach(bl => {
            if (bl.listed) {
                console.log(`⚠️  Listée sur ${bl.name}`);
            }
        });
        
    } catch (err) {
        console.error('❌ Erreur API:', err.message);
    }
}

// Utilisation
interrogerThreatIntel('203.0.113.50');
```

### :fontawesome-brands-php: PHP

**Lecture JSON depuis fichier :**

```php
<?php

// Lecture fichier JSON
$json = file_get_contents('config.json');
$donnees = json_decode($json, true); // true = tableau associatif

echo "Nom: " . $donnees['nom'] . "\n";
echo "Âge: " . $donnees['age'] . "\n";

// Accès imbriqué
if (isset($donnees['adresse'])) {
    echo "Ville: " . $donnees['adresse']['ville'] . "\n";
}

// Ou garder comme objet (false par défaut)
$objet = json_decode($json);
echo "Nom: " . $objet->nom . "\n";
?>
```

**Gestion d'erreurs JSON :**

```php
<?php

$json = file_get_contents('config.json');
$donnees = json_decode($json, true);

// Vérifier erreurs
if (json_last_error() !== JSON_ERROR_NONE) {
    echo "❌ Erreur JSON: " . json_last_error_msg() . "\n";
    exit(1);
}

echo "✅ JSON valide\n";
?>
```

**Écriture JSON vers fichier :**

```php
<?php

$utilisateur = [
    'id' => 1234,
    'nom' => 'Dupont',
    'prenom' => 'Alice',
    'roles' => ['admin', 'user'],
    'actif' => true,
    'metadata' => [
        'created_at' => '2025-11-15T10:00:00Z',
        'last_login' => '2025-11-15T15:30:00Z'
    ]
];

// Convertir en JSON avec indentation
$json = json_encode($utilisateur, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);

// Sauvegarder
file_put_contents('utilisateur.json', $json);

echo "✅ Fichier sauvegardé\n";
?>
```

**Options d'encodage :**

```php
<?php

$donnees = ['nom' => 'Alice', 'âge' => 28, 'ville' => 'Paris'];

// Compact
$compact = json_encode($donnees);
// {"nom":"Alice","\u00e2ge":28,"ville":"Paris"}

// Indenté et sans échappement Unicode
$lisible = json_encode($donnees, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
// {
//     "nom": "Alice",
//     "âge": 28,
//     "ville": "Paris"
// }

// Sans échapper les slashes
$url = ['url' => 'https://example.com/path'];
$sans_escape = json_encode($url, JSON_UNESCAPED_SLASHES);
// {"url":"https://example.com/path"}

// Forcer objet même pour tableau vide
$force_objet = json_encode([], JSON_FORCE_OBJECT);
// {}
?>
```

**Analyse de logs firewall :**

```php
<?php

function analyserLogsFirewall($fichierJson) {
    $json = file_get_contents($fichierJson);
    $data = json_decode($json, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        die("❌ Erreur JSON: " . json_last_error_msg() . "\n");
    }
    
    // Compteurs
    $actions = [];
    $ips_bloquees = [];
    $pays = [];
    
    foreach ($data['events'] as $event) {
        // Compter actions
        $action = $event['action'];
        $actions[$action] = ($actions[$action] ?? 0) + 1;
        
        // IPs bloquées
        if ($action === 'BLOCK') {
            $ip = $event['source']['ip'];
            $ips_bloquees[$ip] = ($ips_bloquees[$ip] ?? 0) + 1;
            
            $pays_source = $event['source']['country'];
            $pays[$pays_source] = ($pays[$pays_source] ?? 0) + 1;
        }
    }
    
    // Affichage
    echo "=== Statistiques Firewall ===\n";
    echo "\nTotal événements: " . count($data['events']) . "\n";
    
    echo "\n📊 Actions:\n";
    foreach ($actions as $action => $count) {
        echo "  $action: $count\n";
    }
    
    echo "\n🚨 Top 5 IPs bloquées:\n";
    arsort($ips_bloquees);
    foreach (array_slice($ips_bloquees, 0, 5, true) as $ip => $count) {
        echo "  $ip: $count blocages\n";
    }
    
    echo "\n🌍 Pays sources:\n";
    arsort($pays);
    foreach ($pays as $pays_source => $count) {
        echo "  $pays_source: $count\n";
    }
}

// Utilisation
analyserLogsFirewall('firewall_logs.json');
?>
```

**Filtrage de vulnérabilités :**

```php
<?php

function extraireVulnsCritiques($inputFile, $outputFile) {
    $scan = json_decode(file_get_contents($inputFile), true);
    
    // Filtrer
    $critiques = array_filter($scan['vulnerabilities'], function($vuln) {
        return in_array($vuln['vulnerability']['severity'], ['CRITICAL', 'HIGH']);
    });
    
    // Réindexer tableau (enlever trous)
    $critiques = array_values($critiques);
    
    // Créer rapport
    $rapport = [
        'scan_id' => $scan['scan_id'],
        'timestamp' => $scan['timestamp'],
        'vulnerabilities_critiques' => $critiques,
        'count' => count($critiques)
    ];
    
    // Sauvegarder
    $json = json_encode($rapport, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    file_put_contents($outputFile, $json);
    
    echo "✅ " . count($critiques) . " vulnérabilités critiques extraites\n";
}

// Utilisation
extraireVulnsCritiques('scan.json', 'critiques.json');
?>
```

**Requête API avec cURL :**

```php
<?php

function interrogerThreatIntel($ipAddress) {
    $apiUrl = "https://api.threatintel.example/v1/ip/$ipAddress";
    
    $ch = curl_init($apiUrl);
    
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer YOUR_API_KEY',
            'Content-Type: application/json'
        ]
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    curl_close($ch);
    
    if ($httpCode !== 200) {
        echo "❌ Erreur API: $httpCode\n";
        return;
    }
    
    $data = json_decode($response, true);
    
    echo "🔍 Analyse de $ipAddress\n";
    echo "Score de menace: {$data['result']['threat_score']}/100\n";
    echo "Classification: {$data['result']['classification']}\n";
    echo "Catégories: " . implode(', ', $data['result']['categories']) . "\n";
    
    // Vérifier blacklists
    foreach ($data['result']['reputation']['blacklists'] as $bl) {
        if ($bl['listed']) {
            echo "⚠️  Listée sur {$bl['name']}\n";
        }
    }
}

// Utilisation
interrogerThreatIntel('203.0.113.50');
?>
```

### :fontawesome-brands-golang: Go (Golang)

**Lecture JSON depuis fichier :**

```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
)

type Config struct {
    Nom    string `json:"nom"`
    Age    int    `json:"age"`
    Actif  bool   `json:"actif"`
    Roles  []string `json:"roles"`
}

func main() {
    // Lire fichier
    data, err := os.ReadFile("config.json")
    if err != nil {
        panic(err)
    }
    
    // Parser JSON
    var config Config
    err = json.Unmarshal(data, &config)
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Nom: %s\n", config.Nom)
    fmt.Printf("Âge: %d\n", config.Age)
    fmt.Printf("Actif: %t\n", config.Actif)
}
```

**Structures imbriquées :**

```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
)

type Utilisateur struct {
    ID       int      `json:"id"`
    Nom      string   `json:"nom"`
    Prenom   string   `json:"prenom"`
    Roles    []string `json:"roles"`
    Actif    bool     `json:"actif"`
    Metadata Metadata `json:"metadata"`
}

type Metadata struct {
    CreatedAt  string `json:"created_at"`
    LastLogin  string `json:"last_login"`
}

func main() {
    data, _ := os.ReadFile("utilisateur.json")
    
    var user Utilisateur
    json.Unmarshal(data, &user)
    
    fmt.Printf("%s %s (ID: %d)\n", user.Prenom, user.Nom, user.ID)
    fmt.Printf("Dernière connexion: %s\n", user.Metadata.LastLogin)
}
```

**Écriture JSON vers fichier :**

```go
package main

import (
    "encoding/json"
    "os"
)

type Utilisateur struct {
    ID       int      `json:"id"`
    Nom      string   `json:"nom"`
    Prenom   string   `json:"prenom"`
    Roles    []string `json:"roles"`
    Actif    bool     `json:"actif"`
}

func main() {
    utilisateur := Utilisateur{
        ID:     1234,
        Nom:    "Dupont",
        Prenom: "Alice",
        Roles:  []string{"admin", "user"},
        Actif:  true,
    }
    
    // Convertir en JSON avec indentation
    jsonData, err := json.MarshalIndent(utilisateur, "", "  ")
    if err != nil {
        panic(err)
    }
    
    // Écrire fichier
    err = os.WriteFile("utilisateur.json", jsonData, 0644)
    if err != nil {
        panic(err)
    }
    
    fmt.Println("✅ Fichier sauvegardé")
}
```

**Analyse de logs firewall :**

```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "sort"
)

type FirewallLogs struct {
    Events []Event `json:"events"`
}

type Event struct {
    Timestamp   string      `json:"timestamp"`
    EventID     string      `json:"event_id"`
    Action      string      `json:"action"`
    Source      NetworkInfo `json:"source"`
    Destination NetworkInfo `json:"destination"`
}

type NetworkInfo struct {
    IP      string `json:"ip"`
    Port    int    `json:"port"`
    Country string `json:"country"`
}

func analyserLogsFirewall(fichierJson string) {
    data, _ := os.ReadFile(fichierJson)
    
    var logs FirewallLogs
    json.Unmarshal(data, &logs)
    
    // Compteurs
    actions := make(map[string]int)
    ipsBloqueesCount := make(map[string]int)
    paysCount := make(map[string]int)
    
    for _, event := range logs.Events {
        actions[event.Action]++
        
        if event.Action == "BLOCK" {
            ipsBloqueesCount[event.Source.IP]++
            paysCount[event.Source.Country]++
        }
    }
    
    // Affichage
    fmt.Println("=== Statistiques Firewall ===")
    fmt.Printf("\nTotal événements: %d\n", len(logs.Events))
    
    fmt.Println("\n📊 Actions:")
    for action, count := range actions {
        fmt.Printf("  %s: %d\n", action, count)
    }
    
    fmt.Println("\n🚨 Top 5 IPs bloquées:")
    printTopN(ipsBloqueesCount, 5)
    
    fmt.Println("\n🌍 Pays sources:")
    printTopN(paysCount, 10)
}

func printTopN(m map[string]int, n int) {
    type kv struct {
        Key   string
        Value int
    }
    
    var ss []kv
    for k, v := range m {
        ss = append(ss, kv{k, v})
    }
    
    sort.Slice(ss, func(i, j int) bool {
        return ss[i].Value > ss[j].Value
    })
    
    for i, kv := range ss {
        if i >= n {
            break
        }
        fmt.Printf("  %s: %d\n", kv.Key, kv.Value)
    }
}

func main() {
    analyserLogsFirewall("firewall_logs.json")
}
```

**Filtrage de vulnérabilités :**

```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
)

type ScanResult struct {
    ScanID          string            `json:"scan_id"`
    Timestamp       string            `json:"timestamp"`
    Vulnerabilities []Vulnerability   `json:"vulnerabilities"`
}

type Vulnerability struct {
    Host           string         `json:"host"`
    Port           int            `json:"port"`
    Service        string         `json:"service"`
    VulnDetails    VulnDetails    `json:"vulnerability"`
}

type VulnDetails struct {
    Name          string   `json:"name"`
    Severity      string   `json:"severity"`
    CVSSScore     float64  `json:"cvss_score"`
    CVE           []string `json:"cve"`
}

type Rapport struct {
    ScanID      string          `json:"scan_id"`
    Timestamp   string          `json:"timestamp"`
    Critiques   []Vulnerability `json:"vulnerabilities_critiques"`
    Count       int             `json:"count"`
}

func extraireVulnsCritiques(inputFile, outputFile string) {
    data, _ := os.ReadFile(inputFile)
    
    var scan ScanResult
    json.Unmarshal(data, &scan)
    
    // Filtrer
    var critiques []Vulnerability
    for _, vuln := range scan.Vulnerabilities {
        if vuln.VulnDetails.Severity == "CRITICAL" || vuln.VulnDetails.Severity == "HIGH" {
            critiques = append(critiques, vuln)
        }
    }
    
    // Créer rapport
    rapport := Rapport{
        ScanID:    scan.ScanID,
        Timestamp: scan.Timestamp,
        Critiques: critiques,
        Count:     len(critiques),
    }
    
    // Sauvegarder
    jsonData, _ := json.MarshalIndent(rapport, "", "  ")
    os.WriteFile(outputFile, jsonData, 0644)
    
    fmt.Printf("✅ %d vulnérabilités critiques extraites\n", len(critiques))
}

func main() {
    extraireVulnsCritiques("scan.json", "critiques.json")
}
```

### :fontawesome-brands-rust: Rust

**Lecture JSON avec serde :**

```rust
use serde::{Deserialize, Serialize};
use std::fs;
use std::error::Error;

#[derive(Debug, Deserialize)]
struct Config {
    nom: String,
    age: u32,
    actif: bool,
    roles: Vec<String>,
}

fn main() -> Result<(), Box<dyn Error>> {
    // Lire fichier
    let data = fs::read_to_string("config.json")?;
    
    // Parser JSON
    let config: Config = serde_json::from_str(&data)?;
    
    println!("Nom: {}", config.nom);
    println!("Âge: {}", config.age);
    println!("Actif: {}", config.actif);
    
    Ok(())
}
```

**Structures imbriquées :**

```rust
use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Debug, Deserialize, Serialize)]
struct Utilisateur {
    id: u32,
    nom: String,
    prenom: String,
    roles: Vec<String>,
    actif: bool,
    metadata: Metadata,
}

#[derive(Debug, Deserialize, Serialize)]
struct Metadata {
    created_at: String,
    last_login: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let data = fs::read_to_string("utilisateur.json")?;
    let user: Utilisateur = serde_json::from_str(&data)?;
    
    println!("{} {} (ID: {})", user.prenom, user.nom, user.id);
    println!("Dernière connexion: {}", user.metadata.last_login);
    
    Ok(())
}
```

**Écriture JSON :**

```rust
use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Debug, Deserialize, Serialize)]
struct Utilisateur {
    id: u32,
    nom: String,
    prenom: String,
    roles: Vec<String>,
    actif: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let utilisateur = Utilisateur {
        id: 1234,
        nom: "Dupont".to_string(),
        prenom: "Alice".to_string(),
        roles: vec!["admin".to_string(), "user".to_string()],
        actif: true,
    };
    
    // Convertir en JSON avec indentation
    let json_data = serde_json::to_string_pretty(&utilisateur)?;
    
    // Écrire fichier
    fs::write("utilisateur.json", json_data)?;
    
    println!("✅ Fichier sauvegardé");
    
    Ok(())
}
```

**Analyse de logs firewall :**

```rust
use serde::Deserialize;
use std::collections::HashMap;
use std::fs;

#[derive(Debug, Deserialize)]
struct FirewallLogs {
    events: Vec<Event>,
}

#[derive(Debug, Deserialize)]
struct Event {
    timestamp: String,
    event_id: String,
    action: String,
    source: NetworkInfo,
    destination: NetworkInfo,
}

#[derive(Debug, Deserialize)]
struct NetworkInfo {
    ip: String,
    port: u16,
    country: String,
}

fn analyser_logs_firewall(fichier_json: &str) -> Result<(), Box<dyn std::error::Error>> {
    let data = fs::read_to_string(fichier_json)?;
    let logs: FirewallLogs = serde_json::from_str(&data)?;
    
    // Compteurs
    let mut actions: HashMap<String, u32> = HashMap::new();
    let mut ips_bloquees: HashMap<String, u32> = HashMap::new();
    let mut pays: HashMap<String, u32> = HashMap::new();
    
    for event in &logs.events {
        *actions.entry(event.action.clone()).or_insert(0) += 1;
        
        if event.action == "BLOCK" {
            *ips_bloquees.entry(event.source.ip.clone()).or_insert(0) += 1;
            *pays.entry(event.source.country.clone()).or_insert(0) += 1;
        }
    }
    
    // Affichage
    println!("=== Statistiques Firewall ===");
    println!("\nTotal événements: {}", logs.events.len());
    
    println!("\n📊 Actions:");
    for (action, count) in &actions {
        println!("  {}: {}", action, count);
    }
    
    println!("\n🚨 Top 5 IPs bloquées:");
    print_top_n(&ips_bloquees, 5);
    
    println!("\n🌍 Pays sources:");
    print_top_n(&pays, 10);
    
    Ok(())
}

fn print_top_n(map: &HashMap<String, u32>, n: usize) {
    let mut vec: Vec<_> = map.iter().collect();
    vec.sort_by(|a, b| b.1.cmp(a.1));
    
    for (i, (key, value)) in vec.iter().enumerate() {
        if i >= n {
            break;
        }
        println!("  {}: {}", key, value);
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    analyser_logs_firewall("firewall_logs.json")
}
```

**Filtrage de vulnérabilités avec rayon (parallèle) :**

```rust
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Debug, Deserialize, Serialize, Clone)]
struct ScanResult {
    scan_id: String,
    timestamp: String,
    vulnerabilities: Vec<Vulnerability>,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
struct Vulnerability {
    host: String,
    port: u16,
    service: String,
    vulnerability: VulnDetails,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
struct VulnDetails {
    name: String,
    severity: String,
    cvss_score: f64,
    cve: Vec<String>,
}

#[derive(Debug, Serialize)]
struct Rapport {
    scan_id: String,
    timestamp: String,
    vulnerabilities_critiques: Vec<Vulnerability>,
    count: usize,
}

fn extraire_vulns_critiques(
    input_file: &str,
    output_file: &str
) -> Result<(), Box<dyn std::error::Error>> {
    let data = fs::read_to_string(input_file)?;
    let scan: ScanResult = serde_json::from_str(&data)?;
    
    // Filtrage parallèle avec rayon
    let critiques: Vec<Vulnerability> = scan.vulnerabilities
        .par_iter()
        .filter(|v| v.vulnerability.severity == "CRITICAL" || v.vulnerability.severity == "HIGH")
        .cloned()
        .collect();
    
    // Créer rapport
    let rapport = Rapport {
        scan_id: scan.scan_id,
        timestamp: scan.timestamp,
        count: critiques.len(),
        vulnerabilities_critiques: critiques,
    };
    
    // Sauvegarder
    let json_data = serde_json::to_string_pretty(&rapport)?;
    fs::write(output_file, json_data)?;
    
    println!("✅ {} vulnérabilités critiques extraites", rapport.count);
    
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    extraire_vulns_critiques("scan.json", "critiques.json")
}
```

## Bonnes pratiques

### Validation de schéma

**JSON Schema (exemple) :**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["nom", "prenom", "email"],
  "properties": {
    "nom": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "prenom": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "age": {
      "type": "integer",
      "minimum": 18,
      "maximum": 120
    },
    "roles": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["admin", "user", "moderator"]
      },
      "minItems": 1,
      "uniqueItems": true
    }
  }
}
```

### Gestion des erreurs

!!! warning "Toujours valider le JSON"
    - **Vérifier les erreurs de parsing** avant d'utiliser les données
    - **Valider les types** attendus (ne pas supposer qu'une clé existe)
    - **Gérer les valeurs null** explicitement
    - **Utiliser des valeurs par défaut** pour les champs optionnels

### Sécurité

!!! danger "Risques de sécurité JSON"
    - **Injection JSON** : Valider toutes les entrées utilisateur
    - **Désérialisation dangereuse** : Éviter `eval()` en JavaScript
    - **Exposition de données sensibles** : Ne jamais inclure de secrets
    - **DoS via JSON** : Limiter la taille des payloads acceptés
    - **Type confusion** : Valider les types de données reçues

**Exemple d'injection JSON :**
```javascript
// ❌ DANGEREUX - Ne JAMAIS faire ça
const userInput = '{"admin": true}';
const userData = eval('(' + userInput + ')'); // TRÈS DANGEREUX

// ✅ SÉCURISÉ
const userData = JSON.parse(userInput); // Sûr
```

### Performance

**Streaming JSON pour gros fichiers :**

=== ":fontawesome-brands-python: Python"

    ```python
    # Python avec ijson :
    import ijson

    # Parser JSON sans charger tout en mémoire
    with open('huge_file.json', 'rb') as f:
        parser = ijson.items(f, 'vulnerabilities.item')
        
        for vuln in parser:
            if vuln['vulnerability']['severity'] == 'CRITICAL':
                print(f"CRITICAL: {vuln['host']}")
    ```

=== ":fontawesome-brands-node: Node.js (JavaScript)"

    ```javascript
    // Node.js avec stream-json
    const { parser } = require('stream-json');
    const { streamArray } = require('stream-json/streamers/StreamArray');
    const fs = require('fs');

    const pipeline = fs.createReadStream('huge_file.json')
        .pipe(parser())
        .pipe(streamArray());

    pipeline.on('data', ({ value }) => {
        if (value.vulnerability.severity === 'CRITICAL') {
            console.log(`CRITICAL: ${value.host}`);
        }
    });
    ```

## Le mot de la fin

!!! quote
    **JSON est devenu le langage universel de l'échange de données** sur le web moderne. Sa syntaxe simple cache une puissance réelle pour représenter des structures complexes et hiérarchiques de manière lisible et interopérable.
    
    Chaque langage offre des outils puissants pour manipuler JSON :
    
    - **Python** avec sa simplicité (`json.loads/dumps`) et `pandas` pour l'analyse
    - **JavaScript** où JSON est natif (objet JavaScript littéral)
    - **PHP** avec `json_encode/decode` omniprésent dans les APIs web
    - **Go** avec son système de types stricts via struct tags
    - **Rust** avec `serde` pour sérialisation/désérialisation type-safe
    
    Maîtriser JSON c'est comprendre ses **forces** (hiérarchie, types, lisibilité) et ses **limites** (pas de commentaires, pas de dates natives, verbeux pour gros volumes). Pour les APIs modernes, les configurations, et l'échange de données structurées, JSON reste le standard incontournable.

---

!!! abstract "Métadonnées"
    **Version** : 1.0  
    **Dernière mise à jour** : Novembre 2025  
    **Durée de lecture** : 50-55 minutes  
    **Niveau** : Débutant & Intermédiaire
