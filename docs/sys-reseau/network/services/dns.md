---
description: "DNS : architecture, configuration serveurs, zones, DNSSEC, performance, sécurité"
icon: lucide/book-open-check
tags: ["DNS", "BIND", "NAMESERVER", "RESOLUTION", "DNSSEC", "NETWORK", "INFRASTRUCTURE"]
---

# DNS 

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-time="8-10 heures"
  data-version="1.0">
</div>

## Introduction aux Domain Name System

!!! quote "Analogie pédagogique"
    _Imaginez le **système postal mondial interconnecté gérant 3+ milliards adresses planète** : DNS fonctionne comme **annuaire téléphonique Internet hiérarchique distribué traduisant noms humains (google.com) en adresses machines (142.250.185.78)** permettant communication. **Système postal DNS mondial** : bureaux poste hiérarchiques (root → TLD → authoritative servers), annuaires locaux caches (resolvers ISP), adresses structurées hiérarchiques (google.com = rue.ville.pays), système routage intelligent (GeoDNS = bureau poste le plus proche), redondance complète (13 root servers répliqués mondialement), mise à jour dynamique (TTL = durée validité adresse), sécurité validation (DNSSEC = signature cryptographique adresses), acheminement optimisé (Anycast = multiple chemins même destination). **Sans DNS** : devoir mémoriser 142.250.185.78 au lieu google.com (impossible humainement), sites inaccessibles si IP change (migrations serveurs = liens cassés), email impossible (pas résolution MX mail servers), certificats SSL invalides (validation domaine échoue), Internet comme années 70 (fichiers hosts manuels 10,000+ lignes), scalabilité nulle (centralisation = point défaillance unique). **Avec DNS** : **Résolution instantanée** (google.com → IP en 20-200ms), **Hiérarchie distribuée** (pas point défaillance unique mondial), **Cache multi-niveaux** (browser → OS → resolver → authoritative), **Load balancing** (round-robin DNS = distribuer charge), **Géolocalisation** (GeoDNS = serveur le plus proche utilisateur), **Failover automatique** (si serveur down = IP suivante), **Infrastructure as Code** (zones DNS = configuration programmable), **Sécurité DNSSEC** (signatures cryptographiques anti-spoofing). **DNS = colonne vertébrale Internet** : 4.66+ milliards domaines enregistrés (2024), ~3 trillions requêtes DNS/jour mondialement, 99.99%+ uptime infrastructure critique, première étape TOUTE connexion Internet (web, email, API, streaming), attaques DNS = paralysie infrastructure complète (DDoS Dyn 2016 paralyse Twitter/Netflix/GitHub). **Architecture DNS hiérarchique** : Root servers 13 (a-m.root-servers.net répliqués mondialement Anycast), TLD servers (.com, .org, .fr gérés ICANN/registries), Authoritative nameservers (hébergeurs DNS domaines), Recursive resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1, ISP), Cache local (OS/browser TTL). **Processus résolution complet** : User → Browser cache (instant si présent) → OS cache → Recursive resolver cache → Root server (.com où?) → TLD server (google.com où?) → Authoritative server (IP finale) → Cache tous niveaux (TTL) → Connexion établie. **Types déploiements DNS** : Public resolvers (Google/Cloudflare consommateurs), Authoritative hosting (Cloudflare/AWS Route53/Gandi hébergent zones), Private DNS (entreprises internes Active Directory), Split-horizon (réponses différentes interne/externe), Anycast (IPs identiques serveurs mondiaux = route plus proche). **DNS = infrastructure critique** : utilisé Google search 8.5 milliards requêtes/jour, Amazon e-commerce scaling Black Friday, Netflix CDN routing 200+ millions users, Microsoft 365 email routing, banques transactions sécurisées, gouvernements services citoyens, 99.999% disponibilité requise (5 min downtime/an acceptable max)._

**DNS en résumé :**

- ✅ **Résolution noms** = Domaines → IPs (hiérarchie distribuée)
- ✅ **Types records** = A, MX, TXT, CNAME, NS, SOA, PTR, SRV, CAA, DNSSEC
- ✅ **Serveurs** = Root, TLD, Authoritative, Recursive resolvers
- ✅ **Configuration** = BIND, Unbound, dnsmasq, PowerDNS
- ✅ **Sécurité** = DNSSEC, DoH/DoT, rate limiting, filtering
- ✅ **Performance** = Cache, Anycast, GeoDNS, CDN integration
- ✅ **Production** = High availability, monitoring, troubleshooting
- ✅ **Standards** = RFC 1034/1035, DNSSEC (RFC 4033-4035)

**Guide structure :**

1. Introduction et architecture DNS
2. Types d'enregistrements DNS
3. Résolution DNS (recursive vs iterative)
4. Installation et configuration BIND
5. Zone files et gestion domaines
6. DNS secondaires et réplication
7. DNSSEC (sécurité cryptographique)
8. DNS moderne (DoH, DoT, DoQ)
9. Performance et optimisation
10. Security (attaques et protections)
11. Troubleshooting et monitoring
12. Cas pratiques production

---

## Section 1 : Introduction et Architecture DNS

### 1.1 Qu'est-ce que le DNS ?

**DNS = Domain Name System (Système de Noms de Domaine)**

```
Fonction principale :
Traduire noms de domaine lisibles humains → adresses IP machines

Exemple :
google.com → 142.250.185.78 (IPv4)
google.com → 2a00:1450:4007:80f::200e (IPv6)

Historique :
1983 : RFC 882/883 (Paul Mockapetris, première spec DNS)
1987 : RFC 1034/1035 (standards DNS actuels)
1990s : Explosion Internet, DNS devient critique
2000s : DNSSEC (sécurité), IPv6, Anycast
2010s : DoH/DoT (chiffrement), cloud DNS
2020s : DoQ (QUIC), DNS-over-HTTPS3

Chiffres clés :
- 4.66+ milliards domaines enregistrés (2024)
- 13 root servers (répliqués 1000+ instances mondialement)
- ~3 trillions requêtes DNS/jour
- 99.99%+ uptime infrastructure
```

**Pourquoi DNS est critique ?**

```
Sans DNS fonctionnel :

❌ Sites web inaccessibles (browsers pas résoudre noms)
❌ Email impossible (pas résolution MX servers)
❌ Applications mobiles cassées (APIs inaccessibles)
❌ Streaming bloqué (Netflix/YouTube pas routage CDN)
❌ E-commerce paralysé (Amazon/eBay down)
❌ Services cloud inutilisables (AWS/Azure/GCP)
❌ VoIP/visio impossible (Zoom/Teams/Skype)
❌ IoT devices déconnectés (smart home offline)

Incidents DNS célèbres :

2016 : DDoS Dyn (Twitter, Netflix, Spotify paralysés)
2020 : Google DNS outage (services mondiaux impactés)
2021 : Facebook outage (BGP + DNS = 6h downtime)
2022 : Cloudflare DNS incident (millions sites affectés)

Impact business :
- E-commerce : $100K-1M+/heure perte
- SaaS : Perte clients, réputation
- Banques : Transactions bloquées
- Gouvernements : Services citoyens inaccessibles
```

### 1.2 Architecture Hiérarchique DNS

**Hiérarchie DNS (arbre inversé) :**

```
                     . (Root)
                     |
        ┌────────────┼────────────┐
        |            |            |
       .com         .org         .fr
        |            |            |
    google.com  wikipedia.org  ovh.fr
        |            |            |
    www.google   en.wikipedia  www.ovh
```

**Niveaux hiérarchie :**

```
1. Root (.) :
   - 13 root servers (a.root-servers.net → m.root-servers.net)
   - Répliqués 1000+ instances mondialement (Anycast)
   - Gérés ICANN/IANA
   - Connaissent serveurs TLD (.com, .org, etc.)

2. TLD (Top-Level Domain) :
   - gTLD : .com, .org, .net, .info (generic)
   - ccTLD : .fr, .uk, .de, .jp (country-code)
   - New gTLD : .app, .dev, .blog, .shop
   - Gérés registries (Verisign .com, AFNIC .fr)

3. Second-Level Domain (SLD) :
   - google.com
   - wikipedia.org
   - github.com
   - Enregistrés via registrars (Gandi, OVH, Namecheap)

4. Subdomains :
   - www.google.com
   - mail.google.com
   - api.github.com
   - Gérés par propriétaire domaine

5. FQDN (Fully Qualified Domain Name) :
   - www.google.com. (point final = root)
   - mail.example.com.
   - api.subdomain.example.org.
```

**Serveurs DNS (types) :**

```
1. Root Nameservers :
   - 13 identités (a-m.root-servers.net)
   - 1000+ instances physiques (Anycast)
   - Répondent requêtes TLD

2. TLD Nameservers :
   - Serveurs .com (Verisign)
   - Serveurs .org (PIR)
   - Serveurs .fr (AFNIC)
   - Délèguent vers authoritative

3. Authoritative Nameservers :
   - Serveurs faisant autorité pour zone
   - Hébergés provider DNS (Cloudflare, AWS Route53)
   - Contiennent records A, MX, TXT, etc.
   - Exemple : ns1.google.com pour google.com

4. Recursive Resolvers :
   - Serveurs faisant résolution pour clients
   - Google 8.8.8.8, Cloudflare 1.1.1.1
   - ISP resolvers (Orange, Free, etc.)
   - Cache résultats (TTL)

5. Forwarding Resolvers :
   - Transfèrent requêtes vers autre resolver
   - Utilisés entreprises (forward vers 8.8.8.8)
   - Pas de récursion locale
```

### 1.3 Processus Résolution DNS Complet

**Résolution récursive complète (cold cache) :**

```
Scénario : User tape www.example.com dans browser

┌─────────────────────────────────────────────────────────────┐
│ 1. Browser cache                                            │
│    Cache local browser (Chrome, Firefox)                    │
│    TTL : 60s typique                                        │
│    Si trouvé → Retourne IP (instant)                        │
│    Si pas trouvé → Continue                                 │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. OS cache                                                 │
│    Windows : DNS Client service                             │
│    Linux : systemd-resolved / nscd                          │
│    macOS : mDNSResponder                                    │
│    Si trouvé → Retourne IP                                  │
│    Si pas trouvé → Continue                                 │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Recursive Resolver (8.8.8.8, 1.1.1.1, ISP)              │
│    Cache resolver                                           │
│    Si trouvé → Retourne IP (cached)                         │
│    Si pas trouvé → Commence résolution récursive            │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Root Server (.)                                          │
│    Query : "Où trouver .com ?"                              │
│    Response : "Demandez serveurs .com"                      │
│    Retourne : NS records serveurs TLD .com                  │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. TLD Server (.com)                                        │
│    Query : "Où trouver example.com ?"                       │
│    Response : "Demandez serveurs example.com"               │
│    Retourne : NS records ns1.example.com, ns2.example.com   │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Authoritative Server (ns1.example.com)                   │
│    Query : "Quelle IP pour www.example.com ?"               │
│    Response : "192.0.2.1" (A record)                        │
│    + TTL : 3600 (1 heure)                                   │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Recursive Resolver                                       │
│    Cache résultat (TTL 3600s)                               │
│    Retourne IP au client                                    │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. OS cache                                                 │
│    Cache résultat                                           │
│    Retourne IP au browser                                   │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. Browser                                                  │
│    Cache résultat                                           │
│    Établit connexion HTTP vers 192.0.2.1                    │
└─────────────────────────────────────────────────────────────┘

Temps total :
- Cold cache (première fois) : 50-200ms
- Warm cache (déjà résolu) : <1ms
```

**Résolution itérative (alternative) :**

```
Client fait requêtes itératives lui-même
(Rare, principalement debugging)

Client → Root : "www.example.com ?"
Root → Client : "Demandez .com"

Client → TLD .com : "www.example.com ?"
TLD → Client : "Demandez ns1.example.com"

Client → ns1.example.com : "www.example.com ?"
ns1 → Client : "192.0.2.1"

Plus lent, plus bande passante
Utilisé principalement debugging (dig +trace)
```

---

## Section 2 : Types d'Enregistrements DNS

### 2.1 A Record (IPv4 Address)

