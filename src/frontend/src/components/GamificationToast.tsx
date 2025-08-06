/**
 * 🎊 GamificationToast - Conscious Celebration Component
 * Celebração que só ocorre em momentos de verdadeiro clímax
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';

interface Achievement {
  id: string;
  title: string;
  description: string;
  points: number;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
  icon: string;
  celebrationIntensity: number;
}

interface GamificationToastProps {
  achievement: Achievement | null;
  onClose: () => void;
  show: boolean;
}

const FLUXO_COLORS = {
  whiteBroken: '#FAFAFA',
  slateBlue: '#475569',
  electricBlue: '#3B82F6',
  mintGreen: '#10B981',
  warning: '#F59E0B',
  success: '#10B981',
  epic: '#8B5CF6',
  legendary: '#F59E0B'
};

const GamificationToast: React.FC<GamificationToastProps> = ({ 
  achievement, 
  onClose, 
  show 
}) => {
  const [confettiTriggered, setConfettiTriggered] = useState(false);
  const [celebrationPhase, setCelebrationPhase] = useState<'initial' | 'climax' | 'completion'>('initial');

  useEffect(() => {
    if (show && achievement && !confettiTriggered) {
      triggerConsciousCelebration(achievement);
      setConfettiTriggered(true);
      
      // Celebration phases for maximum impact
      setTimeout(() => setCelebrationPhase('climax'), 500);
      setTimeout(() => setCelebrationPhase('completion'), 2000);
      setTimeout(() => {
        onClose();
        setConfettiTriggered(false);
        setCelebrationPhase('initial');
      }, 4000);
    }
  }, [show, achievement, confettiTriggered, onClose]);

  // 🎊 Conscious celebration system - only for true achievements
  const triggerConsciousCelebration = (achievement: Achievement) => {
    const intensity = achievement.celebrationIntensity;
    const rarity = achievement.rarity;
    
    // Base confetti for any achievement
    if (intensity >= 0.5) {
      confetti({
        particleCount: Math.floor(50 * intensity),
        spread: 60 + (intensity * 40),
        origin: { y: 0.6 },
        colors: [FLUXO_COLORS.electricBlue, FLUXO_COLORS.mintGreen, FLUXO_COLORS.warning]
      });
    }

    // Enhanced celebration for rare achievements
    if (rarity === 'rare' || rarity === 'epic' || rarity === 'legendary') {
      setTimeout(() => {
        confetti({
          particleCount: 100,
          spread: 120,
          origin: { y: 0.6 },
          colors: rarity === 'legendary' ? 
            ['#FFD700', '#FFA500', '#FF4500'] : 
            [FLUXO_COLORS.epic, FLUXO_COLORS.mintGreen, FLUXO_COLORS.electricBlue]
        });
      }, 300);
    }

    // Epic fireworks for legendary achievements
    if (rarity === 'legendary') {
      const count = 200;
      const defaults = {
        origin: { y: 0.7 }
      };

      function fire(particleRatio: number, opts: any) {
        confetti({
          ...defaults,
          ...opts,
          particleCount: Math.floor(count * particleRatio),
          colors: ['#FFD700', '#FFA500', '#FF4500', '#DC143C']
        });
      }

      setTimeout(() => {
        fire(0.25, { spread: 26, startVelocity: 55 });
        fire(0.2, { spread: 60 });
        fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
        fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
        fire(0.1, { spread: 120, startVelocity: 45 });
      }, 600);
    }
  };

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case 'common': return FLUXO_COLORS.slateBlue;
      case 'rare': return FLUXO_COLORS.electricBlue;
      case 'epic': return FLUXO_COLORS.epic;
      case 'legendary': return FLUXO_COLORS.legendary;
      default: return FLUXO_COLORS.mintGreen;
    }
  };

  const getRarityGlow = (rarity: string) => {
    switch (rarity) {
      case 'rare': return `0 0 20px ${FLUXO_COLORS.electricBlue}40`;
      case 'epic': return `0 0 30px ${FLUXO_COLORS.epic}60`;
      case 'legendary': return `0 0 40px ${FLUXO_COLORS.warning}80, 0 0 60px ${FLUXO_COLORS.warning}40`;
      default: return `0 0 15px ${FLUXO_COLORS.mintGreen}30`;
    }
  };

  const getCelebrationMessage = (rarity: string, points: number) => {
    if (rarity === 'legendary') {
      return `🌟 FEITO LENDÁRIO! ${points} pontos conquistados!`;
    } else if (rarity === 'epic') {
      return `💫 CONQUISTA ÉPICA! ${points} pontos!`;
    } else if (rarity === 'rare') {
      return `✨ Conquista Rara! +${points} pontos`;
    } else {
      return `🎯 Objetivo concluído! +${points} pontos`;
    }
  };

  if (!achievement) return null;

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ opacity: 0, scale: 0.3, y: 50 }}
          animate={{ 
            opacity: 1, 
            scale: celebrationPhase === 'climax' ? 1.05 : 1,
            y: 0 
          }}
          exit={{ opacity: 0, scale: 0.8, y: -50 }}
          transition={{ 
            type: "spring", 
            stiffness: 260, 
            damping: 20,
            duration: celebrationPhase === 'climax' ? 0.8 : 0.5
          }}
          className="fixed top-4 right-4 z-50 max-w-sm"
          style={{
            boxShadow: getRarityGlow(achievement.rarity)
          }}
        >
          <div className="bg-white rounded-xl p-4 border-2 relative overflow-hidden"
               style={{ 
                 borderColor: getRarityColor(achievement.rarity),
                 background: `linear-gradient(135deg, ${FLUXO_COLORS.whiteBroken} 0%, ${getRarityColor(achievement.rarity)}10 100%)`
               }}>
            
            {/* Rarity Indicator */}
            <div className="absolute top-0 right-0 px-3 py-1 text-xs font-bold text-white rounded-bl-lg"
                 style={{ backgroundColor: getRarityColor(achievement.rarity) }}>
              {achievement.rarity.toUpperCase()}
            </div>

            {/* Achievement Content */}
            <div className="flex items-start space-x-3 mt-2">
              <motion.div
                animate={{ 
                  rotate: celebrationPhase === 'climax' ? [0, -10, 10, -10, 0] : 0,
                  scale: celebrationPhase === 'climax' ? [1, 1.2, 1] : 1
                }}
                transition={{ duration: 0.6 }}
                className="text-3xl"
              >
                {achievement.icon}
              </motion.div>
              
              <div className="flex-1">
                <motion.h3 
                  className="font-bold text-lg mb-1"
                  style={{ color: getRarityColor(achievement.rarity) }}
                  animate={{ 
                    scale: celebrationPhase === 'climax' ? [1, 1.1, 1] : 1
                  }}
                  transition={{ duration: 0.4 }}
                >
                  {achievement.title}
                </motion.h3>
                
                <p className="text-sm text-gray-600 mb-2">
                  {achievement.description}
                </p>
                
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '100%' }}
                  transition={{ delay: 0.5, duration: 1 }}
                  className="bg-gray-200 rounded-full h-2 mb-2 overflow-hidden"
                >
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '100%' }}
                    transition={{ delay: 0.8, duration: 0.8 }}
                    className="h-full rounded-full"
                    style={{ backgroundColor: getRarityColor(achievement.rarity) }}
                  />
                </motion.div>
                
                <motion.p 
                  className="text-sm font-semibold"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 1.2 }}
                  style={{ color: getRarityColor(achievement.rarity) }}
                >
                  {getCelebrationMessage(achievement.rarity, achievement.points)}
                </motion.p>
              </div>
            </div>

            {/* Particle Effects for Epic/Legendary */}
            {(achievement.rarity === 'epic' || achievement.rarity === 'legendary') && (
              <motion.div
                className="absolute inset-0 pointer-events-none"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0, 1, 0] }}
                transition={{ duration: 2, repeat: 2 }}
              >
                {[...Array(5)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-1 h-1 rounded-full"
                    style={{ 
                      backgroundColor: getRarityColor(achievement.rarity),
                      left: `${20 + i * 15}%`,
                      top: `${30 + (i % 2) * 40}%`
                    }}
                    animate={{
                      y: [-10, 10, -10],
                      opacity: [0, 1, 0],
                      scale: [0.5, 1.5, 0.5]
                    }}
                    transition={{
                      duration: 1.5,
                      delay: i * 0.2,
                      repeat: Infinity
                    }}
                  />
                ))}
              </motion.div>
            )}

            {/* Close button */}
            <button
              onClick={onClose}
              className="absolute top-2 right-8 text-gray-400 hover:text-gray-600 text-sm"
            >
              ✕
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

