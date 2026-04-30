---
title: 3.16 Documentation laboratoire
description: Méthodologie et template de documentation complète du laboratoire forensic. Wiki labo, inventaire matériel, schémas, journal des changements, procédures opérationnelles.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Documentation
  - Wiki
  - Inventaire
  - Procédures
data-level: 🟡
---

# 3.16 Documentation laboratoire

!!! quote "L'analogie du carnet de bord du capitaine"

    Un capitaine de navire tient un carnet de bord. Position, vitesse, vent, manœuvres, incidents. Sans ce carnet, le voyage devient une succession d'actions oubliées dont les conséquences restent inexpliquées. Votre laboratoire forensic obéit à la même règle. Sans documentation, vous oublierez vos propres choix de configuration en deux mois. Avec, vous reprenez le contrôle en cinq minutes.

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 2 heures |
| Niveau | Documentation |

## 1. Pourquoi documenter

| Avantage | Précision |
|---|---|
| Reproductibilité | Reconstruire le labo sans repartir à zéro |
| Continuité | Ne pas tout oublier après pause |
| Apprentissage | Renforcement par l'écriture |
| Pro | Habitude indispensable en cybersécurité |
| Forensic | Preuve de méthodologie professionnelle |

## 2. Structure recommandée

```text
documentation-labo/
├── README.md                    Vue d'ensemble
├── 01-architecture/
│   ├── topologie.md             Schéma réseau
│   ├── adressage.md             Plan IP
│   └── inventaire-materiel.md   Liste équipements
├── 02-configurations/
│   ├── openwrt.md               Config routeur
│   ├── debian-server.md         Config serveur
│   ├── windows-postes.md        Config postes Win
│   ├── kali.md                  Config Kali
│   ├── caine.md                 Config CAINE
│   └── macbook-m1.md            Config Mac
├── 03-procedures/
│   ├── acquisition-disque.md
│   ├── acquisition-memoire.md
│   ├── analyse-rapide.md
│   └── chaine-garde.md
├── 04-credentials/
│   └── (chiffré, hors git)
├── 05-incidents/
│   └── 2026-XX-XX-incident-X/
├── 06-journal/
│   └── changelog.md
└── 07-references/
    ├── liens-utiles.md
    └── outils.md
```

## 3. Templates de fiche

### 3.1 Fiche équipement

```markdown
# Fiche équipement - [NOM]

## Identification
- **Type** : [Routeur / Serveur / Poste / etc.]
- **Modèle** : [Référence exacte]
- **Numéro de série** : [SN]
- **Date d'acquisition** : [YYYY-MM-DD]
- **Source** : [Backmarket / Le Bon Coin / etc.]
- **Garantie jusqu'au** : [YYYY-MM-DD]

## Caractéristiques techniques
- **CPU** : ...
- **RAM** : ...
- **Stockage** : ...
- **Réseau** : ...
- **OS** : ...

## Configuration réseau
- **Hostname** : ...
- **IP** : ...
- **MAC** : ...
- **Domaine** : ...

## Logiciels installés
- ...

## Particularités forensic
- **Vulnérabilités intentionnelles** : ...
- **BitLocker / LUKS** : ...
- **Sysmon / Auditd** : ...

## Procédures associées
- [Lien vers procédure 1]
- [Lien vers procédure 2]

## Journal
- [YYYY-MM-DD] Installation initiale
- [YYYY-MM-DD] Mise à jour vers ...
```

### 3.2 Fiche procédure

```markdown
# Procédure - [NOM]

## Objectif
Description claire de l'objectif

## Préalable
- ...
- ...

## Matériel nécessaire
- ...
- ...

## Étapes

### Étape 1 - [Titre]
\`\`\`bash
commande
\`\`\`
Description et résultat attendu.

### Étape 2 - [Titre]
...

## Vérification
Comment savoir que la procédure a réussi.

## Cas d'erreur
| Erreur | Cause probable | Résolution |
|---|---|---|
| ... | ... | ... |

## Référence
- [Lien doc officielle]
- [Article connexe]
```

### 3.3 Fiche incident forensic

```markdown
# Incident [NUMÉRO] - [DATE]

## Synthèse exécutive
Une à deux phrases.

## Contexte
- **Date détection** : 
- **Système(s) affecté(s)** : 
- **Premier symptôme** : 

## Chronologie
| Date/Heure UTC | Événement | Source |
|---|---|---|
| ... | ... | ... |

## Acquisition
- **Date** : 
- **Examiner** : 
- **Méthodes** : 
- **Hashes** : 

## Analyse
[Sections détaillées]

## Mapping MITRE ATT&CK
| Technique | Évidence |
|---|---|
| T1078 | ... |

## Conclusions

## Recommandations

## Annexes
- Captures écran
- Hashes
- Timelines exportées
```

## 4. Outils de documentation

| Outil | Type | Avantage |
|---|---|---|
| Markdown + Git | Texte | Versionnable, simple |
| Obsidian | Notes liées | Excellent pour wiki labo |
| Joplin | Multi-plateformes | Synchronisation |
| Bookstack | Wiki self-hosted | Multi-utilisateurs |
| MkDocs | Site statique | Publication |
| Notion | Cloud | Collaboratif |

**Recommandation OmnyAcademy** : Markdown + Git local.

## 5. Sécurité de la documentation

### 5.1 Niveaux de confidentialité

| Niveau | Contenu | Stockage |
|---|---|---|
| Public | Procédures génériques | Git public optionnel |
| Interne | Configuration labo | Git privé local |
| Confidentiel | Credentials, IPs réelles | Coffre-fort chiffré (KeePass) |
| Secret | Cas clients | Hors labo, hors PC personnel |

### 5.2 Protection credentials

```text
NE JAMAIS METTRE EN MARKDOWN
==============================
- Mots de passe en clair
- Clés API
- Hashes utilisables
- Tokens
- Credentials clients

UTILISER À LA PLACE
====================
- KeePassXC (recommandé)
- Bitwarden
- 1Password

RÉFÉRENCER DANS DOC :
"Credentials : voir KeePass entry 'Server Debian Lab'"
```

## 6. Maintenance de la documentation

### 6.1 Périodicité

| Événement | Action |
|---|---|
| Modification config | Mise à jour immédiate de la fiche |
| Nouvelle procédure | Création immédiate |
| Mensuel | Revue inventaire |
| Trimestriel | Revue procédures (à jour ?) |
| Annuel | Refonte si nécessaire |

### 6.2 Checklist de qualité

| Critère | Évaluation |
|---|---|
| Chaque équipement a sa fiche ? | OK |
| Chaque procédure est testée ? | OK |
| Schémas à jour ? | OK |
| Credentials hors git ? | OK |
| Backup régulier ? | OK |

---

**Chapitre suivant** : [3.17 Script de validation bout-en-bout](03-17-script-validation.md)
