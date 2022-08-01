export interface UserStore {
  isLoggedIn: boolean;
  refreshToken?: string;
  accessToken?: string;
  username?: string;
}

export interface GamesSettings {
  areActionButtonsHidden: boolean;
  areUnreleasedGamesHidden: boolean;
}

export interface SettingsStore {
  games: GamesSettings;
}
