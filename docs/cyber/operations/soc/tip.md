---
description: "TIP — Threat Intelligence Platform : centraliser les IOC, enrichir les alertes SIEM et partager la menace avec MISP et OpenCTI."
icon: lucide/book-open-check
tags: ["TIP", "THREAT INTELLIGENCE", "MISP", "OPENCTI", "IOC", "SOC", "CTI"]
---

# TIP — Threat Intelligence Platform

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="MISP 2.4.x / OpenCTI 6.x"
  data-time="~2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Fichier Central de la Police"
    Lorsqu'un policier interpelle un suspect, il consulte immédiatement le fichier central pour savoir si cette personne est recherchée ailleurs. Sans ce fichier, chaque commissariat travaille en silo — un criminel connu dans une ville passe inaperçu dans une autre. La **TIP** est ce fichier central pour les menaces cyber : elle centralise tous les indicateurs connus (IPs malveillantes, hash de malwares, domaines C2) et permet à votre SIEM d'**enrichir automatiquement** chaque alerte avec la connaissance mondiale de la menace.

Une **TIP (Threat Intelligence Platform)** est une plateforme qui :
1. **Collecte** des IOC (Indicateurs of Compromise) depuis de multiples sources
2. **Enrichit** ces IOC avec du contexte (qui est derrière, quelle campagne, quel malware)
3. **Partage** ces informations avec d'autres organisations (communauté ISAC, CERT)
4. **Alimente** le SIEM pour corréler les alertes internes avec la menace externe

<br>

---

## Les IOC — Indicateurs of Compromise

Un **IOC** est une preuve technique qu'un système a été compromis ou est en train de l'être :

| Type d'IOC | Exemples | Durée de vie |
|---|---|---|
| **Hash de fichier** | MD5, SHA1, SHA256 d'un malware | Longue (mois/années) |
| **Adresse IP** | IP d'un serveur C2 | Courte (heures/jours) |
| **Nom de domaine** | Domaine utilisé par un malware | Moyenne (semaines) |
| **URL** | URL de téléchargement de payload | Très courte (heures) |
| **Mutex** | Nom de mutex créé par un malware | Longue |
| **Règle YARA** | Signature de malware dans un fichier | Longue |

!!! warning "Les IOC ont une durée de vie"
    Une IP malveillante peut devenir une IP légitime après quelques jours (réaffectation). Un SIEM qui corrèle sur des IOC obsolètes génère des faux positifs et perd la confiance des analystes. La **fraîcheur des IOC** est critique.

<br>

---

## MISP — La TIP Open-Source de référence

**MISP (Malware Information Sharing Platform)** est la TIP open-source la plus déployée dans le monde. Elle est maintenue par le CIRCL (Luxembourg) et utilisée par plus de 6 000 organisations dont l'ANSSI, l'ENISA, et de nombreux CERTs nationaux.

### Installation rapide (Docker)

```bash title="Déploiement MISP via Docker Compose"
# Cloner le dépôt officiel MISP Docker
git clone https://github.com/MISP/misp-docker
cd misp-docker

# Copier et adapter la configuration
cp template.env .env
nano .env  # Définir MISP_ADMIN_EMAIL, MISP_ADMIN_PASSPHRASE, MISP_BASE_URL

# Démarrer MISP (inclut MISP, MySQL, Redis, Nginx)
docker compose up -d

# Vérifier que tous les conteneurs sont up
docker compose ps

# MISP accessible sur https://localhost (admin@admin.test / admin par défaut)
```

### Créer et partager des IOC

```bash title="API MISP — Ajouter des IOC programmatiquement"
# Exemple : ajouter un hash SHA256 suspect via l'API REST
curl -H "Authorization: VOTRE_CLE_API" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{
       "Event": {
         "distribution": 1,
         "info": "Campagne Phishing - Facture frauduleuse",
         "threat_level_id": 2,
         "analysis": 1,
         "Attribute": [
           {
             "type": "sha256",
             "category": "Payload delivery",
             "value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
             "comment": "Hash du fichier facture_mars.exe",
             "to_ids": true
           },
           {
             "type": "ip-dst",
             "category": "Network activity",
             "value": "185.220.101.45",
             "comment": "Serveur C2 identifié",
             "to_ids": true
           }
         ]
       }
     }' \
     https://votre-misp.exemple.com/events/add
```

