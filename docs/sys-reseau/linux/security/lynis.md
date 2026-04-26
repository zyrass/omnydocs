---
description: "Auditer la configuration de sécurité de son serveur Linux et appliquer les recommandations de conformité avec Lynis."
icon: lucide/book-open-check
tags: ["LYNIS", "AUDIT", "SECURITE", "HARDENING", "CONFORMITE"]
---

# Audit Système avec Lynis

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="15 - 20 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Le durcissement d'un système Linux est comme la construction des fortifications d'un château. Le pare-feu (UFW) correspond aux douves extérieures, les permissions POSIX (chmod/chown) sont les clés des différentes pièces, et la supervision (Fail2Ban/Lynis) agit comme les gardes effectuant des rondes régulières._

!!! quote "Le bilan de santé du serveur"
    _Avant de commencer à fermer des ports ou à installer des antivirus, il est judicieux de faire un état des lieux. **Lynis** est un outil d'audit de sécurité open-source, très respecté dans l'industrie. Il n'installe rien et ne modifie rien sur votre serveur : il se contente de le scanner sous toutes ses coutures pour vérifier s'il respecte les meilleures pratiques de sécurité._

## Pourquoi utiliser Lynis ?

Les administrateurs systèmes utilisent Lynis pour :

```mermaid
graph TD
    Start[Exécution : lynis audit system] --> Collect[Collecte des Configurations (OS, Fichiers, Ports)]
    Collect --> Check[Tests de Sécurité (Comparaison avec la Baseline)]
    
    Check --> ResultOK[✓ Tests Réussis (OK)]
    Check --> ResultWarn[⚠️ Avertissements Critiques (WARNING)]
    Check --> ResultSugg[💡 Bonnes Pratiques (SUGGESTION)]
    
    ResultOK --> Report[Génération du Fichier de Log /var/log/lynis-report.dat]
    ResultWarn --> Report
    ResultSugg --> Report
    
    Report --> Score[Calcul du Score de Durcissement (Hardening Index)]
    
    style Start fill:#1a5276,stroke:#fff,color:#fff
    style ResultOK fill:#27ae60,stroke:#fff,color:#fff
    style ResultWarn fill:#c0392b,stroke:#fff,color:#fff
    style ResultSugg fill:#2980b9,stroke:#fff,color:#fff
    style Score fill:#e67e22,stroke:#fff,color:#fff
```

- **Auditer la sécurité** : Vérifier les permissions des fichiers critiques, la configuration de SSH, la solidité des mots de passe.
- **La Conformité (Compliance)** : S'assurer que le serveur respecte des normes comme PCI-DSS, HIPAA, ou ISO27001.
- **La Détection de vulnérabilités** : Trouver des erreurs de configuration courantes.

L'énorme avantage de Lynis est qu'il est léger, ne nécessite aucune dépendance exotique (c'est un simple script shell), et génère un rapport extrêmement clair.

---

## Installation et Exécution

Lynis est présent dans les dépôts de la plupart des distributions, mais il est souvent conseillé de cloner le dépôt GitHub pour avoir la version la plus à jour (qui inclut les dernières vérifications).

```bash
# Installation via les dépôts (Debian/Ubuntu)
sudo apt update
sudo apt install lynis

# Exécution de l'audit système complet
sudo lynis audit system
```

## Lire le Rapport Lynis

L'audit prend généralement moins d'une minute. Pendant l'exécution, vous verrez défiler des centaines de tests avec les statuts `[ OK ]`, `[ WARNING ]` ou `[ SUGGESTION ]`.

À la fin du scan, Lynis vous donne un résumé et un **Score (Hardening index)** sur 100. Un serveur fraîchement installé tourne souvent autour de 60/100. Le but n'est pas forcément d'atteindre 100/100 (ce qui rendrait le serveur presque inutilisable), mais de corriger l'évidence.

### Les Suggestions (Warnings & Suggestions)
La partie la plus utile du rapport se trouve à la fin :

```text
  -[ Lynis 3.0.0 Results ]-

  Warnings (2):
  ----------------------------
  ! Reboot of system is most likely needed [KRNL-5830]
  ! Found one or more vulnerable packages [PKGS-7392]

  Suggestions (40):
  ----------------------------
  * Install a PAM module for password strength testing like pam_cracklib or pam_pwquality [AUTH-9262]
    - Details  : https://cisofy.com/lynis/controls/AUTH-9262/
```

Chaque suggestion est accompagnée d'un identifiant (ex: `AUTH-9262`) et d'un lien (souvent vers le site de Cisofy, le créateur de Lynis) qui explique *pourquoi* ce réglage est dangereux et *comment* le corriger.

## Conclusion

Lynis devrait être exécuté systématiquement après l'installation initiale d'un serveur (pour établir une "Baseline" de sécurité), puis régulièrement (via Cron) pour s'assurer que des modifications ultérieures n'ont pas introduit de failles de configuration.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Sécuriser un système Linux exige une approche en couches : du pare-feu avec UFW à la détection d'intrusions avec Fail2Ban, en passant par un durcissement régulier. Aucun outil de sécurité ne remplace une bonne configuration de base.

> [Retourner à l'index Linux →](../index.md)
