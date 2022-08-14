export type ListKey = "beaten" | "on-hold" | "playing" | "want-to-play";

export interface JWTDecoded {
  token_type: string;
  exp: number;
  iat: number;
  jti: string;
  user_id: number;
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
  listKey: ListKey;
  order: number;
}

export interface List {
  id: number;
  name: string;
  key: ListKey;
  icon: string;
}
