---
description: "Glossaire — Administration Réseau : Protocoles, infrastructure, routage, commutation et sécurité réseau."
icon: lucide/book-a
tags: ["GLOSSAIRE", "RÉSEAU", "TCP/IP", "INFRASTRUCTURE"]
---

# Administration Réseau

<div
  class="omny-meta"
  data-level="🟢 Tout niveau"
  data-version="1.0"
  data-time="Consultation">
</div>

## A

!!! note "ARP"
    > Protocole résolvant les adresses IP en adresses MAC sur un réseau local.

    Utilisé pour la communication de niveau 2 dans les réseaux Ethernet — chaque hôte doit connaître l'adresse physique de son interlocuteur avant d'envoyer une trame.

    - **Acronyme :** Address Resolution Protocol
    - **Commandes :** `arp -a`, `ip neighbor`
    - **Risque :** ARP spoofing (usurpation au niveau L2)

    ```mermaid
    graph LR
        A[ARP] --> B[Adresse IP]
        A --> C[Adresse MAC]
        A --> D[Réseau local L2]
    ```

<br>

---

!!! note "AS"
    > Groupe de réseaux IP placés sous une administration technique et politique commune.

    Utilisé dans le routage Internet pour identifier les domaines de routage indépendants. Chaque opérateur ou grande organisation possède un ou plusieurs AS.

    - **Acronyme :** Autonomous System
    - **Identifiant :** ASN (Autonomous System Number)
    - **Protocole de liaison :** BGP (entre AS distincts)

    ```mermaid
    graph LR
        A[AS] --> B[BGP]
        A --> C[Internet]
        A --> D[Routage inter-domaine]
    ```

<br>

---

!!! note "ASN"
    > Identifiant numérique unique attribué à chaque système autonome par un registre Internet régional.

    Indispensable pour établir des sessions BGP avec d'autres opérateurs.

    - **Acronyme :** Autonomous System Number
    - **Plages :** 16 bits (1–65 535), 32 bits (RFC 4893)
    - **Attribution :** RIPE NCC (Europe), ARIN (Amérique du Nord), APNIC (Asie-Pacifique)

    ```mermaid
    graph LR
        A[ASN] --> B[AS]
        A --> C[BGP]
        A --> D[Registres Internet]
    ```

<br>

---

## B

!!! note "BGP"
    > Protocole de routage externe utilisé pour échanger des routes entre systèmes autonomes sur Internet.

    BGP est le protocole qui "colle" Internet : chaque opérateur annonce ses préfixes IP à ses voisins BGP, permettant aux paquets de traverser des dizaines d'AS pour atteindre n'importe quelle destination mondiale.

    - **Acronyme :** Border Gateway Protocol
    - **Types :** eBGP (entre AS différents), iBGP (au sein du même AS)
    - **Spécificité :** routage par politiques, pas uniquement par métriques

    ```mermaid
    graph LR
        A[BGP] --> B[AS]
        A --> C[Internet]
        A --> D[Routage EGP]
    ```

<br>

---

!!! note "Broadcast"
    > Mode de transmission envoyant des données à tous les hôtes d'un même segment réseau simultanément.

    Utilisé pour la découverte de services (ARP, DHCP). Le broadcast est limité au domaine de broadcast et ne franchit pas un routeur.

    - **Domaine :** limité au VLAN ou au sous-réseau
    - **Adresse IPv4 :** dernière adresse du sous-réseau (ex. `192.168.1.255`)
    - **Problématique :** prolifération des broadcasts → dégradation des performances

    ```mermaid
    graph LR
        A[Broadcast] --> B[Domaine de broadcast]
        A --> C[VLAN]
        A --> D[ARP / DHCP]
    ```

<br>

---

## C

