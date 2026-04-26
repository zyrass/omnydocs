---
description: "Projet Pratique POO : Découvrir la puissance de l'Héritage Horizontal (Traits) en construisant un Système de Notifications capables d'envoyer des Mails, des SMS, ou des notifications Push."
icon: lucide/bell-ring
tags: ["PHP", "POO", "TRAITS", "NOTIFICATIONS"]
status: stable
---

# Projet 20 : Système de Notifications

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    PHP ne permet pas "l'Héritage Multiple". Une classe `User` ne peut pas hériter à la fois de `Person` ET de `Notifiable`.
    Pour contourner cette limite, PHP a inventé les **Traits** : des morceaux de code volant qu'on "copie-colle" magiquement à l'intérieur d'une classe via le mot clé `use`.
    Nous allons créer un Utilisateur capable d'envoyer des Mails, des SMS, des Pushs... le tout assemblé comme des Legos !

!!! abstract "Objectifs Pédagogiques"
    1.  **Création de Traits** : Définir des comportements séparés et isolés (`EmailNotifiable`, `SmsNotifiable`).
    2.  **L'obligation Abstraite** : Comprendre pourquoi un Trait peut imposer une règle (`abstract protected function getEmail();`) à la classe qui va le consommer.
    3.  **L'Hydratation Multiples** : Utiliser 4 Traits différents dans une même classe (Comportement Frankestein).
    4.  **Le Mot clé Match** : Utiliser le `match` moderne de PHP 8 pour aiguiller la bonne fonction selon le canal demandé.

## 1. Définir les "Super-Pouvoirs" (Les Traits)

Un `Trait` n'est ni une Classe, ni une Interface. C'est purement une "boite à outils virtuelle" qui viendra injecter ses méthodes directement au coeur de la classe qui l'appellera.

```php
<?php
declare(strict_types=1);

// --- TRAIT N°1 : LA CAPACITÉ D'ENVOYER UN EMAIL ---
trait EmailNotifiable {
    
    // Le Trait EXIGE que la Classe possède une méthode getEmail() pour fonctionner !
    abstract protected function getEmail(): string;
    
    protected function sendEmail(string $subject, string $message): bool {
        // En vrai: mail($this->getEmail(), $subject, $message);
        echo "📧 [MAIL] envoyé à {$this->getEmail()} : $subject\n";
        return true;
    }
}

// --- TRAIT N°2 : LA CAPACITÉ D'ENVOYER UN SMS ---
trait SmsNotifiable {
    
    // Le Trait EXIGE de connaitre un Numéro de téléphone
    abstract protected function getPhoneNumber(): string;
    
    protected function sendSms(string $message): bool {
        // En vrai: Appel Twilio / Octopush API
        echo "📱 [SMS] envoyé au {$this->getPhoneNumber()} : $message\n";
        return true;
    }
}

// --- TRAIT N°3 : LA CAPACITÉ DE PUSH MOBILE ---
trait PushNotifiable {
    
    abstract protected function getDeviceToken(): ?string;
    
    protected function sendPush(string $title, string $message): bool {
        $token = $this->getDeviceToken();
        if ($token === null) {
            return false;
        }
        echo "📲 [PUSH] envoyé vers ($token) : $title\n";
        return true;
    }
}

// --- TRAIT N°4 : LA CAPACITÉ D'ALERTER SUR SLACK ---
trait SlackNotifiable {
    
    abstract protected function getSlackChannel(): ?string;
    
    protected function sendSlack(string $message): bool {
        $channel = $this->getSlackChannel();
        if ($channel === null) {
            return false;
        }
        echo "💬 [SLACK] Message déposé sur #$channel : $message\n";
        return true;
    }
}
?>
```

## 2. Assemblage du "Robot" Modulaire

Nous allons créer un simple "User". Mais au lieu de l'encombrer avec 800 lignes de logiques de connexion API, **nous allons "utiliser" (use) nos "Capsules de pouvoirs"**.

```php
<?php
declare(strict_types=1);

// L'Interface garantit qu'il y aura un point d'entrée universel "notify".
interface NotifiableInterface {
    public function notify(string $message, array $channels = []): void;
}

// La Classe User "Monolithique" devient extrêmement légère !
class User implements NotifiableInterface {
    
    // 🔥 L'HÉRITAGE HORIZONTAL (La Magie) 🔥
    use EmailNotifiable, SmsNotifiable, PushNotifiable, SlackNotifiable;
    
    public function __construct(
        private string $name,
        private string $email,
        private ?string $phoneNumber = null,
        private ?string $deviceToken = null,
        private ?string $slackChannel = null
    ) {}
    
    // ============================================
    // SATISFACTION DES CONTRATS DES TRAITS
    // ============================================
    protected function getEmail(): string { return $this->email; }
    protected function getPhoneNumber(): string { return $this->phoneNumber ?? ''; }
    protected function getDeviceToken(): ?string { return $this->deviceToken; }
    protected function getSlackChannel(): ?string { return $this->slackChannel; }
    
    // ============================================
    // LOGIQUE MÉTIER D'ORCHESTRATION
    // ============================================
    
    /**
     * Une seule porte d'entrée pour envoyer le bon signal au bon endroit
     */
    public function notify(string $message, array $channels = ['email']): void {
        foreach ($channels as $channel) {
            
            // Le Super-Switch de PHP 8 ! Court, net et précis.
            match ($channel) {
                // PHP sait que ces méthodes existent car il a "absorbé" les Traits !
                'email' => $this->sendEmail("Nouvelle Notification Omnyvia", $message),
                'sms'   => $this->sendSms($message),
                'push'  => $this->sendPush("Alerte Omnyvia !", $message),
                'slack' => $this->sendSlack($message),
                default => null
            };
            
        }
    }
}
?>
```

## 3. Le Banc d'Essai

Créons un script final pour vérifier si l'Abonné (Le User) va bien recevoir ses notifications disparates.

```php
<?php
$user = new User(
    'Alice',
    'alice@cyberspace.local',
    '+33612345678', // Téléphone Actif
    'TOKEN-APPLE-87G', // Push iPhone activé
    'equipe-developpement' // Slack activé
);

echo ">> SCÉNARIO 1 : L'INSCRIPTION\n";
$user->notify('Bienvenue parmi nous !', array('email', 'sms'));


echo "\n>> SCÉNARIO 2 : ATTAQUE DÉTECTÉE SUR LE COMPTE !\n";
// Oups ! Problème Critique ! On sonne toutes les alarmes.
$user->notify("Tentative de Fraude depuis la Russie détectée !", ['email', 'push', 'slack']);
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-4 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">1</span>
      <span class="text-gray-700">Vous avez évité un Code Spaghetti ou un héritage trop tordu (Exemple: Créer un <code>UserWithSmsAndMail extends User</code> inutile). Les Traits sont une architecture transversale parfaite pour des méthodes isolées (Loggers, Notifications, TimeStamps...).</span>
    </li>
  </ul>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
