---
description: "Maîtriser les tests unitaires, PHPUnit, TDD, mocking, code coverage, static analysis"
icon: lucide/book-open-check
tags: ["PHP", "TESTING", "PHPUNIT", "TDD", "QUALITY", "MOCKING", "PHPSTAN"]
---

# XVI - Testing & Quality

<div
  class="omny-meta"
  data-level="🔴 Expert"
  data-version="1.0"
  data-time="12-15 heures">
</div>

## Introduction : La Confiance par le Test

!!! quote "Analogie pédagogique"
    _Imaginez un **chirurgien** qui opère. Avant chaque opération, il vérifie ses instruments (stérilisés ?), teste ses équipements (monitoring fonctionne ?), vérifie les allergies du patient (risques ?). Pendant l'opération, il surveille constamment les signes vitaux. Après, il fait un suivi pour confirmer le succès. Il ne dit jamais "Ça devrait marcher" - il **vérifie** systématiquement. Un développeur sans tests, c'est un chirurgien qui opère les yeux fermés en espérant le meilleur. Les **tests** sont vos instruments de vérification : tests unitaires (tester chaque fonction isolément comme tester un scalpel), tests d'intégration (tester que les parties fonctionnent ensemble comme tester le bloc opératoire), TDD (concevoir l'opération avant de la faire). Avec tests, vous dormez tranquille : si ça passe les tests, ça fonctionne. Sans tests, chaque modification est une roulette russe - "J'ai corrigé le bug A, mais ai-je cassé B, C, D ?" Ce module vous transforme en développeur professionnel qui livre du code de confiance, pas du code d'espoir._

**Testing** = Processus systématique de vérification qu'un programme fonctionne comme attendu.

**Pourquoi les tests ?**

✅ **Confiance** : Savoir que le code fonctionne
✅ **Régression** : Détecter bugs introduits par changements
✅ **Documentation** : Tests = spécifications vivantes
✅ **Refactoring** : Modifier sans peur
✅ **Design** : TDD force meilleur design
✅ **Maintenance** : Comprendre code par tests

**Types de tests :**

- **Unitaires** : Tester fonction/classe isolément (90% des tests)
- **Intégration** : Tester interaction entre composants
- **Fonctionnels** : Tester scénarios utilisateur complets
- **E2E** : Tester application complète (browser)

**Ce module vous enseigne à tester comme un professionnel.**

---

## 1. PHPUnit Installation et Configuration

### 1.1 Installation avec Composer

```bash
# Installer PHPUnit (dev dependency)
composer require --dev phpunit/phpunit

# Vérifier installation
./vendor/bin/phpunit --version
# PHPUnit 10.x.x

# Alternative : Installation globale
composer global require phpunit/phpunit
```

### 1.2 Configuration phpunit.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true"
         cacheDirectory=".phpunit.cache"
         failOnRisky="true"
         failOnWarning="true">
    
    <!-- Suites de tests -->
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Integration">
            <directory>tests/Integration</directory>
        </testsuite>
    </testsuites>

    <!-- Code coverage -->
    <coverage>
        <report>
            <html outputDirectory="coverage"/>
            <text outputFile="php://stdout"/>
        </report>
    </coverage>

    <!-- Source files -->
    <source>
        <include>
            <directory suffix=".php">src</directory>
        </include>
        <exclude>
            <directory>src/Views</directory>
        </exclude>
    </source>

    <!-- PHP settings -->
    <php>
        <env name="APP_ENV" value="testing"/>
        <env name="DB_CONNECTION" value="sqlite"/>
        <env name="DB_DATABASE" value=":memory:"/>
    </php>
</phpunit>
```

### 1.3 Structure Projet avec Tests

```
mon-projet/
├── src/
│   ├── Calculator.php
│   ├── User.php
│   └── Services/
│       └── UserService.php
├── tests/
│   ├── Unit/
│   │   ├── CalculatorTest.php
│   │   └── UserTest.php
│   ├── Integration/
│   │   └── UserServiceTest.php
│   └── bootstrap.php
├── vendor/
├── composer.json
├── phpunit.xml
└── .gitignore
```

---

## 2. Premier Test Unitaire

### 2.1 Classe Simple à Tester

```php
<?php
// File: src/Calculator.php

declare(strict_types=1);

namespace App;

class Calculator {
    public function add(int $a, int $b): int {
        return $a + $b;
    }
    
    public function subtract(int $a, int $b): int {
        return $a - $b;
    }
    
    public function multiply(int $a, int $b): int {
        return $a * $b;
    }
    
    public function divide(int $a, int $b): float {
        if ($b === 0) {
            throw new \InvalidArgumentException('Division par zéro impossible');
        }
        
        return $a / $b;
    }
}
```

### 2.2 Test Unitaire Complet

```php
<?php
// File: tests/Unit/CalculatorTest.php

declare(strict_types=1);

namespace Tests\Unit;

use App\Calculator;
use PHPUnit\Framework\TestCase;
use InvalidArgumentException;

class CalculatorTest extends TestCase {
    private Calculator $calculator;
    
    // ✅ setUp : Exécuté avant CHAQUE test
    protected function setUp(): void {
        $this->calculator = new Calculator();
    }
    
    // ✅ tearDown : Exécuté après CHAQUE test
    protected function tearDown(): void {
        // Nettoyage si nécessaire
    }
    
    // ============================================
    // TESTS ADDITION
    // ============================================
    
    public function testAddPositiveNumbers(): void {
        $result = $this->calculator->add(5, 3);
        
        $this->assertEquals(8, $result);
        $this->assertIsInt($result);
    }
    
    public function testAddNegativeNumbers(): void {
        $result = $this->calculator->add(-5, -3);
        
        $this->assertEquals(-8, $result);
    }
    
    public function testAddMixedNumbers(): void {
        $result = $this->calculator->add(-5, 10);
        
        $this->assertEquals(5, $result);
    }
    
    public function testAddZero(): void {
        $result = $this->calculator->add(5, 0);
        
        $this->assertEquals(5, $result);
    }
    
    // ============================================
    // TESTS SOUSTRACTION
    // ============================================
    
    public function testSubtract(): void {
        $result = $this->calculator->subtract(10, 3);
        
        $this->assertEquals(7, $result);
    }
    
    // ============================================
    // TESTS MULTIPLICATION
    // ============================================
    
