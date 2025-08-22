import React from 'react';
import { motion } from 'framer-motion';

interface ModernButtonProps {
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  className?: string;
  onClick?: () => void;
}

const ModernButton: React.FC<ModernButtonProps> = ({
  children,
  type = 'button',
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  className = '',
  onClick
}) => {
  const baseClasses = `
    relative
    font-semibold
    rounded-xl
    transition-all
    duration-300
    focus:outline-none
    focus:ring-4
    focus:ring-offset-2
    active:transform
    active:scale-[0.98]
    disabled:cursor-not-allowed
    overflow-hidden
  `;

  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };

  const variantClasses = {
    primary: `
      bg-gradient-to-r from-blue-600 to-blue-700
      hover:from-blue-700 hover:to-blue-800
      text-white
      shadow-lg hover:shadow-xl
      focus:ring-blue-300
      disabled:from-gray-400 disabled:to-gray-500
      disabled:shadow-none
    `,
    secondary: `
      bg-white/90
      backdrop-blur-sm
      border border-gray-200
      hover:bg-white
      hover:border-gray-300
      text-gray-700
      shadow-md hover:shadow-lg
      focus:ring-gray-300
      disabled:bg-gray-100
      disabled:text-gray-400
      disabled:border-gray-200
    `,
    ghost: `
      bg-transparent
      hover:bg-white/10
      text-white
      border border-white/20
      hover:border-white/30
      focus:ring-white/20
      disabled:text-white/50
      disabled:border-white/10
    `
  };

  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        ${baseClasses}
        ${sizeClasses[size]}
        ${variantClasses[variant]}
        ${className}
      `}
      whileHover={disabled || loading ? {} : {
        scale: 1.02,
        y: -1
      }}
      whileTap={disabled || loading ? {} : {
        scale: 0.98
      }}
      initial={false}
    >
      {/* Background shimmer effect */}
      {variant === 'primary' && !disabled && (
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
          initial={{ x: '-100%' }}
          animate={{ x: '100%' }}
          transition={{
            duration: 2,
            repeat: Infinity,
            repeatDelay: 1,
            ease: "easeInOut"
          }}
          style={{ width: '50%' }}
        />
      )}

      {/* Content */}
      <span className={`relative z-10 flex items-center justify-center gap-2 ${loading ? 'opacity-70' : ''}`}>
        {loading && (
          <motion.div
            className="w-4 h-4 border-2 border-current border-t-transparent rounded-full"
            animate={{ rotate: 360 }}
            transition={{
              duration: 1,
              repeat: Infinity,
              ease: "linear"
            }}
          />
        )}
        {children}
      </span>
    </motion.button>
  );
};

export default ModernButton;