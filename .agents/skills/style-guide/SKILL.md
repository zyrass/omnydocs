---
name: guide-style
version: 2.0.0
description: "Conventions strictes de rédaction pour documentation technique Zensical."
author: "Alain Guillon"
tags:
  - documentation
  - styleguide
  - zensical
---

# Guide de Style Documentation

## Objectif

Garantir une documentation :

- pédagogique
- professionnelle
- cohérente
- exploitable par un lecteur technique ou débutant

---

## 1. Structure obligatoire

- Respect strict de la hiérarchie Markdown
- Frontmatter cohérent :

  - cours → `book-open-check`
  - index → Aucune icône

## 2. Règles rédactionnelles

- Français professionnel uniquement
- Phrases courtes et claires
- Aucun contenu inutile
- Sujet traité de manière exhaustive

## 3. Approche pédagogique

Chaque introduction doit contenir :

- une analogie claire et pertinente (non fictive)
- une explication progressive

Si un terme est complexe :

- utiliser des notes de bas de page `[^1]`

## 4. Code (obligatoire)

Chaque bloc doit :

- avoir un titre explicite
- être syntaxiquement correct
- être commenté

Format d'exemple :
```js title="Code JavaScript - Import d'un module ES6"
```

Ensuite :

ajouter une explication en italique en utilisant l'underscore "_" autour du texte.

## 5. Illustrations

* Style : cartoon, flat, pédagogique en français
* Emplacement :

  ```
  ./docs/assets/[section]/[sujet]/[detail]/image.png
  ```

Format :

```md
![alt description](path)
<p><em>Explication technique de l’image</em></p>
```

⚠️ Ne jamais utiliser `<figure>`

## 6. Admonitions (Zensical)

Utiliser les admonitions officielles :
[https://zensical.org/docs/authoring/admonitions/](https://zensical.org/docs/authoring/admonitions/)

## 7. Workflow fichiers

Avant toute modification :

1. Créer une copie :

   ```
   fichier-v1-backup.md
   ```

2. Modifier uniquement l’original

3. Chaque séparation dans un fichier doit être précédé d'un espace et de la balise <br> soit :

```
du contenu

<br>

---

Autre contenu
```

## 8. Validation qualité

Toujours vérifier :

* cohérence globale
* conformité aux standards actuels
* absence de perte de clarté

## 9. Conclusion (obligatoire)

```md
## Conclusion

!!! quote "Résumé clair du module"

> Introduction courte vers le module suivant
```

## Règle critique

Priorité absolue :

1. Clarté
2. Pédagogie
3. Cohérence
4. Exhaustivité