!!! note "CIDR"
    > Méthode d'allocation d'adresses IP utilisant une notation de préfixe variable pour optimiser l'espace d'adressage.

    CIDR remplace le système de classes rigides — `192.168.1.0/24` indique que les 24 premiers bits forment l'identifiant réseau.

    - **Acronyme :** Classless Inter-Domain Routing
    - **Notation :** `réseau/longueur_préfixe` (ex. `10.0.0.0/8`)
    - **Avantage :** agrégation de routes (route summarization)

    ```mermaid
    graph LR
        A[CIDR] --> B[Adressage IP]
        A --> C[Sous-réseau]
        A --> D[Masque de réseau]
    ```

<br>

---

!!! note "Collision domain"
    > Zone réseau où les trames peuvent entrer en collision lors de transmissions simultanées sur le même support.

    Le switch segmente ce domaine : chaque port dispose de son propre domaine de collision, permettant le full-duplex.

    - **Cause :** CSMA/CD sur supports partagés (hubs)
    - **Réduction :** utilisation de switches (chaque port = un domaine)
    - **Quasi-disparu :** avec l'adoption du full-duplex et des switches

    ```mermaid
    graph LR
        A[Collision domain] --> B[Ethernet partagé]
        A --> C[Hub]
        A --> D[Switch — segmentation]
    ```

<br>

---

## D

!!! note "DMZ"
    > Zone réseau intermédiaire isolée, exposant des services publics sans compromettre le réseau interne.

    Les serveurs publics y sont hébergés et séparés du LAN par des firewalls. Une compromission en DMZ ne permet pas l'accès direct au réseau interne.

    - **Acronyme :** Demilitarized Zone
    - **Services typiques :** serveurs web, reverse proxy, mail, DNS publics
    - **Architecture :** Internet → Firewall → DMZ → Firewall → LAN

    ```mermaid
    graph LR
        A[DMZ] --> B[Réseau interne]
        A --> C[Internet]
        A --> D[Double Firewall]
    ```

<br>

---

!!! note "DNS"
    > Système hiérarchique distribué assurant la résolution des noms de domaine en adresses IP.

    Le DNS est l'annuaire d'Internet. Une requête remonte la hiérarchie (racine → TLD → serveur autoritaire) pour obtenir l'adresse IP associée à un nom.

    - **Acronyme :** Domain Name System
    - **Composants :** serveurs racines, TLD, serveurs autoritaires, résolveurs récursifs
    - **Enregistrements courants :** A (IPv4), AAAA (IPv6), CNAME, MX, TXT, NS

    ```mermaid
    graph LR
        A[DNS] --> B[Nom de domaine]
        A --> C[Adresse IP]
        A --> D[Hiérarchie résolveurs]
    ```

<br>

---

## E

!!! note "Ethernet"
    > Standard de réseau local filaire le plus répandu, basé sur la trame Ethernet et la commutation de paquets.

    Ethernet équipe la quasi-totalité des LAN professionnels. La commutation a remplacé les collisions partagées par des liens dédiés full-duplex.

    - **Vitesses courantes :** 100 Mbps, 1 Gbps, 10 Gbps, 100 Gbps
    - **Médias :** câble cuivre UTP (Cat5e, Cat6), fibre optique
    - **Standard :** IEEE 802.3

    ```mermaid
    graph LR
        A[Ethernet] --> B[CSMA/CD]
        A --> C[LAN]
        A --> D[Commutation switching]
    ```

<br>

---

## F

!!! note "FQDN"
    > Nom de domaine complet spécifiant la position exacte d'un hôte dans la hiérarchie DNS.

    Un FQDN identifie un hôte de manière unique et non ambiguë sur Internet.

    - **Acronyme :** Fully Qualified Domain Name
    - **Format :** `hôte.domaine.tld.` (le point final désigne la racine implicite)
    - **Exemple :** `mail.example.com` vs. `mail` seul (relatif, ambigu)

    ```mermaid
    graph LR
        A[FQDN] --> B[DNS]
        A --> C[Hiérarchie domaines]
        A --> D[Identification unique]
    ```

<br>

---

## G

