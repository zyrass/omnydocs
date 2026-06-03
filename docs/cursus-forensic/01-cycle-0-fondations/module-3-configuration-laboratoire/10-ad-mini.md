---
description: "Mise en place optionnelle d'un Active Directory miniature pour reproduire un environnement domaine. Samba AD comme alternative légère à Windows Server, configuration basique, intégration des postes."
icon: lucide/network
tags: ["ACTIVE DIRECTORY", "SAMBA AD", "DOMAINE", "LINUX"]
---

# Active Directory mini (optionnel)

<div
  class="omny-meta"
  data-level="🟡 Standard"
  data-version="Modèle 2026"
  data-time="4 heures">
</div>

!!! note "**Livrables :** _Un Contrôleur de Domaine (DC) Samba opérationnel et des postes joints au domaine_"
!!! note "**Auto-explication :** _10 minutes_"

<br>

---

<br>

!!! quote "L'analogie de la mairie centrale"

    Dans une commune, la mairie centralise l'état civil, les permis, et les inscriptions. Sans elle, chaque service fonctionnerait avec ses propres registres, générant incohérences et fraudes. **Active Directory** (AD) joue ce rôle pour un parc informatique. Il centralise les utilisateurs, les groupes, les politiques de sécurité (GPO) et les permissions. Bien que la majorité des petites PME comme notre ARTECH initiale utilisent des comptes locaux isolés, les entreprises matures s'appuient sur l'AD. Ce chapitre vous montre comment déployer un mini-AD Linux pour préparer les exercices Forensic avancés (Kerberos, NTDS).

## Objectifs pédagogiques

!!! tip "À la fin de ce chapitre, vous serez capable de :"

    - Comprendre l'architecture logique d'un domaine Active Directory.
    - Déployer un Contrôleur de Domaine fonctionnel sous Linux avec **Samba AD**.
    - Provisionner des utilisateurs, des groupes, et des stratégies (GPO) en ligne de commande.
    - Joindre des postes Windows 11 au domaine et analyser les traces Forensic générées.

<br>

---

<br>

## Quand activer ce chapitre ?

Ce chapitre modifie profondément l'architecture du laboratoire. 

> Le tableau ci-dessous indique si vous devez réaliser ce chapitre maintenant :

| Cas d'usage | Recommandation OmnyAcademy |
|---|---|
| **Apprenant débutant (Cycle 0 et 1)** | **Ignorer**. La configuration *Workgroup* des postes (Chapitres précédents) est suffisante. |
| **Apprenant intermédiaire (Cycle 2)** | Optionnel, mais fortement recommandé pour comprendre l'escalade de privilèges. |
| **Forensic avancé (Cycle 3)** | **Indispensable**. La majorité des attaques modernes (Pass-the-Hash, Golden Ticket) ciblent l'AD. |

<br>

---

<br>

## Le choix technologique : Windows Server vs Samba AD

Pour créer un Active Directory, la norme absolue est *Windows Server*. Cependant, il demande beaucoup de ressources.

> Comparatif des solutions pour un Homelab :

