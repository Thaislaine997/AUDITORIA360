import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface MousePattern {
  x: number;
  y: number;
  timestamp: number;
  velocity: number;
}

interface TypingPattern {
  keystroke: string;
  timestamp: number;
  interval: number;
}

interface UserIntention {
  id: string;
  type: 'navigation' | 'action' | 'data_view' | 'form_submission';
  target: string;
  confidence: number;
  timestamp: number;
  context: Record<string, any>;
}

interface CognitiveLoad {
  level: 'low' | 'medium' | 'high';
  indicators: {
    mouseHesitation: number;
    errorFrequency: number;
    navigationPatterns: number;
    typingStress: number;
  };
  adaptationRequired: boolean;
}

interface IntentionState {
  // User interaction patterns
  mousePatterns: MousePattern[];
  typingPatterns: TypingPattern[];
  hoverDuration: Record<string, number>;
  
  // Detected intentions
  currentIntentions: UserIntention[];
  intentionHistory: UserIntention[];
  
  // Cognitive load monitoring
  cognitiveLoad: CognitiveLoad;
  errorCount: Record<string, number>;
  
  // Predictive state
  preloadedData: Record<string, any>;
  speculativeRendering: Record<string, boolean>;
  
  // Actions
  recordMouseMovement: (x: number, y: number) => void;
  recordHover: (elementId: string, duration: number) => void;
  recordKeypress: (key: string) => void;
  recordError: (formId: string, errorType: string) => void;
  detectIntention: (type: string, target: string, context?: any) => void;
  updateCognitiveLoad: () => void;
  requestPreload: (dataType: string, params: any) => void;
  shouldShowEmpathicHelp: (formId: string) => boolean;
  shouldAdaptUI: () => boolean;
  getNavigationPredictions: () => Record<string, number>;
  reset: () => void;

  // API
  sendIntentionToAPI: (intention: UserIntention) => Promise<void>;
}

