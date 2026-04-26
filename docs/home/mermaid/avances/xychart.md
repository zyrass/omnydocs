---
icon: lucide/square-library
---

# XY Chart (beta)

<div
  class="omny-meta"
  data-level="Intermédiaire"
  data-version="1.0"
  data-time="5 minutes">
</div>


!!! note "Importance"
    Le XY chart est utile pour représenter rapidement des scores ou des mesures simples : comparaisons, évolutions, benchmarks. Son support est variable car la syntaxe est encore en version bêta — ce fichier sert précisément à valider le rendu sous Zensical.


!!! quote "Analogie pédagogique"
    _Apprendre la syntaxe de ce diagramme, c'est comme apprendre un nouveau vocabulaire : cela vous permet d'exprimer des idées complexes de manière concise et visuelle._

## Cas d'utilisation

| Domaine | Pertinence | Contexte |
|---|:---:|---|
| Métriques | 🟠 Élevé | Visualisation de scores par domaine, indicateurs de couverture |
| Benchmarks | 🟠 Élevé | Comparaison de niveaux entre profils, environnements ou versions |
| Pilotage | 🟡 Modéré | Représentation d'une progression dans le temps sur un axe quantitatif |
| Tests de compatibilité | 🔴 Critique | Validation du support `xychart-beta` par le renderer Zensical |

## Exemple de diagramme

Le XY chart Mermaid supporte deux types de séries : `bar` pour les barres et `line` pour les courbes. Les axes `x-axis` et `y-axis` acceptent respectivement des labels textuels et une plage numérique. La syntaxe `xychart-beta` est obligatoire — la version stable n'est pas encore disponible.

```mermaid
xychart-beta
  title "Scores par domaine (exemple)"
  x-axis ["Fonda","Dev","Sys","Blue","Red","GRC"]
  y-axis "Score" 0 --> 5
  bar [4,4,4,4,4,2]
```

<p><em>Ce schéma compare des scores par domaine sur une échelle de 0 à 5<br />— représentation alternative à un radar pour une lecture plus linéaire.</em></p>

<br />

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La maîtrise de ce diagramme enrichit considérablement la clarté de votre documentation. Utilisez-le dès qu'une explication textuelle devient trop dense.

<br />

---

!!! info "Lien officiel : [https://mermaid.js.org/syntax/xyChart.html](https://mermaid.js.org/syntax/xyChart.html)"

<br />