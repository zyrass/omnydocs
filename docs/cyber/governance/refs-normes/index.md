---
description: "Vue d’ensemble des autorités, réglementations et référentiels structurants en cybersécurité."
---

# Référentiels & Normes

## Vue d’ensemble

Cette section réunit les **grands piliers** qui encadrent la cybersécurité, la conformité et la gouvernance des systèmes d’information en France et en Europe.  
L’ensemble forme un **écosystème cohérent** composé :

* d’**autorités nationales** qui définissent, recommandent ou contrôlent,
* de **réglementations européennes** qui imposent des obligations,
* de **référentiels et certifications** qui traduisent ces exigences en pratiques opérationnelles.

Chaque élément présenté ici dispose d’une **page dédiée détaillée** dans les sous-sections correspondantes.

!!! info "Comment lire cette carte"
    Le paysage de la cybersécurité se structure en trois couches :
    
    1. **Les autorités françaises**  
        _publient des guides, recommandations et orientations officielles._

    2. **Les réglementations européennes**  
        _définissent les obligations légales transverses._

    3. **Les référentiels et certifications**  
        _fournissent des exigences vérifiables, utilisées pour auditer, qualifier ou sécuriser les systèmes._

## Schéma global de la vue d'ensemble

```mermaid
graph LR
    %% Couche 1 : Autorités françaises
    subgraph "Autorités françaises"
        ANSSI["ANSSI<br/>Sécurité des SI"]
        CNIL["CNIL<br/>Données personnelles"]
        CLUSIF["CLUSIF<br/>Communauté experte SSI"]
    end

    %% Couche 2 : Réglementations européennes
    subgraph "Réglementations Euro."
        RGPD["RGPD<br/>Protection des données"]
        NIS2["NIS2<br/>Cybersécurité renforcée"]
        DORA["DORA<br/>Résilience numérique secteur financier"]
    end

    %% Couche 3 : Référentiels & certifications
    subgraph "Refs. & Certifs"
        SNC["SecNumCloud<br/>Qualification Cloud (ANSSI)"]
        HDS["HDS<br/>Données de santé"]
        PCI["PCI DSS<br/>Données cartes bancaires"]
        NIST["NIST CSF / 800-53<br/>Cadres de contrôle"]
    end

    %% Liens structurants
    CNIL --> RGPD
    ANSSI --> NIS2
    ANSSI --> SNC
    ANSSI --> HDS

    RGPD --> HDS
    RGPD --> PCI

    NIS2 --> SNC
    NIS2 --> NIST

    DORA --> NIST
    DORA --> PCI

    CLUSIF --> RGPD
    CLUSIF --> NIS2
    CLUSIF --> DORA
```

## Présentation des sous-sections

<div class="grid cards" markdown>

-   ### :lucide-building:{ .lg .middle } — Autorité Française

    ---

    Les autorités françaises agissent comme **piliers institutionnels** : elles **précisent**, **interprètent**, **accompagnent** et, dans certains cas, **contrôlent** la mise en œuvre des obligations en cybersécurité et en protection des données.

    [:lucide-book-open-check: Voir la fiche sur les autorités françaises](./autorites)
</div>


<div class="grid cards" markdown>

-   ### :lucide-landmark:{ .lg .middle } — Réglementations européennes

    ---

    Les textes européens définissent les **obligations légales** à respecter. Ils sont transposés ou interprétés en France via les autorités nationales.

    [:lucide-book-open-check: Voir la fiche sur les Réglementations Européennes](./reglementations)
</div>



<div class="grid cards" markdown>

-   ### :lucide-badge-check:{ .lg .middle } — Référentiels & Certifications

    ---

    Ces référentiels transforment les obligations légales en **contrôles opérationnels**, auditables et mesurables. Ils servent de base aux certifications, évaluations ou qualifications.

    [:lucide-book-open-check: Voir la fiche sur les Référentiels et Certifications](./referentiels)
</div>

## Parcours de conformité (vision dynamique)

```mermaid
sequenceDiagram
    participant Org as Organisation
    participant FR as Autorités FR<br/>(ANSSI, CNIL)
    participant EU as UE<br/>(RGPD, NIS2, DORA)
    participant Ref as Référentiels<br/>(SecNumCloud, HDS, PCI DSS, NIST)

    Org->>EU: Analyse des obligations légales
    EU-->>FR: Transposition et recommandations
    FR-->>Org: Interprétation, guides, sanctions

    Org->>Ref: Sélection des référentiels applicables
    Ref-->>Org: Exigences opérationnelles

    Org->>Org: Mise en conformité technique & organisationnelle
```
_Ce parcours illustre de manière simplifiée la manière dont une organisation française engage sa démarche de conformité. Avant toute action technique, elle doit identifier ses obligations légales, comprendre leur interprétation par les autorités nationales, puis sélectionner les référentiels les plus adaptés pour traduire ces exigences en contrôles concrets. La trajectoire représentée ci-dessous montre cette dynamique : de l’analyse réglementaire à la mise en œuvre opérationnelle des mesures de sécurité._

---

## Conclusion

!!! quote "Portail d’introduction"
    Cette page explique où se situe chaque élément, comment il s’articule avec les autres, et **pourquoi* il est essentiel dans le paysage européen de la cybersécurité.
    
    > Les pages dédiées apportent ensuite le **niveau d’expertise détaillé**.

<br />