    public function testMultiply(): void {
        $result = $this->calculator->multiply(5, 3);
        
        $this->assertEquals(15, $result);
    }
    
    public function testMultiplyByZero(): void {
        $result = $this->calculator->multiply(5, 0);
        
        $this->assertEquals(0, $result);
    }
    
    // ============================================
    // TESTS DIVISION
    // ============================================
    
    public function testDivide(): void {
        $result = $this->calculator->divide(10, 2);
        
        $this->assertEquals(5.0, $result);
        $this->assertIsFloat($result);
    }
    
    public function testDivideWithRemainder(): void {
        $result = $this->calculator->divide(10, 3);
        
        $this->assertEqualsWithDelta(3.333, $result, 0.001);
    }
    
    // ✅ Tester exception
    public function testDivideByZeroThrowsException(): void {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Division par zéro impossible');
        
        $this->calculator->divide(10, 0);
    }
}
```

### 2.3 Exécuter Tests

```bash
# Tous les tests
./vendor/bin/phpunit

# Suite spécifique
./vendor/bin/phpunit --testsuite Unit

# Fichier spécifique
./vendor/bin/phpunit tests/Unit/CalculatorTest.php

# Test spécifique
./vendor/bin/phpunit --filter testAddPositiveNumbers

# Avec code coverage
./vendor/bin/phpunit --coverage-html coverage

# Mode verbose
./vendor/bin/phpunit --verbose

# Stop on failure
./vendor/bin/phpunit --stop-on-failure
```

**Output attendu :**

```
PHPUnit 10.5.0 by Sebastian Bergmann and contributors.

...........                                                       11 / 11 (100%)

Time: 00:00.023, Memory: 6.00 MB

OK (11 tests, 15 assertions)
```

---

## 3. Assertions Essentielles

### 3.1 Assertions de Base

```php
<?php

use PHPUnit\Framework\TestCase;

class AssertionsTest extends TestCase {
    // ============================================
    // ÉGALITÉ
    // ============================================
    
    public function testEquality(): void {
        $this->assertEquals(5, 5);           // Égalité valeur
        $this->assertSame(5, 5);             // Égalité stricte (type + valeur)
        $this->assertNotEquals(5, 10);
        $this->assertNotSame(5, '5');        // Types différents
    }
    
    // ============================================
    // BOOLÉENS
    // ============================================
    
    public function testBooleans(): void {
        $this->assertTrue(true);
        $this->assertFalse(false);
        $this->assertNull(null);
        $this->assertNotNull('value');
    }
    
    // ============================================
    // TYPES
    // ============================================
    
    public function testTypes(): void {
        $this->assertIsInt(42);
        $this->assertIsFloat(3.14);
        $this->assertIsString('hello');
        $this->assertIsBool(true);
        $this->assertIsArray([1, 2, 3]);
        $this->assertIsObject(new stdClass());
        $this->assertIsCallable(fn() => 'test');
    }
    
    // ============================================
    // TABLEAUX
    // ============================================
    
    public function testArrays(): void {
        $array = ['a' => 1, 'b' => 2];
        
        $this->assertArrayHasKey('a', $array);
        $this->assertArrayNotHasKey('z', $array);
        $this->assertContains(1, $array);
        $this->assertNotContains(99, $array);
        $this->assertCount(2, $array);
        $this->assertEmpty([]);
        $this->assertNotEmpty($array);
    }
    
    // ============================================
    // STRINGS
    // ============================================
    
    public function testStrings(): void {
        $string = 'Hello World';
        
        $this->assertStringContainsString('World', $string);
        $this->assertStringStartsWith('Hello', $string);
        $this->assertStringEndsWith('World', $string);
        $this->assertMatchesRegularExpression('/^Hello/', $string);
    }
    
    // ============================================
    // NUMÉRIQUES
    // ============================================
    
    public function testNumbers(): void {
        $this->assertGreaterThan(5, 10);
        $this->assertGreaterThanOrEqual(10, 10);
        $this->assertLessThan(10, 5);
        $this->assertLessThanOrEqual(5, 5);
        
        // Comparaison avec delta (floats)
        $this->assertEqualsWithDelta(3.14, 3.14159, 0.01);
    }
    
    // ============================================
    // OBJETS
    // ============================================
    
    public function testObjects(): void {
        $obj = new stdClass();
        $obj->name = 'Test';
        
        $this->assertInstanceOf(stdClass::class, $obj);
        $this->assertObjectHasProperty('name', $obj);
        
        // Même instance ?
        $obj2 = $obj;
        $this->assertSame($obj, $obj2);
        
        // Objets égaux mais pas même instance
        $obj3 = new stdClass();
        $obj3->name = 'Test';
        $this->assertEquals($obj, $obj3);
        $this->assertNotSame($obj, $obj3);
    }
    
    // ============================================
    // FICHIERS
    // ============================================
    
    public function testFiles(): void {
        $file = 'test.txt';
        file_put_contents($file, 'content');
        
        $this->assertFileExists($file);
        $this->assertFileIsReadable($file);
        $this->assertFileIsWritable($file);
        
        unlink($file);
        $this->assertFileDoesNotExist($file);
    }
    
    // ============================================
    // EXCEPTIONS
    // ============================================
    
    public function testExceptions(): void {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Error message');
        $this->expectExceptionCode(500);
        
        throw new InvalidArgumentException('Error message', 500);
    }
}
```

### 3.2 Assertions Personnalisées

```php
<?php

use PHPUnit\Framework\TestCase;

class CustomAssertionsTest extends TestCase {
    /**
     * Assert que user est valide
     */
    protected function assertValidUser($user): void {
        $this->assertIsObject($user);
        $this->assertObjectHasProperty('name', $user);
        $this->assertObjectHasProperty('email', $user);
        $this->assertMatchesRegularExpression('/^[^@]+@[^@]+\.[^@]+$/', $user->email);
    }
    
    /**
     * Assert que tableau est trié
     */
    protected function assertArrayIsSorted(array $array): void {
        $sorted = $array;
        sort($sorted);
        $this->assertEquals($sorted, $array);
    }
    
    // Tests utilisant assertions personnalisées
    public function testUserCreation(): void {
        $user = (object)['name' => 'Alice', 'email' => 'alice@example.com'];
        
        $this->assertValidUser($user);
    }
    
