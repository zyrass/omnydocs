---
description: "Fuzzing & Mutation Testing — Générer des entrées aléatoires pour découvrir les bugs et mesurer la qualité des tests avec Infection PHP."
icon: lucide/book-open-check
tags: ["FUZZING", "MUTATION", "INFECTION", "TESTING", "QUALITE", "PHP"]
---

# Fuzzing & Mutation Testing

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="2024"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Crash Test et le Testeur de Résistance"
    Un crash test envoie la voiture dans un mur avec des mannequins — pour découvrir les points de rupture. Le fuzzing fait pareil avec votre code : il envoie des milliers d'entrées aberrantes, aléatoires, malformées — chaînes de 10 000 caractères, nombres négatifs géants, emojis, caractères nuls, payloads JSON corrompus — pour trouver les comportements inattendus que personne n'aurait pensé à tester. Le mutation testing, lui, est le testeur de résistance de votre suite de tests : il modifie votre code pour vérifier si vos tests sont assez forts pour détecter les mutations.

**Fuzzing** = générer des entrées aléatoires pour découvrir des bugs inattendus.  
**Mutation Testing** = introduire des mutations dans le code pour mesurer si les tests les détectent.

<br>

---

## PARTIE 1 — Fuzzing

## 1. Concept du Fuzzing

Le fuzzing génère automatiquement des milliers de combinaisons d'entrées pour trouver :

- **Crashs** — exceptions non gérées, erreurs fatales
- **Comportements inattendus** — résultats incohérents selon l'entrée
- **Failles de sécurité** — injections, buffer overflows (en C), path traversal
- **Régressions** — comportements différents entre deux versions

```
Types d'entrées que le fuzzer génère :
┌──────────────────────────────────────────────────────────────────┐
│ Chaînes extrêmes  : "", "A"×100000, null bytes, "\x00\xFF\xFF"  │
│ Nombres limites   : PHP_INT_MAX, -1, 0, PHP_FLOAT_EPSILON        │
│ Formats cassés    : JSON invalide, XML malformé, dates absurdes  │
│ Injections        : <script>, ' OR 1=1, ../../../etc/passwd      │
│ Encodages         : UTF-8 cassé, emoji, RTL characters           │
│ Types inattendus  : array au lieu de string, objet au lieu d'int │
└──────────────────────────────────────────────────────────────────┘
```

<br>

---

## 2. Fuzzing PHP avec php-fuzzer

```bash title="Bash — Installer php-fuzzer"
composer require --dev nikic/php-fuzzer
```

```php title="PHP — Créer un fuzzing target"
<?php

// fuzz/FuzzEmailParser.php

/**
 * Fonction cible du fuzzer.
 * Le fuzzer appelle cette fonction avec des entrées aléatoires.
 * Si elle throw une exception inattendue → bug détecté.
 */
function fuzzEmailParser(string $input): void
{
    // On fuzz le parseur d'email de notre application
    $parser = new EmailParser();

    // La fonction NE DOIT PAS :
    // - Lancer une erreur fatale
    // - Causer une boucle infinie
    // - Retourner des résultats incohérents
    try {
        $result = $parser->parse($input);

        // Invariants à vérifier :
        if ($result !== null) {
            assert(str_contains($result['email'], '@'), 'Email invalide retourné');
            assert(strlen($result['domain']) > 0, 'Domaine vide');
        }
    } catch (InvalidEmailException $e) {
        // Exception attendue pour une entrée invalide → OK
        return;
    }
    // Toute autre exception → bug détecté par le fuzzer
}
```

```bash title="Bash — Lancer le fuzzer"
# Fuzzing de base
./vendor/bin/php-fuzzer fuzz fuzz/FuzzEmailParser.php

# Avec corpus de départ (entrées initiales connues)
mkdir -p fuzz/corpus
echo -n "alice@example.com" > fuzz/corpus/valid1
echo -n "invalid-email"     > fuzz/corpus/invalid1
./vendor/bin/php-fuzzer fuzz fuzz/FuzzEmailParser.php --corpus=fuzz/corpus

# Minimiser un crash trouvé (trouver l'entrée minimale qui bug)
./vendor/bin/php-fuzzer minimize fuzz/crash-xyz.php fuzz/FuzzEmailParser.php
```

