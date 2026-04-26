---
description: "Rekall — Un framework de Forensique Mémoire avancé (fork de Volatility) spécialisé dans l'analyse live et l'extraction rapide, bien que son développement soit désormais au ralenti."
icon: lucide/cpu
tags: ["FORENSIC", "MEMORY", "RAM", "REKALL", "DFIR"]
---

# Rekall — L'Alternative Rapide (Legacy)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.7 (Legacy)"
  data-time="~30 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/rekall.png" width="250" align="center" alt="Rekall Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Interview en Direct"
    Si **Volatility** est un médecin légiste qui étudie méticuleusement le corps (le dump mémoire) une fois qu'il est apporté au laboratoire, **Rekall** a été conçu pour être un médecin urgentiste capable d'examiner le patient pendant qu'il est encore vivant (Analyse Live de la RAM).

**Rekall** est un framework open-source d'analyse de la mémoire volatile, initialement créé comme un fork de Volatility (en 2011) par des chercheurs de Google. Son objectif principal était de combler certaines limitations de Volatility 2, notamment en accélérant la gestion des profils OS (via l'utilisation de profils hébergés dans le Cloud) et en introduisant la capacité d'analyser la mémoire *en direct* sur une machine en cours d'exécution (Live Forensics).

!!! warning "Statut du projet : Legacy"
    Depuis la sortie de Volatility 3, la communauté DFIR s'est massivement reconcentrée sur Volatility. Le développement de Rekall est aujourd'hui quasi à l'arrêt. Il reste cependant un outil très intéressant pédagogiquement et pour l'analyse d'anciens systèmes.

<br>

---

## 🛠️ Concepts Fondamentaux : Pourquoi Rekall ?

À son apogée, Rekall a introduit deux concepts majeurs qui ont révolutionné l'industrie (et qui ont depuis été intégrés dans d'autres outils comme GRR ou Velociraptor).

### 1. Les Profils Cloud
Sous Volatility 2, l'analyste devait construire manuellement un "Profil" (fichier zip contenant les structures du kernel) pour les systèmes Linux/Mac cibles, ce qui était une tâche fastidieuse. Rekall a introduit un dépôt Cloud. Si l'analyste possède une connexion Internet, Rekall télécharge automatiquement le profil exact en analysant les signatures de la RAM.

### 2. Le Live Forensics
Rekall peut charger un pilote mémoire localement (`WinPmem` sous Windows) pour analyser la RAM de la propre machine de l'analyste (ou d'une machine compromise) en temps réel, sans avoir à extraire un dump complet de 16 ou 32 Go sur le disque dur.

<br>

---

## 🛠️ Usage Opérationnel

La syntaxe de Rekall est très similaire à celle de Volatility 2, car les plugins partagent la même nomenclature historique.

### 1. Mode Interactif (Console)
Rekall brille par sa console interactive (basée sur IPython) qui permet de naviguer dans les structures mémoire avec auto-complétion, au lieu de lancer de longues commandes répétitives.

```bash title="Lancer le Shell Rekall interactif"
rekal -f /mnt/preuves/memdump.raw
```
*(Dans le shell Rekall)*
```python
# Lister les processus
pslist

# Trouver des processus cachés
psscan

# Extraire les clés de registre
printkey(hve="SAM")
```

### 2. Ligne de commande classique
```bash title="Vérification des connexions réseau (Live Forensics sous Windows)"
# Sans spécifier -f, Rekall analyse la RAM de la machine courante
rekal netstat
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Rekall a apporté des innovations majeures à la communauté DFIR (Profils automatiques, Live Forensics). Bien qu'il soit aujourd'hui éclipsé par Volatility 3, son moteur d'analyse en direct a servi de fondation à de nombreux agents de réponse à incident modernes (Endpoint Detection).

> Pour vos analyses de routine actuelles, privilégiez le framework standard de l'industrie : **[Volatility](./volatility.md)**.