---
description: "Analyse Mémoire (RAM Forensic) — Méthodologie et outils pour extraire les processus cachés, malwares résidents et clés de chiffrement de la mémoire vive."
icon: lucide/cpu
tags: ["FORENSIC", "MEMORY", "RAM", "VOLATILITY", "REKALL"]
---

# Analyse Mémoire (Memory Forensics)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="2026"
  data-time="~15 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/ram.svg" width="250" align="center" alt="Memory Forensic Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — La Mémoire Court Terme"
    L'analyse disque, c'est comme lire le journal intime de quelqu'un : tout y est écrit noir sur blanc, mais c'est figé. L'analyse mémoire, c'est lire dans les pensées instantanées de la machine. Les malwares modernes "Fileless" (sans fichier) ne touchent jamais le disque dur ; ils existent uniquement dans les pensées (la RAM) de l'ordinateur. Éteignez la machine, et le malware disparaît à jamais.

Le *Memory Forensics* est l'art d'analyser un dump de RAM pour y trouver des mots de passe en clair, des clés de déchiffrement (ex: BitLocker), des connexions réseau actives et du code malveillant injecté dans des processus légitimes (Process Injection/Hollowing).

<br>

---

## 🧭 Navigation du Module

| Outil | Rôle Principal | Cas d'usage |
|---|---|---|
| **[Volatility 3](./volatility.md)** | Le Standard Absolu | Analyser un dump de RAM pour trouver les processus malveillants (`windows.pslist`, `windows.malfind`). |
| **[Rekall](./rekall.md)** | Live Analysis & GUI | Alternative (issue de Volatility) puissante pour la réponse à incident en temps réel. |

<br>

---

## 🗺️ Cartographie de l'Analyse Mémoire

```mermaid
graph TD
    A[Fichier Dump .raw / .mem] --> B[Volatility 3]
    B --> C{Que cherche-t-on ?}
    
    C -->|Processus & Arborescence| D[pslist / pstree]
    C -->|Code Injecté (Malware)| E[malfind]
    C -->|Commandes tapées| F[cmdline]
    C -->|Réseau (Sockets)| G[netscan]
    
    D --> H[Corrélation et création de Timeline]
    E --> I[Extraction du payload (dump)]
    G --> H
    I --> J[Reverse Engineering]
```

> **Prêt à plonger ?** Commencez par le standard de l'industrie : **[Volatility](./volatility.md)**.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La réponse à incident (IR) demande méthode et sang-froid. La préservation des preuves, l'endiguement rapide et la remédiation structurée sont essentiels pour limiter l'impact d'une compromission et assurer une reprise d'activité sécurisée.

> [Retour à l'index des opérations →](../../index.md)
