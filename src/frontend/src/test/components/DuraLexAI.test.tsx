import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { createTheme } from '@mui/material';
import DuraLexAI from '../../components/kairos/DuraLexAI';

const theme = createTheme();

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        {component}
      </ThemeProvider>
    </BrowserRouter>
  );
};

describe('DuraLexAI', () => {
  const mockOnClose = vi.fn();

  beforeEach(() => {
    mockOnClose.mockClear();
  });

  it('renders when open is true', () => {
    renderWithProviders(
      <DuraLexAI open={true} onClose={mockOnClose} />
    );

    expect(screen.getByText('DURA LEX')).toBeInTheDocument();
    expect(screen.getByText('Consciência Jurídica Preditiva')).toBeInTheDocument();
  });

  it('does not render when open is false', () => {
    renderWithProviders(
      <DuraLexAI open={false} onClose={mockOnClose} />
    );

    expect(screen.queryByText('DURA LEX')).not.toBeInTheDocument();
  });

  it('shows tabs for the three AI functions', () => {
    renderWithProviders(
      <DuraLexAI open={true} onClose={mockOnClose} />
    );

    expect(screen.getByText('Fiscal do Futuro')).toBeInTheDocument();
    expect(screen.getByText('Simulador de Cenários')).toBeInTheDocument();
    expect(screen.getByText('Vigia da Legislação')).toBeInTheDocument();
  });

  it('displays predictive audit risks by default', () => {
    renderWithProviders(
      <DuraLexAI open={true} onClose={mockOnClose} />
    );

    expect(screen.getByText('Relatório de Risco de Auditoria Preditivo')).toBeInTheDocument();
    expect(screen.getByText(/Dura Lex analisou continuamente/)).toBeInTheDocument();
  });

  it('calls onClose when close button is clicked', () => {
    renderWithProviders(
      <DuraLexAI open={true} onClose={mockOnClose} />
    );

    const closeButton = screen.getByText('Fechar');
    fireEvent.click(closeButton);

    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });
});