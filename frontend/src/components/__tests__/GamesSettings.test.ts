import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'

import { useAuthStore } from '../../stores/auth'
import { useSettingsStore } from '../../stores/settings'
import GamesSettings from '../GamesSettings.vue'

function authenticateUser(username = 'testuser'): void {
  const authStore = useAuthStore()
  authStore.user = {
    isLoggedIn: true,
    username,
    accessToken: 'token',
    refreshToken: 'refresh'
  }
}

const global = {
  stubs: {
    VSheet: { template: '<div class="v-sheet"><slot /></div>' },
    VRow: { template: '<div class="v-row"><slot /></div>' },
    SettingsSwitch: {
      template: '<div class="settings-switch" :data-name="name">{{ label }}</div>',
      props: ['type', 'name', 'label']
    }
  }
}

describe('GamesSettings', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    const settingsStore = useSettingsStore()
    settingsStore.settings.isGamesSettingsActive = true
  })

  it('shows hide ratings alongside hide action buttons for signed-in users', () => {
    authenticateUser()

    const wrapper = mount(GamesSettings, {
      global
    })

    expect(wrapper.find('[data-name="areActionButtonsHidden"]').text()).toBe('Hide action buttons')
    expect(wrapper.find('[data-name="areRatingsHidden"]').text()).toBe('Hide ratings')
  })

  it('hides controls switches on the signed-in user profile', () => {
    authenticateUser()

    const wrapper = mount(GamesSettings, {
      props: {
        username: 'testuser'
      },
      global
    })

    expect(wrapper.find('[data-name="areActionButtonsHidden"]').exists()).toBe(false)
    expect(wrapper.find('[data-name="areRatingsHidden"]').exists()).toBe(false)
  })
})
