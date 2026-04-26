---
description: "Les 5 principes fondamentaux pour concevoir une architecture Orientée Objet maintenable et évolutive."
icon: lucide/book-open-check
tags: ["SOLID", "POO", "ARCHITECTURE", "CLEAN CODE", "PRINCIPES"]
---

# Les Principes S.O.L.I.D.

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="45 - 60 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Les principes SOLID sont les règles de sécurité d'un chantier d'ingénierie. Ils garantissent que si vous ajoutez un étage à votre bâtiment (votre application) dans deux ans, les fondations ne s'effondreront pas sous le nouveau poids._

!!! quote "Éviter la dette technique"
    _Les principes SOLID ont été popularisés par Robert C. Martin ("Uncle Bob") dans les années 2000. Ils représentent les 5 commandements de la Programmation Orientée Objet (POO). Si vous ignorez ces principes, votre application fonctionnera, mais au fur et à mesure qu'elle grandira, le code deviendra rigide, fragile et impossible à modifier sans casser autre chose. SOLID est la clé pour créer une architecture **maintenable**, **testable** et **évolutive**._

---

## 1. [S]ingle Responsibility Principle (SRP)
*Principe de Responsabilité Unique*

> **"Une classe ne doit avoir qu'une seule raison de changer."**

Chaque classe (ou module) doit avoir une seule et unique responsabilité dans le logiciel. Si une classe fait trop de choses, la modification d'une de ses fonctionnalités risque de corrompre les autres.

**L'Anti-Pattern (Mauvais) :**
```php
class User {
    public function calculateTaxes() { /* ... */ }
    public function generatePdfReport() { /* ... */ }
    public function saveToDatabase() { /* ... */ }
}
```
*Ici, la classe gère la logique métier (Taxes), l'affichage (PDF) et la persistance (BDD). Si le format du PDF change, on doit modifier la classe User. C'est une erreur.*

**La Solution (Bon) :**
```php
class User {
    // Ne gère que l'état de l'utilisateur
}

class TaxCalculator {
    public function calculateFor(User $user) { /* ... */ }
}

class UserReportGenerator {
    public function generatePdf(User $user) { /* ... */ }
}
```

---

## 2. [O]pen/Closed Principle (OCP)
*Principe Ouvert/Fermé*

> **"Les entités logicielles doivent être ouvertes à l'extension, mais fermées à la modification."**

Vous devriez pouvoir ajouter de nouvelles fonctionnalités à votre application *sans* avoir à modifier le code source existant (car modifier le code existant implique de devoir le retester entièrement).

**L'Anti-Pattern (Mauvais) :**
```php
class AreaCalculator {
    public function calculateArea(array $shapes) {
        $area = 0;
        foreach ($shapes as $shape) {
            if ($shape instanceof Square) {
                $area += $shape->width * $shape->width;
            } elseif ($shape instanceof Circle) {
                $area += pi() * $shape->radius * $shape->radius;
            }
            // Si on ajoute un Triangle, on DOIT modifier cette classe !
        }
        return $area;
    }
}
```

**La Solution (Bon) :**
Utiliser le polymorphisme et les interfaces.
```php
interface Shape {
    public function area(): float;
}

class Square implements Shape {
    public function area(): float { return $this->width * $this->width; }
}

class Circle implements Shape {
    public function area(): float { return pi() * $this->radius * $this->radius; }
}

class AreaCalculator {
    public function calculateArea(array $shapes) {
        $area = 0;
        foreach ($shapes as $shape) {
            $area += $shape->area(); // Le calculateur ne changera JAMAIS, même avec 100 nouvelles formes.
        }
        return $area;
    }
}
```

---

## 3. [L]iskov Substitution Principle (LSP)
*Principe de Substitution de Liskov*

> **"Les objets d'un programme doivent pouvoir être remplacés par des instances de leurs sous-types sans altérer la cohérence du programme."**

Si la classe B hérite de la classe A, alors vous devriez pouvoir passer B partout où A est attendu, sans casser l'application. L'enfant ne doit pas modifier le contrat imposé par le parent (ex: retourner un string là où le parent retournait un integer, ou lever une exception non prévue).

