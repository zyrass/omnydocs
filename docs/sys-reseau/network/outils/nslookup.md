---
description: "nslookup : résolution DNS, troubleshooting réseau, reconnaissance, enumeration domaines"
icon: lucide/book-open-check
tags: ["NSLOOKUP", "DNS", "NETWORK", "TROUBLESHOOTING", "RECONNAISSANCE", "ENUMERATION"]
---

# nslookup

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-time="3-4 heures"
  data-version="1.0">
</div>

## Introduction à la Résolution DNS et Enumeration

!!! quote "Analogie pédagogique"
    _Imaginez l'**annuaire téléphonique mondial automatisé** : vous connaissez le nom d'une personne (domaine), vous cherchez son numéro de téléphone (adresse IP). nslookup fonctionne comme **assistant recherche intelligent consultant annuaire DNS distribué mondial** pour traduire noms humains (google.com) en adresses machines (142.250.185.78). **Annuaire téléphonique DNS mondial** : annuaire hiérarchique distribué (root servers → TLD → authoritative), recherche instantanée nom→numéro (google.com → IP), informations détaillées contact (MX mail servers, TXT SPF records), vérification validité numéro (domain exists?), historique modifications (TTL cache), multi-annuaires redondants (multiple DNS servers), protection fraude (DNSSEC validation). **Sans nslookup/DNS** : devoir mémoriser toutes IPs (142.250.185.78 au lieu google.com impossible humainement), sites web inaccessibles si IP change, email impossible (pas résolution MX servers), certificats SSL invalides (domain validation échoue), CDN inefficaces (pas geo-routing DNS), load balancing impossible (pas round-robin DNS). **Avec nslookup** : **Résolution noms** (google.com → 142.250.185.78 instantané), **Troubleshooting réseau** (site inaccessible = DNS problem?), **Enumeration domaines** (découvrir subdomains/mail servers), **Validation configurations** (MX records corrects? SPF setup?), **Reconnaissance pentest** (cartographier infrastructure réseau), **Forensique** (tracer attaques via DNS logs), **Monitoring** (détecter DNS hijacking/poisoning). **DNS = colonne vertébrale Internet** : 4.66 milliards noms domaines enregistrés (2024), résolution DNS = première étape TOUTE connexion Internet, 99.9% utilisateurs ignorent existence mais utilisent billions fois/jour, attaques DNS = paralysie infrastructure complète (DDoS Dyn 2016 paralyse Twitter/Netflix/Spotify). **Architecture DNS hiérarchique** : Root servers 13 mondiaux (a-m.root-servers.net), TLD servers (.com, .org, .fr), Authoritative servers (DNS hébergeur domaine), Recursive resolvers (ISP/Google 8.8.8.8/Cloudflare 1.1.1.1), Cache local (OS/browser TTL). **nslookup = outil diagnostic essentiel** : présent TOUS systèmes (Windows/Linux/macOS native), syntaxe simple accessible débutants, modes interactif/non-interactif, debugging DNS step-by-step, alternative dig (Linux)/Resolve-DnsName (PowerShell)._

**nslookup en résumé :**

- ✅ **Résolution DNS** = Nom de domaine → Adresse IP (et inverse)
- ✅ **Multi-plateformes** = Windows, Linux, macOS (natif partout)
- ✅ **Types enregistrements** = A, AAAA, MX, TXT, CNAME, NS, SOA, PTR
- ✅ **Modes** = Interactif (session) et non-interactif (one-shot)
- ✅ **Troubleshooting** = Diagnostiquer problèmes résolution DNS
- ✅ **Reconnaissance** = Enumeration subdomains, mail servers, nameservers
- ✅ **Simple** = Syntaxe accessible, pas de privilèges requis
- ✅ **Debugging** = Voir requêtes DNS complètes (autoritatives, cache)

**Guide structure :**

1. Introduction et concepts DNS
2. Syntaxe et modes nslookup
3. Types d'enregistrements DNS
4. Résolution basique et inverse
5. Mode interactif avancé
6. Troubleshooting DNS
7. Enumeration et reconnaissance
8. DNS security testing
9. Comparaison dig/host/drill
10. Scripting et automation
11. Best practices
12. Cas pratiques (admin/pentest/forensique)

---

## Section 1 : Introduction et Concepts DNS

### 1.1 Qu'est-ce que le DNS ?

**DNS = Domain Name System (Système de Noms de Domaine)**

```
DNS traduit noms humains → adresses IP machines

Exemple :
google.com → 142.250.185.78 (IPv4)
google.com → 2a00:1450:4007:80f::200e (IPv6)

Sans DNS :
http://142.250.185.78 (difficile mémoriser, change souvent)

Avec DNS :
http://google.com (facile, stable)
```

**Architecture DNS hiérarchique :**

```
                    . (Root)
                    |
        ┌───────────┼───────────┐
        |           |           |
       .com        .org        .fr
        |           |           |
    google.com  wikipedia.org  ovh.fr
        |
    ┌───┴───┐
   www   mail
```

**Processus résolution DNS complet :**

```
1. User tape : www.google.com dans navigateur

2. Cache local (OS/browser)
   ├─ Si trouvé → Retourne IP (instant)
   └─ Si pas trouvé → Continue

3. Recursive Resolver (ISP/8.8.8.8)
   ├─ Cache resolver
   └─ Sinon → Interroge autoritatifs

4. Root Server (.)
   └─ Retourne : "Demandez aux serveurs .com"

5. TLD Server (.com)
   └─ Retourne : "Demandez aux serveurs google.com"

6. Authoritative Server (google.com)
   └─ Retourne : 142.250.185.78

7. Recursive Resolver
   ├─ Cache résultat (TTL)
   └─ Retourne IP au client

8. Navigateur
   └─ Connecte HTTP vers 142.250.185.78

Temps total : 20-200ms (première fois)
             : <1ms (si cache)
```

### 1.2 Types d'enregistrements DNS

```
A        : IPv4 address (google.com → 142.250.185.78)
AAAA     : IPv6 address (google.com → 2a00:1450:...)
CNAME    : Alias (www.example.com → example.com)
MX       : Mail server (example.com → mail.example.com)
TXT      : Text record (SPF, DKIM, verification)
NS       : Nameserver (example.com → ns1.provider.com)
SOA      : Start of Authority (zone info, serial)
PTR      : Reverse DNS (IP → nom de domaine)
SRV      : Service locator (LDAP, SIP, etc.)
CAA      : Certification Authority Authorization

Exemples :

A record :
google.com.  300  IN  A  142.250.185.78

MX record :
gmail.com.  3600  IN  MX  5 gmail-smtp-in.l.google.com.

TXT record (SPF) :
example.com.  IN  TXT  "v=spf1 ip4:192.0.2.0/24 -all"

CNAME :
www.example.com.  IN  CNAME  example.com.
```

### 1.3 Serveurs DNS (Resolvers)

```
DNS Resolvers publics :

Google Public DNS :
8.8.8.8
8.8.4.4

Cloudflare DNS :
1.1.1.1
1.0.0.1

Quad9 (security-focused) :
9.9.9.9

OpenDNS :
208.67.222.222
208.67.220.220

DNS Fournisseur Internet :
Automatique DHCP (souvent lent/filtré)

DNS local :
127.0.0.1 (si serveur DNS local installé)
```

