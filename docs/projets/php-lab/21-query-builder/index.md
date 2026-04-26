---
description: "Projet Pratique POO : Développer un constructeur de requêtes SQL maison (Query Builder fluant) en injectant les capacités SELECT, WHERE, et ORDER BY via des Traits modulaires."
icon: lucide/database
tags: ["PHP", "POO", "TRAITS", "BDD", "SQL"]
status: stable
---

# Projet 21 : Query Builder SQL (Traits)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Le Query Builder est comme un traducteur personnel. Au lieu d'écrire des requêtes SQL complexes à la main au risque de faire une faute de frappe, vous utilisez des méthodes PHP élégantes qui construisent la requête SQL parfaite et sécurisée en arrière-plan._

!!! quote "Le Pitch"
    Écrire des requêtes MySQL en dur n'est pas fiable en programmation moderne. Les frameworks comme Laravel (Eloquent) construisent ces chaînes SQL par concaténation intelligente d'objets, ce que l'on appelle un **Query Builder**.
    Un *Pattern Builder* fluide va ressembler à ça : `$query->select('id')->where('age', '>', 18)->toSql();`

!!! abstract "Objectifs Pédagogiques"
    1.  **Architecture Fragmentée** : Comprendre pourquoi isoler la logique du `LIMIT`, du `WHERE` et du `ORDER` dans différents Traits permet un code propre.
    2.  **Chaînage de Méthodes** : Retourner l'instance courante `return $this;` à la fin d'une fonction pour permettre d'enchainer les appels (`Fluent Design Pattern`).
    3.  **Concaténation Master** : Implémenter le fameux compileur final `toSql()` qui assemble le puzzle des modules invoqués.

## 1. Séparer l'Agencement des Requêtes

Les `Traits` sont parfaits ici pour représenter les clauses indépendantes du langage SQL. Chaque `Trait` aura son propre tableau pour retenir ce qu'on a demandé.

```php
<?php
declare(strict_types=1);

// --- LE TRAIT DU SELECT ---
trait Selectable {
    protected array $selects = ['*']; // Par défaut : SELECT *
    
    // Le "splat operator" (...) permet de passer un nombre infini d'arguments !
    public function select(string ...$columns): self {
        $this->selects = $columns;
        return $this; // Indispensable pour enchaîner les flèches (->)
    }
}

// --- LE TRAIT DES CONDITIONS ---
trait Whereable {
    protected array $wheres = [];
    
    public function where(string $column, string $operator, mixed $value): self {
        // Enregistre compactement les 3 variables dans le tableau
        $this->wheres[] = compact('column', 'operator', 'value');
        return $this;
    }
}

// --- LE TRAIT DU TRI ---
trait Orderable {
    protected array $orders = [];
    
    public function orderBy(string $column, string $direction = 'ASC'): self {
        // Validation basique anti-injection SQL sur le ORDER
        $direction = strtoupper($direction);
        if (!in_array($direction, ['ASC', 'DESC'])) {
            $direction = 'ASC';
        }
        
        $this->orders[] = compact('column', 'direction');
        return $this;
    }
}

// --- LE TRAIT DE PAGINATION ---
trait Limitable {
    protected ?int $limit = null;
    protected ?int $offset = null;
    
    public function limit(int $limit): self {
        $this->limit = $limit;
        return $this;
    }
    
    public function offset(int $offset): self {
        $this->offset = $offset;
        return $this;
    }
}
?>
```

## 2. Le Moteur Principal d'Assemblage

Créons la classe `QueryBuilder` (celle que nous l'instancierons réellement). Elle importe tous les traits et procède à la confection de la requête au tout dernier moment, quand on lance `toSql()`.

```php
<?php
declare(strict_types=1);

class QueryBuilder {
    
    // L'absorption complète des 4 capacités distinctes !
    use Selectable, Whereable, Orderable, Limitable;
    
    private string $table;
    
    // Au démarrage, on exige juste de savoir quelle table est visée
    public function __construct(string $table) {
        $this->table = $table;
    }
    
    /**
     * Le Compileur FINAL
     * Assemble prudemment toutes les fractions SQL des Traits
     */
    public function toSql(): string {
        
        // 1. SELECT
        $sql = 'SELECT ' . implode(', ', $this->selects);
        
        // 2. FROM
        $sql .= " FROM {$this->table}";
        
        // 3. WHERE
        if (!empty($this->wheres)) {
            // Transforme le tableau [column, operator, value] en chaîne : "age >= ?"
            // Note: En mode préparé PDO, les valeurs REELLES ne sont pas injectées en dur 
            // pour empêcher le piratage SQL Injection ! On met donc des " ? ".
            $conditions = array_map(
                fn($w) => "{$w['column']} {$w['operator']} ?",
                $this->wheres
            );
            $sql .= ' WHERE ' . implode(' AND ', $conditions);
        }
        
        // 4. ORDER BY
        if (!empty($this->orders)) {
            $orders = array_map(
                fn($o) => "{$o['column']} {$o['direction']}",
                $this->orders
            );
            $sql .= ' ORDER BY ' . implode(', ', $orders);
        }
        
        // 5. LIMIT / OFFSET
        if ($this->limit !== null) {
            $sql .= " LIMIT {$this->limit}";
        }
        if ($this->offset !== null) {
            $sql .= " OFFSET {$this->offset}";
        }
        
        return $sql;
    }
}
?>
```

## 3. L'Essai en Action

Testons la puissance du `Fluent Pattern` rendu incroyablement modulaire par les Traits.

```php
<?php
// require le builder contenant tous vos traits...

$qb = new QueryBuilder('users');

$sqlSecureString = $qb
    ->select('id', 'name', 'email', 'avatar_url')
    ->where('is_active', '=', 1)
    ->where('age', '>=', 18)
    ->where('role', '=', 'Admin')
    ->orderBy('created_at', 'DESC')
    ->limit(10)
    ->offset(20)
    ->toSql(); // Le compileur final lance la machine de concatenation !

// Affichage pur pour vérifier la chaîne SQL Générée :
echo "<h2>🎯 REQUÊTE COMPILÉE (PROTECTION INJECTION INCLUSE) :</h2>\n";
echo "<code>" . $sqlSecureString . "</code>";

// Résultat final renvoyé par le script :
// SELECT id, name, email, avatar_url FROM users WHERE is_active = ? AND age >= ? AND role = ? ORDER BY created_at DESC LIMIT 10 OFFSET 20
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">L'avantage des Traits est la <strong>Séparation Mathématique pure</strong> :</p>
  <ul class="space-y-4 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">1</span>
      <span class="text-gray-700">Imaginez une erreur dans votre code de pagination Limit. Vous savez EXACTEMENT où chercher : Dans le <code>trait Limitable</code>, et non pas perdus au milieu des 400 lignes de la Classe Générale <code>QueryBuilder</code> pleine de WHERE et de ORDER. C'est l'essence du Code Propre.</span>
    </li>
  </ul>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
