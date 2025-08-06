import React, { useState, useEffect } from 'react';
import {
  TextField,
  TextFieldProps,
  Box,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  Chip,
} from '@mui/material';
import {
  Psychology,
  Help,
  Lightbulb,
  ErrorOutline,
} from '@mui/icons-material';
import { useEmpathicForm } from '../../hooks/useNeuralSignals';
import { EmpathicHelpDialog } from '../../pages/ChatbotPage';

interface EmpathicTextFieldProps extends Omit<TextFieldProps, 'error' | 'helperText'> {
  formId: string;
  fieldName: string;
  validationRules?: {
    required?: boolean;
    pattern?: RegExp;
    minLength?: number;
    maxLength?: number;
    custom?: (value: string) => boolean;
  };
  empathicHelp?: {
    errorType: string;
    helpMessage?: string;
    example?: string;
  };
}

export const EmpathicTextField: React.FC<EmpathicTextFieldProps> = ({
  formId,
  fieldName,
  validationRules = {},
  empathicHelp,
  value,
  onChange,
  onBlur,
  ...textFieldProps
}) => {
  const [localValue, setLocalValue] = useState(value || '');
  const [errorState, setErrorState] = useState<string | null>(null);
  const [errorCount, setErrorCount] = useState(0);
  const [showEmpathicDialog, setShowEmpathicDialog] = useState(false);
  const [hasUserInteracted, setHasUserInteracted] = useState(false);
  
  const { recordFormError, needsEmpathicHelp } = useEmpathicForm(formId);

  // Validate field value
  const validateField = (val: string): string | null => {
    const { required, pattern, minLength, maxLength, custom } = validationRules;
    
    if (required && !val.trim()) {
      return 'Este campo é obrigatório';
    }
    
    if (pattern && val && !pattern.test(val)) {
      return 'Formato inválido';
    }
    
    if (minLength && val.length < minLength) {
      return `Mínimo ${minLength} caracteres`;
    }
    
    if (maxLength && val.length > maxLength) {
      return `Máximo ${maxLength} caracteres`;
    }
    
    if (custom && val && !custom(val)) {
      return 'Valor inválido';
    }
    
    return null;
  };

  // Handle value changes
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = event.target.value;
    setLocalValue(newValue);
    setHasUserInteracted(true);
    
    // Clear error when user starts typing again
    if (errorState) {
      setErrorState(null);
    }
    
    if (onChange) {
      onChange(event);
    }
  };

  // Handle blur (when user leaves the field)
  const handleBlur = (event: React.FocusEvent<HTMLInputElement>) => {
    const validationError = validateField(localValue);
    
    if (validationError && hasUserInteracted) {
      setErrorState(validationError);
      setErrorCount(prev => prev + 1);
      
      // Record error for neural interface
      recordFormError(empathicHelp?.errorType || 'validation_error');
      
      // Show empathic help after 3 errors (as per requirements)
      if (errorCount >= 2) { // Will be 3 after increment
        setShowEmpathicDialog(true);
      }
    }
    
    if (onBlur) {
      onBlur(event);
    }
  };

  // Auto-format common field types
  const autoFormat = (val: string, type: string): string => {
    switch (type) {
      case 'phone':
        // Format phone number: (11) 99999-9999
        return val.replace(/\D/g, '')
          .replace(/(\d{2})(\d)/, '($1) $2')
          .replace(/(\d{4,5})(\d{4})/, '$1-$2')
          .slice(0, 15);
      
      case 'cnpj':
        // Format CNPJ: 11.222.333/0001-44
        return val.replace(/\D/g, '')
          .replace(/(\d{2})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1/$2')
          .replace(/(\d{4})(\d)/, '$1-$2')
          .slice(0, 18);
      
      case 'cpf':
        // Format CPF: 123.456.789-00
        return val.replace(/\D/g, '')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1-$2')
          .slice(0, 14);
          
      default:
        return val;
    }
  };

  // Handle auto-formatting on change
  useEffect(() => {
    if (empathicHelp?.errorType && localValue) {
      const formatted = autoFormat(localValue, empathicHelp.errorType);
      if (formatted !== localValue) {
        setLocalValue(formatted);
      }
    }
  }, [localValue, empathicHelp?.errorType]);

  return (
    <Box>
      <TextField
        {...textFieldProps}
        value={localValue}
        onChange={handleChange}
        onBlur={handleBlur}
        error={!!errorState}
        helperText={
          errorState ? (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <ErrorOutline sx={{ fontSize: 16 }} />
              {errorState}
              {errorCount >= 2 && (
                <Chip 
                  label="Ajuda disponível" 
                  size="small" 
                  color="warning" 
                  icon={<Psychology />}
                  onClick={() => setShowEmpathicDialog(true)}
                />
              )}
            </Box>
          ) : textFieldProps.helperText
        }
        InputProps={{
          ...textFieldProps.InputProps,
          endAdornment: (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              {textFieldProps.InputProps?.endAdornment}
              {errorCount >= 2 && (
                <Psychology 
                  color="warning" 
                  sx={{ 
                    cursor: 'pointer',
                    animation: 'pulse 2s infinite',
                    '@keyframes pulse': {
                      '0%': { opacity: 1 },
                      '50%': { opacity: 0.5 },
                      '100%': { opacity: 1 },
                    },
                  }}
                  onClick={() => setShowEmpathicDialog(true)}
                />
              )}
            </Box>
          ),
        }}
      />

      {/* Empathic Help Dialog */}
      <EmpathicHelpDialog
        open={showEmpathicDialog}
        onClose={() => setShowEmpathicDialog(false)}
        errorContext={{
          formId,
          errorType: empathicHelp?.errorType || 'validation_error',
          errorCount: errorCount,
        }}
      />

      {/* Adaptive hint for high error count */}
      {errorCount >= 1 && errorCount < 3 && (
        <Alert 
          severity="info" 
          sx={{ mt: 1 }}
          icon={<Lightbulb />}
        >
          💡 Dica: {getContextualHint(empathicHelp?.errorType)}
        </Alert>
      )}
    </Box>
  );
};

// Get contextual hints based on field type
const getContextualHint = (errorType?: string): string => {
  switch (errorType) {
    case 'email':
      return 'Digite um email válido como: usuario@empresa.com.br';
    case 'phone':
      return 'Use o formato: (11) 99999-9999';
    case 'cnpj':
      return 'Digite apenas números, formatação automática: 11222333000144';
    case 'cpf':
      return 'Digite apenas números: 12345678900';
    case 'date':
      return 'Use o formato: DD/MM/AAAA';
    default:
      return 'Verifique se as informações estão corretas';
  }
};

export default EmpathicTextField;