---
description: "Maîtriser nslookup pour les requêtes DNS simples et multi-plateformes"
icon: lucide/book-open-check
tags: ["DNS", "OUTILS", "DIAGNOSTIC", "RESEAU", "WINDOWS"]
---

# nslookup

## Introduction

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="0"
  data-time="15-20 minutes">
</div>

!!! quote "Analogie pédagogique"
    _Imaginez **nslookup** comme l'**annuaire téléphonique simple** de votre bureau : vous cherchez un nom, vous obtenez un numéro. Pas de détails techniques complexes, pas d'options avancées, juste l'information essentielle. C'est l'outil DNS **accessible à tous**, particulièrement adapté aux **débutants** et aux environnements **Windows**._

> **nslookup (Name Server Lookup)** est un outil de requête DNS **multi-plateforme** disponible nativement sur **Windows, Linux et macOS**. Contrairement à `dig`, il offre une interface **simplifiée et intuitive**, idéale pour des vérifications DNS rapides sans nécessiter une expertise approfondie.

**nslookup** est particulièrement utile pour :

- Vérifications DNS rapides depuis Windows
- Apprentissage des concepts DNS
- Diagnostics basiques de résolution de noms
- Environnements où `dig` n'est pas disponible
- Utilisateurs débutants en administration système

!!! info "Statut de nslookup"
    Bien que considéré comme **obsolète** dans certains environnements Unix/Linux professionnels (au profit de `dig`), **nslookup reste l'outil standard** sous Windows et demeure largement utilisé pour des tâches simples de diagnostic DNS.

## Disponibilité

**nslookup est préinstallé sur :**

- ✅ **Windows** (toutes versions)
- ✅ **macOS** (natif)
- ✅ **Linux** (package `dnsutils` ou `bind-utils`)

### Installation (si absent)

=== ":fontawesome-brands-linux: Debian/Ubuntu"

    ```bash
    # nslookup fait partie du package dnsutils
    sudo apt update
    sudo apt install dnsutils
    
    # Vérifier l'installation
    nslookup -version
    ```

=== ":fontawesome-brands-linux: RHEL/CentOS/Fedora"

    ```bash
    # nslookup fait partie du package bind-utils
    sudo dnf install bind-utils
    
    # Vérifier l'installation
    nslookup -version
    ```

=== ":fontawesome-brands-apple: macOS"

    ```bash
    # nslookup est préinstallé
    nslookup -version
    ```

=== ":fontawesome-brands-windows: Windows"

    ```powershell
    # nslookup est préinstallé
    # Vérifier la disponibilité
    nslookup
    ```

## Syntaxe de base

```bash
nslookup [options] [nom] [serveur]
```

**Paramètres :**

- `nom` : Nom de domaine ou adresse IP à interroger
- `serveur` : Serveur DNS à utiliser (optionnel)
- `options` : Modificateurs du comportement (optionnel)

## Utilisation basique

### Requête simple

```bash
# Requête DNS standard
nslookup example.com
```

**Sortie :**

```plaintext
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
Name:   example.com
Address: 93.184.216.34
```

**Analyse de la sortie :**

| Section | Signification |
|---------|---------------|
| **Server** | Serveur DNS utilisé pour la requête |
| **Address** | Adresse IP du serveur DNS (port 53) |
| **Non-authoritative answer** | Réponse depuis un cache (pas du serveur autoritaire) |
| **Name** | Nom de domaine interrogé |
| **Address** | Adresse IP résultante |

!!! info "Réponse autoritaire vs non-autoritaire"
    - **Non-authoritative** : Réponse depuis un **cache** (serveur récursif)
    - **Authoritative** : Réponse directe du **serveur autoritaire** du domaine

### Requête vers un serveur DNS spécifique

```bash
# Interroger Google DNS
nslookup example.com 8.8.8.8

# Interroger Cloudflare DNS
nslookup example.com 1.1.1.1

# Interroger Quad9 DNS
nslookup example.com 9.9.9.9
```

**Sortie :**

```plaintext
Server:         8.8.8.8
Address:        8.8.8.8#53

Non-authoritative answer:
Name:   example.com
Address: 93.184.216.34
```

### Résolution inverse (IP → nom)

