---
title: 2.1 Auto-évaluation diagnostique
description: Test de positionnement en 80 questions couvrant Linux, Windows, macOS, réseaux, cryptographie et concepts forensic. Identifier vos lacunes pour cibler votre apprentissage du module 2.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Auto-évaluation
  - Diagnostic
  - Compétences
data-level: 🟡
---

# 2.1 Auto-évaluation diagnostique

!!! quote "L'analogie du bilan médical avant un marathon"

    Avant de courir un marathon, un coureur sérieux fait un bilan médical complet. Cardio, articulations, capacité respiratoire. Pas pour se décourager, mais pour identifier ce qui doit être renforcé pendant la préparation. Le test diagnostique de ce chapitre joue le même rôle. Vous ne le passez pas pour obtenir une note. Vous le passez pour identifier les domaines où vous devez approfondir votre apprentissage. Soyez honnête avec vous-même : un domaine où vous bricolez aujourd'hui sera un trou béant dans votre compétence forensic demain.

## Métadonnées du chapitre

| Champ | Valeur |
|---|---|
| Durée estimée | 2 heures |
| Niveau | Diagnostic |
| Prérequis | Aucun |
| Livrables | Tableau de scoring personnel, plan d'apprentissage ciblé |

## Méthode

Répondez aux 80 questions par écrit, sans aide. Chaque question vaut 1 point. Comptez votre score par section.

| Score par section (sur 10) | Niveau |
|---|---|
| 0-3 | Débutant - chapitre indispensable en intégralité |
| 4-6 | Intermédiaire - chapitre à approfondir |
| 7-8 | Avancé - chapitre à survoler |
| 9-10 | Expert - chapitre éventuellement validé sans étude |

---

## Section 1 - Linux fondamentaux (questions 1-10)

1. Quelle commande affiche les permissions d'un fichier en format octal ?
2. Que représentent les trois groupes dans `rwxr-xr--` ?
3. Que fait `chmod u+s fichier` et quel risque cela présente ?
4. Quelle est la différence entre `>` et `>>` en redirection ?
5. Comment trouver tous les fichiers SUID sur un système ?
6. Que contient `/etc/shadow` et qui peut le lire ?
7. Quelle commande affiche les processus en cours avec leur arborescence ?
8. Que fait `kill -9 PID` et pourquoi est-ce dangereux ?
9. Quelle est la différence entre `/etc/passwd` et `/etc/shadow` ?
10. Comment monter une partition en lecture seule ?

## Section 2 - Linux avancé (questions 11-20)

11. Quel répertoire contient les services systemd custom ?
12. Comment afficher les logs systemd des dernières 2 heures ?
13. Que contient `/proc/[PID]/maps` ?
14. Comment voir les sockets ouverts en TCP avec leurs PID ?
15. Quelle est la fonction des namespaces Linux ?
16. Que fait `auditctl -w /etc/passwd -p wa -k passwd_changes` ?
17. Comment lister tous les services systemd actifs ?
18. Que montre `ss -tunlp` ?
19. Que fait `strace` sur un processus en cours ?
20. Où sont stockés les logs d'authentification standard ?

## Section 3 - Windows fondamentaux (questions 21-30)

