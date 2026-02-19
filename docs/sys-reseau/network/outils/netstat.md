---
description: "netstat : monitoring connexions réseau, ports ouverts, troubleshooting, détection intrusions"
icon: lucide/book-open-check
tags: ["NETSTAT", "NETWORK", "MONITORING", "TROUBLESHOOTING", "SECURITY", "FORENSIC"]
---

# netstat

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-time="4-5 heures"
  data-version="1.0">
</div>

## Introduction au Monitoring Réseau et à la Connexions

!!! quote "Analogie pédagogique"
    _Imaginez le **tableau de contrôle aérien aéroport international gérant 1000+ vols simultanés** : netstat fonctionne comme **système monitoring temps réel visualisant TOUTES connexions réseau machine** (avions = paquets, pistes = ports, tours contrôle = services). **Tour contrôle aéroport réseau** : écrans affichant tous vols actifs (connexions TCP établies), pistes disponibles (ports en écoute), décollages/atterrissages en cours (SYN, FIN packets), files attente (backlog connexions), historique trafic (statistiques paquets envoyés/reçus), alertes collision (ports conflits), plan vol complet (tables routage), capacité pistes temps réel (bande passante utilisée). **Sans netstat/monitoring** : impossible savoir quels services tournent (ports ouverts = portes ouvertes invisibles), connexions suspectes non détectées (backdoor malware communique librement), troubleshooting réseau aveugle (pourquoi site lent? connexions TIME_WAIT?), performance dégradée mystérieuse (trop connexions simultanées), sécurité compromise (attaquant connecté port 4444 rootkit), forensique impossible (qui a parlé à qui quand?). **Avec netstat** : **Visibilité complète** (voir TOUTES connexions actives temps réel), **Détection anomalies** (port 31337 suspect = backdoor probable), **Troubleshooting rapide** (trop connexions CLOSE_WAIT = app leak), **Monitoring services** (nginx écoute port 80? MySQL 3306?), **Security auditing** (quels ports exposés Internet?), **Performance analysis** (statistiques paquets/erreurs réseau), **Forensique** (reconstituer communications incident), **Documentation** (inventaire services réseau complet). **netstat = stéthoscope réseau** : ausculte santé réseau machine, détecte battements anormaux (connexions suspectes), mesure performance (throughput), diagnostique maladies (leak connexions), prévient crises (ports ouverts dangereux). **Architecture réseau multicouche** : Application (HTTP, SSH, FTP), Transport (TCP, UDP ports), Network (IP routage), Interface (eth0, wlan0 statistiques). **Cas usage critiques** : Sysadmin vérifie services démarrés correctement, Pentest énumère ports ouverts cible, Forensique analyse connexions malware, DevOps debug leak connexions app, Security détecte backdoor communication C2, Performance optimise TCP window size. **netstat universellement disponible** : Linux (net-tools package), Windows (natif toutes versions), BSD/Unix (natif), macOS (natif jusqu'à 10.13), alternative moderne `ss` (socket statistics Linux plus rapide). **Puissance netstat** : 30+ ans existence (1983 BSD Unix), syntaxe stable compatible, aucun privilège root basique (sauf -p), output parsable scripting, temps réel monitoring (-c continuous), multi-OS (Windows/Linux syntaxe légèrement différente)._

**netstat en résumé :**

- ✅ **Connexions actives** = Voir toutes connexions TCP/UDP établies
- ✅ **Ports écoute** = Lister services en écoute (listening ports)
- ✅ **Tables routage** = Afficher routes réseau système
- ✅ **Statistiques** = Métriques paquets/erreurs par protocole
- ✅ **Multi-OS** = Linux, Windows, BSD, macOS (syntaxe varie)
- ✅ **Temps réel** = Monitoring continu (-c, watch)
- ✅ **Troubleshooting** = Diagnostiquer problèmes réseau
- ✅ **Security** = Détecter backdoors, ports suspects

**Guide structure :**

1. Introduction et concepts réseau
2. Syntaxe et options (Linux vs Windows)
3. Connexions actives TCP/UDP
4. Ports en écoute (listening)
5. États connexions TCP
6. Tables de routage
7. Statistiques interfaces réseau
8. Monitoring temps réel
9. Troubleshooting réseau
10. Security et détection intrusions
11. Comparaison ss/lsof/sockstat
12. Cas pratiques production

---

## Section 1 : Introduction et Concepts Réseau

### 1.1 Qu'est-ce que netstat ?

**netstat = Network Statistics (Statistiques Réseau)**

```
Fonction principale :
Afficher connexions réseau, tables routage, statistiques interfaces

Historique :
1983 : Première version BSD Unix
1990s : Porté sur tous Unix/Linux
2000s : Intégré Windows NT+
2010s : Déprécié Linux (remplacé ss), maintenu compatibilité

Disponibilité :
✅ Linux (package net-tools)
✅ Windows (natif toutes versions)
✅ BSD/Unix (natif)
✅ macOS (natif, déprécié depuis 10.13)

Alternative moderne :
- ss (socket statistics, Linux, plus rapide)
- lsof (list open files, inclut sockets)
- sockstat (BSD)
```

**Pourquoi netstat essentiel ?**

```
Use cases critiques :

1. Monitoring :
   - Quels services tournent? (nginx, mysql, ssh)
   - Combien connexions actives?
   - Ports ouverts exposés Internet?

2. Troubleshooting :
   - Pourquoi connexion échoue?
   - Trop connexions TIME_WAIT?
   - Service écoute bon port?

3. Security :
   - Backdoor écoute port suspect?
   - Connexions sortantes malware C2?
   - Scan port en cours?

4. Performance :
   - Leak connexions application?
   - Bande passante utilisée?
   - Paquets perdus/erreurs?

5. Forensique :
   - Qui connecté à qui incident?
   - Historique connexions malware?
   - Reconstituer timeline attaque?
```

### 1.2 Concepts Réseau Fondamentaux

**Modèle TCP/IP (4 couches) :**

```
Application    : HTTP, SSH, FTP, DNS
    ↓
Transport      : TCP (connexion), UDP (sans connexion)
    ↓
Internet       : IP (adressage, routage)
    ↓
Network Access : Ethernet, WiFi (physique)

netstat opère couche Transport + Internet :
- Connexions TCP/UDP (ports)
- Adresses IP source/destination
- Tables routage IP
- Statistiques interfaces
```

**Ports (0-65535) :**

```
Well-known ports (0-1023) :
20/21   FTP
22      SSH
23      Telnet
25      SMTP (email)
53      DNS
80      HTTP
443     HTTPS
3306    MySQL
5432    PostgreSQL

Registered ports (1024-49151) :
3000    Node.js (dev)
5000    Flask (dev)
8080    HTTP alternate
8443    HTTPS alternate

Dynamic/Private (49152-65535) :
Ports éphémères (connexions client)

Exemple connexion HTTP :
Client: 192.168.1.10:52341 → Server: 93.184.216.34:80
        (IP locale, port éphémère)    (IP serveur, port 80)
```

**Protocoles Transport :**

```
TCP (Transmission Control Protocol) :
✅ Connexion établie (3-way handshake)
✅ Fiable (retransmission paquets perdus)
✅ Ordonné (paquets dans ordre)
✅ Contrôle flux (congestion control)
❌ Plus lent (overhead)

Usage : HTTP, SSH, FTP, email

UDP (User Datagram Protocol) :
✅ Sans connexion (fire and forget)
✅ Rapide (pas overhead)
✅ Léger (streaming, gaming)
❌ Non fiable (paquets peuvent être perdus)
❌ Non ordonné

Usage : DNS, streaming, VoIP, gaming

ICMP (Internet Control Message Protocol) :
Ping, traceroute, erreurs réseau
```

### 1.3 États Connexions TCP

**TCP State Machine (crucial troubleshooting) :**

```
LISTEN         : Port en écoute (serveur attend connexions)
SYN_SENT       : Client envoyé SYN, attend SYN-ACK
SYN_RECEIVED   : Serveur reçu SYN, envoyé SYN-ACK
ESTABLISHED    : Connexion établie (données transitent)
FIN_WAIT_1     : Début fermeture connexion
FIN_WAIT_2     : Attente FIN distant
CLOSE_WAIT     : Distant fermé, local pas encore
CLOSING        : Fermeture simultanée
LAST_ACK       : Attente ACK final
TIME_WAIT      : Attente expiration (2MSL, ~60s)
CLOSED         : Connexion fermée complètement

Lifecycle normal :
1. LISTEN (serveur)
2. SYN_SENT (client)
3. ESTABLISHED (données)
4. FIN_WAIT / CLOSE_WAIT (fermeture)
5. TIME_WAIT (attente)
6. CLOSED

États problématiques :
- Trop TIME_WAIT : App ferme connexions mal
- Trop CLOSE_WAIT : App pas close() sockets
- Trop SYN_RECEIVED : SYN flood attack
```

---

## Section 2 : Syntaxe et Options

### 2.1 Syntaxe Basique

```bash
# Syntaxe générale
netstat [options]

# Linux options principales :
-a, --all              Toutes connexions (actives + listening)
-t, --tcp              Connexions TCP seulement
-u, --udp              Connexions UDP seulement
-l, --listening        Ports en écoute seulement
-n, --numeric          Adresses numériques (pas résolution DNS)
-p, --program          PID et nom programme (root requis)
-c, --continuous       Monitoring continu (rafraîchit)
-r, --route            Table routage
-i, --interfaces       Statistiques interfaces
-s, --statistics       Statistiques par protocole

# Windows options principales :
-a                     Toutes connexions
-n                     Adresses numériques
-o                     PID process (Owner)
-b                     Nom executable (Admin requis)
-p [protocol]          Protocole (TCP, UDP, ICMP)
-r                     Table routage
-s                     Statistiques
-e                     Statistiques ethernet

# Exemples basiques :
netstat                # Connexions actives (default)
netstat -a             # Toutes (actives + listening)
netstat -t             # TCP seulement
netstat -u             # UDP seulement
netstat -l             # Listening ports
netstat -n             # Numeric (pas DNS)
```

### 2.2 Options Linux Essentielles

```bash
# Connexions TCP actives
netstat -t

# Output :
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 192.168.1.10:52341      93.184.216.34:80       ESTABLISHED

# Explications colonnes :
# Proto      : Protocole (tcp, tcp6, udp, udp6)
# Recv-Q     : Bytes reçus pas encore lus par app
# Send-Q     : Bytes envoyés pas encore ACKés
# Local      : IP:port local
# Foreign    : IP:port distant
# State      : État connexion TCP

# Tous ports en écoute + numérique
netstat -tuln

# Output :
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN

# 0.0.0.0:22 = Écoute TOUTES interfaces (accessible de partout)
# 127.0.0.1:3306 = Écoute localhost seulement (pas accessible réseau)

# Avec PID et programme (root requis)
sudo netstat -tulnp

# Output :
Proto Local Address    State       PID/Program name
tcp   0.0.0.0:22       LISTEN      1234/sshd
tcp   0.0.0.0:80       LISTEN      5678/nginx
tcp   127.0.0.1:3306   LISTEN      9012/mysqld

# Monitoring continu (refresh 1s)
netstat -tulnc

# Statistiques complètes
netstat -s

# Table routage
netstat -rn

# Statistiques interfaces
netstat -i
```

### 2.3 Options Windows Essentielles

```powershell
# Connexions actives
netstat -a

# Output :
Proto  Local Address          Foreign Address        State
TCP    0.0.0.0:135            0.0.0.0:0              LISTENING
TCP    192.168.1.10:49152     93.184.216.34:80      ESTABLISHED

# Numérique (pas résolution noms)
netstat -an

# Avec PID (Owner)
netstat -ano

# Output :
Proto  Local Address          Foreign Address        State           PID
TCP    0.0.0.0:80             0.0.0.0:0              LISTENING       4
TCP    192.168.1.10:52341     93.184.216.34:80      ESTABLISHED     1234

# Avec nom executable (Admin requis)
netstat -anb

# Output :
TCP    0.0.0.0:80             0.0.0.0:0              LISTENING
 [System]
TCP    192.168.1.10:52341     93.184.216.34:80      ESTABLISHED
 [chrome.exe]

# TCP seulement
netstat -an -p TCP

# UDP seulement
netstat -an -p UDP

# Statistiques
netstat -s

# Table routage
netstat -r

# Monitoring continu (PowerShell)
while ($true) { cls; netstat -an; Start-Sleep -Seconds 1 }
```

### 2.4 Combinaisons Utiles

```bash
# Linux - Cheatsheet rapide

# Ports TCP en écoute avec programmes
sudo netstat -tlnp

# Toutes connexions TCP actives
netstat -tan

# Compter connexions par état
netstat -tan | awk '{print $6}' | sort | uniq -c

# Top 10 IPs connectées
netstat -tan | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -10

# Connexions vers port spécifique
netstat -tan | grep :80

# Programmes utilisant réseau
sudo netstat -tulnp | grep LISTEN

# Monitoring léger (1 ligne)
watch -n 1 'netstat -tan | grep ESTABLISHED | wc -l'

# Windows - Cheatsheet rapide

# Ports en écoute avec PID
netstat -ano | findstr LISTENING

# Connexions établies
netstat -ano | findstr ESTABLISHED

# Connexions vers port 80
netstat -ano | findstr :80

# Process ID vers nom
tasklist | findstr [PID]

# Kill connexion (via PID)
taskkill /PID [PID] /F
```

---

## Section 3 : Connexions Actives TCP/UDP

### 3.1 Visualiser Connexions TCP

```bash
# Linux : Connexions TCP actives
netstat -tan

# Output :
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 192.168.1.10:52341      93.184.216.34:80       ESTABLISHED
tcp        0      0 192.168.1.10:52342      140.82.121.4:443       ESTABLISHED
tcp        0      0 192.168.1.10:52343      142.250.185.78:443     ESTABLISHED

# Interpréter :
# 192.168.1.10:52341 → 93.184.216.34:80
# Client local (IP privée, port éphémère)
# → Serveur distant (IP publique, port 80 HTTP)

# Avec résolution DNS (lent)
netstat -ta

# Output :
Proto Local Address           Foreign Address         State
tcp   desktop:52341           example.com:http        ESTABLISHED
tcp   desktop:52342           github.com:https        ESTABLISHED

# Filtrer par état
netstat -tan | grep ESTABLISHED
netstat -tan | grep TIME_WAIT
netstat -tan | grep CLOSE_WAIT

# Filtrer par port
netstat -tan | grep :80
netstat -tan | grep :443

# Filtrer par IP
netstat -tan | grep 93.184.216.34
```

### 3.2 Visualiser Connexions UDP

```bash
# Linux : Connexions UDP
netstat -uan

# Output :
Proto Recv-Q Send-Q Local Address           Foreign Address         State
udp        0      0 0.0.0.0:68              0.0.0.0:*                    
udp        0      0 127.0.0.1:53            0.0.0.0:*                    

# UDP = stateless (pas état ESTABLISHED)
# State toujours vide pour UDP

# UDP listening (serveurs)
udp    0.0.0.0:53              # DNS server
udp    0.0.0.0:67              # DHCP server
udp    0.0.0.0:123             # NTP server
udp    0.0.0.0:161             # SNMP

# UDP important : DNS, DHCP, NTP, VPN, streaming
```

### 3.3 Connexions par Programme

```bash
# Linux : Voir quel programme utilise connexion (root)
sudo netstat -tanp

# Output :
Proto Local Address    Foreign Address   State       PID/Program
tcp   192.168.1.10:52341  93.184.216.34:80  ESTABLISHED 1234/firefox
tcp   192.168.1.10:52342  140.82.121.4:443  ESTABLISHED 5678/chrome
tcp   192.168.1.10:22     192.168.1.5:49152 ESTABLISHED 9012/sshd

# Filtrer par programme
sudo netstat -tanp | grep firefox
sudo netstat -tanp | grep nginx
sudo netstat -tanp | grep mysql

# Windows : Voir programme (avec PID)
netstat -ano

# Output :
Proto  Local Address         Foreign Address       State       PID
TCP    192.168.1.10:52341    93.184.216.34:80     ESTABLISHED  1234

# Trouver nom programme depuis PID
tasklist | findstr 1234
# firefox.exe   1234  Console  1  123,456 K

# Ou directement avec -b (Admin)
netstat -anb

# Output :
TCP    192.168.1.10:52341    93.184.216.34:80     ESTABLISHED
 [firefox.exe]
```

### 3.4 Statistiques Connexions

```bash
# Compter connexions par état
netstat -tan | awk '{print $6}' | sort | uniq -c

# Output :
    147 ESTABLISHED
     23 TIME_WAIT
      8 CLOSE_WAIT
     12 LISTEN
      1 State

# Compter connexions totales
netstat -tan | grep -c ESTABLISHED

# Top IPs connectées
netstat -tan | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn

# Output :
     25 93.184.216.34
     18 140.82.121.4
     12 142.250.185.78

# Connexions par port local
netstat -tan | awk '{print $4}' | cut -d: -f2 | sort | uniq -c | sort -rn

# Connexions par port distant
netstat -tan | awk '{print $5}' | cut -d: -f2 | sort | uniq -c | sort -rn
```

---

## Section 4 : Ports en Écoute (Listening)

### 4.1 Lister Ports Écoute

```bash
# Linux : Ports en écoute seulement
netstat -tln

# Output :
Proto Local Address           State
tcp   0.0.0.0:22              LISTEN
tcp   0.0.0.0:80              LISTEN
tcp   127.0.0.1:3306          LISTEN
tcp6  :::443                  LISTEN

# Interpréter :
# 0.0.0.0:22      → Écoute TOUTES interfaces IPv4 (accessible réseau)
# 127.0.0.1:3306  → Écoute localhost seulement (pas accessible réseau)
# :::443          → Écoute TOUTES interfaces IPv6

# Avec programmes (root)
sudo netstat -tlnp

# Output :
Proto Local Address    State   PID/Program
tcp   0.0.0.0:22       LISTEN  1234/sshd
tcp   0.0.0.0:80       LISTEN  5678/nginx
tcp   127.0.0.1:3306   LISTEN  9012/mysqld

# TCP + UDP listening
sudo netstat -tulnp

# Filtrer par port
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :22

# Vérifier service écoute
sudo netstat -tlnp | grep nginx
sudo netstat -tlnp | grep mysql
```

### 4.2 Ports Exposés vs Locaux

```bash
# Ports exposés (0.0.0.0 = toutes interfaces)
sudo netstat -tlnp | grep "0.0.0.0"

# Output :
tcp  0.0.0.0:22       LISTEN  1234/sshd       # SSH accessible réseau
tcp  0.0.0.0:80       LISTEN  5678/nginx      # HTTP accessible réseau
tcp  0.0.0.0:443      LISTEN  5678/nginx      # HTTPS accessible réseau

# DANGER : Services exposés = surface attaque
# SSH, HTTP, HTTPS = OK si intentionnel
# MySQL, Redis, MongoDB exposés = VULNÉRABILITÉ

# Ports locaux seulement (127.0.0.1)
sudo netstat -tlnp | grep "127.0.0.1"

# Output :
tcp  127.0.0.1:3306   LISTEN  9012/mysqld     # MySQL localhost only
tcp  127.0.0.1:6379   LISTEN  1111/redis      # Redis localhost only
tcp  127.0.0.1:9200   LISTEN  2222/elasticsearch

# SÉCURISÉ : Services internes pas accessibles réseau

# Vérifier MySQL accessible seulement localhost
sudo netstat -tlnp | grep :3306
# Si "0.0.0.0:3306" → DANGER (exposé Internet)
# Si "127.0.0.1:3306" → OK (localhost seulement)

# Corriger exposition accidentelle :
# MySQL : bind-address = 127.0.0.1 dans my.cnf
# Redis : bind 127.0.0.1 dans redis.conf
```

### 4.3 Windows Listening Ports

```powershell
# Windows : Ports en écoute
netstat -an | findstr LISTENING

# Output :
TCP    0.0.0.0:135            0.0.0.0:0              LISTENING
TCP    0.0.0.0:445            0.0.0.0:0              LISTENING
TCP    0.0.0.0:3389           0.0.0.0:0              LISTENING

# Avec PID
netstat -ano | findstr LISTENING

# Output :
TCP    0.0.0.0:80             0.0.0.0:0              LISTENING       4
TCP    0.0.0.0:3389           0.0.0.0:0              LISTENING       1234

# Trouver programme depuis PID
tasklist | findstr 4
# System  4  Services  0  8,192 K

tasklist | findstr 1234
# svchost.exe  1234  Services  0  12,345 K

# Avec nom programme (Admin)
netstat -anb | findstr /A LISTENING

# Ports Windows communs :
# 135  : RPC
# 139  : NetBIOS
# 445  : SMB (partage fichiers)
# 3389 : RDP (Remote Desktop)
# 5985 : WinRM HTTP
# 5986 : WinRM HTTPS
```

### 4.4 Audit Ports Ouverts

```bash
# Audit sécurité : Quels ports exposés Internet?

# Linux : Ports exposés toutes interfaces
sudo netstat -tlnp | grep "0.0.0.0" | grep -v "127.0.0.1"

# Ports DEVANT être exposés (intentionnel) :
# 22   SSH (si administration remote)
# 80   HTTP
# 443  HTTPS

# Ports NE DEVANT PAS être exposés :
# 3306   MySQL
# 5432   PostgreSQL
# 6379   Redis
# 27017  MongoDB
# 9200   Elasticsearch
# 11211  Memcached

# Script audit automatique
for port in 3306 5432 6379 27017 9200 11211; do
    if sudo netstat -tln | grep -q "0.0.0.0:$port"; then
        echo "⚠️ WARNING: Port $port exposed to network!"
    fi
done

# Vérifier firewall bloque ports non-exposés
sudo ufw status
sudo iptables -L -n

# Windows : Audit ports
netstat -ano | findstr LISTENING | findstr "0.0.0.0"

# Vérifier firewall
Get-NetFirewallRule | Where-Object {$_.Enabled -eq 'True'}
```

---

## Section 5 : États Connexions TCP

### 5.1 Comprendre États TCP

```bash
# Afficher connexions par état
netstat -tan | awk '{print $6}' | sort | uniq -c | sort -rn

# Output :
    234 ESTABLISHED    # Connexions actives
     45 TIME_WAIT      # Attente fermeture (normal)
     12 CLOSE_WAIT     # App pas fermé socket (problème)
      8 LISTEN         # Ports en écoute
      3 SYN_SENT       # Connexion en cours
      1 FIN_WAIT_1

# ESTABLISHED : Connexion active, données transitent
netstat -tan | grep ESTABLISHED

# TIME_WAIT : Connexion fermée, attente 2MSL (~60s)
# Normal avoir quelques TIME_WAIT
# Si 1000+ TIME_WAIT = problème (app ouvre/ferme trop vite)
netstat -tan | grep TIME_WAIT | wc -l

# CLOSE_WAIT : Distant fermé, local pas encore
# Si persiste = BUG application (leak socket)
netstat -tan | grep CLOSE_WAIT
```

### 5.2 Problèmes États TCP

```bash
# Problème 1 : Trop TIME_WAIT

# Symptôme :
netstat -tan | grep TIME_WAIT | wc -l
# Output : 5000+

# Cause :
# Application ouvre/ferme connexions trop rapidement
# Épuisement ports éphémères (49152-65535)

# Solution :
# 1. Connection pooling (réutiliser connexions)
# 2. Keep-alive HTTP
# 3. Ajuster kernel params :
sudo sysctl -w net.ipv4.tcp_tw_reuse=1
sudo sysctl -w net.ipv4.tcp_fin_timeout=30

# Problème 2 : CLOSE_WAIT persistant

# Symptôme :
netstat -tan | grep CLOSE_WAIT

# Output :
tcp  192.168.1.10:52341  93.184.216.34:80  CLOSE_WAIT  # Depuis 10 min

# Cause :
# Application reçu FIN (distant fermé)
# Mais application pas appelé close() socket
# = LEAK socket, mémoire

# Identifier programme responsable :
sudo netstat -tanp | grep CLOSE_WAIT

# Output :
tcp  ...  CLOSE_WAIT  1234/buggy-app

# Solution :
# Fix code application (appeler close() après recv FIN)
# Redémarrer application temporaire

# Problème 3 : Trop SYN_RECEIVED

# Symptôme :
netstat -tan | grep SYN_RECV | wc -l
# Output : 500+

# Cause :
# SYN flood attack (DoS)
# Attaquant envoie SYN sans ACK

# Solution :
# Enable SYN cookies :
sudo sysctl -w net.ipv4.tcp_syncookies=1

# Rate limit avec iptables :
sudo iptables -A INPUT -p tcp --syn -m limit --limit 1/s -j ACCEPT
```

### 5.3 Monitoring États Temps Réel

```bash
# Linux : Watch états TCP
watch -n 1 'netstat -tan | awk "{print \$6}" | sort | uniq -c | sort -rn'

# Output rafraîchi chaque seconde :
    234 ESTABLISHED
     45 TIME_WAIT
     12 CLOSE_WAIT
      8 LISTEN

# Script monitoring avancé
#!/bin/bash
# tcp-states-monitor.sh

while true; do
    clear
    echo "=== TCP States - $(date) ==="
    echo ""
    
    netstat -tan | awk '{print $6}' | sort | uniq -c | sort -rn
    
    echo ""
    echo "CLOSE_WAIT details:"
    sudo netstat -tanp | grep CLOSE_WAIT | head -10
    
    sleep 1
done

# Alert si trop CLOSE_WAIT
CLOSE_WAIT=$(netstat -tan | grep -c CLOSE_WAIT)
if [ $CLOSE_WAIT -gt 100 ]; then
    echo "WARNING: $CLOSE_WAIT CLOSE_WAIT connections!"
    # Send alert email/slack
fi
```

---

## Section 6 : Tables de Routage

### 6.1 Afficher Table Routage

```bash
# Linux : Table routage
netstat -rn

# Output :
Kernel IP routing table
Destination     Gateway         Genmask         Flags   Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG      eth0
192.168.1.0     0.0.0.0         255.255.255.0   U       eth0
127.0.0.0       0.0.0.0         255.0.0.0       U       lo

# Colonnes :
# Destination : Réseau destination
# Gateway     : Passerelle (router)
# Genmask     : Masque sous-réseau
# Flags       : U=Up, G=Gateway, H=Host
# Iface       : Interface réseau

# Interpréter :
# 0.0.0.0 → 192.168.1.1 : Route par défaut (Internet via gateway)
# 192.168.1.0 : Réseau local direct (pas gateway)
# 127.0.0.0 : Loopback (localhost)

# Avec résolution DNS (lent)
netstat -r

# Alternative moderne (plus détaillé)
ip route show

# Windows : Table routage
netstat -r

# ou
route print
```

### 6.2 Comprendre Routage

```bash
# Scénario : Ping google.com (8.8.8.8)

# 1. Table routage consultée
netstat -rn

# 2. Match route :
# 8.8.8.8 ne match pas 192.168.1.0/24
# → Utilise route par défaut (0.0.0.0)

# 3. Paquet envoyé vers gateway
# Destination : 8.8.8.8
# Next hop : 192.168.1.1 (router)
# Interface : eth0

# Route spécifique vs défaut
# Exemple table :
Destination     Gateway         Genmask         Iface
10.0.0.0        10.0.0.1        255.255.255.0   eth1    # VPN
192.168.1.0     0.0.0.0         255.255.255.0   eth0    # LAN
0.0.0.0         192.168.1.1     0.0.0.0         eth0    # Internet

# Priorité :
# 1. Route la plus spécifique (longest prefix match)
# 2. Route par défaut (0.0.0.0)

# Troubleshooting routage
# Destination inaccessible ?
# 1. Vérifier route existe
netstat -rn | grep <destination>

# 2. Ping gateway
ping 192.168.1.1

# 3. Traceroute
traceroute 8.8.8.8
```

---

## Section 7 : Statistiques Interfaces Réseau

### 7.1 Statistiques Protocoles

```bash
# Linux : Statistiques complètes
netstat -s

# Output (extrait) :
Ip:
    12345 total packets received
    0 forwarded
    0 incoming packets discarded
    12340 incoming packets delivered
    11234 requests sent out

Icmp:
    234 ICMP messages received
    0 input ICMP message failed
    
Tcp:
    5678 active connection openings
    1234 passive connection openings
    123 failed connection attempts
    45 connection resets received
    234 connections established
    456789 segments received
    345678 segments sent out
    123 segments retransmitted
    0 bad segments received
    456 resets sent

Udp:
    12345 packets received
    23 packets to unknown port received
    0 packet receive errors
    11234 packets sent

# Statistiques TCP importantes :
# segments retransmitted : Paquets retransmis (perte réseau)
# failed connection attempts : Connexions échouées
# resets received : Connexions reset (serveur refuse)

# Isoler statistiques TCP
netstat -st

# Isoler statistiques UDP
netstat -su

# Windows : Statistiques
netstat -s

# Statistiques Ethernet
netstat -e
```

### 7.2 Statistiques Interfaces

```bash
# Linux : Stats par interface
netstat -i

# Output :
Iface   MTU   RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
eth0   1500  123456      0      0      0   112345      0      0      0 BMRU
lo    65536   45678      0      0      0    45678      0      0      0 LRU

# Colonnes :
# MTU      : Maximum Transmission Unit (taille max paquet)
# RX-OK    : Paquets reçus OK
# RX-ERR   : Erreurs réception
# RX-DRP   : Paquets droppés (buffer plein)
# TX-OK    : Paquets transmis OK
# TX-ERR   : Erreurs transmission
# Flg      : B=Broadcast, M=Multicast, R=Running, U=Up

# Monitoring continu
watch -n 1 netstat -i

# Détection problèmes :
# RX-ERR > 0 : Problème câble/hardware
# RX-DRP > 0 : Buffer overflow (trop trafic)
# TX-ERR > 0 : Problème transmission

# Alternative détaillée
ifconfig eth0
# ou moderne :
ip -s link show eth0
```

### 7.3 Analyse Performance

```bash
# Calculer taux erreurs
#!/bin/bash
# network-errors.sh

IFACE="eth0"

# Get stats
STATS=$(netstat -i | grep $IFACE)
RX_OK=$(echo $STATS | awk '{print $3}')
RX_ERR=$(echo $STATS | awk '{print $4}')
TX_OK=$(echo $STATS | awk '{print $7}')
TX_ERR=$(echo $STATS | awk '{print $8}')

# Calculate error rate
RX_TOTAL=$((RX_OK + RX_ERR))
TX_TOTAL=$((TX_OK + TX_ERR))

if [ $RX_TOTAL -gt 0 ]; then
    RX_ERR_RATE=$(echo "scale=4; $RX_ERR / $RX_TOTAL * 100" | bc)
    echo "RX Error Rate: $RX_ERR_RATE%"
fi

if [ $TX_TOTAL -gt 0 ]; then
    TX_ERR_RATE=$(echo "scale=4; $TX_ERR / $TX_TOTAL * 100" | bc)
    echo "TX Error Rate: $TX_ERR_RATE%"
fi

# Alert si taux erreur > 0.1%
if (( $(echo "$RX_ERR_RATE > 0.1" | bc -l) )); then
    echo "WARNING: High RX error rate!"
fi
```

---

## Section 8 : Monitoring Temps Réel

### 8.1 Monitoring Continu Linux

```bash
# Option -c (continuous)
netstat -tanc

# Rafraîchit automatiquement chaque seconde

# Watch command (plus flexible)
watch -n 1 'netstat -tan | head -20'

# Monitoring connexions établies
watch -n 1 'netstat -tan | grep ESTABLISHED | wc -l'

# Monitoring par programme
watch -n 1 'sudo netstat -tanp | grep nginx'

# Monitoring complet (dashboard)
watch -n 1 '
echo "=== Network Monitor ==="
echo ""
echo "Established: $(netstat -tan | grep -c ESTABLISHED)"
echo "Time Wait: $(netstat -tan | grep -c TIME_WAIT)"
echo "Listening: $(netstat -tln | grep -c LISTEN)"
echo ""
echo "Top 5 connections:"
netstat -tan | grep ESTABLISHED | awk "{print \$5}" | cut -d: -f1 | sort | uniq -c | sort -rn | head -5
'
```

### 8.2 Monitoring Continu Windows

```powershell
# PowerShell loop
while ($true) {
    Clear-Host
    Write-Host "=== Network Monitor - $(Get-Date) ===" -ForegroundColor Green
    Write-Host ""
    
    $established = (netstat -an | Select-String "ESTABLISHED").Count
    $listening = (netstat -an | Select-String "LISTENING").Count
    $timeWait = (netstat -an | Select-String "TIME_WAIT").Count
    
    Write-Host "Established: $established" -ForegroundColor Cyan
    Write-Host "Listening: $listening" -ForegroundColor Yellow
    Write-Host "Time Wait: $timeWait" -ForegroundColor Magenta
    
    Write-Host ""
    Write-Host "Recent connections:"
    netstat -an | Select-String "ESTABLISHED" | Select-Object -First 10
    
    Start-Sleep -Seconds 1
}

# Batch script simple
:loop
cls
echo === Network Monitor ===
echo.
netstat -an | find "ESTABLISHED"
timeout /t 1 >nul
goto loop
```

### 8.3 Logging et Historique

```bash
# Logger connexions dans fichier
#!/bin/bash
# netstat-logger.sh

LOG_FILE="/var/log/netstat-history.log"

while true; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Count states
    established=$(netstat -tan | grep -c ESTABLISHED)
    time_wait=$(netstat -tan | grep -c TIME_WAIT)
    close_wait=$(netstat -tan | grep -c CLOSE_WAIT)
    
    # Log
    echo "$timestamp | ESTABLISHED:$established | TIME_WAIT:$time_wait | CLOSE_WAIT:$close_wait" >> $LOG_FILE
    
    # Detailed snapshot every 5 min
    if [ $(($(date +%M) % 5)) -eq 0 ]; then
        echo "=== Snapshot $timestamp ===" >> $LOG_FILE
        sudo netstat -tanp >> $LOG_FILE
        echo "" >> $LOG_FILE
    fi
    
    sleep 60
done

# Analyser logs
# Connexions pic
grep ESTABLISHED /var/log/netstat-history.log | sort -t: -k2 -rn | head -1

# Tendance TIME_WAIT
grep TIME_WAIT /var/log/netstat-history.log | tail -60 | awk -F: '{print $2}'
```

---

## Section 9 : Troubleshooting Réseau

### 9.1 Service Pas Accessible

```bash
# Problème : Service HTTP (port 80) inaccessible

# Étape 1 : Vérifier service écoute
sudo netstat -tlnp | grep :80

# Si vide → Service pas démarré
# Action : sudo systemctl start nginx

# Si présent :
tcp  0.0.0.0:80  LISTEN  1234/nginx
# → Service écoute, continuer diagnostic

# Étape 2 : Tester local
curl http://localhost

# Si fonctionne → Problème pas application
# Si échoue → Problème application

# Étape 3 : Vérifier firewall
sudo iptables -L -n | grep 80
sudo ufw status | grep 80

# Si bloqué → Ouvrir port
sudo ufw allow 80

# Étape 4 : Tester depuis distant
curl http://<server-ip>

# Si échoue → Problème réseau/firewall
# Si fonctionne → Problème client

# Étape 5 : Vérifier connexions actives
sudo netstat -tanp | grep :80

# Voir si connexions arrivent
# Si aucune connexion → Problème routage/firewall

# Diagnostic complet automatisé
#!/bin/bash
# service-diagnostic.sh <port>

PORT=$1

echo "=== Service Diagnostic Port $PORT ==="
echo ""

echo "1. Listening?"
if sudo netstat -tln | grep -q ":$PORT "; then
    echo "✓ Service listening on port $PORT"
    sudo netstat -tlnp | grep ":$PORT "
else
    echo "✗ No service listening on port $PORT"
    exit 1
fi

echo ""
echo "2. Firewall?"
if sudo iptables -L -n | grep -q "$PORT"; then
    echo "✓ Firewall rule exists for port $PORT"
else
    echo "⚠ No firewall rule for port $PORT"
fi

echo ""
echo "3. Active connections?"
conn_count=$(netstat -tan | grep ":$PORT " | grep ESTABLISHED | wc -l)
echo "$conn_count active connections on port $PORT"

echo ""
echo "4. Local test?"
if curl -s --connect-timeout 2 http://localhost:$PORT >/dev/null; then
    echo "✓ Local connection successful"
else
    echo "✗ Local connection failed"
fi
```

### 9.2 Performance Dégradée

```bash
# Problème : Site web lent

# Diagnostic 1 : Trop de connexions?
netstat -tan | grep ESTABLISHED | wc -l

# Si > 1000 → Possible surcharge
# Action : Augmenter worker processes/threads

# Diagnostic 2 : Connexions bloquées?
netstat -tan | grep CLOSE_WAIT | wc -l

# Si > 100 → Leak connexions application
# Action : Fix code (close sockets), restart app

# Diagnostic 3 : Ports épuisés?
netstat -tan | grep TIME_WAIT | wc -l

# Si > 5000 → Épuisement ports éphémères
# Action : Connection pooling, ajuster kernel

sudo sysctl -w net.ipv4.ip_local_port_range="10000 65535"
sudo sysctl -w net.ipv4.tcp_tw_reuse=1

# Diagnostic 4 : Retransmissions?
netstat -s | grep retransmit

# Output :
# 1234 segments retransmitted

# Si élevé → Problème réseau (perte paquets)
# Action : Vérifier câbles, switch, MTU

# Diagnostic 5 : Erreurs interfaces?
netstat -i

# Si RX-ERR, TX-ERR > 0 → Problème hardware
# Action : Vérifier câble, remplacer carte réseau

# Script diagnostic performance
#!/bin/bash
# network-performance-check.sh

echo "=== Network Performance Check ==="
echo ""

# Connections
ESTABLISHED=$(netstat -tan | grep -c ESTABLISHED)
TIME_WAIT=$(netstat -tan | grep -c TIME_WAIT)
CLOSE_WAIT=$(netstat -tan | grep -c CLOSE_WAIT)

echo "Connections:"
echo "  ESTABLISHED: $ESTABLISHED"
echo "  TIME_WAIT: $TIME_WAIT $([ $TIME_WAIT -gt 1000 ] && echo '⚠ HIGH')"
echo "  CLOSE_WAIT: $CLOSE_WAIT $([ $CLOSE_WAIT -gt 50 ] && echo '⚠ LEAK?')"

echo ""

# Retransmissions
RETRANS=$(netstat -s | grep retransmit | awk '{print $1}')
echo "TCP Retransmissions: $RETRANS"

echo ""

# Interface errors
echo "Interface Errors:"
netstat -i | grep -v "Iface" | while read line; do
    iface=$(echo $line | awk '{print $1}')
    rx_err=$(echo $line | awk '{print $4}')
    tx_err=$(echo $line | awk '{print $8}')
    
    if [ $rx_err -gt 0 ] || [ $tx_err -gt 0 ]; then
        echo "  $iface: RX-ERR=$rx_err TX-ERR=$tx_err ⚠"
    fi
done
```

### 9.3 Connexion Bloquée

```bash
# Problème : Impossible se connecter serveur distant

# Étape 1 : Vérifier connexion existe
netstat -tan | grep <server-ip>

# Si vide → Connexion jamais établie
# Si SYN_SENT → Connexion en cours (bloquée)

# Étape 2 : Timeout connexion
netstat -tan | grep <server-ip>:<port>

# Si SYN_SENT persiste > 30s → Serveur injoignable
# Causes : Firewall, serveur down, routage

# Étape 3 : Test basique
ping <server-ip>
# Si échoue → Problème réseau
# Si fonctionne → Problème port spécifique

# Étape 4 : Test port
telnet <server-ip> <port>
# ou
nc -zv <server-ip> <port>

# Si échoue → Firewall bloque port

# Étape 5 : Vérifier routage
netstat -rn | grep <server-ip>
traceroute <server-ip>

# Diagnostic script
#!/bin/bash
# connection-diagnostic.sh <host> <port>

HOST=$1
PORT=$2

echo "=== Connection Diagnostic $HOST:$PORT ==="
echo ""

echo "1. Ping test:"
if ping -c 3 -W 2 $HOST >/dev/null 2>&1; then
    echo "✓ Host reachable"
else
    echo "✗ Host unreachable"
    exit 1
fi

echo ""
echo "2. Port test:"
if timeout 5 bash -c "</dev/tcp/$HOST/$PORT" 2>/dev/null; then
    echo "✓ Port $PORT open"
else
    echo "✗ Port $PORT closed/filtered"
fi

echo ""
echo "3. Active connection?"
if netstat -tan | grep -q "$HOST:$PORT"; then
    echo "✓ Connection exists:"
    netstat -tan | grep "$HOST:$PORT"
else
    echo "⚠ No active connection"
fi

echo ""
echo "4. Route:"
netstat -rn | grep -A 5 "Destination"
```

---

## Section 10 : Security et Détection Intrusions

### 10.1 Détecter Backdoors

```bash
# Backdoors = Ports suspects en écoute

# Ports légitimes communs :
# 22    SSH
# 80    HTTP
# 443   HTTPS
# 25    SMTP
# 3306  MySQL (localhost only)

# Ports suspects (backdoors communs) :
# 31337  Elite/leet (backdoor classique)
# 4444   Metasploit default
# 5555   Android ADB (si pas dev)
# 6667   IRC (botnet C2)
# 12345  NetBus
# 27374  SubSeven
# 65535  RC5/Back Orifice

# Scanner ports suspects
sudo netstat -tlnp | grep -E ':(31337|4444|5555|6667|12345|27374|65535) '

# Si trouvé → INVESTIGATION IMMÉDIATE

# Exemple backdoor détecté :
tcp  0.0.0.0:31337  LISTEN  6666/suspicious

# Actions :
# 1. Identifier process
ps aux | grep 6666
lsof -p 6666

# 2. Binaire suspect
ls -la /proc/6666/exe

# 3. Kill process
sudo kill -9 6666

# 4. Analyser binaire
file /proc/6666/exe
strings /proc/6666/exe

# 5. Scanner malware
clamscan /proc/6666/exe

# Script détection automatique
#!/bin/bash
# backdoor-scan.sh

SUSPECT_PORTS=(31337 4444 5555 6667 12345 27374 65535)

echo "=== Backdoor Port Scan ==="
echo ""

for port in "${SUSPECT_PORTS[@]}"; do
    result=$(sudo netstat -tlnp | grep ":$port ")
    
    if [ -n "$result" ]; then
        echo "⚠️ ALERT: Suspect port $port listening!"
        echo "$result"
        echo ""
        
        # Get PID
        pid=$(echo $result | awk '{print $7}' | cut -d/ -f1)
        
        echo "Process details:"
        ps aux | grep $pid
        echo ""
        
        # Send alert
        echo "Suspect port $port detected on $(hostname)" | mail -s "SECURITY ALERT" admin@example.com
    fi
done
```

### 10.2 Détecter Connexions Malveillantes

```bash
# Connexions suspectes sortantes

# Destinations légitimes :
# 80/443 : Web (CDN, APIs)
# 22 : SSH (admin servers)
# 25 : SMTP (email)

# Destinations suspectes :
# Ports hauts aléatoires (malware C2)
# IPs géographiques inhabituelles
# Trafic constant vers même IP

# Lister connexions sortantes
netstat -tan | grep ESTABLISHED | grep -v ":80\|:443\|:22"

# Grouper par IP destination
netstat -tan | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn

# Output :
#  50 93.184.216.34   # Normal (CDN)
# 100 185.XXX.XXX.XXX # SUSPECT (trop connexions IP inconnue)

# Vérifier IP suspecte
whois 185.XXX.XXX.XXX
# Si pays suspect (connu malware) → Investigation

# Identifier programme
sudo netstat -tanp | grep 185.XXX.XXX.XXX

# Output :
tcp  192.168.1.10:52341  185.XXX.XXX.XXX:8080  ESTABLISHED  6666/malware

# Script détection connexions suspectes
#!/bin/bash
# suspicious-connections.sh

# Threshold connexions vers même IP
THRESHOLD=50

echo "=== Suspicious Connection Detector ==="
echo ""

# Top IPs
netstat -tan | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | while read count ip; do
    if [ $count -gt $THRESHOLD ]; then
        echo "⚠️ ALERT: $count connections to $ip"
        
        # Get programs
        sudo netstat -tanp | grep $ip | awk '{print $7}' | sort -u
        
        # Whois
        echo "Whois: $(whois $ip | grep -i country)"
        echo ""
    fi
done

# Connexions vers ports non-standards
echo "Non-standard port connections:"
netstat -tan | grep ESTABLISHED | grep -vE ':(80|443|22|25|53) ' | head -10
```

### 10.3 Forensique Post-Incident

```bash
# Scénario : Serveur compromis, collecter preuves

# 1. Snapshot connexions actives
sudo netstat -tanp > /tmp/netstat-$(date +%Y%m%d-%H%M%S).txt

# 2. Ports en écoute
sudo netstat -tulnp > /tmp/listening-$(date +%Y%m%d-%H%M%S).txt

# 3. Connexions établies détaillées
sudo netstat -tanp | grep ESTABLISHED > /tmp/established-$(date +%Y%m%d-%H%M%S).txt

# 4. Statistiques (retransmissions = exfiltration?)
netstat -s > /tmp/stats-$(date +%Y%m%d-%H%M%S).txt

# 5. Table routage (backdoor route?)
netstat -rn > /tmp/routes-$(date +%Y%m%d-%H%M%S).txt

# 6. Timeline connexions (si logs activés)
grep "netstat" /var/log/syslog > /tmp/netstat-history.txt

# 7. Corréler avec process list
ps aux > /tmp/processes-$(date +%Y%m%d-%H%M%S).txt

# 8. Network interfaces (sniffer?)
netstat -i > /tmp/interfaces-$(date +%Y%m%d-%H%M%S).txt

# Script forensique complet
#!/bin/bash
# network-forensics.sh

EVIDENCE_DIR="/tmp/forensics-$(date +%Y%m%d-%H%M%S)"
mkdir -p $EVIDENCE_DIR

echo "=== Network Forensics Collection ==="
echo "Evidence directory: $EVIDENCE_DIR"
echo ""

# Collect data
echo "Collecting active connections..."
sudo netstat -tanp > $EVIDENCE_DIR/active-connections.txt

echo "Collecting listening ports..."
sudo netstat -tulnp > $EVIDENCE_DIR/listening-ports.txt

echo "Collecting statistics..."
netstat -s > $EVIDENCE_DIR/statistics.txt

echo "Collecting routing table..."
netstat -rn > $EVIDENCE_DIR/routing-table.txt

echo "Collecting interface stats..."
netstat -i > $EVIDENCE_DIR/interfaces.txt

echo "Collecting process list..."
ps auxf > $EVIDENCE_DIR/processes.txt

echo "Collecting open files..."
sudo lsof -i > $EVIDENCE_DIR/open-files.txt 2>/dev/null

echo "Analyzing suspicious connections..."
{
    echo "=== Suspicious Ports ==="
    sudo netstat -tlnp | grep -E ':(31337|4444|5555|6667|12345) '
    echo ""
    echo "=== Non-standard Connections ==="
    netstat -tan | grep ESTABLISHED | grep -vE ':(80|443|22|25) '
    echo ""
    echo "=== High Connection Count IPs ==="
    netstat -tan | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -20
} > $EVIDENCE_DIR/suspicious-analysis.txt

# Create archive
tar -czf $EVIDENCE_DIR.tar.gz -C /tmp $(basename $EVIDENCE_DIR)

echo ""
echo "✓ Forensics collection complete"
echo "Archive: $EVIDENCE_DIR.tar.gz"
```

---

## Section 11 : Comparaison ss/lsof/sockstat

### 11.1 netstat vs ss (Linux)

```bash
# ss = Socket Statistics (remplacement moderne netstat)

# Avantages ss :
# ✅ Plus rapide (kernel direct, pas /proc)
# ✅ Plus d'informations (TCP internals)
# ✅ Filtrage puissant
# ✅ Activement maintenu

# netstat
netstat -tan

# ss équivalent
ss -tan

# Output similaire mais ss plus rapide

# Exemples ss :

# Connexions TCP
ss -t

# Listening ports
ss -tl

# Avec PID (sudo)
sudo ss -tlnp

# Filtres puissants ss
# Connexions vers port 80
ss -tan dst :80

# Connexions depuis IP
ss -tan src 192.168.1.10

# Connexions établies
ss -tan state established

# États TCP
ss -tan state time-wait
ss -tan state close-wait

# Statistiques socket
ss -s

# Output :
# Total: 1234
# TCP:   567 (estab 234, closed 123, orphaned 0, timewait 100)
# UDP:   45

# ss plus performant serveurs haute charge
# Benchmark :
time netstat -tan | wc -l
time ss -tan | wc -l
# ss ~10x plus rapide
```

### 11.2 netstat vs lsof

```bash
# lsof = List Open Files (inclut sockets réseau)

# Avantages lsof :
# ✅ Voir TOUS fichiers ouverts (pas seulement réseau)
# ✅ Détails process complets
# ✅ Filtrage flexible
# ❌ Plus lent que netstat/ss

# netstat : Connexions réseau
sudo netstat -tanp | grep :80

# lsof équivalent : Files réseau
sudo lsof -i :80

# Output lsof (plus détaillé) :
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx   1234 www   6u  IPv4  12345      0t0  TCP *:80 (LISTEN)

# Exemples lsof :

# Tous sockets réseau
sudo lsof -i

# TCP seulement
sudo lsof -i TCP

# Port spécifique
sudo lsof -i :3306

# Process spécifique
sudo lsof -p 1234

# User spécifique
sudo lsof -u www-data

# Combiner filtres
sudo lsof -i TCP -a -u www-data

# Fichiers ET réseau process
sudo lsof -p 1234
# Montre fichiers config, logs, sockets

# Trouver process utilisant port
sudo lsof -t -i :80
# Output : 1234 (PID seulement)

# Kill process utilisant port
sudo kill $(sudo lsof -t -i :80)
```

### 11.3 Comparaison Synthétique

| Feature | netstat | ss | lsof |
|---------|---------|-----|------|
| **Performance** | Moyen | Rapide | Lent |
| **Connexions réseau** | ✅ | ✅ | ✅ |
| **Ports écoute** | ✅ | ✅ | ✅ |
| **Tables routage** | ✅ | ❌ | ❌ |
| **Statistiques** | ✅ | ✅ | ❌ |
| **Filtrage** | Basique | Avancé | Très flexible |
| **Fichiers ouverts** | ❌ | ❌ | ✅ |
| **Process details** | Basique | Basique | Complet |
| **Maintenance** | Déprécié Linux | Moderne | Actif |
| **Disponibilité** | Universel | Linux | Unix/Linux/macOS |

**Recommandation usage :**
- **netstat** : Débutants, Windows, cross-platform scripts
- **ss** : Linux moderne, performance, serveurs production
- **lsof** : Debugging approfondi, forensique, files + network

```bash
# Cheatsheet équivalences

# Connexions actives
netstat -tan
ss -tan
sudo lsof -i -nP

# Ports écoute
netstat -tln
ss -tln
sudo lsof -i -nP | grep LISTEN

# Avec programmes
sudo netstat -tlnp
sudo ss -tlnp
sudo lsof -i -nP

# Port spécifique
netstat -tan | grep :80
ss -tan dst :80
sudo lsof -i :80

# Stats
netstat -s
ss -s
# lsof : N/A
```

---

## Section 12 : Cas Pratiques Production

### 12.1 Audit Sécurité Serveur

```bash
#!/bin/bash
# server-security-audit.sh - Audit complet réseau serveur

echo "=== Server Network Security Audit ==="
echo "Date: $(date)"
echo "Host: $(hostname)"
echo ""

# 1. Ports exposés Internet
echo "=== Exposed Ports ==="
sudo netstat -tlnp | grep "0.0.0.0" | grep -v "127.0.0.1"

# Vérifier ports dangereux exposés
DANGER_PORTS=(3306 5432 6379 27017 9200 11211)
for port in "${DANGER_PORTS[@]}"; do
    if sudo netstat -tln | grep -q "0.0.0.0:$port "; then
        echo "⚠️ WARNING: Port $port exposed!"
    fi
done

echo ""

# 2. Connexions sortantes suspectes
echo "=== Outbound Connections ==="
netstat -tan | grep ESTABLISHED | grep -vE ':(80|443|22|25|53) ' | head -10

echo ""

# 3. Ports hauts suspects (backdoors)
echo "=== High Port Listeners ==="
sudo netstat -tlnp | awk '$4 ~ /:([5-6][0-9]{4})$/ {print}'

echo ""

# 4. Connexions multiples même IP
echo "=== High Connection Count IPs ==="
netstat -tan | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -10

echo ""

# 5. États problématiques
echo "=== Connection States ==="
echo "CLOSE_WAIT: $(netstat -tan | grep -c CLOSE_WAIT)"
echo "TIME_WAIT: $(netstat -tan | grep -c TIME_WAIT)"
echo "SYN_RECV: $(netstat -tan | grep -c SYN_RECV)"

echo ""

# 6. Services inattendus
echo "=== Unexpected Services ==="
sudo netstat -tlnp | grep -v -E ':(22|80|443) ' | grep LISTEN

echo ""

# 7. Recommandations
echo "=== Security Recommendations ==="
echo "- Close unused ports"
echo "- Bind services to localhost if not needed externally"
echo "- Enable firewall (ufw/iptables)"
echo "- Monitor CLOSE_WAIT/TIME_WAIT counts"
echo "- Investigate high connection count IPs"
```

### 12.2 Troubleshooting Production

```bash
#!/bin/bash
# webapp-troubleshoot.sh - Debug web app performance

APP_PORT=8080

echo "=== Web Application Troubleshooting ==="
echo ""

# 1. Service running?
echo "1. Service Status:"
if sudo netstat -tlnp | grep -q ":$APP_PORT "; then
    echo "✓ Application listening on port $APP_PORT"
    sudo netstat -tlnp | grep ":$APP_PORT "
else
    echo "✗ Application NOT listening"
    echo "Action: Start application service"
    exit 1
fi

echo ""

# 2. Active connections
echo "2. Active Connections:"
CONN_COUNT=$(netstat -tan | grep ":$APP_PORT " | grep ESTABLISHED | wc -l)
echo "Active connections: $CONN_COUNT"

if [ $CONN_COUNT -gt 1000 ]; then
    echo "⚠️ High connection count (>1000)"
    echo "Consider: Increase worker processes/threads"
fi

echo ""

# 3. Connection states
echo "3. Connection States:"
netstat -tan | grep ":$APP_PORT " | awk '{print $6}' | sort | uniq -c | sort -rn

echo ""

# 4. CLOSE_WAIT leak?
CLOSE_WAIT=$(netstat -tan | grep ":$APP_PORT " | grep -c CLOSE_WAIT)
echo "4. CLOSE_WAIT Count: $CLOSE_WAIT"

if [ $CLOSE_WAIT -gt 50 ]; then
    echo "⚠️ Connection leak detected!"
    echo "Action: Fix application close() calls, restart service"
fi

echo ""

# 5. TIME_WAIT buildup?
TIME_WAIT=$(netstat -tan | grep ":$APP_PORT " | grep -c TIME_WAIT)
echo "5. TIME_WAIT Count: $TIME_WAIT"

if [ $TIME_WAIT -gt 2000 ]; then
    echo "⚠️ Port exhaustion risk!"
    echo "Action: Enable tcp_tw_reuse, connection pooling"
fi

echo ""

# 6. Network errors
echo "6. Network Errors:"
netstat -s | grep -E "(retransmit|failed)"

echo ""

# 7. Top client IPs
echo "7. Top 10 Client IPs:"
netstat -tan | grep ":$APP_PORT " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -10
```

### 12.3 Monitoring Production

```bash
#!/bin/bash
# network-monitor-daemon.sh - Production monitoring

LOG_FILE="/var/log/network-monitor.log"
ALERT_EMAIL="admin@example.com"

# Thresholds
MAX_ESTABLISHED=1000
MAX_TIME_WAIT=3000
MAX_CLOSE_WAIT=100

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a $LOG_FILE
}

send_alert() {
    local subject="$1"
    local message="$2"
    
    echo "$message" | mail -s "[$HOSTNAME] $subject" $ALERT_EMAIL
    log "ALERT: $subject"
}

check_states() {
    local established=$(netstat -tan | grep -c ESTABLISHED)
    local time_wait=$(netstat -tan | grep -c TIME_WAIT)
    local close_wait=$(netstat -tan | grep -c CLOSE_WAIT)
    
    log "States: ESTABLISHED=$established TIME_WAIT=$time_wait CLOSE_WAIT=$close_wait"
    
    # Alerts
    if [ $established -gt $MAX_ESTABLISHED ]; then
        send_alert "High Connection Count" "ESTABLISHED: $established (threshold: $MAX_ESTABLISHED)"
    fi
    
    if [ $time_wait -gt $MAX_TIME_WAIT ]; then
        send_alert "TIME_WAIT Buildup" "TIME_WAIT: $time_wait (threshold: $MAX_TIME_WAIT)"
    fi
    
    if [ $close_wait -gt $MAX_CLOSE_WAIT ]; then
        send_alert "Connection Leak Detected" "CLOSE_WAIT: $close_wait (threshold: $MAX_CLOSE_WAIT)

Check application close() calls."
    fi
}

check_suspicious() {
    # Backdoor ports
    if sudo netstat -tln | grep -qE ':(31337|4444|5555|6667) '; then
        send_alert "SECURITY: Backdoor Port Detected" "$(sudo netstat -tlnp | grep -E ':(31337|4444|5555|6667) ')"
    fi
    
    # High connection single IP
    local top_ip=$(netstat -tan | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -1)
    local count=$(echo $top_ip | awk '{print $1}')
    
    if [ $count -gt 100 ]; then
        send_alert "High Connections from Single IP" "$top_ip"
    fi
}

# Main loop
log "Network monitor started"

while true; do
    check_states
    check_suspicious
    sleep 60
done
```

### 12.4 Capacity Planning

```bash
#!/bin/bash
# network-capacity-analysis.sh - Analyser capacité réseau

DURATION=3600  # 1 hour
INTERVAL=60    # 1 minute

OUTPUT_FILE="capacity-report-$(date +%Y%m%d-%H%M%S).csv"

echo "timestamp,established,time_wait,close_wait,listening" > $OUTPUT_FILE

echo "=== Network Capacity Analysis ==="
echo "Duration: $DURATION seconds"
echo "Interval: $INTERVAL seconds"
echo "Output: $OUTPUT_FILE"
echo ""

for ((i=0; i<$DURATION; i+=$INTERVAL)); do
    timestamp=$(date +%s)
    established=$(netstat -tan | grep -c ESTABLISHED)
    time_wait=$(netstat -tan | grep -c TIME_WAIT)
    close_wait=$(netstat -tan | grep -c CLOSE_WAIT)
    listening=$(netstat -tln | grep -c LISTEN)
    
    echo "$timestamp,$established,$time_wait,$close_wait,$listening" >> $OUTPUT_FILE
    
    echo "[$(date +'%H:%M:%S')] ESTABLISHED:$established TIME_WAIT:$time_wait CLOSE_WAIT:$close_wait"
    
    sleep $INTERVAL
done

# Analyse
echo ""
echo "=== Analysis ==="

# Peak connections
peak=$(cat $OUTPUT_FILE | cut -d, -f2 | sort -rn | head -1)
echo "Peak ESTABLISHED: $peak"

# Average
avg=$(cat $OUTPUT_FILE | cut -d, -f2 | awk '{sum+=$1; count++} END {print sum/count}')
echo "Average ESTABLISHED: $avg"

# Recommendations
echo ""
echo "=== Recommendations ==="

if (( $(echo "$peak > 1000" | bc -l) )); then
    echo "- Consider scaling horizontally (add servers)"
    echo "- Increase worker processes/threads"
fi

if (( $(echo "$avg > 500" | bc -l) )); then
    echo "- Enable connection pooling"
    echo "- Optimize application response time"
fi

# Generate graph (requires gnuplot)
if command -v gnuplot &>/dev/null; then
    gnuplot << EOF
set terminal png size 1200,600
set output "capacity-graph.png"
set datafile separator ","
set xdata time
set timefmt "%s"
set format x "%H:%M"
set xlabel "Time"
set ylabel "Connections"
set title "Network Capacity Analysis"
set grid
plot "$OUTPUT_FILE" using 1:2 with lines title "ESTABLISHED", \
     "$OUTPUT_FILE" using 1:3 with lines title "TIME_WAIT"
EOF
    echo "Graph generated: capacity-graph.png"
fi
```

---

## Ressources et Références

**Documentation officielle :**

- Linux man page : `man netstat`
- Windows netstat : https://docs.microsoft.com/windows-server/administration/windows-commands/netstat
- TCP/IP Guide : https://www.ietf.org/rfc/rfc793.txt

**Alternatives modernes :**

- ss : https://man7.org/linux/man-pages/man8/ss.8.html
- lsof : https://linux.die.net/man/8/lsof
- sockstat : https://www.freebsd.org/cgi/man.cgi?sockstat

**Learning resources :**

- TCP State Machine : https://www.rfc-editor.org/rfc/rfc793
- Network troubleshooting : https://www.redhat.com/sysadmin/
- Security monitoring : https://www.sans.org/

**Tools complémentaires :**

- tcpdump : Capture paquets réseau
- wireshark : Analyse protocoles
- nmap : Scan ports réseau
- iftop : Monitoring bande passante temps réel

---

## Conclusion

**netstat = Outil monitoring réseau fondamental**

**Points clés maîtrisés :**

✅ **Connexions actives** = Voir toutes connexions TCP/UDP temps réel
✅ **Ports écoute** = Identifier services exposés vs locaux
✅ **États TCP** = Comprendre ESTABLISHED, TIME_WAIT, CLOSE_WAIT
✅ **Troubleshooting** = Diagnostiquer problèmes réseau/performance
✅ **Security** = Détecter backdoors, connexions suspectes
✅ **Statistiques** = Analyser performance réseau (retransmissions, erreurs)
✅ **Forensique** = Collecter preuves post-incident
✅ **Production** = Monitoring continu, alerting, capacity planning

**Ordre apprentissage :**

```
1. Connexions basiques (netstat -tan)
2. Ports écoute (netstat -tln)
3. Programmes (-p flag)
4. États TCP (comprendre lifecycle)
5. Troubleshooting (leak connexions)
6. Security (backdoors, anomalies)
7. Automation (scripts monitoring)
8. Production (alerting, forensique)
```

**Progression stack réseau :**

1. nslookup    ✅ DNS resolution
2. netstat     ✅ Connexions monitoring (actuel)
3. tcpdump     → Capture paquets (prochain)
4. scapy       → Manipulation paquets (avancé)

**Use cases critiques :**

1. **Administration** : Vérifier services, troubleshoot réseau
2. **Security** : Détecter backdoors, connexions malveillantes
3. **Performance** : Analyser leak connexions, capacity planning
4. **Forensique** : Reconstituer communications incident
5. **Pentest** : Enumeration ports, détection services

**Tu maîtrises maintenant netstat du monitoring basique à la forensique avancée !** 📊

**Prochaine étape recommandée : tcpdump (capture et analyse paquets réseau)** 🎯

---

_Version 1.0 | Dernière mise à jour : 2024-01-16_

Voilà le guide complet netstat ! Il couvre **12 sections** :

✅ Introduction et concepts réseau (TCP/IP, ports, états TCP)  
✅ Syntaxe et options (Linux vs Windows)  
✅ Connexions actives TCP/UDP  
✅ Ports en écoute (exposés vs locaux)  
✅ États connexions TCP (ESTABLISHED, TIME_WAIT, CLOSE_WAIT)  
✅ Tables de routage  
✅ Statistiques interfaces réseau  
✅ Monitoring temps réel  
✅ Troubleshooting (service inaccessible, performance, leak connexions)  
✅ Security (backdoors, connexions malveillantes, forensique)  
✅ Comparaison ss/lsof  
✅ Cas pratiques production (audit, monitoring, capacity planning)  

**C'est production-ready avec scripts automation complets !** 🚀