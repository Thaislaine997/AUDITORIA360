import React, { useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Fade,
  alpha,
  useTheme,
} from "@mui/material";
import {
  Lock,
  Close,
  Insights,
  TrendingUp,
  Security,
  AutoAwesome,
  PlayArrow,
} from "@mui/icons-material";

interface PremiumFeatureTeaserProps {
  /** The premium feature being promoted */
  feature: "consultor-riscos" | "insight-cognitivo" | "auditoria-avancada" | "compliance-inteligente";
  /** Visual style variant */
  variant?: "card" | "banner" | "popup";
  /** Custom styling */
  className?: string;
  /** Callback when trial is started */
  onTrialStart?: (feature: string) => void;
  /** Callback when teaser is dismissed */
  onDismiss?: () => void;
}

const featureConfig = {
  "consultor-riscos": {
    title: "Consultor de Riscos IA",
    subtitle: "Análise preditiva de riscos financeiros e operacionais",
    description: "Identifique padrões de risco antes que se tornem problemas críticos. Nossa IA analisa milhares de pontos de dados para fornecer insights acionáveis.",
    icon: <Security />,
    color: "#ff6b35",
    benefits: [
      "Prevenção proativa de fraudes",
      "Análise de conformidade em tempo real",
      "Relatórios de risco personalizados",
      "Alertas inteligentes de anomalias"
    ],
  },
  "insight-cognitivo": {
    title: "Insight Cognitivo",
    subtitle: "Inteligência artificial que aprende com seus dados",
    description: "Transforme dados em decisões estratégicas com nossa engine de IA que compreende o contexto do seu negócio.",
    icon: <Insights />,
    color: "#6c5ce7",
    benefits: [
      "Análise semântica de documentos",
      "Recomendações personalizadas",
      "Automação de processos complexos",
      "Dashboard adaptativos"
    ],
  },
  "auditoria-avancada": {
    title: "Auditoria Avançada",
    subtitle: "Auditoria contínua e automatizada",
    description: "Monitore sua organização 24/7 com auditoria inteligente que detecta irregularidades em tempo real.",
    icon: <TrendingUp />,
    color: "#00b894",
    benefits: [
      "Auditoria contínua automatizada",
      "Trilhas de auditoria completas",
      "Conformidade regulatória",
      "Relatórios executivos dinâmicos"
    ],
  },
  "compliance-inteligente": {
    title: "Compliance Inteligente",
    subtitle: "Conformidade que se adapta às mudanças regulatórias",
    description: "Mantenha-se sempre em conformidade com IA que monitora mudanças regulatórias e adapta seus processos automaticamente.",
    icon: <AutoAwesome />,
    color: "#fd79a8",
    benefits: [
      "Monitoramento regulatório em tempo real",
      "Adaptação automática de processos",
      "Alertas de mudanças normativas",
      "Compliance score dinâmico"
    ],
  },
};

