# Copilot instructions for depot-commun

Quick, actionable notes to help AI coding agents be productive in this repository.

1) Big-picture architecture
  - Backend: Django (project `depotcommun`) — standard manage.py entry, custom `UserProfile` model in `depotcommun/models.py`, site served through `depotcommun.urls`. Templates and static paths point at a built frontend in `buying-frontend/build`.
  - API: django-ninja is used (see `depotcommun/api.py`). API base path is mounted at `/api/` in `depotcommun/urls.py`.
  - Frontends: Two separate frontend apps live under `frontend/` (React + Vite) and `frontend-solid/` (Solid + Vite). The React app is at `frontend/depot-app` and has its own `package.json` and Vite scripts.
  - Deployment: Heroku-oriented files exist (`Procfile`, `django_heroku` usage in `depotcommun/settings_heroku.py`). Top-level `package.json` contains a `heroku-prebuild` script referencing `buying-frontend`.

2) How to run locally (developer workflows)
  - Backend quick start (PowerShell):
    - Create env: use `pipenv` if preferred (Pipfile exists) or `python -m venv .venv` + `pip install -r requirements.txt`.
    - Ensure a `.env` file is present (settings read environment vars via `environ.Env`).
    - Run migrations and server: `python manage.py migrate` then `python manage.py runserver`.
    - Run tests: `python manage.py test` (Django test runner).
  - Frontend (React Vite) dev server:
    - cd into `frontend/depot-app`
    - `npm install` then `npm run dev` (serves via Vite; default port is 5173 as CORS suggests).
  - Frontend (Solid) dev server:
    - cd into `frontend-solid/depot-app`
    - `npm install` then `npm run dev` (similar Vite project).

3) Important integration/config notes & gotchas
  - The Django settings expect a built frontend at `buying-frontend/build` (see `TEMPLATES['DIRS']` and `STATICFILES_DIRS`). Current frontends use `frontend/*/depot-app` — update build paths or adjust settings if you add a new frontend build step.
  - Heroku build script in the top-level `package.json` runs `cd buying-frontend/ && npm run build` — treat that script as legacy or update it when changing CI/CD.
  - Database is configured from environment variables (`env.db()`); local development will typically use `DATABASE_URL` or values in `.env`. Production `settings_heroku.py` contains a sample local DB config but still relies on env values (and uses `django_heroku`).
  - CORS origins are small and explicit in `depotcommun/settings.py` — update when testing a frontend on a different port.

4) Project-specific patterns to follow (examples)
  - API: use `ninja` ModelSchema + `@api.get` / `@api.post` patterns (see `depotcommun/api.py` for `ArticleSchema`, `ShoppingBasketIn`). When returning model querysets, return ORM QuerySets directly (ninja will serialize them if a response schema is set).
  - Admin + PDF generation: invoice and article PDFs are in `invoice_pdf.py` and `articles_pdf.py` and are exposed via views in `depotcommun/views.py`. Keep heavy CPU tasks out of request critical path if possible.
  - Example management commands: `depotcommun/management/commands/createexampledata.py` — use this to seed dev databases.

5) Files to reference when making changes
  - Backend: `depotcommun/settings.py`, `depotcommun/settings_heroku.py`, `depotcommun/urls.py`, `depotcommun/api.py`, `depotcommun/models.py`, `manage.py`.
  - Deployment: `Procfile`, top-level `package.json`, `requirements.txt`, `Pipfile`.
  - Frontend: `frontend/depot-app/package.json`, `frontend-solid/depot-app/package.json`, `frontend/*/src`.

6) Example edits & quick examples
  - Add an API route: mirror `depotcommun/api.py` style — declare a `Schema`/`ModelSchema`, then `@api.get('/path', response=...)` or `@api.post('/path')` and add the function.
  - Fix missing `buying-frontend` build references: either
    - Update `depotcommun/settings.py` to point to `frontend/depot-app/dist` (or `build`) after you run the frontend build, or
    - Add a build job that outputs into `buying-frontend/build` (easier short-term) and update `heroku-prebuild` accordingly.

7) When to ask a human
  - If changes affect deployment (Procfile, heroku scripts, or build output locations) — confirm with the repo owner before altering production paths.
  - If you need secrets or the `.env` contents — do not attempt to infer secrets; request an explicit values file or CI secrets.

If anything here is unclear or you'd like me to include more specific commands (PowerShell-ready scripts, example `.env` variables, or a CI snippet), tell me what to add and I'll iterate.
