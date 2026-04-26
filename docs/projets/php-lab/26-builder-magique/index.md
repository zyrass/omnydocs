---
description: "Projet Pratique POO : Détourner l'intercepteur magique PHP (__call) pour forger des méthodes de base de données fluides et dynamiques à la volée (ex: whereAge, whereEmail)."
icon: lucide/wand-2
tags: ["PHP", "POO", "MAGIC", "BDD", "BUILDER"]
status: stable
---

# Projet 26 : Query Builder Magique

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    Lorsqu'on utilise un Framework comme Laravel (Eloquent ORM), on tape frénétiquement `$user->whereEmail('alice@test.com')->whereAge(25)->get()`.
    Pourtant, si vous ouvrez le code source de Laravel, vous ne trouverez AUCUNE méthode nommée `whereEmail()` ni `whereAge()`. Comment est-ce possible ?
    C'est le pouvoir mystique de la méthode Magique `__call` !

!!! abstract "Objectifs Pédagogiques"
    1.  **L'Éponge à Méthodes** : Implémenter le fameux `__call($nom, $arguments)` qui s'active automatiquement dès qu'on appelle une méthode qui... n'existe pas.
    2.  **L'Analyse Lexicale (Regex)** : Découper le nom de la fausse méthode (`wherePrenom`) pour isoler le mot-clé d'action (`where`) et le nom de la Colonne SQL (`Prenom`).
    3.  **L'Usine à Chaîne** : Empiler les fragments de requête générés dynamiquement et utiliser `__toString()` pour cracher la requête complète prête à être envoyée à PDO.

## 1. La Coque du Builder SQL

On construit une coquille qui va retenir l'état de notre requête au fil de l'eau. `from` sera la seule "vraie" fonction de tout notre script.

```php
<?php
declare(strict_types=1);

class MagicQueryBuilder {
    
    // Les morceaux de la future chaine SQL
    private string $table;
    private array $wheres = [];
    private array $orders = [];
    private ?int $limit = null;
    
    // Le Point de Départ Fixe
    public function from(string $table): self {
        $this->table = $table;
        return $this;
    }
    
    // ... La magie arrive en dessous
}
?>
```

## 2. Le Trou Noir Magique (__call)

C'est ici que ce script acquiert son Grade Supérieur Masterclass.

```php
<?php
declare(strict_types=1);

class MagicQueryBuilder {

    // ... (Code précédent) ...

    /**
     * Intercepteur Magique de Méthodes Fantômes.
     * PHP l'exécute quand il est désespéré (La méthode appelée n'existe pas dans le fichier).
     * 
     * @param string $name Le nom fictif tapé (ex: whereEmail)
     * @param array $args Le tableau des éléments passés entre parenthèses
     */
    public function __call(string $name, array $args): self {
        
        // -------------------------------------------------------------
        // CAS 1 : C'est une fausse méthode commençant par "where"
        // ex: whereEmail('alice@test.com')
        // -------------------------------------------------------------
        if (str_starts_with($name, 'where')) {
            
            // On ampute le mot "where" (5 lettres) = Reste "Email" que l'on passe en minuscule
            $column = lcfirst(substr($name, 5)); 
            
            // Si pas d'Opérateur explicite dans la méthode, on devine "= "
            $operator = $args[1] ?? '=';
            $value = $args[0];
            
            // On compile !
            $this->wheres[] = "$column $operator '$value'";
            
            return $this; // Indispensable pour enchaîner les flèches (Fluent Pattern)
        }
        
        // -------------------------------------------------------------
        // CAS 2 : C'est une fausse méthode commençant par "orderBy"
        // ex: orderByPremiumUser('DESC')
        // -------------------------------------------------------------
        if (str_starts_with($name, 'orderBy')) {
            
            // On ampute le "orderBy" (7 lettres).
            $column = lcfirst(substr($name, 7));
            $direction = $args[0] ?? 'ASC';
            
            $this->orders[] = "$column $direction";
            
            return $this;
        }
        
        // -------------------------------------------------------------
        // CAS 3 : C'est une erreur de frappe (ex: whatAge() au lieu de whereAge())
        // -------------------------------------------------------------
        throw new BadMethodCallException("🚨 Halte là : La méthode dynamique '$name' ne correspond à aucun Pattern Builder SQL valide.");
    }
    
    // ... Le Compiler final arrive
}
?>
```

## 3. L'Auto-Compileur (__toString)

On a vu la magie des faux noms. Faisons encore plus fort. En écrasant la fonction interne `__toString()`, notre Builder va secrètement cracher tout le code SQL généré au moment unique où on passera l'Objet dans une fonction d'affichage PHP (ex: `echo` ou `PDO->query()`).


```php
<?php
declare(strict_types=1);

class MagicQueryBuilder {

    // ... (Code précédent) ...

    /**
     * Compileur Final Furtif
     * S'invoque de lui-même si vous manipulez le "MagicQueryBuilder" comme un string !
     */
    public function __toString(): string {
        
        $sql = "SELECT * FROM {$this->table}";
        
        // Fusion des Conditions Dynamiques
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
?>
```

## 4. L'Essai en Action

Testons cette pure illusion syntaxique de niveau Orfèvre.

```php
<?php
require_once 'MagicQueryBuilder.php';

// LE DÉVELOPPEUR APPELLE DES MÉTHODES QUI N'ONT JAMAIS ÉTÉ ÉCRITES !!!
// ----------------------------------------------------------------------
$queryAutomatique = (new MagicQueryBuilder())
    ->from('utilisateurs_pro')
    ->whereRole('admin')                // "Role" = Colonne (Détourné)
    ->whereAge(25, '>=')                // "Age" = Colonne (Détourné)
    ->whereBiteTheDust('Ahaha', '!=')   // La magie n'a pas de limite (Mais ne faites pas ça en prod)
    ->orderByRank('DESC')
    ->orderByCreatedAt('ASC');
// ----------------------------------------------------------------------

// Déclenchement secret de __toString car 'echo' essaye d'afficher une chaine de charactères !
echo "<h1>🎯 REQUÊTE GÉNÉRÉE MAGIQUEMENT :</h1>\n";
echo "<code>" . $queryAutomatique . "</code>";

// Résultat Magistral final :
// SELECT * FROM utilisateurs_pro WHERE role = 'admin' AND age >= '25' AND biteTheDust != 'Ahaha' ORDER BY rank DESC, createdAt ASC
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">Vous avez désormais le pouvoir de simuler n'importe quelle architecture sans écrire une ligne répétitive. Un ingénieur senior utilise <strong><code>__call</code></strong> lorsqu'il y a un besoin infini de variations (comme les noms de colonnes SQL) qui seraient humainement insoutenables à coder "en dur" (Où alors il aurait fallu écrire 340 méthodes <code>whereXXX()</code> dans la classe principale !)</p>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
