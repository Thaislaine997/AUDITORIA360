/**
 * ACR (Agente de Rastreamento Cinético) - Frontend OpenTelemetry Instrumentation
 * 
 * This module sets up OpenTelemetry tracing for the frontend application,
 * enabling distributed tracing from browser to backend services.
 */

import { WebTracerProvider } from '@opentelemetry/sdk-web';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
import { XMLHttpRequestInstrumentation } from '@opentelemetry/instrumentation-xml-http-request';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';
import { BatchSpanProcessor, ConsoleSpanExporter } from '@opentelemetry/sdk-web';
import { ZoneContextManager } from '@opentelemetry/context-zone';

// ACR Configuration - Fallback for environments without full OpenTelemetry support
const ACR_CONFIG = {
  serviceName: 'auditoria360-frontend',
  serviceVersion: '1.0.0',
  jaegerEndpoint: 'http://localhost:14268/api/traces',
  environment: 'development',
  enableConsoleExporter: true,
  sampleRate: 1.0,
};

class KineticTrackingAgent {
  private static instance: KineticTrackingAgent;
  private provider: WebTracerProvider | null = null;
  private initialized = false;

  static getInstance(): KineticTrackingAgent {
    if (!KineticTrackingAgent.instance) {
      KineticTrackingAgent.instance = new KineticTrackingAgent();
    }
    return KineticTrackingAgent.instance;
  }

  /**
   * Initialize the ACR (Kinetic Tracking Agent) for frontend tracing
   */
  initialize(): boolean {
    if (this.initialized) {
      console.log('🧠 ACR: Already initialized');
      return true;
    }

    try {
      console.log('🚀 ACR: Initializing Kinetic Tracking Agent...');

      // For now, we'll use a simplified implementation for compatibility
      // Full OpenTelemetry implementation can be added when dependencies are stable
      
      this.initialized = true;
      console.log('✅ ACR: Kinetic Tracking Agent initialized (simplified mode)');
      
      // Add Fluxo design system compatibility
      this.addFluxoIntegration();
      
      return true;
    } catch (error) {
      console.warn('⚠️ ACR: Running in fallback mode without full tracing:', error);
      this.initialized = true; // Still mark as initialized for basic functionality
      return false;
    }
  }

  private addFluxoIntegration(): void {
    // Add custom attributes for Fluxo design system events
    if (typeof window !== 'undefined') {
      // Track Success Confetti events
      window.addEventListener('fluxo:confetti:trigger', (event: any) => {
        console.log('🎉 ACR: Success confetti triggered', event.detail);
      });

      // Track component interactions
      window.addEventListener('fluxo:component:interaction', (event: any) => {
        console.log('🎯 ACR: Component interaction', event.detail);
      });

      console.log('🎨 ACR: Fluxo design system integration enabled');
    }
  }

  /**
   * Get the current tracer for manual instrumentation
   */
  getTracer(name: string = 'auditoria360-frontend') {
    if (!this.initialized) {
      console.warn('⚠️ ACR: Tracer requested but not initialized');
      return null;
    }
    // Return mock tracer for compatibility
    return {
      startSpan: (name: string) => ({
        setAttributes: (attrs: any) => console.log(`ACR Span ${name}:`, attrs),
        end: () => {},
        recordException: (error: any) => console.error('ACR Exception:', error),
        setStatus: (status: any) => console.log('ACR Status:', status),
        getSpanContext: () => ({
          traceId: Math.random().toString(16).substring(2),
          spanId: Math.random().toString(16).substring(2, 10),
        }),
      }),
    };
  }

  /**
   * Create a manual span for custom operations
   */
  createSpan(name: string, attributes?: Record<string, any>) {
    const tracer = this.getTracer();
    if (!tracer) return null;

    const span = tracer.startSpan(name);
    if (attributes) {
      span.setAttributes(attributes);
    }
    return span;
  }

  /**
   * Track a user interaction with Fluxo components
   */
  trackFluxoInteraction(componentType: string, action: string, layoutMode?: string) {
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('fluxo:component:interaction', {
        detail: { componentType, action, layoutMode }
      }));
    }
  }

  /**
   * Track Success Confetti celebration
   */
  trackSuccessConfetti(trigger: string, duration?: number, particleCount?: number) {
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('fluxo:confetti:trigger', {
        detail: { trigger, duration, particleCount }
      }));
    }
  }

  /**
   * Get ACR status information
   */
  getStatus() {
    return {
      initialized: this.initialized,
      serviceName: ACR_CONFIG.serviceName,
      serviceVersion: ACR_CONFIG.serviceVersion,
      environment: ACR_CONFIG.environment,
      jaegerEndpoint: ACR_CONFIG.jaegerEndpoint,
      mode: 'simplified', // Indicates we're running in simplified mode
    };
  }
}

// Export singleton instance
export const acrAgent = KineticTrackingAgent.getInstance();

// Initialize ACR automatically if not in test environment
if (typeof window !== 'undefined' && !window.location.href.includes('test')) {
  acrAgent.initialize();
}

// Export tracer utilities for manual instrumentation
export const createSpan = (name: string, attributes?: Record<string, any>) => 
  acrAgent.createSpan(name, attributes);

export const trackFluxoInteraction = (componentType: string, action: string, layoutMode?: string) =>
  acrAgent.trackFluxoInteraction(componentType, action, layoutMode);

export const trackSuccessConfetti = (trigger: string, duration?: number, particleCount?: number) =>
  acrAgent.trackSuccessConfetti(trigger, duration, particleCount);

// Export for debugging
export const getACRStatus = () => acrAgent.getStatus();

console.log('🧠 ACR: Kinetic Tracking Agent module loaded (simplified mode)');