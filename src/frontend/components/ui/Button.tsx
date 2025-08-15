import React from 'react';
import { Button as MuiButton, ButtonProps as MuiButtonProps } from '@mui/material';
import { trackFluxoInteraction } from '../../services/acr';

interface ButtonProps extends MuiButtonProps {
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  loading = false, 
  disabled,
  children,
  onClick,
  ...props 
}) => {
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    // ACR (Kinetic Tracking Agent) - Track button interactions
    trackFluxoInteraction('button', 'click');
    
    // Call original onClick handler
    if (onClick && !disabled && !loading) {
      onClick(event);
    }
  };

  return (
    <MuiButton
      disabled={disabled || loading}
      onClick={handleClick}
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