<br>

---

## 3. Fuzzing Manuel avec Property-Based Testing

Le **property-based testing** est une forme structurée de fuzzing : on définit des **propriétés** qui doivent toujours être vraies, et le framework génère automatiquement des exemples pour les tester.

```php title="PHP — Property-Based Testing avec Pest et des générateurs"
<?php

use Tests\Generators\EmailGenerator;

// Pest + dataset dynamique = property-based testing simplifié
dataset('random_strings', function () {
    return array_map(fn () => [
        fake()->regexify('[A-Za-z0-9\.\-\_\@]{1,200}')
    ], range(1, 100));
});

// La propriété : notre parseur ne doit JAMAIS crasher
it('never crashes on any string input', function (string $input) {
    expect(fn () => (new EmailParser())->parse($input))
        ->not->toThrow(Error::class)     // Pas d'erreur fatale
        ->not->toThrow(TypeError::class); // Pas d'erreur de type
})->with('random_strings');

// La propriété : encoder puis décoder = identité
it('encode/decode is idempotent for any valid input', function (string $input) {
    $encoder = new Base64UrlEncoder();

    $encoded = $encoder->encode($input);
    $decoded = $encoder->decode($encoded);

    expect($decoded)->toBe($input); // Toujours égal, quelle que soit l'entrée
})->with([
    [''],
    ['a'],
    ['Hello World'],
    [str_repeat('x', 10000)],
    ['🎉🚀💡'],
    ["\x00\xFF\xFE"],
    ["'; DROP TABLE users; --"],
]);
```

<br>

---

## PARTIE 2 — Mutation Testing

## 4. Concept du Mutation Testing

Le mutation testing **modifie intentionnellement votre code** (introduit des "mutations") et vérifie que vos tests détectent ces mutations.

```
Mutations typiques :
┌──────────────────────────────────────────────────────────────────┐
│ Arithmétique : + → -, * → /, % → *                              │
│ Comparaison  : > → >=, === → !==, == → !=                       │
│ Logique      : && → ||, ! → rien                                 │
│ Affectation  : ++ → --, += → -=                                  │
│ Retour       : return true → return false                         │
│ Condition    : if (x) → if (!x) → if (true)                     │
└──────────────────────────────────────────────────────────────────┘

Si vos tests passent malgré la mutation → "mutant survivant" → test insuffisant.
Si vos tests échouent à cause de la mutation → "mutant tué" → test efficace.
```

**Mutation Score = Mutants tués / Total mutants × 100**

<br>

---

## 5. Infection — Mutation Testing PHP

**Infection** est l'outil de référence pour le mutation testing PHP.

```bash title="Bash — Installer et configurer Infection"
composer require --dev infection/infection

# Initialiser la configuration
./vendor/bin/infection --init
```

```json title="JSON — infection.json : configuration"
{
    "$schema": "vendor/infection/infection/resources/schema.json",
    "source": {
        "directories": ["app/Services"],  // Code à muter
        "excludes": []
    },
    "mutators": {
        "@default": true               // Tous les mutateurs par défaut
    },
    "testFramework": "phpunit",        // ou pest
    "testFrameworkOptions": "",
    "timeout": 10,
    "minMsi": 75,                      // Minimum Mutation Score Index
    "minCoveredMsi": 90,               // MSI sur le code couvert
    "logs": {
        "text": "infection-log.txt",
        "html": "infection-report.html",
        "summary": "infection-summary.log"
    }
}
```

```bash title="Bash — Lancer Infection"
# Analyse complète
./vendor/bin/infection

# Avec affichage détaillé
./vendor/bin/infection --show-mutations

# Seulement sur les fichiers modifiés (Git diff)
./vendor/bin/infection --git-diff-filter=AM

# Parallélisé (plus rapide)
./vendor/bin/infection --threads=4

# Exiger un score minimum (fail si < 75%)
./vendor/bin/infection --min-msi=75 --min-covered-msi=90
```

