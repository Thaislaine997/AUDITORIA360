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
        transition: 'all var(--transition-fast)',
        position: 'relative',
        // Fluxo "Responsive Click" Physics
        '&:active': {
          transform: 'translateY(var(--fluxo-click-displacement))',
          filter: 'brightness(0.95)',
        },
        '&:hover:not(:disabled)': {
          transform: 'translateY(-1px)',
          boxShadow: 'var(--fluxo-shadow-floating)',
        },
        // Electric Blue focus ring for accessibility
        '&:focus-visible': {
          outline: '2px solid var(--fluxo-electric-blue)',
          outlineOffset: '2px',
        },
        ...props.sx,
      }}
    >
      {loading ? 'Carregando...' : children}
    </MuiButton>
  );
};

export default Button;