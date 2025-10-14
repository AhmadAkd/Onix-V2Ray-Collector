/**
 * Theme Switcher - Dark/Light Mode Toggle
 * سیستم تغییر تم تاریک/روشن
 */

class ThemeSwitcher {
    constructor() {
        this.currentTheme = this.getStoredTheme() || 'light';
        this.init();
    }
    
    init() {
        // Apply stored theme
        this.applyTheme(this.currentTheme);
        
        // Create toggle button
        this.createToggleButton();
        
        // Listen for system theme changes
        this.watchSystemTheme();
    }
    
    getStoredTheme() {
        return localStorage.getItem('v2ray-theme');
    }
    
    storeTheme(theme) {
        localStorage.setItem('v2ray-theme', theme);
    }
    
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        this.storeTheme(theme);
        
        // Update toggle button
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
    
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        
        // Animate transition
        document.body.style.transition = 'background 0.3s ease, color 0.3s ease';
    }
    
    createToggleButton() {
        const button = document.createElement('button');
        button.id = 'theme-toggle';
        button.className = 'theme-toggle-btn';
        button.innerHTML = `<i id="theme-icon" class="fas fa-${this.currentTheme === 'dark' ? 'sun' : 'moon'}"></i>`;
        button.title = 'تغییر تم';
        button.onclick = () => this.toggleTheme();
        
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .theme-toggle-btn {
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: var(--primary-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                z-index: 9999;
                transition: all 0.3s ease;
            }
            
            .theme-toggle-btn:hover {
                transform: scale(1.1) rotate(15deg);
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
            }
            
            .theme-toggle-btn:active {
                transform: scale(0.95);
            }
            
            @media (max-width: 768px) {
                .theme-toggle-btn {
                    width: 50px;
                    height: 50px;
                    bottom: 20px;
                    right: 20px;
                    font-size: 20px;
                }
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(button);
    }
    
    watchSystemTheme() {
        if (window.matchMedia) {
            const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
            darkModeQuery.addListener((e) => {
                if (!this.getStoredTheme()) {
                    this.applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }
}

// Dark mode CSS variables
const darkModeStyles = `
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --text-primary: #000000;
        --text-secondary: #666666;
        --card-bg: rgba(255, 255, 255, 0.95);
        --border-color: #e0e0e0;
    }
    
    [data-theme="dark"] {
        --bg-primary: #1a1a1a;
        --bg-secondary: #2d2d2d;
        --text-primary: #ffffff;
        --text-secondary: #aaaaaa;
        --card-bg: rgba(45, 45, 45, 0.95);
        --border-color: #404040;
    }
    
    [data-theme="dark"] body {
        background: linear-gradient(135deg, #2d3561 0%, #3d2d54 100%);
        color: var(--text-primary);
    }
    
    [data-theme="dark"] .dashboard-header,
    [data-theme="dark"] .hero-section,
    [data-theme="dark"] .stat-card,
    [data-theme="dark"] .chart-card,
    [data-theme="dark"] .table-card,
    [data-theme="dark"] .protocol-card,
    [data-theme="dark"] .country-card {
        background: var(--card-bg);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    [data-theme="dark"] .custom-table {
        color: var(--text-primary);
    }
    
    [data-theme="dark"] .custom-table thead {
        background: rgba(102, 126, 234, 0.2);
    }
    
    [data-theme="dark"] .custom-table tbody tr {
        background: rgba(255, 255, 255, 0.05);
    }
    
    [data-theme="dark"] .custom-table tbody tr:hover {
        background: rgba(102, 126, 234, 0.1);
    }
`;

// Add dark mode styles to page
const styleElement = document.createElement('style');
styleElement.textContent = darkModeStyles;
document.head.appendChild(styleElement);

// Initialize theme switcher when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.themeSwitcher = new ThemeSwitcher();
    });
} else {
    window.themeSwitcher = new ThemeSwitcher();
}

