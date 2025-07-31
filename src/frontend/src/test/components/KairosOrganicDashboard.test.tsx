import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { createTheme } from '@mui/material';
import KairosOrganicDashboard from '../../components/kairos/KairosOrganicDashboard';

// Mock Three.js completely to avoid 3D rendering issues in tests
vi.mock('@react-three/fiber', () => ({
  Canvas: ({ children, ...props }: any) => <div data-testid="canvas" {...props}>{children}</div>,
  useFrame: vi.fn(),
}));

vi.mock('@react-three/drei', () => ({
  OrbitControls: () => <div data-testid="orbit-controls" />,
  Text: ({ children, ...props }: any) => <div data-testid="text-element" {...props}>{children}</div>,
}));

// Mock THREE.js objects
vi.mock('three', () => ({
  Color: vi.fn().mockImplementation(() => ({
    setHSL: vi.fn().mockReturnThis(),
  })),
  Mesh: vi.fn(),
  Object3D: vi.fn(),
}));

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

describe('KairosOrganicDashboard', () => {
  const mockOnBackToTraditional = vi.fn();

  beforeEach(() => {
    mockOnBackToTraditional.mockClear();
    // Mock useEffect to prevent animation loops during testing
    vi.spyOn(React, 'useEffect').mockImplementation((effect, deps) => {
      if (deps && deps.length === 0) {
        // Don't run effects that set up intervals
        return;
      }
      effect();
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders the Kairós dashboard header', () => {
    renderWithProviders(
      <KairosOrganicDashboard onBackToTraditional={mockOnBackToTraditional} />
    );

    expect(screen.getByText('🌱 KAIRÓS - Bioma Operacional')).toBeInTheDocument();
    expect(screen.getByText('Voltar ao Dashboard Tradicional')).toBeInTheDocument();
  });

  it('calls onBackToTraditional when back button is clicked', () => {
    renderWithProviders(
      <KairosOrganicDashboard onBackToTraditional={mockOnBackToTraditional} />
    );

    const backButton = screen.getByText('Voltar ao Dashboard Tradicional');
    fireEvent.click(backButton);

    expect(mockOnBackToTraditional).toHaveBeenCalledTimes(1);
  });

  it('displays Dura Lex AI button', () => {
    renderWithProviders(
      <KairosOrganicDashboard onBackToTraditional={mockOnBackToTraditional} />
    );

    const duraLexButton = screen.getByLabelText('Dura Lex - Consciência Jurídica');
    expect(duraLexButton).toBeInTheDocument();
  });
});