const PremiumFeatureTeaser: React.FC<PremiumFeatureTeaserProps> = ({
  feature,
  variant = "card",
  className = "",
  onTrialStart,
  onDismiss,
}) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [isStartingTrial, setIsStartingTrial] = useState(false);
  const theme = useTheme();
  
  const config = featureConfig[feature];

  const handleTrialStart = async () => {
    setIsStartingTrial(true);
    
    try {
      // Simulate API call to enable feature flag
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      if (onTrialStart) {
        onTrialStart(feature);
      }
      
      setModalOpen(false);
      
      // Show success notification (could integrate with existing notification system)
      console.log(`🚀 Trial started for ${config.title}`);
      
    } catch (error) {
      console.error("Failed to start trial:", error);
    } finally {
      setIsStartingTrial(false);
    }
  };

  const TeaserCard = () => (
    <Card 
      sx={{ 
        position: 'relative',
        background: `linear-gradient(135deg, ${alpha(config.color, 0.1)} 0%, ${alpha(config.color, 0.05)} 100%)`,
        border: `1px solid ${alpha(config.color, 0.2)}`,
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: theme.shadows[4],
          borderColor: alpha(config.color, 0.4),
        }
      }}
      onClick={() => setModalOpen(true)}
      className={className}
    >
      {/* Premium Badge */}
      <Box
        sx={{
          position: 'absolute',
          top: 12,
          right: 12,
          zIndex: 1,
        }}
      >
        <Chip
          icon={<Lock sx={{ fontSize: 16 }} />}
          label="Premium"
          size="small"
          sx={{
            bgcolor: config.color,
            color: 'white',
            fontWeight: 'bold',
          }}
        />
      </Box>

      <CardContent sx={{ pt: 3 }}>
        {/* Feature Icon */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            mb: 2,
            color: config.color,
          }}
        >
          <Box sx={{ mr: 1, fontSize: 28 }}>
            {config.icon}
          </Box>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
            {config.title}
          </Typography>
        </Box>

        {/* Feature Description */}
        <Typography 
          variant="body2" 
          color="text.secondary" 
          sx={{ mb: 2, opacity: 0.8 }}
        >
          {config.subtitle}
        </Typography>

        {/* CTA Button */}
        <Button
          variant="outlined"
          startIcon={<PlayArrow />}
          sx={{
            borderColor: config.color,
            color: config.color,
            '&:hover': {
              bgcolor: alpha(config.color, 0.1),
              borderColor: config.color,
            }
          }}
          fullWidth
        >
          Experimentar Grátis
        </Button>
      </CardContent>

      {/* Subtle Animation Effect */}
      <Box
        sx={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: 3,
          background: `linear-gradient(90deg, ${config.color}, ${alpha(config.color, 0.5)})`,
          opacity: 0.6,
        }}
      />
    </Card>
  );

  const FeatureModal = () => (
    <Dialog 
      open={modalOpen} 
      onClose={() => setModalOpen(false)}
      maxWidth="sm"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 3,
          overflow: 'hidden',
        }
      }}
    >
      {/* Header with gradient */}
      <Box
        sx={{
          background: `linear-gradient(135deg, ${config.color} 0%, ${alpha(config.color, 0.8)} 100%)`,
          color: 'white',
          p: 3,
          position: 'relative',
        }}
      >
        <IconButton
          onClick={() => setModalOpen(false)}
          sx={{ 
            position: 'absolute', 
            top: 8, 
            right: 8,
            color: 'white',
          }}
        >
          <Close />
        </IconButton>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Box sx={{ mr: 2, fontSize: 32 }}>
            {config.icon}
          </Box>
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
              {config.title}
            </Typography>
            <Typography variant="subtitle1" sx={{ opacity: 0.9 }}>
              {config.subtitle}
            </Typography>
          </Box>
        </Box>
      </Box>

      <DialogContent sx={{ p: 3 }}>
        <Typography variant="body1" sx={{ mb: 3, lineHeight: 1.6 }}>
          {config.description}
        </Typography>

        <Typography variant="h6" sx={{ mb: 2, color: config.color }}>
          Recursos Inclusos:
        </Typography>
        
        <Box sx={{ pl: 2 }}>
          {config.benefits.map((benefit, index) => (
            <Typography 
              key={index} 
              variant="body2" 
              sx={{ 
                mb: 1, 
                display: 'flex', 
                alignItems: 'center',
                '&:before': {
                  content: '"✓"',
                  color: config.color,
                  fontWeight: 'bold',
                  mr: 1,
                }
              }}
            >
              {benefit}
            </Typography>
          ))}
        </Box>

        <Box
          sx={{
            mt: 3,
            p: 2,
            bgcolor: alpha(config.color, 0.1),
            borderRadius: 2,
            border: `1px solid ${alpha(config.color, 0.2)}`,
          }}
        >
          <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 1 }}>
            🎯 Trial Gratuito de 14 Dias
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Experimente todos os recursos premium sem compromisso. 
            Cancele a qualquer momento durante o período de trial.
          </Typography>
        </Box>
      </DialogContent>

      <DialogActions sx={{ p: 3, pt: 0 }}>
        <Button 
          onClick={() => setModalOpen(false)}
          color="inherit"
        >
          Talvez Depois
        </Button>
        <Button
          variant="contained"
          onClick={handleTrialStart}
          disabled={isStartingTrial}
          sx={{
            bgcolor: config.color,
            '&:hover': {
              bgcolor: alpha(config.color, 0.8),
            }
          }}
        >
          {isStartingTrial ? "Ativando..." : "Iniciar Trial Gratuito"}
        </Button>
      </DialogActions>
    </Dialog>
  );

  if (variant === "card") {
    return (
      <>
        <TeaserCard />
        <FeatureModal />
      </>
    );
  }

  // Future: implement banner and popup variants
  return (
    <>
      <TeaserCard />
      <FeatureModal />
    </>
  );
};

export default PremiumFeatureTeaser;