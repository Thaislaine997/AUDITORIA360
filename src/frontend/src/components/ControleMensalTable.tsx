// src/frontend/src/components/ControleMensalTable.tsx

import React, { useMemo } from 'react';
import { useReactTable, getCoreRowModel, flexRender, ColumnDef } from '@tanstack/react-table';
import { ControleMensalDetalhado, Tarefa, atualizarStatusTarefa } from '../services/controleMensalService';

// Componente para um único checkbox de tarefa
const TarefaCheckbox = ({ tarefa }: { tarefa?: Tarefa }) => {
    if (!tarefa) return null;

    const handleCheck = async () => {
        // TODO: Adicionar lógica para atualizar o estado local (optimistic update)
        // e depois chamar o serviço da API.
        try {
            await atualizarStatusTarefa(tarefa.id, !tarefa.concluido);
            alert(`Tarefa "${tarefa.nome_tarefa}" atualizada!`);
            // TODO: Recarregar os dados da tabela
        } catch {
            alert(`Falha ao atualizar a tarefa "${tarefa.nome_tarefa}".`);
        }
    };

    return <input type="checkbox" checked={tarefa.concluido} onChange={handleCheck} />;
};

export const ControleMensalTable = ({ data }: { data: ControleMensalDetalhado[] }) => {
  const columns = useMemo<ColumnDef<ControleMensalDetalhado>[]>(
    () => [
      { accessorKey: 'nome_empresa', header: 'Empresa' },
      { accessorKey: 'status_dados', header: 'Status' },
      // Colunas dinâmicas para cada tarefa padrão
      ...['INFO_FOLHA', 'ENVIO_CLIENTE', 'GUIA_FGTS', 'DARF_INSS', 'ESOCIAL_DCTFWEB'].map(nomeTarefa => ({
          id: nomeTarefa,
          header: nomeTarefa.replace('_', ' ').replace('DARF ', ''),
          cell: ({ row }) => {
              const tarefa = row.original.tarefas.find(t => t.nome_tarefa === nomeTarefa);
              return <TarefaCheckbox tarefa={tarefa} />;
          }
      }))
    ],
    []
  );

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <table className="min-w-full bg-white">
      <thead className="bg-gray-200">
        {table.getHeaderGroups().map(headerGroup => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map(header => (
              <th key={header.id} className="py-2 px-4 border-b">{flexRender(header.column.columnDef.header, header.getContext())}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map(row => (
          <tr key={row.id} className="hover:bg-gray-100">
            {row.getVisibleCells().map(cell => (
              <td key={cell.id} className="py-2 px-4 border-b text-center">{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};