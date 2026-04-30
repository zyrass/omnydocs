---
title: 2.2 Linux fondamentaux pour le forensic
description: Maîtrise du système Linux pour l'analyste forensic - structure du système de fichiers FHS, permissions UNIX, processus, signaux, redirections. Bases indispensables pour analyser un système Linux compromis.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Linux
  - Permissions
  - Processus
  - Forensic
data-level: 🟡
---

# 2.2 Linux fondamentaux pour le forensic

!!! quote "L'analogie de la maison aux mille pièces"

    Linux est une maison aux mille pièces, parfaitement organisée. Chaque répertoire a son rôle précis, hérité d'une norme appelée FHS. /etc range les configurations comme une bibliothèque ses dossiers. /var contient ce qui change comme un grenier ses cartons. /proc est un tableau électronique en temps réel des activités de la maison. L'analyste forensic qui ne connaît pas cette organisation est comme un enquêteur qui chercherait des preuves dans une maison sans savoir qu'il y a une cave et un grenier. Il passerait à côté de l'essentiel.

## Métadonnées du chapitre

| Champ | Valeur |
|---|---|
| Durée estimée | 6 heures |
| Niveau | Standard |
| Prérequis | Notions Linux de base |
| Livrables | Mémo CLI, scripts d'investigation |
| Auto-explication | 12 minutes |

## Objectifs pédagogiques

- Naviguer aisément dans la hiérarchie FHS
- Comprendre le modèle de permissions UNIX
- Identifier les processus suspects
- Maîtriser les redirections et pipes pour l'investigation
- Lire les fichiers système clés

---

## 1. Hiérarchie du système de fichiers (FHS)

```mermaid
flowchart TB
    A["/ racine"] --> B[/bin binaires essentiels]
    A --> C[/sbin binaires admin]
    A --> D[/etc configurations]
    A --> E[/var données variables]
    A --> F[/home utilisateurs]
    A --> G[/root admin]
    A --> H[/proc procfs virtuel]
    A --> I[/sys sysfs virtuel]
    A --> J[/tmp temporaires]
    A --> K[/usr utilitaires]
    A --> L[/dev devices]
    A --> M[/boot démarrage]
    A --> N[/run runtime]
```

### 1.1 Répertoires critiques pour le forensic

| Répertoire | Contenu | Intérêt forensic |
|---|---|---|
| `/etc/passwd` | Liste utilisateurs | Identification comptes |
| `/etc/shadow` | Hash des mots de passe | Cracking offline |
| `/etc/sudoers` | Permissions sudo | Escalade privilèges |
| `/var/log/` | Journaux système | Traces d'activité |
| `/var/log/auth.log` | Authentifications | Tentatives intrusion |
| `/var/log/syslog` | Logs système | Anomalies |
| `/var/log/audit/` | Audit auditd | Si configuré |
| `/home/*/.bash_history` | Historique commandes | Activité utilisateur |
| `/etc/cron*` | Tâches planifiées | Persistance |
| `/etc/systemd/system/` | Services personnalisés | Persistance |
| `/proc/[PID]/` | État processus en RAM | Investigation processus |
| `/tmp/` | Fichiers temporaires | Souvent utilisé par malwares |

### 1.2 Lecture rapide de `/etc/passwd`

```text
root:x:0:0:root:/root:/bin/bash
zyrass:x:1000:1000:Zyrass,,,:/home/zyrass:/bin/bash
suspect:x:1001:1001::/home/suspect:/bin/bash
```

| Champ | Signification |
|---|---|
| 1 | Login |
| 2 | Mot de passe (x = dans /etc/shadow) |
| 3 | UID |
| 4 | GID |
| 5 | GECOS (commentaire) |
| 6 | Répertoire home |
| 7 | Shell |

**Indices forensic** :
- UID 0 autre que root = porte dérobée
- Shell `/bin/false` ou `/usr/sbin/nologin` = compte service légitime
- Shell `/bin/bash` sans home = suspect

---

## 2. Permissions UNIX

### 2.1 Modèle classique

