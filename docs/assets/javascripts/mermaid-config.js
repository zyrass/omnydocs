// Configuration globale Mermaid pour Zensical
// Objectif : désactiver les web workers pour corriger le rendu sur Chrome/Brave mobile.
window.mermaid = {
  startOnLoad: true,
  securityLevel: "strict",
  theme: "default",
  // Le point important : désactiver les workers
  workerEnabled: false
};
