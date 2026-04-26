---
description: "Volatility 3 — Le framework open-source de référence pour l'analyse forensique de la mémoire vive (RAM)."
icon: lucide/cpu
tags: ["FORENSIC", "MEMORY", "RAM", "VOLATILITY", "MALWARE", "DFIR"]
---

# Volatility — L'Analyse de la Mémoire Vive

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="3.0+"
  data-time="~1.5 heures">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/volatility.svg" width="250" align="center" alt="Volatility Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Autopsie du Cerveau"
    Si l'analyse de disque (Autopsy) est l'étude des archives d'une personne, l'analyse mémoire (Volatility) est la lecture de ses pensées immédiates au moment de l'incident. C'est ici que se cachent les secrets que le suspect refuse d'écrire sur le papier : les mots de passe tapés au clavier, les communications réseau secrètes, et les virus "sans fichier" (Fileless) qui n'existent que dans l'esprit de l'ordinateur.

**Volatility** est un framework en Python dédié à l'extraction d'artefacts numériques à partir de dumps de mémoire volatile (RAM). 

La **version 3** (Volatility 3) a complètement repensé l'architecture de l'outil. Contrairement à Volatility 2, il n'est plus nécessaire de spécifier manuellement le "Profile" (l'OS exact de la cible). Volatility 3 utilise des symboles (Symbol Tables) pour détecter automatiquement la structure de la mémoire, que ce soit Windows, Linux ou macOS.

<br>

---

## 🛠️ Concepts Fondamentaux : Les Symboles et les Plugins

Pour comprendre un dump de RAM (qui n'est qu'une suite de milliards de zéros et de uns), Volatility a besoin d'une carte.
- **Les Symboles (ISF - Intermediate Symbol Format)** : Ce sont les cartes (fournies par Microsoft ou compilées pour Linux/Mac) qui expliquent à Volatility où se trouvent les structures de données dans la mémoire (ex: "La liste des processus Windows commence à cet offset"). Volatility 3 télécharge souvent ces symboles automatiquement.
- **Les Plugins** : Ce sont les scripts qui utilisent la carte pour extraire une information précise (ex: `windows.pslist.PsList` pour lister les processus).

<br>

---

## 🛠️ Usage Opérationnel — Workflow d'Analyse (Windows)

Un workflow classique d'analyse de malware en mémoire suit un entonnoir : de la vue globale (les processus) jusqu'à l'extraction du code malveillant.

### 1. Identifier l'OS et l'Image
Même si Volatility 3 est "auto-magique", il est bon de vérifier les informations de base du dump.
```bash title="Information sur le dump (Windows)"
# -f : Spécifie le fichier (dump mémoire acquis avec DumpIt, FTK Imager ou LiME)
python3 vol.py -f /mnt/preuves/memdump.raw windows.info.Info
```

### 2. Lister les Processus (Le point de départ)
Trouver le processus malveillant est souvent la première étape.
```bash title="Afficher l'arborescence des processus"
# pstree montre les relations Parent-Enfant (ex: cmd.exe lancé par word.exe est suspect !)
python3 vol.py -f memdump.raw windows.pstree.PsTree
```
!!! tip "Processus Cachés"
    Un Rootkit (malware avancé) peut modifier les structures de l'OS pour se cacher de `pstree`. Utilisez le plugin `windows.psscan.PsScan` : il ignore la liste officielle de l'OS et scanne directement la mémoire à la recherche de blocs ressemblant à des processus (Carving).

### 3. Trouver l'Injection (Malware)
Les malwares modernes n'ont pas de `.exe` propre ; ils s'injectent dans des processus légitimes (comme `explorer.exe` ou `svchost.exe`).
```bash title="Recherche d'injection de code (Process Hollowing / DLL Injection)"
# malfind cherche des pages mémoire qui ont les droits "Exécution" (PAGE_EXECUTE_READWRITE) mais qui ne sont pas associées à un fichier disque légitime.
python3 vol.py -f memdump.raw windows.malfind.Malfind
```

### 4. Analyser le Réseau
Si le malware est un ransomware ou un RAT (Remote Access Trojan), il doit communiquer avec son serveur C2.
```bash title="Lister les connexions réseau actives"
python3 vol.py -f memdump.raw windows.netscan.NetScan
```

### 5. Extraction (Dumping)
Une fois le PID suspect identifié (ex: PID 4012), on l'extrait de la mémoire pour l'analyser dans un outil de Reverse Engineering (Ghidra, IDA Pro).
```bash title="Dumper l'exécutable d'un processus"
# Extrait le binaire complet du processus PID 4012
python3 vol.py -f memdump.raw -o /chemin/vers/dossier_extraction windows.pslist.PsList --pid 4012 --dump
```

<br>

---

## 💀 Scénarios Avancés (DFIR)

- **Extraction des Hashes (Pass-the-Hash)** : Vous pouvez dumper la ruche SAM et les secrets LSA directement depuis la mémoire, ce qui permet de récupérer les hashes NTLM (et parfois les mots de passe en clair) des utilisateurs connectés lors du dump.
  ```bash
  python3 vol.py -f memdump.raw windows.hashdump.Hashdump
  ```
- **Fichiers en Mémoire** : Lors de l'ouverture d'un document Word ou d'un PDF malveillant, le fichier est déchiffré en RAM. Vous pouvez extraire ce fichier avec le plugin `windows.filescan.FileScan` et `windows.dumpfiles.DumpFiles`.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Volatility est l'outil ultime de la Réponse à Incident (IR). Il permet de comprendre le comportement exact d'un attaquant au moment critique. L'analyse mémoire est la seule discipline forensique capable de vaincre les malwares "Fileless" (qui ne touchent jamais le disque dur).

> Pour obtenir un dump mémoire de qualité sur une machine suspecte, utilisez des outils d'acquisition de RAM en mode noyau, comme **[LiME](../acq/lime.md)** pour Linux ou DumpIt/FTK Imager pour Windows.