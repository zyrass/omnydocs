---
description: "bulk_extractor — Un scanner ultra-rapide en ligne de commande (C++) capable d'extraire des artefacts précis (emails, URLs, cartes de crédit) sans se soucier du système de fichiers."
icon: lucide/hard-drive
tags: ["FORENSIC", "EXTRACTION", "BULK EXTRACTOR", "DFIR"]
---

# bulk_extractor — Le Chasseur de Traces

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.6+"
  data-time="~30 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/bulk.svg" width="250" align="center" alt="Bulk Extractor Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Tamis du Chercheur d'Or"
    Si Autopsy est le laboratoire complet et PhotoRec est l'ouvrier qui recolle les pages déchirées, **bulk_extractor** est le tamis du chercheur d'or. Au lieu d'essayer de reconstruire des fichiers entiers, il fait passer l'intégralité du disque dur à travers un crible pour ne retenir que les "pépites" d'information : des adresses email, des numéros de téléphone, des numéros de cartes bleues, ou des noms de domaine.

**bulk_extractor** est un programme en C++ très optimisé qui scanne des images de disques, des fichiers ou des répertoires pour en extraire des informations structurées (artefacts). Son grand atout est sa vitesse : comme il ignore le système de fichiers (NTFS, FAT) et scanne les blocs de données brutes via de multiples threads, il peut parcourir des centaines de gigaoctets en un temps record.

<br>

---

## 🛠️ Le Fonctionnement : Scanners et Histogrammes

L'outil fonctionne grâce à des **Scanners** intégrés. Chaque scanner cherche un motif spécifique (via des expressions régulières ou des algorithmes) :
- `email` : Adresses email valides.
- `accts` : Numéros de cartes de crédit (validés par l'algorithme de Luhn).
- `net` : Traces réseau (MAC, adresses IP).
- `zip` : Données compressées (qu'il va décompresser en mémoire à la volée pour les scanner !).

### Les Fichiers Histogrammes
La fonction la plus utile pour un analyste est la création d'histogrammes. Plutôt que de fournir une liste de 10 000 adresses IP trouvées sur le disque, bulk_extractor crée un fichier `ip_histogram.txt` qui classe ces IP par fréquence d'apparition. Si une adresse IP suspecte (ex: un serveur Command & Control) a été contactée des milliers de fois, elle sera propulsée en tête de liste !

<br>

---

## 🛠️ Usage Opérationnel

### 1. Le Scan Standard (Triage Rapide)

Lors d'un incident, l'analyste a besoin de *Quick Wins* (découvertes rapides). 

```bash title="Scanner une image disque"
# -o : Définit le dossier de destination (qui sera créé par l'outil)
# Le dernier argument est l'image cible (E01, raw, dd)
bulk_extractor -o /mnt/investigation/bulk_results /mnt/preuves/image_suspecte.E01
```
*Le dossier `/mnt/investigation/bulk_results` contiendra des dizaines de fichiers `.txt` (ex: `email.txt`, `domain_histogram.txt`, `url.txt`).*

### 2. Le Filtrage par Liste de Mots (Find List)

Si vous savez déjà ce que vous cherchez (ex: un terme spécifique lié à l'enquête, le nom d'un malware, ou une adresse IP suspecte), vous pouvez demander à bulk_extractor de trouver le contexte exact autour de ce mot.

```bash title="Créer un fichier de termes à rechercher"
echo "hackcorp.com" > mots_cles.txt
echo "192.168.1.50" >> mots_cles.txt
```

```bash title="Scan ciblé avec Find List"
# -F : Fichier contenant les chaînes à chercher
bulk_extractor -o results_cibles -F mots_cles.txt image_suspecte.dd
```
*L'outil extraira le texte se trouvant avant et après chaque occurrence des mots-clés, très utile pour retrouver un bout de code source ou un log supprimé.*

### 3. Exclure des Scanners pour gagner du temps

Si vous analysez un dump de mémoire (RAM) ou que vous êtes pressé, vous pouvez désactiver certains scanners lourds (comme le scanner ZIP qui tente de décompresser des archives).

```bash title="Désactivation de scanners"
# -x : Désactiver un scanner spécifique (ex: zip, gzip, rar)
bulk_extractor -x zip -o results_fast image_suspecte.dd
```

<br>

---

## 💀 Utilité en DFIR et Red Team

- **En Réponse à Incident (IR)** : L'extraction des domaines (`domain_histogram.txt`) permet de repérer immédiatement les serveurs C2 utilisés par un malware, même si les requêtes DNS ont été purgées du cache local.
- **En Forensic Bancaire** : Le scanner de cartes de crédit est redoutable pour auditer un serveur de base de données compromis et vérifier si des numéros de CB y étaient stockés en clair (fuite de données PCI-DSS).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Là où Autopsy est fait pour une analyse profonde et structurée, `bulk_extractor` est l'outil du "Triage" par excellence. Il répond à la question : "Y a-t-il des données sensibles ou des indicateurs de compromission évidents sur ce support ?" et ce, en un minimum de temps.

> Le data carving et l'extraction brute génèrent souvent beaucoup de "bruit" (faux positifs). Pour une enquête structurée, importez les résultats des histogrammes de bulk_extractor dans **[Autopsy](./autopsy.md)**.