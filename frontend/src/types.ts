export interface JWTDecoded {
  token_type: string;
  exp: number;
  iat: number;
  jti: string;
  user_id: number;
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
  isReleased: boolean;
}

export interface RecordType {
  id: number;
  game: Game;
  listKey: string;
  order: number;
}

export interface List {
  id: number;
  name: string;
  key: string;
  icon: string;
}

export interface Switch {
  name: string;
  label: string;
}

export interface GetUserPreferencesData {
  hidden: boolean;
}

export interface TokenErrorData {
  detail: string;
}
