import React, { useEffect, useState } from 'react';
import { Box, keyframes } from '@mui/material';
import { trackSuccessConfetti } from '../../services/acr';

interface ConfettiPiece {
  id: string;
  left: number;
  delay: number;
  duration: number;
  color: string;
}

interface SuccessConfettiProps {
  trigger: boolean;
  duration?: number;
  particleCount?: number;
  onComplete?: () => void;
}

// Fluxo Success Confetti - Subtle and Professional
const fallAnimation = keyframes`
  0% {
    transform: translateY(-100vh) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
    opacity: 0;
  }
`;

const floatAnimation = keyframes`
  0%, 100% {
    transform: translateX(0px);
  }
  50% {
    transform: translateX(10px);
  }
`;

export const SuccessConfetti: React.FC<SuccessConfettiProps> = ({
  trigger,
  duration = 3000,
  particleCount = 20,
  onComplete,
}) => {
  const [confetti, setConfetti] = useState<ConfettiPiece[]>([]);
  const [isActive, setIsActive] = useState(false);

  // Fluxo colors for confetti
  const colors = [
    'var(--fluxo-electric-blue)',
    'var(--fluxo-mint-green)',
    '#F59E0B', // Amber
    '#8B5CF6', // Purple
    '#EF4444', // Red
  ];

  useEffect(() => {
    if (trigger && !isActive) {
      setIsActive(true);
      
      // ACR (Kinetic Tracking Agent) - Track confetti celebration
      trackSuccessConfetti('success_celebration', duration, particleCount);
      
      // Generate confetti pieces
      const pieces: ConfettiPiece[] = Array.from({ length: particleCount }, (_, i) => ({
        id: `confetti-${i}-${Date.now()}`,
        left: Math.random() * 100,
        delay: Math.random() * 1000,
        duration: 2000 + Math.random() * 1000,
        color: colors[Math.floor(Math.random() * colors.length)],
      }));

      setConfetti(pieces);

      // Clean up after animation
      const timer = setTimeout(() => {
        setConfetti([]);
        setIsActive(false);
        onComplete?.();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [trigger, isActive, duration, particleCount, onComplete]);

  if (!isActive || confetti.length === 0) {
    return null;
  }

  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: 9999,
        overflow: 'hidden',
      }}
    >
      {confetti.map((piece) => (
        <Box
          key={piece.id}
          sx={{
            position: 'absolute',
            left: `${piece.left}%`,
            top: '-10px',
            width: '8px',
            height: '8px',
            backgroundColor: piece.color,
            borderRadius: '2px',
            animation: `
              ${fallAnimation} ${piece.duration}ms linear ${piece.delay}ms,
              ${floatAnimation} 2s ease-in-out infinite
            `,
            opacity: 0.8,
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          }}
        />
      ))}
    </Box>
  );
};

// Hook for triggering success confetti
export const useSuccessConfetti = () => {
  const [trigger, setTrigger] = useState(false);

  const celebrate = () => {
    setTrigger(true);
    // Reset trigger after a brief moment
    setTimeout(() => setTrigger(false), 100);
  };

  return { trigger, celebrate };
};

export default SuccessConfetti;