---
description: "Projet Pratique POO : Développer un système complet et sécurisé de gestion de comptes bancaires avec des transactions traçables."
icon: lucide/landmark
tags: ["PHP", "POO", "CLASSE", "SÉCURITÉ"]
status: stable
---

# Projet 15 : Système Bancaire (POO)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    L'argent est un domaine sensible. On ne peut pas simplement faire `$solde = $solde + 200` dans un tableau associatif perdu dans un fichier `traitement.php`.
    La Programmation Orientée Objet trouve tout son sens ici : Créer une Forteresse (La Classe `BankAccount`) qui protègera l'état du Solde comme un coffre-fort. Impossible de voler de l'argent sans laisser de trace !

!!! abstract "Objectifs Pédagogiques"
    1.  **Méthodes d'Instance** : Coder des fonctions métiers (Déposer, Retirer, Virement) encapsulées dans la Classe.
    2.  **Tableau de Traces (Log)** : Comprendre qu'un Objet n'est pas uniquement un Solde, c'est aussi un état de l'historique (Tableau des Transactions privées).
    3.  **Interaction Multi-Objets** : Programmer un `Virement` d'un compte (Objet A) vers un autre (Objet B).
    4.  **Formatage Stricte** : Toujours utiliser le Typage de Retour PHP 7.4+ type (`bool`, `float`).

## 1. L'Entité Transaction

Pour que notre relevé bancaire fonctionne, créons d'abord un Objet qui représente un **Mouvement**.
> Fichier `Transaction.php`

```php
<?php
declare(strict_types=1);

/**
 * Une Transaction est immuable. 
 * Une fois créée, on ne peut plus jamais modifier son montant ou sa date. (Pas de Setters !)
 */
class Transaction {
    
    private DateTime $date;
    private string $type; // 'dépôt', 'retrait', 'virement_entrant', 'virement_sortant'
    private float $amount;
    private float $balanceAfter;
    
    public function __construct(string $type, float $amount, float $balanceAfter) {
        $this->date = new DateTime();
        $this->type = $type;
        $this->amount = $amount;
        $this->balanceAfter = $balanceAfter;
    }
    
    public function getSummary(): string {
        $color = in_array($this->type, ['retrait', 'virement_sortant']) ? '🔴' : '🟢';
        return sprintf(
            "[%s] %s | Type : %s | Montant : %.2f € | Solde Restant : %.2f €",
            $color,
            $this->date->format('d/m/Y H:i:s'),
            strtoupper($this->type),
            $this->amount,
            $this->balanceAfter
        );
    }
}
?>
```

## 2. Le Coffre Fort (Le Compte)

Le cœur du système. Créez `BankAccount.php`.
Observez attentivement comment l'Objet `BankAccount` appelle des Objets `Transaction` pour construire son tableau d'historique interne (Composition).

