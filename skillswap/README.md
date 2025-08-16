# SkillSwap

SkillSwap is a geolocation-based platform to connect people who **have** hard trade skills with people who **want to learn**. Think: electrical work, carpentry, hunting, welding, etc.

This repo includes:
- **backend/** – FastAPI + PostgreSQL (PostGIS) + SQLAlchemy + Redis + WebSockets
- **web/** – Simple server-rendered web (Jinja2 + HTMX) hosted by FastAPI for quick iteration
- **ios/** – BeeWare (Toga) Python iOS client scaffold consuming the same API

## Features (MVP)
- User registration/login (JWT)
- Profiles with skills and bio
- Discover mentors/learners near you (radius search)
- Ratings & reviews
- Real-time 1:1 messaging via WebSockets
- Basic web UI for browsing, login, messaging
- iOS app scaffold (Toga) with a simple "nearby mentors" list

> **Note**: This is a scaffold intended to help you start collaborating. It’s intentionally minimal, with clear `TODO:` markers.

---

## Quick Start (Docker)
Requirements: Docker + Docker Compose

```bash
cp .env.example .env
# edit .env if desired
docker-compose up --build
```

Services:
- API: http://localhost:8000 (docs at http://localhost:8000/docs)
- Web UI: http://localhost:8000
- Postgres (PostGIS): localhost:5432
- Redis: localhost:6379

Create DB tables & seed:
```bash
docker-compose exec api alembic upgrade head
```

---

## Local Dev (without Docker)
Create a Python 3.10+ virtual env and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
export $(grep -v '^#' .env | xargs)  # or use a dotenv loader
uvicorn backend.app.main:app --reload
```

Run migrations:
```bash
alembic -c backend/alembic.ini upgrade head
```

---

## iOS App (BeeWare Toga)
1. Install Briefcase: `pip install briefcase`
2. `cd ios/skillswap_ios`
3. `briefcase dev` to run a desktop view; for iOS, see BeeWare docs to build and run on a device/simulator.

---

## Project Structure
```
skillswap/
  backend/
  web/               # HTML templates + static
  ios/
  docker-compose.yml
  .env.example
```

---

## Environment Variables
Copy `.env.example` to `.env`, then adjust:
- `DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/skillswap`
- `REDIS_URL=redis://redis:6379/0`
- `SECRET_KEY=change-me`
- `JWT_EXPIRES=3600`
- `MAP_DEFAULT_LAT=41.8781`  # Chicago by default
- `MAP_DEFAULT_LON=-87.6298`
- `DEBUG=true`
```

## License
MIT (placeholder). Update for your needs.
