import React from 'react';
import { Card as MuiCard, CardContent, CardProps as MuiCardProps } from '@mui/material';

interface CardProps extends MuiCardProps {
  padding?: 'none' | 'small' | 'medium' | 'large';
}

export const Card: React.FC<CardProps> = ({ 
  padding = 'medium',
  children,
  ...props 
}) => {
  const getPadding = () => {
    switch (padding) {
      case 'none':
        return 0;
      case 'small':
        return 1;
      case 'medium':
        return 2;
      case 'large':
        return 3;
      default:
        return 2;
    }
  };

  return (
    <MuiCard
      {...props}
      sx={{
        borderRadius: 2,
        border: '1px solid var(--border-color)',
        // Fluxo "Floating Shadow" Physics
        boxShadow: 'var(--fluxo-shadow-subtle)',
        transition: 'all var(--transition-normal)',
        '&:hover': {
          boxShadow: 'var(--fluxo-shadow-floating-hover)',
          transform: 'translateY(-2px)',
          borderColor: 'var(--border-hover-color)',
        },
        // Accessibility: ensure focus is visible
        '&:focus-within': {
          outline: '2px solid var(--fluxo-electric-blue)',
          outlineOffset: '2px',
        },
        ...props.sx,
      }}
    >
      <CardContent
        sx={{
          p: getPadding(),
          '&:last-child': {
            pb: getPadding(),
          },
        }}
      >
        {children}
      </CardContent>
    </MuiCard>
  );
};

export default Card;