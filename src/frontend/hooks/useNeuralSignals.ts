import { useEffect, useRef, useCallback } from 'react';
import { useIntentionStore } from '../stores/intentionStore';

/**
 * Hook for tracking neural signals through mouse movements and interactions
 */
export const useNeuralSignalTracking = () => {
  const {
    recordMouseMovement,
    recordHover,
    recordKeypress,
    detectIntention,
    updateCognitiveLoad,
  } = useIntentionStore();

  const hoverTimeouts = useRef<Record<string, NodeJS.Timeout>>({});
  const hoverStartTimes = useRef<Record<string, number>>({});

  // Track mouse movements for neural pattern detection
  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      recordMouseMovement(event.clientX, event.clientY);
    };

    document.addEventListener('mousemove', handleMouseMove, { passive: true });
    
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
    };
  }, [recordMouseMovement]);

  // Track keystrokes for typing pattern analysis
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      recordKeypress(event.key);
      
      // Detect form submission intentions
      if (event.key === 'Enter') {
        const target = event.target as HTMLElement;
        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
          detectIntention('form_submission', target.id || target.name || 'unknown_field');
        }
      }
    };

    document.addEventListener('keydown', handleKeyPress, { passive: true });
    
    return () => {
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, [recordKeypress, detectIntention]);

  // Create hover tracking function for specific elements
  const trackHover = useCallback((elementId: string, element: HTMLElement) => {
    const handleMouseEnter = () => {
      hoverStartTimes.current[elementId] = Date.now();
      
      // Set timeout to detect prolonged hover (intention signal)
      hoverTimeouts.current[elementId] = setTimeout(() => {
        const duration = Date.now() - hoverStartTimes.current[elementId];
        recordHover(elementId, duration);
        
        // Special handling for payroll buttons (as per requirements)
        if (elementId.includes('payroll') || elementId.includes('folha')) {
          detectIntention('data_view', elementId, { 
            type: 'payroll_preview',
            hoverDuration: duration 
          });
        }
      }, 500); // 500ms threshold as specified
    };

    const handleMouseLeave = () => {
      if (hoverTimeouts.current[elementId]) {
        clearTimeout(hoverTimeouts.current[elementId]);
      }
      
      const startTime = hoverStartTimes.current[elementId];
      if (startTime) {
        const duration = Date.now() - startTime;
        recordHover(elementId, duration);
      }
    };

    element.addEventListener('mouseenter', handleMouseEnter);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mouseenter', handleMouseEnter);
      element.removeEventListener('mouseleave', handleMouseLeave);
      if (hoverTimeouts.current[elementId]) {
        clearTimeout(hoverTimeouts.current[elementId]);
      }
    };
  }, [recordHover, detectIntention]);

  return {
    trackHover,
    updateCognitiveLoad,
  };
};

/**
 * Hook for elements that should trigger intention detection on hover
 */
export const useIntentionTrigger = (elementId: string, intentionType: 'navigation' | 'action' | 'data_view' = 'action') => {
  const elementRef = useRef<HTMLElement>(null);
  const { trackHover } = useNeuralSignalTracking();

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    return trackHover(elementId, element);
  }, [elementId, trackHover]);

  return elementRef;
};

/**
 * Hook for form error tracking and empathetic response
 */
export const useEmpathicForm = (formId: string) => {
  const { recordError, shouldShowEmpathicHelp } = useIntentionStore();

  const recordFormError = useCallback((errorType: string) => {
    recordError(formId, errorType);
  }, [formId, recordError]);

  const needsEmpathicHelp = shouldShowEmpathicHelp(formId);

  return {
    recordFormError,
    needsEmpathicHelp,
  };
};

/**
 * Hook for adaptive UI based on cognitive load
 */
export const useAdaptiveUI = () => {
  const { shouldAdaptUI, cognitiveLoad } = useIntentionStore();

  const shouldSimplify = shouldAdaptUI();
  const loadLevel = cognitiveLoad.level;

  // UI adaptation strategies based on cognitive load
  const getAdaptationStrategy = () => {
    if (loadLevel === 'high') {
      return {
        hideAdvancedFeatures: true,
        highlightPrimaryActions: true,
        showHelpHints: true,
        reduceAnimations: true,
      };
    } else if (loadLevel === 'medium') {
      return {
        hideAdvancedFeatures: false,
        highlightPrimaryActions: true,
        showHelpHints: false,
        reduceAnimations: false,
      };
    }
    
    return {
      hideAdvancedFeatures: false,
      highlightPrimaryActions: false,
      showHelpHints: false,
      reduceAnimations: false,
    };
  };

  return {
    shouldSimplify,
    loadLevel,
    adaptationStrategy: getAdaptationStrategy(),
    cognitiveLoad,
  };
};

/**
 * Hook for predictive data pre-loading
 */
export const usePredictiveLoading = () => {
  const { preloadedData, getNavigationPredictions, requestPreload } = useIntentionStore();

  const predictions = getNavigationPredictions();
  
  // Pre-load data for high-probability navigation targets
  const preloadHighProbabilityTargets = useCallback(() => {
    Object.entries(predictions).forEach(([target, probability]) => {
      if (probability > 0.9) { // 90% threshold as per requirements
        if (target.includes('client') || target.includes('cliente')) {
          requestPreload('client_data', { target });
        } else if (target.includes('dashboard')) {
          requestPreload('dashboard_metrics', { target });
        } else if (target.includes('payroll') || target.includes('folha')) {
          requestPreload('payroll_data', { target });
        }
      }
    });
  }, [predictions, requestPreload]);

  // Check if data is already pre-loaded
  const isDataPreloaded = useCallback((dataType: string) => {
    return preloadedData[dataType] && 
           (Date.now() - preloadedData[dataType].timestamp) < 30000; // Valid for 30 seconds
  }, [preloadedData]);

  return {
    predictions,
    preloadedData,
    preloadHighProbabilityTargets,
    isDataPreloaded,
  };
};