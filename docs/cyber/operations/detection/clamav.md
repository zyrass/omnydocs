---
description: "ClamAV — Antivirus open-source : installation, mise à jour des signatures, scan de fichiers et intégration avec Wazuh Active Response."
icon: lucide/book-open-check
tags: ["CLAMAV", "ANTIVIRUS", "SOC", "WAZUH", "ACTIVE RESPONSE", "MALWARE"]
---

# ClamAV — Antivirus Open-Source

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🟡 Intermédiaire"
  data-version="ClamAV 1.x"
  data-time="~1-2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Chien Renifleur des Douanes"
    Aux douanes, le chien renifleur ne vérifie pas lui-même chaque bagage — les douaniers lui amènent les valises suspectes et il détermine s'il y a quelque chose à signaler. **ClamAV** joue ce rôle dans votre SOC : couplé à Wazuh, chaque fois qu'un fichier suspect est détecté par le FIM (File Integrity Monitoring), ClamAV est automatiquement déclenché pour scanner ce fichier et identifier s'il s'agit d'un malware connu.

**ClamAV** est l'antivirus open-source de référence, maintenu par Cisco. Ses points forts en contexte SOC :

- **Gratuit et open-source** : déployable sur tous vos serveurs sans licence
- **Intégration native avec Wazuh** : déclenchement automatique via Active Response
- **Base de signatures fréquemment mise à jour** : ClamAV + YARA + signatures communautaires
- **Multiplateforme** : Linux, Windows, macOS

<br>

---

## Installation

```bash title="Installation ClamAV — Ubuntu 22.04"
# Installer ClamAV et le démon freshclam (mise à jour auto des signatures)
apt-get update && apt-get install -y clamav clamav-daemon

# Arrêter le démon avant la première mise à jour des signatures
systemctl stop clamav-freshclam

# Mettre à jour les signatures manuellement (première fois)
freshclam

# Démarrer le démon freshclam (mises à jour automatiques toutes les heures)
systemctl enable --now clamav-freshclam
systemctl enable --now clamav-daemon

# Vérifier l'état
systemctl status clamav-daemon
clamd --version
```

<br>

---

## Utilisation en ligne de commande

```bash title="Commandes ClamAV — Scan de fichiers et répertoires"
# Scan d'un fichier unique
clamscan /chemin/vers/fichier_suspect.exe

# Scan d'un répertoire entier (récursif)
clamscan -r /var/uploads/

# Scan avec rapport détaillé (fichiers infectés uniquement)
clamscan -r --infected --no-summary /home/

# Scan et déplacement automatique en quarantaine
clamscan -r --move=/var/quarantine/ /var/uploads/

# Scan d'une archive ZIP
clamscan --max-scansize=100M fichier.zip

# Utiliser le démon clamd (beaucoup plus rapide — pas de chargement de signatures à chaque fois)
clamdscan /var/uploads/
```

<br>

---

## Intégration avec Wazuh — Active Response automatique

La vraie valeur de ClamAV en SOC vient de son intégration avec Wazuh : chaque fichier créé (détecté par le FIM) déclenche automatiquement un scan ClamAV.

```xml title="ossec.conf — Commande ClamAV pour Active Response"
<ossec_config>

  <!-- Définir la commande ClamAV -->
  <command>
    <name>clamav-scan</name>
    <!-- Script qui lance ClamAV sur le fichier détecté -->
    <executable>clamav-scan.sh</executable>
    <expect>filename</expect>
    <timeout_allowed>yes</timeout_allowed>
  </command>

  <!-- Déclencher sur les alertes FIM (création de fichier) -->
  <active-response>
    <command>clamav-scan</command>
    <!-- Rule 554 = "File added to the system" (FIM) -->
    <rules_id>554</rules_id>
    <timeout>120</timeout>
  </active-response>

</ossec_config>
```

```bash title="/var/ossec/active-response/bin/clamav-scan.sh — Script de scan automatique"
#!/bin/bash
# Script de scan ClamAV déclenché par Wazuh Active Response
# Reçoit les données de l'alerte via stdin (JSON)

# Lire le chemin du fichier depuis l'alerte Wazuh
read INPUT_JSON
FILE_PATH=$(echo $INPUT_JSON | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('parameters', {}).get('alert', {}).get('syscheck', {}).get('path', ''))
")

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Lancer ClamAV sur le fichier détecté
RESULT=$(clamscan --no-summary "$FILE_PATH" 2>&1)
STATUS=$?

if [ $STATUS -ne 0 ]; then
    # Malware détecté ! Logger et envoyer vers Wazuh
    logger -t "clamav-wazuh" "MALWARE DETECTED: $FILE_PATH — $RESULT"

    # Mettre en quarantaine le fichier
    QUARANTINE_DIR="/var/quarantine/$(date +%Y%m%d)"
    mkdir -p "$QUARANTINE_DIR"
    mv "$FILE_PATH" "$QUARANTINE_DIR/"

    logger -t "clamav-wazuh" "File quarantined: $QUARANTINE_DIR/$(basename $FILE_PATH)"
fi

exit 0
```

_Ce script :_
1. _Reçoit le chemin du fichier créé depuis l'alerte Wazuh FIM_
2. _Lance ClamAV sur ce fichier spécifique_
3. _Si malware détecté : log l'événement (Wazuh le récupère) et met en quarantaine_

<br>

---

## Enrichir ClamAV avec des signatures YARA

ClamAV peut charger des **règles YARA** pour enrichir sa détection au-delà de sa base de signatures officielle :

```bash title="Intégrer des règles YARA dans ClamAV"
# Créer le répertoire de signatures supplémentaires
mkdir -p /var/lib/clamav/custom/

# Copier vos règles YARA (compatibles ClamAV)
cp /etc/yara/rules/*.yar /var/lib/clamav/custom/

# Configurer ClamAV pour charger ces signatures
cat >> /etc/clamav/clamd.conf << 'EOF'
# Charger les règles YARA supplémentaires
DatabaseDirectory /var/lib/clamav
ExtraDatabase /var/lib/clamav/custom/
EOF

# Redémarrer le démon
systemctl restart clamav-daemon

# Vérifier que les signatures YARA sont chargées
clamd --debug 2>&1 | grep -i "yara\|loaded"
```

<br>

---

## Maintenir les signatures à jour

```bash title="Configuration freshclam — Mises à jour automatiques"
# Fichier de configuration : /etc/clamav/freshclam.conf
cat /etc/clamav/freshclam.conf | grep -E "^(DatabaseMirror|Checks|UpdateLogFile)"

# DatabaseMirror database.clamav.net  → Serveur de mise à jour officiel
# Checks 24                           → Vérification 24 fois/jour (toutes les heures)
# UpdateLogFile /var/log/clamav/freshclam.log

# Forcer une mise à jour manuelle
freshclam --verbose

# Voir les dernières signatures chargées
sigtool --info /var/lib/clamav/main.cvd
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    ClamAV seul n'est pas un antivirus "enterprise". Intégré dans votre SOC Wazuh, il devient un **outil de réponse automatique** qui scanne chaque fichier suspect sans intervention humaine. Pour un SOC open-source, la combinaison Wazuh FIM + ClamAV + YARA offre une couverture antivirus solide sans aucun coût de licence. La quarantaine automatique permet de neutraliser immédiatement une menace pendant que l'analyste l'analyse.

> **La Phase 2 (Détection & Analyse) est terminée.** Passez à la **[Phase 3 — Incident Response & DFIR →](../ir/index.md)** pour apprendre à gérer un incident une fois qu'il est détecté.

<br>