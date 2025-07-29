import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { useAuth } from '../../hooks/useAuth'

// Mock authService
vi.mock('../../modules/auth/authService', () => ({
  authService: {
    isAuthenticated: vi.fn(),
    getCurrentUser: vi.fn(),
  },
}))

import { authService } from '../../modules/auth/authService'

const mockAuthService = authService as vi.Mocked<typeof authService>

describe('useAuth Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('returns initial loading state and completes auth check', async () => {
    mockAuthService.isAuthenticated.mockReturnValue(false)
    mockAuthService.getCurrentUser.mockReturnValue(null)

    const { result } = renderHook(() => useAuth())

    // The hook should eventually settle to not loading
    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.isAuthenticated).toBe(false)
  })

  it('returns authenticated state when user is logged in', async () => {
    const mockUser = {
      id: '1',
      name: 'Test User',
      email: 'test@example.com',
      role: 'admin' as const,
    }

    mockAuthService.isAuthenticated.mockReturnValue(true)
    mockAuthService.getCurrentUser.mockReturnValue(mockUser)

    const { result } = renderHook(() => useAuth())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.isAuthenticated).toBe(true)
    expect(result.current.user).toEqual(mockUser)
  })

  it('returns unauthenticated state when user is not logged in', async () => {
    mockAuthService.isAuthenticated.mockReturnValue(false)
    mockAuthService.getCurrentUser.mockReturnValue(null)

    const { result } = renderHook(() => useAuth())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.isAuthenticated).toBe(false)
    expect(result.current.user).toBeUndefined()
  })

  it('handles auth check errors gracefully', async () => {
    mockAuthService.isAuthenticated.mockImplementation(() => {
      throw new Error('Auth check failed')
    })

    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

    const { result } = renderHook(() => useAuth())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.isAuthenticated).toBe(false)
    expect(consoleSpy).toHaveBeenCalledWith('Auth check failed:', expect.any(Error))

    consoleSpy.mockRestore()
  })
})