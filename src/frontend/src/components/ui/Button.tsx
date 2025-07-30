import React from 'react';
import { Button as MuiButton, ButtonProps as MuiButtonProps } from '@mui/material';

interface ButtonProps extends MuiButtonProps {
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  loading = false, 
  disabled,
  children,
  ...props 
}) => {
  return (
    <MuiButton
      disabled={disabled || loading}
      {...props}
      sx={{
        textTransform: 'none',
        fontWeight: 500,
        borderRadius: 2,
        ...props.sx,
      }}
    >
      {loading ? 'Carregando...' : children}
    </MuiButton>
  );
};

export default Button;