---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 5

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Patterns pro : formulaire contrôlé (state cohérent, reset propre, erreurs fréquentes)

### Objectif de la leçon

À la fin, tu sauras :

* ce qu’est un **formulaire contrôlé** (et pourquoi c’est important)
* structurer ton state pour éviter le chaos
* gérer un reset propre sans “bug fantôme”
* éviter les erreurs fréquentes qui rendent un formulaire instable
* construire un pattern réutilisable pour tes futurs projets (Todo, Blog mock, Tracker, etc.)

Cette leçon est essentielle parce qu’un formulaire, c’est souvent le premier endroit où un projet devient fragile.

---

## 1) Définition : “formulaire contrôlé”, ça veut dire quoi ?

Un formulaire contrôlé signifie :

> Les champs du formulaire sont pilotés par ton state (Alpine), et le state est la source de vérité.

Concrètement :

* tu n’utilises pas le DOM comme stockage “caché”
* tu ne récupères pas les valeurs à la fin en mode “surprise”
* tu sais exactement ce que contient ton formulaire à tout moment

### Analogie simple

Un formulaire non contrôlé, c’est comme écrire des infos sur des post-it partout.
Un formulaire contrôlé, c’est comme remplir une fiche unique bien structurée.

Résultat :

* moins de bugs
* plus facile à maintenir
* logique claire

---

## 2) Pattern recommandé : `form`, `errors`, `touched`, `isSubmitting`

Tu l’as déjà vu dans la leçon précédente, mais ici on le verrouille comme une norme.

Un formulaire “pro” en Alpine contient souvent :

* `form` : données utilisateur
* `errors` : messages d’erreurs par champ
* `touched` : champs déjà visités (UX)
* `isSubmitting` : blocage pendant envoi
* `submit()` : logique de soumission
* `reset()` : remise à zéro propre

---

## 3) Le piège numéro 1 : state incohérent

### Exemple classique (mauvais)

Tu reset les champs, mais tu oublies les erreurs :

* l’utilisateur voit encore une erreur rouge
* alors que le champ est vide “normalement”
* donc UX incompréhensible

Ou inversement :

* tu reset les erreurs
* mais tu laisses les champs touchés
* donc l’erreur revient immédiatement

Conclusion :

> Reset = reset de tout ce qui est lié au formulaire.

---

## 4) Le piège numéro 2 : validation dispersée dans le HTML

### Mauvais pattern

Tu fais ça partout :

```html
<button :disabled="name.trim() === '' || email.trim() === '' || accepted === false">
  Envoyer
</button>
```

Puis tu recopies cette condition :

* sur le bouton
* sur le message de statut
* sur une classe CSS
* sur une icône

Résultat :

* tu modifies une règle → tu dois modifier 4 endroits
* tu oublies un endroit → bug

### Pattern pro

Centraliser dans un getter :

```js
get isValid() {
  return ...
}
```

---

## 5) Le piège numéro 3 : “reset mal fait” (le bug fantôme)

Le bug fantôme, c’est quand ton formulaire semble reset…

…mais quelque chose reste en mémoire.

Exemples :

* la checkbox reste cochée
* le select reste sur “Pro”
* un message succès reste affiché
* un champ caché garde une valeur

Solution : reset complet et cohérent.

---

## 6) Pattern “FormFactory” : une base réutilisable (niveau pro)

Là, on va faire un exemple propre et réutilisable.

### Exemple : formulaire d’inscription (pro)

* username : min 3
* password : min 8
* accept : obligatoire

#### Code complet

