---
description: "Protéger les ports réseau de son serveur Linux de manière simplifiée grâce à Uncomplicated Firewall (UFW)."
icon: lucide/book-open-check
tags: ["UFW", "FIREWALL", "IPTABLES", "SECURITE", "RESEAU"]
---

# Pare-Feu Simplifié (UFW)

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>

!!! quote "Garder les portes fermées"
    _Au cœur du noyau Linux (Kernel) réside `Netfilter`, le véritable moteur de filtrage réseau, souvent manipulé via les complexes commandes `iptables` ou `nftables`. Pour éviter les erreurs catastrophiques de syntaxe, Canonical (Ubuntu) a créé **UFW (Uncomplicated Firewall)**. Son but : rendre la configuration du pare-feu aussi simple que de dire "Ouvre le port 80" et "Ferme tout le reste"._

## Le Principe du Pare-Feu Hôte

Même si votre serveur est hébergé chez un Cloud Provider (AWS, OVH) qui propose un "Security Group" (Pare-feu matériel/virtuel externe), il est d'une importance capitale de configurer un pare-feu **directement sur l'hôte Linux**. C'est la défense en profondeur (Defense in Depth).

La règle d'or d'un pare-feu est le **Default Deny** (Refus par défaut) :
> On bloque absolument tout le trafic entrant par défaut, et on n'autorise explicitement que les services dont on a besoin.

```mermaid
graph LR
    Internet[Internet (Hackers & Clients)] --> PareFeu{UFW <br/> Règle: DEFAULT DENY}
    
    PareFeu -->|Requête HTTP Port 80| Allow1[✓ Autorisé: Nginx]
    PareFeu -->|Requête SSH Port 22| Allow2[✓ Autorisé: sshd]
    PareFeu -->|Scan Telnet Port 23| Drop1[❌ Jeté (Drop) Silencieusement]
    PareFeu -->|Attaque BDD Port 3306| Drop2[❌ Jeté (Drop) Silencieusement]
    
    style PareFeu fill:#e67e22,stroke:#fff,stroke-width:2px,color:#fff
    style Allow1 fill:#27ae60,stroke:#fff,color:#fff
    style Allow2 fill:#27ae60,stroke:#fff,color:#fff
    style Drop1 fill:#c0392b,stroke:#fff,color:#fff
    style Drop2 fill:#c0392b,stroke:#fff,color:#fff
```

---

## Configuration Basique de UFW

### 1. Activer le Pare-Feu... Prudemment !
Avant d'activer UFW, vous devez **IMPÉRATIVEMENT** autoriser le port SSH (22). Si vous activez le pare-feu sans faire cela, vous serez instantanément bloqué en dehors de votre propre serveur VPS !

```bash
# Étape 1 : Autoriser la connexion SSH
sudo ufw allow ssh
# (Ou plus précisément : sudo ufw allow 22/tcp)

# Étape 2 : Activer UFW
sudo ufw enable
```

### 2. Ouvrir des ports courants
Si vous hébergez un serveur web, vous devez ouvrir les ports HTTP et HTTPS.

```bash
# Autoriser le port HTTP (80)
sudo ufw allow 80/tcp

# Autoriser le port HTTPS (443)
sudo ufw allow 443/tcp

# UFW gère aussi des noms d'applications s'ils sont enregistrés
sudo ufw allow "Nginx Full"
```

### 3. Règles plus restrictives (Filtrage par IP)
Plutôt que d'ouvrir la base de données (MySQL) à tout Internet (ce qui serait suicidaire), vous pouvez l'autoriser uniquement pour l'IP d'un autre de vos serveurs.

```bash
# Autoriser uniquement l'IP 198.51.100.45 à se connecter au port 3306
sudo ufw allow from 198.51.100.45 to any port 3306
```

---

## Vérifier l'État du Pare-Feu

La commande suivante est essentielle pour comprendre ce qui est actuellement appliqué sur votre serveur.

```bash
sudo ufw status verbose
```

**Sortie attendue :**
```text
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere                  
80/tcp                     ALLOW IN    Anywhere                  
443/tcp                    ALLOW IN    Anywhere                  
3306/tcp                   ALLOW IN    198.51.100.45             
```

*Notez la ligne "Default" : Elle indique bien `deny (incoming)` (bloque tout ce qui entre).*

### Supprimer une règle
Si vous vous êtes trompé, la manière la plus simple est de lister les règles avec leur numéro, puis de supprimer par numéro.

```bash
# Afficher les numéros
sudo ufw status numbered

# Supprimer la règle numéro 2
sudo ufw delete 2
```

## Conclusion
UFW cache l'immense complexité de `iptables` derrière une interface intuitive. Activer UFW (en n'oubliant pas SSH) devrait être la **toute première action** que vous effectuez lors de l'acquisition d'un nouveau serveur Linux.