```bash
# Trouver le nom associé à une IP
nslookup 93.184.216.34
```

**Sortie :**

```plaintext
Server:         192.168.1.1
Address:        192.168.1.1#53

34.216.184.93.in-addr.arpa      name = example.com.
```

## Mode interactif

Le **mode interactif** permet d'effectuer plusieurs requêtes sans relancer la commande.

### Lancer le mode interactif

```bash
# Entrer en mode interactif
nslookup

# ou avec un serveur DNS spécifique
nslookup - 8.8.8.8
```

**Prompt interactif :**

```plaintext
>
```

### Commandes en mode interactif

#### Changer de serveur DNS

```bash
> server 8.8.8.8
Default server: 8.8.8.8
Address: 8.8.8.8#53
```

#### Définir le type d'enregistrement

```bash
# Enregistrements A (IPv4)
> set type=A
> example.com

# Enregistrements AAAA (IPv6)
> set type=AAAA
> example.com

# Enregistrements MX (Mail)
> set type=MX
> example.com

# Enregistrements NS (Name Servers)
> set type=NS
> example.com

# Enregistrements TXT
> set type=TXT
> example.com

# Tous les types
> set type=ANY
> example.com
```

#### Activer le mode debug

```bash
# Activer le mode debug (sortie détaillée)
> set debug
> example.com

# Désactiver le mode debug
> set nodebug
```

**Sortie en mode debug :**

```plaintext
> set debug
> example.com
------------
Got answer:
    HEADER:
        opcode = QUERY, id = 12345, rcode = NOERROR
        header flags: response, want recursion, recursion avail.
        questions = 1, answers = 1, authority records = 0, additional = 0
    QUESTIONS:
        example.com, type = A, class = IN
    ANSWERS:
    ->  example.com
        internet address = 93.184.216.34
        ttl = 86400
------------
```

#### Quitter le mode interactif

```bash
> exit
```

???+ example "Exemple de session interactive"

    ```bash
    $ nslookup
    > server 8.8.8.8
    Default server: 8.8.8.8
    Address: 8.8.8.8#53

    > set type=A
    > example.com
    Server:         8.8.8.8
    Address:        8.8.8.8#53

    Non-authoritative answer:
    Name:   example.com
    Address: 93.184.216.34

    > set type=MX
    > example.com
    Server:         8.8.8.8
    Address:        8.8.8.8#53

    Non-authoritative answer:
    example.com     mail exchanger = 10 mail1.example.com.
    example.com     mail exchanger = 20 mail2.example.com.

    > exit
    ```

## Requêtes par type d'enregistrement

### Enregistrements A (IPv4)

```bash
# Requête simple (type A par défaut)
nslookup example.com

# Requête explicite
nslookup -type=A example.com
```

### Enregistrements AAAA (IPv6)

```bash
nslookup -type=AAAA example.com
```

**Sortie :**

```plaintext
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
example.com     has AAAA address 2606:2800:220:1:248:1893:25c8:1946
```

### Enregistrements MX (Mail)

```bash
nslookup -type=MX example.com
```

**Sortie :**

```plaintext
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
example.com     mail exchanger = 10 mail1.example.com.
example.com     mail exchanger = 20 mail2.example.com.

Authoritative answers can be found from:
```

!!! info "Interprétation des priorités MX"
    Le nombre devant chaque serveur mail indique la **priorité** :
    
    - **10** = Priorité haute (tenté en premier)
    - **20** = Priorité basse (tenté si le premier échoue)
    
    Les emails sont livrés au serveur avec la **priorité la plus basse** d'abord.

### Enregistrements NS (Name Servers)

```bash
nslookup -type=NS example.com
```

**Sortie :**

```plaintext
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
example.com     nameserver = ns1.example.com.
example.com     nameserver = ns2.example.com.
```

### Enregistrements TXT

```bash
nslookup -type=TXT example.com
```

**Sortie :**

```plaintext
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
example.com     text = "v=spf1 include:_spf.google.com ~all"
example.com     text = "google-site-verification=abc123xyz"
```

### Enregistrements SOA (Start of Authority)

```bash
nslookup -type=SOA example.com
```

**Sortie :**

```plaintext
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
example.com
        origin = ns1.example.com
        mail addr = admin.example.com
        serial = 2024011801
        refresh = 7200
        retry = 3600
        expire = 1209600
        minimum = 3600
```

