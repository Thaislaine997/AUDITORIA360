// Migrated from src/frontend/pages/integracoes/IntegracoesPage.tsx
import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Card,
  CardContent,
  Switch,
  FormControlLabel,
  Chip,
  Alert,
} from "@mui/material";
import {
  Add as AddIcon,
  Settings as SettingsIcon,
  CheckCircle,
  Error,
  Sync,
} from "@mui/icons-material";

interface Integracao {
  id: number;
  nome: string;
  descricao: string;
  tipo: string;
  status: 'ATIVA' | 'INATIVA' | 'ERRO';
  ativa: boolean;
  ultima_sincronizacao?: string;
}

const IntegracoesPage: React.FC = () => {
  const [integracoes, setIntegracoes] = useState<Integracao[]>([
    {
      id: 1,
      nome: "Supabase",
      descricao: "Banco de dados e autenticação",
      tipo: "DATABASE",
      status: "ATIVA",
      ativa: true,
      ultima_sincronizacao: "2024-01-18T10:30:00"
    },
    {
      id: 2,
      nome: "Google Gemini",
      descricao: "API de Inteligência Artificial",
      tipo: "AI",
      status: "ATIVA",
      ativa: true,
      ultima_sincronizacao: "2024-01-18T09:15:00"
    },
    {
      id: 3,
      nome: "Sistema Folha Externa",
      descricao: "Integração com sistema legado",
      tipo: "ERP",
      status: "ERRO",
      ativa: false,
      ultima_sincronizacao: "2024-01-17T14:20:00"
    },
    {
      id: 4,
      nome: "Email SMTP",
      descricao: "Servidor de envio de emails",
      tipo: "EMAIL",
      status: "ATIVA",
      ativa: true,
      ultima_sincronizacao: "2024-01-18T11:00:00"
    }
  ]);

  const handleToggleIntegracao = (id: number) => {
    setIntegracoes(prev => 
      prev.map(integracao => 
        integracao.id === id 
          ? { ...integracao, ativa: !integracao.ativa, status: !integracao.ativa ? 'ATIVA' : 'INATIVA' }
          : integracao
      )
    );
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ATIVA': return <CheckCircle color="success" />;
      case 'ERRO': return <Error color="error" />;
      case 'INATIVA': return <Error color="disabled" />;
      default: return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ATIVA': return 'success';
      case 'ERRO': return 'error';
      case 'INATIVA': return 'default';
      default: return 'default';
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" gutterBottom>
            Integrações
          </Typography>
          <Button variant="contained" startIcon={<AddIcon />}>
            Nova Integração
          </Button>
        </Box>

        <Alert severity="info" sx={{ mb: 4 }}>
          Gerencie todas as integrações do sistema AUDITORIA360. 
          Monitore o status e configure conexões com APIs externas.
        </Alert>

        <Box display="flex" flexDirection="column" gap={2}>
          {integracoes.map((integracao) => (
            <Card key={integracao.id}>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="start">
                  <Box flex={1}>
                    <Box display="flex" alignItems="center" gap={2} mb={1}>
                      {getStatusIcon(integracao.status)}
                      <Typography variant="h6">
                        {integracao.nome}
                      </Typography>
                      <Chip 
                        label={integracao.tipo} 
                        size="small" 
                        variant="outlined"
                      />
                      <Chip 
                        label={integracao.status} 
                        color={getStatusColor(integracao.status) as any}
                        size="small"
                      />
                    </Box>
                    
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {integracao.descricao}
                    </Typography>
                    
                    {integracao.ultima_sincronizacao && (
                      <Typography variant="caption" color="text.secondary">
                        Última sincronização: {' '}
                        {new Date(integracao.ultima_sincronizacao).toLocaleString('pt-BR')}
                      </Typography>
                    )}
                  </Box>
                  
                  <Box display="flex" flexDirection="column" gap={1} alignItems="end">
                    <FormControlLabel
                      control={
                        <Switch
                          checked={integracao.ativa}
                          onChange={() => handleToggleIntegracao(integracao.id)}
                        />
                      }
                      label={integracao.ativa ? "Ativa" : "Inativa"}
                    />
                    
                    <Box display="flex" gap={1}>
                      <Button size="small" startIcon={<Sync />}>
                        Sincronizar
                      </Button>
                      <Button size="small" startIcon={<SettingsIcon />}>
                        Configurar
                      </Button>
                    </Box>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          ))}
        </Box>
      </Box>
    </Container>
  );
};

export default IntegracoesPage;