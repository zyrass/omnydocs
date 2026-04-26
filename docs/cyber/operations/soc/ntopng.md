---
description: "ntopng — Monitoring réseau temps réel : analyse du trafic, détection d'anomalies de flux, visualisation et alertes sur les comportements réseau suspects."
icon: lucide/book-open-check
tags: ["NTOPNG", "MONITORING", "RÉSEAU", "FLUX", "SOC", "TRAFIC"]
---

# ntopng — Monitoring Réseau Temps Réel

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🟡 Intermédiaire"
  data-version="ntopng 6.x"
  data-time="~1-2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Tableau de Bord du Poste de Pilotage"
    Un pilote de ligne ne regarde pas chaque instrument séparément — il dispose d'un **tableau de bord unifié** qui synthétise toutes les informations critiques (vitesse, altitude, cap, carburant) et alerte immédiatement sur les anomalies. **ntopng** est ce tableau de bord pour votre réseau : il visualise en temps réel qui communique avec qui, combien de bande passante est consommée, et lève des alertes sur les comportements suspects.

**ntopng** est un outil de **monitoring réseau temps réel** open-source (community edition gratuite). Il analyse les flux réseau et fournit une interface web riche pour visualiser l'activité réseau de votre infrastructure.

**Cas d'usage en SOC :**
- Identifier rapidement une **machine qui consomme anormalement** de la bande passante
- Détecter des **communications vers des pays inhabituels**
- Visualiser les **top talkers** (machines les plus actives)
- Alerter sur des **protocoles non autorisés** (BitTorrent, Tor...)

<br>

---

## Installation

```bash title="Installation ntopng — Ubuntu 22.04"
# Ajouter le dépôt ntop
wget https://packages.ntop.org/apt-stable/22.04/all/apt-ntop-stable.deb
dpkg -i apt-ntop-stable.deb
apt-get update

# Installer ntopng
apt-get install -y pfring-dkms nprobe ntopng

# Configurer l'interface réseau à monitorer
cat > /etc/ntopng/ntopng.conf << 'EOF'
# Interface à surveiller
-i=eth0

# Port d'écoute de l'interface web
-w=3000

# Communauté Redis (stockage des données)
-r=@127.0.0.1

# Activer la géolocalisation des IPs
--community
EOF

# Démarrer ntopng
systemctl enable --now ntopng

# Interface web accessible sur http://localhost:3000 (admin/admin par défaut)
```

<br>

---

## Fonctionnalités clés

### Dashboard temps réel

L'interface web ntopng propose une vue instantanée du trafic réseau :

- **Top Hosts** : les machines les plus actives en émission/réception
- **Top Applications** : protocoles les plus utilisés (HTTP, DNS, TLS, streaming...)
- **Geo Map** : carte mondiale des destinations des connexions
- **Alerts** : comportements anormaux détectés automatiquement

### Détection d'anomalies comportementales

ntopng utilise des **algorithmes d'analyse comportementale** pour détecter :

| Anomalie | Mécanisme de détection |
|---|---|
| **Scan de ports** | Nombre de destinations contactées > seuil en N secondes |
| **Exfiltration** | Volume de données envoyées vers l'extérieur > baseline |
| **DNS anormal** | Requêtes DNS en rafale ou vers des serveurs non-autorisés |
| **Application non-autorisée** | DPI (Deep Packet Inspection) identifie BitTorrent, Tor, etc. |

### Intégration avec Wazuh

```bash title="Envoyer les alertes ntopng vers Wazuh via Syslog"
# Dans l'interface ntopng : Settings > Notifications > Syslog
# Configurer :
# Host : IP du Wazuh Server
# Port : 514 (UDP)
# Format : CEF ou JSON

# Côté Wazuh Agent — recevoir les alertes syslog de ntopng
cat >> /var/ossec/etc/ossec.conf << 'EOF'
<ossec_config>
  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/ntopng/alerts.log</location>
  </localfile>
</ossec_config>
EOF
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    ntopng est le **premier réflexe** de l'analyste SOC qui veut comprendre rapidement ce qui se passe sur son réseau. En quelques clics, vous identifiez les anomalies de trafic majeures : une machine qui exfiltre des données, un serveur infecté qui balaye le réseau interne, ou une application non-autorisée qui consomme la bande passante. C'est un outil de **triage rapide** indispensable.

> Terminez la Phase 1 avec le cours sur la **[Threat Intelligence Platform →](../tip.md)** pour comprendre comment enrichir vos alertes avec l'intelligence mondiale sur les menaces.
