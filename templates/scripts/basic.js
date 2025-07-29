/**
 * AUDITORIA360 - Basic Dashboard JavaScript
 * Simple dashboard functionality
 */

class BasicDashboard {
    constructor() {
        this.refreshInterval = 60000; // 1 minute
        this.init();
    }

    /**
     * Initialize basic dashboard
     */
    init() {
        this.updateTimestamp();
        this.setupAutoRefresh();
        this.setupStatusMonitoring();
    }

    /**
     * Update timestamp display
     */
    updateTimestamp() {
        const timestampElement = document.getElementById('timestamp');
        if (timestampElement) {
            const now = new Date();
            const formatoBR = now.toLocaleString('pt-BR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                timeZone: 'America/Sao_Paulo'
            });
            
            timestampElement.textContent = formatoBR;
            timestampElement.setAttribute('datetime', now.toISOString());
        }
    }

    /**
     * Setup auto-refresh
     */
    setupAutoRefresh() {
        setInterval(() => {
            this.refreshStatus();
            this.updateTimestamp();
        }, this.refreshInterval);
    }

    /**
     * Setup status monitoring
     */
    setupStatusMonitoring() {
        // Add interaction to status items
        const statusItems = document.querySelectorAll('.status-item');
        
        statusItems.forEach(item => {
            item.addEventListener('click', () => {
                this.showStatusDetails(item);
            });

            // Add keyboard support
            item.setAttribute('tabindex', '0');
            item.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.showStatusDetails(item);
                }
            });
        });

        // Start status checking
        this.startStatusChecking();
    }

    /**
     * Show status details
     */
    showStatusDetails(statusItem) {
        const statusText = statusItem.textContent.trim();
        alert(`Status: ${statusText}\n\nDetalhes adicionais seriam exibidos aqui.`);
    }

    /**
     * Start periodic status checking
     */
    startStatusChecking() {
        setInterval(() => {
            this.checkSystemStatus();
        }, 30000); // Check every 30 seconds
    }

    /**
     * Check system status
     */
    async checkSystemStatus() {
        try {
            // Simulate status checks
            const statuses = await this.performStatusChecks();
            this.updateStatusDisplay(statuses);
        } catch (error) {
            console.error('Error checking system status:', error);
        }
    }

    /**
     * Perform status checks
     */
    async performStatusChecks() {
        // Simulate API calls for status checking
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    system: Math.random() > 0.05 ? 'ok' : 'error', // 95% uptime
                    api: Math.random() > 0.02 ? 'ok' : 'error',    // 98% uptime
                    database: Math.random() > 0.01 ? 'ok' : 'error' // 99% uptime
                });
            }, 100);
        });
    }

    /**
     * Update status display
     */
    updateStatusDisplay(statuses) {
        const statusItems = document.querySelectorAll('.status-item');
        const statusMap = ['system', 'api', 'database'];

        statusItems.forEach((item, index) => {
            const statusKey = statusMap[index];
            const currentStatus = statuses[statusKey];
            
            // Update class
            item.className = `status-item status-${currentStatus}`;
            
            // Update icon
            const icon = item.querySelector('.status-icon');
            if (icon) {
                icon.textContent = currentStatus === 'ok' ? '✅' : '❌';
            }

            // Update text if needed
            const statusTexts = {
                system: currentStatus === 'ok' ? 'Sistema: Operacional' : 'Sistema: Falha',
                api: currentStatus === 'ok' ? 'API: Funcionando' : 'API: Indisponível',
                database: currentStatus === 'ok' ? 'Database: Conectado' : 'Database: Desconectado'
            };

            const textNode = Array.from(item.childNodes).find(node => 
                node.nodeType === Node.TEXT_NODE
            );
            
            if (textNode) {
                textNode.textContent = statusTexts[statusKey];
            }

            // Update aria-live region for screen readers
            item.setAttribute('aria-live', 'polite');
        });
    }

    /**
     * Refresh status manually
     */
    async refreshStatus() {
        const statusItems = document.querySelectorAll('.status-item');
        
        // Add loading state
        statusItems.forEach(item => {
            item.style.opacity = '0.6';
        });

        try {
            const statuses = await this.performStatusChecks();
            this.updateStatusDisplay(statuses);
        } finally {
            // Remove loading state
            statusItems.forEach(item => {
                item.style.opacity = '1';
            });
        }
    }

    /**
     * Add manual refresh button
     */
    addRefreshButton() {
        const timestampDisplay = document.querySelector('.timestamp-display');
        if (timestampDisplay) {
            const refreshButton = document.createElement('button');
            refreshButton.className = 'button button-sm button-primary';
            refreshButton.innerHTML = '🔄 Atualizar';
            refreshButton.style.marginLeft = '10px';
            
            refreshButton.addEventListener('click', () => {
                this.refreshStatus();
                this.updateTimestamp();
            });

            timestampDisplay.appendChild(refreshButton);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.basicDashboard = new BasicDashboard();
    
    // Add refresh button after initialization
    setTimeout(() => {
        window.basicDashboard.addRefreshButton();
    }, 100);
});