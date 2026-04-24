---
description: "Jest — React Testing Library : Tester des composants React en se concentrant sur le comportement utilisateur et l'accessibilité."
icon: lucide/book-open-check
tags: ["JEST", "REACT", "TESTING LIBRARY", "FRONTEND", "JAVASCRIPT"]
---

# 03 — React Testing Library

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Jest 29.x / RTL 14.x"
  data-time="~3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    Si vous testez une télévision, vous n'ouvrez pas le capot pour vérifier que le condensateur C4 reçoit 5 volts. Vous prenez la télécommande, vous appuyez sur "Volume +" et vous vérifiez que le son augmente. React Testing Library fait exactement ça : il vous force à tester vos composants **comme un utilisateur les utilise**, et non via leur implémentation interne (state, méthodes de classe).

Créée par Kent C. Dodds, **React Testing Library (RTL)** a remplacé Enzyme comme standard industriel pour tester des composants React. Sa philosophie tient en une phrase : *« Plus vos tests ressemblent à la façon dont votre logiciel est utilisé, plus ils vous donneront confiance »*.

RTL fonctionne conjointement avec Jest : RTL monte (render) le composant en mémoire (jsdom) et fournit des méthodes pour interagir avec, puis Jest vérifie les résultats avec ses assertions `expect()`.

---

## 1. Installation

RTL est généralement inclus par défaut dans `create-react-app` ou les templates Vite modernes. Sinon :

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

**Configuration (`jest-setup.js`) :**

Pour avoir les "custom matchers" spécifiques au DOM (`toBeInTheDocument`, `toHaveClass`, etc.) :

```javascript title="jest-setup.js"
import '@testing-library/jest-dom'
```

---

## 2. Principes Fondamentaux : Les Sélecteurs (Queries)

Pour simuler un utilisateur, RTL refuse que vous sélectionniez par classe CSS (ex: `.btn-primary`) ou par composant interne. L'utilisateur ne voit pas les classes CSS, il voit du texte, des labels et des rôles d'accessibilité.

### L'ordre de priorité des Queries

1. **`getByRole`** : (Favori absolu) Sélectionne par rôle sémantique (button, heading, textbox). Parfait pour l'accessibilité.
2. **`getByLabelText`** : Pour les champs de formulaire.
3. **`getByPlaceholderText`** : Si pas de label.
4. **`getByText`** : Pour les paragraphes, spans.
5. **`getByTestId`** : (Dernier recours) Quand rien d'autre ne marche, utilise l'attribut `data-testid`.

### Variantes : get vs query vs find

- **`getBy...`** : Renvoie l'élément. Échoue *immédiatement* si l'élément n'est pas trouvé. Utile pour les assertions de base.
- **`queryBy...`** : Renvoie l'élément ou `null` s'il n'existe pas. Utile pour vérifier qu'un élément **n'est pas** dans le DOM (`expect(...).toBeNull()`).
- **`findBy...`** : Renvoie une **Promise**. Échoue au bout d'un timeout (1000ms) si non trouvé. Indispensable pour tester l'affichage après une action asynchrone (ex: fetch API).

---

## 3. Exemple Complet : Formulaire de Login

Voici un composant React classique qui fait un appel réseau.

```jsx title="Login.jsx"
import { useState } from 'react'

export default function Login({ onSubmit }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      await onSubmit(e.target.email.value, e.target.password.value)
    } catch (err) {
      setError('Identifiants invalides')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1>Connexion</h1>
      
      {error && <div role="alert">{error}</div>}
      
      <label htmlFor="email">Adresse Email</label>
      <input id="email" type="email" required />
      
      <label htmlFor="password">Mot de passe</label>
      <input id="password" type="password" required />
      
      <button type="submit" disabled={loading}>
        {loading ? 'Chargement...' : 'Se connecter'}
      </button>
    </form>
  )
}
```

### Le test associé avec RTL & user-event

On utilise `@testing-library/user-event` au lieu de `fireEvent` car il simule beaucoup plus fidèlement la vraie interaction du navigateur (focus, frappe clavier réelle).

```jsx title="Login.test.jsx"
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Login from './Login'

describe('Composant <Login />', () => {

  it('affiche le formulaire correctement', () => {
    render(<Login onSubmit={jest.fn()} />)
    
    // Vérifier par les rôles d'accessibilité (bonne pratique)
    expect(screen.getByRole('heading', { name: /connexion/i })).toBeInTheDocument()
    expect(screen.getByLabelText(/adresse email/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /se connecter/i })).toBeInTheDocument()
  })

  it('appelle onSubmit avec les bonnes données et gère le chargement', async () => {
    const mockSubmit = jest.fn().mockResolvedValue('Success')
    const user = userEvent.setup() // Toujours setup() au début du test
    
    render(<Login onSubmit={mockSubmit} />)
    
    // 1. L'utilisateur remplit les champs
    await user.type(screen.getByLabelText(/adresse email/i), 'test@omnyvia.com')
    await user.type(screen.getByLabelText(/mot de passe/i), 'azerty123')
    
    // 2. L'utilisateur clique sur submit
    const button = screen.getByRole('button', { name: /se connecter/i })
    await user.click(button)
    
    // 3. Vérifications (Assertions)
    expect(mockSubmit).toHaveBeenCalledWith('test@omnyvia.com', 'azerty123')
    
    // Vérifier que le bouton affiche le chargement (asynchrone)
    expect(screen.getByRole('button', { name: /chargement/i })).toBeDisabled()
  })

  it('affiche un message d\'erreur si la connexion échoue', async () => {
    const mockSubmit = jest.fn().mockRejectedValue(new Error('Failed'))
    const user = userEvent.setup()
    
    render(<Login onSubmit={mockSubmit} />)
    
    await user.type(screen.getByLabelText(/adresse email/i), 'wrong@email.com')
    await user.type(screen.getByLabelText(/mot de passe/i), 'wrong')
    await user.click(screen.getByRole('button', { name: /se connecter/i }))
    
    // Utiliser findBy pour attendre asynchroniquement l'apparition de l'erreur
    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('Identifiants invalides')
  })
})
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Ne testez **jamais** l'état interne (`useState`) de vos composants React. Testez les effets observables par l'utilisateur final. Si l'utilisateur clique sur un bouton, que voit-il ensuite ? RTL est l'outil parfait pour cela. De plus, forcer l'usage de `getByRole` ou `getByLabelText` améliorera mécaniquement l'accessibilité HTML (a11y) de votre application React, car un test ne passera pas si votre bouton est une simple `<div>` sans rôle.

<br>