```php
<?php
declare(strict_types=1);
require_once 'Transaction.php';

class BankAccount {
    
    // Un IBAN (Account Number) doit être inaltérable de l'extérieur (Readonly)
    public readonly string $accountNumber;
    
    private float $balance;
    private string $owner;
    
    // Tableau qui contiendra une armée d'Objets "Transaction"
    private array $transactions = [];
    
    public function __construct(string $accountNumber, string $owner, float $initialBalance = 0.0) {
        if ($initialBalance < 0) {
            throw new InvalidArgumentException("Dépôt initial négatif interdit par la Loi.");
        }
        
        $this->accountNumber = $accountNumber;
        $this->owner = $owner;
        $this->balance = $initialBalance;
        
        // Mouvement Fondateur (Sauf si 0)
        if ($initialBalance > 0) {
            $this->transactions[] = new Transaction('dépôt_initial', $initialBalance, $this->balance);
        }
    }
    
    // ============================================
    // SECTEUR SÉCURISÉ (Mouvements Financiers)
    // ============================================
    
    /**
     * DÉPÔT
     */
    public function deposit(float $amount): bool {
        if ($amount <= 0) {
            return false; // Impossible de déposer de l'air
        }
        
        $this->balance += $amount;
        $this->transactions[] = new Transaction('dépôt', $amount, $this->balance);
        
        return true;
    }
    
    /**
     * RETRAIT
     */
    public function withdraw(float $amount): bool {
        // Validation stricte du risque bancaire (Agio interdit dans cet exercice)
        if ($amount <= 0 || $amount > $this->balance) {
            return false; // Pas d'argent suffisant
        }
        
        $this->balance -= $amount;
        $this->transactions[] = new Transaction('retrait', $amount, $this->balance);
        
        return true;
    }
    
    /**
     * VIREMENT ENTRE DEUX OBJETS DISTINCTS
     * Notez que l'argument prend un OBJET BankAccount en paramètre !
     */
    public function transfer(BankAccount $destinationAccount, float $amount): bool {
        // L'argent sort de NOTRE compte d'abord !
        if ($this->withdraw($amount)) {
            
            // On a réussi à prélever, on injecte l'argent dans le compte de Bob
            $destinationAccount->balance += $amount; // L'ami Bob
            
            // Re-qualifier le dernier "retrait" en "virement_sortant" pour ce compte
            array_pop($this->transactions); // Retire le faux retrait
            $this->transactions[] = new Transaction('virement_sortant', $amount, $this->balance);
            
            // Ajouter la bonne ligne chez Bob ! On utilise les propriétés virtuelles via la fonction
            // Wait, impossible de manipuler $transactions de l'extérieur si elles sont private.
            // On va donc doter la méthode "deposit" d'une variable optionnelle pour le libellé, 
            // ou bien on utilise une méthode interne. Pour faire simple, 
            // On bypass la méthode standard chez Bob :
            $destinationAccount->transactions[] = new Transaction('virement_entrant', $amount, $destinationAccount->balance);
            
            return true;
        }
        
        return false;
    }
    
    // ============================================
    // VUES EXTERNES (Getters)
    // ============================================
    
    public function getBalance(): float {
        return $this->balance;
    }
    
    public function getOwner(): string {
       return $this->owner;
    }
    
    /**
     * Affiche le reçu complet de la machine ATM
     */
    public function printStatement(): string {
        $output = "========================================\n";
        $output .= "🏦 BANQUE OMNYVIA - RELEVÉ OFFICIEL\n";
        $output .= "========================================\n";
        $output .= "Propriétaire: " . strtoupper($this->owner) . "\n";
        $output .= "I.B.A.N     : " . $this->accountNumber . "\n";
        $output .= "Solde Actuel: " . number_format($this->balance, 2, ',', ' ') . " €\n\n";
        
        $output .= ">> HISTORIQUE DES MOUVEMENTS :\n";
        
        foreach ($this->transactions as $trx) {
            $output .= "  " . $trx->getSummary() . "\n";
        }
        $output .= "========================================\n";
        
        return $output;
    }
}
?>
```

## 3. L'Aire de Jeu

Testez le système comme un script de démarrage `index.php`.

```php
<?php
require_once 'BankAccount.php';

// Création de Alice avec 1 000€
$accountAlice = new BankAccount('FR-ALICE-100K-9', 'Alice Wonderland', 1000.00);

// Création de Bob (À Zéro !)
$accountBob = new BankAccount('FR-BOB-POOR-42', 'Bob Morane', 0.00);

echo "\n--- 1. SCÉNARIO INITIAL ---\n";
echo "Solde Alice : " . $accountAlice->getBalance() . "€ \n";

echo "\n--- 2. DÉPÔT / RETRAIT ---\n";
$accountAlice->deposit(500); // Papa donne 500 balles
$accountAlice->withdraw(100); // Soirée Casino

echo "\n--- 3. LE GRAND VIREMENT ---\n";
// Alice paie le loyer de Bob !
if ($accountAlice->transfer($accountBob, 800)) {
    echo "🟢 Virement réussi !\n";
} else {
    echo "🔴 Virement refusé (Fonds insuffisants).\n";
}

echo "\n\n";

// L'heure de vérité 
echo $accountAlice->printStatement();
echo "\n\n";
echo $accountBob->printStatement();
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-4 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">1</span>
      <span class="text-gray-700">Vous observez le comportement d'une "Injection de Dépendance" basique : La méthode <code>transfer(BankAccount $destination, $amount)</code> prend <strong>une Classe comme paramètre</strong> obligatoire au lieu d'un vulgaire string de type (<code>"FR-BOB-POOR-42"</code>). L'Objet parle à un Objet ! C'est le Graal de PHP OO.</span>
    </li>
  </ul>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