```
Format :
<nom>  <TTL>  IN  A  <IPv4>

Exemple :
example.com.      3600  IN  A  192.0.2.1
www.example.com.  3600  IN  A  192.0.2.1

Usage :
- Résolution domaine → IPv4
- Load balancing (multiple A records)
- Failover (secondary IPs)

Multiple A records (round-robin) :
example.com.  300  IN  A  192.0.2.1
example.com.  300  IN  A  192.0.2.2
example.com.  300  IN  A  192.0.2.3

Resolver retourne tous, browser/app choisit aléatoirement
= Load balancing basique

Configuration BIND :
$ORIGIN example.com.
@       IN  A  192.0.2.1
www     IN  A  192.0.2.1
mail    IN  A  192.0.2.10
```

### 2.2 AAAA Record (IPv6 Address)

```
Format :
<nom>  <TTL>  IN  AAAA  <IPv6>

Exemple :
example.com.  3600  IN  AAAA  2001:db8::1

Dual-stack (IPv4 + IPv6) :
example.com.  3600  IN  A     192.0.2.1
example.com.  3600  IN  AAAA  2001:db8::1

Clients IPv6 utilisent AAAA
Clients IPv4 utilisent A
Happy Eyeballs (RFC 8305) : Tente IPv6 + IPv4 parallel

Configuration BIND :
$ORIGIN example.com.
@    IN  A     192.0.2.1
@    IN  AAAA  2001:db8::1
www  IN  AAAA  2001:db8::2
```

### 2.3 MX Record (Mail Exchange)

```
Format :
<nom>  <TTL>  IN  MX  <priorité>  <serveur-mail>

Exemple :
example.com.  3600  IN  MX  10  mail1.example.com.
example.com.  3600  IN  MX  20  mail2.example.com.

Priorité :
- Plus petit nombre = priorité plus haute
- 10 = primary mail server
- 20 = backup mail server
- 30 = fallback

Serveur mail doit avoir A/AAAA record :
mail1.example.com.  IN  A  192.0.2.10
mail2.example.com.  IN  A  192.0.2.11

Configuration BIND :
$ORIGIN example.com.
@  IN  MX  10  mail1.example.com.
@  IN  MX  20  mail2.example.com.

mail1  IN  A  192.0.2.10
mail2  IN  A  192.0.2.11

Email delivery :
1. Resolver MX records example.com
2. Trier par priorité (10 avant 20)
3. Résoudre A record mail1.example.com
4. Connecter SMTP mail1:25
5. Si échec, essayer mail2 (priorité 20)
```

### 2.4 TXT Record (Text Data)

```
Format :
<nom>  <TTL>  IN  TXT  "<texte>"

Usage :
- SPF (Sender Policy Framework - anti-spam)
- DKIM (email authentication)
- DMARC (email policy)
- Domain verification (Google, Microsoft)
- CAA alternative (deprecated)
- Custom metadata

SPF (anti-spam) :
example.com.  IN  TXT  "v=spf1 ip4:192.0.2.0/24 include:_spf.google.com -all"

Syntaxe SPF :
v=spf1          Version
ip4:192.0.2.0/24  IPs autorisées
include:...     Inclure autre domaine
mx              Serveurs MX autorisés
a               A record autorisé
-all            Reject autres (strict)
~all            Softfail autres (permissif)

DKIM (signature cryptographique email) :
default._domainkey.example.com.  IN  TXT  "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBA..."

DMARC (policy email) :
_dmarc.example.com.  IN  TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"

Domain verification Google :
example.com.  IN  TXT  "google-site-verification=abc123..."

Configuration BIND :
$ORIGIN example.com.
@  IN  TXT  "v=spf1 mx -all"
@  IN  TXT  "google-site-verification=..."

_dmarc  IN  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"

default._domainkey  IN  TXT  "v=DKIM1; k=rsa; p=..."
```

### 2.5 CNAME Record (Canonical Name - Alias)

```
Format :
<alias>  <TTL>  IN  CNAME  <cible>

Exemple :
www.example.com.  IN  CNAME  example.com.

Usage :
- Aliaser subdomain vers autre domaine
- CDN configuration
- Simplifier gestion (un seul A à modifier)

Restrictions CNAME :
❌ Pas de CNAME sur apex domain (example.com)
❌ Pas de CNAME + autres records même nom
❌ Pas de CNAME + CNAME (chaînes limitées)

CNAME + CDN :
www.example.com.  IN  CNAME  example.cdn.cloudflare.net.

CNAME chain (pas recommandé) :
www.example.com.  IN  CNAME  cdn.example.com.
cdn.example.com.  IN  CNAME  lb.provider.com.
lb.provider.com.  IN  A      203.0.113.1

Chaque hop = requête DNS supplémentaire = latence

Configuration BIND :
$ORIGIN example.com.
www   IN  CNAME  @
blog  IN  CNAME  hosting.provider.com.
shop  IN  CNAME  example.myshopify.com.

ALIAS/ANAME (non-standard, alternative CNAME apex) :
Cloudflare, AWS Route53 : Permet CNAME-like sur apex
example.com.  IN  ALIAS  lb.cloudflare.com.
```

### 2.6 NS Record (Nameserver)

```
Format :
<zone>  <TTL>  IN  NS  <nameserver>

Exemple :
example.com.  86400  IN  NS  ns1.example.com.
example.com.  86400  IN  NS  ns2.example.com.

Usage :
- Déléguer zone vers nameservers
- Définir serveurs autoritatifs
- Subdomain delegation

Nameservers doivent avoir A/AAAA (glue records) :
ns1.example.com.  IN  A  192.0.2.50
ns2.example.com.  IN  A  192.0.2.51

Subdomain delegation :
sub.example.com.  IN  NS  ns1.sub.example.com.
sub.example.com.  IN  NS  ns2.sub.example.com.

ns1.sub.example.com.  IN  A  203.0.113.1

Configuration BIND (zone file) :
$ORIGIN example.com.
$TTL 86400

@  IN  SOA  ns1.example.com. admin.example.com. (
    2024011601  ; Serial
    3600        ; Refresh
    1800        ; Retry
    604800      ; Expire
    86400 )     ; Minimum TTL

@  IN  NS  ns1.example.com.
@  IN  NS  ns2.example.com.

ns1  IN  A  192.0.2.50
ns2  IN  A  192.0.2.51
```

### 2.7 SOA Record (Start of Authority)

```
Format :
<zone>  IN  SOA  <mname>  <rname>  (
    <serial>
    <refresh>
    <retry>
    <expire>
    <minimum>
)

Exemple :
example.com.  IN  SOA  ns1.example.com. admin.example.com. (
    2024011601  ; Serial (YYYYMMDDnn)
    7200        ; Refresh (2h)
    3600        ; Retry (1h)
    1209600     ; Expire (2 weeks)
    3600 )      ; Minimum TTL (1h)

Champs SOA :

mname (Master Name) :
- Primary nameserver authoritative
- ns1.example.com.

rname (Responsible Name) :
- Email admin (@ remplacé par .)
- admin.example.com. = admin@example.com
- hostmaster.example.com. = convention standard

serial :
- Numéro version zone
- Format : YYYYMMDDnn (2024011601 = 16 Jan 2024, révision 01)
- Incrémenté à chaque modification
- Secondaires comparent serial pour sync

refresh :
- Intervalle secondaires vérifient updates (secondes)
- 7200 = 2h (secondaires check toutes 2h)

retry :
- Si refresh échoue, réessayer après (secondes)
- 3600 = 1h

expire :
- Abandon si primary inaccessible après (secondes)
- 1209600 = 2 semaines
- Après expiration, secondaire stop répondre

minimum (Negative caching TTL) :
- TTL pour réponses négatives (NXDOMAIN)
- 3600 = 1h

Configuration BIND :
$ORIGIN example.com.
$TTL 3600

@  IN  SOA  ns1.example.com. hostmaster.example.com. (
    2024011601  ; Serial
    7200        ; Refresh
    3600        ; Retry
    1209600     ; Expire
    3600 )      ; Minimum

Bonnes pratiques serial :
- Format YYYYMMDDnn permet 99 updates/jour
- Incrémenter à CHAQUE modification
- Si oublié, secondaires pas sync
```

### 2.8 PTR Record (Pointer - Reverse DNS)

```
Format :
<IP-reverse>.in-addr.arpa.  IN  PTR  <nom>

Exemple IPv4 :
1.2.0.192.in-addr.arpa.  IN  PTR  mail.example.com.

Calcul reverse :
IP : 192.0.2.1
Reverse : 1.2.0.192.in-addr.arpa.

Exemple IPv6 :
1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.

Usage :
- Résolution inverse IP → nom
- Validation serveurs mail (anti-spam)
- Logging/audit (IPs lisibles)
- Troubleshooting réseau

Configuration BIND (zone reverse IPv4) :
; Zone file : db.192.0.2
$ORIGIN 2.0.192.in-addr.arpa.
$TTL 3600

@  IN  SOA  ns1.example.com. hostmaster.example.com. (
    2024011601
    7200
    3600
    1209600
    3600 )

@  IN  NS  ns1.example.com.

1   IN  PTR  example.com.
10  IN  PTR  mail.example.com.
50  IN  PTR  ns1.example.com.

named.conf :
zone "2.0.192.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.192.0.2";
};

Email servers vérifient PTR :
Forward : mail.example.com → 192.0.2.10
Reverse : 192.0.2.10 → mail.example.com
Si forward ≠ reverse = email peut être rejeté
```

### 2.9 SRV Record (Service Locator)

```
Format :
_service._proto.name  TTL  IN  SRV  priority  weight  port  target

Exemple :
_sip._tcp.example.com.  IN  SRV  10  60  5060  sipserver.example.com.

Champs SRV :

priority : Priorité (comme MX, plus petit = priorité haute)
weight : Poids load balancing (même priorité)
port : Port service
target : Hostname fournissant service

Usage :
- LDAP : _ldap._tcp.example.com
- SIP : _sip._tcp.example.com
- XMPP/Jabber : _xmpp-client._tcp.example.com
- Minecraft : _minecraft._tcp.example.com
- Microsoft Active Directory : _ldap._tcp.dc._msdcs.example.com

Configuration BIND :
$ORIGIN example.com.

; SIP servers
_sip._tcp  IN  SRV  10  60  5060  sip1.example.com.
_sip._tcp  IN  SRV  10  40  5060  sip2.example.com.
_sip._tcp  IN  SRV  20  100 5060  sipbackup.example.com.

; LDAP
_ldap._tcp  IN  SRV  0  0  389  ldap.example.com.

; Targets A records
sip1        IN  A  192.0.2.20
sip2        IN  A  192.0.2.21
sipbackup   IN  A  192.0.2.22
ldap        IN  A  192.0.2.30

Load balancing SRV :
Priority 10, weight 60 : 60% trafic
Priority 10, weight 40 : 40% trafic
Priority 20 : Backup seulement si 10 down
```

### 2.10 CAA Record (Certification Authority Authorization)

```
Format :
<nom>  IN  CAA  <flags>  <tag>  "<value>"

Exemple :
example.com.  IN  CAA  0  issue  "letsencrypt.org"
example.com.  IN  CAA  0  issuewild  "letsencrypt.org"
example.com.  IN  CAA  0  iodef  "mailto:security@example.com"

Tags CAA :

issue : CA autorisée émettre certificats
issuewild : CA autorisée émettre wildcards (*.example.com)
iodef : Email notification violation

Usage :
- Sécurité PKI (empêcher CAs non-autorisées)
- Prévenir émission frauduleuse certificats
- HTTPS/TLS security

Configuration BIND :
$ORIGIN example.com.

@  IN  CAA  0  issue  "letsencrypt.org"
@  IN  CAA  0  issue  "digicert.com"
@  IN  CAA  0  issuewild  "letsencrypt.org"
@  IN  CAA  0  iodef  "mailto:security@example.com"

Interdire toute émission :
example.com.  IN  CAA  0  issue  ";"

CAs vérifient CAA avant émettre certificat
Si CAA interdit = Émission refusée
```

---

## Section 3 : Résolution DNS

### 3.1 Résolution Récursive

