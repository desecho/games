# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a full-stack web application for creating and managing game lists (e.g., "Want to Play", "Playing", "Beaten", "On Hold").

**Backend:** Django 5.2+ REST API with Django REST Framework
- Main app: `src/games/` - contains models, views, management commands
- Project configuration: `src/games_project/` - Django settings and URL routing
- Database: MySQL with Django ORM
- External API integration: IGDB API for game data via `src/games/igdb/`
- Authentication: JWT-based with Django REST registration

**Frontend:** Vue.js 3 + Vuetify 3 + TypeScript
- Location: `frontend/` directory
- UI Framework: Vuetify 3 (Material Design)
- State Management: Pinia stores in `frontend/src/stores/`
- Build Tool: Vite
- Package Manager: Yarn

**Key Data Flow:**
- Game data fetched from IGDB API via management commands
- Users create lists and add/remove games via REST API
- Frontend consumes API and manages state via Pinia stores

## Essential Development Commands

### Frontend
```bash
make build             # Build frontend for production
```

### Testing & Linting
```bash
make pytest            # Run Python unit tests only
make eslint            # Run frontend linting
```

### Formatting
```bash
make format            # Format Python code only
make format-frontend   # Format frontend code only
```

### Python Linting (Individual Tools)
```bash
make pylint            # Python linting
make mypy              # Type checking
```

## Code Organization

### Backend Structure
- `src/games/models.py` - Core models (Game, User, List, Record, Category)
- `src/games/views/` - API endpoints organized by functionality
- `src/games/management/commands/` - CLI commands for data management
- `src/games/igdb/` - IGDB API integration
- `src/games/fixtures/` - Initial data (categories, lists)

### Frontend Structure
- `frontend/src/components/` - Reusable Vue components
- `frontend/src/views/` - Page-level components
- `frontend/src/stores/` - Pinia state management (auth, games, settings)
- `frontend/src/composables/` - Vue composables for shared logic
- `frontend/src/types.ts` - TypeScript type definitions

### Key Frontend Components
- `GameCard.vue` - Individual game display
- `GamesList.vue` - Game list display
- `GamesView.vue` - Main games page
- `GamesUserBar.vue` - User navigation bar

## Important Notes

### Testing Framework
- Backend: pytest with Django test client
- Frontend: No test framework currently configured
- Extensive linting via tox (pylint, flake8, mypy, black, etc.)

### API Integration
- IGDB API used for game data via `update_games_data` management command
- Rate limiting and error handling implemented for API calls

## Additional instructions

- Always run backend tests with `make test-python` command
- Always run frontend tests with `make eslint` command
- Before running tests and after you complete the coding - always run `make format` for backend changes and `make format-frontend` for frontend changes
