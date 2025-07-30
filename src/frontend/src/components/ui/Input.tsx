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
          '&:hover fieldset': {
            borderColor: 'primary.main',
          },
        },
        '& .MuiInputLabel-root': {
          fontWeight: 500,
        },
        ...props.sx,
      }}
    />
  );
};

export default Input;