### 1.4 Qu'est-ce que nslookup ?

**nslookup = Name Server Lookup (Interrogation Serveur DNS)**

```
Fonction principale :
Interroger serveurs DNS pour résoudre noms domaines

Présent nativement :
✅ Windows (toutes versions)
✅ Linux (package dnsutils/bind-utils)
✅ macOS (natif)

Alternative modernes :
- dig (Linux, plus puissant)
- host (Linux, simple)
- Resolve-DnsName (PowerShell)

Usage typique :
nslookup google.com

Modes :
1. Non-interactif : une commande = une réponse
2. Interactif : session continue (multiple requêtes)
```

---

## Section 2 : Syntaxe et Modes nslookup

### 2.1 Syntaxe Basique

```bash
# Syntaxe générale
nslookup [option] [nom-domaine] [serveur-dns]

# Résolution simple
nslookup google.com

# Output :
Server:  8.8.8.8
Address:  8.8.8.8#53

Non-authoritative answer:
Name:    google.com
Address: 142.250.185.78

# Spécifier serveur DNS
nslookup google.com 1.1.1.1

# Query type spécifique
nslookup -type=MX gmail.com

# Query class (rare)
nslookup -class=IN google.com

# Timeout
nslookup -timeout=5 example.com

# Retry
nslookup -retry=3 example.com
```

### 2.2 Mode Non-Interactif

```bash
# Une commande = une réponse

# Résolution A record
nslookup google.com

# Résolution MX
nslookup -type=MX gmail.com

# Résolution TXT
nslookup -type=TXT example.com

# Résolution NS (nameservers)
nslookup -type=NS google.com

# Résolution SOA
nslookup -type=SOA google.com

# Résolution ANY (tous types)
nslookup -type=ANY google.com

# Reverse DNS (IP → nom)
nslookup 8.8.8.8

# Multiple commandes script
nslookup google.com > result.txt
nslookup -type=MX gmail.com >> result.txt
```

### 2.3 Mode Interactif

```bash
# Entrer mode interactif
nslookup

# Prompt :
>

# Commandes mode interactif :

# Résolution
> google.com
Server:  8.8.8.8
Address:  8.8.8.8#53

Non-authoritative answer:
Name:    google.com
Address: 142.250.185.78

# Changer type query
> set type=MX
> gmail.com

# Changer serveur DNS
> server 1.1.1.1
Default server: 1.1.1.1
Address: 1.1.1.1#53

> google.com

# Voir configuration actuelle
> set all

# Options utiles :
> set debug          # Mode debug (verbose)
> set nodebug        # Désactiver debug
> set d2             # Super debug (très verbose)
> set timeout=10     # Timeout 10 secondes
> set retry=3        # 3 tentatives
> set recurse        # Récursion activée (default)
> set norecurse      # Récursion désactivée
> set vc             # Virtual Circuit (TCP au lieu UDP)

# Quitter
> exit
```

### 2.4 Options Avancées

```bash
# Debug mode (voir requêtes complètes)
nslookup -debug google.com

# Output :
# Montre :
# - Requête envoyée
# - Serveur contacté
# - Réponse reçue
# - TTL, flags, etc.

# Super debug
nslookup -d2 google.com

# Port custom (pas 53)
nslookup -port=5353 example.com

# Forcer TCP (au lieu UDP)
nslookup -vc google.com

# Désactiver récursion (query directe authoritative)
nslookup -norecurse google.com 8.8.8.8

# Query class
# IN = Internet (99.9% des cas)
# CH = Chaos (rarement utilisé)
nslookup -class=IN google.com
```

---

## Section 3 : Types d'Enregistrements DNS

### 3.1 A Record (IPv4)

```bash
# A = Address (IPv4)

# Query A record
nslookup google.com

# Output :
Name:    google.com
Address: 142.250.185.78

# Explicit type A
nslookup -type=A google.com

# Multiple A records (load balancing)
nslookup facebook.com

# Output :
Name:    facebook.com
Addresses:  157.240.241.35
            157.240.229.35
            157.240.28.35

# Wildcard subdomains
nslookup random123.google.com
# Retourne IP si wildcard configuré
```

### 3.2 AAAA Record (IPv6)

```bash
# AAAA = IPv6 address (quad-A)

# Query IPv6
nslookup -type=AAAA google.com

# Output :
google.com has AAAA address 2a00:1450:4007:80f::200e

# Dual-stack (IPv4 + IPv6)
nslookup -type=ANY google.com
# Retourne A + AAAA

# Vérifier support IPv6
nslookup -type=AAAA example.com
# Si "Non-existent domain" → Pas d'IPv6
```

### 3.3 MX Record (Mail Server)

```bash
# MX = Mail Exchange (serveurs email)

# Query MX records
nslookup -type=MX gmail.com

# Output :
gmail.com       mail exchanger = 5 gmail-smtp-in.l.google.com.
gmail.com       mail exchanger = 10 alt1.gmail-smtp-in.l.google.com.
gmail.com       mail exchanger = 20 alt2.gmail-smtp-in.l.google.com.

# Priorité MX :
# 5  = Priorité haute (primary)
# 10 = Priorité moyenne (backup)
# 20 = Priorité basse (fallback)
# Plus petit nombre = priorité plus haute

# Vérifier config email domaine
nslookup -type=MX example.com

# Troubleshooting email delivery
nslookup -type=MX microsoft.com
# Si pas de MX → Email ne peut pas être reçu

# Resolver MX vers IP
nslookup gmail-smtp-in.l.google.com
```

### 3.4 TXT Record (Text)

```bash
# TXT = Text record (validation, SPF, DKIM, etc.)

# Query TXT
nslookup -type=TXT example.com

# Output exemples :

# SPF (Sender Policy Framework - anti-spam)
"v=spf1 include:_spf.google.com ~all"

# DKIM (DomainKeys Identified Mail)
"v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA..."

# Domain verification (Google, Microsoft)
"google-site-verification=abc123..."
"MS=ms123456"

# DMARC
_dmarc.example.com TXT "v=DMARC1; p=reject; rua=mailto:..."

# Site verification
nslookup -type=TXT google.com

# Custom TXT records
nslookup -type=TXT _github-challenge.example.com
```

### 3.5 CNAME Record (Alias)

```bash
# CNAME = Canonical Name (alias)

# Query CNAME
nslookup www.github.com

# Output :
www.github.com  canonical name = github.com.
Name:   github.com
Address: 140.82.121.4

# CNAME chain
nslookup www.example.com

# Output possible :
www.example.com → cdn.example.com → cdn-provider.com → 192.0.2.1

# Restrictions CNAME :
# ❌ Pas de CNAME sur apex domain (example.com)
# ❌ Pas de CNAME + autres records (MX, TXT)
# ✅ CNAME seulement sur subdomain (www, blog, shop)

# Troubleshooting CNAME loops
nslookup -debug loop.example.com
# Détecte : a.example.com → b.example.com → a.example.com
```

### 3.6 NS Record (Nameserver)

