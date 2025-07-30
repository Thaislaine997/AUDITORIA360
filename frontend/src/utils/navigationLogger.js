/**
 * Navigation Logger for AUDITORIA360
 * Logs navigation errors and routing issues for debugging and monitoring
 */

class NavigationLogger {
  constructor() {
    this.sessionId = this.generateSessionId();
    this.logQueue = [];
    this.maxQueueSize = 100;
    this.isOnline = navigator.onLine;
    
    // Listen for online/offline events
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.flushQueue();
    });
    
    window.addEventListener('offline', () => {
      this.isOnline = false;
    });
    
    // Listen for page visibility changes
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible') {
        this.flushQueue();
      }
    });
  }
  
  generateSessionId() {
    return 'nav_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }
  
  /**
   * Log navigation error
   * @param {Error|string} error - The error that occurred
   * @param {string} route - The route that failed
   * @param {string} action - The action that was attempted
   * @param {Object} context - Additional context information
   */
  logNavigationError(error, route, action = 'navigate', context = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      sessionId: this.sessionId,
      level: 'error',
      type: 'navigation',
      error: {
        message: error?.message || String(error),
        stack: error?.stack || null,
        name: error?.name || 'NavigationError'
      },
      route: route,
      action: action,
      context: {
        userAgent: navigator.userAgent,
        url: window.location.href,
        referrer: document.referrer,
        timestamp: Date.now(),
        userType: this.getCurrentUserType(),
        ...context
      }
    };
    
    // Log to console for immediate debugging
    console.error('[NAVIGATION ERROR]', logEntry);
    
    // Add to queue for remote logging
    this.addToQueue(logEntry);
    
    // Store in localStorage for persistence
    this.storeLocally(logEntry);
  }
  
  /**
   * Log successful navigation for analytics
   * @param {string} route - The route that was navigated to
   * @param {string} action - The action that was performed
   * @param {Object} context - Additional context information
   */
  logNavigationSuccess(route, action = 'navigate', context = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      sessionId: this.sessionId,
      level: 'info',
      type: 'navigation',
      route: route,
      action: action,
      context: {
        userAgent: navigator.userAgent,
        url: window.location.href,
        referrer: document.referrer,
        timestamp: Date.now(),
        userType: this.getCurrentUserType(),
        loadTime: context.loadTime || null,
        ...context
      }
    };
    
    // Log to console in development
    if (this.isDevelopment()) {
      console.info('[NAVIGATION SUCCESS]', logEntry);
    }
    
    this.addToQueue(logEntry);
  }
  
  /**
   * Log route change
   * @param {string} fromRoute - Previous route
   * @param {string} toRoute - New route
   * @param {Object} context - Additional context
   */
  logRouteChange(fromRoute, toRoute, context = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      sessionId: this.sessionId,
      level: 'info',
      type: 'route_change',
      fromRoute: fromRoute,
      toRoute: toRoute,
      context: {
        userAgent: navigator.userAgent,
        timestamp: Date.now(),
        userType: this.getCurrentUserType(),
        ...context
      }
    };
    
    if (this.isDevelopment()) {
      console.info('[ROUTE CHANGE]', logEntry);
    }
    
    this.addToQueue(logEntry);
  }
  
  /**
   * Add log entry to queue
   * @param {Object} logEntry - Log entry to add
   */
  addToQueue(logEntry) {
    this.logQueue.push(logEntry);
    
    // Limit queue size
    if (this.logQueue.length > this.maxQueueSize) {
      this.logQueue = this.logQueue.slice(-this.maxQueueSize);
    }
    
    // Try to flush if online
    if (this.isOnline) {
      this.flushQueue();
    }
  }
  
  /**
   * Flush log queue to remote endpoint
   */
  async flushQueue() {
    if (this.logQueue.length === 0 || !this.isOnline) {
      return;
    }
    
    const logsToSend = [...this.logQueue];
    this.logQueue = [];
    
    try {
      // Send to monitoring endpoint if available
      if (window.AUDITORIA360_CONFIG?.monitoringEndpoint) {
        await fetch(window.AUDITORIA360_CONFIG.monitoringEndpoint + '/logs', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': this.getAuthToken()
          },
          body: JSON.stringify({ logs: logsToSend })
        });
      } else {
        // Fallback to API endpoint
        await fetch('/api/v1/monitoring/logs', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': this.getAuthToken()
          },
          body: JSON.stringify({ logs: logsToSend })
        });
      }
    } catch (error) {
      console.warn('[NavigationLogger] Failed to send logs:', error);
      // Re-add failed logs to queue
      this.logQueue = logsToSend.concat(this.logQueue);
    }
  }
  
  /**
   * Store log entry in localStorage for persistence
   * @param {Object} logEntry - Log entry to store
   */
  storeLocally(logEntry) {
    try {
      const stored = JSON.parse(localStorage.getItem('navigation_logs') || '[]');
      stored.push(logEntry);
      
      // Keep only last 50 entries
      const trimmed = stored.slice(-50);
      localStorage.setItem('navigation_logs', JSON.stringify(trimmed));
    } catch (error) {
      console.warn('[NavigationLogger] Failed to store log locally:', error);
    }
  }
  
  /**
   * Get current user type from session
   * @returns {string} Current user type
   */
  getCurrentUserType() {
    try {
      const session = JSON.parse(localStorage.getItem('auditoria360_session') || '{}');
      return session.userType || 'anonymous';
    } catch {
      return 'anonymous';
    }
  }
  
  /**
   * Get authentication token
   * @returns {string} Auth token or empty string
   */
  getAuthToken() {
    try {
      const session = JSON.parse(localStorage.getItem('auditoria360_session') || '{}');
      return session.token ? `Bearer ${session.token}` : '';
    } catch {
      return '';
    }
  }
  
  /**
   * Check if running in development mode
   * @returns {boolean} True if in development
   */
  isDevelopment() {
    return window.location.hostname === 'localhost' || 
           window.location.hostname === '127.0.0.1' ||
           window.location.hostname.includes('dev');
  }
  
  /**
   * Get stored logs from localStorage
   * @returns {Array} Array of stored log entries
   */
  getStoredLogs() {
    try {
      return JSON.parse(localStorage.getItem('navigation_logs') || '[]');
    } catch {
      return [];
    }
  }
  
  /**
   * Clear stored logs
   */
  clearStoredLogs() {
    localStorage.removeItem('navigation_logs');
  }
  
  /**
   * Get current session statistics
   * @returns {Object} Session statistics
   */
  getSessionStats() {
    const logs = this.getStoredLogs();
    const sessionLogs = logs.filter(log => log.sessionId === this.sessionId);
    
    return {
      sessionId: this.sessionId,
      totalLogs: sessionLogs.length,
      errors: sessionLogs.filter(log => log.level === 'error').length,
      routes: [...new Set(sessionLogs.map(log => log.route || log.toRoute).filter(Boolean))],
      userType: this.getCurrentUserType(),
      sessionDuration: Date.now() - (sessionLogs[0]?.context?.timestamp || Date.now())
    };
  }
}

