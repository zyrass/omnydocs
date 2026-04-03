const fs = require('fs');
const path = require('path');

const srcPath = 'g:/Omnyvia/omnydocs/docs/dev-cloud/frameworks/alpine/alpinejs-fondamentaux.md';
const destPath = 'g:/Omnyvia/omnydocs/docs/projets/alpine-lab/03-pentest-tool.md';
const imagePath = 'file:///C:/Users/alain/.gemini/antigravity/brain/9e92fb0e-7515-41e9-81d3-d924f9af076c/alpine_pentest_tool_1775229161266.png';

try {
    const rawContent = fs.readFileSync(srcPath, 'utf8');
    
    // Extrait à partir du premier vrai contenu (En dessous de <div class="omny-meta"...>)
    const contentLines = rawContent.split('\n');
    let outputLines = [];
    
    // Inject the frontmatter
    outputLines.push('---');
    outputLines.push('description: "Projet 3 : Créer un outil professionnel de Pentest Reporting avec Alpine.js"');
    outputLines.push('icon: lucide/mountain');
    outputLines.push('tags: ["PROJET", "ALPINE", "JAVASCRIPT", "CYBERSECURITY"]');
    outputLines.push('---');
    outputLines.push('');
    outputLines.push('# Pentest Reporting Tool');
    outputLines.push('');
    outputLines.push('<div');
    outputLines.push('  class="omny-meta"');
    outputLines.push('  data-level="🔴 Avancé"');
    outputLines.push('  data-version="Alpine 3.x"');
    outputLines.push('  data-time="15 Heures">');
    outputLines.push('</div>');
    outputLines.push('');
    
    let started = false;
    for (let i = 0; i < contentLines.length; i++) {
        if (!started && contentLines[i].startsWith('!!! quote "Analogie pédagogique"')) {
            started = true;
            outputLines.push(contentLines[i]);
            outputLines.push(contentLines[i+1]);
            
            outputLines.push('<br>\n');
            outputLines.push(`![Alpine Pentest Tool Mockup](${imagePath})`);
            outputLines.push('<p><em>Maquette UI conceptuelle du projet : Le Dashboard complet avec calculs CVSS et exports.</em></p>\n');
            outputLines.push('<br>\n');
            
            i++; // skip next since we copied it
            continue;
        }
        if (started) {
            outputLines.push(contentLines[i]);
        }
    }
    
    // Si cela s'est bien passé
    fs.writeFileSync(destPath, outputLines.join('\n'), 'utf8');
    console.log("SUCCESS");
} catch (e) {
    console.error("ERREUR:", e);
}
