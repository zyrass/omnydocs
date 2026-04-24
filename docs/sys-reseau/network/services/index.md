---
description: "Déploiement et maintien des services fondamentaux de l'infrastructure réseau (DNS, SSH, Fichiers, Annuaires)."
tags: ["SERVICES", "RESEAU", "INFRASTRUCTURE", "SERVEUR"]
---

# Les Services Réseau

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="Sous-Hub Services">
</div>

!!! quote "Les fondations de la communication"
    _Une infrastructure réseau ne sert à rien s'il n'y a rien au bout des câbles. L'administrateur système (Ops) passe la majorité de son temps à installer, configurer et dépanner ces **services fondamentaux**. Si un seul de ces services s'effondre (comme le DNS), c'est l'intégralité de l'entreprise qui s'arrête de fonctionner._

## Panorama des Services d'Infrastructure

Cette section détaille les protocoles et les logiciels les plus couramment déployés dans un environnement d'entreprise, qu'il soit sur site (On-Premise) ou dans le Cloud.

<div class="grid cards" markdown>

-   :lucide-book-marked:{ .lg .middle } **DNS (Bind9 / Unbound)**

    ---
    L'annuaire de l'entreprise. Héberger son propre serveur DNS local pour que les ordinateurs du réseau interne puissent se trouver par leur nom.

    [:octicons-arrow-right-24: Configurer un DNS Local](./dns.md)

-   :lucide-key:{ .lg .middle } **SSH (Secure Shell)**

    ---
    Le tunnel de communication ultime. Pas seulement pour l'administration distante, mais aussi pour les transferts sécurisés (SFTP) et la redirection de ports.

    [:octicons-arrow-right-24: Maîtriser et sécuriser SSH](./ssh.md)

-   :lucide-folder-down:{ .lg .middle } **FTP / SFTP**

    ---
    Les protocoles historiques de transfert de fichiers. Comprendre la différence vitale entre FTP (en clair) et SFTP (chiffré).

    [:octicons-arrow-right-24: Gérer les transferts de fichiers](./ftp.md)

-   :lucide-network:{ .lg .middle } **Partage Windows (Samba)**

    ---
    Le protocole SMB sous Linux. Indispensable pour créer un serveur de fichiers Linux accessible nativement par les ordinateurs Windows de l'entreprise.

    [:octicons-arrow-right-24: Créer un partage Samba](./samba.md)

-   :lucide-users:{ .lg .middle } **LDAP & PAM**

    ---
    L'authentification centralisée (l'équivalent de l'Active Directory, mais pour Linux). Permet de n'avoir qu'un seul mot de passe pour tous les services de l'entreprise.

    [:octicons-arrow-right-24: Centraliser l'identité](./ldap-pam.md)

</div>