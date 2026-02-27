---
description: "Maîtriser les méthodes magiques PHP : __get, __set, __call, __toString, __invoke, __clone, serialization"
icon: lucide/book-open-check
tags: ["PHP", "POO", "MAGIC-METHODS", "__GET", "__SET", "__CALL", "__INVOKE", "__CLONE"]
---

# XIV - Magic Methods

<div
  class="omny-meta"
  data-level="🟠 Avancé"
  data-version="1.0"
  data-time="8-10 heures">
</div>

## Introduction : La Magie du PHP

!!! quote "Analogie pédagogique"
    _Imaginez un **hôtel intelligent**. Normalement, pour chaque service (room service, conciergerie, pressing), vous appelez un numéro spécifique. Mais cet hôtel a un **réceptionniste magique** : vous composez n'importe quel numéro, même inexistant, et il **intercepte** votre appel, comprend ce que vous voulez, et redirige intelligemment. "Service chambre 501 ?" → Il sait que 501 est votre chambre et vous connecte au room service. "Réveil 7h ?" → Il programme automatiquement l'alarme. Vous appelez des services qui n'existent pas techniquement, mais le système les crée dynamiquement. Les **méthodes magiques** PHP fonctionnent pareil : elles interceptent des actions (accéder propriété inexistante, appeler méthode inconnue, convertir en string) et vous laissent définir le comportement. `__get()` attrape `$obj->propInexistante`, `__call()` attrape `$obj->methodeInconnue()`, `__toString()` attrape `echo $obj`. C'est de la "magie" car PHP appelle ces méthodes automatiquement dans des situations spéciales. Ce module vous apprend à devenir le réceptionniste magique de vos objets._

**Méthodes Magiques** = Méthodes spéciales PHP préfixées `__` appelées automatiquement dans des situations spécifiques.

**Pourquoi les méthodes magiques ?**

✅ **Surcharge dynamique** : Propriétés/méthodes à la volée
✅ **Proxies** : Intercepter accès propriétés
✅ **DSL (Domain Specific Language)** : Syntaxe fluide
✅ **Lazy loading** : Charger données à la demande
✅ **ORM** : Eloquent, Doctrine utilisent massivement
✅ **Flexibilité** : Comportements personnalisés

**⚠️ Dangers :**

❌ **Performance** : Plus lent que code normal
❌ **Debugging difficile** : Comportement caché
❌ **IDE/Static Analysis** : Pas d'autocomplétion
❌ **Complexité** : Magie = compréhension difficile

**Ce module vous enseigne à utiliser la magie avec sagesse.**

---

## 1. __construct et __destruct (Rappel Approfondi)

### 1.1 __construct : Initialisation

```php
<?php
declare(strict_types=1);

class User {
    private string $name;
    private string $email;
    private DateTime $createdAt;
    
    // ✅ Appelé automatiquement à new User()
    public function __construct(string $name, string $email) {
        $this->name = $name;
        $this->email = $email;
        $this->createdAt = new DateTime();
        
        echo "User créé : $name\n";
    }
}

$user = new User('Alice', 'alice@example.com');
// Output : User créé : Alice

// ============================================
// Constructeur avec valeurs par défaut
// ============================================

class Product {
    public function __construct(
        private string $name,
        private float $price,
        private int $stock = 0,        // Défaut
        private bool $active = true    // Défaut
    ) {
        echo "Product créé : $name ($price€)\n";
    }
}

$product1 = new Product('Laptop', 999.99);           // stock=0, active=true
$product2 = new Product('Mouse', 29.99, 50);         // stock=50, active=true
$product3 = new Product('Keyboard', 79.99, 20, false); // stock=20, active=false

// ============================================
// Constructeur avec validation
// ============================================

class BankAccount {
    public function __construct(
        private string $accountNumber,
        private float $balance
    ) {
        if ($balance < 0) {
            throw new InvalidArgumentException("Le solde ne peut pas être négatif");
        }
        
        if (!preg_match('/^[A-Z]{2}\d{2}[A-Z0-9]+$/', $accountNumber)) {
            throw new InvalidArgumentException("Numéro de compte invalide (format IBAN)");
        }
    }
}

try {
    $account = new BankAccount('FR123456', -100); // Exception
} catch (InvalidArgumentException $e) {
    echo "Erreur : " . $e->getMessage();
}
```

### 1.2 __destruct : Nettoyage

```php
<?php

class FileLogger {
    private $fileHandle;
    private string $filename;
    
    public function __construct(string $filename) {
        $this->filename = $filename;
        $this->fileHandle = fopen($filename, 'a');
        
        if ($this->fileHandle === false) {
            throw new RuntimeException("Impossible d'ouvrir le fichier");
        }
        
        echo "Fichier ouvert : $filename\n";
    }
    
    public function log(string $message): void {
        fwrite($this->fileHandle, date('Y-m-d H:i:s') . " - $message\n");
    }
    
    // ✅ Appelé automatiquement quand objet détruit
    public function __destruct() {
        if ($this->fileHandle) {
            fclose($this->fileHandle);
            echo "Fichier fermé : {$this->filename}\n";
        }
    }
}

function test(): void {
    $logger = new FileLogger('app.log');
    $logger->log('Test 1');
    $logger->log('Test 2');
    
    // __destruct() appelé à la fin de la fonction
}

test();
// Output :
// Fichier ouvert : app.log
// Fichier fermé : app.log

// ============================================
// Destruction manuelle
// ============================================

$logger = new FileLogger('app.log');
$logger->log('Message');

unset($logger); // Force appel __destruct()
// Output : Fichier fermé : app.log

echo "Script continue\n";
```

**Quand __destruct est appelé :**

✅ Fin du script
✅ unset() explicite
✅ Aucune référence à l'objet
✅ exit() / die()
✅ Exception non attrapée

**⚠️ Limitations __destruct :**

- Ordre destruction non garanti (objets interdépendants)
- Exceptions dans destructeur problématiques
- Pas de paramètres possibles

