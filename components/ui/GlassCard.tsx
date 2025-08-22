import React from 'react';
import { motion } from 'framer-motion';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  blur?: 'sm' | 'md' | 'lg' | 'xl';
  opacity?: number;
  border?: boolean;
  shadow?: 'sm' | 'md' | 'lg' | 'xl';
  hover?: boolean;
}

const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className = '',
  blur = 'lg',
  opacity = 0.9,
  border = true,
  shadow = 'xl',
  hover = true
}) => {
  const blurClasses = {
    sm: 'backdrop-blur-sm',
    md: 'backdrop-blur-md',
    lg: 'backdrop-blur-lg',
    xl: 'backdrop-blur-xl'
  };

  const shadowClasses = {
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
    xl: 'shadow-2xl'
  };

  const baseClasses = `
    ${blurClasses[blur]}
    ${shadowClasses[shadow]}
    ${border ? 'border border-white/20' : ''}
    rounded-2xl
    transition-all
    duration-300
    ease-out
  `;

  const backgroundStyle = {
    background: `rgba(255, 255, 255, ${opacity})`,
  };

  if (hover) {
    return (
      <motion.div
        className={`${baseClasses} ${className}`}
        style={backgroundStyle}
        whileHover={{
          scale: 1.02,
          y: -4,
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        }}
        whileTap={{
          scale: 0.98,
        }}
        initial={{
          opacity: 0,
          y: 20,
        }}
        animate={{
          opacity: 1,
          y: 0,
        }}
        transition={{
          duration: 0.6,
          ease: "easeOut"
        }}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <motion.div
      className={`${baseClasses} ${className}`}
      style={backgroundStyle}
      initial={{
        opacity: 0,
        y: 20,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      transition={{
        duration: 0.6,
        ease: "easeOut"
      }}
    >
      {children}
    </motion.div>
  );
};

export default GlassCard;