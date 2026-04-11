import { flushPromises, mount } from '@vue/test-utils'
import axios from 'axios'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { useAuthStore } from '../../stores/auth'
import { useGamesStore } from '../../stores/games'
import { useSettingsStore } from '../../stores/settings'
import { $toast } from '../../toast'
import GameCard from '../GameCard.vue'

// Mock axios
vi.mock('axios')
const mockedAxios = vi.mocked(axios, true)

// Mock composables
vi.mock('../../composables/addToList', () => ({
  useAddToList: (): { addToList: () => Promise<void> } => ({
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
    category: 'main_game',
    isReleased: true
  },
  listKey: 'want-to-play' as const,
  order: 0,
  rating: 3
}

function authenticateUser(username = 'testuser'): void {
  const authStore = useAuthStore()
  authStore.user = {
    isLoggedIn: true,
    username,
    accessToken: 'token',
    refreshToken: 'refresh'
  }
}

function setGameSettings(areActionButtonsHidden = false, areRatingsHidden = false): void {
  const settingsStore = useSettingsStore()
  settingsStore.settings = {
    games: { areActionButtonsHidden, areRatingsHidden, areUnreleasedGamesHidden: false, areDLCsHidden: false },
    isGamesSettingsActive: false,
    darkMode: false
  }
}

describe('GameCard', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    vi.spyOn(console, 'log').mockImplementation(() => undefined)
  })

  it('renders game card with correct dimensions when actions are visible', () => {
    const gamesStore = useGamesStore()
    authenticateUser()
    setGameSettings()
    gamesStore.records = []

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'want-to-play',
        username: 'anotheruser' // Different user to show actions
      }
    })

    expect(wrapper.find('.v-card').attributes('height')).toBe('275')
    expect(wrapper.find('.v-card-actions').exists()).toBe(true)
    expect(wrapper.find('.v-rating').attributes('data-readonly')).toBe('true')
    expect(wrapper.find('.game-card-poster > .game-card-rating').exists()).toBe(true)
  })

  it('renders game card with smaller height when actions are hidden', () => {
    authenticateUser()
    setGameSettings(true)

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'want-to-play',
        username: 'anotheruser'
      }
    })

    expect(wrapper.find('.v-card').attributes('height')).toBe('224')
    expect(wrapper.find('.v-card-actions').exists()).toBe(false)
  })

  it('does not show actions on own profile', () => {
    authenticateUser()
    setGameSettings()

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'want-to-play',
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
        listKey: 'want-to-play'
      }
    })

    expect(wrapper.find('.v-card-actions').exists()).toBe(false)
  })

  it('renders an editable rating for owned records', () => {
    authenticateUser()
    setGameSettings()

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'want-to-play'
      }
    })

    expect(wrapper.find('.v-rating').attributes('data-model-value')).toBe('3')
    expect(wrapper.find('.v-rating').attributes('data-readonly')).toBe('false')
    expect(wrapper.find('.v-rating').attributes('data-clearable')).toBe('true')
  })

  it('hides the rating when ratings are hidden in settings', () => {
    authenticateUser()
    setGameSettings(false, true)

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'want-to-play'
      }
    })

    expect(wrapper.find('.game-card-rating').exists()).toBe(false)
    expect(wrapper.find('.v-rating').exists()).toBe(false)
  })

  it('updates a rating successfully', async () => {
    authenticateUser()
    setGameSettings()
    mockedAxios.put.mockResolvedValueOnce({})

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'want-to-play'
      }
    })

    await wrapper.find('.v-rating').trigger('click')
    await flushPromises()

    expect(mockedAxios.put).toHaveBeenCalledWith(
      'http://localhost:8000/api/records/1/rating/',
      { rating: 5 }
    )
    expect(wrapper.find('.v-rating').attributes('data-model-value')).toBe('5')
    expect(wrapper.emitted('updateRating')).toEqual([[1, 5]])
  })

  it('reverts the rating when the update fails', async () => {
    authenticateUser()
    setGameSettings()
    mockedAxios.put.mockRejectedValueOnce(new Error('failed'))

    const wrapper = mount(GameCard, {
      props: {
        record: mockRecord,
        index: 0,
        listKey: 'want-to-play'
      }
    })

    await wrapper.find('.v-rating').trigger('click')
    await flushPromises()

    expect(wrapper.find('.v-rating').attributes('data-model-value')).toBe('3')
    expect($toast.error).toHaveBeenCalledWith('Error updating rating')
    expect(wrapper.emitted('updateRating')).toBeUndefined()
  })
})