// Create global instance
window.navigationLogger = new NavigationLogger();

// Export for ES6 modules
export default window.navigationLogger;

// Integration examples:

/**
 * Example usage in navigation functions:
 * 
 * // Log navigation error
 * try {
 *   navigateToRoute('/dashboard');
 * } catch (error) {
 *   window.navigationLogger.logNavigationError(error, '/dashboard', 'navigate', {
 *     trigger: 'user_click',
 *     element: 'sidebar_link'
 *   });
 * }
 * 
 * // Log successful navigation
 * window.navigationLogger.logNavigationSuccess('/dashboard', 'navigate', {
 *   loadTime: 250,
 *   trigger: 'user_click'
 * });
 * 
 * // Log route changes
 * window.navigationLogger.logRouteChange('/login', '/dashboard', {
 *   userType: 'super_admin',
 *   method: 'spa_routing'
 * });
 */

// Auto-detect and log page load errors
window.addEventListener('error', (event) => {
  if (event.filename && event.filename.includes('index.html')) {
    window.navigationLogger.logNavigationError(
      new Error(event.message),
      window.location.pathname,
      'page_load',
      {
        filename: event.filename,
        line: event.lineno,
        column: event.colno
      }
    );
  }
});

// Auto-detect and log unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  if (event.reason && event.reason.message && 
      (event.reason.message.includes('navigation') || 
       event.reason.message.includes('route'))) {
    window.navigationLogger.logNavigationError(
      event.reason,
      window.location.pathname,
      'promise_rejection'
    );
  }
});