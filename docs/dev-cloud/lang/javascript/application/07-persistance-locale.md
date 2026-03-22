---
description: "Conserver la mémoire de votre application sans serveur Backend : le Web Storage API, différences Storage/Cookies, et rappel sur le format JSON."
icon: lucide/book-open-check
tags: ["JAVASCRIPT", "LOCALSTORAGE", "SESSIONSTORAGE", "JSON", "PERSISTANCE"]
---

# Persistance Locale (Web Storage)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1.5 Heures">
</div>

## Introduction

!!! quote "Analogie Pédagogique - Le Tableau Blanc"
    _Toute l'intelligence que nous avons construite jusqu'ici dans les modules précédents est temporaire : elle est dessinée sur un grand **tableau blanc en classe de cours** (la RAM du navigateur). Si l'administrateur ferme la porte, coupe l'électricité, ou "rafraîchit la page", le concierge passe l'éponge et tout s'efface irréversiblement._
    
    _Le Web Storage vous offre un **petit carnet physique** caché dans la poche de l'administrateur. Il pourra retranscrire ses préférences (Thème Sombre, Paramètres Audios) dans ce carnet, afin que demain, à son retour dans la salle, le système lise le carnet et préconfigure la salle automatiquement._

En l'absence de serveur Backend (PHP, bases de données MySQL), l'API `Web Storage` permet de sauvegarder officiellement des données de façon pérenne **dans le navigateur de vos visiteurs**.

!!! danger "Avertissement Critique Sécurité"
    **Ces données vivent SUR LE DISQUE de l'utilisateur.**  
    Il ne doit y avoir aucun secret, aucun mot de passe en clair, absolument **zéro donnée sensible**. L'utilisateur et potentiellement les virus de sa machine ont un accès absolu et modifiable à ce registre.

<br>

---

## LocalStorage vs SessionStorage

L'API de Storage met à votre disposition deux espaces presque identiques dans leur syntaxe, mais différents dans leur immortalité.

### Le `sessionStorage` (Durée d'un "séjour")
La méthode `window.sessionStorage` conserve ses clés tant que la **fenêtre entière ou l'onglet n'est pas tué**. Il survit parfaitement aux simples rafraichissements de la touche `(F5)` ! Cela le rend terriblement utile pour des fenêtres "assistant" (ex: Un panier d'achat temporaire abandonné à la fermeture).

### Le `localStorage` (L'Éternité)
La méthode `window.localStorage` vit (presque) pour toujours. Il résiste à la fermeture du navigateur, et au redémarrage de la prise de courant d'un ordinateur. Cette mémoire s'effacera uniquement si l'utilisateur ordonne expressément à son navigateur de le faire (via "Effacer l'historique de Navigation et les Cookies").

<br>

---

## La Mécanique (Clés et Valeurs)

Le fonctionnement est simplissime : vous rangez une valeur dans un casier étiqueté. Plus tard, vous donnez l'étiquette au gardien, et il vous rend le colis exact.

```javascript title="JavaScript — Saisir, lire, supprimer"
// 1. Je stocke une préférence (Étiquette, Contenu)
localStorage.setItem('theme_choisi', 'dark');
localStorage.setItem('langue_systeme', 'fr');

// 2. Je lis la préférence (Retourne 'dark')
const preferenceVisiteur = localStorage.getItem('theme_choisi');

// 3. Je la supprime physiquement du disque local
localStorage.removeItem('langue_systeme');

// 4. Je vide intégralement TOUT le Storage de ce domaine. (Destruction)
localStorage.clear();
```

<br>

---

## L'Écueil du format : Le JSON obligatoire

Le LocalStorage possède un défaut colossal : il n'enregistre **rien d'autre que des chaînes de texte basiques (Strings)**.

Si vous tentez d'insérer un Tableau avec l'inventaire complet du Héros (`['épée', 500, false]`) ou un Objet Complexe, le Javascript brutálisera cette donnée et la stockera en marquant littéralement `[object Object]` dans le carnet. 

**C'est à cet instant précis qu'intervient le traducteur JSON.**

!!! note "Besoin d'un rappel fondamental sur le JSON ?"
    Le JSON n'est pas du Javascript en soi, c'est un format textuel universel qui *mime* les objets JS. Si ceci est flou, n'hésitez surtout pas à consulter le cours court sur les [Formats et Sérialisation (JSON)](../../../../../bases/formats-serialisation/json.md).

### Stringify & Parse

Le standard JS vous offre un module `JSON` global avec deux ponts majeurs pour faire des allers-retours entre le monde "Objet Vivant" et le monde "Texte Imprimé" du LocalStorage.

```javascript title="JavaScript — L'encodage JSON au secours du localstorage"

const joueur = { 
    pseudo: "Bob", 
    niveau: 42 
};

/* -------------------------------------------------------------
 * ENREGISTREMENT (JSON.stringify) : Le Compacteur
 * ------------------------------------------------------------- 
 * Il écrase un objet vivant et le zippe en une longue phrase de pur texte. 
 * '{"pseudo":"Bob","niveau":42}' 
 */
 
localStorage.setItem('profil_joueur', JSON.stringify(joueur));


/* -------------------------------------------------------------
 * LECTURE (JSON.parse) : Le Gonfleur magique
 * ------------------------------------------------------------- 
 * Le carnet nous recrache son vieux bout de texte poussiéreux,
 * mais la méthode .parse() le réanime instantanément en Objet JS Navigable !
 */
 
const donnéesBrutesDuTexte = localStorage.getItem('profil_joueur');
const joueurRessuscité = JSON.parse(donnéesBrutesDuTexte);

console.log(joueurRessuscité.niveau); // Affiche 42 ! Le moteur revit.
```

<br>

---

## Les Cookies sont-ils morts ?

*"Pourquoi n'utilisons-nous plus les cookies du début des années 2000 que les sites nous réclament toute la journée ?"*

Les cookies n'ont en réalité **rien à voir avec le stockage applicatif Front-End**. Ils ne peuvent contenir que **4 Kilooctets** (contre plus de **5000 Ko** pour un LocalStorage), et sont extrêmement pénibles à lire et écrire en JavaScript. 

Le rôle authentique d'un Cookie en 2026 est de **voyager automatiquement dans le sac à dos d'une requête HTTP vers le serveur Backend** à chaque rechargement de page. Ce sont des jetons de sécurité cryptés pour l'onglet de session, lus généralement par le PHP, jamais par le développeur Front-End pour ranger un système de mode sombre.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Avoir un stockage local pérenne se résume à une danse en deux temps :
    `localStorage.setItem('clé', valeur)` (souvent couplé à `JSON.stringify()` pour les tableaux), puis au rechargement de page une relecture silencieuse avec `getItem('clé')` couplée au restaurateur `JSON.parse()`. Avec cette architecture simple, vos créations Front-End gagnent une persistance digne des applications lourdes de vos machines.

> Les données vivent maintenant en paix dans la machine de l'utilisateur. 
Mais que faire lorsque l'on souhaite "Attendre la fin d'une animation", "Lancer un chronomètre sans freeze l'ordinateur" ou "Demander l'affichage dynamique d'un texte issu d'un autre site en attente réseau" ? 
> C'est ici, et seulement ici, que l'ingénierie Javascript révèle sa vraie puissance asynchrone : [**L'Event Loop et l'Asynchrone**](./08-logique-asynchrone.md).

<br />
