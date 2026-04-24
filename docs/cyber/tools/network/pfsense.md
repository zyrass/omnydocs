---
description: "pfSense — Le pare-feu et routeur open-source de référence pour sécuriser les réseaux d'entreprise et domestiques."
icon: lucide/book-open-check
tags: ["INFRA", "PFSENSE", "FIREWALL", "RÉSEAU", "SÉCURITÉ", "RED TEAM"]
---

# pfSense — Le Rempart du Réseau

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2.7+"
  data-time="~1 heure">
</div>

<div style="text-align: center; margin: 0 auto;">
    <img src="/assets/images/cyber/PfSense_logo.png" width="250" align="center" />
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Poste de Douane"
    Imaginez une ville (votre réseau) entourée d'une muraille. Il n'y a qu'une seule porte pour entrer et sortir. **pfSense** est le chef de la douane à cette porte. Il vérifie les papiers de chaque personne (chaque paquet de données), décide qui a le droit d'entrer, qui doit rester dehors, et il peut même fouiller les sacs pour chercher des objets interdits (**IDS/IPS**). C'est lui qui s'assure que personne ne rentre sans invitation.

1.  **Deny All by Default** : Tout ce qui n'est pas explicitement autorisé est interdit.
2.  **Principe du Moindre Privilège** : N'ouvrez que les ports strictement nécessaires vers les machines spécifiques.
3.  **Journalisation (Logging)** : Gardez des traces de tout le trafic bloqué pour identifier les tentatives d'attaque.

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    pfSense est le cerveau de la défense réseau. Sa polyvalence en fait un outil indispensable pour quiconque souhaite construire une infrastructure sécurisée et résiliente. En tant qu'expert en cybersécurité, savoir configurer et auditer un pfSense est une compétence fondamentale pour protéger les actifs numériques.

> Pour sécuriser les accès distants à travers votre pfSense, configurez un serveur **[OpenVPN](./openvpn.md)**.






