import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import Dashboard from '../../pages/Dashboard'

const theme = createTheme()

// Mock dashboard service
vi.mock('../../modules/dashboard/dashboardService', () => ({
  dashboardService: {
    getMetrics: vi.fn(),
    getTrendIcon: vi.fn(),
  },
}))

import { dashboardService } from '../../modules/dashboard/dashboardService'

const mockDashboardService = dashboardService as vi.Mocked<typeof dashboardService>

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  )
}

describe('Dashboard Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockDashboardService.getTrendIcon.mockReturnValue('↗️')
  })

  it('renders dashboard container', async () => {
    mockDashboardService.getMetrics.mockResolvedValue([])

    renderWithTheme(<Dashboard />)

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    })

    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    mockDashboardService.getMetrics.mockImplementation(() => 
      new Promise(() => {}) // Never resolves to keep loading state
    )

    renderWithTheme(<Dashboard />)

    expect(screen.getByRole('progressbar')).toBeInTheDocument()
    expect(screen.getByText('Carregando dashboard...')).toBeInTheDocument()
  })

  it('renders metrics after loading', async () => {
    const mockMetrics = [
      {
        id: '1',
        title: 'Test Metric',
        value: '100',
        type: 'success' as const,
      },
    ]

    mockDashboardService.getMetrics.mockResolvedValue(mockMetrics)

    renderWithTheme(<Dashboard />)

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    })

    expect(screen.getByText('Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Test Metric')).toBeInTheDocument()
    expect(screen.getByText('100')).toBeInTheDocument()
  })

  it('handles error state gracefully', async () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    
    mockDashboardService.getMetrics.mockRejectedValue(new Error('Failed to load metrics'))

    renderWithTheme(<Dashboard />)

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    })

    expect(consoleSpy).toHaveBeenCalledWith('Error loading dashboard metrics:', expect.any(Error))

    consoleSpy.mockRestore()
  })

  it('displays metrics with trends correctly', async () => {
    const mockMetrics = [
      {
        id: '1',
        title: 'Test Metric',
        value: '100',
        type: 'success' as const,
        trend: {
          value: 15,
          direction: 'up' as const,
        },
      },
    ]

    mockDashboardService.getMetrics.mockResolvedValue(mockMetrics)

    renderWithTheme(<Dashboard />)

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    })

    expect(screen.getByText('Test Metric')).toBeInTheDocument()
    expect(mockDashboardService.getTrendIcon).toHaveBeenCalledWith('up')
  })
})