---
description: "VBoxManage — L'interface en ligne de commande complète de VirtualBox. Automatisez la création, la gestion et le contrôle de vos machines virtuelles sans interface graphique."
icon: lucide/book-open-check
tags: ["VIRTUALISATION", "VIRTUALBOX", "CLI", "AUTOMATISATION", "VBOXMANAGE"]
---

# VBoxManage — VirtualBox en Ligne de Commande

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="7.x"
  data-time="~20 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Cockpit vs les Commandes Radio"
    Utiliser l'interface graphique VirtualBox, c'est piloter depuis le cockpit avec les boutons et jauges visibles. **VBoxManage**, c'est piloter par commandes radio : plus rapide, scriptable, et surtout utilisable depuis un serveur sans interface graphique (headless).

    Un administrateur système qui déploie 10 VMs identiques ne va pas cliquer 200 fois dans l'interface. Il écrit un script `vboxmanage` de 30 lignes, l'exécute, et revient 5 minutes plus tard avec 10 VMs prêtes.

`VBoxManage` est l'outil CLI officiel de VirtualBox. Il expose **100% des fonctionnalités** de l'interface graphique — et davantage. Indispensable pour l'automatisation, les serveurs headless et l'intégration avec des outils comme **Vagrant**.

<br>

---

## Commandes Fondamentales

### Lister les VMs

```bash title="Inventaire des machines virtuelles"
# Toutes les VMs enregistrées
VBoxManage list vms

# VMs actuellement en cours d'exécution
VBoxManage list runningvms

# Exemple de sortie :
# "Ubuntu-24.04-Server" {a1b2c3d4-e5f6-...}
# "Kali-Linux-2024" {f6e5d4c3-b2a1-...}
```

### Démarrer et arrêter une VM

```bash title="Contrôle du cycle de vie"
# Démarrer avec interface graphique
VBoxManage startvm "Ubuntu-24.04-Server"

# Démarrer en mode headless (sans fenêtre — pour les serveurs)
VBoxManage startvm "Ubuntu-24.04-Server" --type headless

# Arrêt propre (équivalent du bouton d'extinction)
VBoxManage controlvm "Ubuntu-24.04-Server" acpipowerbutton

# Arrêt forcé (= débrancher la prise)
VBoxManage controlvm "Ubuntu-24.04-Server" poweroff

# Suspendre (pause)
VBoxManage controlvm "Ubuntu-24.04-Server" savestate
```

### Gestion des Snapshots

```bash title="Snapshots en ligne de commande"
# Créer un snapshot
VBoxManage snapshot "Kali-Linux-2024" take "avant-lab-metasploit" \
  --description "VM propre avant exercice Metasploit"

# Lister les snapshots d'une VM
VBoxManage snapshot "Kali-Linux-2024" list

# Restaurer un snapshot (la VM doit être éteinte)
VBoxManage snapshot "Kali-Linux-2024" restore "avant-lab-metasploit"

# Supprimer un snapshot (libère l'espace disque)
VBoxManage snapshot "Kali-Linux-2024" delete "avant-lab-metasploit"
```

<br>

---

## Créer une VM Complète par Script

```bash title="Script de création d'une VM Ubuntu Server"
#!/bin/bash
VM_NAME="Ubuntu-24.04-Server"
ISO="/path/to/ubuntu-24.04-server.iso"
DISK="/path/to/vms/${VM_NAME}.vdi"

# 1. Créer et enregistrer la VM
VBoxManage createvm --name "$VM_NAME" --ostype "Ubuntu_64" --register

# 2. Configurer CPU et RAM
VBoxManage modifyvm "$VM_NAME" --cpus 2 --memory 2048 --vram 16

# 3. Configurer le réseau (NAT)
VBoxManage modifyvm "$VM_NAME" --nic1 nat

# 4. Créer le disque dur (20 Go, dynamique)
VBoxManage createhd --filename "$DISK" --size 20480 --format VDI

# 5. Attacher un contrôleur SATA et le disque
VBoxManage storagectl "$VM_NAME" --name "SATA Controller" --add sata
VBoxManage storageattach "$VM_NAME" \
  --storagectl "SATA Controller" --port 0 --device 0 \
  --type hdd --medium "$DISK"

# 6. Attacher l'ISO d'installation
VBoxManage storagectl "$VM_NAME" --name "IDE Controller" --add ide
VBoxManage storageattach "$VM_NAME" \
  --storagectl "IDE Controller" --port 0 --device 0 \
  --type dvddrive --medium "$ISO"

# 7. Démarrer
VBoxManage startvm "$VM_NAME"
echo "VM $VM_NAME démarrée !"
```

_Ce script est le point de départ d'une infrastructure automatisée. **Vagrant** abstrait exactement ce niveau de commandes pour vous permettre de décrire vos VMs en Ruby (Vagrantfile) sans écrire vous-même les appels `VBoxManage`._

<br>

---

## Transfert de Fichiers et Port Forwarding

```bash title="Rediriger un port de l'hôte vers la VM"
# Rediriger le port 2222 de l'hôte vers le port 22 (SSH) de la VM
VBoxManage modifyvm "Ubuntu-24.04-Server" \
  --natpf1 "ssh,tcp,,2222,,22"

# Connexion SSH depuis l'hôte vers la VM
ssh -p 2222 user@localhost
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    `VBoxManage` transforme VirtualBox d'un outil graphique en **plateforme de virtualisation scriptable**. Dès que vous devez gérer plus de 2 VMs, créer des labs reproductibles, ou automatiser des opérations de maintenance, la ligne de commande devient indispensable. La maîtrise de `VBoxManage` est également le premier pas vers la compréhension de **Vagrant**, qui en est l'abstraction de haut niveau.

> [Vagrant — Automatiser la création d'environnements de développement →](./vagrant.md)