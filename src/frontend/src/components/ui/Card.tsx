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
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
        border: '1px solid rgba(0, 0, 0, 0.05)',
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