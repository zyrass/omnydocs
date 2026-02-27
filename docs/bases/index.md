---
description: "Socle transversal de connaissances fondamentales, indépendant de toute technologie ou domaine de spécialisation."
icon: lucide/layers
tags: ["FONDAMENTAUX", "BASES", "SOCLE"]
---

# Fondamentaux IT

<div
  class="omny-meta"
  data-level="Débutant"
  data-version="2.0"
  data-time="10-15 minutes">
</div>

!!! quote "Analogie"
    _Construire une expertise technique sans maîtriser les fondamentaux, c'est élever une structure sur des fondations instables. On peut progresser vite au début — mais les lacunes se révèlent au pire moment._

## Objectif

Cette section constitue le **socle transversal** d'OmnyDocs. Elle rassemble les connaissances durables, indépendantes d'un langage, d'un framework ou d'un environnement particulier. Elles sont nécessaires avant d'aborder le développement, l'administration système ou la cybersécurité.

Le contenu est organisé en **huit domaines complémentaires**, progressifs mais consultables indépendamment selon les besoins.

<br />

---

## Vue d'ensemble

```mermaid
flowchart LR
  FI[Fondamentaux IT]

  FT[1. Fondamentaux techniques]
  FS[2. Formats & Sérialisation]
  OD[3. Outils de développement]
  MC[4. Modélisation & Conception]
  GP[5. Gestion de projet]
  CP[6. Concepts de programmation]
  RP[7. Réseaux et Protocoles]
  CK[8. Cryptographie & PKI]

  FI --> FT
  FI --> FS
  FI --> OD
  FI --> MC
  FI --> GP
  FI --> CP
  FI --> RP
  FI --> CK
```

<p><em>Chaque domaine est autonome mais s'appuie sur les précédents.<br />La progression recommandée suit l'ordre de numérotation.</em></p>

<br />

---

## Rôle dans la progression générale

```mermaid
flowchart TB
  FI[Fondamentaux IT]

  DEV[Développement]
  SYS[Systèmes & Infra]
  GRC[Cyber Gouvernance]
  DEF[Cyber Défense]
  ATT[Cyber Attaque]

  FI -->|Logique, formats, outils, Git| DEV
  FI -->|Réseaux, Linux, protocoles| SYS
  FI -->|Cryptographie, modèles, risques| GRC
  SYS -->|Logs, services, hôte| DEF
  DEV -->|Code, vulnérabilités| ATT
```

<p><em>Les Fondamentaux IT alimentent directement les trois branches de spécialisation.<br /><strong>Une lacune à ce niveau se répercute sur l'ensemble de la progression</strong>.</em></p>

<br />

---

## Domaines de la section

<div class="grid cards" markdown>

- ### :lucide-cpu: 1 — Fondamentaux techniques
    ---
    Primitives universelles de la programmation : types, mémoire, logique booléenne, structures de contrôle, fonctions. Commun à la quasi-totalité des langages modernes.

    [Consulter](./fondamentaux/index.md)

- ### :lucide-file-code: 2 — Formats & Sérialisation
    ---
    Formats d'échange et de configuration : JSON, YAML, XML, CSV. Savoir lire, produire et valider des données structurées dans tout contexte technique.

    [Consulter](./formats-serialisation/index.md)

</div>

<div class="grid cards" markdown>

- ### :lucide-terminal: 3 — Outils de développement
    ---
    Environnements virtuels (WSL, NVM, VENV), gestionnaires de paquets Linux, documentation et versionning (Markdown, Git). Outillage transverse pour produire et maintenir du logiciel.

    [Consulter](./outils/index.md)

- ### :lucide-shapes: 4 — Modélisation & Conception
    ---
    Méthodes et notations pour raisonner avant d'implémenter : UML (use case, classes, séquences, états, déploiement) et Merise (MCD, MLD, MPD, SQL).

    [Consulter](./modelisation/index.md)

</div>

<div class="grid cards" markdown>

- ### :lucide-calendar-check: 5 — Gestion de projet
    ---
    Structuration du travail et pilotage : planification, jalons, dépendances. Outillage Gantt pour visualiser et communiquer une trajectoire de projet.

    [Consulter](./projet/index.md)

- ### :lucide-code: 6 — Concepts de programmation
    ---
    Principes structurants et durables : architecture Unix, codes d'erreur standardisés. Socle intellectuel transverse applicable dans tous les environnements.

    [Consulter](./concepts/architecture-unix.md)

</div>

<div class="grid cards" markdown>

- ### :lucide-network: 7 — Réseaux et Protocoles
    ---
    Modèles conceptuels (OSI, TCP/IP), grandes familles de protocoles, HTTP, DNS, sockets. Les mécanismes client-serveur avant leur mise en oeuvre opérationnelle.

    [Consulter](./reseaux/modele-osi.md)

- ### :lucide-lock: 8 — Cryptographie & PKI
    ---
    Bases cryptographiques nécessaires avant d'aborder la sécurité applicative et réseau : GPG, OpenSSL, PKI, chaînes de certificats, TLS.

    [Consulter](./crypto/index.md)

</div>

<br />

---

## Progression recommandée

```mermaid
sequenceDiagram
  participant A as Apprenant
  participant FT as 1. Fondamentaux tech.
  participant FS as 2. Formats
  participant OD as 3. Outils
  participant MC as 4. Modélisation
  participant RP as 7. Réseaux
  participant CK as 8. Cryptographie

  A->>FT: Logique, types, mémoire
  note over FT: Prérequis universel
  FT->>FS: Représentation des données
  note over FS: JSON, YAML, XML, CSV
  FS->>OD: Environnement de travail
  note over OD: WSL, Git, paquets Linux
  OD->>MC: Conception avant implémentation
  note over MC: UML, Merise
  MC->>RP: Communication entre systèmes
  note over RP: OSI, TCP/IP, HTTP, DNS
  RP->>CK: Sécurisation des échanges
  note over CK: GPG, OpenSSL, PKI
  CK-->>A: Socle complet
```

<p><em>Cette progression n'impose aucune contrainte rigide.<br /><strong>Chaque domaine reste accessible indépendamment selon les besoins ou le projet en cours</strong>.<br />L'ordre proposé réduit simplement la friction lors de la première découverte.</em></p>

<br />

---

## Périmètre et délimitations

Il est important de comprendre ce que cette section **ne couvre pas**, pour éviter toute confusion avec les sections suivantes.

| Thème | Fondamentaux IT | Section dédiée |
|---|---|---|
| Administration Linux avancée | Outils CLI de base | Systèmes & Infra |
| Services réseau opérationnels | Concepts OSI/TCP | Systèmes & Infra |
| Sécurité applicative | Bases crypto | Cyber : Défense / Attaque |
| Frameworks web | Aucun | Développement |
| Docker, CI/CD | Git uniquement | Développement |
| Pentest, audit | Aucun | Cyber : Attaque |

<br />

---

## Conclusion

!!! note "Notre recommandation"
    Toute lacune dans les Fondamentaux IT se répercute directement sur les sections suivantes — souvent de manière non évidente. Un profil qui ne comprend pas le modèle OSI diagnostique mal un incident réseau. Un profil qui ne maîtrise pas Git introduit des risques dans tout environnement collaboratif.

    Investir ces bases est le seul raccourci réel vers l'expertise.

**Point d'entrée recommandé : [Fondamentaux techniques](./fondamentaux/index.md)**

<br />