/*
 * ===================================================================
 * ALERT RENDERER MODULE - AUDITORIA 360
 * ===================================================================
 * Descrição: Módulo para renderizar alertas do sistema
 * ===================================================================
 */

export class AlertRenderer {
  constructor() {
    this.template = this.getAlertTemplate();
    this.noAlertsTemplate = this.getNoAlertsTemplate();
  }

  // Get alert template
  getAlertTemplate() {
    return `
      <section class="alerts-section" role="region" aria-label="System alerts">
        <h2>🚨 Active Alerts</h2>
        <div class="alerts-container">
          {{alertItems}}
        </div>
      </section>
    `;
  }

  // Get no alerts template
  getNoAlertsTemplate() {
    return `
      <section class="alerts-section" role="region" aria-label="System alerts">
        <h2>🚨 Active Alerts</h2>
        <div class="alert-container no-alerts">
          <strong>✅ No active alerts</strong><br />
          System running smoothly
        </div>
      </section>
    `;
  }

  // Get alert item template
  getAlertItemTemplate() {
    return `
      <div class="alert-item alert-{{level}}">
        <strong>{{icon}} {{title}}</strong><br />
        {{message}}
        <div class="alert-meta">
          <span class="timestamp">{{timestamp}}</span>
          <span class="source">{{source}}</span>
        </div>
      </div>
    `;
  }

  // Render alerts
  renderAlerts(alerts) {
    if (!alerts || alerts.length === 0) {
      return this.noAlertsTemplate;
    }

    const alertItems = alerts.map(alert => this.renderAlert(alert)).join('');
    return this.template.replace('{{alertItems}}', alertItems);
  }

  // Render single alert
  renderAlert(alert) {
    const template = this.getAlertItemTemplate();
    const icon = this.getAlertIcon(alert.level);
    const timestamp = this.formatTimestamp(alert.timestamp);

    return template
      .replace(/{{level}}/g, alert.level)
      .replace(/{{icon}}/g, icon)
      .replace(/{{title}}/g, alert.title || 'Alert')
      .replace(/{{message}}/g, alert.message)
      .replace(/{{timestamp}}/g, timestamp)
      .replace(/{{source}}/g, alert.source || 'System');
  }

  // Get alert icon by level
  getAlertIcon(level) {
    switch (level) {
      case 'critical':
        return '🔴';
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      case 'info':
        return 'ℹ️';
      default:
        return '🔔';
    }
  }

  // Format timestamp
  formatTimestamp(timestamp) {
    if (!timestamp) return '';
    
    const date = new Date(timestamp);
    return date.toLocaleString('pt-BR');
  }

  // Add new alert dynamically
  addAlert(alert) {
    const alertsContainer = document.querySelector('.alerts-container');
    if (alertsContainer) {
      const alertHtml = this.renderAlert(alert);
      alertsContainer.insertAdjacentHTML('afterbegin', alertHtml);
    }
  }

  // Remove alert by ID
  removeAlert(alertId) {
    const alertElement = document.querySelector(`[data-alert-id="${alertId}"]`);
    if (alertElement) {
      alertElement.remove();
    }
  }

  // Clear all alerts
  clearAlerts() {
    const alertsContainer = document.querySelector('.alerts-container');
    if (alertsContainer) {
      alertsContainer.innerHTML = '';
    }
  }
}