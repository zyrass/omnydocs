---
description: "La pyramide des tests — comprendre les niveaux, la répartition recommandée et l'antipattern du cône de glace."
icon: lucide/triangle
tags: ["TESTS", "PYRAMIDE", "STRATEGIE", "TDD", "E2E", "UNITAIRES"]
---

# La Pyramide des Tests

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="2024"
  data-time="30 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Pyramide de Khéops"
    La pyramide de Khéops est stable parce que sa base est large et son sommet étroit. Si vous inversez la pyramide, elle s'effondre. La pyramide des tests suit le même principe : une large base de tests unitaires (rapides, nombreux, peu coûteux) supporte quelques tests d'intégration, qui supportent un petit nombre de tests E2E (lents, coûteux, fragiles). Inverser la pyramide — beaucoup de tests E2E, peu de tests unitaires — est l'antipattern du "cône de glace".

<br>

---

## 1. Les Trois Niveaux

```
                    ╔═══════╗
                    ║  E2E  ║  ← Peu (5–10 %)
                   ╔╩═══════╩╗    Coûteux, lents, fragiles
                   ║Intégrat.║ ← Moyennement (20–30 %)
                  ╔╩═════════╩╗   Services, BDD, API
                  ║  Unitaire ║ ← Majorité (60–70 %)
                  ╚═══════════╝   Rapides, nombreux, fiables
```

| Niveau | Quoi tester | Outils | Vitesse | Coût |
|---|---|---|---|---|
| **Unitaire** | Une fonction, une classe isolée | Jest, Vitest, PHPUnit, Pest | ⚡ ms | 💚 Bas |
| **Intégration** | Plusieurs modules ensemble (BDD, API) | Jest + Supertest, PHPUnit | 🟡 secondes | 🟡 Moyen |
| **E2E** | L'application entière du point de vue utilisateur | Cypress, Playwright | 🔴 minutes | 🔴 Élevé |

<br>

---

## 2. Tests Unitaires — La Base

**Objectif :** vérifier qu'une unité de code (fonction, méthode, classe) produit le résultat attendu **de façon isolée** des dépendances extérieures.

**Caractéristiques :**
- Rapides (< 1 ms par test)
- Indépendants (pas de BDD, pas de réseau)
- Déterministes (même résultat à chaque exécution)
- Les dépendances sont **mockées**

```javascript title="JavaScript — Test unitaire : vérifier une fonction en isolation"
// Fonction à tester
function calculateTax(amount, rate) {
    if (amount < 0) throw new Error("Montant invalide");
    return Math.round(amount * rate * 100) / 100;
}

// Test unitaire — aucune dépendance externe
test('calcule la TVA correctement', () => {
    expect(calculateTax(100, 0.20)).toBe(20);
    expect(calculateTax(33.33, 0.20)).toBe(6.67);
});

test('lève une erreur pour un montant négatif', () => {
    expect(() => calculateTax(-10, 0.20)).toThrow('Montant invalide');
});
```

<br>

---

## 3. Tests d'Intégration — Le Milieu

**Objectif :** vérifier que plusieurs composants fonctionnent **ensemble** correctement (ex: service + base de données, contrôleur + modèle).

**Caractéristiques :**
- Plus lents que les unitaires (BDD en mémoire ou de test)
- Détectent les problèmes de contrat entre composants
- N'utilisent pas forcément une BDD de production

```php title="PHP — Test d'intégration Laravel (Feature Test) avec BDD de test"
// tests/Feature/ArticleTest.php
class ArticleTest extends TestCase
{
    use RefreshDatabase;  // BDD de test fraîche à chaque test

    public function test_can_create_an_article(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->postJson('/api/articles', [
            'title'   => 'Mon Article',
            'content' => 'Contenu de test...',
        ]);

        $response->assertStatus(201);
        $this->assertDatabaseHas('articles', ['title' => 'Mon Article']);
    }
}
```

<br>

---

## 4. Tests E2E — Le Sommet

**Objectif :** simuler un **utilisateur réel** interagissant avec l'application complète (navigateur, frontend + backend + BDD).

**Caractéristiques :**
- Lents (secondes à minutes par test)
- Fragiles (sensibles aux changements d'UI)
- Haute valeur : valident les parcours critiques
- À réserver aux **happy paths** essentiels (connexion, achat, publication)

```javascript title="JavaScript — Test E2E Cypress : parcours de connexion complet"
// cypress/e2e/auth/login.cy.js
it('se connecte et accède au tableau de bord', () => {
    cy.visit('/login');
    cy.get('[data-cy="email"]').type('alice@example.com');
    cy.get('[data-cy="password"]').type('AlicePass123!');
    cy.get('[data-cy="submit"]').click();
    cy.url().should('include', '/dashboard');
    cy.get('[data-cy="welcome"]').should('contain.text', 'Alice');
});
```

<br>

---

## 5. L'Antipattern — Le Cône de Glace

!!! warning "Le cône de glace : à éviter absolument"
    Le cône de glace (ice cream cone) est l'inverse de la pyramide : beaucoup de tests E2E manuels, peu de tests unitaires automatiques. Résultat : suite de tests lente, fragile, coûteuse à maintenir. Chaque déploiement prend des heures. Les développeurs évitent de lancer les tests.

```
Antipattern — Cône de glace :
    ╔═════════════════╗
    ║ Tests manuels   ║  ← Nombreux (et oubliés)
   ╔╩═════════════════╩╗
   ║    Tests E2E      ║  ← Trop nombreux, trop lents
  ╔╩═══════════════════╩╗
  ║   Tests unitaires   ║  ← Trop peu
  ╚═════════════════════╝
```

**Règle d'or : si un test unitaire peut le valider, pas besoin d'un test E2E.**

<br>

---

## 6. Répartition Recommandée

| Niveau | Proportion | Exemple (100 tests) |
|---|---|---|
| Unitaires | 60–70 % | 65 tests |
| Intégration | 20–30 % | 25 tests |
| E2E | 5–10 % | 10 tests |

!!! tip "Règle pragmatique"
    Commencez par des tests unitaires sur la **logique métier critique**. Ajoutez des tests d'intégration sur les **endpoints API**. Réservez les tests E2E aux **3–5 parcours utilisateurs les plus importants** (connexion, achat, inscription).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La pyramide des tests n'est pas un dogme mais un **guide de proportions**. Plus un test est haut dans la pyramide, plus il est lent, coûteux et fragile — mais plus il donne confiance sur le comportement global. La base (unitaires) assure la solidité de chaque brique ; le sommet (E2E) valide que l'assemblage final fonctionne pour l'utilisateur.

<br>