---
description: "Les meilleures pratiques pour durcir (Harden) un environnement Windows Server et Active Directory."
icon: lucide/book-open-check
tags: ["WINDOWS", "HARDENING", "SECURITE", "DURCISSEMENT", "AD"]
---

# Durcissement (Hardening)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="25 - 35 minutes">
</div>

!!! quote "Réduire la surface d'attaque Microsoft"
    _Par défaut, un système Windows Server est configuré pour un maximum de "compatibilité" (rétro-compatibilité avec d'anciens protocoles des années 90) et de "facilité d'utilisation". En cybersécurité, la facilité est souvent l'ennemie de la protection. Le durcissement (Hardening) consiste à configurer finement l'OS et l'Active Directory pour bloquer les techniques de piratage les plus courantes._

## 1. La désactivation des protocoles obsolètes

La première étape du Hardening Windows consiste à fermer les portes vétustes que les attaquants adorent exploiter.

### Le protocole LLMNR et NBT-NS
Ces protocoles de résolution de noms permettent à un PC de demander "Qui connaît ce serveur ?" sur le réseau local si le DNS échoue. Les attaquants utilisent l'outil `Responder` pour mentir et voler les mots de passe (hashes NTLM).
- **Action** : Désactiver LLMNR et NetBIOS via une GPO globale.

### SMBv1
Le protocole de partage de fichiers SMB version 1 est gravissimement vulnérable (C'est lui qui a permis la propagation mondiale du ransomware WannaCry via la faille EternalBlue).
- **Action** : Désactiver totalement le service SMBv1 sur toutes les machines. Utiliser SMBv3 exclusivement.

### L'authentification NTLMv1
NTLM est un vieux protocole d'authentification. Ses algorithmes de chiffrement sont aujourd'hui cassables en quelques secondes.
- **Action** : Forcer le réseau à n'utiliser que **Kerberos** ou, à défaut, NTLMv2.

---

## 2. Le Modèle d'Administration en Tiers (Tiering)

C'est LA recommandation absolue de Microsoft (et de l'ANSSI en France) pour sécuriser un annuaire Active Directory. Le principe est de compartimenter les privilèges pour empêcher le mouvement latéral.

On divise l'infrastructure en 3 Tiers (Niveaux) hermétiques :

```mermaid
graph TD
    subgraph "Modèle d'Administration en Tiers (Tiering)"
        T0[Tier 0: Joyaux de la Couronne <br/> DC, PKI, Entra Connect]
        T1[Tier 1: Serveurs <br/> ERP, BDD, Fichiers]
        T2[Tier 2: Postes de travail <br/> Laptops, PC]
    end
    
    Admin0[Admin Tier 0 <br/> adm_johndoe] -->|Autorisé| T0
    Admin1[Admin Tier 1 <br/> srv_johndoe] -->|Autorisé| T1
    Admin2[Admin Tier 2 <br/> help_johndoe] -->|Autorisé| T2
    
    Admin0 -.->|Déni d'accès (GPO)| T1
    Admin0 -.->|Déni absolu : Risque de vol de credential| T2
    
    style T0 fill:#c0392b,stroke:#fff,color:#fff
    style T1 fill:#e67e22,stroke:#fff,color:#fff
    style T2 fill:#27ae60,stroke:#fff,color:#fff
    style Admin0 fill:#2980b9,stroke:#fff,color:#fff
```

<div class="grid cards" markdown>

-   :lucide-crown:{ .lg .middle } **Tier 0 (Identité)**
    ---
    Les Contrôleurs de Domaine (DC), PKI, et les administrateurs du domaine. Les joyaux de la couronne.

-   :lucide-server:{ .lg .middle } **Tier 1 (Serveurs)**
    ---
    Les serveurs applicatifs (Web, Base de données, Fichiers).

-   :lucide-laptop:{ .lg .middle } **Tier 2 (Postes de travail)**
    ---
    Les PC des employés et les utilisateurs standards (le point d'entrée classique des ransomwares via Phishing).

</div>

**La règle d'or du Tiering :** 
Un administrateur Tier 0 (Domain Admin) n'a **JAMAIS LE DROIT** de se connecter sur un PC de Tier 2, même pour "dépanner vite fait". Si un PC Tier 2 est compromis par un pirate, et que l'admin s'y connecte, le pirate peut voler son "Token" en mémoire (attaque Pass-The-Hash via l'outil Mimikatz) et rebondir instantanément sur le Tier 0.

L'administrateur doit posséder 2 comptes séparés : `adm_johndoe` (Tier 0, pour gérer l'AD) et `tech_johndoe` (Tier 2, pour dépanner les PC).

---

## 3. Audit et Logs (Event Viewer)

Par défaut, Windows n'enregistre pas suffisamment de journaux (Logs) pour repérer une attaque avancée. Il faut forcer l'audit via GPO (Advanced Audit Policy Configuration).

Ce que vous DEVEZ logger et surveiller (souvent via un SIEM) :
- Les succès/échecs d'authentification (`Event ID 4624` et `4625`).
- L'ajout d'utilisateurs à des groupes sensibles (`Event ID 4728`).
- L'effacement du journal des événements (Le signe ultime qu'un pirate essaie de couvrir ses traces : `Event ID 1102`).
- L'exécution de processus en ligne de commande (Activer le "Command Line Auditing" `Event ID 4688` pour voir ce que font les scripts PowerShell malveillants).

## 4. Outils d'aide au durcissement

Pour ne pas partir de zéro, les administrateurs s'appuient sur des standards de l'industrie :
- **CIS Benchmarks** (Center for Internet Security) : Fournit des documents PDF ultra-détaillés sur la valeur exacte de chaque paramètre de sécurité (des centaines de pages).
- **Microsoft Security Compliance Toolkit (SCT)** : Outils officiels pour tester, comparer et appliquer des baselines de sécurité recommandées par Microsoft directement sous forme de GPO prêtes à l'emploi.

## Conclusion

Le durcissement de Windows est un exercice d'équilibriste. C'est l'opposition classique entre l'Ops (qui veut que le système "fonctionne facilement") et le Sec (qui veut que le système "soit verrouillé"). Désactiver d'anciens protocoles cassera inévitablement de vieilles applications métier. L'art de l'administrateur système moderne est d'appliquer ce durcissement par vagues, en auditant silencieusement l'impact avant d'interdire définitivement.