```bash
# NS = Name Server (serveurs DNS autoritatifs)

# Query NS records
nslookup -type=NS google.com

# Output :
google.com      nameserver = ns1.google.com.
google.com      nameserver = ns2.google.com.
google.com      nameserver = ns3.google.com.
google.com      nameserver = ns4.google.com.

# Vérifier délégation DNS
nslookup -type=NS example.com

# Comparer NS authoritative vs resolver cache
nslookup -type=NS example.com
nslookup -type=NS example.com ns1.example.com

# Troubleshooting propagation DNS
# Si NS différents entre resolvers = propagation en cours
```

### 3.7 SOA Record (Start of Authority)

```bash
# SOA = Start of Authority (metadata zone DNS)

# Query SOA
nslookup -type=SOA google.com

# Output :
google.com
        origin = ns1.google.com
        mail addr = dns-admin.google.com
        serial = 583338932
        refresh = 900
        retry = 900
        expire = 1800
        minimum = 60

# Champs SOA :
# origin   : Primary nameserver
# mail     : Email admin (@ remplacé par .)
# serial   : Version zone (format: YYYYMMDDnn)
# refresh  : Secondaires check updates (secondes)
# retry    : Retry si refresh échoue
# expire   : Abandon si primaire inaccessible
# minimum  : TTL minimum records

# Vérifier serial number (propagation)
nslookup -type=SOA example.com ns1.provider.com
nslookup -type=SOA example.com ns2.provider.com
# Si serial différent → Pas synchronisés
```

### 3.8 PTR Record (Reverse DNS)

```bash
# PTR = Pointer (résolution inverse IP → nom)

# Reverse lookup
nslookup 8.8.8.8

# Output :
8.8.8.8.in-addr.arpa    name = dns.google.

# Format PTR :
# 8.8.8.8 → 8.8.8.8.in-addr.arpa
# IPv6 → format .ip6.arpa

# Vérifier reverse DNS (important mail servers)
nslookup 142.250.185.78

# Si pas de PTR :
# ** server can't find 78.185.250.142.in-addr.arpa: NXDOMAIN

# Troubleshooting email rejection
# Mail servers vérifient PTR (anti-spam)
nslookup mail.example.com  # Forward
nslookup <IP-result>       # Reverse
# Si forward ≠ reverse → Email peut être rejeté
```

---

## Section 4 : Résolution Basique et Inverse

### 4.1 Résolution Forward (Nom → IP)

```bash
# Résolution standard
nslookup google.com

# Output :
Server:  8.8.8.8
Address:  8.8.8.8#53

Non-authoritative answer:
Name:    google.com
Address: 142.250.185.78

# Interpréter output :
# Server       : DNS resolver utilisé (8.8.8.8 = Google)
# Address      : IP:port resolver (53 = port DNS)
# Non-authoritative : Réponse depuis cache (pas authoritative)
# Name         : Domaine résolu
# Address      : IP résultat

# Authoritative answer
nslookup google.com ns1.google.com

# Output :
Server:  ns1.google.com
Address:  216.239.32.10#53

Name:    google.com
Address: 142.250.185.78
# Pas de "Non-authoritative" → Réponse directe serveur autoritatif

# Multiple IPs (load balancing)
nslookup www.google.com

# Output :
Name:    www.google.com
Addresses:  142.250.185.68
            142.250.185.99
            142.250.185.105
# Résultats peuvent varier (round-robin DNS)
```

### 4.2 Résolution Inverse (IP → Nom)

```bash
# Reverse DNS lookup
nslookup 8.8.8.8

# Output :
Server:  8.8.8.8
Address:  8.8.8.8#53

8.8.8.8.in-addr.arpa    name = dns.google.

# Format PTR automatique :
# nslookup convertit 8.8.8.8 → 8.8.8.8.in-addr.arpa

# Explicit PTR query
nslookup -type=PTR 8.8.8.8.in-addr.arpa

# Reverse lookup IPv6
nslookup 2001:4860:4860::8888

# Si pas de PTR configuré :
** server can't find 8.8.8.8.in-addr.arpa: NXDOMAIN

# Vérifier cohérence forward/reverse
# 1. Forward
nslookup mail.example.com
# Result: 192.0.2.10

# 2. Reverse
nslookup 192.0.2.10
# Expected: mail.example.com

# Si différent → Problème configuration
```

### 4.3 Troubleshooting Résolution

```bash
# Site inaccessible - DNS problem?

# Test 1 : Résolution basique
nslookup example.com

# Si "NXDOMAIN" → Domaine n'existe pas
# Si timeout → Problème réseau/DNS server
# Si pas de réponse → Firewall bloque port 53

# Test 2 : Changer resolver
nslookup example.com 1.1.1.1

# Si fonctionne avec 1.1.1.1 mais pas DNS par défaut
# → Problème resolver local/ISP

# Test 3 : Vérifier authoritative
nslookup -type=NS example.com
# Obtenir nameserver
nslookup example.com ns1.example.com
# Query directe authoritative

# Test 4 : Cache DNS local
# Windows :
ipconfig /flushdns

# Linux :
sudo systemd-resolve --flush-caches
# ou
sudo service nscd restart

# macOS :
sudo dscacheutil -flushcache

# Re-test après flush
nslookup example.com

# Test 5 : Propagation DNS (nouveau domaine)
nslookup example.com 8.8.8.8
nslookup example.com 1.1.1.1
# Si résultats différents → Propagation en cours (24-48h)
```

---

## Section 5 : Mode Interactif Avancé

### 5.1 Session Interactive Complète

```bash
# Entrer mode interactif
nslookup

# Session exemple :
> set debug          # Activer debug
> set type=A         # Type A records
> google.com
# [résultat détaillé avec debug]

> set type=MX        # Changer type MX
> gmail.com
# [MX records]

> server 1.1.1.1     # Changer resolver
> google.com
# [requête via Cloudflare DNS]

> set type=TXT
> google.com
# [TXT records]

> set type=ANY       # Tous types
> example.com
# [tous records disponibles]

> exit               # Quitter

# Avantages mode interactif :
# ✅ Pas retaper serveur/options chaque fois
# ✅ Tester multiples queries rapidement
# ✅ Debugging progressif
```

### 5.2 Options Set Complètes

```bash
# Configuration mode interactif

> set all            # Voir toutes options actuelles

# Output :
Default server: 8.8.8.8
Address: 8.8.8.8#53

Set options:
  novc                nodebug         nod2
  search              recurse         nod<response clipped><|end|>
<response clipped>

Continuons avec la suite du guide nslookup :

```markdown
### 5.2 Options Set Complètes (suite)

