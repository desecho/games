export interface UserStore {
  isLoggedIn: boolean;
  refreshToken?: string;
  accessToken?: string;
  username?: string;
}

export type GamesMode = "list" | "gallery";

export interface GamesSettings {
  areActionButtonsHidden: boolean;
  areUnreleasedGamesHidden: boolean;
  areDLCsHidden: boolean;
  mode: GamesMode;
}

export interface SettingsStore {
  games: GamesSettings;
  isGamesSettingsActive: boolean;
}

export interface TokenData {
  refresh: string;
  access: string;
}

export interface TokenRefreshData {
  access: string;
}
