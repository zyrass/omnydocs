---
description: "Remédiation — Comment formuler des recommandations actionnables pour aider le client à corriger les vulnérabilités identifiées."
icon: lucide/book-open-check
tags: ["REPORTING", "PENTEST", "REMEDIATION", "CONSEIL", "AUDIT"]
---

# Plan de Remédiation & Recommandations

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="~30 minutes">
</div>

<img src="../../../assets/images/cyber/remediation.svg" width="100" align="center" style="display: block; margin: 0 auto;">

## Introduction

!!! quote "Analogie pédagogique — L'Ordonnance Médicale"
    Un pentest sans remédiation est comme un médecin qui vous dirait : "Vous avez une grave infection, au revoir". Le travail du médecin ne s'arrête pas au diagnostic, il commence vraiment avec l'ordonnance. La **Remédiation** est votre ordonnance : vous devez dire au client quel médicament prendre (patch), comment l'appliquer (config) et quels effets secondaires surveiller (tests de non-régression).

Le but ultime d'un test d'intrusion n'est pas de casser des systèmes, mais de les renforcer. Vos recommandations de remédiation sont la partie la plus précieuse de votre rapport pour les équipes techniques du client.

---

## Les 3 Niveaux de Traitement du Risque

Face à une vulnérabilité, le client a trois options principales :

### 1. La Correction (Fix)
Éliminer la cause racine de la vulnérabilité.
- **Exemple** : Mettre à jour le serveur vers la version `X.Y.Z`, modifier le code pour utiliser des requêtes préparées.
- **C'est l'option recommandée.**

### 2. L'Atténuation (Mitigation)
Réduire l'impact ou la probabilité d'exploitation sans supprimer la faille.
- **Exemple** : Placer un WAF devant l'application, isoler le serveur dans un VLAN restreint.
- **C'est une solution temporaire ou de défense en profondeur.**

### 3. L'Acceptation du Risque
Décider de ne rien faire car le coût de correction est supérieur au risque.
- **Note** : En tant qu'auditeur, vous ne décidez pas de l'acceptation, vous fournissez les données pour que le client décide.

**La Remédiation** est l'étape finale et la plus importante pour le client après un audit de sécurité. Elle consiste à fournir des recommandations techniques précises et actionnables pour corriger les vulnérabilités identifiées. Un bon rapport d'audit ne se contente pas de montrer comment "casser" un système, il guide les équipes de développement et d'administration vers une solution pérenne.

<br>

---

## Les Niveaux de Recommandation

Pour chaque faille, l'auditeur doit proposer des solutions adaptées aux contraintes du client :
- **Remédiation immédiate (Fix)** : La correction directe du code ou de la configuration pour supprimer la vulnérabilité.
- **Mesure d'atténuation (Mitigation)** : Une protection temporaire (ex: règle de WAF) si la correction profonde prend du temps.
- **Recommandation stratégique** : Une modification des processus ou de l'architecture pour éviter que ce type de faille ne se reproduise (ex: formation des développeurs).

<br>

---

## Structure d'une Fiche de Remédiation

Chaque recommandation doit être structurée de manière claire pour être transmise directement aux équipes techniques :

### 1. Description technique du correctif
Expliquer le changement nécessaire de manière théorique.

```text title="Exemple : Correction d'une injection SQL"
Utiliser des requêtes préparées (Prepared Statements) avec des paramètres liés au lieu de concaténer directement les entrées utilisateur dans la requête SQL.
```
_Cette approche garantit que les entrées utilisateur sont toujours traitées comme des données et jamais comme du code exécutable par la base de données._

### 2. Exemple de code (Avant / Après)
Fournir un exemple concret pour aider les développeurs à appliquer le correctif.

```php title="Correction sécurisée en PHP (PDO)"
// AVANT : Vulnérable
$query = "SELECT * FROM users WHERE id = " . $_GET['id'];

// APRÈS : Sécurisé
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = :id');
$stmt->execute(['id' => $_GET['id']]);
$user = $stmt->fetch();
```
_L'utilisation de PDO avec des paramètres nommés (`:id`) est la méthode standard et la plus sûre pour interagir avec une base de données en PHP._

### 3. Vérification de la correction
Expliquer comment s'assurer que le correctif est efficace.

```bash title="Test de non-régression après correction"
# Tenter à nouveau l'injection pour confirmer le blocage
curl -i "http://target.com/user.php?id=1' OR 1=1"
```
_Si le serveur renvoie désormais une erreur propre ou une page vide sans données sensibles, la vulnérabilité est considérée comme corrigée._

<br>

---

## Principes de Défense en Profondeur

Une remédiation efficace ne doit pas être un simple "patch" isolé. Elle doit s'inscrire dans une stratégie globale :
- **Principe du Moindre Privilège** : Limiter les droits des comptes de service.
- **Défense par Défaut** : Configurer les systèmes pour être sécurisés dès l'installation.
- **Validation Strictes des Entrées** : Ne jamais faire confiance aux données provenant de l'utilisateur (Allow-listing).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La valeur réelle d'un pentest réside dans la qualité de ses remédiations. Votre rôle est d'être un partenaire du client pour améliorer sa sécurité, pas seulement un attaquant. Des conseils clairs, précis et faciles à mettre en œuvre garantissent un meilleur taux de correction et renforcent votre professionnalisme.

!!! tip "Vérification de la correction"
    Proposez toujours une phase de **contre-audit** (re-test) quelques semaines après le rapport pour valider que les remédiations ont bien été appliquées correctement.

> Pour évaluer la priorité des remédiations à appliquer, utilisez le système de notation **[CVSS](./cvss.md)**.
> Pour assurer la pérennité de la sécurité, intégrez ces correctifs dans une démarche de **[Gestion des Vulnérabilités (SOC/Blue Team) →](../../operations/soc/index.md)**.