export const useIntentionStore = create<IntentionState>()(
  devtools(
    (set, get) => ({
      // Initial state
      mousePatterns: [],
      typingPatterns: [],
      hoverDuration: {},
      currentIntentions: [],
      intentionHistory: [],
      cognitiveLoad: {
        level: 'low',
        indicators: {
          mouseHesitation: 0,
          errorFrequency: 0,
          navigationPatterns: 0,
          typingStress: 0,
        },
        adaptationRequired: false,
      },
      errorCount: {},
      preloadedData: {},
      speculativeRendering: {},

      // Record mouse movement patterns for neural signal detection
      recordMouseMovement: (x: number, y: number) => {
        const now = Date.now();
        const patterns = get().mousePatterns;
        const lastPattern = patterns[patterns.length - 1];
        
        let velocity = 0;
        if (lastPattern) {
          const deltaTime = now - lastPattern.timestamp;
          const deltaDistance = Math.sqrt(
            Math.pow(x - lastPattern.x, 2) + Math.pow(y - lastPattern.y, 2)
          );
          velocity = deltaDistance / (deltaTime || 1);
        }

        const newPattern: MousePattern = { x, y, timestamp: now, velocity };
        
        set((state) => ({
          mousePatterns: [...state.mousePatterns.slice(-50), newPattern], // Keep last 50 movements
        }));

        // Analyze for hesitation patterns
        if (velocity < 10 && patterns.length > 5) {
          const recentLowVelocity = patterns.slice(-5).filter(p => p.velocity < 15).length;
          if (recentLowVelocity >= 4) {
            get().updateCognitiveLoad();
          }
        }
      },

      // Record hover duration for intention detection
      recordHover: (elementId: string, duration: number) => {
        set((state) => ({
          hoverDuration: {
            ...state.hoverDuration,
            [elementId]: duration,
          },
        }));

        // Detect hover intention (500ms threshold as per requirements)
        if (duration > 500) {
          get().detectIntention('action', elementId, { hoverDuration: duration });
          
          // Pre-load data for potential actions
          if (elementId.includes('payroll') || elementId.includes('folha')) {
            get().requestPreload('payroll_data', { elementId });
          } else if (elementId.includes('client') || elementId.includes('cliente')) {
            get().requestPreload('client_data', { elementId });
          }
        }
      },

      // Record typing patterns for stress detection
      recordKeypress: (key: string) => {
        const now = Date.now();
        const patterns = get().typingPatterns;
        const lastPattern = patterns[patterns.length - 1];
        
        const interval = lastPattern ? now - lastPattern.timestamp : 0;
        
        const newPattern: TypingPattern = {
          keystroke: key,
          timestamp: now,
          interval,
        };

        set((state) => ({
          typingPatterns: [...state.typingPatterns.slice(-20), newPattern], // Keep last 20 keystrokes
        }));

        // Analyze typing stress (very fast or very slow typing)
        if (patterns.length >= 5) {
          const recentIntervals = patterns.slice(-5).map(p => p.interval).filter(i => i > 0);
          const avgInterval = recentIntervals.reduce((a, b) => a + b, 0) / recentIntervals.length;
          
          if (avgInterval < 50 || avgInterval > 1000) {
            get().updateCognitiveLoad();
          }
        }
      },

      // Record errors for empathetic response system
      recordError: (formId: string, errorType: string) => {
        set((state) => ({
          errorCount: {
            ...state.errorCount,
            [formId]: (state.errorCount[formId] || 0) + 1,
          },
        }));
        
        get().updateCognitiveLoad();
      },

      // Detect and record user intentions
      detectIntention: (type: string, target: string, context = {}) => {
        const now = Date.now();
        const patterns = get().mousePatterns;
        const hoverData = get().hoverDuration;
        
        // Calculate confidence based on interaction patterns
        let confidence = 0.5; // Base confidence
        
        // Increase confidence based on hover duration
        if (hoverData[target] > 500) confidence += 0.3;
        if (hoverData[target] > 1000) confidence += 0.2;
        
        // Increase confidence based on mouse stability
        const recentPatterns = patterns.slice(-10);
        const velocityVariance = recentPatterns.reduce((acc, p) => acc + p.velocity, 0) / recentPatterns.length;
        if (velocityVariance < 20) confidence += 0.2;

        const intention: UserIntention = {
          id: `${type}_${target}_${now}`,
          type: type as any,
          target,
          confidence: Math.min(confidence, 1),
          timestamp: now,
          context,
        };

        set((state) => ({
          currentIntentions: [...state.currentIntentions.slice(-5), intention],
          intentionHistory: [...state.intentionHistory.slice(-50), intention],
        }));

        // Send intention to API for predictive processing
        if (confidence > 0.7) {
          get().sendIntentionToAPI(intention);
        }
      },

      // Update cognitive load based on interaction patterns
      updateCognitiveLoad: () => {
        const state = get();
        const { mousePatterns, errorCount, typingPatterns } = state;
        
        // Calculate indicators
        const recentMouse = mousePatterns.slice(-20);
        const mouseHesitation = recentMouse.filter(p => p.velocity < 10).length / recentMouse.length;
        
        const totalErrors = Object.values(errorCount).reduce((a, b) => a + b, 0);
        const errorFrequency = totalErrors / Math.max(Object.keys(errorCount).length, 1);
        
        const recentTyping = typingPatterns.slice(-10);
        const typingStress = recentTyping.filter(p => p.interval < 100 || p.interval > 800).length / recentTyping.length;
        
        const indicators = {
          mouseHesitation,
          errorFrequency,
          navigationPatterns: 0, // Simplified for now
          typingStress,
        };
        
        // Calculate overall load level
        const loadScore = (mouseHesitation + errorFrequency + typingStress) / 3;
        let level: 'low' | 'medium' | 'high' = 'low';
        
        if (loadScore > 0.7) level = 'high';
        else if (loadScore > 0.4) level = 'medium';
        
        const adaptationRequired = level === 'high' || errorFrequency > 2;
        
        set({
          cognitiveLoad: {
            level,
            indicators,
            adaptationRequired,
          },
        });
      },

      // Request data pre-loading
      requestPreload: (dataType: string, params: any) => {
        // In a real implementation, this would call the API
        console.log(`🧠 Neuro-Symbolic: Pre-loading ${dataType}`, params);
        
        // Simulate API call for pre-loading
        setTimeout(() => {
          set((state) => ({
            preloadedData: {
              ...state.preloadedData,
              [dataType]: {
                ...params,
                data: `Pre-loaded data for ${dataType}`,
                timestamp: Date.now(),
              },
            },
          }));
        }, 100);
      },

      // Check if empathetic help should be shown
      shouldShowEmpathicHelp: (formId: string) => {
        const errorCount = get().errorCount[formId] || 0;
        return errorCount >= 3; // Show help after 3 errors as per requirements
      },

      // Check if UI should be adapted for cognitive load
      shouldAdaptUI: () => {
        return get().cognitiveLoad.adaptationRequired;
      },

      // Get navigation predictions based on user patterns
      getNavigationPredictions: () => {
        const { intentionHistory, currentIntentions } = get();
        const predictions: Record<string, number> = {};
        
        // Analyze intention patterns to predict next navigation
        const recentTargets = intentionHistory.slice(-10).map(i => i.target);
        const targetCounts = recentTargets.reduce((acc, target) => {
          acc[target] = (acc[target] || 0) + 1;
          return acc;
        }, {} as Record<string, number>);
        
        // Convert to probabilities
        const total = recentTargets.length;
        Object.keys(targetCounts).forEach(target => {
          predictions[target] = targetCounts[target] / total;
        });
        
        return predictions;
      },

      // Send intention to API for predictive processing
      sendIntentionToAPI: async (intention: UserIntention) => {
        try {
          // This would be the actual API call in a real implementation
          await fetch('/api/intentions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(intention),
          });
        } catch (error) {
          console.warn('Failed to send intention to API:', error);
        }
      },

      // Reset the intention state
      reset: () => {
        set({
          mousePatterns: [],
          typingPatterns: [],
          hoverDuration: {},
          currentIntentions: [],
          errorCount: {},
          preloadedData: {},
          speculativeRendering: {},
          cognitiveLoad: {
            level: 'low',
            indicators: {
              mouseHesitation: 0,
              errorFrequency: 0,
              navigationPatterns: 0,
              typingStress: 0,
            },
            adaptationRequired: false,
          },
        });
      },
    }),
    {
      name: 'intention-store',
    }
  )
);