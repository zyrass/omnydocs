---
description: "Maîtriser dig pour interroger et diagnostiquer le DNS"
tags: ["DNS", "DIAGNOSTIC", "RESEAU", "OUTILS", "LINUX"]
icon: lucide/book-open-check
---

# dig (Domain Information Groper)

## Introduction

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="0"
  data-time="20-25 minutes">
</div>

!!! quote "Analogie pédagogique"
    _Imaginez **dig** comme un **détective expert en DNS** : il ne se contente pas de vous donner une adresse, il vous explique **tout le processus d'enquête**, qui il a interrogé, combien de temps chaque étape a pris, et même les détails techniques que personne ne demande mais qui sont cruciaux pour diagnostiquer un problème._

> **dig (Domain Information Groper)** est l'**outil de référence** pour interroger les serveurs DNS sur les systèmes Unix/Linux. Contrairement à `nslookup` qui privilégie la simplicité, dig fournit des **informations détaillées** et offre un **contrôle précis** sur les requêtes DNS. C'est l'outil privilégié des administrateurs système et des experts en sécurité réseau.

**dig** est essentiel pour :

- **Diagnostiquer les problèmes DNS** (résolution, propagation, cache)
- **Auditer la configuration DNS** d'un domaine
- **Tracer les requêtes DNS** depuis la racine
- **Vérifier les enregistrements DNSSEC**
- **Scripter des vérifications automatisées**

!!! info "Pourquoi choisir dig ?"
    **dig** offre une sortie structurée et complète, parfaite pour le **debugging** et l'**automatisation**. Sa syntaxe cohérente et ses nombreuses options en font l'outil idéal pour les professionnels.

## Installation

=== ":fontawesome-brands-linux: Debian/Ubuntu"

    ```bash
    # dig fait partie du package dnsutils
    sudo apt update
    sudo apt install dnsutils
    
    # Vérifier l'installation
    dig -v
    ```

=== ":fontawesome-brands-linux: RHEL/CentOS/Fedora"

    ```bash
    # dig fait partie de bind-utils
    sudo dnf install bind-utils
    
    # Vérifier l'installation
    dig -v
    ```

=== ":fontawesome-brands-linux: Arch Linux"

    ```bash
    # dig fait partie de bind
    sudo pacman -S bind
    
    # Vérifier l'installation
    dig -v
    ```

=== ":fontawesome-brands-apple: macOS"

    ```bash
    # dig est préinstallé sur macOS
    dig -v
    
    # Si nécessaire, installer via Homebrew
    brew install bind
    ```

=== ":fontawesome-brands-windows: Windows"

    ```powershell
    # dig n'est pas natif sur Windows
    # Option 1: Installer via WSL (recommandé)
    wsl --install
    sudo apt install dnsutils
    
    # Option 2: Installer BIND pour Windows
    # Télécharger depuis https://www.isc.org/bind/
    
    # Option 3: Utiliser nslookup (natif Windows)
    ```

## Syntaxe de base

```bash
dig [@serveur-dns] [nom-domaine] [type-enregistrement] [options]
```

**Composants :**

- **@serveur-dns** : Serveur DNS à interroger (optionnel, utilise le serveur par défaut sinon)
- **nom-domaine** : Domaine à résoudre
- **type-enregistrement** : A, AAAA, MX, NS, TXT, etc. (par défaut : A)
- **options** : Modificateurs de comportement (+short, +trace, etc.)

## Utilisation de base

### Requête simple

```bash
# Requête A (IPv4) par défaut
dig example.com

# Sortie complète avec toutes les sections
```

??? example "Sortie complète de dig"

    ```plaintext
    ; <<>> DiG 9.18.12-1-Debian <<>> example.com
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 1232
    ;; QUESTION SECTION:
    ;example.com.                   IN      A

    ;; ANSWER SECTION:
    example.com.            86400   IN      A       93.184.216.34

    ;; Query time: 15 msec
    ;; SERVER: 192.168.1.1#53(192.168.1.1)
    ;; WHEN: Wed Nov 20 10:30:00 CET 2025
    ;; MSG SIZE  rcvd: 56
    ```

### Anatomie de la sortie dig