**L'Anti-Pattern (Le carré n'est pas un rectangle) :**
```php
class Rectangle {
    public function setWidth($w) { $this->width = $w; }
    public function setHeight($h) { $this->height = $h; }
}

class Square extends Rectangle {
    // Un carré DOIT avoir des côtés égaux, on modifie donc le comportement
    public function setWidth($w) { $this->width = $w; $this->height = $w; }
    public function setHeight($h) { $this->width = $h; $this->height = $h; }
}

// Fonction attendue :
function testRectangle(Rectangle $r) {
    $r->setWidth(5);
    $r->setHeight(4);
    // On s'attend à une aire de 20. Si on passe un Square, l'aire sera 16 !
    // Le principe de Liskov est violé.
}
```
*Leçon : L'héritage ne doit être utilisé que pour des comportements strictement compatibles. Si les règles changent, n'utilisez pas l'héritage.*

---

## 4. [I]nterface Segregation Principle (ISP)
*Principe de Ségrégation des Interfaces*

> **"Un client ne devrait jamais être forcé d'implémenter une interface qu'il n'utilise pas."**

Il vaut mieux avoir plusieurs petites interfaces spécifiques qu'une seule grosse interface "fourre-tout".

**L'Anti-Pattern (Mauvais) :**
```php
interface Worker {
    public function work();
    public function eat();
    public function sleep();
}

class Robot implements Worker {
    public function work() { /* ... */ }
    public function eat() { throw new Exception("Un robot ne mange pas !"); }
    public function sleep() { throw new Exception("Un robot ne dort pas !"); }
}
```

**La Solution (Bon) :**
```php
interface Workable {
    public function work();
}

interface Feedable {
    public function eat();
}

class Human implements Workable, Feedable {
    // Fait les deux
}

class Robot implements Workable {
    // Ne fait que le travail
}
```

---

## 5. [D]ependency Inversion Principle (DIP)
*Principe d'Inversion des Dépendances*

> **"Les modules de haut niveau ne doivent pas dépendre des modules de bas niveau. Tous deux doivent dépendre d'abstractions (interfaces)."**

C'est sans doute le principe le plus vital pour les frameworks modernes (comme l'Injection de Dépendances dans Laravel). Votre logique métier principale ne doit pas dépendre directement d'un driver MySQL ou d'une API de paiement Stripe.

**L'Anti-Pattern (Fortement couplé) :**
```php
class MySQLConnection {
    public function connect() { return "Database Connection"; }
}

class PasswordReminder {
    private $dbConnection;

    public function __construct(MySQLConnection $dbConnection) {
        $this->dbConnection = $dbConnection;
    }
}
```
*Si vous décidez de passer de MySQL à PostgreSQL, vous devez réécrire la classe PasswordReminder.*

**La Solution (Inversion de Contrôle) :**
```php
interface DBConnectionInterface {
    public function connect();
}

class MySQLConnection implements DBConnectionInterface {
    public function connect() { /* ... */ }
}

class PostgreSQLConnection implements DBConnectionInterface {
    public function connect() { /* ... */ }
}

class PasswordReminder {
    private $dbConnection;

    // Le module haut niveau dépend de l'Interface, pas de l'implémentation
    public function __construct(DBConnectionInterface $dbConnection) {
        $this->dbConnection = $dbConnection;
    }
}
```
*Désormais, `PasswordReminder` se fiche de la base de données utilisée, tant qu'elle respecte le contrat de l'interface. C'est l'essence même du développement flexible.*

## Conclusion
!!! quote "Ce qu'il faut retenir"
    La maîtrise du concept de solid est un pilier de l'informatique fondamentale. Au-delà de la syntaxe technique, c'est cette compréhension théorique qui différencie un simple technicien d'un véritable ingénieur capable de concevoir des systèmes robustes et maintenables.

Appliquer les 5 principes SOLID simultanément au début de votre carrière est très complexe et peut mener à de la "sur-ingénierie". Commencez par maîtriser le principe de **Responsabilité Unique (S)** et d'**Inversion des Dépendances (D)** : ce sont ceux qui auront le plus d'impact immédiat sur la qualité de vos projets.