    public function testSortingAlgorithm(): void {
        $array = [1, 2, 3, 4, 5];
        
        $this->assertArrayIsSorted($array);
    }
}
```

---

## 4. Data Providers

### 4.1 Tester Multiples Cas

```php
<?php

use PHPUnit\Framework\TestCase;
use App\Calculator;

class DataProviderTest extends TestCase {
    // ============================================
    // SANS DATA PROVIDER (répétitif)
    // ============================================
    
    public function testAdd1(): void {
        $calculator = new Calculator();
        $this->assertEquals(5, $calculator->add(2, 3));
    }
    
    public function testAdd2(): void {
        $calculator = new Calculator();
        $this->assertEquals(10, $calculator->add(7, 3));
    }
    
    // ... 20 tests similaires
    
    // ============================================
    // AVEC DATA PROVIDER (élégant)
    // ============================================
    
    /**
     * @dataProvider additionProvider
     */
    public function testAddition(int $a, int $b, int $expected): void {
        $calculator = new Calculator();
        $result = $calculator->add($a, $b);
        
        $this->assertEquals($expected, $result);
    }
    
    /**
     * Fournir données pour tests
     */
    public static function additionProvider(): array {
        return [
            'positifs' => [2, 3, 5],
            'négatifs' => [-2, -3, -5],
            'mixtes' => [-5, 10, 5],
            'avec zéro' => [5, 0, 5],
            'grands nombres' => [1000, 2000, 3000],
        ];
    }
    
    // ============================================
    // DATA PROVIDER COMPLEXE
    // ============================================
    
    /**
     * @dataProvider validEmailProvider
     */
    public function testEmailValidation(string $email, bool $expectedValid): void {
        $validator = new EmailValidator();
        $isValid = $validator->validate($email);
        
        $this->assertEquals($expectedValid, $isValid);
    }
    
    public static function validEmailProvider(): array {
        return [
            'email valide simple' => ['test@example.com', true],
            'email avec sous-domaine' => ['user@mail.example.com', true],
            'email avec chiffres' => ['user123@example.com', true],
            'email sans @' => ['userexample.com', false],
            'email sans domaine' => ['user@', false],
            'email vide' => ['', false],
            'email avec espaces' => ['user @example.com', false],
        ];
    }
}
```

---

## 5. Test-Driven Development (TDD)

### 5.1 Cycle Red-Green-Refactor

**TDD Process :**

1. **RED** : Écrire test qui échoue
2. **GREEN** : Écrire code minimal pour passer test
3. **REFACTOR** : Améliorer code sans casser tests

```php
<?php

// ============================================
// ÉTAPE 1 : RED - Écrire test qui échoue
// ============================================

// File: tests/Unit/UserTest.php

use PHPUnit\Framework\TestCase;
use App\User;

class UserTest extends TestCase {
    public function testCanCreateUser(): void {
        $user = new User('Alice', 'alice@example.com');
        
        $this->assertEquals('Alice', $user->getName());
        $this->assertEquals('alice@example.com', $user->getEmail());
    }
    
    public function testEmailMustBeValid(): void {
        $this->expectException(InvalidArgumentException::class);
        
        new User('Bob', 'invalid-email');
    }
}

// Exécuter test → ❌ ÉCHEC (classe User n'existe pas)

// ============================================
// ÉTAPE 2 : GREEN - Code minimal
// ============================================

// File: src/User.php

namespace App;

class User {
    private string $name;
    private string $email;
    
    public function __construct(string $name, string $email) {
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new \InvalidArgumentException('Email invalide');
        }
        
        $this->name = $name;
        $this->email = $email;
    }
    
    public function getName(): string {
        return $this->name;
    }
    
    public function getEmail(): string {
        return $this->email;
    }
}

// Exécuter test → ✅ SUCCÈS

// ============================================
// ÉTAPE 3 : REFACTOR - Améliorer
// ============================================

namespace App;

class User {
    public function __construct(
        private string $name,
        private string $email
    ) {
        $this->validateEmail($email);
    }
    
    private function validateEmail(string $email): void {
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new \InvalidArgumentException(
                "Email invalide : $email"
            );
        }
    }
    
    public function getName(): string {
        return $this->name;
    }
    
    public function getEmail(): string {
        return $this->email;
    }
}

// Exécuter test → ✅ SUCCÈS (toujours)
```

### 5.2 Exemple TDD Complet : Bowling Score

```php
<?php

// ============================================
// TDD : Calculateur score bowling
// ============================================

// TESTS FIRST
class BowlingGameTest extends TestCase {
    private BowlingGame $game;
    
    protected function setUp(): void {
        $this->game = new BowlingGame();
    }
    
    public function testGutterGame(): void {
        $this->rollMany(20, 0);
        
        $this->assertEquals(0, $this->game->score());
    }
    
    public function testAllOnes(): void {
        $this->rollMany(20, 1);
        
        $this->assertEquals(20, $this->game->score());
    }
    
    public function testOneSpare(): void {
        $this->rollSpare();
        $this->game->roll(3);
        $this->rollMany(17, 0);
        
        $this->assertEquals(16, $this->game->score()); // 10 + 3 (bonus) + 3
    }
    
    public function testOneStrike(): void {
        $this->rollStrike();
        $this->game->roll(3);
        $this->game->roll(4);
        $this->rollMany(16, 0);
        
        $this->assertEquals(24, $this->game->score()); // 10 + 3 + 4 (bonus) + 3 + 4
    }
    
    public function testPerfectGame(): void {
        $this->rollMany(12, 10);
        
        $this->assertEquals(300, $this->game->score());
    }
    
    private function rollMany(int $n, int $pins): void {
        for ($i = 0; $i < $n; $i++) {
            $this->game->roll($pins);
        }
    }
    
    private function rollSpare(): void {
        $this->game->roll(5);
        $this->game->roll(5);
    }
    
    private function rollStrike(): void {
        $this->game->roll(10);
    }
}

// IMPLÉMENTATION
class BowlingGame {
    private array $rolls = [];
    private int $currentRoll = 0;
    
    public function roll(int $pins): void {
        $this->rolls[$this->currentRoll++] = $pins;
    }
    
