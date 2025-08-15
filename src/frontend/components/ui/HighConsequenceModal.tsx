import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Typography,
  Box,
  Alert,
  Chip,
  IconButton,
  Collapse,
} from '@mui/material';
import {
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Info as InfoIcon,
  Close as CloseIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
} from '@mui/icons-material';

/**
 * HighConsequenceModal - Componente de Arquitetura de Escolhas
 * 
 * Implementa "atrito positivo" para decisões de alto risco, seguindo os princípios
 * do Fluxo Design System para reduzir erros humanos em operações críticas.
 * 
 * Parte da Grande Síntese: Initiative II - Fluxo Design System
 */

export interface HighConsequenceAction {
  label: string;
  description: string;
  consequence: 'low' | 'medium' | 'high' | 'critical';
  color?: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
  requiresConfirmation?: boolean;
  confirmationText?: string;
  icon?: React.ReactNode;
}

interface HighConsequenceModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  description: string;
  safeAction: HighConsequenceAction;
  dangerousAction: HighConsequenceAction;
  onSafeAction: () => void;
  onDangerousAction: () => void;
  additionalInfo?: string;
  showImpactAnalysis?: boolean;
  impactDetails?: {
    affectedUsers?: number;
    affectedRecords?: number;
    reversible?: boolean;
    estimatedDowntime?: string;
  };
}