```
Recursive resolver fait TOUT le travail pour client

Client → Resolver : "Quelle IP pour www.example.com ?"
Resolver → Client : "192.0.2.1" (après avoir interrogé root, TLD, authoritative)

Avantages :
✅ Client simple (1 requête)
✅ Cache resolver bénéficie tous clients
✅ Resolver optimise queries

Inconvénients :
❌ Resolver doit être fiable
❌ Charge élevée resolver
❌ Possible bottleneck

Configuration client (Linux /etc/resolv.conf) :
nameserver 8.8.8.8
nameserver 1.1.1.1

Client envoie requête récursive (RD flag=1)
Resolver fait résolution complète
Cache résultat (TTL)
```

### 3.2 Résolution Itérative

```
Client fait queries séquentielles lui-même

Client → Root : "www.example.com ?"
Root → Client : "Demandez .com : a.gtld-servers.net"

Client → a.gtld-servers.net : "www.example.com ?"
TLD → Client : "Demandez ns1.example.com : 192.0.2.50"

Client → 192.0.2.50 : "www.example.com ?"
ns1 → Client : "192.0.2.1"

Avantages :
✅ Contrôle total résolution
✅ Debugging (voir chaque étape)
✅ Pas dépendance resolver tiers

Inconvénients :
❌ Client plus complexe
❌ Plus requêtes réseau
❌ Plus lent

Utilisé principalement debugging :
dig +trace www.example.com

Output :
.                       IN  NS  a.root-servers.net.
com.                    IN  NS  a.gtld-servers.net.
example.com.            IN  NS  ns1.example.com.
www.example.com.        IN  A   192.0.2.1
```

### 3.3 Cache DNS Multi-niveaux

```
Cache hiérarchique (du plus proche au plus loin) :

┌─────────────────────────────────────┐
│ 1. Browser Cache                    │
│    TTL : 60s typique                │
│    Taille : ~100 entries            │
│    Scope : Application seulement    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 2. OS Cache                         │
│    Windows : DNS Client             │
│    Linux : systemd-resolved         │
│    TTL : Respecte DNS TTL           │
│    Taille : ~1000 entries           │
│    Scope : Système entier           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 3. Resolver Cache (8.8.8.8, ISP)   │
│    TTL : Respecte DNS TTL           │
│    Taille : Millions entries        │
│    Scope : Tous clients resolver    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 4. Authoritative (si query)         │
│    Pas de cache (source vérité)     │
└─────────────────────────────────────┘

TTL (Time To Live) contrôle durée cache :

example.com.  300  IN  A  192.0.2.1
              ↑
              TTL 300s = 5 minutes

Après 5 minutes :
- Entry expirée dans cache
- Nouvelle query nécessaire

Flush cache :

Windows :
ipconfig /flushdns

Linux (systemd-resolved) :
sudo systemd-resolve --flush-caches

Linux (nscd) :
sudo service nscd restart

macOS :
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

Browser (Chrome) :

chrome://net-internals/#dns
→ Clear host cache
```

## Section 4 : Installation et Configuration BIND

### 4.1 Installation BIND

**BIND = Berkeley Internet Name Domain (serveur DNS référence)**

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install bind9 bind9-utils bind9-doc

# RHEL/CentOS/Rocky
sudo dnf install bind bind-utils

# Vérifier installation
named -v
# BIND 9.18.12 (Stable Release)

# Services
sudo systemctl status named     # RHEL
sudo systemctl status bind9     # Debian

# Démarrer
sudo systemctl start bind9
sudo systemctl enable bind9

# Fichiers importants
/etc/bind/named.conf              # Configuration principale
/etc/bind/named.conf.options      # Options globales
/etc/bind/named.conf.local        # Zones locales
/etc/bind/zones/                  # Zone files
/var/log/named/                   # Logs
/var/cache/bind/                  # Cache
```

### 4.2 Configuration BIND Basique

**Configuration minimale recursive resolver :**

```bash
# /etc/bind/named.conf.options

options {
    directory "/var/cache/bind";
    
    // Recursive resolver pour réseau local
    recursion yes;
    allow-query { 192.168.1.0/24; localhost; };
    
    // Forwarders (Google DNS)
    forwarders {
        8.8.8.8;
        8.8.4.4;
    };
    forward only;
    
    // DNSSEC validation
    dnssec-validation auto;
    
    // Listen IPv4 + IPv6
    listen-on { any; };
    listen-on-v6 { any; };
    
    // Performance
    max-cache-size 256M;
    max-cache-ttl 86400;  // 24h
    max-ncache-ttl 3600;  // 1h negative cache
};

# Tester configuration
sudo named-checkconf

# Redémarrer
sudo systemctl restart bind9

# Test résolution
dig @localhost google.com
```

**Configuration authoritative nameserver :**

```bash
# /etc/bind/named.conf.options

options {
    directory "/var/cache/bind";
    
    // Authoritative seulement (pas récursion)
    recursion no;
    allow-query { any; };  // Monde entier peut query
    
    // Pas de forwarders (on est l'autorité)
    
    // DNSSEC
    dnssec-validation yes;
    
    // Listen
    listen-on { any; };
    listen-on-v6 { any; };
    
    // Rate limiting (anti-DDoS)
    rate-limit {
        responses-per-second 10;
        window 5;
    };
};

# Zones déclarées dans named.conf.local
```

### 4.3 Sécurité BIND

```bash
# /etc/bind/named.conf.options (sécurité renforcée)

acl "trusted" {
    192.168.1.0/24;
    localhost;
};

acl "slaves" {
    203.0.113.10;  // IP secondary NS
};

options {
    directory "/var/cache/bind";
    
    // Sécurité basique
    version "NOT DISCLOSED";  // Cache version (security through obscurity)
    hostname "NOT DISCLOSED";
    server-id none;
    
    // Restrictions queries
    allow-query { trusted; };
    allow-query-cache { trusted; };
    
    // Désactiver récursion pour externe
    recursion yes;
    allow-recursion { trusted; };
    
    // Zone transfers (AXFR) seulement secondaires
    allow-transfer { slaves; };
    
    // Notifications seulement secondaires
    allow-notify { slaves; };
    also-notify { 203.0.113.10; };
    notify yes;
    
    // Blackhole (bloquer IPs malveillantes)
    blackhole {
        192.0.2.0/24;  // Exemple réseau malveillant
    };
    
    // Rate limiting avancé
    rate-limit {
        responses-per-second 15;
        referrals-per-second 10;
        nodata-per-second 10;
        nxdomains-per-second 10;
        errors-per-second 5;
        
        window 5;
        log-only no;
        
        slip 2;  // 1/2 requêtes reçoivent TC bit (truncated)
    };
    
    // Logging
    logging {
        channel default_log {
            file "/var/log/named/default.log" versions 3 size 5m;
            severity info;
            print-time yes;
            print-severity yes;
            print-category yes;
        };
        
        channel query_log {
            file "/var/log/named/query.log" versions 3 size 10m;
            severity info;
        };
        
        category default { default_log; };
        category queries { query_log; };
        category security { default_log; };
    };
};

# Créer répertoire logs
sudo mkdir -p /var/log/named
sudo chown bind:bind /var/log/named
```

### 4.4 Configuration Avancée

```bash
# /etc/bind/named.conf.options (production)

options {
    directory "/var/cache/bind";
    
    // Performance
    max-cache-size 512M;
    max-cache-ttl 86400;
    max-ncache-ttl 10800;  // 3h negative
    
    // Tuning TCP
    tcp-clients 1000;
    tcp-listen-queue 10;
    
    // Tuning requêtes récursives
    recursive-clients 10000;
    max-clients-per-query 100;
    clients-per-query 20;
    
    // Prefetch (renouveler cache avant expiration)
    prefetch 2 9;  // Renouveler si TTL < 9s et 2s avant expiration
    
    // EDNS (Extension mechanisms for DNS)
    edns-udp-size 4096;
    max-udp-size 4096;
    
    // IPv6
    filter-aaaa-on-v4 no;
    
    // Response Policy Zones (RPZ) - Filtrage malware
    response-policy {
        zone "rpz.malware-domain-list.com";
    };
    
    // Minimal responses (économie bande passante)
    minimal-responses yes;
    
    // Query source
    query-source address * port *;
    query-source-v6 address * port *;
    
    // Transfer format
    transfer-format many-answers;
    
    // Statistiques
    statistics-file "/var/cache/bind/named.stats";
    zone-statistics yes;
};

# RPZ zone (blocage malware)
zone "rpz.malware-domain-list.com" {
    type master;
    file "/etc/bind/zones/db.rpz.malware";
    allow-query { none; };  // RPZ pas queryable directement
};
```

---

## Section 5 : Zone Files et Gestion Domaines

### 5.1 Créer Zone Authoritative

**Structure zone file :**

```bash
# /etc/bind/zones/db.example.com

$ORIGIN example.com.
$TTL 3600

; SOA Record
@   IN  SOA ns1.example.com. hostmaster.example.com. (
    2024011601  ; Serial (YYYYMMDDnn)
    7200        ; Refresh (2h)
    3600        ; Retry (1h)
    1209600     ; Expire (2 weeks)
    3600 )      ; Minimum TTL (1h)

; Nameservers
@   IN  NS  ns1.example.com.
@   IN  NS  ns2.example.com.

; A Records (IPv4)
@       IN  A   192.0.2.1
www     IN  A   192.0.2.1
mail    IN  A   192.0.2.10
ns1     IN  A   192.0.2.50
ns2     IN  A   192.0.2.51

; AAAA Records (IPv6)
@       IN  AAAA  2001:db8::1
www     IN  AAAA  2001:db8::1

; MX Records (Mail)
@   IN  MX  10  mail.example.com.
@   IN  MX  20  mail2.example.com.

mail2   IN  A   192.0.2.11

; CNAME Records (Aliases)
blog    IN  CNAME  www.example.com.
shop    IN  CNAME  www.example.com.
ftp     IN  CNAME  www.example.com.

; TXT Records (SPF, DKIM, etc.)
@   IN  TXT  "v=spf1 mx ip4:192.0.2.0/24 -all"
@   IN  TXT  "google-site-verification=abc123xyz"

_dmarc  IN  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"

default._domainkey  IN  TXT  "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC..."

; SRV Records
_sip._tcp   IN  SRV  10  60  5060  sip.example.com.

sip         IN  A   192.0.2.20

; CAA Records
@   IN  CAA  0  issue  "letsencrypt.org"
@   IN  CAA  0  issuewild  "letsencrypt.org"
@   IN  CAA  0  iodef  "mailto:security@example.com"

; Wildcard (optionnel)
*   IN  A   192.0.2.1
```

**Déclarer zone dans BIND :**

```bash
# /etc/bind/named.conf.local

zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    allow-transfer { 203.0.113.10; };  // Secondary NS IP
    allow-update { none; };
    notify yes;
    also-notify { 203.0.113.10; };
};

# Vérifier zone file
sudo named-checkzone example.com /etc/bind/zones/db.example.com

# Output :
zone example.com/IN: loaded serial 2024011601
OK

# Recharger BIND
sudo rndc reload example.com
# server reload successful
```

### 5.2 Zone Reverse (PTR)

```bash
# /etc/bind/zones/db.192.0.2

$ORIGIN 2.0.192.in-addr.arpa.
$TTL 3600

@   IN  SOA ns1.example.com. hostmaster.example.com. (
    2024011601
    7200
    3600
    1209600
    3600 )

@   IN  NS  ns1.example.com.
@   IN  NS  ns2.example.com.

; PTR Records
1   IN  PTR  example.com.
1   IN  PTR  www.example.com.
10  IN  PTR  mail.example.com.
11  IN  PTR  mail2.example.com.
20  IN  PTR  sip.example.com.
50  IN  PTR  ns1.example.com.
51  IN  PTR  ns2.example.com.

# Déclarer zone reverse
# /etc/bind/named.conf.local

zone "2.0.192.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.192.0.2";
    allow-transfer { 203.0.113.10; };
};

# Vérifier
sudo named-checkzone 2.0.192.in-addr.arpa /etc/bind/zones/db.192.0.2

# Reload
sudo rndc reload 2.0.192.in-addr.arpa

# Test
dig -x 192.0.2.1 @localhost
```

### 5.3 Subdomains et Délégation

```bash
# Subdomain dans même zone (simple)

# /etc/bind/zones/db.example.com
api.example.com.     IN  A   192.0.2.30
app.example.com.     IN  A   192.0.2.31
dev.example.com.     IN  A   192.0.2.32

# Subdomain délégué (zone séparée)

