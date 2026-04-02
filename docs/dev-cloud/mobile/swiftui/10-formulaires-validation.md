---
description: "SwiftUI formulaires : Form, Section, TextField, Toggle, Picker, DatePicker, Stepper et validation en temps réel."
icon: lucide/book-open-check
tags: ["SWIFTUI", "FORM", "TEXTFIELD", "PICKER", "VALIDATION", "FORMULAIRES"]
---

# Formulaires & Validation

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Guichet et le Formulaire Papier"
    À la préfecture, un formulaire papier est rempli case par case. Mais si vous oubliez de cocher une case obligatoire, vous ne le saurez qu'au moment de le déposer. Un formulaire numérique bien conçu invalide une case dès qu'elle est incorrecte — en temps réel, avec un message clair. SwiftUI fournit les composants (`Form`, `TextField`, `Toggle`...) et vous, la logique de validation (`disabled`, messages d'erreur, couleurs). L'objectif : guider l'utilisateur, jamais le bloquer.

`Form` est le container spécialisé pour les formulaires iOS. Il adopte automatiquement l'apparence des Réglages système — styles natifs, regroupement en sections, claviers adaptés.

<br>

---

## `Form` & `Section` — La Structure de Base

```swift title="Swift (SwiftUI) — Form et Section : structure de formulaire iOS native"
import SwiftUI

struct FormulaireCompte: View {

    @State private var nom = ""
    @State private var email = ""
    @State private var mdp = ""
    @State private var mémoriser = true
    @State private var planSélectionné = "Gratuit"

    let plans = ["Gratuit", "Pro", "Entreprise"]

    var body: some View {
        NavigationStack {
            Form {
                // Section 1 : Identité
                Section {
                    TextField("Prénom et Nom", text: $nom)
                        .textContentType(.name)        // Aide la suggestion AutoFill
                        .autocorrectionDisabled()

                    TextField("Adresse email", text: $email)
                        .textContentType(.emailAddress) // Clavier email
                        .keyboardType(.emailAddress)
                        .textInputAutocapitalization(.never)

                    SecureField("Mot de passe", text: $mdp)
                        .textContentType(.newPassword)  // Suggestion de mot de passe fort

                } header: {
                    Text("Informations du compte")
                } footer: {
                    // Texte d'aide sous la section
                    Text("Votre email sera utilisé pour la connexion et les notifications importantes.")
                        .font(.caption)
                }

                // Section 2 : Préférences
                Section("Préférences") {
                    Toggle("Mémoriser le compte", isOn: $mémoriser)

                    Picker("Abonnement", selection: $planSélectionné) {
                        ForEach(plans, id: \.self) { plan in
                            Text(plan)
                        }
                    }
                }

                // Section 3 : Action
                Section {
                    Button("Créer mon compte") {
                        créerCompte()
                    }
                    .frame(maxWidth: .infinity)
                    .foregroundStyle(formulaireValide ? .white : .secondary)
                    .listRowBackground(
                        formulaireValide ? Color.indigo : Color.gray.opacity(0.3)
                    )
                    .disabled(!formulaireValide)
                }
            }
            .navigationTitle("Inscription")
            .navigationBarTitleDisplayMode(.large)
        }
    }

    // Validation globale
    var formulaireValide: Bool {
        !nom.isEmpty && emailValide && mdpValide
    }

    var emailValide: Bool {
        email.contains("@") && email.contains(".")
    }

    var mdpValide: Bool {
        mdp.count >= 8
    }

    func créerCompte() {
        print("Création du compte : \(nom) — \(email) — plan \(planSélectionné)")
    }
}

#Preview {
    FormulaireCompte()
}
```

*`Form` adopte automatiquement le style `insetGrouped` (sections arrondies). Dans une `NavigationStack`, il produit l'apparence exacte des Réglages iOS — familière pour l'utilisateur.*

<br>

---

## `TextField` — Toutes les Configurations

```swift title="Swift (SwiftUI) — TextField : configurations avancées"
import SwiftUI

struct DémoTextFields: View {

    @State private var prénom = ""
    @State private var montant = ""
    @State private var commentaire = ""
    @State private var recherche = ""
    @State private var axe: Axis = .vertical

    var body: some View {
        Form {
            Section("Saisie simple") {
                // TextField standard
                TextField("Prénom", text: $prénom)

                // Avec placeholder formaté
                TextField("Montant (€)", text: $montant)
                    .keyboardType(.decimalPad)  // Clavier numérique avec décimale

                // TextField avec label accessible (sf symbol)
                TextField("Rechercher", text: $recherche)
                    .overlay(alignment: .trailing) {
                        if !recherche.isEmpty {
                            Button {
                                recherche = ""
                            } label: {
                                Image(systemName: "xmark.circle.fill")
                                    .foregroundStyle(.secondary)
                            }
                            .padding(.trailing, 4)
                        }
                    }
            }

            Section("Saisie multiligne") {
                // TextField multilignes (iOS 16+)
                TextField("Votre commentaire...",
                          text: $commentaire,
                          axis: .vertical)  // Grandit verticalement
                    .lineLimit(3...6)        // Entre 3 et 6 lignes visibles
            }

            Section("Styles visuels") {
                // Style par défaut (Form)
                TextField("Style par défaut", text: $prénom)

                // Style bordé avec arrondi
                TextField("RoundedBorder", text: $prénom)
                    .textFieldStyle(.roundedBorder)
                    .padding(.vertical, 4)
            }
        }
        .navigationTitle("TextFields")
    }
}
```

<br>

---

## `Picker` — Sélection parmi des Options

```swift title="Swift (SwiftUI) — Picker : tous les styles"
import SwiftUI

struct DémoPickers: View {

    @State private var langueSélectionnée = "Français"
    @State private var niveauSélectionné = 2
    @State private var couleurSélectionnée = "Indigo"

    let langues = ["Français", "English", "Español", "Deutsch"]
    let niveaux = ["Débutant", "Intermédiaire", "Avancé", "Expert"]
    let couleurs = ["Indigo", "Orange", "Menthe", "Corail"]

    var body: some View {
        Form {
            Section("Dans Form — styles courants") {
                // Style par défaut dans Form : navigation vers liste de choix
                Picker("Langue", selection: $langueSélectionnée) {
                    ForEach(langues, id: \.self) { Text($0) }
                }

                // Inline : options directement dans la section
                Picker("Niveau", selection: $niveauSélectionné) {
                    ForEach(Array(niveaux.enumerated()), id: \.offset) { index, niveau in
                        Text(niveau).tag(index)
                    }
                }
                .pickerStyle(.inline)
            }

            Section("Styles spécifiques") {
                // Segmented : onglets horizontaux
                Picker("Couleur", selection: $couleurSélectionnée) {
                    ForEach(couleurs, id: \.self) { Text($0) }
                }
                .pickerStyle(.segmented)

                // Menu : bouton + menu déroulant
                Picker("Langue via menu", selection: $langueSélectionnée) {
                    ForEach(langues, id: \.self) { Text($0) }
                }
                .pickerStyle(.menu)
            }
        }
    }
}
```

<br>

---

## `DatePicker`, `Toggle`, `Stepper`, `Slider`

```swift title="Swift (SwiftUI) — Les contrôles de saisie spécialisés"
import SwiftUI

struct DémoControles: View {

    @State private var dateNaissance = Date.now
    @State private var notificationsActives = true
    @State private var quantité = 1
    @State private var volume: Double = 0.7

    var body: some View {
        Form {
            Section("Date et Heure") {
                // DatePicker compact (bouton → calendrier pop-over)
                DatePicker("Date de naissance",
                           selection: $dateNaissance,
                           displayedComponents: .date)  // .date seulement, pas l'heure

                // DatePicker graphique — calendrier complet dans la vue
                DatePicker("Sélectionner",
                           selection: $dateNaissance,
                           in: .distantPast...Date.now,  // Plage de dates autorisée
                           displayedComponents: .date)
                .datePickerStyle(.graphical)
            }

            Section("Booléens et Quantités") {
                Toggle("Notifications", isOn: $notificationsActives)
                    .tint(.indigo)  // Couleur du toggle actif

                Stepper("Quantité : \(quantité)",
                        value: $quantité,
                        in: 1...10)  // Plage 1 à 10

                VStack(alignment: .leading) {
                    Text("Volume : \(Int(volume * 100))%")
                    Slider(value: $volume, in: 0...1, step: 0.05)
                        .tint(.indigo)
                }
            }
        }
    }
}
```

<br>

---

## Validation en Temps Réel

```swift title="Swift (SwiftUI) — Validation progressive avec feedback visuel"
import SwiftUI

struct FormulaireInscriptionComplet: View {

    @State private var prénom = ""
    @State private var email = ""
    @State private var mdp = ""
    @State private var mdpConfirmation = ""

    // États de validation (affichés après première interaction)
    @State private var prénomTouché = false
    @State private var emailTouché = false
    @State private var mdpTouché = false

    // Règles de validation
    var erreurPrénom: String? {
        guard prénomTouché else { return nil }
        if prénom.isEmpty { return "Le prénom est requis" }
        if prénom.count < 2 { return "Minimum 2 caractères" }
        return nil
    }

    var erreurEmail: String? {
        guard emailTouché else { return nil }
        if email.isEmpty { return "L'email est requis" }
        if !email.contains("@") || !email.contains(".") { return "Format email invalide" }
        return nil
    }

    var erreurMdp: String? {
        guard mdpTouché else { return nil }
        if mdp.count < 8 { return "Minimum 8 caractères" }
        if !mdp.contains(where: { $0.isNumber }) { return "Au moins un chiffre requis" }
        return nil
    }

    var mdpConfirmÉgal: Bool { mdp == mdpConfirmation && !mdp.isEmpty }

    var formulaireValide: Bool {
        erreurPrénom == nil && erreurEmail == nil && erreurMdp == nil
        && mdpConfirmÉgal && prénomTouché && emailTouché && mdpTouché
    }

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    // TextField avec feedback de validation
                    ChampValidé(
                        valeur: $prénom,
                        touché: $prénomTouché,
                        placeholder: "Prénom",
                        erreur: erreurPrénom
                    )
                    .textContentType(.givenName)

                    ChampValidé(
                        valeur: $email,
                        touché: $emailTouché,
                        placeholder: "Email",
                        erreur: erreurEmail
                    )
                    .keyboardType(.emailAddress)
                    .textInputAutocapitalization(.never)

                } header: { Text("Identité") }

                Section {
                    ChampValidé(
                        valeur: $mdp,
                        touché: $mdpTouché,
                        placeholder: "Mot de passe",
                        erreur: erreurMdp,
                        sécurisé: true
                    )

                    // Confirmation avec indicateur visuel
                    HStack {
                        SecureField("Confirmer le mot de passe", text: $mdpConfirmation)
                        if !mdpConfirmation.isEmpty {
                            Image(systemName: mdpConfirmÉgal ? "checkmark.circle.fill" : "xmark.circle.fill")
                                .foregroundStyle(mdpConfirmÉgal ? .green : .red)
                        }
                    }

                } header: { Text("Sécurité") }
                  footer: { Text("Le mot de passe doit contenir au moins 8 caractères et un chiffre.") }

                Section {
                    Button("Créer le compte") {
                        // Action de soumission
                    }
                    .frame(maxWidth: .infinity)
                    .disabled(!formulaireValide)
                    .listRowBackground(formulaireValide ? Color.indigo : Color.gray.opacity(0.3))
                    .foregroundStyle(formulaireValide ? .white : .secondary)
                    .fontWeight(.semibold)
                }
            }
            .navigationTitle("Inscription")
        }
    }
}

// Composant réutilisable de champ validé
struct ChampValidé: View {
    @Binding var valeur: String
    @Binding var touché: Bool
    let placeholder: String
    let erreur: String?
    var sécurisé: Bool = false

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            if sécurisé {
                SecureField(placeholder, text: $valeur)
                    .onChange(of: valeur) { _, _ in touché = true }
            } else {
                TextField(placeholder, text: $valeur)
                    .onChange(of: valeur) { _, _ in touché = true }
            }

            // Message d'erreur animé
            if let erreur = erreur {
                Text(erreur)
                    .font(.caption)
                    .foregroundStyle(.red)
                    .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
        .animation(.easeInOut(duration: 0.2), value: erreur)
    }
}
```

*`.onChange(of:)` déclenche `touché = true` dès le premier caractère saisi — la validation s'affiche uniquement après interaction, pas dès l'ouverture du formulaire.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Formulaire de réservation**

```swift title="Swift — Exercice 1 : formulaire de réservation de restaurant"
// Créez un formulaire de réservation avec :
// - Nom du réservateur (requis, min 2 caractères)
// - Nombre de couverts (Stepper, 1 à 20)
// - Date et heure (DatePicker — plage : maintenant + 7 jours)
// - Zone fumeur/non-fumeur (Picker segmented)
// - Demandes spéciales (TextField multilignes, optionnel)
// - Bouton "Réserver" désactivé si validation échoue

struct FormulaireResto: View {
    // TODO
    var body: some View { EmptyView() }
}
```

**Exercice 2 — Validation de mot de passe avancée**

```swift title="Swift — Exercice 2 : indicateur de force de mot de passe"
// Créez un IndicateurForce qui affiche une barre colorée :
// - Rouge : moins de 6 caractères
// - Orange : 6-8 caractères OU pas de chiffre
// - Vert : 8+ caractères ET au moins un chiffre ET une majuscule

struct IndicateurForce: View {
    let mdp: String

    var force: Int {
        // 0: faible, 1: moyen, 2: fort
        // TODO : calculer selon les critères
        return 0
    }

    var body: some View {
        // TODO : barre de couleur avec GeometryReader
    }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `Form` est le container standard pour les formulaires iOS — il adopte l'apparence native des Réglages système. `Section` organise les champs en groupes logiques avec des en-têtes et pieds explicatifs. Les modifications de champs sont liées via `$binding` : `TextField(placeholder, text: $valeur)`. La validation en temps réel utilise des computed properties qui examinent l'état courant — le bouton de soumission est désactivé via `.disabled(!formulaireValide)`. La bonne pratique : ne montrer les erreurs qu'après interaction (état `touché`) pour ne pas perturber l'utilisateur dès l'ouverture.

> Dans le module suivant, nous découvrons les **Animations & Transitions** — `withAnimation`, `Animation.spring()`, `.transition()` et `matchedGeometryEffect` pour des interfaces vivantes et expressives.

<br>
