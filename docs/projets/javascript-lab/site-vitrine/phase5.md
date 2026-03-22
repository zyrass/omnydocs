---
description: "Phase 5 : Compilation pour la production avec Vite.js, minification du Javascript et génération du dossier dist. Prêt pour Vercel ou Netlify."
icon: lucide/rocket
tags: ["VITE", "BUILD", "PRODUCTION", "DEPLOY"]
status: stable
---

# Phase 5 : Compilation & Déploiement

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="30m">
</div>

!!! quote "Objectif de la Phase"
    Le site tourne à merveille sur `localhost:5173`. Mais ce serveur de développement Vite est trop lent (il ne compile rien, il injecte du code à chaud pour vous aider). Nous devons écraser, minifier, et compresser ce code en un paquet minuscule, illisible pour l'homme mais parfait pour le navigateur, afin de le mettre en ligne sur un vrai serveur.

## 1. Lancement du Build de Production

Ouvrez le terminal de Visual Studio Code (en stoppant le serveur actuel via `CTRL + C` si nécessaire).

Dans le même dossier où se trouve votre `package.json`, tapez la commande :

```bash
npm run build
```

Vous devriez voir un log semblable à celui-ci :

```text
> vite build

vite v5.X.X building for production...
✓ 15 modules transformed.
dist/index.html          1.24 kB
dist/assets/index-9f8e7d.js    3.45 kB
dist/assets/style-1a2b3c.css   4.12 kB
```

### Que s'est-il passé ?

- Vite a créé un nouveau dossier appelé `dist/` (Distribution). C'est ce dossier, et **uniquement** ce dossier, qui s'envole vers le serveur de production. (Le `src/` massif et le lourd `node_modules` de X gigaoctets restent chez vous !).
- Il a fusionné TOUS vos petits fichiers (`main.js`, `themeManager.js`, `portfolio.js`, `data.js`) en UN unique fichier `index-[hash].js`.
- Il a minifié le CSS et le JS (Suppression des espaces, commentaires, et renommage des variables `const mySuperLongArray` en `const a`).

## 2. Tester l'Artefact de Production Localement

Ne déployez jamais aveuglément. Vite inclut un mini-serveur serveur statique pour tester exactement ce que vivra l'utilisateur final.

```bash
npm run preview
```

Vite ouvrira génèrera un nouveau lien local (souvent `http://localhost:4173`). Vérifiez l'ensemble de l'interface :
- Le menu Burger s'ouvre-t-il ?
- Mon localStorage se sauvegarde-t-il au rechargement de la page ?
- Les filtres du Portfolio marchent-ils ?

Si oui, vous avez le "Feu Vert".

## 3. Le Déploiement Gratuit Zéro-Friction (Vercel / Netlify)

Dans le monde professionnel moderne, envoyer ses fichiers via un client FTP archaïque (FileZilla) vers un hébergeur comme OVH n'a plus beaucoup de sens pour une SPA (Single Page Application) statique JS.

L'écosystème propose des CI/CD ultra-optimisés gratuits.

1. Créez un compte gratuit sur [Vercel](https://vercel.com/) ou [Netlify](https://www.netlify.com/).
2. Drag & Drop : Prenez purement et simplement votre **dossier `dist`** (Pas votre dossier source !), et glissez-le sur l'interface d'accueil de Netlify.
3. Attendez 5 secondes.
4. Netlify vous confie une URL universelle publique (ex: `https://magnificent-vitrine-123.netlify.app`).

### (Optionnel, Mode Pro) Lier avec GitHub

L'approche Drag & Drop est artisanale. L'Ingénieur déploiera via Git :
1. Créez un dépôt sur GitHub avec l'ensemble du projet.
2. Liez votre compte GitHub à Vercel.
3. Dites à Vercel "C'est un projet Vite".
4. Magie : À chaque fois que vous ferez un `git push` d'une modification, Vercel va intercepter le code, lancer `npm run build` lui-même sur ses serveurs, et déployer en 10 secondes Chrono.

## Checklist de la Phase 5 & Conclusion

- [ ] Mon dossier `dist` a été créé.
- [ ] Le code à l'intérieur de `index-XXXX.js` est illisible (minifié).
- [ ] J'ai vérifié ma production avec `npm run preview`.
- [ ] J'ai envoyé un lien HTTPS public fonctionnel à mes amis ou à mon client.

🏆 **FIN DE LA DYNAMISATION**
Vous êtes passé d'intégrateur HTML/CSS à Développeur Front-End natif. Vous maîtrisez le chaînage d'événements, la modularité et l'UI via les Web Storage API. Mais votre site tourne en circuit fermé sur ses propres données. Pour créer l'immensité du web, il faut dialoguer avec d'autres serveurs planétaires en asynchrone pour pomper et afficher de la donnée tierce...

C'est l'objectif titanesque du prochain projet terminal JS : **Le Hub Applicatif Asynchrone.**
