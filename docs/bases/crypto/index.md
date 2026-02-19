---
description: "Comprendre la cryptographie moderne et les infrastructures à clés publiques (PKI) pour maîtriser la sécurité des systèmes et des communications"
tags: ["CRYPTOGRAPHIE", "PKI", "TLS", "SSL", "GPG", "SÉCURITÉ", "CHIFFREMENT"]
---

# Cryptographie & PKI

<div
  class="omny-meta"
  data-level="🟢 Débutant à 🔴 Avancé"
  data-version="1.0"
  data-time="20-30 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    _La cryptographie est au numérique ce que les serrures, coffres-forts et signatures notariales sont au monde physique. Elle protège les messages, vérifie l'identité des interlocuteurs et garantit qu'aucune modification n’a été faite en route._

La **cryptographie moderne** constitue la base de toute sécurité informatique : HTTPS, VPN, authentification, signatures numériques, blockchain, stockage sécurisé, e-mails chiffrés…  
Sans elle, Internet tel que nous le connaissons serait inutilisable.

Ce chapitre sert de **porte d’entrée structurée** pour comprendre :

- comment fonctionne le chiffrement
- comment les identités numériques sont vérifiées
- comment les certificats sont délivrés
- comment les systèmes font confiance aux autorités

---

## Objectif du parcours

À la fin de cette section, vous saurez :

- différencier chiffrement symétrique et asymétrique  
- comprendre le rôle d’une PKI  
- expliquer comment HTTPS fonctionne réellement  
- manipuler OpenSSL et GPG  
- diagnostiquer un problème TLS ou certificat  

---

## Architecture conceptuelle de la cryptographie

```mermaid
flowchart LR
    A[Données] --> B{Chiffrement}
    B -->|Symétrique| C[Clé unique]
    B -->|Asymétrique| D[Paire de clés]
    D --> E[Clé publique]
    D --> F[Clé privée]
    E --> G[Partage sécurisé]
    F --> H[Signature / Déchiffrement]
```

---

## Les trois piliers fondamentaux

Toute la sécurité cryptographique repose sur trois objectifs :

| Pilier          | Rôle                  | Exemple        |
| --------------- | --------------------- | -------------- |
| Confidentialité | Empêcher la lecture   | HTTPS          |
| Intégrité       | Empêcher modification | Hash SHA-256   |
| Authenticité    | Vérifier l’identité   | Certificat TLS |

Ces trois propriétés forment la base de tous les protocoles sécurisés.

---

## Les briques technologiques principales

```mermaid
graph LR
    A[Cryptographie] --> B[Algorithmes]
    A --> C[Protocoles]
    A --> D[Infrastructures]

    B --> B1[AES]
    B --> B2[RSA]
    B --> B3[ChaCha20]
    B --> B4[SHA]

    C --> C1[TLS]
    C --> C2[SSH]
    C --> C3[PGP]

    D --> D1[PKI]
    D --> D2[Autorités de certification]
    D --> D3[Certificats X.509]
```

---

## Navigation des guides

<div class="grid cards" markdown>

* :lucide-key:{ .lg .middle } **OpenSSL**

    ---

    Outil universel de cryptographie : génération de clés, certificats, CSR, debug TLS, inspection HTTPS.

    [:lucide-book-open-check: Ouvrir le guide](./openssl.md)

* :lucide-mail:{ .lg .middle } **GPG — chiffrement & signatures**

    ---

    Chiffrement asymétrique pour fichiers, e-mails, signatures, vérification d’intégrité logicielle.

    [:lucide-book-open-check: Ouvrir le guide](./gpg.md)

</div>

<div class="grid cards" markdown>

* :lucide-shield-check:{ .lg .middle } **PKI — Infrastructure de confiance**

    ---

    Autorités de certification, chaînes de confiance, révocation, hiérarchies, architecture enterprise.

    [:lucide-book-open-check: Ouvrir le guide](./pki.md)

</div>

---

## Modèle réel : comment HTTPS fonctionne

```mermaid
sequenceDiagram
    participant Client
    participant Serveur
    participant Autorité

    Client->>Serveur: Hello TLS
    Serveur->>Client: Certificat
    Client->>Autorité: Vérification
    Autorité-->>Client: Certificat valide
    Client->>Serveur: Clé session chiffrée
    Serveur-->>Client: Communication sécurisée
```

Ce mécanisme combine :

* chiffrement asymétrique (authentification)
* chiffrement symétrique (performance)
* PKI (confiance globale)

---

## Ordre recommandé d’apprentissage

Pour éviter toute confusion conceptuelle, suivez cet ordre :

1. OpenSSL → comprendre les primitives cryptographiques
2. GPG → comprendre chiffrement asymétrique concret
3. PKI → comprendre la confiance globale

---

## Erreurs fréquentes des débutants

!!! warning "Pièges classiques"
- Confondre chiffrement et encodage
- Penser que HTTPS = chiffrement seulement
- Croire que la clé publique doit être secrète
- Penser qu’un certificat auto-signé est “moins sécurisé”
- Croire qu’un hash chiffre des données

---

## Positionnement professionnel

Maîtriser cette section permet de :

* débugger TLS en production
* comprendre un audit sécurité
* configurer un serveur sécurisé
* valider une chaîne de confiance
* expliquer clairement la sécurité à un client ou un RSSI

---

## Le mot de la fin

!!! quote
    La cryptographie n’est pas une option technique. C’est la **fondation invisible** de toute sécurité numérique. Ceux qui la comprennent contrôlent la sécurité. Ceux qui ne la comprennent pas la subissent.

<br />