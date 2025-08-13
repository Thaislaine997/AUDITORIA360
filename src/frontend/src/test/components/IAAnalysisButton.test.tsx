import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { IAAnalysisButton } from '../../components/IAAnalysisButton';
import { jest } from '@jest/globals';

// Mock fetch global
beforeEach(() => {
  global.fetch = jest.fn((url, opts) => {
    if (url?.toString().includes('/api/ia/analyze')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ result: 'Sugestão IA: Teste de integração.' })
      });
    }
    if (url?.toString().includes('/api/tarefas')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true }) });
    }
    if (url?.toString().includes('/api/notificacoes')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true }) });
    }
    if (url?.toString().includes('/api/auditorias')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true }) });
    }
    if (url?.toString().includes('/api/relatorios')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true }) });
    }
    return Promise.reject(new Error('Unknown endpoint'));
  }) as any;
});

afterEach(() => {
  jest.resetAllMocks();
});

describe('IAAnalysisButton', () => {
  it('deve exibir e acionar todos os botões IA-driven', async () => {
    render(<IAAnalysisButton context="Teste contexto IA" />);
    fireEvent.click(screen.getByText('Analisar com IA'));
    await waitFor(() => screen.getByText(/Sugestão IA:/));
    // Botões de ação
    expect(screen.getByText('Criar tarefa sugerida')).toBeInTheDocument();
    expect(screen.getByText('Criar notificação sugerida')).toBeInTheDocument();
    expect(screen.getByText('Criar auditoria sugerida')).toBeInTheDocument();
    expect(screen.getByText('Criar relatório sugerido')).toBeInTheDocument();
    // Testar clique em cada botão
    fireEvent.click(screen.getByText('Criar tarefa sugerida'));
    await waitFor(() => screen.getByText('Tarefa criada com sucesso!'));
    fireEvent.click(screen.getByText('Criar notificação sugerida'));
    await waitFor(() => screen.getByText('Notificação criada com sucesso!'));
    fireEvent.click(screen.getByText('Criar auditoria sugerida'));
    await waitFor(() => screen.getByText('Auditoria criada com sucesso!'));
    fireEvent.click(screen.getByText('Criar relatório sugerido'));
    await waitFor(() => screen.getByText('Relatório criado com sucesso!'));
  });
});