### Enregistrements CNAME (Alias)

```bash
nslookup -type=CNAME www.example.com
```

**Sortie :**

```plaintext
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
www.example.com canonical name = example.com.
```

### Enregistrements PTR (Résolution inverse)

```bash
# Format standard (IP directe)
nslookup 93.184.216.34

# Format explicite
nslookup -type=PTR 34.216.184.93.in-addr.arpa
```

### Tous les enregistrements (ANY)

```bash
nslookup -type=ANY example.com
```

!!! warning "Limitation des requêtes ANY"
    De nombreux serveurs DNS modernes **bloquent ou limitent les requêtes ANY** pour des raisons de sécurité (prévention des attaques DDoS). Préférez des requêtes spécifiques.

## Options en ligne de commande

### Options principales

| Option | Description | Exemple |
|--------|-------------|---------|
| `-type=TYPE` | Spécifie le type d'enregistrement | `nslookup -type=MX example.com` |
| `-debug` | Active le mode debug | `nslookup -debug example.com` |
| `-timeout=N` | Définit le timeout (secondes) | `nslookup -timeout=10 example.com` |
| `-port=N` | Spécifie le port DNS | `nslookup -port=5353 example.com` |
| `-retry=N` | Nombre de tentatives | `nslookup -retry=3 example.com` |

???+ example "Exemples d'utilisation"

    ```bash
    # Requête MX avec timeout de 5 secondes
    nslookup -type=MX -timeout=5 example.com

    # Requête A avec 3 tentatives max
    nslookup -type=A -retry=3 example.com

    # Requête debug vers Google DNS
    nslookup -debug example.com 8.8.8.8
    ```

## Cas d'usage pratiques

### Vérifier la résolution d'un domaine

```bash
# Tester la résolution basique
nslookup example.com

# Tester depuis plusieurs serveurs DNS
nslookup example.com 8.8.8.8
nslookup example.com 1.1.1.1
nslookup example.com 9.9.9.9
```

### Diagnostiquer les problèmes d'email

```bash
# Étape 1 : Vérifier les enregistrements MX
nslookup -type=MX example.com

# Sortie
example.com     mail exchanger = 10 mail.example.com.

# Étape 2 : Vérifier la résolution du serveur mail
nslookup mail.example.com

# Étape 3 : Vérifier les enregistrements SPF
nslookup -type=TXT example.com | grep spf
```

### Identifier un serveur web derrière un CDN

```bash
# Vérifier les redirections CNAME
nslookup -type=CNAME www.example.com

# CDN courants :
# - Cloudflare : .cloudflare.com
# - AWS CloudFront : .cloudfront.net
# - Akamai : .akamaiedge.net
# - Fastly : .fastly.net
```

### Vérifier la propagation DNS

```bash
# Script de vérification multi-serveurs
@echo off
echo Verification de propagation DNS pour example.com
echo ================================================

echo Google DNS (8.8.8.8):
nslookup example.com 8.8.8.8 | findstr "Address"

echo.
echo Cloudflare DNS (1.1.1.1):
nslookup example.com 1.1.1.1 | findstr "Address"

echo.
echo Quad9 DNS (9.9.9.9):
nslookup example.com 9.9.9.9 | findstr "Address"
```

### Tester les serveurs DNS locaux

```bash
# Windows
nslookup example.com

# Identifier le serveur DNS utilisé dans la sortie
# Server: 192.168.1.1  ← Serveur DNS de votre routeur/ISP
```

## Résolution de problèmes

### Problème 1 : "Server failed" ou "connection timed out"

**Symptôme :**

```plaintext
DNS request timed out.
    timeout was 2 seconds.
*** Can't find example.com: No response from server
```

**Causes possibles :**

- Serveur DNS injoignable
- Pare-feu bloquant le port 53
- Problème de connectivité réseau
- Serveur DNS surchargé

**Solutions :**

```bash
# Tester avec un serveur DNS public
nslookup example.com 8.8.8.8

# Vérifier la connectivité au serveur DNS
ping 8.8.8.8

# Augmenter le timeout
nslookup -timeout=10 example.com

# Windows : Vérifier les paramètres DNS
ipconfig /all | findstr "DNS Servers"
```