| Critère | Windows Server (Officiel) | Samba AD (Linux) |
|---|---|---|
| **Coût** | Licence requise (ou Évaluation 180 jours) | 100% Gratuit et Open Source |
| **Ressources** | 4 Go de RAM minimum | 1 à 2 Go de RAM suffisent |
| **Réalisme** | Maximum (C'est la norme) | Très bon (GPO et Kerberos supportés) |
| **Forensic** | Base NTDS.dit standard | Base LDB spécifique (Mais réseau identique) |

**Recommandation :** Nous allons déployer Samba AD sur le serveur Debian existant (Ou idéalement sur un Raspberry Pi 4 dédié à l'adresse `192.168.50.11`).

<br>

---

<br>

## Installation de Samba AD sur Debian

### Préparation de l'hôte

```bash title="Commandes Linux ( Prérequis système ) - Définition du nom de domaine complet (FQDN)"
# Fixer le hostname du Contrôleur de Domaine
sudo hostnamectl set-hostname dc01.lab.local

# Édition du fichier hosts local
sudo vi /etc/hosts
```

```text title="Fichier /etc/hosts"
127.0.0.1       localhost
192.168.50.11   dc01.lab.local dc01
```

> Pour rappel, FQDN signifie *Fully Qualified Domain Name* (Nom de Domaine Complet). Si le fichier hosts a été mis à jour il faut mettre à jour le fichier hostname avec la commande hostnamectl.

!!! warning "La configuration du fichier /etc/hosts et l'utilisation de la commande hostnamectl est propre à Debian et Ubuntu. Pour d'autres distributions Linux, les commandes peuvent varier."

### Nettoyage (Si Samba classique était installé)

!!! quote "Samba AD est incompatible avec un simple serveur de fichiers Samba. Il faut purger l'ancien."

```bash title="Commandes Linux ( Nettoyage de l'ancien Samba ) - Purge des paquets"
# Arrêt des services classiques
sudo systemctl stop smbd nmbd winbind 2>/dev/null

# Désinstallation complète
sudo apt purge samba samba-common samba-common-bin -y
sudo apt autoremove -y

# Suppression des configurations résiduelles
sudo rm -rf /etc/samba/
```

### Installation et Provisionnement du Domaine

```bash title="Commandes Linux ( Déploiement AD ) - Installation des composants"
sudo apt install samba smbclient krb5-user winbind libnss-winbind libpam-winbind ldb-tools -y
```
    
!!! note "Lors de l'installation de Kerberos, l'assistant vous posera 3 questions :"

    - Royaume Kerberos : `LAB.LOCAL` (En majuscules)
    - Serveur Kerberos : `dc01.lab.local`
    - Serveur d'admin : `dc01.lab.local`

```bash title="Commandes Linux - Provisionnement de la forêt"
# Supprimer le fichier conf par défaut
sudo rm /etc/samba/smb.conf 2>/dev/null

# Provisionner le domaine "lab.local"
sudo samba-tool domain provision \
    --realm=LAB.LOCAL \
    --domain=LAB \
    --server-role=dc \
    --dns-backend=SAMBA_INTERNAL \
    --adminpass='AdminLab2026!' \
    --use-rfc2307
```

_Le provisionnement de la forêt consiste à configurer le serveur Samba AD en tant que contrôleur de domaine, à configurer les paramètres DNS, à configurer les paramètres Kerberos, à configurer les paramètres LDAP et à configurer les paramètres Samba AD._

!!! note "La commande samba-tool domain provision est une commande complexe qui nécessite de nombreuses options. Pour plus d'informations sur les options de la commande samba-tool domain provision, veuillez consulter la documentation officielle."

!!! info "Il est important de noter que le Realm Kerberos doit être écrit en majuscules."

### Démarrage des services

!!! quote "Le DNS de la machine doit pointer vers elle-même pour que la résolution AD fonctionne."

```text title="Configuration DNS et Service - Fichier /etc/resolv.conf"
nameserver 192.168.50.11
search lab.local
```

```bash title="Commandes Linux - Activation du Contrôleur"
sudo systemctl unmask samba-ad-dc
sudo systemctl enable samba-ad-dc
sudo systemctl start samba-ad-dc

# Vérification fonctionnelle
samba-tool domain info 192.168.50.11
```

<br>

---

<br>

## Création des Utilisateurs et Groupes

!!! quote "Nous allons recréer la structure RH de l'entreprise ARTECH au sein de l'AD."

```bash title="Commandes Linux ( Gestion de l'AD en CLI ) - Gestion des identités Samba"
# Création des utilisateurs du domaine
sudo samba-tool user create dupont 'Dupont2026!' --given-name='Pierre' --surname='Dupont'
sudo samba-tool user create lemoine 'Lemoine2026!' --given-name='Stéphane' --surname='Lemoine'
sudo samba-tool user create lefebvre 'Lefebvre2026!' --given-name='Hélène' --surname='Lefebvre'
sudo samba-tool user create stagiaire 'Stage2026' --given-name='Paul' --surname='Stagiaire'

# Création des groupes de sécurité
sudo samba-tool group add Compta
sudo samba-tool group add Direction
sudo samba-tool group add Stagiaires

# Affectation des utilisateurs dans les groupes
sudo samba-tool group addmembers Compta dupont
sudo samba-tool group addmembers Direction lefebvre
sudo samba-tool group addmembers Stagiaires stagiaire
```

<br>

---

<br>

## Intégration des postes Windows 11 au Domaine

Pour qu'un PC rejoigne le domaine, **il doit impérativement utiliser le DC comme serveur DNS principal.**

### Sur les postes WIN-COMPTA-01 et WIN-STAGE-01

```powershell title="Commandes PowerShell (Jonction au Domaine ) - Côté Client Windows"
# 1. Pointer le DNS vers notre DC Samba (192.168.50.11)
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses "192.168.50.11","1.1.1.1"

# 2. Joindre le poste au domaine LAB.LOCAL
Add-Computer -DomainName "LAB.LOCAL" -Credential (Get-Credential) -Restart
```

!!! warning "Lors de l'invite `Get-Credential`, entrez :"

    - Utilisateur : `LAB\Administrator`
    - Mot de passe : `AdminLab2026!`

<br>

### Tests post-jonction

Au redémarrage, connectez-vous avec l'utilisateur du domaine (Ex: `LAB\dupont` / `Dupont2026!`).

```powershell title="Commandes PowerShell - Vérification de confiance"
# Vérifier l'identité actuelle
whoami
# Résultat attendu : lab\dupont

# Vérifier la relation de confiance avec le Contrôleur de Domaine
nltest /sc_query:LAB.LOCAL
```

<br>

---

<br>

## Concepts Forensic sur Active Directory

Si vous avez activé ce laboratoire, vous devrez chasser les menaces au niveau du domaine.

> Le tableau ci-dessous indique où chercher les preuves en environnement AD :

| Type d'Artefact | Localisation physique | Intérêt Forensic (Incident Response) |
|---|---|---|
| **Base de données AD** | `C:\Windows\NTDS\` (Win) ou `/var/lib/samba/private/` (Linux) | Contient tous les Hashes NTLM de l'entreprise. |
| **GPO (Stratégies)** | Dossier partagé `SYSVOL` | Les ransomwares y placent souvent des scripts de déploiement automatiques. |
| **Tickets Kerberos** | Mémoire RAM (LSASS) | Détection des attaques de type *Pass-The-Ticket* ou *Golden Ticket*. |
| **Journaux de sécurité** | Observateur d'événements du DC (ID 4624, 4625...) | Traces de bruteforce, connexions illégitimes. |

<br>

---

<br>

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Avec cet Active Directory miniature, votre laboratoire passe d'un environnement PME basique à une infrastructure d'entreprise mature. La gestion centralisée via Kerberos et LDAP introduit de nouvelles vulnérabilités redoutables (AS-REP Roasting, DCSync). Si vous avez déployé ce module, vous êtes prêt pour les scénarios de compromission totale de domaine du Cycle 3.

> [Chapitre suivant : 3.11 Kali Linux portable attaquant →](11-kali-attaquant.md)
>
> [Retour à l'index →](./index.md)

<br>
