/**
 * AUDITORIA360 - Dashboard JavaScript
 * Advanced dashboard functionality
 */

class DashboardManager {
    constructor() {
        this.metricsData = {};
        this.refreshInterval = 30000; // 30 seconds
        this.isAutoRefreshEnabled = true;
        this.init();
    }

    /**
     * Initialize dashboard functionality
     */
    init() {
        this.setupMetricsAnimation();
        this.setupAutoRefresh();
        this.setupInteractiveElements();
        this.loadInitialData();
    }

    /**
     * Setup metrics animation on page load
     */
    setupMetricsAnimation() {
        // Animate metrics with staggered timing
        const metricCards = document.querySelectorAll('.metric-card');
        
        metricCards.forEach((card, index) => {
            // Add entrance animation with delay
            setTimeout(() => {
                card.classList.add('animate-fade-in');
            }, index * 150);
        });

        // Animate metric values
        setTimeout(() => {
            AuditoriaUtils.animateMetrics();
        }, 500);
    }

    /**
     * Setup auto-refresh with user controls
     */
    setupAutoRefresh() {
        if (this.isAutoRefreshEnabled) {
            this.scheduleRefresh();
        }

        // Setup pause/resume controls
        this.setupRefreshControls();
    }

    /**
     * Setup refresh controls
     */
    setupRefreshControls() {
        const pauseButton = document.querySelector('.refresh-pause');
        if (pauseButton) {
            pauseButton.addEventListener('click', () => {
                this.toggleAutoRefresh();
            });
        }
    }

    /**
     * Toggle auto-refresh functionality
     */
    toggleAutoRefresh() {
        this.isAutoRefreshEnabled = !this.isAutoRefreshEnabled;
        const pauseButton = document.querySelector('.refresh-pause');
        
        if (pauseButton) {
            pauseButton.textContent = this.isAutoRefreshEnabled ? '⏸️' : '▶️';
            pauseButton.setAttribute('aria-label', 
                this.isAutoRefreshEnabled ? 'Pausar auto-refresh' : 'Retomar auto-refresh'
            );
        }

        if (this.isAutoRefreshEnabled) {
            this.scheduleRefresh();
        } else {
            this.cancelRefresh();
        }

        // Show notification
        this.showNotification(
            this.isAutoRefreshEnabled ? 'Auto-refresh ativado' : 'Auto-refresh pausado',
            this.isAutoRefreshEnabled ? 'success' : 'warning'
        );
    }

    /**
     * Schedule next refresh
     */
    scheduleRefresh() {
        this.refreshTimeout = setTimeout(() => {
            this.refreshData();
        }, this.refreshInterval);
    }

    /**
     * Cancel scheduled refresh
     */
    cancelRefresh() {
        if (this.refreshTimeout) {
            clearTimeout(this.refreshTimeout);
        }
    }

