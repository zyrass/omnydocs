---
description: "Plongeon dans les magiques d'Alpine : x-init, $watch, $refs, et gestion du temps."
icon: lucide/mountain
tags: ["THEORIE", "ALPINE", "JAVASCRIPT", "LIFECYCLE"]
---

# 04. Réactivité & Boutons Magiques

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Alpine 3.x"
  data-time="3 Heures">
</div>

!!! quote "Les Câblages Sous le Capot"
    Nos données sont connectées à l'écran, oui. Mais que faire lorsque l'on souhaite automatiser une requête API **juste** à l'ouverture de la page ? Ou bien lorsque le changement du nom d'une variable doit déclencher de lourds calculs JavaScript avant de se répercuter ? Pour gérer les coulisses réactives du Framework sans polluer le HTML, on utilise les **Propriétés Magiques**. Toutes les commandes Alpine cachées commencent par le préfixe Dollar : `$`.

<br>

---

## 1. Déclencheurs de Cycle de Vie (x-init)

Une interface s'installe dans le DOM, accomplit des tâches, et meurt à la fermeture du navigateur. Pour initialiser ou automatiser un script dès la création du composant, nous disposons du point d'entrée universel `x-init`.

```html title="Initialisation Asynchrone (Fetch API)"
<div x-data="{ items: [], isLoading: true }" 
     x-init="
        const req = await fetch('https://api.monserveur.net/articles');
        items = await req.json();
        isLoading = false;
     ">
    
    <div x-show="isLoading" class="spinner">Téléchargement en cours...</div>
    
    <ul>
        <template x-for="item in items">
            <li x-text="item.title"></li>
        </template>
    </ul>
</div>
```

_Vous pouvez injecter une pleine requête réseau asynchrone directement dans le `x-init`. Dès que le composant `div` termine de s'imprimer sur l'écran de l'utilisateur, ce code est exécuté._

<br>

---

## 2. Observer avec $watch

Le Data Binding lie une variable à un `input`. Mais `$watch` vous permet de créer une véritable alarme radar. Dès que la variable observée subit une altération (même par le code invisible JS), une fonction lambda exécute un scénario métier.

```html title="Surveillance des données via x-init"
<div x-data="{ codeCVSS: '', isAlert: false }"
     x-init="
        $watch('codeCVSS', (nouveauMode, ancienMode) => {
            if(nouveauMode > 8) {
                isAlert = true;
                notifyAdmin();
            } else {
                isAlert = false;
            }
        })
     ">
     
    <input type="number" x-model="codeCVSS">
    
    <div x-show="isAlert" style="color: red;">
        Alerte Cyber Majeure déclenchée !
    </div>
</div>
```

_Le Hook `$watch` est vital dans le monde Javascript pour éviter d'écouter les événements "change" du hardware : il surveille directement la valeur dans la RAM !_

<br>

---

## 3. L'Échappatoire Sécurisée : $refs

Parfois, on est obligé de manipuler directement le vieux DOM du navigateur (ex: forcer un focus de curseur, récupérer les dimensions exactes X/Y d'un Canvas, initier un graphique ChartJS). Alpine fournit un "raccourci" plutôt que de recourir au long `document.querySelector()`.

```html title="Forcer une manipulation native grâce aux refs"
<div x-data>
    <!-- On signale explicitement qu'on enregistre cet attribut brut -->
    <input type="text" x-ref="monInputSecret" placeholder="Cliquez sur le bouton...">
    
    <!-- On interagit avec l'élément via l'Array $refs -->
    <button @click="$refs.monInputSecret.focus()">
        Attirer le curseur de souris local
    </button>
</div>
```

_Les "Refs" permettent de "sauter par-dessus la barrière du Framework" quand ses mécanismes de Data Binding ne suffisent pas pour un Plugin JQuery ou Chart JS existant._

<br>

---

## Conclusion

!!! quote "Gains d'Architecture"
    Avec les Magics Properties, **votre HTML n'est visuellement plus encombré**. Toute la lourde mécanique de calcul et d'init est repoussée dans `x-init()` ou masquée par `$watch`.

> Reste désormais la conclusion absolue. Jusqu'ici, tous nos composants vivaient en vase clos (un input ne parlait qu'à son parent parent `<div x-data>`). Comment créer des applications majeures où des dizaines de cartes communiquent avec une barre de menu Globale ? Rendons-nous au point final, l'[Écosystème et Production](./05-ecosysteme-production.md).

<br>
