---
description: "Hayabusa — Un outil de chasse aux menaces et de création de timelines (frises chronologiques) d'événements Windows, développé au Japon, extrêmement rapide et axé sur la clarté visuelle."
icon: lucide/file-search
tags: ["FORENSIC", "LOGS", "HAYABUSA", "EVTX", "SIGMA", "TIMELINE", "DFIR"]
---

# Hayabusa — Le Faucon de la Ligne de Commande

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2.14+"
  data-time="~30 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/hayabusa.png" width="250" align="center" alt="Hayabusa Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Réalisateur de Film"
    Si Chainsaw est le chien de chasse qui vous ramène uniquement la facture du cambrioleur, **Hayabusa** est un réalisateur de film. Vous lui donnez des milliers de caméras de sécurité brutes (les logs EVTX incompréhensibles), et il va monter un film chronologique clair : "À 10h01, porte forcée. À 10h03, coffre ouvert. À 10h05, fuite". Il transforme le charabia technique en une histoire lisible par un être humain.

Créé par le groupe Yamato Security au Japon, **Hayabusa** (le "faucon pèlerin") est l'un des outils de réponse à incident (DFIR) les plus populaires du moment. Tout comme Chainsaw, il est écrit en Rust pour des performances extrêmes et utilise les règles **Sigma** pour détecter les comportements malveillants dans les journaux d'événements Windows (`.evtx`).

Sa particularité majeure réside dans la **génération de Timeline (frise chronologique)** ultra-lisible. L'outil consolide les événements système dans un format texte (ou CSV) propre, où les alertes critiques sont mises en évidence.

<br>

---

## 🛠️ Concepts Fondamentaux : La Timeline DFIR

Lorsqu'un réseau est compromis, la question fondamentale de la direction est toujours : *"Que s'est-il passé, et dans quel ordre ?"*
Pour répondre, l'analyste crée une *Timeline*. 

Plutôt que d'afficher de gros blocs XML indigestes (le format natif EVTX), Hayabusa extrait les champs importants (Heure, Nom de l'ordinateur, Utilisateur, Application lancée) et les condense sur une seule ligne. S'il détecte que cette ligne correspond à une attaque connue (via Sigma), il lui attribue un niveau de criticité (Critique, Élevé, Moyen).

<br>

---

## 🛠️ Usage Opérationnel

### 1. Mise à jour des Règles (L'étape indispensable)
Les techniques des attaquants évoluent chaque jour. Hayabusa intègre un gestionnaire de mise à jour.
```bash title="Mise à jour des règles Sigma"
hayabusa update-rules
```

### 2. Création d'une Timeline CSV (Triage)
C'est la commande la plus utilisée. Elle prend un dossier contenant les logs bruts d'une machine compromise et génère un fichier CSV trié par date.

```bash title="Génération d'une frise chronologique globale"
# -d : Dossier source contenant les EVTX
# -o : Fichier CSV de sortie
# --profile : Règle le niveau de verbosité (standard est recommandé pour réduire le bruit)
hayabusa csv-timeline -d /mnt/evtx_triage/ -o timeline_machine1.csv --profile standard
```
*Le fichier `timeline_machine1.csv` peut ensuite être ouvert dans Excel ou Timeline Explorer (Eric Zimmerman) pour filtrer les colonnes.*

### 3. Mode Chasse (Alertes Uniquement)
Si vous n'avez pas le temps de lire toute la chronologie et que vous ne voulez voir que ce qui a sonné aux alarmes (Les règles Sigma qui ont "matché").

```bash title="Afficher uniquement les alertes critiques"
hayabusa search -d /mnt/evtx_triage/
```
*Affiche dans le terminal un tableau coloré avec les niveaux : `crit`, `high`, `med`, `low`.*

### 4. Mode "Live" (Sur le terrain)
Contrairement aux autres outils qui requièrent que l'on copie les fichiers EVTX au préalable, Hayabusa peut scanner la machine sur laquelle il est exécuté (très utile lors d'une intervention sur site avec une clé USB).

```bash title="Scan de la machine locale (Nécessite droits Admin)"
hayabusa search -l
```

<br>

---

## 🆚 Chainsaw vs Hayabusa : Lequel choisir ?

Les deux outils ont un but similaire, mais une philosophie différente.

- **Chainsaw** excelle dans l'intégration (outputs JSON parfaits pour les pipelines automatisés ou l'ingestion dans d'autres scripts) et la chasse pure.
- **Hayabusa** est l'outil préféré des analystes humains. Sa sortie CSV est formatée de manière beaucoup plus riche (traduction des codes EventID obscurs en texte clair), ce qui le rend incontournable pour construire rapidement la Timeline qui figurera dans le rapport final d'incident.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    L'analyse des journaux Windows a longtemps été le cauchemar des analystes DFIR en raison de leur lourdeur. Avec l'avènement des outils en Rust comme Hayabusa, il est désormais possible de transformer des Gigaoctets de logs bruts en une histoire claire et séquencée de l'attaque en quelques secondes, sur un simple ordinateur portable.

> Une fois votre Timeline générée, l'investigation continue. Si Hayabusa détecte qu'un malware a été lancé, il faudra peut-être analyser le fichier exécutable d'origine ou la mémoire RAM avec **[Volatility](../memory/volatility.md)** pour comprendre comment il fonctionne.
