---
description: "Damn Vulnerable Web App (DVWA) — Une application web volontairement vulnérable pour s'entraîner légalement à l'exploitation (SQLi, XSS, CSRF, Brute Force)."
icon: lucide/target
tags: ["DVWA", "WEB", "TRAINING", "LAB", "SQLI", "XSS"]
---

# DVWA & Plateformes de Lab

<div
  class="omny-meta"
  data-level="🟢 Fondamental"
  data-version="2026"
  data-time="~20 minutes">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/dvwa.svg" width="250" align="center" alt="DVWA Logo" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Mannequin de Frappe"
    Essayer vos premiers exploits SQL sur le site d'un client, c'est comme apprendre à tirer à balles réelles au milieu d'une foule : c'est criminel et irresponsable. DVWA est votre **mannequin de frappe**. C'est une application codée spécifiquement pour être criblée de failles, vous permettant de voir ce qui se passe quand l'exploit réussit, et surtout, ce que ça génère comme traces côté serveur.

**Damn Vulnerable Web App (DVWA)** est une application PHP/MySQL volontairement vulnérable. Son objectif principal est d'aider les professionnels de la sécurité à tester leurs compétences et outils dans un environnement légal et isolé.

<br>

---

## 🏗️ 1. Déploiement Sécurisé (Lab-as-Code)

!!! danger "Attention : Ne jamais exposer DVWA sur Internet !"
    Par définition, DVWA est vulnérable à tout. Si vous l'exposez sur un serveur public ou un port ouvert de votre routeur domestique, vous serez compromis en quelques minutes.

La meilleure façon de déployer DVWA est d'utiliser Docker. Cela permet de le lancer en 5 secondes, et de détruire le conteneur quand l'entraînement est terminé (pratique si vous avez cassé la base de données avec une injection SQL destructrice).

```bash title="Déploiement Docker de DVWA"
# Télécharger et lancer l'image officielle sur le port 8080 local
docker run --rm -it -p 8080:80 vulnerables/web-dvwa

# Accès : http://localhost:8080
# Identifiants par défaut : admin / password
```

Une fois connecté, la première chose à faire est de cliquer sur le bouton `Create / Reset Database` en bas de la page de configuration initiale.

<br>

---

## 🎯 2. La Mécanique des Niveaux de Difficulté

La grande force de DVWA réside dans son sélecteur de difficulté (onglet `DVWA Security`). Pour chaque vulnérabilité, vous pouvez affronter 4 niveaux de sécurité :

- **Low (Bas)** : Aucune protection. Le code est naïf. Idéal pour tester la syntaxe de base d'une charge utile (payload).
- **Medium (Moyen)** : Le développeur a tenté d'ajouter une protection basique (ex: remplacer le mot `<script>` par du vide), mais elle est contournable (ex: en écrivant `<ScRipT>`).
- **High (Haut)** : Le développeur a utilisé une bonne pratique, mais avec une faille logique ou une erreur d'implémentation. Réservé aux attaquants expérimentés.
- **Impossible** : Le code utilise les meilleures pratiques de l'industrie (ex: requêtes préparées PDO pour le SQL). Le but est de comparer le code source vulnérable (Low) au code source sécurisé (Impossible) pour apprendre à patcher.

<br>

---

## 💥 3. Vulnérabilités Majeures à Pratiquer

Voici les exercices incontournables à réaliser sur DVWA pour comprendre les failles fondamentales de l'OWASP Top 10 :

### 💉 A. Injection SQL (SQLi)
- **Objectif** : Manipuler une requête de base de données depuis un champ de recherche.
- **Payload niveau Low** : `' OR '1'='1`
- **Scénario "Purple Team"** : Après avoir réussi l'injection, connectez-vous au conteneur Docker et regardez le fichier `/var/log/apache2/access.log`. Vous verrez exactement l'empreinte réseau de votre attaque (et pourquoi un WAF devrait la bloquer).

### 🎭 B. Cross-Site Scripting (XSS)
- **Objectif** : Injecter du code JavaScript exécuté par le navigateur des autres victimes.
- **Payload Reflected XSS (Low)** : `<script>alert('Piraté!');</script>`
- **Payload Stored XSS** : Injecter un script dans le Livre d'Or qui vole le cookie de session `document.cookie` et l'envoie vers un serveur externe.

### 🔑 C. Brute Force
- **Objectif** : Casser un formulaire de connexion.
- **Exercice** : Utilisez **Burp Suite** (Intruder) ou **Hydra** pour bombarder le formulaire avec le dictionnaire populaire `rockyou.txt` et trouver le mot de passe de l'utilisateur.

### 📁 D. File Inclusion (LFI/RFI)
- **Objectif** : Lire des fichiers système critiques ou faire exécuter un script distant.
- **Payload Local (LFI)** : Remplacer un paramètre d'URL (`?page=`) par `../../../../etc/passwd` pour afficher les utilisateurs du système Linux sous-jacent.

<br>

---

## 🌐 4. Autres Plateformes Complémentaires

DVWA est excellent pour commencer, mais le monde des failles web évolue vite (APIs, SSRF, JWT). Quand vous aurez maîtrisé DVWA, vous pourrez passer à :

1. **OWASP Juice Shop** : Une application moderne en Node.js/Angular très aboutie, simulant un site e-commerce bourré de failles subtiles.
2. **PortSwigger Web Security Academy** : Les créateurs de Burp Suite proposent les meilleurs laboratoires gratuits en ligne du monde pour des failles extrêmement modernes et complexes.
3. **Hack The Box (HTB) / TryHackMe** : Des environnements complets (pas que web) instanciés à la demande.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    DVWA est la passerelle entre la théorie et la pratique. Vous pouvez lire 100 pages sur les injections SQL, mais rien ne remplace le "déclic" mental lorsque vous tapez une apostrophe et que la base de données crache ses erreurs à l'écran.

> **Exercice final :** Lancez votre docker DVWA, mettez la sécurité sur "Low", ouvrez **[Burp Suite](./burp.md)**, interceptez la requête de login et modifiez-la à la volée. C'est votre premier pas de pentester web.