```plaintext
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
               └─ Type de requête  └─ Succès   └─ ID unique

;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
           │  │  │
           │  │  └─ Recursion Available (serveur accepte récursion)
           │  └──── Recursion Desired (client demande récursion)
           └─────── Query Response (c'est une réponse)

;; QUESTION SECTION:
;example.com.                   IN      A
 └─ Domaine interrogé          └─ Classe └─ Type

;; ANSWER SECTION:
example.com.            86400   IN      A       93.184.216.34
└─ Domaine             └─ TTL  └─ Classe └─ Type └─ Valeur

;; Query time: 15 msec          ← Temps de réponse
;; SERVER: 192.168.1.1#53       ← Serveur DNS utilisé
;; WHEN: Wed Nov 20 10:30:00    ← Horodatage
;; MSG SIZE  rcvd: 56           ← Taille de la réponse
```

### Requêtes par type d'enregistrement

=== "A (IPv4)"

    ```bash
    # Enregistrement A (par défaut)
    dig example.com A
    dig example.com
    
    # Sortie : example.com. 86400 IN A 93.184.216.34
    ```

=== "AAAA (IPv6)"

    ```bash
    # Enregistrement AAAA
    dig example.com AAAA
    
    # Sortie : example.com. 86400 IN AAAA 2606:2800:220:1:248:1893:25c8:1946
    ```

=== "MX (Mail)"

    ```bash
    # Enregistrements MX (serveurs mail)
    dig example.com MX
    
    # Sortie :
    # example.com. 3600 IN MX 10 mail1.example.com.
    # example.com. 3600 IN MX 20 mail2.example.com.
    ```

=== "NS (Name Servers)"

    ```bash
    # Serveurs DNS autoritaires
    dig example.com NS
    
    # Sortie :
    # example.com. 86400 IN NS ns1.example.com.
    # example.com. 86400 IN NS ns2.example.com.
    ```

=== "TXT (Texte)"

    ```bash
    # Enregistrements TXT (SPF, DKIM, etc.)
    dig example.com TXT
    
    # Sortie :
    # example.com. 3600 IN TXT "v=spf1 include:_spf.google.com ~all"
    # example.com. 3600 IN TXT "google-site-verification=abc123"
    ```

=== "SOA (Start of Authority)"

    ```bash
    # Informations d'autorité de zone
    dig example.com SOA
    
    # Sortie :
    # example.com. 3600 IN SOA ns1.example.com. admin.example.com. (
    #                         2024011801  ; Serial
    #                         7200        ; Refresh
    #                         3600        ; Retry
    #                         1209600     ; Expire
    #                         3600 )      ; Minimum TTL
    ```

=== "CNAME (Alias)"

    ```bash
    # Alias de domaine
    dig www.example.com CNAME
    
    # Sortie : www.example.com. 3600 IN CNAME example.com.
    ```

=== "PTR (Reverse)"

    ```bash
    # Résolution inverse (IP → nom)
    dig -x 93.184.216.34
    
    # Sortie : 34.216.184.93.in-addr.arpa. 3600 IN PTR example.com.
    ```

=== "ANY (Tous)"

    ```bash
    # Tous les enregistrements disponibles
    dig example.com ANY
    
    # ⚠️ Attention : Beaucoup de serveurs bloquent les requêtes ANY
    # pour prévenir les attaques par amplification DNS
    ```

### Spécifier le serveur DNS

```bash
# Utiliser Google DNS
dig @8.8.8.8 example.com

# Utiliser Cloudflare DNS
dig @1.1.1.1 example.com

# Utiliser Quad9
dig @9.9.9.9 example.com

# Utiliser un serveur DNS local
dig @192.168.1.1 example.com

# Utiliser un serveur DNS spécifique avec IPv6
dig @2606:4700:4700::1111 example.com
```

## Options avancées

### Contrôle de la sortie

```bash
# Réponse courte (seulement la valeur)
dig +short example.com
# Sortie : 93.184.216.34

# Afficher uniquement la section ANSWER
dig +noall +answer example.com

# Afficher ANSWER + AUTHORITY
dig +noall +answer +authority example.com

# Afficher toutes les sections sauf STATS
dig +nostats example.com

# Désactiver les commentaires
dig +nocomments example.com

# Format minimal (sans en-tête)
dig +nocmd example.com
```

