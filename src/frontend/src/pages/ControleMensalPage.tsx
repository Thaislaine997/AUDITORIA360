// src/frontend/src/pages/ControleMensalPage.tsx

import React, { useState, useEffect } from 'react';
import { getControlesDoMes, ControleMensalDetalhado } from '../services/controleMensalService';
// Vamos criar este componente a seguir
import { ControleMensalTable } from '../components/ControleMensalTable';

export const ControleMensalPage: React.FC = () => {
  const [controles, setControles] = useState<ControleMensalDetalhado[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Lógica para selecionar o mês/ano
  const [date, setDate] = useState({ month: new Date().getMonth() + 1, year: new Date().getFullYear() });

  useEffect(() => {
    const fetchControles = async () => {
      try {
        setLoading(true);
        const data = await getControlesDoMes(date.year, date.month);
        setControles(data);
        setError(null);
      } catch (err) {
        setError('Falha ao carregar os dados de controle.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchControles();
  }, [date]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Controle de Folha Mensal</h1>

      {/* TODO: Adicionar seletores de mês e ano aqui para atualizar o estado 'date' */}

      {loading && <p>A carregar...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {!loading && !error && <ControleMensalTable data={controles} />}
    </div>
  );
};