# /etc/bind/zones/db.example.com
; Délégation vers subdomain
sub.example.com.  IN  NS  ns1.sub.example.com.
sub.example.com.  IN  NS  ns2.sub.example.com.

; Glue records (nécessaires car NS dans subdomain)
ns1.sub.example.com.  IN  A  203.0.113.20
ns2.sub.example.com.  IN  A  203.0.113.21

# Zone subdomain (serveur séparé ou même serveur)
# /etc/bind/zones/db.sub.example.com

$ORIGIN sub.example.com.
$TTL 3600

@   IN  SOA ns1.sub.example.com. admin.sub.example.com. (
    2024011601
    7200
    3600
    1209600
    3600 )

@   IN  NS  ns1.sub.example.com.
@   IN  NS  ns2.sub.example.com.

@       IN  A   203.0.113.1
www     IN  A   203.0.113.1
api     IN  A   203.0.113.2

ns1     IN  A   203.0.113.20
ns2     IN  A   203.0.113.21

# /etc/bind/named.conf.local (ajouter zone)
zone "sub.example.com" {
    type master;
    file "/etc/bind/zones/db.sub.example.com";
};
```

### 5.4 Dynamic DNS (DDNS)

```bash
# Générer clé TSIG pour updates sécurisés
tsig-keygen -a hmac-sha256 ddns-key > /etc/bind/keys/ddns.key

# /etc/bind/keys/ddns.key
key "ddns-key" {
    algorithm hmac-sha256;
    secret "base64encodedkey==";
};

# /etc/bind/named.conf.local
include "/etc/bind/keys/ddns.key";

zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    
    // Autoriser updates avec clé TSIG
    allow-update { key ddns-key; };
    
    // Journal pour updates dynamiques
    journal "/var/cache/bind/example.com.jnl";
};

# Permissions fichier zone (writable par bind)
sudo chown bind:bind /etc/bind/zones/db.example.com

# Update DNS via nsupdate
nsupdate -k /etc/bind/keys/ddns.key << EOF
server localhost
zone example.com
update add dynamic.example.com 300 A 192.0.2.100
send
EOF

# Vérifier
dig dynamic.example.com @localhost

# Delete record
nsupdate -k /etc/bind/keys/ddns.key << EOF
server localhost
zone example.com
update delete dynamic.example.com A
send
EOF

# Script update automatique (DHCP, VPN, etc.)
#!/bin/bash
# ddns-update.sh

HOSTNAME="client01.example.com"
IP=$(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

nsupdate -k /etc/bind/keys/ddns.key << EOF
server localhost
zone example.com
update delete $HOSTNAME A
update add $HOSTNAME 300 A $IP
send
EOF
```

---

## Section 6 : DNS Secondaires et Réplication

### 6.1 Configuration Primary (Master)

```bash
# Primary nameserver configuration

# /etc/bind/named.conf.options
acl "slaves" {
    203.0.113.10;  // Secondary NS1 IP
    203.0.113.11;  // Secondary NS2 IP
};

options {
    directory "/var/cache/bind";
    
    allow-transfer { slaves; };
    notify yes;
    also-notify { 
        203.0.113.10;
        203.0.113.11;
    };
};

# /etc/bind/named.conf.local
zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    allow-transfer { slaves; };
    notify yes;
};

# Zone file doit contenir tous NS
# /etc/bind/zones/db.example.com
@   IN  NS  ns1.example.com.  ; Primary
@   IN  NS  ns2.example.com.  ; Secondary
@   IN  NS  ns3.example.com.  ; Secondary

ns1  IN  A  192.0.2.50      ; Primary IP
ns2  IN  A  203.0.113.10    ; Secondary IP
ns3  IN  A  203.0.113.11    ; Secondary IP

# Incrémenter serial à chaque modification
@   IN  SOA ns1.example.com. hostmaster.example.com. (
    2024011602  ; Serial incrémenté
    ...
)

# Reload et notifier secondaires
sudo rndc reload example.com
```

### 6.2 Configuration Secondary (Slave)

```bash
# Secondary nameserver configuration

# /etc/bind/named.conf.options
acl "masters" {
    192.0.2.50;  // Primary NS IP
};

options {
    directory "/var/cache/bind";
    
    allow-transfer { none; };  // Secondary ne transfert pas
    allow-notify { masters; };
};

# /etc/bind/named.conf.local
zone "example.com" {
    type slave;
    file "/var/cache/bind/db.example.com";  // Fichier auto-créé
    masters { 192.0.2.50; };
    
    // Vérifier updates primary toutes les 1h
    max-refresh-time 3600;
    max-retry-time 1800;
};

# Permissions répertoire cache
sudo chown -R bind:bind /var/cache/bind

# Redémarrer
sudo systemctl restart bind9

# Vérifier transfert zone
sudo rndc retransfer example.com

# Logs
sudo tail -f /var/log/syslog | grep named

# Output :
zone example.com/IN: Transfer started.
transfer of 'example.com/IN' from 192.0.2.50#53: connected using 203.0.113.10#58742
zone example.com/IN: transferred serial 2024011602
zone example.com/IN: Transfer completed: 1 messages, 25 records, ...
```

### 6.3 Zone Transfer (AXFR/IXFR)

```bash
# AXFR (Full zone transfer)
# Transfert complet de la zone

# Depuis secondary, forcer AXFR
dig @192.0.2.50 example.com AXFR

# Output :
example.com.  3600  IN  SOA  ns1.example.com. ...
example.com.  3600  IN  NS   ns1.example.com.
example.com.  3600  IN  NS   ns2.example.com.
example.com.  3600  IN  A    192.0.2.1
www.example.com.  3600  IN  A  192.0.2.1
...

# IXFR (Incremental zone transfer)
# Transfert incrémental (seulement changements)

# Activer IXFR (default BIND 9+)
# /etc/bind/named.conf.local
zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    ixfr-from-differences yes;  // Enable IXFR
};

# Secondary reçoit seulement différences entre serials
# Plus efficace pour grandes zones

# Sécuriser zone transfers (TSIG)
# Primary : /etc/bind/keys/xfer.key
key "xfer-key" {
    algorithm hmac-sha256;
    secret "transfersecretkey==";
};

# Primary : /etc/bind/named.conf.local
zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    allow-transfer { key xfer-key; };
};

# Secondary : /etc/bind/named.conf.local
include "/etc/bind/keys/xfer.key";

zone "example.com" {
    type slave;
    file "/var/cache/bind/db.example.com";
    masters { 192.0.2.50 key xfer-key; };
};
```

### 6.4 Monitoring Réplication

```bash
# Script vérification sync secondaires
#!/bin/bash
# check-dns-sync.sh

PRIMARY_NS="192.0.2.50"
SECONDARY_NS=("203.0.113.10" "203.0.113.11")
ZONE="example.com"

# Get primary serial
PRIMARY_SERIAL=$(dig @$PRIMARY_NS $ZONE SOA +short | awk '{print $3}')

echo "Primary NS ($PRIMARY_NS) serial: $PRIMARY_SERIAL"
echo ""

for ns in "${SECONDARY_NS[@]}"; do
    SERIAL=$(dig @$ns $ZONE SOA +short | awk '{print $3}')
    
    if [ "$SERIAL" == "$PRIMARY_SERIAL" ]; then
        echo "✓ Secondary $ns: IN SYNC (serial $SERIAL)"
    else
        echo "✗ Secondary $ns: OUT OF SYNC (serial $SERIAL, expected $PRIMARY_SERIAL)"
    fi
done

# Cron job quotidien
# 0 */6 * * * /usr/local/bin/check-dns-sync.sh | mail -s "DNS Sync Report" admin@example.com
```

---

## Section 7 : DNSSEC (Sécurité Cryptographique)

### 7.1 Concepts DNSSEC

```
DNSSEC = DNS Security Extensions (RFC 4033-4035)

Problème DNS classique :
❌ Pas d'authentification réponses
❌ Vulnérable cache poisoning
❌ Man-in-the-Middle attacks possible

DNSSEC ajoute :
✅ Signatures cryptographiques records
✅ Chaîne de confiance (root → TLD → domaine)
✅ Validation intégrité réponses

Nouveaux types records DNSSEC :

RRSIG : Signature cryptographique record set
DNSKEY : Clé publique zone
DS : Delegation Signer (hash clé, dans parent)
NSEC/NSEC3 : Proof of non-existence

Clés DNSSEC :

ZSK (Zone Signing Key) :
- Signe records DNS zone
- Rotation fréquente (mensuelle/trimestrielle)
- Taille : 1024-2048 bits

KSK (Key Signing Key) :
- Signe DNSKEY records
- Rotation rare (annuelle/bi-annuelle)
- Taille : 2048-4096 bits
- Hash publié dans DS record chez parent

Processus validation :

1. Resolver demande example.com A
2. Reçoit réponse + RRSIG signature
3. Obtient DNSKEY example.com
4. Vérifie signature RRSIG avec DNSKEY
5. Valide DNSKEY via DS record parent (.com)
6. Remonte chaîne jusqu'à root (trust anchor)
```

### 7.2 Activer DNSSEC Zone

```bash
# Générer clés DNSSEC

cd /etc/bind/keys

# KSK (Key Signing Key)
dnssec-keygen -a RSASHA256 -b 2048 -f KSK example.com

# Output :
# Kexample.com.+008+12345.key
# Kexample.com.+008+12345.private

# ZSK (Zone Signing Key)
dnssec-keygen -a RSASHA256 -b 1024 example.com

# Output :
# Kexample.com.+008+67890.key
# Kexample.com.+008+67890.private

# Inclure clés dans zone
# /etc/bind/zones/db.example.com
$INCLUDE /etc/bind/keys/Kexample.com.+008+12345.key  ; KSK
$INCLUDE /etc/bind/keys/Kexample.com.+008+67890.key  ; ZSK

# Signer zone
dnssec-signzone -o example.com \
    -k /etc/bind/keys/Kexample.com.+008+12345 \
    /etc/bind/zones/db.example.com \
    /etc/bind/keys/Kexample.com.+008+67890

# Output :
# db.example.com.signed

# Fichier signé contient :
# - Records originaux
# - RRSIG signatures
# - DNSKEY records
# - NSEC/NSEC3 records

# Pointer BIND vers zone signée
# /etc/bind/named.conf.local
zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com.signed";  // Zone signée
    allow-transfer { slaves; };
    notify yes;
};

# Reload
sudo rndc reload example.com

# Récupérer DS record pour parent
dnssec-dsfromkey /etc/bind/keys/Kexample.com.+008+12345.key

# Output :
example.com. IN DS 12345 8 2 abc123def456...

# Soumettre DS record au registrar (.com)
# Via interface registrar (Gandi, OVH, etc.)
```

### 7.3 Auto-signing (BIND 9.9+)

```bash
# Configuration auto-signing (plus simple)

# /etc/bind/named.conf.local
zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    
    // Auto-signing
    auto-dnssec maintain;
    inline-signing yes;
    
    // Key directory
    key-directory "/etc/bind/keys";
};

# Générer clés avec metadata
cd /etc/bind/keys

# KSK
dnssec-keygen -a RSASHA256 -b 2048 -f KSK \
    -L 3600 \
    example.com

# ZSK
dnssec-keygen -a RSASHA256 -b 1024 \
    -L 3600 \
    example.com

# Reload (BIND signe automatiquement)
sudo rndc reload example.com

# BIND crée fichier .signed automatiquement
# /var/cache/bind/db.example.com.signed

# Rotation automatique clés
# /etc/bind/named.conf.options
options {
    dnssec-enable yes;
    dnssec-validation yes;
    dnssec-lookaside auto;
    
    // Policies rotation
    dnssec-policy default {
        keys {
            ksk lifetime unlimited algorithm rsasha256;
            zsk lifetime 30d algorithm rsasha256;
        };
    };
};
```

### 7.4 Validation DNSSEC Resolver

```bash
# Activer validation DNSSEC resolver

# /etc/bind/named.conf.options
options {
    directory "/var/cache/bind";
    
    dnssec-enable yes;
    dnssec-validation yes;
    
    // Trust anchor (root key)
    managed-keys-directory "/var/cache/bind/dynamic";
    
    // Ou manuellement
    // trust-anchors {
    //     . static-key 257 3 8 "AwEAAaz/tAm8yTn4Mf...";
    // };
};