export const HighConsequenceModal: React.FC<HighConsequenceModalProps> = ({
  open,
  onClose,
  title,
  description,
  safeAction,
  dangerousAction,
  onSafeAction,
  onDangerousAction,
  additionalInfo,
  showImpactAnalysis = false,
  impactDetails
}) => {
  const [confirmationText, setConfirmationText] = useState('');
  const [showDetails, setShowDetails] = useState(false);
  const [isConfirmationValid, setIsConfirmationValid] = useState(false);
  
  const expectedConfirmation = dangerousAction.confirmationText || 'CONFIRMAR';
  
  useEffect(() => {
    setIsConfirmationValid(confirmationText === expectedConfirmation);
  }, [confirmationText, expectedConfirmation]);
  
  useEffect(() => {
    if (!open) {
      setConfirmationText('');
      setShowDetails(false);
    }
  }, [open]);
  
  const handleSafeAction = () => {
    onSafeAction();
    onClose();
  };
  
  const handleDangerousAction = () => {
    if (dangerousAction.requiresConfirmation && !isConfirmationValid) {
      return;
    }
    onDangerousAction();
    onClose();
  };
  
  const getConsequenceColor = (consequence: HighConsequenceAction['consequence']) => {
    switch (consequence) {
      case 'low': return '#10B981'; // Success green
      case 'medium': return '#F59E0B'; // Warning amber
      case 'high': return '#EF4444'; // Error red
      case 'critical': return '#DC2626'; // Dark red
      default: return '#6B7280'; // Neutral gray
    }
  };
  
  const getConsequenceIcon = (consequence: HighConsequenceAction['consequence']) => {
    switch (consequence) {
      case 'low': return <CheckCircleIcon />;
      case 'medium': return <InfoIcon />;
      case 'high': return <WarningIcon />;
      case 'critical': return <WarningIcon style={{ color: '#DC2626' }} />;
      default: return <InfoIcon />;
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        style: {
          borderRadius: 12,
          border: `2px solid ${getConsequenceColor(dangerousAction.consequence)}`,
          // Fluxo Design System shadow for high consequence
          boxShadow: '0 20px 50px rgba(0, 0, 0, 0.25)',
        }
      }}
    >
      {/* Header with consequence indicator */}
      <DialogTitle
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          backgroundColor: dangerousAction.consequence === 'critical' ? '#FEF2F2' : 'transparent',
          borderBottom: '1px solid #E5E7EB',
          pb: 2
        }}
      >
        {getConsequenceIcon(dangerousAction.consequence)}
        <Box flex={1}>
          <Typography variant="h5" component="h2" fontWeight="600">
            {title}
          </Typography>
          <Chip
            label={`Risco ${dangerousAction.consequence.toUpperCase()}`}
            size="small"
            style={{
              backgroundColor: getConsequenceColor(dangerousAction.consequence),
              color: 'white',
              marginTop: 4
            }}
          />
        </Box>
        <IconButton onClick={onClose} edge="end">
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent sx={{ pt: 3 }}>
        {/* Main description */}
        <Typography variant="body1" sx={{ mb: 3, lineHeight: 1.6 }}>
          {description}
        </Typography>

        {/* Impact Analysis (if enabled) */}
        {showImpactAnalysis && impactDetails && (
          <Box sx={{ mb: 3 }}>
            <Button
              startIcon={showDetails ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              onClick={() => setShowDetails(!showDetails)}
              variant="outlined"
              size="small"
            >
              Análise de Impacto
            </Button>
            <Collapse in={showDetails}>
              <Alert severity="info" sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Impacto Estimado:
                </Typography>
                <ul style={{ margin: 0, paddingLeft: 20 }}>
                  {impactDetails.affectedUsers && (
                    <li>Utilizadores afetados: {impactDetails.affectedUsers}</li>
                  )}
                  {impactDetails.affectedRecords && (
                    <li>Registos afetados: {impactDetails.affectedRecords}</li>
                  )}
                  {impactDetails.reversible !== undefined && (
                    <li>Reversível: {impactDetails.reversible ? 'Sim' : 'Não'}</li>
                  )}
                  {impactDetails.estimatedDowntime && (
                    <li>Tempo inativo estimado: {impactDetails.estimatedDowntime}</li>
                  )}
                </ul>
              </Alert>
            </Collapse>
          </Box>
        )}

        {/* Additional information */}
        {additionalInfo && (
          <Alert severity="warning" sx={{ mb: 3 }}>
            {additionalInfo}
          </Alert>
        )}

        {/* Confirmation input for dangerous actions */}
        {dangerousAction.requiresConfirmation && (
          <Box sx={{ mt: 3, p: 2, backgroundColor: '#FEF2F2', borderRadius: 1 }}>
            <Typography variant="body2" sx={{ mb: 2, color: '#DC2626' }}>
              Para prosseguir com esta ação de risco {dangerousAction.consequence}, 
              digite <strong>"{expectedConfirmation}"</strong> no campo abaixo:
            </Typography>
            <TextField
              fullWidth
              value={confirmationText}
              onChange={(e) => setConfirmationText(e.target.value)}
              placeholder={`Digite "${expectedConfirmation}" para confirmar`}
              error={confirmationText.length > 0 && !isConfirmationValid}
              helperText={
                confirmationText.length > 0 && !isConfirmationValid
                  ? `Deve digitar exatamente "${expectedConfirmation}"`
                  : ''
              }
              sx={{
                '& .MuiOutlinedInput-root': {
                  '&.Mui-error': {
                    '& fieldset': {
                      borderColor: '#DC2626',
                    },
                  },
                },
              }}
            />
          </Box>
        )}
      </DialogContent>

      <DialogActions sx={{ p: 3, gap: 2, justifyContent: 'space-between' }}>
        {/* Safe Action - Made prominent (Fluxo Choice Architecture) */}
        <Button
          onClick={handleSafeAction}
          variant="contained"
          size="large"
          startIcon={safeAction.icon}
          sx={{
            backgroundColor: getConsequenceColor(safeAction.consequence),
            color: 'white',
            minWidth: '150px',
            '&:hover': {
              backgroundColor: getConsequenceColor(safeAction.consequence),
              filter: 'brightness(0.9)',
              transform: 'translateY(-2px)',
              boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
            },
            // Fluxo Design System animation
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          }}
        >
          {safeAction.label}
        </Button>

        <Box flex={1} />

        {/* Dangerous Action - Muted styling (Fluxo Choice Architecture) */}
        <Button
          onClick={handleDangerousAction}
          variant="outlined"
          size="large"
          startIcon={dangerousAction.icon}
          disabled={dangerousAction.requiresConfirmation && !isConfirmationValid}
          sx={{
            borderColor: getConsequenceColor(dangerousAction.consequence),
            color: getConsequenceColor(dangerousAction.consequence),
            minWidth: '150px',
            // Intentionally less prominent styling
            opacity: dangerousAction.requiresConfirmation && !isConfirmationValid ? 0.5 : 0.8,
            '&:hover': {
              backgroundColor: `${getConsequenceColor(dangerousAction.consequence)}10`,
              borderColor: getConsequenceColor(dangerousAction.consequence),
            },
            '&:disabled': {
              borderColor: '#E5E7EB',
              color: '#9CA3AF',
            },
          }}
        >
          {dangerousAction.label}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default HighConsequenceModal;