### Problème 2 : "Non-existent domain" (NXDOMAIN)

**Symptôme :**

```plaintext
Server:         8.8.8.8
Address:        8.8.8.8#53

** server can't find example.com: NXDOMAIN
```

**Causes possibles :**

- Domaine inexistant ou expiré
- Erreur de saisie (typo)
- Propagation DNS non terminée

**Solutions :**

```bash
# Vérifier l'orthographe du domaine
nslookup examplee.com  # Typo volontaire

# Tester avec plusieurs serveurs DNS
nslookup example.com 8.8.8.8
nslookup example.com 1.1.1.1

# Vérifier si le domaine existe (whois)
whois example.com
```

### Problème 3 : Réponses incohérentes

**Symptôme :** Différentes IPs selon le serveur DNS interrogé.

**Solutions :**

```bash
# Comparer plusieurs serveurs DNS
nslookup example.com 8.8.8.8
nslookup example.com 1.1.1.1
nslookup example.com

# Vider le cache DNS local
# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches

# macOS
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

### Problème 4 : Résolution lente

**Diagnostic :**

```bash
# Mesurer le temps de résolution (Windows PowerShell)
Measure-Command { nslookup example.com }

# Tester avec différents serveurs
Measure-Command { nslookup example.com 8.8.8.8 }
Measure-Command { nslookup example.com 1.1.1.1 }
```

**Solutions :**

- Changer de serveur DNS (1.1.1.1 ou 8.8.8.8)
- Vérifier la latence réseau
- Contacter l'ISP

## Scripts Windows

### Script batch de diagnostic DNS

```batch
@echo off
REM dns_diag.bat - Diagnostic DNS complet

set DOMAIN=%1

if "%DOMAIN%"=="" (
    echo Usage: dns_diag.bat ^<domaine^>
    exit /b 1
)

echo ========================================
echo   DIAGNOSTIC DNS POUR %DOMAIN%
echo ========================================
echo.

echo [1] Enregistrements A (IPv4)
nslookup -type=A %DOMAIN%
echo.

echo [2] Enregistrements AAAA (IPv6)
nslookup -type=AAAA %DOMAIN%
echo.

echo [3] Enregistrements MX (Mail)
nslookup -type=MX %DOMAIN%
echo.

echo [4] Enregistrements NS (Name Servers)
nslookup -type=NS %DOMAIN%
echo.

echo [5] Enregistrements TXT (SPF, DKIM, etc.)
nslookup -type=TXT %DOMAIN%
echo.

echo [6] Enregistrement SOA (Autorite)
nslookup -type=SOA %DOMAIN%
echo.

echo ========================================
echo        FIN DU DIAGNOSTIC
echo ========================================
```

### Script PowerShell de monitoring DNS

```powershell
# dns_monitor.ps1 - Surveillance DNS continue

param(
    [string]$Domain = "example.com",
    [int]$Interval = 300  # 5 minutes
)

Write-Host "Monitoring DNS pour $Domain" -ForegroundColor Green
Write-Host "Intervalle : $Interval secondes" -ForegroundColor Yellow
Write-Host ""

$previousIP = (nslookup $Domain | Select-String "Address:" | Select-Object -Last 1).ToString().Split(":")[-1].Trim()
Write-Host "IP initiale : $previousIP"

while ($true) {
    Start-Sleep -Seconds $Interval
    
    $currentIP = (nslookup $Domain | Select-String "Address:" | Select-Object -Last 1).ToString().Split(":")[-1].Trim()
    
    if ($currentIP -ne $previousIP) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] ALERTE : Changement d'IP detecte !" -ForegroundColor Red
        Write-Host "  Ancienne IP : $previousIP" -ForegroundColor Yellow
        Write-Host "  Nouvelle IP : $currentIP" -ForegroundColor Green
        
        # Envoyer une notification email (à configurer)
        # Send-MailMessage -To "admin@example.com" -Subject "Alerte DNS" -Body "Changement IP pour $Domain"
        
        $previousIP = $currentIP
    } else {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] OK : IP stable ($currentIP)" -ForegroundColor Gray
    }
}
```

### Script de vérification de propagation

```batch
@echo off
REM check_propagation.bat - Verifie la propagation DNS

