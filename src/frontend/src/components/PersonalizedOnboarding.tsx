/**
 * 🔮 PersonalizedOnboarding - Componente Simbiótico
 * Onboarding que se adapta ao estado cognitivo do utilizador
 */

import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface UserCognitiveState {
  focusLevel: number;
  confidenceLevel: number;
  experienceLevel: 'beginner' | 'intermediate' | 'expert';
  learningStyle: 'visual' | 'auditory' | 'kinesthetic' | 'reading';
  currentMood: 'curious' | 'focused' | 'overwhelmed' | 'confident';
}

interface OnboardingStep {
  id: string;
  title: string;
  content: React.ReactNode;
  adaptiveContent: Record<string, React.ReactNode>;
  estimatedDuration: number;
  requiredFocusLevel: number;
}

const FLUXO_COLORS = {
  whiteBroken: '#FAFAFA',
  slateBlue: '#475569',
  electricBlue: '#3B82F6', 
  mintGreen: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444'
};

const PersonalizedOnboarding: React.FC = () => {
  const [cognitiveState, setCognitiveState] = useState<UserCognitiveState>({
    focusLevel: 0.7,
    confidenceLevel: 0.5,
    experienceLevel: 'beginner',
    learningStyle: 'visual',
    currentMood: 'curious'
  });

  const [currentStep, setCurrentStep] = useState(0);
  const [interactionPattern, setInteractionPattern] = useState<{
    mouseMovements: number;
    pauseDuration: number;
    clickHesitation: number;
  }>({
    mouseMovements: 0,
    pauseDuration: 0,
    clickHesitation: 0
  });

  const [isAdapting, setIsAdapting] = useState(false);

  // 🧠 Cognitive State Detection through interaction patterns
  const analyzeUserBehavior = useCallback((event: React.MouseEvent) => {
    setInteractionPattern(prev => ({
      ...prev,
      mouseMovements: prev.mouseMovements + 1
    }));

    // Detect hesitation patterns
    const timestamp = Date.now();
    setTimeout(() => {
      setCognitiveState(prev => {
        let newFocusLevel = prev.focusLevel;
        let newConfidence = prev.confidenceLevel;
        let newMood = prev.currentMood;

        // Analyze mouse movement patterns for cognitive load
        if (interactionPattern.mouseMovements > 20) {
          newFocusLevel = Math.max(0.3, newFocusLevel - 0.1); // Scattered attention
          newMood = 'overwhelmed';
        } else if (interactionPattern.mouseMovements < 5) {
          newFocusLevel = Math.min(1.0, newFocusLevel + 0.1); // Focused behavior
          newMood = 'focused';
        }

        return {
          ...prev,
          focusLevel: newFocusLevel,
          confidenceLevel: newConfidence,
          currentMood: newMood
        };
      });
    }, 1000);
  }, [interactionPattern.mouseMovements]);

  // 🔮 Adaptive content selection based on cognitive state
  const getAdaptiveContent = (step: OnboardingStep): React.ReactNode => {
    const { focusLevel, confidenceLevel, experienceLevel, currentMood } = cognitiveState;

    if (currentMood === 'overwhelmed' || focusLevel < 0.4) {
      return step.adaptiveContent['simplified'] || step.content;
    }

    if (experienceLevel === 'expert' && confidenceLevel > 0.8) {
      return step.adaptiveContent['advanced'] || step.content;
    }

    if (currentMood === 'curious' && focusLevel > 0.7) {
      return step.adaptiveContent['detailed'] || step.content;
    }

    return step.content;
  };

  // 📊 Onboarding steps with adaptive content
  const onboardingSteps: OnboardingStep[] = [
    {
      id: 'welcome',
      title: 'Bem-vindo à Simbiose',
      content: (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-slate-blue">
            🌟 AUDITORIA360 reconhece você
          </h2>
          <p>Esta interface adapta-se ao seu estado cognitivo em tempo real.</p>
        </div>
      ),
      adaptiveContent: {
        simplified: (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-blue">🌟 Bem-vindo</h2>
            <p>Vamos começar de forma simples.</p>
          </div>
        ),
        advanced: (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-slate-blue">
              🌟 Interface Neuro-Simbiótica Ativada
            </h2>
            <p>Sistema de análise cognitiva em tempo real detectado. Personalizando experiência...</p>
          </div>
        ),
        detailed: (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-slate-blue">
              🌟 Despertar da Simbiose Digital
            </h2>
            <p>Esta plataforma utiliza análise de padrões de interação para adaptar-se ao seu estado mental.</p>
            <div className="bg-mint-green/10 p-3 rounded-lg">
              <p className="text-sm">
                💡 <strong>Curiosidade detectada:</strong> Expandindo detalhes da interface simbiótica.
              </p>
            </div>
          </div>
        )
      },
      estimatedDuration: 30,
      requiredFocusLevel: 0.3
    },
    {
      id: 'cognitive_calibration',
      title: 'Calibração Cognitiva',
      content: (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">🧠 Analisando padrões cognitivos...</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-electric-blue/10 p-4 rounded-lg">
              <p className="font-medium">Nível de Foco</p>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-electric-blue h-2 rounded-full transition-all duration-500"
                  style={{ width: `${cognitiveState.focusLevel * 100}%` }}
                />
              </div>
              <p className="text-sm mt-1">{(cognitiveState.focusLevel * 100).toFixed(0)}%</p>
            </div>
            <div className="bg-mint-green/10 p-4 rounded-lg">
              <p className="font-medium">Estado Atual</p>
              <p className="text-sm mt-2 capitalize">{cognitiveState.currentMood}</p>
            </div>
          </div>
        </div>
      ),
      adaptiveContent: {
        simplified: (
          <div className="space-y-4">
            <h3 className="text-lg">🧠 A interface está a aprender consigo</h3>
            <p>Estado detetado: <span className="font-medium capitalize">{cognitiveState.currentMood}</span></p>
          </div>
        )
      },
      estimatedDuration: 45,
      requiredFocusLevel: 0.5
    },
    {
      id: 'interface_introduction',
      title: 'Interface Telepática',
      content: (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">🔮 Funcionalidades Simbióticas</h3>
          <div className="space-y-3">
            <div className="flex items-start space-x-3">
              <span className="text-2xl">👁️</span>
              <div>
                <p className="font-medium">Leitura de Intenção</p>
                <p className="text-sm text-gray-600">A interface detecta pausas e hesitações para oferecer ajuda proativa.</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-2xl">🎯</span>
              <div>
                <p className="font-medium">Antecipação Precognitiva</p>
                <p className="text-sm text-gray-600">Preparamos respostas antes de você solicitar.</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-2xl">🎊</span>
              <div>
                <p className="font-medium">Celebração Consciente</p>
                <p className="text-sm text-gray-600">Feedback especial em momentos de verdadeiro sucesso.</p>
              </div>
            </div>
          </div>
        </div>
      ),
      adaptiveContent: {
        simplified: (
          <div className="space-y-4">
            <h3 className="text-lg">🔮 Interface Inteligente</h3>
            <p>Esta interface vai ajudá-lo automaticamente quando precisar.</p>
          </div>
        ),
        advanced: (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">🔮 Arquitetura Neuro-Simbiótica</h3>
            <div className="bg-slate-blue/5 p-4 rounded-lg">
              <p className="text-sm">
                <strong>Implementação técnica:</strong> Análise de padrões de movimento do cursor, 
                ritmo de digitação e duração de foco para inferência de estado cognitivo.
              </p>
            </div>
          </div>
        )
      },
      estimatedDuration: 60,
      requiredFocusLevel: 0.6
    }
  ];

  // 🔄 Adaptive step progression
  const nextStep = () => {
    setIsAdapting(true);
    
    setTimeout(() => {
      setCurrentStep(prev => Math.min(prev + 1, onboardingSteps.length - 1));
      setIsAdapting(false);
      
      // Reset mouse movement tracking
      setInteractionPattern(prev => ({ ...prev, mouseMovements: 0 }));
    }, 300);
  };

  const previousStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 0));
  };

  const skipToEnd = () => {
    setCurrentStep(onboardingSteps.length - 1);
  };

  // 🎨 Adaptive styling based on cognitive state
  const getAdaptiveStyles = () => {
    const { focusLevel, currentMood } = cognitiveState;
    
    if (currentMood === 'overwhelmed') {
      return {
        backgroundColor: FLUXO_COLORS.whiteBroken,
        border: `2px solid ${FLUXO_COLORS.warning}`,
        filter: 'brightness(1.1)'
      };
    }
    
    if (focusLevel > 0.8) {
      return {
        backgroundColor: FLUXO_COLORS.whiteBroken,
        border: `2px solid ${FLUXO_COLORS.mintGreen}`,
        boxShadow: `0 0 20px ${FLUXO_COLORS.mintGreen}20`
      };
    }
    
    return {
      backgroundColor: FLUXO_COLORS.whiteBroken,
      border: `2px solid ${FLUXO_COLORS.electricBlue}20`
    };
  };

  const currentStepData = onboardingSteps[currentStep];

  return (
    <div 
      className="max-w-2xl mx-auto p-6 rounded-xl transition-all duration-500"
      style={getAdaptiveStyles()}
      onMouseMove={analyzeUserBehavior}
    >
      {/* Progress indicator */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-slate-blue">
            Passo {currentStep + 1} de {onboardingSteps.length}
          </span>
          <span className="text-sm text-gray-500">
            Estado: <span className="capitalize font-medium">{cognitiveState.currentMood}</span>
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className="bg-electric-blue h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${((currentStep + 1) / onboardingSteps.length) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Adaptive content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: isAdapting ? 0.3 : 0.5 }}
          className="mb-6"
        >
          {getAdaptiveContent(currentStepData)}
        </motion.div>
      </AnimatePresence>

      {/* Cognitive state indicator */}
      {cognitiveState.currentMood === 'overwhelmed' && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-warning/10 border border-warning/30 rounded-lg p-3 mb-4"
        >
          <p className="text-sm text-warning font-medium">
            🌸 Detectámos sobrecarga cognitiva. Simplificando interface...
          </p>
        </motion.div>
      )}

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <button
          onClick={previousStep}
          disabled={currentStep === 0}
          className="px-4 py-2 text-slate-blue border border-slate-blue/30 rounded-lg 
                     disabled:opacity-50 disabled:cursor-not-allowed
                     hover:bg-slate-blue/10 transition-colors"
        >
          ← Anterior
        </button>

        <div className="flex space-x-2">
          {cognitiveState.experienceLevel === 'expert' && (
            <button
              onClick={skipToEnd}
              className="px-3 py-2 text-sm text-gray-500 hover:text-slate-blue transition-colors"
            >
              Saltar
            </button>
          )}
        </div>

        <button
          onClick={nextStep}
          disabled={currentStep === onboardingSteps.length - 1}
          className="px-4 py-2 bg-electric-blue text-white rounded-lg
                     disabled:opacity-50 disabled:cursor-not-allowed
                     hover:bg-electric-blue/90 transition-colors"
        >
          {currentStep === onboardingSteps.length - 1 ? 'Completar' : 'Próximo'} →
        </button>
      </div>

      {/* Debug info (only in development) */}
      {process.env.NODE_ENV === 'development' && (
        <div className="mt-6 p-3 bg-gray-100 rounded text-xs">
          <p><strong>Debug - Estado Cognitivo:</strong></p>
          <p>Foco: {(cognitiveState.focusLevel * 100).toFixed(1)}%</p>
          <p>Movimentos do mouse: {interactionPattern.mouseMovements}</p>
          <p>Humor: {cognitiveState.currentMood}</p>
        </div>
      )}
    </div>
  );
};

export default PersonalizedOnboarding;