Trois niveaux d'acteurs : **utilisateur (u)**, **groupe (g)**, **autres (o)**.

Trois permissions : **read (r)**, **write (w)**, **execute (x)**.

```text
-rwxr-xr--  1 zyrass zyrass  1234 Apr 29 14:30 script.sh
│└──┴──┴──┘
│ u  g  o
│
type fichier (- = fichier, d = répertoire, l = lien, etc.)
```

### 2.2 Notation octale

```text
4 = read
2 = write
1 = execute

rwxr-xr-- = 754
rw-rw-r-- = 664
rw------- = 600
```

### 2.3 Permissions spéciales

| Bit | Symbole | Effet |
|---|---|---|
| SUID | `rws` | Exécute avec UID du propriétaire |
| SGID | `rwS` (sur fichier) | Exécute avec GID du propriétaire |
| SGID | `rws` (sur répertoire) | Hérite GID dans le répertoire |
| Sticky | `rwt` | Seul propriétaire peut supprimer |

**Risque SUID** : un binaire SUID root permet à tout utilisateur d'exécuter du code en root. C'est un vecteur classique d'escalade de privilèges.

### 2.4 Recherche forensic des SUID/SGID

```bash
# Trouver tous les binaires SUID sur le système
find / -perm -u=s -type f 2>/dev/null

# Trouver les SGID
find / -perm -g=s -type f 2>/dev/null

# Combinaison SUID + propriétaire root
find / -perm -u=s -user root -type f 2>/dev/null
```

**Liste de référence des SUID légitimes** :

```text
/usr/bin/sudo
/usr/bin/su
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/mount
/usr/bin/umount
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/chfn
```

Tout SUID en dehors de cette liste mérite investigation.

---

## 3. Processus

### 3.1 Modèle de processus

Chaque processus a :

| Attribut | Description |
|---|---|
| PID | Identifiant unique |
| PPID | Parent PID |
| UID/GID | Identité |
| EUID/EGID | Identité effective (peut différer si SUID) |
| Commande | Ligne de commande |
| État | Running, Sleeping, Zombie, Stopped |

### 3.2 Outils d'investigation

```bash
# Voir tous les processus avec arborescence
ps auxf

# Voir avec PPID
ps -ef

# Surveillance en direct
top
htop

# Arborescence visuelle
pstree -p
```

### 3.3 Lecture forensic de `ps auxf`

```text
USER    PID  CPU MEM   VSZ   RSS TTY    STAT START   TIME COMMAND
root      1  0.0 0.5 168320 11440 ?     Ss   Apr29   0:01 /sbin/init
root    234  0.0 0.1  35420  4820 ?     S    Apr29   0:00  \_ /lib/systemd/systemd-journald
```

**Indices forensic** :
- Processus avec PID élevé sans parent visible = suspect
- Processus utilisateur en root = vérification SUID ou injection
- Processus avec nom étrange ou crypté = malware probable
- Processus dans `/tmp/` = très suspect

### 3.4 Inspection détaillée d'un processus

```bash
# Toutes les infos sur un processus précis
ls -la /proc/[PID]/

# Ligne de commande complète
cat /proc/[PID]/cmdline | tr '\0' ' '

# Environnement
cat /proc/[PID]/environ | tr '\0' '\n'

# Fichiers ouverts
ls -la /proc/[PID]/fd/

# Connexions réseau
ls -la /proc/[PID]/net/tcp

# Mappings mémoire
cat /proc/[PID]/maps
```

---

## 4. Signaux et arrêt de processus

### 4.1 Signaux Linux principaux

| Signal | Numéro | Effet |
|---|---|---|
| SIGTERM | 15 | Demande arrêt propre |
| SIGKILL | 9 | Tue immédiatement |
| SIGSTOP | 19 | Suspend |
| SIGCONT | 18 | Reprend |
| SIGHUP | 1 | Relance configuration |
| SIGINT | 2 | Interrupt (Ctrl+C) |

### 4.2 En forensic - Pourquoi pas SIGKILL

