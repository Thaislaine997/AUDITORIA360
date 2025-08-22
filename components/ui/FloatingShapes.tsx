import React from 'react';
import { motion } from 'framer-motion';

interface FloatingShapesProps {
  className?: string;
}

const FloatingShapes: React.FC<FloatingShapesProps> = ({ className = '' }) => {
  return (
    <div className={`absolute inset-0 overflow-hidden pointer-events-none ${className}`}>
      {/* Large floating circle */}
      <motion.div
        className="absolute w-72 h-72 rounded-full bg-gradient-to-r from-blue-400/20 to-purple-500/20 blur-3xl"
        style={{ top: '10%', left: '10%' }}
        animate={{
          y: [0, -20, 0],
          x: [0, 10, 0],
          scale: [1, 1.1, 1],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      {/* Medium floating circle */}
      <motion.div
        className="absolute w-48 h-48 rounded-full bg-gradient-to-r from-cyan-400/15 to-blue-500/15 blur-2xl"
        style={{ top: '60%', right: '15%' }}
        animate={{
          y: [0, 15, 0],
          x: [0, -15, 0],
          scale: [1, 0.9, 1],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 1
        }}
      />
      
      {/* Small floating circle */}
      <motion.div
        className="absolute w-32 h-32 rounded-full bg-gradient-to-r from-indigo-400/10 to-cyan-500/10 blur-xl"
        style={{ bottom: '20%', left: '70%' }}
        animate={{
          y: [0, -10, 0],
          x: [0, 8, 0],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 2
        }}
      />
      
      {/* Geometric shapes */}
      <motion.div
        className="absolute w-16 h-16 bg-blue-500/10 backdrop-blur-sm border border-blue-300/20"
        style={{ top: '30%', right: '5%', transform: 'rotate(45deg)' }}
        animate={{
          rotate: [45, 65, 45],
          scale: [1, 1.1, 1],
        }}
        transition={{
          duration: 7,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      <motion.div
        className="absolute w-12 h-12 rounded-full bg-gradient-to-r from-purple-400/15 to-pink-500/15 border border-purple-300/20"
        style={{ bottom: '40%', left: '5%' }}
        animate={{
          y: [0, -12, 0],
          scale: [1, 0.8, 1],
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 0.5
        }}
      />
    </div>
  );
};

export default FloatingShapes;