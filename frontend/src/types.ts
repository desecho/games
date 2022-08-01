export interface JWTDecoded {
  token_type: string;
  exp: number;
  iat: number;
  jti: string;
  user_id: number;
}

export interface SearchViewComponentData {
  games: Game[];
  valid: boolean;
  rules: { required: any }; // eslint-disable-line @typescript-eslint/no-explicit-any
  query: string;
}

export interface UsersViewComponentData {
  users: string[];
}

export interface UserPreferencesViewComponentData {
  hidden: boolean;
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