```bash
# Mauvaise pratique en forensic (perte d'état)
kill -9 [PID]

# Bonne pratique : suspendre pour analyse
kill -STOP [PID]

# Examiner le processus suspendu
cat /proc/[PID]/maps
ls /proc/[PID]/fd/

# Reprendre ou tuer proprement
kill -CONT [PID]    # ou
kill -TERM [PID]
```

---

## 5. Redirections et pipes

### 5.1 Descripteurs de fichiers

| FD | Nom | Usage |
|---|---|---|
| 0 | stdin | Entrée |
| 1 | stdout | Sortie standard |
| 2 | stderr | Erreurs |

### 5.2 Redirections

```bash
# Sortie standard vers fichier
ls > liste.txt

# Append (ajout)
echo "ligne" >> liste.txt

# Erreurs uniquement
commande 2> erreurs.log

# Tout dans un fichier
commande > output.log 2>&1
commande &> output.log    # raccourci moderne

# Discard (poubelle)
commande > /dev/null 2>&1
```

### 5.3 Pipes - Composer les outils

```bash
# Compter les processus
ps aux | wc -l

# Filtrer
ps aux | grep -i suspect

# Trier
ps aux | sort -k 4 -n -r | head -10    # top 10 mémoire

# Compter occurrences
cat /var/log/auth.log | grep "Failed password" | wc -l

# Top des IP attaquantes
grep "Failed password" /var/log/auth.log | \
  grep -oP "from \K[\d.]+" | \
  sort | uniq -c | sort -rn | head -10
```

---

## 6. Fichiers de configuration critiques

### 6.1 Authentification

| Fichier | Rôle |
|---|---|
| `/etc/passwd` | Liste utilisateurs |
| `/etc/shadow` | Hash mots de passe |
| `/etc/group` | Groupes |
| `/etc/sudoers` | Configuration sudo |
| `/etc/sudoers.d/` | Configurations modulaires |
| `~/.ssh/authorized_keys` | Clés SSH autorisées |

### 6.2 Réseau

| Fichier | Rôle |
|---|---|
| `/etc/hosts` | Résolution locale |
| `/etc/resolv.conf` | DNS |
| `/etc/network/interfaces` | Interfaces (Debian) |
| `/etc/netplan/*` | Interfaces (Ubuntu récent) |
| `/etc/iptables/` | Règles pare-feu |

### 6.3 Démarrage et services

| Fichier | Rôle |
|---|---|
| `/etc/systemd/system/` | Services personnalisés |
| `/lib/systemd/system/` | Services standards |
| `/etc/cron.*/` | Tâches planifiées |
| `/var/spool/cron/crontabs/` | Crontab utilisateurs |
| `/etc/rc*.d/` | Init Sys V (legacy) |
| `~/.bashrc`, `~/.profile` | Auto-exec utilisateur |

### 6.4 Recherche d'altérations

```bash
# Vérifier l'intégrité des fichiers (Debian)
debsums -c

# Vérifier paquets RPM
rpm -Va

# Date de modification suspecte
find /etc -newer /etc/passwd -type f
find / -mtime -1 -type f 2>/dev/null    # modifié dans dernières 24h
```

---

## 7. Bonnes pratiques forensic Linux

### 7.1 Principe de non-altération

Lors d'une investigation, **chaque commande modifie potentiellement le système**. Privilégier :

| À éviter | Préférer |
|---|---|
| Commandes éditant des fichiers | Lecture seule |
| `cat` de gros fichiers en RAM | Acquisition disque dédiée |
| Suppression de processus | Suspension (SIGSTOP) |
| Reboot | Acquisition mémoire avant |

### 7.2 Outils en lecture seule

```bash
# Visualisation sans modification
cat fichier
less fichier
head/tail fichier
strings fichier            # extraire chaînes ASCII

# Inspection système
ps, top, htop
ss, netstat
lsof
who, w
last, lastlog
```

### 7.3 Hash systématique

```bash
# Calculer SHA-256
sha256sum fichier

# Sur tout un répertoire
find /etc -type f -exec sha256sum {} \; > hashes.txt

# Vérifier
sha256sum -c hashes.txt
```

---

