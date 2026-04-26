---
description: "Chainsaw — L'outil ultra-rapide (écrit en Rust) pour rechercher des indicateurs de compromission (IoC) et chasser les menaces dans les journaux d'événements Windows (EVTX) à l'aide des règles Sigma."
icon: lucide/file-search
tags: ["FORENSIC", "LOGS", "CHAINSAW", "EVTX", "SIGMA", "DFIR"]
---

# Chainsaw — La Chasse aux Logs Ultra-Rapide

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2.8+"
  data-time="~30 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/chainsaw.png" width="250" align="center" alt="Chainsaw Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Chien de Chasse"
    Imaginez un entrepôt contenant 10 millions de factures papier (les logs Windows). Chercher à la main la facture du cambrioleur prendrait des années. **Chainsaw** est comme une meute de chiens de chasse robotiques hyper rapides. Vous leur donnez l'odeur du cambrioleur (les règles **Sigma**), vous ouvrez les portes de l'entrepôt, et en quelques secondes, ils vous ramènent exactement la facture recherchée, sans même avoir besoin de lire le reste.

Développé par le groupe de recherche Countercept (F-Secure/WithSecure), **Chainsaw** est un outil en ligne de commande open-source écrit en Rust. Il a été conçu pour un seul but : ingérer et analyser des fichiers journaux Windows Event Logs (`.evtx`) le plus rapidement possible.

Traditionnellement, l'analyse d'EVTX nécessitait de les convertir en XML, de les importer dans un SIEM (Splunk, ELK) ou d'utiliser le très lent Event Viewer de Windows. Chainsaw permet aux consultants en Réponse à Incident (IR) de chasser les malwares sur le terrain sans infrastructure lourde, directement sur la machine compromise.

<br>

---

## 🛠️ Concepts Fondamentaux : Sigma Rules

L'outil tire sa puissance de son intégration native avec **Sigma**. 

**Sigma** est un format générique (YAML) utilisé pour décrire des signatures d'attaques. C'est l'équivalent de YARA ou Snort, mais pour les logs système.

Exemple de règle Sigma : *Alerter si un fichier `cmd.exe` est exécuté en tant qu'enfant du processus `winword.exe` (Word ne devrait jamais lancer de terminal, c'est le comportement typique d'une macro malveillante).*

<br>

---

## 🛠️ Usage Opérationnel

Chainsaw propose principalement deux modes d'utilisation : la Recherche (Search) par mot-clé, et la Chasse (Hunt) via les règles Sigma.

### 1. Mode Hunt (Chasse avec Règles Sigma)

C'est l'utilisation principale. Vous fournissez un dossier contenant des logs `.evtx` (récupérés via Velociraptor ou KAPE) et le dossier officiel des règles Sigma.

```bash title="Chasse automatisée sur un dump de logs"
# hunt : Mode d'analyse par règles
# /logs_triage/ : Dossier contenant les .evtx extraits du PC compromis
# -s sigma/rules : Indique où se trouvent les règles Sigma
# --mapping : Indique à Chainsaw comment comprendre le format Sigma
chainsaw hunt /logs_triage/ \
    -s sigma/rules \
    --mapping mapping_files/sigma-event-logs-all.yml
```
*Le résultat s'affichera sous forme de tableau clair directement dans le terminal, listant chaque alerte critique trouvée (ex: "Pass-the-Hash Detecté", "Vidage du cache LSASS").*

### 2. Mode Search (Recherche Rapide)

Utile quand vous avez un Indicateur de Compromission (IoC) précis, comme une adresse IP suspecte ou le nom d'un attaquant.

```bash title="Recherche textuelle ou Regex"
# -s : La chaîne à chercher (ex: l'IP du serveur Command & Control)
# -i : Case-insensitive
chainsaw search /logs_triage/ -s "192.168.1.50" -i
```
*Chainsaw extraira tous les événements (connexions, lancements de processus) liés à cette IP.*

### 3. Sortie Structurée (JSON / CSV)

Pour une intégration dans un rapport d'incident ou un traitement ultérieur avec Python/jq.

```bash title="Exporter les résultats"
chainsaw hunt /logs_triage/ -s sigma/rules --mapping mapping_files/sigma-event-logs-all.yml --json-out resultats_hunt.json
```

<br>

---

## 💀 Scénario DFIR : L'Analyse Post-Mortem

Une alerte critique sonne. Un serveur Active Directory a été compromis.
1. Le SOC extrait le dossier `C:\Windows\System32\winevt\Logs` complet (plusieurs Gigaoctets) à l'aide d'un script ou de Velociraptor.
2. Le dossier est transféré sur la station d'analyse Linux de l'enquêteur.
3. L'enquêteur lance `chainsaw hunt`.
4. En 3 secondes, Chainsaw retourne 5 alertes critiques :
   - *Clear Security Event Log* (L'attaquant a effacé ses traces).
   - *Psexec Execution* (Mouvement latéral).
   - *Mimikatz LSASS Access* (Vol de mots de passe).
5. L'enquêteur a sa chronologie initiale de l'attaque sans même avoir eu à installer un SIEM.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Chainsaw est l'outil parfait pour le *Triage*. Lors d'une réponse à incident, le temps est compté. Devoir attendre l'indexation de logs volumineux dans un SIEM centralisé est une perte de temps. Chainsaw met la puissance de détection de Splunk dans un petit exécutable en ligne de commande ultra-rapide.

> Son concurrent direct, écrit également en Rust et encore plus focalisé sur le forensic Windows, s'appelle **[Hayabusa](./hayabusa.md)**.