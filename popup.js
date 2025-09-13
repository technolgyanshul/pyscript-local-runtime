document.addEventListener('DOMContentLoaded', () => {
    const themeSelect = document.getElementById('theme-select');

    const applyTheme = (theme) => {
        if (theme === 'system') {
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        } else {
            document.documentElement.setAttribute('data-theme', theme);
        }
    };

    const savedTheme = localStorage.getItem('theme') || 'system';
    themeSelect.value = savedTheme;
    applyTheme(savedTheme);

    themeSelect.addEventListener('change', () => {
        const selectedTheme = themeSelect.value;
        localStorage.setItem('theme', selectedTheme);
        applyTheme(selectedTheme);
    });

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (themeSelect.value === 'system') {
            applyTheme('system');
        }
    });
});