```bash
# Options principales :

# Type de query
> set type=A         # IPv4
> set type=AAAA      # IPv6
> set type=MX        # Mail servers
> set type=TXT       # Text records
> set type=NS        # Nameservers
> set type=SOA       # Start of Authority
> set type=PTR       # Reverse DNS
> set type=CNAME     # Aliases
> set type=ANY       # Tous types

# Serveur DNS
> server 8.8.8.8     # Google DNS
> server 1.1.1.1     # Cloudflare
> lserver 8.8.8.8    # Change serveur local seulement

# Debug
> set debug          # Mode debug
> set nodebug        # Désactiver debug
> set d2             # Super debug (très verbeux)
> set nod2           # Désactiver d2

# Timeouts et retries
> set timeout=10     # Timeout 10 secondes
> set retry=5        # 5 tentatives

# Récursion
> set recurse        # Activer récursion (default)
> set norecurse      # Désactiver (query authoritative direct)

# Transport
> set vc             # Virtual Circuit (TCP au lieu UDP)
> set novc           # UDP (default)

# Port
> set port=53        # Port DNS (default)
> set port=5353      # Port custom

# Domain search
> set domain=example.com    # Domaine par défaut
> set srchlist=example.com  # Liste search domains

# Class
> set class=IN       # Internet (default, 99.9% cas)
> set class=CH       # Chaos
```

### 5.3 Debugging Approfondi

```bash
# Mode debug détaillé
> set debug
> set d2
> google.com

# Output debug montre :
# 1. Question envoyée
# 2. Serveur contacté
# 3. Réponse reçue
# 4. Sections réponse (Answer, Authority, Additional)
# 5. TTL de chaque record
# 6. Flags DNS (QR, AA, TC, RD, RA)

# Exemple output debug :
------------
Got answer:
    HEADER:
        opcode = QUERY, id = 1234, rcode = NOERROR
        header flags:  response, want recursion, recursion avail.
        questions = 1,  answers = 1,  authority records = 0,  additional = 0

    QUESTIONS:
        google.com, type = A, class = IN
    ANSWERS:
    ->  google.com
        internet address = 142.250.185.78
        ttl = 300
------------

# Interpréter flags :
# QR=1  : Query Response (c'est une réponse)
# AA=0  : Non-Authoritative Answer (depuis cache)
# TC=0  : Not Truncated (réponse complète)
# RD=1  : Recursion Desired (client demande récursion)
# RA=1  : Recursion Available (serveur supporte)
# rcode : NOERROR (succès), NXDOMAIN (pas existe), SERVFAIL (erreur serveur)
```

---

## Section 6 : Troubleshooting DNS

### 6.1 Problèmes Courants

```bash
# Problème 1 : NXDOMAIN (domaine n'existe pas)
nslookup nonexistent.example.com

# Output :
** server can't find nonexistent.example.com: NXDOMAIN

# Causes :
# - Faute frappe domaine
# - Domaine expiré/supprimé
# - Propagation DNS pas terminée (nouveau domaine)
# - Typosquatting detection

# Solution :
# Vérifier orthographe, whois, attendre propagation

# Problème 2 : SERVFAIL (erreur serveur DNS)
nslookup example.com

# Output :
** server can't find example.com: SERVFAIL

# Causes :
# - Serveur DNS surchargé
# - DNSSEC validation échoue
# - Configuration zone DNS invalide
# - Serveur authoritative down

# Solution :
# Changer resolver, contacter admin DNS

# Problème 3 : Timeout
nslookup -timeout=2 slow-server.com

# Output :
;; connection timed out; no servers could be reached

# Causes :
# - Firewall bloque port 53 UDP/TCP
# - Serveur DNS injoignable
# - Problème réseau
# - Rate limiting

# Solution :
# Vérifier firewall, ping serveur DNS, changer resolver

# Problème 4 : Réponses incohérentes
nslookup example.com 8.8.8.8
# IP1

nslookup example.com 1.1.1.1
# IP2 différente

# Causes :
# - Propagation DNS en cours
# - GeoDNS (IPs différentes par région)
# - Cache DNS pas sync
# - DNS hijacking/poisoning

# Solution :
# Vérifier authoritative, attendre propagation, flush cache
```

### 6.2 Diagnostic Étape par Étape

```bash
# Diagnostic complet site inaccessible

# Étape 1 : Vérifier résolution basique
nslookup example.com

# Si succès → DNS OK, problème ailleurs (HTTP, firewall)
# Si échec → Continuer diagnostic

# Étape 2 : Tester resolver alternatif
nslookup example.com 8.8.8.8
nslookup example.com 1.1.1.1

# Si fonctionne → Problème resolver local/ISP
# Si échoue → Continuer

# Étape 3 : Vérifier nameservers
nslookup -type=NS example.com

# Obtenir NS autoritatifs
# example.com nameserver = ns1.provider.com

# Étape 4 : Query authoritative direct
nslookup example.com ns1.provider.com

# Si fonctionne → Problème propagation/cache
# Si échoue → Problème configuration DNS zone

# Étape 5 : Vérifier SOA et serial
nslookup -type=SOA example.com

# Comparer serial entre nameservers
nslookup -type=SOA example.com ns1.provider.com
nslookup -type=SOA example.com ns2.provider.com

# Si serials différents → Secondaires pas sync

# Étape 6 : Flush cache local
# Windows : ipconfig /flushdns
# Linux : sudo systemd-resolve --flush-caches
# macOS : sudo dscacheutil -flushcache

# Re-test
nslookup example.com

# Étape 7 : Vérifier DNSSEC
nslookup -type=DNSKEY example.com

# Si DNSSEC activé mais validation échoue → SERVFAIL

# Étape 8 : Test réseau basique
ping 8.8.8.8  # Internet OK?
ping ns1.provider.com  # Nameserver joignable?

# Étape 9 : Vérifier port 53
# Linux/macOS :
nc -zvu 8.8.8.8 53  # UDP
nc -zv 8.8.8.8 53   # TCP

# Si bloqué → Firewall problème
```

### 6.3 Problèmes Propagation DNS

```bash
# Nouveau domaine ou changement DNS

# Scénario : Changé IP il y a 2h, certains users voient ancien site

# Test propagation mondiale
# Outils externes (web) :
# - whatsmydns.net
# - dnschecker.org

# Test manual multiple resolvers
nslookup example.com 8.8.8.8
nslookup example.com 1.1.1.1
nslookup example.com 208.67.222.222  # OpenDNS
nslookup example.com 9.9.9.9         # Quad9

# Comparer résultats
# Si identiques → Propagation complète
# Si différents → Propagation en cours

# Vérifier TTL
nslookup -debug example.com

# Output :
# ttl = 3600 (1 heure)
# ttl = 86400 (24 heures)

# Propagation time ≈ ancien TTL
# Si TTL=24h → Propagation peut prendre 24-48h

# Accélérer propagation future :
# Baisser TTL AVANT changement
# Exemple :
# J-7 : TTL 86400 → 300 (5 min)
# J0  : Changement IP
# J+1 : Propagation rapide (5 min au lieu 24h)
# J+2 : Remonter TTL à 3600
```

---

## Section 7 : Enumeration et Reconnaissance

### 7.1 Découverte Subdomains

