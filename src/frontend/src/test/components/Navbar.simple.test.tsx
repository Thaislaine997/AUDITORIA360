import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import Navbar from '../../components/Navbar'

const theme = createTheme()

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  )
}

describe('Navbar Component - Basic Tests', () => {
  it('renders without crashing', () => {
    renderWithTheme(<Navbar />)
    expect(document.body).toBeInTheDocument()
  })

  it('contains the main title text', () => {
    renderWithTheme(<Navbar />)
    expect(screen.getByText(/AUDITORIA360/)).toBeInTheDocument()
  })

  it('contains portal text', () => {
    renderWithTheme(<Navbar />)
    expect(screen.getByText(/Portal de Gestão da Folha/)).toBeInTheDocument()
  })
})