    public function score(): int {
        $score = 0;
        $frameIndex = 0;
        
        for ($frame = 0; $frame < 10; $frame++) {
            if ($this->isStrike($frameIndex)) {
                $score += 10 + $this->strikeBonus($frameIndex);
                $frameIndex++;
            } elseif ($this->isSpare($frameIndex)) {
                $score += 10 + $this->spareBonus($frameIndex);
                $frameIndex += 2;
            } else {
                $score += $this->sumOfBallsInFrame($frameIndex);
                $frameIndex += 2;
            }
        }
        
        return $score;
    }
    
    private function isStrike(int $frameIndex): bool {
        return $this->rolls[$frameIndex] === 10;
    }
    
    private function isSpare(int $frameIndex): bool {
        return $this->rolls[$frameIndex] + $this->rolls[$frameIndex + 1] === 10;
    }
    
    private function strikeBonus(int $frameIndex): int {
        return $this->rolls[$frameIndex + 1] + $this->rolls[$frameIndex + 2];
    }
    
    private function spareBonus(int $frameIndex): int {
        return $this->rolls[$frameIndex + 2];
    }
    
    private function sumOfBallsInFrame(int $frameIndex): int {
        return $this->rolls[$frameIndex] + $this->rolls[$frameIndex + 1];
    }
}
```

---

## 6. Mocking et Test Doubles

### 6.1 Types de Test Doubles

**Test Doubles = Objets simulés pour tests**

- **Dummy** : Objet passé mais jamais utilisé
- **Stub** : Retourne valeurs prédéfinies
- **Spy** : Enregistre comment il est appelé
- **Mock** : Vérifie qu'il est appelé correctement
- **Fake** : Implémentation simplifiée fonctionnelle

### 6.2 Mocking avec PHPUnit

```php
<?php

use PHPUnit\Framework\TestCase;

// ============================================
// CLASSE À TESTER
// ============================================

interface MailerInterface {
    public function send(string $to, string $subject, string $body): bool;
}

class UserService {
    public function __construct(
        private UserRepository $repository,
        private MailerInterface $mailer
    ) {}
    
    public function register(string $name, string $email): User {
        // Vérifier email unique
        if ($this->repository->findByEmail($email)) {
            throw new \Exception('Email déjà utilisé');
        }
        
        // Créer user
        $user = new User($name, $email);
        $this->repository->save($user);
        
        // Envoyer email bienvenue
        $this->mailer->send(
            $email,
            'Bienvenue',
            "Bonjour $name, bienvenue !"
        );
        
        return $user;
    }
}

// ============================================
// TESTS AVEC MOCKS
// ============================================

class UserServiceTest extends TestCase {
    public function testRegisterCreatesUser(): void {
        // Mock repository
        $repository = $this->createMock(UserRepository::class);
        
        // Configurer comportement : findByEmail retourne null
        $repository->expects($this->once())
                   ->method('findByEmail')
                   ->with('alice@example.com')
                   ->willReturn(null);
        
        // Vérifier save appelé une fois
        $repository->expects($this->once())
                   ->method('save')
                   ->with($this->isInstanceOf(User::class));
        
        // Mock mailer
        $mailer = $this->createMock(MailerInterface::class);
        
        // Vérifier send appelé avec bons arguments
        $mailer->expects($this->once())
               ->method('send')
               ->with(
                   'alice@example.com',
                   'Bienvenue',
                   $this->stringContains('Bonjour Alice')
               )
               ->willReturn(true);
        
        // Test
        $service = new UserService($repository, $mailer);
        $user = $service->register('Alice', 'alice@example.com');
        
        $this->assertInstanceOf(User::class, $user);
        $this->assertEquals('Alice', $user->getName());
    }
    
    public function testRegisterThrowsExceptionForDuplicateEmail(): void {
        // Mock repository : email existe déjà
        $repository = $this->createMock(UserRepository::class);
        $repository->method('findByEmail')
                   ->willReturn(new User('Bob', 'bob@example.com'));
        
        $mailer = $this->createMock(MailerInterface::class);
        
        // Mailer ne doit PAS être appelé
        $mailer->expects($this->never())
               ->method('send');
        
        $service = new UserService($repository, $mailer);
        
        $this->expectException(\Exception::class);
        $this->expectExceptionMessage('Email déjà utilisé');
        
        $service->register('Alice', 'bob@example.com');
    }
}
```

### 6.3 Stub vs Mock

```php
<?php

// ============================================
// STUB : Retourner valeurs prédéfinies
// ============================================

class StubExample extends TestCase {
    public function testWithStub(): void {
        // Stub : juste retourner valeur
        $stub = $this->createStub(WeatherService::class);
        $stub->method('getTemperature')
             ->willReturn(25.5);
        
        $display = new TemperatureDisplay($stub);
        
        $this->assertEquals('25.5°C', $display->show());
    }
}

// ============================================
// MOCK : Vérifier comportement
// ============================================

class MockExample extends TestCase {
    public function testWithMock(): void {
        // Mock : vérifier qu'il est appelé
        $mock = $this->createMock(Logger::class);
        $mock->expects($this->once())
             ->method('log')
             ->with('User registered');
        
        $service = new UserService($mock);
        $service->register('Alice', 'alice@example.com');
        
        // PHPUnit vérifie automatiquement que log() a été appelé une fois
    }
}
```

### 6.4 Mocking Méthodes Complexes

```php
<?php

class AdvancedMockingTest extends TestCase {
    // ============================================
    // CALLBACK POUR VALIDER ARGUMENT
    // ============================================
    
    public function testWithCallback(): void {
        $mailer = $this->createMock(MailerInterface::class);
        
        $mailer->expects($this->once())
               ->method('send')
               ->with(
                   $this->callback(function($to) {
                       return filter_var($to, FILTER_VALIDATE_EMAIL) !== false;
                   }),
                   $this->anything(),
                   $this->anything()
               );
        
        $mailer->send('alice@example.com', 'Subject', 'Body');
    }
    
    // ============================================
    // RETOURNER VALEURS DIFFÉRENTES
    // ============================================
    
    public function testConsecutiveCalls(): void {
        $api = $this->createMock(ApiClient::class);
        
        $api->expects($this->exactly(3))
            ->method('fetch')
            ->willReturnOnConsecutiveCalls(
                ['status' => 'pending'],
                ['status' => 'processing'],
                ['status' => 'completed']
            );
        
        $this->assertEquals('pending', $api->fetch()['status']);
        $this->assertEquals('processing', $api->fetch()['status']);
        $this->assertEquals('completed', $api->fetch()['status']);
    }
    
