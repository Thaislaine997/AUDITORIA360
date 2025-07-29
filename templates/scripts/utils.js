/**
 * AUDITORIA360 - Shared JavaScript Utilities
 * Common functionality for HTML templates
 */

class AuditoriaUtils {
    constructor() {
        this.init();
    }

    /**
     * Initialize common functionality
     */
    init() {
        this.updateTimestamps();
        this.setupAccessibility();
        this.setupAutoRefresh();
        this.setupThemeToggle();
    }

    /**
     * Update all timestamps on the page
     */
    updateTimestamps() {
        const now = new Date();
        const options = {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZone: 'America/Sao_Paulo'
        };
        
        const formatoBR = now.toLocaleString('pt-BR', options);
        const isoString = now.toISOString();

        // Update footer timestamp
        const footerTimestamp = document.getElementById('footer-timestamp');
        if (footerTimestamp) {
            const timeElement = footerTimestamp.querySelector('time');
            if (timeElement) {
                timeElement.textContent = formatoBR;
                timeElement.setAttribute('datetime', isoString);
            }
        }

        // Update any other timestamp elements
        const timestampElements = document.querySelectorAll('[id*="timestamp"]');
        timestampElements.forEach(element => {
            if (element.id !== 'footer-timestamp') {
                element.textContent = formatoBR;
            }
        });

        console.log('Timestamps updated at:', formatoBR);
    }

    /**
     * Setup accessibility enhancements
     */
    setupAccessibility() {
        // Add keyboard navigation for menu items
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    item.click();
                }
            });
        });

        // Enhanced focus management
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });

        // Skip link functionality
        this.addSkipLink();
    }

    /**
     * Add skip link for accessibility
     */
    addSkipLink() {
        const existingSkipLink = document.querySelector('.skip-link');
        if (existingSkipLink) return;

        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-link';
        skipLink.textContent = 'Pular para o conteúdo principal';
        
        document.body.insertBefore(skipLink, document.body.firstChild);

        // Add main content landmark if it doesn't exist
        const mainContent = document.querySelector('main') || 
                           document.querySelector('[role="main"]') ||
                           document.querySelector('#main-content');
        
        if (mainContent && !mainContent.id) {
            mainContent.id = 'main-content';
        }
    }

    /**
     * Setup auto-refresh functionality with user preference
     */
    setupAutoRefresh() {
        const refreshInterval = this.getRefreshInterval();
        
        if (refreshInterval > 0) {
            setTimeout(() => {
                this.refreshPage();
            }, refreshInterval * 1000);

            // Show refresh indicator
            this.showRefreshIndicator(refreshInterval);
        }
    }

    /**
     * Get refresh interval from meta tag or default
     */
    getRefreshInterval() {
        const metaRefresh = document.querySelector('meta[name="refresh-interval"]');
        if (metaRefresh) {
            return parseInt(metaRefresh.content) || 0;
        }
        
        // Default to 30 seconds for monitoring pages
        if (window.location.pathname.includes('monitoring') || 
            window.location.pathname.includes('dashboard')) {
            return 30;
        }
        
        return 0; // No auto-refresh for other pages
    }

    /**
     * Refresh page with fade effect
     */
    refreshPage() {
        // Check if user is actively interacting
        if (this.isUserActive()) {
            console.log('User is active, skipping auto-refresh');
            this.scheduleNextRefresh();
            return;
        }

        document.body.style.opacity = '0.8';
        setTimeout(() => {
            window.location.reload();
        }, 300);
    }

    /**
     * Check if user is actively interacting with the page
     */
    isUserActive() {
        const now = Date.now();
        const lastActivity = this.lastUserActivity || 0;
        return (now - lastActivity) < 10000; // 10 seconds
    }

    /**
     * Schedule next refresh
     */
    scheduleNextRefresh() {
        const refreshInterval = this.getRefreshInterval();
        if (refreshInterval > 0) {
            setTimeout(() => {
                this.refreshPage();
            }, refreshInterval * 1000);
        }
    }

    /**
     * Show refresh indicator
     */
    showRefreshIndicator(interval) {
        const indicator = document.createElement('div');
        indicator.className = 'refresh-indicator';
        indicator.innerHTML = `
            <span class="refresh-text">Auto-refresh em ${interval}s</span>
            <button class="refresh-pause" aria-label="Pausar auto-refresh">⏸️</button>
        `;
        
        // Add to header if exists
        const header = document.querySelector('.header');
        if (header) {
            header.appendChild(indicator);
        }

        // Handle pause functionality
        indicator.querySelector('.refresh-pause').addEventListener('click', () => {
            this.toggleAutoRefresh();
        });
    }

    /**
     * Toggle auto-refresh on/off
     */
    toggleAutoRefresh() {
        // Implementation for toggling auto-refresh
        console.log('Auto-refresh toggled');
    }

    /**
     * Setup theme toggle functionality
     */
    setupThemeToggle() {
        // Respect user's system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        
        prefersDark.addEventListener('change', (e) => {
            this.applyTheme(e.matches ? 'dark' : 'light');
        });
    }

    /**
     * Apply theme
     */
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('auditoria-theme', theme);
    }

    /**
     * Track user activity for auto-refresh logic
     */
    trackUserActivity() {
        this.lastUserActivity = Date.now();
    }

    /**
     * Format numbers for display
     */
    static formatNumber(number, locale = 'pt-BR') {
        return new Intl.NumberFormat(locale).format(number);
    }

    /**
     * Format currency for display
     */
    static formatCurrency(amount, currency = 'BRL', locale = 'pt-BR') {
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currency
        }).format(amount);
    }

    /**
     * Animate metrics with counting effect
     */
    static animateMetrics() {
        const metrics = document.querySelectorAll('[data-metric-value]');
        
        metrics.forEach(metric => {
            const finalValue = parseInt(metric.dataset.metricValue);
            const duration = 2000; // 2 seconds
            const startTime = performance.now();
            
            const updateValue = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                const currentValue = Math.floor(finalValue * progress);
                metric.textContent = AuditoriaUtils.formatNumber(currentValue);
                
                if (progress < 1) {
                    requestAnimationFrame(updateValue);
                }
            };
            
            requestAnimationFrame(updateValue);
        });
    }

    /**
     * Initialize component when DOM is ready
     */
    static init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                new AuditoriaUtils();
            });
        } else {
            new AuditoriaUtils();
        }
    }
}

// Track user activity
['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
    document.addEventListener(event, () => {
        if (window.auditoriaUtils) {
            window.auditoriaUtils.trackUserActivity();
        }
    }, { passive: true });
});

// Initialize when script loads
AuditoriaUtils.init();

// Export for global access
window.AuditoriaUtils = AuditoriaUtils;