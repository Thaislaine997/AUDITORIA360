import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: 'onboarding' | 'productivity' | 'quality' | 'collaboration' | 'expertise';
  xpReward: number;
  unlockedAt?: Date;
  progress: number; // 0-100
  requirements: {
    type: 'action_count' | 'streak' | 'completion' | 'score';
    target: number;
    current: number;
  };
}

export interface Mission {
  id: string;
  title: string;
  description: string;
  category: 'daily' | 'weekly' | 'monthly' | 'special';
  xpReward: number;
  deadline?: Date;
  completed: boolean;
  completedAt?: Date;
  progress: number; // 0-100
  requirements: {
    type: 'cadastro_cliente' | 'gerar_relatorio' | 'revisar_auditoria' | 'configurar_cliente';
    target: number;
    current: number;
  };
}

export interface UserProgress {
  level: number;
  currentXP: number;
  xpToNextLevel: number;
  totalXP: number;
  streak: number; // consecutive days of activity
  lastActivityDate?: Date;
}

export interface SkillTree {
  id: string;
  name: string;
  description: string;
  category: 'auditoria' | 'folha' | 'gestao' | 'compliance';
  unlocked: boolean;
  level: number;
  maxLevel: number;
  xpRequired: number;
  benefits: string[];
}

interface GamificationState {
  userProgress: UserProgress;
  achievements: Achievement[];
  missions: Mission[];
  skillTree: SkillTree[];
  toastQueue: Array<{
    type: 'achievement' | 'mission' | 'level_up' | 'xp_gain';
    data: any;
  }>;
  
  // Actions
  addXP: (amount: number, source: string) => void;
  completeMission: (missionId: string) => void;
  unlockAchievement: (achievementId: string) => void;
  updateMissionProgress: (missionId: string, progress: number) => void;
  updateAchievementProgress: (achievementId: string, progress: number) => void;
  upgradeSkill: (skillId: string) => void;
  dismissToast: () => void;
  recordActivity: () => void;
  
  // Getters
  getUnlockedAchievements: () => Achievement[];
  getActiveMissions: () => Mission[];
  getCompletedMissions: () => Mission[];
  getAvailableSkills: () => SkillTree[];
}

const initialSkillTree: SkillTree[] = [
  {
    id: 'auditoria_basica',
    name: 'Auditoria Básica',
    description: 'Fundamentos de auditoria e conformidade',
    category: 'auditoria',
    unlocked: true,
    level: 1,
    maxLevel: 5,
    xpRequired: 100,
    benefits: ['Relatórios básicos', 'Análise de documentos'],
  },
  {
    id: 'gestao_clientes',
    name: 'Gestão de Clientes',
    description: 'Habilidades de relacionamento e gestão',
    category: 'gestao',
    unlocked: true,
    level: 1,
    maxLevel: 5,
    xpRequired: 150,
    benefits: ['Dashboard avançado', 'Relatórios personalizados'],
  },
];

const initialMissions: Mission[] = [
  {
    id: 'first_client',
    title: 'Primeiro Cliente',
    description: 'Cadastre seu primeiro cliente na plataforma',
    category: 'daily',
    xpReward: 50,
    completed: false,
    progress: 0,
    requirements: {
      type: 'cadastro_cliente',
      target: 1,
      current: 0,
    },
  },
  {
    id: 'generate_report',
    title: 'Primeiro Relatório',
    description: 'Gere seu primeiro relatório de auditoria',
    category: 'daily',
    xpReward: 75,
    completed: false,
    progress: 0,
    requirements: {
      type: 'gerar_relatorio',
      target: 1,
      current: 0,
    },
  },
];

const initialAchievements: Achievement[] = [
  {
    id: 'welcome',
    title: 'Bem-vindo!',
    description: 'Complete seu primeiro login na plataforma',
    icon: '🎉',
    category: 'onboarding',
    xpReward: 25,
    progress: 0,
    requirements: {
      type: 'action_count',
      target: 1,
      current: 0,
    },
  },
  {
    id: 'client_master',
    title: 'Mestre dos Clientes',
    description: 'Cadastre 10 clientes na plataforma',
    icon: '👥',
    category: 'productivity',
    xpReward: 200,
    progress: 0,
    requirements: {
      type: 'action_count',
      target: 10,
      current: 0,
    },
  },
];