### Sources d'alimentation (feeds) gratuites

MISP peut s'abonner à des **feeds** automatiques d'IOC :

| Feed | Source | Contenu |
|---|---|---|
| **CIRCL OSINT** | MISP Project | IOC généraux open-source |
| **Abuse.ch URLhaus** | Abuse.ch | URLs de distribution de malware |
| **Abuse.ch MalwareBazaar** | Abuse.ch | Hash de malwares |
| **CERT-FR Feeds** | ANSSI/CERT-FR | IOC incidents français |
| **Feodo Tracker** | Abuse.ch | IPs de botnets (Emotet, TrickBot...) |

```bash title="Activer les feeds MISP depuis l'interface ou l'API"
# Via l'interface : Administration → Feeds → Activer les feeds souhaités
# Via l'API (exemple feed Abuse.ch URLhaus) :
curl -H "Authorization: VOTRE_CLE_API" \
     -H "Content-Type: application/json" \
     -X POST \
     https://votre-misp.exemple.com/feeds/enable/1
```

<br>

---

## Intégration MISP → Wazuh

L'intégration MISP/Wazuh permet d'**enrichir automatiquement** chaque alerte Wazuh en vérifiant si les IOC (IPs, domaines, hash) sont connus dans MISP.

```python title="/var/ossec/integrations/misp — Script d'intégration"
#!/usr/bin/env python3
# Script d'intégration Wazuh <-> MISP
# Placé dans /var/ossec/integrations/custom-misp

import sys
import json
import requests

# Configuration
MISP_URL = "https://votre-misp.exemple.com"
MISP_API_KEY = "VOTRE_CLE_API_MISP"
MISP_VERIFY_SSL = False  # Mettre True en production avec certificat valide

def query_misp(ioc_value, ioc_type):
    """Interroge MISP pour un IOC donné"""
    headers = {
        "Authorization": MISP_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "returnFormat": "json",
        "type": ioc_type,
        "value": ioc_value,
        "to_ids": True  # Uniquement les IOC de détection
    }
    response = requests.post(
        f"{MISP_URL}/attributes/restSearch",
        headers=headers,
        json=payload,
        verify=MISP_VERIFY_SSL
    )
    return response.json()

# Lire l'alerte Wazuh depuis stdin
alert = json.loads(sys.stdin.read())
src_ip = alert.get("data", {}).get("srcip", "")

if src_ip:
    result = query_misp(src_ip, "ip-src")
    if result.get("response", {}).get("Attribute"):
        # IOC trouvé dans MISP — enrichir l'alerte
        print(json.dumps({
            "misp_match": True,
            "misp_event": result["response"]["Attribute"][0].get("Event", {})
        }))
```

<br>

---

## OpenCTI — La TIP de nouvelle génération

**OpenCTI** est une TIP plus récente orientée **analyse de menaces** (qui, pourquoi, comment) plutôt que simple partage d'IOC. Elle utilise le standard STIX 2.1 et s'intègre avec MISP.

```bash title="Déploiement OpenCTI via Docker"
git clone https://github.com/OpenCTI-Platform/docker
cd docker
cp .env.sample .env
# Générer des clés UUID pour les variables dans .env
nano .env

docker compose up -d
# Interface sur http://localhost:8080
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Une TIP transforme votre SOC de **réactif** (on détecte après l'attaque) à **proactif** (on connaît l'attaquant avant qu'il frappe). MISP connecté à Wazuh permet de corréler automatiquement vos alertes avec les campagnes d'attaque mondiales — une IP inconnue qui touche votre réseau devient immédiatement identifiable comme appartenant à un groupe APT si elle est dans MISP. C'est la différence entre "anomalie réseau" et "compromission probable par APT28".

> **La Phase 1 (Architecture SOC) est terminée.** Passez maintenant à la **[Phase 2 — Détection & Analyse →](../../detection/index.md)** pour apprendre à créer les règles qui exploitent toute cette infrastructure.
