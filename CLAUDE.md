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

### Initial Setup
```bash
make bootstrap          # Complete project setup (deps, DB, migrations, build)
make createsuperuser   # Create Django admin user
```

### Development
```bash
make run               # Start Django backend (localhost:8000)
make dev               # Start Vue.js frontend (localhost:5173)
```

Both commands need to run simultaneously for full development.

### Database
```bash
make create-db         # Create database
make migrate           # Run Django migrations
make drop-db           # Drop database
make load-db           # Load from backup
```

### Python Backend
```bash
make manage [command]  # Run Django management commands
make shell             # Django shell
```

### Frontend
```bash
make build             # Build frontend for production
make yarn-install      # Install/update npm dependencies
make serve             # Serve built frontend
```

### Testing & Linting
```bash
make test              # Run all tests and linters
make tox               # Run Python tests via tox
make pytest            # Run Python unit tests only
make eslint            # Run frontend linting
```

### Formatting
```bash
make format-all        # Format all code (Python, Vue, TS, etc.)
make format            # Format Python code only  
make format-frontend   # Format frontend code only
```

### Docker
```bash
make docker-build-dev  # Build development Docker images
make docker-run        # Run in Docker containers
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

### Environment Setup
- Copy template files: `env_custom.sh.tpl` → `env_custom.sh`, `env_secrets.sh.tpl` → `env_secrets.sh`
- Configure MySQL and Redis via Docker (see README.rst)
- Edit environment files with proper credentials

### Testing Framework
- Backend: pytest with Django test client
- Frontend: No test framework currently configured
- Extensive linting via tox (pylint, flake8, mypy, black, etc.)

### API Integration
- IGDB API used for game data via `update_games_data` management command
- Rate limiting and error handling implemented for API calls

### Development Workflow
1. Use `make bootstrap` for initial setup
2. Run `make run` and `make dev` in separate terminals
3. Use `make format-all` before committing
4. Run `make test` to verify changes

### Production Deployment
- Kubernetes deployment configs in `deployment/`
- Production commands prefixed with `prod-` in Makefile
- Docker images built for both backend and frontend