    /**
     * Setup interactive elements
     */
    setupInteractiveElements() {
        // Add click handlers for metric cards
        const metricCards = document.querySelectorAll('.metric-card');
        metricCards.forEach(card => {
            card.addEventListener('click', () => {
                this.showMetricDetails(card);
            });

            // Add keyboard support
            card.setAttribute('tabindex', '0');
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.showMetricDetails(card);
                }
            });
        });

        // Setup real-time updates for status indicators
        this.setupStatusUpdates();
    }

    /**
     * Show metric details in modal or expanded view
     */
    showMetricDetails(card) {
        const title = card.querySelector('.metric-title').textContent;
        const value = card.querySelector('.metric-value').textContent;
        
        // Create simple modal or alert for now
        alert(`Detalhes de ${title}: ${value}\n\nHistórico e dados detalhados seriam exibidos aqui.`);
    }

    /**
     * Setup status updates with WebSocket or polling
     */
    setupStatusUpdates() {
        // For now, use polling. In production, consider WebSocket
        setInterval(() => {
            this.updateStatusIndicators();
        }, 5000); // Update every 5 seconds
    }

    /**
     * Update status indicators
     */
    updateStatusIndicators() {
        const statusDots = document.querySelectorAll('.status-dot');
        statusDots.forEach(dot => {
            // Simulate status check
            const isOnline = Math.random() > 0.1; // 90% uptime simulation
            
            dot.className = `status-dot ${isOnline ? 'status-ok' : 'status-error'}`;
        });
    }

    /**
     * Load initial data
     */
    async loadInitialData() {
        try {
            // Simulate API call
            await this.fetchMetricsData();
            this.updateMetricsDisplay();
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showNotification('Erro ao carregar dados iniciais', 'error');
        }
    }

    /**
     * Fetch metrics data from API
     */
    async fetchMetricsData() {
        // Simulate API response
        return new Promise((resolve) => {
            setTimeout(() => {
                this.metricsData = {
                    systemStatus: 'online',
                    apiResponseTime: Math.floor(Math.random() * 200) + 100,
                    databaseStatus: 'connected',
                    auditoriasHoje: Math.floor(Math.random() * 100) + 200,
                    complianceScore: (Math.random() * 5 + 95).toFixed(1),
                    usuariosAtivos: Math.floor(Math.random() * 50) + 50
                };
                resolve(this.metricsData);
            }, 500);
        });
    }

    /**
     * Update metrics display with new data
     */
    updateMetricsDisplay() {
        const updates = [
            { selector: '[data-metric-value="156"]', value: this.metricsData.apiResponseTime },
            { selector: '[data-metric-value="247"]', value: this.metricsData.auditoriasHoje },
            { selector: '[data-metric-value="985"]', value: this.metricsData.complianceScore },
            { selector: '[data-metric-value="89"]', value: this.metricsData.usuariosAtivos }
        ];

        updates.forEach(update => {
            const element = document.querySelector(update.selector);
            if (element) {
                this.animateValueChange(element, update.value);
            }
        });
    }

    /**
     * Animate value change with smooth transition
     */
    animateValueChange(element, newValue) {
        const currentValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const startTime = performance.now();

        const updateValue = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const value = Math.floor(currentValue + (newValue - currentValue) * progress);
            element.textContent = AuditoriaUtils.formatNumber(value);
            
            if (progress < 1) {
                requestAnimationFrame(updateValue);
            }
        };

        requestAnimationFrame(updateValue);
    }

    /**
     * Refresh all data
     */
    async refreshData() {
        // Show loading state
        this.showLoadingState();

        try {
            await this.fetchMetricsData();
            this.updateMetricsDisplay();
            this.updateTimestamp();
            
            // Schedule next refresh
            if (this.isAutoRefreshEnabled) {
                this.scheduleRefresh();
            }
        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showNotification('Erro ao atualizar dados', 'error');
        } finally {
            this.hideLoadingState();
        }
    }

    /**
     * Show loading state
     */
    showLoadingState() {
        const metricCards = document.querySelectorAll('.metric-card');
        metricCards.forEach(card => {
            card.classList.add('loading');
        });
    }

    /**
     * Hide loading state
     */
    hideLoadingState() {
        const metricCards = document.querySelectorAll('.metric-card');
        metricCards.forEach(card => {
            card.classList.remove('loading');
        });
    }

    /**
     * Update timestamp
     */
    updateTimestamp() {
        const timestampElement = document.getElementById('timestamp');
        if (timestampElement) {
            const now = new Date();
            timestampElement.textContent = now.toLocaleString('pt-BR');
            timestampElement.setAttribute('datetime', now.toISOString());
        }
    }

    /**
     * Show notification to user
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'}-color);
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            z-index: 1001;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.opacity = '1';
        }, 10);

        // Remove after delay
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    /**
     * Cleanup on page unload
     */
    destroy() {
        this.cancelRefresh();
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardManager = new DashboardManager();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.dashboardManager) {
        window.dashboardManager.destroy();
    }
});