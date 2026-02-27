document.addEventListener("DOMContentLoaded", initMermaid);

function initMermaid() {
  if (typeof mermaid === "undefined") return;

  try {
    mermaid.initialize({ startOnLoad: false });
    mermaid.run({
      querySelector: ".language-mermaid, .mermaid",
    });
  } catch (e) {
    console.warn("Mermaid init error:", e);
  }
}

const observer = new MutationObserver(() => {
  initMermaid();
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
});
