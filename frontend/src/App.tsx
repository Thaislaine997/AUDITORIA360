import React from 'react'
import { Header } from './components/Header'
import { ThemeProvider } from './components/ThemeProvider'

function App() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <h1 className="text-3xl font-bold text-primary-700 mb-6">
            AUDITORIA360
          </h1>
          <p className="text-gray-600 mb-4">
            Portal de Gestão Inteligente para Auditoria Trabalhista
          </p>
        </main>
      </div>
    </ThemeProvider>
  )
}

export default App