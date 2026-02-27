---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 4

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Formulaires : submit propre et UX (validation simple côté front)

### Objectif de la leçon

À la fin, tu sauras :

* gérer un formulaire comme un composant sérieux (pas juste “ça envoie dans la console”)
* faire une validation simple mais propre
* afficher des erreurs compréhensibles pour l’utilisateur
* bloquer le submit tant que ce n’est pas valide
* gérer un état “envoi en cours” (loading)
* éviter les erreurs classiques : reset brutal, validation incohérente, UX frustrante

Cette leçon, c’est le passage “débutant → pro”.
Parce que 90% des formulaires cassés viennent d’une mauvaise UX.

---

## 1) La réalité : un formulaire n’est pas juste un input + bouton

Un formulaire “qui marche” techniquement, c’est facile.
Un formulaire “qui marche bien”, c’est une autre histoire.

Un bon formulaire doit :

* guider l’utilisateur
* empêcher les erreurs évidentes
* expliquer clairement ce qui ne va pas
* ne pas être agressif (pas d’erreurs rouges partout dès la première seconde)
* être cohérent (state + UI alignés)

---

## 2) Les 3 états d’un formulaire “pro”

Un formulaire sérieux a toujours ces 3 états :

### 1) État des données

* ce que l’utilisateur saisit (ex: `email`, `password`)

### 2) État de validation

* ce qui est valide / invalide (ex: `errors.email`)

### 3) État de soumission

* envoi en cours (ex: `isSubmitting`)

Ces 3 blocs doivent être séparés dans ta tête.

---

# 3) Validation simple : règles claires

On va faire un exemple réaliste : formulaire de contact.

Règles :

* nom obligatoire (min 2 caractères)
* email obligatoire + format basique
* message obligatoire (min 10 caractères)

Important : on ne fait pas une validation “parfaite”, on fait une validation utile.

---

## 4) Exemple complet (production mindset)

Ce code est conçu pour être compris par un étudiant, mais structuré comme un vrai composant.

```html
<form
  x-data="contactForm()"
  @submit.prevent="submit()"
  style="border: 1px solid #eee; padding: 16px; border-radius: 12px; max-width: 520px;"
>
  <h2 style="margin-top: 0;">Formulaire de contact</h2>

  <!-- Nom -->
  <div style="margin-top: 12px;">
    <label style="display:block; font-weight: 600;">
      Nom
    </label>

    <input
      type="text"
      x-model="form.name"
      @blur="touch('name')"
      placeholder="Jean Dupont"
      :aria-invalid="hasError('name').toString()"
      style="width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #ddd;"
    />

    <p
      x-show="hasError('name')"
      x-text="errors.name"
      style="margin: 6px 0 0; color: #b00020;"
    ></p>
  </div>

  <!-- Email -->
  <div style="margin-top: 12px;">
    <label style="display:block; font-weight: 600;">
      Email
    </label>

    <input
      type="email"
      x-model="form.email"
      @blur="touch('email')"
      placeholder="jean@mail.com"
      :aria-invalid="hasError('email').toString()"
      style="width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #ddd;"
    />

    <p
      x-show="hasError('email')"
      x-text="errors.email"
      style="margin: 6px 0 0; color: #b00020;"
    ></p>
  </div>

  <!-- Message -->
  <div style="margin-top: 12px;">
    <label style="display:block; font-weight: 600;">
      Message
    </label>

    <textarea
      x-model="form.message"
      @blur="touch('message')"
      placeholder="Explique ton besoin..."
      rows="4"
      :aria-invalid="hasError('message').toString()"
      style="width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #ddd;"
    ></textarea>

    <p
      x-show="hasError('message')"
      x-text="errors.message"
      style="margin: 6px 0 0; color: #b00020;"
    ></p>
  </div>

  <!-- Bouton -->
  <div style="margin-top: 16px;">
    <button
      type="submit"
      :disabled="!isValid || isSubmitting"
      style="padding: 10px 14px; border-radius: 10px; border: 1px solid #ddd; background: #111; color: #fff; cursor: pointer;"
    >
      <span x-show="!isSubmitting">Envoyer</span>
      <span x-show="isSubmitting" x-cloak>Envoi en cours...</span>
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

  <!-- Message succès -->
  <p
    x-show="successMessage"
    x-text="successMessage"
    x-cloak
    style="margin-top: 12px; color: #0a7a2f; font-weight: 600;"
  ></p>
</form>

<script>
  function contactForm() {
    return {
      // Données du formulaire
      form: {
        name: "",
        email: "",
        message: "",
      },

      // Erreurs par champ
      errors: {
        name: "",
        email: "",
        message: "",
      },

      // Champs "touchés" = l’utilisateur a interagi (blur)
      touched: {
        name: false,
        email: false,
        message: false,
      },

      // État d’envoi
      isSubmitting: false,

      // Feedback utilisateur
      successMessage: "",

      // Validation globale
      get isValid() {
        // Important : on valide sur les données actuelles
        // mais sans forcément afficher les erreurs tout de suite
        return (
          this.form.name.trim().length >= 2 &&
          this.isEmailValid(this.form.email) &&
          this.form.message.trim().length >= 10
        );
      },

      // Utilitaire email (simple, pas parfait)
      isEmailValid(value) {
        const email = value.trim();
        return email.includes("@") && email.includes(".");
      },

      // Marquer un champ comme touché
      touch(field) {
        this.touched[field] = true;
        this.validateField(field);
      },

      // Vérifier si un champ a une erreur affichable
      hasError(field) {
        return this.touched[field] && this.errors[field].length > 0;
      },

      // Validation par champ (messages clairs)
      validateField(field) {
        const name = this.form.name.trim();
        const email = this.form.email.trim();
        const message = this.form.message.trim();

        if (field === "name") {
          if (name.length === 0) this.errors.name = "Le nom est obligatoire.";
          else if (name.length < 2) this.errors.name = "Le nom doit faire au moins 2 caractères.";
          else this.errors.name = "";
        }

        if (field === "email") {
          if (email.length === 0) this.errors.email = "L’email est obligatoire.";
          else if (!this.isEmailValid(email)) this.errors.email = "L’email semble invalide.";
          else this.errors.email = "";
        }

        if (field === "message") {
          if (message.length === 0) this.errors.message = "Le message est obligatoire.";
          else if (message.length < 10) this.errors.message = "Le message doit faire au moins 10 caractères.";
          else this.errors.message = "";
        }
      },

      // Valider tout le formulaire (utile au submit)
      validateAll() {
        this.validateField("name");
        this.validateField("email");
        this.validateField("message");
      },

      // Submit (simulation)
      async submit() {
        // 1) marquer tous les champs comme touchés pour afficher les erreurs
        this.touched.name = true;
        this.touched.email = true;
        this.touched.message = true;

        // 2) valider tout
        this.validateAll();

        // 3) si invalide → stop
        if (!this.isValid) return;

        // 4) envoi en cours
        this.isSubmitting = true;
        this.successMessage = "";

        try {
          // Simulation d’un appel API
          await new Promise((resolve) => setTimeout(resolve, 1000));

          this.successMessage = "Message envoyé avec succès.";

          // Reset propre après succès
          this.reset();
        } finally {
          this.isSubmitting = false;
        }
      },

      reset() {
        this.form.name = "";
        this.form.email = "";
        this.form.message = "";

        this.errors.name = "";
        this.errors.email = "";
        this.errors.message = "";

        this.touched.name = false;
        this.touched.email = false;
        this.touched.message = false;
      },
    };
  }
</script>
```

