/*
 * ===================================================================
 * BASIC MONITOR SCRIPT - AUDITORIA 360
 * ===================================================================
 * Descrição: Script modular para o monitor básico
 * ===================================================================
 */

// Import modules
import { MonitoringAPI } from "./modules/monitoring-api.js";
import { StatusRenderer } from "./modules/status-renderer.js";

class BasicMonitor {
  constructor() {
    this.api = new MonitoringAPI();
    this.statusRenderer = new StatusRenderer();

    this.init();
  }

  async init() {
    try {
      // Load status data
      await this.loadStatus();

      // Update timestamp
      this.updateTimestamp();

      // Add animations
      this.addAnimations();

      console.log("Basic monitor initialized successfully");
    } catch (error) {
      console.error("Error initializing basic monitor:", error);
    }
  }

  async loadStatus() {
    try {
      const healthChecks = await this.api.getHealthChecks();
      const container = document.getElementById("status-container");

      if (container) {
        container.innerHTML = this.statusRenderer.renderStatus(healthChecks);
      }
    } catch (error) {
      console.error("Error loading status:", error);
    }
  }

  updateTimestamp() {
    const timestampElement = document.getElementById("timestamp");
    if (timestampElement) {
      timestampElement.textContent = new Date().toLocaleString("pt-BR");
    }
  }

  addAnimations() {
    const statusItems = document.querySelectorAll(".status");
    statusItems.forEach((item, index) => {
      item.style.animationDelay = `${index * 0.2}s`;
      item.classList.add("animate-fade-in");
    });
  }
}

// Initialize monitor when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new BasicMonitor();
});
