import type { List } from "./types";

export enum ListIDs {
  WantToPlay = 1,
  Playing,
  Beaten,
  OnHold,
}

export const ListKeys: Record<number, string> = {};
ListKeys[ListIDs.WantToPlay] = "want-to-play";
ListKeys[ListIDs.Playing] = "playing";
ListKeys[ListIDs.Beaten] = "beaten";
ListKeys[ListIDs.OnHold] = "on-hold";

export const Lists: List[] = [
  {
    id: ListIDs.WantToPlay,
    name: "Want to Play",
    key: ListKeys[ListIDs.WantToPlay],
    icon: "star",
  },
  {
    id: ListIDs.Playing,
    name: "Playing",
    key: ListKeys[ListIDs.Playing],
    icon: "controller",
  },
  {
    id: ListIDs.Beaten,
    name: "Beaten",
    key: ListKeys[ListIDs.Beaten],
    icon: "trophy",
  },
  {
    id: ListIDs.OnHold,
    name: "On Hold",
    key: ListKeys[ListIDs.OnHold],
    icon: "pause-circle-outline",
  },
];

export const Email = import.meta.env.VITE_ADMIN_EMAIL as string;

export const DLCKindCategories = ["DLC", "Expansion", "Standalone Expansion"];

export const DefaultList = ListKeys[ListIDs.WantToPlay];
