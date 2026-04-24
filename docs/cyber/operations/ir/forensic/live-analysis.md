---
description: "Live Forensics — Investigation numérique à chaud : analyse de la RAM avec Volatility, acquisition d'artefacts avec Velociraptor et détection d'artefacts volatils."
icon: lucide/microscope
tags: ["FORENSIC", "LIVE ANALYSIS", "VOLATILITY", "VELOCIRAPTOR", "RAM", "IR", "DFIR"]
---

# Live Forensics — Investigation à Chaud

<div
  class="omny-meta"
  data-level="🔴 Expert"
  data-version="1.0"
  data-time="~5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Autopsie vs la Biopsie"
    Le forensic classique (analyse de disque) est une **autopsie** : on examine un corps inerte pour comprendre ce qui s'est passé. Le **Live Forensics** est une **biopsie** : on prélève des échantillons sur un organisme vivant (système en cours d'exécution) pour détecter la maladie en temps réel. Certains virus (malwares "fileless") ne laissent aucune trace sur le disque et disparaissent dès que la machine s'éteint. Sans analyse à chaud, ils sont invisibles.

Le **Live Forensics** est l'art d'extraire la vérité technique d'un système qui tourne encore. C'est une phase critique car elle permet de capturer des éléments volatils : connexions réseau actives, mots de passe en mémoire, processus injectés et clés de chiffrement.

<br>

---

## 🛠️ Outil 1 : Volatility 3 (Analyse Mémoire)

**Volatility** est le standard mondial pour l'analyse de dumps mémoire (RAM). Il permet de reconstruire l'état complet du système au moment de la capture.

### Flux de travail Volatility
1. **Acquisition** : Capturer la RAM (via `DumpIt` ou `Magnet RAM Capture`).
2. **Analyse** : Utiliser les plugins Volatility pour extraire les informations.

```bash title="Commandes Volatility 3 essentielles"
# Lister les processus au moment du dump
python3 vol.py -f memory.dmp windows.pslist

# Détecter les processus cachés (qui tentent de s'auto-dissimuler)
python3 vol.py -f memory.dmp windows.psscan

# Voir l'arborescence des processus (parent/child)
python3 vol.py -f memory.dmp windows.pstree

# Lister les connexions réseau actives
python3 vol.py -f memory.dmp windows.netscan

# Extraire un binaire suspect de la mémoire pour analyse YARA
python3 vol.py -f memory.dmp windows.dumpfiles --pid <PID>
```

---

## 🦖 Outil 2 : Velociraptor (Hunting à l'échelle)

**Velociraptor** est un outil de visibilité endpoint et de réponse aux incidents qui permet d'interroger des milliers de machines simultanément pour trouver des artefacts spécifiques (fichiers, clés de registre, logs).

### VQL : Velociraptor Query Language
Velociraptor utilise son propre langage de requête pour collecter des preuves.

```sql title="VQL — Chercher une clé de persistance suspecte sur tout le parc"
SELECT FullPath, Type, Data 
FROM glob(globs="HKEY_USERS\\*\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\*")
WHERE Data =~ "temp|appdata"
```

### Pourquoi utiliser Velociraptor en incident ?
- **Vitesse** : Collecter les fichiers `MFT` (Master File Table) de 100 serveurs en 2 minutes.
- **Précision** : Chercher un hash spécifique ou une règle YARA directement en mémoire sur tous les postes.
- **Discrétion** : L'agent est léger et peut être déployé à la volée.

---

## 🔬 Analyse des Artefacts Volatils

Lors d'une investigation à chaud, concentrez-vous sur ces 4 piliers :

| Artefact | Pourquoi ? | Outil recommandé |
|---|---|---|
| **Connexions Réseau** | Identifie le serveur C2 de l'attaquant | `netscan` (Volatility) |
| **Code Injecté** | Détecte les malwares qui vivent dans `explorer.exe` | `malfind` (Volatility) |
| **MFT / USN Journal** | Timeline des fichiers créés/supprimés récemment | `Windows.KapeFiles` (Velociraptor) |
| **Handles & DLLs** | Identifie les bibliothèques malveillantes chargées | `dlllist` (Volatility) |

---

## ⚠️ La Règle d'Or du Forensic

!!! danger "L'Ordre de Volatilité"
    Ne commencez **jamais** par éteindre une machine suspecte. En l'éteignant, vous détruisez 90% des preuves critiques (RAM, connexions réseau). Suivez toujours l'ordre de volatilité (RFC 3227) :
    1. Registres, Cache, Table ARP.
    2. Mémoire Vive (RAM).
    3. État du réseau.
    4. Disque dur.

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le Live Forensics est la frontière entre l'analyste SOC et l'enquêteur DFIR. Maîtriser des outils comme **Volatility** et **Velociraptor** vous permet de voir au-delà du disque dur et de traquer les attaquants les plus sophistiqués (APT) qui utilisent des techniques de "Living off the Land" et du malware résident en mémoire.

> **Exercice pratique :** Téléchargez un dump mémoire d'entraînement (ex: sur *Memory Forensics Case Studies*) et essayez d'identifier le processus malveillant avec `windows.pstree`.