```html
<form
  x-data="signupForm()"
  @submit.prevent="submit()"
  style="border: 1px solid #eee; padding: 16px; border-radius: 12px; max-width: 520px;"
>
  <h2 style="margin-top: 0;">Inscription</h2>

  <!-- Username -->
  <div style="margin-top: 12px;">
    <label style="display:block; font-weight: 600;">Username</label>
    <input
      type="text"
      x-model="form.username"
      @blur="touch('username')"
      placeholder="zyrass"
      :aria-invalid="hasError('username').toString()"
      style="width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #ddd;"
    />

    <p
      x-show="hasError('username')"
      x-text="errors.username"
      style="margin: 6px 0 0; color: #b00020;"
    ></p>
  </div>

  <!-- Password -->
  <div style="margin-top: 12px;">
    <label style="display:block; font-weight: 600;">Password</label>
    <input
      type="password"
      x-model="form.password"
      @blur="touch('password')"
      placeholder="********"
      :aria-invalid="hasError('password').toString()"
      style="width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #ddd;"
    />

    <p
      x-show="hasError('password')"
      x-text="errors.password"
      style="margin: 6px 0 0; color: #b00020;"
    ></p>
  </div>

  <!-- Accept -->
  <div style="margin-top: 12px;">
    <label style="display:flex; gap: 8px; align-items:center;">
      <input type="checkbox" x-model="form.accepted" @change="touch('accepted')" />
      J’accepte les conditions
    </label>

    <p
      x-show="hasError('accepted')"
      x-text="errors.accepted"
      style="margin: 6px 0 0; color: #b00020;"
    ></p>
  </div>

  <!-- Actions -->
  <div style="margin-top: 16px;">
    <button
      type="submit"
      :disabled="!isValid || isSubmitting"
      style="padding: 10px 14px; border-radius: 10px; border: 1px solid #ddd; background: #111; color: #fff; cursor: pointer;"
    >
      <span x-show="!isSubmitting">Créer le compte</span>
      <span x-show="isSubmitting" x-cloak>Création en cours...</span>
    </button>

    <button
      type="button"
      @click="reset()"
      :disabled="isSubmitting"
      style="margin-left: 8px; padding: 10px 14px; border-radius: 10px; border: 1px solid #ddd; background: #fff; cursor: pointer;"
    >
      Reset
    </button>
  </div>

  <!-- Feedback -->
  <p
    x-show="successMessage"
    x-text="successMessage"
    x-cloak
    style="margin-top: 12px; color: #0a7a2f; font-weight: 600;"
  ></p>

  <!-- Debug (optionnel pendant dev) -->
  <pre style="margin-top: 12px; background: #fafafa; padding: 12px; border-radius: 10px; border: 1px solid #eee;">
<form x-text="JSON.stringify(form, null, 2)"></form>
  </pre>
</form>

<script>
  function signupForm() {
    return {
      // State formulaire
      form: {
        username: "",
        password: "",
        accepted: false,
      },

      // Erreurs
      errors: {
        username: "",
        password: "",
        accepted: "",
      },

      // Champs touchés
      touched: {
        username: false,
        password: false,
        accepted: false,
      },

      // Soumission
      isSubmitting: false,

      // Feedback
      successMessage: "",

      // Validation globale
      get isValid() {
        return (
          this.form.username.trim().length >= 3 &&
          this.form.password.trim().length >= 8 &&
          this.form.accepted === true
        );
      },

      touch(field) {
        this.touched[field] = true;
        this.validateField(field);
      },

      hasError(field) {
        return this.touched[field] && this.errors[field].length > 0;
      },

      validateField(field) {
        const username = this.form.username.trim();
        const password = this.form.password.trim();

        if (field === "username") {
          if (username.length === 0) this.errors.username = "Le username est obligatoire.";
          else if (username.length < 3) this.errors.username = "Le username doit faire au moins 3 caractères.";
          else this.errors.username = "";
        }

        if (field === "password") {
          if (password.length === 0) this.errors.password = "Le mot de passe est obligatoire.";
          else if (password.length < 8) this.errors.password = "Le mot de passe doit faire au moins 8 caractères.";
          else this.errors.password = "";
        }

        if (field === "accepted") {
          if (this.form.accepted !== true) this.errors.accepted = "Tu dois accepter les conditions.";
          else this.errors.accepted = "";
        }
      },

      validateAll() {
        this.validateField("username");
        this.validateField("password");
        this.validateField("accepted");
      },

      async submit() {
        // 1) Marquer tout touché (affichage des erreurs)
        this.touched.username = true;
        this.touched.password = true;
        this.touched.accepted = true;

        // 2) Valider tout
        this.validateAll();

        // 3) Stop si invalide
        if (!this.isValid) return;

        // 4) Simuler envoi
        this.isSubmitting = true;
        this.successMessage = "";

        try {
          await new Promise((resolve) => setTimeout(resolve, 1000));

          this.successMessage = "Compte créé avec succès.";

          // Reset propre après succès
          this.reset();
        } finally {
          this.isSubmitting = false;
        }
      },

      reset() {
        // Reset données
        this.form.username = "";
        this.form.password = "";
        this.form.accepted = false;

        // Reset erreurs
        this.errors.username = "";
        this.errors.password = "";
        this.errors.accepted = "";

        // Reset touched
        this.touched.username = false;
        this.touched.password = false;
        this.touched.accepted = false;

        // Reset feedback
        this.successMessage = "";
      },
    };
  }
</script>
```

---

## 7) Pourquoi ce pattern est “contrôlé” et stable

* Le state `form` est la vérité.
* Les erreurs ne sont pas “magiques”, elles sont calculées.
* L’affichage des erreurs dépend de `touched` (UX).
* Le bouton dépend de `isValid` + `isSubmitting`.
* Le reset remet tout à zéro sans laisser de résidu.

C’est un composant fiable.

---

## 8) Les erreurs fréquentes (vraies erreurs de terrain)

### Erreur 1 — double source de vérité

Tu mets `x-model="email"` mais tu lis ensuite `$event.target.value` ailleurs.

Résultat : incohérence.

Règle :

> Si tu utilises `x-model`, tu utilises `x-model` partout.

---

### Erreur 2 — reset partiel

Tu reset le texte mais pas la checkbox.

C’est une des causes les plus fréquentes de bug UX.

---

### Erreur 3 — validation “trop tôt”

Tu affiches l’erreur dès que l’utilisateur tape une lettre.

Ça donne une UI agressive.

Bonne UX :

* erreur après blur
* erreur au submit

---

## Résumé de la leçon

Un formulaire contrôlé en Alpine, c’est :

* `form` (données)
* `errors` (messages)
* `touched` (UX)
* `isSubmitting` (anti double submit)
* `isValid` (validation centralisée)
* `submit()` et `reset()` (actions propres)

Ce pattern est réutilisable partout dans ta formation.

---

## Mini exercice (obligatoire)

Tu dois créer un formulaire “Connexion” :

* email obligatoire (format simple)
* password obligatoire (min 8)
* bouton disabled tant que invalide
* erreurs après blur et au submit
* loading 1 seconde
* reset propre

---

### Étape suivante logique

On a terminé le Chapitre 3.

Prochaine étape : **Atelier UI #2 — Todo list (version simple)**
Et là on va appliquer `x-model` + `@submit.prevent` + rendu dynamique (première version) avec une UX clean.
