---
description: "Phase 5 : Gestion des flux d'images avec Object-Fit, intégration du Portfolio, et structuration du Footer de clôture. Vérifications finales Multi-Devices."
icon: lucide/image-play
tags: ["CSS", "OBJECT-FIT", "FLEXBOX", "FOOTER"]
status: stable
---

# Phase 5 : Portfolio & Résolution Finale

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="1h00">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Défi du Client"
    "Les 3 piliers de la boîte, c'est fait. L'entête aussi. Maintenant il nous faut une grille avec nos derniers travaux (Portfolio). Le problème, c'est que nos designers téléchargent des images qui n'ont jamais la même taille ou le même ratio (carré, rectangle vertical, 16:9). Le code HTML/CSS doit avaler n'importe quelle image sans la déformer."

En CSS classique (avant 2018), gérer un lot de photographies aux dimensions aléatoires était un calvaire absolu, nécessitant souvent de recadrer manuellement chaque image dans Photoshop. Aujourd'hui, avec la propriété `object-fit`, le navigateur Web s'affirme comme un véritable canevas dynamique.

## 1. Structure HTML du Portfolio

En dessous de la `<section id="services">`, ajoutez la section Portfolio. Reprenons nos classes utilitaires `.section-padding` et `.container` pour gagner du temps.

```html
<section id="portfolio" class="portfolio section-padding">
  
  <div class="container">
    <div class="section-title">
      <h2>Nos Derniers Projets</h2>
      <p>L'excellence créative au service de nos clients.</p>
    </div>

    <!-- Le Container Flexbox du Portfolio -->
    <div class="portfolio-grid">
      
      <!-- Cible 1 : Image Verticale (Portrait) -->
      <div class="portfolio-item">
        <img src="https://images.unsplash.com/photo-1542744094-3a31f272c490?auto=format&fit=crop&w=800&q=80" alt="Refonte UI/UX">
        <div class="portfolio-overlay">
          <h3>Refonte UI/UX</h3>
        </div>
      </div>

      <!-- Cible 2 : Image Horizontale (Paysage) -->
      <div class="portfolio-item">
        <img src="https://images.unsplash.com/photo-1627398240454-e4c1935e463a?auto=format&fit=crop&w=800&q=80" alt="Application SaaS">
        <div class="portfolio-overlay">
          <h3>Application SaaS</h3>
        </div>
      </div>

      <!-- Ajoutez autant de .portfolio-item que désiré (Idéalement 6) -->

    </div> <!-- /portfolio-grid -->
  </div> <!-- /container -->
</section>
```