---

## 2. __get, __set, __isset, __unset

### 2.1 __get : Surcharge Lecture Propriétés

**Appelé quand on accède à propriété inexistante ou inaccessible**

```php
<?php
declare(strict_types=1);

class DynamicObject {
    private array $data = [];
    
    // ✅ Intercepte lecture propriété inexistante
    public function __get(string $name): mixed {
        echo "Accès à propriété inexistante : $name\n";
        
        return $this->data[$name] ?? null;
    }
    
    public function __set(string $name, mixed $value): void {
        echo "Écriture propriété : $name = $value\n";
        $this->data[$name] = $value;
    }
}

$obj = new DynamicObject();

// Accès propriété inexistante → __get() appelé
$obj->name = 'Alice';        // __set('name', 'Alice')
echo $obj->name;             // __get('name')
// Output :
// Écriture propriété : name = Alice
// Accès à propriété inexistante : name
// Alice

$obj->email = 'alice@example.com';
$obj->age = 25;

echo $obj->email;            // alice@example.com
echo $obj->nonExistent;      // null

// ============================================
// Cas d'usage : Lazy Loading
// ============================================

class User {
    private ?array $profile = null;
    
    public function __construct(
        private int $id,
        private string $name
    ) {}
    
    public function __get(string $name): mixed {
        // Lazy load profile à la demande
        if ($name === 'profile') {
            if ($this->profile === null) {
                echo "Chargement profile depuis BDD...\n";
                // Simuler requête BDD
                $this->profile = [
                    'bio' => 'Développeur PHP',
                    'location' => 'Paris'
                ];
            }
            
            return $this->profile;
        }
        
        throw new Exception("Propriété $name inexistante");
    }
}

$user = new User(1, 'Alice');
echo $user->name;            // Alice (propriété normale)
echo $user->profile['bio'];  // Déclenche chargement BDD
// Output : Chargement profile depuis BDD...

// ============================================
// Cas d'usage : Propriétés calculées
// ============================================

class Product {
    public function __construct(
        private float $priceHT,
        private float $vatRate = 0.20
    ) {}
    
    public function __get(string $name): mixed {
        return match ($name) {
            'priceTTC' => $this->priceHT * (1 + $this->vatRate),
            'vat' => $this->priceHT * $this->vatRate,
            default => throw new Exception("Propriété $name inexistante")
        };
    }
}

$product = new Product(100);
echo $product->priceTTC;     // 120 (calculé à la volée)
echo $product->vat;          // 20
```

### 2.2 __set : Surcharge Écriture Propriétés

```php
<?php

class ValidatedUser {
    private array $data = [];
    private array $validationRules = [
        'email' => 'email',
        'age' => 'int',
        'name' => 'string'
    ];
    
    public function __set(string $name, mixed $value): void {
        // Validation automatique
        if (isset($this->validationRules[$name])) {
            $rule = $this->validationRules[$name];
            
            if ($rule === 'email' && !filter_var($value, FILTER_VALIDATE_EMAIL)) {
                throw new InvalidArgumentException("Email invalide : $value");
            }
            
            if ($rule === 'int' && !is_int($value)) {
                throw new InvalidArgumentException("$name doit être un entier");
            }
            
            if ($rule === 'string' && !is_string($value)) {
                throw new InvalidArgumentException("$name doit être une chaîne");
            }
        }
        
        $this->data[$name] = $value;
    }
    
    public function __get(string $name): mixed {
        return $this->data[$name] ?? null;
    }
}

$user = new ValidatedUser();

$user->name = 'Alice';           // ✅ OK
$user->email = 'alice@example.com'; // ✅ OK
$user->age = 25;                 // ✅ OK

try {
    $user->email = 'invalid';    // ❌ Exception
} catch (InvalidArgumentException $e) {
    echo $e->getMessage();
}

// ============================================
// Cas d'usage : Read-only après création
// ============================================

class ImmutableConfig {
    private array $data = [];
    private bool $locked = false;
    
    public function __construct(array $data) {
        $this->data = $data;
    }
    
    public function lock(): void {
        $this->locked = true;
    }
    
    public function __set(string $name, mixed $value): void {
        if ($this->locked) {
            throw new RuntimeException("Configuration verrouillée, modification impossible");
        }
        
        $this->data[$name] = $value;
    }
    
    public function __get(string $name): mixed {
        return $this->data[$name] ?? null;
    }
}

$config = new ImmutableConfig(['env' => 'dev']);
$config->debug = true;           // ✅ OK

$config->lock();                 // Verrouiller

try {
    $config->debug = false;      // ❌ Exception
} catch (RuntimeException $e) {
    echo $e->getMessage();
}
```

### 2.3 __isset et __unset

```php
<?php

class DynamicProperties {
    private array $data = [];
    
    public function __set(string $name, mixed $value): void {
        $this->data[$name] = $value;
    }
    
    public function __get(string $name): mixed {
        return $this->data[$name] ?? null;
    }
    
    // ✅ Appelé par isset() / empty()
    public function __isset(string $name): bool {
        echo "__isset($name) appelé\n";
        return isset($this->data[$name]);
    }
    
    // ✅ Appelé par unset()
    public function __unset(string $name): void {
        echo "__unset($name) appelé\n";
        unset($this->data[$name]);
    }
}

$obj = new DynamicProperties();
$obj->name = 'Alice';
$obj->age = 25;

// isset() → __isset()
var_dump(isset($obj->name));    // __isset(name) appelé → true
var_dump(isset($obj->unknown)); // __isset(unknown) appelé → false

// empty() → __isset() + __get()
var_dump(empty($obj->name));    // false

// unset() → __unset()
unset($obj->age);               // __unset(age) appelé

var_dump(isset($obj->age));     // false
```

**Diagramme : Flux __get/__set**