!!! note "Gateway"
    > Dispositif réseau assurant la passerelle entre deux réseaux utilisant des protocoles différents ou des espaces d'adressage distincts.

    Sans gateway configurée, un hôte ne peut communiquer qu'au sein de son propre sous-réseau.

    - **Synonyme :** passerelle
    - **Types :** routeur, proxy, NAT gateway, application gateway
    - **Configuration :** adresse IP de la gateway par défaut dans la pile TCP/IP de chaque hôte

    ```mermaid
    graph LR
        A[Gateway] --> B[Routage inter-réseau]
        A --> C[Interconnexion protocoles]
        A --> D[NAT]
    ```

<br>

---

## H

!!! note "HSRP"
    > Protocole propriétaire Cisco de redondance permettant à plusieurs routeurs de partager une adresse IP virtuelle commune.

    HSRP élimine le point de défaillance unique de la passerelle par défaut. Si le routeur actif tombe, le routeur standby prend le relais automatiquement.

    - **Acronyme :** Hot Standby Router Protocol
    - **Propriétaire :** Cisco (équivalent standard : VRRP — RFC 3768)
    - **Rôles :** Active, Standby, Listen ; élection par priorité

    ```mermaid
    graph LR
        A[HSRP] --> B[Redondance passerelle]
        A --> C[Haute disponibilité]
        A --> D[VRRP — standard]
    ```

<br>

---

## I

!!! note "ICMP"
    > Protocole de messages de contrôle et d'erreur intégré à la suite TCP/IP pour les diagnostics réseau.

    `ping` et `traceroute` reposent entièrement sur ICMP pour tester la connectivité et cartographier les chemins réseau.

    - **Acronyme :** Internet Control Message Protocol
    - **Outils :** `ping`, `traceroute` / `tracert`, Path MTU Discovery
    - **Conseil :** bloquer tout ICMP est une mauvaise pratique — certains messages sont essentiels à TCP

    ```mermaid
    graph LR
        A[ICMP] --> B[Diagnostics réseau]
        A --> C[Ping echo]
        A --> D[Traceroute TTL]
    ```

<br>

---

!!! note "IGP"
    > Protocole de routage utilisé à l'intérieur d'un système autonome pour distribuer les routes internes.

    Les IGP apprennent automatiquement les routes et convergent lors de changements topologiques, sans intervention manuelle.

    - **Acronyme :** Interior Gateway Protocol
    - **Exemples :** OSPF (état de liens), EIGRP (Cisco), RIP (distance-vector)
    - **Contraste :** BGP (EGP) gère le routage entre AS distincts

    ```mermaid
    graph LR
        A[IGP] --> B[OSPF]
        A --> C[RIP]
        A --> D[Système autonome interne]
    ```

<br>

---

## L

!!! note "LACP"
    > Protocole standard de négociation pour l'agrégation de plusieurs liens physiques en un lien logique unique.

    Si un lien physique tombe, le trafic bascule automatiquement sur les liens restants.

    - **Acronyme :** Link Aggregation Control Protocol
    - **Standard :** IEEE 802.3ad / 802.1AX
    - **Avantages :** débit agrégé, redondance automatique, répartition de charge

    ```mermaid
    graph LR
        A[LACP] --> B[Agrégation de liens]
        A --> C[Redondance automatique]
        A --> D[Débit cumulé]
    ```

<br>

---

!!! note "Latency"
    > Délai de transmission des données entre un émetteur et un récepteur sur le réseau.

    Critique pour les applications temps-réel (VoIP, jeux en ligne). Elle dépend de la distance physique, des équipements traversés et de la congestion.

    - **Unité :** millisecondes (ms)
    - **Facteurs :** distance, congestion, qualité des équipements, jitter
    - **Outils :** `ping`, `mtr`, outils de monitoring réseau

    ```mermaid
    graph LR
        A[Latency] --> B[Performance réseau]
        A --> C[Délai propagation]
        A --> D[QoS — priorisation]
    ```

<br>

---

## M

