import React from 'react'

export default function Table({ columns, data }: { columns: string[]; data: any[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-left text-sm">
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={c} className="px-3 py-2 text-gray-600">
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="border-t even:bg-gray-50">
              {columns.map((c) => (
                <td key={c} className="px-3 py-2">
                  {row[c]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
