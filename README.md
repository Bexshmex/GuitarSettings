# ToneVault

ToneVault is my Django project for saving and sharing guitar amp presets.

The idea is simple: a user picks a band and song, adds the amp model, and
saves settings like gain, bass, mid, treble, and reverb. Users can also upload
an audio demo and download a preset as a text file.

## Features

- User registration and login
- List of presets with band filter and text search
- Add, edit, and delete presets (only the author or a superuser)
- Preset detail page with audio demo
- Download preset settings as `.txt`
- Management command with demo data

## How it is built

- Django 5.2, function-based views
- Served with gunicorn in Docker
- PostgreSQL in Docker (SQLite when running without Docker)
- Static files served by WhiteNoise
- Settings come from environment variables

## Run with Docker

```bash
docker compose up --build
```

Then open http://localhost:8000.

Migrations run automatically when the web container starts. Useful commands:

```bash
# run migrations by hand
docker compose run --rm web python manage.py migrate

# create an admin user
docker compose run --rm web python manage.py createsuperuser

# load demo data
docker compose run --rm web python manage.py seed_data
```

Demo login after seeding: username `demo`, password `demo12345`.

## Environment variables

Copy `.env.example` to `.env` if you want to change anything. Everything has
a working default for local use.

- `DJANGO_SECRET_KEY` - set a real random value in production
- `DJANGO_DEBUG` - `True` or `False`
- `DJANGO_ALLOWED_HOSTS` - comma-separated hostnames
- `DJANGO_CSRF_TRUSTED_ORIGINS` - comma-separated origins
- `DJANGO_SECURE_SSL` - set `True` only when the site runs behind HTTPS
- `DATABASE_URL` - PostgreSQL connection; if unset, SQLite is used

## Run without Docker

Recommended local Python version: 3.12 (same as the Docker image).

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Without `DATABASE_URL` the app uses a local `db.sqlite3` file.

## Notes

- Uploaded media is stored in a Docker volume and served by Django itself.
  That is enough for this project; a real deployment would use nginx or
  object storage.
- Static files are collected into the image at build time.

## About

I made this project to practice Django models, views, templates, forms,
authentication, file uploads, and a basic Docker deployment setup.