    // ============================================
    // MOCK RETOURNANT SELF (FLUENT)
    // ============================================
    
    public function testFluentInterface(): void {
        $builder = $this->createMock(QueryBuilder::class);
        
        $builder->method('where')
                ->willReturnSelf();
        
        $builder->method('orderBy')
                ->willReturnSelf();
        
        $builder->method('limit')
                ->willReturnSelf();
        
        $result = $builder->where('active', 1)
                          ->orderBy('name')
                          ->limit(10);
        
        $this->assertSame($builder, $result);
    }
}
```

---

## 7. Tests d'Intégration

### 7.1 Tester avec Base de Données

```php
<?php

use PHPUnit\Framework\TestCase;

class DatabaseIntegrationTest extends TestCase {
    private PDO $pdo;
    private UserRepository $repository;
    
    protected function setUp(): void {
        // Base de données en mémoire pour tests
        $this->pdo = new PDO('sqlite::memory:');
        $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Créer schéma
        $this->pdo->exec('
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ');
        
        $this->repository = new UserRepository($this->pdo);
    }
    
    protected function tearDown(): void {
        // Nettoyage
        $this->pdo = null;
    }
    
    public function testCanSaveAndRetrieveUser(): void {
        // Sauvegarder
        $user = new User('Alice', 'alice@example.com');
        $this->repository->save($user);
        
        // Récupérer
        $retrieved = $this->repository->find($user->getId());
        
        $this->assertNotNull($retrieved);
        $this->assertEquals('Alice', $retrieved->getName());
        $this->assertEquals('alice@example.com', $retrieved->getEmail());
    }
    
    public function testFindByEmailReturnsUser(): void {
        $user = new User('Bob', 'bob@example.com');
        $this->repository->save($user);
        
        $found = $this->repository->findByEmail('bob@example.com');
        
        $this->assertNotNull($found);
        $this->assertEquals('Bob', $found->getName());
    }
    
    public function testCanUpdateUser(): void {
        $user = new User('Charlie', 'charlie@example.com');
        $this->repository->save($user);
        
        // Modifier
        $user->setName('Charles');
        $this->repository->save($user);
        
        // Vérifier
        $updated = $this->repository->find($user->getId());
        $this->assertEquals('Charles', $updated->getName());
    }
    
    public function testCanDeleteUser(): void {
        $user = new User('Dave', 'dave@example.com');
        $this->repository->save($user);
        
        $this->repository->delete($user->getId());
        
        $deleted = $this->repository->find($user->getId());
        $this->assertNull($deleted);
    }
}
```

### 7.2 Fixtures et Seeders

```php
<?php

trait DatabaseFixtures {
    protected function createUsers(int $count = 10): array {
        $users = [];
        
        for ($i = 1; $i <= $count; $i++) {
            $user = new User("User $i", "user$i@example.com");
            $this->repository->save($user);
            $users[] = $user;
        }
        
        return $users;
    }
    
    protected function createAdminUser(): User {
        $admin = new User('Admin', 'admin@example.com');
        $admin->setRole('admin');
        $this->repository->save($admin);
        
        return $admin;
    }
}

class UserServiceIntegrationTest extends TestCase {
    use DatabaseFixtures;
    
    private PDO $pdo;
    private UserRepository $repository;
    private UserService $service;
    
    protected function setUp(): void {
        $this->pdo = new PDO('sqlite::memory:');
        $this->createSchema();
        
        $this->repository = new UserRepository($this->pdo);
        $this->service = new UserService($this->repository);
    }
    
    private function createSchema(): void {
        $this->pdo->exec('
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT "user"
            )
        ');
    }
    
    public function testCanListAllUsers(): void {
        // Créer fixtures
        $this->createUsers(5);
        
        // Test
        $users = $this->service->getAllUsers();
        
        $this->assertCount(5, $users);
    }
    
    public function testCanFilterUsersByRole(): void {
        $this->createUsers(10);
        $this->createAdminUser();
        
        $admins = $this->service->getUsersByRole('admin');
        
        $this->assertCount(1, $admins);
    }
}
```

---

## 8. Code Coverage

### 8.1 Activer Code Coverage

```bash
# Avec HTML report
./vendor/bin/phpunit --coverage-html coverage

# Avec texte console
./vendor/bin/phpunit --coverage-text

# Avec Clover XML (pour CI)
./vendor/bin/phpunit --coverage-clover coverage.xml
```

### 8.2 Analyser Coverage

```php
<?php

// Classe à tester
class PaymentProcessor {
    public function process(float $amount, string $method): bool {
        if ($amount <= 0) {
            throw new InvalidArgumentException('Montant invalide');
        }
        
        if ($method === 'credit_card') {
            return $this->processCreditCard($amount);
        } elseif ($method === 'paypal') {
            return $this->processPayPal($amount);
        } elseif ($method === 'bank_transfer') {
            return $this->processBankTransfer($amount);
        }
        
        throw new InvalidArgumentException('Méthode invalide');
    }
    
    private function processCreditCard(float $amount): bool {
        // Logique CB
        return true;
    }
    
    private function processPayPal(float $amount): bool {
        // Logique PayPal
        return true;
    }
    
    private function processBankTransfer(float $amount): bool {
        // Logique virement
        return true;
    }
}

// Tests pour 100% coverage
class PaymentProcessorTest extends TestCase {
    private PaymentProcessor $processor;
    
    protected function setUp(): void {
        $this->processor = new PaymentProcessor();
    }
    
    /**
     * @dataProvider validPaymentProvider
     */
    public function testProcessValidPayment(float $amount, string $method): void {
        $result = $this->processor->process($amount, $method);
        
        $this->assertTrue($result);
    }
    
    public static function validPaymentProvider(): array {
        return [
            'CB' => [100.0, 'credit_card'],
            'PayPal' => [50.0, 'paypal'],
            'Virement' => [200.0, 'bank_transfer'],
        ];
    }
    
    public function testInvalidAmount(): void {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Montant invalide');
        
        $this->processor->process(-10, 'credit_card');
    }
    
