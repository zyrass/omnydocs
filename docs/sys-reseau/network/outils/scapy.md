---
description: "Créer, manipuler et forger des paquets réseau personnalisés en Python."
icon: lucide/book-open-check
tags: ["SCAPY", "PYTHON", "FORGE", "RESEAU", "SECURITE"]
---

# La Forge Réseau (Scapy)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>

!!! quote "Prendre le contrôle total"
    _Les outils traditionnels (`ping`, `curl`, `nmap`) construisent des paquets réseau pré-définis et vous cachent la machinerie. Vous ne pouvez pas leur dire : "Fais-moi un paquet TCP, mais mets une fausse adresse IP source, et active les flags SYN et FIN en même temps". **Scapy** le peut. C'est un outil interactif (écrit en Python) qui vous permet de forger n'importe quel paquet réseau atome par atome._

## Qu'est-ce que Scapy ?

Scapy est un module Python. Il peut être utilisé soit comme un script Python classique, soit comme une console interactive (qui est en réalité un interpréteur Python spécialisé).

Il est capable de :
1. **Forger** (Créer) de nouveaux paquets.
2. **Décoder** (Lire) des paquets capturés.
3. **Envoyer** des paquets sur le réseau.
4. **Sniffer** (Écouter) les réponses.

*Note : La manipulation de paquets bruts exige les droits `root`.*

---

## 1. Empiler les couches (Le Modèle OSI en pratique)

La syntaxe de Scapy est magique : elle utilise l'opérateur `/` pour empiler les couches du modèle réseau (Encapsulation).

```mermaid
graph TD
    subgraph Forger un paquet avec Scapy
        IP[Couche IP <br/> dst='8.8.8.8']
        TCP[Couche TCP <br/> dport=80, flags='S']
        Payload[Couche Application <br/> 'GET / HTTP/1.1']
    end
    
    IP -->|Encapsule| TCP
    TCP -->|Encapsule| Payload
    
    Code[Code Python : <br/> paquet = IP(...) / TCP(...) / 'GET...'] -.->|L'opérateur '/' empile| Payload
    
    style IP fill:#c0392b,stroke:#fff,color:#fff
    style TCP fill:#2980b9,stroke:#fff,color:#fff
    style Payload fill:#f39c12,stroke:#fff,color:#fff
    style Code fill:#27ae60,stroke:#fff,color:#fff
```

Ouvrez le terminal Scapy en root :
```bash
sudo scapy
```

Pour créer un ping (ICMP) vers Google, on empile la couche 3 (IP) et la couche 4 (ICMP) :
```python
>>> paquet = IP(dst="8.8.8.8") / ICMP()
>>> paquet.show()
```
*Sortie de `show()` :*
```text
###[ IP ]### 
  version   = 4
  ihl       = None
  tos       = 0x0
  len       = None
  id        = 1
  flags     = 
  frag      = 0
  ttl       = 64
  proto     = icmp
  chksum    = None
  src       = 192.168.1.15
  dst       = 8.8.8.8
###[ ICMP ]### 
     type      = echo-request
     code      = 0
...
```
*Scapy a automatiquement rempli les champs obligatoires manquants (comme notre propre IP source et le type ICMP).*

---

## 2. Envoyer et Recevoir (Send / Receive)

Une fois le paquet forgé, il faut l'envoyer. Scapy possède plusieurs fonctions selon ce que vous attendez en retour.

- `send()` : Envoie un paquet au niveau 3 (IP). N'attend pas de réponse.
- `sendp()` : Envoie un paquet au niveau 2 (Ethernet).
- `sr1()` : Envoie un paquet et attend **1** paquet en réponse.

Exemple (Envoyer le ping et recevoir la réponse) :
```python
>>> reponse = sr1( IP(dst="8.8.8.8")/ICMP() )
Begin emission:
Finished sending 1 packets.
*
Received 1 packets, got 1 answers, remaining 0 packets

>>> reponse.show()
```
*Vous verrez alors la réponse de Google (`type = echo-reply`).*

---

## Lien avec la Cybersécurité (L'outil du hacker)

Scapy est rarement utilisé par un administrateur système "Ops" au quotidien, car il est très complexe. En revanche, **c'est l'outil de création de malwares réseau et de scripts de pentest par excellence.**

### Exemple : Usurpation d'adresse IP (IP Spoofing)
Scapy se moque des règles. Il vous laisse écrire une fausse IP source. Si vous envoyez cela, la cible croira que le paquet vient de `1.2.3.4` et renverra la réponse à `1.2.3.4` (ce qui est la base des attaques par déni de service DDoS par amplification).
```python
>>> paquet_malicieux = IP(src="1.2.3.4", dst="8.8.8.8") / TCP(dport=80)
>>> send(paquet_malicieux)
```

### Exemple : Scanner de port furtif (SYN Scan)
Au lieu d'utiliser Nmap, un pirate peut coder son propre scanner de ports en Python en 3 lignes, pour s'assurer d'échapper aux pare-feux standards, en envoyant des paquets TCP malformés ou des flags improbables (comme l'attaque *Xmas Tree*).

## Conclusion

L'utilisation de Scapy exige une maîtrise absolue du fonctionnement de la pile TCP/IP. C'est l'outil qui prouve le dicton : *"On ne peut pas attaquer le réseau si l'on ne sait pas d'abord comment l'ordinateur construit ses paquets."*