---

## 5) Pourquoi cette structure est “pro”

### Point 1 — Erreurs affichées seulement après interaction (`touched`)

C’est un point UX majeur.

Si tu affiches “Nom obligatoire” dès que la page charge, c’est agressif et nul.

Ici :

* l’utilisateur touche le champ → on affiche l’erreur si besoin
* au submit → on affiche tout

C’est le comportement standard des formulaires modernes.

---

### Point 2 — `isSubmitting` empêche les doubles envois

Sans ça, l’utilisateur peut cliquer 10 fois.

Et dans un vrai backend, ça peut :

* créer 10 tickets
* créer 10 commandes
* spammer ton système

Donc `isSubmitting` est obligatoire en UI sérieuse.

---

### Point 3 — validation globale + validation par champ

* `isValid` sert à activer/désactiver le bouton
* `validateField` sert à afficher les messages

C’est plus propre que tout mélanger.

---

## 6) Pièges à éviter (très fréquents)

### Piège A — Reset brutal au mauvais moment

Si tu reset avant d’afficher le message, l’utilisateur croit que ça n’a pas marché.

Ici on affiche d’abord le succès, puis reset propre.

---

### Piège B — Validation trop stricte ou trop complexe

Pour un cours débutant, un regex email parfait est inutile.

On veut :

* comprendre le pattern
* pas faire une guerre de regex

---

### Piège C — Erreurs techniques incompréhensibles

Mauvais message :

* “invalid email format”

Bon message :

* “L’email semble invalide.”

Le but est d’aider l’utilisateur, pas de lui faire passer un entretien technique.

---

## 7) Résumé de la leçon

Tu sais maintenant faire un formulaire qui :

* ne reload pas (`@submit.prevent`)
* affiche des erreurs intelligemment (touched)
* bloque le submit si invalide
* gère un état loading (isSubmitting)
* reset proprement

C’est exactement le niveau attendu pour un projet réel.

---

## Mini exercice (obligatoire)

Crée un formulaire “Inscription” avec :

* username (min 3)
* password (min 8)
* checkbox “J’accepte”
* bouton submit désactivé tant que ce n’est pas valide
* erreurs affichées après blur et au submit
* état “Création en cours...” pendant 1 seconde (simulation)

---

Prochaine leçon : **Leçon 5 — Patterns pro : formulaire contrôlé (state cohérent, reset propre, erreurs fréquentes)**
Là on va voir les erreurs qui tuent 80% des formulaires et comment les corriger proprement.
