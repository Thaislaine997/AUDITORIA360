/*
 * ===================================================================
 * STATUS RENDERER MODULE - AUDITORIA 360
 * ===================================================================
 * Descrição: Módulo para renderizar status básico do sistema
 * ===================================================================
 */

export class StatusRenderer {
  constructor() {
    this.template = this.getStatusTemplate();
  }

  // Get status template
  getStatusTemplate() {
    return `
      <div class="status {{type}}" role="status">
        <span aria-hidden="true">{{icon}}</span>
        <span>{{service}}: {{status}}</span>
      </div>
    `;
  }

  // Render status items
  renderStatus(healthChecks) {
    return healthChecks.map(check => this.renderStatusItem(check)).join("");
  }

  // Render single status item
  renderStatusItem(check) {
    const { type, icon } = this.getStatusDetails(check.status);

    return this.template
      .replace(/{{type}}/g, type)
      .replace(/{{icon}}/g, icon)
      .replace(/{{service}}/g, check.service)
      .replace(/{{status}}/g, check.message || check.status);
  }

  // Get status details (type and icon)
  getStatusDetails(status) {
    switch (status.toLowerCase()) {
      case "ok":
      case "healthy":
      case "operacional":
      case "funcionando":
      case "conectado":
        return { type: "ok", icon: "✅" };
      case "warning":
      case "degraded":
        return { type: "warning", icon: "⚠️" };
      case "error":
      case "unhealthy":
      case "offline":
        return { type: "error", icon: "❌" };
      default:
        return { type: "ok", icon: "✅" };
    }
  }

  // Update status dynamically
  updateStatus(service, newStatus, newMessage) {
    const statusElements = document.querySelectorAll(".status");

    statusElements.forEach(element => {
      const text = element.textContent;
      if (text.includes(service)) {
        const { type, icon } = this.getStatusDetails(newStatus);

        // Update classes
        element.className = `status ${type}`;

        // Update content
        element.innerHTML = `
          <span aria-hidden="true">${icon}</span>
          <span>${service}: ${newMessage || newStatus}</span>
        `;
      }
    });
  }

  // Add loading state
  addLoadingState(container) {
    container.innerHTML = '<div class="loading">Verificando status...</div>';
  }

  // Remove loading state
  removeLoadingState(container) {
    const loadingElement = container.querySelector(".loading");
    if (loadingElement) {
      loadingElement.remove();
    }
  }
}
