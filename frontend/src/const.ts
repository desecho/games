import type { List, ListKey } from "./types";

export enum LIST_IDS {
  WantToPlay = 1,
  Playing,
  Beaten,
  OnHold,
}

export const LIST_KEYS: Record<number, ListKey> = {};
LIST_KEYS[LIST_IDS.WantToPlay] = "want-to-play";
LIST_KEYS[LIST_IDS.Playing] = "playing";
LIST_KEYS[LIST_IDS.Beaten] = "beaten";
LIST_KEYS[LIST_IDS.OnHold] = "on-hold";

export const LISTS: List[] = [
  {
    id: LIST_IDS.WantToPlay,
    name: "Want to Play",
    key: LIST_KEYS[LIST_IDS.WantToPlay],
    icon: "star",
  },
  {
    id: LIST_IDS.Playing,
    name: "Playing",
    key: LIST_KEYS[LIST_IDS.Playing],
    icon: "controller",
  },
  {
    id: LIST_IDS.Beaten,
    name: "Beaten",
    key: LIST_KEYS[LIST_IDS.Beaten],
    icon: "trophy",
  },
  {
    id: LIST_IDS.OnHold,
    name: "On Hold",
    key: LIST_KEYS[LIST_IDS.OnHold],
    icon: "pause-circle-outline",
  },
];

export const ADMIN_EMAIL = import.meta.env.VITE_ADMIN_EMAIL as string;

export const DLC_KIND_CATEGORIES = ["DLC", "Expansion", "Standalone Expansion"];

export const DEFAULT_LIST = LIST_KEYS[LIST_IDS.WantToPlay];