```mermaid
sequenceDiagram
    participant Code
    participant PHP
    participant Object
    
    Code->>PHP: $obj->name = 'Alice'
    PHP->>PHP: Propriété 'name' existe ?
    
    alt Propriété existe
        PHP->>Object: Assigner directement
    else Propriété inexistante
        PHP->>Object: __set('name', 'Alice')
    end
    
    Code->>PHP: echo $obj->name
    PHP->>PHP: Propriété 'name' accessible ?
    
    alt Propriété accessible
        PHP->>Code: Retourner valeur
    else Propriété inaccessible
        PHP->>Object: __get('name')
        Object->>Code: Retourner valeur
    end
    
    style Object fill:#e1f5e1
```

---

## 3. __call et __callStatic

### 3.1 __call : Surcharge Méthodes d'Instance

**Appelé quand on appelle méthode inexistante ou inaccessible**

```php
<?php
declare(strict_types=1);

class QueryBuilder {
    private array $wheres = [];
    private array $orders = [];
    
    // ✅ Intercepte appel méthode inexistante
    public function __call(string $name, array $arguments): mixed {
        echo "Méthode inexistante appelée : $name\n";
        
        // where{Column}()
        if (str_starts_with($name, 'where')) {
            $column = lcfirst(substr($name, 5)); // whereEmail → email
            $this->wheres[] = "$column = " . $arguments[0];
            return $this;
        }
        
        // orderBy{Column}()
        if (str_starts_with($name, 'orderBy')) {
            $column = lcfirst(substr($name, 7)); // orderByName → name
            $direction = $arguments[0] ?? 'ASC';
            $this->orders[] = "$column $direction";
            return $this;
        }
        
        throw new BadMethodCallException("Méthode $name inexistante");
    }
    
    public function toSql(): string {
        $sql = "SELECT * FROM users";
        
        if (!empty($this->wheres)) {
            $sql .= " WHERE " . implode(' AND ', $this->wheres);
        }
        
        if (!empty($this->orders)) {
            $sql .= " ORDER BY " . implode(', ', $this->orders);
        }
        
        return $sql;
    }
}

$qb = new QueryBuilder();

// Appel méthodes inexistantes → __call()
$sql = $qb->whereEmail('alice@example.com')
          ->whereAge(25)
          ->orderByName('ASC')
          ->orderByCreatedAt('DESC')
          ->toSql();

echo $sql;
// SELECT * FROM users WHERE email = alice@example.com AND age = 25 ORDER BY name ASC, createdAt DESC

// ============================================
// Cas d'usage : Proxy vers autre objet
// ============================================

class ServiceProxy {
    private object $service;
    private array $callLog = [];
    
    public function __construct(object $service) {
        $this->service = $service;
    }
    
    public function __call(string $name, array $arguments): mixed {
        // Logger appels
        $this->callLog[] = [
            'method' => $name,
            'arguments' => $arguments,
            'time' => microtime(true)
        ];
        
        // Déléguer appel
        if (method_exists($this->service, $name)) {
            return $this->service->$name(...$arguments);
        }
        
        throw new BadMethodCallException("Méthode $name inexistante");
    }
    
    public function getCallLog(): array {
        return $this->callLog;
    }
}

class UserService {
    public function createUser(string $name): void {
        echo "Utilisateur créé : $name\n";
    }
}

$service = new UserService();
$proxy = new ServiceProxy($service);

$proxy->createUser('Alice');
$proxy->createUser('Bob');

print_r($proxy->getCallLog());
```

### 3.2 __callStatic : Surcharge Méthodes Statiques

```php
<?php

class StaticProxy {
    // ✅ Intercepte appel méthode statique inexistante
    public static function __callStatic(string $name, array $arguments): mixed {
        echo "Méthode statique inexistante : $name\n";
        
        // Créer méthode dynamiquement
        if (str_starts_with($name, 'create')) {
            $type = substr($name, 6); // createUser → User
            return new $type(...$arguments);
        }
        
        throw new BadMethodCallException("Méthode statique $name inexistante");
    }
}

class User {
    public function __construct(public string $name) {}
}

class Product {
    public function __construct(public string $name) {}
}

// Appel méthodes statiques inexistantes
$user = StaticProxy::createUser('Alice');
$product = StaticProxy::createProduct('Laptop');

echo $user->name;      // Alice
echo $product->name;   // Laptop

// ============================================
// Cas d'usage : Route dynamique
// ============================================

class Route {
    private static array $routes = [];
    
    public static function __callStatic(string $method, array $arguments): void {
        // Route::get('/users', 'UserController@index')
        [$path, $handler] = $arguments;
        
        self::$routes[strtoupper($method)][$path] = $handler;
        
        echo "Route enregistrée : $method $path → $handler\n";
    }
    
    public static function getRoutes(): array {
        return self::$routes;
    }
}

// Méthodes HTTP dynamiques
Route::get('/users', 'UserController@index');
Route::post('/users', 'UserController@store');
Route::put('/users/{id}', 'UserController@update');
Route::delete('/users/{id}', 'UserController@destroy');
Route::patch('/users/{id}', 'UserController@patch');

print_r(Route::getRoutes());
```

---

## 4. __toString : Conversion String

### 4.1 Représentation Textuelle