### Lire le Rapport Infection

```
Infection - PHP Mutation Testing Framework

Processing source code files: 5
Creating mutants: 187

. Killed    (test détecté la mutation)
F Escaped   (test n'a pas détecté la mutation ← problème)
S Skipped   (couverture insuffisante)
E Error     (erreur de compilation)

...KKK.F.KKK.S.KKKK.F.KKK...

Results:
Mutations:       187
Killed:          162 (86.6%)  ← MSI
Escaped:          18 (9.6%)   ← À examiner !
Errors:            3
Skipped:           4

Metrics:
Mutation Score Indicator (MSI): 86.6%
Mutation Code Coverage: 94.2%
Covered Code MSI: 91.9%
```

<br>

---

## 6. Corriger les Mutants Survivants

```php title="PHP — Exemple : mutant survivant détecté et corrigé"
<?php
// ─── Code d'origine ───────────────────────────────────────────────────────────
class Discount
{
    public function apply(float $price, int $percent): float
    {
        return $price - ($price * $percent / 100);
    }
}

// ─── Mutant que Infection a introduit ─────────────────────────────────────────
// Infection a changé - en + :
// return $price + ($price * $percent / 100);  ← Le test n'a pas détecté !

// ─── Cause : le test ne vérifie pas la logique de soustraction ──────────────
public function test_apply_discount(): void
{
    $discount = new Discount();
    $result   = $discount->apply(100, 20);
    $this->assertNotNull($result);  // ❌ Test trop laxiste — passe avec + ou -
}

// ─── Fix : ajouter une assertion précise ─────────────────────────────────────
public function test_apply_discount(): void
{
    $discount = new Discount();

    $this->assertEquals(80.00, $discount->apply(100, 20));    // ✅ Valeur exacte
    $this->assertEquals(50.00, $discount->apply(100, 50));    // ✅ Cas limite
    $this->assertEquals(100.00, $discount->apply(100, 0));    // ✅ Réduction nulle
    $this->assertEquals(0.00, $discount->apply(100, 100));    // ✅ Réduction totale
}
// Maintenant Infection tue tous ces mutants.
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Property-Based Testing**

```php title="PHP — Exercice 1 : décrire des propriétés pour un FormatteurMonnaie"
// Implémentez un CurrencyFormatter qui formate les montants en €.
// Définissez et testez ces propriétés avec Pest :
// 1. Le résultat contient toujours "€"
// 2. Un montant négatif produit un résultat avec "-"
// 3. formatter->format(a) + formatter->format(b) produit le même texte que format(a+b)
// 4. Le formatage ne lance jamais d'exception pour n'importe quel float valide
// 5. Tester avec : 0, -0.01, PHP_INT_MAX, PHP_FLOAT_EPSILON, NaN, INF
```

**Exercice 2 — Infection sur un Service**

```bash title="Bash — Exercice 2 : analyser et améliorer le score Infection"
# 1. Installer Infection sur votre projet
# 2. Lancer Infection sur app/Services/ uniquement :
./vendor/bin/infection --filter=Services

# 3. Trouver 3 mutants "Escaped"
# 4. Pour chacun, comprendre pourquoi le test ne détectait pas la mutation
# 5. Ajouter les assertions manquantes pour tuer ces mutants
# 6. Relancer Infection — MSI doit avoir augmenté

# Objectif : MSI >= 80% sur app/Services/
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le **fuzzing** découvre des bugs que personne n'imaginerait tester manuellement : entrées extrêmes, malformées, aux limites du système. Il est particulièrement efficace sur les parseurs, les validators, les APIs publiques. Le **mutation testing** (Infection) répond à la question que le coverage ignore : "Mes tests sont-ils *assez précis* pour détecter une régression ?" Un MSI de **80%+** est un objectif raisonnable. La combinaison Coverage + Mutation Score donne une image fiable de la robustesse de votre suite de tests. Ces deux techniques sont avancées — elles s'appliquent en priorité sur le code métier critique.

> **P6 complet** — La section Tests & Qualité dispose maintenant de 5 modules thématiques complets en plus des formations PHPUnit et Pest.

<br>