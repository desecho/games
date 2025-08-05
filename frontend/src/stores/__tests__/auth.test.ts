import axios from 'axios'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { useAuthStore } from '../auth'

// Mock axios
vi.mock('axios')
const mockedAxios = vi.mocked(axios)

// Mock helpers
vi.mock('../../helpers', () => ({
  getUrl: vi.fn((path: string) => `http://localhost:8000/api/${path}`)
}))

// Mock axios initialization
vi.mock('../../axios', () => ({
  initAxios: vi.fn()
}))

// Mock router
vi.mock('../../router', () => ({
  router: {
    push: vi.fn()
  }
}))

// Mock JWT decode
vi.mock('jwt-decode', () => ({
  jwtDecode: vi.fn().mockReturnValue({ exp: Date.now() / 1000 + 3600 }) // Valid for 1 hour
}))

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    localStorage.clear()
  })

  it('initializes with default user state', () => {
    const authStore = useAuthStore()
    
    expect(authStore.user.isLoggedIn).toBe(false)
    expect(authStore.user.username).toBeUndefined()
    expect(authStore.user.accessToken).toBeUndefined()
    expect(authStore.user.refreshToken).toBeUndefined()
  })

  it('logs in user successfully', async () => {
    const authStore = useAuthStore()
    
    mockedAxios.post.mockResolvedValueOnce({
      data: {
        access: 'access-token',
        refresh: 'refresh-token'
      }
    })

    await authStore.login('testuser', 'password')

    expect(authStore.user.isLoggedIn).toBe(true)
    expect(authStore.user.username).toBe('testuser')
    expect(authStore.user.accessToken).toBe('access-token')
    expect(authStore.user.refreshToken).toBe('refresh-token')
  })

  it('refreshes token successfully', async () => {
    const authStore = useAuthStore()
    
    // Set up logged in user
    authStore.user = {
      isLoggedIn: true,
      username: 'testuser',
      accessToken: 'old-access-token',
      refreshToken: 'refresh-token'
    }

    mockedAxios.post.mockResolvedValueOnce({
      data: {
        access: 'new-access-token'
      }
    })

    await authStore.refreshToken()

    expect(authStore.user.accessToken).toBe('new-access-token')
    expect(authStore.user.refreshToken).toBe('refresh-token') // Should remain the same
  })

  it('logs out user', () => {
    const authStore = useAuthStore()
    
    // Set up logged in user
    authStore.user = {
      isLoggedIn: true,
      username: 'testuser',
      accessToken: 'access-token',
      refreshToken: 'refresh-token'
    }

    authStore.logout()

    expect(authStore.user.isLoggedIn).toBe(false)
    expect(authStore.user.username).toBeUndefined()
    expect(authStore.user.accessToken).toBeUndefined()
    expect(authStore.user.refreshToken).toBeUndefined()
  })
})