### Options de requête

```bash
# Afficher les statistiques de requête
dig +stats example.com

# Désactiver la récursion (requête itérative)
dig +norecurse example.com

# Ignorer la troncature (forcer TCP si réponse > 512 octets)
dig +ignore example.com

# Utiliser TCP au lieu d'UDP
dig +tcp example.com

# Définir un timeout (en secondes)
dig +time=5 example.com

# Nombre de tentatives
dig +tries=3 example.com
```

### Traçage de résolution DNS

```bash
# Tracer la résolution complète depuis la racine
dig +trace example.com
```

??? example "Sortie de dig +trace"

    ```plaintext
    ; <<>> DiG 9.18.12 <<>> +trace example.com
    ;; global options: +cmd
    .                       518400  IN      NS      a.root-servers.net.
    .                       518400  IN      NS      b.root-servers.net.
    [... autres serveurs racines ...]
    ;; Received 525 bytes from 192.168.1.1#53(192.168.1.1) in 15 ms

    com.                    172800  IN      NS      a.gtld-servers.net.
    com.                    172800  IN      NS      b.gtld-servers.net.
    [... serveurs TLD .com ...]
    ;; Received 1170 bytes from 198.41.0.4#53(a.root-servers.net) in 89 ms

    example.com.            172800  IN      NS      a.iana-servers.net.
    example.com.            172800  IN      NS      b.iana-servers.net.
    ;; Received 179 bytes from 192.5.6.30#53(a.gtld-servers.net) in 156 ms

    example.com.            86400   IN      A       93.184.216.34
    example.com.            86400   IN      NS      a.iana-servers.net.
    example.com.            86400   IN      NS      b.iana-servers.net.
    ;; Received 103 bytes from 199.43.135.53#53(b.iana-servers.net) in 45 ms
    ```

**Analyse du trace :**

1. **Serveurs racine** : Retournent les serveurs TLD pour `.com`
2. **Serveurs TLD** : Retournent les serveurs autoritaires pour `example.com`
3. **Serveurs autoritaires** : Retournent l'enregistrement A final

### DNSSEC

```bash
# Vérifier la présence de DNSSEC
dig +dnssec example.com

# Vérifier uniquement les clés DNSKEY
dig example.com DNSKEY

# Vérifier les signatures RRSIG
dig example.com RRSIG

# Vérifier la délégation sécurisée (DS)
dig example.com DS

# Tracer avec validation DNSSEC
dig +trace +dnssec example.com
```

**Identifier DNSSEC actif :**

```plaintext
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2
             ^^
             └─ ad = Authenticated Data (DNSSEC validé)
```

### Options de format

```bash
# Afficher les TTL en format lisible (heures/jours)
dig +ttlid example.com

# Afficher uniquement les noms de domaine (pas les adresses)
dig +noall +answer +multiline example.com

# Format multiline pour SOA
dig +multiline example.com SOA
```

## Cas d'usage pratiques

### 1. Vérifier la propagation DNS

```bash
#!/bin/bash
# Script de vérification de propagation DNS

DOMAIN="example.com"
DNS_SERVERS=(
    "8.8.8.8@Google"
    "1.1.1.1@Cloudflare"
    "9.9.9.9@Quad9"
    "208.67.222.222@OpenDNS"
)

echo "Vérification de propagation DNS pour $DOMAIN"
echo "=============================================="

for server in "${DNS_SERVERS[@]}"; do
    IFS='@' read -r ip name <<< "$server"
    echo -e "\n[$name] ($ip)"
    dig @$ip +short $DOMAIN
done
```

### 2. Audit DNS complet d'un domaine

