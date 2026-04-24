---
description: "Snort 3 — IDS/IPS historique de référence : règles Snort Community, syntaxe des règles et comparatif avec Suricata."
icon: lucide/book-open-check
tags: ["SNORT", "IDS", "IPS", "RÉSEAU", "SOC"]
---

# Snort 3 — IDS/IPS de Référence

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Snort 3.x"
  data-time="~2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Grand-Père de la Détection Réseau"
    Si Suricata est le smartphone dernier cri, **Snort est l'encyclopédie** qui a tout appris à ses descendants. Créé en 1998 par Martin Roesch, Snort a posé les fondations de la détection d'intrusion réseau. Ses règles et sa syntaxe sont devenus le **standard de l'industrie** — Suricata lui-même lit les règles Snort nativement.

**Snort** est le premier IDS/IPS open-source, maintenu depuis 2013 par **Cisco**. Sa version 3.x est une réécriture complète avec support multi-thread.

!!! info "Snort vs Suricata — lequel choisir ?"

    Tableau comparatif :

    | Critère | Snort 3 | Suricata 7 |
    |---|---|---|
    | Performance multi-thread | Partielle | Natif ✅ |
    | Sortie EVE JSON | Limitée | Complète ✅ |
    | Intégration Wazuh native | Non | Oui ✅ |
    | Écosystème | Cisco / historique | Communauté active ✅ |

    **Recommandation** : Pour un nouveau déploiement SOC, privilégiez **Suricata**. Snort est pertinent si votre organisation a déjà des règles ou équipements Cisco.

<br>

---

## Syntaxe des règles Snort

La syntaxe Snort est le **standard universel** — Suricata, Zeek et de nombreux outils commerciaux la comprennent.

```bash title="/etc/snort/rules/local.rules — Exemples de règles"
# FORMAT : action proto src_ip src_port direction dst_ip dst_port (options)

# Règle 1 : Ping sweep (ICMP vers plusieurs hôtes)
alert icmp $EXTERNAL_NET any -> $HOME_NET any (
    msg:"RECON ICMP Ping Sweep potentiel";
    itype:8;                          # Type 8 = Echo Request
    threshold:type threshold, track by_src, count 10, seconds 5;
    classtype:attempted-recon;
    sid:1000001; rev:1;
)

# Règle 2 : Connexion FTP non chiffrée vers l'extérieur
alert tcp $HOME_NET any -> $EXTERNAL_NET 21 (
    msg:"POLICY Connexion FTP en clair vers l'extérieur";
    flow:established,to_server;
    classtype:policy-violation;
    sid:1000002; rev:1;
)

# Règle 3 : Tentative d'injection SQL (UNION SELECT) dans l'URI
alert http $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS (
    msg:"WEBATTACK Injection SQL — UNION SELECT détecté";
    flow:established,to_server;
    http_uri;
    content:"UNION"; nocase;
    content:"SELECT"; nocase; distance:0;
    classtype:web-application-attack;
    sid:1000003; rev:2;
)
```

<br>

---

## Lancement et validation

```bash title="Commandes Snort 3 essentielles"
# Valider la configuration
snort -c /etc/snort/snort.lua --warn-all

# Lancer en mode IDS sur eth0
snort -c /etc/snort/snort.lua -i eth0 -A alert_fast -D

# Tester sur un fichier pcap
snort -c /etc/snort/snort.lua -r capture.pcap -A alert_fast
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La syntaxe des règles Snort est le **langage commun de la détection réseau**. La maîtriser vous permet de lire, écrire et adapter des règles pour Snort, Suricata ou tout outil compatible. C'est un investissement direct dans votre expertise SOC.

> Revenez au hub **[Architecture SOC →](../index.md)** pour continuer avec EDR/XDR, NDR et TIP.

<br>