export const useGamificationStore = create<GamificationState>()(
  persist(
    (set, get) => ({
      userProgress: {
        level: 1,
        currentXP: 0,
        xpToNextLevel: 100,
        totalXP: 0,
        streak: 0,
      },
      achievements: initialAchievements,
      missions: initialMissions,
      skillTree: initialSkillTree,
      toastQueue: [],

      addXP: (amount, source) => {
        set((state) => {
          const newTotalXP = state.userProgress.totalXP + amount;
          let newLevel = state.userProgress.level;
          let newCurrentXP = state.userProgress.currentXP + amount;
          let newXPToNext = state.userProgress.xpToNextLevel;
          const newToastQueue = [...state.toastQueue];

          // Add XP gain toast
          newToastQueue.push({
            type: 'xp_gain',
            data: { amount, source },
          });

          // Check for level up
          while (newCurrentXP >= newXPToNext) {
            newCurrentXP -= newXPToNext;
            newLevel++;
            newXPToNext = newLevel * 100; // Simple progression: level * 100 XP
            
            newToastQueue.push({
              type: 'level_up',
              data: { level: newLevel },
            });
          }

          return {
            userProgress: {
              ...state.userProgress,
              level: newLevel,
              currentXP: newCurrentXP,
              xpToNextLevel: newXPToNext,
              totalXP: newTotalXP,
            },
            toastQueue: newToastQueue,
          };
        });
      },

      completeMission: (missionId) => {
        set((state) => {
          const mission = state.missions.find(m => m.id === missionId);
          if (!mission || mission.completed) return state;

          const updatedMissions = state.missions.map(m =>
            m.id === missionId
              ? { ...m, completed: true, completedAt: new Date(), progress: 100 }
              : m
          );

          const newToastQueue = [...state.toastQueue, {
            type: 'mission',
            data: { mission },
          }];

          // Add XP for completing mission
          get().addXP(mission.xpReward, `Mission: ${mission.title}`);

          return {
            missions: updatedMissions,
            toastQueue: newToastQueue,
          };
        });
      },

      unlockAchievement: (achievementId) => {
        set((state) => {
          const achievement = state.achievements.find(a => a.id === achievementId);
          if (!achievement || achievement.unlockedAt) return state;

          const updatedAchievements = state.achievements.map(a =>
            a.id === achievementId
              ? { ...a, unlockedAt: new Date(), progress: 100 }
              : a
          );

          const newToastQueue = [...state.toastQueue, {
            type: 'achievement',
            data: { achievement },
          }];

          // Add XP for achievement
          get().addXP(achievement.xpReward, `Achievement: ${achievement.title}`);

          return {
            achievements: updatedAchievements,
            toastQueue: newToastQueue,
          };
        });
      },

      updateMissionProgress: (missionId, progress) => {
        set((state) => ({
          missions: state.missions.map(mission =>
            mission.id === missionId
              ? { ...mission, progress: Math.min(100, Math.max(0, progress)) }
              : mission
          ),
        }));

        // Auto-complete if progress reaches 100%
        const mission = get().missions.find(m => m.id === missionId);
        if (mission && progress >= 100 && !mission.completed) {
          get().completeMission(missionId);
        }
      },

      updateAchievementProgress: (achievementId, progress) => {
        set((state) => ({
          achievements: state.achievements.map(achievement =>
            achievement.id === achievementId
              ? { ...achievement, progress: Math.min(100, Math.max(0, progress)) }
              : achievement
          ),
        }));

        // Auto-unlock if progress reaches 100%
        const achievement = get().achievements.find(a => a.id === achievementId);
        if (achievement && progress >= 100 && !achievement.unlockedAt) {
          get().unlockAchievement(achievementId);
        }
      },

      upgradeSkill: (skillId) => {
        set((state) => {
          const skill = state.skillTree.find(s => s.id === skillId);
          if (!skill || skill.level >= skill.maxLevel) return state;

          if (state.userProgress.totalXP >= skill.xpRequired) {
            return {
              skillTree: state.skillTree.map(s =>
                s.id === skillId
                  ? { ...s, level: s.level + 1, xpRequired: s.xpRequired * 1.5 }
                  : s
              ),
            };
          }
          return state;
        });
      },

      dismissToast: () => {
        set((state) => ({
          toastQueue: state.toastQueue.slice(1),
        }));
      },

      recordActivity: () => {
        set((state) => {
          const today = new Date();
          const lastActivity = state.userProgress.lastActivityDate;
          const isConsecutiveDay = lastActivity && 
            (today.getTime() - lastActivity.getTime()) < (48 * 60 * 60 * 1000); // within 48 hours

          return {
            userProgress: {
              ...state.userProgress,
              streak: isConsecutiveDay ? state.userProgress.streak + 1 : 1,
              lastActivityDate: today,
            },
          };
        });
      },

      getUnlockedAchievements: () => {
        return get().achievements.filter(a => a.unlockedAt);
      },

      getActiveMissions: () => {
        return get().missions.filter(m => !m.completed);
      },

      getCompletedMissions: () => {
        return get().missions.filter(m => m.completed);
      },

      getAvailableSkills: () => {
        return get().skillTree.filter(s => s.unlocked);
      },
    }),
    {
      name: 'gamification-state',
    }
  )
);