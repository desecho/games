# Games iOS App

Native SwiftUI iOS client for the Games backend.

## Requirements

- Xcode 15 or newer
- iOS 17.0 or newer
- Games backend running locally for debug builds

## Backend URLs

- Debug: `http://127.0.0.1:8000`
- Release: `https://api.games.samarchyan.me`

## Features

- JWT username/password login
- Persisted login state
- Logout
- Four game list tabs: Want to Play, Playing, Beaten, On Hold
- Search games
- Add games to a list
- Move records between lists
- Delete records
- Edit ratings from 0 to 5

Registration, password reset, and password change are intentionally not included.
