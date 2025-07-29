/*
 * ===================================================================
 * MONITORING MODULE - AUDITORIA 360
 * ===================================================================
 * Descrição: Módulo para funcionalidades de monitoramento
 * ===================================================================
 */

export interface MonitoringAlert {
  id: string;
  level: 'info' | 'warning' | 'error' | 'critical';
  message: string;
  timestamp: Date;
  resolved: boolean;
  source: string;
}

export interface HealthCheck {
  service: string;
  status: 'healthy' | 'degraded' | 'unhealthy';
  responseTime?: number;
  lastCheck: Date;
  error?: string;
}

export interface MonitoringMetrics {
  cpu: number;
  memory: number;
  disk: number;
  network: number;
  requests: number;
  errors: number;
}

export class MonitoringService {
  private static instance: MonitoringService;
  private refreshInterval: number = 30000; // 30 seconds

  private constructor() {}

  static getInstance(): MonitoringService {
    if (!MonitoringService.instance) {
      MonitoringService.instance = new MonitoringService();
    }
    return MonitoringService.instance;
  }

  // Get current alerts
  async getAlerts(): Promise<MonitoringAlert[]> {
    return new Promise((resolve) => {
      setTimeout(() => {
        // For demo, return empty array (no alerts)
        resolve([]);
      }, 200);
    });
  }

  // Get health checks
  async getHealthChecks(): Promise<HealthCheck[]> {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          {
            service: 'API',
            status: 'healthy',
            responseTime: 156,
            lastCheck: new Date(),
          },
          {
            service: 'Database',
            status: 'healthy',
            responseTime: 45,
            lastCheck: new Date(),
          },
          {
            service: 'Authentication',
            status: 'healthy',
            responseTime: 89,
            lastCheck: new Date(),
          },
        ]);
      }, 300);
    });
  }

  // Get system metrics
  async getMetrics(): Promise<MonitoringMetrics> {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          cpu: Math.floor(Math.random() * 30) + 20, // 20-50%
          memory: Math.floor(Math.random() * 20) + 60, // 60-80%
          disk: Math.floor(Math.random() * 10) + 40, // 40-50%
          network: Math.floor(Math.random() * 100),
          requests: Math.floor(Math.random() * 1000) + 500,
          errors: Math.floor(Math.random() * 5),
        });
      }, 250);
    });
  }

  // Auto-refresh monitoring data
  startAutoRefresh(callback: () => void): void {
    setInterval(callback, this.refreshInterval);
  }

  // Format response time
  formatResponseTime(ms: number): string {
    if (ms < 100) {
      return `${ms}ms`;
    } else if (ms < 1000) {
      return `${ms}ms`;
    } else {
      return `${(ms / 1000).toFixed(1)}s`;
    }
  }

  // Get status color for health checks
  getStatusColor(status: HealthCheck['status']): string {
    switch (status) {
      case 'healthy':
        return 'var(--success-color)';
      case 'degraded':
        return 'var(--warning-color)';
      case 'unhealthy':
        return 'var(--danger-color)';
      default:
        return 'var(--muted-text-color)';
    }
  }

  // Get alert level color
  getAlertLevelColor(level: MonitoringAlert['level']): string {
    switch (level) {
      case 'info':
        return 'var(--info-color)';
      case 'warning':
        return 'var(--warning-color)';
      case 'error':
        return 'var(--danger-color)';
      case 'critical':
        return 'var(--danger-color)';
      default:
        return 'var(--muted-text-color)';
    }
  }
}

export const monitoringService = MonitoringService.getInstance();