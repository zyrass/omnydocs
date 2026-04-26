---
description: "Module 7 - Création d'une intégration Python pour alerter le SOC en temps réel via un Webhook Discord."
---

# Module 7 - Notification externe (Discord)

<div
  class="omny-meta"
  data-level="🟠 Intermédiaire"
  data-version="Python 3.12, Webhook"
  data-time="~1 h">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le biper d'astreinte"
    Avoir un tableau de bord (Dashboard) magnifique, c'est bien, mais personne ne regarde un écran fixe 24 heures sur 24. Si une alerte critique (Niveau 12+) tombe à 4h du matin, le système doit pouvoir réveiller l'astreinte. L'intégration Webhook (Discord, Slack, Teams) joue le rôle de biper moderne. Elle pousse l'information vers l'humain, plutôt que d'attendre que l'humain vienne chercher l'information.

## 7.1 - Objectifs pédagogiques

À la fin de ce module, l'apprenant doit être capable de :

- Définir le mécanisme d'un Webhook HTTP(S) et son avantage par rapport à un polling (requête régulière).
- Générer un Webhook sur un outil collaboratif grand public (Discord).
- Lire et modifier un script Python d'intégration pour formater le JSON brut de Wazuh en un message lisible.
- Déclarer une nouvelle intégration de bout en bout dans le fichier de configuration `ossec.conf` du serveur Wazuh.

<br>

---

## 7.2 - Qu'est-ce qu'un Webhook ?

Un **Webhook** est une URL unique générée par un service (ici, Discord). Quand un autre service (Wazuh) envoie une requête HTTP POST vers cette URL contenant des données JSON, Discord l'interprète et publie un message dans le canal associé.

- **Sécurité** : L'URL contient un jeton secret (Token). Quiconque possède l'URL complète peut envoyer des messages en votre nom. **Ne la commitez jamais sur GitHub.**
- **Avantage** : C'est du temps réel. Dès que Wazuh lève l'alerte, la requête HTTP part, et le message s'affiche sur le téléphone de l'analyste en moins de 2 secondes.

### Obtenir l'URL (Côté Discord)
1. Créez un serveur Discord privé (gratuit).
2. Créez un salon `#alertes-soc`.
3. Allez dans les paramètres du salon > Intégrations > Créer un Webhook.
4. Copiez l'URL du Webhook (elle ressemble à `https://discord.com/api/webhooks/123456/AbCdEfGh...`).

<br>

---

## 7.3 - Le script d'intégration Python

Wazuh possède des intégrations natives pour Slack et PagerDuty, mais pas pour Discord. Nous devons écrire notre propre traducteur (Integration Script).

Connectez-vous à la **VM SIEM** (`wazuh-server`) :

```bash title="Création du script Python d'intégration"
# Sur le serveur Wazuh, se déplacer dans le dossier des intégrations
cd /var/ossec/integrations/

# Créer le fichier custom-discord
sudo nano custom-discord
```

Collez le script Python suivant :

```python title="Script custom-discord (Traducteur JSON Wazuh -> JSON Discord)"
#!/usr/bin/env python3
# Script Python 3.12 - Intégration Wazuh vers Discord
import json
import sys
import requests

# Lecture des arguments passés par le binaire ossec-integratord
# sys.argv[1] = Fichier contenant l'alerte JSON brut générée par Wazuh
alert_file = sys.argv[1]
# sys.argv[3] = L'URL du Webhook passée dans la configuration
webhook_url = sys.argv[3]

# Ouverture et parsing du fichier d'alerte JSON
with open(alert_file) as f:
    alert = json.load(f)

# Extraction des données pertinentes pour l'humain
level = alert['rule']['level']
description = alert['rule']['description']
agent_name = alert['agent']['name']
# Certaines alertes ont une adresse IP source (srcip), d'autres non.
srcip = alert.get('data', {}).get('srcip', 'N/A')

# Formatage visuel selon le niveau de gravité
if level >= 12:
    color = 16711680 # Rouge (Critique)
    prefix = "🚨 [CRITIQUE]"
elif level >= 7:
    color = 16753920 # Orange (Avertissement)
    prefix = "⚠️ [WARNING]"
else:
    color = 65280    # Vert (Info)
    prefix = "ℹ️ [INFO]"

# Construction du payload (format Embed) attendu par l'API Discord
payload = {
    "embeds": [
        {
            "title": f"{prefix} Alerte Wazuh (Niveau {level})",
            "description": f"**Règle:** {description}\n**Agent:** {agent_name}\n**IP Source:** {srcip}",
            "color": color
        }
    ]
}

# Envoi de la requête HTTP POST
headers = {'content-type': 'application/json'}
requests.post(webhook_url, json=payload, headers=headers)
```

