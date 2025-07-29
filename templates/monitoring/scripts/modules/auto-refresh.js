/*
 * ===================================================================
 * AUTO REFRESH MODULE - AUDITORIA 360
 * ===================================================================
 * Descrição: Módulo para auto-refresh de dados do dashboard
 * ===================================================================
 */

export class AutoRefresh {
  constructor(interval = 30000) {
    this.interval = interval;
    this.intervalId = null;
    this.countdownId = null;
    this.isRunning = false;
    this.onCountdownCallback = null;
  }

  // Start auto-refresh
  start(callback) {
    if (this.isRunning) {
      this.stop();
    }

    this.isRunning = true;
    
    // Execute immediately
    callback();
    
    // Setup interval
    this.intervalId = setInterval(() => {
      callback();
    }, this.interval);

    // Setup countdown
    this.startCountdown();
  }

  // Stop auto-refresh
  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }

    if (this.countdownId) {
      clearInterval(this.countdownId);
      this.countdownId = null;
    }

    this.isRunning = false;
  }

  // Start countdown display
  startCountdown() {
    let seconds = this.interval / 1000;
    
    // Update immediately
    if (this.onCountdownCallback) {
      this.onCountdownCallback(seconds);
    }

    this.countdownId = setInterval(() => {
      seconds--;
      
      if (this.onCountdownCallback) {
        this.onCountdownCallback(seconds);
      }

      if (seconds <= 0) {
        seconds = this.interval / 1000;
      }
    }, 1000);
  }

  // Set countdown callback
  onCountdown(callback) {
    this.onCountdownCallback = callback;
  }

  // Change interval
  setInterval(newInterval) {
    this.interval = newInterval;
    
    if (this.isRunning) {
      // Restart with new interval
      const currentCallback = this.callback;
      this.stop();
      this.start(currentCallback);
    }
  }

  // Get current interval
  getInterval() {
    return this.interval;
  }

  // Check if running
  isActive() {
    return this.isRunning;
  }

  // Pause auto-refresh (can be resumed)
  pause() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }

    if (this.countdownId) {
      clearInterval(this.countdownId);
      this.countdownId = null;
    }
  }

  // Resume auto-refresh
  resume(callback) {
    if (!this.isRunning) {
      return;
    }

    this.intervalId = setInterval(() => {
      callback();
    }, this.interval);

    this.startCountdown();
  }

  // Force refresh now
  refreshNow(callback) {
    if (callback) {
      callback();
    }
    
    // Reset countdown
    if (this.isRunning) {
      this.pause();
      this.resume(callback);
    }
  }
}