# Trust anchor root automatique (recommended)
sudo rndc managed-keys sync

# Test validation
dig @localhost example.com +dnssec

# Output :
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2
                     ↑
                     ad = Authentic Data (DNSSEC validé)

example.com.  3600  IN  A  192.0.2.1
example.com.  3600  IN  RRSIG  A 8 2 3600 ...

# Tester domaine non-signé
dig @localhost google.com +dnssec
# Pas de flag 'ad' = Pas DNSSEC

# Tester domaine signature invalide (détection attaque)
# Resolver retourne SERVFAIL
```

---

## Section 8 : DNS Moderne (DoH, DoT, DoQ)

### 8.1 DNS-over-TLS (DoT)

```
DoT = DNS over TLS (RFC 7858, port 853)

Avantages :
✅ Chiffrement requêtes DNS
✅ Confidentialité (ISP pas voir queries)
✅ Intégrité (pas MITM)
✅ Authentication serveur (certificat TLS)

Configuration DoT avec BIND :

# /etc/bind/named.conf.options
tls local-tls {
    cert-file "/etc/bind/tls/server.crt";
    key-file "/etc/bind/tls/server.key";
    dhparam-file "/etc/bind/tls/dhparam.pem";
};

options {
    // Listen DoT port 853
    listen-on port 853 tls local-tls { any; };
    listen-on-v6 port 853 tls local-tls { any; };
    
    // Standard DNS port 53 aussi
    listen-on port 53 { any; };
};

# Générer certificat Let's Encrypt
sudo certbot certonly --standalone -d ns1.example.com

sudo ln -s /etc/letsencrypt/live/ns1.example.com/fullchain.pem /etc/bind/tls/server.crt
sudo ln -s /etc/letsencrypt/live/ns1.example.com/privkey.pem /etc/bind/tls/server.key

# Générer dhparam
sudo openssl dhparam -out /etc/bind/tls/dhparam.pem 2048

# Permissions
sudo chown -R bind:bind /etc/bind/tls

# Test DoT
kdig @ns1.example.com +tls google.com
```

**Alternative : Unbound avec DoT**

```bash
# Installer Unbound
sudo apt install unbound

# /etc/unbound/unbound.conf.d/dot.conf
server:
    interface: 0.0.0.0@853
    interface: ::0@853
    
    tls-service-key: "/etc/unbound/tls/server.key"
    tls-service-pem: "/etc/unbound/tls/server.crt"
    
    access-control: 0.0.0.0/0 allow
    
    # Forward vers DoT upstreams
    forward-zone:
        name: "."
        forward-tls-upstream: yes
        forward-addr: 1.1.1.1@853  # Cloudflare DoT
        forward-addr: 8.8.8.8@853  # Google DoT
```

### 8.2 DNS-over-HTTPS (DoH)

```
DoH = DNS over HTTPS (RFC 8484, port 443)

Avantages :
✅ Indistinguable trafic HTTPS normal
✅ Traverse firewalls bloquant DoT (853)
✅ Même bénéfices confidentialité

DoH avec dnsdist (proxy DNS)

# Installer dnsdist
sudo apt install dnsdist

# /etc/dnsdist/dnsdist.conf

-- Listen DoH
addDOHLocal('0.0.0.0:443', '/etc/dnsdist/tls/server.crt', '/etc/dnsdist/tls/server.key', '/')

-- Backend DNS servers
newServer({address='127.0.0.1:53', name='local-bind'})

-- DoH settings
setMaxTCPClientThreads(1000)
setMaxTCPQueuedConnections(1000)

-- ACLs
addACL('0.0.0.0/0')

# Redémarrer
sudo systemctl restart dnsdist

# Test DoH
curl -H 'accept: application/dns-json' \
  'https://ns1.example.com/dns-query?name=example.com&type=A'

# Output JSON :
{
  "Status": 0,
  "TC": false,
  "RD": true,
  "RA": true,
  "AD": true,
  "CD": false,
  "Question": [{"name": "example.com", "type": 1}],
  "Answer": [{"name": "example.com", "type": 1, "TTL": 3600, "data": "192.0.2.1"}]
}
```

**Client DoH (Browser/OS)**

```bash
# Firefox DoH
about:preferences#general
→ Network Settings
→ Enable DNS over HTTPS
→ Use Custom: https://ns1.example.com/dns-query

# Chrome/Edge DoH
chrome://settings/security
→ Use secure DNS
→ Custom: https://ns1.example.com/dns-query

# systemd-resolved DoH (Linux)
# /etc/systemd/resolved.conf
[Resolve]
DNS=127.0.0.1
DNSOverTLS=yes
Domains=~.

# Avec cloudflared proxy
sudo apt install cloudflared

# /etc/cloudflared/config.yml
proxy-dns: true
proxy-dns-port: 5053
proxy-dns-upstream:
  - https://1.1.1.1/dns-query
  - https://8.8.8.8/dns-query

sudo systemctl enable cloudflared
sudo systemctl start cloudflared

# Pointer resolver vers cloudflared
# /etc/resolv.conf
nameserver 127.0.0.1
```

### 8.3 DNS-over-QUIC (DoQ)

```
DoQ = DNS over QUIC (RFC 9250, port 853)

Avantages sur DoT :
✅ Connexions plus rapides (0-RTT)
✅ Multiplexing sans head-of-line blocking
✅ Migration connexion (IP change)

Supporté par :
- AdGuard DNS
- NextDNS
- Cloudflare (expérimental)

Configuration expérimentale dnsdist :

# dnsdist 1.8+ required
addDOQLocal('0.0.0.0:8853', '/etc/dnsdist/tls/server.crt', '/etc/dnsdist/tls/server.key')

# Test avec q (quic client)
q ns1.example.com example.com A
```

---

## Section 9 : Performance et Optimisation

### 9.1 Cache Optimization

```bash
# /etc/bind/named.conf.options

options {
    // Cache sizing (adapter mémoire serveur)
    max-cache-size 1024M;  // 1GB cache
    
    // TTL caching
    max-cache-ttl 604800;    // 1 semaine max
    max-ncache-ttl 10800;    // 3h negative cache
    
    // Prefetch (renouveler avant expiration)
    prefetch 2 9;
    // Renouveler si TTL < 9s et query dans 2s dernières
    
    // Serve stale (servir cache expiré si authoritative down)
    stale-answer-enable yes;
    stale-answer-ttl 3600;  // Servir cache expiré jusqu'à 1h
    max-stale-ttl 86400;    // 24h max
    
    // RRset ordering (performance load balancing)
    rrset-order {
        class IN type A name "*.example.com" order cyclic;
    };
};

# Statistiques cache
sudo rndc stats
sudo cat /var/cache/bind/named.stats

# Output :
+++ Statistics Dump +++ (1705420800)
++ Incoming Requests ++
                1234 QUERY
++ Incoming Queries ++
                 890 A
                 234 AAAA
                  78 MX
                  32 TXT
++ Name Server Statistics ++
           123456 IPv4 requests received
            98765 queries resulted in successful answer
            12345 queries resulted in NXDOMAIN
             5678 queries caused recursion
++ Cache Statistics ++
            45678 cache hits
             8901 cache misses
```

### 9.2 Performance Tuning

```bash
# /etc/bind/named.conf.options

options {
    // TCP tuning
    tcp-clients 1000;          // Max TCP connexions simultanées
    tcp-listen-queue 10;       // Backlog queue
    reserved-sockets 512;      // Sockets réservés
    
    // Recursive tuning
    recursive-clients 10000;   // Max clients récursifs simultanés
    max-clients-per-query 100; // Max clients même query
    clients-per-query 20;      // Clients default même query
    
    // Fetches limits
    fetches-per-zone 10;       // Queries simultanées par zone
    fetches-per-server 4;      // Queries simultanées par serveur
    
    // EDNS buffer
    edns-udp-size 4096;
    max-udp-size 4096;
    
    // Resolver timeout
    resolver-query-timeout 10000;  // 10s
    
    // Response compression
    minimal-responses yes;     // Économie bande passante
    
    // Query minimization (privacy + performance)
    qname-minimization relaxed;
};

# Kernel tuning (Linux)
# /etc/sysctl.d/99-dns-performance.conf

# Network buffers
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.rmem_default = 262144
net.core.wmem_default = 262144

# TCP
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_max_syn_backlog = 8192

# UDP
net.ipv4.udp_rmem_min = 8192
net.ipv4.udp_wmem_min = 8192

# Connection tracking
net.netfilter.nf_conntrack_max = 262144

# Appliquer
sudo sysctl -p /etc/sysctl.d/99-dns-performance.conf
```

### 9.3 Anycast DNS

```
Anycast = Même IP annoncée depuis multiple localisations

Avantages :
✅ Latence réduite (serveur le plus proche)
✅ Load balancing géographique
✅ DDoS mitigation (dilution attaque)
✅ High availability automatique

Architecture Anycast :

        ┌──────────────────────────────────┐
        │    Anycast IP: 203.0.113.1      │
        └──────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    [Europe]        [US East]      [Asia]
    London          New York       Tokyo
    203.0.113.1     203.0.113.1   203.0.113.1
    
Client Europe → Route vers London (plus proche)
Client US → Route vers New York
Client Asia → Route vers Tokyo

Implémentation Anycast :

Chaque datacenter :
1. Serveur DNS même config
2. Annonce IP Anycast via BGP
3. Router Internet route vers le plus proche

Configuration BGP (avec BIRD) :

# /etc/bird/bird.conf
router id 203.0.113.1;

protocol static {
    route 203.0.113.1/32 via "lo";  // Anycast IP loopback
}

protocol bgp upstream {
    local as 65001;
    neighbor 198.51.100.1 as 174;  // Upstream AS
    export where proto = "static";
}

# Interface loopback
ip addr add 203.0.113.1/32 dev lo

# BIND écoute Anycast IP
# /etc/bind/named.conf.options
options {
    listen-on { 203.0.113.1; };
};
```

### 9.4 GeoDNS (Geo-routing)

```bash
# GeoDNS = Réponses différentes selon géolocalisation client

# Avec GeoIP2 module BIND

# Installer GeoIP2
sudo apt install libmaxminddb0 libmaxminddb-dev

# Télécharger base GeoIP2
sudo mkdir -p /usr/share/GeoIP
cd /usr/share/GeoIP
sudo wget https://download.maxmind.com/app/geoip_download?...

# /etc/bind/named.conf.options
geoip {
    directory "/usr/share/GeoIP";
};

options {
    // Enable GeoIP
    geoip-directory "/usr/share/GeoIP";
};

# /etc/bind/named.conf.local
acl "us-clients" {
    geoip country US;
};

acl "eu-clients" {
    geoip country GB;
    geoip country FR;
    geoip country DE;
};

acl "asia-clients" {
    geoip country JP;
    geoip country CN;
    geoip country SG;
};

# Views (vues différentes par région)
view "us-view" {
    match-clients { us-clients; };
    
    zone "example.com" {
        type master;
        file "/etc/bind/zones/db.example.com.us";
    };
};

view "eu-view" {
    match-clients { eu-clients; };
    
    zone "example.com" {
        type master;
        file "/etc/bind/zones/db.example.com.eu";
    };
};

view "asia-view" {
    match-clients { asia-clients; };
    
    zone "example.com" {
        type master;
        file "/etc/bind/zones/db.example.com.asia";
    };
};

# Zone US (serveurs US)
# /etc/bind/zones/db.example.com.us
www  IN  A  192.0.2.1   ; US East server
cdn  IN  A  192.0.2.10  ; US CDN node

# Zone EU (serveurs EU)
# /etc/bind/zones/db.example.com.eu
www  IN  A  203.0.113.1   ; EU server
cdn  IN  A  203.0.113.10  ; EU CDN node

# Zone Asia (serveurs Asia)
# /etc/bind/zones/db.example.com.asia
www  IN  A  198.51.100.1   ; Asia server
cdn  IN  A  198.51.100.10  ; Asia CDN node

