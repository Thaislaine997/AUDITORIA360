import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Eye, EyeOff } from 'lucide-react';

interface ModernInputProps {
  id: string;
  type: 'email' | 'password' | 'text';
  label: string;
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
  error?: string;
  className?: string;
}

const ModernInput: React.FC<ModernInputProps> = ({
  id,
  type: initialType,
  label,
  placeholder,
  value,
  onChange,
  required = false,
  error,
  className = ''
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  
  const isPassword = initialType === 'password';
  const inputType = isPassword && showPassword ? 'text' : initialType;

  const hasValue = value.length > 0;
  const hasError = !!error;

  return (
    <div className={`relative ${className}`}>
      <div className="relative">
        <input
          id={id}
          type={inputType}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          required={required}
          className={`
            w-full
            px-4
            py-3.5
            bg-white/50
            backdrop-blur-sm
            border
            rounded-xl
            text-gray-900
            placeholder-transparent
            transition-all
            duration-300
            focus:outline-none
            focus:ring-2
            peer
            ${hasError 
              ? 'border-red-300 focus:border-red-500 focus:ring-red-200' 
              : isFocused || hasValue 
                ? 'border-blue-400 focus:border-blue-500 focus:ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'
            }
            ${isPassword ? 'pr-12' : ''}
          `}
          placeholder={placeholder}
        />

        {/* Floating Label */}
        <motion.label
          htmlFor={id}
          className={`
            absolute
            left-4
            transition-all
            duration-300
            pointer-events-none
            select-none
            font-medium
            ${isFocused || hasValue
              ? 'text-xs -top-2.5 bg-white/90 px-2 rounded-md'
              : 'text-base top-3.5'
            }
            ${hasError
              ? 'text-red-600'
              : isFocused || hasValue
                ? 'text-blue-600'
                : 'text-gray-500'
            }
          `}
          animate={{
            y: isFocused || hasValue ? 0 : 0,
            scale: isFocused || hasValue ? 0.9 : 1,
          }}
          transition={{ duration: 0.2 }}
        >
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </motion.label>

        {/* Password Toggle */}
        {isPassword && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
            tabIndex={-1}
          >
            {showPassword ? (
              <EyeOff className="w-5 h-5" />
            ) : (
              <Eye className="w-5 h-5" />
            )}
          </button>
        )}
      </div>

      {/* Error Message */}
      {hasError && (
        <motion.div
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -5 }}
          className="mt-2 text-sm text-red-600 flex items-center gap-1"
        >
          <span className="w-1 h-1 bg-red-600 rounded-full"></span>
          {error}
        </motion.div>
      )}
    </div>
  );
};

export default ModernInput;