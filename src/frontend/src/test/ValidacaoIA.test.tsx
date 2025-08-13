// src/frontend/src/test/ValidacaoIA.test.tsx

import React from 'react';
import { render, screen } from '@testing-library/react';
import { ValidacaoIARow } from '../components/ValidacaoIARow';
import { ValidacaoIAPage } from '../pages/ValidacaoIAPage';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { describe, it, expect, jest } from '@jest/globals';

// Mock Supabase
jest.mock('../lib/supabaseClient', () => ({
  supabase: {
  from: jest.fn(() => ({
  select: jest.fn(() => ({
  order: jest.fn(() => Promise.resolve({
          data: [],
          error: null
        }))
      })),
  insert: jest.fn(() => Promise.resolve({ error: null })),
      update: jest.fn(() => ({ 
        eq: jest.fn(() => Promise.resolve({ error: null }))
      }))
    }))
  }
}));

const theme = createTheme();

const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <BrowserRouter>
    <ThemeProvider theme={theme}>
      {children}
    </ThemeProvider>
  </BrowserRouter>
);

describe('ValidacaoIARow Component', () => {
  const mockExtracao = {
    id: 1,
    documento_id: 1,
    nome_parametro: 'aliquota_inss_faixa_1',
    valor_parametro: '7.5',
    tipo_valor: 'percentual',
    contexto_original: 'A alíquota para a primeira faixa salarial é de 7,5%.',
    ia_confidence_score: 0.95,
    modelo_utilizado: 'gemini-1.5-flash-latest',
    criado_em: '2024-01-01T10:00:00Z',
    status_validacao: 'PENDENTE' as const
  };

  it('renders AI extraction data correctly', () => {
  const mockOnApprove = jest.fn();
  const mockOnEdit = jest.fn();

    render(
      <TestWrapper>
        <ValidacaoIARow 
          extracao={mockExtracao} 
          onApprove={mockOnApprove} 
          onEdit={mockOnEdit} 
        />
      </TestWrapper>
    );

    expect(screen.getByText('aliquota_inss_faixa_1')).toBeInTheDocument();
    expect(screen.getByText('7.5')).toBeInTheDocument();
    expect(screen.getByText('percentual')).toBeInTheDocument();
    expect(screen.getByText(/A alíquota para a primeira faixa salarial é de 7,5%/)).toBeInTheDocument();
    expect(screen.getByText('Confiança: 95%')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /aprovar/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /editar/i })).toBeInTheDocument();
  });

  it('displays confidence score with correct color coding', () => {
    const highConfidenceExtracao = { ...mockExtracao, ia_confidence_score: 0.95 };
    const lowConfidenceExtracao = { ...mockExtracao, ia_confidence_score: 0.45 };

    const { rerender } = render(
      <TestWrapper>
        <ValidacaoIARow 
          extracao={highConfidenceExtracao} 
          onApprove={jest.fn()} 
          onEdit={jest.fn()} 
        />
      </TestWrapper>
    );

    // High confidence should show success color (green)
    expect(screen.getByText('Confiança: 95%')).toBeInTheDocument();

    rerender(
      <TestWrapper>
        <ValidacaoIARow 
          extracao={lowConfidenceExtracao} 
          onApprove={jest.fn()} 
          onEdit={jest.fn()} 
        />
      </TestWrapper>
    );

    // Low confidence should show error color (red)
    expect(screen.getByText('Confiança: 45%')).toBeInTheDocument();
  });
});

describe('ValidacaoIAPage Component', () => {
  it('renders validation page without crashing', () => {
    render(
      <TestWrapper>
        <ValidacaoIAPage />
      </TestWrapper>
    );

    expect(screen.getByText('Validação de Extrações da IA')).toBeInTheDocument();
    expect(screen.getByText(/Revise e valide os parâmetros extraídos pela IA/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /atualizar/i })).toBeInTheDocument();
  });

  it('displays tab navigation correctly', () => {
    render(
      <TestWrapper>
        <ValidacaoIAPage />
      </TestWrapper>
    );

    expect(screen.getByRole('tab', { name: /pendentes/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /concluídas/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /aprovadas/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /rejeitadas/i })).toBeInTheDocument();
  });
});