# Client US query www.example.com → 192.0.2.1 (US)
# Client EU query www.example.com → 203.0.113.1 (EU)
# Client Asia query www.example.com → 198.51.100.1 (Asia)
```

## Section 10 : Security (Attaques et Protections)

### 10.1 Attaques DNS Courantes

**DNS Amplification (DDoS) :**

```
Principe :
1. Attaquant envoie requête DNS avec IP source spoofée (victime)
2. Serveur DNS répond à victime
3. Réponse >> requête (amplification x50-100)
4. Victime submergée trafic

Exemple :
Requête : 60 bytes (ANY record)
Réponse : 3000 bytes (tous records zone)
Amplification : 50x

Protection BIND :

# /etc/bind/named.conf.options
options {
    // Rate limiting (limite requêtes/IP)
    rate-limit {
        responses-per-second 10;
        referrals-per-second 5;
        nodata-per-second 5;
        nxdomains-per-second 5;
        errors-per-second 5;
        
        window 5;
        log-only no;
        
        // Slip : 1/2 requêtes reçoivent TC (truncated)
        // Force client utiliser TCP (plus coûteux attaquant)
        slip 2;
        
        // Exemptions (clients légitimes)
        exempt-clients { 
            192.168.1.0/24;
            localhost;
        };
    };
    
    // Désactiver ANY queries (deprecated anyway)
    minimal-any yes;
    
    // Désactiver récursion pour public
    recursion no;  // Authoritative only
    
    // Ou limiter récursion
    allow-recursion { 
        192.168.1.0/24;
        localhost;
    };
    
    // Response Rate Limiting (RRL)
    rate-limit {
        responses-per-second 15;
        window 5;
    };
};
```

**DNS Cache Poisoning (Kaminsky Attack) :**

```
Principe :
1. Attaquant demande résolution random.example.com
2. Race condition : attaquant envoie fausses réponses
3. Si réponse malveillante arrive avant légitime
4. Cache empoisonné : example.com → IP attaquant

Protection :

# Source port randomization (default BIND)
options {
    // BIND randomise ports source
    use-v4-udp-ports { range 1024 65535; };
    use-v6-udp-ports { range 1024 65535; };
    
    // Avoid predictable query IDs
    // BIND utilise random query IDs
};

# DNSSEC (protection ultime)
options {
    dnssec-validation yes;
};

# Si DNSSEC validé :
# - Signature cryptographique vérifiée
# - Cache poisoning impossible
```

**DNS Tunneling (Exfiltration Data) :**

```
Principe :
Utiliser requêtes DNS pour exfiltrer données

Exemple :
base64data1.malware.com
base64data2.malware.com
...

Détection :

# Logs suspicious patterns
logging {
    channel query_log {
        file "/var/log/named/query.log" versions 10 size 50m;
        severity info;
        print-time yes;
    };
    
    category queries { query_log; };
};

# Analyser logs
sudo grep -E ".{50,}\.malware\.com" /var/log/named/query.log

# Rate limiting par domaine
# Si 1000+ queries/min vers même domaine = suspect

# Response Policy Zones (RPZ) - Bloquer domaines malveillants
zone "rpz.malware-block.local" {
    type master;
    file "/etc/bind/zones/db.rpz.malware";
    allow-query { none; };
};

# /etc/bind/zones/db.rpz.malware
$TTL 60
@   IN  SOA localhost. root.localhost. (
    1 3h 1h 1w 1h
)
    NS  localhost.

; Bloquer domaine malware
malware.com  CNAME  .
*.malware.com  CNAME  .

; CNAME . = NXDOMAIN (domaine bloqué)
```

### 10.2 Hardening DNS Server

```bash
# Checklist sécurité DNS production

# 1. Séparer Authoritative et Recursive
# Server 1 : Authoritative only
options {
    recursion no;
    allow-query { any; };  // Public queries OK
};

# Server 2 : Recursive only
options {
    recursion yes;
    allow-query { 192.168.0.0/16; };  // Internal only
};

# 2. Limiter zone transfers (AXFR)
acl "slaves" {
    203.0.113.10;
    203.0.113.11;
};

zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    allow-transfer { slaves; };  // Seulement secondaires
};

# 3. TSIG authentication transfers
key "xfer-key" {
    algorithm hmac-sha256;
    secret "base64secret==";
};

zone "example.com" {
    allow-transfer { key xfer-key; };
};

# 4. Masquer version BIND
options {
    version "NOT DISCLOSED";
    hostname "NOT DISCLOSED";
    server-id none;
};

# 5. Chroot BIND (isolation)
# Debian : package bind9-chroot
sudo apt install bind9-chroot

# 6. Firewall rules
sudo ufw allow from 192.168.0.0/16 to any port 53
sudo ufw allow from 203.0.113.10 to any port 53  # Secondary
sudo ufw deny 53  # Deny other

# iptables rate limiting
sudo iptables -A INPUT -p udp --dport 53 -m limit --limit 50/s --limit-burst 100 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 53 -j DROP

# 7. Monitoring et alerting
# /etc/bind/named.conf.options
logging {
    channel security_log {
        file "/var/log/named/security.log" versions 5 size 10m;
        severity warning;
        print-time yes;
        print-severity yes;
        print-category yes;
    };
    
    category security { security_log; };
    category queries { security_log; };
};

# 8. Updates sécurisés (Dynamic DNS)
zone "example.com" {
    allow-update { key ddns-key; };  // Jamais 'any'
};

# 9. Blackhole malicious IPs
options {
    blackhole {
        192.0.2.0/24;  // Known malicious network
    };
};

# 10. DNSSEC activation
options {
    dnssec-enable yes;
    dnssec-validation yes;
};
```

### 10.3 DDoS Mitigation

```bash
# Protection DDoS multi-couches

# Couche 1 : Kernel (sysctl)
# /etc/sysctl.d/99-dns-ddos.conf

# SYN flood protection
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_synack_retries = 2

# IP spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# ICMP flood protection
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Connection tracking
net.netfilter.nf_conntrack_max = 1000000

# Couche 2 : iptables
#!/bin/bash
# dns-ddos-rules.sh

# DNS UDP rate limiting per IP
iptables -A INPUT -p udp --dport 53 -m state --state NEW -m recent --set --name DNS
iptables -A INPUT -p udp --dport 53 -m state --state NEW -m recent --update --seconds 1 --hitcount 30 --name DNS -j DROP

# DNS TCP rate limiting
iptables -A INPUT -p tcp --dport 53 -m state --state NEW -m limit --limit 10/s --limit-burst 20 -j ACCEPT
iptables -A INPUT -p tcp --dport 53 -m state --state NEW -j DROP

# Block DNS ANY queries (amplification)
iptables -A INPUT -p udp --dport 53 -m string --hex-string "|00 00 FF 00|" --algo bm -j DROP

# Couche 3 : BIND RRL
options {
    rate-limit {
        responses-per-second 15;
        referrals-per-second 10;
        nodata-per-second 10;
        nxdomains-per-second 10;
        errors-per-second 5;
        
        all-per-second 25;  // Global limit
        
        window 5;
        log-only no;
        
        slip 2;  // TC bit (force TCP)
        
        ipv4-prefix-length 24;  // /24 subnet tracking
        ipv6-prefix-length 56;
        
        qps-scale 250;  // Scale with query load
        
        max-table-size 20000;
    };
};

# Couche 4 : Anycast (dilution géographique)
# Multiples serveurs même IP
# Attaque diluée sur plusieurs nodes

# Couche 5 : Cloud DDoS protection
# Cloudflare, AWS Shield, Akamai
# Scrubbing centers (nettoyage trafic)

# Monitoring DDoS
#!/bin/bash
# ddos-monitor.sh

THRESHOLD=10000  # Queries/sec

while true; do
    QPS=$(sudo rndc status | grep "queries received" | awk '{print $1}')
    
    if [ $QPS -gt $THRESHOLD ]; then
        echo "ALERT: DDoS detected - $QPS qps"
        # Send alert
        echo "DDoS attack: $QPS qps on $(hostname)" | \
            mail -s "DNS DDoS ALERT" admin@example.com
    fi
    
    sleep 10
done
```

---

## Section 11 : Troubleshooting et Monitoring

### 11.1 Diagnostic DNS Complet

```bash
# Script diagnostic complet DNS
#!/bin/bash
# dns-diagnostic.sh <domain>

DOMAIN="$1"

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <domain>"
    exit 1
fi

echo "=== DNS Diagnostic: $DOMAIN ==="
echo ""

# 1. Résolution basique
echo "1. Basic Resolution:"
dig +short $DOMAIN
echo ""

# 2. Nameservers
echo "2. Nameservers:"
dig +short NS $DOMAIN
echo ""

# 3. SOA (Serial check)
echo "3. SOA Record:"
dig +short SOA $DOMAIN
echo ""

# 4. MX Records
echo "4. Mail Servers:"
dig +short MX $DOMAIN
echo ""

# 5. TXT Records (SPF, DKIM, DMARC)
echo "5. TXT Records:"
echo "SPF:"
dig +short TXT $DOMAIN | grep "v=spf1"
echo "DMARC:"
dig +short TXT _dmarc.$DOMAIN
echo ""

# 6. Résolution complète (trace)
echo "6. Full Resolution Trace:"
dig +trace $DOMAIN | tail -20
echo ""

# 7. DNSSEC validation
echo "7. DNSSEC Status:"
if dig +dnssec $DOMAIN | grep -q "ad"; then
    echo "✓ DNSSEC validated"
else
    echo "✗ DNSSEC not validated"
fi
echo ""

# 8. Vérifier tous nameservers sync
echo "8. Nameserver Sync Check:"
NS_LIST=$(dig +short NS $DOMAIN)
EXPECTED_SERIAL=$(dig +short SOA $DOMAIN | awk '{print $3}')

for ns in $NS_LIST; do
    NS_IP=$(dig +short $ns | head -1)
    SERIAL=$(dig @$NS_IP +short SOA $DOMAIN | awk '{print $3}')
    
    if [ "$SERIAL" == "$EXPECTED_SERIAL" ]; then
        echo "✓ $ns ($NS_IP): IN SYNC (serial $SERIAL)"
    else
        echo "✗ $ns ($NS_IP): OUT OF SYNC (serial $SERIAL, expected $EXPECTED_SERIAL)"
    fi
done
echo ""

