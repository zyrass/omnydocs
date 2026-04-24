---
description: "Assurer la Haute Disponibilité (HA) et la répartition de charge avec le Reverse Proxy HAProxy."
icon: lucide/book-open-check
tags: ["HAPROXY", "REVERSE PROXY", "LOAD BALANCING", "RESEAU", "INFRASTRUCTURE"]
---

# Reverse Proxy (HAProxy)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>

!!! quote "Le chef d'orchestre du trafic"
    _Un serveur web unique, c'est ce qu'on appelle un **SPOF** (Single Point Of Failure : Point Individuel de Défaillance). S'il tombe en panne, le site est mort. Pour assurer une disponibilité 24/7, il faut plusieurs serveurs qui hébergent le même site. Le **Reverse Proxy** se place devant eux : il reçoit toutes les requêtes des internautes et les distribue intelligemment aux différents serveurs. **HAProxy** est la référence absolue dans ce domaine._

## 1. Forward Proxy vs Reverse Proxy

Il est important de ne pas confondre les deux :
- Le **Proxy classique (Forward Proxy)** protège les *utilisateurs*. L'entreprise l'installe pour surveiller/bloquer les sites sur lesquels vont les employés (ex: bloquer Facebook).
- Le **Reverse Proxy (Proxy Inverse)** protège les *serveurs*. Il se place devant vos serveurs web et cache leur existence. L'internaute pense se connecter directement à votre serveur web, mais il se connecte en fait au Reverse Proxy.

---

## 2. Le Load Balancing (Répartition de charge)

La fonction principale de **HAProxy** (High Availability Proxy) est le *Load Balancing*.

```mermaid
graph TD
    Client1[Visiteur 1] -->|Requête| HAProxy[HAProxy <br/> Frontend Public]
    Client2[Visiteur 2] -->|Requête| HAProxy
    Client3[Visiteur 3] -->|Requête| HAProxy
    
    subgraph Cluster Web (Backend)
        HAProxy -->|Round-Robin| S1[Serveur Web A <br/> ✓ Healthy]
        HAProxy -->|Round-Robin| S2[Serveur Web B <br/> ✓ Healthy]
        HAProxy -.->|Health Check Failed <br/> Trafic stoppé| S3[Serveur Web C <br/> ❌ DOWN]
    end
    
    style HAProxy fill:#8e44ad,stroke:#fff,stroke-width:2px,color:#fff
    style S1 fill:#27ae60,stroke:#fff,color:#fff
    style S2 fill:#27ae60,stroke:#fff,color:#fff
    style S3 fill:#c0392b,stroke:#fff,color:#fff
    style Client1 fill:#2980b9,stroke:#fff,color:#fff
    style Client2 fill:#2980b9,stroke:#fff,color:#fff
    style Client3 fill:#2980b9,stroke:#fff,color:#fff
```

Si vous avez 3 serveurs web (Backend), HAProxy (Frontend) va analyser les performances et distribuer les visiteurs (Requêtes TCP ou HTTP) selon différents algorithmes :

1. **Round Robin (Tourniquet)** : La requête 1 va au Serveur A, la 2 au Serveur B, la 3 au Serveur C, puis on recommence. (L'algorithme de base).
2. **Least Connections** : HAProxy envoie le visiteur vers le serveur qui a actuellement le moins de connexions actives. Idéal pour les sites très fréquentés.
3. **Source IP Hash** : Une fonction mathématique assure que l'IP d'un visiteur précis sera *toujours* redirigée vers le même serveur. C'est critique si votre site web gère des "sessions utilisateurs" mal codées qui ne sont pas partagées entre les serveurs (Sticky Sessions).

### Health Checks (Vérification de santé)
C'est la magie de la "Haute Disponibilité" (HA). HAProxy interroge vos 3 serveurs toutes les secondes (`PING` ou `GET /status`).
Si le Serveur B crashe brutalement, HAProxy le détecte instantanément et arrête de lui envoyer des visiteurs, les redirigeant vers A et C. **Pour l'internaute, la panne est totalement invisible.**

---

## 3. Autres cas d'usage massifs (Ops)

Bien qu'un Nginx puisse aussi faire office de Reverse Proxy, HAProxy est souvent préféré dans les architectures massives pour ses performances extrêmes de routage pur et sa souplesse.

### La terminaison SSL (Offloading)
Gérer des certificats SSL/TLS coûte très cher en calcul (CPU).
Plutôt que d'obliger vos 3 serveurs web à chiffrer et déchiffrer le trafic (ce qui les ralentit), on installe le certificat SSL directement sur HAProxy.
Le trafic entre le Visiteur et HAProxy est chiffré (HTTPS). Mais le trafic interne entre HAProxy et vos serveurs web se fait en clair (HTTP), soulageant les serveurs de ce poids mathématique.

### Le Routage par nom de domaine (SNI)
Vous possédez une seule adresse IP publique, mais vous voulez héberger 10 sites différents (qui tournent sur 10 serveurs locaux différents).
HAProxy écoute sur le port 80/443 de votre IP publique. Il lit la requête (`Host: forum.omnyvia.local`) et sait qu'il doit forwarder ce trafic précis vers le serveur interne `192.168.1.10`, alors qu'une requête `Host: blog.omnyvia.local` ira sur le `192.168.1.20`.

## Conclusion et Sécurité

Le Reverse Proxy est la porte d'entrée de l'architecture applicative. Placer un HAProxy devant ses serveurs a un énorme effet bénéfique en cybersécurité :
1. **Dissimulation** : Les attaquants ne voient jamais la vraie IP de vos serveurs (qui restent cachés dans un réseau privé, non accessibles depuis Internet).
2. **DDoS Mitigation** : Encaisser des millions de requêtes en répartissant intelligemment la charge empêche un serveur unique de s'effondrer.