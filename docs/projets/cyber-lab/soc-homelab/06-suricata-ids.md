---
description: "Module 6 - Installation et configuration de Suricata (IDS) pour analyser le trafic réseau et générer des alertes spécifiques."
---

# Module 6 - Suricata IDS et règles locales

<div
  class="omny-meta"
  data-level="🟠 Intermédiaire"
  data-version="Suricata 7 LTS"
  data-time="~45 min">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le douanier"
    Wazuh regarde ce qui se passe *à l'intérieur* de la maison (qui a ouvert une porte, qui a allumé la lumière). Suricata regarde *ce qui passe par la fenêtre* (le réseau). C'est un douanier qui ouvre chaque paquet de données, lit son contenu, et crie (crée un log) si le paquet contient de la contrebande selon une liste de règles prédéfinies. Wazuh écoutera ensuite les cris du douanier.

## 6.1 - Objectifs pédagogiques

À la fin de ce module, l'apprenant doit être capable de :

- Distinguer un IDS (Intrusion Detection System) d'un IPS (Intrusion Prevention System).
- Installer Suricata sur Ubuntu et identifier son fichier de configuration principal.
- Rédiger une règle Suricata personnalisée simple (détection ICMP).
- Configurer l'Agent Wazuh pour lire le fichier `eve.json` généré par Suricata.

<br>

---

## 6.2 - L'approche IDS (Détection) vs IPS (Prévention)

**Suricata** peut fonctionner selon deux modes :
- **IDS (Mode passif)** : Il copie le trafic, l'analyse et génère des logs. Il ne ralentit pas le trafic et ne peut rien bloquer. S'il plante, le trafic réseau continue.
- **IPS (Mode actif)** : Le trafic *traverse* Suricata. S'il détecte une anomalie, il drop (détruit) le paquet. S'il plante, le réseau est coupé.

Dans un SOC jeune, on commence **toujours** par de l'IDS. Mettre un IPS trop tôt génère des faux positifs qui bloquent les processus métiers légitimes (le fameux "La compta n'arrive plus à envoyer les factures").

<br>

---

## 6.3 - Installation de Suricata (Sur la VM Cible)

Connectez-vous à la machine `ubuntu-target` (VM 2).

```bash title="Connexion SSH à la cible et installation de Suricata"
# Sur l'hôte
vagrant ssh ubuntu-target

# Dans la VM cible : ajout du dépôt PPA officiel pour avoir la version 7 (LTS)
sudo add-apt-repository ppa:oisf/suricata-stable -y
sudo apt-get update

# Installation
sudo apt-get install suricata -y
```

Par défaut, Suricata écoute sur l'interface réseau principale (souvent `eth0`). Dans notre configuration Vagrant, le réseau privé qui nous intéresse est sur `eth1` (l'IP `192.168.56.20`). 

```bash title="Configuration de l'interface réseau d'écoute"
# Édition du fichier principal
sudo nano /etc/suricata/suricata.yaml

# Trouvez la section "af-packet:"
# Modifiez "interface: eth0" en "interface: eth1"
```

<br>

---

## 6.4 - Création d'une règle personnalisée (Le Scénario)

Notre scénario d'attaque sera un Flood ICMP (Ping massif) depuis la VM Attaquant. Nous allons créer une règle très basique : "Alerter dès qu'on reçoit un ping".

```bash title="Création de la règle personnalisée r03-icmp.rules"
# Créer le fichier de règles
sudo nano /etc/suricata/rules/r03-icmp.rules

# Ajouter cette ligne EXACTEMENT :
alert icmp any any -> any any (msg:"ALERTE SOC - Scan ICMP Detecte"; sid:1000001; rev:1;)
```

**Explication de la syntaxe :**
- `alert` : L'action (générer un log).
- `icmp` : Le protocole ciblé.
- `any any -> any any` : De "N'importe quelle IP, N'importe quel port" vers "N'importe quelle IP, N'importe quel port".
- `msg` : Le texte qui apparaîtra dans le SIEM.
- `sid:1000001` : Signature ID. Obligatoire. De 1 000 000 à 1 999 999, ce sont les règles "locales" personnalisées.

Il faut maintenant dire à Suricata de lire ce fichier.

```bash title="Inclusion du fichier dans suricata.yaml"
sudo nano /etc/suricata/suricata.yaml

# Descendez vers la ligne 1900, section "rule-files:"
# Ajoutez - r03-icmp.rules à la liste :
rule-files:
  - suricata.rules
  - r03-icmp.rules    # Notre nouvelle ligne

# Redémarrez Suricata pour appliquer
sudo systemctl restart suricata
```

<br>

---

## 6.5 - Connexion de Wazuh à Suricata

Suricata génère désormais ses alertes dans le fichier `/var/log/suricata/eve.json`. Mais le SIEM (Wazuh Manager) n'en sait rien. Il faut dire à l'**Agent Wazuh** (sur la cible) de lire ce fichier et de l'envoyer au Manager.

```bash title="Configuration de l'agent Wazuh (Sur la cible)"
sudo nano /var/ossec/etc/ossec.conf

# Ajoutez ce bloc XML juste avant la balise de fin </ossec_config>
  <localfile>
    <log_format>json</log_format>
    <location>/var/log/suricata/eve.json</location>
  </localfile>

# Redémarrez l'agent
sudo systemctl restart wazuh-agent
```

<br>

---

## 6.6 - Points de vigilance

- L'indentation du fichier `suricata.yaml` est extrêmement stricte (YAML). N'utilisez **jamais** de tabulation (TAB), uniquement des espaces. Une erreur d'indentation empêchera le service de redémarrer.
- Oublier le `sid` (Signature ID) dans une règle la rend invalide.
- Si vous copiez-collez le bloc XML dans `ossec.conf` et que l'agent ne redémarre pas (`sudo systemctl status wazuh-agent` en erreur), c'est souvent un problème de balises mal fermées.

<br>

---

## 6.7 - Axes d'amélioration vs projet original

| Constat dans le projet 2025 | Amélioration recommandée |
|---|---|
| Utilisation de Suricata 6.0 | Passage sur le dépôt `ppa:oisf/suricata-stable` pour garantir la version 7.x (LTS) sur Ubuntu 24.04. |
| Le lien entre Suricata et Wazuh est traité comme un bloc abstrait ("ça marche"). | Expliciter le rôle du format `eve.json`. Wazuh le comprend nativement (il a un décodeur intégré pour ça), ce qui est la seule raison pour laquelle ce bloc XML très simple fonctionne sans configuration supplémentaire sur le serveur. |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Suricata ne protège pas, il observe et alerte. La création de règles locales permet de repérer des comportements spécifiques au métier de l'entreprise (ex: "Alerte si le serveur Web initie une connexion SSH vers l'extérieur", ce qui est un comportement hautement suspect).

> Nous avons la détection système (Wazuh) et la détection réseau (Suricata). L'étape suivante est de faire remonter ces alertes hors de l'interface web, directement sur le téléphone de l'analyste, dans le **[Module 7 : Notification externe via Discord →](./07-notifications-discord.md)**