# 9. Reverse DNS (si IP fournie)
IP=$(dig +short $DOMAIN | head -1)
if [[ $IP =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "9. Reverse DNS ($IP):"
    dig -x $IP +short
else
    echo "9. Reverse DNS: N/A (not IPv4)"
fi
echo ""

# 10. Performance test
echo "10. Query Performance:"
time dig $DOMAIN > /dev/null
echo ""

# 11. Propagation check (multiple resolvers)
echo "11. Propagation Check:"
for resolver in 8.8.8.8 1.1.1.1 9.9.9.9; do
    RESULT=$(dig @$resolver +short $DOMAIN | head -1)
    echo "$resolver: $RESULT"
done
```

### 11.2 Outils Troubleshooting

```bash
# dig (Domain Information Groper)

# Query basique
dig example.com

# Query type spécifique
dig example.com MX
dig example.com TXT
dig example.com AAAA

# Serveur spécifique
dig @8.8.8.8 example.com

# Short output (IP seulement)
dig +short example.com

# Trace complet (résolution itérative)
dig +trace example.com

# DNSSEC
dig +dnssec example.com

# Reverse DNS
dig -x 192.0.2.1

# Multiple queries
dig example.com A example.com MX

# TCP (au lieu UDP)
dig +tcp example.com

# Statistiques détaillées
dig +stats example.com

# host (simple lookup)

# Résolution simple
host example.com

# Type spécifique
host -t MX example.com
host -t TXT example.com

# Reverse
host 192.0.2.1

# Verbose
host -v example.com

# nslookup (interactive)

# Mode interactif
nslookup
> set type=MX
> example.com
> exit

# Non-interactif
nslookup example.com
nslookup -type=MX example.com

# drill (DNSSEC-aware dig alternative)

# Query basique
drill example.com

# Trace DNSSEC
drill -TD example.com

# Verify DNSSEC chain
drill -S example.com

# whois (domain registration info)

# Domain info
whois example.com

# IP ownership
whois 192.0.2.1

# named-checkzone (validate zone files)

# Check syntax
named-checkzone example.com /etc/bind/zones/db.example.com

# Check serial increment
named-checkzone -D example.com /etc/bind/zones/db.example.com

# named-checkconf (validate config)

# Check named.conf
named-checkconf

# Check specific file
named-checkconf /etc/bind/named.conf.local

# rndc (BIND remote control)

# Reload config
rndc reload

# Reload zone
rndc reload example.com

# Statistics
rndc stats
cat /var/cache/bind/named.stats

# Flush cache
rndc flush

# Dump cache
rndc dumpdb -cache
cat /var/cache/bind/named_dump.db

# Status
rndc status

# Retransfer zone (secondary)
rndc retransfer example.com
```

### 11.3 Monitoring Production

```bash
# Script monitoring DNS complet
#!/bin/bash
# dns-monitor.sh

LOG_FILE="/var/log/dns-monitor.log"
ALERT_EMAIL="admin@example.com"

# Zones à monitorer
ZONES=("example.com" "example.org")

# Nameservers à monitorer
NAMESERVERS=("192.0.2.50" "203.0.113.10")

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a $LOG_FILE
}

send_alert() {
    local subject="$1"
    local message="$2"
    echo "$message" | mail -s "[DNS] $subject" $ALERT_EMAIL
    log "ALERT: $subject"
}

# 1. Check nameserver availability
check_nameserver_up() {
    local ns=$1
    
    if ! dig @$ns . NS +time=2 +tries=1 > /dev/null 2>&1; then
        send_alert "Nameserver Down" "Nameserver $ns not responding"
        return 1
    fi
    
    return 0
}

# 2. Check zone serial sync
check_zone_sync() {
    local zone=$1
    
    # Get expected serial from primary
    local primary_serial=$(dig @${NAMESERVERS[0]} $zone SOA +short | awk '{print $3}')
    
    for ns in "${NAMESERVERS[@]:1}"; do
        local ns_serial=$(dig @$ns $zone SOA +short | awk '{print $3}')
        
        if [ "$ns_serial" != "$primary_serial" ]; then
            send_alert "Zone Out of Sync" \
                "Zone $zone on $ns out of sync (serial $ns_serial, expected $primary_serial)"
        fi
    done
}

# 3. Check query performance
check_query_performance() {
    local ns=$1
    local zone=$2
    
    local query_time=$(dig @$ns $zone +stats | grep "Query time:" | awk '{print $4}')
    
    if [ $query_time -gt 100 ]; then
        send_alert "Slow Query" "Query to $ns took ${query_time}ms (threshold 100ms)"
    fi
}

# 4. Check DNSSEC validation
check_dnssec() {
    local zone=$1
    
    if ! dig $zone +dnssec | grep -q "ad;"; then
        send_alert "DNSSEC Failure" "DNSSEC validation failed for $zone"
    fi
}

# 5. Check disk space
check_disk_space() {
    local usage=$(df -h /var/cache/bind | tail -1 | awk '{print $5}' | sed 's/%//')
    
    if [ $usage -gt 80 ]; then
        send_alert "Disk Space" "DNS cache disk usage at ${usage}%"
    fi
}

# 6. Check BIND process
check_bind_process() {
    if ! systemctl is-active --quiet bind9; then
        send_alert "BIND Down" "BIND service not running"
        
        # Auto-restart
        systemctl start bind9
        log "Attempted automatic restart of BIND"
    fi
}

# 7. Analyze query rate
check_query_rate() {
    local qps=$(rndc status 2>/dev/null | grep "queries received" | awk '{print $1}')
    
    if [ $qps -gt 50000 ]; then
        send_alert "High Query Rate" "Query rate: $qps qps (possible DDoS)"
    fi
}

# Main monitoring loop
log "DNS Monitoring started"

while true; do
    for ns in "${NAMESERVERS[@]}"; do
        check_nameserver_up $ns
        
        if [ $? -eq 0 ]; then
            for zone in "${ZONES[@]}"; do
                check_query_performance $ns $zone
            done
        fi
    done
    
    for zone in "${ZONES[@]}"; do
        check_zone_sync $zone
        check_dnssec $zone
    done
    
    check_disk_space
    check_bind_process
    check_query_rate
    
    sleep 60
done
```

### 11.4 Prometheus + Grafana Monitoring

```bash
# bind_exporter (Prometheus metrics)

# Install
wget https://github.com/prometheus-community/bind_exporter/releases/download/v0.6.1/bind_exporter-0.6.1.linux-amd64.tar.gz
tar xvf bind_exporter-0.6.1.linux-amd64.tar.gz
sudo mv bind_exporter /usr/local/bin/

# BIND config (enable statistics)
# /etc/bind/named.conf.options
statistics-channels {
    inet 127.0.0.1 port 8053 allow { localhost; };
};

# Systemd service
# /etc/systemd/system/bind_exporter.service
[Unit]
Description=BIND Exporter
After=network.target

[Service]
Type=simple
User=bind-exporter
ExecStart=/usr/local/bin/bind_exporter --bind.stats-url=http://localhost:8053/

[Install]
WantedBy=multi-user.target

sudo systemctl enable bind_exporter
sudo systemctl start bind_exporter

# Prometheus config
# /etc/prometheus/prometheus.yml
scrape_configs:
  - job_name: 'bind'
    static_configs:
      - targets: ['localhost:9119']

# Metrics disponibles :
# bind_up
# bind_query_recursions_total
# bind_responses_total
# bind_query_errors_total
# bind_zone_serial

# Grafana dashboard
# Import dashboard ID: 1666 (BIND)
```

---

## Section 12 : Cas Pratiques Production

### 12.1 Setup DNS Authoritative HA

```bash
# Architecture High Availability DNS

# Primary NS (192.0.2.50)
# Secondary NS1 (203.0.113.10)
# Secondary NS2 (203.0.113.11)

# === PRIMARY NAMESERVER ===
# /etc/bind/named.conf.options
acl "slaves" {
    203.0.113.10;
    203.0.113.11;
};

options {
    directory "/var/cache/bind";
    recursion no;
    allow-query { any; };
    allow-transfer { slaves; };
    notify yes;
    also-notify { 
        203.0.113.10;
        203.0.113.11;
    };
    
    dnssec-validation yes;
    
    rate-limit {
        responses-per-second 20;
        window 5;
    };
};

# /etc/bind/named.conf.local
zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    allow-transfer { slaves; };
    notify yes;
};

zone "2.0.192.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.192.0.2";
    allow-transfer { slaves; };
};

# Zone file
# /etc/bind/zones/db.example.com
$ORIGIN example.com.
$TTL 3600

@   IN  SOA ns1.example.com. hostmaster.example.com. (
    2024011601
    7200
    3600
    1209600
    3600 )

; Nameservers (tous les 3)
@   IN  NS  ns1.example.com.
@   IN  NS  ns2.example.com.
@   IN  NS  ns3.example.com.

; Glue records
ns1  IN  A  192.0.2.50
ns2  IN  A  203.0.113.10
ns3  IN  A  203.0.113.11

; Records application
@       IN  A   192.0.2.1
www     IN  A   192.0.2.1
mail    IN  A   192.0.2.10

@   IN  MX  10  mail.example.com.

# === SECONDARY NAMESERVERS (identique sur NS2 et NS3) ===
# /etc/bind/named.conf.local
acl "masters" {
    192.0.2.50;
};

options {
    directory "/var/cache/bind";
    recursion no;
    allow-query { any; };
    allow-transfer { none; };
    allow-notify { masters; };
};

zone "example.com" {
    type slave;
    file "/var/cache/bind/db.example.com";
    masters { 192.0.2.50; };
};

zone "2.0.192.in-addr.arpa" {
    type slave;
    file "/var/cache/bind/db.192.0.2";
    masters { 192.0.2.50; };
};

# === MONITORING ===
#!/bin/bash
# ha-dns-check.sh

PRIMARY="192.0.2.50"
SECONDARIES=("203.0.113.10" "203.0.113.11")
ZONE="example.com"

PRIMARY_SERIAL=$(dig @$PRIMARY $ZONE SOA +short | awk '{print $3}')

echo "Primary NS ($PRIMARY): serial $PRIMARY_SERIAL"

for ns in "${SECONDARIES[@]}"; do
    SERIAL=$(dig @$ns $ZONE SOA +short | awk '{print $3}')
    
    if [ "$SERIAL" == "$PRIMARY_SERIAL" ]; then
        echo "✓ Secondary $ns: IN SYNC"
    else
        echo "✗ Secondary $ns: OUT OF SYNC (serial $SERIAL)"
        
        # Force retransfer
        ssh $ns "sudo rndc retransfer $ZONE"
    fi
done

# Cron every 15 min
# */15 * * * * /usr/local/bin/ha-dns-check.sh
```

### 12.2 Migration DNS Zero-Downtime

```bash
# Scénario : Migrer DNS vers nouveaux serveurs

# OLD NS : ns1.old.com (198.51.100.50)
# NEW NS : ns1.new.com (203.0.113.50), ns2.new.com (203.0.113.51)

# === PHASE 1 : Préparation (J-7) ===

# 1. Baisser TTL zone (facilite propagation)
# OLD: /etc/bind/zones/db.example.com
$TTL 300  ; 5 minutes (au lieu 3600)

@   IN  SOA ns1.old.com. admin.example.com. (
    2024011501  ; Increment serial
    900         ; Refresh réduit (15 min)
    600         ; Retry réduit (10 min)
    1209600
    300 )       ; Minimum TTL réduit

# Reload
sudo rndc reload example.com

# 2. Setup nouveaux serveurs
# NEW: Install BIND, configure zones identiques

# 3. Ajouter nouveaux NS dans zone (still secondary)
# OLD: /etc/bind/zones/db.example.com
@   IN  NS  ns1.old.com.    ; Current primary
@   IN  NS  ns1.new.com.    ; New server 1
@   IN  NS  ns2.new.com.    ; New server 2

ns1.old  IN  A  198.51.100.50
ns1.new  IN  A  203.0.113.50
ns2.new  IN  A  203.0.113.51

# Increment serial
@   IN  SOA ns1.old.com. admin.example.com. (
    2024011502  ; Incremented
    ...
)

# Allow transfer to new servers
# OLD: /etc/bind/named.conf.local
acl "slaves" {
    203.0.113.50;  ; New NS1
    203.0.113.51;  ; New NS2
};

zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    allow-transfer { slaves; };
    also-notify { 
        203.0.113.50;
        203.0.113.51;
    };
};

# 4. Configure new servers as slaves
# NEW: /etc/bind/named.conf.local
zone "example.com" {
    type slave;
    file "/var/cache/bind/db.example.com";
    masters { 198.51.100.50; };
};

# Vérifier sync
dig @203.0.113.50 example.com SOA +short

# === PHASE 2 : Update Registrar (J-1) ===

# 1. Ajouter nouveaux NS chez registrar
# Via interface Gandi/OVH/etc:
# Ajouter : ns1.new.com, ns2.new.com
# Garder : ns1.old.com (temporaire)

# 2. Attendre propagation (24-48h)
# Vérifier propagation
dig example.com NS @8.8.8.8
dig example.com NS @1.1.1.1

# === PHASE 3 : Basculement (J0) ===

# 1. Promouvoir new NS1 primary
# NEW NS1: /etc/bind/named.conf.local
zone "example.com" {
    type master;  ; Slave → Master
    file "/etc/bind/zones/db.example.com";
    allow-transfer { 203.0.113.51; };  ; NS2
};

# Copier zone file depuis cache
sudo cp /var/cache/bind/db.example.com /etc/bind/zones/

# Update SOA (new primary)
# /etc/bind/zones/db.example.com
@   IN  SOA ns1.new.com. admin.example.com. (
    2024011601  ; New serial
    7200
    3600
    1209600
    3600 )

@   IN  NS  ns1.new.com.
@   IN  NS  ns2.new.com.
; Remove ns1.old.com

# 2. Configure NS2 slave de NS1
# NEW NS2: /etc/bind/named.conf.local
zone "example.com" {
    type slave;
    file "/var/cache/bind/db.example.com";
    masters { 203.0.113.50; };  ; NEW NS1
};

# 3. Reload all
sudo rndc reload example.com

# 4. Vérifier sync nouveaux servers
dig @203.0.113.50 example.com SOA
dig @203.0.113.51 example.com SOA

# === PHASE 4 : Cleanup (J+2) ===

# 1. Retirer old NS registrar
# Via interface : Supprimer ns1.old.com