## 8. Manipulation pratique

### Exercice 8.1 - Investigation rapide

Sur un système Linux suspect (votre VM ou serveur labo), répondez :

| Question | Commande |
|---|---|
| Combien de comptes UID 0 ? | `awk -F: '$3==0 {print $1}' /etc/passwd` |
| Quels SUID custom (hors liste standard) ? | `find / -perm -u=s -type f 2>/dev/null` |
| Quels processus root non-système ? | `ps auxf \| grep ^root` |
| Quelles tâches cron utilisateur ? | `for u in $(cut -d: -f1 /etc/passwd); do crontab -l -u $u 2>/dev/null; done` |
| Quels services systemd custom actifs ? | `systemctl list-unit-files --state=enabled` |
| Quelles connexions TCP établies ? | `ss -tnp` |
| Quels fichiers modifiés dernières 24h dans /etc ? | `find /etc -mtime -1 -type f` |
| Dernières connexions ? | `last -20` |

### Exercice 8.2 - Script d'inventaire

Créez un script bash qui produit un rapport forensic basique :

```bash
#!/bin/bash
# Script forensic-quick.sh
# Inventaire rapide d'un système Linux

OUTPUT="/tmp/forensic_$(hostname)_$(date +%Y%m%d_%H%M%S).txt"

echo "=== FORENSIC QUICK REPORT ===" > "$OUTPUT"
echo "Date: $(date -u)" >> "$OUTPUT"
echo "Hostname: $(hostname)" >> "$OUTPUT"
echo "" >> "$OUTPUT"

echo "=== UTILISATEURS UID 0 ===" >> "$OUTPUT"
awk -F: '$3==0 {print}' /etc/passwd >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== PROCESSUS EN COURS ===" >> "$OUTPUT"
ps auxf >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== CONNEXIONS RÉSEAU ===" >> "$OUTPUT"
ss -tnp >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== SERVICES ACTIFS ===" >> "$OUTPUT"
systemctl list-units --type=service --state=running >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== TÂCHES PLANIFIÉES ===" >> "$OUTPUT"
ls -la /etc/cron.* >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== FICHIERS RÉCEMMENT MODIFIÉS ===" >> "$OUTPUT"
find / -mtime -7 -type f 2>/dev/null | head -100 >> "$OUTPUT"

echo "Rapport écrit dans $OUTPUT"
sha256sum "$OUTPUT"
```

---

## 9. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Que contient /etc/shadow ? | Hash des mots de passe |
| 2 | Permission octale de rwxr-xr-- ? | 754 |
| 3 | Que fait SUID ? | Exécution avec UID du propriétaire |
| 4 | Comment lister fichiers ouverts d'un PID ? | `ls /proc/[PID]/fd/` |
| 5 | Différence kill -9 et kill -STOP ? | -9 tue, -STOP suspend (préférable forensic) |
| 6 | Top 10 IP failed login ? | grep + awk + sort + uniq + head |
| 7 | Vérifier intégrité paquets Debian ? | `debsums -c` |
| 8 | Préférer suspendre ou tuer en forensic ? | Suspendre |

---

## 10. Synthèse mémo

```text
LINUX FORENSIC - ESSENTIELS

FHS critique :
  /etc/passwd     comptes
  /etc/shadow     hashs
  /var/log/       traces
  /proc/[PID]/    état RAM
  /tmp/           suspect souvent

Permissions :
  rwx = 421
  SUID = exécution propriétaire
  Find SUID custom = priorité

Processus :
  ps auxf          arborescence
  /proc/[PID]/     toute info
  kill -STOP       suspend (préférable)

Investigation rapide :
  UID 0 multiples ?
  SUID custom ?
  Cron suspects ?
  Services exotiques ?
  Fichiers modifiés récemment ?

Hash systématique :
  sha256sum tout artefact
```

---

**Chapitre précédent** : [2.1 Auto-évaluation diagnostique](02-1-auto-evaluation.md)

**Chapitre suivant** : [2.3 Linux avancé - systemd, journaux, /proc, namespaces](02-3-linux-avance.md)
