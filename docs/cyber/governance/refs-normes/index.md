---
description: "Vue d'ensemble des autorités, réglementations et référentiels structurants en cybersécurité"
tags: ["RÉFÉRENTIELS", "NORMES", "RÉGLEMENTATION", "CONFORMITÉ"]
---

# Référentiels & Normes

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="5-7 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Les normes et référentiels sont comme le code de la route : ils ne vous apprennent pas à conduire, mais ils garantissent que tout le monde roule de manière prévisible sans provoquer de carambolage systémique._

## Vue d'ensemble

Cette section réunit les **grands piliers** qui encadrent la cybersécurité, la conformité et la gouvernance des systèmes d'information en France et en Europe.

L'ensemble forme un **écosystème cohérent** composé :

* d'**autorités nationales** qui définissent, recommandent ou contrôlent,
* de **réglementations européennes** qui imposent des obligations,
* de **référentiels et certifications** qui traduisent ces exigences en pratiques opérationnelles,
* de **normes ISO** qui fournissent des cadres internationaux de management.

> Chaque élément présenté ici dispose d'une **page dédiée détaillée** dans les sous-sections correspondantes.

## Les quatre piliers de l'écosystème

<div class="grid cards" markdown>

-   :lucide-building:{ .lg .middle } **Autorités françaises**

    ---

    Les autorités françaises agissent comme **piliers institutionnels** : elles **précisent**, **interprètent**, **accompagnent** et, dans certains cas, **contrôlent** la mise en œuvre des obligations en cybersécurité et en protection des données.

    **Acteurs clés** : ANSSI, CNIL, CLUSIF

    [:lucide-book-open-check: Découvrir les autorités françaises](./autorites/)

-   :lucide-landmark:{ .lg .middle } **Réglementations européennes**

    ---

    Les textes européens définissent les **obligations légales** à respecter. Ils sont transposés ou interprétés en France via les autorités nationales et conditionnent l'ensemble de l'écosystème de conformité.

    **Textes majeurs** : RGPD, NIS2, DORA, DSA, DMA, AI Act, Data Act, CRA, DGA

    [:lucide-book-open-check: Découvrir les réglementations européennes](./reglementations/)

</div>

<div class="grid cards" markdown>

-   :lucide-badge-check:{ .lg .middle } **Référentiels & Certifications**

    ---

    Ces référentiels transforment les obligations légales en **contrôles opérationnels**, auditables et mesurables. Ils servent de base aux certifications, évaluations ou qualifications.

    **Référentiels clés** : SecNumCloud, HDS, PCI DSS, NIST CSF

    [:lucide-book-open-check: Découvrir les référentiels et certifications](./referentiels/)

-   :lucide-stamp:{ .lg .middle } **Normes ISO**

    ---

    Les normes ISO fournissent des **cadres internationaux de management** applicables à la sécurité de l'information, la continuité d'activité et la gestion des services IT.

    **Normes majeures** : ISO 27001, ISO 27002, ISO 31000, ISO 22301, ISO 20000

    [:lucide-book-open-check: Découvrir les normes ISO](./isos/)

</div>

## Rôle dans l'écosystème

Ces quatre piliers constituent **le socle réglementaire et normatif** de la cybersécurité en France et en Europe. Ils orientent la compréhension des obligations légales et influencent directement les pratiques de conformité des organisations.

## Parcours de conformité dynamique

```mermaid
---
config:
  theme: "base"
---
sequenceDiagram
    autonumber
    participant Org as 🏢 Organisation
    participant EU as 🇪🇺 UE (Lois)
    participant FR as 🇫🇷 Autorités FR
    participant Ref as 📋 Référentiels
    participant ISO as 🏗️ Normes ISO

    Note over Org, EU: 1. Identification des obligations
    Org->>EU: Analyse du périmètre (NIS2, RGPD, DORA)
    EU-->>Org: Exigences légales & Sanctions

    Note over Org, FR: 2. Cadrage National
    Org->>FR: Consultation des guides (ANSSI, CNIL)
    FR-->>Org: Interprétation & Recommandations

    Note over Org, Ref: 3. Traduction Opérationnelle
    Org->>Ref: Choix des contrôles (PCI DSS, HDS)
    Ref-->>Org: Exigences de certification

    Note over Org, ISO: 4. Management & Certification
    Org->>ISO: Implémentation SMSI (27001)
    ISO-->>Org: Cadre structurant & Amélioration continue

    Note right of Org: 5. Mise en conformité réelle
```

_Ce parcours illustre la cascade de conformité : on part de la **Loi (UE)**, on l'interprète via les **Autorités (FR)**, on la traduit en **Contrôles (Référentiels)** et on la manage via les **Normes (ISO)**._

## Tableau de synthèse des interactions

| Couche | Acteurs | Rôle | Impact |
|--------|---------|------|--------|
| **Autorités FR** | ANSSI, CNIL, CLUSIF | Orientation, interprétation, contrôle | Guides nationaux, sanctions |
| **Réglementations UE** | RGPD, NIS2, DORA, DSA, AI Act | Obligations légales | Sanctions jusqu'à 4% CA ou 10M€ |
| **Référentiels** | SecNumCloud, HDS, PCI DSS, NIST | Contrôles opérationnels | Certification/qualification |
| **Normes ISO** | ISO 27001, 27002, 22301 | Cadres de management | Certification internationale |

> Les pages suivantes détaillent les missions, le périmètre et l'impact de chaque pilier sur la conformité des organisations françaises.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    L'écosystème réglementaire européen et ses déclinaisons nationales ne sont pas une accumulation de textes contradictoires — ils forment une architecture cohérente : la Loi impose, l'Autorité interprète, le Référentiel traduit en contrôles, la Norme structure la mise en œuvre. Maîtriser cette cascade est la compétence fondamentale du professionnel GRC.

> [Approfondissez la démarche SMSI pour structurer votre gouvernance interne →](../smsi/)
