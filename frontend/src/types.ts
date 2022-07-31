export interface UserStore {
  isLoggedIn: boolean;
  refreshToken?: string;
  accessToken?: string;
}

export interface JWTDecoded {
  token_type: string;
  exp: number;
  iat: number;
  jti: string;
  user_id: number;
}

export interface GameSearchResult {
  id: number;
  name: string;
  cover: string;
  category: string;
}

export interface SearchViewComponentData {
  games: GameSearchResult[];
  valid: boolean;
  rules: { required: any }; // eslint-disable-line @typescript-eslint/no-explicit-any
  query: string;
}

export interface UsersViewComponentData {
  users: string[];
}

export interface SortData {
  id: number;
  order: number;
}

export interface Game {
  id: number;
  name: string;
  cover: string | null;
  category: string;
}

export interface RecordType {
  id: number;
  game: Game;
  listKey: string;
  order: number;
}