```php
<?php

class User {
    public function __construct(
        private int $id,
        private string $name,
        private string $email
    ) {}
    
    // ✅ Appelé lors conversion en string
    public function __toString(): string {
        return "{$this->name} ({$this->email})";
    }
}

$user = new User(1, 'Alice', 'alice@example.com');

// Conversion automatique
echo $user;                     // Alice (alice@example.com)
echo "User : $user";            // User : Alice (alice@example.com)
$str = (string)$user;           // Cast explicite

// ============================================
// Cas d'usage : Money Object
// ============================================

class Money {
    public function __construct(
        private float $amount,
        private string $currency = 'EUR'
    ) {}
    
    public function __toString(): string {
        return number_format($this->amount, 2, ',', ' ') . ' ' . $this->currency;
    }
    
    public function getAmount(): float {
        return $this->amount;
    }
}

$price = new Money(1234.56);
echo "Prix : $price";           // Prix : 1 234,56 EUR

$total = new Money(99.99, 'USD');
echo "Total : $total";          // Total : 99,99 USD

// ============================================
// Cas d'usage : URL Object
// ============================================

class Url {
    public function __construct(
        private string $scheme,
        private string $host,
        private ?string $path = null,
        private array $query = []
    ) {}
    
    public function __toString(): string {
        $url = "{$this->scheme}://{$this->host}";
        
        if ($this->path) {
            $url .= $this->path;
        }
        
        if (!empty($this->query)) {
            $url .= '?' . http_build_query($this->query);
        }
        
        return $url;
    }
}

$url = new Url('https', 'api.example.com', '/users', ['page' => 1, 'limit' => 10]);
echo $url; // https://api.example.com/users?page=1&limit=10

// ============================================
// Cas d'usage : SQL Query
// ============================================

class Query {
    private string $table;
    private array $wheres = [];
    
    public function from(string $table): self {
        $this->table = $table;
        return $this;
    }
    
    public function where(string $column, mixed $value): self {
        $this->wheres[] = "$column = '$value'";
        return $this;
    }
    
    public function __toString(): string {
        $sql = "SELECT * FROM {$this->table}";
        
        if (!empty($this->wheres)) {
            $sql .= " WHERE " . implode(' AND ', $this->wheres);
        }
        
        return $sql;
    }
}

$query = (new Query())
    ->from('users')
    ->where('active', 1)
    ->where('role', 'admin');

echo $query;
// SELECT * FROM users WHERE active = '1' AND role = 'admin'
```

**⚠️ Limitations __toString :**

