/**
 * AUDITORIA360 - Template Processor
 * Simple template engine for combining components
 */

class TemplateProcessor {
    constructor() {
        this.components = new Map();
        this.loadComponents();
    }

    /**
     * Load all components into memory
     */
    async loadComponents() {
        const componentFiles = [
            'head.html',
            'header.html',
            'footer.html'
        ];

        for (const file of componentFiles) {
            try {
                const response = await fetch(`/templates/components/${file}`);
                const content = await response.text();
                const componentName = file.replace('.html', '').toUpperCase();
                this.components.set(`TEMPLATE_${componentName}_PLACEHOLDER`, content);
            } catch (error) {
                console.warn(`Failed to load component ${file}:`, error);
            }
        }
    }

    /**
     * Process template with given configuration
     */
    async processTemplate(templateConfig) {
        try {
            // Load base template
            const response = await fetch('/templates/base.html');
            let template = await response.text();

            // Replace placeholders with actual content
            template = this.replacePlaceholders(template, templateConfig);

            return template;
        } catch (error) {
            console.error('Error processing template:', error);
            return null;
        }
    }

    /**
     * Replace placeholders in template
     */
    replacePlaceholders(template, config) {
        // Replace component placeholders
        for (const [placeholder, content] of this.components) {
            template = template.replace(`<!-- ${placeholder} -->`, content);
        }

        // Replace configuration placeholders
        const placeholders = {
            'TEMPLATE_TITLE_PLACEHOLDER': config.title || 'Dashboard',
            'TEMPLATE_REFRESH_PLACEHOLDER': config.refreshInterval || '0',
            'TEMPLATE_STYLES_PLACEHOLDER': this.generateStyleLinks(config.styles),
            'TEMPLATE_SCRIPTS_PLACEHOLDER': this.generateScriptTags(config.scripts),
            'TEMPLATE_CONTENT_PLACEHOLDER': config.content || '',
            'TEMPLATE_ANALYTICS_PLACEHOLDER': config.analytics || ''
        };

        for (const [placeholder, value] of Object.entries(placeholders)) {
            const regex = new RegExp(`<!-- ${placeholder} -->`, 'g');
            template = template.replace(regex, value);
        }

        return template;
    }

    /**
     * Generate style link tags
     */
    generateStyleLinks(styles = []) {
        return styles.map(style => 
            `<link rel="stylesheet" href="${style}">`
        ).join('\n    ');
    }

    /**
     * Generate script tags
     */
    generateScriptTags(scripts = []) {
        return scripts.map(script => 
            `<script src="${script}"></script>`
        ).join('\n    ');
    }

    /**
     * Create monitoring dashboard
     */
    static createMonitoringDashboard() {
        const config = {
            title: 'Monitoring Dashboard',
            refreshInterval: '30',
            styles: ['/templates/styles/dashboard.css'],
            scripts: ['/templates/scripts/dashboard.js'],
            content: `
                <div class="dashboard-header">
                    <h1>🎯 AUDITORIA360 - Monitoring Dashboard</h1>
                    <p>Sistema de Monitoramento Avançado em Tempo Real</p>
                </div>
                
                <div class="metrics-grid" role="region" aria-label="Métricas do sistema">
                    <div class="metric-card">
                        <div class="metric-title">🔧 System Status</div>
                        <div class="metric-value" style="color: var(--success-color);" data-metric-value="1">Online</div>
                        <span class="badge badge-success">All Systems Operational</span>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">📊 API Response Time</div>
                        <div class="metric-value" style="color: var(--success-color);" data-metric-value="156">156ms</div>
                        <span class="badge badge-success">Excellent Performance</span>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">💾 Database Status</div>
                        <div class="metric-value" style="color: var(--success-color);" data-metric-value="1">Connected</div>
                        <span class="badge badge-success">12 Active Connections</span>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">🎯 Auditorias Hoje</div>
                        <div class="metric-value" style="color: var(--info-color);" data-metric-value="247">247</div>
                        <span class="badge badge-info">+15% vs ontem</span>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">🔒 Compliance Score</div>
                        <div class="metric-value" style="color: var(--success-color);" data-metric-value="985">98.5%</div>
                        <span class="badge badge-success">LGPD Compliant</span>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">👥 Usuários Ativos</div>
                        <div class="metric-value" style="color: var(--info-color);" data-metric-value="89">89</div>
                        <span class="badge badge-info">Online agora</span>
                    </div>
                </div>
                
                <section class="alerts-section" role="region" aria-label="Alertas do sistema">
                    <h2>🚨 Active Alerts</h2>
                    <div class="alert alert-success" role="alert">
                        <strong>✅ No active alerts</strong><br>
                        System running smoothly
                    </div>
                </section>
            `,
            analytics: '<!-- Google Analytics or other tracking code -->'
        };

        return new TemplateProcessor().processTemplate(config);
    }

    /**
     * Create basic dashboard
     */
    static createBasicDashboard() {
        const config = {
            title: 'Basic Monitor',
            refreshInterval: '60',
            styles: ['/templates/styles/basic.css'],
            scripts: ['/templates/scripts/basic.js'],
            content: `
                <div class="basic-header">
                    <h1>🎯 AUDITORIA360 - Monitor Básico</h1>
                </div>
                
                <div class="status-list" role="region" aria-label="Status dos sistemas">
                    <div class="status-item status-ok" role="status" aria-live="polite">
                        <span class="status-icon" aria-hidden="true">✅</span>
                        Sistema: Operacional
                    </div>
                    <div class="status-item status-ok" role="status" aria-live="polite">
                        <span class="status-icon" aria-hidden="true">✅</span>
                        API: Funcionando
                    </div>
                    <div class="status-item status-ok" role="status" aria-live="polite">
                        <span class="status-icon" aria-hidden="true">✅</span>
                        Database: Conectado
                    </div>
                </div>
                
                <p class="timestamp-display">
                    Última atualização: <time id="timestamp" datetime=""></time>
                </p>
            `
        };

        return new TemplateProcessor().processTemplate(config);
    }
}

// Export for use in other scripts
window.TemplateProcessor = TemplateProcessor;