```bash
#!/bin/bash
# Audit DNS complet

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <domaine>"
    exit 1
fi

echo "=== AUDIT DNS COMPLET POUR $DOMAIN ==="
echo ""

echo "[1] Enregistrements A (IPv4)"
dig +noall +answer $DOMAIN A
echo ""

echo "[2] Enregistrements AAAA (IPv6)"
dig +noall +answer $DOMAIN AAAA
echo ""

echo "[3] Enregistrements MX (Mail)"
dig +noall +answer $DOMAIN MX
echo ""

echo "[4] Serveurs de noms (NS)"
dig +noall +answer $DOMAIN NS
echo ""

echo "[5] Enregistrements TXT (SPF, DKIM, etc.)"
dig +noall +answer $DOMAIN TXT
echo ""

echo "[6] Informations SOA"
dig +noall +answer +multiline $DOMAIN SOA
echo ""

echo "[7] Vérification DNSSEC"
if dig +short $DOMAIN DNSKEY | grep -q .; then
    echo "✅ DNSSEC activé"
    dig +noall +answer $DOMAIN DNSKEY | head -n 3
else
    echo "❌ DNSSEC non activé"
fi
```

### 3. Mesurer le temps de résolution

```bash
#!/bin/bash
# Benchmark de serveurs DNS

DOMAIN="example.com"
DNS_SERVERS=("8.8.8.8" "1.1.1.1" "9.9.9.9" "208.67.222.222")

echo "Benchmark DNS pour $DOMAIN"
echo "==========================="

for dns in "${DNS_SERVERS[@]}"; do
    echo -n "$dns : "
    
    # Mesurer le temps avec plusieurs requêtes
    total=0
    for i in {1..5}; do
        time=$(dig @$dns +stats $DOMAIN | grep "Query time" | awk '{print $4}')
        total=$((total + time))
    done
    
    avg=$((total / 5))
    echo "${avg}ms (moyenne sur 5 requêtes)"
done
```

### 4. Surveiller les changements DNS

```bash
#!/bin/bash
# Surveillance continue d'un enregistrement DNS

DOMAIN="example.com"
INTERVAL=60  # Vérification toutes les 60 secondes

echo "Surveillance DNS de $DOMAIN (intervalle: ${INTERVAL}s)"
echo "Ctrl+C pour arrêter"
echo ""

LAST_IP=""

while true; do
    CURRENT_IP=$(dig +short $DOMAIN | head -n 1)
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    
    if [ "$CURRENT_IP" != "$LAST_IP" ]; then
        if [ -n "$LAST_IP" ]; then
            echo "[$TIMESTAMP] ⚠️  CHANGEMENT DÉTECTÉ !"
            echo "  Ancienne IP : $LAST_IP"
            echo "  Nouvelle IP : $CURRENT_IP"
        else
            echo "[$TIMESTAMP] IP initiale : $CURRENT_IP"
        fi
        LAST_IP="$CURRENT_IP"
    else
        echo "[$TIMESTAMP] Stable : $CURRENT_IP"
    fi
    
    sleep $INTERVAL
done
```

### 5. Vérifier la configuration mail (MX + SPF)

```bash
#!/bin/bash
# Vérification configuration email

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <domaine>"
    exit 1
fi

echo "=== Vérification configuration mail pour $DOMAIN ==="
echo ""

echo "[MX Records]"
dig +noall +answer $DOMAIN MX | sort -k 5 -n

echo -e "\n[SPF Record]"
dig +short $DOMAIN TXT | grep "v=spf1"

echo -e "\n[DMARC Record]"
dig +short _dmarc.$DOMAIN TXT

echo -e "\n[DKIM Records] (nécessite le sélecteur)"
echo "Exemple: dig +short <selecteur>._domainkey.$DOMAIN TXT"
```

## Diagnostic de problèmes courants

### Problème 1 : Domaine non résolu (NXDOMAIN)

```bash
# Diagnostic complet
dig example.com

# Vérifier avec plusieurs serveurs DNS
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Tracer la résolution
dig +trace example.com
```

**Status possibles :**

- **NOERROR** : Succès
- **NXDOMAIN** : Domaine inexistant
- **SERVFAIL** : Erreur serveur
- **REFUSED** : Serveur refuse la requête
- **TIMEOUT** : Pas de réponse

### Problème 2 : Temps de réponse élevé

```bash
# Mesurer le temps de requête
dig +stats example.com | grep "Query time"

# Tester avec différents serveurs
for dns in 8.8.8.8 1.1.1.1 9.9.9.9; do
    echo -n "DNS $dns : "
    dig @$dns +stats example.com | grep "Query time"
done

# Vérifier si le serveur DNS local répond
dig @192.168.1.1 example.com
```