!!! note "MAC Address"
    > Identifiant matériel unique de 48 bits attribué à chaque interface réseau pour l'adressage au niveau liaison de données.

    Le switch s'en sert pour construire sa table de commutation et acheminer les trames vers le bon port de destination.

    - **Acronyme :** Media Access Control Address
    - **Format :** `00:1B:44:11:3A:B7` — les 3 premiers octets identifient le fabricant (OUI)
    - **Couche OSI :** Liaison de données — Couche 2

    ```mermaid
    graph LR
        A[MAC Address] --> B[Interface réseau]
        A --> C[Couche 2 liaison]
        A --> D[Table de commutation]
    ```

<br>

---

!!! note "MTU"
    > Taille maximale en octets d'un paquet transmissible sur un lien réseau sans fragmentation.

    Un paquet dépassant la MTU est fragmenté (IPv4) ou rejeté (IPv6). Les Jumbo Frames (9 000 octets) sont utilisées dans les datacenters.

    - **Acronyme :** Maximum Transmission Unit
    - **Ethernet standard :** 1 500 octets
    - **Jumbo Frames :** 9 000 octets (datacenters, iSCSI)
    - **Diagnostic :** `ping -s <taille> -M do` (Path MTU Discovery)

    ```mermaid
    graph LR
        A[MTU] --> B[Fragmentation évitée]
        A --> C[Performance TCP]
        A --> D[Jumbo Frames DC]
    ```

<br>

---

!!! note "Multicast"
    > Mode de transmission envoyant des données à un groupe spécifique d'abonnés, sans dupliquer inutilement le trafic.

    Seuls les hôtes ayant rejoint le groupe reçoivent les données. Utilisé pour l'IPTV, la diffusion de firmware et les protocoles réseau (OSPF, PIM).

    - **Plages :** IPv4 `224.0.0.0/4`, IPv6 `ff00::/8`
    - **Protocoles :** IGMP (gestion des groupes), PIM (routage multicast)
    - **Avantage :** économie de bande passante vs. broadcast

    ```mermaid
    graph LR
        A[Multicast] --> B[Groupe d'abonnés]
        A --> C[IGMP gestion]
        A --> D[Diffusion efficace]
    ```

<br>

---

## N

!!! note "NAT"
    > Technique de traduction des adresses IP permettant à des réseaux privés d'accéder à Internet via une adresse publique partagée.

    Le NAT a permis à Internet de survivre à l'épuisement des adresses IPv4. Il traduit les adresses privées en adresse publique routable.

    - **Acronyme :** Network Address Translation
    - **Types :** statique (1:1), dynamique (pool), PAT/Overload (N:1 — le plus courant)
    - **Limitation :** casse le modèle end-to-end d'Internet, complexifie SIP et FTP actif

    ```mermaid
    graph LR
        A[NAT] --> B[Adresse privée RFC1918]
        A --> C[Adresse publique]
        A --> D[Internet]
    ```

<br>

---

!!! note "NetFlow"
    > Protocole de collecte et d'analyse des métadonnées de trafic réseau pour le monitoring et la sécurité.

    NetFlow ne capture pas le contenu des paquets, mais leurs métadonnées (source, destination, protocole, volume). Précieux pour détecter les anomalies et investiguer des incidents.

    - **Développé par :** Cisco (standard dérivé : IPFIX — RFC 7011)
    - **Versions :** NetFlow v5, v9, puis IPFIX
    - **Cas d'usage :** monitoring, anomalies, facturation, forensics réseau

    ```mermaid
    graph LR
        A[NetFlow] --> B[Métadonnées trafic]
        A --> C[Monitoring réseau]
        A --> D[IPFIX standard]
    ```

<br>

---

## O

!!! note "OSPF"
    > Protocole de routage à état de liens utilisant l'algorithme de Dijkstra pour calculer les chemins optimaux.

    Chaque routeur construit une carte complète de la topologie (LSDB) et calcule indépendamment le chemin le plus court. La convergence est rapide et la métrique basée sur le coût lié à la bande passante.

    - **Acronyme :** Open Shortest Path First
    - **Standards :** RFC 2328 (OSPFv2 IPv4), RFC 5340 (OSPFv3 IPv6)
    - **Concepts clés :** aires (Area 0 = backbone), DR/BDR, LSA, LSDB, SPF tree

    ```mermaid
    graph LR
        A[OSPF] --> B[LSDB état de liens]
        A --> C[Algorithme Dijkstra]
        A --> D[Aires Area 0]
    ```

