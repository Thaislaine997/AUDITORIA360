/*
 * ===================================================================
 * MONITORING API MODULE - AUDITORIA 360
 * ===================================================================
 * Descrição: Módulo para comunicação com APIs de monitoramento
 * ===================================================================
 */

export class MonitoringAPI {
  constructor(baseUrl = "/api") {
    this.baseUrl = baseUrl;
  }

  // Get system metrics
  async getMetrics() {
    // Mock data for demo - in real app, this would fetch from actual API
    return new Promise(resolve => {
      setTimeout(() => {
        resolve([
          {
            id: "system-status",
            title: "System Status",
            value: "Online",
            type: "success",
            status: "All Systems Operational",
            icon: "🔧",
          },
          {
            id: "response-time",
            title: "API Response Time",
            value: "156ms",
            type: "success",
            status: "Excellent Performance",
            icon: "📊",
          },
          {
            id: "database-status",
            title: "Database Status",
            value: "Connected",
            type: "success",
            status: "12 Active Connections",
            icon: "💾",
          },
          {
            id: "audits-today",
            title: "Auditorias Hoje",
            value: "247",
            type: "info",
            status: "+15% vs ontem",
            icon: "🎯",
          },
          {
            id: "compliance-score",
            title: "Compliance Score",
            value: "98.5%",
            type: "success",
            status: "LGPD Compliant",
            icon: "🔒",
          },
          {
            id: "active-users",
            title: "Usuários Ativos",
            value: "89",
            type: "info",
            status: "Online agora",
            icon: "👥",
          },
        ]);
      }, 500);
    });
  }

  // Get alerts
  async getAlerts() {
    // Mock data for demo - in real app, this would fetch from actual API
    return new Promise(resolve => {
      setTimeout(() => {
        resolve([]); // No alerts for demo
      }, 300);
    });
  }

  // Get health checks
  async getHealthChecks() {
    // Mock data for demo
    return new Promise(resolve => {
      setTimeout(() => {
        resolve([
          { service: "Sistema", status: "ok", message: "Operacional" },
          { service: "API", status: "ok", message: "Funcionando" },
          { service: "Database", status: "ok", message: "Conectado" },
        ]);
      }, 200);
    });
  }

  // Generic API request method
  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("API request failed:", error);
      throw error;
    }
  }
}
