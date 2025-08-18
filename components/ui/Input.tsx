import React from 'react';
import { TextField as MuiTextField, TextFieldProps as MuiTextFieldProps } from '@mui/material';

interface InputProps extends Omit<MuiTextFieldProps, 'variant'> {
  variant?: 'outlined' | 'filled' | 'standard';
}

export const Input: React.FC<InputProps> = ({ 
  variant = 'outlined',
  ...props 
}) => {
  return (
    <MuiTextField
      variant={variant}
      {...props}
      sx={{
        '& .MuiOutlinedInput-root': {
          borderRadius: 2,
          transition: 'all var(--transition-fast)',
          // Fluxo "Electric Blue Focus Border"
          '&:hover fieldset': {
            borderColor: 'var(--fluxo-electric-blue)',
            borderWidth: '1.5px',
          },
          '&.Mui-focused fieldset': {
            borderColor: 'var(--fluxo-electric-blue)',
            borderWidth: '2px',
            boxShadow: '0 0 0 3px rgba(0, 119, 255, 0.1)',
          },
          // Error state with maintained Fluxo aesthetics  
          '&.Mui-error.Mui-focused fieldset': {
            borderColor: 'var(--danger-color)',
            boxShadow: '0 0 0 3px rgba(239, 68, 68, 0.1)',
          },
        },
        '& .MuiInputLabel-root': {
          fontWeight: 500,
          // Fluxo focus color for labels
          '&.Mui-focused': {
            color: 'var(--fluxo-electric-blue)',
          },
        },
        // Success state helper text
        '& .MuiFormHelperText-root.Mui-success': {
          color: 'var(--fluxo-mint-green)',
        },
        ...props.sx,
      }}
    />
  );
};

export default Input;