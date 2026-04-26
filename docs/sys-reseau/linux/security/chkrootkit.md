---
description: "Rechercher des traces de compromission profonde de l'OS avec le détecteur de Rootkits (Chkrootkit)."
icon: lucide/book-open-check
tags: ["CHKROOTKIT", "ROOTKIT", "SECURITE", "LINUX", "COMPROMISSION"]
---

# Chasse aux Rootkits (Chkrootkit)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="15 - 20 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Le durcissement d'un système Linux est comme la construction des fortifications d'un château. Le pare-feu (UFW) correspond aux douves extérieures, les permissions POSIX (chmod/chown) sont les clés des différentes pièces, et la supervision (Fail2Ban/Lynis) agit comme les gardes effectuant des rondes régulières._

!!! quote "L'ennemi de l'intérieur"
    _Un **Rootkit** est le pire cauchemar d'un administrateur système. C'est un ensemble de logiciels malveillants dont le but est d'obtenir des privilèges "root", puis de modifier le cœur même du système d'exploitation (le noyau ou des commandes de base comme `ls`, `ps` ou `netstat`) pour se rendre totalement invisible. Un pirate équipé d'un rootkit peut ouvrir des portes dérobées, masquer ses fichiers et ses processus : l'OS ment ouvertement à l'administrateur._

## Qu'est-ce que Chkrootkit ?

**Chkrootkit** est un outil shell d'investigation. Il vérifie le système à la recherche des signes de présence (IOC - Indicators of Compromise) de plus de 70 rootkits connus.

```mermaid
graph TD
    subgraph Couche Utilisateur
        CMD[Commande 'ps' ou 'ls']
        Chkrootkit[Détecteur Chkrootkit]
    end
    
    subgraph Couche Noyau (Kernel)
        Kernel[Noyau Linux]
        Rootkit[Module Rootkit Malveillant]
    end
    
    Rootkit -.->|Intercepte & Masque le processus pirate| Kernel
    CMD -->|Demande liste des processus| Kernel
    Kernel -->|Retourne liste MENTIEuse| CMD
    
    Chkrootkit -->|Demande à 'ps'| CMD
    Chkrootkit -->|Interroge directement (Bas niveau)| Kernel
    
    Chkrootkit -->|Compare les deux résultats| Check{Différence ?}
    Check -->|Oui : ps ment !| Alert[⚠️ ROOTKIT DÉTECTÉ]
    Check -->|Non| Safe[✓ OK]
    
    style Rootkit fill:#c0392b,stroke:#fff,color:#fff
    style Chkrootkit fill:#2980b9,stroke:#fff,stroke-width:2px,color:#fff
    style CMD fill:#e67e22,stroke:#fff,color:#fff
    style Alert fill:#c0392b,stroke:#fff,color:#fff
```

Pour ce faire, il n'utilise pas l'antivirus classique, mais compare le comportement de certaines commandes avec ce qui est attendu. Par exemple, il peut interroger directement le noyau pour lister les processus, puis utiliser la commande `ps`. Si les deux listes diffèrent, cela signifie qu'un Rootkit a altéré la commande `ps` pour masquer un processus pirate !

---

## Installation et Exécution

L'outil est très léger et disponible sur la plupart des dépôts.
*(Un outil alternatif très connu et similaire est `rkhunter` / Rootkit Hunter).*

```bash
sudo apt update
sudo apt install chkrootkit
```

### Lancement de la vérification

Il est crucial de lancer `chkrootkit` en tant que `root`, car l'outil doit avoir accès aux fichiers sensibles du système pour vérifier leur intégrité.

```bash
sudo chkrootkit
```

Le scan va lister des dizaines de vérifications en affichant généralement `not found` ou `not infected`.

```text
Checking `amd'... not found
Checking `basename'... not infected
Checking `biff'... not found
Checking `chfn'... not infected
...
Checking `bindshell'... not found
Checking `lkm'... chkproc: nothing detected
```

!!! danger "Faux Positifs"
    `chkrootkit` est connu pour générer occasionnellement des "Faux Positifs" (signaler un danger qui n'en est pas un), notamment avec la détection de processus cachés ou sur certains ports réseau spécifiques. Si l'outil signale `INFECTED`, gardez votre calme et investiguez manuellement (ou croisez les résultats avec `rkhunter`) avant de formater le serveur.

## Comment réagir en cas d'infection réelle ?

Si `chkrootkit` (et `rkhunter`) confirment la présence d'un Rootkit noyau profond (LKM - Loadable Kernel Module), la situation est critique.

La règle d'or en cybersécurité face à un serveur "rooté" est amère :
> **Un système compromis par un rootkit ne peut plus jamais être considéré comme sûr.**

Vous ne pouvez pas vous contenter de "supprimer le rootkit" avec un antivirus, car vous ne pouvez plus faire confiance aux commandes système pour vous dire la vérité.

**La procédure standard (Incident Response) :**
1. Isoler immédiatement le serveur du réseau (déconnecter le câble / stopper la carte réseau virtuelle).
2. Sauvegarder les données métier strictes (bases de données textuelles, fichiers utilisateurs), sans copier les exécutables.
3. Formater le serveur et réinstaller l'OS à partir de zéro.
4. Trouver par quelle faille le pirate est entré initialement (le rootkit est la *conséquence* de l'attaque, pas la *cause*).

## Conclusion

L'utilisation de Chkrootkit est souvent la dernière étape d'un audit de sécurité. S'il ne trouve rien, vous pouvez être raisonnablement serein sur l'intégrité de votre socle système. Cependant, pour qu'il soit vraiment efficace, il faudrait l'exécuter depuis un CD Live ou une clé USB saine, car un rootkit très avancé pourrait même berner `chkrootkit` s'il est exécuté depuis le système déjà infecté.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Sécuriser un système Linux exige une approche en couches : du pare-feu avec UFW à la détection d'intrusions avec Fail2Ban, en passant par un durcissement régulier. Aucun outil de sécurité ne remplace une bonne configuration de base.

> [Retourner à l'index Linux →](../index.md)