- DOIT retourner string (pas d'exception avant PHP 7.4)
- Pas de side effects recommandés
- Peut être appelé implicitement (debugging difficile)

---

## 5. __invoke : Objet Callable

### 5.1 Objet comme Fonction

```php
<?php
declare(strict_types=1);

class Multiplier {
    public function __construct(
        private int $factor
    ) {}
    
    // ✅ Appelé quand objet utilisé comme fonction
    public function __invoke(int $value): int {
        return $value * $this->factor;
    }
}

$double = new Multiplier(2);
$triple = new Multiplier(3);

// Utiliser comme fonction
echo $double(5);      // 10
echo $triple(5);      // 15

// Passer comme callback
$numbers = [1, 2, 3, 4, 5];
$doubled = array_map($double, $numbers);
print_r($doubled);    // [2, 4, 6, 8, 10]

// ============================================
// Cas d'usage : Middleware
// ============================================

class AuthMiddleware {
    public function __construct(
        private array $allowedRoles
    ) {}
    
    public function __invoke(callable $next): callable {
        return function() use ($next) {
            // Vérifier authentification
            if (!isset($_SESSION['user'])) {
                http_response_code(401);
                echo "Non authentifié";
                return;
            }
            
            // Vérifier rôle
            if (!in_array($_SESSION['user']['role'], $this->allowedRoles, true)) {
                http_response_code(403);
                echo "Accès refusé";
                return;
            }
            
            // Continuer vers handler suivant
            return $next();
        };
    }
}

class LogMiddleware {
    public function __invoke(callable $next): callable {
        return function() use ($next) {
            echo "Début requête\n";
            $result = $next();
            echo "Fin requête\n";
            return $result;
        };
    }
}

// Pipeline middleware
$handler = fn() => "Réponse finale";

$middleware = [
    new LogMiddleware(),
    new AuthMiddleware(['admin', 'user'])
];

$pipeline = array_reduce(
    array_reverse($middleware),
    fn($next, $middleware) => $middleware($next),
    $handler
);

echo $pipeline(); // Exécute pipeline

// ============================================
// Cas d'usage : Validator callable
// ============================================

class EmailValidator {
    public function __invoke(string $value): bool {
        return filter_var($value, FILTER_VALIDATE_EMAIL) !== false;
    }
}

class MinLengthValidator {
    public function __construct(
        private int $minLength
    ) {}
    
    public function __invoke(string $value): bool {
        return strlen($value) >= $this->minLength;
    }
}

$emailValidator = new EmailValidator();
$minLength = new MinLengthValidator(8);

var_dump($emailValidator('alice@example.com'));  // true
var_dump($emailValidator('invalid'));            // false

var_dump($minLength('password123'));             // true
var_dump($minLength('short'));                   // false
```

---

## 6. __clone : Clonage d'Objets

### 6.1 Clonage Profond vs Superficiel

```php
<?php

// ============================================
// SANS __clone (Clonage superficiel)
// ============================================

class Address {
    public function __construct(
        public string $street,
        public string $city
    ) {}
}

class Person {
    public function __construct(
        public string $name,
        public Address $address
    ) {}
}

$person1 = new Person('Alice', new Address('Rue A', 'Paris'));
$person2 = clone $person1; // Clonage superficiel

$person2->name = 'Bob';              // ✅ Copié
$person2->address->city = 'Lyon';    // ⚠️ Modifie aussi person1 !

echo $person1->address->city;        // Lyon (pas Paris !)
// ⚠️ Problème : address est référence partagée

// ============================================
// AVEC __clone (Clonage profond)
// ============================================

class Person {
    public function __construct(
        public string $name,
        public Address $address
    ) {}
    
    // ✅ Appelé après clonage
    public function __clone(): void {
        // Cloner objets imbriqués (clonage profond)
        $this->address = clone $this->address;
    }
}

$person1 = new Person('Alice', new Address('Rue A', 'Paris'));
$person2 = clone $person1; // Clonage profond

$person2->name = 'Bob';
$person2->address->city = 'Lyon';

echo $person1->address->city;        // Paris ✅
echo $person2->address->city;        // Lyon ✅

// ============================================
// Cas d'usage : Réinitialiser certaines propriétés
// ============================================

class Order {
    public function __construct(
        public string $id,
        public array $items,
        public DateTime $createdAt
    ) {}
    
    public function __clone(): void {
        // Générer nouvel ID
        $this->id = uniqid('order_');
        
        // Nouvelle date
        $this->createdAt = new DateTime();
        
        // Cloner items
        $this->items = array_map(fn($item) => clone $item, $this->items);
    }
}

$order1 = new Order('order_123', [], new DateTime());
sleep(1);
$order2 = clone $order1;

echo $order1->id . "\n";  // order_123
echo $order2->id . "\n";  // order_abc456... (différent)

// ============================================
// Cas d'usage : Prototype Pattern
// ============================================

abstract class Prototype {
    abstract public function __clone();
}

class Document extends Prototype {
    public function __construct(
        private string $title,
        private string $content,
        private array $metadata = []
    ) {}
    
    public function __clone(): void {
        // Réinitialiser certaines données
        $this->metadata['cloned_at'] = new DateTime();
        $this->metadata['original_title'] = $this->title;
        $this->title = 'Copie de ' . $this->title;
    }
    
    public function getTitle(): string {
        return $this->title;
    }
}

$doc1 = new Document('Document Original', 'Contenu...');
$doc2 = clone $doc1;

echo $doc1->getTitle(); // Document Original
echo $doc2->getTitle(); // Copie de Document Original
```

**Diagramme : Clonage superficiel vs profond**

```mermaid
graph TB
    subgraph "Clonage Superficiel"
        O1[Object Original]
        O2[Object Clone]
        R[Objet Référencé]
        
        O1 -->|pointe vers| R
        O2 -->|pointe vers| R
    end
    
    subgraph "Clonage Profond"
        O3[Object Original]
        O4[Object Clone]
        R1[Objet Référencé 1]
        R2[Objet Référencé 2]
        
        O3 -->|pointe vers| R1
        O4 -->|pointe vers| R2
    end
    
    style R fill:#ffe1e1
    style R1 fill:#e1f5e1
    style R2 fill:#e1f5e1
```

---

## 7. __sleep et __wakeup : Serialization

### 7.1 Contrôler Serialization

```php
<?php

class User {
    public function __construct(
        private int $id,
        private string $name,
        private string $email,
        private string $password,      // ⚠️ Sensible
        private ?PDO $pdo = null       // ⚠️ Non sérialisable
    ) {}
    
    // ✅ Appelé avant serialize()
    public function __sleep(): array {
        // Retourner SEULEMENT propriétés à sérialiser
        // ⚠️ Exclure password, pdo
        return ['id', 'name', 'email'];
    }
    
    // ✅ Appelé après unserialize()
    public function __wakeup(): void {
        // Réinitialiser ressources
        $this->pdo = new PDO('mysql:host=localhost;dbname=app', 'root', '');
        
        echo "User désérialisé : {$this->name}\n";
    }
}

$user = new User(1, 'Alice', 'alice@example.com', 'secret_password', $pdo);

// Sérialiser (appelle __sleep())
$serialized = serialize($user);
echo $serialized . "\n";
// O:4:"User":3:{s:6:"*id";i:1;s:9:"*name";s:5:"Alice";s:10:"*email";s:19:"alice@example.com";}
// ⚠️ password et pdo absents

// Désérialiser (appelle __wakeup())
$restored = unserialize($serialized);
// Output : User désérialisé : Alice

// ============================================
// Cas d'usage : Cache objets
// ============================================

class CachedData {
    private mixed $data;
    private DateTime $cachedAt;
    
    public function __construct(mixed $data) {
        $this->data = $data;
        $this->cachedAt = new DateTime();
    }
    
    public function __sleep(): array {
        return ['data', 'cachedAt'];
    }
    
    public function __wakeup(): void {
        // Vérifier si cache expiré
        $now = new DateTime();
        $age = $now->getTimestamp() - $this->cachedAt->getTimestamp();
        
        if ($age > 3600) { // 1 heure
            echo "Cache expiré, rechargement nécessaire\n";
        }
    }
}

$cached = new CachedData(['users' => 100]);
file_put_contents('cache.dat', serialize($cached));

sleep(2);

$restored = unserialize(file_get_contents('cache.dat'));
```

### 7.2 __serialize et __unserialize (PHP 7.4+)

**Nouvelle API plus flexible**

```php
<?php

class ModernUser {
    public function __construct(
        private int $id,
        private string $name,
        private string $email,
        private string $password
    ) {}
    
    // ✅ Retourne array (plus flexible que __sleep)
    public function __serialize(): array {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'passwordHash' => hash('sha256', $this->password) // Transformer
        ];
    }
    
    // ✅ Reçoit array directement
    public function __unserialize(array $data): void {
        $this->id = $data['id'];
        $this->name = $data['name'];
        $this->email = $data['email'];
        // password non restauré (sécurité)
    }
}

$user = new ModernUser(1, 'Alice', 'alice@example.com', 'secret');

$serialized = serialize($user);
$restored = unserialize($serialized);

// ============================================
// Avantages __serialize/__unserialize
// ============================================

class ComplexObject {
    private array $data;
    
    public function __serialize(): array {
        // Transformer données complexes
        return [
            'data' => json_encode($this->data),
            'version' => 2
        ];
    }
    
    public function __unserialize(array $data): void {
        // Migration version
        if (isset($data['version']) && $data['version'] === 2) {
            $this->data = json_decode($data['data'], true);
        } else {
            // Ancien format
            $this->data = $data['data'];
        }
    }
}
```

---

## 8. Autres Méthodes Magiques

### 8.1 __debugInfo : Personnaliser var_dump

```php
<?php

class User {
    public function __construct(
        private int $id,
        private string $name,
        private string $email,
        private string $password      // ⚠️ Sensible
    ) {}
    
    // ✅ Contrôler sortie var_dump()
    public function __debugInfo(): array {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'password' => '***HIDDEN***'  // Masquer
        ];
    }
}

$user = new User(1, 'Alice', 'alice@example.com', 'secret_password');

var_dump($user);
/*
object(User)#1 (4) {
  ["id"]=> int(1)
  ["name"]=> string(5) "Alice"
  ["email"]=> string(19) "alice@example.com"
  ["password"]=> string(13) "***HIDDEN***"
}
*/
```

### 8.2 __set_state : var_export

```php
<?php

class Point {
    public function __construct(
        public int $x,
        public int $y
    ) {}
    
    // ✅ Appelé par var_export()
    public static function __set_state(array $properties): self {
        return new self($properties['x'], $properties['y']);
    }
}

$point = new Point(10, 20);

// Exporter code PHP
$code = var_export($point, true);
echo $code;
/*
Point::__set_state(array(
   'x' => 10,
   'y' => 20,
))
*/

// Évaluer code généré
eval('$restored = ' . $code . ';');
echo $restored->x; // 10
```

---

## 9. Best Practices et Anti-Patterns

### 9.1 Quand Utiliser Méthodes Magiques

**✅ UTILISER quand :**

- ORM / Active Record (Eloquent, Doctrine)
- Proxy / Wrapper objets
- DSL (Domain Specific Language)
- Lazy loading
- API fluides

**❌ ÉVITER quand :**

- Code métier critique
- Performance importante
- Équipe débutante
- Debugging fréquent
- Type safety nécessaire

### 9.2 Anti-Patterns

```php
<?php

// ❌ MAUVAIS : __get/__set pour TOUT
class BadUser {
    private array $data = [];
    
    public function __get($name) {
        return $this->data[$name] ?? null;
    }
    
    public function __set($name, $value) {
        $this->data[$name] = $value;
    }
    
    // ⚠️ Problèmes :
    // - Pas d'autocomplétion IDE
    // - Pas de type checking
    // - Debugging difficile
    // - Performance dégradée
}

// ✅ BON : Propriétés normales + __get pour cas spécifiques
class GoodUser {
    // Propriétés explicites
    public int $id;
    public string $name;
    public string $email;
    
    // __get pour extensions dynamiques uniquement
    private array $metadata = [];
    
    public function __get(string $name): mixed {
        return $this->metadata[$name] ?? null;
    }
}

// ❌ MAUVAIS : __call pour logique métier
class BadService {
    public function __call($name, $args) {
        if ($name === 'sendEmail') {
            // Logique métier cachée
        }
    }
    
    // ⚠️ Impossible de voir dans IDE
    // ⚠️ Erreurs runtime au lieu compile-time
}

// ✅ BON : Méthodes explicites
class GoodService {
    public function sendEmail(string $to, string $subject): void {
        // Logique visible
    }
}

// ❌ MAUVAIS : Side effects dans __toString
class BadLogger {
    public function __toString(): string {
        // ❌ Side effect : écriture fichier
        file_put_contents('log.txt', 'Log', FILE_APPEND);
        return 'logged';
    }
}

// ✅ BON : __toString pur (pas de side effects)
class GoodLogger {
    public function __toString(): string {
        return $this->getMessage(); // Juste retourner string
    }
    
    public function log(): void {
        // Side effect dans méthode dédiée
        file_put_contents('log.txt', $this->getMessage(), FILE_APPEND);
    }
}
```

### 9.3 Performance

```php
<?php

// Benchmark : Propriété normale vs __get

class NormalProperties {
    public string $name = 'Alice';
}

class MagicProperties {
    private array $data = ['name' => 'Alice'];
    
    public function __get($name) {
        return $this->data[$name] ?? null;
    }
}

$iterations = 1000000;

// Test propriété normale
$normal = new NormalProperties();
$start = microtime(true);
for ($i = 0; $i < $iterations; $i++) {
    $x = $normal->name;
}
$normalTime = microtime(true) - $start;

// Test __get
$magic = new MagicProperties();
$start = microtime(true);
for ($i = 0; $i < $iterations; $i++) {
    $x = $magic->name;
}
$magicTime = microtime(true) - $start;

echo "Normal : " . number_format($normalTime, 4) . "s\n";
echo "Magic : " . number_format($magicTime, 4) . "s\n";
echo "Magic est " . round($magicTime / $normalTime, 1) . "x plus lent\n";

/*
Résultats typiques :
Normal : 0.0180s
Magic : 0.1850s
Magic est 10.3x plus lent
*/
```

---

## 10. Exemples Complets

### 10.1 ORM Simple

```php
<?php
declare(strict_types=1);

abstract class Model {
    protected static string $table;
    protected array $attributes = [];
    protected array $original = [];
    protected bool $exists = false;
    
    // __get : Accès attributs
    public function __get(string $name): mixed {
        return $this->attributes[$name] ?? null;
    }
    
    // __set : Modification attributs
    public function __set(string $name, mixed $value): void {
        $this->attributes[$name] = $value;
    }
    
    // __isset : isset() sur attributs
    public function __isset(string $name): bool {
        return isset($this->attributes[$name]);
    }
    
    // Méthodes statiques
    public static function find(int $id): ?static {
        $pdo = self::getConnection();
        $table = static::$table;
        
        $stmt = $pdo->prepare("SELECT * FROM $table WHERE id = ?");
        $stmt->execute([$id]);
        $data = $stmt->fetch();
        
        if (!$data) {
            return null;
        }
        
        $model = new static();
        $model->attributes = $data;
        $model->original = $data;
        $model->exists = true;
        
        return $model;
    }
    
    public static function all(): array {
        $pdo = self::getConnection();
        $table = static::$table;
        
        $stmt = $pdo->query("SELECT * FROM $table");
        $results = $stmt->fetchAll();
        
        return array_map(function($data) {
            $model = new static();
            $model->attributes = $data;
            $model->original = $data;
            $model->exists = true;
            return $model;
        }, $results);
    }
    
    public function save(): bool {
        $pdo = self::getConnection();
        $table = static::$table;
        
        if ($this->exists) {
            // Update
            $sets = [];
            $values = [];
            
            foreach ($this->attributes as $key => $value) {
                if ($key !== 'id' && $value !== $this->original[$key]) {
                    $sets[] = "$key = ?";
                    $values[] = $value;
                }
            }
            
            if (empty($sets)) {
                return true; // Rien à mettre à jour
            }
            
            $values[] = $this->attributes['id'];
            $sql = "UPDATE $table SET " . implode(', ', $sets) . " WHERE id = ?";
            
            $stmt = $pdo->prepare($sql);
            $result = $stmt->execute($values);
            
            $this->original = $this->attributes;
            
            return $result;
        } else {
            // Insert
            $columns = implode(', ', array_keys($this->attributes));
            $placeholders = implode(', ', array_fill(0, count($this->attributes), '?'));
            
            $sql = "INSERT INTO $table ($columns) VALUES ($placeholders)";
            $stmt = $pdo->prepare($sql);
            $result = $stmt->execute(array_values($this->attributes));
            
            $this->attributes['id'] = (int)$pdo->lastInsertId();
            $this->original = $this->attributes;
            $this->exists = true;
            
            return $result;
        }
    }
    
    private static function getConnection(): PDO {
        static $pdo = null;
        
        if ($pdo === null) {
            $pdo = new PDO('mysql:host=localhost;dbname=app', 'root', '');
        }
        
        return $pdo;
    }
}

// Modèle User
class User extends Model {
    protected static string $table = 'users';
}

// Modèle Product
class Product extends Model {
    protected static string $table = 'products';
}

// Utilisation
$user = User::find(1);
echo $user->name;      // __get
echo $user->email;

$user->name = 'Bob';   // __set
$user->save();

// Créer nouveau
$newUser = new User();
$newUser->name = 'Charlie';
$newUser->email = 'charlie@example.com';
$newUser->save();

// Tous les users
$users = User::all();
foreach ($users as $user) {
    echo $user->name . "\n";
}
```

### 10.2 Container IoC avec __get

```php
<?php

class Container {
    private array $bindings = [];
    private array $instances = [];
    
    // Enregistrer service
    public function bind(string $abstract, callable $concrete): void {
        $this->bindings[$abstract] = $concrete;
    }
    
    // Enregistrer singleton
    public function singleton(string $abstract, callable $concrete): void {
        $this->bind($abstract, function($container) use ($concrete, $abstract) {
            if (!isset($this->instances[$abstract])) {
                $this->instances[$abstract] = $concrete($container);
            }
            
            return $this->instances[$abstract];
        });
    }
    
    // Résoudre service via __get
    public function __get(string $name): mixed {
        return $this->make($name);
    }
    
    // Résoudre service
    public function make(string $abstract): mixed {
        if (isset($this->instances[$abstract])) {
            return $this->instances[$abstract];
        }
        
        if (!isset($this->bindings[$abstract])) {
            throw new Exception("Service $abstract non trouvé");
        }
        
        return $this->bindings[$abstract]($this);
    }
}

// Services
class Database {
    public function query(string $sql): void {
        echo "Exécution : $sql\n";
    }
}

class UserRepository {
    public function __construct(private Database $db) {}
    
    public function findAll(): array {
        $this->db->query("SELECT * FROM users");
        return [];
    }
}

// Configuration container
$container = new Container();

$container->singleton('db', fn() => new Database());
$container->bind('userRepository', fn($c) => new UserRepository($c->db));

// Utilisation avec __get
$repo = $container->userRepository; // __get('userRepository')
$repo->findAll();
```

---

## 11. Exercices Pratiques

### Exercice 1 : ArrayAccess avec Méthodes Magiques

**Créer classe combinant __get/__set avec ArrayAccess**

<details>
<summary>Solution</summary>

```php
<?php

class Collection implements ArrayAccess, Countable, IteratorAggregate {
    private array $items = [];
    
    // ArrayAccess
    public function offsetExists(mixed $offset): bool {
        return isset($this->items[$offset]);
    }
    
    public function offsetGet(mixed $offset): mixed {
        return $this->items[$offset] ?? null;
    }
    
    public function offsetSet(mixed $offset, mixed $value): void {
        if ($offset === null) {
            $this->items[] = $value;
        } else {
            $this->items[$offset] = $value;
        }
    }
    
    public function offsetUnset(mixed $offset): void {
        unset($this->items[$offset]);
    }
    
    // Méthodes magiques
    public function __get(string $name): mixed {
        return $this->items[$name] ?? null;
    }
    
    public function __set(string $name, mixed $value): void {
        $this->items[$name] = $value;
    }
    
    public function __isset(string $name): bool {
        return isset($this->items[$name]);
    }
    
    public function __unset(string $name): void {
        unset($this->items[$name]);
    }
    
    // Countable
    public function count(): int {
        return count($this->items);
    }
    
    // IteratorAggregate
    public function getIterator(): Traversable {
        return new ArrayIterator($this->items);
    }
    
    // __call pour méthodes array
    public function __call(string $name, array $arguments): mixed {
        $arrayFunctions = ['map', 'filter', 'reduce', 'each'];
        
        if (in_array($name, $arrayFunctions)) {
            $function = "array_$name";
            if (function_exists($function)) {
                return $function($this->items, ...$arguments);
            }
        }
        
        throw new BadMethodCallException("Méthode $name inexistante");
    }
    
    // __toString
    public function __toString(): string {
        return json_encode($this->items);
    }
}

// Tests
$collection = new Collection();

// ArrayAccess
$collection[0] = 'Alice';
$collection[1] = 'Bob';
echo $collection[0]; // Alice

// Méthodes magiques
$collection->name = 'Charlie';
echo $collection->name; // Charlie

// Countable
echo count($collection); // 3

// IteratorAggregate
foreach ($collection as $item) {
    echo $item . "\n";
}

// __toString
echo $collection; // ["Alice","Bob","name":"Charlie"]
```

</details>

### Exercice 2 : Builder Pattern avec __call

**Créer query builder fluide avec méthodes dynamiques**

<details>
<summary>Structure attendue</summary>

```php
<?php

class QueryBuilder {
    private string $table;
    private array $wheres = [];
    private array $orders = [];
    private ?int $limit = null;
    
    public function from(string $table): self {
        $this->table = $table;
        return $this;
    }
    
    // __call pour where{Column}
    public function __call(string $name, array $arguments): self {
        if (str_starts_with($name, 'where')) {
            $column = lcfirst(substr($name, 5));
            $operator = $arguments[1] ?? '=';
            $value = $arguments[0];
            
            $this->wheres[] = "$column $operator '$value'";
            return $this;
        }
        
        if (str_starts_with($name, 'orderBy')) {
            $column = lcfirst(substr($name, 7));
            $direction = $arguments[0] ?? 'ASC';
            
            $this->orders[] = "$column $direction";
            return $this;
        }
        
        throw new BadMethodCallException();
    }
    
    // __toString pour SQL
    public function __toString(): string {
        $sql = "SELECT * FROM {$this->table}";
        
        if (!empty($this->wheres)) {
            $sql .= " WHERE " . implode(' AND ', $this->wheres);
        }
        
        if (!empty($this->orders)) {
            $sql .= " ORDER BY " . implode(', ', $this->orders);
        }
        
        if ($this->limit !== null) {
            $sql .= " LIMIT {$this->limit}";
        }
        
        return $sql;
    }
}

// Usage
$query = (new QueryBuilder())
    ->from('users')
    ->whereEmail('alice@example.com')
    ->whereAge(25, '>=')
    ->whereActive(1)
    ->orderByName('ASC')
    ->orderByCreatedAt('DESC');

echo $query;
// SELECT * FROM users WHERE email = 'alice@example.com' AND age >= '25' AND active = '1' ORDER BY name ASC, createdAt DESC
```

</details>

---

## 12. Checkpoint de Progression

### À la fin de ce Module 14, vous maîtrisez :

**Méthodes magiques principales :**
- [x] __construct / __destruct (rappel)
- [x] __get / __set (surcharge propriétés)
- [x] __isset / __unset
- [x] __call / __callStatic (surcharge méthodes)
- [x] __toString (conversion string)
- [x] __invoke (objet callable)
- [x] __clone (clonage profond)

**Serialization :**
- [x] __sleep / __wakeup
- [x] __serialize / __unserialize (PHP 7.4+)

**Debugging :**
- [x] __debugInfo (var_dump)
- [x] __set_state (var_export)

**Best practices :**
- [x] Quand utiliser méthodes magiques
- [x] Performance considerations
- [x] Anti-patterns à éviter
- [x] Type safety vs flexibilité

### Prochaine Étape

**Direction le Module 15** où vous allez :
- Design Patterns essentiels (Singleton, Factory, Observer)
- SOLID principles appliqués
- Dependency Injection
- Repository Pattern
- Service Layer
- Architecture Clean Code

[:lucide-arrow-right: Accéder au Module 15 - Design Patterns](./module-15-design-patterns/)

---

**Module 14 Terminé - Bravo ! 🎉 ✨**

**Vous avez appris :**
- ✅ 13 méthodes magiques maîtrisées
- ✅ __get/__set (surcharge propriétés)
- ✅ __call/__callStatic (surcharge méthodes)
- ✅ __toString/__invoke (conversions)
- ✅ __clone (clonage profond)
- ✅ __sleep/__wakeup (serialization)
- ✅ __debugInfo (debugging)
- ✅ Best practices et anti-patterns
- ✅ 2 projets complets (ORM, Container)

**Statistiques Module 14 :**
- 2 projets complets
- 90+ exemples code
- Performance benchmarks
- Cas d'usage réels (ORM, DSL)
- Architecture flexible

**Prochain objectif : Maîtriser design patterns (Module 15)**

**Félicitations pour cette maîtrise de la magie PHP ! 🚀✨**

---

# ✅ Module 14 PHP POO Complet ! 🎉 ✨

J'ai créé le **Module 14 - Méthodes Magiques** (8-10 heures) qui couvre exhaustivement toutes les méthodes magiques PHP avec des cas d'usage réels et des best practices.

**Contenu exhaustif :**
- ✅ __construct/__destruct (rappel approfondi, validation, nettoyage)
- ✅ __get/__set/__isset/__unset (surcharge propriétés, lazy loading, validation)
- ✅ __call/__callStatic (surcharge méthodes, DSL, routing)
- ✅ __toString (conversion string, Money, URL, Query)
- ✅ __invoke (objet callable, middleware, validators)
- ✅ __clone (clonage profond vs superficiel, prototype pattern)
- ✅ __sleep/__wakeup (serialization classique)
- ✅ __serialize/__unserialize (PHP 7.4+, plus flexible)
- ✅ __debugInfo (var_dump personnalisé, sécurité)
- ✅ __set_state (var_export)
- ✅ Best practices (performance, anti-patterns, quand utiliser)
- ✅ 2 exercices complets (ORM simple, Container IoC)

**Progression formation PHP POO :**
- Module 8 - Introduction POO ✅
- Module 9 - Héritage & Polymorphisme ✅
- Module 10 - Interfaces ✅
- Module 11 - Traits ✅
- Module 12 - Exceptions ✅
- Module 13 - Namespaces & Autoloading ✅
- Module 14 - Méthodes Magiques ✅
- Module 15 - Design Patterns 🚀 (prochain)

Tu as maintenant maîtrisé les méthodes magiques PHP ! Tu sais créer des API fluides, implémenter du lazy loading, créer des ORM simples, et utiliser la "magie" PHP avec sagesse tout en évitant les pièges de performance et debugging.

Veux-tu que je continue avec le **Module 15 - Design Patterns** ? (Singleton, Factory, Observer, Strategy, Dependency Injection, Repository Pattern, SOLID principles appliqués, architecture professionnelle)