// src/frontend/src/components/ControleMensalTable.tsx

import React, { useMemo, useState } from 'react';
import { useReactTable, getCoreRowModel, flexRender, ColumnDef } from '@tanstack/react-table';
import { ControleMensalDetalhado, Tarefa, atualizarStatusTarefa } from '../services/controleMensalService';

interface TarefaCheckboxProps {
  tarefa?: Tarefa;
  onUpdate?: (tarefaId: number, concluido: boolean) => void;
}

// Componente para um único checkbox de tarefa
const TarefaCheckbox = ({ tarefa, onUpdate }: TarefaCheckboxProps) => {
    if (!tarefa) return <span className="text-gray-400">-</span>;

    const handleCheck = async () => {
        try {
          // Optimistic update - update UI immediately
          if (onUpdate) {
            onUpdate(tarefa.id, !tarefa.concluido);
          }
          
          // Then try to update via API
          await atualizarStatusTarefa(tarefa.id, !tarefa.concluido);
          console.log(`Tarefa "${tarefa.nome_tarefa}" atualizada com sucesso!`);
        } catch (error) {
          console.error(`Falha ao atualizar a tarefa "${tarefa.nome_tarefa}":`, error);
          // Revert optimistic update on error
          if (onUpdate) {
            onUpdate(tarefa.id, tarefa.concluido);
          }
        }
    };

    return (
      <div className="flex justify-center">
        <input 
          type="checkbox" 
          checked={tarefa.concluido} 
          onChange={handleCheck}
          className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
        />
      </div>
    );
};

export const ControleMensalTable = ({ data }: { data: ControleMensalDetalhado[] }) => {
  const [localData, setLocalData] = useState(data);

  // Update local data when props change
  React.useEffect(() => {
    setLocalData(data);
  }, [data]);

  // Handler for optimistic updates
  const handleTarefaUpdate = (tarefaId: number, newConcluido: boolean) => {
    setLocalData(prevData => 
      prevData.map(controle => ({
        ...controle,
        tarefas: controle.tarefas.map(tarefa => 
          tarefa.id === tarefaId 
            ? { ...tarefa, concluido: newConcluido }
            : tarefa
        )
      }))
    );
  };

  const columns = useMemo<ColumnDef<ControleMensalDetalhado>[]>(
    () => [
      { 
        accessorKey: 'nome_empresa', 
        header: 'Empresa',
        cell: ({ row }) => (
          <div className="font-medium text-gray-900">{row.original.nome_empresa}</div>
        )
      },
      { 
        accessorKey: 'status_dados', 
        header: 'Status',
        cell: ({ row }) => {
          const status = row.original.status_dados;
          const statusColors = {
            'CONCLUÍDO': 'bg-green-100 text-green-800',
            'EM ANDAMENTO': 'bg-yellow-100 text-yellow-800',
            'AGUARD. DADOS': 'bg-red-100 text-red-800'
          };
          const colorClass = statusColors[status as keyof typeof statusColors] || 'bg-gray-100 text-gray-800';
          
          return (
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${colorClass}`}>
              {status}
            </span>
          );
        }
      },
      // Colunas dinâmicas para cada tarefa padrão
      ...['INFO_FOLHA', 'ENVIO_CLIENTE', 'GUIA_FGTS', 'DARF_INSS', 'ESOCIAL_DCTFWEB'].map(nomeTarefa => ({
          id: nomeTarefa,
          header: nomeTarefa.replace(/_/g, ' ').replace('DARF ', 'DARF ').replace('ESOCIAL', 'eSocial'),
          cell: ({ row }: any) => {
              const tarefa = row.original.tarefas.find((t: Tarefa) => t.nome_tarefa === nomeTarefa);
              return <TarefaCheckbox tarefa={tarefa} onUpdate={handleTarefaUpdate} />;
          }
      }))
    ],
    [localData]
  );

  const table = useReactTable({
    data: localData,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="overflow-x-auto shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
      <table className="min-w-full divide-y divide-gray-300">
        <thead className="bg-gray-50">
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th 
                  key={header.id} 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {table.getRowModel().rows.map(row => (
            <tr key={row.id} className="hover:bg-gray-50">
              {row.getVisibleCells().map(cell => (
                <td key={cell.id} className="px-6 py-4 whitespace-nowrap text-sm">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};