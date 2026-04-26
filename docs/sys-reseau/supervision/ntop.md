---
description: "Inspection visuelle et temporelle du trafic réseau avec ntopng."
icon: lucide/book-open-check
tags: ["NTOP", "SUPERVISION", "RESEAU", "FLUX", "DIAGNOSTIC"]
---

# Observabilité Réseau (Ntop)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="15 - 20 minutes">
</div>


!!! quote "Analogie pédagogique"
    _La supervision (monitoring, logs) est l'équivalent du tableau de bord d'un avion de ligne. Sans ces cadrans et ces alertes, le pilote (l'administrateur) navigue à l'aveugle et ne s'apercevra d'une baisse de pression moteur que lorsque l'avion commencera à perdre de l'altitude._

!!! quote "Voir le sang couler dans les veines"
    _Grafana/Zabbix vous dit que le lien Internet de l'entreprise est saturé à 100%. C'est bien. Mais Zabbix ne sait pas **pourquoi** il est saturé. Est-ce une attaque DDoS ? Est-ce qu'un employé télécharge un jeu vidéo de 100 Go ? Est-ce que le serveur de base de données est en train de répliquer ses fichiers de sauvegarde ? Pour répondre à la question "Qui fait quoi ?", il faut descendre au niveau de l'inspection de paquets. C'est le domaine de **Ntop**._

## 1. Ntopng (Network Top Next Generation)

Le vieux `top` sous Linux liste les processus qui consomment le plus de CPU.
`ntop` a été créé historiquement pour lister "qui consomme le plus de réseau".

Aujourd'hui, l'outil s'appelle **ntopng** et se présente sous la forme d'une interface web incroyablement détaillée. Il se comporte comme un "tcpdump visuel".

### Comment il est positionné ?
Pour que Ntop puisse analyser le réseau, il faut qu'il puisse "voir" tout ce qui passe. On l'installe généralement sur un serveur dont la carte réseau est branchée sur un **Port Miroir (SPAN Port)** du switch central de l'entreprise. Le switch est configuré pour copier 100% de la donnée qui le traverse et l'envoyer vers Ntop.

```mermaid
graph TD
    Internet[Box Internet] --> pfSense[Pare-Feu pfSense]
    pfSense --> Switch[Switch Central]
    
    Switch --> PC1[PC Comptabilité]
    Switch --> Serveur1[Serveur Web]
    Switch -.->|Copie de tous les paquets (Port Miroir)| ServeurNtop[Serveur Ntopng]
    
    style ServeurNtop fill:#e74c3c,stroke:#fff,stroke-width:2px,color:#fff
```

---

## 2. Le DPI (Deep Packet Inspection)

La force majestueuse de Ntopng réside dans son moteur nDPI (Deep Packet Inspection).

Rappelez-vous : avec un tcpdump basique, vous voyez que l'IP locale `192.168.1.5` communique massivement sur Internet sur le port `443` (HTTPS). Problème : sur le port HTTPS, ça peut être Netflix, YouTube, Facebook, du téléchargement Google Drive, ou un malware communiquant en secret. 
Puisque le trafic est chiffré, le port 443 est devenu un fourre-tout aveugle.

Le moteur **nDPI** est capable d'analyser l'enveloppe cryptographique (les certificats SNI, la taille des paquets, les timings) pour **deviner avec une extrême précision l'application**.
Ntopng vous affichera clairement : "L'IP `192.168.1.5` consomme 80% de la bande passante avec l'application *Netflix*".

### Cas d'usage Ops (Le goulot d'étranglement)
Vous êtes ingénieur réseau, la visioconférence (Teams/Zoom) du Directeur coupe sans arrêt à 14h00.
Vous ouvrez Ntopng. Vous voyez que l'application `WindowsUpdate` consomme 95% de la fibre optique, car Microsoft a décidé de pousser une mise à jour sur les 500 PCs de l'entreprise au même moment.
L'analyse est terminée en 3 minutes. Le plan d'action (restreindre Windows Update la nuit) peut commencer.

## Le lien fort avec la Cybersécurité (NTA)

Parce qu'il scrute chaque paquet, Ntopng inclut aujourd'hui nativement des alertes de cybersécurité. Ce domaine s'appelle le **NTA (Network Traffic Analysis)**.

Sans être un pare-feu, Ntopng alertera silencieusement l'équipe réseau si :
- Un ordinateur de la comptabilité commence à émettre des trames de type "Scanner de ports" (Comportement typique d'un Malware qui cherche à se propager).
- Un serveur commence à télécharger des paquets depuis un pays identifié comme "À haut risque" ou vers le réseau Tor (Darknet).
- Il détecte des certificats SSL auto-signés ou périmés.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Une supervision efficace transforme le bruit en alertes exploitables. La centralisation des logs et la création de dashboards pertinents réduisent drastiquement le MTTR (Mean Time To Respond) lors d'un incident.

> [Retourner à l'index →](../index.md)