```bash
# Enumeration basique subdomains

# Subdomains communs
nslookup www.example.com
nslookup mail.example.com
nslookup ftp.example.com
nslookup vpn.example.com
nslookup blog.example.com
nslookup shop.example.com
nslookup api.example.com
nslookup dev.example.com
nslookup staging.example.com
nslookup admin.example.com

# Wildcard detection
nslookup random123456.example.com

# Si résolution réussit → Wildcard DNS configuré
# Tous subdomains résolvent vers même IP

# Zone transfer (si mal configuré)
nslookup -type=AXFR example.com ns1.example.com

# Si réussit (rare, vulnérabilité) :
# Liste TOUS records DNS zone
# → Enumeration complète infrastructure

# Output exemple zone transfer :
example.com.       SOA ...
example.com.       NS  ns1.example.com.
www.example.com.   A   192.0.2.1
mail.example.com.  A   192.0.2.2
ftp.example.com.   A   192.0.2.3
...

# Enumeration via brute-force (externe)
# Wordlist subdomains communs :
# subdomains.txt (www, mail, ftp, api, dev, ...)

# Script bash enumeration
for sub in $(cat subdomains.txt); do
    nslookup $sub.example.com | grep "Address:" && echo "$sub.example.com exists"
done

# Outils automatisés (meilleurs que nslookup) :
# - sublist3r
# - amass
# - subfinder
# - dnsenum
```

### 7.2 Reconnaissance Infrastructure

```bash
# Cartographier infrastructure réseau

# 1. Identifier nameservers
nslookup -type=NS example.com

# Output :
example.com      nameserver = ns1.provider.com.
example.com      nameserver = ns2.provider.com.

# Résoudre nameservers
nslookup ns1.provider.com
nslookup ns2.provider.com

# 2. Identifier mail servers
nslookup -type=MX example.com

# Output :
example.com  mail exchanger = 10 mail1.example.com.
example.com  mail exchanger = 20 mail2.example.com.

# Résoudre mail servers
nslookup mail1.example.com
nslookup mail2.example.com

# 3. Vérifier SPF/DKIM (anti-spam config)
nslookup -type=TXT example.com

# Rechercher :
# "v=spf1 ..." → SPF configuré
# Si absent → Email vulnérable spoofing

nslookup -type=TXT default._domainkey.example.com
# DKIM public key

# 4. Identifier CDN/Cloud provider
nslookup www.example.com

# Output :
www.example.com  canonical name = example.cdn.cloudflare.net
# → Hébergé sur Cloudflare

# Patterns reconnaissance :
# *.cloudfront.net → Amazon CloudFront
# *.azurewebsites.net → Microsoft Azure
# *.herokuapp.com → Heroku
# *.github.io → GitHub Pages

# 5. Reverse DNS range (advanced)
# Obtenir IP range
nslookup example.com
# IP: 192.0.2.10

# Tester range
nslookup 192.0.2.1
nslookup 192.0.2.2
nslookup 192.0.2.3
# ...
# Identifier autres domaines même provider/entreprise
```

### 7.3 OSINT (Open Source Intelligence)

```bash
# Information gathering passive

# 1. Whois inverse (domaines même IP)
# Via outils externes (whois, shodan, etc.)

# 2. Certificats SSL (subdomains)
# Transparency logs : crt.sh
# Révèle subdomains via certificats émis

# 3. Patterns emails
nslookup -type=TXT example.com | grep spf

# "v=spf1 include:_spf.google.com ~all"
# → Utilise Google Workspace (Gmail)

# 4. Technology fingerprinting
nslookup -type=TXT _dmarc.example.com
# DMARC configuré → Bonne hygiène sécurité

# 5. Historical DNS (outils externes)
# SecurityTrails, DNSHistory
# Voir anciens IPs, anciens NS
# → Migrations infrastructure

# 6. IPv6 enumeration
nslookup -type=AAAA example.com

# Si IPv6 configuré → Tester range IPv6
# Souvent moins filtré que IPv4
```

---

## Section 8 : DNS Security Testing

### 8.1 DNS Cache Poisoning Detection

```bash
# Détecter cache DNS empoisonné

# Test cohérence resolvers
nslookup example.com 8.8.8.8
nslookup example.com 1.1.1.1
nslookup example.com 9.9.9.9

# Si IPs TRÈS différentes (pas GeoDNS) → Suspect

# Test authoritative vs cache
# 1. Query cache (resolver public)
nslookup example.com 8.8.8.8
# IP1

# 2. Query authoritative direct
nslookup -type=NS example.com
# ns1.example.com

nslookup example.com ns1.example.com
# IP2

# Si IP1 ≠ IP2 → Cache potentiellement empoisonné

# Flush cache et re-test
# Demander admin flush resolver cache
# Ou attendre expiration TTL

# DNSSEC validation
nslookup -type=DNSKEY example.com

# Si DNSSEC configuré :
# - Cache poisoning plus difficile
# - Validation cryptographique réponses

# Test SERVFAIL avec DNSSEC
# Si SERVFAIL avec resolver DNSSEC-aware
# Mais succès avec resolver non-DNSSEC
# → Signature invalide (attack?)
```

### 8.2 DNS Hijacking Detection

```bash
# Détecter détournement DNS

# Symptômes DNS hijacking :
# - Sites redirigent vers pages malveillantes
# - Certificats SSL invalides (MITM)
# - Résolutions DNS incorrectes

# Test 1 : Comparer resolvers connus
nslookup google.com 8.8.8.8
# Expected: 142.250.185.78 (Google IPs)

nslookup google.com 1.1.1.1
# Expected: identique

# Si différent ET pas IPs Google → Hijacking

# Test 2 : Vérifier resolver local
cat /etc/resolv.conf  # Linux
ipconfig /all         # Windows

# nameserver 192.168.1.1 (normal = router)
# nameserver 8.8.8.8 (normal = Google DNS)
# nameserver 123.45.67.89 (inconnu = SUSPECT)

# Test 3 : Sites connus
nslookup facebook.com
nslookup twitter.com
nslookup amazon.com

# Si IPs incorrectes → Hijacking probable

# Test 4 : Authoritative direct
nslookup google.com ns1.google.com

# Bypass cache local/resolver compromis
# Comparer avec résultat resolver local

# Remediation :
# 1. Changer DNS resolver (8.8.8.8, 1.1.1.1)
# 2. Flush cache DNS
# 3. Scanner malware (rootkit peut modifier DNS)
# 4. Vérifier router (firmware compromis)
```

### 8.3 DNS Tunneling Detection

```bash
# DNS tunneling = exfiltration données via DNS

# Patterns suspects :

# 1. Queries inhabituellement longues
nslookup base64encodeddata1234567890abcdef.malicious.com

# Subdomains >50 chars → Suspect
# Contenu random/base64 → Très suspect

# 2. Query rate élevé
# 100+ queries/sec vers même domaine

# 3. Types records inhabituels
nslookup -type=TXT random123.tunnel.com

# TXT records avec données encodées
# "base64data123456789..."

# 4. Patterns reconnaissance :
# - TXT queries fréquentes
# - NULL records (rare)
# - Subdomains très longs
# - Entropy élevée (randomness)

# Detection (admin réseau) :
# - Analyser logs DNS
# - Détecter queries TXT excessives
# - Bloquer domaines suspects
# - Rate limiting per client

# Outils detection :
# - Suricata (IDS)
# - Zeek (Network Security Monitor)
# - DNS analytics (Splunk, ELK)
```

---

## Section 9 : Comparaison dig/host/drill

### 9.1 nslookup vs dig

