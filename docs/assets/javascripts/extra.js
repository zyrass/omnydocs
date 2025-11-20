/* JavaScript supplémentaire : https://zensical.org/docs/customization/#additional-javascript */

/**
 * ---------------------------------------------------------------------------
 * Composant dynamique : Metadata (niveau, version, durée)
 * ---------------------------------------------------------------------------
 * Ce script transforme automatiquement tout élément HTML ayant la classe
 * `.omny-meta` en un bloc complet et stylisé de métadonnées.
 *
 * API d'utilisation dans Markdown :
 *
 *    <div
 *      class="omny-meta"
 *      data-level="🟢 Débutant & 🟡 Intermédiaire"
 *      data-version="1.4"
 *      data-time="35-40 minutes">
 *    </div>
 *
 * Le JavaScript génère automatiquement le HTML final :
 *
 *    <aside class="metadata">
 *      <span class="metadata__version">v1.4</span>
 *      <span class="metadata__niveau">🟢 Débutant & 🟡 Intermédiaire</span>
 *      <div class="metadata__duree">
 *        <span class="metadata__duree-text">Temps de lecture estimé :</span>
 *        <span class="metadata__duree-time">35-40 minutes</span>
 *      </div>
 *    </aside>
 *
 * Objectifs :
 *   - Réutilisable partout
 *   - Aucun HTML compliqué dans les fichiers Markdown
 *   - Compatible thème light/dark (CSS via Zensical)
 *   - Facilement extensible (statuts, badges, tags…)
 * ---------------------------------------------------------------------------
 */

/**
 * Fonction principale de transformation des blocs omny-meta
 */
function transformMetadataBlocks() {
  /**
   * Sélectionne tous les blocs Metadata déclarés via la classe `omny-meta`.
   *
   * Exemple dans un fichier .md :
   *   <div class="omny-meta" data-level="..." data-version="..." data-time="..."></div>
   */
  const metaBlocks = document.querySelectorAll(".omny-meta");

  // Si aucun bloc trouvé, on arrête (évite les exécutions inutiles)
  if (metaBlocks.length === 0) return;

  // Parcourt chaque bloc trouvé
  metaBlocks.forEach((placeholder) => {
    /**
     * Extraction des paramètres déclarés en data-attributes.
     *
     * data-level   → difficulté ou public cible
     * data-version → numéro de version (ex: "1.4")
     * data-time    → temps estimé (ex: "30-40 minutes")
     */
    const level = placeholder.dataset.level || "";
    const version = placeholder.dataset.version || "";
    const time = placeholder.dataset.time || "";

    /**
     * Construction du HTML final.
     * Le bloc <span class="metadata__version"> est inséré uniquement si une
     * version est fournie (condition ternaire propre et compacte).
     */
    const html = `
      <aside class="metadata">
        ${version ? `<span class="metadata__version">v${version}</span>` : ""}
        <span class="metadata__niveau">${level}</span>
        <div class="metadata__duree">
          <span class="metadata__duree-text">Temps de lecture estimé :</span>
          <span class="metadata__duree-time">${time}</span>
        </div>
      </aside>
    `;

    /**
     * Remplacement propre :
     * outerHTML permet de remplacer entièrement le placeholder original.
     *
     * On supprime donc le <div class="omny-meta"> et on injecte directement
     * le <aside class="metadata"> final, parfaitement stylisé par le CSS.
     */
    placeholder.outerHTML = html;
  });

  console.log(`✅ OmnyMeta: ${metaBlocks.length} bloc(s) transformé(s)`);
}

/**
 * ---------------------------------------------------------------------------
 * STRATÉGIE DE DÉCLENCHEMENT MULTIPLE
 * ---------------------------------------------------------------------------
 * Zensical peut charger le contenu à différents moments selon le contexte :
 * - Navigation initiale
 * - Navigation client-side (SPA)
 * - Rechargement de page
 *
 * On écoute donc TOUS les événements pertinents pour garantir l'exécution.
 * ---------------------------------------------------------------------------
 */

// 1️⃣ Chargement initial du DOM
document.addEventListener("DOMContentLoaded", transformMetadataBlocks);

// 2️⃣ Chargement complet de la page (fallback si DOMContentLoaded rate)
window.addEventListener("load", transformMetadataBlocks);

// 3️⃣ Navigation client-side (SPA) - événement custom Zensical
document.addEventListener("zensical:navigation", transformMetadataBlocks);

// 4️⃣ MutationObserver - détecte les changements dynamiques dans le DOM
const observer = new MutationObserver(() => {
  // On vérifie s'il y a de nouveaux blocs omny-meta non transformés
  const untransformedBlocks = document.querySelectorAll(".omny-meta");
  if (untransformedBlocks.length > 0) {
    transformMetadataBlocks();
  }
});

// Observe le body pour détecter les ajouts dynamiques de contenu
observer.observe(document.body, {
  childList: true, // Détecte l'ajout/suppression d'éléments
  subtree: true, // Observe tous les descendants
});
