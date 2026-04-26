---
description: "Module 4 - Création automatisée de l'infrastructure (IaC) via Vagrant et VirtualBox, avec configuration des adresses IP."
---

# Module 4 - Provisioning via Vagrant

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Vagrant 2.4, VirtualBox 7"
  data-time="~45 min">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'architecte et les ouvriers"
    Créer des VMs à la main (cliquer sur "Nouvelle", allouer la RAM, monter l'ISO d'Ubuntu, installer l'OS), c'est comme construire une maison brique par brique. Si vous vous trompez, vous devez tout casser. Vagrant est votre architecte : vous lui donnez un plan (le fichier texte `Vagrantfile`) et il construit les 3 maisons en 5 minutes, exactement à l'identique, de manière automatique. C'est l'essence de l'**Infrastructure as Code (IaC)**.

## 4.1 - Objectifs pédagogiques

À la fin de ce module, l'apprenant doit être capable de :

- Définir le concept d'Infrastructure as Code (IaC).
- Lire et modifier un `Vagrantfile` basique (allocation RAM, adresse IP).
- Déployer simultanément 3 VMs Linux via la commande `vagrant up`.
- Détruire proprement son laboratoire avec `vagrant destroy`.

<br>

---

## 4.2 - Installation des pré-requis (Windows)

Si vous êtes sous Linux ou Mac, adaptez les commandes. Sous Windows 10/11, la méthode la plus propre est d'utiliser le gestionnaire de paquets `winget` intégré au système.

```powershell title="PowerShell - Installation des pré-requis sur Windows"
# Ouvre PowerShell en mode Administrateur
# Installation de VirtualBox (Hyperviseur)
winget install Oracle.VirtualBox

# Installation de Vagrant (Orchestrateur)
winget install Hashicorp.Vagrant
```

!!! caution "Redémarrage requis"
    Après l'installation de Vagrant, il est impératif de **redémarrer votre PC**. Vagrant modifie les variables d'environnement système (le PATH) pour être accessible depuis n'importe quel dossier. Sans redémarrage, la commande `vagrant` renverra une erreur "commande introuvable".

<br>

---

## 4.3 - Organisation des dossiers

La propreté est cruciale. Créez un dossier racine `HomeLab_SOC` sur votre disque dur (idéalement sur un SSD, car 3 VMs génèrent beaucoup d'entrées/sorties disque).

```text title="Arborescence du projet"
HomeLab_SOC/
├── Vagrantfile              # Le plan de construction
└── scripts/
    ├── install_wazuh.sh     # Script d'installation du SIEM
    └── install_agent.sh     # Script d'installation des cibles
```

<br>

---

## 4.4 - Le fichier Vagrantfile (Infrastructure as Code)

Dans le dossier `HomeLab_SOC`, créez un fichier nommé exactement `Vagrantfile` (sans extension `.txt`). Copiez le code ci-dessous. 

Prenez 2 minutes pour lire les commentaires (lignes commençant par `#`), ils expliquent chaque action.

```ruby title="Vagrantfile - Déploiement des 3 VMs Ubuntu 24.04"
# Spécifie la version minimale de l'API Vagrant
Vagrant.configure("2") do |config|
  
  # Image de base : Ubuntu 24.04 LTS packagée par Bento (Chef)
  config.vm.box = "bento/ubuntu-24.04"

  # ==========================================
  # VM 1 : Le Défenseur (Wazuh SIEM)
  # ==========================================
  config.vm.define "wazuh-server" do |wazuh|
    wazuh.vm.hostname = "wazuh-server"
    # Configuration du réseau privé (Host-Only)
    wazuh.vm.network "private_network", ip: "192.168.56.10"
    
    # Configuration VirtualBox spécifique
    wazuh.vm.provider "virtualbox" do |vb|
      vb.name = "SOC_Wazuh_Server"
      vb.memory = "6144" # 6 Go de RAM obligatoires pour Indexer
      vb.cpus = 2
    end
  end

  # ==========================================
  # VM 2 : La Cible (Ubuntu Target)
  # ==========================================
  config.vm.define "ubuntu-target" do |target|
    target.vm.hostname = "ubuntu-target"
    target.vm.network "private_network", ip: "192.168.56.20"
    
    target.vm.provider "virtualbox" do |vb|
      vb.name = "SOC_Ubuntu_Target"
      vb.memory = "1024" # 1 Go est suffisant
      vb.cpus = 1
    end
  end

  # ==========================================
  # VM 3 : L'Attaquant (Ubuntu Hacker)
  # ==========================================
  config.vm.define "ubuntu-hacker" do |hacker|
    hacker.vm.hostname = "ubuntu-hacker"
    hacker.vm.network "private_network", ip: "192.168.56.30"
    
    hacker.vm.provider "virtualbox" do |vb|
      vb.name = "SOC_Ubuntu_Hacker"
      vb.memory = "1024"
      vb.cpus = 1
    end
  end

end
```

_Ce code crée 3 machines distinctes, attribue les IP statiques, définit la RAM, et nomme les VMs proprement dans l'interface VirtualBox._

<br>

---

## 4.5 - Lancement et gestion du laboratoire

Ouvrez un terminal (Powershell ou Bash) dans votre dossier `HomeLab_SOC` et tapez :

```bash title="Commandes Vagrant essentielles"
# Lancer la création des 3 VMs en arrière-plan
vagrant up

# Vérifier le statut des VMs (running, saved, poweroff)
vagrant status

# Se connecter en SSH à la VM cible
vagrant ssh ubuntu-target

# Éteindre proprement toutes les VMs
vagrant halt

# Supprimer le laboratoire (si vous avez tout cassé)
vagrant destroy -f
```

La première exécution de `vagrant up` prendra du temps (téléchargement de l'image Ubuntu de ~600 Mo). Les lancements suivants prendront moins de 30 secondes.

<br>

---

## 4.6 - Points de vigilance

- L'indentation du `Vagrantfile` (qui utilise la syntaxe Ruby) n'est pas aussi stricte qu'en Python, mais une erreur de `end` manquant fera planter le script.
- Si le téléchargement de la box `bento` est très lent, c'est que les serveurs Hashicorp sont saturés. Laissez tourner.
- N'ouvrez **jamais** l'interface VirtualBox pour modifier la RAM ou les IP à la main. Tout doit être géré via le `Vagrantfile` pour garantir le principe d'Infrastructure as Code.

<br>

---

## 4.7 - Axes d'amélioration vs projet original

| Constat dans le projet 2025 | Amélioration recommandée |
|---|---|
| Le Vagrantfile d'origine intégrait l'installation de Wazuh via un script shell long (`config.vm.provision`). | Séparer l'infrastructure (Vagrant) et la configuration logicielle (Wazuh). Le provisioner Vagrant cache les erreurs d'installation. Il vaut mieux que l'apprenant lance le script manuellement en SSH pour voir les logs d'erreur éventuels. |
| Utilisation de l'image `ubuntu/jammy64`. | Passage sur `bento/ubuntu-24.04` qui est généralement mieux optimisée pour VirtualBox (Guest Additions pré-installées correctement). |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Grâce à l'Infrastructure as Code (IaC), reconstruire votre laboratoire entier suite à une erreur fatale ne prend désormais qu'une seule commande (`vagrant destroy && vagrant up`) et 5 minutes d'attente, contre des heures d'installation manuelle d'OS.

> Notre fondation réseau et système est prête et fonctionnelle. Les 3 VMs tournent. Il est temps d'installer le cerveau de notre SOC sur la machine défensive dans le **[Module 5 : Installation du SIEM Wazuh →](./05-installation-wazuh.md)**