Le code est épuré. Un conteneur `.portfolio-item` englobe une véritable balise `<img>` (contrairement au `background-image` de la bannière Hero, car l'image du portfolio **a du sens** pour le visiteur SEO) et un encart contenant le futur texte au survol.

## 2. Le CSS : Flexbox & Object-Fit

Pourquoi utiliser Flexbox et non Grid ici ? Pour l'exercice. Nous pourrions très bien utiliser Grid, mais Flexbox avec `flex-wrap: wrap` est utile si nous voulons que les images de la dernière ligne se répartissent d'une façon différente.

```css
/* --- LE PORTFOLIO --- */
.portfolio {
  background-color: var(--color-light); /* Alternance douce de fond si les services étaient blancs */
}

/* Le Container Flexbox Multilignes */
.portfolio-grid {
  display: flex;
  flex-wrap: wrap; /* INTERDICTION de compresser, passe à la ligne */
  gap: var(--spacing-md);
}

/* Le Container Enfant (La tuile individuelle) */
.portfolio-item {
  /* Magie Flexbox: La base est de 300px.
   * flex-grow: 1 (Prend tout l'espace disponible)
   * Résultat : Sur ligne 1, s'il y a 3 boîtes, elles font 33%.
   * S'il y a 2 boîtes sur la dernière ligne, elles feront 50% ! 
   */
  flex: 1 1 300px;
  
  /* L'élément devient la référence (0 de coordonnée) pour ses fils absolus */
  position: relative; 
  height: 300px; /* On force une hauteur stricte */
  border-radius: var(--radius-md);
  
  /* Masque tout ce qui dépasse du border-radius */
  overflow: hidden; 
}
```

### La Révolution `object-fit: cover`

C'est ici que la magie s'opère sur l'image interne brute.

```css
.portfolio-item img {
  width: 100%;
  height: 100%;
  
  /* SANS CETTE REGLE: L'image s'écrase ou s'allonge affreusement !
   * AVEC CETTE REGLE: Le navigateur recadre sans déformer, comme un zoom centré.
   */
  object-fit: cover; 
  
  transition: transform 0.5s ease;
}

/* Au survol de la balise parent, j'agrandis légèrement l'enfant */
.portfolio-item:hover img {
  transform: scale(1.1);
}
```

### Le Filtre d'Informations (Overlay)

On rajoute l'information encadrante (texte) qui n'apparaît qu'au survol de la souris.

```css
.portfolio-overlay {
  position: absolute;
  top: 0; left: 0; bottom: 0; right: 0;
  background: rgba(15, 23, 42, 0.8); /* Noir très légèrement bleuté (--color-dark) */
  color: var(--color-light);
  
  display: flex;
  align-items: center;
  justify-content: center;
  
  /* On le cache initialement avec l'opacité */
  opacity: 0;
  transition: opacity 0.3s ease;
}

.portfolio-item:hover .portfolio-overlay {
  opacity: 1; /* Il apparait magiquement ! */
}
```

## 3. Le Footer Final

Une page n'est jamais terminée sans un pied de page fort, contenant le maillage (les liens) d'autorité et le copyright légal.

```html
<!-- Tout en bas, Sous le Main -->
<footer class="main-footer">
  <div class="container footer-content">
    <div class="footer-brand">
      <h3>DigitalCraft</h3>
      <p>Votre partenaire architectural digital.</p>
    </div>
    
    <div class="footer-links">
        <!-- Liens réseaux sociaux ou légaux -->
        <a href="#">LinkedIn</a> | 
        <a href="#">Mentions Légales</a>
    </div>
  </div>
  
  <div class="copyright">
    <p>&copy; 2026 DigitalCraft Agency. Code artisanal.</p>
  </div>
</footer>
```

```css
/* --- FOOTER --- */
.main-footer {
  background-color: var(--color-dark); /* Le footer est sombre */
  color: var(--color-light); /* Le texte est clair */
  text-align: center;
}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  gap: var(--spacing-md);
}

.copyright {
  border-top: 1px solid rgba(255,255,255, 0.1);
  padding: var(--spacing-md);
  font-size: 0.9rem;
}
```

## 🎯 Liste de Validation Finale du Projet !

Prenez une profonde expiration. Appuyez sur F12. Activez la vue Mobile ("Toggle Device Toolbar").

- [ ] Je n'ai aucune barre de "scrollbar" horizontale sous Firefox ou Chrome. Le site ne glisse pas sur les côtés.
- [ ] Le menu caché Burger s'ouvre, se referme fidèlement via le hack CSS de l'input caché.
- [ ] Mes images Header (Absolute Overlay) et Portfolio (Object-fit) avalent tous les formats sans aucune distorsion du sujet d'origine !
- [ ] À aucun endroit, je n'ai utilisé une unité de `Fixed pixels` écrasant l'espace (Ex: interdiction de mettre des width 1400px sur un conteneur principal). Tout est en Pourcentage '%', ou bridé avec des `max-width`.

🏆 **Conclusion Majeure** : Ce laboratoire confirme vos acquis structurels. Vous avez bâti la carrosserie et le réseau électrique d'une voiture robuste. Vous êtes prêt pour entamer les couches dynamiques de données. Archivez ce projet (Il servira de base au laboratoire JavaScript suivant !).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
