---
description: "Recommandations & Correctifs — La phase d'assistance. Comment rédiger des plans de remédiation clairs, réalistes et applicables par les équipes de développement."
icon: lucide/book-open-check
tags: ["REPORTING", "REMEDIATION", "CORRECTIF", "PENTEST"]
---

# Recommandations & Correctifs — Le Plan de Guérison

<div
  class="omny-meta"
  data-level="🟢 Fondamental"
  data-version="Standard Industrie"
  data-time="~15 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/remediation.svg" width="250" align="center" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Diagnostic sans Ordonnance"
    Si votre médecin vous dit "Vous avez une grave infection", et qu'il quitte la pièce sans vous prescrire d'antibiotiques, c'est un mauvais médecin.
    De la même manière, si vous terminez votre fiche de vulnérabilité en disant "Il y a une injection SQL Critique", sans expliquer précisément au développeur comment réparer son code, vous n'avez fait que la moitié de votre travail d'auditeur.

La valeur d'un rapport de cybersécurité ne réside pas dans le nombre de failles trouvées, mais dans **l'applicabilité des solutions proposées**. Un bon pentester est un constructeur (Builder) autant qu'un destructeur (Breaker). La section "Recommandations" est celle qui sera la plus lue par les ingénieurs (DevOps, SysAdmins, Développeurs) dans les semaines qui suivront votre départ.

<br>

---

## Les 3 Niveaux de Remédiation

Une recommandation professionnelle ne doit jamais se limiter à une seule phrase abstraite ("Sécurisez le serveur"). Elle doit proposer des solutions à court, moyen et long terme.

```mermaid
flowchart TD
    %% Couleurs à fort contraste
    classDef root fill:#f8d7da,stroke:#dc3545,stroke-width:2px,color:#000
    classDef short fill:#fff3cd,stroke:#ffc107,stroke-width:2px,color:#000
    classDef medium fill:#cce5ff,stroke:#0d6efd,stroke-width:2px,color:#000
    classDef long fill:#d1e7dd,stroke:#198754,stroke-width:2px,color:#000

    A("🛠️ Plan de Remédiation") --> B("🚨 1. Solution de Contournement<br>(Immédiat / Workaround)")
    A --> C("🔧 2. Correctif Technique<br>(Moyen terme / Patch)")
    A --> D("🏰 3. Défense en Profondeur<br>(Long terme / Stratégie)")

    B --> B1("Ex: Bloquer l'IP attaquante<br>Ex: Désactiver temporairement la fonctionnalité")
    C --> C1("Ex: Mettre à jour la librairie Log4j<br>Ex: Réécrire la requête SQL avec PDO")
    D --> D1("Ex: Mettre en place un WAF<br>Ex: Auditer systématiquement le code avant MEP")

    class A root
    class B,B1 short
    class C,C1 medium
    class D,D1 long
```

### 1. La Solution de Contournement (Workaround)
Lorsque la faille est **Critique** et qu'elle est activement exploitée (ou très facile à exploiter), le client ne peut pas attendre 3 semaines que ses développeurs réécrivent l'application. Vous devez proposer une solution "Pansement" applicable dans l'heure :
*Exemple : "En attendant la mise à jour, configurez le pare-feu Web (WAF) pour bloquer toutes les requêtes HTTP contenant le mot-clé `jndi:`".*

### 2. Le Correctif Technique Définitif (Le Patch)
C'est la vraie solution au problème. Elle cible la racine (Root Cause).
- **Failles applicatives** : Fournir des exemples de code sécurisé (ex: montrer comment échapper les balises HTML en React pour bloquer un XSS).
- **Failles d'infrastructure** : Fournir la configuration recommandée (ex: donner la liste exacte des Cipher Suites TLS cryptographiquement sûrs à copier-coller dans le fichier `nginx.conf`).

### 3. La Défense en Profondeur (Defense in Depth)
Expliquer comment s'assurer que ce type de faille ne se reproduise *plus jamais* à l'avenir.
*Exemple : "Intégrer l'outil SonarQube dans la chaîne CI/CD (GitLab) pour que la compilation échoue automatiquement si une injection SQL est détectée par l'analyseur de code statique."*

<br>

---

## Bonnes & Mauvaises Pratiques (Do's & Don'ts)

| Action | Recommandation | Explication technique |
|---|---|---|
| ✅ **À FAIRE** | **Adapter la solution au contexte du client** | Si le client héberge un vieux serveur industriel sous Windows XP qui pilote une usine (ICS/SCADA), ne recommandez pas "Mettez à jour vers Windows 11". C'est techniquement impossible pour le client. Recommandez l'isolation réseau absolue (Air-Gap) du serveur. |
| ❌ **À NE PAS FAIRE** | **Donner des liens morts ou vagues** | Ne dites pas "Lisez la documentation Microsoft". Fournissez le lien direct vers le correctif exact (KBs) ou vers la page spécifique de l'OWASP Cheat Sheet Series qui traite du problème. L'administrateur système ne doit pas avoir à chercher sur Google pour comprendre votre correctif. |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un pentester détruit des systèmes en quelques heures, mais un administrateur système met parfois des mois à les reconstruire de manière sécurisée. La phase de remédiation est la main tendue entre le monde de l'offensive (Red Team) et le monde de la défense (Blue Team). Rédiger des recommandations claires, respectueuses et réalisables est ce qui garantira votre rappel pour l'audit de l'année suivante.
