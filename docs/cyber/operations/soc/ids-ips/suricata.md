---
description: "Suricata — IDS/IPS open-source haute performance : installation, configuration, écriture de règles .rules, modes IDS/IPS et intégration avec Wazuh."
icon: lucide/book-open-check
tags: ["SURICATA", "IDS", "IPS", "RÉSEAU", "RÈGLES", "WAZUH", "SOC"]
---

# Suricata — IDS/IPS Open-Source

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Suricata 7.x"
  data-time="~3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Scanner de Bagages à l'Aéroport"
    À l'aéroport, chaque bagage passe dans un scanner qui compare son contenu à une base de **profils d'objets dangereux** connus (armes, explosifs). Si un match est trouvé, l'alarme sonne. Suricata fait exactement cela avec les **paquets réseau** : chaque paquet est analysé et comparé à des milliers de signatures d'attaques. Et comme le scanner moderne détecte aussi les comportements suspects (forme inhabituelle, densité anormale), Suricata analyse également les **anomalies de protocoles**.

**Suricata** est le moteur IDS/IPS open-source le plus performant disponible. Développé par la fondation OISF, il se distingue par :

- Sa capacité **multi-thread** (exploit de tous les cœurs CPU)
- Son analyse complète des protocoles (HTTP, DNS, TLS, SSH, SMB...)
- Sa compatibilité native avec les **règles Emerging Threats**
- Son format de sortie **EVE JSON** — ingérable directement par Wazuh, Elastic, Splunk
- Sa capacité à fonctionner en **mode IDS passif ou IPS inline**

<br>

---

## Installation

```bash title="Installation Suricata 7.x — Ubuntu 22.04"
# 1. Ajouter le PPA officiel OISF
add-apt-repository ppa:oisf/suricata-stable
apt-get update

# 2. Installer Suricata
apt-get install -y suricata suricata-update

# 3. Vérifier la version installée
suricata --build-info | grep "Version"

# 4. Mise à jour des règles Emerging Threats (gratuit)
suricata-update

# 5. Activer et démarrer le service
systemctl enable --now suricata

# 6. Vérifier que Suricata est actif
systemctl status suricata
```

<br>

---

## Configuration principale

Le fichier de configuration central est `/etc/suricata/suricata.yaml`.

```yaml title="/etc/suricata/suricata.yaml — Paramètres essentiels"
# ===========================================================================
# Variables réseau — CRITIQUE : adapter à votre réseau
# ===========================================================================
vars:
  address-groups:
    # Définir votre réseau interne (LAN)
    HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"
    # Tout le reste = externe
    EXTERNAL_NET: "!$HOME_NET"

    # Serveurs exposés (pour cibler les règles)
    HTTP_SERVERS: "$HOME_NET"
    DNS_SERVERS: "$HOME_NET"
    SQL_SERVERS: "$HOME_NET"

  port-groups:
    HTTP_PORTS: "80"
    HTTPS_PORTS: "443"
    SSH_PORTS: "22"

# ===========================================================================
# Interface réseau à surveiller — adapter à votre interface
# ===========================================================================
af-packet:
  - interface: eth0        # Remplacer par votre interface (ip a pour vérifier)
    cluster-id: 99
    cluster-type: cluster_flow
    defrag: yes
    use-mmap: yes          # Améliore les performances
    tpacket-v3: yes

# ===========================================================================
# Format de sortie EVE JSON — pour intégration Wazuh/SIEM
# ===========================================================================
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      # Chemin du fichier de log principal (ingéré par l'agent Wazuh)
      filename: /var/log/suricata/eve.json
      # Types d'événements à logger
      types:
        - alert:
            payload: yes           # Inclure le payload brut (déchiffrable)
            payload-buffer-size: 4kb
            metadata: yes
        - http:
            extended: yes          # Headers HTTP complets
        - dns:
            query: yes             # Requêtes DNS
            answer: yes            # Réponses DNS
        - tls:
            extended: yes          # Détails certificats TLS
        - files:
            force-magic: yes       # Type MIME des fichiers transférés
        - ssh                      # Sessions SSH
        - flow                     # Métadonnées de flux réseau
        - stats:
            totals: yes

# ===========================================================================
# Règles à charger
# ===========================================================================
rule-files:
  - suricata.rules               # Règles Emerging Threats (auto-gérées)
  - /etc/suricata/rules/local.rules  # Vos règles personnalisées
```

_La variable `HOME_NET` est **critique** : une valeur incorrecte désactive des dizaines de règles ou génère des milliers de faux positifs. Vérifiez deux fois votre plage réseau._

<br>

---

## Écriture de règles Suricata

### Structure d'une règle

```
action protocole src_ip src_port -> dst_ip dst_port (options;)
```

### Exemples pratiques

