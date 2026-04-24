---
description: "Preuves d'exploitation — Comment collecter, documenter et présenter vos preuves d'intrusion de manière irréfutable et professionnelle."
icon: lucide/book-open-check
tags: ["REPORTING", "PENTEST", "PREUVES", "POC", "AUDIT"]
---

# Collecte des Preuves d'Exploitation

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="~30 minutes">
</div>

<img src="../../../assets/images/cyber/preuves.svg" width="100" align="center" style="display: block; margin: 0 auto;">

## Introduction

!!! quote "Analogie pédagogique — La Scène de Crime"
    Imaginez un détective sur une scène de crime. S'il dit au juge "Je suis sûr que c'est lui, je l'ai vu", il risque d'être ignoré. S'il apporte une photo des empreintes,**La Collecte de Preuves** (Evidence Collection) est l'étape la plus critique d'un audit de sécurité. Sans preuves tangibles (captures d'écran, logs, sorties de commandes), une vulnérabilité n'est qu'une hypothèse. La qualité et l'intégrité de ces preuves déterminent la crédibilité de l'auditeur et la capacité du client à comprendre et reproduire le problème.

<br>

---

## Les Principes d'une Bonne Preuve

Pour être considérée comme valide et professionnelle, une preuve doit respecter plusieurs critères :
- **Clarté** : L'information critique doit être immédiatement visible (entourage, fléchage).
- **Contexte** : Inclure des éléments permettant d'identifier la cible (adresse IP, nom d'hôte, URL).
- **Traçabilité** : Indiquer la date et l'heure de la capture (timestamp).
- **Intégrité** : Ne jamais altérer la donnée originale. Si une modification est nécessaire (anonymisation), elle doit être précisée.

<br>

---

## Techniques de Collecte

### 1. Captures d'écran (Screenshots)
1.  **État initial** : Montrer la page ou le service normal.
2.  **L'injection** : Montrer la payload envoyée (ex: `' OR 1=1 --`).
3.  **Le résultat** : Montrer l'accès obtenu (ex: dashboard administrateur).
4.  **La preuve d'impact** : Exécuter une commande neutre (`whoami`, `ipconfig`, `id`).

---

## Erreurs à Éviter (OpSec & Pro)

!!! danger "Les données client"
    Ne laissez **JAMAIS** des données sensibles en clair dans votre rapport (numéros de CB, mots de passe, documents confidentiels). Masquez-les systématiquement.

!!! warning "Le 'Vandalisme'"
    N'utilisez pas de messages provocateurs pour vos PoC (ex: `HACKED BY ME`). Utilisez des fichiers neutres comme `audit_omnyvia.txt` contenant la date et l'heure de l'audit.

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Une preuve est réussie si un technicien du client peut reproduire la faille en suivant vos étapes sans vous appeler. La qualité de vos preuves définit votre professionnalisme : soyez clair, précis, et surtout, respectueux de la confidentialité des données que vous manipulez.

> Une fois vos preuves collectées, vous devez proposer une solution pour corriger la faille dans votre **[Plan de Remédiation →](./remediation.md)**.





