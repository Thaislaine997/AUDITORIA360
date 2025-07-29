/*
 * ===================================================================
 * MONITORING DASHBOARD SCRIPT - AUDITORIA 360
 * ===================================================================
 * Descrição: Script modular para o dashboard de monitoramento
 * ===================================================================
 */

// Import modules (in a real setup, these would be actual ES6 imports)
import { MonitoringAPI } from './modules/monitoring-api.js';
import { MetricRenderer } from './modules/metric-renderer.js';
import { AlertRenderer } from './modules/alert-renderer.js';
import { AutoRefresh } from './modules/auto-refresh.js';

class MonitoringDashboard {
  constructor() {
    this.api = new MonitoringAPI();
    this.metricRenderer = new MetricRenderer();
    this.alertRenderer = new AlertRenderer();
    this.autoRefresh = new AutoRefresh(30000); // 30 seconds
    
    this.init();
  }

  async init() {
    try {
      // Load initial data
      await this.loadMetrics();
      await this.loadAlerts();
      
      // Setup auto-refresh
      this.setupAutoRefresh();
      
      // Add loading animations
      this.addLoadingAnimations();
      
      console.log('Monitoring dashboard initialized successfully');
    } catch (error) {
      console.error('Error initializing monitoring dashboard:', error);
    }
  }

  async loadMetrics() {
    try {
      const metrics = await this.api.getMetrics();
      const container = document.getElementById('metrics-container');
      
      if (container) {
        container.innerHTML = this.metricRenderer.renderMetrics(metrics);
      }
    } catch (error) {
      console.error('Error loading metrics:', error);
    }
  }

  async loadAlerts() {
    try {
      const alerts = await this.api.getAlerts();
      const container = document.getElementById('alerts-container');
      
      if (container) {
        container.innerHTML = this.alertRenderer.renderAlerts(alerts);
      }
    } catch (error) {
      console.error('Error loading alerts:', error);
    }
  }

  setupAutoRefresh() {
    this.autoRefresh.start(async () => {
      await this.loadMetrics();
      await this.loadAlerts();
    });

    // Update countdown display
    this.autoRefresh.onCountdown((seconds) => {
      const countdownElement = document.getElementById('refresh-countdown');
      if (countdownElement) {
        countdownElement.textContent = seconds;
      }
    });
  }

  addLoadingAnimations() {
    const cards = document.querySelectorAll('.metric-card');
    cards.forEach((card, index) => {
      card.style.animationDelay = `${index * 0.1}s`;
      card.classList.add('animate-fade-in');
    });
  }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new MonitoringDashboard();
});