21. Quelle est la différence entre HKEY_CURRENT_USER et HKEY_LOCAL_MACHINE ?
22. Que fait `taskmgr.exe` et quelles infos clés affiche-t-il ?
23. Comment voir les services Windows en CLI ?
24. Quelle commande liste les utilisateurs locaux ?
25. Que fait `gpedit.msc` ?
26. Quelle clé du registre liste les programmes lancés au démarrage ?
27. Que contient `C:\Windows\System32\config\` ?
28. Quelle est la différence entre LSASS et SAM ?
29. Que fait `whoami /priv` ?
30. Que fait `net user` sans argument ?

## Section 4 - macOS fondamentaux (questions 31-40)

31. Comment afficher les caractéristiques du Mac (puce, RAM, version macOS) en CLI ?
32. Quelle est la différence entre /System/Library et /Library ?
33. Que fait System Integrity Protection (SIP) ?
34. Comment lister les launchd agents avec leur statut ?
35. Que contient `~/Library/Preferences/` ?
36. Comment voir les logs unifiés de la dernière heure en CLI ?
37. Qu'est-ce que TCC.db et où est-il stocké ?
38. Quelle commande affiche les processus en cours ?
39. Comment activer ou désactiver FileVault depuis le terminal ?
40. Qu'est-ce que la Secure Enclave et où réside-t-elle ?

## Section 5 - Réseaux (questions 41-50)

41. Que contient un en-tête TCP minimum (5 champs) ?
42. À quoi sert le 3-way handshake ?
43. Que fait ARP et pourquoi est-il vulnérable ?
44. Quelle plage IP est privée selon RFC 1918 ?
45. Que renvoie `nslookup omnyvia.fr A` ?
46. Que fait `dig +trace omnyvia.fr` ?
47. Quelle est la différence TCP/UDP ?
48. À quoi sert un port en TCP ?
49. Que capture `tcpdump -i eth0 -nn port 443` ?
50. Que sont les ports privilégiés et lesquels ?

## Section 6 - Cryptographie (questions 51-60)

51. Différence symétrique / asymétrique ?
52. Pourquoi AES-256 est-il considéré sûr en 2026 ?
53. Que fait un hash cryptographique ?
54. Pourquoi MD5 est-il déconseillé ?
55. Qu'est-ce qu'une signature numérique ?
56. Que contient un certificat X.509 ?
57. Différence entre chiffrement et encodage (base64) ?
58. Que fait HMAC ?
59. Qu'est-ce que la PKI ?
60. Pourquoi RSA-2048 minimum aujourd'hui ?

## Section 7 - Systèmes de fichiers (questions 61-70)

61. Que contient le MFT en NTFS ?
62. Que sont les ADS (Alternate Data Streams) ?
63. Comment ext4 organise-t-il les données ?
64. Qu'est-ce qu'un inode ?
65. Que fait le journaling ext4 ?
66. Qu'est-ce qu'APFS et quand est-il devenu standard ?
67. Que sont les snapshots APFS ?
68. Comment APFS gère le copy-on-write ?
69. Que fait fsck (Linux) ?
70. Que fait chkdsk (Windows) ?

## Section 8 - Concepts forensic (questions 71-80)

71. Que dit RFC 3227 sur la priorité d'acquisition ?
72. Quelle est la chaîne de garde ?
73. Qu'est-ce que la volatilité des données ?
74. Quelle différence entre acquisition à chaud et à froid ?
75. Pourquoi calculer un hash après acquisition ?
76. Qu'est-ce qu'un write-blocker ?
77. Quelle différence entre dd et dc3dd ?
78. Que sont les artefacts forensic ?
79. Qu'est-ce que la timeline forensic ?
80. Quel format est standard pour images forensic (E01) ?

---

## Auto-correction

Pour chaque question, relisez le chapitre concerné si vous n'aviez pas la réponse. Les chapitres correspondants sont :

| Section | Chapitres OmnyAcademy |
|---|---|
| 1 | 2.2 Linux fondamentaux |
| 2 | 2.3 Linux avancé |
| 3 | 2.4 Windows |
| 4 | 2.4 bis macOS |
| 5 | 2.6 Réseaux |
| 6 | 2.7 et 2.8 Crypto |
| 7 | 2.9, 2.10, 2.10 bis Systèmes de fichiers |
| 8 | Cycle 1 forensic |

## Tableau de scoring personnel

```text
RÉSULTAT AUTO-ÉVALUATION - DD/MM/2026

Section 1 Linux fond.   : __/10  Niveau : __________
Section 2 Linux avancé  : __/10  Niveau : __________
Section 3 Windows       : __/10  Niveau : __________
Section 4 macOS         : __/10  Niveau : __________
Section 5 Réseaux       : __/10  Niveau : __________
Section 6 Cryptographie : __/10  Niveau : __________
Section 7 Systèmes fich.: __/10  Niveau : __________
Section 8 Forensic      : __/10  Niveau : __________

TOTAL                   : __/80

PRIORITÉS DE TRAVAIL :
1. _________________________________
2. _________________________________
3. _________________________________
```

## Plan d'apprentissage adaptatif

| Score total | Plan recommandé |
|---|---|
| 0-30 | Module 2 complet en intensif (10-12 semaines) |
| 31-50 | Module 2 ciblé sur sections faibles (6-8 semaines) |
| 51-65 | Module 2 survol + approfondissement ciblé (4 semaines) |
| 66-80 | Module 2 validé, passage direct au module 3 |

---

**Chapitre suivant** : [2.2 Linux fondamentaux](02-2-linux-fondamentaux.md)
