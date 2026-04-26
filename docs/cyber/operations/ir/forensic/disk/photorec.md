---
description: "PhotoRec — L'outil de récupération de données (Data Carving) qui ignore le système de fichiers pour reconstruire les fichiers effacés."
icon: lucide/image-off
tags: ["FORENSIC", "CARVING", "PHOTOREC", "TESTDISK", "RECOVERY"]
---

# PhotoRec — Le Nécromancien des Données

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="7.2+"
  data-time="~30 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/testdisk.png" width="250" align="center" alt="PhotoRec Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Puzzle sans Modèle"
    Imaginez un livre dont on a arraché le sommaire (la table d'allocation des fichiers). Le système d'exploitation vous dit que le livre est vide. Mais les pages sont toujours là, mélangées en vrac sur le sol. **PhotoRec** ne cherche pas le sommaire. Il ramasse chaque page, regarde le début du texte (les signatures de fichiers), et scotche les pages ensemble pour reconstruire le document original. C'est ce qu'on appelle le *Data Carving* (sculpture de données).

Développé par CGSecurity (les mêmes créateurs que **TestDisk**), **PhotoRec** est un outil en ligne de commande (avec une interface en mode texte, TUI) conçu pour récupérer des fichiers perdus (vidéos, documents, archives, images) sur des disques durs, CD-ROMs et appareils photo numériques.

Il est "File System agnostic" : il se moque de savoir si votre disque était en NTFS, FAT, ext4 ou exFAT. S'il est formaté ou gravement corrompu, PhotoRec travaillera directement au niveau des blocs physiques.

<br>

---

## 🛠️ Le Concept Clé : Les "Magic Numbers"

Comment PhotoRec sait-il qu'un bloc de données est une image JPEG ? 

Presque tous les types de fichiers commencent par une séquence d'octets unique appelée *Magic Number* ou Signature.
- Un PDF commence toujours par les octets hexadécimaux `25 50 44 46` (`%PDF`).
- Un JPEG commence par `FF D8 FF E0`.
- Un exécutable Windows (.exe) commence par `4D 5A` (`MZ`).

PhotoRec lit le disque secteur par secteur. Dès qu'il croise `FF D8 FF E0`, il suppose que c'est le début d'une image, et il va extraire tous les secteurs suivants jusqu'à trouver la signature de fin (EOF, `FF D9`), puis il sauvegarde le bloc sous la forme d'un nouveau fichier (ex: `f12345.jpg`).

!!! warning "Perte des noms de fichiers"
    Puisque PhotoRec ne lit pas la table des fichiers (Master File Table sous NTFS), il ne connaît pas le nom original du fichier ni l'arborescence des dossiers. Vous obtiendrez des milliers de fichiers nommés de manière séquentielle (`f0001.pdf`, `f0002.doc`). Le tri manuel est le vrai défi du Carving !

<br>

---

## 🛠️ Usage Opérationnel — Workflow de Carving

PhotoRec est très sûr à utiliser en mode Forensic, car il ne fonctionne qu'en **lecture seule** sur le disque source.

### Étape 1 : Préparer la destination
Vous devez *absolument* créer un dossier sur un **autre** disque pour stocker les fichiers récupérés. Ne jamais écrire sur le disque en cours d'analyse !
```bash
mkdir /mnt/forensic_drive/recovered_files
```

### Étape 2 : Lancement
On fournit l'image du disque acquise précédemment à PhotoRec.
```bash title="Lancer PhotoRec sur une image brute"
photorec /mnt/forensic_drive/suspect_disk.dd
```

### Étape 3 : L'Interface Ncurses (TUI)
1. **Sélection du Média** : Choisissez le fichier image.
2. **Options de Fichiers (File Opt)** : *Très important*. Par défaut, PhotoRec cherche plus de 480 types de fichiers. Si vous ne cherchez qu'un PDF, désactivez tout avec `[s]` puis cochez uniquement `pdf`. Cela divisera le temps de traitement par 10 et évitera de noyer les résultats.
3. **Partition** : Sélectionnez la partition entière ou l'espace non alloué (*Free* / *Whole*).
4. **Type de Système** : Choisissez *Other* (FAT/NTFS) ou *ext2/ext3*.
5. **Destination** : Naviguez vers le dossier `/mnt/forensic_drive/recovered_files` créé à l'étape 1 et appuyez sur `C`.

<br>

---

## 💀 Utilité en Red Team et DFIR

- **DFIR (Défense)** : Un attaquant a exfiltré des données puis supprimé l'archive RAR utilisée. L'anti-forensic de l'attaquant était faible (simple commande `rm` ou `del`). L'analyste utilise PhotoRec pour extraire (*carve*) l'archive depuis l'espace non alloué et découvrir exactement quelles données ont fuité.
- **Red Team / Pentest** : L'auditeur met la main sur un vieux disque dur formaté appartenant à un administrateur système. Il lance PhotoRec pour retrouver d'anciens fichiers `.kdbx` (KeePass), des clés SSH privées (`.pem`, `.key`) ou des documents de configuration réseau.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    PhotoRec est l'ultime recours. Quand la partition est détruite, que le MBR est corrompu et que le système d'exploitation ne voit plus rien, la sculpture de données au niveau brut reste souvent le seul moyen de récupérer les preuves.

> Si vous devez fouiller parmi les dizaines de milliers de fichiers sans nom générés par PhotoRec, il est fortement conseillé de les importer dans une plateforme d'analyse avec recherche par mot-clé comme **[Autopsy](./autopsy.md)**.