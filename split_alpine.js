const fs = require('fs');
const path = require('path');

const filepath = 'g:/Omnyvia/omnydocs/docs/dev-cloud/frameworks/alpine/alpinejs-fondamentaux.md';
const outDir = 'g:/Omnyvia/omnydocs/docs/projets/alpine-lab/';

const content = fs.readFileSync(filepath, 'utf8');
const lines = content.split('\n');

const outFiles = {
    1: '03-pentest-tool-p1.md',
    2: '04-pentest-tool-p2.md',
    3: '05-pentest-tool-p3.md',
    4: '06-pentest-tool-p4.md'
};

const fileContents = { 1: [], 2: [], 3: [], 4: [] };
let currentIdx = 1;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('## Phase 2')) {
        currentIdx = 2;
    } else if (line.startsWith('## Phase 4')) {
        currentIdx = 3;
    } else if (line.startsWith('## Phase 6')) {
        currentIdx = 4;
    }
    fileContents[currentIdx].push(line);
}

const frontmatters = {
    2: "---\ndescription: \"Projet 3 - Phase 2 : CRUD, Formulaires et Filtres avec Alpine.js\"\nicon: lucide/mountain\ntags: [\"PROJET\", \"ALPINE\", \"CRUD\"]\n---\n\n",
    3: "---\ndescription: \"Projet 3 - Phase 3 : Calculateurs complexes (CVSS) et Persistance LocalStorage\"\nicon: lucide/mountain\ntags: [\"PROJET\", \"ALPINE\", \"CVSS\", \"PERSISTENCE\"]\n---\n\n",
    4: "---\ndescription: \"Projet 3 - Phase 4 : Export Multi-Format (PDF, Markdown), UX et Librairie\"\nicon: lucide/mountain\ntags: [\"PROJET\", \"ALPINE\", \"EXPORT\", \"UX\"]\n---\n\n"
};

for (let i = 2; i <= 4; i++) {
    if (fileContents[i].length > 0 && fileContents[i][0].startsWith('## Phase')) {
        fileContents[i][0] = fileContents[i][0].replace('## Phase', '# Phase');
    }
}

for (let i = 1; i <= 4; i++) {
    const outPath = path.join(outDir, outFiles[i]);
    const outContent = (i === 1 ? '' : frontmatters[i]) + fileContents[i].join('\n');
    fs.writeFileSync(outPath, outContent, 'utf8');
}

console.log('Split completed successfully with Node!');
