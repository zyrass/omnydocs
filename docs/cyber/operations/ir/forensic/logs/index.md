---
description: "Analyse des Logs — Reconstruction de la Timeline de l'attaque via l'agrégation et l'analyse rapide des journaux d'événements (EVTX, Syslog)."
icon: lucide/scroll-text
tags: ["FORENSIC", "LOGS", "TIMELINE", "EVTX", "HAYABUSA"]
---

# Analyse des Logs (Timeline Forensics)

<div
  class="omny-meta"
  data-level="🟠 Intermédiaire"
  data-version="2026"
  data-time="~10 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/logs.svg" width="250" align="center" alt="Logs Forensic Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Journal de Bord"
    Sur un navire, le journal de bord consigne chaque événement : l'heure de départ, le changement de cap, la tempête. Les logs informatiques (Event Logs Windows, Syslog Linux) sont les journaux de bord de l'infrastructure. Quand un serveur est piraté, les logs racontent toute l'histoire... à condition de savoir les lire avant que le pirate ne les efface.

L'analyse de logs consiste à extraire, parser et corréler des millions d'événements pour recréer une **Timeline** exacte de l'intrusion : quel utilisateur s'est connecté, à quelle heure, depuis quelle IP, et quel processus a-t-il lancé.

<br>

---

## 🧭 Navigation du Module

| Outil | Description | Cas d'usage |
|---|---|---|
| **[Hayabusa](./hayabusa.md)** | Le Rapace des Logs | Outil écrit en Rust pour parser des EVTX Windows à une vitesse fulgurante et les matcher contre des règles Sigma (Threat Hunting). |
| **[Chainsaw](./chainsaw.md)** | La Tronçonneuse | Développé par F-Secure, idéal pour découper massivement des dossiers entiers de logs à la recherche d'IOCs. |

<br>

---

## 🗺️ Cartographie de la Timeline

```mermaid
graph TD
    A[Collecte des EVTX / Syslog] --> B[Outil de Parsing]
    B --> C[Chainsaw]
    B --> D[Hayabusa]
    
    C --> E{Matching}
    D --> E
    
    E -->|Règles Sigma| F[Alertes Comportementales]
    E -->|IOCs (IPs, Hash)| G[Match Exact]
    
    F --> H[Génération de la Timeline (CSV/JSON)]
    G --> H
```

> **Par où commencer ?** Lancez-vous dans l'analyse ultra-rapide des événements Windows avec **[Hayabusa](./hayabusa.md)**.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La réponse à incident (IR) demande méthode et sang-froid. La préservation des preuves, l'endiguement rapide et la remédiation structurée sont essentiels pour limiter l'impact d'une compromission et assurer une reprise d'activité sécurisée.

> [Retour à l'index des opérations →](../../index.md)
