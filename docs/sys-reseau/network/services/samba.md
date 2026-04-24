---
description: "Héberger un serveur de fichiers (NAS) sous Linux accessible nativement par les postes Windows via Samba."
icon: lucide/book-open-check
tags: ["SAMBA", "SMB", "CIFS", "RESEAU", "PARTAGE"]
---

# Partage Windows (Samba / SMB)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>

!!! quote "Le pont entre deux mondes"
    _Les entreprises utilisent des serveurs Linux (pour leur stabilité, gratuité, et résistance aux ransomwares classiques) mais possèdent un parc d'ordinateurs pour les employés sous Windows. Comment faire pour qu'un employé Windows puisse faire un simple "clic-droit -> Partager" ou monter un "Lecteur réseau Z:" qui pointe en réalité vers un serveur Linux ? La réponse est **Samba**._

## 1. Qu'est-ce que Samba ?

Microsoft a inventé le protocole **SMB** (Server Message Block), aussi appelé CIFS, pour le partage de fichiers et d'imprimantes sur les réseaux locaux.
**Samba** est l'implémentation de ce protocole propriétaire par la communauté Open Source pour les systèmes Unix/Linux.

```mermaid
graph TD
    subgraph Postes Clients (Windows)
        Win1[💻 PC Employé <br/> Accès Anonyme]
        Win2[💻 PC Direction <br/> Authentifié en tant qu'Alice]
    end
    
    subgraph Serveur Fichiers (Linux)
        SMB[Processus smbd <br/> Port TCP 445]
        D1[📁 /srv/samba/commun <br/> Droits: 777 Public]
        D2[📁 /srv/samba/direction <br/> Droits: 700 alice:alice]
    end
    
    Win1 -->|Requête SMB| SMB
    Win2 -->|Requête SMB avec identifiants| SMB
    
    SMB -->|Traduit en droits POSIX| D1
    SMB -->|Traduit en droits POSIX| D2
    
    style Win1 fill:#2980b9,stroke:#fff,color:#fff
    style Win2 fill:#2980b9,stroke:#fff,color:#fff
    style SMB fill:#c0392b,stroke:#fff,stroke-width:2px,color:#fff
    style D1 fill:#27ae60,stroke:#fff,color:#fff
    style D2 fill:#e67e22,stroke:#fff,color:#fff
```

Samba permet à un serveur Linux :
- De partager des dossiers réseau visibles par Windows.
- D'authentifier les utilisateurs avec leurs identifiants Windows.
- Et même (dans des cas très avancés) d'agir comme un Contrôleur de Domaine (Active Directory) rudimentaire.

---

## 2. Installation et Configuration Basique

```bash
sudo apt update
sudo apt install samba
```

La configuration de Samba se fait dans un fichier extrêmement long et verbeux : `/etc/samba/smb.conf`.
Il est fortement recommandé de faire une sauvegarde de l'original avant de commencer.

```bash
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.backup
```

### Le Partage Public (Anonyme)
Créons un dossier "Commun", lisible et inscriptible par tout le monde sur le réseau, sans mot de passe (Pratique pour des échanges de fichiers temporaires non critiques).

1. **Création du dossier sur Linux**
```bash
sudo mkdir -p /srv/samba/commun
# On donne les droits au groupe "nogroup" ou "nobody" géré par Samba
sudo chown nobody:nogroup /srv/samba/commun
sudo chmod 777 /srv/samba/commun
```

2. **Configuration dans Samba**
Ajoutez ce bloc à la toute fin de `/etc/samba/smb.conf` :
```ini
[Commun]
   comment = Espace d'échange public
   path = /srv/samba/commun
   browseable = yes
   guest ok = yes
   read only = no
   create mask = 0755
```

3. **Redémarrage**
```bash
sudo systemctl restart smbd
```

Désormais, depuis un PC Windows sur le même réseau, si l'on tape `\\IP-DU-SERVEUR-LINUX` dans l'explorateur de fichiers, le dossier "Commun" apparaît.

---

## 3. Le Partage Privé (Sécurisé par Mot de Passe)

Créons maintenant un dossier "Direction" accessible uniquement par l'utilisateur "Alice" après authentification.

1. **L'utilisateur Linux et Samba**
Alice doit exister en tant qu'utilisatrice Linux, MAIS elle doit aussi avoir un mot de passe spécifique pour Samba (géré par la commande `smbpasswd`).
```bash
# 1. Créer l'utilisateur système sans accès shell
sudo useradd -M -s /sbin/nologin alice

# 2. Créer le mot de passe Samba d'Alice
sudo smbpasswd -a alice
```

2. **Création du dossier protégé**
```bash
sudo mkdir -p /srv/samba/direction
sudo chown alice:alice /srv/samba/direction
# Seule Alice a les droits (700)
sudo chmod 700 /srv/samba/direction
```

3. **Configuration dans Samba**
```ini title="/etc/samba/smb.conf"
[Direction]
   comment = Dossier strictement confidentiel
   path = /srv/samba/direction
   browseable = yes
   guest ok = no
   valid users = alice
   read only = no
```
*Si Bob essaie d'ouvrir ce dossier depuis son PC Windows, Windows lui demandera immédiatement un identifiant et un mot de passe (qu'il n'a pas).*

---

## Sécurité et Ransomwares (Avertissement)

Déployer un serveur de fichiers Samba est très rapide. Mais attention : si un PC Windows d'un employé est infecté par un Ransomware (comme *LockBit*), le logiciel malveillant va scanner le réseau local, trouver le partage Samba, utiliser les droits de l'employé pour s'y connecter, et **chiffrer tous les fichiers situés sur le serveur Linux**.

Le serveur Linux lui-même ne plantera pas (le ransomware tourne sur le CPU Windows de l'employé), mais vos fichiers métiers partagés seront perdus.

La défense (Ops) contre ce scénario repose sur trois piliers :
1. Les permissions strictes (Alice ne doit pas avoir accès au dossier RH).
2. L'activation des **Snapshots** sur le système de fichiers (ZFS ou LVM) côté Linux.
3. Le durcissement strict du protocole : **Désactivez absolument SMBv1** dans la configuration Samba globale (`server min protocol = SMB2_02`).