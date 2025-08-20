import { useState, useCallback } from 'react';

// Hook para lógica empática de formulário
export function useEmpathicForm(formId?: string) {
  const [empathyLevel, setEmpathyLevel] = useState<'low' | 'medium' | 'high'>('medium');
  const [errorCounts, setErrorCounts] = useState<Record<string, number>>({});

  // Registra erro por tipo
  const recordFormError = useCallback((errorType: string) => {
    setErrorCounts(prev => ({
      ...prev,
      [errorType]: (prev[errorType] || 0) + 1,
    }));
  }, []);

  // Determina se precisa de ajuda empática
  const needsEmpathicHelp = useCallback((errorType: string) => {
    return (errorCounts[errorType] || 0) >= 3;
  }, [errorCounts]);

  return { empathyLevel, setEmpathyLevel, recordFormError, needsEmpathicHelp };
}

// Hook para adaptação de UI
export function useAdaptiveUI() {
  const [uiMode, setUiMode] = useState<'normal' | 'accessible'>('normal');
  const [shouldSimplify, setShouldSimplify] = useState(false);
  const [adaptationStrategy, setAdaptationStrategy] = useState({
    hideAdvancedFeatures: false,
    reduceAnimations: false,
    highlightPrimaryActions: false,
    showHelpHints: false,
  });

  // Exemplo: ativa simplificação e estratégias se modo acessível
  const updateUiMode = (mode: 'normal' | 'accessible') => {
    setUiMode(mode);
    if (mode === 'accessible') {
      setShouldSimplify(true);
      setAdaptationStrategy({
        hideAdvancedFeatures: true,
        reduceAnimations: true,
        highlightPrimaryActions: true,
        showHelpHints: true,
      });
    } else {
      setShouldSimplify(false);
      setAdaptationStrategy({
        hideAdvancedFeatures: false,
        reduceAnimations: false,
        highlightPrimaryActions: false,
        showHelpHints: false,
      });
    }
  };

  return { uiMode, setUiMode: updateUiMode, shouldSimplify, adaptationStrategy };
}