set DOMAIN=%1

if "%DOMAIN%"=="" (
    echo Usage: check_propagation.bat ^<domaine^>
    exit /b 1
)

echo Verification de propagation DNS pour %DOMAIN%
echo =============================================
echo.

echo Google DNS (8.8.8.8):
nslookup %DOMAIN% 8.8.8.8 | findstr "Address:" | findstr /V "8.8.8.8"
echo.

echo Cloudflare DNS (1.1.1.1):
nslookup %DOMAIN% 1.1.1.1 | findstr "Address:" | findstr /V "1.1.1.1"
echo.

echo Quad9 DNS (9.9.9.9):
nslookup %DOMAIN% 9.9.9.9 | findstr "Address:" | findstr /V "9.9.9.9"
echo.

echo OpenDNS (208.67.222.222):
nslookup %DOMAIN% 208.67.222.222 | findstr "Address:" | findstr /V "208.67.222.222"
echo.
```

## Configuration DNS sous Windows

### Afficher la configuration DNS actuelle

```powershell
# Afficher tous les paramètres réseau
ipconfig /all

# Afficher uniquement les serveurs DNS
ipconfig /all | findstr "DNS Servers"
```

### Modifier les serveurs DNS

=== "Interface graphique"

    1. **Panneau de configuration** → Réseau et Internet
    2. **Centre Réseau et partage** → Modifier les paramètres de la carte
    3. Clic droit sur la connexion → **Propriétés**
    4. Sélectionner **IPv4** → **Propriétés**
    5. **Utiliser les adresses de serveur DNS suivantes :**
       - Serveur DNS préféré : `1.1.1.1`
       - Serveur DNS auxiliaire : `8.8.8.8`

=== "PowerShell (Administrateur)"

    ```powershell
    # Lister les interfaces réseau
    Get-NetAdapter
    
    # Définir les serveurs DNS pour une interface
    Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses ("1.1.1.1","8.8.8.8")
    
    # Vérifier la configuration
    Get-DnsClientServerAddress
    
    # Vider le cache DNS
    Clear-DnsClientCache
    
    # Afficher le cache DNS
    Get-DnsClientCache
    ```

=== "Ligne de commande (cmd)"

    ```batch
    REM Définir les serveurs DNS
    netsh interface ip set dns "Ethernet" static 1.1.1.1 primary
    netsh interface ip add dns "Ethernet" 8.8.8.8 index=2
    
    REM Vérifier
    netsh interface ip show dns
    
    REM Vider le cache DNS
    ipconfig /flushdns
    
    REM Afficher le cache DNS
    ipconfig /displaydns
    ```

### Vider le cache DNS

```batch
# Vider le cache DNS
ipconfig /flushdns

# Sortie
Configuration IP de Windows
Le cache de résolution DNS a été vidé.
```

### Afficher le cache DNS

```batch
# Afficher tout le cache
ipconfig /displaydns

