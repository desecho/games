import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { useAuthStore } from '../../stores/auth'
import { useGamesStore } from '../../stores/games'
import { useSettingsStore } from '../../stores/settings'
import GameCard from '../GameCard.vue'

// Mock axios
vi.mock('axios')

// Mock composables
vi.mock('../../composables/addToList', () => ({
  useAddToList: () => ({
    addToList: vi.fn().mockResolvedValue(undefined)
  })
}))

// Mock helpers
vi.mock('../../helpers', () => ({
  getUrl: vi.fn((path: string) => `http://localhost:8000/api/${path}`),
  requireAuthenticated: vi.fn()
}))

// Mock toast
vi.mock('../../toast', () => ({
  $toast: {
    error: vi.fn()
  }
}))

const mockRecord = {
  id: 1,
  game: {
    id: 1,
    name: 'Test Game',
    cover: 'test-cover.jpg',
    isReleased: true
  },
  listKey: 'wantToPlay' as const
}

describe('GameCard', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders game card with correct dimensions when actions are visible', () => {
    const authStore = useAuthStore()
    const gamesStore = useGamesStore()
    const settingsStore = useSettingsStore()
    
    // Set up authenticated user
    authStore.user = {
      isLoggedIn: true,
      username: 'testuser',
      accessToken: 'token',
      refreshToken: 'refresh'
    }
    
    // Set up settings to show action buttons
    settingsStore.settings = {
      games: { areActionButtonsHidden: false }
    }
    
    gamesStore.records = []

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'wantToPlay',
        username: 'anotheruser' // Different user to show actions
      }
    })

    expect(wrapper.find('.v-card').attributes('height')).toBe('275')
    expect(wrapper.find('.v-card-actions').exists()).toBe(true)
  })

  it('renders game card with smaller height when actions are hidden', () => {
    const authStore = useAuthStore()
    const settingsStore = useSettingsStore()
    
    // Set up authenticated user but hide actions
    authStore.user = {
      isLoggedIn: true,
      username: 'testuser',
      accessToken: 'token',
      refreshToken: 'refresh'
    }
    
    settingsStore.settings = {
      games: { areActionButtonsHidden: true }
    }

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'wantToPlay',
        username: 'anotheruser'
      }
    })

    expect(wrapper.find('.v-card').attributes('height')).toBe('224')
    expect(wrapper.find('.v-card-actions').exists()).toBe(false)
  })

  it('does not show actions on own profile', () => {
    const authStore = useAuthStore()
    const settingsStore = useSettingsStore()
    
    authStore.user = {
      isLoggedIn: true,
      username: 'testuser',
      accessToken: 'token',
      refreshToken: 'refresh'
    }
    
    settingsStore.settings = {
      games: { areActionButtonsHidden: false }
    }

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'wantToPlay',
        username: 'testuser' // Same user
      }
    })

    expect(wrapper.find('.v-card-actions').exists()).toBe(false)
  })

  it('does not show actions when user is not logged in', () => {
    const authStore = useAuthStore()
    
    authStore.user = {
      isLoggedIn: false
    }

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'wantToPlay'
      }
    })

    expect(wrapper.find('.v-card-actions').exists()).toBe(false)
  })
})