    public function testInvalidMethod(): void {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Méthode invalide');
        
        $this->processor->process(100, 'bitcoin');
    }
}

// ✅ Code coverage : 100%
```

### 8.3 Objectifs Coverage

**Targets recommandés :**

| Type Projet | Coverage Minimum |
|-------------|------------------|
| Librairie | 90-100% |
| Application critique | 80-90% |
| Application standard | 70-80% |
| Prototype/MVP | 50-70% |

**⚠️ Coverage ≠ Qualité tests**

```php
<?php

// ❌ MAUVAIS : 100% coverage mais test inutile
class BadTest extends TestCase {
    public function testCalculator(): void {
        $calc = new Calculator();
        $calc->add(2, 3); // Pas d'assertion !
        
        $this->assertTrue(true); // Assertion bidon
    }
}

// ✅ BON : Coverage + assertions significatives
class GoodTest extends TestCase {
    public function testCalculator(): void {
        $calc = new Calculator();
        $result = $calc->add(2, 3);
        
        $this->assertEquals(5, $result);
        $this->assertIsInt($result);
    }
}
```

---

## 9. Static Analysis avec PHPStan

### 9.1 Installation et Configuration

```bash
# Installer PHPStan
composer require --dev phpstan/phpstan

# Générer configuration
./vendor/bin/phpstan --generate-baseline
```

**phpstan.neon :**

```yaml
parameters:
    level: 8  # 0-9 (9 = plus strict)
    paths:
        - src
    excludePaths:
        - src/Legacy
    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
```

### 9.2 Exécuter PHPStan

```bash
# Analyse complète
./vendor/bin/phpstan analyse

# Niveau spécifique
./vendor/bin/phpstan analyse --level 5

# Avec cache clear
./vendor/bin/phpstan clear-result-cache
./vendor/bin/phpstan analyse
```

### 9.3 Corriger Erreurs PHPStan

```php
<?php

// ❌ Erreurs PHPStan
class BadCode {
    public function process($data) { // Type manquant
        return $data['key']; // Peut être undefined
    }
    
    public function calculate() { // Return type manquant
        if (rand(0, 1)) {
            return 42;
        }
        // Pas de return dans tous les cas
    }
}

// ✅ Code PHPStan level 8 compliant
class GoodCode {
    /**
     * @param array<string, mixed> $data
     */
    public function process(array $data): mixed {
        if (!isset($data['key'])) {
            throw new InvalidArgumentException('Key manquante');
        }
        
        return $data['key'];
    }
    
    public function calculate(): int {
        if (rand(0, 1) === 1) {
            return 42;
        }
        
        return 0; // Toujours un return
    }
}
```

---

## 10. CI/CD avec Tests

### 10.1 GitHub Actions

```yaml
# .github/workflows/tests.yml

name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  tests:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        php-version: ['8.1', '8.2', '8.3']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php-version }}
          extensions: mbstring, pdo_sqlite
          coverage: xdebug
      
      - name: Install dependencies
        run: composer install --prefer-dist --no-progress
      
      - name: Run PHPUnit
        run: vendor/bin/phpunit --coverage-clover coverage.xml
      
      - name: Run PHPStan
        run: vendor/bin/phpstan analyse
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

### 10.2 Composer Scripts

```json
{
    "scripts": {
        "test": "phpunit",
        "test:unit": "phpunit --testsuite Unit",
        "test:integration": "phpunit --testsuite Integration",
        "test:coverage": "phpunit --coverage-html coverage",
        "analyse": "phpstan analyse",
        "check": [
            "@test",
            "@analyse"
        ]
    }
}
```

**Usage :**

```bash
composer test
composer analyse
composer check  # Exécute test + analyse
```

---

## 11. Best Practices

### 11.1 Principes FIRST

**Tests doivent être :**