```bash title="/etc/suricata/rules/local.rules — Règles SOC personnalisées"
# ===========================================================================
# Règle 1 : Détection d'un scan de ports Nmap (SYN scan)
# ===========================================================================
# alert   = lever une alerte (ne pas bloquer)
# tcp     = protocole TCP
# any any = toute IP source, tout port source
# ->      = direction : vers
# $HOME_NET any = vers notre réseau, tout port
alert tcp any any -> $HOME_NET any (
    msg:"SCAN Nmap SYN Scan détecté";
    flags:S;                    # Paquet SYN uniquement (sans ACK = scan)
    threshold:type threshold, track by_src, count 20, seconds 2;
    classtype:attempted-recon;  # Classification MITRE : reconnaissance
    sid:9000001;                # ID unique de la règle
    rev:1;                      # Version de la règle
)

# ===========================================================================
# Règle 2 : Détection d'exfiltration DNS (tunneling)
# ===========================================================================
# Les tunnels DNS utilisent des sous-domaines très longs pour exfiltrer des données
alert dns any any -> any 53 (
    msg:"POSSIBLE Tunneling DNS — sous-domaine anormalement long";
    dns.query;
    pcre:"/^[a-zA-Z0-9+\/]{50,}\./";  # Sous-domaine > 50 chars (base64-like)
    classtype:policy-violation;
    sid:9000002;
    rev:1;
)

# ===========================================================================
# Règle 3 : Connexion vers un C2 connu (Cobalt Strike)
# ===========================================================================
# Exemple de beacon Cobalt Strike (pattern JA3 de fingerprint TLS)
alert tls any any -> any any (
    msg:"CRITICAL Possible Cobalt Strike beacon — JA3 fingerprint connu";
    ja3.hash; content:"72a589da586844d7f0818ce684948eea"; # JA3 hash CS
    classtype:trojan-activity;
    sid:9000003;
    rev:2;
)

# ===========================================================================
# Règle 4 : Téléchargement d'un exécutable Windows via HTTP non-HTTPS
# ===========================================================================
alert http $EXTERNAL_NET any -> $HOME_NET any (
    msg:"INFO Téléchargement exécutable Windows en clair (HTTP)";
    http.uri;
    content:".exe"; nocase; endswith; # URI se termine par .exe
    classtype:policy-violation;
    sid:9000004;
    rev:1;
)
```

_La directive `threshold` sur la règle 1 évite le flood d'alertes : Suricata n'alerte qu'une fois si 20 paquets SYN arrivent de la même source en 2 secondes, plutôt que de générer 20 alertes._

<br>

---

## Modes IDS vs IPS

### Mode IDS (passif — défaut)

Suricata reçoit une **copie du trafic** via un port SPAN ou un TAP réseau. Il ne peut pas bloquer, seulement alerter.

```bash title="Lancer Suricata en mode IDS sur l'interface eth0"
# Démarrage en mode IDS (lecture seule)
suricata -i eth0 --pidfile /var/run/suricata.pid -D

# Vérifier que les alertes arrivent
tail -f /var/log/suricata/eve.json | python3 -m json.tool | grep '"event_type":"alert"'
```

### Mode IPS (inline — bloquant)

Suricata est positionné **sur le chemin du trafic** via NFQueue (Linux) ou WinDivert (Windows). Il peut bloquer les paquets en temps réel.

```bash title="Configuration IPS via NFQueue — iptables"
# Rediriger le trafic entrant vers Suricata (NFQueue 0)
iptables -I FORWARD -j NFQUEUE --queue-num 0

# Lancer Suricata en mode IPS
suricata -q 0 --pidfile /var/run/suricata.pid -D

# IMPORTANT : transformer les règles "alert" en "drop" pour le blocage
# Dans les règles, remplacer "alert" par "drop" pour bloquer activement
```

!!! warning "IPS en production"
    Avant de passer en mode IPS, testez en mode IDS pendant **au moins 2 semaines** pour identifier et supprimer les faux positifs. Une règle IPS mal calibrée peut bloquer du trafic légitime et causer une interruption de service.

<br>

---

## Intégration avec Wazuh

Wazuh ingère nativement les alertes Suricata via le fichier `eve.json`. Il suffit de configurer l'agent Wazuh sur la machine Suricata.

```xml title="/var/ossec/etc/ossec.conf — Section localfile pour Suricata"
<ossec_config>

  <!-- Ajouter cette section à la configuration de l'agent Wazuh -->
  <localfile>
    <!-- Format JSON (eve.json de Suricata) -->
    <log_format>json</log_format>
    <!-- Chemin vers le fichier d'alertes Suricata -->
    <location>/var/log/suricata/eve.json</location>
    <!-- Collecte uniquement les alertes (pas les flows pour économiser les ressources) -->
    <only-future-events>yes</only-future-events>
  </localfile>

</ossec_config>
```

_Une fois configuré, les alertes Suricata apparaissent automatiquement dans le Wazuh Dashboard avec leur level CVSS, leur classification et leur mappage MITRE ATT&CK._

<br>

---

## Gestion des règles avec suricata-update

```bash title="Gestion des règles Emerging Threats"
# Lister les sources de règles disponibles
suricata-update list-sources

# Activer les règles Emerging Threats Pro (gratuites)
suricata-update enable-source et/open

# Activer les règles PT Research (menaces avancées)
suricata-update enable-source ptresearch/attackdetection

# Mettre à jour toutes les sources activées
suricata-update

# Recharger Suricata sans redémarrage complet
kill -USR2 $(cat /var/run/suricata.pid)

# Vérifier les stats de règles chargées
suricatasc -c "ruleset-stats"
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Suricata est le composant réseau incontournable d'un SOC moderne. Sa puissance vient de la **combinaison de trois capacités** : l'analyse de signatures (règles ET), l'analyse protocolaire (HTTP, DNS, TLS) et la génération de métadonnées de flux. Couplé à Wazuh, il offre une visibilité réseau complète que les seuls agents endpoint ne peuvent pas fournir.

> Passez maintenant au cours sur **[EDR/XDR →](../edr-xdr.md)** pour comprendre comment couvrir la couche endpoint, complémentaire à la couche réseau de Suricata.

<br>