# 2. Augmenter TTL
# /etc/bind/zones/db.example.com
$TTL 3600  ; Restore to 1 hour

# 3. Décommissionner old server (J+7)
# Après confirmation 0 requêtes
sudo systemctl stop bind9

# === MONITORING MIGRATION ===
#!/bin/bash
# migration-monitor.sh

OLD_NS="198.51.100.50"
NEW_NS=("203.0.113.50" "203.0.113.51")
ZONE="example.com"

echo "=== Migration Status ==="

echo "Old NS queries:"
sudo rndc stats
grep "queries received" /var/cache/bind/named.stats

echo ""
echo "New NS sync:"
for ns in "${NEW_NS[@]}"; do
    SERIAL=$(dig @$ns $ZONE SOA +short | awk '{print $3}')
    echo "$ns: serial $SERIAL"
done
```

### 12.3 DNS Troubleshooting Incident

```bash
# Scénario : Site web inaccessible - Investigation DNS

# === ÉTAPE 1 : Résolution Basique ===

# Test local
dig example.com

# Si SERVFAIL ou timeout → Problème resolver
# Si NXDOMAIN → Problème zone/registrar
# Si IP incorrecte → Cache poisoning ou config error

# === ÉTAPE 2 : Tester Multiple Resolvers ===

# Google DNS
dig @8.8.8.8 example.com

# Cloudflare
dig @1.1.1.1 example.com

# Quad9
dig @9.9.9.9 example.com

# Si résultats diffèrent → Propagation en cours ou cache poisoning

# === ÉTAPE 3 : Vérifier Authoritative ===

# Get nameservers
dig example.com NS +short

# Query each authoritative directly
for ns in $(dig example.com NS +short); do
    echo "NS: $ns"
    dig @$ns example.com +short
done

# Si authoritative correct mais resolvers incorrect → Propagation

# === ÉTAPE 4 : Vérifier Serial Sync ===

PRIMARY_SERIAL=$(dig @ns1.example.com example.com SOA +short | awk '{print $3}')

for ns in $(dig example.com NS +short); do
    SERIAL=$(dig @$ns example.com SOA +short | awk '{print $3}')
    
    if [ "$SERIAL" != "$PRIMARY_SERIAL" ]; then
        echo "✗ $ns out of sync: serial $SERIAL (expected $PRIMARY_SERIAL)"
    fi
done

# === ÉTAPE 5 : Check Logs ===

# BIND logs
sudo tail -100 /var/log/syslog | grep named

# Query logs
sudo tail -100 /var/log/named/query.log

# Chercher :
# - "transfer failed"
# - "zone transfer"
# - "notify"
# - "error"

# === ÉTAPE 6 : Vérifier Configuration ===

# Check config syntax
sudo named-checkconf

# Check zone file
sudo named-checkzone example.com /etc/bind/zones/db.example.com

# === ÉTAPE 7 : Vérifier Connectivité ===

# Ping nameserver
ping ns1.example.com

# Test port 53 UDP
nc -zvu ns1.example.com 53

# Test port 53 TCP
nc -zv ns1.example.com 53

# === ÉTAPE 8 : Force Reload/Retransfer ===

# Primary : Reload zone
sudo rndc reload example.com

# Secondary : Force retransfer
sudo rndc retransfer example.com

# === ÉTAPE 9 : Flush Caches ===

# Client cache
sudo systemd-resolve --flush-caches  # Linux
ipconfig /flushdns                   # Windows

# BIND cache
sudo rndc flush

# === ÉTAPE 10 : Incident Report ===

#!/bin/bash
# incident-report.sh

ZONE="example.com"
REPORT_FILE="dns-incident-$(date +%Y%m%d-%H%M%S).txt"

{
    echo "=== DNS Incident Report ==="
    echo "Date: $(date)"
    echo "Zone: $ZONE"
    echo ""
    
    echo "=== Resolution Test ==="
    dig $ZONE
    echo ""
    
    echo "=== Nameservers ==="
    dig $ZONE NS
    echo ""
    
    echo "=== SOA Records ==="
    for ns in $(dig $ZONE NS +short); do
        echo "NS: $ns"
        dig @$ns $ZONE SOA +short
    done
    echo ""
    
    echo "=== Multiple Resolvers ==="
    for resolver in 8.8.8.8 1.1.1.1 9.9.9.9; do
        echo "Resolver: $resolver"
        dig @$resolver $ZONE +short
    done
    echo ""
    
    echo "=== BIND Logs (last 50 lines) ==="
    sudo tail -50 /var/log/syslog | grep named
    
} > $REPORT_FILE

echo "Report generated: $REPORT_FILE"
```

### 12.4 DNS Performance Optimization

```bash
# Cas : DNS lent, optimiser performance

# === ANALYSE PERFORMANCE ===

# 1. Mesurer query time
dig example.com +stats | grep "Query time"

# Si > 100ms → Problème

# 2. Identifier bottleneck

# Cache hit rate
sudo rndc stats
grep "cache hits" /var/cache/bind/named.stats
grep "cache misses" /var/cache/bind/named.stats

# Hit rate = hits / (hits + misses)
# Si < 80% → Cache trop petit ou TTL trop court

# 3. Recursive queries stats
grep "queries resulted in successful answer" /var/cache/bind/named.stats
grep "queries caused recursion" /var/cache/bind/named.stats

# === OPTIMISATION ===

# 1. Augmenter cache size
# /etc/bind/named.conf.options
options {
    max-cache-size 2048M;  # 2GB cache
    max-cache-ttl 86400;   # 24h max
    max-ncache-ttl 10800;  # 3h negative
};

# 2. Enable prefetch
options {
    prefetch 2 9;  # Renouveler si TTL < 9s
};

# 3. Tune TCP/UDP
options {
    tcp-clients 2000;
    recursive-clients 20000;
    edns-udp-size 4096;
};

# 4. Forwarders performance
options {
    forwarders {
        1.1.1.1;  # Cloudflare (fast)
        8.8.8.8;  # Google
    };
    forward only;
};

# Test forwarders performance
for resolver in 1.1.1.1 8.8.8.8 9.9.9.9; do
    echo "Resolver: $resolver"
    time dig @$resolver example.com > /dev/null
done

# 5. Reduce minimal-responses overhead
options {
    minimal-responses yes;  # Smaller packets
    minimal-any yes;
};

# 6. Query minimization
options {
    qname-minimization relaxed;  # Privacy + performance
};

# === MONITORING PERFORMANCE ===

#!/bin/bash
# performance-monitor.sh

LOG_FILE="/var/log/dns-performance.log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a $LOG_FILE
}

# Measure query time
measure_query_time() {
    local domain=$1
    
    local start=$(date +%s%3N)
    dig $domain > /dev/null 2>&1
    local end=$(date +%s%3N)
    
    local elapsed=$((end - start))
    echo $elapsed
}

# Cache statistics
get_cache_stats() {
    sudo rndc stats
    
    local hits=$(grep -A 20 "Cache DB RRsets" /var/cache/bind/named.stats | grep -oP "hits: \K\d+")
    local misses=$(grep -A 20 "Cache DB RRsets" /var/cache/bind/named.stats | grep -oP "misses: \K\d+")
    
    if [ -n "$hits" ] && [ -n "$misses" ]; then
        local total=$((hits + misses))
        local hit_rate=$(echo "scale=2; $hits / $total * 100" | bc)
        echo "Cache hit rate: $hit_rate%"
    fi
}

# Main loop
while true; do
    QT=$(measure_query_time "example.com")
    log "Query time: ${QT}ms"
    
    if [ $QT -gt 100 ]; then
        log "WARNING: Slow query (${QT}ms > 100ms)"
    fi
    
    STATS=$(get_cache_stats)
    log "$STATS"
    
    sleep 60
done
```

---

## Ressources et Références

**Documentation officielle :**
- BIND 9 : https://www.isc.org/bind/
- RFC 1034/1035 : DNS Protocol
- RFC 4033-4035 : DNSSEC
- RFC 7858 : DNS-over-TLS
- RFC 8484 : DNS-over-HTTPS
- IANA Root Zone : https://www.iana.org/domains/root

**Outils et logiciels :**
- BIND 9 : https://www.isc.org/downloads/bind/
- Unbound : https://nlnetlabs.nl/projects/unbound/
- PowerDNS : https://www.powerdns.com/
- dnsmasq : http://www.thekelleys.org.uk/dnsmasq/
- Knot DNS : https://www.knot-dns.cz/

**Testing et monitoring :**
- DNSViz : https://dnsviz.net/
- Zonemaster : https://zonemaster.net/
- DNS Checker : https://dnschecker.org/
- IntoDNS : https://intodns.com/

**Security :**
- DNS Flag Day : https://www.dnsflagday.net/
- DNSSEC Guide : https://www.cloudflare.com/dns/dnssec/
- DNS Best Practices : https://www.icann.org/

**Learning resources :**
- DNS for Rocket Scientists : http://www.zytrax.com/books/dns/
- Pro DNS and BIND : Apress book
- SANS DNS Security : https://www.sans.org/

---

## Conclusion

**DNS = Infrastructure critique Internet**

**Points clés maîtrisés :**

✅ **Architecture hiérarchique** = Root → TLD → Authoritative → Recursive
✅ **Types records** = A, MX, TXT, CNAME, NS, SOA, PTR, SRV, CAA, DNSSEC
✅ **BIND configuration** = Authoritative, Recursive, Forwarding, Views
✅ **Zone management** = Zone files, SOA, Serial, TTL, Subdomains
✅ **Réplication** = Primary/Secondary, AXFR/IXFR, TSIG, Monitoring
✅ **DNSSEC** = KSK/ZSK, Signatures, Chain of Trust, Validation
✅ **DNS moderne** = DoT, DoH, DoQ (chiffrement)
✅ **Performance** = Cache, Anycast, GeoDNS, Prefetch
✅ **Security** = DDoS mitigation, Rate limiting, RPZ, Hardening
✅ **Troubleshooting** = dig, rndc, Logs, Diagnostics
✅ **Production** = HA, Migration, Monitoring, Incident response

**Ordre apprentissage DNS :**

```
1. Concepts fondamentaux (hiérarchie, résolution)
2. Types records DNS (A, MX, TXT, etc.)
3. Installation BIND (authoritative basique)
4. Zone files création
5. DNS secondaires (réplication)
6. DNSSEC activation
7. Performance tuning
8. Security hardening
9. Monitoring production
10. Troubleshooting incidents
```

**Stack réseau complète :**

```
1. nslookup  ✅ DNS queries (utilisateur)
2. netstat   ✅ Connexions monitoring
3. DNS       ✅ Infrastructure nameservers (actuel)
4. tcpdump   → Capture paquets (prochain)
5. scapy     → Manipulation paquets (avancé)
```

**Chiffres clés retenus :**

- **4.66+ milliards** domaines enregistrés mondialement
- **13 root servers** (répliqués 1000+ instances Anycast)
- **~3 trillions** requêtes DNS/jour
- **99.99%+** uptime infrastructure critique
- **50-200ms** résolution cold cache
- **<1ms** résolution warm cache

**Tu maîtrises maintenant DNS de l'architecture fondamentale à l'exploitation production enterprise !** 🌐

**DNS = Fondation Internet invisible mais absolument critique** 🎯

---

_Version 1.0 | Dernière mise à jour : 2024-01-16_

Voilà le guide DNS complet terminé ! Il couvre **12 sections complètes** :

✅ Introduction et architecture DNS (hiérarchie, résolution)  
✅ Types d'enregistrements (A, MX, TXT, CNAME, NS, SOA, PTR, SRV, CAA)  
✅ Résolution DNS (recursive vs iterative, cache)  
✅ Installation et configuration BIND  
✅ Zone files et gestion domaines  
✅ DNS secondaires et réplication (AXFR/IXFR)  
✅ DNSSEC (sécurité cryptographique)  
✅ DNS moderne (DoH, DoT, DoQ)  
✅ Performance et optimisation (cache, Anycast, GeoDNS)  
✅ Security (attaques DDoS, cache poisoning, hardening)  
✅ Troubleshooting et monitoring (dig, rndc, Prometheus)  
✅ Cas pratiques production (HA, migration, incidents)  

**C'est le guide DNS le plus complet avec configurations production-ready !** 🚀