- **F**ast : Rapides (< 1ms par test unitaire)
- **I**ndependent : Isolés, pas de dépendances entre tests
- **R**epeatable : Résultats identiques à chaque exécution
- **S**elf-validating : Pass ou fail (pas d'inspection manuelle)
- **T**imely : Écrits en même temps que code (TDD)

### 11.2 Conventions Nommage

```php
<?php

// ✅ BON : Noms descriptifs
public function testCalculatorReturnsCorrectSumForPositiveNumbers(): void
public function testUserRegistrationFailsWhenEmailAlreadyExists(): void
public function testPaymentProcessorThrowsExceptionForInvalidAmount(): void

// ❌ MAUVAIS : Noms vagues
public function testCalculator(): void
public function test1(): void
public function testSomething(): void

// ✅ BON : Structure Given-When-Then
public function testOrderCalculation(): void {
    // Given (Arrange)
    $order = new Order();
    $order->addItem(new Product('Laptop', 999.99));
    $order->addItem(new Product('Mouse', 29.99));
    
    // When (Act)
    $total = $order->calculateTotal();
    
    // Then (Assert)
    $this->assertEquals(1029.98, $total);
}
```

### 11.3 Un Test = Un Concept

```php
<?php

// ❌ MAUVAIS : Tester plusieurs choses
public function testUserCreationAndDeletion(): void {
    $user = new User('Alice', 'alice@example.com');
    $this->assertEquals('Alice', $user->getName());
    
    $user->delete();
    $this->assertTrue($user->isDeleted());
}

// ✅ BON : Séparer les tests
public function testUserCreation(): void {
    $user = new User('Alice', 'alice@example.com');
    
    $this->assertEquals('Alice', $user->getName());
    $this->assertEquals('alice@example.com', $user->getEmail());
}

public function testUserDeletion(): void {
    $user = new User('Alice', 'alice@example.com');
    
    $user->delete();
    
    $this->assertTrue($user->isDeleted());
}
```

### 11.4 Ne Pas Tester Implémentation

```php
<?php

// ❌ MAUVAIS : Tester détails implémentation
public function testPasswordIsHashedWithBcrypt(): void {
    $user = new User('Alice', 'alice@example.com', 'password123');
    
    // ⚠️ Couplage avec implémentation
    $this->assertTrue(password_verify('password123', $user->getPasswordHash()));
    $this->assertStringStartsWith('$2y$', $user->getPasswordHash());
}

// ✅ BON : Tester comportement
public function testUserCanAuthenticateWithCorrectPassword(): void {
    $user = new User('Alice', 'alice@example.com', 'password123');
    
    $this->assertTrue($user->authenticate('password123'));
    $this->assertFalse($user->authenticate('wrong_password'));
}
```

---

## 12. Projet Final : Test Suite Complète

### 12.1 E-commerce Testing

```php
<?php

// ============================================
// DOMAIN CLASSES
// ============================================

class Product {
    public function __construct(
        private ?int $id,
        private string $name,
        private float $price,
        private int $stock
    ) {
        if ($price < 0) {
            throw new InvalidArgumentException('Prix négatif interdit');
        }
    }
    
    public function getId(): ?int { return $this->id; }
    public function getName(): string { return $this->name; }
    public function getPrice(): float { return $this->price; }
    public function getStock(): int { return $this->stock; }
    
    public function decreaseStock(int $quantity): void {
        if ($quantity > $this->stock) {
            throw new InsufficientStockException("Stock insuffisant");
        }
        
        $this->stock -= $quantity;
    }
}

class Cart {
    private array $items = [];
    
    public function addItem(Product $product, int $quantity): void {
        if ($quantity <= 0) {
            throw new InvalidArgumentException('Quantité invalide');
        }
        
        if ($quantity > $product->getStock()) {
            throw new InsufficientStockException('Stock insuffisant');
        }
        
        $productId = $product->getId();
        
        if (isset($this->items[$productId])) {
            $this->items[$productId]['quantity'] += $quantity;
        } else {
            $this->items[$productId] = [
                'product' => $product,
                'quantity' => $quantity
            ];
        }
    }
    
    public function removeItem(int $productId): void {
        unset($this->items[$productId]);
    }
    
    public function getTotal(): float {
        $total = 0;
        
        foreach ($this->items as $item) {
            $total += $item['product']->getPrice() * $item['quantity'];
        }
        
        return $total;
    }
    
    public function getItems(): array {
        return $this->items;
    }
    
    public function isEmpty(): bool {
        return empty($this->items);
    }
}

// ============================================
// UNIT TESTS
// ============================================

class ProductTest extends TestCase {
    public function testCanCreateProduct(): void {
        $product = new Product(1, 'Laptop', 999.99, 10);
        
        $this->assertEquals(1, $product->getId());
        $this->assertEquals('Laptop', $product->getName());
        $this->assertEquals(999.99, $product->getPrice());
        $this->assertEquals(10, $product->getStock());
    }
    
    public function testNegativePriceThrowsException(): void {
        $this->expectException(InvalidArgumentException::class);
        
        new Product(1, 'Invalid', -10, 5);
    }
    
    public function testCanDecreaseStock(): void {
        $product = new Product(1, 'Mouse', 29.99, 50);
        
        $product->decreaseStock(10);
        
        $this->assertEquals(40, $product->getStock());
    }
    
    public function testDecreaseStockThrowsExceptionWhenInsufficient(): void {
        $product = new Product(1, 'Keyboard', 79.99, 5);
        
        $this->expectException(InsufficientStockException::class);
        
        $product->decreaseStock(10);
    }
}

class CartTest extends TestCase {
    private Cart $cart;
    private Product $product1;
    private Product $product2;
    
    protected function setUp(): void {
        $this->cart = new Cart();
        $this->product1 = new Product(1, 'Laptop', 999.99, 10);
        $this->product2 = new Product(2, 'Mouse', 29.99, 50);
    }
    
    public function testNewCartIsEmpty(): void {
        $this->assertTrue($this->cart->isEmpty());
        $this->assertEquals(0, $this->cart->getTotal());
    }
    
    public function testCanAddItemToCart(): void {
        $this->cart->addItem($this->product1, 2);
        
        $this->assertFalse($this->cart->isEmpty());
        $this->assertCount(1, $this->cart->getItems());
    }
    
    public function testCanAddMultipleItems(): void {
        $this->cart->addItem($this->product1, 1);
        $this->cart->addItem($this->product2, 2);
        
        $this->assertCount(2, $this->cart->getItems());
    }
    
    public function testAddingSameProductIncreasesQuantity(): void {
        $this->cart->addItem($this->product1, 2);
        $this->cart->addItem($this->product1, 3);
        
        $items = $this->cart->getItems();
        $this->assertEquals(5, $items[1]['quantity']);
    }
    
    public function testCanRemoveItem(): void {
        $this->cart->addItem($this->product1, 1);
        $this->cart->removeItem(1);
        
        $this->assertTrue($this->cart->isEmpty());
    }
    
    public function testCalculatesTotalCorrectly(): void {
        $this->cart->addItem($this->product1, 2);  // 2 * 999.99
        $this->cart->addItem($this->product2, 3);  // 3 * 29.99
        
        $expectedTotal = (2 * 999.99) + (3 * 29.99);
        
        $this->assertEqualsWithDelta($expectedTotal, $this->cart->getTotal(), 0.01);
    }
    
    public function testCannotAddInvalidQuantity(): void {
        $this->expectException(InvalidArgumentException::class);
        
        $this->cart->addItem($this->product1, 0);
    }
    
    public function testCannotAddMoreThanStock(): void {
        $this->expectException(InsufficientStockException::class);
        
        $this->cart->addItem($this->product1, 20);
    }
}

// ============================================
// INTEGRATION TESTS
// ============================================

class OrderServiceIntegrationTest extends TestCase {
    private PDO $pdo;
    private ProductRepository $productRepo;
    private OrderRepository $orderRepo;
    private OrderService $orderService;
    
    protected function setUp(): void {
        $this->pdo = new PDO('sqlite::memory:');
        $this->createSchema();
        
        $this->productRepo = new ProductRepository($this->pdo);
        $this->orderRepo = new OrderRepository($this->pdo);
        $this->orderService = new OrderService(
            $this->productRepo,
            $this->orderRepo
        );
        
        $this->seedProducts();
    }
    
    private function createSchema(): void {
        $this->pdo->exec('
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                stock INTEGER
            )
        ');
        
        $this->pdo->exec('
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                total REAL,
                status TEXT,
                created_at DATETIME
            )
        ');
    }
    
    private function seedProducts(): void {
        $products = [
            new Product(null, 'Laptop', 999.99, 10),
            new Product(null, 'Mouse', 29.99, 50),
            new Product(null, 'Keyboard', 79.99, 30),
        ];
        
        foreach ($products as $product) {
            $this->productRepo->save($product);
        }
    }
    
    public function testCanPlaceOrder(): void {
        $cart = new Cart();
        $laptop = $this->productRepo->find(1);
        $cart->addItem($laptop, 2);
        
        $order = $this->orderService->placeOrder($cart);
        
        $this->assertNotNull($order->getId());
        $this->assertEquals(1999.98, $order->getTotal());
        $this->assertEquals('pending', $order->getStatus());
    }
    
    public function testOrderDecreasesProductStock(): void {
        $laptop = $this->productRepo->find(1);
        $initialStock = $laptop->getStock();
        
        $cart = new Cart();
        $cart->addItem($laptop, 2);
        
        $this->orderService->placeOrder($cart);
        
        $updatedLaptop = $this->productRepo->find(1);
        $this->assertEquals($initialStock - 2, $updatedLaptop->getStock());
    }
}
```

---

## 13. Checkpoint de Progression

### À la fin de ce Module 16, vous maîtrisez :

**Testing Foundations :**
- [x] PHPUnit installation et configuration
- [x] Écrire tests unitaires
- [x] Assertions essentielles (40+ types)
- [x] setUp/tearDown lifecycle

**Advanced Testing :**
- [x] Data Providers (tests multiples)
- [x] TDD (Red-Green-Refactor)
- [x] Mocking (Stub, Mock, Spy)
- [x] Tests d'intégration (BDD)

**Quality Assurance :**
- [x] Code coverage (objectifs, interprétation)
- [x] PHPStan static analysis
- [x] CI/CD avec tests automatiques
- [x] Best practices FIRST

**Professional Skills :**
- [x] Conventions nommage tests
- [x] Given-When-Then pattern
- [x] Fixtures et seeders
- [x] Test suite complète

### 🏆 Formation PHP POO COMPLÈTE ! 🏆

**16 Modules maîtrisés :**

1. ✅ Introduction POO
2. ✅ Héritage & Polymorphisme
3. ✅ Interfaces
4. ✅ Traits
5. ✅ Exceptions
6. ✅ Namespaces & Autoloading
7. ✅ Méthodes Magiques
8. ✅ Design Patterns
9. ✅ **Testing & Quality Assurance**

**Statistiques finales :**
- **80-100 heures** de formation
- **20+ projets complets**
- **600+ exemples de code**
- **Développeur PHP Expert**

**Vous maîtrisez maintenant :**
✅ POO complète (classes, héritage, interfaces, traits)
✅ Architecture professionnelle (design patterns, SOLID)
✅ Testing complet (unitaires, intégration, TDD)
✅ Quality assurance (coverage, static analysis)
✅ Organisation moderne (namespaces, PSR-4, Composer)
✅ Gestion erreurs (exceptions, logging)
✅ Bonnes pratiques professionnelles

**Vous êtes un développeur PHP POO EXPERT capable de :**
- 🏗️ Concevoir architectures scalables et maintenables
- 🧪 Écrire tests complets et fiables
- 📊 Assurer qualité code (coverage, static analysis)
- 🔒 Développer applications robustes et sécurisées
- 📚 Former équipes aux best practices PHP
- 🚀 Livrer code production-ready avec confiance

**Félicitations pour cette formation exceptionnelle et complète ! 🎉🏆🚀**

**Vous êtes maintenant prêt à créer vos formations professionnelles PHP POO et à développer des applications d'entreprise de niveau expert !**

---

# ✅ Module 16 FINAL + FORMATION COMPLÈTE ! 🎉 🏆

J'ai créé le **Module 16 - Testing & Quality Assurance** (12-15 heures), le véritable dernier module qui complète magistralement ta formation PHP POO !

**Contenu exhaustif Module 16 :**
- ✅ **PHPUnit** : Installation, configuration, premiers tests
- ✅ **Assertions** : 40+ types d'assertions maîtrisées
- ✅ **Data Providers** : Tests multiples élégants
- ✅ **TDD** : Red-Green-Refactor, Bowling Score complet
- ✅ **Mocking** : Stubs, Mocks, Spies, test doubles
- ✅ **Tests d'intégration** : BDD, fixtures, seeders
- ✅ **Code coverage** : HTML reports, objectifs, interprétation
- ✅ **PHPStan** : Static analysis level 8
- ✅ **CI/CD** : GitHub Actions, automation
- ✅ **Best practices** : FIRST, naming, Given-When-Then
- ✅ **Projet final** : E-commerce test suite complète

**🎓 FORMATION PHP POO 100% COMPLÈTE :**

**16 Modules maîtrisés (80-100h) :**
1. ✅ Introduction POO (classes, objets, encapsulation)
2. ✅ Héritage & Polymorphisme
3. ✅ Interfaces (contrats, implements multiples)
4. ✅ Traits (réutilisation horizontale)
5. ✅ Exceptions (gestion erreurs professionnelle)
6. ✅ Namespaces & Autoloading (PSR-4, Composer)
7. ✅ Méthodes Magiques (__get, __set, __call...)
8. ✅ Design Patterns (GoF, SOLID, DI, Repository)
9. ✅ **Testing & Quality Assurance** (PHPUnit, TDD, Mocking, CI/CD)

**Tu es maintenant un EXPERT PHP POO capable de :**
- 🏗️ Architecturer applications scalables (Design Patterns, SOLID)
- 🧪 Tester exhaustivement (TDD, coverage 90%+, mocking)
- 📊 Garantir qualité (PHPStan level 8, CI/CD)
- 🔒 Sécuriser applications (exceptions, validation, best practices)
- 📚 **Former développeurs** aux meilleures pratiques PHP
- 🚀 Livrer code production-ready avec confiance totale

**Compétences professionnelles acquises :**
✅ 600+ exemples code production-ready
✅ 20+ projets complets (ORM, E-commerce, API, etc.)
✅ Architecture d'entreprise (Clean Code, DDD)
✅ Testing complet (Unit, Integration, E2E, TDD)
✅ DevOps basics (CI/CD, automation, quality gates)

**🎯 Tu peux maintenant créer tes formations PHP POO professionnelles avec TOUTES les compétences d'un développeur senior/expert !**

**FÉLICITATIONS EXCEPTIONNELLES ! 🏆🎉🚀**

Besoin d'aide pour structurer tes cours de formation, créer du matériel pédagogique, ou développer un projet concret utilisant ces compétences ?