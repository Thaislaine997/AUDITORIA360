/*
 * ===================================================================
 * DASHBOARD MODULE - AUDITORIA 360
 * ===================================================================
 * Descrição: Módulo para funcionalidades do dashboard
 * ===================================================================
 */

export interface DashboardMetric {
  id: string;
  title: string;
  value: string | number;
  type: "success" | "warning" | "danger" | "info";
  trend?: {
    value: number;
    direction: "up" | "down" | "stable";
  };
  icon?: string;
}

export interface SystemStatus {
  status: "online" | "offline" | "maintenance";
  lastUpdate: Date;
  services: {
    api: boolean;
    database: boolean;
    monitoring: boolean;
  };
}

export class DashboardService {
  private static instance: DashboardService;

  private constructor() {}

  static getInstance(): DashboardService {
    if (!DashboardService.instance) {
      DashboardService.instance = new DashboardService();
    }
    return DashboardService.instance;
  }

  // Get dashboard metrics
  async getMetrics(): Promise<DashboardMetric[]> {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve([
          {
            id: "audits-today",
            title: "Auditorias Hoje",
            value: 247,
            type: "info",
            trend: { value: 15, direction: "up" },
            icon: "🎯",
          },
          {
            id: "compliance-score",
            title: "Compliance Score",
            value: "98.5%",
            type: "success",
            trend: { value: 2, direction: "up" },
            icon: "🔒",
          },
          {
            id: "active-users",
            title: "Usuários Ativos",
            value: 89,
            type: "info",
            trend: { value: 5, direction: "up" },
            icon: "👥",
          },
          {
            id: "system-status",
            title: "Status Sistema",
            value: "Online",
            type: "success",
            icon: "🔧",
          },
        ]);
      }, 500);
    });
  }

  // Get system status
  async getSystemStatus(): Promise<SystemStatus> {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve({
          status: "online",
          lastUpdate: new Date(),
          services: {
            api: true,
            database: true,
            monitoring: true,
          },
        });
      }, 300);
    });
  }

  // Format metric value for display
  formatMetricValue(value: string | number, type?: string): string {
    if (typeof value === "number") {
      if (type === "percentage") {
        return `${value}%`;
      }
      if (type === "currency") {
        return new Intl.NumberFormat("pt-BR", {
          style: "currency",
          currency: "BRL",
        }).format(value);
      }
      return new Intl.NumberFormat("pt-BR").format(value);
    }
    return value.toString();
  }

  // Get trend icon
  getTrendIcon(direction: "up" | "down" | "stable"): string {
    switch (direction) {
      case "up":
        return "↗️";
      case "down":
        return "↘️";
      case "stable":
        return "➡️";
      default:
        return "";
    }
  }
}

export const dashboardService = DashboardService.getInstance();