<br>

---

## P

!!! note "Packet"
    > Unité de données formatée transmise sur un réseau à commutation de paquets, comprenant des en-têtes et le payload.

    Chaque paquet voyage indépendamment et peut emprunter des chemins différents. Les en-têtes sont ajoutés par encapsulation à chaque couche OSI.

    - **Composants :** en-tête L2 (Ethernet), L3 (IP), L4 (TCP/UDP), payload
    - **Processus :** encapsulation (émission) → routage → désencapsulation (réception)
    - **Modèle :** commutation de paquets (Internet) vs. commutation de circuits (PSTN)

    ```mermaid
    graph LR
        A[Packet] --> B[En-têtes OSI]
        A --> C[Payload données]
        A --> D[Routage indépendant]
    ```

<br>

---

!!! note "Port mirroring"
    > Technique de copie du trafic d'un ou plusieurs ports de switch vers un port d'analyse dédié.

    Permet d'analyser le trafic réseau sans l'interrompre ni le perturber — un IDS ou Wireshark est connecté sur le port miroir.

    - **Synonymes :** SPAN (Switched Port Analyzer — Cisco), port monitoring
    - **Types :** SPAN local, RSPAN (switch distant), ERSPAN (via IP)
    - **Applications :** IDS/IPS passif, Wireshark, sondes DLP

    ```mermaid
    graph LR
        A[Port mirroring] --> B[SPAN copie trafic]
        A --> C[Analyse non intrusive]
        A --> D[IDS Wireshark]
    ```

<br>

---

## Q

!!! note "QoS"
    > Ensemble de mécanismes gérant la qualité et la priorité du trafic réseau pour garantir les performances des applications critiques.

    Sans QoS, un transfert de fichier volumineux peut saturer le lien et dégrader la qualité des appels VoIP.

    - **Acronyme :** Quality of Service
    - **Mécanismes :** classification, marquage (DSCP/CoS), mise en file d'attente, limitation de débit
    - **Marquage :** DSCP (Differentiated Services Code Point) dans l'en-tête IP

    ```mermaid
    graph LR
        A[QoS] --> B[Priorité trafic]
        A --> C[DSCP marquage]
        A --> D[VoIP temps-réel]
    ```

<br>

---

## R

!!! note "RIP"
    > Protocole de routage à vecteur de distance utilisant le nombre de sauts comme métrique unique.

    Sa simplicité le rend facile à configurer, mais ses limitations (15 sauts maximum, convergence lente) le rendent inadapté aux réseaux modernes. Remplacé par OSPF.

    - **Acronyme :** Routing Information Protocol
    - **Versions :** RIPv1, RIPv2 (CIDR + auth), RIPng (IPv6)
    - **Limitations :** 15 sauts max, convergence lente (30 s), count-to-infinity

    ```mermaid
    graph LR
        A[RIP] --> B[Distance-vector sauts]
        A --> C[Petits réseaux]
        A --> D[OSPF successeur]
    ```

<br>

---

!!! note "Route"
    > Entrée dans la table de routage définissant le chemin qu'un paquet doit emprunter pour atteindre un réseau de destination.

    Les routes peuvent être statiques (configurées manuellement) ou dynamiques (apprises via OSPF, BGP, etc.).

    - **Composants :** réseau destination, masque, next-hop, interface, métrique
    - **Types :** statique, dynamique, route par défaut (`0.0.0.0/0`)
    - **Commandes :** `ip route show` (Linux), `show ip route` (Cisco IOS)

    ```mermaid
    graph LR
        A[Route] --> B[Table de routage]
        A --> C[Next-hop passerelle]
        A --> D[Statique / Dynamique]
    ```

