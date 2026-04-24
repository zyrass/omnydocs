---
title: Orchestration (Docker Swarm)
description: Démystifier l'orchestration multi-nœuds, le clustering avec Docker Swarm, et ses limites face à Kubernetes.
icon: lucide/book-open-check
tags: ["DOCKER", "SWARM", "ORCHESTRATION", "KUBERNETES", "CLUSTER"]
---

# L'Orchestration et Docker Swarm

<div
  class="omny-meta"
  data-level="🟠 Avancé"
  data-version="1.0"
  data-time="20-30 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Transporteur Routier"
    Utiliser **Docker Compose**, c'est comme posséder un camion très bien rangé. Vous pouvez y mettre des dizaines de conteneurs différents, c'est propre et organisé. Mais que faire le jour où vous devez livrer 10 000 conteneurs par jour ? Un seul camion ne suffit plus. Il vous faut une **flotte** de 50 camions, et un gestionnaire logistique central qui indique en temps réel à quel camion attribuer tel conteneur, en fonction de sa place disponible ou d'une panne moteur.
    
    Cette "flotte de camions", c'est un **Cluster** (une grappe de serveurs). Et le "gestionnaire logistique", c'est **l'Orchestrateur** (Docker Swarm ou Kubernetes).

Docker Compose est fantastique pour le développement local ou pour déployer une application sur un **seul serveur**. Mais les géants du web (ou toute application critique) ne peuvent pas se permettre de dépendre d'un seul serveur (qui peut tomber en panne). Ils déploient sur des *Clusters*.

<br>

---

## Qu'est-ce qu'un Cluster ?

Un cluster est un regroupement de plusieurs serveurs physiques (ou virtuels) qui communiquent ensemble pour se comporter comme un seul super-ordinateur.

Dans l'écosystème Docker Swarm, les serveurs d'un cluster ont deux rôles distincts :
1. **Les Managers (Chefs d'orchestre)** : Ils ne font pas tourner vos applications. Ils surveillent l'état du système, stockent la configuration globale, et distribuent les ordres.
2. **Les Workers (Ouvriers)** : Ce sont eux qui exécutent physiquement vos conteneurs Web, API, BDD. S'ils n'ont plus de CPU, le Manager envoie le travail au Worker suivant.

!!! tip "La Haute Disponibilité (High Availability - HA)"
    Si le *Worker 3* prend feu, le *Manager* s'en rend compte en moins d'une seconde. Il relance instantanément les conteneurs qui tournaient sur le *Worker 3* vers le *Worker 1* et le *Worker 2*, sans qu'aucun client ne s'aperçoive de la coupure de service. C'est l'essence même de l'orchestration.

<br>

---

## Docker Swarm : La simplicité native

**Docker Swarm** est l'orchestrateur natif inclus directement dans le moteur Docker. Vous n'avez absolument rien à installer de plus si vous possédez déjà Docker.

### Initialiser un Swarm

Transformer un simple serveur Docker en un *Manager* de cluster prend littéralement une seule commande :

```bash
docker swarm init --advertise-addr <IP_DU_SERVEUR>
```

Le terminal vous répondra en vous donnant un "Token" (un mot de passe).
Vous vous connectez ensuite sur vos autres serveurs (les *Workers*) et vous tapez :

```bash
docker swarm join --token <LE_TOKEN_SECRET> <IP_DU_MANAGER>:2377
```

**C'est tout.** Vos serveurs sont désormais fusionnés en un cluster. Vous pouvez lancer un service exigeant "5 répliques Nginx", et Swarm se chargera de répartir 2 conteneurs sur le serveur A, 2 sur le serveur B et 1 sur le serveur C.

<br>

---

## Tableau Comparatif : Compose vs Swarm vs Kubernetes

Vous entendrez très souvent parler de **Kubernetes** (surnommé K8s). C'est le titan de l'industrie, créé par Google. Mais il est d'une complexité effarante par rapport à Swarm.

| Caractéristique | Docker Compose | Docker Swarm | Kubernetes (K8s) |
| --- | --- | --- | --- |
| **Cible** | 1 seul serveur (PC dev / Monolithe) | Multi-serveurs (PME / Projets de taille moyenne) | Data-centers entiers (Entreprises massives / Cloud pur) |
| **Complexité** | 🟢 Très faible (1 fichier YAML) | 🟡 Faible (Le même fichier YAML, étendu) | 🔴 Extrême (Nécessite des équipes dédiées) |
| **Installation** | Fourni avec Docker | Fourni avec Docker | Nécessite des outils tiers lourds (kubeadm, k3s, minikube) |
| **Haute Disponibilité** | Non (Si le serveur meurt, tout s'arrête) | Oui (Auto-réparation si un nœud tombe) | Oui (Auto-réparation, auto-scaling complexe) |
| **Standard de l'industrie**| Standard absolu pour le dev local | Acteur de niche, en déclin | Standard absolu de la production Cloud Native |

!!! danger "Faut-il apprendre Kubernetes ?"
    Si vous n'êtes pas à l'aise avec Docker Swarm, **fuyez Kubernetes**. K8s est un écosystème d'une lourdeur prodigieuse qui rajoute de nouvelles couches d'abstraction (Pods, Ingress, ConfigMaps). Swarm utilise exactement les mêmes fichiers `docker-compose.yml` que vous connaissez déjà, il est donc la passerelle idéale pour comprendre l'orchestration multi-nœuds sans douleur.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Docker Compose orchestre des conteneurs sur une machine unique. Dès que votre projet nécessite la résilience de plusieurs serveurs (un Cluster), il faut un véritable orchestrateur. **Docker Swarm** est l'outil parfait pour passer à l'échelle en douceur : il est inclus nativement dans Docker et réutilise la syntaxe YAML de Compose. **Kubernetes** est l'outil ultime, mais sa courbe d'apprentissage vertigineuse le réserve aux grandes infrastructures Cloud.

> Maintenant que nous avons vu comment *conteneuriser* nos applications (Docker) et les *orchestrer* (Swarm), nous devons comprendre comment provisionner les serveurs bruts nécessaires à l'hébergement de ce cluster. C'est le rôle de l'Infrastructure as Code (IaC) de niveau 1 : **Terraform / OpenTofu**.

<br>