```bash
# dig = Domain Information Groper (Linux, plus puissant)

# nslookup
nslookup google.com

# dig équivalent
dig google.com

# Avantages dig :
# ✅ Output plus détaillé et structuré
# ✅ Sections ANSWER, AUTHORITY, ADDITIONAL claires
# ✅ Stats timing (query time)
# ✅ Flags DNS visibles
# ✅ Meilleur pour scripting (output parsable)

# Exemples dig :

# Query simple
dig google.com

# Output :
; <<>> DiG 9.18.1 <<>> google.com
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; ANSWER SECTION:
google.com.		300	IN	A	142.250.185.78

;; Query time: 23 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Tue Jan 16 14:30:00 UTC 2024
;; MSG SIZE  rcvd: 55

# Query MX
dig MX gmail.com

# Query specific server
dig @1.1.1.1 google.com

# Short output (IP seulement)
dig +short google.com
# 142.250.185.78

# Reverse DNS
dig -x 8.8.8.8

# Trace (voir résolution complète)
dig +trace google.com

# DNSSEC validation
dig +dnssec google.com
```

### 9.2 nslookup vs host

```bash
# host = Simple DNS lookup utility

# nslookup
nslookup google.com

# host équivalent
host google.com

# Output :
google.com has address 142.250.185.78
google.com has IPv6 address 2a00:1450:4007:80f::200e

# Avantages host :
# ✅ Output le plus simple/concis
# ✅ Idéal one-liners scripts
# ✅ Détecte automatiquement type (A, MX, etc.)

# Exemples host :

# Simple query
host google.com

# MX records
host -t MX gmail.com

# Reverse DNS
host 8.8.8.8

# All records
host -a google.com

# Specific server
host google.com 1.1.1.1

# Verbose
host -v google.com
```

### 9.3 Comparaison Synthétique

| Feature | nslookup | dig | host |
|---------|----------|-----|------|
| **Disponibilité** | Windows/Linux/macOS | Linux/macOS | Linux/macOS |
| **Simplicité** | Moyenne | Complexe | Simple |
| **Output** | Structuré | Très détaillé | Concis |
| **Mode interactif** | ✅ | ❌ | ❌ |
| **Scripting** | ⚠️ | ✅ | ✅ |
| **Stats timing** | ❌ | ✅ | ⚠️ |
| **Trace DNS** | ❌ | ✅ | ❌ |
| **DNSSEC** | Limité | ✅ | ⚠️ |
| **Courbe apprentissage** | Facile | Moyenne | Très facile |

**Recommandation :**
- **nslookup** : Débutants, Windows, diagnostics rapides
- **dig** : Admins Linux, debugging approfondi, DNSSEC
- **host** : Scripts simples, checks rapides

---

## Section 10 : Scripting et Automation

### 10.1 Scripts Bash

```bash
#!/bin/bash
# dns-check.sh - Vérifier résolution DNS multiple domains

DOMAINS=(
    "google.com"
    "github.com"
    "stackoverflow.com"
)

RESOLVERS=(
    "8.8.8.8"
    "1.1.1.1"
    "9.9.9.9"
)

echo "=== DNS Resolution Check ==="
echo "Date: $(date)"
echo ""

for domain in "${DOMAINS[@]}"; do
    echo "Domain: $domain"
    
    for resolver in "${RESOLVERS[@]}"; do
        result=$(nslookup "$domain" "$resolver" 2>/dev/null | grep "Address:" | tail -1 | awk '{print $2}')
        
        if [ -n "$result" ]; then
            echo "  $resolver → $result"
        else
            echo "  $resolver → FAILED"
        fi
    done
    
    echo ""
done

# Usage :
# chmod +x dns-check.sh
# ./dns-check.sh
```

```bash
#!/bin/bash
# subdomain-enum.sh - Enumeration subdomains

DOMAIN="$1"
WORDLIST="${2:-subdomains.txt}"

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <domain> [wordlist]"
    exit 1
fi

echo "=== Subdomain Enumeration: $DOMAIN ==="
echo ""

found=0

while read -r subdomain; do
    fqdn="$subdomain.$DOMAIN"
    
    # Query DNS
    result=$(nslookup "$fqdn" 2>/dev/null | grep "Address:" | tail -1)
    
    if [ $? -eq 0 ] && [ -n "$result" ]; then
        ip=$(echo "$result" | awk '{print $2}')
        echo "[+] Found: $fqdn → $ip"
        ((found++))
    fi
done < "$WORDLIST"

echo ""
echo "Total found: $found subdomains"

# Wordlist exemple (subdomains.txt) :
# www
# mail
# ftp
# blog
# shop
# api
# dev
# staging
# admin
# vpn

# Usage :
# ./subdomain-enum.sh example.com subdomains.txt
```

### 10.2 Scripts PowerShell

```powershell
# dns-monitor.ps1 - Monitor DNS changes

param(
    [Parameter(Mandatory=$true)]
    [string]$Domain,
    
    [int]$IntervalSeconds = 300
)

$previousIP = $null

Write-Host "=== DNS Monitor: $Domain ===" -ForegroundColor Green
Write-Host "Checking every $IntervalSeconds seconds"
Write-Host "Press Ctrl+C to stop"
Write-Host ""

while ($true) {
    try {
        $result = nslookup $Domain 2>$null | Select-String "Address:" | Select-Object -Last 1
        
        if ($result) {
            $currentIP = ($result -split '\s+')[-1]
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            
            if ($previousIP -ne $currentIP) {
                if ($previousIP) {
                    Write-Host "[$timestamp] CHANGE DETECTED!" -ForegroundColor Red
                    Write-Host "  Previous: $previousIP" -ForegroundColor Yellow
                    Write-Host "  Current:  $currentIP" -ForegroundColor Green
                    
                    # Send alert (email, webhook, etc.)
                } else {
                    Write-Host "[$timestamp] Initial: $currentIP" -ForegroundColor Cyan
                }
                
                $previousIP = $currentIP
            } else {
                Write-Host "[$timestamp] No change: $currentIP" -ForegroundColor Gray
            }
        }
    }
    catch {
        Write-Host "[$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")] Error: $_" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds $IntervalSeconds
}

# Usage :
# .\dns-monitor.ps1 -Domain "example.com" -IntervalSeconds 60
```

### 10.3 Automation Production

