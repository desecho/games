export interface UserStore {
  isLoggedIn: boolean;
  refreshToken?: string;
  accessToken?: string;
  username?: string;
}

export interface GamesSettings {
  areActionButtonsHidden: boolean;
}

export interface SettingsStore {
  games: GamesSettings;
}
