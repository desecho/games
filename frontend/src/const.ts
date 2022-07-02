export enum ListIds {
  WantToPlay = 1,
  Playing,
  Beaten,
  OnHold,
}

export const ListKeys: Record<number, string> = {};
ListKeys[ListIds.WantToPlay] = "want-to-play";
ListKeys[ListIds.Playing] = "playing";
ListKeys[ListIds.Beaten] = "beaten";
ListKeys[ListIds.OnHold] = "on-hold";

export const Lists = [
  {
    id: ListIds.WantToPlay,
    name: "Want to Play",
    key: ListKeys[ListIds.WantToPlay],
    icon: "star",
  },
  {
    id: ListIds.Playing,
    name: "Playing",
    key: ListKeys[ListIds.Playing],
    icon: "google-controller",
  },
  {
    id: ListIds.Beaten,
    name: "Beaten",
    key: ListKeys[ListIds.Beaten],
    icon: "trophy",
  },
  {
    id: ListIds.OnHold,
    name: "On Hold",
    key: ListKeys[ListIds.OnHold],
    icon: "pause-circle-outline",
  },
];
