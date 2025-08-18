// Migrated from src/frontend/pages/folha/ControleMensalPage.tsx
import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
} from '@mui/material';

// Note: These components and services will be created/migrated separately
// import { getControlesDoMes, ControleMensalDetalhado } from '../../../services/controleMensalService';
// import { ControleMensalTable } from '../../../components/ControleMensalTable';
// import { TemplateManager } from '../../../components/TemplateManager';

interface ControleMensalDetalhado {
  id: string;
  nome: string;
  // Add other properties as needed
}

const ControleMensalPage: React.FC = () => {
  const [controles, setControles] = useState<ControleMensalDetalhado[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Logic for selecting month/year
  const [date, setDate] = useState({ 
    month: new Date().getMonth() + 1, 
    year: new Date().getFullYear() 
  });

  const fetchControles = async () => {
    try {
      setLoading(true);
      // const data = await getControlesDoMes(date.year, date.month);
      // setControles(data);
      
      // Temporary mock data for migration purposes
      setControles([]);
      setError(null);
    } catch (err) {
      setError('Falha ao carregar os dados de controle.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchControles();
  }, [date]);

  const handleTemplateApplied = () => {
    // Reload data after applying template
    fetchControles();
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Controle de Folha Mensal
        </Typography>

        {/* Month and Year Selectors */}
        <Paper sx={{ p: 3, mb: 4 }}>
          <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={3} alignItems="center">
            <Box>
              <FormControl sx={{ minWidth: 200 }}>
                <InputLabel id="month-select-label">Mês</InputLabel>
                <Select
                  labelId="month-select-label"
                  value={date.month}
                  label="Mês"
                  onChange={(e) => setDate(prev => ({ ...prev, month: Number(e.target.value) }))}
                >
                  {Array.from({ length: 12 }, (_, i) => (
                    <MenuItem key={i + 1} value={i + 1}>
                      {new Date(2024, i, 1).toLocaleDateString('pt-BR', { month: 'long' })}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
            
            <Box>
              <FormControl sx={{ minWidth: 120 }}>
                <InputLabel id="year-select-label">Ano</InputLabel>
                <Select
                  labelId="year-select-label"
                  value={date.year}
                  label="Ano"
                  onChange={(e) => setDate(prev => ({ ...prev, year: Number(e.target.value) }))}
                >
                  {Array.from({ length: 5 }, (_, i) => (
                    <MenuItem key={2020 + i} value={2020 + i}>
                      {2020 + i}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
            
            <Box>
              <Typography variant="body2" color="text.secondary">
                Mostrando dados para{' '}
                <strong>
                  {new Date(date.year, date.month - 1, 1).toLocaleDateString('pt-BR', { 
                    month: 'long', 
                    year: 'numeric' 
                  })}
                </strong>
              </Typography>
            </Box>
          </Box>
        </Paper>

        {/* Template Management Section */}
        {/* <TemplateManager onTemplateApplied={handleTemplateApplied} /> */}

        {loading && (
          <Box display="flex" justifyContent="center" alignItems="center" py={8}>
            <CircularProgress />
            <Typography variant="body2" sx={{ ml: 2 }}>
              Carregando...
            </Typography>
          </Box>
        )}
        
        {error && (
          <Alert severity="error" sx={{ mb: 4 }}>
            {error}
          </Alert>
        )}
        
        {!loading && !error && (
          <Paper sx={{ p: 3 }}>
            {controles.length > 0 ? (
              // <ControleMensalTable data={controles} />
              <Typography>Tabela de controles será implementada</Typography>
            ) : (
              <Box textAlign="center" py={8}>
                <Typography color="text.secondary">
                  Nenhum controle encontrado para o período selecionado.
                </Typography>
              </Box>
            )}
          </Paper>
        )}
      </Box>
    </Container>
  );
};

export default ControleMensalPage;