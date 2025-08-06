import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Grid,
  Button,
  Card,
  CardContent,
  CardActions,
  Alert,
  Chip,
  Divider,
} from '@mui/material';
import {
  Psychology,
  Speed,
  Visibility,
  Science,
  AutoAwesome,
} from '@mui/icons-material';
import { useIntentionStore } from '../stores/intentionStore';
import { useNeuralSignalTracking, useIntentionTrigger, usePredictiveLoading, useAdaptiveUI } from '../hooks/useNeuralSignals';
import EmpathicTextField from '../components/ui/EmpathicTextField';

const NeuroSymbolicDemo: React.FC = () => {
  const [demoFormData, setDemoFormData] = useState({
    email: '',
    phone: '',
    cnpj: '',
  });

  // Neural interface hooks
  const {
    currentIntentions,
    cognitiveLoad,
    preloadedData,
    mousePatterns,
    typingPatterns,
    hoverDuration,
  } = useIntentionStore();

  const { predictions, isDataPreloaded } = usePredictiveLoading();
  const { shouldSimplify, adaptationStrategy, loadLevel } = useAdaptiveUI();
  
  // Demo intention triggers
  const demoButton1Ref = useIntentionTrigger("demo_button_1", "action");
  const demoButton2Ref = useIntentionTrigger("demo_button_2", "navigation");
  const demoButton3Ref = useIntentionTrigger("demo_button_3", "data_view");

  const handleFormSubmit = () => {
    alert('🧠 Formulário processado com interface neuro-simbólica!\n\nDados adaptados baseados nos seus padrões neurais.');
  };

  const triggerPrivacyIntention = () => {
    // This will activate the LGPD Guardian
    window.location.hash = '#lgpd-compliance';
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" gutterBottom sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
          <Psychology color="primary" />
          Interface Neuro-Simbólica
          <AutoAwesome color="secondary" />
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Demonstração do Diálogo Preditivo entre Mente e Máquina
        </Typography>
      </Box>

      {/* Neural Status Panel */}
      <Paper sx={{ p: 3, mb: 4, bgcolor: 'background.default' }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Science color="primary" />
          Status Neural da Interface
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="primary">
                  🧠 Sinais Neurais
                </Typography>
                <Typography variant="body2">
                  Movimentos do mouse: {mousePatterns.length}
                </Typography>
                <Typography variant="body2">
                  Padrões de digitação: {typingPatterns.length}
                </Typography>
                <Typography variant="body2">
                  Elementos monitorados: {Object.keys(hoverDuration).length}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="secondary">
                  🎯 Intenções Detectadas
                </Typography>
                <Typography variant="body2">
                  Intenções ativas: {currentIntentions.length}
                </Typography>
                <Typography variant="body2">
                  Carga cognitiva: {cognitiveLoad.level.toUpperCase()}
                </Typography>
                <Typography variant="body2">
                  Adaptação necessária: {cognitiveLoad.adaptationRequired ? 'Sim' : 'Não'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="success">
                  🚀 Dados Pré-carregados
                </Typography>
                <Typography variant="body2">
                  Cache entries: {Object.keys(preloadedData).length}
                </Typography>
                <Typography variant="body2">
                  Predições: {Object.keys(predictions).length}
                </Typography>
                <Typography variant="body2">
                  Interface adaptativa: {shouldSimplify ? 'Ativa' : 'Inativa'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>

      {/* Demo Form with Empathetic Error Handling */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          📝 Formulário com Tratamento Empático de Erros
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Tente cometer erros nos campos abaixo. Após 3 erros, o assistente empático será ativado.
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <EmpathicTextField
              formId="demo_form"
              fieldName="email"
              label="Email"
              fullWidth
              empathicHelp={{
                errorType: 'email',
                helpMessage: 'Emails devem ter formato válido',
                example: 'usuario@empresa.com.br'
              }}
              validationRules={{
                required: true,
                pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
              }}
              value={demoFormData.email}
              onChange={(e) => setDemoFormData(prev => ({ ...prev, email: e.target.value }))}
            />
          </Grid>
          
          <Grid item xs={12} md={4}>
            <EmpathicTextField
              formId="demo_form"
              fieldName="phone"
              label="Telefone"
              fullWidth
              empathicHelp={{
                errorType: 'phone',
                helpMessage: 'Telefones devem seguir o formato brasileiro',
                example: '(11) 99999-9999'
              }}
              validationRules={{
                required: true,
                pattern: /^\(\d{2}\) \d{4,5}-\d{4}$/
              }}
              value={demoFormData.phone}
              onChange={(e) => setDemoFormData(prev => ({ ...prev, phone: e.target.value }))}
            />
          </Grid>
          
          <Grid item xs={12} md={4}>
            <EmpathicTextField
              formId="demo_form"
              fieldName="cnpj"
              label="CNPJ"
              fullWidth
              empathicHelp={{
                errorType: 'cnpj',
                helpMessage: 'CNPJ deve ter 14 dígitos',
                example: '11.222.333/0001-44'
              }}
              validationRules={{
                required: true,
                pattern: /^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/
              }}
              value={demoFormData.cnpj}
              onChange={(e) => setDemoFormData(prev => ({ ...prev, cnpj: e.target.value }))}
            />
          </Grid>
        </Grid>
        
        <Box sx={{ mt: 3 }}>
          <Button variant="contained" onClick={handleFormSubmit}>
            Enviar Formulário
          </Button>
        </Box>
      </Paper>

      {/* Intention Detection Demo */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          🎯 Demonstração de Detecção de Intenções
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Pouse o mouse sobre os botões por mais de 500ms para ativar a detecção neural de intenções.
        </Typography>
        
        <Grid container spacing={2}>
          <Grid item>
            <Button
              ref={demoButton1Ref}
              variant="outlined"
              color="primary"
              sx={{
                '&:hover': {
                  transform: 'scale(1.05)',
                  transition: 'all 0.3s ease',
                },
              }}
            >
              Botão de Ação
            </Button>
          </Grid>
          
          <Grid item>
            <Button
              ref={demoButton2Ref}
              variant="outlined"
              color="secondary"
              sx={{
                '&:hover': {
                  transform: 'scale(1.05)',
                  transition: 'all 0.3s ease',
                },
              }}
            >
              Navegação
            </Button>
          </Grid>
          
          <Grid item>
            <Button
              ref={demoButton3Ref}
              variant="outlined"
              color="success"
              sx={{
                '&:hover': {
                  transform: 'scale(1.05)',
                  transition: 'all 0.3s ease',
                },
              }}
            >
              Visualizar Dados
            </Button>
          </Grid>
          
          <Grid item>
            <Button
              variant="outlined"
              color="warning"
              onClick={triggerPrivacyIntention}
            >
              🛡️ Ativar Guardião LGPD
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Adaptive UI Demo */}
      {shouldSimplify && (
        <Alert severity="warning" sx={{ mb: 4 }} icon={<Psychology />}>
          <Typography variant="h6">
            🧠 Interface Adaptativa Ativada
          </Typography>
          <Typography variant="body2">
            A interface detectou alta carga cognitiva e se adaptou automaticamente:
          </Typography>
          <Box sx={{ mt: 1 }}>
            {adaptationStrategy.hideAdvancedFeatures && <Chip label="Recursos avançados ocultos" color="warning" size="small" sx={{ mr: 1 }} />}
            {adaptationStrategy.highlightPrimaryActions && <Chip label="Ações primárias destacadas" color="info" size="small" sx={{ mr: 1 }} />}
            {adaptationStrategy.showHelpHints && <Chip label="Dicas de ajuda ativas" color="success" size="small" sx={{ mr: 1 }} />}
            {adaptationStrategy.reduceAnimations && <Chip label="Animações reduzidas" color="secondary" size="small" />}
          </Box>
        </Alert>
      )}

      {/* Current Intentions Display */}
      {currentIntentions.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Visibility color="primary" />
            Intenções Neurais Detectadas
          </Typography>
          {currentIntentions.map((intention, index) => (
            <Alert 
              key={intention.id} 
              severity="info" 
              sx={{ mb: 1 }}
              icon={<Speed />}
            >
              <Typography variant="body2">
                <strong>{intention.type}</strong> → {intention.target} 
                (Confiança: {(intention.confidence * 100).toFixed(0)}%)
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {new Date(intention.timestamp).toLocaleTimeString()}
              </Typography>
            </Alert>
          ))}
        </Paper>
      )}
    </Container>
  );
};

export default NeuroSymbolicDemo;