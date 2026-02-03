/**
 * CyberQuant Theme Manager
 * Handles Light/Dark mode toggling, system preference detection, and persistence.
 * executed in <head> to prevent FOUC.
 */
(function() {
    // 1. Core Logic: Determine Theme
    function getTheme() {
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            return 'dark';
        } else {
            return 'light';
        }
    }

    // 2. Apply Theme Immediately (Prevent FOUC)
    const theme = getTheme();
    const html = document.documentElement;
    
    if (theme === 'dark') {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
    }

    // 3. UI Logic: Handle Toggle Button (Waits for DOM)
    document.addEventListener('DOMContentLoaded', () => {
        const themeToggleBtn = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');

        // Update Icon based on current state
        function updateIcon() {
            if (!themeIcon) return;
            if (html.classList.contains('dark')) {
                themeIcon.classList.remove('ph-sun');
                themeIcon.classList.add('ph-moon');
            } else {
                themeIcon.classList.remove('ph-moon');
                themeIcon.classList.add('ph-sun');
            }
        }

        // Initial Icon State
        updateIcon();

        // Event Listener
        if (themeToggleBtn) {
            themeToggleBtn.addEventListener('click', () => {
                html.classList.toggle('dark');
                
                if (html.classList.contains('dark')) {
                    localStorage.theme = 'dark';
                } else {
                    localStorage.theme = 'light';
                }
                
                updateIcon();
            });
        }
    });
})();
