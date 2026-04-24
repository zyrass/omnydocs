---
title: L'Entropie des Mots de Passe
description: Démystifier le mythe de la complexité obligatoire face à l'entropie mathématique (la longueur), et comprendre les recommandations de la CNIL.
icon: lucide/book-open-check
tags: ["SECRETS", "ENTROPIE", "CNIL", "BRUTE-FORCE", "SECURITE"]
---

# L'Entropie des Mots de Passe

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="20-30 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Coffre-Fort"
    Imaginez un coffre-fort avec un cadran à 3 chiffres. Pour l'ouvrir, le voleur essaie "000", puis "001", jusqu'à "999". Il y a 1000 combinaisons possibles. C'est rapide.
    
    Pour compliquer la tâche, le fabricant décide de rajouter l'alphabet sur le cadran. Le voleur doit maintenant essayer des lettres et des chiffres sur 3 cases (ex: "A1B"). C'est plus dur (environ 46 000 combinaisons).
    
    Mais un ingénieur plus malin propose autre chose : gardons le cadran avec **seulement des chiffres**, mais ajoutons **7 roulettes** supplémentaires (un code à 10 chiffres). Le voleur doit essayer de "0000000000" à "9999999999" (10 milliards de combinaisons). 
    
    *Moralité : La longueur du code protège infiniment plus que la complexité des symboles.*

Pendant des décennies, l'informatique nous a imposé la règle de la complexité arbitraire : *"Votre mot de passe doit contenir 1 majuscule, 1 chiffre, 1 caractère spécial, et le sang d'une licorne"*. Cette règle a créé une catastrophe mondiale de sécurité humaine.

<br>

---

## L'Échec de la Complexité Arbitraire

Face aux règles de complexité, le cerveau humain trouve des failles de facilité.

On demande à un utilisateur de changer son mot de passe `Soleil`.
Avec la règle de complexité, il choisira `Soleil1!`. Puis au prochain changement obligatoire de 90 jours : `Soleil2!`, puis `Soleil3!`.

Les pirates le savent. Leurs dictionnaires d'attaque Brute-Force testent automatiquement ces patterns. Le mot de passe `T0m@te!` est mathématiquement "complexe", mais il sera craqué en **2 secondes** par une carte graphique moderne.

<br>

---

## Le Triomphe de l'Entropie Mathématique

L'entropie est l'unité de mesure du chaos, ou de la "quantité de désordre" dans un mot de passe. Elle se mesure en **bits**.

- **Mot de passe Complexe, mais court** : `Tr0ub4dor&3` (11 caractères). 
  Il contient des majuscules, des chiffres et des symboles. Une ferme de cartes graphiques le trouvera en **3 jours**.

- **Mot de passe Simple, mais long (Passphrase)** : `correct cheval batterie agrafe` (30 caractères).
  Il ne contient *que* des lettres minuscules et des espaces. Il est très facile à mémoriser pour un humain. Pourtant, sa longueur est telle qu'il faudrait **500 millions d'années** aux supercalculateurs de la planète entière pour essayer toutes les combinaisons possibles.

!!! tip "La Règle d'Or"
    **La longueur bat la complexité, à chaque fois.** Privilégiez les *Phrases Secrètes* (Passphrases) aux Mots de Passe.

<br>

---

## La Position Officielle de la CNIL

En France, la gestion des mots de passe n'est pas qu'une question technique, c'est une question **Légale**. La **CNIL** (Commission Nationale de l'Informatique et des Libertés) édite des recommandations strictes, qui peuvent valoir des sanctions financières colossales aux entreprises en cas de fuite de données (RGPD).

En 2022, la CNIL a mis à jour sa doctrine (Délibération n° 2022-100) en donnant le choix aux entreprises entre plusieurs scénarios. Observez comment la CNIL a officiellement intégré le concept d'entropie :

| Scénario CNIL | Condition requise (Longueur) | Condition requise (Complexité) |
| --- | --- | --- |
| **Cas n°1 (Le Classique)** | Minimum **12 caractères** | Au moins 3 des 4 catégories (Majuscules, Minuscules, Chiffres, Spéciaux) |
| **Cas n°2 (La Passphrase)** | Minimum **14 caractères** | **AUCUNE COMPLEXITÉ REQUISE**. Juste des lettres ! |
| **Cas n°3 (Avec MFA)** | Minimum **8 caractères** | Complété obligatoirement par une authentification multi-facteurs (Code SMS, App Authenticator) |

> *Source : Recommandations de la CNIL relatives à l’authentification par mot de passe.*

Les développeurs ont le devoir d'implémenter ces standards et de guider l'utilisateur lors de son inscription avec une barre de progression jaugeant l'entropie réelle (et non la simple présence de caractères spéciaux).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les pirates ne "devinent" pas les mots de passe de tête. Ils utilisent des machines qui calculent des milliards de combinaisons par seconde. Face aux mathématiques, la **longueur d'une phrase** (Entropie) est un mur infranchissable, alors qu'une suite de **symboles complexes courts** est un filet percé. Alignez systématiquement votre politique de sécurité sur les recommandations légales de la **CNIL**.

> Les utilisateurs humains savent mémoriser des Passphrases. Mais comment un *Serveur Automatisé* fait-il pour s'authentifier auprès de la Base de Données s'il n'a pas de cerveau humain pour se souvenir d'un mot de passe ? C'est tout le génie de **HashiCorp Vault**.

<br>