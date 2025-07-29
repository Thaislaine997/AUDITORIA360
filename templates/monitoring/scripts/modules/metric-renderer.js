/*
 * ===================================================================
 * METRIC RENDERER MODULE - AUDITORIA 360
 * ===================================================================
 * Descrição: Módulo para renderizar métricas do dashboard
 * ===================================================================
 */

export class MetricRenderer {
  constructor() {
    this.template = this.getMetricTemplate();
  }

  // Get metric card template
  getMetricTemplate() {
    return `
      <article class="metric-card" data-metric-id="{{id}}">
        <h2 class="metric-title">{{icon}} {{title}}</h2>
        <div class="metric-value {{type}}">{{value}}</div>
        <span class="metric-status status-{{statusType}}">{{status}}</span>
      </article>
    `;
  }

  // Render all metrics
  renderMetrics(metrics) {
    return metrics.map(metric => this.renderMetric(metric)).join("");
  }

  // Render single metric
  renderMetric(metric) {
    const statusType = this.getStatusType(metric.type);

    return this.template
      .replace(/{{id}}/g, metric.id)
      .replace(/{{icon}}/g, metric.icon || "")
      .replace(/{{title}}/g, metric.title)
      .replace(/{{value}}/g, metric.value)
      .replace(/{{type}}/g, metric.type)
      .replace(/{{status}}/g, metric.status)
      .replace(/{{statusType}}/g, statusType);
  }

  // Get status type for CSS classes
  getStatusType(type) {
    switch (type) {
      case "success":
        return "ok";
      case "warning":
        return "warning";
      case "danger":
      case "error":
        return "error";
      case "info":
      default:
        return "ok";
    }
  }

  // Update metric value dynamically
  updateMetric(id, newValue, newStatus) {
    const metricCard = document.querySelector(`[data-metric-id="${id}"]`);
    if (metricCard) {
      const valueElement = metricCard.querySelector(".metric-value");
      const statusElement = metricCard.querySelector(".metric-status");

      if (valueElement) {
        valueElement.textContent = newValue;
      }

      if (statusElement && newStatus) {
        statusElement.textContent = newStatus;
      }
    }
  }

  // Add loading state to metrics
  addLoadingState(container) {
    container.innerHTML = '<div class="loading">Carregando métricas...</div>';
  }

  // Remove loading state
  removeLoadingState(container) {
    const loadingElement = container.querySelector(".loading");
    if (loadingElement) {
      loadingElement.remove();
    }
  }
}
