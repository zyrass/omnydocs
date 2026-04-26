---
description: "Forensic Endpoint — Outils de télémétrie et d'investigation distribuée pour interroger des milliers de machines en temps réel (Velociraptor, osquery)."
icon: lucide/network
tags: ["FORENSIC", "ENDPOINT", "EDR", "VELOCIRAPTOR", "OSQUERY"]
---

# Outils Endpoint (Télémétrie & Live Forensics)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="2026"
  data-time="~15 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/endpoint.svg" width="250" align="center" alt="Endpoint Forensic Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Hélicoptère de Police"
    L'analyse disque traditionnelle, c'est envoyer un inspecteur à pied regarder chaque recoin d'une maison. C'est long. Mais que se passe-t-il si vous avez 10 000 maisons (postes de travail) et qu'un criminel court de l'une à l'autre ? Il vous faut un hélicoptère avec un porte-voix. L'Endpoint Forensics permet d'interroger instantanément tout le parc informatique : "Est-ce qu'une de ces 10 000 machines a ce fichier malveillant précis actuellement en mémoire ?"

L'Endpoint Forensics marque la frontière entre le SOC (Détection continue) et la Réponse à Incident. Il s'agit de déployer des agents (légers) sur tout le parc pour lancer des "chasses" (Threat Hunts) en temps réel.

<br>

---

## 🧭 Navigation du Module

| Outil | Description | Cas d'usage |
|---|---|---|
| **[osquery](./osquery.md)** | Le SQL du système | Transforme le système d'exploitation en une base de données relationnelle. Idéal pour demander `SELECT * FROM processes WHERE name = 'malware.exe'`. |
| **[Velociraptor](./velociraptor.md)** | Le Super-Prédateur | Le nec plus ultra de l'investigation distribuée (VQL). Permet non seulement de trouver, mais aussi de récupérer des fichiers à distance. |

<br>

---

## 🗺️ Cartographie de l'Investigation Endpoint

```mermaid
graph TD
    A[Analyste SOC / DFIR] --> B(Plateforme Serveur)
    B -->|Requête VQL / SQL| C[Flotte d'Agents]
    
    C --> D[Poste Windows 1]
    C --> E[Poste Windows 2]
    C --> F[Poste Linux]
    
    D -.->|Résultats| B
    E -.->|Résultats| B
    F -.->|Résultats| B
    
    B --> G{Action de remédiation}
    G -->|Tuer le processus| D
    G -->|Récupérer la MFT| E
```

> **Prenez les commandes du parc :** Découvrez le langage VQL et la puissance absolue de **[Velociraptor](./velociraptor.md)**.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La réponse à incident (IR) demande méthode et sang-froid. La préservation des preuves, l'endiguement rapide et la remédiation structurée sont essentiels pour limiter l'impact d'une compromission et assurer une reprise d'activité sécurisée.

> [Retour à l'index des opérations →](../../index.md)
