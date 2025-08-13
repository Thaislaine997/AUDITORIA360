import React from 'react'
import Button from './Button'

export default function Header() {
  return (
    <header className="flex items-center justify-between p-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-primary-500" />
        <h1 className="text-lg font-semibold">Auditoria360</h1>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="ghost">Ajuda</Button>
        <Button>Exportar</Button>
      </div>
    </header>
  )
}
