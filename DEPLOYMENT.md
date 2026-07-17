git init# Safe Deployment Notes

This project is already structured for deployment with Gunicorn and a `Procfile`.

## Safe deployment approach

1. Keep the current local XAMPP installation as-is.
2. Use a separate deployment copy or deployment branch for the public host.
3. Point the deployed app to a separate external MySQL database using environment variables.
4. Do not overwrite the existing local database or local Apache/XAMPP configuration.

## Environment variables required by the app

- `APP_PREFIX`
- `SECRET_KEY`
- `LOGIN_PASSWORD`
- `FLASK_DEBUG`
- `USE_MYSQL`
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

A ready-to-copy template is available in `.env.example`.

## Recommended external host flow

- Host the Flask application on a free PaaS such as Render.
- Use a separate external MySQL-compatible database provider.
- Set the host database connection variables from the platform environment settings.
- Leave the local root path and MySQL defaults unchanged for the existing system.

## Important

The app already supports a root-hosted prefix by default and keeps compatibility with older `/prediction_system` links. That means the public deployment can be isolated cleanly from the current local setup.