<br>

---

## S

!!! note "Spanning Tree"
    > Protocole réseau évitant les boucles de commutation dans les infrastructures de switches redondants.

    Sans STP, une trame de broadcast bouclerait à l'infini dans un réseau maillé, saturant complètement l'infrastructure en quelques secondes.

    - **Standards :** IEEE 802.1D (STP), 802.1w (RSTP — rapide), 802.1s (MSTP — multi-instance)
    - **États ports :** Blocking → Listening → Learning → Forwarding
    - **Évolution :** RSTP est aujourd'hui le standard de facto

    ```mermaid
    graph LR
        A[Spanning Tree] --> B[Prévention boucles]
        A --> C[Ports Blocking/Forwarding]
        A --> D[RSTP convergence rapide]
    ```

<br>

---

!!! note "Subnet"
    > Subdivision logique d'un réseau IP en segments plus petits pour améliorer organisation, sécurité et performances.

    Chaque sous-réseau forme un domaine de broadcast isolé, segmentant le réseau par fonction (serveurs, clients, DMZ, management).

    - **Synonyme :** sous-réseau
    - **Outils :** masque de sous-réseau, notation CIDR
    - **Bénéfices :** isolation, segmentation sécurité, réduction broadcast

    ```mermaid
    graph LR
        A[Subnet] --> B[Segmentation IP]
        A --> C[VLAN segmentation L2]
        A --> D[CIDR notation]
    ```

<br>

---

!!! note "Switch"
    > Équipement de commutation opérant au niveau 2 du modèle OSI pour interconnecter les hôtes d'un réseau local.

    Le switch apprend dynamiquement les adresses MAC et achemine les trames uniquement vers le bon port de destination — contrairement au hub qui diffusait à tous.

    - **Fonctions :** apprentissage MAC (table CAM), commutation, filtrage
    - **Évolution :** hub partagé → switch non-manageable → switch manageable (VLAN, QoS, STP)
    - **Niveaux :** L2 (MAC), L3 (routage IP), L4 (QoS)

    ```mermaid
    graph LR
        A[Switch] --> B[Table CAM MAC]
        A --> C[Commutation L2]
        A --> D[VLAN segmentation]
    ```

<br>

---

## T

!!! note "Trunking"
    > Technique permettant de transporter le trafic de plusieurs VLANs sur un seul lien physique entre équipements réseau.

    Chaque trame est étiquetée avec un identifiant VLAN (802.1Q tag) pour maintenir la séparation logique des VLANs sur un lien partagé.

    - **Standard :** IEEE 802.1Q (tag 12 bits = 4094 VLANs possibles)
    - **VLAN natif :** VLAN non étiqueté sur un trunk (modifier le VLAN 1 par défaut pour raisons de sécurité)
    - **Obsolète :** ISL (Inter-Switch Link, Cisco propriétaire)

    ```mermaid
    graph LR
        A[Trunking] --> B[802.1Q étiquetage]
        A --> C[VLANs multiples sur 1 lien]
        A --> D[Interconnexion switches]
    ```

<br>

---

!!! note "TTL"
    > Valeur numérique décrémentée à chaque saut réseau empêchant les paquets de circuler indéfiniment.

    Quand le TTL atteint 0, le paquet est abandonné et un message ICMP "Time Exceeded" est renvoyé. `traceroute` exploite ce mécanisme pour cartographier les chemins.

    - **Acronyme :** Time To Live
    - **Valeurs initiales :** Linux = 64, Windows = 128, Cisco IOS = 255
    - **IPv6 équivalent :** Hop Limit (même concept, nom différent)

    ```mermaid
    graph LR
        A[TTL] --> B[Décrémentation par saut]
        A --> C[Protection boucles]
        A --> D[Traceroute diagnostic]
    ```

<br>

---

## U

