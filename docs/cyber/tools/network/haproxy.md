---
description: "HAProxy — Le répartiteur de charge (Load Balancer) et proxy inverse ultra-performant pour garantir la haute disponibilité et la sécurité des applications web."
icon: lucide/book-open-check
tags: ["INFRA", "HAPROXY", "LOAD BALANCING", "RÉSEAU", "DISPONIBILITÉ", "RED TEAM"]
---

# HAProxy — Le Chef d'Orchestre du Trafic

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="2.8+"
  data-time="~1 heure">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/Haproxy-logo.png" width="250" align="center" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Maître d'Hôtel"
    Imaginez un restaurant très populaire avec 10 cuisiniers en cuisine. Si tous les clients essayaient de parler directement aux cuisiniers, ce serait le chaos. **HAProxy** est le Maître d'Hôtel à l'entrée. Il accueille chaque client, vérifie s'il est habillé correctement (**SSL/TLS**), et l'envoie vers le cuisinier qui est le moins occupé (**Load Balancing**). Si un cuisinier tombe malade, le Maître d'Hôtel ne lui envoie plus personne jusqu'à ce qu'il soit guéri (**Health Checks**).

**HAProxy** (High Availability Proxy) est une solution open-source de répartition de charge et de proxy inverse pour les applications TCP et HTTP. Il est réputé pour sa vitesse exceptionnelle et sa fiabilité.

---

## Les 3 Missions de HAProxy

### 1. La Haute Disponibilité (High Availability)
Si vous avez plusieurs serveurs web, HAProxy s'assure que si l'un d'eux tombe en panne, le trafic est automatiquement redirigé vers les autres. L'utilisateur ne voit aucune interruption.

### 2. La Répartition de Charge (Load Balancing)
Il distribue les requêtes entre les serveurs selon différents algorithmes (Round Robin, Least Connections, etc.) pour éviter qu'un seul serveur ne soit surchargé.

### 3. La Sécurité (Proxy Inverse)
- **Terminaison SSL** : HAProxy gère les certificats HTTPS pour décharger les serveurs web de cette tâche complexe.
- **Protection DoS** : Peut limiter le nombre de connexions par adresse IP pour contrer les attaques par déni de service.
- **ACL (Access Control Lists)** : Permet d'autoriser ou bloquer le trafic selon des critères précis (IP, URL, Headers).

<br>

---

## Les Concepts Clés de HAProxy

Pour bien configurer HAProxy, il faut comprendre ses quatre sections principales :
- **Frontend** : Définit comment les requêtes sont reçues (IP, port, certificats SSL).
- **Backend** : Définit l'ensemble des serveurs réels qui traiteront les requêtes.
- **ACL (Access Control Lists)** : Permet de router le trafic en fonction de conditions spécifiques (ex: URL, en-têtes HTTP).
- **Global / Defaults** : Paramètres de performance et de sécurité applicables à l'ensemble de l'instance.

<br>

---

## Pourquoi un Red Teamer s'y intéresse ?

- **Redirecteurs C2** : En Red Team, on utilise souvent HAProxy comme "Front-end" pour masquer l'adresse IP réelle de notre serveur de Command & Control (**[C2](./methodology/c2-frameworks.md)**).
- **Analyse de configuration** : Une mauvaise règle d'ACL dans HAProxy peut permettre d'accéder à des ressources internes normalement protégées.

<br>

---

## Usage Opérationnel

### 1. Configuration d'un Load-Balancer simple
Répartir le trafic web entre deux serveurs d'application.

```haproxy title="Exemple de configuration de base (haproxy.cfg)"
frontend http-in
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    server server1 10.0.0.1:80 check
    server server2 10.0.0.2:80 check
```
_Cette configuration utilise l'algorithme `roundrobin` pour alterner les requêtes entre les deux serveurs. L'option `check` permet à HAProxy de vérifier la santé des serveurs avant d'envoyer du trafic._

### 2. Terminaison SSL (Offloading)
Gérer le chiffrement HTTPS au niveau du proxy pour décharger les serveurs de backend.

```haproxy title="Configuration du Frontend pour le support HTTPS"
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/site.pem
    reqadd X-Forwarded-Proto:\ https
    default_backend secure_web_servers
```
_Le certificat SSL est centralisé sur HAProxy. Les serveurs de backend reçoivent du trafic HTTP standard, ce qui simplifie leur gestion et améliore leurs performances._

### 3. Protection contre les attaques (ACL)
Utiliser HAProxy comme un premier rempart contre les robots malveillants.

```haproxy title="Blocage d'accès basé sur le User-Agent"
frontend http-in
    acl is_scanner hdr_sub(user-agent) -i nikto nmap sqlmap
    http-request deny if is_scanner
```
_Les ACL permettent de détecter les signatures d'outils de scan connus et de rejeter leurs requêtes avant même qu'elles n'atteignent l'application._

<br>

---

## Les Algorithmes de Répartition

- **`roundrobin`** : Alterne équitablement entre les serveurs.
- **`leastconn`** : Envoie la requête au serveur ayant le moins de connexions actives (idéal pour les sessions longues).
- **`source`** : Assure que le même client (basé sur son IP) arrive toujours sur le même serveur (persistance de session).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    HAProxy est le gardien de l'infrastructure web moderne. Plus qu'un simple répartiteur, c'est un outil de sécurité et de haute disponibilité capable de transformer un ensemble de serveurs fragiles en une plateforme robuste et évolutive.

> Pour une analyse approfondie des performances de votre proxy, activez l'interface de statistiques via la directive `stats enable`.

---