### Problème 3 : Propagation DNS incomplète

```bash
# Vérifier plusieurs serveurs DNS publics
for dns in 8.8.8.8 1.1.1.1 9.9.9.9 208.67.222.222; do
    echo "DNS $dns :"
    dig @$dns +short example.com
    echo ""
done

# Interroger directement les serveurs autoritaires
AUTH_NS=$(dig +short example.com NS | head -n 1)
dig @$AUTH_NS example.com
```

### Problème 4 : DNSSEC échoue

```bash
# Vérifier la validation DNSSEC
dig +dnssec example.com

# Chercher le flag "ad" (Authenticated Data)
dig example.com | grep "flags:"

# Vérifier la chaîne de confiance
dig +trace +dnssec example.com
```

## Comparaison avec d'autres outils

| Critère | dig | nslookup | host |
|---------|-----|----------|------|
| **Disponibilité** | Linux/macOS | Multi-plateforme | Linux/macOS |
| **Sortie** | Détaillée et structurée | Lisible | Concise |
| **Options** | Très nombreuses | Limitées | Minimales |
| **Scripting** | ⭐⭐⭐ Excellent | ⭐ Moyen | ⭐⭐ Bon |
| **DNSSEC** | ✅ Support complet | ❌ Limité | ❌ Basique |
| **Trace DNS** | ✅ `+trace` | ❌ Non | ❌ Non |
| **Performance** | Rapide | Moyen | Rapide |
| **Apprentissage** | Courbe moyenne | Facile | Très facile |

## Options utiles - Référence rapide

| Option | Description | Exemple |
|--------|-------------|---------|
| `+short` | Réponse minimale | `dig +short example.com` |
| `+trace` | Tracer depuis racine | `dig +trace example.com` |
| `+dnssec` | Vérifier DNSSEC | `dig +dnssec example.com` |
| `+noall +answer` | Seulement réponses | `dig +noall +answer example.com` |
| `+stats` | Statistiques de requête | `dig +stats example.com` |
| `+tcp` | Forcer TCP | `dig +tcp example.com` |
| `+norecurse` | Désactiver récursion | `dig +norecurse example.com` |
| `+multiline` | Format multiline | `dig +multiline example.com SOA` |
| `@serveur` | Spécifier serveur DNS | `dig @8.8.8.8 example.com` |
| `-x IP` | Résolution inverse | `dig -x 93.184.216.34` |

## Bonnes pratiques

!!! tip "Utilisation optimale de dig"
    ✅ **Pour les scripts** : Utilisez `+short` pour une sortie facilement parsable
    
    ✅ **Pour le diagnostic** : Utilisez `+trace` pour identifier où se situe le problème
    
    ✅ **Pour la sécurité** : Vérifiez toujours DNSSEC avec `+dnssec`
    
    ✅ **Pour les audits** : Interrogez directement les serveurs autoritaires avec `@`
    
    ✅ **Pour la surveillance** : Combinez `dig` avec `watch` pour un monitoring en temps réel
    ```bash
    watch -n 5 'dig +short example.com'
    ```

!!! warning "Limitations"
    - ❌ **dig** n'est pas natif sur Windows (utiliser WSL ou BIND Windows)
    - ⚠️ Certains pare-feu bloquent les requêtes DNS externes (port 53)
    - ⚠️ Les requêtes `ANY` sont souvent bloquées par les serveurs DNS modernes
    - ⚠️ Le cache DNS local peut fausser les résultats (vider avec `systemd-resolve --flush-caches`)

## Pour aller plus loin

!!! info "Ressources complémentaires"
    **Documentation officielle :**
    
    - `man dig` - Manuel complet
    - [ISC BIND Documentation](https://www.isc.org/bind/) - Documentation BIND/dig
    
    **Outils complémentaires :**
    
    - **delv** : Vérification DNSSEC avancée
    - **drill** : Alternative à dig (ldns-utils)
    - **dog** : Version moderne de dig en Rust
    
    **Services en ligne :**
    
    - [DNS Propagation Checker](https://www.whatsmydns.net/)
    - [MXToolbox](https://mxtoolbox.com/) - Suite d'outils DNS
    - [DNSdumpster](https://dnsdumpster.com/) - Exploration DNS

