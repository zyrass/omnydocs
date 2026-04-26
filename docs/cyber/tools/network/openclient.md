---
description: "OpenConnect — Le client VPN open-source compatible avec les passerelles d'entreprise propriétaires (Cisco AnyConnect, Palo Alto, Pulse Secure)."
icon: lucide/book-open-check
tags: ["INFRA", "VPN", "RÉSEAU", "SÉCURITÉ", "RED TEAM"]
---

# OpenConnect — L'Accès Universel aux VPN d'Entreprise

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="9.0+"
  data-time="~30 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/openconnect.svg" width="250" align="center" alt="OpenConnect Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Passe-partout"
    Imaginez que de nombreuses entreprises utilisent des serrures électroniques propriétaires très chères pour laisser entrer leurs employés (VPN Cisco, Palo Alto, Pulse Secure). Chacune vous oblige à installer son application spécifique. **OpenConnect** est un passe-partout universel. C'est un outil open-source capable de parler le langage de toutes ces différentes serrures, vous permettant d'entrer sans avoir besoin d'installer le logiciel fermé de chaque constructeur.

**OpenConnect** est un client VPN SSL conçu à l'origine pour remplacer Cisco AnyConnect. Il a depuis évolué pour prendre en charge Juniper/Pulse Secure, Palo Alto Networks GlobalProtect, et F5 Big-IP SSL VPN.

Il est particulièrement prisé sur Linux et dans les distributions orientées sécurité (comme Kali Linux) car il permet de se connecter aux infrastructures des clients lors d'audits sans polluer sa machine avec des agents logiciels propriétaires invasifs.

<br>

---

## 🛠️ Usage Opérationnel — Configuration Client

### 1. Connexion Basique (Cisco AnyConnect)

La syntaxe de base requiert simplement l'URL de la passerelle VPN.

```bash title="Connexion à une passerelle Cisco"
sudo openconnect https://vpn.entreprise.com
```
*Le client va s'authentifier auprès du serveur, demander le nom d'utilisateur et le mot de passe, puis établir le tunnel.*

### 2. Spécification du Protocole (Pulse Secure, Palo Alto)

Si la cible n'est pas Cisco, vous devez spécifier le protocole réseau cible avec le flag `--protocol`.

```bash title="Connexion à différentes passerelles"
# Pour un VPN Pulse Secure (Ivanti)
sudo openconnect --protocol=nc https://vpn.entreprise.com

# Pour un VPN Palo Alto GlobalProtect
sudo openconnect --protocol=gp https://vpn.entreprise.com

# Pour un VPN F5 BIG-IP
sudo openconnect --protocol=f5 https://vpn.entreprise.com
```

### 3. Exécution en Arrière-plan (Daemon)

Comme pour OpenVPN, il est souvent utile de lancer le client en tâche de fond.

```bash title="Exécution silencieuse"
# -b : Lance en background après authentification
sudo openconnect -b https://vpn.entreprise.com
```

<br>

---

## 💀 Red Team & Evasion

En Red Team ou lors de Pentests internes, OpenConnect est un atout majeur pour l'accès initial ou le pivotement, particulièrement dans des scénarios de "Bring Your Own Device" (BYOD).

### 1. Évitement des contrôles de conformité (Host Checker)

Les VPN d'entreprise incluent souvent des outils de "Posture Assessment" (comme Cisco CSD ou Pulse Secure Host Checker) qui vérifient si votre machine a un antivirus à jour, fait partie du domaine, etc.

OpenConnect permet souvent de **contourner ces vérifications ou de les simuler** via des scripts wrappers (ex: `csd-wrapper.sh` pour Cisco), ce qui permet à l'attaquant de connecter sa propre machine Kali directement sur le réseau interne de l'entreprise sans posséder un poste fourni par l'employeur.

### 2. Automatisation (Non-Interactive Mode)

Pour s'intégrer dans des scripts d'attaque automatisés, on peut passer les identifiants directement sans interaction (utile si des identifiants valides ont été obtenus via Phishing ou OSINT).

```bash title="Connexion automatisée avec identifiants"
echo "MonSuperMotDePasse" | sudo openconnect -u "john.doe" --passwd-on-stdin https://vpn.entreprise.com
```

<br>

---

## 🏗️ Architecture et Place dans le Réseau

```mermaid
---
config:
  theme: "base"
---
flowchart LR
    KALI["Machine Pentester<br>(Kali Linux)"] -- "OpenConnect (Client Universel)" --> INTERNET((Internet))
    INTERNET -- "Trafic SSL" --> PASSERELLE["Passerelle Propriétaire<br>(Cisco, Palo Alto, Pulse)"]
    PASSERELLE --> LAN["Réseau Interne Entreprise"]
    
    style KALI fill:#ff4c4c,stroke:#333,stroke-width:2px,color:#fff
    style PASSERELLE fill:#34495e,stroke:#333,stroke-width:2px,color:#fff
    style LAN fill:#2ecc71,stroke:#333,stroke-width:2px,color:#fff
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    OpenConnect est la solution universelle et open-source face à l'hétérogénéité des passerelles VPN d'entreprise. Pour l'auditeur et l'attaquant, c'est l'outil qui garantit un accès fluide et transparent au réseau cible, tout en offrant la possibilité de contourner les vérifications d'intégrité souvent imposées par les clients VPN officiels.

> Une fois connecté avec OpenConnect, n'oubliez pas d'utiliser des outils de découverte réseau comme **[Nmap](./nmap.md)** ou **[CrackMapExec](./cme.md)** pour explorer votre nouvel environnement.