// 🎮 Achievement System Hook
export const useGamification = () => {
  const [currentAchievement, setCurrentAchievement] = useState<Achievement | null>(null);
  const [showToast, setShowToast] = useState(false);
  const [userProgress, setUserProgress] = useState({
    totalPoints: 0,
    completedTasks: 0,
    streakDays: 0,
    level: 1
  });

  // 🏆 Predefined achievements for conscious celebration
  const achievements: Achievement[] = [
    {
      id: 'first_payroll',
      title: 'Primeiro Processamento',
      description: 'Concluiu o seu primeiro processamento de vencimentos',
      points: 100,
      rarity: 'common',
      icon: '💰',
      celebrationIntensity: 0.6
    },
    {
      id: 'cct_master',
      title: 'Especialista CCT',
      description: 'Utilizou 5 códigos CCT diferentes',
      points: 250,
      rarity: 'rare',
      icon: '📋',
      celebrationIntensity: 0.8
    },
    {
      id: 'error_free_week',
      title: 'Semana Perfeita',
      description: 'Uma semana inteira sem erros de processamento',
      points: 500,
      rarity: 'epic',
      icon: '🎯',
      celebrationIntensity: 0.9
    },
    {
      id: 'telepathic_symbiosis',
      title: 'Simbiose Telepática',
      description: 'Interface antecipou 100 ações suas com sucesso',
      points: 1000,
      rarity: 'legendary',
      icon: '🔮',
      celebrationIntensity: 1.0
    },
    {
      id: 'productivity_surge',
      title: 'Produtividade Máxima',
      description: 'Processou 50 vencimentos num só dia',
      points: 750,
      rarity: 'epic',
      icon: '⚡',
      celebrationIntensity: 0.95
    }
  ];

  // 🎊 Trigger achievement celebration
  const triggerAchievement = (achievementId: string) => {
    const achievement = achievements.find(a => a.id === achievementId);
    if (achievement) {
      setCurrentAchievement(achievement);
      setShowToast(true);
      
      // Update user progress
      setUserProgress(prev => ({
        ...prev,
        totalPoints: prev.totalPoints + achievement.points,
        level: Math.floor((prev.totalPoints + achievement.points) / 1000) + 1
      }));
    }
  };

  // 🔍 Check for achievement triggers based on user actions
  const checkAchievements = (action: string, context: any = {}) => {
    switch (action) {
      case 'payroll_completed':
        if (userProgress.completedTasks === 0) {
          triggerAchievement('first_payroll');
        }
        setUserProgress(prev => ({ ...prev, completedTasks: prev.completedTasks + 1 }));
        break;
        
      case 'cct_used':
        // Logic to track different CCT usage
        triggerAchievement('cct_master'); // Simplified for demo
        break;
        
      case 'telepathic_success':
        // Logic to track telepathic interface successes
        if (context.successCount >= 100) {
          triggerAchievement('telepathic_symbiosis');
        }
        break;
        
      case 'high_productivity':
        if (context.dailyProcessed >= 50) {
          triggerAchievement('productivity_surge');
        }
        break;
    }
  };

  const closeToast = () => {
    setShowToast(false);
    setTimeout(() => setCurrentAchievement(null), 300);
  };

  return {
    currentAchievement,
    showToast,
    userProgress,
    triggerAchievement,
    checkAchievements,
    closeToast,
    GamificationToast: (props: Partial<GamificationToastProps>) => (
      <GamificationToast
        achievement={currentAchievement}
        show={showToast}
        onClose={closeToast}
        {...props}
      />
    )
  };
};

export default GamificationToast;