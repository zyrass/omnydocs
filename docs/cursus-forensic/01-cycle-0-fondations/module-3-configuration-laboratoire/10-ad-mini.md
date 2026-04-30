---
title: 3.10 Active Directory mini (optionnel)
description: Mise en place optionnelle d'un Active Directory miniature pour reproduire un environnement domaine. Samba AD comme alternative légère à Windows Server, configuration basique, intégration des postes.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Active Directory
  - Samba AD
  - Domaine
data-level: 🟡
---

# 3.10 Active Directory mini (optionnel)

!!! quote "L'analogie de la mairie centrale"

    Dans une commune, la mairie centralise l'état civil, les permis, les inscriptions. Sans elle, chaque service tournerait avec ses propres registres incohérents. Active Directory joue ce rôle pour un parc Windows. Il centralise utilisateurs, groupes, politiques, permissions. La majorité des PME comme ARTECH n'en ont pas et utilisent des comptes locaux. Mais beaucoup d'entreprises plus matures en ont. Ce chapitre vous montre comment déployer un mini-AD pour vous y entraîner.

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 4 heures |
| Niveau | Pratique avancé |
| Caractère | OPTIONNEL pour le cycle 0 |

## 1. Quand activer ce chapitre

| Cas | Recommandation |
|---|---|
| Apprenant débutant | Ignorer, postes en workgroup suffit |
| Cycle 0 - 1 | Optionnel |
| Cycle 2 et 3 | Recommandé |
| Forensic AD attendu en pro | Indispensable |

## 2. Choix - Windows Server vs Samba AD

| Critère | Windows Server | Samba AD |
|---|---|---|
| Coût | Eval 180 jours puis licence | Gratuit |
| Ressources | 4 Go RAM minimum | 1-2 Go RAM |
| Réalisme | Maximum | Très bon |
| Apprentissage | Plus standard pro | Tout aussi pédagogique |
| Maintenance | Standard MS | Apt/dpkg |

**Recommandation OmnyAcademy** : Samba AD sur le serveur Debian existant ou un Pi 4 dédié.

## 3. Installation Samba AD sur Debian

### 3.1 Préparation

```bash
# Sur le serveur Debian (autre que le partage Samba existant)
# Idéalement, Pi 4 dédié à 192.168.50.11

# Hostname FQDN
sudo hostnamectl set-hostname dc01.lab.local
```

### 3.2 /etc/hosts

```text
127.0.0.1       localhost
192.168.50.11   dc01.lab.local dc01
```

### 3.3 Désinstallation Samba existant

```bash
sudo systemctl stop smbd nmbd winbind 2>/dev/null
sudo systemctl disable smbd nmbd winbind 2>/dev/null

sudo apt purge samba samba-common samba-common-bin -y
sudo apt autoremove -y

# Suppression configs résiduelles
sudo rm -rf /etc/samba/
```

### 3.4 Installation Samba AD-DC

```bash
sudo apt install samba smbclient krb5-user winbind libnss-winbind libpam-winbind ldb-tools -y
```

Lors de l'installation Kerberos :

| Paramètre | Valeur |
|---|---|
| Royaume Kerberos | LAB.LOCAL |
| Serveur Kerberos | dc01.lab.local |
| Serveur d'admin | dc01.lab.local |

### 3.5 Provisionnement du domaine

```bash
# Stop Samba
sudo systemctl stop samba-ad-dc

# Reset config
sudo mv /etc/samba/smb.conf /etc/samba/smb.conf.original

# Provisionnement
sudo samba-tool domain provision \
    --realm=LAB.LOCAL \
    --domain=LAB \
    --server-role=dc \
    --dns-backend=SAMBA_INTERNAL \
    --adminpass='AdminLab2026!' \
    --use-rfc2307
```

### 3.6 Configuration DNS

```bash
sudo vi /etc/resolv.conf
```

```text
nameserver 192.168.50.11
nameserver 192.168.50.1
search lab.local
```

### 3.7 Démarrage du service

```bash
sudo systemctl unmask samba-ad-dc
sudo systemctl enable samba-ad-dc
sudo systemctl start samba-ad-dc

# Vérification
sudo systemctl status samba-ad-dc
samba-tool domain info 192.168.50.11
```

## 4. Création utilisateurs et groupes

```bash
# Création utilisateurs
sudo samba-tool user create dupont 'Dupont2026!' --given-name='Pierre' --surname='Dupont'
sudo samba-tool user create lemoine 'Lemoine2026!' --given-name='Stéphane' --surname='Lemoine'
sudo samba-tool user create lefebvre 'Lefebvre2026!' --given-name='Hélène' --surname='Lefebvre'
sudo samba-tool user create stagiaire 'Stage2026' --given-name='Paul' --surname='Stagiaire'

# Création groupes
sudo samba-tool group add Compta
sudo samba-tool group add Direction
sudo samba-tool group add Stagiaires

# Affectation
sudo samba-tool group addmembers Compta dupont
sudo samba-tool group addmembers Direction lefebvre
sudo samba-tool group addmembers Stagiaires stagiaire

# Liste
sudo samba-tool user list
sudo samba-tool group list
```

## 5. Joindre les postes Windows au domaine

### 5.1 Sur chaque poste Windows

```powershell
# Configurer DNS pointant sur le DC
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses "192.168.50.11","1.1.1.1"

# Joindre au domaine
Add-Computer -DomainName "LAB.LOCAL" -Credential (Get-Credential) -Restart
```

Lors du Get-Credential, entrer :

```text
Utilisateur : LAB\Administrator
Mot de passe : AdminLab2026!
```

### 5.2 Tests post-jonction

```powershell
# Connexion en utilisateur du domaine
# Login : LAB\dupont, Pwd : Dupont2026!

# Vérifications
whoami
whoami /groups
nltest /sc_query:LAB.LOCAL
```

## 6. Politiques de groupe basiques

```bash
# Sur le DC, créer une GPO simple
sudo samba-tool gpo create "ARTECH_PolitiqueMotDePasse" \
    --user=Administrator --password='AdminLab2026!'

# Lister
sudo samba-tool gpo listall
```

## 7. Forensic AD - Concepts importants

| Élément | Localisation | Forensic |
|---|---|---|
| ntds.dit | C:\Windows\NTDS\ (DC Windows) ou /var/lib/samba/private/sam.ldb | Base utilisateurs/hashes |
| GPO | SYSVOL | Configuration appliquée |
| Logs Security | DC | Logons réussis/échoués |
| Kerberos tickets | RAM | Pass-the-ticket attaque |
| Kerberos AS-REP roasting | Sans pré-auth | Cassage offline |

## 8. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Alternative à Windows Server ? | Samba AD |
| 2 | Realm Kerberos labo ? | LAB.LOCAL |
| 3 | DNS pour les postes Windows ? | DC à 192.168.50.11 |
| 4 | Base utilisateurs DC Samba ? | sam.ldb dans /var/lib/samba/private |
| 5 | Joindre poste Windows ? | Add-Computer -DomainName |

---

**Chapitre suivant** : [3.11 Kali Linux portable attaquant](03-11-kali-attaquant.md)