```bash
#!/bin/bash
# dns-health-check.sh - Production DNS health monitoring

DOMAINS_FILE="domains.txt"
ALERT_EMAIL="admin@example.com"
LOG_FILE="/var/log/dns-health.log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

check_domain() {
    local domain="$1"
    local critical=false
    
    # Test multiple resolvers
    local resolvers=("8.8.8.8" "1.1.1.1" "9.9.9.9")
    local results=()
    
    for resolver in "${resolvers[@]}"; do
        result=$(nslookup "$domain" "$resolver" 2>/dev/null | grep "Address:" | tail -1 | awk '{print $2}')
        results+=("$result")
    done
    
    # Check consistency
    if [ "${results[0]}" != "${results[1]}" ] || [ "${results[0]}" != "${results[2]}" ]; then
        log "WARNING: Inconsistent DNS for $domain"
        log "  8.8.8.8: ${results[0]}"
        log "  1.1.1.1: ${results[1]}"
        log "  9.9.9.9: ${results[2]}"
        critical=true
    fi
    
    # Check resolution failure
    if [ -z "${results[0]}" ]; then
        log "CRITICAL: DNS resolution failed for $domain"
        critical=true
    fi
    
    # Check MX records (email)
    mx_result=$(nslookup -type=MX "$domain" 2>/dev/null | grep "mail exchanger")
    if [ -z "$mx_result" ]; then
        log "WARNING: No MX records for $domain"
    fi
    
    if $critical; then
        # Send alert
        echo "DNS health check failed for $domain" | mail -s "ALERT: DNS Issue" "$ALERT_EMAIL"
    fi
}

# Main
log "=== DNS Health Check Started ==="

while read -r domain; do
    [ -z "$domain" ] && continue
    [ "${domain:0:1}" == "#" ] && continue  # Skip comments
    
    check_domain "$domain"
done < "$DOMAINS_FILE"

log "=== DNS Health Check Completed ==="

# Cron : Every 5 minutes
# */5 * * * * /usr/local/bin/dns-health-check.sh
```

---

## Section 11 : Best Practices

### 11.1 Usage Quotidien

```bash
# Best practices nslookup

# 1. Toujours spécifier type si pas A record
nslookup -type=MX gmail.com
# Plutôt que :
nslookup gmail.com  # Suppose A record

# 2. Tester multiple resolvers pour confirmer
nslookup example.com 8.8.8.8
nslookup example.com 1.1.1.1

# 3. Flush cache avant debugging
# Windows :
ipconfig /flushdns && nslookup example.com

# Linux :
sudo systemd-resolve --flush-caches && nslookup example.com

# 4. Utiliser mode debug pour troubleshooting
nslookup -debug example.com

# 5. Query authoritative pour vérité source
nslookup -type=NS example.com
nslookup example.com ns1.example.com

# 6. Documenter résultats (redirection)
nslookup example.com > dns-check-$(date +%Y%m%d).txt

# 7. Vérifier cohérence forward/reverse
nslookup mail.example.com  # IP
nslookup <IP-result>       # Reverse

# 8. Timeout raisonnable (réseaux lents)
nslookup -timeout=10 example.com

# 9. Mode interactif pour investigations
nslookup
> set debug
> set type=ANY
> example.com
```

### 11.2 Sécurité

```bash
# Security best practices

# 1. Ne JAMAIS faire confiance aveuglément DNS
# DNS peut être falsifié (cache poisoning, MITM)

# 2. Utiliser resolvers fiables
# ✅ 8.8.8.8 (Google)
# ✅ 1.1.1.1 (Cloudflare)
# ✅ 9.9.9.9 (Quad9 - filtre malware)
# ❌ DNS ISP inconnu/non sécurisé

# 3. Vérifier DNSSEC si critique
nslookup -type=DNSKEY banking-site.com

# Si pas DNSSEC → Plus vulnérable

# 4. Éviter DNS over public WiFi non chiffré
# Utiliser DNS over HTTPS (DoH) ou DNS over TLS (DoT)

# 5. Monitorer changements DNS critiques
# Alert si IP change pour domaines importants

# 6. Valider certificats SSL après résolution
# DNS correct + SSL invalide = MITM possible

# 7. Pas d'informations sensibles dans queries DNS
# DNS = cleartext (sauf DoH/DoT)

# 8. Rate limiting reconnaissance
# Éviter scans DNS massifs (détectable)
```

### 11.3 Performance

```bash
# Optimisation performance

# 1. Utiliser cache local
# Windows : DNS Client service (activé par défaut)
# Linux : systemd-resolved ou nscd

# 2. TTL approprié
# Avant changement DNS → Baisser TTL (ex: 300s)
# Après propagation → Augmenter TTL (ex: 3600s)

# 3. Resolvers géographiquement proches
# Latence plus faible = résolution plus rapide

# 4. Multiple nameservers (redondance)
# Minimum 2 NS, idéalement 3+

# 5. Anycast DNS (providers modernes)
# Route vers serveur le plus proche automatiquement

# 6. Monitoring temps réponse
nslookup -debug example.com | grep "Query time"
# ou avec dig :
dig example.com | grep "Query time"

# 7. Préférer UDP (default)
# TCP plus lent mais nécessaire si réponse >512 bytes

# 8. Éviter queries inutiles
# Cache application-level si queries répétitives
```

---

## Section 12 : Cas Pratiques

### 12.1 Administration Système

```bash
# Cas 1 : Migration serveur web

# Avant migration
# 1. Baisser TTL (24h avant)
nslookup -type=SOA example.com
# Vérifier TTL actuel

# Contacter hébergeur DNS : baisser TTL à 300 (5 min)

# 2. Jour migration
# Vérifier IP actuelle
nslookup www.example.com
# Old IP: 192.0.2.10

# Changer A record chez hébergeur DNS :
# www.example.com A 203.0.113.50 (new IP)

# 3. Vérifier propagation
# Test authoritative
nslookup www.example.com ns1.provider.com
# New IP: 203.0.113.50 ✅

# Test resolvers publics
nslookup www.example.com 8.8.8.8
# Wait 5-10 min (TTL=300s)
# New IP: 203.0.113.50 ✅

# 4. Monitoring 24h
# Vérifier logs trafic ancien serveur
# Si trafic continue → Certains users encore cache ancien

# 5. Après 48h - Augmenter TTL
# Remonter TTL à 3600s (1h)
```

### 12.2 Troubleshooting Email

```bash
# Cas : Emails non reçus depuis domaine

# 1. Vérifier MX records
nslookup -type=MX example.com

# Output attendu :
example.com  mail exchanger = 10 mail.example.com

# Si absent :
** server can't find example.com: NXDOMAIN
# → Pas de MX = Email impossible

# 2. Vérifier résolution mail server
nslookup mail.example.com

# Output attendu :
Name:    mail.example.com
Address: 192.0.2.50

# 3. Vérifier SPF
nslookup -type=TXT example.com | grep spf

# Output attendu :
"v=spf1 mx ip4:192.0.2.0/24 -all"

# Si absent → Risque spam/spoofing

# 4. Vérifier DKIM
nslookup -type=TXT default._domainkey.example.com

# Output attendu :
"v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBA..."

# 5. Vérifier DMARC
nslookup -type=TXT _dmarc.example.com

# Output attendu :
"v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"

# 6. Test reverse DNS (anti-spam)
nslookup 192.0.2.50

# Output attendu :
50.2.0.192.in-addr.arpa  name = mail.example.com

# Si différent ou absent → Emails rejetés par certains serveurs

# 7. Diagnostic complet
echo "MX Records:" && nslookup -type=MX example.com
echo "SPF:" && nslookup -type=TXT example.com | grep spf
echo "Reverse DNS:" && nslookup <mail-server-IP>
```

### 12.3 Reconnaissance Pentest