!!! caution "Droits et permissions (Crucial)"
    Un script, même parfait, ne s'exécutera pas si le moteur Wazuh n'a pas les droits pour le lire. Le groupe propriétaire doit être `ossec` et le fichier doit être exécutable.

```bash title="Attribution des droits d'exécution"
sudo chmod 750 /var/ossec/integrations/custom-discord
sudo chown root:ossec /var/ossec/integrations/custom-discord
```

<br>

---

## 7.4 - Configuration du serveur (`ossec.conf`)

Maintenant que le script existe, disons au Manager de l'appeler chaque fois qu'une alerte de niveau 7 ou plus est déclenchée.

```bash title="Déclaration de l'intégration dans Wazuh"
sudo nano /var/ossec/etc/ossec.conf

# Ajoutez ce bloc XML juste avant </ossec_config>
  <integration>
    <name>custom-discord</name>           # Doit correspondre exactement au nom du script
    <hook_url>VOTRE_URL_WEBHOOK_DISCORD_ICI</hook_url>
    <level>7</level>                      # Seules les alertes >= 7 déclenchent le script
    <alert_format>json</alert_format>
  </integration>

# Redémarrer le Manager
sudo systemctl restart wazuh-manager
```

<br>

---

## 7.5 - Points de vigilance

- **Le niveau d'alerte (Spam)** : Mettre `<level>3</level>` va inonder votre canal Discord de messages sans intérêt (ex: une connexion SSH réussie est de niveau 3). Le niveau minimum recommandé en production pour ne pas épuiser les analystes est **7** (Voire 10 pour le réveil nocturne).
- **Python-Requests** : Le script utilise la bibliothèque `requests`. Bien qu'elle soit standard, sur certaines versions minimales d'Ubuntu, il peut être nécessaire de l'installer via `sudo apt install python3-requests`.
- **Indentation Python** : Comme YAML, Python est sensible à l'indentation. Une espace de trop dans le bloc `if` et le script plantera silencieusement en arrière-plan.

<br>

---

## 7.6 - Axes d'amélioration vs projet original

| Constat dans le projet 2025 | Amélioration recommandée |
|---|---|
| Le webhook URL était hardcodé en clair dans le code Python ou dans le repo GitHub. | L'URL est désormais injectée via la configuration XML locale `ossec.conf` (`<hook_url>`) et passée dynamiquement au script via `sys.argv[3]`. Cela évite les fuites de sécurité et permet de versionner le script Python publiquement. |
| Le script affichait la donnée brute sans formatage conditionnel. | Ajout des codes couleurs (Vert/Orange/Rouge) selon la criticité (`level`), car en gestion de crise, l'information visuelle doit être traitée en une fraction de seconde par l'analyste. |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    L'intégration externe est la porte de sortie de notre SOC. Elle traduit la machine (JSON) en langage humain (Message formaté) et l'achemine là où l'humain se trouve (Discord, téléphone). C'est le lien critique qui permet à l'équipe de réagir à temps.

> Les trois VMs sont en place, le SIEM est configuré, l'IDS est aux aguets et notre biper d'astreinte est branché. Il est temps d'ouvrir le feu. Le module suivant couvre la simulation d'une attaque en direct dans le **[Module 8 : Scénario d'attaque complet →](./08-scenario-attaque.md)**