# Filtrer pour un domaine spécifique
ipconfig /displaydns | findstr example.com
```

## Différences avec dig et host

### Comparaison des outils DNS

| Critère | nslookup | dig | host |
|---------|----------|-----|------|
| **Disponibilité** | Windows/Linux/macOS | Principalement Linux | Linux/macOS |
| **Sortie** | Lisible pour humains | Technique détaillée | Concise |
| **Options** | Limitées | Très nombreuses | Basiques |
| **Mode interactif** | ✅ Oui | ❌ Non | ❌ Non |
| **Traçage résolution** | ❌ Non | ✅ `+trace` | ❌ Non |
| **DNSSEC** | ❌ Non | ✅ `+dnssec` | ❌ Non |
| **Parsing (scripts)** | Difficile | Facile | Moyen |
| **Maintenance** | Active mais limitée | Active (ISC) | Active |
| **Usage recommandé** | Windows, débutants | Linux, pros | Vérifications rapides |

### Quand utiliser nslookup

**Situations favorables :**

- ✅ Environnement **Windows** (natif)
- ✅ Utilisateurs **débutants**
- ✅ Vérifications DNS **simples et rapides**
- ✅ **Mode interactif** pour explorer plusieurs enregistrements
- ✅ Scripts batch Windows basiques

**Situations défavorables :**

- ❌ Diagnostic DNS **approfondi** → Utiliser `dig`
- ❌ Validation **DNSSEC** → Utiliser `dig +dnssec`
- ❌ Traçage de résolution → Utiliser `dig +trace`
- ❌ Scripts nécessitant un **parsing précis** → Utiliser `dig +short`

### Équivalences de commandes

| Tâche | nslookup | dig | host |
|-------|----------|-----|------|
| **Requête A** | `nslookup example.com` | `dig example.com` | `host example.com` |
| **Requête MX** | `nslookup -type=MX example.com` | `dig MX example.com` | `host -t MX example.com` |
| **Serveur spécifique** | `nslookup example.com 8.8.8.8` | `dig @8.8.8.8 example.com` | `host example.com 8.8.8.8` |
| **Résolution inverse** | `nslookup 1.2.3.4` | `dig -x 1.2.3.4` | `host 1.2.3.4` |
| **Réponse courte** | Mode interactif | `dig +short example.com` | `host example.com` |

## Limitations de nslookup

### Limitations techniques

!!! warning "Limites de nslookup"
    
    **Fonctionnalités absentes :**
    
    - ❌ **Pas de traçage de résolution** (équivalent `dig +trace`)
    - ❌ **Pas de support DNSSEC** natif
    - ❌ **Options avancées limitées** (TTL, statistiques, etc.)
    - ❌ **Sortie difficile à parser** pour les scripts avancés
    - ❌ **Pas de contrôle fin** sur les requêtes DNS
    
    **Considérations :**
    
    - Considéré comme **obsolète** dans certains environnements Unix professionnels
    - **Ne remplace pas `dig`** pour le diagnostic avancé
    - Sortie **non standardisée** entre les différentes implémentations

### Alternatives recommandées

**Pour Linux/Unix :**

```bash
# Préférer dig pour le diagnostic
dig example.com

# Ou host pour les vérifications rapides
host example.com
```

**Pour Windows :**

```powershell
# nslookup reste l'outil standard
nslookup example.com

# Alternative : Resolve-DnsName (PowerShell natif)
Resolve-DnsName example.com
```

## Bonnes pratiques

!!! tip "Utilisation efficace de nslookup"
    
    **Diagnostic basique :**
    
    - ✅ Utiliser nslookup pour des **vérifications DNS rapides**
    - ✅ Tester avec **plusieurs serveurs DNS** (8.8.8.8, 1.1.1.1, 9.9.9.9)
    - ✅ Utiliser le **mode interactif** pour explorer différents types d'enregistrements
    - ✅ Toujours vérifier le serveur DNS utilisé dans la sortie
    
    **Environnement Windows :**
    
    - ✅ nslookup est l'outil **natif et standard** sous Windows
    - ✅ Combiner avec `ipconfig /flushdns` pour vider le cache
    - ✅ Utiliser **PowerShell** pour des scripts plus avancés
    
    **Limites à connaître :**
    
    - ⚠️ Pour du diagnostic avancé, **migrer vers dig** (WSL sous Windows)
    - ⚠️ Ne pas se fier uniquement à nslookup pour des **audits DNS professionnels**
    - ⚠️ Vérifier la **propagation DNS** avec des outils en ligne pour une vue mondiale

## Pour aller plus loin

!!! info "Ressources complémentaires"
    
    **Outils alternatifs :**
    
    - **dig** : Outil DNS avancé pour diagnostic approfondi
    - **host** : Outil DNS simple et rapide
    - **Resolve-DnsName** : Cmdlet PowerShell natif (Windows)
    - **dog** : Alternative moderne à dig (écrit en Rust)
    
    **Services en ligne :**
    
    - [MXToolbox](https://mxtoolbox.com/) - Diagnostic DNS complet
    - [What's My DNS](https://www.whatsmydns.net/) - Vérification propagation mondiale
    - [DNSdumpster](https://dnsdumpster.com/) - Exploration DNS
    - [IntoDNS](https://intodns.com/) - Audit de configuration DNS
    
    **Documentation :**
    
    - [Microsoft Docs - nslookup](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/nslookup) - Documentation officielle
    - [RFC 1034/1035](https://tools.ietf.org/html/rfc1034) - Standards DNS

---