---
description: "Bibliothèque des travaux pratiques et projets mobiles en SwiftUI et Vapor."
icon: lucide/folder-kanban
tags: ["PROJETS", "SWIFTUI", "VAPOR", "PRATIQUE"]
---

# Bibliothèque de Projets (SwiftUI & Vapor)

<div
  class="omny-meta"
  data-level="🟢 Multi-niveaux"
  data-version="1.0"
  data-time="Variable">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "L'importance de la pratique"
    La lecture d'une documentation technique forge le **savoir**. Mais l'écriture d'une application de bout en bout forge le **savoir-faire**. Les concepts de `@State`, de Cycle de Vie ou de Middlewares Vapor ne deviendront instinctifs qu'après les avoir intégrés dans des projets utilitaires bien réels. 

Cette section est le cœur pratique de la formation Mobile. Elle propose un cursus de **6 projets** allant de la simple interface isolée (Débutant) au "Saint Graal" de l'application sécurisée Fullstack avec base de données, biométrie, et connexion serveur.

---

## 🟢 Niveau 1 : Initiation Interface et États
*Focus : SwiftUI pur et persistance locale extrêmement rapide. Aucun appel réseau externe.*

1. **[Projet 1 : Pomodoro Focus](01-pomodoro-focus.md)**
   Un minuteur de productivité. Prise en main des composants temporels (`Timer`), des modificateurs visuels dynamiques (`Circle().trim`), et des états d'interface vitaux.
2. **[Projet 2 : Disney Vault](02-disney-vault.md)**
   Une base de données personnelle. Gestion des listes dynamiques (`List`, `ForEach`), des vues de détail (Navigation), et application de logiques conditionnelles strictes (L'Easter Egg de la VHS *Mélodie du Sud*).
3. **[Projet 3 : Hero Tap Clicker](03-hero-clicker.md)**
   Un micro-jeu addictif. Introduction brutale à `@AppStorage` pour la persistance locale du score et gestion d'une UI à haute réactivité (rafraîchissement 60fps).

---

## 🟡 Niveau 2 : Monde Réel, Données & Matériel
*Focus : Appels asynchrones, API du Cloud, et interfaçage avec les composants du téléphone.*

4. **[Projet 4 : OmnyScan](04-omnyscan.md)** 
   Le gestionnaire de chariot. Utilisation de l'appareil photo via `AVFoundation` pour lire des codes-barres. Intégration de **Swift Charts** pour afficher les courbes d'inflation tarifaire de vos produits re-scannés.
5. **[Projet 5 : OmnyNews](05-omnynews.md)**
   L'aggrégateur d'articles externe. Gestion intégrale du protocole HTTP client avec `URLSession` et `async/await`. Décodage de la donnée (`Codable`) et traitement des erreurs de chargement.

---

## 🔴 Niveau 3 : Le "Saint Graal"
*Focus : Architecture de production, Sécurité Cyber, Backend Linux et Frontend iOS en harmonie.*

6. **[Projet 6 : OmnySafe (Fullstack)](06-omnysafe.md)**
   Un coffre-fort numérique encrypté et son gestionnaire d'équipe.
   - **Côté Serveur (Vapor) :** Base de données PostgreSQL, encryptage de mots de passe par l'algorithme fort `BCrypt`, émission de tokens de sécurité `JWT`, et blocage de requêtes par "Rate Limiting". Modélisation stricte MCD/MLD/MPD.
   - **Côté Client (SwiftUI) :** Protection de l'application via `Face ID` / `Touch ID`, sauvegarde des sercrets dans le `Keychain` d'Apple, architecture en Intercepteurs (Rafraichissement du token silencieux).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