!!! note "Unicast"
    > Mode de transmission point à point entre un émetteur unique et un récepteur unique.

    L'unicast est le mode de communication le plus courant — HTTP, SSH, DNS, SMTP. Par opposition, le broadcast diffuse à tous et le multicast cible un groupe.

    - **Contraste :** broadcast (tous), multicast (groupe), anycast (le plus proche)
    - **Avantage :** bande passante ciblée, pas de trafic inutile

    ```mermaid
    graph LR
        A[Unicast] --> B[Point à point]
        A --> C[Broadcast comparaison]
        A --> D[Multicast comparaison]
    ```

<br>

---

## V

!!! note "VLAN"
    > Réseau local virtuel segmentant logiquement un réseau physique en groupes d'hôtes isolés, indépendamment de leur position physique.

    Permet de regrouper des hôtes par fonction (RH, Informatique, Serveurs) sans câblage physique séparé. La communication inter-VLAN nécessite un routeur ou un switch L3.

    - **Acronyme :** Virtual Local Area Network
    - **Plage :** VLAN 1–4094 (1 et 1002–1005 réservés)
    - **Avantages :** segmentation sécurité, réduction broadcast, flexibilité

    ```mermaid
    graph LR
        A[VLAN] --> B[Segmentation logique]
        A --> C[Switch manageable]
        A --> D[Trunking transport]
    ```

<br>

---

!!! note "VRRP"
    > Protocole standard ouvert de redondance de passerelle, permettant à plusieurs routeurs de partager une adresse IP virtuelle.

    Équivalent standardisé (RFC) du HSRP Cisco. Garantit la haute disponibilité de la passerelle par défaut.

    - **Acronyme :** Virtual Router Redundancy Protocol
    - **Standard :** RFC 5798 (VRRPv3 — supporte IPv4 et IPv6)
    - **Élection :** routeur avec la plus haute priorité devient Master (défaut : 100/255)

    ```mermaid
    graph LR
        A[VRRP] --> B[Redondance passerelle]
        A --> C[Haute disponibilité]
        A --> D[HSRP équivalent Cisco]
    ```

<br>

---

!!! note "VTP"
    > Protocole propriétaire Cisco gérant la synchronisation centralisée des informations VLAN entre switches d'un même domaine.

    Un changement de VLAN sur le serveur VTP se propage aux switches clients. Risque : un switch avec un numéro de révision plus élevé peut écraser la config de tout le domaine.

    - **Acronyme :** VLAN Trunking Protocol
    - **Modes :** Server, Client, Transparent
    - **Risque :** suppression accidentelle de tous les VLANs du domaine

    ```mermaid
    graph LR
        A[VTP] --> B[Synchronisation VLANs]
        A --> C[Domaine VTP]
        A --> D[Cisco propriétaire]
    ```

<br>

---

## W

!!! note "WAN"
    > Réseau étendu couvrant une large zone géographique pour interconnecter des sites distants ou des organisations.

    L'accès se fait via des opérateurs télécoms. Latence et débit sont les contraintes principales du WAN.

    - **Acronyme :** Wide Area Network
    - **Technologies :** MPLS (opérateur), SD-WAN, Internet VPN (IPsec/WireGuard), liaisons louées
    - **Métriques :** débit (Mbps/Gbps), latence (ms), disponibilité (uptime %)

    ```mermaid
    graph LR
        A[WAN] --> B[Sites distants]
        A --> C[MPLS SD-WAN]
        A --> D[VPN chiffrement]
    ```

<br>

---

## Conclusion

!!! quote "Résumé — Administration Réseau"
    Maîtriser le vocabulaire réseau, c'est comprendre comment les données voyagent de votre clavier jusqu'au serveur distant : adressage (CIDR, Subnet, NAT), résolution de noms (DNS, FQDN), routage (OSPF, BGP, Route), commutation (Switch, VLAN, Trunking, STP) et optimisation (QoS, LACP, MTU). Ces termes forment le socle de toute infrastructure IT professionnelle.

> Continuez avec le [Glossaire DevSecOps](./devsecops.md) pour explorer les termes liés à l'automatisation, l'infrastructure as code et la sécurité intégrée au cycle de développement.