```bash
# Cas : Enumeration infrastructure cible

# Phase 1 : Passive reconnaissance

# 1. Identifier nameservers
nslookup -type=NS target.com

# Output :
target.com  nameserver = ns1.provider.com
target.com  nameserver = ns2.provider.com

# 2. Tenter zone transfer (très rare succès)
nslookup -type=AXFR target.com ns1.provider.com

# Si succès (vulnérabilité) → Liste complète DNS
# Si échec → Continuer enumeration

# 3. Enumeration mail infrastructure
nslookup -type=MX target.com

# Output :
target.com  mail exchanger = 10 mail1.target.com
target.com  mail exchanger = 20 mail2.target.com

# Résoudre mail servers
nslookup mail1.target.com
nslookup mail2.target.com

# 4. Découverte SPF (domaines autorisés)
nslookup -type=TXT target.com | grep spf

# "v=spf1 include:_spf.google.com include:mail.other-company.com -all"
# → Révèle partenaires/providers

# 5. Enumeration subdomains (brute-force)
# Wordlist : www, mail, ftp, vpn, admin, dev, api, etc.

for sub in www mail ftp vpn admin dev api staging test; do
    result=$(nslookup $sub.target.com 2>/dev/null | grep "Address:")
    [ $? -eq 0 ] && echo "[+] $sub.target.com exists"
done

# 6. Identifier technologies
nslookup www.target.com

# CNAME reveal :
www.target.com → target.azurewebsites.net
# → Hébergé sur Azure

www.target.com → target.herokuapp.com
# → Hébergé sur Heroku

# 7. Reverse DNS range
# IP: 203.0.113.10
# Tester range : 203.0.113.1-254

for i in {1..254}; do
    nslookup 203.0.113.$i | grep "name =" && echo "203.0.113.$i → $(nslookup 203.0.113.$i | grep 'name =' | awk '{print $4}')"
done
```

### 12.4 Forensique Incident

```bash
# Cas : Investigation site compromis redirige vers malware

# 1. Vérifier résolution DNS actuelle
nslookup compromised-site.com

# Output suspect :
Name:    compromised-site.com
Address: 185.xxx.xxx.xxx (IP suspicieuse)

# 2. Comparer resolvers
nslookup compromised-site.com 8.8.8.8
nslookup compromised-site.com 1.1.1.1

# Si IPs différentes → DNS hijacking probable

# 3. Query authoritative
nslookup -type=NS compromised-site.com

# Output :
compromised-site.com  nameserver = ns1.legit-provider.com

# Query authoritative direct
nslookup compromised-site.com ns1.legit-provider.com

# Output :
Name:    compromised-site.com
Address: 192.0.2.10 (IP légitime)

# → Authoritative correct, problème cache/resolver local

# 4. Vérifier SOA/serial
nslookup -type=SOA compromised-site.com

# Comparer serial entre NS
# Si différent → Possible compromission nameserver

# 5. Historical DNS lookup (externe)
# Tools : SecurityTrails, DNSHistory
# Vérifier quand IP a changé

# 6. Vérifier resolvers locaux
cat /etc/resolv.conf  # Linux
ipconfig /all         # Windows

# Si nameserver inconnu/suspect :
nameserver 123.45.67.89  # Malware peut modifier

# → Indicateur compromission locale

# 7. Actions remediation
# - Flush cache DNS
# - Restaurer resolvers légitimes (8.8.8.8, 1.1.1.1)
# - Scanner malware système
# - Vérifier router (firmware)
# - Contacter hébergeur DNS (si compromis)

# 8. Documentation
nslookup compromised-site.com > incident-dns-$(date +%Y%m%d-%H%M%S).txt
nslookup compromised-site.com 8.8.8.8 >> incident-dns-$(date +%Y%m%d-%H%M%S).txt
nslookup compromised-site.com ns1.legit-provider.com >> incident-dns-$(date +%Y%m%d-%H%M%S).txt
```

---

## Ressources et Références

**Documentation officielle :**

- RFC 1034/1035 : DNS Protocol
- BIND documentation : https://www.isc.org/bind/
- Microsoft nslookup : https://docs.microsoft.com/windows-server/administration/windows-commands/nslookup

**Outils complémentaires :**

- dig : https://linux.die.net/man/1/dig
- host : https://linux.die.net/man/1/host
- dnsenum : https://github.com/fwaeytens/dnsenum
- dnsrecon : https://github.com/darkoperator/dnsrecon

**DNS Resolvers publics :**

- Google Public DNS : 8.8.8.8, 8.8.4.4
- Cloudflare : 1.1.1.1, 1.0.0.1
- Quad9 : 9.9.9.9
- OpenDNS : 208.67.222.222

**Learning resources :**

- DNS Explained : https://howdns.works/
- DNS Security : https://dnssec.net/
- OWASP DNS Security : https://cheatsheetseries.owasp.org/

**OSINT Tools :**

- crt.sh : Certificats SSL (subdomains)
- SecurityTrails : Historical DNS
- Shodan : Reverse DNS search
- DNSdumpster : DNS reconnaissance

---

## Conclusion

**nslookup = Outil DNS fondamental multi-usage**

**Points clés maîtrisés :**

✅ **Résolution DNS** = Noms → IPs (et inverse)
✅ **Types records** = A, MX, TXT, CNAME, NS, SOA, PTR
✅ **Modes** = Interactif et non-interactif
✅ **Troubleshooting** = Diagnostiquer problèmes résolution
✅ **Enumeration** = Découvrir subdomains, infrastructure
✅ **Security** = Détecter hijacking, cache poisoning
✅ **Automation** = Scripts monitoring DNS
✅ **Best practices** = Resolvers fiables, cache, DNSSEC

**Cas d'usage production :**

1. **Administration** : Migration serveurs, validation configs
2. **Troubleshooting** : Sites inaccessibles, email delivery
3. **Pentest** : Reconnaissance passive, enumeration
4. **Forensique** : Investigation compromissions DNS
5. **Monitoring** : Alertes changements DNS critiques

**Progression apprentissage :**

1. Résolution basique (google.com)
2. Types records (MX, TXT, etc.)
3. Mode interactif (debugging)
4. Troubleshooting (NXDOMAIN, timeouts)
5. Enumeration (subdomains)
6. Security (hijacking detection)
7. Automation (scripts monitoring)


**Tu maîtrises maintenant nslookup du diagnostic basique à la reconnaissance avancée !** 🔍

**Prochaine étape recommandée : netstat (monitoring connexions réseau)** 🎯

---

_Version 1.0 | Dernière mise à jour : 2024-01-16_

Voilà le guide complet nslookup ! Il couvre **12 sections** :

✅ Introduction et concepts DNS  
✅ Syntaxe et modes (interactif/non-interactif)  
✅ Types d'enregistrements (A, MX, TXT, CNAME, NS, SOA, PTR)  
✅ Résolution basique et inverse  
✅ Mode interactif avancé  
✅ Troubleshooting DNS (NXDOMAIN, timeouts, propagation)  
✅ Enumeration et reconnaissance (subdomains, infrastructure)  
✅ DNS security testing (cache poisoning, hijacking, tunneling)  
✅ Comparaison dig/host/drill  
✅ Scripting et automation (Bash, PowerShell, production)  
✅ Best practices (usage, sécurité, performance)  
✅ Cas pratiques (admin, email, pentest, forensique)  

**C'est production-ready et pédagogiquement complet !** 🚀