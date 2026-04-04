---
description: "Évaluer ses compétences avec un parcours de carrière, un QCM de conclusion et terminer les apprentissages sur le Framework PHP."
icon: lucide/graduation-cap
tags: ["LARAVEL", "SUMMARY", "CAREER", "QCM", "EXERCICE"]
---

# Évaluations & Parcours

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1 Heure">
</div>

## 1. Exercice de Synthèse Moderne TALL

En utilisant les outils vus précédemment sur les modules de Modélisation BDD et le cours du TALL : Essayer de monter sur Livewire un "Mécanisme Magique de Upvote/Downvote" pour des Modèles d'Avis Post ! 

Si l'utilisateur connecté clique en `x-click`, alors les scores visuels au re-render se mettent à jour avec le compte SQL !!

**Piste : Ne pas oublier que dans la méthode `public function render()` d'un livewire, on insère d'ordinaire pas nos Update ou DB. Etudiez comment vous y prendre côté Controller PHP en injectant l''id de Post !** 

<details>
<summary>Correction du Projet et Méthodologies</summary>

- [ ] L'idée est celle d'un nouveau Bouton `php artisan make:livewire VoteComponent`.
- [ ] Sa classe PHP doit recevoir par les params depuis la page mere une Valeur du Post (`<livewire:vote-component :postID="$postID" />`).
- [ ] Avec la réception magique avec `Public Function mount($postID)` (similaire à Construct au démarage du component). IL faut enregistrer son ID en global !
- [ ] On crée dans ce fichier Livewire une simple méthode d'Upload du style `Public function clickScoreUp()` et son parent au CSS `clickScoreDown()`.
- [ ] Avec les `Score++` enregistrés en BDD dans les fonctions PHP, le Render Livewire lui va rebalancer la page à lui seul en retournant le `count()` ou le `$score`.
- [ ] HTML Side : `<button wire:click="clickScoreUp"> Upvote Moi </button>`.

</details>

<br>

---


##  2. Roadmap de progression Post-Formation

A l'issue des Modules 1-8. Vous avez accomplit de fond en comble la validation de votre Profil en tant que Développeur Backend Junior+.  (Laravel Route, Eloquent, Middlewares, API/JSON, Validation/Uploads et notions d'Architecture FSM, TALL, Starter Kit & Service Externes). Mais vous n'avez pas acquis l'Etape Senior. 

Mois 1-3 : Consolidation (Back Junior+)
* Effectuer des tests TDD automatisés complexes (Pest/PhPunit).

**Si vous visez ce Full-Stack ou Backend Master (Intermédiaire+)**
* Les Architectures plus profondes (Domaine Drive Design), l'Héxagone. Repositories.
* Implémenter et relier un Redis de Notification et Queue Works.
* Implémenter **Laravel Sanctum ou Passport** pour fermer des JSON API par Tokens pour les Mobile. 
* Les Devops Cloud (Déploié via CI/CD Pipeline vos repos et la base AWS).
* Laravel Sail (Docker) local.
* Sécurisation Pentest et Telescope Debuggage avancé.


<br>

---

## 3. L'Ultime Auto-Évaluation Masterclass Laravel

Validez vos compétences acquises globales :


1. **Question :** Dans l'univers de Laravel pour propulser un frontend. Quelle différence fondamentale existe entre Alpine "TA[LL]" face à Livewire "[TA]LL" ?
   <details>
   <summary>Réponse</summary>
   Le rôle du script : Alpine fait bouger les éléments HTML par son attribut Javascript (`x` : Toggle un Menu, Binding live Input..), là ou Livewire requiert la base de donnée serveuse via PHP et le controller magique asynchrone (`wire:` Afficher des tables, Pagination Ajax sans refresh...).
   </details>

2. **Question :** Quelle est la différence entre une application SPAs pour une compagnie ?
   <details>
   <summary>Réponse</summary>
   L'application TALL et Breeze est le rempart pour un dev solo désirant les memes technologies temps réel. Avec React (SPA), la base de données doit créer une Route API qui réponds du brut JSON. React et la Team doivent consommer ce JSON des mois durant avant d'avoir des résultats probants de requetage client/serveur via leur outil (Vue, Axios... Redux..)
   Liveware le fait nativement et directement rendu en HTML au "moteur backend" (S.S.R), excellent au référencement web des robots Google (S.E.O).
   </details>



## Félicitations ! ✨

> Vous avez complété avec succès plus de **80 à 100 heures** de cursus pédagogiques sur l'Univers de Laravel ! Vous êtes pret à entreprendre en maitrisant votre Backoffice, l'authentification native par jetons, la configuration et modélisation de relations base de données complexes et d'upload asynchrones, le tout via des composants réactifs Tailwind modernes par le Bias des technologies de l'Éssaim de PHP ! Continuez de consolider. Chaque bugs rencontré est un formateur vers le monde Senior et la contribution Open-Source. C'était la Zensical Masterclass de l'Equipe OmnyDocs !
