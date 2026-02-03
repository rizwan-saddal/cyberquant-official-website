const fs = require('fs');
const path = require('path');

// Configuration
const ROOT_DIR = path.join(__dirname, '..');
const HTML_FILES = [
    path.join(ROOT_DIR, 'index.html'),
    path.join(ROOT_DIR, 'contact.html'),
    path.join(ROOT_DIR, 'security.html')
];
const BACKUP_DIR = path.join(__dirname, '..', 'backups');

// Theme Definitions (Must match prototype_Master.html)
const themes = {
    'cyber-sovereign': {
        dark: '#030712', slate: '#0f172a', blue: '#0ea5e9', neon: '#00f0ff',
        purple: '#8b5cf6', accent: '#10b981', danger: '#ef4444'
    },
    'executive-navy': {
        dark: '#0a192f', slate: '#112240', blue: '#64ffda', neon: '#ccd6f6',
        purple: '#8892b0', accent: '#64ffda', danger: '#ff6b6b'
    },
    'quantum-noir': {
        dark: '#000000', slate: '#121212', blue: '#ffffff', neon: '#e0e0e0',
        purple: '#333333', accent: '#ffffff', danger: '#cf6679'
    },
    'defense-grade': {
        dark: '#1c1c1c', slate: '#2f3136', blue: '#d4af37', neon: '#d4af37',
        purple: '#7289da', accent: '#43b581', danger: '#f04747'
    },
    'crimson-guard': {
        dark: '#1a0505', slate: '#2d0a0a', blue: '#ff3333', neon: '#ff9999',
        purple: '#aa0000', accent: '#ffcc00', danger: '#ff0000'
    },
    'azure-horizon': {
        dark: '#f0f9ff', slate: '#e0f2fe', blue: '#0284c7', neon: '#0ea5e9',
        purple: '#6366f1', accent: '#3b82f6', danger: '#ef4444'
    },
    'sovereign-gold': {
        dark: '#121212', slate: '#1e1e1e', blue: '#ffd700', neon: '#ffed4a',
        purple: '#b8860b', accent: '#daa520', danger: '#cd5c5c'
    },
    'violet-matrix': {
        dark: '#13001f', slate: '#240046', blue: '#9d4edd', neon: '#e0aaff',
        purple: '#7b2cbf', accent: '#c77dff', danger: '#ff006e'
    },
    'corporate-steel': {
        dark: '#1e293b', slate: '#334155', blue: '#94a3b8', neon: '#cbd5e1',
        purple: '#64748b', accent: '#475569', danger: '#ef4444'
    },
    'obsidian-glass': {
        dark: '#050505', slate: '#101010', blue: '#38bdf8', neon: '#7dd3fc',
        purple: '#818cf8', accent: '#34d399', danger: '#fb7185'
    }
};

const themeName = process.argv[2];

if (!themeName || !themes[themeName]) {
    console.error(`Error: Please provide a valid theme name. Options: \n${Object.keys(themes).join(', ')}`);
    process.exit(1);
}

// Helper to convert hex to rgba
function hexToRgba(hex, alpha) {
    let r = parseInt(hex.slice(1, 3), 16),
        g = parseInt(hex.slice(3, 5), 16),
        b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// Ensure backup dir exists
if (!fs.existsSync(BACKUP_DIR)){
    fs.mkdirSync(BACKUP_DIR);
}

// Loop over each file
HTML_FILES.forEach(filePath => {
    if (!fs.existsSync(filePath)) {
        console.warn(`Warning: File not found, skipping: ${filePath}`);
        return;
    }

    // 1. Read file
    let htmlContent;
    try {
        htmlContent = fs.readFileSync(filePath, 'utf8');
    } catch (err) {
        console.error(`Error reading ${filePath}:`, err);
        return;
    }

    // 2. Backup
    const fileName = path.basename(filePath);
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = path.join(BACKUP_DIR, `${fileName}.bak.${timestamp}.${themeName}.html`);
    fs.writeFileSync(backupPath, htmlContent);
    console.log(`Backup created at: ${backupPath}`);

    // 3. Update Colors
    const theme = themes[themeName];
    let updatedContent = htmlContent;

    // 3.1 Special handling for glow
    if (theme.blue) {
        const glowColor = hexToRgba(theme.blue, 0.15);
        const glowRegex = /--color-blue-glow:\s*rgba\(.*?\);/g;
        updatedContent = updatedContent.replace(glowRegex, `--color-blue-glow: ${glowColor};`);
    }

    // 3.2 Update :root variables
    Object.keys(theme).forEach(key => {
        const regex = new RegExp(`--color-${key}:\\s*(#[a-fA-F0-9]{3,6});`, 'g');
        updatedContent = updatedContent.replace(regex, `--color-${key}: ${theme[key]};`);
    });

    // 4. Update Tailwind Config colors
    Object.keys(theme).forEach(key => {
        const regex = new RegExp(`${key}:\\s*'#[a-fA-F0-9]{3,6}'`, 'g');
        updatedContent = updatedContent.replace(regex, `${key}: '${theme[key]}'`);
    });

    fs.writeFileSync(filePath, updatedContent);
    console.log(`Successfully applied theme: ${themeName} to ${fileName}`);
});
