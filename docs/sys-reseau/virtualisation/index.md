---
description: "Comprendre et implémenter les technologies d'isolation et d'hypervision en production."
tags: ["VIRTUALISATION", "HYPERVISEUR", "INFRASTRUCTURE", "KVM", "QEMU"]
---

# Virtualisation (Hyperviseurs)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="Hub Virtualisation">
</div>

!!! quote "Diviser pour mieux régner"
    _Avant la virtualisation, un serveur physique n'hébergeait qu'un seul système d'exploitation. Si le serveur web plantait et faisait un "Kernel Panic", toute la machine s'éteignait, emportant la base de données avec elle. La virtualisation a permis d'isoler chaque application dans sa propre "boîte" (Machine Virtuelle), partageant mathématiquement le processeur et la mémoire du serveur hôte._

## Architecture et Abstraction

Ce hub clôture l'infrastructure classique (avant l'ère des conteneurs Docker/Kubernetes). Comprendre comment un système d'exploitation peut en faire tourner un autre, de manière isolée, est essentiel pour l'Ops et pour le chercheur en sécurité (Malware Analysis).

<div class="grid cards" markdown>

-   :lucide-layers:{ .lg .middle } **Panorama des Hyperviseurs**

    ---
    Comprendre la différence fondamentale entre l'émulation, la virtualisation de Type 1 (Bare-Metal) et de Type 2 (Hosted).

    [:octicons-arrow-right-24: Les concepts de base](./panorama-hyperviseurs.md)

-   :lucide-box:{ .lg .middle } **L'Émulation (QEMU)**

    ---
    Comment faire tourner un programme conçu pour une puce ARM (Raspberry Pi) sur votre processeur Intel/AMD grâce à la traduction d'instructions à la volée.

    [:octicons-arrow-right-24: Comprendre QEMU](./qemu.md)

-   :lucide-server-cog:{ .lg .middle } **KVM & Proxmox**

    ---
    Le standard de l'industrie Open Source. Transformer le noyau Linux lui-même en hyperviseur (KVM) et gérer des clusters entiers de machines virtuelles avec Proxmox VE.

    [:octicons-arrow-right-24: Virtualiser en production](./kvm-proxmox.md)

</div>

## Le lien avec la Cybersécurité (Sandbox)

La virtualisation est l'outil quotidien des chercheurs en cybersécurité. Lorsqu'ils analysent un Ransomware (Malware Analysis), ils ne l'exécutent jamais sur leur propre PC. Ils créent une Machine Virtuelle (Une "Sandbox" ou bac à sable), coupée d'Internet, et lancent le virus à l'intérieur pour observer son comportement en toute sécurité. Une fois l'analyse terminée, ils détruisent la VM en un clic.
